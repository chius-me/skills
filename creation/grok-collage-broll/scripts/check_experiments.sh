#!/usr/bin/env bash
# Integrity check for experiments/scheme-compare outputs.
# Exit 0 only if required deliverables exist and basic media properties hold.

set -u

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
EXP="$ROOT/experiments/scheme-compare"
FAIL=0
PASS=0

pass() { printf 'ok  %s\n' "$1"; PASS=$((PASS + 1)); }
fail() { printf 'not ok  %s\n' "$1"; FAIL=$((FAIL + 1)); }

echo "# check_experiments"
echo "# EXP=$EXP"

if [ ! -d "$EXP" ]; then
  fail "experiment root missing"
  echo "# pass=$PASS fail=$FAIL"
  exit 1
fi

# Shared still required
if [ -f "$EXP/shared/approved-still.png" ] || [ -f "$EXP/shared/last-frame.png" ]; then
  pass "shared approved still present"
else
  fail "shared approved still missing"
fi

if [ -f "$EXP/QUALITY_REPORT.md" ]; then
  pass "QUALITY_REPORT.md present"
  for axis in 'Assemble-from-empty' 'End-frame' 'Camera' 'text' 'Paper-collage' 'recommended default'; do
    if grep -qiF "$axis" "$EXP/QUALITY_REPORT.md" || grep -qiE "$axis" "$EXP/QUALITY_REPORT.md"; then
      pass "report covers: $axis"
    else
      fail "report missing axis: $axis"
    fi
  done
  if grep -qiE 'recommended default|Default Gate-3|C .reference_to_video' "$EXP/QUALITY_REPORT.md"; then
    pass "report names recommended default"
  else
    fail "report has no recommended default"
  fi

else
  fail "QUALITY_REPORT.md missing"
fi

SCHEMES=(A-empty-first-i2v B-multishot-concat C-reference-to-video D-final-still-i2v)
COMPLETED=0

for S in "${SCHEMES[@]}"; do
  D="$EXP/$S"
  if [ ! -d "$D" ]; then
    fail "scheme dir missing: $S"
    continue
  fi
  # still
  if ls "$D"/frames/*still* "$D"/frames/last-frame.png "$D"/frames/approved-still.png 2>/dev/null | head -1 | grep -q .; then
    pass "$S has still"
  elif [ -f "$D/frames/last-frame.png" ]; then
    pass "$S has still (last-frame)"
  else
    fail "$S missing still image"
  fi
  # silent video
  VID=""
  if [ -f "$D/video/final-noaudio.mp4" ]; then VID="$D/video/final-noaudio.mp4"
  elif [ -f "$D/video/final.mp4" ]; then VID="$D/video/final.mp4"
  fi
  if [ -n "$VID" ]; then
    pass "$S has video"
    if command -v ffprobe >/dev/null 2>&1; then
      HAS_V=$(ffprobe -v error -select_streams v:0 -show_entries stream=codec_type -of csv=p=0 "$VID" 2>/dev/null || true)
      DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$VID" 2>/dev/null || true)
      HAS_A=$(ffprobe -v error -select_streams a:0 -show_entries stream=codec_type -of csv=p=0 "$VID" 2>/dev/null || true)
      if [ "$HAS_V" = "video" ] && [ -n "$DUR" ] && [ "$(printf '%.0f' "$DUR" 2>/dev/null || echo 0)" -gt 0 ]; then
        pass "$S ffprobe video duration=$DUR"
      else
        fail "$S ffprobe bad (v=$HAS_V dur=$DUR)"
      fi
      if [ -z "$HAS_A" ]; then
        pass "$S no audio stream"
      else
        # prefer silent; soft fail if audio present on final.mp4 only
        if echo "$VID" | grep -q noaudio; then
          fail "$S final-noaudio still has audio"
        else
          pass "$S has audio on non-stripped file (ok if strip exists separately)"
        fi
      fi
    fi
    COMPLETED=$((COMPLETED + 1))
  else
    fail "$S missing video mp4"
  fi
  if ls "$D"/video/contact-sheet.jpg "$D"/video/*contact* 2>/dev/null | head -1 | grep -q .; then
    pass "$S contact sheet"
  else
    fail "$S missing contact sheet"
  fi
  if ls "$D"/video/end-frame-comparison.jpg "$D"/video/*end-frame* 2>/dev/null | head -1 | grep -q .; then
    pass "$S end-frame comparison"
  else
    fail "$S missing end-frame comparison"
  fi
  if [ -f "$D/run-log.md" ]; then
    pass "$S run-log.md"
    if grep -qiE 'GEMINI_API_KEY|google-genai|generate_video\.py|gemini-omni' "$D/run-log.md"; then
      if grep -qiE 'Not used|no Gemini|禁止' "$D/run-log.md"; then
        pass "$S run-log demotes Gemini"
      else
        fail "$S run-log still invokes Gemini path"
      fi
    else
      pass "$S run-log clean of Gemini invokes"
    fi
  else
    fail "$S missing run-log.md"
  fi
done

if [ "$COMPLETED" -ge 3 ]; then
  pass "at least 3 schemes completed ($COMPLETED)"
else
  fail "need ≥3 completed schemes, got $COMPLETED"
fi

echo "# pass=$PASS fail=$FAIL completed_schemes=$COMPLETED"
if [ "$FAIL" -ne 0 ]; then
  exit 1
fi
exit 0
