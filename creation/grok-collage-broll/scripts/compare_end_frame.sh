#!/usr/bin/env bash
# Extract last video frame and hstack with approved still for end-frame QA.
# Usage: compare_end_frame.sh <video.mp4> <still.png> <output.jpg>

set -euo pipefail

if [ "$#" -lt 3 ]; then
  echo "Usage: $0 <video.mp4> <still.png> <output.jpg>" >&2
  exit 2
fi

VIDEO="$1"
STILL="$2"
OUT="$3"
TMPDIR_LOCAL="$(mktemp -d)"
trap 'rm -rf "$TMPDIR_LOCAL"' EXIT

if ! command -v ffmpeg >/dev/null 2>&1; then
  echo "ffmpeg not found" >&2
  exit 1
fi

LAST="$TMPDIR_LOCAL/video-last.jpg"
ffmpeg -y -sseof -0.1 -i "$VIDEO" -frames:v 1 -q:v 2 "$LAST" >/dev/null 2>&1

ffmpeg -y -i "$STILL" -i "$LAST" \
  -filter_complex "[0:v]scale=270:480:force_original_aspect_ratio=decrease,pad=270:480:(ow-iw)/2:(oh-ih)/2[a];[1:v]scale=270:480:force_original_aspect_ratio=decrease,pad=270:480:(ow-iw)/2:(oh-ih)/2[b];[a][b]hstack=inputs=2" \
  -frames:v 1 "$OUT" >/dev/null 2>&1

echo "Wrote $OUT (still | video-last)"
