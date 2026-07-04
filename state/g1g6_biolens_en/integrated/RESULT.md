# H_9129 rung-2 — integrated PFC-BG-hippo lane on REAL 303M engine representations

**Ladder (a_verified_must_wire):** (1) STEP-0 DIRECTIONAL-mirror ✅ → **(2) 303M
engine-native re-verify ← THIS** → (3) live core/ wire → (4) ARCHITECTURE lockstep.

## What changed vs STEP-0 (the escalation)
STEP-0 (`state/g1_combolane_step0/integrated/combolane.py`) ran the 3-part lane
(PFC role↔filler bind → BG Go/NoGo gate → hippocampal pattern-completion → mouth
READOUT) on **ideal random hypervectors** (near-orthogonal, unit-norm — perfect
for HRR). This rung swaps the atomic FILLER symbols for **REAL h1129 303M engine
residual representations**, pulled from the actual forward pass using the EXACT
engine ops imported from `core/decode.py` (byte-parity with `cli/evaluate.hexa`).
Everything else (HRR bind/unbind/cleanup, gate, ablations, frozen bar) is
identical. Two arms: **A** = synthetic permutation topology; **B** = real corpus
co-occurrence topology (`core/testdata/clm_mid_5lang_c4.txt`+`flores`).

## Honest diagnostic — real 303M reps are NOT ideal (reps_diag.json)
| rep form | norm_ratio | offdiag \|cos\|_mean | cos_max |
|---|---|---|---|
| raw residual (mean-pool) | 1.0 | **1.000** | 1.000 |
| **centered** (mean-pool) | 1.8 | **0.170** | 0.908 |
| centered (last-token) | 3.1 | 0.182 | 0.944 |
| *(ideal random hypervector)* | *1.0* | *0.031* | *~0.1* |

Raw residuals are ~collinear (the residual-stream "rogue dimension" dominates);
mean-centering exposes the semantic structure but it is still ~5.5× more
correlated than ideal random, with heavy anisotropy (top-1 PC = 18% of variance).
Centering is pre-registered (extract_reps.py docstring) as the primary form.

## Arm A — synthetic topology (result_armA.json · 12 seeds · D=1024 · chance=0.042)
| codebook | reach | unreach | gap | fooled | shuffleΔ | bindΔ | gateΔ | compΔ |
|---|---|---|---|---|---|---|---|---|
| rand1024 (control) | 0.701 | 0.056 | +0.646 | False | 0.688 | 0.65 | 0.55 | 0.63 |
| **real_mean_c (primary)** | **0.424** | **0.021** | **+0.403** | **False** | **0.389** | 0.37 | 0.38 | 0.38 |
| real_last_c | 0.333 | 0.021 | +0.312 | False | 0.319 | 0.31 | 0.26 | 0.28 |
| real_mean_raw (no center) | 0.049 | 0.035 | +0.014 | **True** | 0.000 | 0.02 | 0.02 | 0.01 |

## Arm B — REAL corpus co-occurrence topology + real 303M reps (result_armB.json)
corpus-backed edges: a=96% · b=100% (mappings = argmax line co-occurrence).
```
reach=0.236  unreach=0.023  gap=+0.213  fooled=False
shuffle_reach=0.048  shuffleΔ=0.189  collapsed=True
bindoff Δ=0.190 CAUSAL · gateoff Δ=0.207 CAUSAL · compoff Δ=0.207 CAUSAL
```

## Verdict — DIRECTIONAL (mechanism SURVIVES real engine representations)
frozen bar (VERBATIM from STEP-0/task, no tune-to-green): reach>>unreach (gap>0.10,
not fooled) ∧ shuffle collapse (Δ>0.15) ∧ all-3 lane-OFF collapse (Δ>0.15).

- **real_mean_c (Arm A)** and **Arm B** both PASS every leg of the frozen bar:
  reach ≫ unreach (10× / 5.6× chance vs ~1× chance), shuffle collapses to chance,
  all three components (bind/gate/completion) causal, NOT fooled by surface form.
- **rand1024 control** isolates the cause of the degradation (0.70→0.42→0.24):
  real-vector non-orthogonality + hub structure, NOT a mechanism failure. This is
  the honest "not handed" signature — reach did NOT come out 1.0 exact (the
  by-construction advantage the frozen bar warned about is absent).
- **real_mean_raw** collapses (fooled, INERT ablations) → a real rung-3 constraint:
  a wired lane MUST remove the residual rogue dimension (center/whiten) before HRR.

**Why DIRECTIONAL not GREEN (a_engine_native_learning):** the SYMBOLS are engine-
native (real 303M forward), but this is NOT the `anima evaluate --py` decode-scoring
path and the lane is NOT wired into `core/` (that is rung-3). Per the strict gate,
a non-`evaluate --py`, non-wired lane caps at DIRECTIONAL. It is however a *strong
supportive* directional: the STEP-0 result is confirmed to be a property of the
mechanism, not of ideal toy vectors.

## binding-family (H_1816/1823 mouth-readout NOT-SUP) — 3 근거 preserved
1. **별개 lane**: composition happens in the PFC-bind / BG-gate / hippocampal
   relational memory M, not in the mouth; the mouth only cleanup-reads the lane state.
2. **disjoint objective**: recombination is never a mouth-target — the mouth names
   the surfaced size symbol; the 2-hop chain is a property of M + roles.
3. **mouth 읽기만**: completion-OFF gives the mouth the same raw vector and it still
   fails (Δ 0.38/0.21 CAUSAL) → recombination is the upstream 3-part product, not
   readout training. (H_1816/1823 forced recombination INTO the Broca readout →
   additive floor; here it lives in the relational substrate.)

## Cost / infra (honest)
$0 — all CPU-local (~30s total: 72+72 forward passes for rep extraction + numpy
lane). No GPU pod rented: rep extraction is 144 short single-forward passes, far
below any heavy-decode threshold — renting would be pure waste (a_wall_first does
not apply to a seconds-long CPU job). No pod → no teardown/PULL needed; artifacts
are the state/ files below.

## Artifacts (state/g1g6_biolens_en/integrated/)
`extract_reps.py` · `reps_h1129.npz` · `reps_diag.json` · `integrated_engine.py`
(Arm A) · `result_armA.json` · `arm_b_corpus.py` (Arm B) · `result_armB.json`.

## Next (rung-3 — for main to schedule)
Wire the 3-part lane DISJOINT from the emit-drive lane {0,4} (a_substrate_disjoint):
L1 role-filler bind → engine_cli §WM-BUFFER, L2 Go/NoGo gate → brain vbasal_*, L3
hippocampal completion → `.kosmos` anchor store; centering/whitening of engine reps
is a REQUIRED preprocessing (real_mean_raw collapse). Then re-measure via the
`anima evaluate --py` decode path for a GREEN-eligible engine-native verdict.
