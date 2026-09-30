---
name: auto-research-grok
description: Autonomous research loop with knowledge-gap detection, xAI SDK wiring, tool install gates, multi-agent chain Researcher-Analyst-Synthesizer-Verifier, and skill registry updates. Use when the user invokes AutoResearchGrok, AUTO_RESEARCH, autonomous research agent, knowledge-gap plus install or search language, or /auto-research.
---

# Auto-research Grok

Controlled autonomous research. Prefer built-in tools and installed skills over new packages.

## Triggers
AutoResearchGrok, AUTO_RESEARCH, autonomous research agent, knowledge-gap + install/search, `/auto-research`.

Related: `tool-use`, `agent-orchestration`, `grok-4-20-multi-agent`, `ethical-data-harvesting`, `ethical-scraper-orchestration`, `xai-sdk-python`.

## Roles
1. Researcher — missing facts, search plan, call tools
2. Analyst — structure evidence, confidence, conflicts
3. Synthesizer — final answer + citations
4. Verifier — challenge unsupported claims

## Procedure
1. Name the knowledge gap in one sentence.
2. Actions allowlist only: `search:`, `skill:`, `install:` (user approval only), `code:`.
3. Execute real tool calls. Never invent tool results.
4. Summarize with uncertainty marked.
5. Optional skill_updates — no secrets.

## Driver
`scripts/auto_research_driver.py` with `XAI_API_KEY`. See references/xai-sdk-wiring.md.

## Safety
No silent pip install. No API keys in files. Public sources only for OSINT. Review generated code before import.
