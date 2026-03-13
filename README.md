# BlockRun: Real-Time X/Twitter Data & Image Gen for Your AI Agent

<div align="center">

![BlockRun](assets/blockrun-agent-skill.png)

[![Claude Code](https://img.shields.io/badge/Claude_Code-Skill-orange.svg)](https://github.com/anthropics/skills)
[![Antigravity](https://img.shields.io/badge/Antigravity-Compatible-4285F4.svg)](https://antigravity.google)
[![No API Keys](https://img.shields.io/badge/API_Keys-None_Required-brightgreen.svg)](https://blockrun.ai)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

</div>

**Your AI agent can't access X/Twitter, generate images, or call other models. BlockRun fixes that — no API keys, no subscriptions, just micropayments.**

---

## Use Cases

### 1. Competitor Intelligence

_Track what your competitors post, who follows them, and how they stack up against you._

```
"compare @competitor vs @us"                → side-by-side engagement scores
"get followers of @competitor"              → export 5,000 followers to CSV
"analyze @competitor's X presence"          → content strategy insights
"what has @competitor been tweeting?"       → recent posts with engagement stats
```

**Total cost: ~$0.32** — vs $100+/month for an X API subscription.

### 2. Lead Generation from X

_Build a prospect list from any account's followers — verified, with bios, ready for outreach._

```
"get verified followers of @targetcompany"  → high-value leads with bios
"export followings of @investor"            → find their portfolio companies
"lookup @lead1 @lead2 @lead3"              → enrich with follower counts, bios
```

CSV output with names, bios, follower counts — pipe straight into your CRM.

**Total cost: ~$0.25 per 1,000 accounts.**

### 3. Content & Trend Research

_Find what's working on X before you post._

```
"what's trending on X?"                     → trending topics ($0.002)
"search X for AI agents"                    → top tweets with engagement
"generate a cover image for my blog post"   → DALL-E image ($0.04)
```

**Total cost: ~$0.07** for a full research session.

### 4. Multi-Model Dev Workflow

_Get GPT to review what Claude wrote. Use DeepSeek to process 500 files for $0.05._

```
"GPT review this PR for security issues"    → GPT-5.2 second opinion (~$0.02)
"deepseek summarize every file in /docs"    → bulk processing at $0.0001/call
"generate a logo for my startup"            → DALL-E image ($0.04)
```

**30+ models, one wallet.** No API keys to juggle.

---

## Install

In Claude Code, just say:

```
try https://github.com/BlockRunAI/blockrun-agent-skill
```

Claude will install it, create a USDC wallet, and show a QR code to fund. Done.

<details>
<summary>Other install methods</summary>

- **Shell:** `curl -fsSL https://raw.githubusercontent.com/BlockRunAI/blockrun-agent-skill/main/install.sh | bash`
- **Solana:** `CHAIN=solana bash install.sh`
- **MCP Server:** `claude mcp add blockrun -- npx @blockrun/mcp`
- **Antigravity:** `git clone https://github.com/BlockRunAI/blockrun-agent-skill ~/.gemini/antigravity/skills/blockrun`

</details>

---

## X/Twitter Endpoints

15 endpoints your agent can't get natively:

| What you say | Endpoint | Cost |
|-------------|----------|------|
| "get @user's profile" | `x_user_info()` | $0.002 |
| "lookup @user1 @user2" | `x_user_lookup()` | $0.002/user |
| "get followers of @user" | `x_followers()` | $0.05/page |
| "who does @user follow?" | `x_followings()` | $0.05/page |
| "verified followers of @user" | `x_verified_followers()` | $0.048/page |
| "get @user's tweets" | `x_user_tweets()` | $0.032/page |
| "who's mentioning @user?" | `x_user_mentions()` | $0.032/page |
| "get data on this tweet" | `x_tweet_lookup()` | $0.16/batch |
| "show replies to this tweet" | `x_tweet_replies()` | $0.032/page |
| "show the full thread" | `x_tweet_thread()` | $0.032/page |
| "search X for..." | `x_search()` | $0.032/page |
| "what's trending?" | `x_trending()` | $0.002 |
| "what articles are going viral?" | `x_articles_rising()` | $0.05 |
| "analyze @user's presence" | `x_author_analytics()` | $0.02 |
| "compare @user1 vs @user2" | `x_compare_authors()` | $0.05 |

---

## Pricing

| Capability | $1 gets you |
|------------|-------------|
| X trending / profiles | ~500 calls |
| X followers / followings | ~20 pages (~4,000 accounts) |
| X tweets / search | ~31 pages |
| DALL-E images | ~25 images |
| GPT second opinions | ~50 calls |
| DeepSeek bulk processing | ~10,000 calls |

**$1-5 lasts weeks.** Compare: a single X API profile lookup costs $0.002 here vs $100/month for the official X API.

---

## How It Works

Your agent has a USDC wallet. When it needs a capability, it pays per request:

- No API keys to manage
- No monthly subscriptions ($0.002 per profile vs $100/month X API)
- Wallet balance is your spending cap
- Private key stays local (`~/.blockrun/`), never sent to any server

**New to USDC?** [5-minute guide](USDC_ON_BASE.md)

---

## Auto-Save

All paid data is automatically saved to `~/.blockrun/data/` — you never pay twice for the same data.

---

## Links

[blockrun.ai](https://blockrun.ai) · [USDC Guide](USDC_ON_BASE.md) · [x402 Protocol](https://x402.org) · [care@blockrun.ai](mailto:care@blockrun.ai)

---

MIT · Built by [@bc1beat](https://x.com/bc1beat)
