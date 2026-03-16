---
name: __SKILL_NAME__
description: |
  Managed by SocialSwag

  X/Twitter intelligence via the official X API v2 + OpenRouter AI.
  Set X_API_BEARER_TOKEN to authenticate. Set OPENROUTER_API_KEY for AI features.

  AVAILABLE SERVICES:
  - X/Twitter intelligence: accounts, tweets, search, followers, mentions, analytics
  - AI analysis: OpenRouter (default: x-ai/grok-4.20-beta)
  TRIGGERS: research, social data, twitter, x.com, tweet, trending, followers, mentions, engagement, KOL, influencer, social media data, x/twitter
homepage: https://developer.x.com/
---

# SocialSwag — X/Twitter Intelligence (X API v2) + OpenRouter AI

This skill is managed by SocialSwag.

- Backup of the original `SKILL.md`: `__BACKUP_PATH__`
- Roll back everything: `bash "__INSTALL_SCRIPT__" --uninstall`

All API calls go through the official X API v2 using your Bearer Token.
AI features use OpenRouter (default: x-ai/grok-4.20-beta).

## Quick Start

```python
import subprocess
import sys
import os

subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "requests>=2.28.0"], stdout=subprocess.DEVNULL)

import requests

BEARER_TOKEN = os.environ.get("X_API_BEARER_TOKEN") or open(
    os.path.expanduser("~/.socialswag/api_key")
).read().strip()

session = requests.Session()
session.headers["Authorization"] = f"Bearer {BEARER_TOKEN}"
```

Get your Bearer Token at [developer.x.com](https://developer.x.com/).

## AI Configuration (Optional)

```bash
# OpenRouter (default model: x-ai/grok-4.20-beta)
export OPENROUTER_API_KEY="your_openrouter_key"
# Change model:
export OPENROUTER_MODEL="anthropic/claude-3.5-sonnet"

# Or use OpenAI as fallback:
export OPENAI_API_KEY="your_openai_key"

# For image generation:
export GOOGLE_API_KEY="your_google_key"
```

## X/Twitter Intelligence (SocialSwag)

**For any X/Twitter data request, use these endpoints through the X API v2.**

CLI shortcut: `socialswag <command>`

| Command | What |
|---------|------|
| `socialswag insight @handle` | Profile stats + mentions + followers |
| `socialswag radar "topic"` | Latest tweets + top tweets on a topic |
| `socialswag compare @a @b` | Side-by-side comparison |
| `socialswag audience @handle` | Follower segmentation |
| `socialswag scout "topic"` | Find top voices |
| `socialswag hitlist "topic"` | High-engagement conversations |
| `socialswag tweet <id/url>` | Single tweet lookup |
| `socialswag thread <id/url>` | Full thread |
| `socialswag analytics @handle` | Author analytics |
| `socialswag engage @handle` | Mentions + AI reply drafts |
| `socialswag check @handle` | Recent tweets + engagement |
| `socialswag brief @handle` | Morning brief |

## Important Rules

- **Use the official X API for all X/Twitter data calls.**
- **Always include tweet URLs** (`https://x.com/user/status/id`) when referencing posts.
- **Present insights, not raw JSON.** Synthesize results into actionable analysis.
- All responses are saved to `~/.socialswag/data/`.