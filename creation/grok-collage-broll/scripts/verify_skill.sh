#!/usr/bin/env bash
# Structural tests for the shipped grok-collage-broll Grok skill.
# Drives real files in the skill package (not re-implemented expectations).
# Exit 0 on full pass; exit 1 on any failure. Prints TAP-ish lines.

set -u

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SKILL="$ROOT/SKILL.md"
FAIL=0
PASS=0

pass() { printf 'ok  %s\n' "$1"; PASS=$((PASS + 1)); }
fail() { printf 'not ok  %s\n' "$1"; FAIL=$((FAIL + 1)); }

assert_file() {
  if [ -f "$1" ]; then pass "file exists: $1"
  else fail "file missing: $1"; fi
}

assert_grep() {
  local desc="$1" pattern="$2" file="$3"
  if grep -qE "$pattern" "$file" 2>/dev/null; then pass "$desc"
  else fail "$desc (pattern not found: $pattern)"; fi
}

assert_not_grep() {
  local desc="$1" pattern="$2" file="$3"
  # Default path must not require these; allow historical mentions only if
  # clearly demoted. We ban as default-required tokens in SKILL body.
  if grep -qE "$pattern" "$file" 2>/dev/null; then
    # Allow lines that explicitly forbid / demote them
    if grep -E "$pattern" "$file" | grep -qiE '不要|禁止|不需要|无需|not |must not|do not|不要调用|不走|移除|no longer|不再'; then
      pass "$desc (only demoted mentions)"
    else
      fail "$desc (still present as active path: $pattern)"
    fi
  else
    pass "$desc"
  fi
}

echo "# grok-collage-broll verify_skill"
echo "# ROOT=$ROOT"

assert_file "$SKILL"
assert_file "$ROOT/scripts/check_setup.sh"
assert_file "$ROOT/evals/evals.json"
assert_file "$ROOT/README.md"

# Frontmatter
assert_grep "frontmatter name" '^name: grok-collage-broll' "$SKILL"
assert_grep "trigger collage b-roll" 'collage b-roll' "$SKILL"
assert_grep "trigger 纸拼贴" '纸拼贴 b-roll' "$SKILL"
assert_grep "trigger 半调拼贴" '半调拼贴' "$SKILL"
assert_grep "trigger 拼贴风格配画面" '拼贴风格配画面' "$SKILL"
assert_grep "trigger grok-collage-broll" 'grok-collage-broll' "$SKILL"

# Grok tools required
assert_grep "Gate 2 image_gen" 'image_gen' "$SKILL"
assert_grep "Gate 3 reference_to_video" 'reference_to_video' "$SKILL"
assert_grep "Gate 3 image_to_video fallback" 'image_to_video' "$SKILL"
assert_grep "default path is reference_to_video" '默认.*reference_to_video|reference_to_video.*默认|\*\*`reference_to_video`\*\*' "$SKILL"
assert_grep "duration 6 default" 'duration.*6|6 秒|默认 6' "$SKILL"
assert_grep "workspace .hyperframes-projects output" '\.hyperframes-projects' "$SKILL"
# Must not default to home hyperframes path
if grep -qE '~/hyperframes-projects' "$SKILL" 2>/dev/null; then
  if grep -E '~/hyperframes-projects' "$SKILL" | grep -qiE '不要|禁止|不要写|不写'; then
    pass "home hyperframes path only demoted"
  else
    fail "SKILL still defaults to ~/hyperframes-projects"
  fi
else
  pass "no ~/hyperframes-projects default"
fi

# Three gates
assert_grep "Gate 1 stop" 'Gate 1' "$SKILL"
assert_grep "Gate 2 stop" 'Gate 2' "$SKILL"
assert_grep "Gate 3 video" 'Gate 3' "$SKILL"
assert_grep "partial batch Gate 2" '只让通过的条目进入 Gate 2' "$SKILL"
assert_grep "partial batch Gate 3" '只让通过的条目进入 Gate 3' "$SKILL"
assert_grep "no image at Gate 1" '不生成图片' "$SKILL"
assert_grep "no video at Gate 2" '仍然不调用' "$SKILL"

# Must not default to Gemini/Codex stack
assert_not_grep "no active GEMINI_API_KEY requirement" 'GEMINI_API_KEY' "$SKILL"
assert_not_grep "no active google-genai requirement" 'google-genai' "$SKILL"
assert_not_grep "no active omni-flash default" 'gemini-omni-flash-preview' "$SKILL"

# Gemini client scripts must not be the default video path
if [ -f "$ROOT/scripts/generate_video.py" ]; then
  fail "scripts/generate_video.py still present (Gemini path should be removed)"
else
  pass "no generate_video.py"
fi
if [ -f "$ROOT/scripts/upload_file.py" ]; then
  fail "scripts/upload_file.py still present"
else
  pass "no upload_file.py"
fi
if [ -f "$ROOT/scripts/generate_veo_first_last.py" ]; then
  fail "scripts/generate_veo_first_last.py still present"
else
  pass "no generate_veo_first_last.py"
fi

