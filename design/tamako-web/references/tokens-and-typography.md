# 视觉 Token 与字体字阶

本文档将 REA 实测得到的 `tamakomarket.com` 双世代视觉数值整合为单一可复用的现代 CSS 变量系统，并针对小号文字补齐 WCAG 2.1 AA（`>= 4.5:1`）对比度硬化。

## 一、原站采样值 → `tamako-web` 语义 Token 映射

| 语义角色 | 2013 原站实测 | 2023 十周年实测 | `tamako-web` 规范值 | 调整说明与对比度基准 |
| --- | --- | --- | --- | --- |
| **主画布背景** | `/img/bg.jpg` 暖米点纹 `#FBF8F1` | `#FDFFF2` | `--tamako-bg-ivory: #fdfff2` / `--tamako-bg-washi: #fbf8f1` | 长卷专题用 `#FDFFF2`，日常手账站用 `#FBF8F1` 配极淡和纸纹理 |
| **奶油 / 淡樱分组面** | `#FAF4E0` / `#EFE9D4` | `#FFF4F7` / `#FFFFFF` | `--tamako-bg-custard: #faf4e0` / `--tamako-bg-blush: #fff4f7` / `--tamako-surface: #ffffff` | 避免纯灰底，保持蒸糯米与淡樱花瓣衬底 |
| **正文主墨色** | `#8E4C28`（焙茶棕） | `#993338`（豆沙褐红） | `--tamako-ink: #993338` / `--tamako-ink-roast: #8e4c28` | `#993338` 在白底 `7.28:1`；`#8E4C28` 在暖纸 `6.16:1`，均达高可读标准 |
| **次级说明字墨** | `#BA8860`（浅棕） | `#FF979D`（仅大字导语） | `--tamako-ink-muted: #8a5a36` | 原站 `#BA8860` 在暖纸仅 `2.92:1`，硬化为 `#8A5A36` 达 `5.51:1`（暖纸）/ `5.31:1`（奶油） |
| **正文文本超链接** | `#EE86A7`（粉）/ `#428FDB`（蓝） | `#F66E75` | `--tamako-link: #bf3b5e`（或 `#184070` 冷色公告） | 原站 `#EE86A7` 白底仅 `2.44:1`；硬化樱莓红 `#BF3B5E` 在五种浅底均达 `4.77:1–5.25:1` |
| **主品牌樱珊瑚** | `#EE86A7` | `#FF7B82` / `#F66E75` / `#FF979D` | `--tamako-sakura: #ff7b82` / `--tamako-coral: #f66e75` / `--tamako-petal: #ff979d` | 专用于大字号标题（`>= 18px bold` 或 `24px+`）、吸顶边框、图标描边与按钮底 |
| **和果子副色与朱红警示** | `#EDD18F` / `#DE9132` / `#FF5B5B` | `#F69E6E` / `#31CBB7` / `#0EB2FF` / `#93D548` / `#41A8DD` / `#2E62A2` / `#E4362D` | `--tamako-apricot` / `--tamako-mint` / `--tamako-sky` / `--tamako-leaf` / `--tamako-demachi` / `--tamako-alert` | `#F69E6E` 配深豆沙 `#5C2226`（`5.86:1`）；`#31CBB7` 配深青墨 `#13463F`（`5.24:1`）；`#2E62A2` 配白字（`6.20:1`） |
| **店方回复与手账针脚** | `#FF6600` 回复 / `hrbg.png` `#D8BDA3` / `#CC9966` 虚线 | `1px #FFCDC6` 细线 / `rgba(255,249,250,0.9)` 顶栏 | `--tamako-reply-warm: #c84b12` / `--tamako-rule-craft: #d8bda3` / `--tamako-rule-petal: #ffcdc6` | 小字回信由 `#FF6600` 加深至 `#C84B12` 保对比，装饰线保留轻暖棕与淡粉 |

## 二、标准 CSS 变量声明（可直接复制进 `:root`）

