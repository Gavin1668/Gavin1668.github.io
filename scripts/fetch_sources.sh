#!/usr/bin/env bash
# 每日信息源拉取：民生热点 RSS
# 产物：data/news.json
# 用法：由 .github/workflows/deploy.yml 的 schedule/workflow_dispatch 触发，
#       也可本地手动执行（本地执行只生成数据，不提交推送）
set -euo pipefail

DATA_DIR="data"
TMP_DIR="${TMPDIR:-/tmp}"
export TMP_DIR
mkdir -p "$DATA_DIR"

# ---------- 1. 民生热点 Top 5（RSS）----------
# 民生新闻 RSS 源：中国新闻网·社会新闻（稳定可用）
NEWS_RSS="${NEWS_RSS_URL:-https://www.chinanews.com.cn/rss/society.xml}"
curl -sSL --max-time 30 --compressed \
    -A "Mozilla/5.0 (compatible; Gavin1668-portfolio)" \
    "$NEWS_RSS" -o "$TMP_DIR/news.xml"

python3 - "$DATA_DIR/news.json" <<'EOF'
import json, os, sys
from xml.etree import ElementTree as ET
try:
    xml_path = os.path.join(os.environ.get('TMP_DIR', '/tmp'), 'news.xml')
    root = ET.parse(xml_path).getroot()
    items = []
    for item in root.iter('item'):
        title = (item.findtext('title') or '').strip()
        link = (item.findtext('link') or '').strip()
        date = (item.findtext('pubDate') or '').strip()
        if title:
            # pubDate 形如 "Sat, 22 Aug 2026 16:28:40 +0800"，取日期部分
            parts = date.split(' ')
            short = f"{parts[1]}-{parts[2]}" if len(parts) >= 3 else date[:16]
            items.append({"title": title, "url": link, "date": short})
        if len(items) >= 5:
            break
except Exception:
    items = []
json.dump(items, open(sys.argv[1], 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print(f"news: {len(items)} items")
EOF

# ---------- 2. 提交并推送（仅 CI 环境执行）----------
if [ "${CI:-}" = "true" ]; then
    git config user.name "github-actions[bot]"
    git config user.email "github-actions[bot]@users.noreply.github.com"
    git add "$DATA_DIR"
    if git diff --cached --quiet; then
        echo "No data changes"
    else
        git commit -m "chore: daily sources update $(date +%F)"
        git push
    fi
fi
