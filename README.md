# SocialClaw

<div align="center">

<img src="assets/banner.png" alt="SocialClaw" width="600" />

<h3>Grow your X/Twitter to 1M+ views with AI-powered intelligence</h3>

<p>Real-time trend detection, audience insights, engagement optimization, and content strategy — all from your AI coding agent. No API keys needed.</p>

<br />

[![Claude Code](https://img.shields.io/badge/Claude_Code-Skill-orange.svg)](https://github.com/anthropics/skills)
[![OpenAI Codex](https://img.shields.io/badge/OpenAI_Codex-Compatible-412991.svg)](https://openai.com/codex)
[![Gemini CLI](https://img.shields.io/badge/Gemini_CLI-Compatible-4285F4.svg)](https://github.com/google-gemini/gemini-cli)
[![Cursor](https://img.shields.io/badge/Cursor-Compatible-000000.svg)](https://cursor.com)

[Growth Playbooks](#growth-playbooks) · [Get Started](#get-started) · [Docs](docs/) · [Pricing](docs/pricing.md)

</div>

---

## Growth Playbooks

### How to get your first 1M impression week

The accounts hitting 1M+ views aren't posting better content — they're posting the right content at the right time in the right conversations.

```
"Run a SocialClaw radar on AI agents"
```

SocialClaw shows you **what's trending right now with real view counts**:

```
  Anthropic          158 articles   115,983,616 views
  OpenAI              48 articles    51,378,182 views
  Claude Code         29 articles    44,825,583 views
  Bitcoin             34 articles    27,136,645 views
```

Then pulls the **latest tweets getting engagement** on your topic — so you can see what angles are working, what format gets likes, and where the conversation is heading.

**The play:** Post your take on the #1 trending topic within 2 hours of it spiking. SocialClaw catches it. You ride the wave.

---

### How to build a high-value audience (not just followers)

10K followers who are all bots = worthless. 500 followers where 20 have 50K+ followers = distribution machine.

```
"Run a SocialClaw audience analysis on @jessepollak"
```

SocialClaw segments followers by influence tier:

```
  MEGA (100K+):  @alloxdotai (131K), @AprilCumberland (60K)
  MACRO (10K-100K):  8 accounts
  MICRO (1K-10K):  15 accounts

  COMMON BIO THEMES: "crypto", "web3", "builder", "defi"
```

**The play:** Study what Mega and Macro followers care about. Create content for THEM — not for the masses. When a 100K account likes your post, their followers see it. That's how you 10x impressions without 10x effort.

---

### How to 10x your engagement rate

Most people post and pray. SocialClaw finds the conversations that are already getting traction — you just need to show up.

```
"Run a SocialClaw hitlist on AI agents crypto"
```

```
  @solana_daily (45K followers) — 15 likes, climbing
    "Solana Projects to Watch this Week: @BlockRunAI..."
    → Jump in: share a specific insight or data point about your project

  @A47X124 (12K followers) — 8 likes
    "The ones not on these lists are usually the ones that surprise..."
    → Jump in: agree + drop your own unlisted pick
```

**The play:** Spend 15 minutes replying to the top 5 conversations SocialClaw surfaces. A thoughtful reply on a trending thread gets more impressions than a standalone tweet to your 500 followers.

---

### How to find the right people to connect with

Growth on X is about relationships, not broadcasting. SocialClaw finds who actually drives conversation in your space.

```
"Run a SocialClaw scout on base blockchain"
```

```
  TOP VOICES
    @jessepollak            347,004 followers — @base builder #001
    @BuildOnBase             89,200 followers — Official Base account
    @coinaborsh              45,000 followers — Ecosystem analyst
```

**The play:** Pick 5-10 accounts from the scout list. Follow them, engage with their content consistently for 2 weeks. Not spam — genuine replies with insights. When they notice you, one retweet from a 50K account = more reach than a month of solo posting.

---

### How to know what to post every morning

Decision fatigue kills consistency. SocialClaw gives you 3 actions every morning — just execute.

```
"Run a SocialClaw brief on @myaccount"
```

```
  YOUR MENTIONS: 5 new (reply to @Rich_lifee_ — talking about you to 5K followers)
  TRENDING: Anthropic at 115M views, Claude Code at 44M views
  RISING: "AI agents reshape products" going viral

  SUGGESTED ACTIONS
    1. Reply to @Rich_lifee_ with a specific insight
    2. Post your take on the Anthropic trend
    3. Quote-tweet the rising AI agents article with your angle
```

**The play:** Run this every morning before your first tweet. 2 minutes. 3 actions. Done. Consistency > creativity.

---

### How to benchmark your growth

You can't improve what you don't measure. Compare your account against others at your stage or above.

```
"Run a SocialClaw compare on @me vs @competitor"
```

```
  METRIC              @you            @them
  ─────────────────────────────────────────
  Followers           2,100           8,400
  Mention likes          56               7
  Top follower      131,567             525
```

**The insight:** Fewer followers but way more mention engagement and higher-quality followers? You're on the right track — your audience is more engaged per capita. Double down on engagement quality, not follower count.

---

### How to study what content actually works

Stop copying what looks good. See what actually gets numbers.

```
"Run a SocialClaw insight on @topaccount"
```

SocialClaw pulls their mentions, engagement patterns, and audience composition. Look at:

- **Which of their tweets get mentioned by big accounts?** That's the content format that works.
- **What's their F/F ratio?** High ratio = their content pulls followers organically.
- **Who are their most influential followers?** That tells you who they create content for.

**The play:** Find 3 accounts at 10x your size. Run insight on each. Look for patterns in what gets their big followers to engage. Adapt that format for your niche.

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

Wallet auto-detected from any `~/.<provider>/` folder. Base or Solana USDC. No config needed.

---

## Works With Every AI Agent

| Platform | How |
|----------|-----|
| **Claude Code** | Loads as a skill. Just say "run socialclaw insight on @user". |
| **OpenAI Codex** | `pip install blockrun-llm[solana]` in sandbox. |
| **Gemini CLI** | Clone to `~/.gemini/antigravity/skills/socialclaw`. |
| **Cursor / Windsurf** | Agent reads CLAUDE.md, calls SDK via terminal. |
| **Any terminal** | `python scripts/socialclaw.py radar "topic"` |
| **Your own agent** | `from blockrun_llm import SolanaLLMClient` |

---

## How It Works

```
   "How do I get more views on my AI content?"
    ↓
   SocialClaw finds your wallet (auto-scan ~/.<any>/)
    ↓
   Pulls real-time X data via BlockRun API (x402 micropayment)
    ↓
   Saves everything locally (~/.blockrun/data/)
    ↓
   AI agent turns data into actionable growth strategy
```

- **No API keys.** Your wallet IS your authentication.
- **No subscriptions.** ~$0.08 per report. $1 = ~12 reports.
- **Private key stays local.** Only signatures are sent.
- **Data is yours.** Every response saved as JSON.

---

## Docs

| | |
|--|--|
| [Pricing](docs/pricing.md) | Costs per workflow, per endpoint, vs. alternatives |
| [API Reference](docs/api-reference.md) | All 16 X/Twitter endpoints + 30 AI models |

---

<div align="center">

**[blockrun.ai](https://blockrun.ai)** · **[AttentionVC](https://attentionvc.com)** · **[x402 Protocol](https://x402.org)** · **[hello@blockrun.ai](mailto:hello@blockrun.ai)**

Powered by [BlockRun](https://blockrun.ai) × [AttentionVC](https://attentionvc.com) · MIT

</div>
