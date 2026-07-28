#!/usr/bin/env python3
"""Direct Gemini REST API fallback for image editing.

Used when the nanobanana MCP server is unavailable. Prefer the MCP tool
(`gemini_edit_image`) when it's up -- this hits the API with no MCP
dependency, for the same crafted edit instruction Claude would otherwise
pass to the MCP.
"""
import argparse
import base64
import mimetypes
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _gemini_common import RESOLUTION_TO_IMAGE_SIZE, call_generate_content, extract_image  # noqa: E402

DEFAULT_MODEL = "gemini-3.1-flash-image-preview"


def main() -> None:
    parser = argparse.ArgumentParser(description="Edit an existing image directly via the Gemini API")
    parser.add_argument("--image", required=True, help="Path to the source image")
    parser.add_argument("--prompt", required=True, help="Fully-crafted edit instruction")
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--resolution", default="2K", choices=sorted(RESOLUTION_TO_IMAGE_SIZE))
    parser.add_argument("--aspect-ratio", default=None, help="e.g. 1:1, 16:9, 3:4 -- omit to keep the source image's framing")
    parser.add_argument("--output", default="edited.png", help="Path to save the edited image")
    args = parser.parse_args()

    image_path = Path(args.image)
    if not image_path.exists():
        print(f"[ERROR] Image not found: {image_path}", file=sys.stderr)
        sys.exit(1)

    mime_type = mimetypes.guess_type(image_path.name)[0] or "image/png"
    image_data = base64.b64encode(image_path.read_bytes()).decode("ascii")

    contents = [
        {
            "role": "user",
            "parts": [
                {"text": args.prompt},
                {"inlineData": {"mimeType": mime_type, "data": image_data}},
            ],
        }
    ]
    image_config = {"imageSize": RESOLUTION_TO_IMAGE_SIZE[args.resolution]}
    if args.aspect_ratio:
        image_config["aspectRatio"] = args.aspect_ratio

    generation_config = {
        "responseModalities": ["IMAGE"],
        "imageConfig": image_config,
    }

    response = call_generate_content(args.model, contents, generation_config)
    output_path = extract_image(response, Path(args.output))
    print(f"[INFO] Saved edited image to {output_path}")


if __name__ == "__main__":
    main()
