#!/usr/bin/env python3
"""AutoResearch driver wired to official xai-sdk when installed.
Requires: pip install xai-sdk && export XAI_API_KEY=...
"""
from __future__ import annotations
import argparse, importlib, json, os, subprocess, sys
from typing import Any

SYSTEM = """You are an autonomous research agent.
On hard knowledge gaps, plan actions from: search, skill, install (only if allowed), code.
Do not invent facts. Prefer existing tools."""

def get_client():
    try:
        from xai_sdk import Client
    except ImportError as e:
        raise SystemExit("xai-sdk not installed. Run: pip install xai-sdk") from e
    if not os.environ.get("XAI_API_KEY"):
        raise SystemExit("Set XAI_API_KEY in the environment (do not hardcode).")
    return Client()

class AutoResearchGrok:
    def __init__(self, allow_pip_install: bool = False, model: str = "grok-3") -> None:
        self.allow_pip_install = allow_pip_install
        self.model = model
        self.client = get_client()
        self.tools: dict[str, Any] = {}
        self.skill_registry: dict[str, Any] = {}

    def install_tool(self, module_name: str) -> None:
        if not self.allow_pip_install:
            raise RuntimeError(f"pip install blocked for {module_name!r}. Pass --allow-pip after approval.")
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
            user += "\n\nRespond with JSON only using keys: status, missing_knowledge, actions, tool_code, research_summary, skill_updates."
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
            return {"error": f"chat failed: {e}", "hint": "Check xai-sdk examples for your version"}
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
                    with open("auto_tool.py", "w", encoding="utf-8") as f:
                        f.write(str(data["tool_code"]))
                    print("Wrote auto_tool.py — review before import")
                if isinstance(data.get("skill_updates"), dict):
                    self.skill_registry.update(data["skill_updates"])
            return data
        return text

def main() -> None:
    p = argparse.ArgumentParser(description="AutoResearchGrok + xai-sdk driver")
    p.add_argument("query", nargs="?", default="What is the xAI SDK chat quickstart?")
    p.add_argument("--allow-pip", action="store_true")
    p.add_argument("--machine", action="store_true")
    p.add_argument("--model", default=os.environ.get("XAI_MODEL", "grok-3"))
    args = p.parse_args()
    ag = AutoResearchGrok(allow_pip_install=args.allow_pip, model=args.model)
    out = ag.ask(args.query, machine=args.machine)
    print(json.dumps(out, indent=2, default=str) if isinstance(out, (dict, list)) else out)

if __name__ == "__main__":
    main()
