# 两站参考

这是两站的实现基准。色值可作为同系列站点的起点；尺寸反映当时的页面内容，按新页面的文字与目标调整。

## 共用配色

| 角色 | 浅色 | 深色 |
| --- | --- | --- |
| 页面背景 | `#fdfcfb` | `#202530` |
| 正文 | `#292c30` | `#e1e5ed` |
| 次级文本、元信息 | `#6b7076` | `#a4adbb` |
| 链接、交互强调 | `#256786` | `#eab38b` |
| 链接悬停 | `#124c68` | `#ffd1ad` |
| 句点、井号等标记 | `#b24c37` | `#eab38b` |
| 分隔线、边框 | `#e5e4e1` | `#3c4350` |
| 按钮、搜索框、内联代码等柔和表面 | `#f2f1ee` | `#2a303c` |
| 博客代码块表面 | `#f5f4f1` | `#252c38` |

参考交互细节：正文链接用 1px 下划线、约 `.25em` 偏移；键盘焦点用 2px 强调色虚线、默认 5px 外偏移。细边线用于辅助分组，若控件边界仅靠它标识，按实际背景提高对比。

## 链接页：chius.me

- 外容器最大 `37.5rem`，关键内容沿中轴排列。圆头像 `8rem`，下方是粗体紧字距站名；站名约桌面 `3.05rem`、窄屏 `2rem`。
- 链接宽 `18.75rem`（不超过容器），最小高 `3rem`，间隔 `1rem`。文字 500 字重，配 `1.25rem` 单色图标；1px 边框、4px 圆角。悬停切纸底、强调色边框与文字，可见反馈来自色差。
- 页脚前的细线与链接同宽。可用细噪点赋予纸感，原站采用固定 SVG 背景、透明度约 `.045`；头像是主要图像。配色跟随系统。
- 参考：[线上页面](https://chius.me/) · [纸色、字体与交互 CSS](https://github.com/chius-me/chius.me/blob/b575efa472afb582290e21cf7805ff14a6b6758e/public/css/paper.css) · [容器和基础尺度](https://github.com/chius-me/chius.me/blob/b575efa472afb582290e21cf7805ff14a6b6758e/public/css/style.css)

## 博客：chius.cc / Chipaper

- 阅读外栏最大 `48rem`；桌面两侧至少 `1.5rem`，窄屏约 `1.25rem`。页头、引言、列表、正文和页脚沿同一栏对齐。搜索、主题和语言可合成一组细线控件，社交链接可用小号线性图标。窄屏让导航换行，维持明确的触控目标。
- 首页标题约 `1.85–2.5rem`（随宽度变化），最近文章分区标题约 `1.2rem`；文章列表的标题约 `1.15rem`、元信息 `.75rem`、摘要 `.9rem`，条目间距约 `2.5rem`。分区可用砖红 `#` 作标记，日期与阅读时间用点分隔。正文约 `1.025rem`、行高 `2`；博客底色是平面的。
- 拉丁用 Google Sans Code，中文用 Sarasa Mono SC（更纱等宽黑体），其次用系统中文字体。按真实内容判断是否需要分段加载 CJK 字体。可以借用薄线框可折叠目录、侧线引文、低圆角代码块和虚线分隔；内容需要时才加。主题默认随系统，手动选择可记忆。
- 参考：[线上页面](https://chius.cc/) · [Chipaper 排版与双主题 CSS](https://github.com/chius-me/chipaper/blob/fdc1c03432268b9ce93590bb55af37a761b6a2ae/assets/css/paper.css) · [首页模板](https://github.com/chius-me/chipaper/blob/fdc1c03432268b9ce93590bb55af37a761b6a2ae/layouts/home.html) · [文章列表模板](https://github.com/chius-me/chipaper/blob/fdc1c03432268b9ce93590bb55af37a761b6a2ae/layouts/partials/paper/post-list.html)
