"""从短样片等距抽取最多四帧，按阅读顺序写入一张 PNG。"""

import argparse
import json
import subprocess
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("video", type=Path)
    parser.add_argument("output", type=Path, help="输出 PNG 文件")
    args = parser.parse_args()
    if args.output.suffix.lower() != ".png":
        parser.error("输出路径应以 .png 结尾")

    probe = subprocess.check_output([
        "ffprobe", "-v", "error", "-select_streams", "v:0", "-count_frames",
        "-show_entries", "stream=nb_read_frames", "-of", "json",
        str(args.video.resolve()),
    ], text=True).strip()
    streams = json.loads(probe).get("streams", [])
    count = streams[0].get("nb_read_frames", "") if streams else ""
    if not count.isdigit() or int(count) == 0:
        parser.error("未读到可解码的视频帧")
    last = int(count) - 1
    frames = sorted({round(i * last / 3) for i in range(4)})
    select = "+".join(f"eq(n,{frame})" for frame in frames)
    filters = (
        f"select='{select}',scale=480:480:force_original_aspect_ratio=decrease,"
        f"tile=2x2:nb_frames={len(frames)}:padding=4:color=black"
    )
    subprocess.run([
        "ffmpeg", "-v", "error", "-n", "-i", str(args.video.resolve()),
        "-map", "0:v:0", "-vf", filters, "-frames:v", "1", "-update", "1",
        str(args.output.resolve()),
    ], check=True)
    print("视频帧序号（从 0 起）", *frames)


if __name__ == "__main__":
    main()
