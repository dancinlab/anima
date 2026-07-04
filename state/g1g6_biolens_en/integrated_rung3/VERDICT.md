# H_9129 INTEGRATED rung-3 — VERDICT: 🟡 DIRECTIONAL (wire LANDED · capability L5-carried, L1 INERT)

**사다리 (3)/4 — live `core/` wire + engine-native re-measure of the 3-component lane.**
Cost ≈ **$0** (mini CPU-local, `--py` canonical; no GPU pod, no rent). Base ckpt `~/anima-weights/bytegpt303_h1129/h1129.bin`.

## Wire LANDED (additive-only `core/`, byte-parity, disjoint, enforce CLEAN)
- **L1 PFC** `core/wm_bind_lane.py` (HRR bind/unbind/superpose/cleanup + `recon_fidelity` disjoint objective) + hexa twin `core/kosmos_io.hexa::wmbind_*`.
- **L2 basal-ganglia** `core/content_gate_lane.py` (`grounding_value`/`cgate_admit` Go/NoGo + RPE-EMA) + hexa twin `core/kosmos_io.hexa::cgate_*`.
- **L5 hippocampus** REUSED verbatim: `core/hippo_lane.py` + `core/kosmos_io.hexa::hippo_*` (already GREEN #2996).
- **Byte-parity hexa⟷py:** 5/5 keys MATCH on the deterministic fixture (`recon_fidelity=1.000000`, `unbind0_idx=0`, `unbind0_sim=0.432817`, `shuffle0_idx=1`, `n_admitted=3`) — the L1/L2 twins **build + run LIVE on mini** (kosmos_io.hexa is FFI-free), `integrated_hexa_smoke.hexa`.
- **Disjoint ON==OFF:** `git diff core/kosmos_io.hexa` = ADDITIVE-ONLY (151 insertions, 0 removed/changed; every emit-consumed fn byte-unchanged). New `.py` lanes imported by **NO** emit-path file (generator/brain/decode/engine_cli/pure_field/engine_g) → generation byte-identical lane-ON == lane-OFF **by construction** (nothing in the emit loop consults them; measurement-only). `enforce_anima_gates` = CLEAN.
- **LIVE-OP:** `integrated_measure.py` calls the live `core/wm_bind_lane` + `content_gate_lane` + `hippo_lane` ops on real 303M reps.

## Frozen-bar result (PREREG.md · verbatim from `result_integrated.txt`)
Real ByteGPT-303M h1129 reps via `core/decode.py` (== `anima evaluate --py` ops), 8 chains × len 6.

| arm | reach | unreach | gap | drop | causal (bar drop≥0.50) |
|---|---|---|---|---|---|
| **FULL (L1+L2+L5)** | 0.9881 | 0.5097 | **+0.4784** | — | gap>0.15 ✅ |
| lane-off (empty W) | 0.0000 | — | — | — | ✅ collapse |
| L5-OFF (single hop) | 0.0025 | 0.1397 | −0.1372 | +1.287 | ✅ **strongly causal** |
| L2-OFF (admit distractors) | 0.9884 | 0.7491 | +0.2394 | +0.500 | ⚠️ **borderline** (0.4996 < 0.50) |
| L1-OFF (no role-bind) | 0.4903 | 0.1759 | +0.3144 | +0.343 | ❌ **NOT causal** |
| RAW (no centering) | 0.9884 | 0.6566 | +0.3319 | +0.306 | ❌ centering NOT load-bearing |

Gate: `tp=55 fp=0 tn=25 fn=0` — L2 rejects every strength-0 distractor, but the corpus has cross-chain co-occurrences, so 15 genuinely-grounded cross-chain edges are admitted → unreach floor rises to 0.51 (grounding ≠ chain-membership).

## Why DIRECTIONAL (not GREEN) — honest, no tune-to-green
The pre-registered GREEN bar required **all 3 components CAUSAL + centering load-bearing**. Measured:
1. **L5 completion is the sole strong carrier** (single-hop → gap flips negative). It is already GREEN as a standalone faculty (#2996); the integrated gap is L5-driven.
2. **L2 content-gate is borderline** (~50% gap; rejects fabricated strength-0 distractors but not grounded cross-chain edges).
3. **L1 PFC HRR role-binding is INERT-to-HARMFUL** — it inflates BOTH reach and unreach via crosstalk (raises the unreach floor 0.18→0.51), i.e. it adds correlated noise, not clean variable-binding discrimination. This **concords the anima binding-INERT meta-law** (DPI; H_1816/1823/1834 readout/bind family): binding operators do not add compositional structure — the associative store does.
4. **Centering not load-bearing** in this config (raw gap 0.33) — HRR-bind + a dense store keep raw reps completable, contradicting rung-2's raw→0 claim for this wiring.

## Scope (a_scale_honest_scope · MANDATORY)
Even the L5-carried gap is an **explicit-store combo FACULTY over real 303M reps**, NOT a proof the 303M trunk composes. The HRR ALGEBRA and the corpus RELATION graph are injected. The **G1 trunk-recombination wall is UNTOUCHED**; the only arm that could move it is **γ trained-constructive-bind** (GPU, out of scope). This rung-3 additionally **retires the PFC-binding lever with engine-native evidence** (L1 INERT even wired disjoint over real reps), narrowing the frontier.

## Remaining wire (bounded follow-on · not a tier blocker)
`brain_emit`/`generator.hexa` actually consulting these lanes in the live chat loop needs a `generator.hexa` rebuild (`_hexa_ffi_dlopen` build wall on mini; doable on pool). That consult is READ-ONLY and cannot change emit (ON==OFF holds regardless). ARCHITECTURE.json lockstep = main-agent bookkeep.
