"""Shared helpers for the Gemini direct-API fallback scripts (generate.py, edit.py).

Used only when the nanobanana MCP server is unavailable -- see the "MCP
unavailable" row in SKILL.md's Error Handling table.
"""
import base64
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

BANANA_CONFIG_PATH = Path.home() / ".banana" / "config.json"
API_BASE = "https://generativelanguage.googleapis.com/v1beta/models"

RESOLUTION_TO_IMAGE_SIZE = {"512": "512", "1K": "1K", "2K": "2K", "4K": "4K"}


def load_api_key() -> str:
    key = os.environ.get("GEMINI_API_KEY")
    if key:
        return key
    if BANANA_CONFIG_PATH.exists():
        try:
            with BANANA_CONFIG_PATH.open() as f:
                key = json.load(f).get("gemini_api_key")
        except (json.JSONDecodeError, OSError):
            key = None
    if not key:
        print(
            "[ERROR] No Gemini API key found. Set GEMINI_API_KEY or run "
            "scripts/setup_mcp.py --key YOUR_KEY first.",
            file=sys.stderr,
        )
        sys.exit(1)
    return key


def call_generate_content(model: str, contents: list, generation_config: dict) -> dict:
    api_key = load_api_key()
    url = f"{API_BASE}/{model}:generateContent"
    body = {
        "contents": contents,
        "generationConfig": generation_config,
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "x-goog-api-key": api_key,
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", errors="replace")
        if e.code == 429:
            print("[ERROR] HTTP 429 rate limited. Wait and retry with backoff.", file=sys.stderr)
        elif e.code == 400 and "FAILED_PRECONDITION" in detail:
            print("[ERROR] HTTP 400 FAILED_PRECONDITION -- check billing on your API key.", file=sys.stderr)
        else:
            print(f"[ERROR] HTTP {e.code}: {detail}", file=sys.stderr)
        sys.exit(1)


def extract_image(response: dict, output_path: Path) -> Path:
    candidates = response.get("candidates") or []
    if not candidates:
        print(f"[ERROR] Empty response, no candidates: {json.dumps(response)}", file=sys.stderr)
        sys.exit(1)

    candidate = candidates[0]
    finish_reason = candidate.get("finishReason", "")
    if finish_reason == "IMAGE_SAFETY":
        print(
            "[ERROR] finishReason=IMAGE_SAFETY -- the prompt was blocked. "
            "Rephrase using abstraction/artistic framing and retry.",
            file=sys.stderr,
        )
        sys.exit(1)
    if finish_reason == "PROHIBITED_CONTENT":
        print("[ERROR] finishReason=PROHIBITED_CONTENT -- non-retryable, topic is blocked.", file=sys.stderr)
        sys.exit(1)

    parts = candidate.get("content", {}).get("parts", [])
    for part in parts:
        inline_data = part.get("inlineData")
        if inline_data and inline_data.get("data"):
            image_bytes = base64.b64decode(inline_data["data"])
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_bytes(image_bytes)
            return output_path

    print("[ERROR] No image parts in response -- verify responseModalities includes IMAGE.", file=sys.stderr)
    sys.exit(1)
