# API keys ops (Codespaces + Vercel)

## Principle
Never put secrets in chat, commits, or SKILL.md. Inject via:

1. **GitHub → Repo → Settings → Secrets and variables → Codespaces**
2. **Vercel → Project → Settings → Environment Variables** (Production / Preview / Development)

## Canonical names
| Service | Env names (first wins) |
|---------|------------------------|
| xAI | `XAI_API_KEY`, `XAI_KEY` |
| AI Gateway | `AI_GATEWAY_API_KEY` |
| OpenAI-compat | `OPENAI_API_KEY`, `OPENAI_KEY` |
| Vercel | `VERCEL_TOKEN`, `VERCEL_OIDC_TOKEN` |
| GitHub | `GITHUB_TOKEN`, `GITHUB_PAT`, `GH_TOKEN` |
| Supabase | `SUPABASE_URL`, `SUPABASE_ANON_KEY` |
| ElevenLabs | `ELEVEN_LABS_KEY_`, `ELEVENLABS_API_KEY` |

## Driver
```bash
python skills/auto-research-grok/scripts/api_keys_driver.py --verify --json
python skills/auto-research-grok/scripts/auto_research_driver.py "query"
```

## Rotation
1. Create new key at provider
2. Update Codespaces secret + Vercel env
3. Redeploy
4. Re-run `--verify`

## Vercel Connect
Long-lived provider keys can also live in Connect api-key connectors
(`api.x.ai/xai-sdk-key`) and be fetched at runtime via OIDC + `@vercel/connect`.
