---
name: socialclaw
user-invocable: true
description: X/Twitter marketing intelligence — account insights, topic trends, competitor analysis, audience mapping, content strategy, and KOL discovery. Powered by BlockRun's unified API gateway with USDC micropayments.
allowed-tools: Read, Bash(python:*), Bash(python3:*), Bash(pip:*)
---

# SocialClaw — X/Twitter Marketing Intelligence

SocialClaw turns X/Twitter data into actionable marketing insights. All data comes through BlockRun's unified API gateway — one SDK, one wallet.

## Setup (run once)

```python
# Auto-installs SDK and finds any available wallet
import subprocess, sys
subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "blockrun-llm[solana]>=0.8.0"], stdout=subprocess.DEVNULL)

from pathlib import Path
chain_file = Path.home() / ".blockrun" / ".chain"
chain = chain_file.read_text().strip() if chain_file.exists() else "base"

if chain == "solana":
    from blockrun_llm import setup_agent_solana_wallet
    client = setup_agent_solana_wallet(silent=True)
else:
    from blockrun_llm import setup_agent_wallet
    client = setup_agent_wallet(silent=True)

print(f"Wallet: {client.get_wallet_address()}")
print(f"Balance: ${client.get_balance():.2f} USDC")
```

The SDK auto-scans `~/.<any-folder>/wallet.json` and `solana-wallet.json` — works with any compatible wallet provider.

## Workflows

### 1. Insight — Account Deep-Dive (`insight @username`)

Who is this account? What's their influence? Who talks about them?

```python
username = "jessepollak"  # CHANGE THIS

# Profile
info = client.x_user_info(username)
d = info.data
print(f"@{d.get('userName')}: {d.get('followers'):,} followers, verified={d.get('isBlueVerified')}")
print(f"Bio: {d.get('description','')[:120]}")
print(f"F/F ratio: {d.get('followers',0) / max(d.get('following',1), 1):.1f}x")

# Who mentions them (engagement quality)
mentions = client.x_user_mentions(username)
for tw in mentions.tweets[:5]:
    print(f"  @{tw.author.get('userName','?')}: {tw.text[:100]}")

# Top followers by influence
followers = client.x_followers(username)
top = sorted(followers.followers, key=lambda x: x.get('followers_count', 0), reverse=True)[:10]
for f in top:
    print(f"  @{f.get('userName','?'):20s} {f.get('followers_count',0):>10,} followers")

print(f"Cost: ${client.get_spending()['total_usd']:.4f}")
```

**Cost: ~$0.08** | Present as: audience size, engagement quality, content themes, growth signals.

---

### 2. Radar — Topic Intelligence (`radar <topic>`)

What's hot? What content is working? Where should I jump in?

```python
topic = "AI agents"  # CHANGE THIS

# Trending topics with view counts
trending = client.x_trending()
for t in trending.data.get("topics", [])[:10]:
    print(f"  {t['name']:<28} {t.get('articleCount',0):>4} articles  {t.get('totalViews',0):>12,} views")

# Latest conversation
search = client.x_search(topic)
for tw in search.tweets[:10]:
    print(f"  @{tw.author.get('userName','?')}: {tw.text[:100]}")

# Viral content detection
rising = client.x_articles_rising()
for a in rising.data.get("articles", [])[:5]:
    print(f"  {a.get('title','?')[:70]} — {a.get('url','')}")

print(f"Cost: ${client.get_spending()['total_usd']:.4f}")
```

**Cost: ~$0.07** | Present as: trending angles, top content formats, suggested post ideas.

---

### 3. Compare — Competitor Analysis (`compare @user1 @user2`)

Side-by-side: who's winning and why?

```python
user1, user2 = "jessepollak", "VitalikButerin"  # CHANGE THESE

# Profiles
i1 = client.x_user_info(user1).data
i2 = client.x_user_info(user2).data
print(f"{'':20s} @{user1:>15s} @{user2:>15s}")
print(f"{'Followers':20s} {i1.get('followers',0):>15,} {i2.get('followers',0):>15,}")

# Mention engagement
m1 = client.x_user_mentions(user1).tweets
m2 = client.x_user_mentions(user2).tweets
likes1 = sum(tw.likeCount or 0 for tw in m1)
likes2 = sum(tw.likeCount or 0 for tw in m2)
print(f"{'Mention likes':20s} {likes1:>15,} {likes2:>15,}")

# Top followers
f1 = sorted(client.x_followers(user1).followers, key=lambda x: x.get('followers_count',0), reverse=True)[:3]
f2 = sorted(client.x_followers(user2).followers, key=lambda x: x.get('followers_count',0), reverse=True)[:3]

print(f"Cost: ${client.get_spending()['total_usd']:.4f}")
```

**Cost: ~$0.15** | Present as: who has momentum, content strategy differences, audience quality.

---

### 4. Audience — Follower Segmentation (`audience @username`)

Who follows them? Cluster by influence tier and interests.

```python
username = "jessepollak"  # CHANGE THIS

# Get followers (200 per page)
followers = client.x_followers(username)
all_followers = followers.followers

# Batch lookup top 50 for detailed profiles
top_handles = [f.get("userName") for f in sorted(all_followers, key=lambda x: x.get("followers_count",0), reverse=True)[:50] if f.get("userName")]
details = client.x_user_lookup(top_handles)

# Segment by tier
mega = [u for u in details.users if u.followers >= 100000]
macro = [u for u in details.users if 10000 <= u.followers < 100000]
micro = [u for u in details.users if 1000 <= u.followers < 10000]

print(f"Mega (100K+): {len(mega)}")
for u in mega: print(f"  @{u.userName}: {u.followers:,} — {u.description[:80]}")
print(f"Macro (10K-100K): {len(macro)}")
print(f"Micro (1K-10K): {len(micro)}")

print(f"Cost: ${client.get_spending()['total_usd']:.4f}")
```

