---
name: grok-collage-broll
description: >
  将约 5–6 秒口播文稿、观点句或抽象概念做成高级 editorial
  halftone paper-collage / 半调纸拼贴 B-roll。用户说“collage b-roll”
  “纸拼贴 b-roll”“半调拼贴”“拼贴风格配画面”“用这段文稿做拼贴动画”
  “grok-collage-broll”，或希望把一句文稿转成拼贴视觉隐喻时，必须使用此
  skill。强制三阶段审批：Gate 1 只提视觉隐喻并停下；用户确认后 Gate 2 用
  Grok Build image_gen 生成彩色拼贴静帧 + contact sheet 再停下；静帧确认后
  Gate 3 默认用 Grok Build reference_to_video（纯色空场 + 已确认静帧）做
  assemble-from-empty 组装动画；失败或需保底时再退到 image_to_video。
  默认不走 Gemini Omni / Veo / GEMINI_API_KEY。
---

# grok-collage-broll

把一句约 5–6 秒的口播压成一个 sharp visual idea，再做成高级编辑风纸拼贴组装动画。

默认链路（Grok Build 原生）：

1. 只设计视觉隐喻，等待用户确认（**Gate 1 停下**）
2. 用 Grok Build `image_gen` 只生成最终静帧 + contact sheet，等待用户确认（**Gate 2 停下**）
3. 静帧通过后，默认用 Grok Build **`reference_to_video`**（空场 + 已确认静帧）生成 assemble-from-empty 视频并完成 ffmpeg QA（**Gate 3**）

> 路径对照见 `experiments/scheme-compare/`：默认 **C `reference_to_video`**（组装 + 末帧贴合优于空场 i2v / 多镜头 / 终态 hold）。

这两个确认闸门是工作流的一部分。它们让用户把注意力放在审美和方向上，同时避免错误隐喻或错误静帧直接消耗视频生成成本。

## 首次使用：环境自检

每次触发本 skill 时，进入 Gate 1 之前先运行自检脚本：

```bash
bash <本skill目录>/scripts/check_setup.sh
```

全部通过则直接开始 Gate 1，不要向用户重复配置信息。任何一项失败时，视为首次使用：不进入 Gate 1，先向用户输出下面的配置指南（只列出缺失项），等用户确认配置完成后重新自检。

### 配置指南（按缺失项输出）

1. **不在 Grok Build 环境 / 没有 image_gen / reference_to_video**
   Gate 2 静帧依赖 Grok Build 内置 `image_gen`；Gate 3 默认依赖 **`reference_to_video`**（保底可用 `image_to_video`）。在其他 agent 环境下运行时，向用户说明需要 Grok Build，或由用户手动提供静帧/视频后从对应闸门继续。

2. **ffmpeg / ffprobe 缺失**
   macOS：`brew install ffmpeg`；Debian/Ubuntu：`sudo apt install ffmpeg`。
   用于空首帧、去音轨、contact sheet、尾帧对照。

本 skill **不需要** `GEMINI_API_KEY`、`google-genai`、Python 视频客户端，也不依赖 Codex 专用 image_gen。

## 强制审批协议

### Gate 1：隐喻确认

收到文稿后，先提视觉隐喻，**不生成图片、不生成视频、不调用 image_gen / image_to_video / reference_to_video**。

向用户交付每条的：

- 核心意思
- 情绪
- 一句话视觉命题
- 3–6 个关键物件
- 建议底色与局部点色
- 预期组装顺序

然后**明确停下**，等待用户回复“可以”“通过”“全部通过”或给出逐条修改意见。

如果用户只确认部分编号，**只让通过的条目进入 Gate 2**；未通过条目继续修改隐喻。不得把未确认条目推进到静帧或视频。

### Gate 2：静帧确认

隐喻确认后，才写 visual spec 和 imagegen prompt，并用 Grok Build **`image_gen`** 生成最终静帧（`aspect_ratio: "9:16"`）。

把原图保存到项目目录，生成带编号的静帧 contact sheet，向用户展示并**再次停下**。此阶段**仍然不调用** `image_to_video` / `reference_to_video`，也不生成视频。

如果用户只确认部分静帧，**只让通过的条目进入 Gate 3**；需要修改的静帧先重生（可用 `image_gen` 或 `image_edit`）并重新确认。

### Gate 3：视频生成

静帧确认后，不再询问使用哪个视频模型，**默认**走：

