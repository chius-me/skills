# 视觉 Token、动效、Z-index 与页面架构

本文档记录 `CITY` 系列网站的精准样式基准与页面原型几何尺度，对应 `city-shell.css` 与站点专属 `city-theme.css` 的分工边界。

## 一、核心 CSS Token 与动效声明

以下变量与关键帧定义在共享 `src/styles/city-shell.css` 的 `:root` 与全局域中，任何 `city-web` 项目不得在站点主题文件内重写同名 Token 破坏一致性：

| 分组 | 变量 / 属性 | 精准数值 | 职责说明 |
| --- | --- | --- | --- |
| **C-I-T-Y 品牌四色** | `--color-logo-C` / `I` / `T` / `Y` | `#f7b647` / `#f09cb4` / `#99cb77` / `#ee847d` | 标志、菜单瓷砖、四色圆点、四条变形按钮、旋转光环固定顺序 |
| **交互与功能色** | `--color-blue` / `--color-lightblue` / `--color-red` / `--color-green` / `--color-link` / `--color-alert` | `#1395ea` / `#c4e4f5` / `#dd5549` / `#8cc466` / `#f2638c` / `#e84646` | 幕布/定位强调、雷达天蓝瓷砖、冲突红、安全绿、超链粉、报错红 |
| **纸面与深墨灰阶** | `--color-paper` / `--color-cream` / `--color-white` / `--color-navyblue` / `--color-commentary` / `--color-grey100..700` | `#fffdf9` / `#faf6ee` / `#ffffff` / `#141419` / `#33333f` / `#eceae4` · `#d6d3cb` · `#777785` · `#424250` | 纸白画布、弱奶油分组底、深墨描边与文本、冷面吐槽/生物简介气泡 |
| **磨砂半透明表面** | `--color-white-alpha92` / `--color-white-alpha96` | `rgba(255, 253, 249, 0.92)` / `0.96` | 右上角控制托架 `.city-top-shelf`（配 `blur(10px)`）与全屏菜单底（`blur(12px)`） |
| **官方缓动曲线** | `--ease-city` / `--ease-city-out` / `--ease-bounce` | `cubic-bezier(0.65, 0.05, 0.36, 1)` / `cubic-bezier(0.22, 0.61, 0.36, 1)` / `cubic-bezier(0.34, 1.56, 0.64, 1)` | 幕布推拉与菜单四杠变形 / 抽屉与瓷砖滑出 / 徽章弹跳 |

### 核心 CSS 装饰与边框原语

- `.city-ink-card`：`border: 3px solid #141419; box-shadow: 4px 4px 0 #141419;`（主面板、重弹窗）
- `.city-ink-card-sm`：`border: 2.5px solid #141419; box-shadow: 2.5px 2.5px 0 #141419;`（子卡片、生态卡片、搜索下拉）
- `.city-ink-pill`：`border: 2.5px solid #141419; border-radius: 9999px; box-shadow: 2px 2px 0 #141419;`（悬浮胶囊控件）
- `.city-conic-frame`：通过 `@property --rotate-angle` 驱动 `conic-gradient` 16 秒步进旋转 `4px` 彩色外框；**不包含 `border-radius` 或外阴影**，由调用容器（例如 `DetailDrawer` 的 `rounded-[24px]` 或 `AvatarStage` 的 `.stage-conic-frame { border-radius: 30px; }`）各自控制圆角。
- `.city-hover-cycle`：通过 `@property --hover-color` 16 秒步进轮转 C-I-T-Y 四色，供放大镜定位钮、缩放按钮组与主行动胶囊 `--hover-color` 取色。

## 二、全局 Z-index 阶梯（强制约定）

所有叠加层遵循固定垂直顺序，避免右上角 `.city-top-shelf`（`70`）遮挡全屏弹窗或侧边抽屉自带的关闭按钮：

