# METROLOGY — log

Append-only history sister of `METROLOGY.md`. Each entry starts with `## <ISO> — <header>` (newest on top).

## 2026-06-02 — instrument-validity pipeline: brainstorm→Hc_1307–1313→verify (branch feat/metrology-pipeline)

Brainstorm depleted in 3 rounds (14 distinct ideas; round-4 >50% paraphrase → STOP). Generated 7 Hc (1307–1313), each ADDING a concrete measurement-validity TEST (not a restatement of the correlational X⊥Φ lineage). Verified $0 CPU-local on the canonical machinery (phi_proxy_native.hexa --input/--selftest · edu/cell/phi/phi_iit.hexa inline · H_278 frozen ledger); verbatim stdout in `.verdicts/metrology_instrument_validity/{1307..1313}.txt`. NO GPU/chip fire dispatched (a_cpu_local_no_waiter).

Verify matrix (Hc × falsifier × tier × key number):

| Hc | falsifier | tier | verbatim finding |
|----|-----------|------|------------------|
| 1307 | F-1307-BOUNDARY | 🟢 | jittered κ-ladder up to κ=5.0e7 ALL FINITE; EXACT rank-1/2 FINITE but EXACT rank-8 → SENTINEL (i_full breaks, k_eval=0). Onset is structure-specific (exact rank≈HID), NOT smooth-in-κ, NON-monotone in rank. |
| 1308 | F-1308-SHUFFLE-NULL | 🟢 | i_full orig=456558 == rowshuf=456558 (byte-identical); phi Δ=0.003% (partition RNG only). Sample-shuffle preserves cov exactly → metric blind to temporal integration. |
| 1309 | F-1309-TWO-FAMILY | 🟢 | MI-coherence white=0.0394 < integrated=0.0910 (finite, ranks higher); Gaussian-logdet on same low-rank class → sentinel -2147483647. Two rulers disagree on composed input. |
| 1310 | F-1310-RIDGE-RESCUE | 🟢 | ridge swept 1e3→1e9 (×1e6) = 1e-3→1000.0 real: sentinel persists at EVERY ridge. i_full itself = sentinel; ×1e6 cov ~1e12 makes ridge ≤1e9 ~1000× sub-noise. Ceiling STRUCTURAL. |
| 1311 | F-1311-FAITHFUL-FLOOR | 🟢 | H_278 ledger: 4/6 scales (rules 110/90/110/110, couplings 0.10/0.20/0.45/0.60) all = 0.000011; 3/6 distinct faithful values. Oracle degenerate in low-Φ floor. |
| 1312 | F-1312-BATTERY | 🟢 | construct-validity fingerprint {a:FAIL · b:HOLD · c:FAIL · d:FAIL}; 0/4 clean passes → phi_proxy_native is a covariance statistic, not a construct-valid integration measure. |
| 1313 | F-1313-SCALE-TRANSFER | 🟠 | DEFERRED — production D=768 CLM hidden-state dump needs a model forward pass; no $0 CPU path; NO fire. Toy verdicts scoped to n=16. |

counts: 🟢 6 · 🟠 1 · 🔴 0. Discovery log: `.discoveries/metrology_instrument_validity.tape`.

Headline: the canonical Gaussian-logdet Φ proxy is NOT construct-valid — it BREAKS (structurally, un-rescuable) on the maximally-composed inputs it should score, is mathematically BLIND to temporal integration, disagrees with the other Φ family, and even the faithful oracle is degenerate in the low-Φ band. The Lane A weak-lift "no lift" closed-negative inherits all of these caveats.

## 2026-06-02 — domain opened (측정자 검증)
- [x] opened METROLOGY: validate the measuring instruments (phi_proxy · faithful big-Φ · concept-margin) themselves
- [x] seed: Hc_1302 🟢 (Φ proxy self-breaks on composed input = metric ceiling) · Hc_1301 🟢 (proxy≠faithful real gap) · X⊥Φ proxy-pathology lineage (H_287/288/294/912)
- [ ] HELD: brainstorm→generate metrology Hc (≥1307)→verify · phi_proxy ceiling boundary map · construct-validity battery · breakdown-floor-guarded richer signal
