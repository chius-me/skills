# 预设色板与页面模式

本文档提供 `chius.me` 与 `chius.cc`（Chipaper）的实现基准，同时定义同风格站点的语义 Token、符号语法与五类页面尺度。色值可作为新站起点；字号与间距随实际语种和内容密度微调，但主轴与层级关系保持不变。

## 共用语义配色与对比度基准

| 语义 Token | 用途角色 | 浅色预设（对比度 vs `--bg`） | 深色预设（对比度 vs `--bg`） |
| --- | --- | --- | --- |
| `--bg` | 页面主背景 | `#fdfcfb`（暖纸白） | `#202530`（蓝灰夜色） |
| `--text` | 正文与主标题 | `#292c30`（`13.69:1` AAA） | `#e1e5ed`（`12.15:1` AAA） |
| `--muted` | 次级文本、日期、元信息、引文 | `#6b7076`（`4.87:1` AA） | `#a4adbb`（`6.78:1` AA） |
| `--accent` | 链接、键盘焦点、当前态与主交互 | `#256786`（`6.09:1` AA） | `#eab38b`（`8.27:1` AAA） |
| `--accent-hover` | 链接与交互悬停 | `#124c68`（`9.07:1` AAA） | `#ffd1ad`（`10.94:1` AAA） |
| `--mark` | 句点、井号、列表圆点、引文侧线 | `#b24c37`（`5.15:1` AA） | `#eab38b`（`8.27:1` AAA） |
| `--line` | `1px` 分隔细线、辅助描边 | `#e5e4e1`（`1.24:1` 装饰线） | `#3c4350`（`1.54:1` 装饰线） |
| `--soft` | 按钮、搜索框、内联代码、表头表面 | `#f2f1ee` | `#2a303c` |
| `--code-bg` | 独立代码块与代码工具栏表面 | `#f5f4f1` | `#252c38` |

### 对比度与换色边界

- **柔和表面上的次级字色**：浅色 `--muted`（`#6b7076`）在 `--bg` 上为 `4.87:1`，但落在 `--soft`（`#f2f1ee`）上会降至 `4.42:1`。小字号次级说明优先排在 `--bg` 主底上；若必须放进 `--soft` 容器，改用 `--text` 或加深灰阶以维持 ≥ `4.5:1`。
- **细边线的可感知边界**：`--line` 仅承担区块分隔；当按钮、搜索框或悬浮入口需要明确指示可操作范围时，须配合 `--soft` 底色填充、悬停变色或提高边框不透明度（如 `rgb(41 44 48 / .18)`）。
- **自定义品牌色替换**：非 Chius 站点沿用本风格时，保留 90%–95% 的暖纸/蓝灰中性面积，只替换 `--accent`、`--accent-hover` 与 `--mark`。浅色宜选沉稳低明度色，深色需单独调配柔和提亮色（不可直接照搬浅色色值或机械反相）；避开 `#000`/`#fff` 刺眼纯色对撞与 `OKLCH 270°–330°` 紫色系光晕渐变。

## 线型、符号与表面语法

每个视觉符号只承担固定职责，不在无对应语义处混用：

| 语法元素 | 形态规范 | 适用语义 |
| --- | --- | --- |
| **实线下划线** | `1px solid`，`text-underline-offset: .25em` | 通用文本链接、次级入口、页脚与归档条目悬停 |
| **虚线下划线** | `dashed`，配合 `overflow-wrap: anywhere` | 正文 `.prose a` 内链、文章列表标题 `h3 a:hover` |
| **波浪下划线** | `wavy`，`text-underline-offset: .5em` | 主导航链接悬停与当前页 `[aria-current="page"]` |
| **键盘焦点环** | `outline: 2px dashed var(--accent)`，外偏移 `5px`（紧凑按钮组内改 `-3px`） | 所有可交互元素的 `:focus-visible`，瞬时显示，禁加过渡动画 |
| **文本选中态** | `::selection { background: var(--accent); color: var(--bg); }` | 全站正文与代码选中高亮 |
| **强调句点 `.`** | 着色 `--mark`，装饰时加 `aria-hidden="true"` | 站名尾缀（`Chius.`）、异常状态标题（`404.`）、长文收束（`EOF.` / `全文完.`） |
| **井号 `#`** | 着色 `--mark`（标签内降透明度 `.6`），加 `aria-hidden="true"` | 首页分区标题前缀、正文标题悬停锚点、标签前缀 |
| **方向箭头** | `↗` 标示跳出或全量列表；`← / →` 标示返回或上下篇时序 | 按跳转方向如实使用（窄屏导航可隐藏外链 `↗` 腾出横向空间），禁在每个普通按钮后机械追加 `→` |
| **细线与圆角** | 区块划界用 `1px solid var(--line)`，文内转折与文末翻页用 `1px dashed var(--line)`；控件圆角统一 `3px–4px` | 描边盒最多一层，严禁在卡片框内再套描边代码块或内嵌面板 |

