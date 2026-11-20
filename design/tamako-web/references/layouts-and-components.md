# 页面原型、组件蓝本与响应式

所有组件使用纯语义 `.tamako-*` 类名，不耦合特定 JS/CSS 框架（可直接用于静态 HTML、React、Vue 或 Astro）。

## 一、四类页面原型几何尺度

| 原型 | 适用场景 | 容器与栅格尺度 | 核心组合组件 |
| --- | --- | --- | --- |
| **原型 A：商店街拱廊门户** | 综合官网、社团/店铺多栏目站、工具索引站 | 全宽彩篷顶栏；主内容外框 `max-width: 1080px`，桌面左栏导航 `200px–220px` ＋ 右侧主卡 `minmax(0, 1fr)`；`<=834px` 左栏收纳至顶部抽屉 | 彩篷顶栏 + 看板鸟气泡导航 + 白/奶油卷轴卡 |
| **原型 B：街区导览与图鉴** | 商店街地图、角色关系网、摊位/展区分布 | 图版容器 `max-width: 820px` 居中，支持 `100%` 自适应缩放；`>=44×44px` 按钮热点；原位弹卡 `max-width: 800px` | 交互图版 + 无障碍热点圆章 + 分组替代卡片流 |
| **原型 C：庆典与特设长卷** | 周年专题、音乐会/快闪活动、产品发布页 | 固定磨砂粉白吸顶栏；主视觉 `min-height: min(82vh, 920px)`；白岛 `.tamako-island` `max-width: 960px`（`width: 92%`）、内文 `.tamako-inner` `max-width: 800px` | 吸顶栏 + `30px` 圆角白岛 + 和果子胶囊 + 手风琴 + 交替表 |
| **原型 D：手记专栏与揭示板** | 制作日誌、更新公告、FAQ 与留言板 | 单栏居中 `max-width: 820px`，或 `minmax(0, 1fr) 260px` 带归档侧栏；正文宽 `<= 65ch`（约 `34–42` 中文字符） | 六瓣花/小鸟标题 + `dotted` 针脚 + 相纸切图 + 店方回复块 |

## 二、七大核心组件 CSS 与 HTML 蓝本

### 1. 磨砂樱白吸顶栏与手机端三杠变 `×` 抽屉

```css
.tamako-header {
  position: fixed;
  inset: 0 0 auto 0;
  z-index: 99;
  background: var(--tamako-header-glass);
  backdrop-filter: blur(8px);
  border-bottom: 2px solid var(--tamako-sakura);
  padding: 18px 0;
  transition: padding 0.2s ease-out;
}
.tamako-header.is-scrolled {
  padding: 10px 0;
}
.tamako-nav-wrap {
  max-width: 840px;
  width: 92%;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 24px;
}
.tamako-nav-list {
  display: flex;
  align-items: center;
  gap: clamp(14px, 2vw, 28px);
  list-style: none;
  margin: 0;
  padding: 0;
}
.tamako-nav-list a {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  color: var(--tamako-link);
  font-family: var(--tamako-font-display);
  font-size: clamp(1rem, 0.92rem + 0.4vw, 1.25rem);
  font-weight: 900;
  text-decoration: none;
  transition: opacity 0.2s ease-out;
}
.tamako-nav-list a:hover {
  opacity: 0.7;
  text-decoration: underline;
}
.tamako-burger {
  display: none;
}

@media (max-width: 768px) {
  .tamako-header {
    background: var(--tamako-drawer-pink);
    border-bottom: none;
    padding: 8px 16px;
  }
  .tamako-burger {
    position: relative;
    z-index: 100;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    width: 44px;
    height: 44px;
    padding: 13px 7px;
    margin: 0 auto;
    border: 0;
    background: transparent;
    cursor: pointer;
  }
  .tamako-burger span {
    display: block;
    width: 100%;
    height: 3px;
    border-radius: 2px;
    background: #ffffff;
    transition: transform 0.3s ease-out, opacity 0.2s ease-out;
  }
  .tamako-header.is-open .tamako-burger span:nth-child(1) {
    transform: translateY(7.5px) rotate(-45deg);
  }
  .tamako-header.is-open .tamako-burger span:nth-child(2) {
    opacity: 0;
  }
  .tamako-header.is-open .tamako-burger span:nth-child(3) {
    transform: translateY(-7.5px) rotate(45deg);
  }
  .tamako-nav-wrap {
    position: fixed;
    inset: 0;
    width: 100%;
    max-width: none;
    background: var(--tamako-drawer-pink);
    flex-direction: column;
    justify-content: center;
    opacity: 0;
    pointer-events: none;
    transition: opacity 0.3s ease-out;
  }
  .tamako-header.is-open .tamako-nav-wrap {
    opacity: 1;
    pointer-events: auto;
  }
  .tamako-nav-list {
    flex-direction: column;
    gap: 18px;
  }
  .tamako-nav-list a {
    color: var(--tamako-ink);
    font-size: 1.25rem;
  }
}
```

