# SIM lane -- IIT4 big-Phi probe sources (regenerated 2026-05-29)

> Reproducibility sources (run.hexa + run.log + result.json) for the 10 SIM probes.
> Numbers already merged in s_catalog_2026_05_29/S_CATALOG_MATRIX.md (#1386); this dir
> restores the run sources lost to a concurrent worktree sync.
>
> Substrate: ECA n=4, GZ inhibition I=0.21232 applied as TPM scale (1-I).
> Engine: iit4_bigphi.big_phi(tpm, n, state)[0], max over 2^n states.
> HEXA_LANG=/Users/ghost/core/hexa-lang-buildmain, deterministic, $0, mac-local.
> Engine cross-check: coupled rule110 n=4 = 14.1492 (reproduced exactly,
> 14.149200000000001) -- every probe re-derives this as the determinism anchor.
> All regenerated numbers MATCH the #1386 targets (no discrepancy).

| id | hypothesis | key Phi (regenerated = #1386 target) | verdict |
|---|---|---|---|
| S10 | panpsychism (uncoupled->Phi0) | IDENTITY/NOT/CONST = 0.0 each; coupled rule110 = 14.1492 | SUPPORTED-NUMERICAL |
| S11 | single-cell Phi | Phi(n=1..4) = [0.0, 0.10246, 5.14627, 14.1492] | SUPPORTED-NUMERICAL |
| S14 | time-scale (x100) | 1-step = 14.1492; 2-step = 7.38843; 16/16 states differ | SUPPORTED-NUMERICAL |
| S24 | distributed (exclusion) | whole = 14.1492; severed = 0.0; drop = 100% | SUPPORTED-NUMERICAL |
| S6  | merge | parts-sum = 0.20492; merged n=4 = 14.1492; abs-delta = 13.9443 | SUPPORTED-NUMERICAL (non-additive) |
| S7  | split | whole n=4 = 14.1492; pieces-sum = 0.20492 | SUPPORTED-NUMERICAL (not conserved) |
| S15 | evolution curve | rule90 = 0.20492; 184 = 19.9378; 110 = 14.1492; 30 = 17.8619 (non-monotone) | SUPPORTED-NUMERICAL |
| S26 | hive mind | I=0.05 -> 19.0933; 0.21232 -> 14.1492; 0.45 -> 9.50722 | SUPPORTED-NUMERICAL |
| S28 | conway/ECA spectrum | rule {30=17.8619, 54=8.23847, 90=0.20492, 110=14.1492, 184=19.9378} | SUPPORTED-NUMERICAL |
| S39 | free will (Libet) | pred_accuracy(t-1->t) = 1.0 (16/16); max big-Phi = 14.1492 | SUPPORTED-NUMERICAL |

**Finding clusters (mirrors matrix S5):** S24 distributed-consciousness closed-negative;
S10/S11/S7/S6 coupling-necessary cluster (Phi needs irreducible causal coupling, not matter
or size); S39 deterministic-integration (predictable orthogonal to Phi>0); S15/S28
substrate-(rule-)dependence with non-monotone complexity ordering.

**hexa gotchas (for future regen):** no ternary ?: operator (use if/else); `drop` is a
reserved keyword; unary `!` not supported (use `== false`).
