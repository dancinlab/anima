# TAPE-AUDIT — anima-agent

Consciousness-driven autonomous agent runtime, extracted from `anima/anima-agent/` 2026-05-04. Tool-tier-gated by agent's own Φ/tension/curiosity/emotion. A natural `.tape` consumer — the runtime literally produces typed agent-execution traces.

## A. Audit-class ledgers (cargo / migration candidates)

- **`state/markers/` (~17 `*.marker` files)** — `anima-agent_*`, `browser_harness_*`, `install_*`, `_argv_inspect_*`, several `_FAILED.marker`. Hexa hook artifacts; pure cargo. Direct `state/markers.tape` migration with grade=err for the `_FAILED` entries.
- No `*.jsonl` ledgers and no `*audit*/` dirs at the top level — the runtime currently does not emit a structured run trace. This is the biggest gap: a runtime whose entire purpose is gated tool-use has no append-only trace today. `.tape` would land here as the missing run-history primitive.
- `state/` itself contains only `markers/`.

## B. Identity surface

Strong implicit identity (the agent runtime carries Φ / tension / curiosity / emotion / growth_stage state per the README table) but no on-disk identity manifest today. `anima-agent/identity.tape` would capture: provider config, consciousness signal baselines, tool-tier promotion history (T0→T5), employee/persona overlays from `employee/`.

## C. Domain.md files

Light. `AGENTS.md`, `CHANGELOG.md`, `README.md`, `RELEASE_NOTES_v1.0.0.md` only — no `UPPERCASE.md` per-subject convention. Domain split is by Python/hexa package (`anima_agent/`, `autonomy_live/`, `autonomy_loop/`, `consciousness_features/`, `philosophy_lenses/`, `trading/`, ...). Each package could grow a sibling tape (`autonomy_loop.tape` per-cycle, `trading.tape` per-trade).

## D. Per-run / per-event history surfaces

The runtime is essentially per-event: every channel (CLI / Telegram / Discord / Slack / MCP) is a stream, every autonomy-loop tick a `@T` event, every tool gate a `@D` decision, every actual tool call a `@A`. The 18+ `test_*` dirs (test_e2e, test_autonomy_loop, test_claude_*, test_agent_platform, etc.) imply per-test trace logs that could become tapes. `examples/` runs too.

## E. Promotion candidates

- **n6 atoms** — Φ formula, tension/curiosity/emotion gating laws (T0..T5 unlock conditions), growth_stage formulas. Each → n6 atom in atlas.
- **hxc wire** — `dashboard_bridge/` + `ecosystem_bridge/` + `metrics_exporter/` could emit hxc.
- **n12 cells** — Φ time-series, tool-tier histogram, sentiment time-series → n12 cube cells per channel × time.

**Verdict: MEDIUM** (3-4 tape surfaces — markers, runtime trace gap, identity manifest, per-channel per-tick events; no current jsonl ledgers).
