# anima-agent standalone extraction — LANDED 2026-05-04

**Cycle**: `anima_agent_standalone_extraction_2026_05_04`
**Status**: LANDED (with USER_ACTION pending — HF mirror token)
**5th publishable HEXA-family standalone** (after qmirror v2.0.0, sim-universe v1.0.0,
hexa-bio v1.0.0, honesty-monitor v1.0.0).

## TL;DR

Extracted `/Users/ghost/core/anima/anima-agent/` (117 hexa, ~20k LoC, 0 .py)
to standalone repo `/Users/ghost/core/anima-agent/` with Apache-2.0 license,
hexa.toml manifest, CLI router, hx install hook, smoke test, 3 quick-start
examples, GitHub Actions HF auto-mirror, ~280 LoC qmirror-style README.

GitHub: <https://github.com/dancinlab/anima-agent> (public, commit `106f2b6`)
Release: <https://github.com/dancinlab/anima-agent/releases/tag/v1.0.0>
HF mirror: <https://huggingface.co/dancinlab/anima-agent> (PENDING HF_TOKEN)
Registry: `hexa-lang/tool/pkg/registry.tsv` L26 (`anima-agent 1.0.0`)

## Origin location ambiguity (resolved)

`find` returned 2 candidates:
- `/Users/ghost/core/anima/anima-agent` (33 entries, 117 hexa, full source) ← **CHOSEN**
- `/Users/ghost/core/anima/ready/anima-agent` (build artifacts only — `dashboard-api/target/`, `.pytest_cache/`, `data/`)

The `ready/` location is artifacts staging; canonical source is `anima/anima-agent`.

## What shipped

### Standalone scaffold (added on top of copied modules)

- `LICENSE` — Apache-2.0 (Copyright 2026 박민우)
- `.gitignore`, `CHANGELOG.md`, `RELEASE_NOTES_v1.0.0.md`
- `hexa.toml` — kebab-case `anima-agent`, version `1.0.0`, library entry `modules/anima_agent.hexa`, `[[bin]]` shim → `cli/anima-agent.hexa`
- `cli/anima-agent.hexa` — subcmd router (status / run / mcp / channel / autonomy / self-test / version / help). 4-tier root resolution mirrors qmirror.
- `install.hexa` — hx install hook (pre: no-op note; post: self-test warn-only)
- `tests/test_smoke.hexa` — boots cli, validates version + help + self-test
- `examples/01_status.hexa`, `examples/02_cli_chat.hexa`, `examples/03_self_test.hexa`
- `.github/workflows/sync-to-hf.yml` — GH push → HF mirror (raw#15 strict, HF_TOKEN secret)
- `README.md` — ~280 LoC, qmirror-style, badges + install + quick start + architecture + module map + sister cross-links + caveats

### Modules (copied verbatim)

117 `.hexa` files across:
- `modules/` (top-level): anima_agent, agent_sdk, agent_tools, tool_policy, unified_registry, run, autonomy_loop, autonomy_live, discovery_loop, dashboard_bridge, ecosystem_bridge, metrics_exporter, philosophy_lenses, consciousness_features, llm_claude_adapter (+ tests)
- `modules/hexa/` — platform internals (agent.hexa, channel.hexa, code_guardian, faction, phi_router, law_gate, provider, scheduler, singularity, plugins/*, target/*, …)
- `modules/employee/` — scratchpad, goal_store, emit_report
- `modules/trading/` — engine, strategies, scanner, risk, broker, executor, portfolio, regime, data, phi_weighted_trading, autonomous (+ ensemble test)
- `modules/dashboard/` — Next.js scaffold (mirrored as source, not built)

Stripped: `build/`, `results/`, `.hypothesis_bridge_state.json`, `__pycache__/`, `node_modules/`.

## Nexus refactor (STAGED — NOT committed)

Per task constraint "DO NOT auto-commit nexus deletes":

| # | File                              | Change                                                                                |
|---|-----------------------------------|---------------------------------------------------------------------------------------|
| 1 | `nexus/cli/agent.hexa`            | NEW — 237 LoC, 4-tier shellout router (mirrors `cli/honesty.hexa` pattern)            |
| 2 | `nexus/engine/nexus_cli.hexa`     | EDIT — add `AGENT_CLI` constant, `cmd_agent()` function, dispatch wire, help block    |
| 3 | `nexus/hexa.toml`                 | EDIT — add `[dependencies] anima-agent = "^1.0.0"` with provenance comment block      |
| 4 | `nexus/install.hexa`              | EDIT — add `ensure_runtime_dep("anima-agent", "^1.0.0")` + comment update             |

Review:
```bash
git -C /Users/ghost/core/nexus diff cli/agent.hexa engine/nexus_cli.hexa hexa.toml install.hexa
```

## raw#10 honest C3 caveats (5)

1. **Extraction may break edge cases** — anima-agent has tight runtime coupling to `anima/core/` (consciousness engine: PureField, Φ, tension, curiosity, emotion). The standalone copy preserves the *interface surface* but consumers must point at an anima backend (env or local checkout) for the consciousness side. Standalone-only mode = surface only, no live consciousness.
2. **License audit deferred** — Apache-2.0 declared at top level; per-file LICENSE header sweep deferred. Origin README badged MIT but the package was never license-audited end-to-end; v1.1.0 cycle should reconcile.
3. **Dual-mirror sync USER_ACTION pending HF_TOKEN** — `.github/workflows/sync-to-hf.yml` requires `secrets.HF_TOKEN` (write scope) on the GH repo settings before the first auto-mirror succeeds. Local `hf auth whoami` confirmed current token is invalid (401).
4. **`hx install` may need testing post-publish** — `install.hexa` mirrors the qmirror/honesty-monitor pattern; smoke under `hx install anima-agent@1.0.0` is deferred until the standalone is on the registry.
5. **Scope boundary verify** — the in-repo origin grew sub-domains (trading, employee, hexa/ platform internals) that are arguably out-of-scope for a "publishable agent runtime". v1.0.0 ships the full surface for parity; a v1.1.0 cleanup cycle may carve out trading / employee into their own packages.

## USER_ACTION pending

1. **GH repo secret HF_TOKEN** (write scope) — at <https://github.com/dancinlab/anima-agent/settings/secrets/actions>
2. **(Optional)** `hf auth login --force` then `hf repo create dancinlab/anima-agent --type model` (the workflow will idempotently create on first sync once token is set)
3. **Review staged nexus refactor** before commit (4 files in `/Users/ghost/core/nexus/`)
4. **Origin cleanup** (separate cycle, not this one) — add deprecation comment + cross-link in `anima/anima-agent/` after standalone smoke PASS

## Cost

$0 — Mac local + GH Actions free + HF free. Per-query runtime depends on provider (Claude API metered by user; Composio metered; ConsciousLM local-CPU $0).