| 优先级 | 场景 | 工具 | 说明 |
|--------|------|------|------|
| **1 · 默认** | assemble-from-empty + 末帧贴合 | **`reference_to_video`** | `images`: 纯色空场 + 已确认静帧；`aspect_ratio: "9:16"`；组装 prompt |
| 2 · 保底 | 末帧 QA 失败后仍要可用成片 | `image_to_video` 以**确认静帧**为 source | settle/hold，几乎不动；**不是**主路径 |
| 3 · 不推荐默认 | 仅空场 `image_to_video` | `image_to_video` 空场 source | 组装过程可能好看，但末帧常整张重画，**不要默认** |

**不要**调用 Gemini Omni Flash、Veo、`generate_video.py`、`GEMINI_API_KEY` 或 `google-genai`。

## 成功标准

- 一句话只表达一个清晰隐喻
- 同一批画面有统一设计语言，但不强制全部蓝底
- 背景是强烈、平坦、均匀的色场，可按语意变化
- 主体以黑白 halftone photographic cut-outs 为骨架
- 关键卡片、按钮、胶片、规则册等允许使用红、黄、青、橙、紫、奶油白等彩色纸张
- 所有纸片有清晰裁切边、奶油白 keyline、低透明度柔和阴影和纸张颗粒
- 动作是 assemble-from-empty，而不是轻微漂移、晃动或慢 zoom
- 无字幕、无口播全文、无 logo、无水印、无 UI
- 默认交付 9:16、**6 秒**（Grok 视频工具仅支持 6 或 10；默认 6，最接近原 5s）、无声 MP4
  - 优先 `resolution_name: "720p"`；交付前用 ffmpeg 去音轨
  - 用户明确要求更长时用 `duration: 10`

## 什么时候不要用

- 需要精确控制图层、遮挡、镜头穿越或可编辑时间线：改用分层动画工具（如 HyperFrames 类 HTML 渲染视频方案）
- 只需要视频提示词，不需要生成成片：直接写 prompt 即可，不用走本流程
- 需要真实人物产品广告或口播演员：不要走本拼贴流程
- 用户明确要可逐层修改的透明素材：本 skill 默认不拆透明图层

## 默认项目目录

所有中间产物与成片写在**当前工作区**根目录下的隐藏文件夹（不要写到用户 home 的 `~/hyperframes-projects/`）：

```text
<workspace>/.hyperframes-projects/YYYY-MM-DD-collage-broll-标题/
```

规则：

- `<workspace>` = 当前 Grok 会话工作区根（即 git 仓库根 / 打开的项目根），用绝对路径创建
- 首次使用先 `mkdir -p <workspace>/.hyperframes-projects`
- 子目录名用北京时间 `Asia/Shanghai`：`YYYY-MM-DD-collage-broll-<短标题 slug>`
- 用户若明确指定其他输出目录，以用户指定为准；否则一律用上述路径
- 建议将 `.hyperframes-projects/` 加入项目 `.gitignore`（本 skill 仓库已忽略）

批量项目推荐结构（`<project>` 即上式完整路径）：

```text
<project>/
├── brief.md
├── visual-spec.json
├── imagegen-prompts.md
├── gate2-qa.md
├── gate3-qa.md
├── still-contact-sheet.jpg
├── video-contact-sheet-all.jpg
├── video-first-frame-all.jpg
├── end-frame-comparison-all.jpg
├── 01-概念名/
│   ├── motion-prompt.txt
│   ├── frames/
│   │   ├── last-frame-original.png   # Gate 2 确认静帧
│   │   ├── first-frame.png           # 同 hex 纯色空场
│   │   └── last-frame.png            # 规范化 9:16 静帧
│   └── video/run-v01/
│       ├── final.mp4                 # 工具原始输出
│       ├── final-noaudio.mp4         # 默认交付
│       ├── contact-sheet.jpg
│       ├── video-last-frame.jpg
│       └── end-frame-comparison.jpg
└── 02-概念名/...
```

## Phase 1：设计视觉隐喻

先把文稿压成一个视觉命题。

提取：

- 核心意思：观众最终要看懂什么
- 情绪：冷静、惊讶、紧迫、豁然开朗、荒诞、反讽
- 动作动词：打开、连接、漏掉、装订、归档、点亮、压缩、分叉、组装
- 可视化隐喻：机器、时钟、胶片、档案柜、控制台、规则册、漏斗、轨道、棋子

