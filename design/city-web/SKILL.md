---
name: city-web
description: >-
  《CITY THE ANIMATION》系列网站与 Web 应用的设计、开发与评审规范：统一四色 Token、字体栈、极简主页面与页脚、共享顶栏（TopBar）与舒适一屏全屏菜单壳层（city-shell）、Z-index
  层级、全屏画布与工作室两类页面原型、三语切换及 *.city.chius.dev 与 GitHub 原仓库在菜单内互链。Use when building, refactoring,
  unifying, or auditing CITY-themed websites or fan web apps (including city-social-map, city-avatar, and future *.city.chius.dev sites).
---

# CITY 网站设计规范 · City Web Design System

本规范用于将[CITY 通用设计理念 (`city`)](../city/SKILL.md)落地为工程可复用、多站点造型统一的现代 Web 应用，确保每一个 `*.city.chius.dev` 项目在顶栏交互、视觉 Token、三语体系、无障碍可用性与**轻盈无压的页面/菜单结构**上保持家族一致性。

按需查阅三份配套参考（编码或评审时只读相关章节，不机械照搬无关规则）：

- CSS 变量、动效关键帧、Z-index 阶梯与两类页面原型尺度：[视觉 Token 与页面架构](references/tokens-and-layouts.md)
- 共享 `city-shell` 组件接口、生态站注册表（`CITY_SITES`）、`index.html` 与部署模板：[共享壳层、生态互链与工程模板](references/shared-shell-and-ecosystem.md)
- 网页反模式避坑表、五维交付核对单与评审报告模板：[反模式、质量门禁与评审规范](references/quality-and-audit.md)

## 六条核心网页法则

1. **先读 `city` 理念，再写页面代码**：保留纸面 `#FFFDF9`、深墨 `#141419`、硬偏移投影（`2.5px–4px`）、**C-I-T-Y** 四色节拍（`#F7B647` / `#F09CB4` / `#99CB77` / `#EE847D`）及 `#33333F` 旁白盒，严禁套用模糊灰度 SaaS 卡片或霓虹渐变。
2. **共享 `city-shell` 纯语义 CSS，严禁框架泄漏**：共享壳层文件（`src/styles/city-shell.css` 与 `src/components/city-shell/`）**只写标准 CSS `.city-*` 类与内联 SVG**，绝不写 Tailwind 工具类——因为 `city-social-map` 使用 `@tailwindcss/vite` 而 `city-avatar` 与轻量站可使用纯 CSS。品牌图标不依赖可能随大版本删改的第三方 icon（例如 GitHub 徽标统一使用共享组件内联 `<GitHubMark />`）。
3. **主页面与页眉/页脚极简，互链与 GitHub 收纳进右上角菜单**：
   - **顶部右侧曲面托架（`.city-top-shelf`）**：只放 **本站核心功能控件插槽 → `中 / EN / 日` 三语切换 → 四色横条变形菜单按钮（`.city-menu-btn`）**。严禁在主页面页眉放置 GitHub 图标或外站跳转胶囊，保持主工作区纯净。
   - **流式页面页脚（`CityFooter`）**：仅保留单行版权/非官方免责声明，不在页脚堆放外链。
   - **全屏展开菜单（`CityMenuOverlay`，最大宽 `840px`）**：保持与 `avatar.city.chius.dev` 相同的「**Hero（字标＋Mimineko＋2×2 四色瓷砖）→（仅信息较多的站点允许加 1 个紧凑标签卡与单行键盘提示）→ 居中胶囊链接行（`.city-menu-links`）→ 单行版权尾注**」紧凑结构。姊妹站链接、本站 GitHub 源码、官网与 `Awesome CITY` 通过主瓷砖或底部胶囊行进入（并自动去重），**不单独增设大块生态站介绍卡片占空间**。
