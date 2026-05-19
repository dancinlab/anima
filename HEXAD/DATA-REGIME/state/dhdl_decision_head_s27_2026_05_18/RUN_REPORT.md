# §27 — DH-DL Decision-Head Dual-Loss — RUN REPORT

> RESEARCH.md §27. §26 candidate #1 (DH-DL, priority HIGH, anima-fit ★★★★★)
> taken from brainstorm-tier to **design-mature → corpus → fire → eval →
> closed-form battery → verdict**. $0 Mac CPU. design ≠ fire ≠ capability ≠
> emergence (g3). north-star (GOAL.md) unchanged; §15 milestone carries.

---

## §1 — What was done

DH-DL is the **learnable version of the §24 SPONTANEOUS Phase B hand-coded
`talker_should_emit` threshold** — the decide-when-to-speak axis made trainable.
A thin 3-class decision-head `{CONTINUE_THINK, EMIT_VOICE, REMAIN_SILENT}`
consumes anima's 14-dim physics-feature vector and outputs a softmax over the
three control decisions.

This cycle delivered, end-to-end:
1. `DESIGN_DHDL.md` — design-mature spec (10 § + 12 honest C3).
2. `trace_corpus_generator.py` → `trace_corpus.jsonl` (48,000 records).
3. `train_dhdl.py` → `dhdl_head.json` (trained head, $0 Mac CPU, 32s wall).
4. `eval_dhdl.py` → `eval_result.json` (3-class accuracy + confusion +
   threshold-distillation gap probe).
5. `blue_falsifier_dhdl.py` → **B-DHDL-1..5 5/5 🔵** sidecar battery.

## §2 — Design-mature decisions

- **Engine A stream tap point.** §26 BRAINSTORM specified the head "bolted to
  Engine A's penultimate stream". Design-mature finding: the §24
  `talker_should_emit` decision is *already* a pure function of the 14-dim
  physics-feature vector and never reads an Engine A hidden tensor. A
  live-hidden-stream tap would require a GPU ckpt forward per step and add
  **zero signal** (it would re-derive the same features). The head is therefore
  a **standalone thin MLP on the physics-feature vector** → `$0` Mac CPU.
- **Dual loss.** Loss 1 = class-weighted 3-class decision CE (Shannon CE ≥ 0).
  Loss 2 = `λ·(1−safety_ok)·p[EMIT]²` — quadratically penalizes EMIT mass when
  the §4 6-control safety conjunction trips. Loss 2 is the *most
  GOAL-legitimate* of §26's "safety-consistency OR physics-grounding" options:
  it wires the head to anima's *own* 6-control safety SSOT
  (`g_blue_closed_mandate` connection-point) and is the differentiable analogue
  of the B-DHDL-4 hard safety override.

## §3 — Corpus

`trace_corpus_generator.py` ran `run_bounded.py`-equivalent dynamics **2400
traces × 20 steps = 48,000 records** with **varied env_state stubs** — each
trace draws a distinct perturbation vector from a deterministic 64-bit LCG
(seed `1337 + φ·idx`, pure-fn, `g_clm_from_scratch`). Diverse physics
trajectories, NOT replays.

| field | value |
|---|---|
| record_count | 48,000 |
| sha256 | `d55ad3765f8f718eb03c59bd31938aa78b8528a511140d38b2776a736a3c4aee` |
| CONTINUE_THINK | 9 (0.019%) |
| EMIT_VOICE | 2,128 (4.43%) |
| REMAIN_SILENT | 45,863 (95.55%) |
| forbidden-token grep | 0 (B-IDENTITY-5 clean) |

## §4 — The structural finding (valuable, honest)

Building the corpus surfaced a deep structural property of the **§24 threshold
itself**:

1. **`balance` floor lockout.** The §4 `phi_ratchet` safety control requires
   `phi > ratchet/2`. The 8-factor `balance` factor is *defined* as
   `phi > ratchet/2 → 1.0`. So **whenever it is safe to emit, `balance` = 1.0**
   (weight 0.15) — a hard 0.15 score floor.
