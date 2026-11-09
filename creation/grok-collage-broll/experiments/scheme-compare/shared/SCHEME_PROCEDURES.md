# Scheme procedures (runnable recipes)

Common prep (once):

```bash
ROOT=.../gbro-collage-broll
EXP=$ROOT/experiments/scheme-compare
# approved-still.png from image_gen 9:16
ffmpeg scale last-frame; prepare_empty_first_frame 2B1B4A first-frame.png
```

Motion order: mirror → question card → figure + cracks.

## A — empty-first image_to_video

1. Copy `shared/first-frame.png`, `shared/last-frame.png` into scheme dir.
2. `image_to_video` image=first-frame, duration=6, resolution_name=720p, prompt=assemble-from-empty on purple field.
3. Save → `final.mp4`; strip_audio → `final-noaudio.mp4`.
4. make_video_contact_sheet; compare_end_frame vs last-frame.
5. Write `run-log.md` (tools only: image_to_video + ffmpeg scripts).

## B — multi-shot intermediate + concat

1. From approved still, produce intermediate stills (image_edit or image_gen):
   - `mid-01.png`: empty-ish field + mirror only
   - `mid-02.png`: mirror + question card
   - `mid-03.png` = approved still (full)
2. Shots:
   - S1: image_to_video(first-frame → toward mid-01)
   - S2: image_to_video(mid-01 → mid-02)
   - S3: image_to_video(mid-02 → mid-03 / hold full)
3. ffmpeg concat demuxer `-c copy` → `final.mp4`; strip audio.
4. Contact sheet on full concat; end-frame vs approved still.
5. run-log lists every tool call.

## C — reference_to_video empty + still

1. `reference_to_video` images=[first-frame, last-frame], aspect_ratio=9:16, duration=6, 720p, assemble prompt.
2. strip + contact + end-frame compare.
3. run-log.

## D — final-still image_to_video (variant)

1. `image_to_video` image=last-frame (approved still), prompt=stop-motion pieces settling / brief assemble energy then hold (or reverse: slight empty-to-full if model allows from finished frame).
2. strip + contact + end-frame compare.
3. run-log.

Note: Parent agent owns image_gen / video tools; subagents may only postprocess if video tools unavailable to children.
