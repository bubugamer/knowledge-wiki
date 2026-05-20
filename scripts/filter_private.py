#!/usr/bin/env python3
"""Pre-build filter: remove pages without 'visibility: public' from docs/ and mkdocs.yml nav.

Usage:
    python scripts/filter_private.py

This script is meant to run in CI before `mkdocs build`. It:
1. Scans all .md files in docs/ for frontmatter `visibility: public`
2. Removes files that don't have it (no visibility field, or visibility: private)
3. Strips corresponding entries from mkdocs.yml nav
4. Rewrites mkdocs.yml in place

Only run this in CI — it destructively modifies the working tree.
log.md is always kept (no frontmatter, but it's a structural file).
"""

import re
import sys
from pathlib import Path

WIKI_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = WIKI_ROOT / "docs"
MKDOCS_YML = WIKI_ROOT / "mkdocs.yml"

# Files that are always kept regardless of visibility field
ALWAYS_KEEP = {"log.md", "index.md"}


def is_public(filepath: Path) -> bool:
    """Check if a markdown file has 'visibility: public' in frontmatter."""
    if filepath.name in ALWAYS_KEEP:
        return True

    content = filepath.read_text(encoding="utf-8")
    if not content.startswith("---"):
        return False

    # Extract frontmatter block
    match = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return False

    frontmatter = match.group(1)
    for line in frontmatter.split("\n"):
        stripped = line.strip()
        if stripped.startswith("visibility:"):
            value = stripped.split(":", 1)[1].strip()
            return value == "public"

    # No visibility field found → not public
    return False


def remove_from_nav(nav_content: str, filenames_to_remove: set[str]) -> str:
    """Remove nav entries that reference any of the given filenames.

    Handles the YAML nav structure by line-based filtering.
    Also removes section headers that become empty after filtering.
    """
    lines = nav_content.split("\n")
    result = []
    removed_files = set()

    for line in lines:
        # Check if this line references a file to remove
        should_remove = False
        for fname in filenames_to_remove:
            if fname in line and ":" in line:
                should_remove = True
                removed_files.add(fname)
                break

        if not should_remove:
            result.append(line)

    # Second pass: remove empty sections (a section header followed by another
    # section header or end of nav, with no content lines in between)
    cleaned = []
    i = 0
    while i < len(result):
        line = result[i]

        # Check if this is a section header (has text before : but no .md after :)
        stripped = line.strip()
        if stripped.startswith("- ") and ":" in stripped and ".md" not in stripped:
            # Look ahead: is the next non-empty line at the same or lower indent level?
            current_indent = len(line) - len(line.lstrip())
            has_children = False

            for j in range(i + 1, len(result)):
                next_line = result[j]
                if not next_line.strip():
                    continue
                next_indent = len(next_line) - len(next_line.lstrip())
                if next_indent > current_indent:
                    has_children = True
                break

            if not has_children:
                # Empty section, skip it
                i += 1
                continue

        cleaned.append(line)
        i += 1

    return "\n".join(cleaned)


def main():
    if not DOCS_DIR.is_dir():
        print(f"Error: {DOCS_DIR} not found")
        return 1

    # Find all non-public pages
    private_files = []
    for f in sorted(DOCS_DIR.glob("*.md")):
        if not is_public(f):
            private_files.append(f)

    if not private_files:
        print("All pages are public. Nothing to filter.")
        return 0

    # Remove private files from docs/
    filenames_to_remove = set()
    for f in private_files:
        print(f"  Removing: {f.name}")
        filenames_to_remove.add(f.name)
        f.unlink()

    # Update mkdocs.yml nav
    if MKDOCS_YML.exists():
        content = MKDOCS_YML.read_text(encoding="utf-8")
        new_content = remove_from_nav(content, filenames_to_remove)
        MKDOCS_YML.write_text(new_content, encoding="utf-8")
        print(f"  Updated mkdocs.yml (removed {len(filenames_to_remove)} entries)")

    print(f"\nFiltered {len(private_files)} private page(s) before build.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
