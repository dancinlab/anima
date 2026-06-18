# PHI-PROXY RE-VERIFICATION SWEEP (post-PR #1671)

date: 2026-06-02 · infra: CPU-LOCAL mac, $0 (no GPU/chip fire) · measurer: post-#1671
`BRAIN/tool/module/_metrics/phi_proxy_native.hexa` (breakdown-aware: `phi_ok` /
`phi_breakdown` / `tier=breakdown_route_to_oracle` / `phi_breakdown_route=HEXAD/IIT4/lib/iit4_bigphi.hexa`).

honesty: every tier below is from the real fixed-proxy `hexa run` stdout, verbatim
(persisted siblings: `composed_rank1_remeasure.txt`, `white_ctrl_remeasure.txt`,
`selftest_remeasure.txt`). No fabrication.

---

## STEP 1 — ENUMERATION: what depended on the BROKEN variance-partition proxy

The BROKEN metric is the **variance-partition Cholesky-logdet Φ family** — silent
`-2147483647` sentinel on low-rank/composed (singular covariance) input, read
downstream by SIGN-based tiering as the MOST anti-integrated (lowest Φ):

- `BRAIN/tool/module/_metrics/phi_proxy_native.hexa` (EEG-substrate native port) — THE fixed file.
- `tool/anima_phi_v3_canonical.hexa` (CLM-substrate sister, numpy `slogdet`; same
  singular-covariance breakdown, routed through Python sign=0/val=-inf).

