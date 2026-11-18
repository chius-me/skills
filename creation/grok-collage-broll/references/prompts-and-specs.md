# 提示词模板、Spec 与项目目录规范

本文件供 `grok-collage-broll` 在 Gate 1 方案示例、Gate 2 静帧生成与 Gate 3 视频生成阶段按需读取。

## 1. 推荐项目目录结构

默认在当前工作区创建 `<workspace>/.hyperframes-projects/YYYY-MM-DD-collage-broll-<短标题 slug>/`（日期按 `Asia/Shanghai`）。批量项目推荐如下：

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

## 2. Gate 1 输出示例

```text
1. 核心意思：经验每次都在重复消耗
   情绪：紧迫、略带自嘲
   视觉命题：熟练剪辑师围着巨大的胶片时钟逐帧裁切，时钟走完一圈却只得到一小段成片
   关键物件：胶片时钟、剪辑师、剪刀、短胶片
   色彩：焦橙底，奶油白与浅青点色
   组装顺序：胶片时钟 → 人物与剪刀 → 裁切动作 → 最终短胶片输出
```

## 3. Visual Spec 结构

隐喻确认后，先写自包含的 `visual-spec.json`：

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

### 语意色彩参考

同一批作品应保持“同设计语言、不同底色”，避免把单一底色当作唯一默认值：

- **焦橙 / 红**：时间消耗、劳动、紧迫
- **芥末黄**：工具、警示、经验漏失
- **墨绿**：认知、审美、系统重置
- **深紫**：规范、沉淀、长期记忆
- **青绿**：判断、协作、自动执行

## 4. Gate 2 静帧 Prompt 模板（`image_gen`）

调用 `image_gen`（`aspect_ratio: "9:16"`）：

```text
Create a finished editorial paper-collage still for a 9:16 B-roll last frame expressing [一句话视觉命题]. Perfectly flat [颜色] paper field [hex] with subtle uncoated paper fiber. Premium editorial stop-motion paper collage: black-and-white halftone photographic cut-outs mixed with selective [点色] colored cardstock. Vertical locked poster frame; central subject within the middle 70 percent; generous clean color-field negative space; 3–6 large separable paper groups for later assemble-from-empty animation. Visible printed halftone dots, crisp machine-cut edges, thin warm-cream paper keylines, soft low-opacity physical drop shadows. [本条隐喻必须一眼看懂的关系]. No typography, no readable letters, no numerals, no logos, no watermark, no UI, no subtitles, no glossy 3D, no photoreal environment, no clutter.
```

## 5. Gate 3 视频 Prompt 模板

动作顺序默认：`基础结构 → 人物或关键卡片 → 连接件 → 动作 → 最终结果`。

### 默认路径：`reference_to_video`（空场 + 确认静帧）

参数：`images=[first-frame.png 绝对路径, last-frame.png 绝对路径]`（**空场在前，静帧在后**）、`aspect_ratio: "9:16"`、`duration: 6`（或 `10`）、优先 `resolution_name: "720p"`。

```text
Paper-collage stop-motion assembly on a flat [color] paper field matching the finished reference. Locked-off vertical 9:16 shot. Open near the empty [color] paper field, then assemble piece by piece with crisp physical stop-motion timing: [按顺序描述 3–6 个元素如何滑入、卡位、连接和完成动作]. End by holding the completed collage matching the finished reference composition. Restrained tactile 2D paper craft only; preserve [hex] color field, halftone cut-outs, cream keylines and soft shadows. No scene cuts, no camera movement, no zoom, no morphing, no new objects, no text, no letters, no numbers, no logos, no watermark, no UI, no sound.
```

### 保底路径：`image_to_video`（确认静帧 hold / settle）

仅当默认路径末帧 QA 严重失败且用户接受弱组装时使用：

- `image`: `last-frame.png`（已确认静帧）
- `prompt`: `Finished paper-collage composition settles with minimal tactile snap, then holds steady. Locked-off vertical 9:16 shot, no camera movement, no zoom, no new objects, no text, no sound.`
- `duration`: `6`，`resolution_name`: `"720p"`
