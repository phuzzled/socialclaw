#!/usr/bin/env python3
"""
SocialSwag — Bluesky Marketing Intelligence + AI Agent

AT Protocol (Bluesky) for structured data. OpenRouter (x-ai/grok-4.20-beta default) for AI analysis.
Nano Banana 2 (Gemini 3.1 Flash Image) for image generation.

Data layer:
  - Bluesky AT Protocol (primary): user profiles, posts, search, followers
  - OpenRouter (default): AI-powered analysis via x-ai/grok-4.20-beta
  - OpenAI (fallback): AI-powered analysis if OPENAI_API_KEY set
  - Nano Banana 2 (optional): image generation via GOOGLE_API_KEY

Environment:
  - BLUESKY_HANDLE: Bluesky handle (e.g., "user.bsky.team")
  - BLUESKY_APP_PASSWORD: Bluesky app password (get from Bluesky settings)
  - OPENROUTER_API_KEY: For AI analysis (default, x-ai/grok-4.20-beta)
  - OPENROUTER_MODEL: Override default model (e.g., "anthropic/claude-3.5-sonnet")
  - OPENAI_API_KEY: Fallback for AI analysis if no OpenRouter key
  - GOOGLE_API_KEY: For image generation

Note: Public data accessible without credentials. Full access requires Bluesky login.

Workflows:
  1. insight @handle      — deep-dive account analysis
  2. radar <topic>         — trending topics + content opportunities
  3. compare @a @b         — side-by-side competitor analysis
  4. audience @handle      — segment followers by influence tier
  5. scout <topic>         — identify top voices in a niche
  6. hitlist <topic>       — rank high-value conversations to join
  7. engage @handle        — find posts & generate reply drafts
  8. check @handle         — verify posted content & engagement
  9. search <query>        — structured search + top posts
 10. post <id_or_uri>      — look up specific post + replies
 11. thread <id_or_uri>   — get full post thread
 12. analytics @handle     — author intelligence report
  13. brief @handle         — morning brief with suggested actions
"""

import json
import os
import subprocess
import sys
from datetime import datetime
from typing import Any, Dict, List, Optional

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from scripts.utils.config import get_bluesky_credentials, get_openai_key, get_openrouter_key, get_openrouter_model
except ImportError:
    from utils.config import get_bluesky_credentials, get_openai_key, get_openrouter_key, get_openrouter_model


def _ensure_deps():
    """Ensure requests library is available."""
    try:
        import requests  # noqa: F401
    except ImportError:
        print("  Installing requests...")
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "-q", "requests"],
            stdout=subprocess.DEVNULL,
        )


# ── Bluesky AT Protocol Client ──────────────────────────────────

class BlueskyClient:
    """Client for Bluesky (AT Protocol) public API."""

    BASE = "https://api.bsky.app/xrpc"

    def __init__(self, handle: str = None, app_password: str = None, timeout: float = 30.0):
        import requests
        self._session = requests.Session()
        self._timeout = timeout
        self._calls = 0
        self._auth = None

        # If credentials provided, authenticate to get access token
        if handle and app_password:
            self._authenticate(handle, app_password)

    def _authenticate(self, handle: str, app_password: str):
        """Authenticate with Bluesky to get session token."""
        try:
            r = self._session.post(
                f"{self.BASE}/com.atproto.server.createSession",
                json={"identifier": handle, "password": app_password},
                timeout=self._timeout,
            )
            r.raise_for_status()
            data = r.json()
            self._auth = data.get("accessJwt")
            self._session.headers["Authorization"] = f"Bearer {self._auth}"
        except Exception as e:
            print(f"  Warning: Bluesky authentication failed: {e}")
            self._auth = None

    def get(self, endpoint: str, **params) -> dict:
        self._calls += 1
        url = f"{self.BASE}/{endpoint.lstrip('/')}"
        try:
            r = self._session.get(
                url,
                params={k: v for k, v in params.items() if v is not None},
                timeout=self._timeout,
            )
            r.raise_for_status()
        except Exception as exc:
            import requests as _req
            if isinstance(exc, _req.exceptions.HTTPError):
                status = exc.response.status_code if exc.response is not None else "?"
                if status == 401:
                    raise RuntimeError(
                        "Bluesky auth failed (401) — check your BLUESKY_HANDLE and "
                        "BLUESKY_APP_PASSWORD. Get an app password from Bluesky settings."
                    ) from exc
                if status == 429:
                    raise RuntimeError(
                        "Bluesky API rate limit reached (429) — please retry later"
                    ) from exc
            raise
        return r.json()

    @property
    def calls(self) -> int:
        return self._calls

    def close(self):
        self._session.close()


# ── Data Normalization ───────────────────────────────────────────

def _norm_user(u: dict) -> dict:
    """Normalize a Bluesky user object to the internal format."""
    return {
        "userName": u.get("handle", ""),
        "name": u.get("displayName", u.get("handle", "")),
        "description": u.get("description", ""),
        "location": "",
        "url": u.get("url", ""),
        "profileImageUrl": u.get("avatar", ""),
        "createdAt": u.get("indexedAt", ""),
        "followers": u.get("followersCount", 0),
        "followersCount": u.get("followersCount", 0),
        "following": u.get("followingCount", 0),
        "followingCount": u.get("followingCount", 0),
        "statusesCount": u.get("postsCount", 0),
        "tweetsCount": u.get("postsCount", 0),
        "listedCount": 0,
        "isBlueVerified": False,
        "id": u.get("did", u.get("id", "")),
        "followers_count": u.get("followersCount", 0),
    }


def _norm_post(post: dict) -> dict:
    """Normalize a Bluesky post object to the internal format."""
    author = post.get("author", {})
    record = post.get("record", {})
    return {
        "id": post.get("uri", ""),
        "text": record.get("text", post.get("text", "")),
        "lang": "",
        "author": _norm_user(author),
        "likeCount": post.get("likeCount", 0),
        "retweetCount": post.get("repostCount", 0),
        "replyCount": post.get("replyCount", 0),
        "quoteCount": 0,
        "viewCount": 0,
        "bookmarkCount": 0,
        "createdAt": record.get("createdAt", post.get("indexedAt", "")),
        "conversationId": "",
    }


def _extract_posts(data: dict) -> list:
    """Extract posts from Bluesky API response."""
    feed = data.get("feed", [])
    return [item.get("post", {}) for item in feed]


# ── Bluesky AT Protocol Endpoint Functions ────────────────────────


def _bsky_get_profile(client: BlueskyClient, handle: str) -> dict:
    """GET app.bsky.actor.getProfile"""
    try:
        data = client.get("app.bsky.actor.getProfile", actor=handle)
        return {"data": _norm_user(data)}
    except Exception as e:
        print(f"  Warning: Could not fetch profile for @{handle}: {e}")
        return {}


def _bsky_get_followers(client: BlueskyClient, handle: str, limit: int = 100) -> dict:
    """GET app.bsky.graph.getFollowers"""
    try:
        data = client.get("app.bsky.graph.getFollowers", actor=handle, limit=limit)
        followers = [_norm_user(u) for u in data.get("followers", [])]
        return {"followers": followers, "total": data.get("total", len(followers))}
    except Exception as e:
        print(f"  Warning: Could not fetch followers for @{handle}: {e}")
        return {"followers": [], "total": 0}


def _bsky_get_following(client: BlueskyClient, handle: str, limit: int = 100) -> dict:
    """GET app.bsky.graph.getFollows"""
    try:
        data = client.get("app.bsky.graph.getFollows", actor=handle, limit=limit)
        following = [_norm_user(u) for u in data.get("following", [])]
        return {"following": following}
    except Exception as e:
        print(f"  Warning: Could not fetch following for @{handle}: {e}")
        return {"following": []}


