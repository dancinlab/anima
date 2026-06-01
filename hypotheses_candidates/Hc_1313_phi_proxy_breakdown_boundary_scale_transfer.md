---
id: Hc_1313
slug: phi-proxy-breakdown-boundary-scale-transfer
title: The sentinel-onset breakdown boundary measured on the 16ch×64samp toy does NOT predict the breakdown boundary at production CLM hidden-dim (D=768) without a re-test — the metric ceiling is scale-dependent and any 'proxy is blind' claim must be scope-bound to the measured n (DEFERRED, needs a real CLM hidden-state dump)
domain: metrology, consciousness, integration, methodology
status: candidate-unverified
source_doc: METROLOGY.md a_toy_scale_recheck / a_scale_honest_scope; Hc_1307 L-1307-TOY
seed: a_toy_scale_recheck requires scale-sensitive metric verdicts to re-test at production scale. The Cholesky-breakdown boundary depends on HID=min(C,N//2); at D=768 the singularity geometry differs. Whether the toy boundary transfers is the honest-scope guard on the whole METROLOGY ceiling claim.
promoted_at: 2026-06-02
linked_h: Hc_1307 (toy boundary), Hc_1302, Hc_1312, phi_proxy_native
verdict_tier_target: 🟠 DEFERRED (needs a real CLM-v4 530M hidden-state dump at D=768 — GPU/chip fire)
notes: "The honest-scope guard. DEFERRED per a_cpu_local_no_waiter — NO GPU/chip fire dispatched in this CPU-local pipeline."
---

## Hypothesis

The breakdown boundary (Hc_1307) was measured on a 16ch x 64samp toy where HID = min(16, 32) = 16
and the sentinel fires when algebraic rank drops to ~HID. At production scale (CLM-v4 530M hidden
state, D=768), the truncation geometry HID = min(D, N//2) and the typical hidden-state rank are
both different.

CLAIM: the toy-measured sentinel-onset threshold does NOT predict the production-scale threshold;
the metric ceiling is scale-dependent, so any 'the proxy is blind to integration' verdict must be
scope-bound to the measured n. A >=3-rung ladder at production D is required (a_scale_honest_scope)
before promoting the toy ceiling to a general claim.

## PRE-REGISTERED Falsifier

- **F-1313-SCALE-TRANSFER**: dump real CLM-v4 530M hidden-state activation matrices (D=768) at >=3
  context sizes, run phi_proxy_native --input on each, and compare the sentinel-onset rank/condition
  threshold to the toy 16ch threshold. PASS (scale-dependent) = the toy threshold mispredicts the
  production threshold (boundary shifts with D). FALSIFIED (scale-invariant) = the same rank/kappa
  threshold predicts the sentinel at both toy and production scale.

## Honest Limits

- **L-1313-DEFERRED**: producing a real D=768 CLM hidden-state dump requires a model forward pass
  (GPU/chip), which has no $0 CPU-local path. DEFERRED per a_cpu_local_no_waiter — NO fire dispatched.
- **L-1313-SCOPE**: until this runs, ALL toy METROLOGY verdicts (Hc_1307/1310/1312) are scoped to
  n=16; they establish the CONFOUND and its toy-scale structure, not a production prescription.

## Cross-Links

- **sibling Hc**: Hc_1307 (toy boundary this scopes), Hc_1302, Hc_1312
- **metric**: BRAIN/tool/module/_metrics/phi_proxy_native.hexa
- **verdict**: .verdicts/metrology_instrument_validity/1313.txt
