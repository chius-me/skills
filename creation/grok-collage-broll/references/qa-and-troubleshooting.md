# 质检清单、原始命令与排错指南

本文件供 `grok-collage-broll` 在 Gate 2 静帧 QA、Gate 3 视频 QA 及故障排查时读取。

## 1. Gate 2 静帧 QA 清单

结论记录到 `<project>/gate2-qa.md`：

- 隐喻是否一眼看懂，没有文字依赖
- 主体是否集中在画面中部约 70% 区域，留出足够纯色负空间
- 是否有假字、数字、logo、水印或 UI 残影
- 是否可清晰拆成 3–6 个大纸片组，而非满屏细碎物体
- 同一批作品是否质感统一且底色随语意有变化

若用户要求部分重抽，生成递增版本接触表 `still-contact-sheet-v2.jpg`、`v3.jpg`……保留旧版不覆盖。

## 2. Gate 3 视频 QA 清单

不要只看尾帧，必须同时检查 contact sheet 与尾帧对照图，逐条结论写入 `<project>/gate3-qa.md`：

- 首帧接近纯色空场（边缘轻微提前露出纸片可接受）
- 中段能看到结构、人物或卡片逐步进入，而不是整体淡入
- 无切镜、无推拉缩放（zoom）、无 3D 化或写实场景漂移
- 无假字、logo、水印或 UI
- 最终帧与确认静帧语义一致（轻微姿态或纸片错位只要不破坏隐喻即可判通过）
- 成片为 9:16、6 秒（或 10 秒）、零音轨（`ffprobe` 确认无 audio 流）

批量项目额外合并三张总览图：
- `video-contact-sheet-all.jpg`：全部成片逐秒抽帧
- `video-first-frame-all.jpg`：全部成片实际首帧，验证从空色场起幅
- `end-frame-comparison-all.jpg`：确认静帧与视频末帧并排对照

## 3. 常用底层 ffmpeg 命令（等价于 `scripts/*.sh`）

通常直接调用 `scripts/` 下脚本即可；需要自定义参数时参考以下原语：

```bash
# 规范化确认静帧为 1080x1920（9:16）
ffmpeg -y -i <item>/frames/last-frame-original.png \
  -vf "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920" \
  <item>/frames/last-frame.png

# 生成同 hex 纯色空首帧（HEX 不带 #）
ffmpeg -y -f lavfi -i color=c=0x<HEX>:s=1080x1920 \
  -frames:v 1 <item>/frames/first-frame.png

# 去除音轨（默认交付 final-noaudio.mp4）
ffmpeg -y -i <run>/final.mp4 -map 0:v:0 -c:v copy -an <run>/final-noaudio.mp4

# 逐秒视频抽帧拼图（6s 用 6x1；10s 用 10x1 或 5x2）
ffmpeg -y -i <run>/final-noaudio.mp4 \
  -vf "fps=1,scale=270:480:force_original_aspect_ratio=decrease,pad=270:480:(ow-iw)/2:(oh-ih)/2,tile=6x1" \
  -frames:v 1 <run>/contact-sheet.jpg
```

## 4. 常见问题排错

| 问题现象 | 处置方式 |
| --- | --- |
| 首帧边缘提前露出 | 轻微可接受；若要求严格零露出，可交由分层渲染工具补前段定格 |
| 组装感太弱 | 减少物件数量，将 prompt 改为明确的逐件 slide in / snap into place；检查是否误用 hold 路径 |
| 尾帧严重漂移 | 确认使用 `reference_to_video` 且 `images` 顺序为 `[空场, 确认静帧]`；强化末尾 hold 描述；仍差再退到静帧 `image_to_video` 保底 |
| 误用空场 `image_to_video` 导致重画 | 改回默认 `reference_to_video` 重跑 |
| 画面出现假字或畸变 | 回到 Gate 2 简化或重生静帧，不要在 Gate 3 用视频 prompt 硬修 |
| 批量中有个别条目失败 | 只重跑失败条目，不要重跑已通过条目 |