4. **选定单一页面原型，守住 Z-index 与抽屉避让纪律**：
   - **原型 A — 全屏沉浸画布**（如 `city-social-map`）：`100vw × 100vh; overflow: hidden`；飘浮字母背景不透明度 `0.42`（`36s`）；开场可用天蓝幕布 `CityLoadingCurtain`（`prefers-reduced-motion` 下跳过）；右侧详情抽屉打开时，桌面端右下角搜索/缩放 HUD 自动左移让位（或窄屏隐藏），绝不允许抽屉遮住搜索自动补全弹出层。
   - **原型 B — 工作室 / 图文专题页**（如 `city-avatar`）：`max-width: 1080px` 居中流式网格；`body::before` 固定极淡 `0.24` 字母彩纸底纹；**全屏内至多为一处主舞台或核心结果框**使用 `.city-conic-frame` 旋转四色边框，其余面板一律退回静态墨边白卡；底部配极简 `CityFooter`。
   - **Z-index 严格分层**：左上角品牌徽章 `45` → 全屏菜单 `65` → 右上角控制托架 `70` → 全屏弹窗（如名鉴）`80` → 灯箱预览 `85` → 侧边滑出抽屉 `95` → 开场幕布 `9999`。所有自带右上角关闭 `×` 按钮的弹窗与抽屉必须高于 `70`。
5. **三语优先与真实字体栈**：全站固定提供 **简体中文（默认）/ English / 日本語** 切换，字体栈采用 Google Fonts `M PLUS Rounded 1c`（400/500/700/800/900）＋ `Noto Sans SC`，配合 `@media (prefers-reduced-motion: reduce)` 停止飘移、旋转与弹跳动效。
6. **一致的托管与工程规范**：基于 React 19 + TypeScript 5.8 + Vite 8 + Cloudflare Workers，域名统一规划在 `<slug>.city.chius.dev`，站点副标采用全大写英文短词（如 `SOCIAL MAP`、`AVATAR`、`EPISODES`）。

## 新建或统一 CITY 网站的工作流

1. **核对项目角色与原型**：确认新站属于 **原型 A（全屏画布/地图/网络）** 还是 **原型 B（工作室/索引/工具流）**，确定唯一 `CitySiteId`、子域名 `<slug>.city.chius.dev` 与 GitHub 仓库 `chius-cc/<repo>`。
2. **接入与同步 `city-shell`**：
   - 将新站条目注册进 `CITY_SITES`（`src/components/city-shell/ecosystem.ts`）；
   - 将最新一致的 `city-shell.css` 与 `src/components/city-shell/*` 同步到新站与姊妹站（如 `city-social-map`、`city-avatar`），保持共享文件逐字节相同；
   - 新站页面具体样式写在站点自身的 `src/styles/city-theme.css`（顶部 `@import './city-shell.css';`），不重复定义 `.city-wordmark`、`.city-top-shelf`、`.city-menu-*` 等共享规则。
3. **实现页面与菜单互链**：
   - 顶栏使用 `<CityTopShell siteId="..." ...>` 只传入本站核心工具控件；
   - 菜单使用 `<CityMenuOverlay siteId="..." ...>` 传入 4 枚固定 C-I-T-Y 瓷砖（若内容站确实需要扩展索引，使用 `.city-menu-tabs-card` 单卡片＋标签页折叠展示，避免纵向堆砌）；通过 `tiles` 或 `extraLinks` + 内置胶囊行提供姊妹站、`Awesome CITY`、官网与 GitHub 原仓直达；
   - 流式页配极简 `<CityFooter />`，并在 `README.md` / `README.zh.md` 互相链接姊妹站与原仓。
4. **多视口验收与构建检查**：参照 [反模式、质量门禁与评审规范](references/quality-and-audit.md)，在 `1440 / 1024 / 900 / 640 / 375` 宽度、`zh / en / ja` 切换、菜单一屏呼吸感、弹窗关闭按钮无遮挡、无横向滚动与 `tsc -b && vite build` 全绿后交付。
