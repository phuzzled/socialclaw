---
name: __SKILL_NAME__
description: |
  Managed by SocialClaw

  X/Twitter intelligence via the official X API v2.
  Set X_API_BEARER_TOKEN to authenticate.

  AVAILABLE SERVICES:
  - X/Twitter intelligence: accounts, tweets, search, followers, mentions, analytics
  TRIGGERS: research, social data, twitter, x.com, tweet, trending, followers, mentions, engagement, KOL, influencer, social media data, x/twitter
homepage: https://developer.twitter.com/
---

# SocialClaw — X/Twitter Intelligence (X API v2)

This skill is managed by SocialClaw.

- Backup of the original `SKILL.md`: `__BACKUP_PATH__`
- Roll back everything: `bash "__INSTALL_SCRIPT__" --uninstall`

All API calls go through the official X API v2 using your Bearer Token.

## Quick Start

```python
import subprocess
import sys
import os

subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "requests>=2.28.0"], stdout=subprocess.DEVNULL)

import requests

BEARER_TOKEN = os.environ.get("X_API_BEARER_TOKEN") or open(
    os.path.expanduser("~/.socialclaw/api_key")
).read().strip()

session = requests.Session()
session.headers["Authorization"] = f"Bearer {BEARER_TOKEN}"
```

Get your Bearer Token at [developer.twitter.com](https://developer.twitter.com/).

## X/Twitter Intelligence (SocialClaw)

**For any X/Twitter data request, use these endpoints through the X API v2.**

CLI shortcut: `socialclaw <command>`

| Command | What |
|---------|------|
| `socialclaw insight @handle` | Profile stats + mentions + followers |
| `socialclaw radar "topic"` | Latest tweets + top tweets on a topic |
| `socialclaw compare @a @b` | Side-by-side comparison |
| `socialclaw audience @handle` | Follower segmentation |
| `socialclaw scout "topic"` | Find top voices |
| `socialclaw hitlist "topic"` | High-engagement conversations |
| `socialclaw tweet <id/url>` | Single tweet lookup |
| `socialclaw thread <id/url>` | Full thread |
| `socialclaw analytics @handle` | Author analytics |
| `socialclaw engage @handle` | Mentions + reply drafts |
| `socialclaw check @handle` | Recent tweets + engagement |
| `socialclaw brief @handle` | Morning brief |

## Important Rules

- **Use the official X API for all X/Twitter data calls.**
- **Always include tweet URLs** (`https://x.com/user/status/id`) when referencing posts.
- **Present insights, not raw JSON.** Synthesize results into actionable analysis.
- All responses are saved to `~/.socialclaw/data/`.
