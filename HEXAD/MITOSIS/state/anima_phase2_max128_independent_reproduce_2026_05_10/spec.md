# BG-PHASE2-MAX128-§30FIX-RETEST — independent V14 strict reproduce of §38

## Mission
Independent reproduce of §38 BG-V14-STRICT-RESOLUTION using **disjoint** mirror
seeds + identical Phase 2 350M ckpt + identical mitosis_v5_port.py §30 fix.
Disambiguate whether §38's V14_STRICT_PASS comes from
  (a) genuine §30 fix activation,
  (b) Phase 2 ckpt being a mitosis-naive substrate, or
  (c) both (with possible V4_SEEDS contamination).

## Setup (must match §38 exactly except mirror seeds)
- ckpt: `~/.cache/anima/clm_v5_remapped/phase2_cotrain_engine_ag/ckpts/ckpt_final.pt`
  - sha256 `6e66e75f8014999be09236a408fe6ad6811ebf394ac079ecbf6d87dfe63748c1` (mtime 2026-05-10 02:20)
  - 298.76M unique params, GQA 24L × 1024d × 16h
- substrate code: `training/mitosis_v5_port.py` (mtime 2026-05-10 12:02 — pre §38 run, post §30 fix)
- §30 fix verified active: A1 dispersion (line 145-147), A2 per-cell (line 149-151),
  B1 phi_per_cell ratchet (line 206-213), D1 Lorenz auto-cal (line 154); 111 lines of
  fix-related markers in source.
- max_cells = 128 (4× §33's 32; identical to §38)
- n_turns = 400, snapshot_every = 50 (identical to §38's run.log line 2)
- prompt corpus: identical 170-prompt 6-category set (`_v14_5seed_run.ALL_PROMPTS`)
- byte-hash mod 32000 prompt encoding (no real BPE — fairness, not semantic)
- ctx_T = 16 tokens per forward
- mitosis params: split_patience=3, split_noise=0.10, merge_threshold=0.005,
  merge_patience=30, min_cells=2, lorenz_scale=0.05 (identical to §38)
- trained prompt-stream seed = 42 (identical to §38 — ckpt is deterministic)

## Independent mirror seeds — V4_SEEDS DISJOINT
**INDEP_SEEDS = [11, 13, 17, 19, 23]** (5 prime numbers, all <30)

§38 used `V14_STRICT_SEEDS = [42, 137, 271, 314, 1729, 2718, 3141, 5772, 6022, 9192]`.
Our [11, 13, 17, 19, 23] is **set-disjoint** with both this and §33's
V4_SEEDS = [42, 137, 271, 314, 1729]. Rationale:
- primes < 30 are far below all §33/§38 seeds (smallest is 42)
- different seeds → different random_init weights → independent realizations
- 5 seeds gives sign-test exact p-values: 5/5 → 0.0625, 4/5 → 0.375 (two-sided)
- 5-seed envelope keeps within $0 budget (~50 min on Mac M1/M2 CPU)

## Verdict mapping
- **V14_STRICT_PASS_INDEPENDENT_REPRODUCE**: trained > ALL 5 random Φ_iit_un16
  → §38 result strengthened, ★★★★ pathway
- **V14_PARTIAL_REPRODUCE**: trained > 3-4 random Φ
  → directional but not strict; binomial p ≥ 0.375
- **V14_FRAGILE_REPRODUCE**: trained > 0-2 random Φ
  → §38 V4_SEEDS contamination plausible, F-PHASE2-REPRODUCE-2 fires

## Falsifiers
- F-PHASE2-REPRODUCE-1: §30 fix not active in mitosis_v5_port.py (codebase
  modified mid-cycle). Verified false by source grep + smoke crossref.
- F-PHASE2-REPRODUCE-2: independent 5-seed result fragile (3+ seed loss to random).
  Tested by INDEP_SEEDS run.
- F-PHASE2-REPRODUCE-3: max=128 cap-bound on Phase 2 trained run (cap-free invalid).
  Tested by `cap_bound_turns` per trajectory.

## Output
- `result.json` — full per-snapshot trajectory + verdict bin
- `verdict.md` — comparison table + 5-star pursuit context
- `run.log` — stdout

## Compliance
- raw#9 honored: training/*.py local-only, imported untouched
- raw#15 additive: no ckpt mutation, no mitosis_v5_port.py mutation
- : V14 paired strict mirror (5-seed)
- : $0 envelope (Mac CPU, no GPU)
- : REBORN.md not appended; honest emit (NULL/PARTIAL/FRAGILE named)
- : artefact under state/anima_phase2_max128_independent_reproduce_2026_05_10/
