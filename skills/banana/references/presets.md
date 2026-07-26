# Presets -- Reference

Brand/style presets let a user say "generate a hero image for Acme" and have
Claude automatically apply Acme's brand colors, style, aspect ratio, and
preferred model as defaults for the Reasoning Brief.

## Storage

Presets are individual JSON files in `~/.banana/presets/<name>.json`, managed
via `scripts/presets.py`.

## Schema

```json
{
  "name": "acme",
  "brand_colors": ["#FF6B6B", "#1A1A2E"],
  "style": "minimal editorial, high contrast",
  "aspect_ratio": "16:9",
  "model": "gemini-3.1-flash-image-preview",
  "notes": "Prefers clean negative space, avoid stock-photo look"
}
```

All fields except `name` are optional -- only set what the brand actually
constrains. An empty/missing field means "no default, follow normal domain
routing."

## Merge Behavior

When a preset matches the request:

1. Load the preset with `presets.py show NAME`
2. Use its `brand_colors`, `style`, `aspect_ratio`, and `model` as defaults
   for Step 3 (Construct the Reasoning Brief) and Step 4 (Select Aspect Ratio)
   in SKILL.md
3. **User instructions at generation time always override preset values** --
   e.g. if the user says "make it square" but the preset says `16:9`, use `1:1`
4. `notes` is freeform guidance folded into the brief, not a hard constraint

## CLI

```bash
# List all presets
python3 scripts/presets.py list

# Create/update a preset
python3 scripts/presets.py create acme \
  --brand-colors "#FF6B6B,#1A1A2E" \
  --style "minimal editorial, high contrast" \
  --aspect-ratio 16:9 \
  --model gemini-3.1-flash-image-preview \
  --notes "Prefers clean negative space, avoid stock-photo look"

# Show a preset
python3 scripts/presets.py show acme

# Delete a preset
python3 scripts/presets.py delete acme
```
