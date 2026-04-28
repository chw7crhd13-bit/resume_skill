#!/usr/bin/env python3
"""Download optional resume templates on demand.

The main skill package is intentionally lightweight. Full Word templates live
in a historical GitHub commit and can be fetched by category when needed.
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any


REPO = "chw7crhd13-bit/resume_skill"
TEMPLATE_SOURCE_REF = "b9bfa7f14d29d71193a9f19d0c7abb015a7cbb9b"
BASE_PATH = "skills/lobster-resume/assets/templates"
API_TREE_URL = f"https://api.github.com/repos/{REPO}/git/trees/{TEMPLATE_SOURCE_REF}?recursive=1"
RAW_BASE_URL = f"https://raw.githubusercontent.com/{REPO}/{TEMPLATE_SOURCE_REF}"


def fetch_json(url: str) -> dict[str, Any]:
    req = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json", "User-Agent": "lobster-resume"})
    with urllib.request.urlopen(req, timeout=60) as response:
        return json.loads(response.read().decode("utf-8"))


def template_files() -> list[str]:
    data = fetch_json(API_TREE_URL)
    prefix = BASE_PATH + "/"
    files = [
        item["path"]
        for item in data.get("tree", [])
        if item.get("type") == "blob" and item.get("path", "").startswith(prefix)
    ]
    return sorted(files)


def category_of(path: str) -> str:
    rest = path[len(BASE_PATH) + 1 :]
    return rest.split("/", 1)[0]


def grouped(files: list[str]) -> dict[str, list[str]]:
    result: dict[str, list[str]] = {}
    for path in files:
        result.setdefault(category_of(path), []).append(path)
    return dict(sorted(result.items()))


def download_file(remote_path: str, output_root: Path, force: bool) -> str:
    relative = Path(remote_path).relative_to(BASE_PATH)
    target = output_root / relative
    if target.exists() and not force:
        return "skipped"

    target.parent.mkdir(parents=True, exist_ok=True)
    quoted = urllib.parse.quote(remote_path)
    url = f"{RAW_BASE_URL}/{quoted}"
    req = urllib.request.Request(url, headers={"User-Agent": "lobster-resume"})
    with urllib.request.urlopen(req, timeout=120) as response:
        target.write_bytes(response.read())
    return "downloaded"


def main() -> int:
    parser = argparse.ArgumentParser(description="Download optional lobster-resume Word templates.")
    parser.add_argument("--list", action="store_true", help="List available template categories.")
    parser.add_argument("--category", help="Download one category, for example: 通用")
    parser.add_argument("--all", action="store_true", help="Download the full template library.")
    parser.add_argument("--output-dir", type=Path, default=Path(__file__).resolve().parents[1] / "assets" / "templates")
    parser.add_argument("--force", action="store_true", help="Overwrite existing files.")
    args = parser.parse_args()

    try:
        files = template_files()
    except urllib.error.URLError as exc:
        print(f"Failed to read template index: {exc}", file=sys.stderr)
        return 1

    groups = grouped(files)
    if args.list or (not args.category and not args.all):
        for category, paths in groups.items():
            print(f"{category}\t{len(paths)} files")
        if not args.list:
            print("\nUse --category <name> to download one category, or --all for every template.")
        return 0

    if args.all:
        selected = files
    else:
        if args.category not in groups:
            print(f"Unknown category: {args.category}", file=sys.stderr)
            print("Run with --list to see available categories.", file=sys.stderr)
            return 2
        selected = groups[args.category]

    counts = {"downloaded": 0, "skipped": 0}
    for path in selected:
        status = download_file(path, args.output_dir, args.force)
        counts[status] += 1

    print(json.dumps({"output_dir": str(args.output_dir), **counts}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
