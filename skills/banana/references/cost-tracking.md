# Cost Tracking -- Reference

## Pricing Table (approximate, USD per image)

| Model | 512 | 1K | 2K | 4K |
|-------|-----|----|----|----|
| `gemini-2.5-flash-image` | $0.02 | $0.02 | $0.03 | $0.05 |
| `gemini-3.1-flash-image-preview` | $0.03 | $0.04 | $0.06 | $0.10 |

These figures live in `scripts/cost_tracker.py` (`PRICING` dict) and are
**estimates** -- Google AI Studio pricing changes over time, and the free
tier absorbs cost entirely up to its daily/rate limits. Treat cost_tracker
output as directional budgeting, not an invoice.

Batch API generations get an approximate 50% discount (non-urgent, bulk
jobs) -- pass `--batch` to `cost_tracker.py estimate` to apply it.

## Usage

```bash
# Log a completed generation
python3 scripts/cost_tracker.py log --model gemini-3.1-flash-image-preview --resolution 2K --prompt "hero banner for launch"

# All-time summary by model
python3 scripts/cost_tracker.py summary

# Today's generations only
python3 scripts/cost_tracker.py today

# Estimate before a batch run
python3 scripts/cost_tracker.py estimate --model gemini-3.1-flash-image-preview --resolution 2K --count 12 --batch
```

Data is stored as a flat JSON array of entries in `~/.banana/costs.json`:

```json
[
  {
    "timestamp": "2026-07-26T12:00:00+00:00",
    "model": "gemini-3.1-flash-image-preview",
    "resolution": "2K",
    "prompt": "hero banner for launch",
    "cost_usd": 0.06
  }
]
```

## Free Tier Limits (approximate)

| Limit | Value |
|-------|-------|
| Requests per minute | ~5-15 RPM |
| Requests per day | ~20-500 RPD |

Get a free API key at https://aistudio.google.com/apikey. Limits and pricing
are set by Google and can change without notice -- verify against the AI
Studio console if a number here looks stale.
