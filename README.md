# Banana Claude

A Claude Code skill that turns Claude into a Creative Director for AI image
generation, powered by Google's Gemini Nano Banana image models.

## Install

```bash
./install.sh                    # Install skill only
./install.sh --with-mcp KEY     # Install skill + configure MCP with a Gemini API key
./install.sh --uninstall        # Remove the skill
```

Or as a plugin: `/plugin marketplace add AgriciDaniel/banana-claude`

## Usage

Once installed, restart Claude Code and use the `/banana` command:

| Command | What it does |
|---------|---------------|
| `/banana` | Interactive -- detect intent, craft prompt, generate |
| `/banana generate <idea>` | Generate an image with full prompt engineering |
| `/banana edit <path> <instructions>` | Edit an existing image intelligently |
| `/banana chat` | Multi-turn visual session (character/style consistent) |
| `/banana inspire [category]` | Browse prompt ideas |
| `/banana batch <idea> [N]` | Generate N variations |
| `/banana setup` | Install the MCP server and configure the API key |
| `/banana preset [list\|create\|show\|delete]` | Manage brand/style presets |
| `/banana cost [summary\|today\|estimate]` | View cost tracking and estimates |

Get a free Gemini API key at https://aistudio.google.com/apikey.

## Layout

```
install.sh                     Standalone installer
skills/banana/
  SKILL.md                     Skill definition Claude reads
  scripts/                     setup, validation, cost tracking, presets, batch planning, direct-API fallback
  references/                 Model specs, prompt engineering, MCP tool docs, post-processing, cost & preset docs
```

## Data

Runtime data (cost log, presets, fallback API key) lives outside the repo, in
`~/.banana/`.
