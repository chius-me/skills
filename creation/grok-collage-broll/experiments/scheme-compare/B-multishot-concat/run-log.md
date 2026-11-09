# Scheme B run log — multi-shot intermediate stills + `image_to_video` + ffmpeg concat

**Status:** completed  
**Executor:** parent Grok Build agent

## Tools used (no Gemini)

1. Shared still + empty first frame (same as A)
2. `image_edit` → mid-01 (mirror + shards; figure/card removed) — 1st attempt OK
3. mid-02: `image_edit` retried twice → **503**; fallback `image_gen` for mirror+card only
4. mid-03 = copy of approved still
5. `image_to_video` ×3 (first→mid01, mid01→mid02, mid02→full), each 6s 720p
6. ffmpeg scale/fps normalize + concat demuxer → `video/final.mp4` (~18s)
7. strip_audio, contact sheet (fps=1 tile 9×2), compare_end_frame

## Outputs

| File | Role |
|------|------|
| `frames/mid-01.png` … `mid-03.png` | intermediate stills |
| `video/shots/s1.mp4` … `s3.mp4` | per-shot clips |
| `video/final-noaudio.mp4` | concatenated delivery |
| `video/contact-sheet.jpg` | process overview |
| `video/end-frame-comparison.jpg` | still \| video-last |

## Notes

- Intermediate stills drifted in identity/style (mirror design, figure becomes different person).
- Concat length ~18s (3×6s), longer than VO target.

## Not used

Gemini/Omni/Veo/google-genai.
