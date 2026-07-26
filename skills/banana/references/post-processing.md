# Post-Processing -- Reference

## Pre-flight

Before running any post-processing, verify tools are available:

```bash
which magick || which convert || echo "ImageMagick not installed -- install with: sudo apt install imagemagick"
```

If `magick` (v7) is not found, fall back to `convert` (v6). If neither exists,
inform the user rather than guessing at a workaround.

## Common Recipes

```bash
# Crop to exact dimensions
magick input.png -resize 1200x630^ -gravity center -extent 1200x630 output.png

# Remove white background -> transparent PNG
magick input.png -fuzz 10% -transparent white output.png

# Convert format
magick input.png output.webp

# Add border/padding
magick input.png -bordercolor white -border 20 output.png

# Resize for a specific platform
magick input.png -resize 1080x1080 instagram.png
```

(Substitute `convert` for `magick` on ImageMagick 6 installs -- same flags.)

## Green Screen Transparency Pipeline

For clean transparent-background PNGs where a simple `-transparent white`
fuzz match isn't precise enough (fine hair strands, semi-transparent edges),
generate against a solid green (chroma key) background instead of asking the
model for "transparent background" directly, then key it out:

1. In the prompt, explicitly request a solid, evenly-lit green background:
   `"...isolated on a solid, evenly lit chroma green background (#00FF00),
   no shadows on the background, studio lighting on the subject."`
2. Key out the green with ImageMagick's fuzz-based transparency, tuned to
   avoid eating into the subject:
   ```bash
   magick input.png -fuzz 15% -transparent "#00FF00" output.png
   ```
3. Inspect edges for green fringing (common on hair/fur). If present, tighten
   the fuzz percentage and re-run, or feather the edge:
   ```bash
   magick output.png -alpha extract -blur 0x1 -level 15%,85% mask.png
   magick input.png mask.png -alpha off -compose CopyOpacity -composite final.png
   ```
4. Verify transparency actually round-trips (some viewers render transparent
   PNGs on a white canvas, masking a failed key):
   ```bash
   magick identify -format "%[channels]\n" final.png   # expect "srgba" or similar
   ```

Use this pipeline whenever the deliverable needs to composite cleanly over
arbitrary backgrounds (app icons, product cutouts, sticker packs).
