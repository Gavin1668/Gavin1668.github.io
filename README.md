# Gavin's Blog

基于 [Hugo](https://gohugo.io/) + [hugo-theme-stack](https://github.com/CaiJimmy/hugo-theme-stack) 构建的个人技术博客，托管于 GitHub Pages。

## 技术栈

- **Hugo Extended** v0.145.0 — 静态站点生成器
- **hugo-theme-stack** — 卡片式主题（自定义 fork）
- **GitHub Pages** — 托管
- **GitHub Actions** — 自动部署 + 每日日报自动生成
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
│   ├── post/         # 博客文章
│   ├── daily/        # 每日日报（自动生成）
│   ├── page/         # 独立页面（关于、归档、搜索）
│   └── recommended/  # 推荐页
├── layouts/          # 自定义布局（覆盖主题）
├── static/           # 静态资源（工具页面、robots.txt 等）
├── scripts/          # 自动化脚本
│   └── gen_daily.py  # 每日 RSS 日报生成
├── .github/workflows/
│   ├── deploy.yml    # 部署到 GitHub Pages
│   └── daily.yml     # 每日自动生成日报
└── hugo.yaml         # Hugo 配置
```

## 自动日报

每天北京时间 07:00，GitHub Actions 自动抓取少数派、V2EX、Hacker News、掘金的 RSS，生成日报并推送，随后自动部署。

## 写作

```bash
# 新建文章
hugo new post/my-post/index.md

# 新建独立页面
hugo new page/my-page/index.md
```

写完后将 `draft: true` 改为 `false`，push 到 main 分支即自动部署。
