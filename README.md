# SocialClaw

<div align="center">

<img src="assets/banner.png" alt="SocialClaw" width="600" />

<h1>Intelligence-as-a-function</h1>

<p><strong>The first X/Twitter analytics an agent can call.</strong><br>
One function call = one intelligence report. $0.08, not $49/month.<br>
No dashboard. No login. No subscription. Because agents don't need UI.</p>

<br />

[![Claude Code](https://img.shields.io/badge/Claude_Code-Skill-orange.svg)](https://github.com/anthropics/skills)
[![OpenAI Codex](https://img.shields.io/badge/OpenAI_Codex-Compatible-412991.svg)](https://openai.com/codex)
[![Gemini CLI](https://img.shields.io/badge/Gemini_CLI-Compatible-4285F4.svg)](https://github.com/google-gemini/gemini-cli)
[![Cursor](https://img.shields.io/badge/Cursor-Compatible-000000.svg)](https://cursor.com)

[How It's Different](#how-its-different) · [Workflows](#workflows) · [Get Started](#get-started) · [Pricing](docs/pricing.md)

</div>

---

## How It's Different

TweetHunter, Typefully, Hypefury — they're all **dashboards for humans**. $49-99/month for a UI you log into.

SocialClaw is none of that.

| | Traditional Tools | SocialClaw |
|---|---|---|
| **Interface** | Dashboard (human logs in) | Function call (agent calls it) |
| **Pricing** | $49-99/month subscription | $0.08 per report |
| **Auth** | Email + password | USDC wallet signature |
| **Output** | Charts you read | JSON your agent processes |
| **Workflow** | Human reads → decides → acts | Agent calls → gets data → acts |

**The flow:**

```
agent calls socialclaw → gets trend data → writes tweet → posts
```

No dashboard. No login. No subscription. Intelligence-as-a-function.

---

## Workflows

### `insight @username` — Deep-dive account analysis

```bash
socialclaw insight @targetaccount
```

Who follows them, who mentions them, what content works. Your agent gets structured intelligence, not a pretty chart.

### `radar <topic>` — What's trending right now

```bash
socialclaw radar "AI agents"
```

```
TRENDING NOW
  Anthropic          158 articles   115,983,616 views
  Claude Code         29 articles    44,825,583 views
  Bitcoin             34 articles    27,136,645 views
```

Real view counts, not vanity metrics. Your agent reads this and knows what to post about.

### `scout <topic>` — Find the right people

```bash
socialclaw scout "x402 crypto"
```

```
TOP VOICES
  @jessepollak        347,004 followers — @base builder #001
  @BuildOnBase         89,200 followers — Official Base account
  @coinaborsh          45,190 followers — ecosystem builder
```

### `audience @account` — Follower analysis by influence tier

```bash
socialclaw audience @targetaccount
```

```
MEGA (100K+):   @alloxdotai (131K), @AprilCumberland (60K)
MACRO (10K-100K):  8 accounts
MICRO (1K-10K):  15 accounts
```

### `compare @user1 @user2` — Side-by-side competitor analysis

```bash
socialclaw compare @you @competitor
```

### `hitlist <topic>` — High-engagement conversations to join

```bash
socialclaw hitlist "AI agents crypto"
```

```
@solana_daily (45K followers) — 15 likes, climbing
  "Solana Projects to Watch this Week"
  https://x.com/solana_daily/status/123456789
  → Reply with specific data. Numbers get retweeted.
```

### `brief @handle` — Morning mentions and alerts

```bash
socialclaw brief @yourhandle
```

> "@HarryKamaAI (196K followers) just mentioned you. 3 new mentions overnight."
>
> Reply within 30 minutes. Speed = visibility.

---

## Get Started

**Claude Code:**
```
try https://github.com/BlockRunAI/socialclaw
```

**Codex / Cursor / any agent:**
```bash
pip install blockrun-llm[solana]
```

**CLI:**
```bash
git clone https://github.com/BlockRunAI/socialclaw && cd socialclaw
pip install blockrun-llm[solana]
python scripts/socialclaw.py radar "your topic"
```

Wallet auto-detected. Base or Solana USDC. No config needed.

---

## Works With Every AI Agent

| Platform | How |
|----------|-----|
| **Claude Code** | Loads as a skill. "Run socialclaw insight on @user". |
| **OpenAI Codex** | `pip install blockrun-llm[solana]` in sandbox. |
| **Gemini CLI** | Clone to `~/.gemini/antigravity/skills/socialclaw`. |
| **Cursor / Windsurf** | Agent reads CLAUDE.md, calls SDK via terminal. |
| **Any terminal** | `python scripts/socialclaw.py radar "topic"` |
| **Your own agent** | `from blockrun_llm import SolanaLLMClient` |

---

## How It Works

- **No API keys.** Your USDC wallet IS your authentication.
- **No subscriptions.** ~$0.08 per report. $1 = ~12 reports.
- **Private key stays local.** Only signatures are sent.
- **Data is yours.** Every response saved as JSON in `~/.blockrun/data/`.

[Pricing details](docs/pricing.md) · [API Reference](docs/api-reference.md)

---

## Growth Playbook

These are the plays that get results:

**Ride the wave** — `radar` shows you what's trending with real view counts. Post your angle on the #1 trend within 2 hours.

**Activate your big followers** — `audience` segments followers by influence. One retweet from a 100K account > 100 of your own tweets.

**Join the right conversations** — `hitlist` finds high-engagement threads. 15 minutes replying to top 5 conversations > 1 standalone tweet.

**Build relationships** — `scout` finds KOLs in your space. Pick 5, engage consistently for 2 weeks. One RT from a 50K = a month of solo posting.

**Study what works** — `insight` shows what content gets numbers. Don't guess, measure.

---

## From the BlockRun Ecosystem

<table>
<tr>
<td width="50%">

### 🦞 SocialClaw
**Intelligence-as-a-function for X/Twitter**

You're here. The first X analytics an agent can call. $0.08 per report, no dashboard, no subscription.

`pip install blockrun-llm[solana]`

</td>
<td width="50%">

### ⚡ [ClawRouter](https://github.com/BlockRunAI/ClawRouter)
**The LLM router built for autonomous agents**

41+ models, local smart routing, x402 USDC payments — the only stack that lets agents operate independently.

`curl -fsSL https://blockrun.ai/ClawRouter-update | bash`

[![GitHub stars](https://img.shields.io/github/stars/BlockRunAI/ClawRouter?style=flat-square)](https://github.com/BlockRunAI/ClawRouter)

</td>
</tr>
</table>

> **SocialClaw + ClawRouter together:** SocialClaw pulls X/Twitter intelligence. ClawRouter routes your LLM requests to the cheapest capable model. Same wallet, same payment layer, two agent superpowers.

---

<div align="center">

**[blockrun.ai](https://blockrun.ai)** · **[AttentionVC](https://attentionvc.com)** · **[x402 Protocol](https://x402.org)** · **[hello@blockrun.ai](mailto:hello@blockrun.ai)**

Powered by [BlockRun](https://blockrun.ai) × [AttentionVC](https://attentionvc.com) · MIT

</div>
