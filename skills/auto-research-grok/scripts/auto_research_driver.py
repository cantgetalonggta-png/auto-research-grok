#!/usr/bin/env python3
"""AutoResearch driver: xai-sdk OR Vercel AI Gateway (OpenAI-compatible).

Env (one of):
  XAI_API_KEY          -> xai_sdk Client
  AI_GATEWAY_API_KEY   -> OpenAI client at https://ai-gateway.vercel.sh/v1
"""
from __future__ import annotations
import argparse, importlib, json, os, subprocess, sys
from typing import Any

SYSTEM = (
    "You are an autonomous research agent. "
    "On hard knowledge gaps, plan actions from: search, skill, install (only if allowed), code. "
    "Do not invent facts. Prefer existing tools."
)

def _openai_gateway_client():
    try:
        from openai import OpenAI
    except ImportError as e:
        raise SystemExit("pip install openai  (for AI Gateway path)") from e
    key = os.environ.get("AI_GATEWAY_API_KEY")
    if not key:
        raise SystemExit("Set AI_GATEWAY_API_KEY")
    return OpenAI(api_key=key, base_url="https://ai-gateway.vercel.sh/v1")

def _xai_client():
    try:
        from xai_sdk import Client
    except ImportError as e:
        raise SystemExit("pip install xai-sdk") from e
    if not os.environ.get("XAI_API_KEY"):
        raise SystemExit("Set XAI_API_KEY")
    return Client()

class AutoResearchGrok:
    def __init__(self, allow_pip_install: bool = False, model: str | None = None, backend: str = "auto") -> None:
        self.allow_pip_install = allow_pip_install
        self.tools: dict[str, Any] = {}
        self.skill_registry: dict[str, Any] = {}
        self.backend = backend
        if backend == "auto":
            if os.environ.get("AI_GATEWAY_API_KEY"):
                self.backend = "gateway"
            elif os.environ.get("XAI_API_KEY"):
                self.backend = "xai"
            else:
                raise SystemExit("Set AI_GATEWAY_API_KEY or XAI_API_KEY")
        if self.backend == "gateway":
            self.client = _openai_gateway_client()
            self.model = model or os.environ.get("AI_GATEWAY_MODEL", "openai/gpt-4o-mini")
        else:
            self.client = _xai_client()
            self.model = model or os.environ.get("XAI_MODEL", "grok-3")

    def install_tool(self, module_name: str) -> None:
        if not self.allow_pip_install:
            raise RuntimeError(f"pip install blocked for {module_name!r}")
        try:
            self.tools[module_name] = importlib.import_module(module_name)
            return
        except ImportError:
            subprocess.check_call([sys.executable, "-m", "pip", "install", module_name])
            importlib.invalidate_caches()
            self.tools[module_name] = importlib.import_module(module_name)

    def ask(self, query: str, machine: bool = False) -> Any:
        user = query
        if machine:
            user += (
                "\n\nRespond with JSON only using keys: status, missing_knowledge, "
                "actions, tool_code, research_summary, skill_updates."
            )
        if self.backend == "gateway":
            resp = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": SYSTEM},
                    {"role": "user", "content": user},
                ],
            )
            text = resp.choices[0].message.content or ""
        else:
            chat = self.client.chat.create(model=self.model)
            try:
                chat.append(role="system", content=SYSTEM)
            except Exception:
                pass
            try:
                chat.append(role="user", content=user)
            except TypeError:
                chat.append({"role": "user", "content": user})
            try:
                response = chat.sample()
                text = getattr(response, "content", None) or str(response)
            except Exception as e:
                return {"error": f"chat failed: {e}"}

        if machine:
            try:
                data = json.loads(text)
            except json.JSONDecodeError:
                return {"status": "text", "research_summary": text}
            if data.get("status") == "auto_research":
                for action in data.get("actions") or []:
                    if isinstance(action, str) and action.startswith("install:"):
                        self.install_tool(action.split("install:", 1)[1].strip())
                if data.get("tool_code"):
                    from pathlib import Path
                    Path("auto_tool.py").write_text(str(data["tool_code"]), encoding="utf-8")
                if isinstance(data.get("skill_updates"), dict):
                    self.skill_registry.update(data["skill_updates"])
            return data
        return text

def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("query", nargs="?", default="Say hello in one sentence.")
    p.add_argument("--allow-pip", action="store_true")
    p.add_argument("--machine", action="store_true")
    p.add_argument("--backend", choices=["auto", "gateway", "xai"], default="auto")
    p.add_argument("--model", default=None)
    args = p.parse_args()
    ag = AutoResearchGrok(allow_pip_install=args.allow_pip, model=args.model, backend=args.backend)
    out = ag.ask(args.query, machine=args.machine)
    print(json.dumps(out, indent=2, default=str) if isinstance(out, (dict, list)) else out)

if __name__ == "__main__":
    main()
