# H_1816 predictive-coding parametric-bias binding — 303M engine-native G0-G6 RESULT

**verdict: NOT-SUPPORTED (terminal, seed 7).** predictive-coding binding (L_bind) + free-energy
spread (L_var) auxiliary trunk objectives do NOT lift G1 recombination OR G6 ideation above the
ce_marginal CE-only control on the 303M CLMConvMoE (d3784 L4 E2→E3, 4-cell register corpus).

## Setup
- Arch: CLMConvMoE byte V=256, L=4 d=3784 E0=2→Emax=3 mid-split, K=3, dilation min(2^l,512).
  345.665M params. savant golden-zone inhibition anneal + mitosis split ON (= `cli/train.py --canon`).
- Corpus: 4-cell register (a_chat_registers) from HF `dancinlab/anima-corpus-{ko,en}-{general,sns}`,
  sha-verified (ko-gen 19e6ac9e 60MB, en-gen 66140944 60MB, ko-sns c836e9fc 6.18MB, en-sns 49f347c7 1.33MB),
  proportional sampling, val_frac 0.05.
- 3 arms, single variable = the PC auxiliary objective. Trunk/readout/data/step/seed shared.
  steps=2000, bf16, seed 7. Host: summer RTX 5070 (pool, free).
- BIND projection (Linear d→32) is TRAINING-ONLY → all arms serialize to the SAME additive `.clm`
  → engine-native G1/G6 by-construction open.
- Frozen hyper (pre-reg, NOT tuned): LAMBDA_BIND=0.1, LAMBDA_VAR=0.01, BIND_DIM=32.

## Held-out DESCENT gate (math.log mirror, per register · integrity guard)
| arm            | pooled val_CE | registers DESCENT | verdict-valid? |
|----------------|---------------|-------------------|----------------|
| ce_marginal    | 1.699         | **4/4** (ko-gen 1.69·en-gen 1.85·ko-sns 1.51·en-sns 1.85, overfit_warning=False) | YES |
| pc_bind        | 1.717         | **4/4** (ko-gen 1.67·en-gen 1.87·ko-sns 1.49·en-sns 1.86, overfit_warning=False) | YES |
| pc_free_energy | 5.877         | **1/4** (ko-gen 6.85 > uniform 5.545 = NO-DESCENT) | **NO — INTEGRITY FAIL** |

- ce_marginal + pc_bind: clean generalization, no overfit (vs the old clm303 NO-DESCENT overfit).
- **pc_free_energy: held-out DESCENT FAIL** — the L_var anti-collapse spread term (`−β·var_batch(PB_seq)`)
  destabilized next-byte training (ce 5.34, collapsed: mitosis_cells 3). Per PREREG FALSIFY clause this
  arm is broken/not a valid verdict ckpt (천장 아님; the spread term, as frozen, breaks the model).

## Engine-native G0-G6 (py 2-production core/g_gates.py ← core/clm_decode.py, gen 80; DIRECTIONAL under 2026-06-28 py-retire policy — hexa is terminal)
| gate | ce_marginal (control) | pc_bind | pc_free_energy (integrity-FAIL) |
|------|-----------------------|---------|----------------------------------|
| G0 COHERENCE   | PASS 5/5 | PASS 5/5 | (broken ckpt) |
| **G1 RECOMBINATION** | **FAIL** distinct=0 max_single=1 | **FAIL** distinct=0 max_single=1 | — |
| G2 NOVELTY     | PASS n_novel=74 ctrl=0 | PASS n_novel=66 ctrl=0 | — |
| G5 NON-FAB     | PASS l1=0.026 | PASS l1=0.060 | — |
| **G6 IDEATION ★** | **PASS** dist=6 fals=1 | **FAIL** dist=6 fals=0 | — |
| **CLOSURE (G0∧G1∧G2)** | **FAIL** | **FAIL** | — |

(detector calibration 10/10 advisory.)

## LIFT (the hypothesis test)
- **G1 lift: ZERO.** composed_distinct = 0 for control AND pc_bind (and torch-probe = 0 for all 3 arms
  incl. pc_free_energy). Binding objective gives no recombination gain. G1 wall holds.
- **G6 lift: NEGATIVE.** pc_bind fals=0 < control fals=1. Binding objective did not add — slightly hurt.
- ⇒ **pc_bind / pc_free_energy engine-native G1 AND G6 ≤ ce_marginal** = PREREG FALSIFY condition MET
  = predictive-coding parametric-bias binding is **NOT a G1/G6 lever** at this config (NOT-SUPPORTED).

## Why (mechanism honest-scope)
- **L_bind collapsed to ~0 by step ~550** (0.287→0.003): per-step penultimate latents already match
  their sequence-mean under the additive CLMConvMoE, so the binding pressure is trivially satisfied and
  exerts no compositional force on the trunk. PREREG flagged this exact failure mode (latent collapse);
  the L_var spread term meant to prevent it instead broke generalization (pc_free_energy DESCENT FAIL).
- Consistent with the standing objective-lever census ([[g1-lever-multilens-objective]],
  [[exp3-bind-g1g6-engine-native-floor]]): CE-trunk does not reward composition, and a penultimate-readout
  binding term (multiplicative OR free-energy-aux) does not open G1 — the lever is the trunk OBJECTIVE itself.

## Scope / caveats (c9 honesty)
- seed 7 only (time). PREREG asked majority {7,4302,4303}; this is a single-seed read but the G1 lift is
  0 (not marginal), so seed-robustness would not change FAIL→PASS. Multi-seed follow-on = ING.
- Eval engine = py g_gates.py. Under the 2026-06-28 py-retire policy (core/CLAUDE.md, cli/evaluate.hexa
  L26) the **terminal** engine is hexa-native `anima evaluate`; py is now DIRECTIONAL. Hexa-native eval on
  these `.clm` hit a CONTENTION CUDA-OOM during training (RTX5070 12GB; bump-allocator per-decode reload,
  precedent a_engine_native_learning) — hexa terminal re-run on the free GPU = ING follow-on. The py result
  here is the same production core/clm_decode.py mouth, byte-parity-proven, and is decisive at distinct=0.

## ckpts (a_fire_recover_complete — PULLED)
- state/1816_predcoding_binding/ckpt/
  - ce_marginal_seed7.clm  sha256 ffa42cdb865b69a3c000505a2cf3caacbebc7602bf458b099f3ea11a36a71c49 (176MB) + .pt (1.38GB)
  - pc_bind_seed7.clm       sha256 b4b84a6fd808d72e389475932878badc0b7005a2f4ef2ad6fd9e6b59c25f4764 (176MB) + .pt (1.38GB)
  - pc_free_energy_seed7.clm sha256 e263b42e4e06e7e0c657f12f00f789cd7e91dc80d7b455b3032d2ba62df8172f (176MB · INTEGRITY-FAIL)
- logs/json/descent/g0g6 txt all in ckpt/.

## Cost
- summer (pool, free) for the production run. One vast A40 ($0.574/hr) died mid-bootstrap (flaky net,
  GONE) + one redundant A40 torn down — total throwaway rent ≈ $0.10. Net GPU spend for the verdict ≈ $0.
