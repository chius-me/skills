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
  Use when turning short voiceover lines into 9:16 editorial halftone
  paper-collage B-roll animations via Grok Build's three-gate workflow.
---

# grok-collage-broll

把一句约 5–6 秒的口播压成一个 sharp visual idea，再做成编辑风纸拼贴组装动画。

默认三阶段链路（Grok Build 原生，对照实验见 [QUALITY_REPORT.md](experiments/scheme-compare/QUALITY_REPORT.md)）：

1. **Gate 1**：只设计视觉隐喻，停下等待确认
2. **Gate 2**：用 `image_gen` 生成 9:16 静帧 + 编号 contact sheet，停下等待确认
3. **Gate 3**：默认用 **`reference_to_video`**（纯色空场 + 已确认静帧）生成 6s 无声 assemble-from-empty 视频并完成 QA

模板、Spec、QA 详表与排错见 [提示词与 Spec 参考](references/prompts-and-specs.md) 和 [质检与排错参考](references/qa-and-troubleshooting.md)。

## 首次使用：环境自检

每次进入 Gate 1 之前，同时核对两项条件：
1. 检查当前会话工具列表是否具备 Grok Build 的 `image_gen` 与 `reference_to_video`（或 `image_to_video`）；
2. 运行本地依赖检查：

```bash
bash <本skill目录>/scripts/check_setup.sh
```

若 `ffmpeg`/`ffprobe` 缺失或不在 Grok Build 环境，不进入 Gate 1，只输出对应缺失项指引：
- **缺少 Grok Build 生成工具**：Gate 2/3 依赖 Grok Build 内置 `image_gen` 与 `reference_to_video`（保底 `image_to_video`）。在其他 Agent 环境下使用时，向用户说明需要 Grok Build，或由用户手动提供静帧/视频后从对应闸门继续。
- **缺少 `ffmpeg` / `ffprobe`**：macOS 执行 `brew install ffmpeg`，Debian/Ubuntu 执行 `sudo apt install ffmpeg`。

## 强制审批协议（不可跳步）

### Gate 1：隐喻确认
- 收到文稿后，先提视觉隐喻：**不生成图片、不生成视频、不调用 `image_gen` / `image_to_video` / `reference_to_video`**。
- 为每条文稿列出：核心意思、情绪、一句话视觉命题、3–6 个关键物件、建议底色与点色、预期组装顺序（格式见 [提示词与 Spec 参考](references/prompts-and-specs.md)）。
- **明确停下**等待确认。若用户只确认部分编号，**只让通过的条目进入 Gate 2**。

### Gate 2：静帧确认
- 隐喻确认后，先写 `visual-spec.json`，再调用 `image_gen`（`aspect_ratio: "9:16"`）生成最终静帧并保存到 `<item>/frames/last-frame-original.png`。
- 经 QA 检查后，运行 `scripts/make_still_contact_sheet.sh` 生成带编号静帧接触表展示给用户，**再次停下**。此阶段**仍然不调用** `image_to_video` / `reference_to_video`。
- 若用户只确认部分静帧，**只让通过的条目进入 Gate 3**；需修改条目可用 `image_gen` / `image_edit` 重生并递增接触表版本。

### Gate 3：视频生成（默认路径）

| 优先级 | 场景 | 工具与参数 |
| --- | --- | --- |
| **1 · 默认** | assemble-from-empty + 末帧贴合 | **`reference_to_video`**，`images=[first-frame.png, last-frame.png]`（空场在前，确认静帧在后），`aspect_ratio: "9:16"`，`duration: 6`（用户要求更长时用 `10`），优先 `resolution_name: "720p"` |
| 2 · 保底 | 默认路径末帧 QA 失败 | `image_to_video` 以**确认静帧**为 source 做轻量 settle/hold（**不是**主路径） |
| 3 · 不推荐默认 | 仅空场 `image_to_video` | 空场单图输入常在末帧整张重画，仅调试或用户明确允许时使用 |

