# OpenAI Runtime Adapter Plan

Verified against current OpenAI platform documentation on 2026-09-15.

## Current platform primitives

OpenAI's Agents API supports reusable agents with named instructions/model configuration and explicit multi-agent configuration. Sessions can create/coordinate subagents. OpenAI Skills are versioned reusable workflow bundles built around `SKILL.md` plus resources.

DLADS is intentionally usable before any runtime publication: Codex reads Git-controlled instructions/state directly.

## Provider-neutral mapping

Internal DLADS manifest -> OpenAI runtime concept:

| DLADS | OpenAI |
|---|---|
| `id` / `version` | metadata + Git release/version reference |
| `name` | reusable agent `name` |
| `instructions_file` | agent `instructions` |
| `model_policy` | selected API `model` + reasoning configuration |
| `allow_subagents` | `multi_agent.enabled` |
| `max_concurrent_subagents` | multi-agent concurrency setting |
| Codex `SKILL.md` bundle | Skills API skill/version |
| `capabilities` | persisted tools/MCP/runtime tool policy |
| program state | Git/Command data, **not** hidden provider memory |
| provider agent/session IDs | metadata only |

## Publication rule

Do not publish or update a runtime agent merely because a manifest changed in Git.

Required sequence:

```text
Git agent version
  -> schema validation
  -> dry-run/eval gate
  -> permission/tool review
  -> cost policy review
  -> publish candidate runtime agent/skill
  -> staging/shadow session
  -> acceptance evidence
  -> make version active
```

## Credentials

Never commit API keys or provider session credentials. Runtime credentials belong in approved secret storage/environment configuration.

## Cost policy

Initial recommended split:

- Codex/ChatGPT subscription workflows: heavy engineering implementation where practical;
- Agents API: supervisor/routing, durable service integration, scheduled/API-driven work, and bounded specialist execution when API autonomy is useful;
- lower-cost validation role: deterministic exhaustive proof where model capability permits.

## Runtime state rule

GitHub documentation and repository evidence remain the source of program truth. A provider session may retain conversational execution context, but it must not become the only place where milestone state, architecture decisions, or exact continuation points exist.

## Initial runtime agents

When publication is authorized, publish in this order:

1. Daily Line Supervisor — read-first, no mutation tools;
2. QA/Audit — read-only evidence review;
3. Documentation — scoped Git/document writes;
4. Engineering — scoped repository write tools;
5. Modeling — scoped model/research tools;
6. Validation/CI — CI/log/status tools.

Only after read-first behavior is proven should any agent receive tools that can create state-changing production ActionRequests.