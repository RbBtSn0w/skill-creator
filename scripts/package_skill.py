#!/usr/bin/env python3
"""
Skill Packager - Creates a distributable .skill file of a skill folder

Usage:
    python scripts/package_skill.py <path/to/skill-folder> [output-directory] [--exclude dir1,dir2]

Example:
    python scripts/package_skill.py skills/my-skill
    python scripts/package_skill.py skills/my-skill ./dist
    python scripts/package_skill.py . ./dist --exclude docs,legacy
"""

import argparse
import fnmatch
import os
import sys
import zipfile
from pathlib import Path
try:
    from scripts.quick_validate import validate_skill
except ImportError:
    from quick_validate import validate_skill

# Standard directories and files excluded across all packaging operations.
DEFAULT_EXCLUDE_DIRS = {"__pycache__", "node_modules", ".git", ".venv", "venv", ".idea", ".vscode"}
DEFAULT_EXCLUDE_GLOBS = {"*.pyc"}
DEFAULT_EXCLUDE_FILES = {".DS_Store", "Thumbs.db"}
# Root-level non-runtime directories excluded from skill packages.
DEFAULT_ROOT_EXCLUDES = {"evals", "tests", "benchmarks", ".skills_staging", ".upstream"}


def should_exclude(rel_path: Path, custom_excludes: set[str] | None = None) -> bool:
    """Check if a path should be excluded from packaging."""
    parts = rel_path.parts
    exclude_dirs = DEFAULT_EXCLUDE_DIRS | (custom_excludes or set())
    if any(part in exclude_dirs for part in parts):
        return True
    # Exclude root-level non-runtime folders
    if len(parts) > 1 and parts[1] in DEFAULT_ROOT_EXCLUDES:
        return True
    name = rel_path.name
    if name in DEFAULT_EXCLUDE_FILES:
        return True
    return any(fnmatch.fnmatch(name, pat) for pat in DEFAULT_EXCLUDE_GLOBS)


def package_skill(skill_path, output_dir=None, custom_excludes: set[str] | None = None):
    """
    Package a skill folder into a .skill file.

    Args:
        skill_path: Path to the skill folder
        output_dir: Optional output directory for the .skill file (defaults to current directory)
        custom_excludes: Optional set of directory/file names to exclude

    Returns:
        Path to the created .skill file, or None if error
    """
    skill_path = Path(skill_path).resolve()

    # Validate skill folder exists
    if not skill_path.exists():
        print(f"❌ Error: Skill folder not found: {skill_path}")
        return None

    if not skill_path.is_dir():
        print(f"❌ Error: Path is not a directory: {skill_path}")
        return None

    # Validate SKILL.md exists
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        print(f"❌ Error: SKILL.md not found in {skill_path}")
        return None

    # Run validation before packaging
    print("🔍 Validating skill...")
    valid, message = validate_skill(skill_path)
    if not valid:
        print(f"❌ Validation failed: {message}")
        print("   Please fix the validation errors before packaging.")
        return None
    print(f"✅ {message}\n")

    # Determine output location
    skill_name = skill_path.name
    if output_dir:
        output_path = Path(output_dir).resolve()
        output_path.mkdir(parents=True, exist_ok=True)
    else:
        output_path = Path.cwd()

    skill_filename = output_path / f"{skill_name}.skill"

    # Merge environment and explicit excludes
    env_excludes = set(filter(None, os.environ.get("SKILL_PACKAGE_EXCLUDE", "").split(",")))
    merged_excludes = (custom_excludes or set()) | env_excludes

    # Create the .skill file (zip format)
    try:
        with zipfile.ZipFile(skill_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Walk through the skill directory, excluding build artifacts
            for file_path in skill_path.rglob('*'):
                if not file_path.is_file():
                    continue
                arcname = file_path.relative_to(skill_path.parent)
                if should_exclude(arcname, merged_excludes):
                    print(f"  Skipped: {arcname}")
                    continue
                zipf.write(file_path, arcname)
                print(f"  Added: {arcname}")

        print(f"\n✅ Successfully packaged skill to: {skill_filename}")
        return skill_filename

    except Exception as e:
        print(f"❌ Error creating .skill file: {e}")
        return None


def main():
    parser = argparse.ArgumentParser(description="Package a skill folder into a .skill archive")
    parser.add_argument("skill_path", help="Path to the skill directory")
    parser.add_argument("output_dir", nargs="?", default=None, help="Optional output directory (default: current directory)")
    parser.add_argument("--exclude", default="", help="Comma-separated additional directories/files to exclude")
    args = parser.parse_args()

    skill_path = Path(args.skill_path)
    output_dir = args.output_dir
    custom_excludes = {x.strip() for x in args.exclude.split(",") if x.strip()}

    print(f"📦 Packaging skill: {skill_path}")
    if output_dir:
        print(f"   Output directory: {output_dir}")
    if custom_excludes:
        print(f"   Custom excludes: {', '.join(sorted(custom_excludes))}")
    print()

    result = package_skill(skill_path, output_dir, custom_excludes)

    if result:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
