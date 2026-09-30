# Vercel Connect vs AI Gateway tokens

## Two different systems

1. **Grok Vercel MCP connector** — OAuth token for Vercel REST/MCP tools in this chat.
   - Can list projects without team scope.
   - Team-scoped writes (create AI Gateway keys, Connect admin) need scope `echo-ec69`.

2. **@vercel/connect SDK** — runs *inside a Vercel deployment* (or local with OIDC).
   - Reads `VERCEL_OIDC_TOKEN` (auto on Vercel; local: `vercel link` + `vercel env pull`).
   - `getToken(connectorUid, { subject: { type: 'app' } })` exchanges OIDC for provider tokens (Slack, GitHub, …).

3. **AI Gateway** — model inference API.
   - Base: `https://ai-gateway.vercel.sh/v1`
   - Auth: `AI_GATEWAY_API_KEY` **or** deployment OIDC (`VERCEL_OIDC_TOKEN`) for some AI SDK paths.
   - Does not use `@vercel/connect` for chat completions.

## Local OIDC (CLI)

```bash
vercel link          # pick project e.g. manus-mcp-bridge
vercel env pull      # writes .env.local with VERCEL_OIDC_TOKEN
# token is short-lived; re-pull on auth errors
```

## SDK minimal

```ts
import { getToken } from '@vercel/connect';
const token = await getToken('slack/my-bot', {
  subject: { type: 'app' },
  scopes: ['chat:write'],
});
```

Override: `{ vercelToken: process.env.MY_VERCEL_TOKEN }`.

## AI Gateway driver (Python)

```bash
export AI_GATEWAY_API_KEY=...   # from dashboard AI Gateway keys
python skills/auto-research-grok/scripts/auto_research_driver.py --backend gateway "query"
```

## When team MCP is 403

Use dashboard AI Gateway API key + this driver. Connect admin requires team-scoped token.