def _bsky_get_author_feed(client: BlueskyClient, handle: str, limit: int = 20) -> dict:
    """GET app.bsky.feed.getAuthorFeed"""
    try:
        data = client.get("app.bsky.feed.getAuthorFeed", actor=handle, limit=limit)
        posts = [_norm_post(p) for p in _extract_posts(data)]
        return {"posts": posts}
    except Exception as e:
        print(f"  Warning: Could not fetch posts for @{handle}: {e}")
        return {"posts": []}


def _bsky_search_posts(client: BlueskyClient, query: str, limit: int = 25) -> dict:
    """GET app.bsky.feed.searchPosts"""
    try:
        data = client.get("app.bsky.feed.searchPosts", q=query, limit=limit)
        # Search returns posts directly, not wrapped in {"post": ...}
        posts = [_norm_post(p) for p in data.get("posts", [])]
        return {"posts": posts}
    except Exception as e:
        print(f"  Warning: Could not search posts for '{query}': {e}")
        return {"posts": []}


def _bsky_get_post_thread(client: BlueskyClient, uri: str) -> dict:
    """GET app.bsky.feed.getPostThread"""
    try:
        data = client.get("app.bsky.feed.getPostThread", uri=uri, depth=10)
        # Extract posts from thread
        thread = []
        if "thread" in data:
            # Handle threadgate or post
            thread_item = data["thread"]
            if "post" in thread_item:
                thread.append(_norm_post(thread_item["post"]))
            # Add replies if present
            if "replies" in thread_item:
                for reply in thread_item["replies"]:
                    if "post" in reply:
                        thread.append(_norm_post(reply["post"]))
        return {"posts": thread}
    except Exception as e:
        print(f"  Warning: Could not fetch thread for {uri}: {e}")
        return {"posts": []}


# Legacy function names for compatibility
def _x_user_info(client: BlueskyClient, username: str) -> dict:
    """Get user profile (Bluesky handle)"""
    # Strip @ if present
    username = username.lstrip("@")
    return _bsky_get_profile(client, username)


def _x_user_id(client: BlueskyClient, username: str) -> Optional[str]:
    """Resolve a handle to DID."""
    username = username.lstrip("@")
    info = _bsky_get_profile(client, username)
    return info.get("data", {}).get("id")


def _x_user_mentions(client: BlueskyClient, username: str) -> dict:
    """Bluesky doesn't have mentions - use search instead."""
    # Use search to find posts mentioning the user
    username = username.lstrip("@")
    try:
        # Search for posts mentioning the handle
        data = client.get("app.bsky.feed.searchPosts", q=f"@{username}", limit=50)
        posts = [_norm_post(p.get("post", {})) for p in data.get("posts", [])]
        return {"tweets": posts}
    except Exception as e:
        print(f"  Warning: Could not fetch mentions for @{username}: {e}")
        return {"tweets": []}


def _x_user_tweets(client: BlueskyClient, username: str) -> dict:
    """GET app.bsky.feed.getAuthorFeed"""
    username = username.lstrip("@")
    return _bsky_get_author_feed(client, username)


def _x_user_followers(client: BlueskyClient, username: str) -> dict:
    """GET app.bsky.graph.getFollowers"""
    username = username.lstrip("@")
    return _bsky_get_followers(client, username)


def _x_search(client: BlueskyClient, query: str, query_type: str = "Latest") -> dict:
    """GET app.bsky.feed.searchPosts"""
    # Bluesky doesn't have "Latest" vs "Top" - just returns recent by relevance
    result = _bsky_search_posts(client, query)
    # Map "posts" to "tweets" for compatibility with existing workflow code
    return {"tweets": result.get("posts", [])}


def _x_trending(_client: BlueskyClient) -> dict:
    """Bluesky doesn't have trending topics API."""
    # Could implement by searching for popular hashtags
    return {"data": {"topics": []}}


def _x_articles_rising(_client: BlueskyClient) -> dict:
    """Bluesky doesn't have articles feature."""
    return {"data": {"articles": []}}


def _x_tweet_lookup(client: BlueskyClient, post_uri: str) -> dict:
    """GET app.bsky.feed.getPostThread"""
    if not post_uri:
        return {"tweets": []}
    try:
        # Ensure URI has the proper format
        if not post_uri.startswith("at://"):
            post_uri = f"at://{post_uri}"
        data = client.get("app.bsky.feed.getPostThread", uri=post_uri, depth=1)
        if "thread" in data and "post" in data["thread"]:
            return {"tweets": [_norm_post(data["thread"]["post"])]}
        return {"tweets": []}
    except Exception as e:
        print(f"  Warning: Could not fetch post {post_uri}: {e}")
        return {"tweets": []}


def _x_tweet_replies(client: BlueskyClient, post_uri: str) -> dict:
    """Get replies to a post."""
    try:
        if not post_uri.startswith("at://"):
            post_uri = f"at://{post_uri}"
        data = client.get("app.bsky.feed.getPostThread", uri=post_uri, depth=10)
        posts = []
        if "thread" in data:
            thread = data["thread"]
            if "replies" in thread:
                for reply in thread["replies"]:
                    if "post" in reply:
                        posts.append(_norm_post(reply["post"]))
        return {"tweets": posts}
    except Exception as e:
        print(f"  Warning: Could not fetch replies for {post_uri}: {e}")
        return {"tweets": []}


def _x_tweet_thread(client: BlueskyClient, post_uri: str) -> dict:
    """Get a post thread."""
    if not post_uri.startswith("at://"):
        post_uri = f"at://{post_uri}"
    return _bsky_get_post_thread(client, post_uri)


def _x_author_analytics(client: BlueskyClient, handle: str) -> dict:
    """Compute basic author analytics from profile + recent posts."""
    handle = handle.lstrip("@")
    try:
        user_data = _x_user_info(client, handle).get("data", {})
        recent = _x_user_tweets(client, handle)
        tweets = recent.get("tweets", [])
        n = len(tweets) or 1
        total_likes = sum(tw.get("likeCount", 0) for tw in tweets)
        total_rts = sum(tw.get("retweetCount", 0) for tw in tweets)
        total_replies = sum(tw.get("replyCount", 0) for tw in tweets)
        return {
            "data": {
                "followers": user_data.get("followers", 0),
                "following": user_data.get("following", 0),
                "totalTweets": user_data.get("tweetsCount", 0),
                "recentTweetsSampled": len(tweets),
                "avgLikesPerTweet": round(total_likes / n, 1),
                "avgRetweetsPerTweet": round(total_rts / n, 1),
                "avgRepliesPerTweet": round(total_replies / n, 1),
                "totalEngagement": total_likes + total_rts + total_replies,
            }
        }
    except Exception as e:
        print(f"  Warning: Could not compute analytics for @{handle}: {e}")
        return {}


# ── API Dispatcher ───────────────────────────────────────────────

