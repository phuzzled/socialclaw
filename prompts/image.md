# Image Mode Prompt Template

## Context

You are generating an optimized image for an X post about: **{{DESCRIPTION}}**

## Image Generation

Use the OpenAI Images API directly (requires `OPENAI_API_KEY`):

```python
import os
import requests

openai_key = os.environ.get("OPENAI_API_KEY")
if not openai_key:
    print("Set OPENAI_API_KEY to enable image generation.")
    print("Get your key at: https://platform.openai.com/api-keys")
else:
    description = "{{DESCRIPTION}}"  # CHANGE THIS
    optimized_prompt = (
        f"{description}, high contrast, bold colors, clean composition, "
        "professional quality, minimalist style, 16:9 aspect ratio"
    )

    r = requests.post(
        "https://api.openai.com/v1/images/generations",
        json={
            "model": "dall-e-3",
            "prompt": optimized_prompt,
            "size": "1792x1024",   # best for X/Twitter preview
            "quality": "standard",
            "n": 1,
        },
        headers={"Authorization": f"Bearer {openai_key}"},
        timeout=60,
    )
    r.raise_for_status()
    image_url = r.json()["data"][0]["url"]
    print(f"Image URL: {image_url}")
    print(f"Revised prompt: {r.json()['data'][0].get('revised_prompt', '')}")
```

Cost: ~$0.040 per image (DALL-E 3 standard), ~$0.080 (HD quality).

## X-Optimized Image Guidelines

1. **High Contrast** — Stops the scroll in the feed
2. **Minimal Text** — X algorithm prefers native images over text-heavy graphics
3. **Bold Colors** — Stand out in the timeline
4. **Simple Composition** — Single clear focal point
5. **Aspect Ratio** — `1792×1024` (16:9) for optimal X card preview; `1024×1024` for square posts

## Prompt Enhancement

Take the user's description and always add:
- `"high contrast"`
- `"bold colors"`
- `"clean composition"`
- `"professional quality"`
- Specific style if appropriate (e.g., `"minimalist tech"`, `"abstract"`, `"photorealistic"`)

## Model Selection

| Model | Size | Quality | Cost | Use when |
|-------|------|---------|------|----------|
| `dall-e-3` | 1792×1024 | standard | $0.040 | Most posts |
| `dall-e-3` | 1024×1024 | hd | $0.080 | Important announcements |
| `dall-e-3` | 1024×1024 | standard | $0.040 | Square posts |

## Output Format

Present:
1. Generated image (URL or saved file path)
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
