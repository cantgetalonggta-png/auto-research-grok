#!/usr/bin/env python3
"""Safe API key / token presence checks for AutoResearchGrok.

NEVER prints secret values. Only reports present/missing and optional live checks
that do not echo tokens.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from typing import Any

KEY_MAP = {
    "xai": ("XAI_API_KEY", "XAI_KEY"),
    "ai_gateway": ("AI_GATEWAY_API_KEY",),
    "openai": ("OPENAI_API_KEY", "OPENAI_KEY"),
    "vercel": ("VERCEL_TOKEN", "VERCEL_OIDC_TOKEN"),
    "github": ("GITHUB_TOKEN", "GITHUB_PAT", "GH_TOKEN"),
    "supabase_url": ("SUPABASE_URL", "NEXT_PUBLIC_SUPABASE_URL"),
    "supabase_anon": ("SUPABASE_ANON_KEY", "NEXT_PUBLIC_SUPABASE_ANON_KEY"),
    "elevenlabs": ("ELEVEN_LABS_KEY_", "ELEVENLABS_API_KEY", "ELEVEN_LABS_API_KEY"),
}


def _first_present(names: tuple[str, ...]) -> str | None:
    for n in names:
        v = os.environ.get(n)
        if v and str(v).strip():
            return n
    return None


def load_status() -> dict[str, Any]:
    services: dict[str, Any] = {}
    for svc, names in KEY_MAP.items():
        env_name = _first_present(names)
        services[svc] = {
            "status": "present" if env_name else "missing",
            "env": env_name,
        }
    return {
        "status": "connection_check",
        "services": services,
        "note": "Values never logged. Set secrets in Codespaces/Vercel only.",
    }


def verify_live(timeout: float = 8.0) -> dict[str, Any]:
    out: dict[str, Any] = {}
    try:
        req = urllib.request.Request(
            "https://ai-gateway.vercel.sh/v1/models",
            headers={"User-Agent": "auto-research-grok/1.0"},
        )
        with urllib.request.urlopen(req, timeout=timeout) as r:
            data = json.loads(r.read().decode("utf-8", errors="replace"))
            out["ai_gateway_public"] = {
                "ok": True,
                "model_count": len(data.get("data") or []),
            }
    except Exception as e:
        out["ai_gateway_public"] = {"ok": False, "error": type(e).__name__}

    for name, url in (
        ("manus_mcp_bridge", "https://manus-mcp-bridge-olive.vercel.app/health"),
        ("ma_os_console", "https://ma-os-12-console-echo-ec69.vercel.app/"),
        ("strand_osint", "https://strand-osint-mesh.vercel.app/"),
    ):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "auto-research-grok/1.0"})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                out[name] = {"ok": True, "http": r.status}
        except urllib.error.HTTPError as e:
            out[name] = {"ok": e.code < 500, "http": e.code}
        except Exception as e:
            out[name] = {"ok": False, "error": type(e).__name__}

    gw = _first_present(KEY_MAP["ai_gateway"])
    if gw:
        try:
            key = os.environ[gw]
            req = urllib.request.Request(
                "https://ai-gateway.vercel.sh/v1/models",
                headers={
                    "Authorization": f"Bearer {key}",
                    "User-Agent": "auto-research-grok/1.0",
                },
            )
            with urllib.request.urlopen(req, timeout=timeout) as r:
                out["ai_gateway_auth"] = {"ok": True, "http": r.status}
        except Exception as e:
            out["ai_gateway_auth"] = {"ok": False, "error": type(e).__name__}
    else:
        out["ai_gateway_auth"] = {"ok": False, "error": "missing_key"}

    xai = _first_present(KEY_MAP["xai"])
    if xai:
        try:
            key = os.environ[xai]
            req = urllib.request.Request(
                "https://api.x.ai/v1/models",
                headers={
                    "Authorization": f"Bearer {key}",
                    "User-Agent": "auto-research-grok/1.0",
                },
            )
            with urllib.request.urlopen(req, timeout=timeout) as r:
                out["xai_auth"] = {"ok": True, "http": r.status}
        except Exception as e:
            out["xai_auth"] = {"ok": False, "error": type(e).__name__}
    else:
        out["xai_auth"] = {"ok": False, "error": "missing_key"}

    return out


def main() -> None:
    p = argparse.ArgumentParser(description="API key presence + optional live checks")
    p.add_argument("--verify", action="store_true", help="Run live connectivity checks")
    p.add_argument("--json", action="store_true", help="JSON only")
    args = p.parse_args()
    report = load_status()
    if args.verify:
        report["live"] = verify_live()
    print(json.dumps(report, indent=2))
    sys.exit(0)


if __name__ == "__main__":
    main()
