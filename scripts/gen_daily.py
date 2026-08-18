#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""每日自动抓取公开 RSS 源，生成「每日热点 Top 10」日报。

- 多源混合，跨源去重
- 统一取前 10 条，按来源标注
- 自动生成 description 用于 SEO
- 仅用 Python 标准库，确保在 GitHub Actions runner 上可直接运行
"""
import datetime
import html
import os
import re
import time
import urllib.request
import xml.etree.ElementTree as ET

# 北京时间 UTC+8
CST = datetime.timezone(datetime.timedelta(hours=8))

SOURCES = [
    ("少数派", "https://sspai.com/feed"),
    ("V2EX", "https://www.v2ex.com/index.xml"),
    ("Hacker News", "https://hnrss.org/frontpage"),
    ("掘金", "https://rsshub.app/juejin/category/frontend"),
    ("InfoQ", "https://www.infoq.cn/feed"),
]

OUT_DIR = "content/daily"
ATOM = "{http://www.w3.org/2005/Atom}"
TOP_N = 10
MAX_SUMMARY = 100


def fetch(url: str, retries: int = 2) -> bytes:
    """带重试的 HTTP 请求。"""
    last_exc = None
    for attempt in range(retries + 1):
        try:
            req = urllib.request.Request(
                url, headers={"User-Agent": "Mozilla/5.0 (daily-bot)"}
            )
            with urllib.request.urlopen(req, timeout=20) as resp:
                return resp.read()
        except Exception as exc:  # noqa: BLE001
            last_exc = exc
            if attempt < retries:
                time.sleep(2 * (attempt + 1))
    raise last_exc  # type: ignore[misc]


def clean_summary(text: str) -> str:
    """清理 RSS 摘要：移除标签、图片链接、多余空白，截断到合理长度。"""
    if not text:
        return ""
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"查看全文.*$", "", text)
    text = re.sub(r"Article URL:.*$", "", text, flags=re.IGNORECASE)
    text = re.sub(r"Comments URL:.*$", "", text, flags=re.IGNORECASE)
    text = re.sub(r"https?://\S+\.(?:png|jpg|jpeg|gif|webp|svg)\S*", "", text)
    text = html.unescape(text)
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) > MAX_SUMMARY:
        cut = text[:MAX_SUMMARY]
        for sep in ("。", "！", "？", ".", "!", "?"):
            idx = cut.rfind(sep)
            if idx > MAX_SUMMARY // 2:
                text = cut[: idx + 1]
                break
        else:
            text = cut + "…"
    return text


def parse_items(xml_bytes: bytes):
    """解析 RSS 2.0 和 Atom 格式。"""
    root = ET.fromstring(xml_bytes)
    for item in root.iter("item"):
        title = (item.findtext("title") or "").strip()
        link = (item.findtext("link") or "").strip()
        desc = clean_summary(item.findtext("description") or "")
        if title:
            yield title, link, desc
    for entry in root.iter(f"{ATOM}entry"):
        title = (entry.findtext(f"{ATOM}title") or "").strip()
        link = ""
        for link_el in entry.findall(f"{ATOM}link"):
            link = link_el.get("href", "")
            if link:
                break
        desc = clean_summary(
            entry.findtext(f"{ATOM}summary")
            or entry.findtext(f"{ATOM}content")
            or ""
        )
        if title:
            yield title, link, desc


def normalize_title(title: str) -> str:
    """标题归一化，用于去重比较。"""
    title = re.sub(r"[\[\]【】\s]", "", title)
    return title.lower()


def main() -> None:
    today = datetime.datetime.now(CST).date()
    os.makedirs(OUT_DIR, exist_ok=True)
    out_file = os.path.join(OUT_DIR, today.strftime("%Y-%m-%d.md"))

    seen_titles = set()
    all_items = []  # (source, title, link, desc)
    fetch_errors = []

    for name, url in SOURCES:
        try:
            data = fetch(url)
            items = list(parse_items(data))
        except Exception as exc:  # noqa: BLE001
            fetch_errors.append(f"{name}：{exc}")
            continue

        for title, link, desc in items:
            norm = normalize_title(title)
            if norm in seen_titles:
                continue
            seen_titles.add(norm)
            all_items.append((name, title, link, desc))

    # 取前 Top_N 条
    top_items = all_items[:TOP_N]

    # 生成 description
    titles_for_desc = [t for _, t, _, _ in top_items[:3]]
    description = (
        f"{today.strftime('%Y-%m-%d')} 每日热点 Top 10："
        + "；".join(titles_for_desc)
        + "。"
        if titles_for_desc
        else f"{today.strftime('%Y-%m-%d')} 每日热点资讯。"
    )

    lines = [
        "---",
        f'title: "{today.strftime("%Y-%m-%d")} 每日热点 Top 10"',
        f'date: {today.isoformat()}T08:00:00+08:00',
        f'slug: "{today.strftime("%Y-%m-%d")}"',
        f'description: "{description}"',
        "categories:",
        "  - 日报",
        "tags:",
        "  - 日报",
        "  - 热点新闻",
        "draft: false",
        "---",
        "",
        f"自动聚合于 {today.strftime('%Y-%m-%d')}。今日热点 Top {len(top_items)}：",
        "",
    ]

    for idx, (source, title, link, desc) in enumerate(top_items, 1):
        line = f"{idx}. [{title}]({link}) `{source}`"
        if desc:
            line += f"\n   > {desc}"
        lines.append(line)
        lines.append("")

    if fetch_errors:
        lines.append("---")
        lines.append("")
        lines.append("**抓取失败的源：**")
        for err in fetch_errors:
            lines.append(f"- {err}")
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append(
        "*本日报由 GitHub Actions 每日自动生成，内容来自公开 RSS 源，仅供参考。*\n"
    )

    with open(out_file, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))
    print(f"written: {out_file} ({len(top_items)} items)")


if __name__ == "__main__":
    main()
