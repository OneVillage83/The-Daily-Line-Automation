# Daily Line Agent Definitions

These directories contain version-controlled **non-coding supervisory** DLADS role definitions. They are internal manifests, not provider-native API objects.

## Non-negotiable rule

**Codex is the sole code-changing executor.**

DLADS agents may read repositories, inspect Codex output, summarize, monitor, review, update coordination-only records, and draft the next Codex prompt. They may not modify source code, tests, migrations, model code, or production configuration.

Each agent has:

- `agent.json` — identity, authority, capabilities, eval gates, future runtime mapping;
- `instructions.md` — durable role instructions.

Current roles:

- `daily-line-supervisor` — chooses/steers the next Codex task;
- `codex-liaison` — monitors Codex handoffs and drafts next prompts;
- `engineering` — engineering review/prompt specialist, not an implementer;
- `modeling` — scientific/modeling review specialist, not an implementer;
- `qa-audit` — independent read-only audit of Codex output;
- `documentation` — coordination-state/documentation role;
- `validation-ci` — validation/CI monitor, not a fixer.

All runtime manifests begin `not_published`. Publishing an agent requires the gate in `docs/GrokBot OpenAI Bridge/EVALUATION_GATES.md` and the relevant runtime adapter process.
