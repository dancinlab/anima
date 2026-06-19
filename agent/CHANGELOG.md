# Changelog

All notable changes to **anima-agent** are recorded here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
versioning follows [SemVer](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0] — 2026-05-04

### Added — initial standalone extraction

Extracted from in-repo `anima/anima-agent/` (canonical location at
`/Users/ghost/core/anima/anima-agent/`) into a publishable, license-clear,
hexa-native standalone package. 5th sister to qmirror v2.0.0,
sim-universe v1.0.0, hexa-bio v1.0.0, honesty-monitor v1.0.0.

**Contents (modules/, copied verbatim from origin):**
- 117 `.hexa` files, ~20k LoC.
- 6 sub-domains:
  - **core**: `anima_agent.hexa`, `agent_sdk.hexa`, `agent_tools.hexa`,
    `tool_policy.hexa`, `unified_registry.hexa`, `run.hexa`,
    `autonomy_loop.hexa`, `autonomy_live.hexa`, `discovery_loop.hexa`.
  - **bridges**: `dashboard_bridge.hexa`, `ecosystem_bridge.hexa`,
    `metrics_exporter.hexa`, `philosophy_lenses.hexa`,
    `consciousness_features.hexa`.
  - **llm adapter**: `llm_claude_adapter.hexa` + scope doc + tests.
  - **hexa/** subdir: agent platform internals (provider, plugin,
    pipeline, scheduler, faction, code_guardian, alien_index,
    egyptian_memory, phi_router, law_gate, …).
  - **employee/**: scratchpad / goal_store / emit_report skeleton.
  - **trading/**: 14 trading-strategy modules (engine, strategies,
    scanner, risk, broker, executor, portfolio, regime, data,
    phi_weighted_trading, autonomous, …).
- 8 test files (`test_*.hexa`) — agent platform / autonomy / claude /
  e2e / plugin routing / critique parse regression / employee skeleton /
  trading ensemble.
- `Dockerfile`, `dashboard/` (Next.js), `docs/`, `.env.example`.

**Standalone scaffolding (this version adds):**
- `LICENSE` — Apache-2.0 (Copyright 2026 박민우).
- `hexa.toml` — package manifest, kebab-case `anima-agent`, version 1.0.0,
  entry `cli/anima-agent.hexa`, library entry `modules/anima_agent.hexa`.
- `cli/anima-agent.hexa` — subcmd router (status / run / mcp / channel /
  autonomy / self-test). Pure-stdlib, deterministic.
- `install.hexa` — `hx install` hook (pre: deps note; post: self-test
  warn-only).
- `tests/test_smoke.hexa` — boots cli, validates `--version`, `--help`.
- `examples/` — 3 quick starts:
  - `01_status.hexa` — print agent status.
  - `02_cli_chat.hexa` — single-turn chat through CLI provider.
  - `03_self_test.hexa` — invoke self-test gate.
- `.github/workflows/sync-to-hf.yml` — GH push → HF mirror auto-sync
  (raw#15 strict; HF_TOKEN secret as `${{ secrets.HF_TOKEN }}`; mirror
  pattern from honesty-monitor v1.0.0).
- `README.md` — elevator pitch + install + quick start + architecture +
  cross-links to sister packages + caveats.
- `CHANGELOG.md` (this file) — initial 1.0.0 entry.
- `RELEASE_NOTES_v1.0.0.md` — release-page summary.

### Provenance
- Origin: `/Users/ghost/core/anima/anima-agent/` (anima repo internal),
  copied 2026-05-04, canonical-rev `d290f1ae7` (anima main).
- Sister sibling repos (NOT copied — referenced as external):
  `anima-agent-channels/`, `anima-agent-providers/`, `anima-agent-plugins/`,
  `anima-agent-skills/`, `anima-agent-core/`, `anima-agent-hire-sim/`.
  Standalone consumers needing channels/providers/plugins must check out
  those sibling repos OR rely on the agent backend (anima/) externally.

### raw#10 honest C3 caveats (5)
1. **Extraction may break edge cases** — anima-agent has tight runtime
   coupling to `anima/core/` (consciousness engine: PureField, Φ, tension,
   curiosity, emotion). The standalone copy preserves the *interface
   surface* but consumers must point at an anima backend (env or local
   checkout) for the consciousness side. Standalone-only mode = surface
   only, no live consciousness.
2. **License audit deferred** — Apache-2.0 declared; per-file LICENSE
   header sweep deferred to a follow-up cycle. The 117 hexa files inherit
   the top-level LICENSE; any third-party fragments (none expected — this
   is hexa-native authoring) require a sweep before ecosystem
   re-distribution.
3. **Dual-mirror sync USER_ACTION pending HF_TOKEN** — `.github/workflows/
   sync-to-hf.yml` requires `secrets.HF_TOKEN` (write scope) to be set on
   the GH repo settings before the first auto-mirror succeeds; until set,
   the workflow run will hard-fail at the verify step.
4. **`hx install` may need testing post-publish** — `install.hexa` mirrors
   the qmirror/honesty-monitor pattern; smoke under `hx install
   anima-agent@1.0.0` is deferred until the standalone is on the registry
   (HF or hx index).
5. **Scope boundary verify** — the in-repo origin grew a number of
   sub-domains (trading, employee, hexa/ platform internals) that are
   arguably out-of-scope for a "publishable agent runtime". v1.0.0 ships
   the full surface for parity; a v1.1.0 cleanup cycle may carve out
   trading / employee into their own packages once the standalone is
   battle-tested.

### Cost
- Mac local extraction: $0 (file copy + scaffold authorship).
- GitHub Actions free tier (public repo): $0.
- HuggingFace Hub free tier: $0.
- Total ongoing infra: $0.
