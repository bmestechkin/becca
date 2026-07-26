# Gemini Image Models -- Reference

## Available Models

| Model | Best for | Notes |
|-------|----------|-------|
| `gemini-2.5-flash-image` | Quick drafts, rapid iteration, budget-conscious work | Cheapest option, fastest turnaround, supports 512/1K/2K/4K |
| `gemini-3.1-flash-image-preview` | Default -- most use cases, final assets, text-heavy assets | Best prompt adherence, supports 21:9 ultra-wide, supports `thinking: high` for text rendering |

Default model: `gemini-3.1-flash-image-preview`. Only switch to `gemini-2.5-flash-image`
for rapid/cheap iteration where final quality is not required.

## Domain Routing Table

| Domain | Preferred model | Notes |
|--------|-----------------|-------|
| Cinema / storytelling | `gemini-3.1-flash-image-preview` | Full 5-component brief with camera/lens/lighting |
| Product / e-commerce | `gemini-3.1-flash-image-preview` | Clean studio lighting descriptions |
| Portrait | `gemini-3.1-flash-image-preview` | Facial detail sensitive -- use 2K minimum |
| Editorial / fashion | `gemini-3.1-flash-image-preview` | Publication reference anchors |
| UI/Web assets | `gemini-2.5-flash-image` | Flat design, fast iteration acceptable |
| Logo | `gemini-3.1-flash-image-preview` | Text rendering benefits from `thinking: high` |
| Landscape | `gemini-3.1-flash-image-preview` | Atmospheric depth needs strong prompt adherence |
| Abstract | `gemini-2.5-flash-image` | Style tolerant of faster/cheaper model |
| Infographic | `gemini-3.1-flash-image-preview` | Text rendering critical |

## Rate Limits (Free Tier, approximate)

| Limit | Value |
|-------|-------|
| Requests per minute | ~5-15 RPM |
| Requests per day | ~20-500 RPD |

Limits vary by account tier and change over time -- treat these as rough
guidance, not guarantees. On `429`, wait 60s and retry with exponential backoff.

## Aspect Ratios

| Ratio | Support |
|-------|---------|
| `1:1`, `16:9`, `9:16`, `3:4`, `4:3`, `3:2`, `2:3`, `4:5`, `5:4`, `4:1`, `8:1` | Both models |
| `21:9` | `gemini-3.1-flash-image-preview` only |

## Resolution (`imageSize`)

| Value | Use case |
|-------|----------|
| `512` | Quick drafts, rapid iteration |
| `1K` | Budget-conscious, web thumbnails, social |
| `2K` | Default -- quality assets, most use cases |
| `4K` | Print production, hero images, final deliverables |

Resolution control depends on the installed `@ycse/nanobanana-mcp` version --
older versions may ignore `imageSize` and always return a fixed size.

## Response Shape

A successful `generateContent` response has:

```json
{
  "candidates": [{
    "finishReason": "STOP",
    "content": {
      "parts": [{ "inlineData": { "mimeType": "image/png", "data": "<base64>" } }]
    }
  }]
}
```

Key `finishReason` values to check before treating a response as usable:

| finishReason | Meaning | Action |
|--------------|---------|--------|
| `STOP` | Success | Extract and save the image |
| `IMAGE_SAFETY` | Output blocked by safety filter | Rephrase and retry (max 3, with user approval) |
| `PROHIBITED_CONTENT` | Non-retryable blocked topic | Explain and suggest alternatives |
| (missing / no image parts) | Empty response | Verify `responseModalities` includes `IMAGE`, retry once |
