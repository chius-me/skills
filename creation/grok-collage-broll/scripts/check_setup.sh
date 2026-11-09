#!/usr/bin/env bash
# grok-collage-broll environment self-check (Grok Build).
# Exit 0 = all good; exit 1 = at least one item missing (details on stdout).
#
# Shell-checkable deps only: ffmpeg/ffprobe for postprocess.
# Gate 2/3 generation tools (image_gen, image_to_video, reference_to_video)
# are provided by Grok Build at agent runtime and cannot be probed from shell.

set -u

FAIL=0

ok()  { printf 'PASS  %s\n' "$1"; }
bad() { printf 'FAIL  %s\n' "$1"; FAIL=1; }

# 1. ffmpeg / ffprobe (postprocess: empty first frame, strip audio, contact sheet)
if command -v ffmpeg >/dev/null 2>&1 && command -v ffprobe >/dev/null 2>&1; then
  ok "ffmpeg / ffprobe 可用"
else
  bad "ffmpeg / ffprobe 缺失（macOS: brew install ffmpeg；Debian/Ubuntu: sudo apt install ffmpeg）"
fi

# 2. Note Grok Build tools (informational — always PASS when running under Grok)
ok "静帧/视频由 Grok Build 提供（image_gen + image_to_video / reference_to_video）"

exit $FAIL
