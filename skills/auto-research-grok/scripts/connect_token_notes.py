#!/usr/bin/env python3
"""Map Vercel Connect auth to AutoResearchGrok backends."""
from __future__ import annotations
import json
import os

CONNECTOR_UIDS = [
    os.environ.get("CONNECT_GROK_UID") or "",
    "grok/acme-grok",
    "api.x.ai/xai-sdk-key",
    "xai_sdk_key/ma-os-12-console",
]

def report() -> dict:
    return {
        "connect_leg": "OIDC or VERCEL_TOKEN → POST /v1/connect/token/{uid}",
        "subject": {"type": "app"},
        "connector_uid_candidates": [u for u in CONNECTOR_UIDS if u],
        "python_env_fallback": {
            "XAI_API_KEY": bool(os.environ.get("XAI_API_KEY") or os.environ.get("XAI_KEY")),
            "AI_GATEWAY_API_KEY": bool(os.environ.get("AI_GATEWAY_API_KEY")),
            "VERCEL_OIDC_TOKEN": bool(os.environ.get("VERCEL_OIDC_TOKEN")),
        },
        "cli_setup": [
            "vercel link",
            "vercel connect create grok --name acme-grok",
            "vercel env pull",
        ],
    }

if __name__ == "__main__":
    print(json.dumps(report(), indent=2))