def _api(client: BlueskyClient, endpoint: str, body: dict) -> dict:
    """
    Route old-style endpoint calls to the appropriate Bluesky API function.

    This dispatcher preserves the existing workflow code structure while
    mapping to the Bluesky AT Protocol under the hood.
    """
    username = body.get("username") or body.get("handle", "")

    if endpoint == "/v1/x/users/info":
        return _x_user_info(client, username)
    elif endpoint == "/v1/x/users/mentions":
        return _x_user_mentions(client, username)
    elif endpoint == "/v1/x/users/followers":
        return _x_user_followers(client, username)
    elif endpoint == "/v1/x/users/tweets":
        return _x_user_tweets(client, username)
    elif endpoint == "/v1/x/trending":
        return _x_trending(client)
    elif endpoint == "/v1/x/articles/rising":
        return _x_articles_rising(client)
    elif endpoint == "/v1/x/search":
        return _x_search(client, body.get("query", ""), body.get("queryType", "Latest"))
    elif endpoint == "/v1/x/tweets/lookup":
        return _x_tweet_lookup(client, body.get("tweetIds", [''])[0] if body.get("tweetIds") else "")
    elif endpoint == "/v1/x/tweets/replies":
        return _x_tweet_replies(client, body.get("tweetId", ""))
    elif endpoint == "/v1/x/tweets/thread":
        return _x_tweet_thread(client, body.get("tweetId", ""))
    elif endpoint == "/v1/x/authors/analytics":
        return _x_author_analytics(client, username)
    else:
        print(f"  Warning: Unknown endpoint {endpoint}")
        return {}



