---
id: Hc_1310
slug: phi-proxy-ceiling-structural-not-ridge-rescuable
title: No finite ridge rescues the phi_proxy Cholesky sentinel — sweeping the regularizer from 1e-3 to 1000.0 leaves the breakdown intact because the full-sample covariance is exactly rank-deficient (hid>rank) and the x1e6 fixed-point scale makes the ridge ~1000x sub-noise — the metric ceiling is STRUCTURAL, not a tunable artifact
domain: metrology, consciousness, integration, methodology
status: candidate-unverified
source_doc: METROLOGY.md milestone "breakdown-floor-guarded richer signal"; Hc_1302 L-1302-RIDGE caveat
seed: Hc_1302 noted (L-1302-RIDGE) that a larger ridge MIGHT rescue the sentinel. If true, the ceiling is a fixable regularization artifact and a guarded richer signal is recoverable. If no ridge rescues, the blindness is structural. Test the ridge knob directly.
promoted_at: 2026-06-02
linked_h: Hc_1302 (ceiling seed + ridge caveat), Hc_1307 (boundary), phi_proxy_native
verdict_tier_target: 🟢 numerical (CPU-local phi_proxy_native --input exact_rank08 --ridge-x1e6 sweep)
notes: "Directly resolves the open L-1302-RIDGE caveat with a measurement. ADDS a fixability test the lineage never posed."
---

## Hypothesis

The phi_proxy_native Cholesky core returns F_PHI_01 when a diagonal pivot goes non-positive
(matrix not PD). The metric adds a ridge (default ridge_x1e6=1000, i.e. 1e-3 real) to the
covariance diagonal before factorizing. Hc_1302 left open whether a larger ridge rescues the
sentinel.

CLAIM: NO finite ridge in the canonical range rescues the sentinel on an exactly rank-deficient
input. Root cause: (i) the FULL-sample covariance itself is exactly singular when algebraic
rank < HID, so i_full breaks before any partition; (ii) the metric scales floats x1e6 then forms
the covariance, so cov diagonal entries are ~1e12 in fixed-point, making even a ridge of 1e9
(x1e6 = 1000.0 real) roughly 1000x sub-noise on the diagonal. The breakdown ceiling is therefore
STRUCTURAL (a hid>rank singularity, scale-locked), not a tunable regularization artifact.

## PRE-REGISTERED Falsifier

- **F-1310-RIDGE-RESCUE**: on the exact rank-8 fixture that returns the sentinel (Hc_1307), sweep
  --ridge-x1e6 over 1e3, 1e4, ... 1e9. PASS (structural) = the sentinel PERSISTS at every ridge
  (no finite ridge yields a finite phi_x1000). FALSIFIED (rescuable) = some finite ridge converts
  the sentinel to a finite, well-ordered phi_x1000 -> the ceiling is a fixable regularizer artifact.

## Honest Limits

- **L-1310-FIXEDPOINT**: the non-rescue is partly a fixed-point x1e6 scaling interaction; a
  float64 slogdet backend with a proportional ridge could rescue. The claim is scoped to the
  canonical pure-native fixed-point metric as deployed.
- **L-1310-EXACT**: tested on EXACTLY rank-deficient input; merely ill-conditioned input does not
  hit the sentinel at all (Hc_1307), so the ridge question only arises in the exact-degeneracy band.

## Cross-Links

- **sibling Hc**: Hc_1302 (resolves L-1302-RIDGE), Hc_1307 (boundary), Hc_1312 (battery axis a)
- **metric**: BRAIN/tool/module/_metrics/phi_proxy_native.hexa
- **verdict**: .verdicts/metrology_instrument_validity/1310.txt
