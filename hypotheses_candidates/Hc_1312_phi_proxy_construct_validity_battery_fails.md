---
id: Hc_1312
slug: phi-proxy-construct-validity-battery-fails
title: Construct-validity 4-axis battery — phi_proxy_native FAILS (a) finite-on-composed, (c) survives-shuffle-NULL, (d) not-a-variance-artifact and cannot certify (b) tracks-faithful-rank; fingerprint {a:FAIL, b:HOLD, c:FAIL, d:FAIL} — the canonical Gaussian-logdet proxy is a covariance statistic, not a construct-valid integration measure
domain: metrology, consciousness, integration, methodology
status: candidate-unverified
source_doc: METROLOGY.md milestone "construct-validity battery"; aggregates Hc_1302/1307/1308/1309/1310/1311
seed: The METROLOGY @goal demands a measure pass a 4-axis gate to count as construct-valid: (a) finite-on-composed, (b) tracks faithful-Phi rank, (c) survives a shuffle-NULL as a discriminator, (d) not a pure variance/covariance artifact. Run all four on phi_proxy_native and report the fingerprint of which axes fail.
promoted_at: 2026-06-02
linked_h: Hc_1302, Hc_1307, Hc_1308, Hc_1309, Hc_1310, Hc_1311, phi_proxy_native
verdict_tier_target: 🟢 numerical (CPU-local — aggregates the four axis verdicts into the battery)
notes: "The integrative headline of the METROLOGY domain. ADDS a SYSTEMATIC construct-validity gate (4 concrete tests) the single-axis X-perp-Phi lineage never assembled."
---

## Hypothesis

A measure is construct-valid for integration only if it passes ALL of: (a) FINITE on a
maximally-composed (low-rank) input; (b) TRACKS the faithful-Phi rank ordering; (c) a shuffle-NULL
that destroys integration DROPS its score (it DISCRIMINATES); (d) it is NOT a pure variance /
covariance artifact (carries integration info beyond the second moment).

CLAIM: phi_proxy_native FAILS at least one axis. Specifically the fingerprint is
{a: FAIL, b: HOLD, c: FAIL, d: FAIL}:
- (a) FAIL — composed/low-rank input returns the F_PHI_01 sentinel (Hc_1302/1307), structurally
  (no ridge rescues, Hc_1310).
- (b) HOLD — rank-concordant on H_278 but ratio-CV 30.1% (Hc_1301) AND the faithful oracle is
  itself degenerate in the low-Phi floor (Hc_1311), so 'tracks-rank' is uncertifiable.
- (c) FAIL — phi(orig) == phi(sample-shuffled NULL) (Hc_1308); the metric does not discriminate
  an integrated signal from its temporally-shuffled NULL.
- (d) FAIL — phi depends only on the static covariance (sample-order invariant, Hc_1308) and the
  other Phi family disagrees on composed input (Hc_1309); it is a 2nd-moment statistic.

## PRE-REGISTERED Falsifier

- **F-1312-BATTERY**: assemble the four axis verdicts (Hc_1307/1308/1309/1310/1311 + Hc_1301).
  PASS (battery validated) = phi_proxy_native FAILS >= 1 axis, and the fingerprint is reported.
  FALSIFIED (fully construct-valid) = phi_proxy_native PASSES all four axes (finite-on-composed
  AND tracks-rank AND shuffle-discriminates AND not-a-variance-artifact).

## Honest Limits

- **L-1312-AGGREGATE**: this is a meta-verdict aggregating five axis runs; each axis carries its
  own toy-scale / fixed-point caveats (see the per-axis L-notes). The battery DESIGN is the
  contribution; the fingerprint is scoped to the toy substrate.
- **L-1312-AXIS-B**: axis (b) is HOLD (not FAIL) because the oracle degeneracy (Hc_1311) makes
  'tracks-rank' undefined in the low band, not because the proxy passed it.

## Cross-Links

- **sibling Hc**: Hc_1302, Hc_1307, Hc_1308, Hc_1309, Hc_1310, Hc_1311 (the axis providers)
- **metric**: BRAIN/tool/module/_metrics/phi_proxy_native.hexa
- **verdict**: .verdicts/metrology_instrument_validity/1312.txt