### 2. 商店街三色彩篷顶带 ＋ 吉祥物气泡导航（原型 A）

使用纯 CSS 渐变复刻 2013 官网 `globalHeader/bg.jpg` 的浅薄荷 `#DBFDF6`、淡樱 `#F9EDED` 与浅奶黄 `#F3FBD7` 商店街遮阳篷斜纹，零图片依赖且适配任意分辨率：

```css
.tamako-awning-band {
  background:
    linear-gradient(to bottom, rgba(251, 248, 241, 0) 65%, var(--tamako-bg-washi) 100%),
    repeating-linear-gradient(
      90deg,
      #dbfdf6 0 48px,
      #f9eded 48px 96px,
      #f3fbd7 96px 144px
    );
  padding: 28px 0 48px;
}

.tamako-mascot-bubble {
  min-height: 52px;
  padding: 10px 14px;
  margin-bottom: 12px;
  border-radius: 16px;
  background: var(--tamako-surface);
  border: 2px solid var(--tamako-rule-petal);
  color: var(--tamako-ink);
  font-size: 0.875rem;
  font-weight: 700;
  box-shadow: var(--tamako-shadow-soft);
}
```

交互规范：左侧导航每项悬停或 `:focus-visible` 聚焦时，通过 `aria-live="polite"` 更新 `.tamako-mascot-bubble` 的街坊提示短语，确保键盘玩家同样体验「看板搭话」乐趣。

### 3. 糯米白岛（`.tamako-island`）、相纸缩略图与内联六瓣花 SVG

```html
<!-- 内联六瓣樱花符（取自 10th-event 矢量花瓣比例），可用于 h2/导航前缀 -->
<svg class="tamako-floret" viewBox="0 0 20 22" width="18" height="20" aria-hidden="true">
  <path fill="currentColor" d="M11.55 17.39c.14.54.5 2.05.5 2.45 0 .97-.86 2.2-2.23 2.2s-2.23-1.22-2.23-2.2c0-.4.07-.68.79-3.49.43-1.69.61-2.52 1.22-4.93-2.34 2.23-3.13 3.02-4.43 4.28-1.76 1.76-1.98 1.94-2.92 1.94-1.26 0-2.27-1.01-2.27-2.23 0-1.69 1.3-2.05 2.34-2.38 1.94-.58 5.08-1.44 7.06-2.02-1.26-.36-6.77-1.91-7.88-2.27-1.26-.43-1.51-1.62-1.51-2.12 0-1.22.97-2.23 2.27-2.23.94 0 1.12.22 2.92 1.94 1.44 1.44 2.92 2.88 4.43 4.28-.65-2.59-.9-3.64-1.51-5.98-.14-.54-.5-2.05-.5-2.45 0-.97.86-2.2 2.23-2.2s2.23 1.22 2.23 2.2c0 .4-.07.68-.79 3.49-.43 1.69-.61 2.52-1.22 4.93 1.48-1.4 2.99-2.84 4.43-4.28 1.8-1.73 1.98-1.94 2.92-1.94 1.3 0 2.27 1.01 2.27 2.23 0 1.69-1.3 2.05-2.34 2.38-1.94.58-5.08 1.44-7.06 2.02 1.26.36 6.77 1.91 7.88 2.27 1.26.43 1.51 1.62 1.51 2.12 0 1.22-.97 2.23-2.27 2.23-.94 0-1.12-.22-2.92-1.94-1.44-1.4-2.95-2.88-4.43-4.28.65 2.59.9 3.67 1.51 5.98z"/>
</svg>
```

```css
.tamako-island {
  max-width: 960px;
  width: 92%;
  margin: 30px auto 72px;
  padding: clamp(24px, 4vw, 44px) 0;
  background: var(--tamako-surface);
  border-radius: var(--tamako-radius-island);
  box-shadow: var(--tamako-shadow-soft);
}
.tamako-island-inner {
  width: 90%;
  max-width: 800px;
  margin: 0 auto;
}
.tamako-photo-mount {
  padding: 4px;
  background: var(--tamako-surface);
  border: 1px solid var(--tamako-frame-gold);
  border-radius: var(--tamako-radius-thumb);
  transition: border-color 0.2s ease-out;
}
.tamako-photo-mount:hover {
  border-color: var(--tamako-frame-gold-hover);
}
.tamako-stitch-hr {
  border: 0;
  border-bottom: 1.5px dotted var(--tamako-rule-stitch);
  margin: 24px 0;
}
@media (max-width: 768px) {
  .tamako-island {
    border-radius: var(--tamako-radius-island-sm);
    margin: 20px auto 48px;
  }
}
```