不要把文稿逐字放进画面。默认一条文稿只做一个隐喻，控制在 3–6 个关键物件；元素过多会让语意变弱，也会让组装动画不稳定。

批量隐喻优先形成前后叙事：例如先表现手工消耗与经验流失，再表现规范沉淀与人机分工。

### Gate 1 输出示例

```text
1. 核心意思：经验每次都在重复消耗
   视觉隐喻：熟练剪辑师围着巨大的胶片时钟逐帧裁切，时钟走完一圈却只得到一小段成片
   关键物件：胶片时钟、剪辑师、剪刀、短胶片
   色彩：焦橙底，奶油白与浅青点色
   组装顺序：时钟 → 人物与剪刀 → 胶片 → 最终短输出
```

输出后**停下等待确认**。不得调用任何生成工具。

## Phase 2：生成彩色拼贴静帧

隐喻确认后，先写自包含的 `visual-spec.json`，再写 imagegen prompt。

### Visual spec

```json
{
  "script_meaning": "",
  "visual_metaphor": "",
  "style_signature": "flat bold color field, mixed black-and-white halftone cut-outs and colored cardstock accents, crisp cut edges, cream keylines, soft paper shadows, editorial paper collage",
  "aspect_ratio": "9:16",
  "color_field": {
    "background_hex": "",
    "accent_colors": [],
    "paper_grain": "fine uncoated-paper fiber"
  },
  "elements": [
    {
      "what": "",
      "role": "",
      "motion": "",
      "placement": ""
    }
  ],
  "composition": {
    "layout": "",
    "negative_space": "",
    "final_frame": ""
  },
  "motion_plan": "structure first, subject or cards second, action and result last",
  "avoid": "typography, readable letters, numerals, logos, watermark, UI, subtitles, glossy 3D, photoreal environment"
}
```

### 色彩规则

不要把 cobalt blue 当成唯一默认值。根据语意挑选强色场，并在一批作品中保持“同设计语言、不同底色”：

- 焦橙 / 红：时间消耗、劳动、紧迫
- 芥末黄：工具、警示、经验漏失
- 墨绿：认知、审美、系统重置
- 深紫：规范、沉淀、长期记忆
- 青绿：判断、协作、自动执行

主体可以黑白半调为主，但局部彩色纸张必须服务信息层级，不要为了彩色而彩色。

### Imagegen prompt 模板

使用 Grok Build 内置 **`image_gen`**（`aspect_ratio: "9:16"`）。可同时遵守 `imagine` skill 的提示词原则：主语优先、正面描述、2–5 句、自然散文。

```text
Create a finished editorial paper-collage still for a 9:16 B-roll last frame expressing [一句话视觉命题]. Perfectly flat [颜色] paper field [hex] with subtle uncoated paper fiber. Premium editorial stop-motion paper collage: black-and-white halftone photographic cut-outs mixed with selective [点色] colored cardstock. Vertical locked poster frame; central subject within the middle 70 percent; generous clean color-field negative space; 3–6 large separable paper groups for later assemble-from-empty animation. Visible printed halftone dots, crisp machine-cut edges, thin warm-cream paper keylines, soft low-opacity physical drop shadows. [本条隐喻必须一眼看懂的关系]. No typography, no readable letters, no numerals, no logos, no watermark, no UI, no subtitles, no glossy 3D, no photoreal environment, no clutter.
```

调用方式（agent tool call，不是 shell）：

- 工具：`image_gen`
- `prompt`：上表展开后的全文
- `aspect_ratio`：`"9:16"`

将返回的图片复制/移动到 `<item>/frames/last-frame-original.png`（或项目约定路径）。

### 静帧 QA

- 隐喻是否一眼看懂
- 主体是否集中
- 是否有假字、logo、水印或 UI
- 是否保留足够纯色场，方便从空场组装
- 是否是 3–6 个清晰大组，而不是满屏碎片
- 同一批是否统一质感但有色彩变化

将通过 QA 的原图保存到项目目录，用 ffmpeg 生成带编号的静帧 contact sheet，展示给用户并**停下等待 Gate 2 确认**。静帧 QA 结论写入 `<project>/gate2-qa.md`。

静帧 contact sheet 示例（多图 hstack；单图可直接展示）：

