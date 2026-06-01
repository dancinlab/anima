# METROLOGY — log

Append-only history sister of `METROLOGY.md`. Each entry starts with `## <ISO> — <header>` (newest on top).

## 2026-06-02 — PHI-PROXY RE-VERIFICATION SWEEP (post-#1671) — suspect verdicts re-measured, 1 metric-level FLIP
Re-ran every prior verdict/claim that could have consumed the BROKEN variance-partition Cholesky-logdet Φ proxy, using the post-#1671 breakdown-aware measurer (`phi_ok`/`phi_breakdown`/`tier=breakdown_route_to_oracle`). CPU-local, $0, no fire. Full enumeration + flip table + verbatim stdout: `.verdicts/phi_proxy_reverify_1671/` (`REVERIFY_SWEEP.md` + `{composed_rank1,white_ctrl,selftest}_remeasure.txt`). branch `reverify/phi-proxy-sweep`.
- [x] ENUMERATION — the broken family is **variance-partition Cholesky-logdet Φ** only: `BRAIN/tool/module/_metrics/phi_proxy_native.hexa` (EEG native port, the fixed file) + `tool/anima_phi_v3_canonical.hexa` (CLM sister, numpy slogdet). Faithful big-Φ oracle (`HEXAD/IIT4/lib/iit4_bigphi.hexa`, a6/a7) EXCLUDED (not the proxy).
- [x] **KEY SCOPING RESULT**: H_911 3-axis PHI (RED) and B2 HEXAD#10 physics-liveness (FLAT) did NOT use the broken proxy — H_911 uses an **MI-bipartition** `phi_proxy` (`whole−min_bipartition`, `best=1e6` init, finite MI) and B2 uses `edu/cell/phi/phi_iit.hexa` **pairwise-MI** `compute_phi` (clamped ≥0). Neither has the Cholesky `-2147483647` silent sentinel → neither RED is a breakdown artifact. They are real negatives, now TRUSTWORTHY (were suspect-by-association, now CONFIRMED).
- [x] **THE FLIP (metric level, verbatim)**: composed rank-1 (maximally integrated) input → BROKEN proxy emitted bare `-2147483647` with sign-tier `negative_anti_integrated` (silently the MOST anti-integrated, more negative than the white control's −438892). FIXED proxy emits `phi_ok=0 / phi_breakdown=1 / tier=breakdown_route_to_oracle / phi_breakdown_route=HEXAD/IIT4/lib/iit4_bigphi.hexa`. White control stays a REAL low-Φ (`phi_ok=1 phi_x1000=-438892 verdict=PASS`). The prior "lowest-Φ on the most integrated input" was a MEASUREMENT ARTIFACT.
- [x] ORACLE route honored: faithful `iit4_bigphi` (a6) gives big-Φ=**17.66** for the integrated bypass-hub TPM vs **0.0** separable (n=4 engine-exact, 🟢) — the HIGH-Φ-on-integrated the proxy could not produce. 16-node faithful big-Φ = exponential = production-scale → 🟠 DEFERRED (no fire).
- [x] H_912 phi_proxy⊥LZ76 r=−0.277 (already 🔴 REFUTED on-chip #1652/#1653): tier HOLDS; INTERPRETATION sharpens — the negative proxy↔emergence correlation is partly the silent-breakdown artifact on the most-composed inputs, STRENGTHENING the proxy-pathology lineage (H_287/288/294/268/269). H_axisf sync robustness (order-proxy) 🟢 HOLDS — not breakdown-dependent.

## 2026-06-02 — STDLIB FIX (Hc_1302) shipped — FIRST FEEDBACK-MANDATE closure
- [x] Verified the flaw: `phi_proxy_native.hexa` `cholesky_logdet_x1000()` (line ~546, `if diag_x1e6 <= 0 { return F_PHI_01_SENTINEL }`) returns the silent sentinel -2147483647 on low-rank/composed input. Sign-based tiering then reads a metric BREAKDOWN as the MOST anti-integrated (lowest-Φ) input — silent failure.
- [x] Reproduced (verbatim selftest): white `phi_x1000=-173702` (finite) vs structured `phi_x1000=-2147483647` (breakdown). The sentinel is MORE negative than the real white value → composed input silently scored as lowest Φ.
- [x] HONESTY ruling (g5/g63): ridge regularization REJECTED. Ridge sweep on the structured fixture — ridge_x1e6 1e3 (breakdown) → 1e6 phi=-91398 → 1e9 phi=-148000 → 1e12 phi=-222670 → 1e15 phi=-330592 → 1e18 phi=-440992. Φ tracks the ridge magnitude = regulariser artefact, NOT the true Φ. Fake finite number rejected.
- [x] FIX (explicit out-of-band status, option 1b): KV now emits `phi_ok=0` / `phi_breakdown=1` / `tier=breakdown_route_to_oracle` / `phi_breakdown_route=HEXAD/IIT4/lib/iit4_bigphi.hexa`. F_PHI_01 falsifier contract preserved verbatim (phi_x1000 stays -2147483647). White finite path unchanged (phi_ok=1, tier=negative_anti_integrated, verdict=PASS).
- [x] Regression test added to native selftest (white finite vs structured breakdown) — asserts composed case is explicit-breakdown (out-of-band, routed to oracle), never a low-Φ-looking sign tier. selftest GREEN: `__PHI_PROXY_NATIVE__ PASS -173702`.
- [x] `hexa parse` clean (verbatim): `OK: BRAIN/tool/module/_metrics/phi_proxy_native.hexa parses cleanly`.
- [x] Mirror: no hexa-lang `stdlib/consciousness/` copy of this variance-partition proxy exists (that stdlib is IIT4-based) → no mirror needed (recorded honestly).
- [x] SHIPPED: **PR #1671** (merged, squash) https://github.com/dancinlab/anima/pull/1671. **Proves the FEEDBACK MANDATE: a verified metric flaw → a shipped stdlib fix.**

## 2026-06-02 — domain opened (측정자 검증)
- [x] opened METROLOGY: validate the measuring instruments (phi_proxy · faithful big-Φ · concept-margin) themselves
- [x] seed: Hc_1302 🟢 (Φ proxy self-breaks on composed input = metric ceiling) · Hc_1301 🟢 (proxy≠faithful real gap) · X⊥Φ proxy-pathology lineage (H_287/288/294/912)
- [ ] HELD: brainstorm→generate metrology Hc (≥1307)→verify · phi_proxy ceiling boundary map · construct-validity battery · breakdown-floor-guarded richer signal