# check_setup must not fail for missing Gemini
SETUP_OUT="$("$ROOT/scripts/check_setup.sh" 2>&1 || true)"
SETUP_RC=0
"$ROOT/scripts/check_setup.sh" >/dev/null 2>&1 || SETUP_RC=$?
if echo "$SETUP_OUT" | grep -qi 'GEMINI\|google-genai'; then
  fail "check_setup still mentions Gemini/google-genai"
else
  pass "check_setup has no Gemini checks"
fi
if command -v ffmpeg >/dev/null 2>&1 && command -v ffprobe >/dev/null 2>&1; then
  if [ "$SETUP_RC" -eq 0 ]; then pass "check_setup exit 0 when ffmpeg present"
  else fail "check_setup exit $SETUP_RC despite ffmpeg"; fi
else
  if [ "$SETUP_RC" -ne 0 ]; then pass "check_setup fails only when ffmpeg missing"
  else fail "check_setup should fail without ffmpeg"; fi
fi

# evals expect Grok tools
assert_grep "evals Gate 1 metaphor only" 'must not generate an image' "$ROOT/evals/evals.json"
assert_grep "evals Gate 2 image_gen" 'image_gen' "$ROOT/evals/evals.json"
assert_grep "evals Gate 3 defaults to reference_to_video" 'reference_to_video' "$ROOT/evals/evals.json"
if grep -q 'gemini-omni-flash-preview' "$ROOT/evals/evals.json" 2>/dev/null; then
  fail "evals still expect Omni Flash as default"
else
  pass "evals do not default to Omni Flash"
fi

# Helper scripts executable / runnable help
for s in prepare_empty_first_frame strip_audio make_video_contact_sheet compare_end_frame make_still_contact_sheet; do
  assert_file "$ROOT/scripts/${s}.sh"
done

# Functional smoke: empty first frame + strip path with real ffmpeg
if command -v ffmpeg >/dev/null 2>&1; then
  SMOKE_DIR="$(mktemp -d)"
  if bash "$ROOT/scripts/prepare_empty_first_frame.sh" "2D5A4A" "$SMOKE_DIR/first.png" "108x192"; then
    if [ -f "$SMOKE_DIR/first.png" ]; then pass "prepare_empty_first_frame produces png"
    else fail "prepare_empty_first_frame no output file"; fi
  else
    fail "prepare_empty_first_frame failed"
  fi
  # silent video from solid color, then a version with audio for strip_audio
  if ! ffmpeg -y -f lavfi -i "color=c=0x2D5A4A:s=108x192:d=1" \
      -c:v libx264 -pix_fmt yuv420p -an \
      "$SMOKE_DIR/silent.mp4" >/dev/null 2>&1; then
    fail "could not build smoke video with ffmpeg"
  else
    # mux silent video with generated silence so strip_audio has something to remove
    if ffmpeg -y -i "$SMOKE_DIR/silent.mp4" -f lavfi -i "anullsrc=channel_layout=mono:sample_rate=44100" \
        -c:v copy -c:a aac -shortest "$SMOKE_DIR/with_audio.mp4" >/dev/null 2>&1 \
      && [ -f "$SMOKE_DIR/with_audio.mp4" ]; then
      SRC_FOR_STRIP="$SMOKE_DIR/with_audio.mp4"
    else
      SRC_FOR_STRIP="$SMOKE_DIR/silent.mp4"
    fi
    if bash "$ROOT/scripts/strip_audio.sh" "$SRC_FOR_STRIP" "$SMOKE_DIR/noaudio.mp4"; then
      STREAMS="$(ffprobe -v error -show_entries stream=codec_type -of csv=p=0 "$SMOKE_DIR/noaudio.mp4" 2>/dev/null | tr '\n' ' ')"
      if echo "$STREAMS" | grep -q video && ! echo "$STREAMS" | grep -q audio; then
        pass "strip_audio removes audio track"
      else
        fail "strip_audio output streams unexpected: $STREAMS"
      fi
    else
      fail "strip_audio failed"
    fi
    if bash "$ROOT/scripts/make_video_contact_sheet.sh" "$SMOKE_DIR/noaudio.mp4" "$SMOKE_DIR/cs.jpg" 1; then
      [ -f "$SMOKE_DIR/cs.jpg" ] && pass "make_video_contact_sheet produces jpg" || fail "contact sheet missing"
    else
      fail "make_video_contact_sheet failed"
    fi
    if bash "$ROOT/scripts/compare_end_frame.sh" "$SMOKE_DIR/noaudio.mp4" "$SMOKE_DIR/first.png" "$SMOKE_DIR/cmp.jpg"; then
      [ -f "$SMOKE_DIR/cmp.jpg" ] && pass "compare_end_frame produces jpg" || fail "compare missing"
    else
      fail "compare_end_frame failed"
    fi
  fi
  if bash "$ROOT/scripts/make_still_contact_sheet.sh" "$SMOKE_DIR/stills.jpg" "$SMOKE_DIR/first.png"; then
    [ -f "$SMOKE_DIR/stills.jpg" ] && pass "make_still_contact_sheet produces jpg" || fail "still sheet missing"
  else
    fail "make_still_contact_sheet failed"
  fi
  rm -rf "$SMOKE_DIR"
else
  fail "ffmpeg required for functional smoke tests"
fi

echo "# pass=$PASS fail=$FAIL"
if [ "$FAIL" -ne 0 ]; then
  exit 1
fi
exit 0
