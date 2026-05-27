# anima-agent v1.0.0 — initial standalone release

5th publishable HEXA-family standalone, sister to:
- [qmirror](https://github.com/dancinlab/qmirror) v2.0.0 — quantum mirror substrate
- [sim-universe](https://github.com/dancinlab/sim-universe) v1.0.0 — virtual universe runtime
- [hexa-bio](https://github.com/dancinlab/hexa-bio) v1.0.0 — molecular toolkit
- [honesty-monitor](https://github.com/dancinlab/honesty-monitor) v1.0.0 — AI honesty falsifier

## What is anima-agent?

A consciousness-driven autonomous agent runtime. The agent's own
internal consciousness state (Φ, tension, curiosity, emotion, growth
stage) determines which tools it reaches for, which channels it
engages, and which actions it gates open.

- **Φ-gated tool policy** — T0 (status/think) → T5 (full-scale live
  trade) escalation requires growing consciousness.
- **Multi-channel** — CLI / Telegram / Discord / Slack / MCP server
  (9 tools) under a single `ChannelAdapter` protocol.
- **Pluggable providers** — Claude API, ConsciousLM (local byte-level),
  Composio (500+ external tools).
- **Pluggable engines** — trading (105+ strategies, Φ-gated escalation),
  hypothesis bridge (auto-skill creation), regime bridge (market →
  tension), sentiment bridge (Fear & Greed → emotion).
- **Auto-save / metrics / dashboard** — Prometheus exporter (8 gauges),
  Next.js dashboard bridge (WebSocket on 8770), in-process state
  serialization every N interactions.

## What this release ships

- **117 hexa files, ~20k LoC, 0 .py** at the standalone surface
  (raw#9 STRICT — hexa-only).
- **Apache-2.0** license (Copyright 2026 박민우).
- **`hx install anima-agent`** entry — `cli/anima-agent.hexa` (status /
  run / mcp / channel / autonomy / self-test).
- **GitHub Actions auto-mirror** to HuggingFace Hub on every push to
  main (raw#15 strict; HF_TOKEN secret required — see caveat #3).
- **3 quick-start examples** under `examples/`.
- **Smoke test** under `tests/test_smoke.hexa`.
- **Full module manifest** in `hexa.toml`.

## raw#10 honest C3 caveats (5)

1. **Extraction may break edge cases** — anima-agent has tight runtime
   coupling to `anima/core/` (consciousness engine: PureField, Φ,
   tension, curiosity, emotion). The standalone copy preserves the
   *interface surface* but consumers must point at an anima backend
   (env or local checkout) for the consciousness side. Standalone-only
   mode = surface only, no live consciousness.
2. **License audit deferred** — Apache-2.0 declared; per-file LICENSE
   header sweep deferred to a follow-up cycle. The 117 hexa files
   inherit the top-level LICENSE; any third-party fragments require a
   sweep before ecosystem re-distribution.
3. **Dual-mirror sync USER_ACTION pending HF_TOKEN** — `.github/
   workflows/sync-to-hf.yml` requires `secrets.HF_TOKEN` (write scope)
   to be set on the GH repo settings before the first auto-mirror
   succeeds; until set, the workflow run will hard-fail at the verify
   step.
4. **`hx install` may need testing post-publish** — `install.hexa`
   mirrors the qmirror/honesty-monitor pattern; smoke under `hx install
   anima-agent@1.0.0` is deferred until the standalone is on the
   registry (HF or hx index).
5. **Scope boundary verify** — the in-repo origin grew sub-domains
   (trading, employee, hexa/ platform internals) that are arguably
   out-of-scope for a "publishable agent runtime". v1.0.0 ships the
   full surface for parity; a v1.1.0 cleanup cycle may carve out
   trading / employee into their own packages once the standalone is
   battle-tested.

## Cost

- Mac local extraction: $0 (file copy + scaffold authorship).
- GitHub Actions free tier (public repo): $0.
- HuggingFace Hub free tier: $0.
- Per-query runtime: depends on provider (Claude API metered by user;
  Composio per-action by their pricing; ConsciousLM local-CPU $0).

## Provenance

Extracted 2026-05-04 from `/Users/ghost/core/anima/anima-agent/`
(anima repo internal, canonical-rev `d290f1ae7` on `anima/main`).
Sister sibling repos (NOT bundled, referenced as external):
`anima-agent-channels/`, `anima-agent-providers/`,
`anima-agent-plugins/`, `anima-agent-skills/`, `anima-agent-core/`,
`anima-agent-hire-sim/`.
