#!/usr/bin/env python3
"""Track and estimate Gemini image generation costs.

Subcommands:
  log --model MODEL --resolution RES --prompt "..."   Log a generation
  summary                                              All-time totals by model
  today                                                Totals for the current day
  estimate --model MODEL --resolution RES --count N    Estimate cost for N images

Pricing is approximate (Google AI Studio, per-image, in USD) and may drift
as Google updates pricing -- treat estimates as directional, not exact.
"""
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

BANANA_DIR = Path.home() / ".banana"
COSTS_PATH = BANANA_DIR / "costs.json"

# USD cost per generated image, keyed by (model, resolution).
# Falls back to the model's "default" entry if the exact resolution is unknown.
PRICING = {
    "gemini-2.5-flash-image": {"512": 0.02, "1K": 0.02, "2K": 0.03, "4K": 0.05, "default": 0.02},
    "gemini-3.1-flash-image-preview": {"512": 0.03, "1K": 0.04, "2K": 0.06, "4K": 0.10, "default": 0.06},
}
DEFAULT_MODEL = "gemini-3.1-flash-image-preview"
DEFAULT_RESOLUTION = "2K"
BATCH_API_DISCOUNT = 0.5  # 50% off for non-urgent bulk generation


def price_for(model: str, resolution: str) -> float:
    table = PRICING.get(model)
    if not table:
        return PRICING[DEFAULT_MODEL]["default"]
    return table.get(resolution, table["default"])


def load_entries() -> list:
    if not COSTS_PATH.exists():
        return []
    try:
        with COSTS_PATH.open() as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return []


def save_entries(entries: list) -> None:
    BANANA_DIR.mkdir(parents=True, exist_ok=True)
    with COSTS_PATH.open("w") as f:
        json.dump(entries, f, indent=2)
        f.write("\n")


def cmd_log(args: argparse.Namespace) -> None:
    cost = price_for(args.model, args.resolution)
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "model": args.model,
        "resolution": args.resolution,
        "prompt": args.prompt,
        "cost_usd": cost,
    }
    entries = load_entries()
    entries.append(entry)
    save_entries(entries)
    print(f"[INFO] Logged generation -- {args.model} @ {args.resolution} -- ${cost:.4f}")


def cmd_summary(_args: argparse.Namespace) -> None:
    entries = load_entries()
    if not entries:
        print("No generations logged yet.")
        return

    total = sum(e["cost_usd"] for e in entries)
    by_model: dict = {}
    for e in entries:
        by_model.setdefault(e["model"], {"count": 0, "cost": 0.0})
        by_model[e["model"]]["count"] += 1
        by_model[e["model"]]["cost"] += e["cost_usd"]

    print(f"Total generations: {len(entries)}")
    print(f"Total cost:        ${total:.4f}")
    print("")
    print("By model:")
    for model, stats in sorted(by_model.items(), key=lambda kv: -kv[1]["cost"]):
        print(f"  {model:<35} {stats['count']:>4} images   ${stats['cost']:.4f}")


def cmd_today(_args: argparse.Namespace) -> None:
    entries = load_entries()
    today = datetime.now(timezone.utc).date().isoformat()
    todays = [e for e in entries if e["timestamp"].startswith(today)]
    if not todays:
        print(f"No generations logged today ({today}).")
        return
    total = sum(e["cost_usd"] for e in todays)
    print(f"Today ({today}): {len(todays)} images, ${total:.4f}")
    for e in todays:
        print(f"  {e['timestamp']}  {e['model']} @ {e['resolution']}  ${e['cost_usd']:.4f}  {e['prompt']}")


def cmd_estimate(args: argparse.Namespace) -> None:
    unit_cost = price_for(args.model, args.resolution)
    total = unit_cost * args.count
    if args.batch:
        total *= BATCH_API_DISCOUNT
        print(f"Batch API estimate ({int(BATCH_API_DISCOUNT * 100)}% discount applied):")
    print(f"  Model:      {args.model}")
    print(f"  Resolution: {args.resolution}")
    print(f"  Count:      {args.count}")
    print(f"  Unit cost:  ${unit_cost:.4f}")
    print(f"  Total:      ${total:.4f}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Banana Claude cost tracker")
    sub = parser.add_subparsers(dest="command", required=True)

    p_log = sub.add_parser("log", help="Log a completed generation")
    p_log.add_argument("--model", default=DEFAULT_MODEL)
    p_log.add_argument("--resolution", default=DEFAULT_RESOLUTION)
    p_log.add_argument("--prompt", required=True, help="Short description of what was generated")
    p_log.set_defaults(func=cmd_log)

    p_summary = sub.add_parser("summary", help="Show all-time cost summary")
    p_summary.set_defaults(func=cmd_summary)

    p_today = sub.add_parser("today", help="Show today's generations and cost")
    p_today.set_defaults(func=cmd_today)

    p_estimate = sub.add_parser("estimate", help="Estimate cost for N images")
    p_estimate.add_argument("--model", default=DEFAULT_MODEL)
    p_estimate.add_argument("--resolution", default=DEFAULT_RESOLUTION)
    p_estimate.add_argument("--count", type=int, default=1)
    p_estimate.add_argument("--batch", action="store_true", help="Apply Batch API discount")
    p_estimate.set_defaults(func=cmd_estimate)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
