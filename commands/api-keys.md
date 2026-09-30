---
description: Check API key presence and optional live connectivity (never prints secrets)
---
Run the safe key driver:

```bash
python skills/auto-research-grok/scripts/api_keys_driver.py --verify --json
```

Set secrets only in GitHub Codespaces Secrets and Vercel Project Environment Variables.
Canonical names: XAI_API_KEY, AI_GATEWAY_API_KEY, OPENAI_API_KEY, VERCEL_TOKEN, GITHUB_TOKEN.
