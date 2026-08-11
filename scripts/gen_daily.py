#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""每日自动抓取公开 RSS 源，生成一篇日报到 content/daily/YYYY-MM-DD.md。
无第三方依赖，仅用 Python 标准库，确保在 GitHub Actions runner 上可直接运行。
"""
import datetime
import html
import os
import re
import urllib.request
import xml.etree.ElementTree as ET

SOURCES = [
    ("少数派", "https://sspai.com/feed"),
    ("V2EX", "https://www.v2ex.com/index.xml"),
    ("Hacker News", "https://hnrss.org/frontpage"),
]

OUT_DIR = "content/daily"
ATOM = "{http://www.w3.org/2005/Atom}"


def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (daily-bot)"})
    with urllib.request.urlopen(req, timeout=25) as resp:
        return resp.read()


def strip_tags(text: str) -> str:
    if not text:
        return ""
    text = re.sub(r"<[^>]+>", "", text)
    return html.unescape(text).strip()


def parse_items(xml_bytes: bytes):
    root = ET.fromstring(xml_bytes)
    # RSS 2.0
    for item in root.iter("item"):
        title = (item.findtext("title") or "").strip()
        link = (item.findtext("link") or "").strip()
        desc = strip_tags(item.findtext("description") or "")
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
        desc = strip_tags(
            (entry.findtext(f"{ATOM}summary") or entry.findtext(f"{ATOM}content") or "")
        )
        if title:
            yield title, link, desc


def main() -> None:
    today = datetime.date.today()
    os.makedirs(OUT_DIR, exist_ok=True)
    out_file = os.path.join(OUT_DIR, today.strftime("%Y-%m-%d.md"))

    lines = [
        "---",
        f'title: "{today.strftime("%Y-%m-%d")} 日报"',
        f'date: {today.isoformat()}T08:00:00+08:00',
        f'slug: "{today.strftime("%Y-%m-%d")}"',
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

    for name, url in SOURCES:
        try:
            data = fetch(url)
            items = list(parse_items(data))[:4]
        except Exception as exc:  # noqa: BLE001
            lines.append(f"\n## {name}\n")
            lines.append(f"\n> 抓取失败：{exc}\n")
            continue
        lines.append(f"\n## {name}\n")
        if not items:
            lines.append("\n> 暂无可抓取内容。\n")
        for title, link, desc in items:
            desc = desc[:80]
            line = f"- [{title}]({link})"
            if desc:
                line += f" — {desc}"
            lines.append(line)

    lines.append("\n\n---\n")
    lines.append("\n*本日报由 GitHub Actions 每日自动生成，内容来自公开 RSS 源，仅供参考。*\n")

    with open(out_file, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))
    print(f"written: {out_file}")


if __name__ == "__main__":
    main()
