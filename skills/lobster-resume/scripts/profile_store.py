#!/usr/bin/env python3
"""Small JSON store for the lobster-resume skill."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any


DEFAULT_PROFILE: dict[str, Any] = {
    "basics": {
        "name": "",
        "email": "",
        "phone": "",
        "links": [],
        "target_roles": [],
        "target_locations": [],
        "languages": [],
    },
    "education": [],
    "experience": [],
    "projects": [],
    "awards": [],
    "skills": {
        "technical": [],
        "domain": [],
        "tools": [],
        "certifications": [],
    },
    "preferences": {
        "language": "auto",
        "length": "auto",
        "redactions": [],
    },
}


REQUIRED_PATHS = [
    ("basics", "name"),
    ("basics", "email"),
    ("education",),
    ("experience",),
    ("projects",),
    ("skills", "technical"),
]


def default_path() -> Path:
    env_path = os.environ.get("LOBSTER_RESUME_PROFILE")
    if env_path:
        return Path(env_path).expanduser()
    return Path.cwd() / ".lobster-resume" / "profile.json"


def load_profile(path: Path) -> dict[str, Any]:
    if not path.exists():
        return json.loads(json.dumps(DEFAULT_PROFILE, ensure_ascii=False))
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    return merge(DEFAULT_PROFILE, data)


def save_profile(path: Path, profile: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(profile, handle, ensure_ascii=False, indent=2)
        handle.write("\n")


def merge(base: Any, incoming: Any) -> Any:
    if isinstance(base, dict) and isinstance(incoming, dict):
        result = dict(base)
        for key, value in incoming.items():
            result[key] = merge(result.get(key), value)
        return result
    if isinstance(base, list) and isinstance(incoming, list):
        result = list(base)
        for item in incoming:
            if item not in result:
                result.append(item)
        return result
    if incoming in ("", None, [], {}):
        return base
    return incoming


def missing_fields(profile: dict[str, Any]) -> list[str]:
    missing: list[str] = []
    for path in REQUIRED_PATHS:
        value: Any = profile
        for part in path:
            value = value.get(part, None) if isinstance(value, dict) else None
        if value in ("", None, [], {}):
            missing.append(".".join(path))
    return missing


def main() -> int:
    parser = argparse.ArgumentParser(description="Manage lobster-resume profile JSON.")
    parser.add_argument("--path", type=Path, default=default_path())
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("show")
    subparsers.add_parser("missing")

    merge_parser = subparsers.add_parser("merge")
    merge_parser.add_argument("--input", type=Path, required=True)

    args = parser.parse_args()
    profile = load_profile(args.path.expanduser())

    if args.command == "show":
        print(json.dumps(profile, ensure_ascii=False, indent=2))
        return 0

    if args.command == "missing":
        print(json.dumps(missing_fields(profile), ensure_ascii=False, indent=2))
        return 0

    if args.command == "merge":
        with args.input.open("r", encoding="utf-8") as handle:
            incoming = json.load(handle)
        profile = merge(profile, incoming)
        save_profile(args.path.expanduser(), profile)
        print(json.dumps({"path": str(args.path.expanduser()), "missing": missing_fields(profile)}, ensure_ascii=False, indent=2))
        return 0

    return 2


if __name__ == "__main__":
    raise SystemExit(main())

