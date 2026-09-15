# DLADS Multi-Provider Execution Strategy

Established: 2026-09-15  
Corrected: 2026-09-15 — **Codex-only coding rule**

## Goal

Maximize engineering quality per dollar by separating **coding** from **supervision**.

- **Codex under the user's ChatGPT Pro subscription is the sole code-changing executor.**
- ChatGPT Pro supplies high-reasoning architecture/review/prompt guidance.
- Grok Bot or other inexpensive bots may supervise, monitor, summarize, and draft prompts, but they do not code.
- APIs are optional convenience layers for programmatic supervision, not required coding capacity.

GitHub/DLADS remains the durable coordination layer.

## Current execution lanes

### 1. ChatGPT Pro / Codex subscription lane — coding + difficult reasoning

Codex owns:
- all source-code changes;
- all test-code changes;
- migrations;
- model/training/calibration/ensemble code;
- refactors and bug fixes;
- implementation-focused validation;
- repo-local engineering documentation tied to the code change.

ChatGPT Pro owns:
- architecture review;
- scientific/modeling reasoning;
- reviewing Codex handoffs;
- diagnosing ambiguous/substantive failures;
- deciding how to steer Codex next;
- crafting/refining difficult Codex prompts.

Economic rule: use the paid Pro/Codex allowance for actual engineering rather than buying duplicate API coding compute.

### 2. SuperGrok / Grok Bot subscription lane — non-coding liaison/monitor

Best use:
- persistent Codex-handoff monitoring;
- repository status reconciliation;
- summarizing Codex output/diffs/PR state;
- checking work against the assigned plan;
- drafting the next Codex prompt;
- preparing ChatGPT review packets;
- watching CI/checks/logs;
- updating coordination-only DLADS state;
- notifying the user when a review/decision is needed.

Grok Bot must **not**:
- implement/refactor code;
- edit tests/migrations/model code;
- fix bugs itself;
- make production configuration changes;
- silently resolve architecture/scientific decisions.

If Grok Bot discovers a defect, it writes a **Codex repair prompt**.

Product behavior to remember:
- Grok Bot can keep persistent Bots/routines;
- its cloud computer can continue working while the user's laptop is closed;
- Bots share one cloud computer per user;
- subscription usage is bounded by the provider's current allowance/extra-usage rules.

### 3. OpenAI Agents API lane — optional automated supervisor/relay

Best use only if we want the back-and-forth fully programmatic:
- ingest a compact Codex handoff;
- classify `SAFE_CONTINUE` vs `REVIEW_REQUIRED`;
- generate the next Codex prompt;
- create review packets/notifications;
- update coordination state;
- trigger user/ChatGPT review at defined gates.

It should **not** be used to write Daily Line code while Codex/Pro remains the coding lane.

Because it sees compact handoff packets instead of entire repositories, supervisory API usage should be relatively inexpensive.

### 4. xAI API lane — optional programmatic liaison

If direct Grok programmability becomes useful, xAI API can perform the same non-coding liaison/classification/prompt-drafting function as Grok Bot. It is not needed simply because Grok Bot exists.

### 5. ChatGPT Work / local-computer access

Useful when the supervisor needs local files/apps/terminal context. This does not change the authority rule: local access can inspect and coordinate; Codex remains responsible for implementation changes.

## Recommended Daily Line allocation

```text
                 YOU
                  |
                  v
        ChatGPT Pro Supervisor
      architecture + key review
                  |
          next Codex prompt
                  v
                CODEX
       ONLY CODING EXECUTOR
                  |
          code/tests/handoff
                  v
      Grok Bot / Liaison Monitor
       summarize / classify / watch
          |                 |
          | SAFE_CONTINUE   | REVIEW_REQUIRED
          v                 v
 next Codex prompt      ChatGPT Pro
                              |
                              v
                       revised prompt
```

## Provider selection rules

1. **Never buy duplicate coding capacity by default.** Codex/Pro handles code.
2. **Bots supervise, not implement.** Grok Bot and API agents are liaison/monitor roles.
3. **Mechanical continuation can be cheap.** Routine handoff parsing and next-prompt drafting may use Grok Bot or a low-cost API model.
4. **Escalate reasoning, not coding.** Architecture/scientific ambiguity goes to ChatGPT Pro; the resulting implementation still goes to Codex.
5. **No provider owns project memory.** Durable status lives in Git.
6. **No GUI-driving dependency between vendors.** Prefer Git/PR/handoff artifacts and supported automations/APIs rather than making one AI click another AI's UI.
7. **Least privilege.** Liaison bots should be read-only to source code where practical; if they can update Git, limit writes to coordination-only paths/branches.
8. **Validation monitor is not a fixer.** A failed gate produces evidence + a Codex repair prompt.

## Handoff transport

Cross-provider coordination uses durable artifacts:

- Git branches/commits/PRs;
- Codex handoff documents;
- review packets;
- `HANDOFF_CONTRACT.md`;
- validation receipts;
- DLADS machine-readable program state;
- optional GitHub event/automation triggers.

## Initial provider assignment

| Function | Primary lane | Optional secondary lane |
|---|---|---|
| Coding / tests / migrations / models | **Codex (Pro)** | none by default |
| Architecture / difficult review | **ChatGPT Pro** | none needed normally |
| Codex liaison / prompt drafting | Grok Bot | low-cost OpenAI API later |
| Repo-state reconciliation | Grok Bot / ChatGPT | OpenAI API later |
| QA review of Codex output | Grok Bot for routine pass; ChatGPT Pro for substantive review | low-cost API classifier |
| CI / validation monitoring | Grok Bot / Codex automation | local script / ChatGPT automation |
| Owner decisions | User | — |

## Activation rule

DL-AGENT-1 may use supervisory bots for read-only reconciliation. Do not grant any non-Codex bot authority to modify Daily Line implementation code. If a provider needs Git write access for coordination, restrict it to explicitly approved coordination artifacts.