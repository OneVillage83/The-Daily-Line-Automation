# DLADS Multi-Provider Execution Strategy

Established: 2026-09-15

## Goal

Maximize engineering quality per dollar by separating **project truth and workflow contracts** from the model/provider that performs a task.

DLADS is provider-neutral. GitHub remains the durable coordination layer; Codex, ChatGPT Work, Grok Bot, OpenAI Agents API, xAI API/Grok Build, and future providers are execution lanes.

## Current execution lanes

### 1. ChatGPT Pro / Codex subscription lane

Best use:
- high-reasoning architecture;
- difficult repository implementation/refactors;
- cross-repository contract work;
- scientific/modeling design;
- debugging substantive failures;
- owner-interactive development.

Economic rule: prefer subscription Codex/Work for heavy engineering while included plan usage is available before moving identical work to usage-billed APIs.

### 2. SuperGrok / Grok Bot subscription lane

Best use:
- persistent long-running worker tasks;
- repository audits/reconciliation;
- documentation/status synchronization;
- repetitive bounded implementation;
- browser/tool workflows;
- CI monitoring/evidence collection;
- independent second-pass QA;
- multiple parallel bots for independent scopes.

Important product behavior:
- SuperGrok includes Grok Bot access;
- Grok Bot receives included weekly usage, not unlimited usage;
- additional usage may be billed based on token cost;
- Bots share one persistent cloud computer per user, not one isolated machine per bot;
- the cloud computer can remain active while the user's laptop is closed.

Grok Bot should clone/use the same Git repositories and DLADS handoff contracts rather than become a separate hidden source of program state.

### 3. OpenAI Agents API lane

Best use:
- programmatic/scheduled/API-triggered supervisor work;
- structured multi-agent orchestration;
- product/service integration where a persistent API agent is needed;
- bounded specialists that must be invoked from One Village Command or another service.

Economic rule: Agents API has no separate platform fee; pay for chosen model tokens and tools. Use low-cost models for routing/reconciliation and escalate selectively.

### 4. xAI API / Grok Build lane

Best use:
- programmatic Grok execution when direct API integration is required;
- long-running code/agent tasks that benefit from xAI models;
- alternative provider/fallback evaluation.

This is separate from the SuperGrok/Grok Bot subscription and is usage-billed.

### 5. ChatGPT Work / local computer lane

Best use:
- local Windows files/apps/browser workflows;
- operations that require the user's local environment;
- tasks needing direct access to local repositories, terminal, app server, or desktop tools.

Prefer native desktop Work/Codex local access when available. A remote-desktop/plugin bridge may be used when remote chat access to a specific authorized machine is materially useful.

## Recommended Daily Line allocation

```text
Daily Line Supervisor
    |
    +-- architecture / hard reasoning ----------> Codex / ChatGPT Pro
    |
    +-- persistent cheap worker ----------------> Grok Bot
    |
    +-- independent QA --------------------------> Grok Bot or OpenAI low/mid-cost model
    |
    +-- deterministic validation / CI ----------> Grok Bot or low-cost validation lane
    |
    +-- scheduled/API service orchestration ----> OpenAI Agents API (when needed)
    |
    +-- alternative programmatic Grok ----------> xAI API (when needed)
```

## Provider selection rules

1. **Subscription-first for heavy interactive engineering.** Do not pay API rates for work already well served by included Codex/Grok Bot allowance.
2. **API only when programmability matters.** Use API agents for scheduled/service-driven workflows, not merely because an API exists.
3. **Use the lowest-cost capable model.** Routing, state reconciliation, formatting, and deterministic documentation do not normally need the flagship model.
4. **Escalate on evidence.** Move a task to a stronger model when it fails defined evals or encounters architecture/scientific ambiguity.
5. **Independent review can be cross-provider.** A patch written by Codex may be audited by Grok Bot, and vice versa.
6. **No provider owns project memory.** Durable status lives in Git.
7. **No GUI-driving dependency between agents.** Do not make the production workflow depend on ChatGPT clicking Grok Bot's UI or Grok Bot clicking ChatGPT. Use Git branches/PRs/issues/handoff files or supported APIs.
8. **Least privilege.** Grok Bot/cloud workers should use scoped GitHub access and work on branches/PRs rather than direct production/main mutation unless explicitly authorized.
9. **Shared cloud-computer awareness.** Multiple Grok Bots share one user cloud computer; avoid conflicting checkouts, ports, credentials, or working directories.

## Handoff transport

Until there is a supported direct Grok Bot orchestration API/ChatGPT plugin integration, cross-provider agents coordinate through durable artifacts:

- Git branches and commits;
- pull requests/issues;
- `HANDOFF_CONTRACT.md` records;
- validation receipts;
- DLADS machine-readable program state.

This is intentional: the coordination protocol remains stable even if model vendors change.

## Initial provider assignment by DLADS role

| Role | Primary initial lane | Secondary lane |
|---|---|---|
| Daily Line Supervisor | Codex / ChatGPT Pro | Grok Bot; OpenAI Agents API later |
| Engineering | Codex | Grok Bot / Grok Build |
| Modeling | Codex / high-reasoning OpenAI | Grok 4.6 as independent comparison |
| QA / Audit | Grok Bot | OpenAI Terra/Sol as needed |
| Documentation | Grok Bot | OpenAI Luna/Terra |
| Validation / CI | Grok Bot | OpenAI Luna/Terra or local automation |

## Activation rule

DL-AGENT-1 may use multiple providers for read-only reconciliation. Before any provider receives write access to private authoritative repositories, confirm its GitHub permissions, branch policy, secrets handling, and rollback path.