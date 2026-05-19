# BG-V14-MAX256-B-NO-COTRAIN — substrate B × max=256 × 5-seed strict

## ts
2026-05-10 (5-star pursuit cycle; cleanest disambiguation of §47 cotrain-exercise hypothesis)

## Mission
§47 cotrain-exercise hypothesis FALSIFIED for v2 substrates (C/E PASS at max=256
with no chat-cotrain; previous V14_VIOLATED at max=128). Substrate B (BG-LA
350M pretrain, EngineAG path, NO Phase-2 cotrain) was V14_VIOLATED at max=128
(§47 audit, all 5 random beat trained). The remaining ambiguity:

- B at max=128: V14_VIOLATED (5/5 random > trained)
- A at max=256: V14_PASS (5/5 trained > random) — has cotrain
- C/E at max=256: V14_PASS (n=2 partial) — v2 path different

If B at max=256 also V14_VIOLATED → §47 partial preservation: cotrain regime
is the necessary driver in EngineAG path at high cap. If B at max=256 V14_PASS
→ cap-conditional polarity is truly universal across cotrain/no-cotrain × all
substrates.

## Substrate
| ID | path | ckpt | paradigm |
|----|------|------|----------|
| B_bgla_pretrain_no_cotrain | EngineAG d=1024 GQA 24L (298.76M) | /Users/ghost/.cache/anima/clm_v5_remapped/bg_la_350m_pretrain/ckpts/step_12000_final.pt | naive_pretrain (NO chat-cotrain) |

ckpt sha256_prefix: 4fc6eccce0def045 (per meta.json)

## Run config
- max_cells=256 (sole override vs §47 max=128)
- V4_SEEDS=[42, 137, 271, 314, 1729] paired (strict)
- TRAINED_PROMPT_SEED=42 (same as A in §51)
- n_turns=200 (budget compromise; mission asked 1K-turn but EngineAG cap-free at
  max=256 → first_cap=None expected; race dynamics fully observable in 200 turn
  given A finished at ~85-105s/run)
- snap_every=25
- §30 all-fix mitosis (split_patience=3, split_noise=0.10, merge_threshold=0.005,
  merge_patience=30, lorenz_scale=0.05)
- Phi metric: iit_phi_unnorm_b16 (Fiedler MIP, 16-bin spatial)

## Falsifier
- F-B-MAX256-1: B max=256 V14_VIOLATED (n_beats <= 1) → §47 cotrain regime is
  the EngineAG-path driver for V14 PASS; cap-conditional NOT universal.
  Diagnostic: B.verdict in V14_VIOLATED family (n_beats <= 1).
- F-B-MAX256-2: B cap-bound at max=256 (first_cap_turn != None) → unexpected
  cap dynamics for EngineAG no-cotrain path; mitosis fundamental limit at high
  cap for pretrain-only ckpt.
- F-B-MAX256-3: B partial PASS (n_beats in {3, 4}) → universal claim
  AMBIGUOUS; require larger n.

## Verdict matrix
- **B_PASS_5/5 → ★★★★★ UNIVERSAL_CAP_CONDITIONAL_CONFIRMED**: B 5/5 trained
  beats random at max=256 → cap-conditional polarity truly universal across
  cotrain/no-cotrain × architecture-paths.
- **B_VIOLATED → §47_PARTIAL_PRESERVED**: B 0-1/5 → cotrain regime is the
  necessary driver in EngineAG path; cap-conditional refined to "v2 path universal,
  EngineAG path cotrain-conditional".
- **B_AMBIGUOUS_3-4/5**: direction-only signal at n=5 underpowered; suggest
  larger n follow-up.

## Constraints (raw / own)
- raw#9: training/*.py local-only (gitignored)
- raw#15 additive: B ckpt 미수정 (sha256 verified pre-run)
- : V14 5-seed strict (V4_SEEDS paired)
- : $0 local CPU
- : REBORN.md NOT directly appended — dispatcher injects §56 slot
- : doc save state/anima_v14_max256_b_no_cotrain_2026_05_10/{spec.md,
  result.json, verdict.md, run_b.log}

## Cap-arrival latency cross-verify (§51 mechanism)
§51: in v2 path, trained reaches cap LATER than random (denser representation).
For EngineAG path at max=256, A_phase2_cotrain showed first_cap=None for ALL
6 runs (no cap-bound). B is expected to also be cap-free at max=256 since
pretrain ckpt produces ~40-50 cells terminal in §47 max=128. We will report
max_n_cells_observed and first_cap_turn for trained vs random to verify
EngineAG natural saturation envelope.
