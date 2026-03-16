# API Reference

SocialSwag uses the official [X API v2](https://docs.x.com/x-api/introduction).

## Setup

```python
import os
import requests

BEARER_TOKEN = os.environ["X_API_BEARER_TOKEN"]

session = requests.Session()
session.headers["Authorization"] = f"Bearer {BEARER_TOKEN}"

# Example: get user profile
resp = session.get(
    "https://api.x.com/2/users/by/username/jack",
    params={"user.fields": "public_metrics,description,verified"},
)
user = resp.json()["data"]
print(f"@{user['username']}: {user['public_metrics']['followers_count']:,} followers")
```

Or use the SocialSwag CLI (handles auth automatically):

```bash
export X_API_BEARER_TOKEN="your_bearer_token_here"
socialswag insight @jack
```

## Authentication

Get your Bearer Token from [developer.x.com](https://developer.x.com/).

```bash
# Option 1: environment variable (recommended)
export X_API_BEARER_TOKEN="your_bearer_token_here"

# Option 2: config file
mkdir -p ~/.socialswag
echo "your_bearer_token_here" > ~/.socialswag/api_key
```

> **Tip:** Never commit your Bearer Token to version control. Use environment variables or the config file.

## Base URL

All X API v2 requests use: `https://api.x.com/2`

(The legacy `https://api.twitter.com/2` base also works but `api.x.com` is the current canonical URL.)

## X/Twitter Endpoints Used by SocialSwag

| Endpoint | What | X API v2 path | Access tier |
|----------|------|---------------|-------------|
| User profile | Profile, bio, stats, verification | `GET /2/users/by/username/{username}` | Free |
| User's tweets | Tweets + engagement metrics | `GET /2/users/{id}/tweets` | Basic+ |
| User's mentions | Tweets mentioning user | `GET /2/users/{id}/mentions` | Basic+ |
| Followers | Follower list | `GET /2/users/{id}/followers` | Basic+ |
| Tweet search | Search recent tweets (7-day window) | `GET /2/tweets/search/recent` | Basic+ |
| Tweet lookup | Single tweet data | `GET /2/tweets/{id}` | Free |
| Replies / thread | Tweets in a conversation | `GET /2/tweets/search/recent?query=conversation_id:{id}` | Basic+ |

### X API Access Tiers

| Tier | Price | Rate limits | Notes |
|------|-------|-------------|-------|
| Free | $0 | 1 app, 500K tweets/month write, limited read | Basic lookups only |
| Basic | $100/month | 10K app read, 5M user read | Most SocialSwag workflows |
| Pro | $5,000/month | 1M app read | Heavy-usage / commercial |
| Enterprise | Custom | Unlimited | Full firehose access |

See [docs.x.com/x-api/getting-started/about-x-api](https://docs.x.com/x-api/getting-started/about-x-api) for up-to-date tier details.

## Per-Workflow API Usage

| Workflow | CLI command | Endpoints called | Approx. API reads |
|----------|-------------|-----------------|-------------------|
| Insight | `insight @handle` | users/by/username, users/{id}/mentions, users/{id}/followers, users/{id}/tweets | ~4 requests |
| Radar | `radar <topic>` | tweets/search/recent ×2 | ~2 requests |
| Compare | `compare @a @b` | users/by/username ×2, users/{id}/mentions ×2, users/{id}/followers ×2 | ~6 requests |
| Audience | `audience @handle` | users/by/username, users/{id}/followers | ~2 requests |
| Scout | `scout <topic>` | tweets/search/recent | ~1 request |
| Hitlist | `hitlist <topic>` | tweets/search/recent | ~1 request |
| Engage | `engage @handle` | users/by/username, users/{id}/mentions, tweets/search/recent | ~3 requests |
| Check | `check @handle` | users/by/username, users/{id}/tweets, users/{id}/mentions | ~3 requests |
| Search | `search <query>` | tweets/search/recent ×2 | ~2 requests |
| Tweet | `tweet <id/url>` | tweets/{id}, tweets/search/recent (replies) | ~2 requests |
| Thread | `thread <id/url>` | tweets/search/recent | ~1 request |
| Analytics | `analytics @handle` | users/by/username, users/{id}/tweets | ~2 requests |
| Brief | `brief @handle` | users/by/username, users/{id}/mentions, users/{id}/followers | ~3 requests |

## Request Fields

SocialSwag requests these fields for maximum data richness:

**User fields:** `public_metrics,description,username,name,verified,created_at,location,url,profile_image_url`

**Tweet fields:** `public_metrics,created_at,author_id,conversation_id,lang,entities`

**Expansions:** `author_id`

## Rate Limits

X API v2 rate limits are per 15-minute window. Key limits (Basic tier):

| Endpoint | Limit per 15 min |
|----------|-----------------|
| `GET /2/users/by/username/{u}` | 300 |
| `GET /2/users/{id}/tweets` | 900 |
| `GET /2/users/{id}/mentions` | 450 |
| `GET /2/users/{id}/followers` | 15 |
| `GET /2/tweets/search/recent` | 180 |
| `GET /2/tweets/{id}` | 300 |

See [docs.x.com/x-api/rate-limits](https://docs.x.com/x-api/rate-limits) for current values.

On `429 Too Many Requests`, SocialSwag surfaces the `x-rate-limit-reset` epoch timestamp.

## AI Models (Optional)

### OpenRouter (Primary - Default: x-ai/grok-4.20-beta)

```bash
export OPENROUTER_API_KEY="your_openrouter_key"
# Optionally change the model:
export OPENROUTER_MODEL="anthropic/claude-3.5-sonnet"
socialswag engage @yourhandle
```

The `engage` workflow uses OpenRouter by default. Get your key at [openrouter.ai](https://openrouter.ai/).

**Popular models:**
- `x-ai/grok-4.20-beta` (default)
- `anthropic/claude-3.5-sonnet`
- `google/gemini-2.0-flash-exp`
- `meta-llama/llama-3.3-70b-instruct`

### OpenAI (Fallback)

```bash
export OPENAI_API_KEY="your_openai_key"
socialswag engage @yourhandle
```

Used as fallback if no OpenRouter key is set. Uses `gpt-4o-mini` by default.

## Image Generation (Optional)

Set `GOOGLE_API_KEY` to enable the `image` workflow using Nano Banana 2 (Gemini 3.1 Flash Image):

```bash
export GOOGLE_API_KEY="your_google_api_key"
socialswag image "description"
```

Cost: ~$0.04 per image. Get your key at [Google AI Studio](https://aistudio.google.com/).

## Data Auto-Save

All responses saved to `~/.socialswag/data/` as timestamped JSON.

```
~/.socialswag/data/
  20240316_091200_users_info_elonmusk.json
  20240316_091205_tweets_search_recent_AI-agents.json
```
