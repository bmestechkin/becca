#!/usr/bin/env python3
"""Query the local /banana prompt library (references/prompt_library.json).

Usage:
  python3 inspire.py --list-categories
  python3 inspire.py --category sci-fi
  python3 inspire.py --mode product --limit 3
  python3 inspire.py --random --limit 5
  python3 inspire.py --model gemini-3-pro-image-preview
"""
import argparse
import json
import os
import random

LIBRARY_PATH = os.path.join(
    os.path.dirname(__file__), "..", "references", "prompt_library.json"
)


def load_library():
    with open(LIBRARY_PATH) as f:
        return json.load(f)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--category", default=None, help="Filter by category slug")
    parser.add_argument("--mode", default=None, help="Filter by domain mode")
    parser.add_argument("--model", default=None, help="Filter by suggested model (substring match)")
    parser.add_argument("--type", default="image", help="Content type; this library only holds 'image' prompts")
    parser.add_argument("--random", action="store_true", help="Shuffle results before limiting")
    parser.add_argument("--limit", type=int, default=5)
    parser.add_argument("--list-categories", action="store_true", help="Print all categories and their prompt counts, then exit")
    args = parser.parse_args()

    data = load_library()
    prompts = data["prompts"]

    if args.list_categories:
        counts = {c: 0 for c in data["categories"]}
        for p in prompts:
            counts[p["category"]] = counts.get(p["category"], 0) + 1
        for cat, count in counts.items():
            print(f"{cat}: {count}")
        return

    if args.type and args.type != "image":
        print(f"No prompts of type '{args.type}' -- this library only holds image prompts.")
        return

    if args.category:
        if args.category not in data["categories"]:
            print(f"Unknown category '{args.category}'. Run --list-categories to see valid values.")
            return
        prompts = [p for p in prompts if p["category"] == args.category]

    if args.mode:
        if args.mode not in data["modes"]:
            print(f"Unknown mode '{args.mode}'. Valid modes: {', '.join(data['modes'])}")
            return
        prompts = [p for p in prompts if p["mode"] == args.mode]

    if args.model:
        prompts = [p for p in prompts if args.model.lower() in p.get("model", "").lower()]

    if not prompts:
        print("No prompts matched those filters.")
        return

    if args.random:
        prompts = random.sample(prompts, k=min(args.limit, len(prompts)))
    else:
        prompts = prompts[: args.limit]

    for p in prompts:
        print(f"[{p['id']}] {p['title']}  ({p['category']} / {p['mode']})")
        print(f"  {p['prompt']}")
        print(
            f"  suggested -> model: {p.get('model')}, aspect_ratio: {p.get('aspect_ratio')}, "
            f"image_size: {p.get('image_size')}"
        )
        print()


if __name__ == "__main__":
    main()
