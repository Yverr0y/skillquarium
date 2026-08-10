---
title: semgrep
tags:
  - skill
  - domain/security-auditing
domain: security-auditing
status: untried
source: skills/semgrep/SKILL.md
created: 2026-06-09
---

# semgrep

> [!info] What it does
> Run Semgrep static analysis scan on a codebase using parallel subagents. Supports two scan modes — "run all" (full ruleset coverage) and "important only" (high-confidence security vulnerabilities). Automatically detects and uses Semgrep Pro for cross-file taint analysis when available. Use when asked to scan code for vulnerabilities, run a security audit with Semgrep, find bugs, or perform static analysis. Spawns parallel workers for multi-language codebases.

**Source:** [skills/semgrep/SKILL.md](../../../skills/semgrep/SKILL.md)  ·  **Domain:** [Security & Auditing](../../maps/security-auditing.md)  ·  **Table:** [skills.base](../../skills.base)  ·  **Index:** [Skills Index](../../index.md)

## Related skills

- [llm-agent-security-redteam](../../notes/security-auditing/llm-agent-security-redteam.md) — LLM and agent security red teaming with agentic-actions-auditor, supply-chain-risk-auditor, semgrep, codeql, and sarif-parsing
- [sarif-parsing](../../notes/security-auditing/sarif-parsing.md) — Parses and processes SARIF files from static analysis tools like CodeQL, Semgrep, or other scanners
- [semgrep-rule-creator](../../notes/security-auditing/semgrep-rule-creator.md) — Creates custom Semgrep rules for detecting security vulnerabilities, bug patterns, and code patterns
- [variant-analysis](../../notes/security-auditing/variant-analysis.md) — Hunts for the other instances of a bug already found — the variants of one root cause across a codebase

%% ---8<--- personal notes below are preserved on re-run ---8<--- %%

## Notes

> [!warning] Vault audit 2026-07-24 — MNT-9
> Cross-references a nonexistent `semgrep-rule-variant-creator` skill — the actual skill is `semgrep-rule-creator`. Use that name.
> _Remote-managed skill — the durable fix belongs upstream; this wrapper note is the local record._
