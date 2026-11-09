#!/usr/bin/env bash
# 1fps tile contact sheet for a finished silent clip.
# Usage: make_video_contact_sheet.sh <input.mp4> <output.jpg> [cols]
# Default cols=6 (matches default 6s duration).

set -euo pipefail

if [ "$#" -lt 2 ]; then
  echo "Usage: $0 <input.mp4> <output.jpg> [cols]" >&2
  exit 2
fi

IN="$1"
OUT="$2"
COLS="${3:-6}"

if ! command -v ffmpeg >/dev/null 2>&1; then
  echo "ffmpeg not found" >&2
  exit 1
fi

ffmpeg -y -i "$IN" \
  -vf "fps=1,scale=270:480,tile=${COLS}x1" \
  -frames:v 1 "$OUT" >/dev/null 2>&1
echo "Wrote $OUT"