**禁止默认走 Gemini Omni / Veo / `GEMINI_API_KEY` / `google-genai`**。

## 审美与产出约束

- **隐喻聚焦**：一句话只表达一个视觉命题，3–6 个大纸片组；多条优先构成前后叙事。
- **材质与色彩**：平坦强色场（随语意选焦橙、芥末黄、墨绿、深紫、青绿，不强制全蓝底）+ 黑白半调照片剪贴骨架 + 局部彩色卡纸点缀 + 奶油白 keyline + 柔和纸片投影。
- **克制留白**：无文字、无数字、无 logo、无水印、无 UI、无字幕、无 3D 写实场景。
- **交付格式**：9:16、默认 6 秒（Grok 视频工具仅支持 6/10 秒）、无声 MP4（`final-noaudio.mp4`）。

## 什么时候不要用

- 需要精确图层控制、遮挡穿越或可编辑时间线：改用分层动画方案（如 HyperFrames 类 HTML 渲染视频）
- 只需要写提示词不需要出片：直接给文字 prompt
- 需要真实人物口播演员广告或要求交付可逐层修改的透明素材

## 默认项目目录与脚本

所有产物默认写入**当前工作区**根目录（不要写到 `~/hyperframes-projects/`）：

```text
<workspace>/.hyperframes-projects/YYYY-MM-DD-collage-broll-<短标题 slug>/
```

（日期用北京时间 `Asia/Shanghai`；用户若另行指定目录则以其为准。完整目录树见 [提示词与 Spec 参考](references/prompts-and-specs.md)。）

后处理统一优先调用 `<本skill目录>/scripts/`（具体 `ffmpeg` 原语与 QA 清单见 [质检与排错参考](references/qa-and-troubleshooting.md)）：

```bash
# 1. 准备同 hex 纯色空首帧（HEX 不带 #），并将确认静帧统一裁切至 1080x1920
bash <本skill目录>/scripts/prepare_empty_first_frame.sh <HEX> <item>/frames/first-frame.png

# 2. 静帧接触表（Gate 2）
bash <本skill目录>/scripts/make_still_contact_sheet.sh <project>/still-contact-sheet.jpg <still1.png> [<still2.png> ...]

# 3. 去除音轨（Gate 3，默认交付 final-noaudio.mp4）
bash <本skill目录>/scripts/strip_audio.sh <run>/final.mp4 <run>/final-noaudio.mp4

# 4. 逐秒视频抽帧接触表（6s 默认 cols=6；10s 传 10）与尾帧并排对照
bash <本skill目录>/scripts/make_video_contact_sheet.sh <run>/final-noaudio.mp4 <run>/contact-sheet.jpg
bash <本skill目录>/scripts/compare_end_frame.sh <run>/final-noaudio.mp4 <item>/frames/last-frame.png <run>/end-frame-comparison.jpg
```

## 默认交付

向用户交付每条 `final-noaudio.mp4`、每条 `contact-sheet.jpg`、批量总览图（`video-contact-sheet-all.jpg` / `video-first-frame-all.jpg` / `end-frame-comparison-all.jpg`）、`end-frame-comparison.jpg`，以及一句说明每条口播如何转化为视觉隐喻。QA 结论分别记入 `gate2-qa.md` 与 `gate3-qa.md`。

## 工具边界（勿发明 API）

| 能力 | 正确做法 |
| --- | --- |
| 静帧 / 微调 | Grok Build `image_gen`（`aspect_ratio: "9:16"`）/ `image_edit` |
| 视频（默认） | **`reference_to_video`**，`images=[空场, 确认静帧]`，`aspect_ratio: "9:16"`，`duration: 6`，优先 `720p` |
| 视频（保底） | `image_to_video` 以确认静帧为 source |
| 后处理 | 系统 `ffmpeg` / `ffprobe`（通过 `scripts/*.sh` 调用） |
| 禁止默认路径 | 不使用 Gemini Omni / Veo / `GEMINI_API_KEY` / `google-genai` |
