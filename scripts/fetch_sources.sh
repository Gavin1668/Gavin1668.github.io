#!/usr/bin/env bash
# 每日信息源拉取：GitHub Trending + 民生热点 RSS
# 产物：data/github_trending.json、data/news.json
# 用法：由 .github/workflows/deploy.yml 的 schedule/workflow_dispatch 触发，
#       也可本地手动执行（本地执行只生成数据，不提交推送）
set -euo pipefail

DATA_DIR="data"
TMP_DIR="${TMPDIR:-/tmp}"
export TMP_DIR
mkdir -p "$DATA_DIR"

# ---------- 1. GitHub Trending Top 10 ----------
# GitHub Search API（可选 GH_TOKEN 防限流；匿名 60 次/小时）
GITHUB_API="https://api.github.com/search/repositories"
SINCE=$(date -u -d '7 days ago' +%Y-%m-%d)

curl -sS --max-time 30 -H "Accept: application/vnd.github+json" \
    ${GH_TOKEN:+-H "Authorization: Bearer $GH_TOKEN"} \
    -H "User-Agent: Gavin1668-portfolio" \
    "$GITHUB_API?q=created:>$SINCE&sort=stars&order=desc&per_page=10" \
    -o "$TMP_DIR/gh_raw.json"

python3 - "$DATA_DIR/github_trending.json" <<'EOF'
import json, os, sys
try:
    raw_path = os.path.join(os.environ.get('TMP_DIR', '/tmp'), 'gh_raw.json')
    raw = json.load(open(raw_path))
    items = raw.get('items', [])[:10]
except Exception:
    items = []
out = [{
    "rank": i + 1,
    "repo": it.get("full_name", ""),
    "lang": (it.get("language") or ""),
    "stars": it.get("stargazers_count", 0),
    "desc": (it.get("description") or "")[:80],
    "url": it.get("html_url", ""),
} for i, it in enumerate(items)]
json.dump(out, open(sys.argv[1], 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print(f"github_trending: {len(out)} items")
EOF

# ---------- 2. 民生热点 Top 5（RSS）----------
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

# ---------- 3. 提交并推送（仅 CI 环境执行）----------
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
