# Vercel Connect authentication (distilled)

Two legs on every token request:

1. **Caller → Connect** (who is allowed to ask)
2. **Connect → Provider** (how Connect proves itself to xAI/Slack/…)

## Caller → Connect

| Runtime | Auth |
|---------|------|
| Vercel deployment | `VERCEL_OIDC_TOKEN` (automatic) |
| Local + `vercel link` | `vercel env pull` → OIDC (~12h TTL) |
| CI / non-Vercel | `options.vercelToken` = access token |

```
POST https://api.vercel.com/v1/connect/token/{url-encoded-uid}
Authorization: Bearer <OIDC | access token>
{ "subject": { "type": "app" }, "scopes": [...] }
```

UID `slack/acme-slack` → path `slack%2Facme-slack`.

Project must be **linked** or SDK throws `ClientNotLinkedToProjectError` / `ClientNotEnabledForEnvironmentError`.

## Connect → Provider (this account)

| Connector UID | Type | Linked projects |
|---------------|------|-----------------|
| `api.x.ai/xai-sdk-key` | api-key | manus-mcp-bridge, ma-os-12-console |
| `xai_sdk_key/ma-os-12-console` | api-key | ma-os-12-console |

API-key connectors: **`subject: { type: 'app' }` only**.

## Official Grok connector

```bash
vercel link
vercel connect create grok --name acme-grok
vercel env pull
```

```ts
import { getToken } from '@vercel/connect';
const token = await getToken('grok/acme-grok', { subject: { type: 'app' } });
```

## AutoResearch mapping

| Mode | Auth |
|------|------|
| Python driver | `AI_GATEWAY_API_KEY` or `XAI_API_KEY` |
| Vercel Function | OIDC + getToken |
| Grok chat MCP | Separate OAuth |

Prefer OIDC over long-lived access tokens.
