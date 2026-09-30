# auto-research-grok plugin

Autonomous research + safe API key checks.

## Drivers

```bash
python skills/auto-research-grok/scripts/api_keys_driver.py --verify --json

export AI_GATEWAY_API_KEY=...   # or XAI_API_KEY
python skills/auto-research-grok/scripts/auto_research_driver.py "your question"
```

## Secrets

Set only in GitHub Codespaces Secrets and Vercel Environment Variables.
See `skills/auto-research-grok/references/api-keys-ops.md`.

Do not commit API keys.
