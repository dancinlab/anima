---
id: Hc_1307
slug: phi-proxy-cholesky-breakdown-boundary-map
title: The phi_proxy Cholesky-breakdown sentinel is NOT a smooth function of condition number nor monotone in rank — it fires only on EXACT rank-deficiency near rank==HID, a structure-specific (not kappa-threshold) boundary
domain: metrology, consciousness, integration, methodology
status: candidate-unverified
source_doc: METROLOGY.md @goal + Hc_1302 seed; live boundary sweep on phi_proxy_native.hexa --input (2026-06-02)
seed: Hc_1302 established the metric HAS a ceiling (sentinel on composed input). The natural next metrology question — WHERE exactly is the boundary? Map sentinel onset against input rank and covariance condition number kappa to characterize the blind region.
promoted_at: 2026-06-02
linked_h: Hc_1302 (metric-ceiling seed), Hc_1301, phi_proxy_native (anima_phi_v3_canonical sample-partition Phi-star port)
verdict_tier_target: 🟢 numerical (CPU-local phi_proxy_native --input on rank/kappa-controlled npy fixtures)
notes: "ADDS a concrete boundary-characterization test the X-perp-Phi lineage (H_287/288/294/912) never ran — they were correlational; this maps the breakdown surface directly. Distinct from Hc_662/665 (architecture-agnosticism/dim-dominance)."
---

## Hypothesis

Hc_1302 showed phi_proxy_native returns the F_PHI_01 sentinel (-2147483647) on a maximally-
composed (low-rank) input. WHERE is the boundary? Naively one expects the sentinel to onset
smoothly as the covariance becomes ill-conditioned (high condition number kappa) or as input
rank drops.

CLAIM: the boundary is NOT smooth in kappa and NOT monotone in rank. Because the metric scales
floats x1e6 and adds a ridge before a fixed-point Cholesky, merely ILL-CONDITIONED input (high
kappa, numerically full-rank) stays FINITE; the sentinel requires EXACT rank-deficiency, and
fires specifically when the algebraic rank drops at/below the HID truncation (HID = min(C, N//2)),
where the HID x HID covariance becomes exactly singular. The blind region is therefore a
structure-specific exact-degeneracy threshold, not a condition-number cut.

## PRE-REGISTERED Falsifier

- **F-1307-BOUNDARY**: build (i) a jittered condition-number ladder (eps=1e-3, numerically
  full-rank, kappa from ~7 to ~5e7) and (ii) EXACT rank-deficient fixtures (rank 1, 2, 8),
  run phi_proxy_native --input on each. PASS (structure-specific threshold) = the jittered
  high-kappa inputs stay FINITE while the EXACT rank-deficient inputs show a SHARP, non-monotone
  onset (sentinel at exact rank-8 but finite at exact rank-1/2). FALSIFIED (smooth-in-kappa) =
  the sentinel onsets monotonically as kappa rises, with a clean kappa threshold predicting it.

## Honest Limits

- **L-1307-TOY**: 16ch x 64samp toy geometry; the exact rank at which HID-singularity fires is
  scale-dependent (HID=min(C,N//2)). Transfer to production D=768 is DEFERRED (Hc_1313).
- **L-1307-FIXEDPOINT**: the finite-on-high-kappa behavior is partly a fixed-point x1e6 scaling
  effect; a float64 slogdet backend might onset differently. The pure-native path is the contract.

## Cross-Links

- **sibling Hc**: Hc_1302 (ceiling seed), Hc_1310 (ridge does not rescue), Hc_1312 (battery axis a)
- **metric**: BRAIN/tool/module/_metrics/phi_proxy_native.hexa
- **verdict**: .verdicts/metrology_instrument_validity/1307.txt
