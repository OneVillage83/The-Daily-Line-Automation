# Daily Line Agent Definitions

These directories contain version-controlled DLADS role definitions. They are **internal manifests**, not provider-native API objects.

Each agent has:

- `agent.json` — identity, authority, capabilities, eval gates, future runtime mapping;
- `instructions.md` — durable role instructions.

Initial roles:

- `daily-line-supervisor`
- `engineering`
- `modeling`
- `qa-audit`
- `documentation`
- `validation-ci`

All runtime manifests begin `not_published`. Publishing an agent requires the gate in `docs/agent-system/EVALUATION_GATES.md` and the adapter process in `OPENAI_RUNTIME_ADAPTER.md`.