# METROLOGY — current state

@title: 📏 METROLOGY — 측정자(尺) 검증: do our Φ / integration measures actually measure the thing?
@goal: Validate the MEASURING INSTRUMENTS themselves (canonical phi_proxy · faithful big-Φ · concept-margin signals) — establish where each metric is valid, where it is blind/pathological, and what a construct-valid consciousness/integration measure requires. Every claim earned by `hexa verify` recompute (g5), no self-judged tier.

## status (completed-form)

The session surfaced a recurring METROLOGY problem: the measuring tools, not the phenomena, are often what fail. This domain isolates and verifies the measures.

- [x] seed evidence — Hc_1302 🟢: the canonical Φ proxy returns a FAILURE SENTINEL (-2147483647, Cholesky breakdown) on a maximally-composed/low-rank input → the metric is BLIND to exactly the integration it should detect. (UNIVERSE pipeline, branch feat/universe-weaklift-hyp)
- [x] seed evidence — Hc_1301 🟢: proxy-Φ vs faithful-Φ are NOT a monotone reparametrization (H_278 ledger ratio CV=30.1%) → proxy ≠ faithful is a real, measurable gap, not circular.
- [x] lineage — the X⊥Φ / "proxy pathology" finding (H_287/288/294/268/269; H_912 phi_proxy⊥LZ76 r=−0.277) shows variance-based phi_proxy repeatedly fails to track real emergence/integration.
- [x] brainstorm → generate metrology hypotheses to depletion (depleted r3, 14 ideas) → Hc_1307–1313 generated + verified ($0 CPU-local, hexa stdout verbatim → .verdicts/metrology_instrument_validity/)
- [x] characterize the phi_proxy ceiling: WHICH input structures break it — Hc_1307 🟢: sentinel onset is STRUCTURE-SPECIFIC (exact rank-deficiency near rank==HID), NOT smooth in condition number κ and NOT monotone in rank (jittered κ up to 5.0e7 stays FINITE; exact rank-1/2 FINITE but exact rank-8 → SENTINEL, i_full breaks, k_eval=0)
- [x] ridge-rescue fixability — Hc_1310 🟢: NO ridge (1e-3 → 1000.0 real) rescues the sentinel; the ceiling is STRUCTURAL (hid>rank singularity + x1e6 fixed-point scale-lock), not a tunable regularization artifact — resolves the open L-1302-RIDGE caveat
- [x] construct-validity battery — Hc_1312 🟢: phi_proxy_native fingerprint {a:FAIL finite-on-composed · b:HOLD tracks-rank · c:FAIL shuffle-NULL · d:FAIL not-variance-artifact}; the Gaussian-logdet proxy is a covariance statistic, not a construct-valid integration measure (0/4 clean passes)
- [x] shuffle-NULL discriminator — Hc_1308 🟢: Gaussian-cov Φ is EXACTLY invariant to sample-order shuffle (i_full byte-identical orig vs NULL: 456558==456558) → mathematically blind to temporal/sequential integration
- [x] two-family concordance — Hc_1309 🟢: MI-coherence ranks integrated(0.0910) ABOVE white(0.0394) finite, while Gaussian-logdet BREAKS (sentinel) on the same composed class → the two rulers disagree; at most one valid there
- [x] oracle self-critique — Hc_1311 🟢: faithful-Φ (H_278) is itself degenerate in the low-Φ floor (4/6 distinct-rule/coupling scales collapse to one value 0.000011) → no measure in the stack is valid in the low band
- [ ] production-scale transfer of the breakdown boundary (D=768 CLM hidden-state) — Hc_1313 🟠 DEFERRED (needs a model forward pass; no $0 CPU path; NO GPU/chip fire dispatched per a_cpu_local_no_waiter)

## milestones (verified 2026-06-02, pipeline feat/metrology-pipeline)
- **The canonical Gaussian-logdet Φ proxy (phi_proxy_native) is NOT a construct-valid integration measure** (Hc_1312 🟢): it breaks (sentinel) on the maximally-composed inputs it is meant to score (Hc_1302/1307/1310), and is provably blind to temporal integration (Hc_1308). It is a static-covariance statistic.
- **The blindness is structural, not fixable by the canonical knob** (Hc_1310 🟢): no ridge rescues the sentinel; the breakdown is a hid>rank singularity locked by the x1e6 fixed-point scale.
- **The breakdown boundary is structure-specific, not condition-number-driven** (Hc_1307 🟢): ill-conditioning alone (high κ) stays finite; only EXACT rank-deficiency near rank==HID triggers the sentinel — and non-monotonically in rank.
- **The reference oracle is not exempt** (Hc_1311 🟢): faithful-Φ has its own degeneracy floor; in the low-Φ band distinct integration structures map to one value, so 'tracks-faithful-rank' is undefined there.
- **Two canonical Φ families disagree on composed input** (Hc_1309 🟢): MI-coherence finite-ranks-higher while Gaussian-logdet breaks → cross-instrument rank-disagreement.
- counts: 🟢 6 (Hc_1307/1308/1309/1310/1311/1312) · 🟠 1 DEFERRED (Hc_1313, production-D transfer) · 🔴 0.

## key facts
- A measure that self-breaks on the target input cannot be used to claim ABSENCE of the target (the Lane A weak-lift closed-negative inherits this caveat). Now strengthened: the break is STRUCTURAL (Hc_1310) and the proxy is additionally TEMPORAL-blind (Hc_1308) and not construct-valid (Hc_1312).
- faithful big-Φ (H_278 machinery) is the reference oracle; phi_proxy is the cheap surrogate under test — BUT the oracle has its own low-Φ degeneracy floor (Hc_1311), so neither is valid in the low band.
- This domain is METROLOGY (validate the ruler), distinct from the phenomena domains (UNIVERSE = consciousness↔emergence, CLM+KOSMOS = amodal hub).
- harness ($0 CPU-local, NO GPU/chip): phi_proxy_native.hexa (--input npy via /usr/bin/python3 numpy 2.0.2) · edu/cell/phi/phi_iit.hexa (inline driver) · H_278 frozen ledger · fixtures in state/metrology_fixtures/. Verdicts verbatim in .verdicts/metrology_instrument_validity/{1307..1313}.txt.