**Cost: ~$0.15** | Present as: audience tiers, common interests/bios, potential partners.

---

### 5. Scout — KOL Discovery (`scout <topic>`)

Find the key voices in any topic.

```python
topic = "AI agents crypto"  # CHANGE THIS

# Find who's talking about it
search = client.x_search(topic)

# Extract unique authors
authors = {}
for tw in search.tweets:
    a = tw.author or {}
    handle = a.get("userName", "")
    if handle and handle not in authors:
        fc = a.get("followers", a.get("followersCount", 0))
        authors[handle] = {"followers": fc, "text": tw.text[:100], "likes": tw.likeCount or 0}

# Rank by influence
ranked = sorted(authors.items(), key=lambda x: x[1]["followers"], reverse=True)

print(f"Top voices on '{topic}':")
# Batch lookup for full profiles
top_handles = [h for h, _ in ranked[:20]]
if top_handles:
    details = client.x_user_lookup(top_handles)
    for u in details.users:
        print(f"  @{u.userName:20s} {u.followers:>10,} followers — {str(u.description)[:60]}")

print(f"Cost: ${client.get_spending()['total_usd']:.4f}")
```

**Cost: ~$0.07** | Present as: ranked influencer list with follower counts and bios.

---

### 6. Hitlist — Engagement Targets (`hitlist <topic>`)

High-value conversations to engage with RIGHT NOW.

```python
topic = "base blockchain"  # CHANGE THIS

# Find high-engagement recent tweets
search = client.x_search(topic)

# Sort by engagement (likes + RTs)
tweets = [(tw, (tw.likeCount or 0) + (tw.retweetCount or 0)) for tw in search.tweets]
tweets.sort(key=lambda x: x[1], reverse=True)

print(f"Engagement targets for '{topic}':")
for tw, eng in tweets[:10]:
    a = tw.author or {}
    handle = a.get("userName", "?")
    fc = a.get("followers", a.get("followersCount", 0))
    print(f"  @{handle} ({fc:,} followers) — {eng} engagement")
    print(f"    {tw.text[:120]}")
    print(f"    Suggest: reply with insight about...")
    print()

print(f"Cost: ${client.get_spending()['total_usd']:.4f}")
```

**Cost: ~$0.03** | Present as: ranked conversations to join, with suggested reply angles.

---

### 7. Brief — Daily Marketing Report (`brief @myaccount`)

What happened overnight? What should I post today?

```python
username = "blockrunai"  # CHANGE THIS — user's own handle

# 1. My mentions (who's talking about me?)
mentions = client.x_user_mentions(username)
print(f"Mentions: {len(mentions.tweets)} new")
for tw in mentions.tweets[:5]:
    print(f"  @{tw.author.get('userName','?')}: {tw.text[:80]}")

# 2. Trending (what's hot in my space?)
trending = client.x_trending()
for t in trending.data.get("topics", [])[:5]:
    print(f"  {t['name']}: {t.get('totalViews',0):,} views")

# 3. Rising content (what's going viral?)
rising = client.x_articles_rising()
articles = rising.data.get("articles", [])[:3]
for a in articles:
    print(f"  {a.get('title','?')[:60]}")

# 4. Actionable summary
print("\nSUGGESTED ACTIONS:")
print("  1. Reply to top mentions to boost engagement")
print("  2. Create content around trending topic #1")
print("  3. Share perspective on rising article #1")

print(f"Cost: ${client.get_spending()['total_usd']:.4f}")
```

**Cost: ~$0.08** | Present as: morning brief with 3 concrete actions for today.

---

## Data Auto-Save

All paid API responses are saved to `~/.blockrun/data/` as JSON. You paid for it, you keep it.

## API Reference

| Method | What | Cost |
|--------|------|------|
| `x_user_info(username)` | Profile stats | $0.002 |
| `x_user_lookup([users])` | Batch profiles (up to 100) | $0.002/user |
| `x_followers(username)` | Follower list (~200/page) | $0.05/page |
| `x_followings(username)` | Following list (~200/page) | $0.05/page |
| `x_user_tweets(username)` | User's tweets | $0.032/page |
| `x_user_mentions(username)` | Mentions of user | $0.032/page |
| `x_search(query)` | Search tweets | $0.032/page |
| `x_trending()` | Trending topics | $0.002 |
| `x_articles_rising()` | Viral content | $0.05 |
| `x_tweet_lookup([ids])` | Batch tweet data | $0.16/batch |
| `x_tweet_replies(id)` | Replies | $0.032/page |
| `x_tweet_thread(id)` | Thread | $0.032/page |
| `x_author_analytics(handle)` | Author intelligence | $0.02 |
| `x_compare_authors(h1, h2)` | Compare two accounts | $0.05 |
| `chat(model, prompt)` | LLM (GPT, Grok, DeepSeek) | varies |
| `generate(prompt)` | Image generation | $0.01-0.04 |

## Triggers

Activate when user mentions: `socialclaw`, `twitter`, `x.com`, `trending`, `followers`, `mentions`, `competitor`, `audience`, `growth`, `engagement`, `KOL`, `influencer`, `marketing intel`, `who follows`, `what's trending`, `analyze @`, `compare @`
