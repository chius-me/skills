#!/usr/bin/env bash
# Create a solid color-field first frame (empty paper) matching the still palette.
# Usage: prepare_empty_first_frame.sh <HEX without #> <output.png> [WxH]
# Example: prepare_empty_first_frame.sh C45C26 ./frames/first-frame.png 1080x1920

set -euo pipefail

if [ "$#" -lt 2 ]; then
  echo "Usage: $0 <HEX> <output.png> [WxH]" >&2
  exit 2
fi

HEX="${1#\#}"
OUT="$2"
SIZE="${3:-1080x1920}"

if ! command -v ffmpeg >/dev/null 2>&1; then
  echo "ffmpeg not found" >&2
  exit 1
fi

ffmpeg -y -f lavfi -i "color=c=0x${HEX}:s=${SIZE}" -frames:v 1 "$OUT" >/dev/null 2>&1
echo "Wrote $OUT (${SIZE}, #${HEX})"
