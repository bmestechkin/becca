# MCP Tools -- Reference

Provided by the `@ycse/nanobanana-mcp` package, configured via `scripts/setup_mcp.py`
(or `/banana setup`) as the `nanobanana` MCP server.

## `set_aspect_ratio`

Sets the aspect ratio for subsequent generations in the current session.

| Param | Type | Notes |
|-------|------|-------|
| `ratio` | string | One of the supported ratios, e.g. `"16:9"` (see gemini-models.md) |

Call this **before** `gemini_generate_image` whenever the ratio differs from
the session default (`1:1`).

## `set_model`

Switches the active model for subsequent calls.

| Param | Type | Notes |
|-------|------|-------|
| `model` | string | `gemini-2.5-flash-image` or `gemini-3.1-flash-image-preview` |

Only call this when routing away from the default model.

## `gemini_generate_image`

Generates a new image from a fully-crafted prompt.

| Param | Type | Notes |
|-------|------|-------|
| `prompt` | string | The crafted Reasoning Brief -- never raw user text |
| `imageSize` | string | `512`, `1K`, `2K`, or `4K` (version-dependent support) |

Returns image data plus `finishReason` (see gemini-models.md for handling).

## `gemini_edit_image`

Edits an existing image using a crafted edit instruction.

| Param | Type | Notes |
|-------|------|-------|
| `imagePath` | string | Path to the source image |
| `prompt` | string | The crafted edit instruction (see SKILL.md Editing Workflows) |

## `gemini_chat`

Multi-turn generation/refinement within a persistent session, preserving
character and style consistency across calls.

| Param | Type | Notes |
|-------|------|-------|
| `message` | string | The next instruction in the conversation |

## `get_image_history`

Returns the list of images generated in the current session (paths + prompts).
No parameters.

## `clear_conversation`

Resets the session's chat/image history and any character/style memory.
No parameters. Use between unrelated creative projects.

## Fallback

If the MCP server is unavailable (not configured, npx failure, connection
error), fall back to the direct-API scripts:

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/generate.py --prompt "..." --aspect-ratio "16:9" --resolution 2K --output out.png
python3 ${CLAUDE_SKILL_DIR}/scripts/edit.py --image path/to/in.png --prompt "..." --output out.png
```

These call the Gemini REST API (`generateContent`) directly, reading the API
key from `GEMINI_API_KEY` or `~/.banana/config.json`.
