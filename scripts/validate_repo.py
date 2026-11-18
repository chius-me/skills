#!/usr/bin/env python3
"""Repository-wide structural validation for skill packages.

Checks:
1. Every directory containing SKILL.md has valid YAML frontmatter (name, description).
2. The directory name strictly matches frontmatter `name`.
3. If agents/openai.yaml exists, verifies required interface fields and $<name> reference.
4. Every relative Markdown link in SKILL.md and references/*.md resolves to an existing path.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
IGNORED_PARTS = {".git", ".github", "node_modules", ".venv", "__pycache__", "experiments"}
LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")


def parse_frontmatter(text: str) -> dict[str, str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("missing opening '---' YAML frontmatter delimiter")
    end_idx = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end_idx = i
            break
    if end_idx is None:
        raise ValueError("missing closing '---' YAML frontmatter delimiter")

    data: dict[str, str] = {}
    block_lines = lines[1:end_idx]
    i = 0
    while i < len(block_lines):
        raw = block_lines[i]
        stripped = raw.strip()
        if not stripped or stripped.startswith("#"):
            i += 1
            continue
        if ":" not in raw:
            raise ValueError(f"invalid frontmatter line: {raw!r}")
        key, rest = raw.split(":", 1)
        key = key.strip()
        val = rest.strip()
        if val in (">", ">-", "|", "|-"):
            collected: list[str] = []
            i += 1
            while i < len(block_lines):
                nxt = block_lines[i]
                if nxt.startswith((" ", "\t")) or not nxt.strip():
                    collected.append(nxt.strip())
                    i += 1
                else:
                    break
            data[key] = " ".join(part for part in collected if part).strip()
            continue
        if len(val) >= 2 and ((val[0] == val[-1] == '"') or (val[0] == val[-1] == "'")):
            val = val[1:-1]
        data[key] = val
        i += 1
    return data


def iter_markdown_links(md_path: Path) -> list[tuple[int, str]]:
    """Extract relative link targets outside fenced code blocks."""
    results: list[tuple[int, str]] = []
    in_fence = False
    fence_marker = ""
    for lineno, line in enumerate(md_path.read_text(encoding="utf-8").splitlines(), 1):
        stripped = line.lstrip()
        if stripped.startswith(("```", "~~~")):
            marker = stripped[:3]
            if not in_fence:
                in_fence = True
                fence_marker = marker
            elif stripped.startswith(fence_marker):
                in_fence = False
                fence_marker = ""
            continue
        if in_fence:
            continue
        # Strip inline code spans so template examples like `[label](url)` are skipped.
        cleaned = re.sub(r"`[^`]*`", "", line)
        for match in LINK_RE.finditer(cleaned):
            target = match.group(1).strip()
            if not target:
                continue
            target = target.split()[0].strip("<>")
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            results.append((lineno, target))
    return results


def validate_openai_yaml(yaml_path: Path, skill_name: str, errors: list[str]) -> None:
    text = yaml_path.read_text(encoding="utf-8")
    for field in ("display_name:", "short_description:", "default_prompt:"):
        if field not in text:
            errors.append(f"{yaml_path.relative_to(ROOT)}: missing '{field[:-1]}'")
    if f"${skill_name}" not in text:
        errors.append(
            f"{yaml_path.relative_to(ROOT)}: default_prompt should reference '${skill_name}'"
        )


def find_skill_dirs(root: Path) -> list[Path]:
    dirs: list[Path] = []
    for path in sorted(root.rglob("SKILL.md")):
        rel_parts = set(path.relative_to(root).parts[:-1])
        if rel_parts & IGNORED_PARTS:
            continue
        dirs.append(path.parent)
    return dirs


def main() -> int:
    skill_dirs = find_skill_dirs(ROOT)
    if not skill_dirs:
        print("No skill directories found.", file=sys.stderr)
        return 1

    errors: list[str] = []
    seen_names: dict[str, Path] = {}

    for skill_dir in skill_dirs:
        rel_dir = skill_dir.relative_to(ROOT)
        skill_md = skill_dir / "SKILL.md"
        try:
            fm = parse_frontmatter(skill_md.read_text(encoding="utf-8"))
        except ValueError as exc:
            errors.append(f"{rel_dir}/SKILL.md: {exc}")
            continue

        name = fm.get("name", "").strip()
        desc = fm.get("description", "").strip()
        if not name:
            errors.append(f"{rel_dir}/SKILL.md: missing frontmatter 'name'")
        if not desc:
            errors.append(f"{rel_dir}/SKILL.md: missing frontmatter 'description'")
        if name and name != skill_dir.name:
            errors.append(
                f"{rel_dir}/SKILL.md: frontmatter name '{name}' != directory name '{skill_dir.name}'"
            )
        if name:
            if name in seen_names:
                errors.append(
                    f"duplicate skill name '{name}': {seen_names[name]} and {rel_dir}"
                )
            seen_names[name] = rel_dir

        openai_yaml = skill_dir / "agents" / "openai.yaml"
        if openai_yaml.is_file() and name:
            validate_openai_yaml(openai_yaml, name, errors)

        md_files = [skill_md]
        refs_dir = skill_dir / "references"
        if refs_dir.is_dir():
            md_files.extend(sorted(refs_dir.glob("*.md")))
        readme_md = skill_dir / "README.md"
        if readme_md.is_file():
            md_files.append(readme_md)

        for md_file in md_files:
            for lineno, target in iter_markdown_links(md_file):
                path_part = unquote(target.split("#", 1)[0])
                if not path_part:
                    continue
                resolved = (md_file.parent / path_part).resolve()
                if not resolved.exists():
                    errors.append(
                        f"{md_file.relative_to(ROOT)}:{lineno}: broken link target '{target}'"
                    )

        lines = len(skill_md.read_text(encoding="utf-8").splitlines())
        print(f"OK  {rel_dir} (name={name}, lines={lines})")

    root_readme = ROOT / "README.md"
    if root_readme.is_file():
        for lineno, target in iter_markdown_links(root_readme):
            path_part = unquote(target.split("#", 1)[0])
            if not path_part:
                continue
            resolved = (ROOT / path_part).resolve()
            if not resolved.exists():
                errors.append(f"README.md:{lineno}: broken link target '{target}'")

    if errors:
        print("\nValidation errors:", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        return 1

    print(f"\nValidated {len(skill_dirs)} skill(s) with 0 errors.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
