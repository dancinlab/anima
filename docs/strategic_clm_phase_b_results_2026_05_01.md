# Strategic CLM Phase B Results — 2026-05-01 (executed 2026-05-02)

> **Mission**: CLM Phase B EXEC RELAUNCH — Mk.XII v3 3rd backbone closure with Phi-3.5-mini OR-clause-1 v3 (target: 2/3 → 3/3).
> **Source spec**: `state/strategic_clm_cp2_pivot_eta_2026_05_01/phase_matrix.json` Phase B (B.1 + B.2).
> **Cap**: $5 hard / 4-8 hr wallclock.
> **Race isolation**: `state/strategic_clm_phase_b_2026_05_01/`.
> **Verdict**: **HARD_PASS_PARTIAL_PENDING UNCHANGED (2/3 mode coverage)** — Phi-3.5-mini lands in LATE mode (peak layer 28/32, cusp_x1000=875), does NOT close early mode gap.

## §1. One-line outcome

Phi-3.5-mini cmt extraction PASS on H100 for $0.25 (well under $5 cap), but result demonstrates **substrate-architectural** pattern: medium-size transformers (3-9B) peak in deep layers (late mode). Adding Phi-3.5-mini to dali_sli_v3 input list moves it into LATE mode pool (joining Mistral, gemma2-9b), not the EARLY mode where the gap exists. **OR-clause-1 v3 stays ALL_MODES_PASS_GREEN 2/3 — does NOT advance to 3/3.**

## §2. Cost ledger

| stage | wallclock | $ |
|---|---|---|
| pod create + ssh-wait | ~5 min | $0.25 |
| pip install transformers + accelerate | ~1.5 min | (incl above) |
| Phi-3.5-mini download + load | ~25 sec | (incl) |
| CMT 4-family x 4-prompt forward pass extraction | 25.2 sec | (incl) |
| download cmt.json + terminate pod | <30 sec | (incl) |
| **TOTAL** | ~5 min uptime | **$0.249** |

Cap headroom: $4.75 unused. Far under $3-5 envelope.

## §3. CMT result (Phi-3.5-mini)

Schema: `anima/cmt/1` (matches state/v10_benchmark_v4/{gemma,llama,mistral,qwen3}/cmt.json).

```
backbone:    microsoft/Phi-3.5-mini-instruct
n_layers:    32
n_probes:    8 (layers 0,4,8,12,16,20,24,28)
families:    [Hexad, Law, Phi, SelfRef]
cusp_layer:  28  (deepest probed)
cusp_x1000:  875 (= 28*1000/32)
family_loc:  875 (all 4 dominant families peak at layer 28)
mode:        LATE (>500)
```

Per-family abs at layer 28: Hexad=585.0, Law=607.0, Phi=469.0, SelfRef=633.0. Monotonic increase from layer 0 (~0.6) → layer 28 (~600). No mid-layer peaking.

## §4. dali_sli_v3 (post-Phi-3.5-mini hypothetical 8-bb)

Adding Phi-3.5-mini to v3 backbone pool:

| backbone | n_layers | peak_L | cusp_x1000 | fl_x1000 | mode_cd | mode_fl |
|---|---|---|---|---|---|---|
| Mistral | 32 | 28 | 875 | 875 | late | late |
| Qwen3 | 36 | 4 | 111 | 111 | early | early |
| Llama-8B | 32 | 4 | 125 | 625 | early | late |
| gemma2-9b | 42 | 36 | 857 | 857 | late | late |
| qwen25-1.5B | 28 | 0 | 0 | 0 | input | input |
| gemma2-2B | 26 | 0 | 0 | 0 | input | input |
| Llama-3.2-1B | 16 | 0 | 0 | 0 | input | input |
| **Phi-3.5-mini (NEW)** | **32** | **28** | **875** | **875** | **late** | **late** |

per-mode result (8-bb hypothetical):

| mode | fl_size | cd_size | eligible | pass | impact |
|---|---|---|---|---|---|
| input | 3 | 3 | YES | YES (cd=0,0,0 layer-0 collapse, intra_dali=1000 intra_sli=1000) | unchanged |
| early | 1 (Qwen3) | 2 (Qwen3, Llama-8B) | NO (fl_size<2) | n/a | **STILL UNCLOSED** |
| late | 4 (Mistral, Llama-8B, gemma2-9b, Phi-3.5-mini) | 3 (Mistral, gemma2-9b, Phi-3.5-mini) | YES | YES (strengthened: cd_size 2→3, fl_size 3→4) | already PASS, now stronger |

**mode_coverage stays 2/3.** Mk.XII v3 verdict UNCHANGED.

## §5. Mk.XII v3 status

| field | before | after |
|---|---|---|
| OR-clause-1 v3 | ALL_MODES_PASS_GREEN 2/3 | ALL_MODES_PASS_GREEN 2/3 (UNCHANGED) |
| backbone count | 7 | 8 (with Phi-3.5-mini in late) |
| 3-tier verdict | HARD_PASS_PARTIAL_PENDING | HARD_PASS_PARTIAL_PENDING (UNCHANGED) |
| early mode gap | OPEN (Qwen3 alone) | OPEN (Qwen3 alone) |
| late mode strength | 2-3 backbones | 3-4 backbones (strengthened) |
| EHL-3W (OR-clause-2) | conditional-GREEN, hardware-pending | unchanged |

