#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""抓取 chenshaowen.com/trending 的构建期快照，生成热榜 JSON。

- 输出 data/daily/<date>.json，供 layouts/daily/single.html（版本 D）渲染
- 日期口径与 gen_daily.py 一致：北京时间当天
- 仅用标准库；单源失败不阻塞，错误记录在 errors 字段
"""
import json
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

CST = timezone(timedelta(hours=8))
ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "data" / "daily"

# key 是趋势大盘的 board id（完整清单见其 assets/boards.js，共 39 个可选）
# span: 2 = 双列宽卡, 1 = 普通卡；grad = 卡片图标渐变色
BOARDS = [
    {"key": "itzhijia", "name": None, "en": "ITHOME",   "span": 2, "grad": "linear-gradient(135deg,#7a96ff,#3d5bff)"},
    {"key": "juejin",   "name": None, "en": "JUEJIN",   "span": 1, "grad": "linear-gradient(135deg,#12b58f,#0a8f70)"},
    {"key": "weibo",    "name": None, "en": "WEIBO",    "span": 1, "grad": "linear-gradient(135deg,#ff8a5c,#e0563f)"},
    {"key": "zhihu",    "name": None, "en": "ZHIHU",    "span": 1, "grad": "linear-gradient(135deg,#5c9dff,#2f6bff)"},
    {"key": "bilibili", "name": None, "en": "BILIBILI", "span": 1, "grad": "linear-gradient(135deg,#ff9ec2,#e0568f)"},
    {"key": "douban",   "name": None, "en": "DOUBAN",   "span": 2, "grad": "linear-gradient(135deg,#3ecfae,#12b58f)"},
]
TOP_N = 10

# 不宜在日报展示的关键词，按需增删
BLOCK = [
    "黄之锋", "特朗普", "中期选举", "弹劾", "参众两院", "以色列", "翻红", "翻蓝", "选举",
    "刑案", "搜捕", "卖淫", "厕所被拍", "缅甸", "遗书", "去世", "卵巢癌",
]


def fetch_json(url: str):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (daily-bot)"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))


def trending_board(key: str, n: int):
    """取一个榜，自动带 ?v= 时间戳穿透 CDN 缓存。"""
    v = int(datetime.now().timestamp() * 1000)
    d = fetch_json(f"https://www.chenshaowen.com/trending/assets/data/{key}.json?v={v}")
    items = []
    for it in d.get("items", []):
        title = it.get("title", "")
        if any(b in title for b in BLOCK):
            continue
        items.append({
            "title": title,
            "url": it.get("url", ""),
            "extra": str(it.get("extra") or ""),
        })
        if len(items) >= n:
            break
    return items, d.get("fetchedAt", ""), d.get("name", key)


def main():
    today = datetime.now(CST).date()
    date_str = today.strftime("%Y-%m-%d")
    boards, errors = [], []
    for cfg in BOARDS:
        try:
            items, fetched, name = trending_board(cfg["key"], TOP_N)
        except Exception as exc:  # noqa: BLE001
            errors.append(f"{cfg['key']}：{exc}")
            continue
        boards.append({**cfg, "name": name, "items": items, "fetched": fetched[:10]})

    payload = {
        "date": date_str,
        "generatedAt": datetime.now(CST).isoformat(timespec="seconds"),
        "week": ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"][today.weekday()],
        "boards": boards,
        "errors": errors,
    }
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out_file = OUT_DIR / f"{date_str}.json"
    out_file.write_text(
        json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8"
    )
    n_items = sum(len(b["items"]) for b in boards)
    print(f"written: {out_file} boards={len(boards)} items={n_items} errors={errors}")


if __name__ == "__main__":
    main()
