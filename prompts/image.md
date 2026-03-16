# Image Mode Prompt Template

## Context

You are generating an optimized image for an X post about: **{{DESCRIPTION}}**

## Image Generation

Use the Nano Banana 2 API (Gemini 3.1 Flash Image) directly (requires `GOOGLE_API_KEY`):

```python
import base64
import os
import requests

gemini_key = os.environ.get("GOOGLE_API_KEY")
if not gemini_key:
    print("Set GOOGLE_API_KEY to enable image generation (Nano Banana 2).")
    print("Get your key at: https://aistudio.google.com/")
else:
    description = "{{DESCRIPTION}}"  # CHANGE THIS
    optimized_prompt = (
        f"{description}, high contrast, bold colors, clean composition, "
        "professional quality, minimalist style, 16:9 aspect ratio"
    )

    r = requests.post(
        "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-image-preview:generateContent",
        json={
            "contents": [
                {"parts": [{"text": optimized_prompt}]}
            ],
            "generationConfig": {
                "responseModalities": ["IMAGE"],
            },
        },
        headers={
            "x-goog-api-key": gemini_key,
            "Content-Type": "application/json",
        },
        timeout=60,
    )
    r.raise_for_status()
    parts = r.json()["candidates"][0]["content"]["parts"]
    for part in parts:
        if "inline_data" in part:
            image_data = base64.b64decode(part["inline_data"]["data"])
            with open("generated_image.png", "wb") as f:
                f.write(image_data)
            print("Image saved as: generated_image.png")
            break
```

Cost: ~$0.04–$0.05 per image (Nano Banana 2 / Gemini 3.1 Flash Image).

## X-Optimized Image Guidelines

1. **High Contrast** — Stops the scroll in the feed
2. **Minimal Text** — X algorithm prefers native images over text-heavy graphics
3. **Bold Colors** — Stand out in the timeline
4. **Simple Composition** — Single clear focal point
5. **Aspect Ratio** — 16:9 for optimal X card preview; 1:1 for square posts

## Prompt Enhancement

Take the user's description and always add:
- `"high contrast"`
- `"bold colors"`
- `"clean composition"`
- `"professional quality"`
- Specific style if appropriate (e.g., `"minimalist tech"`, `"abstract"`, `"photorealistic"`)

## Model Selection

| Model | Aspect Ratio | Cost | Use when |
|-------|-------------|------|----------|
| `gemini-3.1-flash-image-preview` | 16:9 | ~$0.04 | Most posts (landscape) |
| `gemini-3.1-flash-image-preview` | 1:1 | ~$0.04 | Square posts |
| `gemini-3.1-flash-image-preview` | 4:3 | ~$0.04 | Blog-style previews |

## Output Format

Present:
1. Generated image (saved file path: `generated_image.png`)
2. The optimized prompt used
3. Suggested accompanying post text
4. Alternative prompt if the user wants variations

## Image Types by Post Category

### Announcements
- Abstract tech visuals, gradients, geometric shapes
- Branded colors + product concept if available

### Educational Content
- Simple diagrams or visual metaphors
- Before/after comparisons
- Step-by-step visual flows

### Personal/Story Posts
- Abstract emotional visuals, atmospheric backgrounds
- Relevant contextual imagery

### Technical Content
- Stylized code snippets on dark background
- Architecture diagrams (minimal, clean)
- Dashboard/UI mockup previews
