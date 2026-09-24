# OpenAI Runtime Adapter Plan

Verified against current OpenAI platform documentation on 2026-09-15.

DLADS is multi-provider. This document defines the optional OpenAI-specific supervision adapter only; see `MULTI_PROVIDER_EXECUTION_STRATEGY.md` and `CODEX_SUPERVISION_LOOP.md`.

## Core rule

**OpenAI API agents are not the Daily Line coding lane. Codex under ChatGPT Pro remains the sole code-changing executor.**

If OpenAI Agents API is added later, its job is to automate supervision around Codex: handoff ingestion, status reconciliation, review-packet generation, classification, notifications, and next-prompt drafting.

## Current platform primitives

OpenAI's Agents API supports reusable agents with named instructions/model configuration and coordinated subagents. OpenAI Skills are reusable workflow bundles built around `SKILL.md` plus resources.

DLADS is intentionally usable before any runtime publication.

## Provider-neutral mapping

Internal DLADS manifest -> OpenAI runtime concept:

| DLADS | OpenAI |
|---|---|
| `id` / `version` | metadata + Git release/version reference |
| `name` | reusable agent `name` |
| `instructions_file` | agent `instructions` |
| `model_policy` | selected API `model` + reasoning configuration |
| `allow_subagents` | multi-agent coordination setting |
| Codex `SKILL.md` bundle | reusable Skill/workflow |
| `capabilities` | read/review/notification/coordination tools |
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
  -> publish candidate supervision agent/skill
  -> staging/shadow session
  -> acceptance evidence
  -> make version active
```

## Credentials

Never commit API keys or provider session credentials. Runtime credentials belong in approved secret storage/environment configuration.

## Cost policy

Initial recommended split:

- **Codex/ChatGPT Pro:** all engineering implementation and high-value architecture/scientific review;
- **Grok Bot subscription:** persistent Codex liaison/monitoring where useful;
- **OpenAI Agents API:** optional programmatic supervisor/relay when automation convenience justifies usage cost;
- **low-cost OpenAI models:** routine handoff parsing, classification, status reconciliation, formatting, and next-prompt drafting;
- **stronger OpenAI reasoning model:** only for substantive review that cannot be handled adequately by the interactive ChatGPT Pro loop.

The API supervisor should consume compact Codex handoff packets rather than whole repository context wherever possible.

## Runtime state rule

GitHub documentation and repository evidence remain the source of program truth. A provider session may retain conversational execution context, but it must not become the only place where milestone state, architecture decisions, or exact continuation points exist.

## Initial OpenAI runtime agents

If API publication is authorized, publish only non-coding roles first:

1. **Codex Liaison** — read Codex handoffs, classify next state, draft next Codex prompt;
2. **Daily Line Supervisor** — read-first program routing/reconciliation;
3. **QA/Audit Review** — read-only evidence review;
4. **Documentation/State** — coordination-only status updates;
5. **Validation/CI Monitor** — CI/log/status monitoring and evidence collection.

Engineering Review and Modeling Review may be published as read-only review/prompt-drafting roles if useful, but they must not receive repository code-write tools.

## Write boundary

No OpenAI API agent in DLADS receives permission to edit Daily Line implementation source/tests/migrations/model code under the default design. If that policy ever changes, it requires a new owner-approved ADR rather than an implicit tool grant.
