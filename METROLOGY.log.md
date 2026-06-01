# METROLOGY — log

Append-only history sister of `METROLOGY.md`. Each entry starts with `## <ISO> — <header>` (newest on top).

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
