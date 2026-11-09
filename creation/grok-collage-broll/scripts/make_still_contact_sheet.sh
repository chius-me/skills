#!/usr/bin/env bash
# Numbered horizontal contact sheet from one or more still images.
# Usage: make_still_contact_sheet.sh <output.jpg> <still1.png> [still2.png ...]

set -euo pipefail

if [ "$#" -lt 2 ]; then
  echo "Usage: $0 <output.jpg> <still1> [still2 ...]" >&2
  exit 2
fi

OUT="$1"
shift
STILLS=("$@")

if ! command -v ffmpeg >/dev/null 2>&1; then
  echo "ffmpeg not found" >&2
  exit 1
fi

N="${#STILLS[@]}"
if [ "$N" -eq 1 ]; then
  ffmpeg -y -i "${STILLS[0]}" -vf "scale=-1:480" -frames:v 1 "$OUT" >/dev/null 2>&1
  echo "Wrote $OUT"
  exit 0
fi

INPUTS=()
for s in "${STILLS[@]}"; do
  INPUTS+=(-i "$s")
done

FILTERS=""
LABELS=""
for i in $(seq 0 $((N - 1))); do
  FILTERS+="[${i}:v]scale=-1:480[v${i}];"
  LABELS+="[v${i}]"
done
FILTERS+="${LABELS}hstack=inputs=${N}"

ffmpeg -y "${INPUTS[@]}" -filter_complex "$FILTERS" -frames:v 1 "$OUT" >/dev/null 2>&1
echo "Wrote $OUT (${N} stills)"