| CSS 变量 / 建议值 | 层级 | 对应组件 | 规则要点 |
| --- | --- | --- | --- |
| `--z-topbar-brand` | `45` | `.city-topbar-brand`（左上角 `CityLogo`） | 被菜单遮罩与全屏弹窗自然覆盖 |
| 站内浮动 HUD | `30–40` | `DetailDrawer` / `BottomControls` / `PathFinderBar` | 位于桌面视口中下方，留出 `top >= 72px` 不碰顶栏 |
| `--z-menu-overlay` | `65` | `CityMenuOverlay` | 低于 `--z-top-shelf`，让右上角变形 `×` 按钮始终可点关闭 |
| `--z-top-shelf` | `70` | `.city-top-shelf`（工具栏 + 姊妹站 + GitHub + 语言 + 菜单钮） | 在主视图与全屏菜单态保持可交互 |
| `--z-modal` | `80` | 全屏独立弹窗（如 `DirectoryModal`、`z-[80]`） | 自带独立右上角关闭 `×` 按钮，必须高于 `70` |
| `--z-lightbox` | `85` | 大图灯箱（如头像放大层、`z-[85]`） | 覆盖弹窗与细节抽屉 |
| `--z-drawer` | `95` | 滑出侧边抽屉（如 `HistoryDrawer`） | 从右滑入全高遮罩，完全接管屏幕焦点 |
| `--z-curtain` | `9999` | `CityLoadingCurtain` | 开场天蓝幕布，入场 `520ms` 后向右滑出并在 `1150ms` 卸载 |

## 三、两类页面原型尺度

### 原型 A：全屏沉浸式交互画布（参考 `city-social-map`）

- **根布局**：`html, body, #root { width: 100%; height: 100%; overflow: hidden; }`，无原生页面滚动条。
- **底纹**：画布容器挂载 `.city-confetti-bg`（C-I-T-Y 错落字母 `opacity: 0.42`，`420×420` `36s` 慢飘）。
- **四区 HUD 对齐**：
  - 左上 `top: 14px; left: 16px`：品牌徽章；左下：筛选 / 图例胶囊及向上展开卡（`drawerOpen` 在 `<640px` 手机端自动隐藏）。
  - 右上 `top: 0; right: 0`：`.city-top-shelf`（桌面端内嵌 4 枚模式/工具药丸；`<768px` 收敛成双态快切胶囊 ＋ 小图标）。
  - 右下：字符搜索药丸与竖排缩放三连胶囊（`city-zoom-btn--top / --mid / --bottom`）；**关键规约**：当右侧详情抽屉在桌面/平板打开时（`sm:` 宽 `364px` / `lg:` `384px`），右下 HUD `right` 自动移至 `392px / 412px` 并折叠轮播副标，确保搜索建议向上弹出时不被右侧卡片或键盘输入遮挡。

### 原型 B：工作室 / 图文专题页（参考 `city-avatar`）

- **根布局**：正常文档流，`.city-app { min-height: 100vh; display: flex; flex-direction: column; overflow-x: clip; }`，`main` 使用 `.studio-shell`（`max-width: 1080px; margin: 0 auto; padding: 86px 24px 36px;`）。
- **底纹**：使用 `body::before` `position: fixed` 平铺轻盈彩字纹样（推荐 `opacity: 0.24`，`42s` 慢漂），不干扰主体工作区与阅读。
- **双栏或索引节拍**：
  - 顶部紧凑引言条（`h1` 主标题紧接 `<CityDots />` ＋ 单句副标，右侧可放圆形参照/状态小胶囊）。
  - 工作区桌面 `grid-template-columns: minmax(320px, 440px) minmax(0, 1fr)`，`gap: 28px`；`<=900px` 收为单栏并将舞台列居中限宽 `480px`。
  - 底部必须挂载共享 `<CityFooter />`。

## 四、响应式断点与动效降级

- `<= 1024px`（中平板）：`city-shell.css` 自动隐藏 `.city-sister-pill`，避免四按钮站点导航在 iPad 竖屏下挤压左上角品牌药丸。
- `<= 900px`（窄平板）：全屏菜单 `.city-menu-hero` 从左文右瓷砖双列改为上下居中单列；工作室双栏改为单栏。
- `<= 720px`（大屏手机）：菜单内生态站对比网格 `.city-ecosystem-grid` 转为单列。
- `<= 640px`（常规手机）：左上角 `.city-wordmark` 缩小至 `svg height: 22px`，`.city-top-shelf` 圆角收敛至 `18px`，菜单按钮缩至 `34×34px`，GitHub 圆钮缩至 `30×30px`；站点自定义次要文字标签（如 `galleryBtn` 文案）隐藏仅留图标与数量徽标；`.city-menu-tiles` 转为单列。
- `<= 359px`（超窄防溢出）：隐藏 `.city-github-btn`（用户仍可在全屏菜单生态卡或页脚点击 GitHub 原仓），彻底保证零横向溢出。
- `@media (prefers-reduced-motion: reduce)`：立刻停止背景平铺漂移、渐变旋转、颜色循环、`MiminekoMascot` 晃动及点跳动画，`CityLoadingCurtain` 不等待滑出直接跳过。
