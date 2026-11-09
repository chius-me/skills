# Scheme D run log — final-still `image_to_video` (hold/settle variant)

**Status:** completed  
**Executor:** parent Grok Build agent

## Tools used (no Gemini)

1. Shared approved still as `image_to_video` source (last-frame.png)
2. `image_to_video` duration=6 resolution_name=720p (settle/hold prompt)
3. strip_audio, make_video_contact_sheet, compare_end_frame

## Outputs

| File | Role |
|------|------|
| `video/final-noaudio.mp4` | delivery |
| `video/contact-sheet.jpg` | 1fps × 6 |
| `video/end-frame-comparison.jpg` | still \| video-last |

## Not used

Gemini/Omni/Veo/google-genai.