```bash
# 示例：将多张静帧缩放到同高后横向拼接
ffmpeg -y -i still-01.png -i still-02.png \
  -filter_complex "[0:v]scale=-1:480[a];[1:v]scale=-1:480[b];[a][b]hstack=inputs=2" \
  still-contact-sheet.jpg
```

也可用本 skill 的 `scripts/make_still_contact_sheet.sh`（见 scripts 说明）。

如果用户要求重生部分静帧，重生后生成 `still-contact-sheet-v2.jpg`（后续轮次递增 v3、v4…），保留旧版 contact sheet 不覆盖，方便对比。

## Phase 3：用 Grok Build `reference_to_video` 生成 assemble-from-empty

Grok 视频**没有**真正的 Omni 式 first+last 关键帧插值 API。实证对比后，**默认**用「纯色空场 + 已确认静帧」的 **`reference_to_video`**：空场引导 assemble-from-empty 起幅，确认静帧约束完成态，单次 ~6s 内组装可读性与末帧贴合最好。

不要默认只用空场 `image_to_video`（末帧易整张重画）。不要默认用终态静帧 `image_to_video` hold（末帧稳但几乎无组装）。

### 1. 准备首尾帧（ffmpeg）— 两条都要

保留 image_gen 原图，再统一尾帧尺寸（9:16，建议 1080×1920）：

```bash
ffmpeg -y -i <item>/frames/last-frame-original.png \
  -vf "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920" \
  <item>/frames/last-frame.png
```

首帧是与尾帧相同底色的纯色空纸面（hex 来自 visual-spec 的 `background_hex`，不要带 `#`）：

```bash
ffmpeg -y -f lavfi -i color=c=0x<HEX>:s=1080x1920 \
  -frames:v 1 <item>/frames/first-frame.png
```

或：

```bash
bash <本skill目录>/scripts/prepare_empty_first_frame.sh <HEX> <item>/frames/first-frame.png
```

如果用户明确要求不从完全空白开始，首帧才保留一个基础物件。

### 2. 写组装动画 prompt

动作顺序默认采用：

```text
基础结构 → 人物或关键卡片 → 连接件 → 动作 → 最终结果
```

#### 默认路径：`reference_to_video`（空场 + 确认静帧）

```text
Paper-collage stop-motion assembly on a flat [color] paper field matching the finished reference. Locked-off vertical 9:16 shot. Open near the empty purple/color field, then assemble piece by piece with crisp physical stop-motion timing: [按顺序描述 3–6 个元素如何滑入、卡位、连接和完成动作]. End by holding the completed collage matching the finished reference composition. Restrained tactile 2D paper craft only; preserve [hex] color field, halftone cut-outs, cream keylines and soft shadows. No scene cuts, no camera movement, no zoom, no morphing, no new objects, no text, no letters, no numbers, no logos, no watermark, no UI, no sound.
```

工具参数（**必填齐全**）：

- `images`：`[first-frame.png 绝对路径, last-frame.png 绝对路径]`（**空场在前，完成静帧在后**）
- `prompt`：上表展开后的组装描述
- `aspect_ratio`：`"9:16"`（**必填**）
- `duration`：`6`（默认）或 `10`
- `resolution_name`：优先 `"720p"`（草稿可用 `480p`）

说明：`reference_to_video` 不是像素级 first/last 插值 API，但空场+静帧双参考在实测中同时保住「从空组装」与「末帧贴近 Gate 2」。首帧边缘轻微提前露出纸片可接受。

#### 保底路径 A：终态 `image_to_video`（hold / settle）

仅当默认路径末帧 QA 严重失败、且用户接受弱组装时使用：

- `image`：`last-frame.png`（已确认静帧）
- `prompt`：finished collage settles with minimal tactile snap, then hold；locked-off；no zoom
- `duration`：`6`；`resolution_name`：`720p`

#### 不推荐作默认：空场 `image_to_video`

仅调试或用户明确要求「忽略末帧贴合」时：

- `image`：`first-frame.png`
- prompt 描述 assemble；**预期末帧常偏离确认静帧**，交付前必须做 end-frame compare 并倾向重跑默认路径

### 3. 保存输出并强制无声交付

将工具返回的视频复制到 `<item>/video/run-v01/final.mp4`，再去音轨：

```bash
ffmpeg -y -i <run>/final.mp4 \
  -map 0:v:0 -c:v copy -an \
  <run>/final-noaudio.mp4
```

