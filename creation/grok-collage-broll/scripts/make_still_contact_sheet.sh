#!/usr/bin/env bash
# Numbered horizontal contact sheet from one or more still images.
# Usage: make_still_contact_sheet.sh <output.jpg> <still1.png> [still2.png ...]
# Draws [01], [02], ... index badges via ffmpeg drawtext or Pillow when available;
# falls back gracefully to a plain contact sheet if neither text renderer exists.

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

HAS_DRAWTEXT=0
if ffmpeg -hide_banner -filters 2>/dev/null | grep -qw drawtext; then
  HAS_DRAWTEXT=1
fi

N="${#STILLS[@]}"
if [ "$N" -eq 1 ]; then
  VF="scale=-1:480,format=rgb24"
  if [ "$HAS_DRAWTEXT" -eq 1 ]; then
    VF="${VF},drawtext=text='01':x=12:y=12:fontsize=24:fontcolor=white:box=1:boxcolor=black@0.7:boxborderw=6"
  fi
  ffmpeg -y -i "${STILLS[0]}" -vf "$VF" -frames:v 1 "$OUT" >/dev/null 2>&1
else
  INPUTS=()
  for s in "${STILLS[@]}"; do
    INPUTS+=(-i "$s")
  done

  FILTERS=""
  LABELS=""
  for i in $(seq 0 $((N - 1))); do
    IDX=$(printf '%02d' $((i + 1)))
    if [ "$HAS_DRAWTEXT" -eq 1 ]; then
      FILTERS+="[${i}:v]scale=-1:480,format=rgb24,setsar=1,drawtext=text='${IDX}':x=12:y=12:fontsize=24:fontcolor=white:box=1:boxcolor=black@0.7:boxborderw=6[v${i}];"
    else
      FILTERS+="[${i}:v]scale=-1:480,format=rgb24,setsar=1[v${i}];"
    fi
    LABELS+="[v${i}]"
  done
  FILTERS+="${LABELS}hstack=inputs=${N}"

  ffmpeg -y "${INPUTS[@]}" -filter_complex "$FILTERS" -frames:v 1 "$OUT" >/dev/null 2>&1
fi

# Fallback badge numbering via Pillow when ffmpeg lacks libfreetype/drawtext.
if [ "$HAS_DRAWTEXT" -eq 0 ] && command -v python3 >/dev/null 2>&1; then
  python3 - "$OUT" "${STILLS[@]}" <<'PY' 2>/dev/null || true
import sys
from PIL import Image, ImageDraw, ImageFont

out_path = sys.argv[1]
stills = sys.argv[2:]
n = len(stills)
with Image.open(out_path) as sheet:
    sheet = sheet.convert("RGB")
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default(size=20)
    x = 0
    for i, s in enumerate(stills, 1):
        with Image.open(s) as im:
            w = max(1, round(im.width * (sheet.height / im.height)))
        label = f"{i:02d}"
        bbox = draw.textbbox((0, 0), label, font=font)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        pad = 6
        draw.rectangle((x + 10, 10, x + 10 + tw + pad * 2, 10 + th + pad * 2), fill=(18, 18, 18))
        draw.text((x + 10 + pad - bbox[0], 10 + pad - bbox[1]), label, fill=(255, 255, 255), font=font)
        x += w
    sheet.save(out_path, quality=92)
PY
fi

echo "Wrote $OUT (${N} still(s))"
