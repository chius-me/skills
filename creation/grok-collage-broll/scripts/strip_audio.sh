#!/usr/bin/env bash
# Strip all audio tracks; copy video stream. Default delivery is silent MP4.
# Usage: strip_audio.sh <input.mp4> <output-noaudio.mp4>

set -euo pipefail

if [ "$#" -lt 2 ]; then
  echo "Usage: $0 <input.mp4> <output-noaudio.mp4>" >&2
  exit 2
fi

IN="$1"
OUT="$2"

if ! command -v ffmpeg >/dev/null 2>&1; then
  echo "ffmpeg not found" >&2
  exit 1
fi

ffmpeg -y -i "$IN" -map 0:v:0 -c:v copy -an "$OUT" >/dev/null 2>&1
echo "Wrote $OUT (video-only)"
