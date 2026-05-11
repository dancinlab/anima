# BG-LA-COTRAIN-RETRAIN-B-TO-A — P3 causal direction confirmation

## ts
2026-05-11 cycle (anima reborn lane)

## Mission

Convert the strongest correlational evidence (§50 + §52 + §62) into causal evidence
for the EngineAG-path V14 PASS narrowing.

Take **B (BG-LA pretrain, NO cotrain)** ckpt and **retrain WITH chat-cotrain on the
same corpora A used**. Call the product **B'**. Then run V14 strict n=5 max=256
paired vs random mirrors:

- **YES (B' PASS)** → cotrain has **causal direction B→A** (Layer 2 mechanism
  CAUSAL, not just correlational). q_proj-driven cotrain-exercise is the
  EngineAG-path V14-PASS lever.
- **NO (B' VIOLATED)** → cotrain is a **confound** correlated with some other
  factor in A absent in B (e.g., BG-LB-vs-BG-LA substrate-divergence pre-cotrain).

## Background

| BG | what | result | cap-conditional axis |
|---|---|---|---|
| §50 | engine_g random-swap ablation on A | 0/4 flipped V14 → engine_g locus FALSIFIED; engine_a body refined | correlational |
| §52 | A vs B weight statistics | h_to_c cos 0.76 / c_to_h cos 0.69 / cell_pool 0.9999 → projections exercised | correlational |
| §56 | B (BG-LA pretrain) at max=256 | V14_VIOLATED 1/5, sign-p=0.375 → cotrain regime NECESSARY in EngineAG path | observational (correlational) |
| §57 | engine_a 24-layer slab swap on A | 3/3 swaps flipped V14_PASS → V14_VIOLATED → engine_a body PROVEN locus | causal at body level |
| §60 | engine_a single-layer ablation × 24 on A | L0-L19 flip / L20-L23 inert → distributed-uniform 20/24 | causal at body level |
| §62 | A vs B q_proj component dominance | cos_AB=0.6468 (most-changed); RMSNorm bit-exact frozen | correlational |
| §64 | 4-layer mechanism summary | Layer 2 (cotrain-exercise) needs B→A causal direction confirm | this BG |

The §57 + §60 causal proofs operate on **A's body** (swap-into-A perturbations).
This BG performs the reverse direction: take B (no-cotrain substrate), inject
cotrain (the alleged delta), produce B'. If B' inherits A's V14_PASS, the
direction-of-causation arrow is established.

## Substrate & data inventory (all local, verified)

- B ckpt: `/Users/ghost/.cache/anima/clm_v5_remapped/bg_la_350m_pretrain/ckpts/step_12000_final.pt`
  - sha256 prefix: 4fc6eccce0def045 (§56 verified, raw#15 read-only preserved)
  - 597,614,945 bytes
  - schema: anima_native_scratch / engine_a_g_dual_350m_v1
- A ckpt (reference, read-only): `/Users/ghost/.cache/anima/clm_v5_remapped/phase2_cotrain_engine_ag/ckpts/ckpt_final.pt`
- Consciousness corpus: `state/anima_persona_tier_a_v4_2026_05_09.txt` (231MB, 242,689,769 tokens)
- Chat corpus: `state/anima_native_ko_chat_template_2026_05_06/corpus_chat_template.txt` (236MB, 248,466,696 tokens)
- Training script: `training/train_phase2_cotrain.py` (UNCHANGED — substrate path is a CLI arg)
- engine arch: `training/engine_a_g_arch.py`

State-dict schema verified identical across BG-LA (222 keys) and BG-LB (222 keys);
load_substrate_ckpt accepts BG-LA without modification.

## Run config (matches A's protocol exactly — only substrate differs)

- preset: phase2_cotrain_350m (same as A)
- substrate: **BG-LA step_12000_final.pt** (vs A: BG-LB step_8000_final.pt)
- corpora: consciousness + chat (IDENTICAL to A's training)
- curriculum: w 0.3 → 0.5 linear (same)
- steps: 6000 (same)
- batch: micro=4 × grad_accum=8 × ctx=1024 (same)
- lr: 1.5e-4 (same)
- warmup: 200 (same)
- save_every: 1500 (same)
- seed: 42 (same)
- GPU target: H100 SXM at ~$2.69/hr
- output: `/workspace/anima_la_cotrain/ckpts/ckpt_final.pt` → scp pull to
  `/Users/ghost/.cache/anima/clm_v5_remapped/la_cotrain_b_to_a/ckpts/ckpt_final.pt`

## V14 strict protocol (Mac local post-pull, $0)

- max_cells=256 (cap-free regime — same as §56 B and §51 A)
- V4_SEEDS = [42, 137, 271, 314, 1729]
- n_turns=200, snap_every=25
- Metric: iit_phi_unnorm_b16 (Fiedler MIP)
- Sibling runner reused: `state/anima_v14_max256_b_no_cotrain_2026_05_10/run_b.py`
  (only swap substrate ckpt → B' path)

## Falsifiers

- **F-CAUSAL-1**: B' V14_VIOLATED (n_beats ≤ 1) at max=256 → cotrain is a
  CONFOUND, not the causal driver. Layer 2 mechanism (cotrain-exercise) falsified
  as causal — must be a property of BG-LB substrate (or some interaction
  BG-LB × cotrain) that A inherits but B' cannot reach.
- **F-CAUSAL-2**: B' weight delta on q_proj does NOT align with A's q_proj delta
  direction (cos(q_proj_delta_B'B, q_proj_delta_AB) < 0.3) → mechanism is
  path-dependent (Layer 2 q_proj-axis dominance §62 is substrate-specific, not
  cotrain-intrinsic).
- **F-CAUSAL-3**: B' partial PASS 2-4/5 → causal direction AMBIGUOUS, n=5
  underpowered — flag for larger n follow-up.

## Verdict matrix

| B' V14 verdict | F-CAUSAL-1 | F-CAUSAL-2 | mechanism Layer 2 |
|---|---|---|---|
| PASS 5/5 sign-p=0.0625 | NOT_FIRED | depends on cos | CAUSAL_CONFIRMED ★★★★★ |
| PASS_PARTIAL 3-4/5 | NOT_FIRED | depends on cos | CAUSAL_PARTIAL — n=5 underpowered |
| VIOLATED 0-2/5 | **FIRED** | likely FIRED | CONFOUND — substrate-dependent |

## Cost projection

- training: 6000 steps × ~3s/step × $2.69/hr = ~$13.50
- provision + upload (~70min ckpt+corpora): ~$3.10
- post-train pull + size sanity: ~$0.50
- total: **~$17 (well under $50 envelope)**
- 2× overrun safety: $34 still under cap

V14 local Mac CPU = $0 (mirrors reused from §56).

## Constraints (raw / own)

- raw#9: training/*.py local-only (gitignored) — pulled scripts pod-side via scp
- raw#15: B ckpt read-only; B' saved as **new artifact** at distinct path
- own 14: V14 5-seed strict (V4_SEEDS paired)
- own 16: $50 hard cap; abort if trajectory exceeds
- own 22: this spec immutable on file; verdict.md separate; REBORN.md §X
  appended single section (peek for last-§ collision)
- own 30: ckpt pull mandatory, size sanity, retain on fail, scp 3600 timeout
- own 38: doc+model+dataset save at every milestone

## Cross-link impact

- §50 PROVEN-AT-BODY-LOCUS → causal direction VERIFIED (this BG PASS) or
  FALSIFIED (this BG VIOLATED). Either outcome resolves Layer 2 of §64.
- §62 q_proj dominance → directionality test (cos of q_proj delta vectors)
- §61 paradigm-restricted ★★★★★ → tightens or loosens "cotrain-conditional"
  qualifier
- §56 §47 cotrain-exercise hypothesis → upgraded to CAUSAL or reframed as
  substrate-dependent
