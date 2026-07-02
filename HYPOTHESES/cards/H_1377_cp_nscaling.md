# H_1377 — CP N-SCALING (density-constant dimensional ladder — does the H_1375 D*=3 break vanish?)

**slug** `cp_nscaling` · **tier** 🧱 CURSE-CEILING-TERMINAL (COH_D-DISTINCTNESS; absolute concentration RECOVERS under density but the EARNED/SEPARATION controls collapse) · **DIRECTIONAL** numpy mirror, $0 CPU, 3 seeds [4333,4334,4335], live CORE UNTOUCHED · DECISIVE follow-on to H_1375

## Claim
H_1375 (🧱 BREAKS-AT-D*=3) split the CP move-the-cells law: RELOCATION dimension-invariant, but bounded CONCENTRATION COH_D collapsed monotonically (0.714→0.428→0.201→0.079→0.038) below COH_MIN=0.50 from D=3 — at **CONSTANT N=169**, the classic curse-of-dimensionality signature at a FIXED sample budget. **The open question H_1375 deferred:** is D*=3 a FUNDAMENTAL dimensional ceiling, or purely a constant-N SPARSITY artifact (insufficient investment, c16 cause #3)? **The test:** hold per-dimension sample DENSITY constant (N ∝ c^D) instead of raw N, re-run the ladder. If COH_D recovers → sampling artifact (🟢). If it still breaks → real curse ceiling (🧱). Lens: a_break_the_wall (THIS is the pre-registered breakthrough attempt H_1375 pointed at — "scale N with D"), a_no_llm_frame_trap, a_scale_honest_scope.

## Method (ONLY the sampling rule changes vs H_1375; everything else VERBATIM)
- **Density-constant rule (frozen)**: constant per-axis linear density k = N^(1/D). H_1375 anchor D=2,N=169 = 13/axis → **N(D) = min(N_CAP, round(13^D))**, N_CAP=4000. D=2→169 (= H_1375 anchor, EXACT), D=3→**2197 (UNCAPPED, the DECISIVE rung)**, D=4→4000 (CAPPED; true density-N=28561), D=6→4000 (CAPPED; true 4.8M), D=8→4000 (CAPPED; true 815M). N_CAP is the $0-CPU compute ceiling — D≥4 truncation declared honest up front (a_scale_honest_scope), so the **decisive answer to H_1375's question lives at the UNCAPPED D=3**.
- Metrics (RELOCATION = |ridge_s−c_A'| along normal; COH_D = S_CONC·(1−RIDGE_FRAC), normal-projection spread; KNN=4 discrimination field), 4 arms (RE-PACK eta=.15 / SPLIT-ONLY eta=0 / NO-RETRAIN holds c_A / SHUFFLE), 4 legs c1-c4, all thresholds (LOC_TOL=0.12, COH_MIN=0.50, COH_SEP=0.10, SHUF_COH_MAX=0.20, S_STD_REF=0.20), seeds, hyperplane setup, eta — all VERBATIM from H_1375 / H_1369 R2. NO bar moved. (Whitening second-pass dropped — H_1375 proved it irrelevant; this lane's a_break_the_wall angle IS the N-scaling.)

## Frozen bars (verbatim H_1375; pre-registered — `.verdicts/1377_cp_nscaling/FREEZE.txt`)
Per-D PASS iff (c1) |ridge_s−c_A'|≤0.12 all seeds · (c2) COH_D≥0.50 AND ≥ split-only+0.10 · (c3) no-retrain holds c_A≤0.12 AND shuffle COH_D≤0.20 · (c4) split-only stays short >0.12. Ladder verdict up front: **🟢 DIMENSION-INVARIANT-UNDER-DENSITY** if all D pass; **🧱 CURSE-CEILING-TERMINAL** if COH_D still breaks (decisive rung = UNCAPPED D=3).

## Result — 🧱 CURSE-CEILING-TERMINAL (but the mechanism is NOT a simple sparsity ceiling)

| D | N(D) | RELOCATION \|rs−c_A'\| | COH_D rp/split/shuf | c1 | c2 | c3 | c4 | PASS |
|---|---|---|---|---|---|---|---|---|
| 2 | 169 | 0.008 | 0.714 / 0.297 / 0.045 | ✅ | ✅ | ✅ | ✅ | **PASS** |
| 3 | **2197 (uncapped)** | 0.018 | **0.675** / 0.579 / 0.351 | ✅ | ❌ | ❌ | ✅ | FAIL (c2,c3) |
| 4 | 4000 (CAP) | 0.027 | 0.339 / 0.110 / 0.271 | ✅ | ❌ | ❌ | ❌ | FAIL |
| 6 | 4000 (CAP) | 0.087 | 0.013 / 0.084 / 0.000 | ❌ | ❌ | ❌ | ✅ | FAIL |
| 8 | 4000 (CAP) | 0.048 | 0.000 / 0.000 / 0.000 | ✅ | ❌ | ❌ | ❌ | FAIL |

**DECISIVE RUNG D=3 (uncapped N=2197), the honest mechanism:**
- **c1 RELOCATION ✅** — ridge lands on the moved hyperplane (|rs−c_A'|=0.018); dimension-invariant under density too.
- **c2-RAW (COH_D ≥ COH_MIN) ✅ RECOVERED** — COH_D=**0.675 ≥ 0.50**, vs H_1375 constant-N=0.428 (Δ **+0.247**). The ABSOLUTE bounded concentration the curse killed at constant-N IS restored once density is held constant → the raw "ridge can't stay thin" reading of H_1375's D*=3 break WAS a constant-N sampling artifact.
- **c2-SEP (≥ split-only+0.10) ❌** — re-pack 0.675 vs split-only **0.579**, gap 0.096 < 0.10. Density ALSO concentrates the no-drift control (split-only 0.297→0.579) → the re-pack drift no longer SEPARATES from eta=0.
- **c3 EARNED ❌** — SHUFFLE COH_D jumped 0.045→**0.351** > 0.20. On a dense cloud even random phase-2 labels yield a concentrated KNN discrimination ridge → the anti-Goodhart shuffle control is itself defeated by density.

So density-constant sampling **RESCUES the absolute concentration (c2-raw) but DESTROYS the discriminators (c2-separation + c3-shuffle)** that prove the concentration is EARNED by move-the-cells drift rather than a generic dense-cloud artifact. Same family lesson as H_1374 (RELOCATION robust; the COH concentration-SEPARATION stringency is the fragile part) — here density makes the controls concentrate too.

## Honest verdict (c9)
move-the-cells **RELOCATION** is dimension-invariant under BOTH constant-N (H_1375) AND density-constant (H_1377) sampling. The bounded-COH_D **CONCENTRATION as a DISTINCT, EARNED, control-surviving signal** does NOT clear the frozen 4-leg gate beyond D=2 under either regime: constant-N kills the absolute concentration (H_1375), density-constant rescues the absolute value but collapses the separation+shuffle controls (H_1377). The frozen COH_D-distinctness gate is a D=2 (2-D-axis) result — it does not generalize as a clean PASS up the dimensional ladder under either sampling regime. **🧱 terminal for the COH_D-distinctness ladder; RELOCATION remains 🟢-family.** Crucially this is NOT a naive "sparsity ceiling" — the absolute concentration DID recover under density (answering one half of H_1375's question: the COH-collapse-below-COH_MIN was a sampling artifact); what is terminal is the *distinctness* of that concentration, which neither sampling regime can demonstrate beyond 2-D-axis. NO bar moved.

## Scope (UNVERIFIED — a_scale_honest_scope / a_toy_scale_recheck)
DIRECTIONAL numpy mirror (engine-transfer UNVERIFIED). TOY: Monte-Carlo / 3 seeds / DIM=64 / one normal per seed / deterministic readout. **N_CAP=4000 truncates true density-constant N at D≥4** (28561/4.8M/815M infeasible on $0 CPU) → D=4/6/8 breaks are cap-confounded and NON-decisive; only **D=3 (uncapped N=2197) is decisive**. scale / real-corpus / learned-net / uncapped-high-D / engine-transfer UNVERIFIED. live CORE/*.hexa UNTOUCHED (wires nothing).

## Artifacts
- `state/cp-nscaling/h1377_cp_nscaling.py`
- `.verdicts/1377_cp_nscaling/{FREEZE.txt, result.txt}`

## xref
H_1375 (🧱 constant-N D*=3 break, the parent) · H_1374 (🧱 2-D diagonal, COH-separation axis-aligned-only — same fragility) · H_1369 (🟢 2-D axis, COH2D source + 4-leg gate) · H_1360 (🟢 1-D move-the-cells) · H_1364 (split-only ablation) · H_1343 (RBF population code) · a_break_the_wall · a_no_llm_frame_trap · a_scale_honest_scope · a_toy_scale_recheck · p1 · p2 · p3 · p6 · p7 · c9 · c15 · c16.