```css
:root {
  /* 表面与纸张 */
  --tamako-bg-ivory: #fdfff2;
  --tamako-bg-washi: #fbf8f1;
  --tamako-bg-custard: #faf4e0;
  --tamako-bg-sand: #efe9d4;
  --tamako-bg-blush: #fff4f7;
  --tamako-surface: #ffffff;
  --tamako-header-glass: rgba(255, 249, 250, 0.92);
  --tamako-drawer-pink: #ffb1b5;
  --tamako-tint-pink: rgba(225, 158, 194, 0.28);

  /* 字墨（WCAG AA 验证） */
  --tamako-ink: #993338;
  --tamako-ink-roast: #8e4c28;
  --tamako-ink-muted: #8a5a36;
  --tamako-ink-navy: #184070;
  --tamako-ink-date: #224c89;
  --tamako-link: #bf3b5e;
  --tamako-link-hover: #993338;
  --tamako-reply-warm: #c84b12;

  /* 樱饼与和果子色盘 */
  --tamako-sakura: #ff7b82;
  --tamako-coral: #f66e75;
  --tamako-petal: #ff979d;
  --tamako-sakura-classic: #ee86a7;
  --tamako-apricot: #f69e6e;
  --tamako-apricot-ink: #5c2226;
  --tamako-mint: #31cbb7;
  --tamako-mint-ink: #13463f;
  --tamako-sky: #0eb2ff;
  --tamako-demachi-sky: #41a8dd;
  --tamako-demachi-navy: #2e62a2;
  --tamako-leaf: #93d548;
  --tamako-alert: #e4362d;

  /* 手账线条、圆角、轻影与动效 */
  --tamako-rule-craft: #d8bda3;
  --tamako-rule-stitch: #cc9966;
  --tamako-rule-petal: #ffcdc6;
  --tamako-frame-gold: #edd18f;
  --tamako-frame-gold-hover: #de9132;
  --tamako-scrollbar: #ffc0b8;

  --tamako-radius-island: 30px;
  --tamako-radius-island-sm: 15px;
  --tamako-radius-pill: 9999px;
  --tamako-radius-thumb: 8px;
  --tamako-shadow-soft: 0 4px 18px rgba(142, 76, 40, 0.08);
  --tamako-ease: cubic-bezier(0.22, 0.61, 0.36, 1);

  /* 字族栈 */
  --tamako-font-display: 'Zen Maru Gothic', 'Hiragino Maru Gothic ProN', 'Noto Sans SC', 'Noto Sans JP', sans-serif;
  --tamako-font-body: 'Zen Maru Gothic', 'Noto Sans SC', 'Noto Sans JP', 'Hiragino Maru Gothic ProN', sans-serif;
}
```

## 三、Google Fonts 加载与全局排版基础

在 `<head>` 预连接并引入 `Zen Maru Gothic`（`500/700/900`）与 `Noto Sans SC` / `Noto Sans JP`（兼顾中文、日文与平假名混排圆润度）：

```html
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link
  href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700;900&family=Noto+Sans+SC:wght@400;500;700;900&family=Zen+Maru+Gothic:wght@500;700;900&display=swap"
  rel="stylesheet"
/>
```

基础字体、行宽、`::selection` 与滚动条规则：

```css
html {
  scroll-behavior: smooth;
  font-size: 16px;
}

body {
  margin: 0;
  color: var(--tamako-ink);
  background-color: var(--tamako-bg-ivory);
  font-family: var(--tamako-font-body);
  font-size: clamp(0.9375rem, 0.9rem + 0.2vw, 1rem); /* 15px–16px */
  font-weight: 500;
  line-height: 1.75;
  letter-spacing: 0.03em;
  font-feature-settings: 'palt' 1;
  overflow-wrap: anywhere;
  -webkit-font-smoothing: antialiased;
}

::selection {
  color: #ffffff;
  background: rgba(238, 134, 167, 0.5);
}

/* 章节大标题、导语与规格表流式字阶（对齐十周年站 clamp 曲线） */
.tamako-display-lg {
  font-family: var(--tamako-font-display);
  font-size: clamp(1.5rem, 0.85rem + 2.8vw, 3rem);
  font-weight: 900;
  line-height: 1.25;
  color: var(--tamako-sakura);
}

.tamako-section-title {
  font-family: var(--tamako-font-display);
  font-size: clamp(1.25rem, 0.85rem + 2vw, 2.375rem);
  font-weight: 900;
  color: var(--tamako-sakura);
}

.tamako-lead {
  font-size: clamp(0.9375rem, 0.8rem + 0.6vw, 1.25rem);
  font-weight: 700;
  color: var(--tamako-ink);
}

/* 窄滚动条仅用于独立内嵌列表容器，不覆盖浏览器主滚动条导致难以抓取 */
.tamako-scrollbox::-webkit-scrollbar {
  width: 4px;
}
.tamako-scrollbox::-webkit-scrollbar-track {
  background: var(--tamako-surface);
}
.tamako-scrollbox::-webkit-scrollbar-thumb {
  background: var(--tamako-scrollbar);
  border-radius: 9999px;
}
```
