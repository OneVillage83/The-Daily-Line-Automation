---
name: daily-line-repo-audit
description: Reconcile the real current engineering state of a Daily Line repository from Git, local instructions, status documents, PR/CI evidence, and exact continuation points.
---

# Daily Line Repository Audit

## Required output

Return:

- repository;
- default branch and exact HEAD;
- governing instruction files;
- current frozen/certified milestone;
- current draft/active milestone;
- exact next authorized task;
- blockers;
- relevant PRs/branches;
- validation/owner gates;
- cross-repo dependencies;
- stale DLADS state detected;
- recommended program-state patch.

## Process

1. Never start from chat memory alone.
2. Read local `AGENTS.md`/override hierarchy.
3. Locate repo-defined `CODEX_START_HERE`, resume, implementation status, certification log, roadmap, and newest dated handoffs/receipts.
4. Check current Git/PR evidence where needed to distinguish historical text from current authority.
5. Prefer the newest authoritative exact-source statement, not the newest filename blindly.
6. Mark uncertainty `UNKNOWN` rather than inferring.
7. Do not edit implementation during an audit unless the user explicitly broadened scope.

## Final check

The result must be sufficient for a different agent to enter the repo at the correct SHA/branch and start the next authorized task without prior conversation context.