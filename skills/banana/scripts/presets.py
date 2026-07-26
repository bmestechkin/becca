#!/usr/bin/env python3
"""Manage brand/style presets for Banana Claude.

Subcommands:
  list                     List preset names
  create NAME [--field value ...]   Create/overwrite a preset
  show NAME                Print a preset's contents
  delete NAME               Delete a preset

Presets are stored as individual JSON files in ~/.banana/presets/<name>.json
and are meant to be loaded as defaults for the Reasoning Brief (see
references/presets.md for the schema). User instructions at generation time
always override preset values.
"""
import argparse
import json
import sys
from pathlib import Path

PRESETS_DIR = Path.home() / ".banana" / "presets"


def preset_path(name: str) -> Path:
    safe_name = "".join(c for c in name if c.isalnum() or c in ("-", "_")).lower()
    if not safe_name:
        print(f"[ERROR] Invalid preset name: {name!r}", file=sys.stderr)
        sys.exit(1)
    return PRESETS_DIR / f"{safe_name}.json"


def cmd_list(_args: argparse.Namespace) -> None:
    PRESETS_DIR.mkdir(parents=True, exist_ok=True)
    presets = sorted(p.stem for p in PRESETS_DIR.glob("*.json"))
    if not presets:
        print("No presets found.")
        return
    for name in presets:
        print(name)


def cmd_show(args: argparse.Namespace) -> None:
    path = preset_path(args.name)
    if not path.exists():
        print(f"[ERROR] Preset not found: {args.name}", file=sys.stderr)
        sys.exit(1)
    with path.open() as f:
        print(json.dumps(json.load(f), indent=2))


def cmd_create(args: argparse.Namespace) -> None:
    PRESETS_DIR.mkdir(parents=True, exist_ok=True)
    path = preset_path(args.name)

    preset = {}
    if path.exists():
        with path.open() as f:
            preset = json.load(f)

    preset["name"] = args.name
    if args.brand_colors:
        preset["brand_colors"] = [c.strip() for c in args.brand_colors.split(",")]
    if args.style:
        preset["style"] = args.style
    if args.aspect_ratio:
        preset["aspect_ratio"] = args.aspect_ratio
    if args.model:
        preset["model"] = args.model
    if args.notes:
        preset["notes"] = args.notes

    with path.open("w") as f:
        json.dump(preset, f, indent=2)
        f.write("\n")
    print(f"[INFO] Saved preset '{args.name}' to {path}")


def cmd_delete(args: argparse.Namespace) -> None:
    path = preset_path(args.name)
    if not path.exists():
        print(f"[WARN] Preset not found: {args.name}")
        return
    path.unlink()
    print(f"[INFO] Deleted preset '{args.name}'")


def main() -> None:
    parser = argparse.ArgumentParser(description="Banana Claude preset manager")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("list", help="List preset names").set_defaults(func=cmd_list)

    p_show = sub.add_parser("show", help="Show a preset's contents")
    p_show.add_argument("name")
    p_show.set_defaults(func=cmd_show)

    p_create = sub.add_parser("create", help="Create or update a preset")
    p_create.add_argument("name")
    p_create.add_argument("--brand-colors", help="Comma-separated hex colors, e.g. #FF6B6B,#1A1A2E")
    p_create.add_argument("--style", help="Style descriptor, e.g. 'minimal editorial'")
    p_create.add_argument("--aspect-ratio", help="Default aspect ratio, e.g. 16:9")
    p_create.add_argument("--model", help="Default model to route to")
    p_create.add_argument("--notes", help="Freeform notes for the Creative Director")
    p_create.set_defaults(func=cmd_create)

    p_delete = sub.add_parser("delete", help="Delete a preset")
    p_delete.add_argument("name")
    p_delete.set_defaults(func=cmd_delete)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