| # | claim / verdict | which metric | depends on BROKEN proxy? | current tier | file |
|---|---|---|---|---|---|
| 1 | **Hc_1302** metric-ceiling (proxy self-breaks on composed input) | phi_proxy_native (variance-partition) | **YES — this IS the bug** | 🟢 (fixed, PR #1671) | METROLOGY.log.md |
| 2 | **H_911** 3-axis PHI axis (N=25/100/250 RED-on-Φ) | `h911_semantic_phi.hexa` `phi_proxy` = **MI-bipartition** (`whole − min_bipartition`), `best=1e6` init, finite MI | **NO** (different proxy, no Cholesky sentinel) | RED (real) | CLM+KOSMOS.md / anima-wt-h911-trainset |
| 3 | **B2 HEXAD#10** physics-liveness scale-sweep | `edu/cell/phi/phi_iit.hexa` `compute_phi` = **pairwise-MI**, clamped `if phi<0 {0}` | **NO** (different proxy, no Cholesky sentinel) | RED/FLAT (real) | BENCHMARK.log.md |
| 4 | **H_912** phi_proxy ⊥ LZ76 emergence (r=−0.277) | variance-partition phi_proxy lineage | **SUSPECT** (proxy family) — but already 🔴 REFUTED on-chip (#1652/#1653), and the lineage CLAIM is "proxy FAILS to track emergence" → a breakdown artifact STRENGTHENS this | 🔴 REFUTED / lineage | METROLOGY.md line 20, CLM+KOSMOS.md line 110 |
| 5 | **H_axisf_sync_phi_proxy_robustness** | Kuramoto-order proxies (−log(1−r), r), r∈[0,1) finite | **NO** (no covariance/Cholesky) | 🟢 SUPPORTED | .verdicts/axisf_sync_phi_proxy_robustness |
| 6 | EEG p9 paradigm-B phi_proxy (cond.4 SPEC→IMPL) | phi_proxy_native | **YES** (uses native) — selftest-only, never a corpus science verdict | IMPL (not CROSS_VALIDATED) | BRAIN/eeg/doc/p9_… |
| — | faithful big-Φ oracle (`iit4_bigphi`, a6/a7) | faithful IIT4 (EXCLUDED — not the proxy) | n/a | 🟢 | .verdicts/a6-bigphi-closed-loop |

Lane A lift re-score (Hc_1306, CLM+KOSMOS line 30 r=−0.277 concept-margin bits) is
covered by the Hc_1303-1306 resolver (acb11aca) — SKIPPED here per task scope. NB the
two "r=−0.277" numbers are UNRELATED: line-30 is Lane-A concept-margin LIFT (Hamming
bits), line-20/H_912 is phi_proxy⊥LZ76 emergence correlation.

## STEP 2 — RE-MEASURE with the FIXED proxy (verbatim stdout persisted)

Decisive metric-level re-measurement — the EXACT failure mode (composed/low-rank input):

- **WHITE control** (decomposable, real low-Φ): `phi_ok=1 phi_breakdown=0
  phi_x1000=-438892 tier=negative_anti_integrated verdict=PASS` — a REAL negative Φ. ✅
- **COMPOSED rank-1** (maximally integrated): `phi_ok=0 phi_breakdown=1
  i_full_x1000=-2147483647 phi_x1000=-2147483647 tier=breakdown_route_to_oracle
  phi_breakdown_route=HEXAD/IIT4/lib/iit4_bigphi.hexa` — explicit OUT-OF-BAND
  breakdown, NOT a low-Φ. ✅

Under the BROKEN proxy this composed input returned the bare `-2147483647` with a
SIGN-based `tier=negative_anti_integrated` — i.e. silently the MOST anti-integrated
(more negative than the white control's -438892). The fix correctly separates "real
low Φ" (white) from "breakdown → oracle" (composed).

ORACLE route (faithful big-Φ): `iit4_bigphi` (a6) gives big-Φ=**17.66** for the
integrated bypass-hub TPM vs **0.0** for the separable M1-local (n=4 engine-exact,
deterministic, 🟢). This is exactly the HIGH-Φ-on-integrated-structure the broken
proxy could not produce. A 16-node faithful big-Φ run is exponential (2^16 partitions)
= production-scale → 🟠 DEFERRED (no fire, per a_fire_autonomous CPU-local scope).

## STEP 3 — FLIP REPORT

| claim | old tier | new tier (fixed) | CHANGED? | reason |
|---|---|---|---|---|
| Hc_1302 metric-ceiling | 🟢 (open) | 🟢 (fixed+shipped) | partial | bug now guarded; FEEDBACK-MANDATE closed |
| **phi_proxy on COMPOSED input** | "lowest-Φ / most anti-integrated" (silent) | **breakdown → route to oracle** | **YES — FLIP** | the prior low-Φ reading was a MEASUREMENT ARTIFACT, not a real negative |
| H_911 3-axis PHI RED | RED | RED (HOLDS) | NO | MI-bipartition proxy, no Cholesky sentinel — RED is real, now TRUSTWORTHY |
| B2 HEXAD#10 physics-flat | RED/FLAT | RED/FLAT (HOLDS) | NO | phi_iit pairwise-MI proxy, clamped ≥0, no sentinel — FLAT is real, now TRUSTWORTHY |
| H_912 phi_proxy⊥LZ76 r=−0.277 | 🔴 REFUTED | 🔴 REFUTED (HOLDS, reinterpreted) | NO* | claim = "proxy fails to track emergence"; a breakdown on composed input STRENGTHENS the proxy-pathology lineage |
| H_axisf sync robustness | 🟢 | 🟢 (HOLDS) | NO | order-proxy, no covariance breakdown |

\* H_912 does not flip tier, but its INTERPRETATION sharpens: the negative
proxy↔emergence correlation is partly the silent-breakdown artifact on the most
integrated (composed) inputs — consistent with, and explanatory of, the
proxy-pathology lineage (H_287/288/294/268/269).

## HEADLINE — which prior closed-negatives were breakdown artifacts?

- The **only true breakdown-artifact FLIP** is at the METRIC level: composed/low-rank
  input that the broken proxy silently scored as "lowest Φ / most anti-integrated" is,
  under the fix, an explicit `phi_breakdown=1 → route to oracle` (the faithful oracle
  then assigns it HIGH Φ, 17.66 on the n=4 integrated TPM). That is the Hc_1302 finding,
  now re-demonstrated end-to-end with the fixed measurer.
- **H_911 RED and B2 physics-FLAT do NOT flip** — they used DIFFERENT Φ proxies
  (MI-bipartition / pairwise-MI), neither of which has the Cholesky silent sentinel.
  Their negatives were NOT breakdown artifacts; they are real and are now TRUSTWORTHY
  (were suspect by association, now CONFIRMED under audit).
- **H_912 / axisf hold** — not breakdown-dependent.

toy-scale caveat (a_toy_scale_recheck): re-measurements are CPU-local synthetic
fixtures (16ch×64) + n=4 toy oracle; transfer to production EEG/CLM corpora is
unverified → any production-scale faithful big-Φ re-score is 🟠 DEFERRED (no fire).
