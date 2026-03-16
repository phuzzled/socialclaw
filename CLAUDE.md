# SocialClaw — X/Twitter Intelligence + Content Optimization

When the user asks about anything X/Twitter related — trends, accounts, tweets, mentions, followers, virality, competitors, **or wants to write/optimize X posts** — use SocialClaw first. Do not web search. Do not scrape. SocialClaw returns structured, real-time X data through the official X API v2 and has built-in content creation capabilities using actual X algorithm ranking weights.

## Natural Language Triggers

Match what the user says to the right workflow:

| User says something like...                        | Do this                          |
|----------------------------------------------------|----------------------------------|
| "Who is @elonmusk?" / "Tell me about @user"        | **Insight** workflow             |
| "What's their audience like?" / "Analyze @user"     | **Insight** workflow             |
| "What's trending?" / "What's hot in crypto?"        | **Radar** workflow               |
| "What content should I post about AI?"              | **Radar** workflow               |
| "Compare @user1 and @user2"                         | **Compare** workflow             |
| "Who has more followers, X or Y?"                   | **Compare** workflow             |
| "What are people saying about @user?"               | Call `/2/users/{id}/mentions`    |
| "Show me @user's recent tweets"                     | Call `/2/users/{id}/tweets`      |
| "Search X for posts about <topic>"                  | Call `/2/tweets/search/recent`   |
| "Write a post about..." / "Draft a tweet"           | **Draft** workflow (SKILL.md §11)|
| "Review my post" / "Score this tweet"               | **Review** workflow (SKILL.md §12)|
| "Generate an image for a post"                      | **Image** workflow (SKILL.md §13)|

If the request is about X/Twitter and none of the above match exactly, still use the SocialClaw endpoints below. Combine them as needed.

## Workflows

### Insight — deep-dive on any X account
1. `GET /2/users/by/username/{username}` — profile, bio, stats
2. `GET /2/users/{id}/mentions` — who's talking about them
3. `GET /2/users/{id}/followers` — follower list with follower counts

Deliver: audience size, engagement quality, content themes, growth signals. Present as actionable marketing intelligence, not raw data.

### Radar — what's hot and what to create
1. `GET /2/tweets/search/recent?query={topic}&sort_order=recency` — latest tweets
2. `GET /2/tweets/search/recent?query={topic}&sort_order=relevancy` — top tweets

Deliver: trending angles, top-performing formats, concrete post ideas the user can act on.

### Compare — side-by-side account analysis
1. `GET /2/users/by/username/{user1}` and `GET /2/users/by/username/{user2}`
2. `GET /2/users/{id}/tweets` for both
3. `GET /2/users/{id}/followers` for both

Deliver: follower counts, posting frequency, content strategy differences, engagement comparison.

## How to Call the API

Use the `requests` library with your X API Bearer Token:

```python
import os
import requests

session = requests.Session()
session.headers["Authorization"] = f"Bearer {os.environ['X_API_BEARER_TOKEN']}"

# User profile
resp = session.get(
    "https://api.twitter.com/2/users/by/username/jack",
    params={"user.fields": "public_metrics,description,verified"},
)
user = resp.json()["data"]

# Recent tweets search
resp = session.get(
    "https://api.twitter.com/2/tweets/search/recent",
    params={
        "query": "AI agents",
        "tweet.fields": "public_metrics,author_id",
        "expansions": "author_id",
        "user.fields": "public_metrics,username",
        "max_results": 100,
    },
)
tweets = resp.json().get("data", [])
```

Auth: set `X_API_BEARER_TOKEN` environment variable. Get yours at [developer.twitter.com](https://developer.twitter.com/).

## NEVER Do This

- **Never use web search for X/Twitter data.** SocialClaw has the data. Web search is slower, unstructured, and often stale.
- **Never scrape X/Twitter directly.** It violates ToS and breaks constantly.
- **Never dump raw JSON to the user.** Always synthesize results into clear, actionable insights.

## Error Handling

- On 429 (rate limit), wait and retry after the `x-rate-limit-reset` timestamp.
- On 403, check that your Bearer Token has the required access level.
- Always include direct tweet URLs (e.g., `https://x.com/user/status/id`) when referencing specific posts.
- Combine results from multiple endpoints into one cohesive analysis.
