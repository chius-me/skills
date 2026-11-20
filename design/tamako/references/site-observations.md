# 《玉子市场》官网双世代观察记录

取样日期为 2026-11-20，使用 REA（`rea@6.9.0` `capture_browser_scenario`，Chromium `158.0.8127.37`）对 `https://tamakomarket.com/` 进行受控回放与静态资源采样，覆盖 **2013 年 TV 动画经典门户（`/` 及 9 个主要内页）** 与 **2023–2024 年 10 周年特设站（`/10th-event/`）**。以下事实严格区分「原站观测结果」与「跨项目复用建议」。

## 一、双世代站点结构与视觉对照（实测观测）

| 观察维度 | 2013 TV 动画官网（`/`、`common.css`、`top.css`） | 2023–2024 十周年特设站（`/10th-event/`、`main.css`、`top.css`） |
| --- | --- | --- |
| **视口与网格** | `meta viewport: width=980` 固定双栏架构；左栏导航 `170px`（内含 `150×59px` 菜单项），右栏主视觉 `536×773px`（前景溢出 `560×795px`）配右信息栏 `250px`；内页 `#mainContent` 固定 `810px`（内容区 `750px` + 左右 `30px` 内距）。 | 响应式 `width=device-width, initial-scale=1`；导航限宽 `840px`；白色内容岛 `.contentbox` `max-width: 960px`（`width: 90%`）、内文 `.content-wrap` `max-width: 800px`，设置 `1320px` / `834px` / `768px` 断点。 |
| **背景与纸面** | 和纸点纹平铺 `/img/bg.jpg`（`16×16` 主色 `#FBF8F1` / `#F4F1E6`）；顶部 `245px` 浅薄荷/淡粉/浅黄斜纹彩篷 `/img/globalHeader/bg.jpg`（`#DBFDF6` / `#F9EDED` / `#F3FBD7`）；内页卷轴由上 `#FAF4E0`、中 `#EFE9D4`、下 `#FAF4E0` 拼接。 | 整体纯色糯米象牙底 `#FDFFF2` 配合 `.contentbox` 纯白 `#FFFFFF` 圆角岛（桌面 `border-radius: 30px`，手机 `15px`）；底部叠 `1708px` 高大背景插画（`<=768px` 切换移动端专属图）。 |
| **字墨与主色** | 字体栈 `Hiragino Maru Gothic Pro` / `メイリオ`（基准 `12px`，`line-height: 1.5`）；内页正文焙茶棕 `#8E4C28`、副信息 `#BA8860`、标题与链接樱粉 `#EE86A7`、强调红 `#FF5B5B`；首页更新栏独立冷色系 `dt #224C89` / `dd #184070` / 链接 `#428FDB`。 | 引入 Google Fonts `Zen Maru Gothic` + `Noto Sans JP`（`500/700/900`，启用 `palt`）；正文豆沙褐红 `#993338`、主强调与标题樱珊瑚 `#FF7B82` / `#F66E75` / `#FF979D`，按场次/商品启用黄豆杏 `#F69E6E`、薄荷青 `#31CBB7`、天蓝 `#0EB2FF`、艾草绿 `#93D548`、出町座双蓝 `#41A8DD` / `#2E62A2`。 |
| **开场与导航交互** | 首次访问经 `sessionStorage.FirstTime` 触发 `#loadingWrap` + `856×783` `#intro` 幕布，依次淡入两句竖排宣传语（`あの娘はかわいい` `65×350`、`もち屋の娘。` `65×245`）并设右上 `100×60` `#skip` 按钮与顶栏 `#restart` 重看按钮；左侧悬停 14 枚菜单时，顶部 `#mochi` 德拉看板逐条切换气泡台词。 | 白色全屏 `#overlay` 在 `load` 后 `800ms` 淡出；固定磨砂粉白顶栏 `rgba(255,249,250,0.9)` 配 `2px solid #FF7B82` 底线，滚动超 `100px` 压缩内距（`20px -> 10px`）；`<=768px` 转为 `#FFB1B5` 全屏抽屉，顶部三道白杠平滑旋转合为 `×`。 |
| **页脚与回顶** | `980×255px` 奶黄商店街剪影 `/img/globalFooter/bg.png`（`#F8F2DE` / `#FFFCE7`），右上 `.goToTop`（`85×70px`）悬停时 `background-position-y` 由 `20px` 上移至 `0`（`0.2s ease-out`），提示「ページトップへお連れしよう」，附电影横幅与京阿尼徽标。 | 底部切换桌面/手机专属云朵背景图（`footer-bg.webp` / `footer-bg-sp.webp`）；圆形描边 SNS 钮（`2px solid #FF7B82`）；右下固定悬浮 `69×62px` `pagetop.webp` 回顶按钮（滚动超 `500px` 淡入）。 |

