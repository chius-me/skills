# 反模式、质量门禁与评审规范

用于新站开发前排雷、同步改造后验收，以及独立评审任何 `CITY` 风格网站。

## 一、CITY 网站高频反模式避坑表

| 严禁做法（Anti-Pattern） | 破坏了什么规范 | 正确替代方案 |
| --- | --- | --- |
| **写进 `city-shell/` 的 Tailwind 工具类** | `city-avatar` 与纯 CSS 子站没有 Tailwind 构建插件，直接复制会丢样式或样式崩溃 | `city-shell.css` 与 `components/city-shell/` 100% 使用纯语义 `.city-*` CSS 类 |
| **模糊黑灰大阴影 / 玻璃紫霓虹渐变** | 与平涂赛璐珞画风和 `#141419` 漫画墨线水火不容 | 使用 `2.5px–3.5px` 实墨描边配等大硬边偏移阴影 `2px–6px 0 #141419` |
| **全屏滥用旋转彩虹光环 `.city-conic-frame`** | 多个卡片同时慢旋造成视觉晕眩与焦点失焦 | 仅留给全页 **唯一主舞台或当前细节抽屉**，其余使用静态墨框 |
| **“盒中套盒”粗墨嵌套** | 大卡片内部的子区块又画 `2.5px` 黑实线配硬投影，页面显得拥挤噪杂 | 内部次级区块用浅灰 `1.5px–2px` 细线（`--color-grey200`）或 `--color-cream` `#faf6ee` 底色 |
| **抽屉遮挡搜索建议或缩放控件** | 像打开详情卡时底层搜索自动补全被右边抽屉盖住一半 | 右侧抽屉开启后，左下/右下控件自动调整 `right` 偏移让出抽屉宽度，或窄屏隐藏次级控件 |
| **弹窗 `z-index` 低于右上控制托架（`70`）** | 全屏弹窗自带的右上关闭 `×` 被 `.city-top-shelf` 压在底下点不到 | 遵守阶梯：`CityMenuOverlay` (`65`) < `.city-top-shelf` (`70`) < 全屏弹窗 (`80`) < 灯箱 (`85`) < 侧边抽屉 (`95`) |
| **缺少 GitHub 原仓或姊妹站直链** | 网站与源代码、系列作品彼此孤岛化 | `CityTopShell` 放 `.city-github-btn` + 桌面 `.city-sister-pill`，`CityMenuOverlay` 渲染完整生态站卡片，`CityFooter` 与双语 README 双向补全 |
| **手机窄屏顶栏溢出 / 碰撞** | `375px` 或 `640px` 下四tab或双行文本把右上角挤出屏外 | `<=1024px` 隐藏 `.city-sister-pill` 退入全屏菜单；`<=640px` 缩字标 `22px`、隐次要标签、降圆钮尺寸；`<=359px` 隐 `.city-github-btn` 杜绝横向滚动条 |

## 二、五维交付核对单

交付任何新建站或双站统一改造前，逐项验证：

### 1. 共享壳层与工程一致性（Critical）
- [ ] `src/styles/city-shell.css` 与 `src/components/city-shell/*` 与基准站（`city-social-map` / `city-avatar`）**零差异**（可用 `diff -ru` 校验）。
- [ ] 没有遗留旧版分散的 `CityLogo.tsx` 或重复菜单/页脚组件；站点 CSS 顶部干净 `@import` 共享 `city-shell.css`。
- [ ] `tsc -b` 与 `vite build` 严格通过，无类型错误或未使用变量阻塞构建。

### 2. 生态互链与仓库溯源（Critical）
- [ ] 桌面端顶栏一眼可见 **姊妹站直达胶囊**（`>1024px`）与 **本站 GitHub 原仓图标按钮**（`>=360px`）。
- [ ] 展开四色变形菜单 `CityMenuOverlay`，可清晰看到所有已登记站点的名称、简介、线上访问链接与 GitHub 仓库链接。
- [ ] 流式站点底部挂有 `<CityFooter />`，各仓库 `README.md` 与 `README.zh.md` 均互相链接了姐妹站线上域名与 GitHub 仓库。

### 3. 视口适配与不碰撞 HUD（Critical）
- [ ] 在桌面 `1440×900`、平板 `768×1024`、常见手机 `390×844`（`375×812`）与窄屏 `320px` 下检查无横向滚动溢出（`scrollWidth <= innerWidth`）。
- [ ] 左右两块顶栏（`.city-topbar-brand` 与 `.city-top-shelf`）在所有断点均互不重叠、不折行变形。
- [ ] 若存在右侧抽屉或全屏弹窗，`×` 关闭钮不被 `.city-top-shelf` 挡住，右下搜索框与缩放按钮能智能退让。

### 4. 三语体系、对比度与键盘无障碍（High）
- [ ] `中 / EN / 日` 切换即时覆盖壳层菜单、生态卡片、页脚、弹窗及空状态。
- [ ] 所有图标钮（GitHub 按钮、四杠菜单、关闭圆形钮）均有当前语言 `aria-label` 与 `:focus-visible` 焦点反馈；菜单与抽屉支持 `Escape` 与点击外遮罩关闭。
- [ ] C-I-T-Y 浅彩底上的文字默认使用深墨 `#141419` 保证可读对比度，不用浅白字贴浅黄 `#F7B647` / 浅绿 `#99CB77`。

### 5. 动效克制与元数据完整（Medium）
- [ ] `@media (prefers-reduced-motion: reduce)` 下自动静止飘字背景、旋转边框、Mimineko 摇晃与滑出幕布。
- [ ] `<title>`、`meta description`、`og:url`、`canonical`、`theme-color="#f7b647"` 与家族 `favicon.svg` 配置准确。

## 三、页面评审输出模板

受托审查既有网站时，优先实测运行界面（如无法启动服务，先静查组件树、CSS 层叠与 `city-shell` diff，再声明实测范围），按以下结构报告：

```markdown
## CITY 网站设计评审 — <站点名称或 URL>
**核验范围**：视口 `1440 / 1024 / 768 / 390 / 320` · 语言 `zh / en / ja` · 壳层同步情况

### Blocker（功能不可用、弹窗关闭钮被遮挡、横向溢出或互链缺失，必改）
- [现象与文件行号] → [违背的 CITY Web 规范] → [具体改法]

### High（偏离视觉 Token、硬投影体系、抽屉避让或共享壳层漂移，建议发布前修复）
- ...

### Medium / Nit（间距、微文案三语对齐、动效降级或 README 补全）
- ...

### 做得好的既有设计（迭代中务必保留）
- ...
```
