# API Reference

SocialClaw uses the official [X API v2](https://developer.twitter.com/en/docs/twitter-api).

## Setup

```python
import os
import requests

BEARER_TOKEN = os.environ["X_API_BEARER_TOKEN"]

session = requests.Session()
session.headers["Authorization"] = f"Bearer {BEARER_TOKEN}"

# Example: get user profile
resp = session.get(
    "https://api.twitter.com/2/users/by/username/jack",
    params={"user.fields": "public_metrics,description,verified"},
)
user = resp.json()["data"]
print(f"@{user['username']}: {user['public_metrics']['followers_count']:,} followers")
```

Or use the SocialClaw CLI (handles auth automatically):

```bash
export X_API_BEARER_TOKEN="your_bearer_token_here"
socialclaw insight @jack
```

## Authentication

Get your Bearer Token from [developer.twitter.com](https://developer.twitter.com/).

```bash
# Option 1: environment variable
export X_API_BEARER_TOKEN="your_bearer_token_here"

# Option 2: config file
mkdir -p ~/.socialclaw
echo "your_bearer_token_here" > ~/.socialclaw/api_key
```

## X/Twitter Endpoints (via X API v2)

| Endpoint | What | X API v2 path |
|----------|------|---------------|
| User profile | Profile, bio, stats, verification | `GET /2/users/by/username/{username}` |
| User's tweets | Tweets + engagement metrics | `GET /2/users/{id}/tweets` |
| User's mentions | Tweets mentioning user | `GET /2/users/{id}/mentions` |
| Followers | Follower list | `GET /2/users/{id}/followers` |
| Tweet search | Search recent tweets | `GET /2/tweets/search/recent` |
| Tweet lookup | Single tweet data | `GET /2/tweets/{id}` |
| Replies | Replies to a tweet | `GET /2/tweets/search/recent?query=conversation_id:{id}` |
| Thread | Full conversation thread | `GET /2/tweets/search/recent?query=conversation_id:{id}` |

## AI Models (Optional)

Set `OPENAI_API_KEY` to enable AI-powered reply drafts in the `engage` workflow:

```bash
export OPENAI_API_KEY="your_openai_key"
socialclaw engage @yourhandle
```

## Data Auto-Save

All responses saved to `~/.socialclaw/data/` as timestamped JSON.
