# auto-research-grok plugin

Grok Build plugin for autonomous research.

## Backends

- `AI_GATEWAY_API_KEY` + OpenAI SDK → `https://ai-gateway.vercel.sh/v1`
- `XAI_API_KEY` + xai-sdk

```bash
export AI_GATEWAY_API_KEY=...   # or XAI_API_KEY
pip install openai   # gateway path
# or: pip install xai-sdk
python skills/auto-research-grok/scripts/auto_research_driver.py "your question"
```

Local plugin test:

```bash
grok --plugin-dir .
```

Do not commit API keys.
