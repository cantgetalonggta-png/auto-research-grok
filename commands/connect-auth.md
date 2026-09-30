---
description: Vercel Connect auth notes for Grok/xAI
---
```bash
python skills/auto-research-grok/scripts/connect_token_notes.py
python skills/auto-research-grok/scripts/api_keys_driver.py --verify --json
```

```bash
vercel connect create grok --name acme-grok
vercel env pull
```

TS helper: `skills/auto-research-grok/scripts/connect_grok_token.ts`
