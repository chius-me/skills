# Scheme A run log — empty-first `image_to_video`

**Status:** completed  
**Executor:** parent Grok Build agent (image/video tools not available to spawn_subagent children)

## Tools used (no Gemini)

1. Shared: `image_gen` → approved still (once for all schemes)
2. `scripts/prepare_empty_first_frame.sh` HEX=2B1B4A → `frames/first-frame.png`
3. `image_to_video` image=`frames/first-frame.png` duration=6 resolution_name=720p
4. `scripts/strip_audio.sh` → `video/final-noaudio.mp4`
5. `scripts/make_video_contact_sheet.sh` → `video/contact-sheet.jpg`
6. `scripts/compare_end_frame.sh` vs `frames/last-frame.png`

## Outputs

| File | Role |
|------|------|
| `../shared/approved-still.png` | Gate-2 still (shared) |
| `../shared/first-frame.png` | solid purple empty (shared) |
| `../../../assets/demo-a-empty-i2v.mp4` | canonical silent delivery (deduplicated) |
| `video/contact-sheet.jpg` | 1fps × 6 |
| `video/end-frame-comparison.jpg` | still \| video-last |

## Not used

`generate_video.py`, `GEMINI_API_KEY`, `google-genai`, Omni/Veo.