### 4. 双色交替圆角规格表（`.tamako-chart`）

```css
.tamako-chart {
  border: 1px solid var(--tamako-petal);
  border-radius: var(--tamako-radius-island-sm);
  overflow: hidden;
  margin: 16px 0 32px;
}
.tamako-chart-row {
  display: grid;
  grid-template-columns: 180px minmax(0, 1fr);
  min-height: 4.25rem;
}
.tamako-chart-row + .tamako-chart-row {
  border-top: 1px solid var(--tamako-petal);
}
.tamako-chart-row dt {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 12px 16px;
  text-align: center;
  font-weight: 900;
  color: #ffffff;
}
.tamako-chart-row:nth-child(odd) dt { background: var(--tamako-coral); }
.tamako-chart-row:nth-child(even) dt { background: var(--tamako-ink); }
.tamako-chart-row dd {
  margin: 0;
  display: flex;
  align-items: center;
  padding: 14px 24px;
  font-weight: 700;
  color: var(--tamako-ink);
}
.tamako-chart-row:nth-child(odd) dd { background: var(--tamako-surface); }
.tamako-chart-row:nth-child(even) dd { background: var(--tamako-bg-blush); }

@media (max-width: 768px) {
  .tamako-chart-row {
    grid-template-columns: 1fr;
  }
  .tamako-chart-row dt {
    padding: 8px 14px;
  }
  .tamako-chart-row dd {
    padding: 14px;
  }
}
```

### 5. `+` 旋转 `45deg` 变 `×` 的胶囊手风琴（`.tamako-accordion`）

```css
.tamako-accordion {
  width: 100%;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 14px;
  padding: 14px 24px;
  border: 0;
  border-radius: var(--tamako-radius-pill);
  background: var(--tamako-sky);
  color: #083b5c;
  font-family: var(--tamako-font-display);
  font-size: clamp(0.9375rem, 0.8rem + 0.5vw, 1.25rem);
  font-weight: 900;
  cursor: pointer;
}
.tamako-accordion-icon {
  position: relative;
  width: 34px;
  height: 34px;
  border-radius: 50%;
  background: #ffffff;
  flex-shrink: 0;
  transition: transform 0.3s var(--tamako-ease);
}
.tamako-accordion-icon::before,
.tamako-accordion-icon::after {
  content: "";
  position: absolute;
  inset: 0;
  margin: auto;
  background: #083b5c;
  border-radius: 2px;
}
.tamako-accordion-icon::before { width: 3.5px; height: 18px; }
.tamako-accordion-icon::after { width: 18px; height: 3.5px; }
.tamako-accordion[aria-expanded="true"] .tamako-accordion-icon {
  transform: rotate(45deg);
}
```

### 6. 竖排开场幕布（可选）与店方回复／虚线分页

- **竖排开场幕布**：仅首页或特设首屏可用，通过 `writing-mode: vertical-rl` 排两句短语；配合 `sessionStorage` 记录已读，顶部必置 `<button class="tamako-skip-btn">` 跳过钮，并在 `@media (prefers-reduced-motion: reduce)` 下彻底隐藏幕布与跳过淡入等待。
- **店方回复块与虚线分页**：读者留言或卡片尾注内可插 `.tamako-staff-reply { margin-top: 12px; padding: 10px 14px; border-radius: 12px; background: var(--tamako-bg-blush); color: var(--tamako-reply-warm); font-weight: 700; }`；分页链接默认 `border: 1px dotted var(--tamako-link)`，当前页用实线边框配 `var(--tamako-tint-pink)` 柔粉底。

## 三、Z-index 阶梯、锚点与断点纪律

- **Z-index 阶梯**：固定背景装饰 `-1` → 页面内浮动热点/角标 `40` → 右下回顶胶囊 `.tamako-pagetop` `80` → 吸顶顶栏 / 移动全屏抽屉 `99` → 移动汉堡钮 `100` → 全屏弹卡遮罩 `1040` → 弹卡主体 `1050` → 可选首访开场幕布 `9999`。
- **锚点偏移**：长卷页面被固定顶栏吸顶时，所有带 `#id` 的区块统一设置 `scroll-margin-top: 110px;`（`@media (max-width: 768px)` 下设为 `60px`），禁止继续使用十周年站旧式 `padding-top: 110px; margin-top: -110px` 负边距黑魔法（避免元素命中区相互重叠）。
- **无障碍焦点与减动效**：

```css
:where(a, button, summary, input, [tabindex]):focus-visible {
  outline: 3px solid var(--tamako-ink);
  outline-offset: 3px;
}

@media (prefers-reduced-motion: reduce) {
  html { scroll-behavior: auto; }
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
  .tamako-intro-curtain { display: none !important; }
}
```
