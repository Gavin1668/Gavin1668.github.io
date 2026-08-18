#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""每日自动抓取公开 RSS 源，生成一篇日报到 content/daily/YYYY-MM-DD.md。

改进点：
- 跨源去重（标题相似度）
- 更干净的摘要清洗（移除图片链接、多余空白、HTML 残留）
- 自动生成 description 用于 SEO
- 网络请求带重试
- 仅用 Python 标准库，确保在 GitHub Actions runner 上可直接运行
"""
import datetime
import html
import os
import re
import time
import urllib.request
import xml.etree.ElementTree as ET

SOURCES = [
    ("少数派", "https://sspai.com/feed"),
    ("V2EX", "https://www.v2ex.com/index.xml"),
    ("Hacker News", "https://hnrss.org/frontpage"),
    ("掘金", "https://rsshub.app/juejin/category/frontend"),
]

OUT_DIR = "content/daily"
ATOM = "{http://www.w3.org/2005/Atom}"
MAX_PER_SOURCE = 4
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
    # 移除 HTML 标签
    text = re.sub(r"<[^>]+>", "", text)
    # 移除常见的 "查看全文"、"Article URL:" 等残留
    text = re.sub(r"查看全文.*$", "", text)
    text = re.sub(r"Article URL:.*$", "", text, flags=re.IGNORECASE)
    text = re.sub(r"Comments URL:.*$", "", text, flags=re.IGNORECASE)
    # 移除图片 URL 残留
    text = re.sub(r"https?://\S+\.(?:png|jpg|jpeg|gif|webp|svg)\S*", "", text)
    # HTML 实体解码
    text = html.unescape(text)
    # 合并空白
    text = re.sub(r"\s+", " ", text).strip()
    # 智能截断：优先在标点处断
    if len(text) > MAX_SUMMARY:
        cut = text[:MAX_SUMMARY]
        # 尝试在最近的句号/问号/感叹号处断
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
    # RSS 2.0
    for item in root.iter("item"):
        title = (item.findtext("title") or "").strip()
        link = (item.findtext("link") or "").strip()
        desc = clean_summary(item.findtext("description") or "")
        if title:
            yield title, link, desc
    # Atom
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
    today = datetime.date.today()
    os.makedirs(OUT_DIR, exist_ok=True)
    out_file = os.path.join(OUT_DIR, today.strftime("%Y-%m-%d.md"))

    seen_titles = set()
    all_items = []  # (source, title, link, desc)

    for name, url in SOURCES:
        try:
            data = fetch(url)
            items = list(parse_items(data))
        except Exception as exc:  # noqa: BLE001
            all_items.append((name, None, None, f"抓取失败：{exc}"))
            continue

        count = 0
        for title, link, desc in items:
            if count >= MAX_PER_SOURCE:
                break
            norm = normalize_title(title)
            if norm in seen_titles:
                continue
            seen_titles.add(norm)
            all_items.append((name, title, link, desc))
            count += 1

    # 生成 description（取前几条标题拼接）
    titles_for_desc = [t for _, t, _, _ in all_items if t][:3]
    description = (
        f"{today.strftime('%Y-%m-%d')} 日报：" + "；".join(titles_for_desc) + "。"
        if titles_for_desc
        else f"{today.strftime('%Y-%m-%d')} 技术与生活资讯日报。"
    )

    lines = [
        "---",
        f'title: "{today.strftime("%Y-%m-%d")} 日报"',
        f'date: {today.isoformat()}T08:00:00+08:00',
        f'slug: "{today.strftime("%Y-%m-%d")}"',
        f'description: "{description}"',
        "categories:",
        "  - 日报",
        "tags:",
        "  - 日报",
        "  - 每日资讯",
        "draft: false",
        "---",
        "",
        f"自动聚合于 {today.strftime('%Y-%m-%d')}。以下为今日抓取的技术与生活资讯：",
        "",
    ]

    current_source = None
    for source, title, link, desc in all_items:
        if source != current_source:
            current_source = source
            lines.append(f"\n## {source}\n")
        if title is None:
            # 抓取失败
            lines.append(f"\n> {desc}\n")
            continue
        line = f"- [{title}]({link})"
        if desc:
            line += f" — {desc}"
        lines.append(line)

    lines.append("\n\n---\n")
    lines.append(
        "\n*本日报由 GitHub Actions 每日自动生成，内容来自公开 RSS 源，仅供参考。*\n"
    )

    with open(out_file, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))
    print(f"written: {out_file}")


if __name__ == "__main__":
    main()
