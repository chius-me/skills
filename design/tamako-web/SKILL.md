---
name: tamako-web
description: >-
  《玉子市场》（Tamako Market）网页设计主题与系统规范：基于 tamakomarket.com 双世代官网逆向提炼的糯米暖纸与豆沙棕红无障碍
  Token、`Zen Maru Gothic` 流式丸体排版、拱廊遮阳篷与吉祥物搭话导航、`30px` 糯米白岛、胶囊 `+`→`×` 手风琴、四类页面原型及三段响应式评审门禁。
  Use when designing, building, refactoring, or auditing Tamako Market-inspired websites,
  neighborhood/arcade guide portals, character or shop directories, community journals/boards,
  or campaign landing pages.
---

# 玉子市场网页设计规范 · Tamako Web Design System

本规范将[玉子市场通用设计理念 (`tamako`)](../tamako/SKILL.md)落地为通用、框架无关的现代网页设计系统：把 2013 年官方门户的**商店街拱廊彩篷、和纸肌理、手账虚线针脚与德拉看板搭话**，融合进 2023–2024 年十周年特设站的**流式丸体字阶、`30px` 糯米白岛、和果子胶囊手风琴与三段响应式断点**，同时修正早期 `980px` 定宽与低对比度文字缺陷。

按需查阅三份配套参考（编写或评审时按任务取用，不堆砌无关样式）：

- 双世代逆向基线、WCAG 硬化语义 Token 与丸体排版栈：[视觉 Token 与字体字阶](references/tokens-and-typography.md)
- 四类页面原型尺度、7 种核心组件 CSS/HTML 蓝本、Z-index 与断点矩阵：[页面原型、组件蓝本与响应式](references/layouts-and-components.md)
- 常见误区避坑表、五维交付核对单与分级评审输出模板：[反模式、质量门禁与评审规范](references/quality-and-audit.md)

## 六条核心网页法则

1. **融合双世代精髓，去旧疾留手作**：保留暖纸和风、彩篷条纹、白边相纸框与温柔动效，但**彻底摒弃** 2013 原站的 `viewport: width=980` 固定宽度、图片替换文字后藏 `<span>`（`display: none`）以及 `a:focus { outline: none }` 等无障碍硬伤。
2. **暖纸豆沙对比度守恒（WCAG AA 门禁）**：背景维持 85%–92% 糯米象牙 `#FDFFF2` / 和纸暖白 `#FBF8F1` / 纯白 `#FFFFFF`（分组面用奶黄 `#FAF4E0`、淡樱 `#FFF4F7`）；正文使用豆沙褐红 `#993338`（白底 `7.28:1`）或焙茶暖棕 `#8E4C28`（暖纸 `6.16:1`）；次级信息采用硬化焦糖棕 `#8A5A36`（`>= 5.31:1`，取代原站低对比的 `#BA8860`）；正文内联链接统一使用樱莓红 `#BF3B5E`（全浅底 `>= 4.77:1`）并带清晰下划线。全站禁用 `#000000` 粗黑边与生硬阴影，卡片依靠纯白岛与轻暖棕柔影（`0 4px 18px rgba(142, 76, 40, 0.08)`）划界。
3. **樱饼粉主色与和果子语义分工**：一级标题、吸顶栏底线与六瓣花 SVG 使用樱珊瑚 `#FF7B82` / `#F66E75`；多主题入口与胶囊手风琴按和果子色系分配（黄豆杏 `#F69E6E`、汽水薄荷 `#31CBB7`、晴空蓝 `#0EB2FF` / `#41A8DD`、艾草绿 `#93D548`、祭典蓝 `#2E62A2`）；**浅亮胶囊（`#F69E6E` / `#31CBB7`）内小字必须使用深墨字（`#5C2226` / `#13463F`，`>= 5.2:1`）**，高饱和深底或大号粗体标题方可使用白字。
4. **四类页面原型按任务择一**：
   - **原型 A — 商店街拱廊门户与内页**：顶栏三色淡彩遮阳篷条纹 ＋ 桌面左栏木牌导航与 `aria-live="polite"` 看板鸟搭话气泡 ＋ 右侧奶油/白底内容卷轴（`<=834px` 收敛为顶部抽屉）。
   - **原型 B — 街区导览地图与关系图鉴**：手绘底图配 `>= 44×44px` 键盘可达圆章热点 ＋ 原位 `max-width: 800px` 详情弹卡 ＋ 窄屏自动切换分组卡片列表，不依赖像素坐标硬点击。
   - **原型 C — 庆典与特设长卷**：磨砂樱白吸顶栏（`rgba(255, 249, 250, 0.92)` + `2px solid #FF7B82`，滚过 `100px` 收窄内距） ＋ 全幅主视觉与居中字标 ＋ 多座 `max-width: 960px`（内文 `800px`）的 `30px` 圆角白岛。
   - **原型 D — 手记专栏与街坊揭示板**：小鸟/六瓣花图标领衔标题 ＋ `1px–2px dotted` 虚线手账针脚分隔 ＋ 双色交替圆角规格表（`.tamako-chart`） ＋ 店方暖色回音批注与虚线方格分页。
5. **丸体排版与街坊式微交互**：标题与导航使用 `Zen Maru Gothic`（`700/900`），正文衔接 `Noto Sans SC` / `Noto Sans JP`（`400/500`，行高 `1.7–1.8`，开启 `font-feature-settings: "palt" 1`，用 `overflow-wrap: anywhere` 代替破坏英文单词的 `word-break: break-all`）。若启用 `vertical-rl` 竖排开场幕布，必须同时具备 `sessionStorage` 首次记忆、键盘可达的「跳过」钮、可选「重看」入口，以及 `@media (prefers-reduced-motion: reduce)` 下直接跳过与停止浮动的降级。
6. **三段断点与 Z-index 秩序**：`1320px`（主视觉横竖画幅切换） → `834px`（平板双栏转单栏与导航收敛） → `768px`（手机 `#FFB1B5` 樱粉全屏抽屉与三道白杠变 `×` 按钮、`30px` 圆角缩为 `15px`、双色 `dl` 表格转纵向堆叠）；所有锚点目标统一设 `scroll-margin-top: 110px`（手机 `60px`），严格遵守全局 Z-index 阶梯防止回顶钮与抽屉互相遮挡。

## 两遍式落地与评审工作流

1. **定原型并做去模板自审**：写代码前先确定页属原型（A/B/C/D）、主色与 1–2 个和果子辅色、字阶与断点，自检绝不混入纯黑描边、深灰 SaaS 卡片或霓虹玻璃渐变。
2. **注入语义 Token 与丸体字体栈**：复制 `references/tokens-and-typography.md` 中的 `--tamako-*` CSS 变量、字体声明、`::selection` 与细粉滚动条；核查所有浅彩底配字达到 WCAG AA。
3. **拼装拱廊与糯米岛组件**：按 `references/layouts-and-components.md` 实现吸顶栏/彩篷、`.tamako-island`、`.tamako-chart`、`.tamako-accordion`、`.tamako-photo-mount` 与可见 `:focus-visible` 焦点环。
4. **多视口验收与评审输出**：在 `1440 / 1024 / 834 / 768 / 375 / 320` 宽度、纯键盘 `Tab`、`prefers-reduced-motion: reduce` 及锚点跳转下逐项核验 [反模式、质量门禁与评审规范](references/quality-and-audit.md)。