def _unwrap_data(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Unwrap nested API payloads like {'data': {'data': {...}}}."""
    data: Dict[str, Any] = payload.get("data", payload)
    while isinstance(data, dict) and isinstance(data.get("data"), dict):
        data = data["data"]
    return data


def _follower_count(entity: dict) -> int:
    return (
        entity.get("followers")
        or entity.get("followersCount")
        or entity.get("followers_count")
        or 0
    )


def _bio_text(entity: dict) -> str:
    return entity.get("description") or entity.get("bio") or ""


def _display_name(entity: dict) -> str:
    return entity.get("name") or entity.get("displayName") or entity.get("userName") or "?"


def _get_client() -> BlueskyClient:
    """Get a Bluesky client using the configured credentials."""
    creds = get_bluesky_credentials()
    if creds:
        handle, app_password = creds
        return BlueskyClient(handle, app_password)
    # If no credentials, create client without auth (public data only)
    return BlueskyClient()


DATA_DIR = os.path.expanduser("~/.socialswag/data")


def _save_local(endpoint: str, body: dict, result):
    """Save API response locally for future reference."""
    os.makedirs(DATA_DIR, exist_ok=True)

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    slug = endpoint.strip("/").replace("v1/x/", "").replace("v1/", "").replace("/", "_")

    ctx = ""
    if isinstance(body, dict):
        ctx = body.get("username") or body.get("query") or body.get("handle") or ""
    ctx = str(ctx).replace(" ", "-").replace("@", "")[:30]
    if ctx:
        slug = f"{slug}_{ctx}"

    filename = f"{ts}_{slug}.json"
    filepath = os.path.join(DATA_DIR, filename)

    save_data = result if isinstance(result, dict) else {"text": str(result)}
    with open(filepath, "w") as f:
        json.dump({"endpoint": endpoint, "request": body, "response": save_data,
                    "timestamp": ts}, f, indent=2, ensure_ascii=False)
    return filepath


def _ai_analyze(prompt: str, system: str = None) -> Optional[str]:
    """
    Optional AI analysis using OpenRouter (default: x-ai/grok-4.20-beta).
    Falls back to OpenAI if OPENAI_API_KEY is set but OPENROUTER_API_KEY is not.

    Returns the AI response string, or None if no key is configured.
    """
    # Priority: OpenRouter > OpenAI
    openrouter_key = get_openrouter_key()
    openai_key = get_openai_key()

    if not openrouter_key and not openai_key:
        return None

    try:
        import requests as _req
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        # Use OpenRouter if available
        if openrouter_key:
            model = get_openrouter_model()
            r = _req.post(
                "https://openrouter.ai/api/v1/chat/completions",
                json={"model": model, "messages": messages, "max_tokens": 3000},
                headers={
                    "Authorization": f"Bearer {openrouter_key}",
                    "HTTP-Referer": "https://socialswag.ai",
                    "X-Title": "SocialSwag",
                },
                timeout=60,
            )
            r.raise_for_status()
            return r.json()["choices"][0]["message"]["content"]

        # Fallback to OpenAI
        r = _req.post(
            "https://api.openai.com/v1/chat/completions",
            json={"model": "gpt-4o-mini", "messages": messages, "max_tokens": 3000},
            headers={"Authorization": f"Bearer {openai_key}"},
            timeout=60,
        )
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"  Note: AI analysis unavailable: {e}")
        return None


def _x_search_text(client: BlueskyClient, query: str, *, max_results: int = 10) -> str:
    """
    Search Bluesky and return a formatted plain-text summary.

    Used as the human-readable output replacement for Grok Live Search.
    """
    result = _x_search(client, query, "Latest")
    posts = result.get("tweets", [])[:max_results]
    if not posts:
        return f"No recent posts found for: {query}"
    lines = []
    for tw in posts:
        author = tw.get("author", {})
        handle = author.get("userName", "?")
        text = tw.get("text", "")[:200].replace("\n", " ")
        likes = tw.get("likeCount", 0)
        rts = tw.get("retweetCount", 0)
        link = _post_link(tw)
        lines.append(f"@{handle}: {text}")
        lines.append(f"  Likes: {likes:,}  Reposts: {rts:,}")
        if link:
            lines.append(f"  {link}")
        lines.append("")
    return "\n".join(lines)


def _smart_search(client: BlueskyClient, query: str, query_type: str = "Latest") -> Dict[str, Any]:
    """Search Bluesky via the API and return structured results."""
    result = _x_search(client, query, query_type)
    return {"source": "api", "data": result}


def _smart_user_tweets(client: BlueskyClient, username: str) -> Dict[str, Any]:
    """Fetch a user's recent posts via the API."""
    result = _x_user_tweets(client, username)
    return {"source": "api", "data": result}


# ── Display Helpers ────────────────────────────────────────────

def _post_link(tw: dict) -> str:
    """Get direct link to a Bluesky post."""
    uri = tw.get("id", "")
    author = tw.get("author", {})
    handle = author.get("userName", "")
    if uri and handle:
        # URI format: at://did:plc:.../app.bsky.feed.post/...
        # Extract the rkey (last part after /)
        if "/app.bsky.feed.post/" in uri:
            rkey = uri.split("/app.bsky.feed.post/")[-1]
            return f"https://bsky.app/profile/{handle}/post/{rkey}"
        return f"https://bsky.app/profile/{handle}"
    return ""


# Keep old name for backwards compatibility
def _tweet_link(tw: dict) -> str:
    """Get direct link (alias for _post_link)."""
    return _post_link(tw)


def _print_tweet(tw: dict, indent: str = "    ", max_text: int = 100):
    """Print a tweet with author, engagement, text, and link."""
    author = tw.get("author", {})
    handle = author.get("userName", "?")
    text = tw.get("text", "")[:max_text].replace("\n", " ")
    likes = tw.get("likeCount", 0)
    rts = tw.get("retweetCount", 0)
    link = _tweet_link(tw)
    print(f"{indent}@{handle:<16} {likes:>3} likes  {rts:>3} RTs  {text}")
    if link:
        print(f"{indent}  {link}")


def _print_grok_result(result: Dict[str, Any], label: str = ""):
    """Print result from either structured API or text fallback."""
    if result["source"] == "api":
        tweets = result["data"].get("tweets", [])
        if label:
            print(f"\n  {label} ({len(tweets)} found)")
        for tw in tweets[:8]:
            _print_tweet(tw, max_text=110)
    else:
        if label:
            print(f"\n  {label}")
        print(result["data"])


# ── Workflow 1: Insight Report ──────────────────────────────────

def insight(username: str):
    """Deep-dive analysis of a Bluesky account."""
    username = username.lstrip("@")
    client = _get_client()

    print(f"\n{'=' * 60}")
    print(f"  SOCIALCLAW INSIGHT — @{username}")
    print(f"{'=' * 60}")

    # 1. Profile (structured API — stable)
    print("\n  Fetching profile...")
    info = _api(client, "/v1/x/users/info", {"username": username})
    d = _unwrap_data(info)

    followers = _follower_count(d)
    following = d.get("following") or d.get("followingCount") or 0
    tweets = d.get("statusesCount") or d.get("tweetsCount") or 0
    verified = d.get("isBlueVerified", False)
    bio = _bio_text(d)
    name = _display_name(d) or username

    print(f"\n  PROFILE")
    print(f"  {'Name:':<14} {name}")
    print(f"  {'Bio:':<14} {bio[:120]}")
    print(f"  {'Followers:':<14} {followers:,}")
    print(f"  {'Following:':<14} {following:,}")
    print(f"  {'Tweets:':<14} {tweets:,}")
    print(f"  {'Verified:':<14} {'Yes' if verified else 'No'}")
    if followers and following:
        ratio = followers / max(following, 1)
        print(f"  {'F/F Ratio:':<14} {ratio:.1f}x")

    # 2. Mentions (structured API — stable)
    print("\n  Fetching mentions...")
    mentions = _api(client, "/v1/x/users/mentions", {"username": username})
    mention_tweets = mentions.get("tweets", [])

    print(f"\n  MENTIONS ({len(mention_tweets)} recent)")
    for tw in mention_tweets[:5]:
        _print_tweet(tw)

    # 3. Followers (structured API — stable)
    print("\n  Fetching followers...")
    fdata = _api(client, "/v1/x/users/followers", {"username": username})
    follower_list = fdata.get("followers", [])

    top_followers = sorted(
        follower_list, key=lambda x: x.get("followers_count", 0), reverse=True
    )[:10]

    print(f"\n  TOP FOLLOWERS (by their follower count)")
    for f in top_followers:
        v = "+" if f.get("isBlueVerified") else " "
        fname = f.get("userName", "?")
        fc = f.get("followers_count", 0)
        print(f"    {v} @{fname:<22} {fc:>10,} followers")

    # 4. Recent tweets
    print("\n  Fetching recent tweets...")
    tweets_result = _smart_user_tweets(client, username)
    _print_grok_result(tweets_result, "RECENT TWEETS")

    # 5. Engagement analysis from mentions
    if mention_tweets:
        total_likes = sum(tw.get("likeCount", 0) for tw in mention_tweets)
        total_rts = sum(tw.get("retweetCount", 0) for tw in mention_tweets)
        avg_likes = total_likes / len(mention_tweets)
        avg_rts = total_rts / len(mention_tweets)
        print(f"\n  MENTION ENGAGEMENT (last {len(mention_tweets)} mentions)")
        print(f"    Avg likes per mention:    {avg_likes:.1f}")
        print(f"    Avg retweets per mention: {avg_rts:.1f}")
        print(f"    Total reach (likes+RTs):  {total_likes + total_rts:,}")

    _print_cost(client)
    client.close()


# ── Workflow 2: Topic Radar ─────────────────────────────────────

def radar(topic: str):
    """What's hot on Bluesky around a topic."""
    client = _get_client()

    print(f"\n{'=' * 60}")
    print(f"  SOCIALCLAW RADAR — \"{topic}\"")
    print(f"{'=' * 60}")

    # 1. Trending (structured API — stable)
    print("\n  Fetching trending topics...")
    trending = _api(client, "/v1/x/trending", {})
    topics = trending.get("data", {}).get("topics", [])

    print(f"\n  TRENDING NOW (top 10)")
    for t in topics[:10]:
        name = t.get("name", "?")
        articles = t.get("articleCount", 0)
        views = t.get("totalViews", 0)
        match = " <--" if topic.lower() in name.lower() else ""
        print(f"    {name:<28} {articles:>4} articles  {views:>12,} views{match}")

    # 2. Search latest
    print(f"\n  Searching \"{topic}\"...")
    search_result = _smart_search(client, topic, "Latest")
    _print_grok_result(search_result, "LATEST TWEETS")

    # 3. Top tweets
    print(f"\n  Searching top tweets...")
    top_result = _smart_search(client, topic, "Top")
    _print_grok_result(top_result, "TOP PERFORMING POSTS")

    # 4. Rising articles (not available in X API v2 standard tier)
    print("\n  Fetching rising articles...")
    rising = _api(client, "/v1/x/articles/rising", {})
    articles = rising.get("data", {}).get("articles", [])

    relevant = [a for a in articles if topic.lower() in json.dumps(a).lower()]
    show_articles = relevant[:5] if relevant else articles[:5]

    print(f"\n  RISING ARTICLES {'(topic-related)' if relevant else '(general)'}")
    for a in show_articles:
        title = a.get("title", "?")[:70]
        url = a.get("url", "")
        score = a.get("score", "?")
        print(f"    [{score}] {title}")
        if url:
            print(f"         {url[:80]}")

    # 5. Engagement summary
    if search_result["source"] == "api":
        search_tweets = search_result["data"].get("tweets", [])
        if search_tweets:
            total_likes = sum(tw.get("likeCount", 0) for tw in search_tweets)
            total_rts = sum(tw.get("retweetCount", 0) for tw in search_tweets)
            print(f"\n  TOPIC PULSE")
            print(f"    Total engagement (latest {len(search_tweets)} tweets): {total_likes + total_rts:,}")
            print(f"    Avg likes per tweet: {total_likes / len(search_tweets):.1f}")

    _print_cost(client)
    client.close()


# ── Workflow 3: Competitor Compare ──────────────────────────────

def compare(user1: str, user2: str):
    """Side-by-side comparison of two X accounts."""
    user1 = user1.lstrip("@")
    user2 = user2.lstrip("@")
    client = _get_client()

    print(f"\n{'=' * 60}")
    print(f"  SOCIALCLAW COMPARE — @{user1} vs @{user2}")
    print(f"{'=' * 60}")

    # Profiles (structured API — stable)
    print("\n  Fetching profiles...")
    info1 = _unwrap_data(_api(client, "/v1/x/users/info", {"username": user1}))
    info2 = _unwrap_data(_api(client, "/v1/x/users/info", {"username": user2}))

    def _get(d, *keys):
        for k in keys:
            if d.get(k):
                return d[k]
        return 0

    f1 = _get(info1, "followersCount", "followers")
    f2 = _get(info2, "followersCount", "followers")
    fw1 = _get(info1, "followingCount", "following")
    fw2 = _get(info2, "followingCount", "following")
    t1 = _get(info1, "statusesCount", "tweetsCount")
    t2 = _get(info2, "statusesCount", "tweetsCount")

    print(f"\n  {'METRIC':<20} {'@' + user1:>18} {'@' + user2:>18}")
    print(f"  {'-' * 56}")
    print(f"  {'Followers':<20} {f1:>18,} {f2:>18,}")
    print(f"  {'Following':<20} {fw1:>18,} {fw2:>18,}")
    print(f"  {'Tweets':<20} {t1:>18,} {t2:>18,}")

    v1 = "Yes" if info1.get("isBlueVerified") else "No"
    v2 = "Yes" if info2.get("isBlueVerified") else "No"
    print(f"  {'Verified':<20} {v1:>18} {v2:>18}")

    r1 = f1 / max(fw1, 1)
    r2 = f2 / max(fw2, 1)
    print(f"  {'F/F Ratio':<20} {r1:>17.1f}x {r2:>17.1f}x")

    # Mentions (structured API — stable)
    print("\n  Fetching mentions...")
    m1 = _api(client, "/v1/x/users/mentions", {"username": user1}).get("tweets", [])
    m2 = _api(client, "/v1/x/users/mentions", {"username": user2}).get("tweets", [])

    ml1 = sum(tw.get("likeCount", 0) for tw in m1)
    ml2 = sum(tw.get("likeCount", 0) for tw in m2)
    mr1 = sum(tw.get("retweetCount", 0) for tw in m1)
    mr2 = sum(tw.get("retweetCount", 0) for tw in m2)

    print(f"\n  {'MENTIONS':<20} {'@' + user1:>18} {'@' + user2:>18}")
    print(f"  {'-' * 56}")
    print(f"  {'Recent mentions':<20} {len(m1):>18} {len(m2):>18}")
    print(f"  {'Total likes':<20} {ml1:>18,} {ml2:>18,}")
    print(f"  {'Total RTs':<20} {mr1:>18,} {mr2:>18,}")
    if m1:
        print(f"  {'Avg likes/mention':<20} {ml1/len(m1):>17.1f} ", end="")
    else:
        print(f"  {'Avg likes/mention':<20} {'--':>18} ", end="")
    if m2:
        print(f"{ml2/len(m2):>17.1f}")
    else:
        print(f"{'--':>18}")

    # Followers (structured API — stable)
    print("\n  Fetching followers...")
    fl1 = _api(client, "/v1/x/users/followers", {"username": user1}).get("followers", [])
    fl2 = _api(client, "/v1/x/users/followers", {"username": user2}).get("followers", [])

    top1 = sorted(fl1, key=lambda x: x.get("followers_count", 0), reverse=True)[:3]
    top2 = sorted(fl2, key=lambda x: x.get("followers_count", 0), reverse=True)[:3]

    print(f"\n  TOP FOLLOWERS")
    print(f"  @{user1}:")
    for f in top1:
        print(f"    @{f.get('userName', '?'):<20} {f.get('followers_count', 0):>10,}")
    print(f"  @{user2}:")
    for f in top2:
        print(f"    @{f.get('userName', '?'):<20} {f.get('followers_count', 0):>10,}")

    # Verdict
    print(f"\n  QUICK TAKE")
    if f1 > f2:
        print(f"    @{user1} has {f1/max(f2,1):.1f}x more followers")
    else:
        print(f"    @{user2} has {f2/max(f1,1):.1f}x more followers")

    if ml1 + mr1 > ml2 + mr2:
        print(f"    @{user1} gets more mention engagement ({ml1+mr1:,} vs {ml2+mr2:,})")
    else:
        print(f"    @{user2} gets more mention engagement ({ml2+mr2:,} vs {ml1+mr1:,})")

    _print_cost(client)
    client.close()


# ── Workflow 4: Audience ────────────────────────────────────────

def audience(username: str):
    """Segment an account's followers by influence tier."""
    username = username.lstrip("@")
    client = _get_client()

    print(f"\n{'=' * 60}")
    print(f"  SOCIALCLAW AUDIENCE — @{username}")
    print(f"{'=' * 60}")

    print("\n  Fetching followers...")
    fdata = _api(client, "/v1/x/users/followers", {"username": username})
    follower_list = fdata.get("followers", [])

    if not follower_list:
        print("\n  No follower data returned.")
        _print_cost(client)
        client.close()
        return

    buckets = {
        "mega": {"label": "100K+ followers", "items": []},
        "macro": {"label": "10K-100K followers", "items": []},
        "micro": {"label": "1K-10K followers", "items": []},
        "emerging": {"label": "<1K followers", "items": []},
    }

    for follower in follower_list:
        followers = _follower_count(follower)
        if followers >= 100_000:
            buckets["mega"]["items"].append(follower)
        elif followers >= 10_000:
            buckets["macro"]["items"].append(follower)
        elif followers >= 1_000:
            buckets["micro"]["items"].append(follower)
        else:
            buckets["emerging"]["items"].append(follower)

    print(f"\n  FOLLOWER TIERS ({len(follower_list)} sampled)")
    for key in ("mega", "macro", "micro", "emerging"):
        print(f"    {buckets[key]['label']:<20} {len(buckets[key]['items']):>4}")

    for key in ("mega", "macro", "micro"):
        items = sorted(
            buckets[key]["items"],
            key=lambda item: _follower_count(item),
            reverse=True,
        )[:5]
        if not items:
            continue

        print(f"\n  TOP {buckets[key]['label'].upper()}")
        for item in items:
            handle = item.get("userName", "?")
            name = _display_name(item)
            followers = _follower_count(item)
            bio = _bio_text(item)[:70]
            print(f"    @{handle:<20} {followers:>10,} followers  {name}")
            if bio:
                print(f"      {bio}")

    verified = [f for f in follower_list if f.get("isBlueVerified")]
    print(f"\n  SIGNALS")
    print(f"    Verified followers: {len(verified)}")
    print(f"    Top 10 followers hold: {sum(_follower_count(f) for f in sorted(follower_list, key=_follower_count, reverse=True)[:10]):,} combined followers")

    _print_cost(client)
    client.close()


# ── Workflow 5: Scout ───────────────────────────────────────────

def scout(topic: str):
    """Find top voices talking about a topic."""
    client = _get_client()

    print(f"\n{'=' * 60}")
    print(f"  SOCIALCLAW SCOUT — \"{topic}\"")
    print(f"{'=' * 60}")

    print(f"\n  Searching top tweets...")
    search_result = _smart_search(client, topic, "Top")

    if search_result["source"] != "api":
        print(f"\n  TOP VOICES (via Grok Live Search)")
        print(search_result["data"])
        _print_cost(client)
        client.close()
        return

    tweets = search_result["data"].get("tweets", [])
    if not tweets:
        print("\n  No tweets returned.")
        _print_cost(client)
        client.close()
        return

    authors: Dict[str, Dict[str, Any]] = {}
    for tw in tweets:
        author = tw.get("author", {})
        handle = author.get("userName")
        if not handle:
            continue
        followers = _follower_count(author)
        engagement = tw.get("likeCount", 0) + tw.get("retweetCount", 0)
        entry = authors.setdefault(
            handle,
            {
                "followers": followers,
                "name": _display_name(author),
                "bio": _bio_text(author),
                "engagement": engagement,
                "sample": tw.get("text", ""),
                "link": _tweet_link(tw),
            },
        )
        if followers > entry["followers"] or engagement > entry["engagement"]:
            entry["followers"] = max(entry["followers"], followers)
            entry["engagement"] = max(entry["engagement"], engagement)
            entry["sample"] = tw.get("text", "")
            entry["link"] = _tweet_link(tw)
            if _bio_text(author):
                entry["bio"] = _bio_text(author)

    ranked = sorted(
        authors.items(),
        key=lambda item: (item[1]["followers"], item[1]["engagement"]),
        reverse=True,
    )

    print(f"\n  TOP VOICES ({len(ranked)} unique authors)")
    for handle, data in ranked[:10]:
        bio = (data.get("bio") or "")[:70]
        sample = (data.get("sample") or "")[:110].replace("\n", " ")
        print(f"    @{handle:<20} {data['followers']:>10,} followers  {data['engagement']:>6} engagement")
        if bio:
            print(f"      {bio}")
        if sample:
            print(f"      \"{sample}\"")
        if data.get("link"):
            print(f"      {data['link']}")

    _print_cost(client)
    client.close()


def _suggest_reply_angle(text: str, topic: str) -> str:
    lowered = text.lower()
    if "?" in text:
        return "Answer the question with one concrete example or metric."
    if any(token in lowered for token in (" vs ", "versus", "compare", "better", "worse")):
        return "Add a differentiated tradeoff or benchmark instead of a generic opinion."
    if any(token in lowered for token in ("cost", "price", "cheap", "expensive", "save")):
        return "Reply with a concrete cost or performance datapoint."
    if any(token in lowered for token in ("launch", "launched", "shipping", "released", "announcement")):
        return "Connect the launch to a practical use case or user outcome."
    return f"Add one sharp insight or operator datapoint related to {topic}."


# ── Workflow 6: Hitlist ─────────────────────────────────────────

def hitlist(topic: str):
    """Find high-value conversations worth engaging with right now."""
    client = _get_client()

    print(f"\n{'=' * 60}")
    print(f"  SOCIALCLAW HITLIST — \"{topic}\"")
    print(f"{'=' * 60}")

    print(f"\n  Searching recent tweets...")
    search_result = _smart_search(client, topic, "Latest")

    if search_result["source"] != "api":
        print(f"\n  ENGAGEMENT TARGETS (via Grok Live Search)")
        print(search_result["data"])
        _print_cost(client)
        client.close()
        return

    tweets = search_result["data"].get("tweets", [])
    if not tweets:
        print("\n  No tweets returned.")
        _print_cost(client)
        client.close()
        return

    ranked = sorted(
        tweets,
        key=lambda tw: (
            tw.get("likeCount", 0) + tw.get("retweetCount", 0),
            _follower_count(tw.get("author", {})),
        ),
        reverse=True,
    )

    print(f"\n  ENGAGEMENT TARGETS")
    for tw in ranked[:10]:
        author = tw.get("author", {})
        handle = author.get("userName", "?")
        followers = _follower_count(author)
        engagement = tw.get("likeCount", 0) + tw.get("retweetCount", 0)
        text = tw.get("text", "")[:140].replace("\n", " ")
        link = _tweet_link(tw)
        print(f"    @{handle:<18} {followers:>9,} followers  {engagement:>5} engagement")
        print(f"      {text}")
        if link:
            print(f"      {link}")
        print(f"      Suggest: {_suggest_reply_angle(tw.get('text', ''), topic)}")

    _print_cost(client)
    client.close()


# ── Workflow 7: Engage ──────────────────────────────────────────

def engage(username: str, product: str = None):
    """
    Find unanswered mentions & high-value conversations, generate reply drafts.

    Uses AI analysis if OPENAI_API_KEY is set; otherwise shows raw mention data.
    """
    username = username.lstrip("@")
    client = _get_client()

    products_context = product or "SocialSwag (Bluesky intelligence)"

    print(f"\n{'=' * 60}")
    print(f"  SOCIALCLAW ENGAGE — @{username}")
    print(f"{'=' * 60}")

    # 1. Get mentions
    print("\n  Fetching mentions...")
    mentions = _api(client, "/v1/x/users/mentions", {"username": username})
    mention_tweets = mentions.get("tweets", [])

    print(f"\n  INCOMING MENTIONS ({len(mention_tweets)} found)")
    for tw in mention_tweets[:10]:
        _print_tweet(tw, max_text=150)
        print()

    # 2. AI analysis (optional — requires OPENAI_API_KEY)
    mention_summary = []
    for tw in mention_tweets[:15]:
        author = tw.get("author", {})
        mention_summary.append({
            "handle": author.get("userName", "?"),
            "followers": author.get("followers", author.get("followersCount", 0)),
            "text": tw.get("text", "")[:200],
            "likes": tw.get("likeCount", 0),
            "rts": tw.get("retweetCount", 0),
            "link": _tweet_link(tw),
        })

    ai_prompt = f"""Analyze these mentions of @{username} and generate engagement replies.

MENTIONS:
{json.dumps(mention_summary, indent=2)}

PRODUCTS TO PROMOTE (when relevant):
{products_context}

For each mention that deserves a reply, output:
1. PRIORITY: high/medium/low (based on author followers, engagement, relevance)
2. TWEET: the original tweet text and link
3. REPLY DRAFT: a natural, non-spammy reply that adds value.
4. REASON: why this mention is worth replying to

Skip mentions that are just "GM", emoji-only, or spam.
Focus on: questions, feature requests, comparisons, and high-follower accounts.

Output as structured text, not JSON."""

    analysis = _ai_analyze(
        ai_prompt,
        system="You are a social media growth strategist. Generate authentic, value-adding replies — never generic or spammy. Always include the tweet URL in your output.",
    )

    print(f"\n  ENGAGEMENT RECOMMENDATIONS")
    print(f"  {'-' * 56}")
    if analysis:
        print(analysis)
    else:
        print("  (Set OPENAI_API_KEY to enable AI-generated reply suggestions)")
        print("\n  High-priority mentions (by follower count):")
        sorted_mentions = sorted(
            mention_summary,
            key=lambda m: m.get("followers", 0),
            reverse=True,
        )
        for m in sorted_mentions[:5]:
            print(f"    @{m['handle']} ({m['followers']:,} followers) — {m['text'][:100]}")
            if m.get("link"):
                print(f"      {m['link']}")

    # 3. Find high-value conversations to join via X API search
    print(f"\n  Finding conversations to join...")
    opportunities = _x_search_text(
        client,
        "AI agents OR LLM infrastructure OR model routing",
        max_results=10,
    )

    print(f"\n  HIGH-VALUE CONVERSATION OPPORTUNITIES")
    print(f"  {'-' * 56}")
    print(opportunities)

    _print_cost(client)
    client.close()


# ── Workflow 8: Check ───────────────────────────────────────────

def check(username: str):
    """
    Verify posted tweets and check engagement.
    """
    username = username.lstrip("@")
    client = _get_client()

    print(f"\n{'=' * 60}")
    print(f"  SOCIALCLAW CHECK — @{username}")
    print(f"{'=' * 60}")

    # 1. Profile stats
    print("\n  Fetching profile...")
    info = _api(client, "/v1/x/users/info", {"username": username})
    d = _unwrap_data(info)

    followers = _follower_count(d)
    print(f"  Followers: {followers:,}")

    # 2. Latest tweets via X API
    print("\n  Fetching latest tweets...")
    tweets_result = _x_user_tweets(client, username)
    tweets = tweets_result.get("tweets", [])

    print(f"\n  LATEST TWEETS & ENGAGEMENT")
    print(f"  {'-' * 56}")
    if tweets:
        for tw in tweets[:15]:
            _print_tweet(tw, max_text=150)
            print()
    else:
        print("  No recent posts found.")

    # 3. Mention activity (structured API — stable)
    print("\n  Fetching new mentions...")
    mentions = _api(client, "/v1/x/users/mentions", {"username": username})
    mention_tweets = mentions.get("tweets", [])

    unanswered = []
    for tw in mention_tweets[:10]:
        author = tw.get("author", {})
        handle = author.get("userName", "?")
        if handle.lower() != username.lower():
            unanswered.append(tw)

    if unanswered:
        print(f"\n  MENTIONS TO CHECK ({len(unanswered)} from others)")
        for tw in unanswered[:10]:
            _print_tweet(tw, max_text=150)
            print()
    else:
        print("\n  No new mentions from others.")

    _print_cost(client)
    client.close()


# ── Workflow 9: Search (structured API first, Grok enhancement) ─

def search(query: str, x_only: bool = True):
    """Search Bluesky — structured API first, Grok for AI analysis."""
    client = _get_client()

    print(f"\n{'=' * 60}")
    print(f"  SOCIALCLAW SEARCH — \"{query}\"")
    print(f"{'=' * 60}")

    # 1. Search latest tweets
    print("\n  Searching Bluesky...")
    search_result = _smart_search(client, query, "Latest")

    if search_result["source"] == "api":
        tweets = search_result["data"].get("tweets", [])
        print(f"\n  RESULTS ({len(tweets)} posts found)")
        for tw in tweets[:15]:
            _print_tweet(tw, max_text=120)
            print()

        # Show engagement summary
        if tweets:
            total_likes = sum(tw.get("likeCount", 0) for tw in tweets)
            total_rts = sum(tw.get("retweetCount", 0) for tw in tweets)
            print(f"  ENGAGEMENT SUMMARY")
            print(f"    Total tweets: {len(tweets)}")
            print(f"    Total likes: {total_likes:,}")
            print(f"    Total RTs: {total_rts:,}")
            print(f"    Avg likes/tweet: {total_likes / len(tweets):.1f}")

        # 2. Also get top tweets
        print(f"\n  Searching top posts...")
        top_result = _smart_search(client, query, "Top")
        _print_grok_result(top_result, "TOP PERFORMING POSTS")
    else:
        print(f"\n  RESULTS")
        print(f"  {'-' * 56}")
        print(search_result["data"])

    _print_cost(client)
    client.close()


# ── Workflow 10: Tweet Lookup ─────────────────────────────────

def tweet(tweet_id: str):
    """Look up a specific tweet by ID."""
    client = _get_client()

    print(f"\n{'=' * 60}")
    print(f"  SOCIALCLAW TWEET — {tweet_id}")
    print(f"{'=' * 60}")

    # Extract post ID from URL if needed
    if "x.com/" in tweet_id or "twitter.com/" in tweet_id:
        tweet_id = tweet_id.rstrip("/").split("/")[-1]
    elif "bsky.app/" in tweet_id:
        # Handle Bluesky URL format: https://bsky.app/profile/{handle}/post/{rkey}
        parts = tweet_id.rstrip("/").split("/")
        if "post" in parts:
            idx = parts.index("post")
            if idx + 1 < len(parts):
                tweet_id = parts[idx + 1]

    print("\n  Fetching tweet...")
    result = _api(client, "/v1/x/tweets/lookup", {"tweetIds": [tweet_id]})
    tweets = result.get("tweets", [])

    if tweets:
        tw = tweets[0]
        author = tw.get("author", {})
        handle = author.get("userName", "?")
        name = author.get("name", "?")
        text = tw.get("text", "")
        likes = tw.get("likeCount", 0)
        rts = tw.get("retweetCount", 0)
        replies = tw.get("replyCount", 0)
        views = tw.get("viewCount", 0)
        link = _tweet_link(tw)

        print(f"\n  TWEET")
        print(f"  {'Author:':<12} {name} (@{handle})")
        print(f"  {'Text:':<12} {text}")
        print(f"  {'Likes:':<12} {likes:,}")
        print(f"  {'Retweets:':<12} {rts:,}")
        print(f"  {'Replies:':<12} {replies:,}")
        if views:
            print(f"  {'Views:':<12} {views:,}")
        if link:
            print(f"  {'URL:':<12} {link}")

        # Get replies
        print("\n  Fetching replies...")
        replies_data = _api(client, "/v1/x/tweets/replies", {"tweetId": tweet_id})
        reply_tweets = replies_data.get("tweets", [])

        if reply_tweets:
            print(f"\n  REPLIES ({len(reply_tweets)} found)")
            for rtw in reply_tweets[:10]:
                _print_tweet(rtw, max_text=140)
                print()
    else:
        print("\n  Tweet not found or unavailable.")

    _print_cost(client)
    client.close()


# ── Workflow 11: Thread ───────────────────────────────────────

def thread(tweet_id: str):
    """Get a full thread starting from a tweet."""
    client = _get_client()

    print(f"\n{'=' * 60}")
    print(f"  SOCIALCLAW THREAD — {tweet_id}")
    print(f"{'=' * 60}")

    # Extract post ID from URL if needed
    if "x.com/" in tweet_id or "twitter.com/" in tweet_id:
        tweet_id = tweet_id.rstrip("/").split("/")[-1]
    elif "bsky.app/" in tweet_id:
        # Handle Bluesky URL format: https://bsky.app/profile/{handle}/post/{rkey}
        parts = tweet_id.rstrip("/").split("/")
        if "post" in parts:
            idx = parts.index("post")
            if idx + 1 < len(parts):
                tweet_id = parts[idx + 1]

    print("\n  Fetching thread...")
    result = _api(client, "/v1/x/tweets/thread", {"tweetId": tweet_id})
    tweets = result.get("tweets", [])

    if tweets:
        print(f"\n  THREAD ({len(tweets)} tweets)")
        for i, tw in enumerate(tweets, 1):
            author = tw.get("author", {})
            handle = author.get("userName", "?")
            text = tw.get("text", "")
            likes = tw.get("likeCount", 0)
            link = _tweet_link(tw)
            print(f"\n  [{i}] @{handle} ({likes:,} likes)")
            print(f"      {text}")
            if link:
                print(f"      {link}")
    else:
        print("\n  Thread not found or unavailable.")

    _print_cost(client)
    client.close()


# ── Workflow 12: Author Analytics ─────────────────────────────

def analytics(handle: str):
    """Deep author intelligence report."""
    handle = handle.lstrip("@")
    client = _get_client()

    print(f"\n{'=' * 60}")
    print(f"  SOCIALCLAW ANALYTICS — @{handle}")
    print(f"{'=' * 60}")

    # 1. Author analytics (dedicated endpoint)
    print("\n  Fetching author analytics...")
    result = _api(client, "/v1/x/authors/analytics", {"handle": handle})

    if result:
        data = result.get("data", result)
        print(f"\n  AUTHOR ANALYTICS")
        for key, value in data.items():
            if isinstance(value, (int, float)):
                print(f"  {key:<30} {value:>15,}" if isinstance(value, int) else f"  {key:<30} {value:>15.2f}")
            elif isinstance(value, str):
                print(f"  {key:<30} {value}")
            elif isinstance(value, list):
                print(f"  {key:<30} ({len(value)} items)")
                for item in value[:5]:
                    print(f"    - {str(item)[:80]}")
            elif isinstance(value, dict):
                print(f"  {key}:")
                for k, v in value.items():
                    print(f"    {k:<28} {v}")

    # 2. Also get profile for context
    print("\n  Fetching profile...")
    info = _api(client, "/v1/x/users/info", {"username": handle})
    d = _unwrap_data(info)

    followers = _follower_count(d)
    following = d.get("following") or d.get("followingCount") or 0
    bio = _bio_text(d)

    print(f"\n  PROFILE CONTEXT")
    print(f"  {'Followers:':<14} {followers:,}")
    print(f"  {'Following:':<14} {following:,}")
    print(f"  {'Bio:':<14} {bio[:120]}")

    _print_cost(client)
    client.close()


# ── Workflow 13: Brief ────────────────────────────────────────

def brief(username: str):
    """Morning brief — mentions, trends, top followers, action items."""
    username = username.lstrip("@")
    client = _get_client()

    print(f"\n{'=' * 60}")
    print(f"  SOCIALCLAW BRIEF — @{username}")
    print(f"{'=' * 60}")

    # 1. Profile
    print("\n  Fetching profile...")
    info = _api(client, "/v1/x/users/info", {"username": username})
    d = _unwrap_data(info)

    followers = _follower_count(d)
    bio = _bio_text(d)
    print(f"\n  PROFILE")
    print(f"  Followers: {followers:,}")
    if bio:
        print(f"  Bio: {bio[:100]}")

    # 2. Mentions
    print("\n  Fetching mentions...")
    mentions = _api(client, "/v1/x/users/mentions", {"username": username})
    mention_tweets = mentions.get("tweets", [])

    print(f"\n  OVERNIGHT MENTIONS ({len(mention_tweets)} new)")
    for tw in mention_tweets[:8]:
        _print_tweet(tw, max_text=120)
        print()

    # 3. Trending
    print("  Fetching trends...")
    trending = _api(client, "/v1/x/trending", {})
    topics = trending.get("data", {}).get("topics", [])

    print(f"\n  TRENDING NOW")
    for t in topics[:5]:
        name = t.get("name", "?")
        views = t.get("totalViews", 0)
        print(f"    {name:<24} {views:>15,} views")

    # 4. Top followers
    print("\n  Fetching followers...")
    fdata = _api(client, "/v1/x/users/followers", {"username": username})
    flist = fdata.get("followers", [])
    top = sorted(flist, key=lambda x: x.get("followers_count", 0), reverse=True)[:5]

    print(f"\n  TOP FOLLOWERS")
    for f in top:
        print(f"    @{f.get('userName', '?'):<22} {f.get('followers_count', 0):>10,} followers")

    # 5. Suggested actions
    print(f"\n  SUGGESTED ACTIONS")
    if mention_tweets:
        top_mention = max(
            mention_tweets[:15],
            key=lambda t: (t.get("author", {}).get("followers", 0)
                           or t.get("author", {}).get("followersCount", 0) or 0),
        )
        a = top_mention.get("author", {})
        h = a.get("userName", "?")
        fc = a.get("followers", a.get("followersCount", 0))
        if fc:
            print(f"    1. Reply to @{h} ({fc:,} followers) — high-value mention")
        else:
            print(f"    1. Reply to @{h} — recent mention")
    if topics:
        print(f"    2. Post about \"{topics[0]['name']}\" — {topics[0].get('totalViews', 0):,} views and trending")
    print(f"    3. Engage in top 5 threads in your niche (use hitlist)")

    _print_cost(client)
    client.close()


# ── Helpers ────────────────────────────────────────────────────

def _print_cost(client: BlueskyClient):
    print(f"\n{'=' * 60}")
    print(f"  Bluesky API calls made: {client.calls}")
    print(f"{'=' * 60}")


# ── CLI ─────────────────────────────────────────────────────────

def _print_help():
    print("SocialSwag v4 — Bluesky Marketing Intelligence")
    print()
    print("  Powered by the AT Protocol (Bluesky).")
    print("  Set BLUESKY_HANDLE and BLUESKY_APP_PASSWORD to authenticate.")
    print("  Optionally set OPENAI_API_KEY to enable AI-generated reply drafts.")
    print()
    print("COMMANDS:")
    print()
    print("  Account Intelligence:")
    print("    insight @handle            Deep-dive: profile, followers, posts")
    print("    audience @handle           Segment followers by influence tier")
    print("    analytics @handle          Author intelligence report (posting patterns, reach)")
    print("    brief @handle              Morning brief: posts, trends, actions")
    print("    check @handle              Verify posted content & check engagement")
    print()
    print("  Discovery & Search:")
    print("    search <query>             Search Bluesky posts")
    print("    radar <topic>             Trending topics + content opportunities")
    print("    scout <topic>              Find top voices and KOLs on a topic")
    print("    hitlist <topic>            Find high-value conversations to join")
    print("    post <id_or_url>           Look up a specific post + replies")
    print("    thread <id_or_url>         Get a full post thread")
    print()
    print("  Competitive & Engagement:")
    print("    compare @user1 @user2      Side-by-side competitor analysis")
    print("    engage @username           Find mentions & generate reply drafts")
    print()
    print("EXAMPLES:")
    print("  socialswag insight @elonmusk")
    print("  socialswag audience @jack")
    print("  socialswag search 'AI agents'")
    print("  socialswag radar 'AI infrastructure'")
    print("  socialswag scout 'machine learning'")
    print("  socialswag hitlist 'open source AI'")
    print("  socialswag post https://bsky.app/profile/handle.bsky.team/post/abc123")
    print("  socialswag thread https://bsky.app/profile/handle.bsky.team/post/abc123")
    print("  socialswag analytics @handle.bsky.team")
    print("  socialswag compare @a.bsky.team @b.bsky.team")
    print()
    print("AUTH: Set BLUESKY_HANDLE and BLUESKY_APP_PASSWORD environment variables")
    print("      Get app password from Bluesky settings (not your login password)")
    print("      Public data accessible without authentication")
    print("DATA: All responses saved to ~/.socialswag/data/")


def main():
    if len(sys.argv) < 2:
        _print_help()
        return

    cmd = sys.argv[1].lower()
    known_commands = {
        "insight",
        "radar",
        "compare",
        "audience",
        "scout",
        "hitlist",
        "engage",
        "check",
        "search",
        "tweet",
        "thread",
        "analytics",
        "brief",
        "help",
        "--help",
        "-h",
    }

    if cmd not in known_commands:
        print(f"Unknown: {cmd}")
        print("Commands: insight, radar, compare, audience, scout, hitlist, engage, check, search, tweet, thread, analytics, brief")
        print("Run without arguments for full help.")
        return

    if cmd in {"help", "--help", "-h"}:
        _print_help()
        return

    _ensure_deps()

    if cmd == "insight" and len(sys.argv) >= 3:
        insight(sys.argv[2])
    elif cmd == "radar" and len(sys.argv) >= 3:
        radar(" ".join(sys.argv[2:]))
    elif cmd == "compare" and len(sys.argv) >= 4:
        compare(sys.argv[2], sys.argv[3])
    elif cmd == "audience" and len(sys.argv) >= 3:
        audience(sys.argv[2])
    elif cmd == "scout" and len(sys.argv) >= 3:
        scout(" ".join(sys.argv[2:]))
    elif cmd == "hitlist" and len(sys.argv) >= 3:
        hitlist(" ".join(sys.argv[2:]))
    elif cmd == "engage" and len(sys.argv) >= 3:
        engage(sys.argv[2], " ".join(sys.argv[3:]) if len(sys.argv) > 3 else None)
    elif cmd == "check" and len(sys.argv) >= 3:
        check(sys.argv[2])
    elif cmd == "search" and len(sys.argv) >= 3:
        search(" ".join(sys.argv[2:]))
    elif cmd == "tweet" and len(sys.argv) >= 3:
        tweet(sys.argv[2])
    elif cmd == "thread" and len(sys.argv) >= 3:
        thread(sys.argv[2])
    elif cmd == "analytics" and len(sys.argv) >= 3:
        analytics(sys.argv[2])
    elif cmd == "brief" and len(sys.argv) >= 3:
        brief(sys.argv[2])
    else:
        print(f"Usage error for command: {cmd}")
        print("Commands: insight, radar, compare, audience, scout, hitlist, engage, check, search, tweet, thread, analytics, brief")
        print("Run without arguments for full help.")


if __name__ == "__main__":
    main()
