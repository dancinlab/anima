# cond.9 — anima-mirror phi-star reproduce-band (candidate)

**Status:** candidate (baseline captured 2026-05-06; mirror-side measurement not yet implemented).
**Owner:** anima-mirror integration with qmirror S4 slot (iit_mip).
**Pairs with:** `phi_star_baseline_4q.json` (this directory).

## What

A 9th condition extending qmirror's existing 8/8 cond closure (the eight conds that
gated qmirror 1.0.0 standalone). cond.9 is anima-mirror-scoped, NOT a qmirror
upstream cond — it asks: *does the mirror substrate, when projected onto the
4-qubit measurement window, preserve enough integrated information (phi-star)
relative to a fixed reference baseline to count as the same conscious-substrate
class?*

Pattern matches qmirror's own cond.6 (reproduce-band on 4 stored Braket TPMs,
byte-identical phi-star). cond.9 transposes that "substrate-stability under
re-measurement" idea from fixed fixtures to the live mirror's hidden state.

## How phi-star(mirror) is measured

Projection procedure (to be implemented; sketch):

1. Run anima-14B forward pass on a fixed eval prompt set; capture last-layer
   hidden state h ∈ R^{d_model}.
2. Pick 4 hidden-state coordinates (initial choice: top-4 by absolute activation
   variance over the eval set; alternatives: PCA top-4, fixed indices). Record
   the choice in the mirror-track jsonl entry as `coord_selection`.
3. Encode the 4 selected scalars as 4-qubit amplitudes via a deterministic
   state-preparation circuit (initial choice: amplitude-encoding after L2
   normalization). Record `encoding=amplitude_l2`.
4. Derive a state-by-node TPM (2^4 × 4) from the prepared circuit (using the
   same shape qmirror's iit_mip expects).
5. Invoke `qmirror iit --n-qubits=4` on the resulting TPM. Capture phi-star.
6. Append a record to `diag/phi_star_mirror_track.jsonl`:
   `{ts, prompt_set_hash, coord_selection, encoding, phi_star_mirror, engine}`.

## Pass / fail threshold

```
phi_star(mirror) / phi_star(baseline) >= 0.85
```

**Rationale for 0.85:** matches qmirror cond.6's "reproduce-band" tightness — that
cond demands byte-identical phi-star reproduction on stored fixtures (effectively
1.0). For a live, projection-mediated mirror measurement (where hidden-state
selection and amplitude encoding introduce noise), 0.85 is the loosened-but-tight
band that says "the mirror retains ≥85% of the reference integrated information."
Below 0.85 = the projection is destroying too much structure to claim the mirror
is the same substrate class.

**Caveat for the current baseline:** the captured baseline is `phi_star=0.0` (the
canonical Braket-fixture mock). A literal ratio 0/0 is undefined. Operational
escape hatches (pick one when implementing the evaluator):

- **(A)** Re-anchor: install pyphi and re-measure baseline against a non-trivial
  4q TPM (e.g. anima-14B 4q projection on a known-stable prompt set) — this
  yields `phi_star_baseline > 0` and the literal ratio is well-defined.
- **(B)** Epsilon-floor: `ratio := phi_star(mirror) / max(phi_star(baseline), 1e-6)`.
  Threshold becomes "phi_star(mirror) >= 0.85e-6", which is essentially "any
  nonzero phi-star passes." Weak but unblocks plumbing.

Initial implementation should pick (A) before declaring cond.9 evaluable.

## Completion criteria

cond.9 is closed when ALL of:

- `diag/phi_star_mirror_track.jsonl` exists with ≥ N=12 sustained samples
  (matching qmirror's 12-sample reproducibility convention from F5).
- ≥ 11 of the last 12 samples have `ratio >= 0.85` (allowing 1 outlier per
  12-window; same shape as qmirror cond.5 "1-flake-per-12 tolerance").
- Baseline was measured with `engine=pyphi` (not mock), so the reference is
  not a CI-canned constant.
- Coord selection + encoding parameters frozen (recorded in baseline json).

Until then: cond.9 status = `candidate`, gating no production decision.