## 二、REA 证据与取样边界

本次全部观测均有下列 REA `capture_browser_scenario` 证据链支撑（各页采样均在受控无头 Chromium 中完成，且受 `reduced_motion: "reduce"`、第三方社交脚本未完成加载或单个大图片超出 `65536` 字节正文缓存上限等场景采集约束限制；跨项目复用需按现代无障碍对比度与响应式结构改写，不可直接照搬 `width=980` 与图片字替文本）：

| 采样范围 | REA Evidence ID | 关键验证内容 |
| --- | --- | --- |
| 首页与核心脚本/样式 | `ev_44981e2f1a0ca4daf25e764b54356100bd55d4b40c3b1eaad808a61dd8ba21ef` | 完整 DOM、`reset.css`、`common.css`、`top.css`、`prettyPopin.css`、`common.js`、`top.js` 与首页 30+ 切图尺寸/色板 |
| 跳过开场 → 活动页 | `ev_d49435e11c2d48b31c23f5e78fb445a5afe5c07709fa2a00c6b232a7b8f19322` | 实测点击 `#skip` 跳过幕布并点击 `#comment-05` 跳转 `/event/`，获取 `event.css` 与活动页可访问性树 |
| 商店街地图 `/map/` | `ev_17a068c981d829a40d11b3fb1221451bed5e571e6b93e7d8f820ba0c5717e70f` | `map.css`、`lower.js`、23 枚热点定位及桌面截图（SHA-256 `8c652793a3fd81f517b4d3c732be2dc20a65ec7af0c964b2f01b3a160fd49617`） |
| 人物图鉴与关系图 | `ev_4d4a12e076c52aefe1aad91e94d41f0e2bc022f890098db050174b02474e0994`、`ev_d839001f486f3efc9d7865d02f04a3fe4a8da1e3b8a3698839f0821d2f7f52ab` | `/character/` 放射图与 `/character/1/` 立绘轮播、表情切换脚本及 `/message/` 留言板实测（图鉴截图 SHA-256 `63f0a280b9054ad1b661deb7877ea436936035fcb0bcd507cebbbd062b0bed54`） |
| 故事分集 `/story/` | `ev_f17bf22164f1a6f1ad1a48d8f1956e731f4083c694ab30570e5af4a24fd5bd68` | `story.css`、`story.js` 的 Hash 切换、切图边框（`#EDD18F` -> `#DE9132`）与三列主创短评 |
| 资讯/日誌/放送/广播/特别企划 | `ev_9d2b546df18259f9f51365569666bf0825b802affde272618209798751ffe43f`、`ev_b97821e53c012f494a84966c6393099d5582d36cb0c1f72d4259b384e1d34a26` | 多步点击走查 `/news/`、`/diary/`、`/message/top/`、`/staff-cast/`、`/onair/`、`/special/`、`/radio/` 及各页独立 CSS |
| 十周年特设站 `/10th-event/` | `ev_20218a6cae2d8f6b0e0454019ef77985362bcb84afeaf193838831349918ad1b` | `10th-event/css/common.css`、`main.css`、`top.css`、`main.js` 及完整 DOM/截图（SHA-256 `86676cd32b68eeddc3ae1d498532fc8f2a2dd0177868753d7f7cfd4e95fae8a3`） |
