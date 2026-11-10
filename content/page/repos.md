---
title: 开源资源合集
slug: repos
layout: repos
description: "收集一批可以反复查阅的开源资料：过日子的生活指南、找工作的避坑清单、人际与情感的场景手册、学习与理财的入门读本，再加上开发者常用的免费 API、无头浏览器和本地 AI 工具。"
notice: "GitHub 直连经常打不开。每张卡片备了 jsDelivr 文本和 gh-proxy 备用两个入口，按「文本 → 备用」换着点。文本是仓库 README 的纯文本版，能读文字，看不到图片和子页面。"
date: 2026-11-10
draft: false
menu:
  main:
    name: 资源合集
    weight: 6
    params:
      icon: bookmark
repo_groups:
  - title: 过日子
    note: 生活、健康、吃饭、住房
    items:
      - name: 高性价比人生指南
        star: "7 万+"
        tag: 生活指南
        desc: 767 条生活建议，租房、突然失业、给家里备应急物资都能查到；还讲安全习惯、疫苗建议、身体预警信号和消费避坑。租房与买房单独成章，押金、返还时间、扣减情形都写明了要确认什么。
        short: "767 条建议，安全健康、省钱、应急物资、租房"
        url: https://github.com/eternity4719/HowToLiveBetter
        raw: https://cdn.jsdelivr.net/gh/eternity4719/HowToLiveBetter@main/README.md
        raw2: https://gh-proxy.com/https://raw.githubusercontent.com/eternity4719/HowToLiveBetter/main/README.md
        points:
          - 767 条生活建议，遇到具体问题按需查：租房、失业、应急物资
          - 讲意外伤害防护、基础疫苗、身体预警信号
          - 教省钱避坑，别买彩票、少踩厂商套路
      - name: 程序员延寿指南
        star: "3 万+"
        tag: 健康科学
        desc: 把饮食、运动、睡眠的研究整理成 64 条建议，每条附论文出处、适用人群与局限，还带一个可溯源的 AI Skill。
        short: "64 条带论文出处的健康建议，附 AI Skill"
        url: https://github.com/geekan/HowToLiveLonger
        raw: https://cdn.jsdelivr.net/gh/geekan/HowToLiveLonger@main/README.md
        raw2: https://gh-proxy.com/https://raw.githubusercontent.com/geekan/HowToLiveLonger/main/README.md
        points:
          - 64 条饮食、运动、睡眠建议，每条附论文出处
          - 标注适用人群与局限，避免断章取义
          - 附带 AI Skill，可按你的记录查证并给来源
      - name: 程序员做饭指南 HowToCook
        star: "10 万+"
        tag: 菜谱厨房
        desc: 用明确的原料、用量和步骤讲常见菜，素菜、荤菜、主食、早餐都分好类，连厨房准备和刷碗都有指导。
        short: "精确用料、分步菜谱，厨房基础全覆盖"
        url: https://github.com/Anduin2017/HowToCook
        raw: https://cdn.jsdelivr.net/gh/Anduin2017/HowToCook@master/README.md
        raw2: https://gh-proxy.com/https://raw.githubusercontent.com/Anduin2017/HowToCook/master/README.md
        points:
          - 按份数算原料用量，步骤细到先炒蛋、盛出、再炒番茄
          - 素菜 / 荤菜 / 主食 / 早餐分类，按类找菜
          - 附厨房准备、工具用法、刷碗等基础指导
      - name: 买房实战功课
        star: "2.6 万+"
        tag: 住房买房
        desc: 2017 年杭州买房过程整理出来的功课，从看房、查购房资格、算税费到签约过户一步步讲。政策条款已经过时，流程和要提前问清的问题仍然有用。
        short: "买房流程、资格税费、签约过户功课"
        url: https://github.com/houshanren/hangzhou_house_knowledge
        raw: https://cdn.jsdelivr.net/gh/houshanren/hangzhou_house_knowledge@master/README.md
        raw2: https://gh-proxy.com/https://raw.githubusercontent.com/houshanren/hangzhou_house_knowledge/master/README.md
        points:
          - 从看房、查购房资格到算税费的完整功课
          - 讲签约、贷款、过户这些环节要确认的细节
          - 2017 年杭州案例，政策已变，流程思路仍可参考
      - name: 租房避坑清单
        star: "—"
        tag: 租房要点
        desc: 从《高性价比人生指南》第 15 章整理出的租房要点。押金、中介代收款、断水断电逼搬、隔断房这几处最容易亏钱，每条都能回到原文的法规出处。
        short: "押金、中介、断水断电、隔断房四处要点"
        url: https://github.com/eternity4719/HowToLiveBetter/blob/main/book/15-%E7%A7%9F%E6%88%BF%E4%B8%8E%E4%B9%B0%E6%88%BF.md
        raw: https://cdn.jsdelivr.net/gh/eternity4719/HowToLiveBetter@main/book/15-%E7%A7%9F%E6%88%BF%E4%B8%8E%E4%B9%B0%E6%88%BF.md
        raw2: https://gh-proxy.com/https://raw.githubusercontent.com/eternity4719/HowToLiveBetter/main/book/15-%E7%A7%9F%E6%88%BF%E4%B8%8E%E4%B9%B0%E6%88%BF.md
        points:
          - 押金的数额、退还时间、扣减情形写进合同；合同没写的情形，房东无正当理由不能扣
          - 中介不得代收代付租金押金，钱直接给房东；长租公寓先查资金监管账户，别一次付一年
          - 断水断电、换锁、上门威胁逼搬先报警留证；租期内房子被卖掉，租约照旧有效
  - title: 找工作与职场
    note: 面试、校招，签字之前先查一遍
    items:
      - name: 面试反问指南
        star: "1.8 万+"
        tag: 求职面试
        desc: 面试最后「你有什么想问的」这一环节的提问清单，按团队、职责、流程、技术、职业发展分组。用来判断岗位真实情况，也避开问了会减分的问题。
        short: "面试反问清单，判断岗位真实情况"
        url: https://github.com/perkfly/reverse-interview-zh
        raw: https://cdn.jsdelivr.net/gh/perkfly/reverse-interview-zh@master/README.md
        raw2: https://gh-proxy.com/https://raw.githubusercontent.com/perkfly/reverse-interview-zh/master/README.md
        points:
          - 按团队、职责、流程、技术、职业发展分组的提问清单
          - 用来判断加班情况、团队归属、成长空间
          - 也标注了哪些问题问出口会减分
      - name: 校招避雷清单
        star: "5 千+"
        tag: 求职避雷
        desc: 收集校招过程中毁约、虚假承诺、流程不规范的记录，签三方或接 offer 之前，可以先按公司名查一遍再决定。
        short: "校招污点记录，签三方前先查公司"
        url: https://github.com/ShameCom/ShameCom
        raw: https://cdn.jsdelivr.net/gh/ShameCom/ShameCom@main/README.md
        raw2: https://gh-proxy.com/https://raw.githubusercontent.com/ShameCom/ShameCom/main/README.md
        points:
          - 记录校招毁约、虚假承诺、流程不规范的公司与组织
          - 按公司名和事件检索，接 offer 前先查一遍
          - 内容是社区补充，看到记录建议自己再核实
  - title: 人际与关系
    note: 说话、借钱、感情拿不准的时候
    items:
      - name: 人情世故指南
        star: "—"
        tag: 人际社交
        desc: 写给大学生和职场新人的 10 章 77 条经验，校园合作、求助、职场沟通、朋友借钱都有场景分析和示例话术。
        short: "10 章 77 条，借钱、求助、职场沟通话术"
        url: https://github.com/kkk-bot/HowToGetAlong
        raw: https://cdn.jsdelivr.net/gh/kkk-bot/HowToGetAlong@main/README.md
        raw2: https://gh-proxy.com/https://raw.githubusercontent.com/kkk-bot/HowToGetAlong/main/README.md
        points:
          - 10 章 77 条，写给大学生和职场新人
          - 校园合作、求助、职场沟通、朋友借钱都有场景分析
          - 每条含情境、考量、示例表达和可能代价
      - name: 狗头军师
        star: "—"
        tag: 情感分析
        desc: 一套恋爱关系分析的 AI Skill，可装进 Claude Code 或 Codex；导入聊天记录后先分清事实、推测和未知，再给回复建议和下一步行动。
        short: "导入聊天记录，分析关系并给回复建议"
        url: https://github.com/shengjidaguai-china/goutoujunshi
        raw: https://cdn.jsdelivr.net/gh/shengjidaguai-china/goutoujunshi@main/README.md
        raw2: https://gh-proxy.com/https://raw.githubusercontent.com/shengjidaguai-china/goutoujunshi/main/README.md
        points:
          - 装进 Claude Code / Codex 就能用的恋爱关系分析 Skill
          - 导入聊天记录后，先分清事实、推测和未知
          - 输出回复建议、下一步行动，以及该不该止损
  - title: 学习与理财
    note: 重新进入学习状态、补点金融常识
    items:
      - name: 人生进阶指南 up
        star: "7 万+"
        tag: 学习成长
        desc: 从英语学习起步，扩展到怎样借助 AI 学习、怎样做真实项目、生活节奏乱掉以后怎样重新开始。
        short: "英语学习 → AI 学习 → 项目复盘与重启"
        url: https://github.com/byoungd/up
        raw: https://cdn.jsdelivr.net/gh/byoungd/up@main/README.md
        raw2: https://gh-proxy.com/https://raw.githubusercontent.com/byoungd/up/main/README.md
        points:
          - 从英语词汇、语法、听说读写起步
          - 扩展到用 AI 学习、完成真实项目
          - 教记录水平和目标、留下作品与反馈、定期复盘重启
      - name: 初学者的投资指南
        star: "—"
        tag: 金融科普
        desc: 徐冲浪写的中文投资入门，不教怎么赚钱，只把美股交易时段、财报、估值、期权、波动率这些术语讲清楚。
        short: "美股、期权、财报等金融术语词条科普"
        url: https://github.com/xuchonglang/investing-for-beginners
        raw: https://cdn.jsdelivr.net/gh/xuchonglang/investing-for-beginners@main/README.md
        raw2: https://gh-proxy.com/https://raw.githubusercontent.com/xuchonglang/investing-for-beginners/main/README.md
        points:
          - 中文金融术语词条，先看懂名词到底什么意思
          - 覆盖美股交易时段、下单、财报、估值、风险
          - 期权部分讲收益结构、时间损耗、波动率
  - title: AI 与开发
    note: 免费 API、无头浏览器、Agent 工具
    items:
      - name: Public APIs
        star: "49.7 万"
        tag: 数据与 API
        desc: 社区维护的免费 API 目录，按天气、图书、地理、开发工具等分类整理。每个接口都标了用途、认证方式、是否支持 HTTPS 和浏览器跨站调用，再附服务文档。有网页检索入口，能按分类和条件筛。
        short: "49.7 万 star 的免费 API 目录，按类查接口"
        url: https://github.com/public-apis/public-apis
        raw: https://cdn.jsdelivr.net/gh/public-apis/public-apis@master/README.md
        raw2: https://gh-proxy.com/https://raw.githubusercontent.com/public-apis/public-apis/master/README.md
        points:
          - 按天气、图书、地理、开发工具等分类，每项附服务文档
          - 标注认证方式、HTTPS、浏览器跨站调用支持情况
          - 有网页入口，可按分类和条件筛选
      - name: Lightpanda
        star: "4.1 万"
        tag: 无头浏览器
        desc: 给 AI 和自动化脚本用的无头浏览器，后台运行、不开窗口。能打开网页、跑页面脚本、读内容、点按钮、填表单。省掉了把网页绘制成画面的步骤，所以启动快、占内存少。已在用 Puppeteer、Playwright 的可以接过来执行它支持的操作。
        short: "快、省内存的无头浏览器，给 AI 和脚本用"
        url: https://github.com/lightpanda-io/browser
        raw: https://cdn.jsdelivr.net/gh/lightpanda-io/browser@main/README.md
        raw2: https://gh-proxy.com/https://raw.githubusercontent.com/lightpanda-io/browser/main/README.md
        points:
          - 无窗口后台运行，能开页、跑脚本、读内容、点按钮、填表单
          - 去掉画面渲染环节，启动快、内存占用低
          - 兼容 Puppeteer、Playwright 的部分操作
      - name: OpenMausBot
        star: "2 万"
        tag: AI Agent
        desc: Grok Bot 的开源替代。把 Agent 做成聊天软件里的联系人，分别设置职责和模型，单独聊或拉进同一个群组。已在本机登录的 Claude、Codex 能接进来，也能连 Gmail、GitHub。需要操作网页或桌面时，可以挂云端 Linux 电脑，支持屏幕预览和接管，要确认的步骤以审批卡片出现在聊天里。
        short: "Agent 做成联系人，群组自动分派任务"
        url: https://github.com/milind-soni/OpenMausBot
        raw: https://cdn.jsdelivr.net/gh/milind-soni/OpenMausBot@main/README.md
        raw2: https://gh-proxy.com/https://raw.githubusercontent.com/milind-soni/OpenMausBot/main/README.md
        points:
          - 每个 Bot 单独配职责、模型与服务，也可放进同一群组
          - 本机已登录的 Claude、Codex 可接入，也能连 Gmail、GitHub
          - 群组可设自动选回复者，聊天记录与配置存在本地
      - name: Claude Code Game Studios
        star: "3.7 万"
        tag: 游戏开发
        desc: 把游戏工作室的分工做成一套模板，49 个 Agent 角色配置加 72 套工作流 Skill，覆盖讨论玩法、拆任务、实现功能、查设计和代码到准备发布。设计、程序、美术、音频、测试各有职责，Godot、Unity、Unreal 都有对应专家配置。装好插件运行 /start，会按当前进度引导后续工作。
        short: "49 个角色加 72 套 Skill，一条链做游戏"
        url: https://github.com/Donchitos/Claude-Code-Game-Studios
        raw: https://cdn.jsdelivr.net/gh/Donchitos/Claude-Code-Game-Studios@main/README.md
        raw2: https://gh-proxy.com/https://raw.githubusercontent.com/Donchitos/Claude-Code-Game-Studios/main/README.md
        points:
          - 49 个 Agent 角色，设计、程序、美术、音频、测试分工明确
          - 72 套 Skill 覆盖玩法讨论、任务拆分、实现、评审、发布
          - Godot、Unity、Unreal 各有专家配置，小项目不必一开始上全套
      - name: FreeToken
        star: "1.7 万"
        tag: 本地推理
        desc: 面向消费级硬件的本地推理引擎，跑大型 MoE 模型。让显卡、CPU 和系统内存一起参与计算，用缓存减少模型数据的重复搬运，把显存之外的资源也用上。带桌面界面，能启动模型、聊天、调参数；也能通过兼容 OpenAI、Anthropic 的接口，把 Claude Code、Codex 接到自己的本地服务。
        short: "显卡加 CPU 加内存一起跑大型 MoE"
        url: https://github.com/FlashML-org/FreeToken
        raw: https://cdn.jsdelivr.net/gh/FlashML-org/FreeToken@main/README.md
        raw2: https://gh-proxy.com/https://raw.githubusercontent.com/FlashML-org/FreeToken/main/README.md
        points:
          - 显存、CPU、系统内存协同，缓存减少数据搬运
          - 自带桌面界面，可启动模型、聊天、调参数
          - 兼容 OpenAI、Anthropic 接口，能接 Claude Code、Codex
  - title: 本地小工具
    note: 装在本机，离线也能用
    items:
      - name: Handy
        star: "3.8 万"
        tag: 语音输入
        desc: 跨 Windows、macOS、Linux 的离线语音转文字。装好应用、下载模型后基础识别就在本机跑，不注册账号也不连云端。模型可选 Whisper、Parakeet 等，按语言和电脑配置调。按快捷键说话，文字直接落到光标位置。
        short: "离线语音转文字，按住快捷键就能写"
        url: https://github.com/cjpais/Handy
        raw: https://cdn.jsdelivr.net/gh/cjpais/Handy@main/README.md
        raw2: https://gh-proxy.com/https://raw.githubusercontent.com/cjpais/Handy/main/README.md
        points:
          - 支持 Windows、macOS、Linux，免注册账号
          - 模型可选 Whisper、Parakeet，按语言和配置调
          - 基础识别全程在本机跑，不连云端
      - name: hex
        star: "6 千"
        tag: 语音听写
        desc: 本地语音听写工具。把光标放到输入位置，按住快捷键讲话，松开后转写好的文字就落在光标处。基础听写用本机语音模型，不连云端。常用名字和术语容易错，比如 Claude 常被转成 Cloud，可以在里面设纠正词。
        short: "按住说话，松开就在光标处出字"
        url: https://github.com/anomalyco/hex
        raw: https://cdn.jsdelivr.net/gh/anomalyco/hex@dev/README.md
        raw2: https://gh-proxy.com/https://raw.githubusercontent.com/anomalyco/hex/dev/README.md
        points:
          - 支持 macOS、Windows、Linux，基础听写全离线
          - 松开快捷键，文字直接出现在光标位置
          - 可设纠正词，专有名词误识别能改回来
---

> 收集一些可以反复查阅的开源资料，全部指向 GitHub 仓库，点开即用。

- **过日子**：01 高性价比人生指南、02 延寿指南、03 做饭指南、04 买房功课、05 租房避坑
- **找工作**：06 面试反问、07 校招避雷
- **人情往来**：08 人情世故、09 狗头军师
- **重新开始学**：10 人生进阶指南、11 投资指南
- **开发与 AI**：12 Public APIs、13 Lightpanda、14 OpenMausBot、15 Game Studios、16 FreeToken
- **本机小工具**：17 Handy、18 hex

> 租房这块 GitHub 上没有独立的高星中文项目，05 是从 01 第 15 章摘出来的要点索引，细则和法规出处回原文看。
>
> 15 的 `/start` 是 Claude Code 里运行的斜杠命令，需要先装插件；17、18 都是本地应用，装完下载模型才能离线用。