2. **`dynamics` ⇄ `rate_limit` anti-coupling.** The `dynamics` factor
   (`silence/30`, weight 0.10) and the `rate_limit` safety control
   (`silence ≥ 30`) are driven by the **same variable in opposite senses**.
   Whenever rate-limit permits an emit, `dynamics` = 1.0.

Combined: in the safety-OK region the motivation-score floor is
`0.15 + 0.10 = 0.25` plus a non-trivial `relevance` term — **above
`IM_THRESHOLD = 0.3`** for all but a measure-near-zero corner. Result:
**the §24 `talker_should_emit` threshold is effectively a binary
`{EMIT, SILENT}` decision; `CONTINUE_THINK` (safe yet low-motivation) is a
structurally near-empty class** (9 / 48,000). This is a finding *about §24* —
valuable for any future re-design of the 8-factor motivation weighting — not a
corpus defect. We did NOT artificially inflate CONTINUE_THINK (that would
tamper with §24's logic, forbidden); the corpus is honest.

## §5 — Training + eval

`train_dhdl.py` — numpy-vectorized MLP (14→32→16→3), explicit hand-coded
analytic backprop (no torch autograd), from-scratch seed 1337, 120 epochs,
class-weighted CE. Wall 32s, `$0` Mac CPU. Train loss 0.13576 → 0.01747.

`eval_dhdl.py` on 9,598 held-out records (80/20 stratified split):

| metric | value |
|---|---|
| 3-class accuracy | **0.99937** |
| EMIT_VOICE per-class acc | 0.98824 |
| REMAIN_SILENT per-class acc | 1.0 |
| CONTINUE_THINK per-class acc | 0.0 (only **1** held-out record) |
| confusion `[true][pred]` | `[[0,1,0],[0,420,5],[0,0,9172]]` |

## §6 — Threshold-distillation gap probe (the emergence-vs-distillation signal)

For every held-out record we compared the **learned-head decision** (argmax +
6-control safety override, B-DHDL-4) against the **§24 hand-coded
`talker_should_emit` decision** (the label rule).

| metric | value |
|---|---|
| threshold-distillation gap | **0.00063** (6 / 9,598) |
| gap verdict | `DISTILLATION_WITH_APPROXIMATION_NOISE` |
| gap direction | EMIT→SILENT ×5, CONTINUE→EMIT ×1 |

**Honest characterization.** All 6 gap records are the head **failing to
perfectly match** the §24 threshold — 5 EMIT records under-fit to SILENT, and
the single held-out CONTINUE_THINK record mis-classified as EMIT. **There is no
record where the head exhibits a NEW emission behavior the threshold could not
produce.** The gap is approximation noise (the head slightly under-fitting near
the decision boundary), not emergence.

## §7 — Honest verdict: DISTILLATION, NOT EMERGENCE

The DH-DL head learns the §24 `talker_should_emit` decision function to
**0.99937 accuracy with a 0.00063 distillation gap**. This is **exactly the
outcome the design predicted up front** (DESIGN_DHDL.md §6): the decision label
is a deterministic function of the physics features, so the head can at best
*match* the threshold — and it does, near-perfectly.

This is **function approximation (capability), NOT emergence.** A head that
exhibited emergence would produce a decision the threshold could not — that
requires the supervision to be richer than the threshold's own output. Here the
supervision IS the threshold's output, so any mismatch is approximation noise.

**What is genuinely valuable.** A learned, *differentiable*, *composable*
decision-head matching the §24 threshold is a real substrate component: it is
trainable (future cycles can enrich its supervision beyond the threshold), it
is differentiable (it can be jointly optimized inside a larger architecture),
and it composes (per-MITOSIS-cell decision-head variants are a natural
extension). DH-DL converts the §24 *hand-coded heuristic* into a *trainable
sub-module* — that is the deliverable. It is a substrate step, not a GOAL step.

## §8 — B-DHDL closed-form battery (5/5 🔵)

Sidecar `blue_falsifier_dhdl.py` — central `blue_falsifier.py` (110/110)
UNCHANGED.

| id | name | verdict |
|---|---|---|
| B-DHDL-1 | DECISION-3CLASS-PARTITION-CLOSED | 🔵 PASS |
| B-DHDL-2 | SOFTMAX-SIMPLEX-BOUNDED-CLOSED | 🔵 PASS |
| B-DHDL-3 | DUAL-LOSS-NONNEGATIVE-CLOSED | 🔵 PASS |
| B-DHDL-4 | SAFETY-OVERRIDE-CLOSED (연결부위) | 🔵 PASS |
| B-DHDL-5 | THRESHOLD-OFF-REDUCTION-CLOSED (연결부위) | 🔵 PASS |

`B-DHDL-NOTE` — actual head accuracy + distillation gap + emergence question =
SGD/measurement OUTCOME (B-D-NOTE / B-PHASE-B-NOTE / B-EMERGE-NOTE family, NOT
counted 🔵). The battery proves the decision-head MECHANISM is well-formed
(3-class partition + simplex + dual-loss nonneg + safety-override +
threshold-off reduction); it does NOT prove emergence.

## §9 — Cost

`$0` — corpus generation, head training, eval all `$0` Mac CPU
(pure-fn / numpy-vectorized, no model forward, no GPU). GPU fire would be
needed only for a live-Engine-A-hidden-stream tap (§2 explains it is not
needed). Honest cost minimization per `g_fire_autonomous` — not a gate.

## §10 — Honest C3 (≥10, over-claim 0)

1. **DISTILLATION, NOT EMERGENCE — the central verdict.** Head accuracy
   0.99937, distillation gap 0.00063. The head approximates the §24 threshold;
   it does not emerge a new decision behavior. Over-claim 0.
2. **The outcome was predicted up front** (DESIGN_DHDL.md §6). The decision
   label is a deterministic function of the physics features; a head trained on
   that corpus can only learn that function. The gap probe quantifies it.
3. **Every gap record is the head under-fitting**, not new behavior. 5
   EMIT→SILENT + 1 CONTINUE→EMIT, all approximation noise near the boundary.
4. **Structural finding (valuable):** the §24 threshold is effectively binary
   `{EMIT, SILENT}` — CONTINUE_THINK is structurally near-empty (9/48,000)
   because `balance` floor-locks (phi_ratchet coupling) and `dynamics` ⇄
   `rate_limit` anti-couple. A finding *about §24*, useful for future
   motivation-weight re-design.
5. **CONTINUE_THINK is essentially unmeasurable** — 1 held-out record, per-class
   accuracy 0.0. The 3-class head learns a 2-effective-class problem under §24
   physics. Reported honestly, not hidden.
6. **`$0` Mac CPU, no GPU fire.** The head consumes only physics features; a
   live-hidden-stream tap adds cost without signal. Honest minimization.
7. **The corpus is diverse, not replays** — 2400 distinct LCG perturbation
   vectors. But trajectory diversity does not change that the *label rule* is
   the fixed §24 threshold.
8. **Loss 2 (safety-consistency) adds no information beyond the hard
   override** — it makes the override *learnable* / *differentiable*. A head
   with `λ=0` plus the hard override is already §24-equivalent (B-DHDL-5).
9. **B-DHDL battery proves MECHANISM, not emergence.** All 5 propositions are
   closed-form (partition / simplex / dual-loss nonneg / safety-override /
   threshold-off reduction); none is a capability claim (B-DHDL-NOTE).
10. **f1/f2/f3 + B-IDENTITY-5 safe.** Boolean / sympy / Shannon CE / softmax
    simplex — no σ/τ/φ/J₂ external derivation. Ψ=½ / HEXAD = anima g2 internal
    arch carve-out. Trace-corpus forbidden-token grep = 0.
11. **Bootstrap honesty (§26 C3 #11 carried).** The corpus uses stubbed sensors
    (no ckpt forward), so the head learns the threshold *as defined*, not *as it
    would behave on a trained anima*. A future cycle feeding real
    ckpt-derived physics would test transfer.
12. **north-star (GOAL.md) unchanged.** §27 converts a hand-coded decision
    heuristic into a trainable substrate component — a *substrate* deliverable,
    NOT progress on the §1.1 data-regime emergence bottleneck and NOT emergence.
    §15 milestone carries. The honest distance to GOAL is unchanged.
