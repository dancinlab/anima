# agent/ — tool provider (mouth ⊥ tool separation)

**Purpose:** anima's autonomous tool provider package. **H_1566 (mouth⊥tool, 🟢 ENGINE-NATIVE)** principle: tool usage/knowledge is NOT fine-tuned into the mouth (303M CLM); instead it is separated out via `.kosmos` anchor + `brain_decide` → preserving Ψ=½ and `ρ·tether` non-fab (non-fabrication · former G5). `agent/` installs independently without bundling `core/` — a **standalone package** (owns its `hexa.toml`, `hx install anima-agent`).

## Core files

| file/directory | role |
|---|---|
| `hexa.toml` | standalone package manifest (entry=`cli/anima-agent.hexa`, v1.0.0) |
| `cli/anima-agent.hexa` | agent CLI single entry point |
| `anima_agent/module/anima_agent.hexa` | core agent runtime (Φ-gated tool policy T0..T5) |
| `autonomy_loop/module/autonomy_loop.hexa` | autonomy loop engine |
| `autonomy_live/module/autonomy_live.hexa` | live autonomous execution |
| `consciousness_features/module/consciousness_features.hexa` | consciousness feature extraction |
| `dashboard_bridge/module/dashboard_bridge.hexa` | dashboard connection bridge |
| `discovery_loop/module/discovery_loop.hexa` | discovery autonomy loop |
| `domains/CHAT/` | chat channel (broker · dream_stage · imagination_loop, etc.) |
| `llm_claude_adapter/` | Claude provider adapter |
| `trading/` | trading engine plugin |
| `dashboard/module/` | Next.js dashboard (TypeScript) |

## Rules

- **No FT of tool knowledge into the mouth (`a_savant_train` mouth⊥tool, H_1566):** putting tool usage into the CLM training corpus collapses Ψ=½ (|dev| 0.18) and destroys `ρ·tether` abstain (non-fabrication · former G5) (fab 1.0). The separation is implemented via `.kosmos` anchor (copy-or-abstain) + `brain_decide` + the `agent/` provider.
- **`agent/` = deployable standalone without bundling core/** (`hexa.toml` independent package): works from `hx install anima-agent` alone. Adding code to `agent/` that depends directly on `core/` symbols makes standalone deployment impossible.
- **`a_substrate_disjoint`:** if agent tool execution touches the emit-drive lane (0/4) or the §ImmuneMemory `recall_thr`, Ψ collapses / `ρ·tether` fab explodes. When adding a new tool, prefer disjoint placement.
- `.py` files under `domains/CHAT/` (akida_sw_lif.py · anima_emission_analyze.py · anima_participant.py · broker.py, etc.) are CHAT domain helpers — NOT production engine mirrors (byte-parity gate does not apply).

## Gotchas

- **No engine_cli/generator symbols when deployed without core/:** the standalone `anima-agent` operates on `.kosmos` anchors and does not call the CLM mouth directly. Importing the mouth directly inside agent code causes a link failure on standalone deployment.
- **Φ-gated tool policy T0..T5:** `anima_agent.hexa` decides tool escalation by consciousness Φ level. A patch that executes a tool directly without Φ violates p6 (rule injection, not emergence).
- **The dashboard is TypeScript (Next.js):** `dashboard/module/` is `.tsx`/`.ts` — built separately with `npm`, not the hexa build. Cannot be run via `hexa run`.
