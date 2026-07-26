#!/usr/bin/env python3
"""Direct Gemini REST API fallback for text-to-image generation.

Used when the nanobanana MCP server is unavailable. Prefer the MCP tool
(`gemini_generate_image`) when it's up -- this hits the API with no MCP
dependency, for the same crafted prompt Claude would otherwise pass to the MCP.
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _gemini_common import RESOLUTION_TO_IMAGE_SIZE, call_generate_content, extract_image  # noqa: E402

DEFAULT_MODEL = "gemini-3.1-flash-image-preview"


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate an image directly via the Gemini API")
    parser.add_argument("--prompt", required=True, help="Fully-crafted image prompt")
    parser.add_argument("--aspect-ratio", default="1:1", help="e.g. 1:1, 16:9, 9:16")
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--resolution", default="2K", choices=sorted(RESOLUTION_TO_IMAGE_SIZE))
    parser.add_argument("--output", default="output.png", help="Path to save the generated image")
    args = parser.parse_args()

    contents = [{"role": "user", "parts": [{"text": args.prompt}]}]
    generation_config = {
        "responseModalities": ["IMAGE"],
        "imageConfig": {
            "aspectRatio": args.aspect_ratio,
            "imageSize": RESOLUTION_TO_IMAGE_SIZE[args.resolution],
        },
    }

    response = call_generate_content(args.model, contents, generation_config)
    output_path = extract_image(response, Path(args.output))
    print(f"[INFO] Saved image to {output_path}")


if __name__ == "__main__":
    main()
