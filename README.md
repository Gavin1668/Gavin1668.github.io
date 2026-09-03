# Gavin's Blog

基于 [Hugo](https://gohugo.io/) + [hugo-theme-stack](https://github.com/CaiJimmy/hugo-theme-stack) 构建的个人主页，托管于 GitHub Pages。包含四大板块：**个人展示 / 作品集 / 随笔 / 网页工具**。

## 技术栈

- **Hugo Extended** v0.145.0 — 静态站点生成器
- **hugo-theme-stack** — 卡片式主题（自定义 fork）
- **GitHub Pages** — 托管
- **GitHub Actions** — 自动部署 + 每日日报自动生成 + 每日信息源抓取
- **GoatCounter** — 轻量隐私统计

## 本地开发

```bash
# 1. 克隆主题（首次）
npm run theme

# 2. 启动开发服务器
npm run dev
# 或直接
hugo server -D

# 3. 构建生产版本
npm run build
# 或
hugo --minify
```

## 目录结构

```
├── archetypes/       # 文章模板
├── assets/           # Hugo Pipes 处理的资源（CSS、图片）
├── content/          # 内容
│   ├── post/         # 博客文章（技术）
│   ├── essay/        # 随笔
│   ├── portfolio/    # 作品集（每个子目录一个项目）
│   ├── daily/        # 每日日报（自动生成）
│   ├── page/         # 独立页面（关于、归档、搜索、工具中心）
│   └── recommended/  # 推荐页
├── data/             # 数据文件
│   ├── github_trending.json  # GitHub Trending Top 10（每日自动抓取）
│   └── news.json             # 民生热点 Top 5（每日自动抓取）
├── layouts/          # 自定义布局（覆盖主题）
│   ├── _default/baseof.html  # 全站顶部导航栏
│   ├── portfolio/list.html   # 作品集卡片网格
│   └── page/tools.html       # 工具中心卡片
├── static/           # 静态资源（工具页面、robots.txt 等）
├── scripts/          # 自动化脚本
│   ├── gen_daily.py          # 每日 RSS 日报生成
│   └── fetch_sources.sh      # 每日信息源拉取（Trending + 民生热点）
├── .github/workflows/
│   ├── deploy.yml    # 部署到 GitHub Pages（含每日 08:00 信息源定时任务）
│   └── daily.yml     # 每日自动生成日报
└── hugo.yaml         # Hugo 配置（含首页 Hero 参数、timeZone）
```

## 常用操作

**新增随笔/文章**：在 `content/essay/` 或 `content/post/` 下新建 `xxx/index.md`，改 `draft: false` 后 push 即自动部署。

**新增作品**：在 `content/portfolio/` 下新建目录 + `index.md`（含 `icon`、`link`、`tags` 字段），作品集会以卡片形式自动展示。

**新增网页工具**：把静态 HTML 放入 `static/tools/`，再在 `content/page/tools/index.md` 的 `tools` 列表追加一条即可。

**修改首页展示**：`hugo.yaml` 的 `params.hero` 控制首页姓名、职位、技能标签等。

## 自动日报

每天北京时间 07:00，GitHub Actions 自动抓取少数派、V2EX、Hacker News、掘金的 RSS，生成日报并推送，随后自动部署。

## 每日信息源

每天北京时间 08:00，`deploy.yml` 定时运行 `scripts/fetch_sources.sh`：

- 抓取 **GitHub Trending Top 10**（近 7 天新建、按 star 排序，GitHub Search API）；
- 抓取**每日民生热点 Top 5**（中国新闻网社会频道 RSS，可在 `hugo.yaml` 的 `newsSourceUrl` 替换源）；
- 写入 `data/github_trending.json` 与 `data/news.json` 并提交，随后用最新数据重新构建部署。

首页「每日民生热点」「GitHub Trending」两张卡片即读取上述数据渲染，信息源开关与条数可在 `hugo.yaml` 的 `params` 中调整（`enableNewsSource`、`enableTrendingSource`、`newsLimit`、`trendingLimit`）。

## 写作

```bash
# 新建文章
hugo new post/my-post/index.md

# 新建独立页面
hugo new page/my-page/index.md
```

写完后将 `draft: true` 改为 `false`，push 到 main 分支即自动部署。
