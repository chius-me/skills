#!/usr/bin/env python3
"""Render photographic map annotations with Pillow, without a browser.

Typography is measured with the actual font; labels, leaders and bounds share
that geometry. Input coordinates refer to the EXIF-oriented photograph.
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont, ImageOps
except ImportError:
    raise SystemExit("Pillow is required. Run: uv run --with pillow python render_plate.py spec.json")

REF_W = 1600
ROLES = {
    "city": {"size": 40, "track": 0.22},
    "place": {"size": 30, "track": 0.14},
    "water": {"size": 34, "track": 0.25},
    "region": {"size": 20, "track": 0.12},
    "caption": {"size": 18, "track": 0.02},
}
TOP_KEYS = {"base", "labels", "compass", "inset", "guides"}
LABEL_KEYS = {"text", "x", "y", "role", "align", "dot", "target"}
TARGET_KEYS = {"x", "y", "color"}
COMPASS_KEYS = {"x", "y", "north"}
INSET_KEYS = {"x", "y", "w", "h", "strokes", "labels"}
INSET_LABEL_KEYS = {"text", "x", "y", "dot"}
GUIDE_KEYS = {"points", "style"}
ALIGNS = {"left", "center", "right"}
COLORS = {"white", "red"}
WHITE = (255, 255, 250, 240)


def die(msg):
    raise SystemExit(msg)


def num(value, name: str, errors: list[str]) -> float | None:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        errors.append(f"{name} must be a number")
        return None
    if not math.isfinite(value):
        errors.append(f"{name} must be finite")
        return None
    return float(value)


def unit(value, name: str, errors: list[str]) -> float | None:
    v = num(value, name, errors)
    if v is None:
        return None
    if v < 0 or v > 1:
        errors.append(f"{name} must be between 0 and 1, got {v}")
        return None
    return v


def require_keys(obj, allowed: set[str], name: str, errors: list[str]) -> None:
    if not isinstance(obj, dict):
        errors.append(f"{name} must be an object")
        return
    extra = set(obj) - allowed
    if extra:
        errors.append(f"{name} has unknown keys: {', '.join(sorted(extra))}")


def has_cjk(text: str) -> bool:
    for c in text:
        if "\u3040" <= c <= "\u30ff" or "\u4e00" <= c <= "\u9fff" or "\uac00" <= c <= "\ud7af":
            return True
    return False


def validate(spec) -> list[str]:
    errors: list[str] = []
    if not isinstance(spec, dict):
        return ["spec must be a JSON object"]
    require_keys(spec, TOP_KEYS, "spec", errors)
    if "base" not in spec or not isinstance(spec.get("base"), str) or not spec["base"].strip():
        errors.append("base must be a png or jpeg path")
    labels = spec.get("labels", [])
    if not isinstance(labels, list):
        errors.append("labels must be a list")
        labels = []
    for i, label in enumerate(labels):
        p = f"labels[{i}]"
        require_keys(label, LABEL_KEYS, p, errors)
        if not isinstance(label, dict):
            continue
        text = label.get("text")
        if not isinstance(text, str) or not text.strip():
            errors.append(f"{p}.text must be a non-empty string")
        unit(label.get("x"), f"{p}.x", errors)
        unit(label.get("y"), f"{p}.y", errors)
        role = label.get("role", "place")
        if not isinstance(role, str) or role not in ROLES:
            errors.append(f"{p}.role must be one of {', '.join(ROLES)}")
        align = label.get("align", "center")
        if not isinstance(align, str) or align not in ALIGNS:
            errors.append(f"{p}.align must be left, center, or right")
        dot = label.get("dot", False)
        if not isinstance(dot, bool):
            errors.append(f"{p}.dot must be true or false")
        if "target" in label:
            if dot is True:
                errors.append(f"{p} uses both dot and target; pick one")
            t = label["target"]
            require_keys(t, TARGET_KEYS, f"{p}.target", errors)
            if isinstance(t, dict):
                unit(t.get("x"), f"{p}.target.x", errors)
                unit(t.get("y"), f"{p}.target.y", errors)
                color = t.get("color", "white")
                if not isinstance(color, str) or color not in COLORS:
                    errors.append(f"{p}.target.color must be white or red")
    if "compass" in spec:
        c = spec["compass"]
        require_keys(c, COMPASS_KEYS, "compass", errors)
        if isinstance(c, dict):
            unit(c.get("x"), "compass.x", errors)
            unit(c.get("y"), "compass.y", errors)
            north = num(c.get("north", 0), "compass.north", errors)
            if north is not None and not -360 <= north <= 360:
                errors.append("compass.north must be between -360 and 360")
    if "inset" in spec:
        inset = spec["inset"]
        require_keys(inset, INSET_KEYS, "inset", errors)
        if isinstance(inset, dict):
            unit(inset.get("x"), "inset.x", errors)
            unit(inset.get("y"), "inset.y", errors)
            unit(inset.get("w"), "inset.w", errors)
            unit(inset.get("h"), "inset.h", errors)
            strokes = inset.get("strokes", [])
            if not isinstance(strokes, list):
                errors.append("inset.strokes must be a list")
            else:
                for i, stroke in enumerate(strokes):
                    check_points(stroke, f"inset.strokes[{i}]", errors)
            ilabels = inset.get("labels", [])
            if not isinstance(ilabels, list):
                errors.append("inset.labels must be a list")
            else:
                for i, label in enumerate(ilabels):
                    p = f"inset.labels[{i}]"
                    require_keys(label, INSET_LABEL_KEYS, p, errors)
                    if not isinstance(label, dict):
                        continue
                    if not isinstance(label.get("text"), str) or not label.get("text", "").strip():
                        errors.append(f"{p}.text must be a non-empty string")
                    unit(label.get("x"), f"{p}.x", errors)
                    unit(label.get("y"), f"{p}.y", errors)
                    if "dot" in label and not isinstance(label["dot"], bool):
                        errors.append(f"{p}.dot must be true or false")
    guides = spec.get("guides", [])
    if not isinstance(guides, list):
        errors.append("guides must be a list")
    else:
        for i, guide in enumerate(guides):
            require_keys(guide, GUIDE_KEYS, f"guides[{i}]", errors)
            if isinstance(guide, dict):
                check_points(guide.get("points"), f"guides[{i}].points", errors)
    for i, guide in enumerate(guides):
        if not isinstance(guide, dict):
            continue
        if guide.get("style", "dotted") not in ("dotted", "solid"):
            errors.append(f"guides[{i}].style must be dotted or solid")
    inset = spec.get("inset")
    if isinstance(inset, dict):
        for start, span in (("x", "w"), ("y", "h")):
            a, b = inset.get(start), inset.get(span)
            if all(isinstance(v, (int, float)) and not isinstance(v, bool) for v in (a, b)):
                if b <= 0 or a + b > 1:
                    errors.append(f"inset.{span} must be positive and fit inside the photograph")
    red_count = sum(isinstance(l, dict) and isinstance(l.get("target"), dict)
                    and l["target"].get("color") == "red" for l in labels)
    if red_count > 1:
        errors.append("use at most one red camera-location marker")
    return errors


def check_points(points, name: str, errors: list[str]) -> None:
    if not isinstance(points, list) or len(points) < 2:
        errors.append(f"{name} must be a list of at least two [x, y] points")
        return
    for i, pt in enumerate(points):
        if not isinstance(pt, list) or len(pt) != 2:
            errors.append(f"{name}[{i}] must be [x, y]")
            continue
        unit(pt[0], f"{name}[{i}].x", errors)
        unit(pt[1], f"{name}[{i}].y", errors)


def find_font(cjk=False, override=None):
    candidates = [override] if override else (
        ["/System/Library/Fonts/PingFang.ttc",
         "/System/Library/Fonts/STHeiti Light.ttc",
         "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
         "C:/Windows/Fonts/msyh.ttc"] if cjk else
        ["/System/Library/Fonts/Helvetica.ttc",
         "/System/Library/Fonts/Supplemental/Arial.ttf",
         "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
         "C:/Windows/Fonts/arial.ttf"]
    )
    for candidate in candidates:
        if candidate and Path(candidate).is_file():
            return str(candidate)
    die("No suitable font found; pass --font /path/to/font.ttf (with CJK glyphs for Chinese).")


def text_layout(label, width, height, font_path):
    role = label.get("role", "place")
    params = ROLES[role]
    scale = width / REF_W
    size = max(10, round(params["size"] * scale))
    font = ImageFont.truetype(font_path, size)
    text = label["text"] if role == "caption" else label["text"].upper()
    tracking = (0.08 if has_cjk(text) else params["track"]) * size
    lines = text.splitlines()
    rows = []
    for line in lines:
        pen, glyphs, bounds = 0.0, [], []
        for char in line:
            l, t, r, b = font.getbbox(char, anchor="ls")
            if char.strip():
                bounds.append((pen+l, t, pen+r, b))
            glyphs.append((char, pen))
            pen += font.getlength(char) + tracking
        box = (min(b[0] for b in bounds), min(b[1] for b in bounds),
               max(b[2] for b in bounds), max(b[3] for b in bounds)) if bounds else (0,0,0,size)
        rows.append({"glyphs": glyphs, "ink": box})
    widths = [r["ink"][2]-r["ink"][0] for r in rows]
    line_height = size * 1.38
    box_w = max(widths)
    box_h = rows[-1]["ink"][3]-rows[-1]["ink"][1] + (len(lines)-1)*line_height
    x, y = label["x"] * width, label["y"] * height
    align = label.get("align", "center")
    left = x - {"left": 0, "center": box_w / 2, "right": box_w}[align]
    top = y - box_h / 2
    return {"box": (left, top, left + box_w, top + box_h), "font": font,
            "rows": rows, "widths": widths,
            "tracking": tracking, "line_height": line_height, "align": align}


def leader_start(box, target, gap):
    """Intersect the target ray with the *aligned* text rectangle."""
    left, top, right, bottom = box
    cx, cy = (left + right) / 2, (top + bottom) / 2
    dx, dy = target[0] - cx, target[1] - cy
    length = math.hypot(dx, dy)
    if not length or (left - gap <= target[0] <= right + gap
                      and top - gap <= target[1] <= bottom + gap):
        return None
    ux, uy = dx / length, dy / length
    reach = min((right - left) / 2 / abs(ux) if ux else math.inf,
                (bottom - top) / 2 / abs(uy) if uy else math.inf) + gap
    return (cx + ux * reach, cy + uy * reach)


def stroke(draw, points, scale, dotted=False, opacity=210, weight=1.25):
    """Space dots by arc length, independent of vertex density."""
    color = (255, 255, 250, opacity)
    thickness = max(1, round(weight * scale))
    if not dotted:
        draw.line(points, fill=color, width=thickness, joint="curve")
        return
    step, radius, carry = 5.5 * scale, max(0.7, 0.8 * scale), 0.0
    for a, b in zip(points, points[1:]):
        length = math.dist(a, b)
        if not length:
            continue
        distance = carry
        while distance <= length:
            t = distance / length
            x, y = a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t
            draw.ellipse((x-radius, y-radius, x+radius, y+radius), fill=color)
            distance += step
        carry = distance - length


def draw_label(draw, item, scale):
    left, top, right, _ = item["box"]
    for row, plan in enumerate(item["rows"]):
        row_width = item["widths"][row]
        x = left + {"left": 0, "center": (right-left-row_width)/2,
                    "right": right-left-row_width}[item["align"]]
        y = top + row * item["line_height"]
        for char, offset in plan["glyphs"]:
            draw.text((x + offset - plan["ink"][0], y - plan["ink"][1]),
                      char, font=item["font"], anchor="ls", fill=WHITE,
                      stroke_width=max(1, round(0.45 * scale)), stroke_fill=(15, 32, 42, 95))


def layout_issues(items, width, height):
    issues = []
    margin = 0.025 * min(width, height)
    for i, item in enumerate(items):
        l, t, r, b = item["box"]
        if l < margin or t < margin or r > width-margin or b > height-margin:
            issues.append(f"label {i}: outside the 2.5% safe margin")
        for j, earlier in enumerate(items[:i]):
            a, c, d, e = earlier["box"]
            if min(r, d) > max(l, a) and min(b, e) > max(t, c):
                issues.append(f"labels {j} and {i}: text overlaps")
    return issues


def render(spec, base, font_override=None):
    width, height = base.size
    scale = width / REF_W
    overlay = Image.new("RGBA", base.size)
    draw = ImageDraw.Draw(overlay)
    labels = list(spec.get("labels", []))
    inset = spec.get("inset")
    if inset:
        for line in inset.get("strokes", []):
            points = [((inset["x"] + x*inset["w"])*width,
                       (inset["y"] + y*inset["h"])*height) for x, y in line]
            stroke(draw, points, scale, opacity=190)
        for label in inset.get("labels", []):
            labels.append({**label, "role": "region",
                           "x": inset["x"] + label["x"] * inset["w"],
                           "y": inset["y"] + label["y"] * inset["h"]})
    items = [text_layout(l, width, height,
                        find_font(has_cjk(l["text"]), font_override)) for l in labels]
    issues = layout_issues(items, width, height)
    for guide in spec.get("guides", []):
        stroke(draw, [(x*width, y*height) for x,y in guide["points"]], scale,
               dotted=guide.get("style", "dotted") == "dotted", opacity=205)
    for label, item in zip(labels, items):
        target = label.get("target")
        if target:
            tx, ty = target["x"]*width, target["y"]*height
            start = leader_start(item["box"], (tx, ty), 12*scale)
            if start and math.dist(start, (tx, ty)) > 20*scale:
                length = math.dist(start, (tx, ty))
                end = (tx + (start[0]-tx)*6*scale/length,
                       ty + (start[1]-ty)*6*scale/length)
                stroke(draw, [start, end], scale, opacity=220, weight=1.0)
            radius = (3.5 if target.get("color") == "red" else 2.5)*scale
            color = (233, 83, 65, 255) if target.get("color") == "red" else WHITE
            draw.ellipse((tx-radius,ty-radius,tx+radius,ty+radius), fill=color)
        if label.get("dot"):
            l,t,r,b = item["box"]
            cx,cy,radius = (l+r)/2,b+9*scale,2.5*scale
            draw.ellipse((cx-radius,cy-radius,cx+radius,cy+radius),fill=WHITE)
        draw_label(draw, item, scale)
    compass = spec.get("compass")
    if compass:
        cx,cy = compass["x"]*width,compass["y"]*height
        angle = math.radians(compass.get("north",0))
        tip = (cx+math.sin(angle)*22*scale,cy-math.cos(angle)*22*scale)
        tail = (cx-math.sin(angle)*16*scale,cy+math.cos(angle)*16*scale)
        stroke(draw,[tail,tip],scale)
        for delta in (-0.5,0.5):
            wing = (tip[0]-math.sin(angle+delta)*9*scale,
                    tip[1]+math.cos(angle+delta)*9*scale)
            stroke(draw,[tip,wing],scale)
        font = ImageFont.truetype(find_font(False,font_override), max(10,round(18*scale)))
        draw.text((cx+math.sin(angle)*38*scale,cy-math.cos(angle)*38*scale),
                  "N",font=font,anchor="mm",fill=WHITE)
    return Image.alpha_composite(base.convert("RGBA"),overlay).convert("RGB"), issues


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("spec",type=Path)
    parser.add_argument("-o","--out",type=Path)
    parser.add_argument("--font",help="Font file; must cover every label's glyphs")
    parser.add_argument("--preview",type=Path,help="Also save a 1080px-wide review PNG")
    parser.add_argument("--strict",action="store_true",help="Reject overlaps or unsafe text bounds")
    args = parser.parse_args()
    try:
        spec = json.loads(args.spec.read_text(),parse_constant=lambda v: float(v))
    except (OSError,ValueError) as exc:
        die(f"Cannot read spec: {exc}")
    errors = validate(spec)
    if errors:
        die("Invalid spec:\n"+"\n".join(errors))
    base_path = Path(spec["base"]).expanduser()
    if not base_path.is_absolute():
        base_path = args.spec.resolve().parent/base_path
    out = args.out or args.spec.parent/"plate.png"
    if out.suffix.lower() != ".png":
        die("Output must be a .png")
    paths = [out] + ([args.preview] if args.preview else [])
    if any(p.resolve() in (base_path.resolve(),args.spec.resolve()) for p in paths):
        die("Output must not overwrite the source photograph or spec")
    if args.preview and args.preview.resolve() == out.resolve():
        die("Preview and full-size output must have different paths")
    try:
        with Image.open(base_path) as source:
            base = ImageOps.exif_transpose(source).convert("RGB")
            # Keep the original color profile; strip location metadata from exports.
            profile = source.info.get("icc_profile")
    except (OSError,ValueError) as exc:
        die(f"Cannot open photograph: {exc}")
    result, issues = render(spec,base,args.font)
    for issue in issues:
        print(f"Layout warning: {issue}",file=sys.stderr)
    if issues and args.strict:
        die("Adjust spec before exporting (--strict).")
    out.parent.mkdir(parents=True,exist_ok=True)
    result.save(out,icc_profile=profile)
    if args.preview:
        args.preview.parent.mkdir(parents=True,exist_ok=True)
        preview = result.copy()
        preview.thumbnail((1080,round(1080*result.height/result.width)),Image.Resampling.LANCZOS)
        preview.save(args.preview,icc_profile=profile)
    print(f"Wrote {out} ({result.width}x{result.height}); {len(issues)} layout warnings")


if __name__ == "__main__":
    main()


