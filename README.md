# SocialSwag

<div align="center">

<h3>Bluesky intelligence + AI-powered content agent.</h3>

<p>Research → Analyze → Write → Optimize → Visualize. Full loop.<br>
One command → structured data → your agent acts on it.</p>

<br />

[![Claude Code](https://img.shields.io/badge/Claude_Code-Skill-orange.svg)](https://github.com/anthropics/skills)
[![OpenAI Codex](https://img.shields.io/badge/OpenAI_Codex-Compatible-412991.svg)](https://openai.com/codex)
[![Gemini CLI](https://img.shields.io/badge/Gemini_CLI-Compatible-4285F4.svg)](https://github.com/google-gemini/gemini-cli)
[![Cursor](https://img.shields.io/badge/Cursor-Compatible-000000.svg)](https://cursor.com)

[What Can I Do?](#what-can-i-do) · [Get Started](#get-started) · [Configuration](#configuration)

</div>

---

## What Is SocialSwag?

SocialSwag is an AI-powered Bluesky intelligence platform that combines:

- **AT Protocol (Bluesky)** — free, open API for Bluesky data
- **OpenRouter AI** — x-ai/grok-4.20-beta as default, with 100+ models available
- **Nano Banana 2** — image generation for posts

Perfect for autonomous agents that need to research, analyze, and create content on Bluesky.

---

## What Can I Do?

### Find out what to post right now

```bash
socialswag radar "AI agents"
```

```
TRENDING NOW (Bluesky)
  #AI                     1,234 posts
  #machinelearning         892 posts

LATEST POSTS (24 found)
  @aiwhale.bsky.social   0 likes  "📉 Smart Money DUMPED $13,091 of #TAO..."
    https://bsky.app/profile/aiwhale.bsky.social/post/3mh6kdnvinr2q
```

Your agent sees real engagement, finds the wave, and tells you exactly what to post about. No more scrolling Bluesky for 45 minutes hoping for inspiration.

---

### Know who to engage with

```bash
socialswag hitlist "Solana DeFi"
```

```
@solana_daily (45K followers) — 89 likes, climbing
  "Solana Projects to Watch this Week"
  https://bsky.app/profile/solana_daily/post/123456789
  → Reply with specific data. Numbers get boosted.

@DefiIgnas (240K followers) — 312 likes
  "Unpopular opinion: most AI agent tokens are..."
  https://bsky.app/profile/DefiIgnas/post/987654321
  → Counter with your build story. Builders > speculators.
```

15 minutes replying to these 5 conversations > 1 hour writing a standalone post nobody sees. Your agent finds the high-leverage conversations for you.

---

### Understand any account in 10 seconds

```bash
socialswag insight @bsky.app
```

```
PROFILE
  Name:          Bluesky
  Bio:           official Bluesky account
  Followers:     32,390,968
  Following:     0
  Posts:         725
```

Before you DM someone, pitch them, or reply to their thread — know their actual influence and whether engaging with them is worth your time.

---

### Find the right people in any niche

```bash
socialswag scout "AI"
```

```
TOP VOICES
  @bsky.app            32.4M followers — Official Bluesky
  @naomiwhelpley.bsky.social  125K followers — AI researcher
  @emily皿.bsky.social   89K followers — AI developer
```

Building a product? Find the 10 people who actually matter in your space. Your agent identifies them by real engagement, not follower count.

---

### Compare yourself against competitors

```bash
socialswag compare @you @competitor
```

```
METRIC               @you              @competitor
Followers             12,400              8,900
Post engagement        1,892              3,410
Avg likes/post         12.3               28.4

QUICK TAKE: @competitor gets 2.3x more engagement despite fewer followers.
Their audience is more active. Study their reply strategy.
```

Stop wondering if you're winning. Know exactly where you stand and what to fix.

---

### Get your morning brief

```bash
socialswag brief @yourhandle
```

```
3 new posts mentioning you overnight
  @HarryKamaAI (196K followers) — reply within 30 minutes
  @defi_whale (45K) reposted your thread

SUGGESTED ACTIONS:
 1. Reply to @HarryKamaAI (high-value mention, big audience)
 2. Post about AI infrastructure — ride the trend
 3. Thank @defi_whale for the repost — builds relationship
```

Wake up knowing exactly what happened and what to do first. Your agent monitors while you sleep.

---

### Look up any post or thread

```bash
socialswag post https://bsky.app/profile/bsky.app/post/3l6oveex3ii2l
socialswag thread https://bsky.app/profile/bsky.app/post/3l6oveex3ii2l
```

Get full post data, engagement metrics, replies, and complete threads — all structured, all actionable.

---

### Deep analytics on any creator

```bash
socialswag analytics @handle.bsky.social
```

Posting patterns, audience composition, engagement trajectory, content performance by topic. Everything you need to understand what makes an account grow.

---

### AI-Powered Reply Drafts

```bash
socialswag engage @yourhandle
```

SocialSwag uses OpenRouter (default: x-ai/grok-4.20-beta) to generate contextually relevant reply drafts. The AI analyzes recent posts and suggests responses.

---

## Get Started

**Clone and install:**

```bash
git clone https://github.com/phuzzled/socialswag && cd socialswag
pip install -r requirements.txt
```

---

## Configuration

### Optional: Bluesky Credentials

Bluesky's public API is free and works without authentication. For full access (your own posts, likes, etc.):

```bash
export BLUESKY_HANDLE="your-handle.bsky.social"
export BLUESKY_APP_PASSWORD="xxxx xxxx xxxx xxxx"
```

Get an app password from your Bluesky settings (NOT your login password).

---

### Optional: OpenRouter API Key (AI Analysis)

**Default model: x-ai/grok-4.20-beta**

```bash
export OPENROUTER_API_KEY="your_openrouter_key"
# Change model (any from openrouter.ai/models):
export OPENROUTER_MODEL="anthropic/claude-3.5-sonnet"
# or:
export OPENROUTER_MODEL="google/gemini-2.0-flash-exp"
```

Get your OpenRouter key at [openrouter.ai](https://openrouter.ai/).

### Optional: OpenAI API Key (Fallback AI)

```bash
export OPENAI_API_KEY="your_openai_key"
```

Used as fallback if no OpenRouter key is set.

### Optional: Google API Key (Image Generation)

```bash
export GOOGLE_API_KEY="your_google_key"
```

Enables the `image` workflow using Nano Banana 2 (Gemini 3.1 Flash Image). Get your key at [aistudio.google.com](https://aistudio.google.com/).

---

## All Commands

### Intelligence (Research & Analysis)

| Command | What you get |
|---------|---------------|
| `insight @handle` | Full account analysis: profile, followers, posts |
| `radar <topic>` | Trending topics + latest posts |
| `search <query>` | Search Bluesky with structured results |
| `compare @a @b` | Side-by-side account comparison |
| `scout <topic>` | Find top voices in any niche |
| `hitlist <topic>` | High-engagement conversations to reply to |
| `audience @handle` | Follower segmentation by influence tier |
| `brief @handle` | Morning brief: mentions, trends, action items |
| `analytics @handle` | Deep author intelligence report |
| `post <id/url>` | Look up specific post + replies |
| `thread <id/url>` | Get full post thread |
| `engage @handle` | Find posts + AI-generated reply drafts |
| `check @handle` | Verify posted content + engagement metrics |

### Content Creation (Write & Optimize)

| Command | What you get | Cost |
|---------|-------------|------|
| `draft "topic"` | Algorithm-optimized post with 3 variations + strategy explanation | Free |
| `review` | Score your draft (1-10) with checklist audit + optimized rewrite | Free |
| `image "description"` | Bluesky-optimized image via Nano Banana 2 | ~$0.04/call |

**Full loop:** Research (`radar`/`scout`) → Write (`draft`) → Optimize (`review`) → Visualize (`image`) → Monitor (`brief`/`analytics`)

---

## Cost Estimation

**Bluesky API is FREE** — no authentication required for public data.

### OpenRouter AI (Optional)

| Model | Input Cost | Output Cost | Est. per `engage` |
|-------|------------|-------------|-------------------|
| **x-ai/grok-4.20-beta** (default) | ~$2/M tokens | ~$10/M tokens | ~$0.003 |
| anthropic/claude-3.5-sonnet | ~$3/M | ~$15/M | ~$0.005 |
| google/gemini-2.0-flash-exp | ~$0 | ~$0 | Free |

Set `OPENROUTER_API_KEY` at [openrouter.ai](https://openrouter.ai/).

### Image Generation (Optional)

| Provider | Model | Cost per image |
|----------|-------|----------------|
| Google AI | Nano Banana 2 (Gemini 3.1 Flash) | ~$0.04 |

Set `GOOGLE_API_KEY` at [aistudio.google.com](https://aistudio.google.com/).

### Monthly Cost Example

**Heavy usage (500 workflows/month):**

| Workflow | Count | Bluesky API | OpenRouter |
|----------|-------|-------------|------------|
| `radar` | 200 | Free | — |
| `insight` | 100 | Free | — |
| `engage` | 100 | Free | ~$0.30 |
| `search` | 100 | Free | — |

- **Bluesky API: Free**
- OpenRouter (100 `engage` calls): ~$0.30/month
- **Total: ~$0.30/month** (plus image generation if used)

---

## How It Works

- **AT Protocol (Bluesky)** — Free public API (`api.bsky.app`)
- **OpenRouter AI** — Default model is x-ai/grok-4.20-beta. Change via `OPENROUTER_MODEL` env var
- **OpenAI fallback** — Uses gpt-4o-mini if no OpenRouter key provided
- **Image generation** — Nano Banana 2 (Gemini 3.1 Flash Image) via `GOOGLE_API_KEY`
- **Data is yours** — Every response saved to `~/.socialswag/data/`

---

## Works With Every AI Agent

| Platform | How |
|----------|-----|
| **Claude Code** | Installs as a skill. Say "analyze @handle on Bluesky". |
| **OpenAI Codex** | Install `requests>=2.28.0`, set `BLUESKY_HANDLE`. |
| **Gemini CLI** | Auto-installs to `~/.gemini/antigravity/skills/socialswag`. |
| **Cursor / Windsurf** | Agent reads CLAUDE.md, calls CLI via terminal. |
| **Any terminal** | `socialswag radar "topic"` |
| **Your own agent** | Use `requests` to call Bluesky API. |

---

## Why Bluesky?

|  | X/Twitter API | SocialSwag (Bluesky) |
|---|---|---|
| **Cost** | $100+/month | Free |
| **API access** | Limited tiers | Full access |
| **Your agent** | Pay to play | One command |
| **Data** | Pay per request | Unlimited |

Every API response is saved as JSON in `~/.socialswag/data/`. You keep every result.

---

## From the BlockRun Ecosystem

> **Together:** SocialSwag pulls the intelligence. ClawRouter routes your LLM calls. Your agent's full stack.

---

<div align="center">

**[bsky.app](https://bsky.app)** · **[openrouter.ai](https://openrouter.ai/)**

MIT

</div>