或：

```bash
bash <本skill目录>/scripts/strip_audio.sh <run>/final.mp4 <run>/final-noaudio.mp4
```

默认交付 `final-noaudio.mp4`，保留 `final.mp4` 作为中间产物。

**时长说明**：Grok 视频工具仅支持 6s / 10s，默认 6s（最接近原 Omni 5s）。不要伪造 5s 模型参数；若必须卡 5s 口播，可在交付前用 ffmpeg 裁剪作 polish（可选，非默认）。

## 视频 QA

不要只看尾帧，必须检查组装过程和最终落位。

### Contact sheet

```bash
ffmpeg -y -i <run>/final-noaudio.mp4 \
  -vf "fps=1,scale=270:480,tile=6x1" \
  -frames:v 1 <run>/contact-sheet.jpg
```

（6s 默认用 `tile=6x1`；10s 用 `tile=10x1` 或 `5x2`。）

或：

```bash
bash <本skill目录>/scripts/make_video_contact_sheet.sh <run>/final-noaudio.mp4 <run>/contact-sheet.jpg
```

通过标准：

- 首帧接近纯色空场；边缘轻微提前露出纸片可以接受
- 中段能看到结构、人物或卡片逐步进入，而不是整体淡入
- 没有切镜、zoom、3D 化或写实场景漂移
- 没有假字、logo、水印或 UI
- 最终帧与确认静帧语义一致；轻微姿态或细节漂移只要不影响隐喻即可判通过，不要为此无脑重跑
- 成片为 9:16、6 秒（或 10 秒）、零音轨

另外抽取视频末帧，与确认静帧并排生成 `end-frame-comparison.jpg`：

```bash
bash <本skill目录>/scripts/compare_end_frame.sh \
  <run>/final-noaudio.mp4 \
  <item>/frames/last-frame.png \
  <run>/end-frame-comparison.jpg
```

批量项目再合并总览图：

- `video-contact-sheet-all.jpg`：全部成片逐秒抽帧
- `video-first-frame-all.jpg`：全部成片实际首帧，验证真的从空色场开始
- `end-frame-comparison-all.jpg`：确认静帧与视频末帧并排对照

逐条 QA 结论（含带瑕疵通过的判定理由）写入 `<project>/gate3-qa.md`。

### 常见问题

- 首帧边缘提前露出：轻微可接受；严格空场需求改用 HyperFrames 补前段
- 组装感弱：缩短元素数量，prompt 改为明确的逐件 slide in / snap into place；仍弱则检查是否误用了终态 hold 路径
- 尾帧漂移：确认默认用的是 `reference_to_video` 且 `images` 顺序为 `[空场, 确认静帧]`；强化 “End by holding the completed collage matching the finished reference”；仍差再考虑终态 `image_to_video` 保底（接受弱组装）
- 误用空场 `image_to_video` 导致末帧重画：改回默认 `reference_to_video`，不要用空场 i2v 当主路径
- 出现假字：先回到静帧重生（Gate 2），不要直接用视频 prompt 修补
- 个别视频失败：只重跑对应条目，不要重跑已经通过的条目
- 复杂静帧动画畸变：Gate 2 简化静帧后重生，或保底 hold 路径

## 默认交付

向用户交付：

- 每条 `<item>/video/run-v01/final-noaudio.mp4`
- 每条 contact sheet
- 批量总 contact sheet
- 最终帧对照图
- 一句说明每条文稿如何转成视觉隐喻

如果成片问题来自视频模型的快速生成限制，直接说明；只有需要精确图层控制时，才建议切换到 HyperFrames。

## 工具边界（勿发明 API）

| 能力 | 正确做法 |
|------|----------|
| 静帧 | Grok Build `image_gen`，`aspect_ratio: "9:16"` |
| 静帧微调 | Grok Build `image_edit`（可选） |
| **视频（默认）** | **`reference_to_video`**，`images=[空场, 确认静帧]`，`aspect_ratio: "9:16"`，`duration` 6，优先 720p |
| 视频（保底 hold） | `image_to_video` 以确认静帧为 source |
| 视频（不推荐默认） | 空场 `image_to_video` |
| 后处理 | 系统 `ffmpeg` / `ffprobe`（scripts 封装） |
| 禁止默认路径 | Gemini Omni / Veo / `GEMINI_API_KEY` / `google-genai` / Codex-only 客户端 |
