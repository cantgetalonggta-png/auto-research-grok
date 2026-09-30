# auto-research-grok plugin

Grok Build plugin for autonomous research with xAI SDK driver.

## Local test

```bash
grok --plugin-dir /path/to/auto-research-grok
```

## Driver

```bash
export XAI_API_KEY=...
pip install xai-sdk
python skills/auto-research-grok/scripts/auto_research_driver.py "your question"
```

Do not commit API keys.
