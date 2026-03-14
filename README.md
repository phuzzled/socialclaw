# SocialClaw

<div align="center">

<img src="assets/banner.png" alt="SocialClaw" width="600" />

<h3>Grow your X/Twitter to 5M+ views in 3 months with AI-powered intelligence</h3>

<p>Real-time trend detection, audience insights, engagement optimization, and content strategy — powered by your AI agent. No API keys needed.</p>

<br />

[![Claude Code](https://img.shields.io/badge/Claude_Code-Skill-orange.svg)](https://github.com/anthropics/skills)
[![OpenAI Codex](https://img.shields.io/badge/OpenAI_Codex-Compatible-412991.svg)](https://openai.com/codex)
[![Gemini CLI](https://img.shields.io/badge/Gemini_CLI-Compatible-4285F4.svg)](https://github.com/google-gemini/gemini-cli)
[![Cursor](https://img.shields.io/badge/Cursor-Compatible-000000.svg)](https://cursor.com)

[Daily Routine](#your-daily-growth-routine) · [Playbooks](#growth-playbooks) · [Get Started](#get-started) · [Pricing](docs/pricing.md)

</div>

---

## Your Daily Growth Routine

Three commands. Every day. That's it.

**Morning — see who's talking about you, reply immediately:**
```
socialclaw brief @yourhandle
```
> _"@HarryKamaAI (196K followers) just mentioned you. @solana_daily listed you as Project to Watch. 3 new mentions overnight."_
>
> Reply within 30 minutes. Speed = visibility.

**Before you post — see what has momentum right now:**
```
socialclaw radar "your topic"
```
> _"Anthropic is at 115M views today. Claude Code has 44M. Bitcoin at 27M."_
>
> Post your angle on the #1 trend within 2 hours of it spiking. That's how you ride 100M+ view waves.

**Weekly — discover new people to connect with:**
```
socialclaw scout "x402 crypto"
```
> _"Top voices: @jessepollak (347K), @BuildOnBase (89K), @coinaborsh (45K)..."_
>
> Pick 5 accounts. Engage consistently for 2 weeks. One retweet from a 50K account = more reach than a month of solo posting.

---

## Real Example: Growing a Startup's X Presence

We ran SocialClaw on a startup account with ~3K followers. Here's the playbook it generated:

### 3 things to do right now

**1. Activate your biggest followers**

SocialClaw scans your follower list and ranks by influence. Typical output:

```
  TOP FOLLOWERS
    @mega_influencer         196,829 followers
    @vc_partner               83,120 followers
    @ecosystem_builder        55,190 followers
    @community_lead           16,822 followers  ← DM'd you, reply!
    @early_supporter          11,662 followers  ← publicly praised you, reply with update
```

> One retweet from a 100K+ account = more impressions than 100 of your own tweets. Engage with these people first.

**2. Ride today's trending wave**

SocialClaw pulls real-time trending data with actual view counts:

```
  TRENDING NOW
    Anthropic          158 articles   115,983,616 views
    Claude Code         29 articles    44,825,583 views
    Bitcoin             34 articles    27,136,645 views
```

> Find the trend that overlaps with what you're building. Post your angle within 2 hours. That's how you ride a 100M+ view wave.

**3. Join the conversations that matter**

SocialClaw finds high-engagement conversations in your space with direct links:

```
  @major_account (45K followers) — 15 likes, climbing
    "Projects to Watch this Week: @yourproject..."
    https://x.com/major_account/status/123456789
    → Reply with specific data. "We just shipped X — 7 features, Y metric." Numbers get retweeted.
```

> "We shipped X with Y result" > "Great list!" Every time.

### Your weekly growth routine

| Day | Action | Tool |
|-----|--------|------|
| Every morning | Check mentions, reply fast | `socialclaw brief @yourhandle` |
| Before posting | Find trending angle | `socialclaw radar "your niche"` |
| Mon & Thu | Discover new KOLs to engage | `socialclaw scout "your topic"` |
| Wednesday | Study a bigger account in your space | `socialclaw insight @targetaccount` |
| Friday | Benchmark your growth | `socialclaw compare @you @similaraccount` |

---

## Growth Playbooks

### Get your first 1M impression week

The accounts hitting 1M+ views aren't posting better content — they're posting the right content at the right time.

```
socialclaw radar "AI agents"
```

SocialClaw shows trending topics with **real view counts** (not vanity metrics):

```
  Anthropic          158 articles   115,983,616 views
  OpenAI              48 articles    51,378,182 views
  Claude Code         29 articles    44,825,583 views
```

**The play:** Post your take on the #1 trend within 2 hours. SocialClaw catches the spike. You ride the wave.

---

### Build a high-value audience

10K followers who are all bots = worthless. 500 followers where 20 have 50K+ = a distribution machine.

```
socialclaw audience @targetaccount
```

SocialClaw segments followers by influence tier:

```
  MEGA (100K+):  @alloxdotai (131K), @AprilCumberland (60K)
  MACRO (10K-100K):  8 accounts
  MICRO (1K-10K):  15 accounts
```

**The play:** Study what Mega followers care about. Create content for THEM. When a 100K account likes your post, their followers see it.

---

### 10x your engagement rate

Stop posting into the void. Show up in conversations that are already getting traction.

```
socialclaw hitlist "AI agents crypto"
```

```
  @solana_daily (45K followers) — 15 likes, climbing
    "Solana Projects to Watch this Week"
    → Jump in with a specific data point
```

**The play:** 15 minutes replying to top 5 conversations > 1 standalone tweet to your followers.

---

### Find the right people to connect with

Growth on X is relationships, not broadcasting.

```
socialclaw scout "base blockchain"
```

```
  @jessepollak        347,004 followers — @base builder #001
  @BuildOnBase         89,200 followers — Official Base account
```

**The play:** Pick 5 accounts. Engage consistently for 2 weeks. Not spam — genuine replies. One RT from a 50K = a month of solo posting.

---

### Study what content actually works

Don't guess. See what gets numbers.

```
socialclaw insight @topaccount
```

Look at: Which mentions come from big accounts? What's their F/F ratio? Who are their most influential followers — that's who they're really creating content for.

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

## From the BlockRun Ecosystem

<table>
<tr>
<td width="50%">

### 🦞 SocialClaw
**X/Twitter Marketing Intelligence**

You're here. Grow to 5M+ views in 3 months with trend detection, audience insights, and engagement optimization.

`pip install blockrun-llm[solana]`

</td>
<td width="50%">

### ⚡ [ClawRouter](https://github.com/BlockRunAI/ClawRouter)
**Smart LLM Router — 92% Cost Savings**

Route every AI request to the right model at the right price. 41+ models, <1ms local routing, auto-switches between GPT, Claude, Gemini, DeepSeek based on task.

`curl -fsSL https://blockrun.ai/ClawRouter-update | bash`

[![GitHub stars](https://img.shields.io/github/stars/BlockRunAI/ClawRouter?style=flat-square)](https://github.com/BlockRunAI/ClawRouter)

</td>
</tr>
</table>

> **SocialClaw + ClawRouter together:** SocialClaw uses ClawRouter under the hood to route your LLM requests to the cheapest model that can do the job. Your marketing intelligence reports cost less because ClawRouter picks DeepSeek for simple tasks and GPT-5 only when needed.

---

<div align="center">

**[blockrun.ai](https://blockrun.ai)** · **[AttentionVC](https://attentionvc.com)** · **[x402 Protocol](https://x402.org)** · **[hello@blockrun.ai](mailto:hello@blockrun.ai)**

Powered by [BlockRun](https://blockrun.ai) × [AttentionVC](https://attentionvc.com) · MIT

</div>
