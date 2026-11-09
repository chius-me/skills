# Fixed brief for scheme comparison (apples-to-apples)

## Voiceover line (Gate-0 input)

很多人以为 AI 是来替你思考的，其实它更像一面镜子，会把你问题里的漏洞照出来。

## Pre-approved Gate-1 metaphor (do not re-design between schemes)

| Field | Value |
|-------|--------|
| 核心意思 | AI 不替你思考，而是把提问里的漏洞照清楚 |
| 情绪 | 冷静、略带刺痛的清醒 |
| 一句话视觉命题 | 半调人物把一面碎裂的镜子对准一张写满缺口的问号卡片，镜面把漏洞放大成清晰的纸片裂缝 |
| 关键物件（4） | ① 碎裂镜子 ② 问号卡片 ③ 半调剪影人物 ④ 裂纹/漏洞纸片 |
| 底色 hex | `2B1B4A`（深紫色场） |
| 点色 | 奶油白 keyline、浅青裂纹、芥末黄卡片边 |
| 组装顺序 | 色场空镜 → 镜子落位 → 问号卡片滑入 → 人物与裂纹卡位完成 |

## Shared Gate-2 still

- Path: `shared/approved-still.png` (and `shared/last-frame.png` 1080×1920)
- Empty first frame: `shared/first-frame.png` (solid `#2B1B4A`, 1080×1920)
- Style: editorial halftone paper-collage, flat purple field, 9:16, no typography/logos/UI

## Scheme IDs

| ID | Dir | Gate-3 method |
|----|-----|----------------|
| A | `A-empty-first-i2v` | pure empty first → `image_to_video` assemble prompt |
| B | `B-multishot-concat` | intermediate stills + per-shot `image_to_video` + ffmpeg concat |
| C | `C-reference-to-video` | `reference_to_video` with empty + approved still |
| D | `D-final-still-i2v` | approved still as source → `image_to_video` (assemble/hold variant) |

All schemes: duration 6s per clip (B may concat multiple 6s then optional trim), prefer `resolution_name: 720p`, strip audio, build contact sheet + end-frame compare via repo `scripts/`.