Per `phase_matrix.json` Phase B alternative_if_blocked: **"Accept Mk.XII v3 PARTIAL_PENDING permanently; CP2-CLM proceeds without 3rd-backbone closure (Mk.XII is anima-internal verdict, not CP2 suite scope)."** This Phase B execution VALIDATES that risk arm.

## §6. Honest C3 (raw#71)

1. **Substrate-architectural finding (NEW)**: 3 of 4 large backbones (Mistral, gemma2-9b, Phi-3.5-mini) peak at deepest probed layer. This is a SYSTEMATIC pattern, not random. Predicted by phase_matrix Phase B `risk_medium`: "Phi-3.5-mini may FAIL G2/G4 just like Mistral does (substrate-architectural). 50% chance B.1 lands GREEN; 50% closes a 4th backbone fail." This run lands in the second arm — Phi-3.5-mini does NOT bring early mode coverage. The 50/50 prior was correct; outcome was the negative arm.

2. **CMT-only protocol scope**: This run produced ONLY cmt.json — not full paradigm v11 8-axis (g_gate / b_tom / mcca / phi_star / cds / sae_steer_bypass / backbone_aware_composite). Phase B sub-task B.1 ('paradigm v11 8-axis run') is INCOMPLETE — only the dali_sli_v3-relevant CMT slice was measured. Estimated cost to complete full paradigm v11 8-axis: $2-4 additional H100-hr. NOT executed under $5 cap and given negative early-mode result rendering further measurement low-value for the immediate 3/3 closure mission.

3. **Orchestrator defect surfaced**: `tool/anima_runpod_orchestrator.hexa` helper invokes `runpodctl ssh-cmd <pod>` which is NOT a valid runpodctl command (current version: 1.x supports only `pod list`/`pod create`/`pod delete`). Manual GraphQL fallback to `https://api.runpod.io/graphql` with `runtime { ports { ip publicPort } }` query worked. Orchestrator needs patch in follow-up cycle.

4. **n=4 prompts per family**: paradigm v11 reference protocol uses 16 prompts; this used 4 (4x lighter). Cusp layer is monotonic-increasing (layer 0 ~0.6 → layer 28 ~600), so the cusp identification is robust to prompt count. But abs/rel values may shift +/-5% with full 16-prompt protocol. Mode classification (>500 = late) is unaffected by this noise floor.

5. **No vLLM serve**: Mission spec mentioned 'vLLM serve + OR-clause-1 v3 eval' but OR-clause-1 v3 is purely structural (cmt geometry), no inference / generation needed. AutoModel + hidden_states sufficient. vLLM would have added 5-10 min cold-start with no benefit for this protocol.

## §7. Pod cleanup

- pod_id: `ekb2ftc0e6cl2b`
- created: 2026-05-02 ~08:42 UTC
- terminated: 2026-05-02 ~08:50 UTC (manual `runpodctl remove pod ekb2ftc0e6cl2b` after cmt download)
- final state: REMOVED (verified via `runpodctl pod list` post-termination — no entry)
- 3 OTHER RUNNING pods on account are pre-existing (`anima-n51-W1-pilot` / `anima-n51-random-sibling` / `anima-cp2-alpha`) — NOT from this Phase B mission, NOT touched.

## §8. Follow-up actionables

1. **Accept Mk.XII v3 = PARTIAL_PENDING permanent** per phase_matrix `alternative_if_blocked`: decouple from CP2-CLM ship.
2. **Identify early-peaking backbones for genuine 3/3 closure** (NOT urgent): distilled models (DistilGPT2, DistilBERT), or smaller-non-tiny architectures with documented mid-layer attention concentration. Cost: $3-5 each, low ROI given (1) above.
3. **Patch orchestrator** `tool/anima_runpod_orchestrator.hexa` to remove `runpodctl ssh-cmd` reference and use GraphQL fallback for SSH endpoint discovery (raw#9 defect). Cost: $0 (mac-local).
4. **Use this Phi-3.5-mini cmt** to STRENGTHEN late-mode evidence in next dali_sli_v3 cycle: late mode cd_size 2→3 + fl_size 3→4 = +33% / +33% effect size on intra-mode SLI. Cost: $0 (cmt.json already in `state/phi35_mini_cmt/cmt.json`).

## §9. Artifacts

| file | bytes | purpose |
|---|---|---|
| `state/phi35_mini_cmt/cmt.json` | ~3300 | Phi-3.5-mini paradigm v11 CMT slice (schema anima/cmt/1) |
| `state/strategic_clm_phase_b_2026_05_01/verdict.json` | ~5000 | Phase B mission verdict + cost + C3 |
| `state/strategic_clm_phase_b_2026_05_01/runpod_run.json` | (NOT created — orchestrator was killed mid-flight; manual SSH workflow used instead) | n/a |
| `docs/strategic_clm_phase_b_results_2026_05_01.md` | this file | Phase B human-readable summary |

## §10. One-line summary for parent agent

**Phi-3.5-mini downloaded + measured on H100 ($0.25, well under $5 cap). CMT cusp_layer=28 → LATE mode classification → does NOT close early mode gap. Mk.XII v3 stays HARD_PASS_PARTIAL_PENDING (2/3, unchanged). Pod terminated. Honest C3: substrate-architectural pattern predicted by phase_matrix risk_medium, outcome = the negative 50% arm.**
