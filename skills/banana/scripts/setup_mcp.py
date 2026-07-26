#!/usr/bin/env python3
"""Configure the nanobanana MCP server for Claude Code.

Writes/merges a "nanobanana" entry into the user-scope Claude Code config
(~/.claude.json under "mcpServers"), pointing it at the @ycse/nanobanana-mcp
package via npx, with the Gemini API key passed as an environment variable.
"""
import argparse
import json
import os
import sys
from pathlib import Path

CLAUDE_CONFIG_PATH = Path.home() / ".claude.json"
MCP_SERVER_NAME = "nanobanana"
MCP_PACKAGE = "@ycse/nanobanana-mcp"


def load_config(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        with path.open() as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        print(f"[ERROR] Could not parse {path}: {e}", file=sys.stderr)
        sys.exit(1)


def save_config(path: Path, config: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = path.with_suffix(".json.tmp")
    with tmp_path.open("w") as f:
        json.dump(config, f, indent=2)
        f.write("\n")
    tmp_path.replace(path)


def main() -> None:
    parser = argparse.ArgumentParser(description="Configure the nanobanana MCP server")
    parser.add_argument("--key", required=True, help="Google AI (Gemini) API key")
    parser.add_argument(
        "--config",
        default=str(CLAUDE_CONFIG_PATH),
        help="Path to the Claude Code config file (default: ~/.claude.json)",
    )
    args = parser.parse_args()

    config_path = Path(args.config)
    config = load_config(config_path)
    config.setdefault("mcpServers", {})

    config["mcpServers"][MCP_SERVER_NAME] = {
        "command": "npx",
        "args": ["-y", MCP_PACKAGE],
        "env": {"GEMINI_API_KEY": args.key},
    }

    save_config(config_path, config)

    # Also drop the key in ~/.banana/config.json for the direct-API fallback
    # scripts (generate.py / edit.py) to use when the MCP server is unavailable.
    banana_dir = Path.home() / ".banana"
    banana_dir.mkdir(parents=True, exist_ok=True)
    banana_config_path = banana_dir / "config.json"
    banana_config = load_config(banana_config_path)
    banana_config["gemini_api_key"] = args.key
    save_config(banana_config_path, banana_config)
    os.chmod(banana_config_path, 0o600)

    print(f"[INFO] Configured MCP server '{MCP_SERVER_NAME}' in {config_path}")
    print(f"[INFO] Stored API key for fallback scripts in {banana_config_path}")


if __name__ == "__main__":
    main()
