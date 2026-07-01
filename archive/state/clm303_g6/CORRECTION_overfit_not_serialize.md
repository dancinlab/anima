# H_1579 CORRECTION — clm303 NO-DESCENT = OVERFIT, not a serialization defect

**Date 2026-06-24.** The original `GARBLE_3WAY_RESULT.md` diagnosis ("clm303.clm SERIALIZATION DEFECT")
is **overturned**. The raw measurements there are all valid; the *conclusion* was wrong. This file holds
the torch-free reference-match that proves the serializer is byte-faithful and the real cause is
OVERFITTING + an engine `dt_ln` CE bug. (c9 — the oversight is reported, not hidden.)

## 1. The serializer is byte-faithful (reference-match)

| measurement | result | implication |
|---|---|---|
| re-serialize `state/g6-deep-mouth-ladder/ckpts/clm303_L4_d3784.pt` via `train/clm/model/clm_serialize_v2.serialize(L=4,E=2)` vs the shipped `.clm` | **BYTE-IDENTICAL** (155074330 B == 155074330 B) | serializer is deterministic + faithful |
| TORCH-GOLDEN fp32 forward (raw `.pt` weights, **bypassing the `.clm`**) vs the int4 `.clm` mirror, both on **English** (L4's training language) | **2.2346 vs 2.2349** (agree to 4 decimals; Δ = pure int4 quant noise) | int4 → v0.3 round-trip is functionally exact |

Tools (torch-free, `state/clm303_g6/tools/`): `ptload.py` (pure-Python torch `.pt` → numpy, handles bf16),
`fastmirror.py` (vectorized `clm_decode` mirror, byte-reproduces the canonical mirror), `torch_golden_fwd.py`
(numpy `model.py` forward from raw `.pt`).

## 2. The NO-DESCENT is OVERFITTING + wrong-corpus testing

| artifact | corpus | mirror model_ce | uniform=ln256 | verdict |
|---|---|---|---|---|
| `clm_d768_e2l1.clm` (CONTROL) | ko held-out | 4.44 | 5.545 | DESCENT (generalizes) |
| `clm303_L4_d3784.clm` (English-only) | **English** | 2.235 | 5.545 | DESCENT (own language!) |
| `clm303_L4_d3784.clm` | ko held-out | 22.98 | 5.545 | NO-DESCENT (never saw Korean) |
| `clm303.clm` savant (L4 E3) | **own training slice** | **0.656** | 5.545 | DESCENT (memorized) |
| `clm303.clm` savant | English held-out | 13.74 | 5.545 | NO-DESCENT |
| `clm303.clm` savant | ko held-out | 7.6 – 12.6 | 5.545 | NO-DESCENT |

clm303 trained on only ~25 MB (5-lang) to torch `lossF 0.047` (near-perfect = memorization). It DESCENDS
hard on its training data and fails ALL held-out text = textbook overfit. The original diagnostic only
tested held-out, so an overfit-but-working model looked "worse than random." The garble decode was a
held-out **prompt** on an overfit model (also expected).

## 3. Second, real bug — engine `clm_forward_ce` `dt_ln` masks overfit

`~/.hx/src/stdlib/flame/flame_math.hexa::dt_ln` uses the atanh series `2·Σ uᵏ/(2k+1)`, `u=(x−1)/(x+1)`,
24 terms — only converges near x=1. Measured: `dt_ln(256)=4.799` (true `ln=5.545`), `dt_ln(1e-6)=−5.14`
(true `−13.82`). `nn_lib.hexa::nn_ce_loss_allpos` computes `−dt_ln(p_t)` with `p_t≥1e-6`, so per-position
CE is **clamped at ~5.14** → a broken/overfit model's CE is falsely low and reads GREEN. The live engine
`clm_forward_ce` called overfit clm303 GREEN: `model_ce 3.30 < shuffle 4.93 < (buggy)uniform 4.799`. The
numpy mirror (`math.log`) is correct. → the held-out gate must score with `math.log`, NOT the engine CE.
Filed to hexa-lang (affects every engine CE/Φ readout, not just clm303).

## 4. Fix (this PR)

- **No serialize fix** — the serializer is byte-faithful.
- **Held-out mirror-DESCENT gate** added to `verify_clm_v2.py` (`descent_gate` / `serialize_self_verify`,
  math.log mirror, dt_ln-immune; held-out required + train-vs-held-out gap → overfit warning) and wired into
  `train/clm/train/train_lane_p*.py` + `cli/train.hexa` post-serialize, so a broken/overfit `.clm` can't be
  marked done / HF-uploaded. Validated: CONTROL PASS, clm303 FAIL+overfit_warning(gap 6.42), random-weight
  self-test FAIL (broken-detector fires).
- savant clm303 needs RE-TRAINING (regularization / larger corpus) — cost-gate follow-on. Re-serialization
  cannot fix an overfit model.