## 五类页面尺度与组件细节

### 1. 身份与去向页（参考预设：`chius.me`）

- **容器与主轴**：外容器最大 `37.5rem`（`600px`），主内容沿中轴排列；同站附属左对齐短页（如 `404`、`Privacy`）复用 `37.5rem` 外宽并切换左对齐内边距 `1.25rem`。
- **首屏构成**：圆头像 `8rem × 8rem`（显式声明 `width="128" height="128"`、配 `2x srcset` 与 `fetchpriority="high"`） → 粗体紧字距站名（`700` 字重，`letter-spacing: -.055em`，桌面约 `3.05rem`、窄屏 `2rem`）及可选 `--mark` 句点。
- **等宽按钮栈**：每行宽 `18.75rem`（`300px`，`max-width: 100%`）、最小高 `3rem`（`48px`）、间距 `1rem`。文字 `500` 字重，配 `1.25rem` 单色 SVG 图标（`alt="" aria-hidden="true"`，通过滤镜或 `currentColor` 统一墨色，不混用五彩平台底色）；`1px` 边框、`4px` 圆角与极轻内高光。悬停在 `0.18s` 内切为 `--bg` 纸底与 `--accent` 边框及文字，**零位移**（`transform: none`）。
- **页脚与纸纹**：页脚宽 `18.75rem`，以 `1px solid var(--line)` 顶线分隔，字号 `.8rem`。短页可用固定 SVG 细噪点营造纸感（`position: fixed; inset: 0; opacity: .045; pointer-events: none`）。若接入第三方悬浮挂件，需预留 `env(safe-area-inset-*)` 安全边距并提供 `<noscript>` 纯文本链接兜底。
- **参考出处**：[线上页面](https://chius.me/) · [纸色与交互 CSS](https://github.com/chius-n/chius.me/blob/b575efa472afb582290e21cf7805ff14a6b6758e/public/css/paper.css) · [容器与基础尺度](https://github.com/chius-n/chius.me/blob/b575efa472afb582290e21cf7805ff14a6b6758e/public/css/style.css)

### 2. 博客首页与文章索引（参考预设：`chius.cc` / `Chipaper`）

- **统一阅读外栏**：`.site-shell` 取 `width: min(100% - 3rem, 48rem)`（`<= 480px` 窄屏改为 `calc(100% - 2.5rem)`），居中放置；页头、引言、分区标题、列表、正文与页脚严格共享同一左右边线。阅读站底色保持纯平，不叠纸纹噪点。
- **页头与工具组**：桌面最小高 `100px`，底边 `1px solid var(--line)`。左侧站名 `1.3rem`（`700` 字重，`-.055em` 字距，不换行）；右侧导航链接（`.875rem`）与细线工具组（搜索、主题切换、多语言 `<details>` 下拉合入同一个 `1px` 描边、`4px` 圆角容器，内部以 `1px` 竖线分隔）。`<= 760px` 时页头允许换行，图标按钮扩至 `44×44px` 触控尺寸；`<= 374px` 极窄屏隐藏语言名文字仅保留地球图标。
- **引言与开放列表**：首页引言上下留白 `3.8rem / 2.8rem`，标题 `clamp(1.85rem, 4vw, 2.5rem)`，配一句 `1rem` 次级灰自述与紧凑线性社交图标，底边 `1px` 细线。最近文章分区标题 `1.2rem`（前置 `--mark` 色 `#`），右侧基线对齐「全部文章 `↗`」。列表不加卡片框与分隔线，条目间距 `2.5rem`（窄屏 `2.1rem`），按「`1.15rem` 标题 → `.75rem` 日期与阅读时间 → `.9rem` 两行截断摘要 → 可选 `#tag` 行」重复排列。

### 3. 长文阅读页（参考预设：`Chipaper` `.prose`）

- **页头与目录**：顶部 `.75rem` 面包屑（`文章 / 当前标题`） → `clamp(1.8rem, 3.4vw, 2.3rem)` 标题（窄屏 `1.65rem`、`1.65` 行高，`text-wrap: pretty`） → 元信息与标签 → 按需渲染上下 `1px` 细线夹持的 `<details class="post-toc">` 折叠目录（无标题时不渲染空壳）。
- **正文与富媒体排版**：正文 `.prose` 字号 `1.025rem`（窄屏 `1rem`）、行高 `2`、`line-break: strict`；`h2` `1.4rem`、`h3` `1.15rem`、`h4` `1rem`，标题悬停或聚焦时浮现低透明度 `#` 锚点。列表项目符号与引文左侧 `3px` 竖线均用 `--mark` 色。正文图片块级居中并带 `1px solid var(--line)` 细框与 `3px` 圆角，配居中 `.8rem` 次级灰图注。
- **代码与宽表格隔离**：内联代码用 `--soft` 底、`1px` 边与 `.85em` 字号；独立代码块置于 `--code-bg` 与 `1px` 描边容器内，顶部设 `2.2rem` 高工具栏显示语言名与带 `aria-live="polite"` 的复制按钮，`pre` 设 `overflow-x: auto` 与 `tabindex="0"`。宽表格外包 `.table-scroll`（`overflow-x: auto`、`tabindex="0"`、`role="region"`），表头用 `--soft` 底色，严禁撑出视口横向滚动条。
- **文末收束**：居中 `.8rem` 完结标记配 `--mark` 句点 → `1px dashed var(--line)` 顶线分隔的双栏上下篇导航 → 可选评论区。
- **参考出处**：[线上页面](https://chius.cc/) · [Chipaper 排版与双主题 CSS](https://github.com/chius-n/chipaper/blob/fdc1c03432268b9ce93590bb55af37a761b6a2ae/assets/css/paper.css) · [首页模板](https://github.com/chius-n/chipaper/blob/fdc1c03432268b9ce93590bb55af37a761b6a2ae/layouts/home.html) · [文章列表模板](https://github.com/chius-n/chipaper/blob/fdc1c03432268b9ce93590bb55af37a761b6a2ae/layouts/partials/paper/post-list.html)

### 4. 归档、标签与站内检索页

- **归档页（Archives）**：按年份 `h2` 分组（年份旁可用 `.75rem` 次级灰标注篇数）；每行采用 `display: flex; align-items: baseline; gap: 1.5rem`，左侧等宽 `<time>`（`flex-shrink: 0; color: var(--muted)`）天然对齐成列，右侧放文章标题链接。
- **标签汇总（Taxonomy）**：使用宽松换行的无序列表（`gap: 1rem 1.7rem`），每个标签后跟 `.7rem` 次级灰篇数角标，不用彩色胶囊（Pill）堆砌。
- **站内检索（Search）**：显式 `<label for>` + `--soft` 底色 `1px` 描边输入栏（字号 ≥ `.85rem` / 移动端建议 `1rem` 防止 iOS 自动缩放）。下方放置状态行（空闲提示 / 检索中 / 匹配篇数 / 无结果 / 索引加载失败），匹配结果直接复用 `.post-item` 排式。

### 5. 独立说明与异常页（`About` / `404`）

- **说明页（About / Now / Uses）**：延续左对齐主轴，正文栏可收窄至 `42rem` 提升纯文字专注度；分节 `h2` 降为 `1rem`、`500` 字重与 `--muted` 色，扮演安静的栏目标签而非喧宾夺主的大标题。
- **异常页（404）与空状态**：设置 `<meta name="robots" content="noindex">`，展示清晰的 `404.` 标题、一句平实原因说明与明确的回首页链接（`← Back` 或 `返回首页 →`），不堆砌插画或戏谑文案。

## 关键基础骨架片段

### 防闪烁双主题初始化与无脚本退化

在 `<head>` 样式表前同步写入 `data-theme`，并在无脚本环境下自动隐藏仅依赖 JS 的主题切换按钮：

```html
<meta name="color-scheme" content="light dark">
<meta name="theme-color" content="#fdfcfb" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#202530" media="(prefers-color-scheme: dark)">
<script>
  (() => {
    let pref;
    try { pref = localStorage.getItem('site-theme'); } catch (_) {}
    document.documentElement.dataset.theme = pref === 'light' || pref === 'dark'
      ? pref : (matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
  })();
</script>
```

```css
/* 无脚本时隐藏无法点击生效的主题按钮，保留语言切换等原生 <details> 控件 */
html:not([data-theme]) .theme-toggle { display: none; }

@media (prefers-reduced-motion: reduce) {
  html { scroll-behavior: auto; }
  *, *::before, *::after { transition-duration: 0.01ms !important; animation-duration: 0.01ms !important; }
}

@media print {
  .site-nav, .social-links, .post-toc, .code-toolbar, .post-navigation, .comments { display: none !important; }
  .site-shell { width: 100%; max-width: none; }
  :root, html[data-theme="dark"] { --bg: #fff; --text: #000; --muted: #444; --code-bg: #f5f5f5; --accent: #000; }
  .prose pre { white-space: pre-wrap; overflow-wrap: anywhere; }
}
```
