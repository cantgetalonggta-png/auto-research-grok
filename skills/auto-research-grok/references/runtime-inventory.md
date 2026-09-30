# Runtime inventory (automated, 2026-09-30)

## Vercel account
- User: `nevagetalong-1199` (`g7D3g321jvKBIYIQFMXmPAK8`)
- Default team: `team_kgQcPVmumwtmK3MdAGlxKJtg` (echo-ec69)
- Plan: hobby

## Projects
| Project | ID | Notes |
|---------|-----|-------|
| strand-osint-mesh | prj_LjAxbC9jdFsKAoRBVVcJeKcY0Yx5 | tanstack-start, LIVE |
| ma-os-12-console | prj_Ozz5MVxosia5r1JLxa5ah8Lb4ZV7 | Connect x2 |
| manus-mcp-bridge | prj_SuTX6tfZ84FFE6HvgZV6YdWKY2Eg | fastapi, LIVE olive |
| ma-os-12-unified-codespace | prj_iHmAU01G2PlvdNwc7mhk4P6fiaTZ | |
| agentbridge-launch | prj_6xN9B9YA5TuN8wTUVPKXdj6d7m9i | |
| agentbridge-beta | prj_HCDkOPI6kiDGGXPyI1yHJschYC0d | |

## Vercel Connect (api-key type)
| Connector ID | UID | Linked projects |
|--------------|-----|-----------------|
| scl_AuXxroMAqGl92nD7u02HRg | api.x.ai/xai-sdk-key | manus-mcp-bridge, ma-os-12-console |
| scl_iNr9BxHLpf0e7hgUPSMvA | xai_sdk_key/ma-os-12-console | ma-os-12-console |

Values encrypted — runtime via OIDC + `@vercel/connect` getToken, not MCP.

## Live URLs
- https://manus-mcp-bridge-olive.vercel.app
- https://strand-osint-mesh.vercel.app
- https://ma-os-12-console-echo-ec69.vercel.app

## Env pattern (ma-os-12-console .env.example)
```
AI_GATEWAY_API_KEY=
AI_GATEWAY_MODEL=openai/gpt-5.5
```

## MCP privilege map
| Action | Status |
|--------|--------|
| list/get projects (no teamId) | OK |
| list Connect project links | OK |
| get connector metadata | OK |
| get deployment | OK |
| create AI Gateway API key | 403 team scope |
| project OIDC mint | 403 |
| buy credits confirm | role missing |

## Driver
`skills/auto-research-grok/scripts/auto_research_driver.py`
- backend auto: AI_GATEWAY_API_KEY or XAI_API_KEY
