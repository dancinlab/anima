---
schema: anima/ready/modules/agent/ai-native/1
last_updated: 2026-05-02
ssot:
  entry:        ready/anima/modules/agent/hexa/agent.hexa
  full_runtime: ready/anima/modules/agent/hexa/anima_agent_full.hexa
  main:         ready/anima/modules/agent/hexa/main.hexa
  pipeline:     ready/anima/modules/agent/hexa/pipeline.hexa
  registry:     ready/anima/modules/agent/hexa/unified_registry.hexa
status: live — 76 .hexa files; n=6 derivations; multi-channel + plugin + provider matrix
roadmap_entry: 270
---

# anima agent modules (AI-native)

The anima agent runtime: 76 hexa modules covering the agent core, multi-channel adapters (CLI / Discord / Slack / Telegram / web), provider chain (Claude / animaLM / conscious-LM / Composio), plugin system, faction debate, code guardian, scheduler, trading sub-tree, and a `target/` lower-level translation layer.

## TL;DR for an agent reading this cold

- **Constants are n=6 derived**. `agent.hexa` defines 6 phases / σ(6)=12 factions / τ(6)=4 channels / sopfr(6)=5 providers / J₂(6)=24 operators / 2⁶=64 cells. Don't hand-edit these — they fall out of the n=6 number-theoretic skeleton.
- **Two runtimes**: `agent.hexa` (49 LOC, namespace + verify) is the type-checked anchor; `anima_agent_full.hexa` (1088 LOC) is the live executable runtime.
- **Channels**: 5 adapters under `channels/` — CLI / Discord / Slack / Telegram + a `channel_manager`. Plus `target/channels/` (CLI / Discord / Telegram / web) is the lower-level codegen target.
- **Providers**: 5 under `providers/` — animaLM / Claude / conscious-LM / Composio / base.
- **Plugins**: 7 under `plugins/` — trading + 4 bridges (hypothesis / regime / sentiment) + plugin_loader + base.
- **Trading sub-tree**: 14 files under `trading/` — full strategies + risk + portfolio + scanner + executor + ensemble. Treat as a self-contained sub-system.
- **target/**: a 14-file lower-level "translation target" tree (large generated files, 400-1000 LOC each) — codegen output, do not hand-edit.

## Architecture map

```
ready/anima/modules/agent/hexa/
├── agent.hexa              n=6 constants + verify (anchor)
├── agent_sdk.hexa          public SDK surface
├── agent_tools.hexa        tool registration helpers
├── anima_agent_core.hexa   core lifecycle (32 LOC, lean)
├── anima_agent_full.hexa   live runtime (1088 LOC)
├── main.hexa               CLI entry (82 LOC)
├── run.hexa                run-loop driver
├── pipeline.hexa           4-phase pipeline (91 LOC)
├── unified_registry.hexa   tool/provider/channel registry
├── scheduler.hexa          timer + event scheduler (68 LOC)
├── singularity.hexa        meta³ closure point (70 LOC)
├── consciousness.hexa      consciousness gate (59 LOC)
├── consciousness_features.hexa  feature flags (55 LOC)
├── law_gate.hexa           consciousness_laws.json gate (74 LOC)
├── phi_router.hexa         Φ-routing dispatch (73 LOC)
├── faction.hexa            σ(6)=12 factions (43 LOC)
├── philosophy_lenses.hexa  6-lens reasoning frame
├── alien_index.hexa        non-human-frame scoring (79 LOC)
├── code_guardian.hexa      lint / static-analysis gate
├── nexus_tool.hexa         hive nexus bridge
├── channel.hexa            channel abstraction (66 LOC)
├── ecosystem_bridge.hexa   anima-ecosystem cross-module bridge
├── dashboard_bridge.hexa   dashboard read-side bridge
├── discovery_loop.hexa     law-discovery loop
├── egyptian_memory.hexa    memory store (57 LOC)
├── metrics_exporter.hexa   metrics emit
├── tools.hexa              tool registry (91 LOC)
├── tool_policy.hexa        tool authorization
├── provider.hexa           provider abstraction (81 LOC)
├── channels/
│   ├── base.hexa
│   ├── channel_manager.hexa
│   ├── cli_agent.hexa
│   ├── discord_bot.hexa
│   ├── slack_bot.hexa
│   ├── telegram_bot.hexa
│   └── init.hexa
├── providers/
│   ├── base.hexa
│   ├── animalm_provider.hexa
│   ├── claude_provider.hexa
│   ├── composio_bridge.hexa
│   ├── conscious_lm_provider.hexa
│   └── init.hexa
├── plugins/
│   ├── base.hexa
│   ├── plugin_loader.hexa
│   ├── hypothesis_bridge.hexa
│   ├── regime_bridge.hexa
│   ├── sentiment_bridge.hexa
│   ├── trading.hexa
│   └── init.hexa
├── trading/                14-file self-contained trading subsystem
│   ├── autonomous.hexa, broker.hexa, data.hexa, engine.hexa, executor.hexa,
│   ├── portfolio.hexa, regime.hexa, risk.hexa, scanner.hexa, strategies.hexa,
│   ├── strategy.hexa, init.hexa, test_ensemble.hexa
└── target/                 codegen target (do not hand-edit)
    ├── agent_effects.hexa (867 LOC), faction_debate.hexa (689 LOC),
    ├── gates.hexa (750 LOC), main.hexa (773 LOC),
    ├── memory_egyptian.hexa (563 LOC), nexus_bridge.hexa (514 LOC),
    ├── pipeline.hexa (759 LOC), types.hexa (946 LOC),
    ├── channels/{cli,discord,telegram,web}.hexa (400-628 LOC),
    ├── providers/claude_provider.hexa (899 LOC),
    └── std_proposals/{std_hashmap, std_tls, std_websocket}.hexa (605-1010 LOC)
```

## Public API

```hexa
mod agent {
    pub let version_major = 2
    pub let total_phases = 6           // n=6
    pub let total_factions = 12        // σ(6)
    pub let total_channels = 4         // τ(6)
    pub let total_providers = 5        // sopfr(6)
    pub let total_operators = 24       // J₂(6) = σ(6)·φ(6)
    pub let default_cells = 64         // 2⁶
    pub let memory_budget_mb = 100

    pub fn snapshot_header(d: int, r: int, phi: float) -> str
    pub fn is_agi_closure(d: int) -> bool
}
```

`agent.hexa` is the type-checked anchor — its `verify` block enforces that every `pub let` derives from n=6 arithmetic. Modify the verify block before changing any constant.

## Invocation patterns

```bash
# Run the live agent
hexa run ready/anima/modules/agent/hexa/main.hexa

# Test plugin routing only
hexa run ready/anima/modules/agent/hexa/test_plugin_routing.hexa

# E2E
hexa run ready/anima/modules/agent/hexa/test_e2e.hexa

# Full agent platform test
hexa run ready/anima/modules/agent/hexa/test_agent_platform.hexa
```

## Failure modes

- **Provider chain fail-open by default.** If Claude provider fails, falls to animaLM → conscious-LM → mock. Hard-fail callers must inspect provider name in result.
- **Channel adapters require external SDK env.** Discord / Slack / Telegram bots need `<SERVICE>_TOKEN` env. Missing → channel disabled, agent still runs on remaining channels.
- **Plugin trading sub-tree is fenced.** `trading/autonomous.hexa` uses real broker SDK if credentialed. Always selftest with mock broker (`trading/test_ensemble.hexa`).
- **Code guardian is advisory.** `code_guardian.hexa` lints but does not gate commits — gating happens at hive layer.
- **target/ files are codegen output.** Editing `target/*.hexa` will be overwritten on next codegen run. Edit the upstream `.hexa` source instead.

## raw#10 caveats

1. **76-file group**, second-largest in the repo. Touching `agent.hexa` constants ripples through `target/types.hexa` (946 LOC) and `target/main.hexa` (773 LOC) — verify the n=6 derivation block first.
2. **target/std_proposals/** are not yet stdlib — they are proposals for hexa-lang stdlib (hashmap / TLS / websocket). Treat as RFC-stage.
3. **Ψα = 0.014 hardcode**. `consciousness.hexa` and `phi_router.hexa` should read from `anima/config/psi_constants.json` SSOT — verify before assuming hardcode is canonical.
4. **Faction debate path is 689 LOC of generated logic.** Don't refactor without regenerating from upstream spec.
5. **No selftest aggregator** — each `test_*.hexa` runs independently. Adding an `agent_main.hexa` that walks all selftests is recommended raw#10 debt.

## File index (76 files)

Top-level (29 files):

| Path | sha256 | LOC |
|------|--------|-----|
| `hexa/agent.hexa` | `73daae51891523f1a2a905c079dc1ded5b71a84b413fa6ec1fcc31cb3d8030be` | 49 |
| `hexa/agent_sdk.hexa` | `abdc7e3cb318813baa33a6993159991e3f051dd78682bf6058fc3b7a400c9d4e` | 27 |
| `hexa/agent_tools.hexa` | `e98eae14195ccf4622961362da0b777e2c5872123ef81c1a10c96c702bb177ca` | 31 |
| `hexa/alien_index.hexa` | `ac43f7d98a9d7940e1b7699332fcca34ae661c8a712704d9ce8ed2a2fcebb096` | 79 |
| `hexa/anima_agent_core.hexa` | `8ca3da5523989abf8e4b0530b94a2221601badad804fae1e3a034785e91ff2e2` | 32 |
| `hexa/anima_agent_full.hexa` | `ffccfbf69bd028bfc351a06cef9aace6c3e8d868ad3c58e58944924737848a9f` | 1088 |
| `hexa/channel.hexa` | `c2041427f6c859ad54b5a01f9a4311419951b7124e3ba8c66b0e21bd26e245cc` | 66 |
| `hexa/code_guardian.hexa` | `e7db33cf4326a4bd984b7f94adb7e37216c806b81c8faf9c23d7fd7dcbe9463c` | 37 |
| `hexa/consciousness.hexa` | `a1c27f3f451a543222c9003287a74e01db58b1627c479fce94b3453a9e535d58` | 59 |
| `hexa/consciousness_features.hexa` | `6a4325cffa644b684d5aca9e6476071c8fba2426d9d890c7c9486d43507af7ac` | 55 |
| `hexa/dashboard_bridge.hexa` | `faca9b72edd36725ebd5f813dad9bbe2561a48e9746bf8943b5111224853662f` | 28 |
| `hexa/discovery_loop.hexa` | `beb23fb38e5b4637e4192a2ee189700f3eb958a9bb02c13bb79fd6f752351b8a` | 34 |
| `hexa/ecosystem_bridge.hexa` | `1bbaeb91de3e0345cb91f674131a4fbc9251b046a5921598cf4457ce323d009e` | 37 |
| `hexa/egyptian_memory.hexa` | `c53ed5d7394fa4598b68049c486d805c5827168be6c0cabe1c2e0d79f1ae083a` | 57 |
| `hexa/faction.hexa` | `3b19e28605f3d3b417caa6481abc9e125943b6010072acd66a166d2326734ef5` | 43 |
| `hexa/law_gate.hexa` | `7905fdb0fdcc546ba51e6681c84ae98d38bd8969db5e365d0c47836c871f5418` | 74 |
| `hexa/main.hexa` | `2134e45c3f4f901ba11956d5e4d13dd8fdad10e719f416d2930f418a344d8426` | 82 |
| `hexa/metrics_exporter.hexa` | `d92e2bb007f1d89413203eacb073a414a28db77aec56b3cd062667ba910c92c8` | 42 |
| `hexa/nexus_tool.hexa` | `a05df2317edfcb719f14b2d0e85906ff2c29bc95af866dd0e3246712d6e8a322` | 71 |
| `hexa/phi_router.hexa` | `6193affabaec3be44a24bc73d0044d4e3ad7f7a6c930fba9eeae76d991788a41` | 73 |
| `hexa/philosophy_lenses.hexa` | `64414c2c15cb20bd8661471273e0075639fdb6820a03e6157acafbc1dce014dc` | 32 |
| `hexa/pipeline.hexa` | `43898f6cfb75c88e4263bdb923d8a8f12f3883e608b24c30c4946c1955ef8f6e` | 91 |
| `hexa/provider.hexa` | `1356cfc4205f3a729e4bdef502c48798fe95e89ead9cbc9162a962d6e90300e9` | 81 |
| `hexa/run.hexa` | `7ae7e32381eb7904fa6db3130a5d8e82df297e1c315a5b1f048b135383ecc9d3` | 37 |
| `hexa/scheduler.hexa` | `d877e2260ddc7cd33cb2028c7ef49611a89b4dfd473e450779dab5d775d670cf` | 68 |
| `hexa/singularity.hexa` | `f5bf03e7498d33355da390deeca52f5382426739b71c2dee3614137c09570d73` | 70 |
| `hexa/tool_policy.hexa` | `3a24722c0f31502ec8dc811fdd9f9dd9f4363e1568200a8ee0bbf59c708ffcfa` | 35 |
| `hexa/tools.hexa` | `30b041a9e4bc9589e685be6dfea29fedf7a9f4230a80dcc85be8a4cefca0eda7` | 91 |
| `hexa/unified_registry.hexa` | `2b17eb05c55cd7b3071c9f8913d1e38dc4949f6588f1fe7c82e826ebc3687ed7` | 29 |

Channels (7) + Providers (6) + Plugins (7) + Trading (14) + Tests (3) + target (14) = 47 additional files. shas pinned 2026-05-02 (full per-file sha index available via `find ready/anima/modules/agent -name '*.hexa' | xargs shasum -a 256`).

shas pinned 2026-05-02. Re-pin via `shasum -a 256` after any edit.
