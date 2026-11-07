# 术语对照与语意化译例参考

本文件供 `blog-localization` 技能在需要查阅具体词汇对照或译例时读取。

---

## 1. 专有名词标准写法与易错词表

| 常见误写 / 病句 | 标准写法 | 说明 |
| --- | --- | --- |
| `Macos` / `MacOS` | `macOS` | 首字母小写 `m`，后接大写 `OS` |
| `Jetbrains` | `JetBrains` | `B` 大写 |
| `GitHub Action` / `Forgejo Action` | `GitHub Actions` / `Forgejo Actions` | 产品名为复数 `Actions` |
| `ArgoCD` | `Argo CD` | 官方名称中间带空格 |
| `opencode` | `OpenCode` | 正文提及工具名时使用驼峰大写 |
| `Netbird` | `NetBird` | `B` 大写 |
| `Sumatra PDF` | `SumatraPDF` | 官方名称连写 |
| `Last.FM` | `Last.fm` | 后缀 `fm` 小写 |
| `Citypop` | `City Pop` | 两个单词，首字母大写 |
| `Paul Mccartney` | `Paul McCartney` | `Mc` 后紧跟大写 `C` |
| `GPT 5.4` | `GPT-5.4` | GPT 系列模型名带连字符 |
| `你好 HUGO` | `你好，Hugo` | Hugo 非首字母缩略词，不高亮全大写 |
| `首言` | `前言` | 中文无“首言”一词 |
| `长达 3 年的调教` | `长达 3 年的调校` | 软硬件/机械调整用“调校” |
| `届时 GitHub Copilot 还是很香的` | `那时候 GitHub Copilot 还是很香的` | “届时”仅用于将来时，回忆过去用“那时候／当时” |
| `控制层面` | `控制平面（Control Plane）` | 网络与分布式架构标准术语 |
| `不运行来宾时` / `21 个来宾` | `不运行任何 VM 时` / `21 个实例` | PVE 中的 Guest 在中文里称作“VM 和容器”或“实例” |
| `动画社 [京都动画]` | `动画公司[京都动画]` | “动画社”在中文里指学校社团 |

---

## 2. 简繁（`zh-CN` → `zh-TW`）核心术语对照表

| 简体中文 (`zh-CN`) | 台湾正体 (`zh-TW`) | 避坑说明 |
| --- | --- | --- |
| 博客 | 部落格 | |
| 软件 / 程序 / 应用 | 軟體 / 程式 / 應用程式 | |
| 硬件 / 内存 / 硬盘 / U 盘 | 硬體 / 記憶體 / 硬碟 / USB 隨身碟 | 硬碟量词用“顆”，NVMe SSD 用“條”或“顆” |
| 服务器 / 宿主机 / 虚拟机 | 伺服器 / 宿主機 / 虛擬機 | **禁用**“客體”指代 Guest，用 `VM`、`VM 和容器` 或 `執行個體` |
| 物理机 | 實體機 | |
| 电源（主机电源） / 机箱 / 盘位 | 電源供應器 / 機殼 / 槽位 | 如：八槽位機殼 |
| 笔记本（电脑） / 游戏本 | 筆電 / 電競筆電 | |
| 显示器 / 屏幕 / 系统托盘 | 螢幕 / 螢幕 / 系統匣 | |
| 包管理器 / 插件 / 镜像 | 套件管理器 / 擴充套件 / 映像檔 | |
| 运行时 / 线程 / 进程 | 執行環境 (Runtime) / 執行緒 / 程序 | |
| 运维 / 持续集成 / 仓库 | 維運 / 持續整合 / 儲存庫 | |
| 打洞 / 中转 | NAT 穿透 / 中繼 | |
| 自托管 / 对象存储 | 自架（或自託管） / 物件儲存 | |
| 光猫 / 软路由 | 數據機（光貓） / 軟路由 | |
| 刷屏 | 洗版 | 如：信箱被警報洗版了 |
| 考研 | 考研究所 | **禁用**死板的“研究所入學考試” |
| 计算机专业 / 本科 | 資訊相關科系 / 大學（或大學部） | |
| 岗位 / 二面 / 面经 | 職缺 / 二面 / 面試心得 | |

---

## 3. 中英（`zh-CN` → `en-US`）技术术语与跨文化表达对照

| 中文原词 | ❌ 常见机翻 / Chinglish | ✅ 地道美式英语表达 |
| --- | --- | --- |
| 大模型 | large models | **LLMs** / **large language models** / **foundation models** |
| 大模型训推平台 | large model train-push platform | **LLM training and inference platforms** |
| 断点续传（训练） | breakpoint resume | **checkpoint resuming** / **resuming from checkpoints** |
| 打洞 | hole punching | **NAT traversal** |
| 软路由 | soft router | **OpenWrt router** |
| 光猫 | optical cat | **ONT (fiber modem)** |
| 监控级机械硬盘 | mechanical monitoring disk | **surveillance HDDs** |
| 空转烧 CPU | burning CPU | **pegging a physical core at 100%** / **runaway thread** |
| 天选 4 笔记本 | Tianxuan 4 laptop | **ASUS TUF Gaming (Tianxuan 4) laptop** |
| 211 院校本科在读生 | 211 college undergraduate | **an undergraduate at a Project 211 university** |
| 2027 届 | 2027 session | **Class of 2027** |
| 考研 | postgraduate entrance examination | **the graduate school entrance exam**（简写 **grad school exam**） |
| 刷 LeetCode | brush LeetCode | **grinding LeetCode** |
| HC 有限 | HC is limited | **headcount was tight** |

---

## 4. 英文语意化重塑示例（Before vs. After）

### 示例 1：自嘲与冷幽默
- **中文原稿**：
  > 博客的文章是懒得写的，但各种博客系统都要尝一下的。经历了 WordPress、Halo、Typecho、Ghost 后，还是选择了 **Hugo** 这款静态站点生成器。
- **❌ 机翻/平淡**：
  > Blog posts are lazy to write, but various blog systems must be tried. After experiencing WordPress, Halo, Typecho, and Ghost, I still chose **Hugo**.
- **✅ 语意化重写**：
  > I can never be bothered to actually write blog posts, yet I still have to try out every blogging platform out there. After tinkering with WordPress, Halo, Typecho, and Ghost, I finally settled on **Hugo**, a static site generator.

### 示例 2：口语比喻与网络梗
- **中文原稿**：
  > 直到今天下午，某块硬盘又开始反复横跳。真后悔上次事发时没有记录到底是哪块硬盘一直在那“蹦迪”，这次吸取教训，赶紧记录下来……
- **❌ 机翻/平淡**：
  > Until this afternoon, a hard drive started jumping back and forth again. I regretted not recording which drive was dancing last time, so I learned the lesson to record it now...
- **✅ 语意化重写**：
  > Until this afternoon, when a drive started flapping all over again. I really kicked myself for not writing down which drive was throwing a rave in the bay last time—so lesson learned, I'm documenting it properly now…

### 示例 3：硬件折腾与生活吐槽
- **中文原稿**：
  > 光看数量好像也不算特别夸张，但这些机器一天到晚开着，200W 就有点肉疼了，而且房间里还会多一个稳定的热源。
- **❌ 机翻/平淡**：
  > Looking at the number, it is not too exaggerated, but these machines are on all day, 200W hurts my flesh, and there is a stable heat source in the room.
- **✅ 语意化重写**：
  > Four boxes might not sound like much on paper, but when they run 24/7, 200 W starts to sting on the power bill—not to mention turning my room into a space heater.
