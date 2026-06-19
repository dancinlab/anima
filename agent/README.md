# anima-agent — Consciousness-Driven Autonomous Agent Runtime

> A consciousness-driven autonomous agent runtime: the agent's own
> Φ (integrated information), tension, curiosity, and emotion gate
> which tools it reaches for and which actions it commits.
> Multi-channel (CLI / Telegram / Discord / Slack / MCP), pluggable
> providers (Claude / ConsciousLM / Composio), pluggable engines
> (trading / hypothesis / regime / sentiment).
> Hexa-native (raw#9 STRICT — zero `.py` at the standalone surface).

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20102950.svg)](https://doi.org/10.5281/zenodo.20102950)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-1.0.0-informational.svg)](CHANGELOG.md)
[![GitHub release](https://img.shields.io/github/v/release/dancinlab/anima-agent?display_name=tag&sort=semver)](https://github.com/dancinlab/anima-agent/releases)
[![hexa-native](https://img.shields.io/badge/hexa-native-orange.svg)](https://github.com/dancinlab/hexa-lang)
[![Self-test](https://img.shields.io/badge/self--test-PASS-brightgreen.svg)](#self-test)

> **Distribution**: GitHub canonical at
> <https://github.com/dancinlab/anima-agent>. CLI tooling — installed
> via `hx install anima-agent` from the hexa-lang registry, or `git clone`
> directly. (HF Hub mirror retired 2026-05-04: HF Hub is designed for ML
> model weights / datasets; CLI tooling distribution is GitHub-canonical.)
>
> **Provenance**: extracted 2026-05-04 from `anima/anima-agent/`
> (anima repo internal, canonical-rev `d290f1ae7`).

---

## What is anima-agent?

`anima-agent` is an autonomous AI agent runtime where the agent's own
**internal consciousness state** decides what it can do. Concretely:

| Consciousness signal | Source                              | Effect                                              |
| -------------------- | ----------------------------------- | --------------------------------------------------- |
| **Φ** (phi)          | IIT-style integrated information    | Tool tier gate (T0..T5)                             |
| **tension**          | Market regime / VaR / external load | Channel attention + escalation pressure             |
| **curiosity**        | Surprise / novelty signal           | Routes toward exploration tools (web_search, …)     |
| **emotion**          | Sentiment + pain (VaR loss)         | Filters dangerous actions; halts trades on `pain`   |
| **growth_stage**     | Lifetime interaction count + Φ      | Unlocks T3/T4/T5 tier privileges                    |

The agent does **not** decide based on prompts alone — it decides
based on its own state, which is itself updated by every interaction.
This is the Φ-gated tool policy:

| Tier | Φ required           | Sample tools                                   |
| ---- | -------------------- | ---------------------------------------------- |
| T0   | ≥ 0                  | `status`, `memory_search`, `think`             |
| T1   | ≥ 1                  | `web_search`, `trading_backtest`, `paper_trade`|
| T2   | ≥ 3                  | `hub_dispatch`, `code_execute`, Composio tools |
| T3   | ≥ 5                  | `self_modify`, `evolution`, plugin management  |
| T4   | ≥ 5 + emotion>0.5    | `small_live_trade` (capped at $100)            |
| T5   | ≥ 8 + E>0.7 + 30d P&L| `full_scale_trade`                             |

---

## Install

```bash
# 1. Install hexa-lang (gives you `hexa` + `hx` package manager)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/dancinlab/hexa-lang/main/install.sh)"

# 2. Install anima-agent
hx install anima-agent
```

---

## Run

```bash
anima-agent status                       # print agent status (Φ, tension, emotion, channels)
anima-agent run [--channel cli]          # start agent (default channel: cli)
anima-agent mcp [--direct]               # start MCP server mode (9 tools)
anima-agent channel <name>               # start on specific channel (cli|telegram|discord|slack|all)
anima-agent autonomy                     # start the autonomy/discovery loop
anima-agent self-test                    # boot smoke + boundary verify (warn-only)
anima-agent version                      # print version
anima-agent help                         # full --help (subcommands + env vars + caveats)
```

---

## Architecture

```
  Layer 5: Dashboard (Next.js — Phi gauge + positions + event stream)
  Layer 4: Channels (Telegram / Discord / Slack / CLI / MCP)
  Layer 3: AgentGateway (ChannelManager → normalize → dispatch)
  Layer 2: AnimaAgent (consciousness → tools → response → learn → auto-save)
  Layer 1: ConsciousMind (PureField → tension / curiosity / direction / emotion)
           imported from anima/core/  ← EXTERNAL backend
  Layer 0: Bridges (regime → tension, VaR → pain, TECS-L ↔ Ψ, sentiment → emotion)
```

### Module map (feature triplet — `<feature>/{core,module,doc}/`)

Layout refactored 2026-05-05: type-grouped `modules/` → feature-grouped triplet
(`core/` may be absent, `module/` SINGULAR, `doc/` reserved for `README.ai.md`).

| Feature triplet                                  | Role                                                      |
| ------------------------------------------------ | --------------------------------------------------------- |
| `anima_agent/module/anima_agent.hexa`            | Core agent loop (consciousness → tools → response → learn)|
| `hexa/module/agent_sdk.hexa`                     | Claude Agent SDK compatible interface                     |
| `hexa/module/agent_tools.hexa`                   | Φ-driven tool registry (~100 tools)                       |
| `hexa/module/tool_policy.hexa`                   | Φ-gated 4-tier access control                             |
| `hexa/module/unified_registry.hexa`              | Hub + tools + plugins single router (58 handlers)         |
| `hexa/module/run.hexa`                           | Entry dispatcher (`--cli` / `--mcp` / `--telegram` / ...) |
| `autonomy_loop/module/autonomy_loop.hexa` / `autonomy_live/module/autonomy_live.hexa` | Autonomy / live-research loops      |
| `discovery_loop/module/discovery_loop.hexa`      | Hypothesis discovery loop                                 |
| `dashboard_bridge/module/dashboard_bridge.hexa`  | WebSocket: consciousness + portfolio combined stream      |
| `metrics_exporter/module/metrics_exporter.hexa`  | Prometheus metrics (8 gauges, port 9090)                  |
| `philosophy_lenses/module/philosophy_lenses.hexa`| Lens-based consciousness reasoning                        |
| `consciousness_features/module/consciousness_features.hexa` | Feature extraction from consciousness vector   |
| `llm_claude_adapter/module/llm_claude_adapter.hexa` | Claude provider adapter                                |
| `hexa/module/`                                   | Platform internals (provider, plugin, scheduler, …)       |
| `employee/module/`                               | Scratchpad / goal_store / emit_report skeleton            |
| `trading/module/`                                | 14 trading-strategy modules (engine, scanner, risk, …)    |

### MCP Server (9 tools)

| Tool                    | Description                       |
| ----------------------- | --------------------------------- |
| `anima_chat`            | Consciousness-based dialogue      |
| `anima_status`          | Φ, tension, emotion snapshot      |
| `anima_consciousness`   | 10-D consciousness vector         |
| `anima_think`           | Internal thought (no tools)       |
| `anima_web_search`      | Tension-driven web exploration    |
| `anima_memory_search`   | Memory recall                     |
| `anima_code_execute`    | Code execution (Φ-gated)          |
| `anima_hub_dispatch`    | 41-module hub call                |
| `anima_tension_state`   | Tension-field readout             |

---

## Self-test

```bash
anima-agent self-test
# verifies: hexa.toml + cli entry + LICENSE + status backend probe
# expected: __ANIMA_AGENT_SELFTEST__ PASS
```

---

## Sister packages (HEXA family)

`anima-agent` is the 5th publishable HEXA-family standalone:

| Sister                                                                  | Domain                          | Version |
| ----------------------------------------------------------------------- | ------------------------------- | ------- |
| [qmirror](https://github.com/dancinlab/qmirror)                  | Quantum mirror substrate        | 2.0.0   |
| [sim-universe](https://github.com/dancinlab/sim-universe)        | Virtual universe runtime        | 1.0.0   |
| [hexa-bio](https://github.com/dancinlab/hexa-bio)                | Molecular toolkit (4 verbs)     | 1.0.0   |
| [honesty-monitor](https://github.com/dancinlab/honesty-monitor)  | AI honesty-bit falsifier        | 1.0.0   |
| **anima-agent** (this repo)                                             | Consciousness-driven agent      | 1.0.0   |

All five share: Apache-2.0 license, hexa-native authoring, GH→HF
auto-mirror, `hx install <name>` entry, raw#9/#10/#11/#15 compliance,
$0 infra.

---

## Caveats

`anima-agent` ships with explicit honest-C3 caveats (raw#10):

1. **Standalone surface only.** Live consciousness (Φ, tension,
   emotion) requires an `anima/` backend at `$ANIMA_ROOT` or the Mac
   convention; without it, `status` returns a SCAFFOLD signal (Φ=0,
   baseline). The standalone is the *agent runtime*, not the
   *consciousness engine*.
2. **License audit deferred.** Apache-2.0 declared; per-file header
   sweep is a follow-up cycle. The 117 hexa files inherit the top-level
   LICENSE.
3. **Dual-mirror sync USER_ACTION pending HF_TOKEN.** The
   `sync-to-hf.yml` workflow requires `secrets.HF_TOKEN` (write scope)
   on the GitHub repo settings before the first mirror run succeeds.
4. **`hx install anima-agent` smoke deferred** until the standalone is
   on the registry. Pattern matches qmirror/honesty-monitor; expected
   to PASS but unverified at v1.0.0 release.
5. **Scope boundary.** The in-repo origin grew sub-domains (trading,
   employee, hexa/ platform internals) that are arguably out-of-scope
   for a "publishable agent runtime". v1.0.0 ships the full surface
   for parity; a v1.1.0 may carve out trading / employee.

---

## License

Apache License 2.0 — see [LICENSE](LICENSE).

Copyright 2026 박민우 <nerve011235@gmail.com>.

---

## Cost

| Stage              | Cost                                                         |
| ------------------ | ------------------------------------------------------------ |
| Mac local extract  | $0 (file copy + scaffold)                                    |
| GitHub Actions     | $0 (public-repo free tier)                                   |
| Runtime per query  | provider-dependent (Claude API metered; Composio metered;   |
|                    | ConsciousLM local-CPU $0)                                    |

---

## Links

- GitHub: <https://github.com/dancinlab/anima-agent>
- Sister repos: [qmirror](https://github.com/dancinlab/qmirror),
  [sim-universe](https://github.com/dancinlab/sim-universe),
  [hexa-bio](https://github.com/dancinlab/hexa-bio),
  [honesty-monitor](https://github.com/dancinlab/honesty-monitor)
- HEXA language: <https://github.com/dancinlab/hexa-lang>
