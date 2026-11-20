# 《CITY THE ANIMATION》官网观察记录

取样日期为 2026-11-20，范围包含第二版主视觉首页、菜单、九个主导航栏目及代表性详情。网页结构和 CSS 用于核对版式；另在 1280 × 800 与 390 × 844 的浏览器视口中对照新闻列表、新闻详情、配信、放送时间表及插画页脚。另在 1100px 宽视口检查第 1 集、人物图鉴、制作名单、影片目录、片头曲、碟片第 1 卷、专题目录、制作手记与找不同的正文区域。以下记录的是原站，主文件中的维修铺示例、静态版面与减少动态效果方案属于跨项目应用建议。

| 观察位置 | 可复核的细节 |
| --- | --- |
| 主题 | 作品介绍用笑意、爱意和感伤并置来讲居民的日常。首页画面把列车、商店街、海滩、球场和许多小人物并排展开，把“认识这里的人”变成一次找人游戏。[作品介绍](https://city-the-animation.com/story/introduction/) · [首页](https://city-the-animation.com/) |
| 首页取景 | 桌面实看为左下字标与社交入口、右上菜单和资讯、右下找人与缩放。390 × 844 视口里字标和社交入口移到左上，底部保留查找。两种尺寸都只显示大图的一部分。HTML 在 960px 分界选择 3940 × 2774 或 2048 × 1442 的图，每个居民都有对应的两组坐标。[首页](https://city-the-animation.com/) · [首页样式](https://city-the-animation.com/_assets_kv2/css/top.css) |
| 查找与运镜 | REA 浏览器回放点击“下一位”和放大镜，结束时选中「にーくら」。另在 390 × 844 视口读取实际变换，换名后画面保持原位，定位后比例从约 0.585 变为 1 并移动到人物处。脚本中定点移动采用 1000ms 缓动，缩放按钮采用 150ms 过渡，拖动时直接跟手。[首页交互脚本](https://city-the-animation.com/_assets_kv2/js/top.js) |
| 品牌与菜单 | 公共样式把标志的四个字母分别定义为黄、粉、绿、珊瑚色；正文为 M PLUS Rounded 1c。手机菜单实看为半透明白底，黑边四色按钮排成两列，底图依稀可见。主标题和栏目字标多处以图形资源呈现。[公共样式](https://city-the-animation.com/_assets_kv2/css/common.css) · [首页](https://city-the-animation.com/) |
| 通用刊头与底纹 | 三幅横景在 30 秒循环中错开淡入淡出，宽屏字标与画面分栏，窄屏字标叠入同一格。浅色碎字纹样在桌面以 800px、窄屏以 400px 平铺，30 秒斜移。白色内容面板的上缘和右缘露出四色轮换的细线。[内页样式](https://city-the-animation.com/_assets_kv2/css/lower.css) |
| 栏目、段落、页脚 | 栏名下有副标题与四点；播出等长页的段落小标题居中，下接更长的点列。页尾从波浪白边过渡到城市远景、树林和前景红按钮。公共脚本将按钮点击与人物升空、景层错动和回到页首联动。新闻采用简单版权页脚。[播出页](https://city-the-animation.com/onair/) · [内页脚本](https://city-the-animation.com/_assets_kv2/js/lower.js) |

## 栏目与取样范围

| 设计问题 | 核对的页面与资料 |
| --- | --- |
| 没有大幅插画时怎样传达品牌，长标题和时刻表怎样在手机上重排 | [新闻目录](https://city-the-animation.com/news/)、[公告详情](https://city-the-animation.com/news/?id=62)、[播出页](https://city-the-animation.com/onair/)。复用方式见[新闻与日程](news-and-schedule.md)。 |
| 叙事、图鉴和署名如何分配图文比重 | [分集与介绍](https://city-the-animation.com/story/)、[人物](https://city-the-animation.com/character/)、[职员](https://city-the-animation.com/staff/)与[声优](https://city-the-animation.com/cast/)。各入口及代表性详情见[故事、人物与署名](stories-and-people.md)。 |
| 形状相似的缩略图如何表达不同的下一步 | [影片](https://city-the-animation.com/movie/)、[音乐](https://city-the-animation.com/music/)、[碟片](https://city-the-animation.com/bddvd/)。媒体、艺人和各卷的排版见[影音与商品](media-and-products.md)。 |
| 如何在一个栏目内容纳不同长度和玩法 | [SPECIAL 目录](https://city-the-animation.com/special/)列出 11 个专题入口。活动、制作手记、画作、赠品与小游戏的变体见[特别企划](special-features.md)。 |

REA 回放的 Evidence ID 为 `ev_b5bb5328d8abb407354641fbce1fdf9fcc91440059580b73f0f783e150104888`，记录此次点击与最终可访问性树。画面、配色和取景判断另据桌面浏览器截图、移动视口模拟及公开 HTML/CSS/JS。纸纹和笔触是对成像效果的描述，原画媒材与制作软件未核实。
