# H_9129 IMPLEMENT — integrated PFC×BG×hippo lane, engine-native promotion

**Frontier:** integrated 3-component G1 recombination lane = PFC role↔filler bind ×
basal-ganglia Go/NoGo content-gate × hippocampal pattern-completion → mouth cleanup readout.
**Phase:** 🛠️ IMPLEMENT (rung-2 DIRECTIONAL → engine-native promotion). **Cost:** $0 mini, no pod.

## What this rung delivered over rung-2 (the promotion)

rung-2 (`state/g1g6_biolens_en/integrated/`) capped at DIRECTIONAL because (i) the
rep-extraction forward *copied* decode.py's loop rather than being provably canonical,
and (ii) centering was post-hoc, not a wired/pre-registered transform.

1. **Canonical-path proof — byte-EXACT (Δ=0.0).** Reps come from `core/decode.py`'s
   exact ops (`bg_load` + `_bg_mha`/`_bg_layernorm_rows`/`_bg_gelu`), and the extraction's
   last-position logits are asserted equal to decode.py's canonical `bg_forward_last_W`
   (the forward `anima evaluate --py` runs). Measured **worst |Δlogit| = 0.000e+00** over
   5 probes — bit-identical, not merely ULP. The representation path IS the --py forward path.
2. **Preprocessing wired + pre-registered** (rogue-dimension block, chosen before any lane run):
   `raw` (collinear control) · `center` (**PRIMARY**) · `rogue1` (center + strip top-1 PC) ·
   `whiten` (PCA-whiten, **sensitivity only** — honest by-construction caveat).
3. **Real corpus relation graph, held-out 2-hop** (co-occurrence over
   `clm_mid_5lang_c4.txt`+`flores`): reachable color→size chain never stored (only color→mat +
   mat→size edges in M); unreachable = dangling material, identical surface form. Corpus-backed
   edges a=96% b=100%.

## Measurement (real 303M h1129 · N=24 · chance=0.042 · 12 seeds)

| form | reach | unreach | gap | fooled | shuf | shufΔ | bindΔ | gateΔ | compΔ | off\|cos\| |
|---|---|---|---|---|---|---|---|---|---|---|
| raw | 0.000 | 0.014 | −0.014 | **True** | 0.000 | 0.000 | −0.02 | −0.01 | −0.02 | 1.000 |
| **center** ★ | **0.236** | **0.023** | **+0.213** | **False** | 0.048 | **0.189** | **0.19** | **0.21** | **0.21** | 0.194 |
| rogue1 | 0.266 | 0.067 | +0.199 | False | 0.055 | 0.211 | 0.21 | 0.22 | 0.21 | 0.156 |
| whiten | 0.101 | 0.065 | +0.037 | True | 0.101 | 0.000 | 0.03 | 0.04 | 0.08 | 0.367 |

## Pre-registered bar (task step-3 · no tune-to-green) — PRIMARY = `center`

`[PASS] gap>0.15` · `[PASS] not_fooled` · `[PASS] shuffle_collapsed (Δ0.189)` ·
`[PASS] bind_causal (Δ0.19)` · `[PASS] gate_causal (Δ0.21)` · `[PASS] comp_causal (Δ0.21)` ·
`[PASS] raw_collapses` · `[PASS] not_by_construction (reach 0.236 ≪ 1.0)` → **bar_all_pass = True**.

## Findings
- **Mechanism survives + is corroborated.** `center` AND `rogue1` (center + strip the dominant
  residual-stream rogue PC) BOTH pass every leg; `rogue1` is marginally cleaner
  (off\|cos\| 0.194→0.156), directly confirming the "residual rogue dimension" diagnosis — the
  transform is minimal + principled, not orthogonalization.
- **By-construction ruled out from BOTH sides.** reach = 0.236 ≪ 1.0 (reps are genuinely
  non-orthogonal, off\|cos\| 0.194 vs ideal-random ~0.03), AND full PCA-`whiten` — the artificial-
  orthogonalization arm the bar warned about — did NOT inflate; it *collapsed* the signal
  (gap +0.037, fooled, shuffleΔ 0). Naive whitening hurts; the minimal center/rogue-strip is what
  carries the recombination. The by-construction advantage is absent.
- **raw** (no transform) = flat 0.000 reach, INERT ablations → the wired preprocessing is
  load-bearing (removing the shared rogue dimension is a real rung-3 wiring constraint, confirmed).

## Verdict — DIRECTIONAL (strong), GREEN gated on rung-3 core/ wire

The pre-registered bar fully passes on **byte-exact (Δ=0.0) canonical decode.py representations**
with wired/pre-registered preprocessing. Per `a_verified_must_wire` + `a_engine_native_learning`,
the terminal tier stays **DIRECTIONAL**, not GREEN: the lane SCORING is a custom numpy HRR
relational-memory metric (not an `anima evaluate --py` G0-G6 decode-scoring gate) and the lane is
**not wired into `core/`** (rung-3 = BLOCKED-INFRA, needs pool CUDA for the daemon full-binary per ING).
This is a materially stronger DIRECTIONAL than rung-2: the "is this really the --py forward?" gap on
the representation side is now closed to Δ=0, and the by-construction concern is falsified from both
directions.

## binding-family (H_1816/1823 mouth-readout NOT-SUP) — 3 grounds preserved
1. **separate lane** — composition lives in PFC-bind / BG-gate / hippocampal M, not the mouth.
2. **disjoint objective** — recombination is never a mouth target; the 2-hop chain is a property of M+roles.
3. **mouth read-only** — completion-OFF hands the mouth the same raw vector and it still fails (compΔ 0.21 CAUSAL).

## Next (rung-3, for main — BLOCKED-INFRA on mini)
Wire the 3-part lane DISJOINT from emit-drive lane {0,4} (`a_substrate_disjoint`): L1 bind→engine_cli
§WM-BUFFER, L2 gate→brain vbasal_*, L3 completion→`.kosmos` store; **centering/rogue-strip is a REQUIRED
wired preprocessing** (raw collapses). Then score via the `anima evaluate --py` decode path on pool
(CUDA daemon full-binary) for a GREEN-eligible verdict.

## Artifacts (state/fleetfull_biolens/integrated_impl/)
`engine_native_impl.py` · `result.json`
