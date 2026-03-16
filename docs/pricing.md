# Pricing

SocialClaw is free software. You pay only for the underlying services you use.

## What You Pay For

### 1. X API Subscription (required)

SocialClaw calls the official X API v2 ([docs.x.com/x-api](https://docs.x.com/x-api/introduction)).
You need an X Developer account and access tier:

> **Note:** Pricing is set by X/Twitter and may change. Always check [developer.x.com/en/portal/products](https://developer.x.com/en/portal/products) for current rates.

| Tier | Monthly cost (approx.) | Recommended for |
|------|-------------|----------------|
| **Free** | $0 | Testing, tweet/user lookups only |
| **Basic** | $100 | Most SocialClaw workflows (search, mentions, followers) |
| **Pro** | $5,000 | High-volume usage, commercial apps |
| **Enterprise** | Custom | Firehose, full archive search |

Get a key at [developer.x.com](https://developer.x.com/).

> **Most users need Basic ($100/mo).** Free tier does not allow tweet search or mentions.

### 2. OpenAI API (optional)

Only needed if you use the `engage` command's AI reply-draft feature.

Set `OPENAI_API_KEY` to enable. Uses `gpt-4o-mini` by default.

| Model | Input | Output | Cost for engage workflow |
|-------|-------|--------|--------------------------|
| `gpt-4o-mini` | $0.15/M tokens | $0.60/M tokens | ~$0.001 per call |
| `gpt-4o` | $2.50/M tokens | $10.00/M tokens | ~$0.01 per call |

See [platform.openai.com/pricing](https://platform.openai.com/pricing) for current rates.

### 3. Image Generation (optional)

For the `image` prompt workflow, you need an image generation API key.

| Provider | Model | Cost |
|----------|-------|------|
| OpenAI DALL-E 3 | Standard 1024×1024 | $0.040/image |
| OpenAI DALL-E 3 | HD 1024×1024 | $0.080/image |

Set `OPENAI_API_KEY` and use the image generation code in `prompts/image.md`.

## API Calls Per Workflow

| Workflow | Command | X API calls | Notes |
|----------|---------|-------------|-------|
| Tweet Lookup | `tweet <id>` | ~2 | 1 lookup + 1 search for replies |
| Thread Lookup | `thread <id>` | ~1 | conversation_id search |
| Author Analytics | `analytics @handle` | ~2 | profile + tweets |
| Account Deep-Dive | `insight @username` | ~4 | profile + mentions + followers + tweets |
| Topic Intelligence | `radar <topic>` | ~2 | recent + top search |
| Competitor Analysis | `compare @a @b` | ~6 | 2× (profile + mentions + followers) |
| Follower Segmentation | `audience @username` | ~2 | profile + followers |
| KOL Discovery | `scout <topic>` | ~1 | top tweet search |
| Engagement Targets | `hitlist <topic>` | ~1 | recent tweet search |
| Daily Marketing Brief | `brief @handle` | ~3 | profile + mentions + followers |
| Engage | `engage @handle` | ~3 | profile + mentions + search |
| Draft Post | `draft "topic"` | ~1 | search for examples |
| Review Post | `review` | 0 | no API calls (local scoring) |
| Search | `search <query>` | ~2 | recent + top |

## vs. Dashboard Tools

| What you need | SaaS dashboard | SocialClaw |
|--------------|---------------|------------|
| **Cost** | $49–$299/month fixed | X API Basic ($100/mo) + usage |
| **Output** | Charts for human eyes | Structured JSON your agent processes |
| **Agent-usable** | No (human UI only) | Yes — designed for agents |
| **Data ownership** | Locked in their platform | Saved locally to `~/.socialclaw/data/` |
| **Customizable** | No | Full source code — fork and adapt |

## Cost Example

Running `socialclaw radar "AI agents"` (2 API calls) on the X API Basic plan:

- Basic plan: $100/month flat rate
- 10,000 reads/month included
- Each `radar` call uses ~2 reads
- You could run ~5,000 radar calls per month on Basic

SocialClaw itself is free and open source (MIT).
