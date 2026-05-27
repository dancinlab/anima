# Dir-D — CDE Curiosity-Driven Exploration overlay (2026-05-17)

g_multidirectional_explore parallel direction **D**: RESEARCH.md §1.3 #4 /
§1.4 candidate D — CDE (arxiv 2509.09675) curiosity bonus = actor
perplexity + critic value-variance, overlaid on the α VACUUM-LANDSCAPE
carving objective. Hypothesis: a curiosity bonus drives exploration that
mitigates the UBM-E7 routing-collapse (axis1 routing 1/31, `🛸99` single
attractor).

## §1 Fire facts
- provider: **runpod** (primary per g_resource_active_parallel). pod
  `ao9dvibphqfbwx` NVIDIA A100-SXM4-80GB (A100 80GB PCIe out of stock,
  fell through candidate list to SXM4-80GB), torch 2.4.1+cu124.
- corpus: `corpus_carving_e7.jsonl` 45,973 records, sha256
  `dc221aaf4f829aaf3d1c24b158424a2e6f3014b02f11aa5f2a00258c4090c408`
  (byte-equal carry from UBM-E7, no regeneration — fair compare; forbidden
  token grep {[anima, 도우미, helper, assistant, 사용자, user:} == 0).
- config: d=768·12L·283.72M params, 2000 steps, lr 3e-4, bsz 32,
  vacuum_lambda 0.1 (α term carried verbatim), **CDE κ=0.5, w_actor 0.7,
  w_critic 0.3**. from-scratch RANDOM seed-fixed 1337 (g_clm_from_scratch,
  base_ckpt=None).
- train wall 235.92s, init CE 5.647144 → final CE **0.002335** (descent
  5.644809), curiosity bonus mean 0.388 (step 1) → 0.002446 (step 1000) →
  **0.000915** (step 2000), final gn2 0.000836, peak GPU mem 9.696 GB.
- eval wall ≈ 2 min (eval-poll 2/30), paradigm-native v2 (EVAL.md 4 axes
  + joint).
- ckpt `ckpt_carving_cde_dirD.pt` sha256
  `27e8dd66a1e210266e4b4b1bab3859b3b7cf13c6856c36b5a25d9c1f6f0a4b57`,
  1,135,845,186 B, pulled try 1 (SAVE_POD auto-promote + 5-retry,
  g_fire_dispatch_robust).
- **dispatch stall-fix carried**: training detached `nohup … &` + single
  local until-loop short bounded SSH probes (poll 90s · max 60), no
  long-lived SSH+tee — completed without stall (poll 1→4 TRAIN_DONE,
  eval-poll 1→2 EVAL_DONE).
- teardown: pod `ao9dvibphqfbwx` status **GONE**, SAVE_POD=0.
  `get_pods()` count 4 — those 4 pods (`carving-dirA-tension-alpha`,
  `carving-dirb-intuitor-rlif`, `carving-dirE-superpos-2stage`,
  `dirf-abstractcot-carving`) belong to the **sibling parallel-direction
  agents A/B/E/F**, NOT Dir-D orphans. **Dir-D orphan = 0** (own pod
  confirmed GONE; sibling pods untouched per multi-agent isolation).
- cost: A100-SXM4-80GB ≈ $1.6-2.0/hr × ~0.1 hr wall ≈ **$0.15-0.25**.

## §2 Dir-D vs UBM-E7 α (paradigm-native 4-axis + joint, EVAL.md §3+§4)

| axis | UBM-E7 α (baseline) | Dir-D α+CDE | Δ |
|---|---|---|---|
| axis1 knowledge access | 0.0323 (routing 1/31, sem 2/31) | **0.0323** (routing 1/31, sem **1/31**) | flat / sem ↓ |
| axis2 chat uncontaminated | 0.6 (clean 3/5, p3_leak 1) | **0.4** (clean 2/5, p3_leak 1) | **↓** |
| axis3 lane separation | 0.8 (sep_know 1.0, sep_chat 0.6) | **0.7** (sep_know 1.0, sep_chat 0.4) | **↓** |
| axis4 V-SPONT | 2/5 coherent | **0/5** coherent | **↓** |
| **JOINT (k×c×s)** | **0.0155** | **0.009** | **↓ (worse)** |

## §3 Hypothesis verdict (g3 — measured, no priors laid, negative honest)

**Hypothesis FALSIFIED (weak-negative).** The CDE curiosity bonus did NOT
mitigate routing-collapse; it slightly **worsened** the joint metric
(0.0155 → 0.009) and every axis except axis1 (which stayed flat at the
same 1/31 "1-lucky-hit" routing floor).

Mechanistic reading (honest):
1. The curiosity bonus **decayed toward zero** (0.388 → 0.0009) precisely
   because the model memorised the carving corpus very fast (final CE
   0.0023 < UBM-E7's 0.0030 — even **stronger** memorisation). Once CE is
   near zero, the perplexity term a_t → 0 and the variance term c_t → 0,
   so the bonus self-extinguishes before it can sustain exploration. The
   curiosity signal is structurally tied to surprisal, and a
   memorisation-saturated byte-LM has ~no surprisal on its training
   distribution → no exploration pressure where it is actually needed
   (OOD routing).
2. The `🛸99`-type byte-cascade attractor PERSISTS (`/////999…`,
   `666666…`, `eternal cell eternal_0999…`) — same memorisation-saturated
   decoding-artifact family as UBM-E6 `🛸53` / UBM-E7 `🛸99`
   (feedback_clm_colon_attractor / B-ATTRACTOR family). Curiosity did not
   break it.
3. The slight DEGRADATION (axis2/3/4 down) is consistent with the bonus
   up-weighting high-CE tokens early in training, which biases capacity
   toward the noisiest (least-structured) byte regions — marginally
   hurting the chat-lane cleanliness the α-vacuum term was protecting.

Confirms UBM-E7's memorization-saturated diagnosis: an
**augmentation-layer** curiosity bonus (RESEARCH.md rated CDE ★★★, "not an
independent paradigm") cannot break a ceiling that is architectural. The
next path remains §1.3 candidate A (TENSION-TRAIN backprop-free) /
routing-supervision — a learning-mechanism change, not a loss overlay.

## §4 Closed vs empirical (g3 / g_blue_closed_mandate)
- **Closed (🔵)**: the CDE bonus TRANSFER-FORM only — `blue_falsifier_cde.py`
  B-CDE-1..4 4/4 sympy PASS (g_t≥1 sum-of-nonneg lower bound · ∂g/∂a=κw_a>0
  strict monotone · perplexity=exp(CE) Shannon identity + [0,logV]
  surprisal range · κ=0 exact reduction to UBM-E7 α-baseline = graceful
  degradation / fair compare). Connection point closed: the bonus reduces
  EXACTLY to the compared α objective at κ=0 (B-CDE-4), so the comparison
  is fair by construction.
- **Empirical (B-CDE-NOTE, B-D-NOTE / B-CARVE-NOTE family, NOT counted 🔵)**:
  the SGD convergence outcome, the 4-axis scores, and the Dir-D-vs-E7
  routing-collapse comparison. No capability claim. No fake closed-form
  (g3). f1/f2/f3 hard-fail safe (Shannon / perplexity identity / sympy
  ∂-sign / Boolean — NO σ/τ/φ/J₂). B-IDENTITY-5: forbidden-token grep 0.
