# Scheme C run log — `reference_to_video` empty + approved still

**Status:** completed  
**Executor:** parent Grok Build agent

## Tools used (no Gemini)

1. Shared still + empty first frame
2. `reference_to_video` images=[first-frame, last-frame] aspect_ratio=9:16 duration=6 resolution_name=720p
3. strip_audio, make_video_contact_sheet, compare_end_frame

## Outputs

| File | Role |
|------|------|
| `video/final-noaudio.mp4` | delivery |
| `video/contact-sheet.jpg` | 1fps × 6 |
| `video/end-frame-comparison.jpg` | still \| video-last |
| `video/video-first-frame.jpg` | empty-field check |

## Not used

Gemini/Omni/Veo/google-genai.
