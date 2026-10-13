"""Behavior checks: python -m unittest discover -s scripts -p 'test_*.py'."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageOps
import render_plate as renderer


class RenderTests(unittest.TestCase):
    def test_invalid_coordinates_and_markers(self):
        for value in (float("nan"), float("inf"), True, -0.1, 1.1):
            spec = {"base": "base.jpg", "labels": [{"text": "A", "x": value, "y": 0.5}]}
            self.assertTrue(renderer.validate(spec))
        label = {"text": "A", "x": 0.5, "y": 0.5,
                 "target": {"x": 0.4, "y": 0.4, "color": "red"}}
        self.assertTrue(renderer.validate({"base": "b.png", "labels": [label, label]}))
        self.assertTrue(renderer.validate({"base": "b.png", "inset":
                                         {"x": .9, "y": .1, "w": .2, "h": .2}}))

    def test_leader_respects_left_and_right_alignment(self):
        for align in ("left", "center", "right"):
            label = {"text": "GRAND\nLISBOA", "x": .5, "y": .5, "align": align}
            item = renderer.text_layout(label, 1600, 1200, renderer.find_font())
            l, t, r, b = item["box"]
            self.assertAlmostEqual({"left": l, "center": (l+r)/2, "right": r}[align], 800)
            start = renderer.leader_start(item["box"], (0, (t+b)/2), 12)
            self.assertAlmostEqual(start[0], l-12)
            self.assertAlmostEqual(start[1], (t+b)/2)

    def test_measured_text_contains_rendered_glyphs(self):
        item = renderer.text_layout({"text": "Grand\nLisboa", "x": .5, "y": .5},
                                    1600, 1200, renderer.find_font())
        overlay = Image.new("RGBA", (1600, 1200))
        renderer.draw_label(ImageDraw.Draw(overlay), item, 1)
        ink = overlay.getbbox()
        l, t, r, b = item["box"]
        self.assertGreaterEqual(ink[0], l-2)
        self.assertGreaterEqual(ink[1], t-2)
        self.assertLessEqual(ink[2], r+2)
        self.assertLessEqual(ink[3], b+2)

    def test_empty_overlay_preserves_pixels(self):
        base = Image.new("RGB", (800, 600), (100, 130, 185))
        result, issues = renderer.render({"base": "base.png"}, base)
        self.assertIsNone(ImageChops.difference(base, result).getbbox())
        self.assertEqual(issues, [])

    def test_layout_detects_overlaps_and_clipping(self):
        labels = [{"text": "A LONG PLACE NAME", "x": .99, "y": .01, "align": "left"}]*2
        items = [renderer.text_layout(l, 1600, 1200, renderer.find_font()) for l in labels]
        issues = renderer.layout_issues(items, 1600, 1200)
        self.assertTrue(any("overlaps" in issue for issue in issues))
        self.assertTrue(any("margin" in issue for issue in issues))

    def test_dot_spacing_does_not_depend_on_vertex_density(self):
        a, b = Image.new("RGBA", (400, 100)), Image.new("RGBA", (400, 100))
        renderer.stroke(ImageDraw.Draw(a), [(10,50),(390,50)], 1, dotted=True)
        renderer.stroke(ImageDraw.Draw(b), [(10,50),(50,50),(200,50),(390,50)], 1, dotted=True)
        self.assertIsNone(ImageChops.difference(a,b).getbbox())

    def test_cli_orientation_source_protection_and_strict_mode(self):
        script = Path(renderer.__file__)
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source, spec, output = root/"base.png", root/"spec.json", root/"plate.png"
            base = Image.new("RGB", (80, 60), "blue")
            ImageDraw.Draw(base).rectangle((0,0,20,20), fill="red")
            exif = Image.Exif()
            exif[274] = 6
            base.save(source, exif=exif)
            original = source.read_bytes()
            spec.write_text(json.dumps({"base": "base.png"}))
            def run(*args):
                return subprocess.run([sys.executable,str(script),str(spec),*args],
                                      capture_output=True,text=True)
            self.assertEqual(run().returncode, 0)
            with Image.open(source) as src, Image.open(output) as result:
                expected = ImageOps.exif_transpose(src).convert("RGB")
                self.assertEqual(result.size, (60,80))
                self.assertIsNone(ImageChops.difference(result,expected).getbbox())
                self.assertFalse(result.getexif())
            self.assertNotEqual(run("--out",str(source)).returncode, 0)
            self.assertEqual(source.read_bytes(), original)
            spec.write_text(json.dumps({"base": "base.png", "labels":
                                       [{"text":"OFF FRAME","x":1,"y":0,"align":"left"}]}))
            rejected = root/"rejected.png"
            self.assertNotEqual(run("--strict","--out",str(rejected)).returncode, 0)
            self.assertFalse(rejected.exists())

    def test_example_spec_is_valid(self):
        folder = Path(renderer.__file__).resolve().parents[1]/"example"/"grand-lisboa"
        self.assertEqual(renderer.validate(json.loads((folder/"spec.json").read_text())), [])


if __name__ == "__main__":
    unittest.main()
