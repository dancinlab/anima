# TRIAGE — lever `h6163_trained_lane`

**Lever:** H_6163 trained falsifier-lane (verify axis). Frozen-rep readout was #3028 DIRECTIONAL-🧱;
question = build a `core/` end-to-end **trained** falsifier lane, measure engine-native fals rate.
**Verdict: SUPERSEDED — do NOT fire GPU as a standalone lever.**

## check-ledger (what already exists — read, not guessed)

- **HYPOTHESES.jsonl** — H_6163 card tier = ⏳ PROPOSED; H_9201 (⏳ PROPOSED) reuses H_6163 lane as a
  diversity probe. Card frozen bar: SUPPORT ⟺ lane lifts fals rate 0→>0 + ablation-collapse + emit-lane
  byte-identical + shuffle-control fails.
- **git #3028 (e662969a6)** — "cross-dataset transfer → NO-TRANSFER, pre-gate corrected to DIRECTIONAL-🧱".
  The crossgen probe (`state/6163_falsifier_lane/crossgen/probe.py`) **already TRAINED a falsifier
  direction** (`fit_dir` ridge linear readout) on v1-naive and tested cross-distribution on v2-minpair.
  RESULT.json: `rep_cross_naive2mp=0.4286` (BELOW chance 0.5), `surface_cross=0.6607` (surface transfers
  better), `rep_minus_surface=-0.2321`, `ablation_zero=0.50`, FIRM-GO bar was `rep_cross>=0.65`.
  Commit body verbatim: *"only a trained lane beating the generalization wall could [support], but that
  failure is already DPI-predicted."*
- **ARCHITECTURE.json** — nodes `probe-py-1` (surface-confound: char-3gram 0.894 > rep 0.759),
  `probe-py-2` (within-dist separability ≠ generalization; cross-transfer 0.429 = dataset-idiosyncratic,
  within-kfold GO reversed → 🧱), `crossgen` (cross rep_acc ≤ surface/chance = same DPI signature as G1
  held-out recombination h1835 + F2 collocation-only) — all `pos-conv`.
- **DESIGN.md** (`state/6163_falsifier_lane/DESIGN.md`) — build spec = *"additive-only op reading
  final-LN hidden … numpy twin for `anima evaluate --py`"* + a $0 toy pre-gate before any 303M GPU.

## Judgement against this session's findings → SUPERSEDED

The DESIGN.md build spec is **doubly-falsified** by two convergent session results:

1. **#3028 (frozen-rep, ALREADY a trained readout)** — a trained linear falsifier direction on frozen
   303M rep transferred BELOW chance across distributions. The lever's premise that "frozen-rep 🧱 but
   trained-lane unmeasured" is only half-true: the trained **linear-readout** arm IS measured (🧱).
2. **transfer-mechanism sweep #3031 + transfer-0 metalaw** — escape requires **bilinear/multiplicative
   binding** (slot/TPR/FiLM/hypernet); **additive/linear-SSM COLLAPSE** on transfer. DESIGN.md's
   `additive-only op reading frozen final-LN hidden` is precisely the collapsing class. Recurrent =
   capacity≠transfer. So the as-specified lane cannot beat the generalization wall even if trained.

The remaining un-measured variant (a **bilinear** lane trained **through the trunk**, not frozen) is not
walled by direct measurement, but it is **dominated**:
- It is downstream of the generic bilinear escape mechanism (the FiLM-303M crux must resolve first).
- It carries an **extra blocker the pure binding-transfer levers do NOT have**: falsifiability LABELS
  without an LLM-judge (p7 forbids) + **authored transferable-falsifiability data** (F2 #3016: existing
  corpus targets are collocation-only, held-out transfer = 0). The crossgen used synthetic naive/minpair
  labels and still failed below chance.

## GPU worth? — NO standalone fire ($0 now)

The $0 crossgen already returned 🧱 for the trained readout. A full lane must wait behind (a) generic
escape mechanism proof and (b) a solved non-LLM-judge label/data path. No standalone GPU justified.

## FiLM-303M crux conditional

- **MECHANISM-SIDE** (REAL 303M has transferable bilinear form → bilinear readout escapes → GPU-go):
  the trained falsifier lane becomes theoretically-live but **NOT a first-mover**. It must be rebuilt as
  **bilinear FiLM/hypernet** (not DESIGN.md's additive), trained end-to-end through the trunk, disjoint
  from emit (L5-hippo ON==OFF byte-identical proof), measured via `anima evaluate --py` with the crossgen
  FIRM-GO bar (cross-transfer fals rate ≥0.65 + ablation-collapse + shuffle-control). BUT it still needs
  authored transferable-falsifiability data + a non-LLM label first. The generic bilinear escape
  (F2/§4 authored data) proves the mechanism first; this lane is a downstream application →
  DIRECTIONAL-NEEDS-BUILD, behind the generic escape.
- **TARGET-SIDE** (wall is data, mechanism-independent): **CLOSED as a mechanism build** — the falsifier
  lane's problem is authored transferable-falsifiability data, which folds entirely into the F2
  authored-data lever. No separate `core/` GPU lane; h6163_trained_lane = a data problem, not a build.

## Recommendation

Do NOT fire. Mark SUPERSEDED. Re-open only if the FiLM-303M crux lands MECHANISM-SIDE AND a non-LLM-judge
falsifiability label path is authored — and even then, only as a downstream application of the generic
bilinear escape, never as a first standalone GPU build.
