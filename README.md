# SocialSwag

<div align="center">

<img src="assets/banner.png" alt="SocialSwag" width="600" />

<h3>X/Twitter intelligence + AI-powered content agent.</h3>

<p>Research → Analyze → Write → Optimize → Visualize. Full loop.<br>
One command → structured data → your agent acts on it.</p>

<br />

[![Claude Code](https://img.shields.io/badge/Claude_Code-Skill-orange.svg)](https://github.com/anthropics/skills)
[![OpenAI Codex](https://img.shields.io/badge/OpenAI_Codex-Compatible-412991.svg)](https://openai.com/codex)
[![Gemini CLI](https://img.shields.io/badge/Gemini_CLI-Compatible-4285F4.svg)](https://github.com/google-gemini/gemini-cli)
[![Cursor](https://img.shields.io/badge/Cursor-Compatible-000000.svg)](https://cursor.com)

[What Can I Do?](#what-can-i-do) · [Get Started](#get-started) · [Pricing](docs/pricing.md) · [API Reference](docs/api-reference.md) · [Configuration](#configuration)

</div>

---

## What Is SocialSwag?

SocialSwag is an AI-powered X/Twitter intelligence platform that combines:

- **Official X API v2** — structured, real-time data
- **OpenRouter AI** — x-ai/grok-4.20-beta as default, with 100+ models available
- **Nano Banana 2** — image generation for posts

Perfect for autonomous agents that need to research, analyze, and create content on X/Twitter.

---

## What Can I Do?

### Find out what to post right now

```bash
socialswag radar "AI agents"
```

```
TRENDING NOW
  Anthropic          158 articles   115,983,616 views  <--
  Claude Code         29 articles    44,825,583 views
  Bitcoin             34 articles    27,136,645 views

LATEST TWEETS (42 found)
  @buildonsol     892 likes  "AI agents are about to change how we..."
    https://x.com/buildonsol/status/1234567890

SUGGESTED: Post your take on "Anthropic" — 115M views and climbing.
```

Your agent sees real view counts, finds the wave, and tells you exactly what to post about. No more scrolling Twitter for 45 minutes hoping for inspiration.

---

### Know who to engage with

```bash
socialswag hitlist "Solana DeFi"
```

```
@solana_daily (45K followers) — 89 likes, climbing
  "Solana Projects to Watch this Week"
  https://x.com/solana_daily/status/123456789
  → Reply with specific data. Numbers get retweeted.

@DefiIgnas (240K followers) — 312 likes
  "Unpopular opinion: most AI agent tokens are..."
  https://x.com/DefiIgnas/status/987654321
  → Counter with your build story. Builders > speculators.
```

15 minutes replying to these 5 conversations > 1 hour writing a standalone tweet nobody sees. Your agent finds the high-leverage conversations for you.

---

### Understand any account in 10 seconds

```bash
socialswag insight @jessepollak
```

```
PROFILE
  Followers:     347,004
  F/F Ratio:     72.3x (creator, not consumer)
  Verified:      Yes

TOP FOLLOWERS
  @coinbase           4,200,000 followers
  @brian_armstrong     1,800,000 followers

MENTION ENGAGEMENT
  Avg likes/mention:    23.4
  Total reach:          4,892
```

Before you DM someone, pitch them, or reply to their thread — know their actual influence, who follows them, and whether engaging with them is worth your time.

---

### Find the right people in any niche

```bash
socialswag scout "x402"
```

```
TOP VOICES
  @jessepollak        347,004 followers — @base builder #001
  @BuildOnBase         89,200 followers — Official Base account
  @coinaborsh          45,190 followers — ecosystem builder
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
Mention likes          1,892              3,410
Avg likes/mention       12.3               28.4

QUICK TAKE: @competitor gets 2.3x more mention engagement despite fewer followers.
Their audience is more active. Study their reply strategy.
```

Stop wondering if you're winning. Know exactly where you stand and what to fix.

---

### Get your morning brief

```bash
socialswag brief @yourhandle
```

```
3 new mentions overnight
  @HarryKamaAI (196K followers) mentioned you — reply within 30 minutes
  @defi_whale (45K) quote-tweeted your thread

TRENDING: "AI infrastructure" is spiking (28M views)

SUGGESTED ACTIONS:
  1. Reply to @HarryKamaAI (high-value mention, big audience)
  2. Post about AI infrastructure — ride the trend
  3. Thank @defi_whale for the QT — builds relationship
```

Wake up knowing exactly what happened and what to do first. Your agent monitors while you sleep.

---

### Look up any tweet or thread

```bash
socialswag tweet https://x.com/elonmusk/status/1234567890
socialswag thread https://x.com/VitalikButerin/status/9876543210
```

Get full tweet data, engagement metrics, replies, and complete threads — all structured, all actionable.

---

### Deep analytics on any creator

```bash
socialswag analytics @VitalikButerin
```

Posting patterns, audience composition, engagement trajectory, content performance by topic. Everything you need to understand what makes an account grow.

---

### AI-Powered Reply Drafts

```bash
socialswag engage @yourhandle
```

SocialSwag uses OpenRouter (default: x-ai/grok-4.20-beta) to generate contextually relevant reply drafts. The AI analyzes recent mentions and suggests responses.

---

## Get Started

**Clone and install:**

```bash
git clone https://github.com/BlockRunAI/socialswag && cd socialswag
bash install.sh                          # install SocialSwag (safe mode)
MODE=takeover bash install.sh            # also replace sibling skills
MODE=force bash install.sh               # overwrite every sibling skill
bash install.sh --dry-run                # preview changes
bash install.sh --uninstall              # restore backups + remove launcher
```

This installs the skill, creates a `socialswag` launcher in `~/.local/bin`, and installs dependencies.

---

## Configuration

### Required: X API Bearer Token

Get your Bearer Token from [developer.x.com](https://developer.x.com/) and set it:

```bash
export X_API_BEARER_TOKEN="your_bearer_token_here"
# Or save permanently:
mkdir -p ~/.socialswag && echo "your_token" > ~/.socialswag/api_key
```

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

| Command | What you get | API Calls |
|---------|-------------|-----------|
| `insight @handle` | Full account analysis: profile, followers, mentions, tweets | ~4 |
| `radar <topic>` | Trending topics + latest tweets + rising articles | ~2 |
| `search <query>` | Search X with structured results + top tweets | ~2 |
| `compare @a @b` | Side-by-side account comparison | ~6 |
| `scout <topic>` | Find top voices in any niche | ~1 |
| `hitlist <topic>` | High-engagement conversations to reply to | ~1 |
| `audience @handle` | Follower segmentation by influence tier | ~2 |
| `brief @handle` | Morning brief: mentions, trends, action items | ~3 |
| `analytics @handle` | Deep author intelligence report | ~2 |
| `tweet <id/url>` | Look up specific tweet + replies | ~2 |
| `thread <id/url>` | Get full tweet thread | ~1 |
| `engage @handle` | Find mentions + AI-generated reply drafts | ~3 |
| `check @handle` | Verify posted tweets + engagement metrics | ~3 |

### Content Creation (Write & Optimize)

| Command | What you get | Cost |
|---------|-------------|------|
| `draft "topic"` | Algorithm-optimized post with 3 variations + strategy explanation | Free |
| `review` | Score your draft (1-10) with checklist audit + optimized rewrite | Free |
| `image "description"` | X-optimized image via Nano Banana 2 (high contrast, bold colors, clean composition) | ~$0.04/call |

**Full loop:** Research (`radar`/`scout`) → Write (`draft`) → Optimize (`review`) → Visualize (`image`) → Monitor (`brief`/`analytics`)

---

## Cost Estimation

X API uses **consumption-based billing** — pay only for what you use. See [developer.x.com](https://developer.x.com/) for full details.

### X API Pricing (Pay-per-use)

| Resource | Cost per unit |
|----------|---------------|
| **Posts: Read** (tweets, search) | $0.005/resource |
| **User: Read** (profiles, followers, mentions) | $0.010/resource |

### X API Cost Per Workflow

| Workflow | X API Calls | Cost |
|----------|-------------|------|
| `radar <topic>` | 2 (search) | $0.01 |
| `search <query>` | 2 (search) | $0.01 |
| `scout <topic>` | 1 (search) | $0.005 |
| `hitlist <topic>` | 1 (search) | $0.005 |
| `thread <id/url>` | 1 (search) | $0.005 |
| `tweet <id/url>` | 2 (tweet + search) | $0.01 |
| `analytics @handle` | 2 (user + tweets) | $0.02 |
| `brief @handle` | 3 (user + mentions + followers) | $0.04 |
| `engage @handle` | 3 (user + mentions + search) | $0.04 |
| `check @handle` | 3 (user + tweets + mentions) | $0.04 |
| `audience @handle` | 2 (user + followers) | $0.02 |
| `insight @handle` | 4 (user + mentions + followers + tweets) | $0.05 |
| `compare @a @b` | 6 (2× user + 2× mentions + 2× followers) | $0.08 |
| `draft "topic"` | 1 (search) | $0.005 |
| `review` | 0 | Free |

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

| Workflow | Count | X API Cost |
|----------|-------|------------|
| `radar` | 200 | $2.00 |
| `insight` | 100 | $5.00 |
| `engage` | 100 | $4.00 |
| `search` | 100 | $1.00 |

- X API: ~$12/month
- OpenRouter (100 `engage` calls): ~$0.30/month
- **Total: ~$13-15/month** (plus image generation if used)

---

## How It Works

- **X API v2** — Direct access to Twitter's data through their public API (`api.x.com/2`)
- **OpenRouter AI** — Default model is x-ai/grok-4.20-beta. Change via `OPENROUTER_MODEL` env var
- **OpenAI fallback** — Uses gpt-4o-mini if no OpenRouter key provided
- **Image generation** — Nano Banana 2 (Gemini 3.1 Flash Image) via `GOOGLE_API_KEY`
- **Data is yours** — Every response saved to `~/.socialswag/data/`

[Full API Reference](docs/api-reference.md)

---

## Works With Every AI Agent

| Platform | How |
|----------|-----|
| **Claude Code** | Installs as a skill. Say "analyze @elonmusk on Twitter". |
| **OpenAI Codex** | Install `requests>=2.28.0`, set `X_API_BEARER_TOKEN`. |
| **Gemini CLI** | Auto-installs to `~/.gemini/antigravity/skills/socialswag`. |
| **Cursor / Windsurf** | Agent reads CLAUDE.md, calls CLI via terminal. |
| **Any terminal** | `socialswag radar "topic"` |
| **Your own agent** | Use `requests` to call X API v2 with your Bearer Token. |

---

## Why API Access beats $49/month

|  | Dashboard tools | SocialSwag |
|---|---|---|
| **You pay** | $49-99/month whether you use it or not | X API subscription + one command |
| **You get** | Charts you read with your eyes | JSON your agent processes instantly |
| **You do** | Log in, click around, screenshot results | One function call, structured output |
| **Your agent can use it** | No (human-only UI) | Yes (that's the whole point) |

Every API response is saved as JSON in `~/.socialswag/data/`. You keep every result.

---

## From the BlockRun Ecosystem

<table>
<tr>
<td width="50%">

### SocialSwag
**X/Twitter intelligence for your agent**

You're here. One function call = one intelligence report.

`bash install.sh`

</td>
<td width="50%">

### [ClawRouter](https://github.com/BlockRunAI/ClawRouter)
**LLM router for autonomous agents**

41+ models, smart routing, automatic model selection. Your agent picks the best model at the best price automatically.

`curl -fsSL https://blockrun.ai/ClawRouter-update | bash`

[![GitHub stars](https://img.shields.io/github/stars/BlockRunAI/ClawRouter?style=flat-square)](https://github.com/BlockRunAI/ClawRouter)

</td>
</tr>
</table>

> **Together:** SocialSwag pulls the intelligence. ClawRouter routes your LLM calls. Your agent's full stack.

---

<div align="center">

**[developer.x.com](https://developer.x.com/)** · **[openrouter.ai](https://openrouter.ai/)** · **[hello@blockrun.ai](mailto:hello@blockrun.ai)**

MIT

</div>