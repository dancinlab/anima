# G1/G6 engine-divergence trace — clm303_clean

**Question (user hypothesis):** "torch passed G1(recombination)/G6(ideation) but the
production engine (.clm int4 + dt_* decode) drops it → the engine corrupts the
result." Isolate the *first divergence point*: quantization (B) vs decode-arithmetic
(A/C) vs scorer (D), or is the signal simply absent from the weights (floor)?

**Verdict: ENGINE IS INNOCENT — it is a WEIGHT/TRAINING FLOOR, not a measurement
artifact.** G1 and G6-falsifiability are **zero at full-precision fp32 with exact
math**. int4 quantization and the dt_* approximations have **no effect** on the
G1/G6 outcome. (break-walls type-(d) structural floor on the recombination/ideation
axes; type-(a) measurement-artifact is REFUTED.)

All work local, CPU, $0 (OMP_NUM_THREADS=4, one 303M numpy forward ≈ 0.6 s). torch
absent → .pt read torch-free via `state/clm303_g6/tools/ptload.py`.

---

## 0. A blocking discovery that reshaped the method: .pt and .clm live in DIFFERENT hidden bases

A naive 3-way per-stage tensor dump (.pt-fp32 vs .clm-int4) is **invalid** here:

- The .clm-int4 weights and the .pt-fp32 weights have the **same value multiset**
  (embed |·|mean 0.6808 vs 0.6805; conv 0.0115 vs 0.0117) but are **element-wise
  uncorrelated** (per-byte embedding corr ≈ 0.00; no channel-permutation match —
  best-col-corr 0.23, not bijective).
- Yet they are the **same model**: the two existing trusted tools agree end-to-end —
  `fastmirror.py`(.clm int4, math.log) **model_ce 1.691** ≈ `torch_golden_fwd.py`
  (.pt fp32 via ptload) **model_ce 1.742** on the same corpus (both strong DESCENT,
  shuffle ≈ 7.2–7.4). Argmax agrees 27/30 on real-text contexts.

→ The .clm and .pt express the **same function in a permuted/rescaled hidden-channel
basis** (a network symmetry; conv→GroupNorm(G=1) lets you permute+rescale the d=3784
channels with downstream compensation). V-indexed (`roB` corr 0.91) and E-indexed
(`rB` corr 1.0) tensors line up; every d-indexed tensor does not. This is **not a
defect and not different checkpoints** (consistent with the prior verified
"serialize-not-defect" result).

**Consequence:** you cannot diff `.pt`-derived and `.clm`-derived *intermediate*
tensors element-wise — different bases ⇒ everything "diverges" spuriously. The clean
isolation must be done **within one basis**: take the .pt fp32 weights and ablate
quantization / dt-math against *themselves*. (Future divergence-hunts: don't burn
time on element-wise `.pt`-vs-`.clm` weight diffs — compare at the output/CE level.)

Mapping used to build an fp32 W in the `core/clm_decode.py` format (validated:
fp32 math.log CE 1.307 ≈ README held-out val_CE 1.33): `Wt[ci*K+k, co] =
torch_w[co,ci,k]` i.e. `w.reshape(Cout, Cin*K).T`; experts/router clipped to the
active **E=3** (the .pt's 4th expert slot is the pruned Emax slot, |·|mean 0.004 —
.clm E=3 is correct).

---

## 1. DECISIVE: self-consistent ablation (basis F = the .pt fp32 weights), gen=40

Same forward, same seeded top-k sampler, same g_gates G1/G6 detectors; only the
named factor changes. (`state/g1_engine_divergence_trace/ablate.py`, full log
`ablate.log`.) My int4 quant (int4-sym per-output-channel, replicating the serializer
dequant `w=(nibble-8)·scale`) adds only **+0.046 CE** (fp32 1.483 → int4 1.530).

| config | weights | math | G0 | G1 best_distinct (pass) | G6 dist / fals (pass) |
|---|---|---|---|---|---|
| **A** fp32_eng  | fp32 | engine dt_* | 5/5 ✓ | **0** (✗) | 6 / **0** (✗) |
| **B** int4_eng  | int4 | engine dt_* | 5/5 ✓ | **0** (✗) | 6 / **0** (✗) |
| **C** fp32_corr | fp32 | exact np    | 5/5 ✓ | **0** (✗) | 6 / **0** (✗) |
| **D** int4_corr | int4 | exact np    | 5/5 ✓ | **0** (✗) | 6 / **0** (✗) |
| **E** real .clm | .clm | production engine | 5/5 ✓ | **0** (✗) | 5 / **0** (✗) |

- **A vs B (pure quantization):** identical. int4 does NOT kill G1/G6.
- **A vs C (pure dt-math):** identical. dt_* does NOT kill G1/G6.
- **A (fp32, exact-precision possible):** G1=0, G6 fals=0 already. **The signal is
  not in the weights.**
