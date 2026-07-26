#!/usr/bin/env python3
"""Validate that the Banana Claude skill is correctly configured.

Checks (in order): Node/npx availability, the nanobanana MCP server entry in
~/.claude.json, a usable Gemini API key, and the ~/.banana data directory.
Exits non-zero if any hard requirement is missing.
"""
import json
import os
import shutil
import sys
from pathlib import Path

CLAUDE_CONFIG_PATH = Path.home() / ".claude.json"
BANANA_DIR = Path.home() / ".banana"
BANANA_CONFIG_PATH = BANANA_DIR / "config.json"
MCP_SERVER_NAME = "nanobanana"

GREEN = "\033[0;32m"
YELLOW = "\033[1;33m"
RED = "\033[0;31m"
NC = "\033[0m"


def ok(msg: str) -> None:
    print(f"{GREEN}[ OK ]{NC} {msg}")


def warn(msg: str) -> None:
    print(f"{YELLOW}[WARN]{NC} {msg}")


def fail(msg: str) -> None:
    print(f"{RED}[FAIL]{NC} {msg}")


def load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        with path.open() as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {}


def gemini_api_key() -> str:
    if os.environ.get("GEMINI_API_KEY"):
        return os.environ["GEMINI_API_KEY"]
    banana_config = load_json(BANANA_CONFIG_PATH)
    if banana_config.get("gemini_api_key"):
        return banana_config["gemini_api_key"]
    claude_config = load_json(CLAUDE_CONFIG_PATH)
    mcp_env = (
        claude_config.get("mcpServers", {})
        .get(MCP_SERVER_NAME, {})
        .get("env", {})
    )
    return mcp_env.get("GEMINI_API_KEY", "")


def main() -> int:
    problems = 0

    # Node / npx
    if shutil.which("npx"):
        ok("npx found (required to run the MCP server)")
    else:
        fail("npx not found -- install Node.js 18+ from https://nodejs.org")
        problems += 1

    # MCP server config
    claude_config = load_json(CLAUDE_CONFIG_PATH)
    mcp_servers = claude_config.get("mcpServers", {})
    if MCP_SERVER_NAME in mcp_servers:
        ok(f"MCP server '{MCP_SERVER_NAME}' configured in {CLAUDE_CONFIG_PATH}")
    else:
        warn(
            f"MCP server '{MCP_SERVER_NAME}' not found in {CLAUDE_CONFIG_PATH} -- "
            "run: /banana setup (or install.sh --with-mcp KEY)"
        )

    # API key
    key = gemini_api_key()
    if key:
        masked = key[:4] + "..." + key[-4:] if len(key) > 8 else "****"
        ok(f"Gemini API key available ({masked})")
    else:
        warn(
            "No Gemini API key found -- get a free key at "
            "https://aistudio.google.com/apikey and run /banana setup"
        )

    # Data directory
    presets_dir = BANANA_DIR / "presets"
    if presets_dir.is_dir():
        ok(f"Data directory present: {BANANA_DIR}")
    else:
        fail(f"Data directory missing: {BANANA_DIR} -- re-run install.sh")
        problems += 1

    print("")
    if problems:
        fail(f"Validation failed with {problems} problem(s)")
        return 1

    ok("Validation passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
