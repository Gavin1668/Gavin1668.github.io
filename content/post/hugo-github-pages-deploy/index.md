---
title: "Hugo + GitHub Pages 从零部署踩坑实录"
description: "记录从安装 Hugo、用 hugo-theme-stack 搭站，到通过 GitHub Pages 自动部署上线的完整流程，以及途中踩过的 baseurl、主题子模块、草稿不发布、404 样式丢失、自定义域名等真实坑。"
date: 2026-08-11
lastmod: 2026-08-11
categories:
  - 技术
tags:
  - Hugo
  - GitHub Pages
  - 静态博客
  - 部署
draft: false
---

这是我的第一篇"实战型"技术笔记。开博那篇《你好，世界！》只是个开始，这篇把**从零搭好一个 Hugo 博客并丢到 GitHub Pages 上自动部署**这条路上，我亲自踩过的坑都记下来，省得以后重蹈覆辙，也希望能帮到同样在折腾的你。

## 一、为什么选 Hugo + GitHub Pages

选型本身不纠结：

- **Hugo**：Go 写的静态站点生成器，构建速度极快（几千篇文章秒级），主题生态成熟。
- **GitHub Pages**：免费、稳定、自带 HTTPS，配合 GitHub Actions 能实现 push 即部署。
- **hugo-theme-stack**：颜值在线、自带暗色模式、搜索、归档、RSS，几乎是开箱即用。

组合下来：**零成本 + 高稳定 + 自己完全掌控内容**，对个人技术博客非常合适。

## 二、本地安装与环境

```bash
# macOS
brew install hugo

# Windows（已装 winget）
winget install Hugo.Hugo.Extended

# 验证
hugo version
```

> 坑 1：务必装 **Extended 版**。Stack 主题用到了 SCSS，标准版会在构建时报 `SASS/SCSS` 相关错误。Windows 上 `Hugo.Hugo.Extended` 就是扩展版。

初始化站点：

```bash
hugo new site myblog
cd myblog
git init
```

## 三、主题子模块（第一个隐形坑）

新手最容易卡在这里。很多人直接把主题文件复制进 `themes/`，结果以后没法更新。正确做法是 **git submodule**：

```bash
git submodule add https://github.com/CaiJimmy/hugo-theme-stack.git themes/hugo-theme-stack
```

> 坑 2：克隆仓库时如果不带 `--recurse-submodules`，本地是没有主题目录的，构建会报 `module "hugo-theme-stack" not found`。
>
> ```bash
> git clone --recurse-submodules <你的仓库地址>
> ```

在 `hugo.yaml`（或 `config.toml`）里指定主题：

```yaml
theme: hugo-theme-stack
```

## 四、本地预览：草稿看不见？

写完第一篇文章：

```bash
hugo new post/hello-world/index.md
```

默认 `draft: true`，本地 `hugo server` 是**看不到草稿**的。要么把 front matter 的 `draft` 改成 `false`，要么用：

```bash
hugo server -D    # -D = 包含草稿
```

> 坑 3：改完 `draft: false` 准备发布，但本地一直 `hugo server` 看效果——注意 `hugo server` 是开发服务器，**不会生成 `public/` 目录**，真正部署用的是 `hugo` 这条构建命令。

## 五、推到 GitHub Pages（Actions 自动部署）

我用的方案是：**源码放 `main` 分支，GitHub Actions 构建后部署到 Pages**。仓库根目录放一个工作流文件 `.github/workflows/hugo.yaml`：

```yaml
name: Deploy Hugo site to Pages
on:
  push:
    branches: [main]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          submodules: recursive   # 关键：拉取主题子模块
          fetch-depth: 0
      - uses: peaceiris/actions-hugo@v3
        with:
          hugo-version: "latest"
          extended: true          # 关键：扩展版，否则 SCSS 报错
      - run: hugo --minify
      - uses: actions/upload-pages-artifact@v3
        with:
          path: ./public
      - uses: actions/deploy-pages@v4
```

在仓库 **Settings → Pages** 里把 Source 设为 `GitHub Actions` 即可。之后每次 push 到 `main` 都会自动构建部署。

## 六、部署后 404 / 样式全丢（最坑的一个）

这是出现频率最高的事故：**页面能打开，但 CSS/JS 全 404，整站裸奔**。

根因几乎都是 `baseURL` 不对。GitHub Pages 的访问地址分两种：

- 用户/组织页：`https://<用户名>.github.io/`（根路径）
- 项目页：`https://<用户名>.github.io/<仓库名>/`（带子路径）

对应配置：

```yaml
# 用户页
baseURL: "https://gavin1668.github.io/"

# 项目页（注意结尾斜杠和中间路径）
baseURL: "https://gavin1668.github.io/myblog/"
```

> 坑 4：**结尾一定要有斜杠**。漏掉会变成 `https://gavin1668.github.io/css/...` 拼错，资源全 404。
>
> 坑 5：如果你和我一样 `baseURL` 留空 `""`，Hugo 会用相对路径，用户页恰好能跑；但一旦将来绑定**自定义域名**，就必须改成绝对地址，否则分享链接和 sitemap 全错。

## 七、绑定自定义域名 + HTTPS

1. 在域名服务商处加一条 **CNAME 记录**，指向 `<用户名>.github.io`；
2. 仓库 Settings → Pages → Custom domain 填入你的域名；
3. Hugo 里把 `baseURL` 改成你的域名（带 `https://` 和结尾斜杠）；
4. 在仓库根目录（或 `static/`）放一个 `CNAME` 文件，内容就是你的域名，避免每次部署被清空；
5. GitHub 会自动签发 HTTPS 证书，等几分钟变绿即可。

> 坑 6：`CNAME` 文件要放进 `static/` 而不是仓库根，否则 Hugo 构建不会把它输出到 `public/` 根目录，下次部署就被覆盖了。

## 八、中文内容专属注意点

```yaml
hasCJKLanguage: true        # 正确统计中文阅读时长、分词
DefaultContentLanguage: zh-cn
languageCode: zh-cn
```

> 坑 7：不设 `hasCJKLanguage: true`，"阅读约 3 分钟"会变成"阅读约 0 分钟"。
>
> 坑 8：URL 里带中文（slug 用中文）在部分环境下会乱码。建议 slug 用英文/拼音，正文标题用中文，由 `permalinks` 控制路径：
>
> ```yaml
> permalinks:
>   post: /p/:slug/
> ```

## 九、常见报错速查表

| 现象 | 原因 | 解法 |
|---|---|---|
| `module not found` | 主题子模块没拉 | `git submodule update --init --recursive` |
| SCSS 编译失败 | 用了标准版 Hugo | 换 Extended 版 |
| 本地能看到、线上 404 | `baseURL` 缺结尾斜杠 | 补全 `https://域名/` |
| 草稿线上不显示 | 忘了 `-D` / `draft` 没改 | 发布前设 `draft: false` |
| 部署后样式丢 | Actions 没拉子模块 | workflow 加 `submodules: recursive` |
| 阅读时长 0 分钟 | 未开 `hasCJKLanguage` | 配置里打开 |

## 十、小结

整套流程真正卡人的就几处：**主题用 submodule 管理、Actions 要拉子模块且用扩展版、baseURL 结尾斜杠、CNAME 放 static/**。把这四条记住，基本一路绿灯。

博客只是工具，内容是长久的事。接下来我打算把"主题配置完全指南""站内搜索与 RSS"也写成系列，把这套栈彻底吃透。

如果你也在折腾 Hugo，欢迎在 GitHub 上交流，或者订阅本站的 RSS —— 统计我已经接好了，你的每一次访问我都能看到 😉
