# BG-V14-MAX256-CE-STRICT-N5 — C + E n=5 strict upgrade at max=256

## ts
2026-05-10 (5-star pursuit cycle, post §51 PARTIAL → FULL upgrade)

## Mission
§51 BG-V14-MAX256-CAP-FREE-MULTI delivered ★★★★★ PARTIAL (n=2 underpowered for
v2 substrates):
- A_phase2_cotrain: 5/5 V14_PASS (full)
- C_cells64_aware:  2/2 V14_PASS (n=2, sign-p=0.5)
- E_convo5k_ft:     2/2 V14_PASS (n=2, sign-p=0.5, mirrors reused from C)

★★★★★ FULL upgrade prereq: **C + E n=5 strict at max=256**.

This BG closes the n=5 gap by running the 3 missing mirror seeds
[271, 314, 1729] at max_cells=256, n_turns=100 — only ONCE (shared between
C and E) thanks to the deterministic ckpt-independent mirror property of
the v2 path verified empirically in §51 (E-s42 turn 50 phi == C-s42 turn 50
phi exactly).

## Substrates
| ID | path | ckpt | sha256 |
|----|------|------|--------|
| C_cells64_aware | v2 d=384 6L heads=6 | state/anima_clm_v2_mitosis_cells_recovery_2026_05_09/cells64_final.pt | 61e1d735... |
| E_convo5k_ft | v2-derived d=384 6L byte-level | state/anima_convo_5k_ft_extended_2026_05_10/post_ft_ext_ckpt.pt | 608d38a5... |

## Run config (matches §51 exactly)
- max_cells=256
- n_turns=100
- snap_every=25
- prompt_seed=2026 (v2 path)
- §30 all-fix: A1 dispersion ON, A2 per_cell_threshold ON, B1 ratchet ON, D1 lorenz_auto ON
- TRAINED ckpts unchanged → reuse §51 cached trained_phi (deterministic; verified)
- mirrors run: NEW seeds [271, 314, 1729] only (s42, s137 cached from §51)

## Seed plan
| seed | source |
|------|--------|
| 42   | §51 cached (mirror_runs[0] in result_C/E.json) |
| 137  | §51 cached (mirror_runs[1] in result_C/E.json) |
| 271  | NEW this BG, shared C+E |
| 314  | NEW this BG, shared C+E |
| 1729 | NEW this BG, shared C+E |

## Determinism precondition (sanity_s42_short.py)
Re-run mirror s42 for 51 turns. Expected: turn-50 phi = 1886.851 (§51 claim).
Sanity result: phi = 1886.8508414 (abs diff 0.0002, 0.000% relative). PASS.
F-CE-STRICT-2 NOT fired → mirror reuse legitimate.

## Falsifier
- F-CE-STRICT-1 (★★★★★ FULL FAIL): C 5/5 fails → ★★★★★ FULL not reached. If
  C n_beats < 5 OR E n_beats < 5 at max=256, FULL claim falsified.
- F-CE-STRICT-2 (DETERMINISM CLAIM FAIL): mirror s42 re-run produces different
  trajectory than §51 cached → reuse invalid → must run all 5 seeds fresh per
  substrate. Sanity step gates this BG; PASSED at start.
- F-CE-STRICT-3 (PARTIAL_STRONG): both C and E land 4/5 (sign-p=0.0625) →
  ★★★★★ PARTIAL_STRONG, FULL miss but stronger than §51's n=2 partial.

## Verdict matrix (post hoc)
- **★★★★★ FULL**: C n_beats == 5 AND E n_beats == 5 (sign-p=0.0625 both)
  → universal cap-conditional PASS strict at n=5 across both v2 substrates
- **★★★★★ PARTIAL_STRONG**: C n_beats >= 4 AND E n_beats >= 4 (one or both
  is 4/5, sign-p=0.0625 or 0.375)
- **★★★★ partial-only**: either C n_beats <= 2 OR E n_beats <= 2 → universal
  claim weakened; substrate-specific result

## raw / own
- raw#9: training/v5mitosis_d384_v14_mirror.py local-only (gitignored)
- raw#15 additive: 2 ckpts unmodified (sha256 verified pre-run, matches §51)
- own 14: V14 5-seed strict per substrate (C, E)
- own 16: $0 local CPU
- own 22: REBORN.md NOT directly appended — dispatcher injects §52 slot
- own 38: doc save to state/anima_v14_max256_ce_strict_n5_2026_05_10/{spec.md, result.json, verdict.md, run_n5_strict.py, sanity_s42_short.py, run_n5.log, run_n5.stdout}
