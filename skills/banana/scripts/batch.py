#!/usr/bin/env python3
"""Build a generation plan (with cost estimate) from a CSV of prompts.

Expected CSV columns (header row required):
  prompt            (required) the base idea/brief for this row
  aspect_ratio      (optional) default: 1:1
  model             (optional) default: gemini-3.1-flash-image-preview
  resolution        (optional) default: 2K

This script does NOT call the Gemini API -- it only prints the plan and the
estimated total cost. Claude executes each row via the MCP `gemini_generate_image`
tool (or the generate.py fallback) after the user reviews the plan.
"""
import argparse
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from cost_tracker import DEFAULT_MODEL, DEFAULT_RESOLUTION, price_for  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description="Plan a CSV-driven batch generation")
    parser.add_argument("--csv", required=True, help="Path to the input CSV file")
    args = parser.parse_args()

    csv_path = Path(args.csv)
    if not csv_path.exists():
        print(f"[ERROR] CSV file not found: {csv_path}", file=sys.stderr)
        sys.exit(1)

    with csv_path.open(newline="") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None or "prompt" not in reader.fieldnames:
            print("[ERROR] CSV must have a header row with a 'prompt' column", file=sys.stderr)
            sys.exit(1)
        rows = list(reader)

    if not rows:
        print("[WARN] CSV has no data rows.")
        return

    total = 0.0
    print(f"Generation plan -- {len(rows)} row(s) from {csv_path.name}")
    print("-" * 70)
    for i, row in enumerate(rows, start=1):
        prompt = row["prompt"].strip()
        if not prompt:
            print(f"[WARN] Row {i}: empty prompt, skipping")
            continue
        model = (row.get("model") or DEFAULT_MODEL).strip()
        resolution = (row.get("resolution") or DEFAULT_RESOLUTION).strip()
        aspect_ratio = (row.get("aspect_ratio") or "1:1").strip()
        cost = price_for(model, resolution)
        total += cost

        print(f"{i:>3}. {prompt}")
        print(f"     model={model} resolution={resolution} aspect_ratio={aspect_ratio} cost=${cost:.4f}")

    print("-" * 70)
    print(f"Estimated total cost: ${total:.4f}")


if __name__ == "__main__":
    main()
