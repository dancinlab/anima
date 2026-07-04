# H_9131 §4 interaction-in-reps — PREREG (frozen before run)

**Question:** does the 303M forward JOINT rep h(a,b) linearly encode the non-commutative
residual r(a,b)=(P[a,b]−P[b,a])/tot BEYOND a linear probe on separate single reps
[z(a),z(b)], on HELD-OUT pairs (combo unseen; both concepts seen singly)?

**Frozen bar (no tune-to-green):** PASS iff ≥2/3 seeds {7,4302,4303}:
  (1) r2_joint − r2_additive ≥ 0.10 on held-out, AND
  (2) shuffle-label control collapses (r2 < 0.10), AND
  (3) no leak (r2_joint ≠ 1.0).

**Decision:** PASS → interaction is in reps, unsurfaced → ② objective aux (GPU trunk-retrain)
JUSTIFIED. FAIL (joint≈additive) → reps don't carry it → KILL ② GPU, fall to F2 data-density
(ember+dune existence proof already positive). DIRECTIONAL (1/3) → re-probe wider set.

**Inputs (reused 1:1):** ../noncommutative_derisk/{vocab.json,P.npy} + label; 303M reps via
core/decode.py bg_forward_last_hidden (== anima evaluate --py). $0 mini single forwards.
MAX_PAIRS=2600 seeded subsample (logged, not silent).