- E (real production .clm, separate basis) reproduces the same failure — matches the
  known engine-native baseline (`state/clm303_clean_corpus/g0g6_py.txt`).

G1 ladder is flat across all configs (k2..k5 composed coverage = 0, max_single = 1):
the model does not even surface concept keywords under composition. G6 passes the
**distinctness** sub-bar (dist 5–6 ≥ 5) but `fals=0` in *every* config — it fails
purely on the **falsifiability** detector, identically with or without the engine.

**fp32 at full precision with exact math cannot clear G1 or G6-falsifiability ⇒
the wall is a weight/training floor; quantization and decode-arithmetic are
exonerated.**

---

## 2. Per-stage divergence (SAME basis F — now meaningful), G6 frame prompt

`fp32+eng` vs `int4+eng` (pure quant) and vs `fp32+correct-primitives` (dt-math).
max-abs-diff per stage:

| stage | QUANT (int4) | DT-prim | \|stage\|max |
|---|---|---|---|
| s0 embed (fp32 ext, unquantized) | 0.0 | 0.0 | 3.21 |
| s1 ec-conv        | 1.33 | 0.0  | 150.7 |
| s2 trunk0..3      | 2.1→4.7 | 2.6→9.7 | ~150–161 |
| s3 router logits  | 1.02 | 16.6* | 27.5 |
| s4 expert stack   | 52.7 | 252* | 707 |
| s5 moe mix        | 53.2 | 248* | 697 |
| s6 norm_out       | 2.83 | 9.46* | 24.9 |
| **s7 logits**     | **6.07** | 19.9* | 28.9 |

QUANT column is clean: int4 perturbs hidden stages ~1–7% and the final logits by
~6/29 ≈ 21% — enough to flip the occasional **near-tie** top token on a single prompt
(this prompt: fp32 argmax 116 vs int4 97, the top-1/top-2 pair) but with **zero**
aggregate G1/G6 effect (§1). *DT-prim column (\*) is partially inflated by a
GroupNorm-convention mismatch I introduced in the stage-capture "correct" mode
(per-row LN vs the engine's global GN over T×C); the clean dt-math isolation is the
§1 config C, which monkeypatches only the scalar primitives and keeps the engine GN
structure — and shows no G1/G6 effect.*

---

## 3. dt_* primitive accuracy (the decode arithmetic itself)

| primitive | role | accuracy vs exact |
|---|---|---|
| `dt_exp`  | softmax (sampler, MoE) | max rel-err **4.2e-14** over x∈[-12,12] — exact |
| `dt_erf`  | GELU gate | max abs-err **1.4e-7** over x∈[-6,6] — negligible |
| `dt_ln`   | CE loss only | **BROKEN** far from 1: err 0.235 @0.01, 8.67 @1e-6, **0.746 @256** (dt_ln(256)=4.799 ≠ ln256=5.545) |

- `dt_exp`/`dt_erf` are effectively exact → sampling/logits are faithful → no G1/G6
  impact (confirmed §1).
- `dt_ln` is the known-buggy one, but it is used **only in `clm_forward_ce`** (the CE
  scalar), never in decode/sampling. It clamps CE (uniform shows as 4.799 not 5.545)
  and hides overfit in the engine CE readout — **irrelevant to the decode-based
  G1/G6 verdicts here**. (Cross-check with math.log mirror as already mandated.)

---

## 4. Conclusion + root-cause target

- **First divergence point for G1/G6: there is none in the engine.** Quantization
  (B), decode arithmetic (A/C), and scorer (D, same detectors throughout) are all
  exonerated. fp32-exact already yields G1 distinct=0 and G6 fals=0.
- **The signal is absent from the weights** = training/objective floor. This matches
  the standing memory `g1-lever-multilens-objective`: CE training does not reward
  recombination; the G1 lever is the **trunk learning OBJECTIVE**, not the decode
  path. G6 here fails specifically on *falsifiability*, not distinctness (dist≥5).
- **Root-cause target = NOT the engine.** Do not "fix" serialization precision or
  dt_* for G1/G6 (no payoff — proven). The lever is upstream: a recombination/
  ideation-rewarding training objective (recomb-objective H_1602 family), per the
  G1-closure campaign. The engine's only real arithmetic defect, `dt_ln`, is a
  hexa-lang upstream fix that affects the **CE metric** only, not these verdicts.

Artifacts: `ablate.py`/`ablate.log` (decisive §1), `wbuild.py` (fp32→clm-format map),
`stage_capture.py` (§2), this RESULT.md. All under
`state/g1_engine_divergence_trace/`. DIRECTIONAL caveat: torch/.pt is reference only;
the production verdict (E) is engine-native and reproduces the floor.
