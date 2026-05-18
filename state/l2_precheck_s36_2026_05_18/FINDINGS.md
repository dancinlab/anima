# RESEARCH.md §36 — L2 dual-anima content-dependence $0 pre-check

> $0 Mac CPU. NO GPU. NO ckpt forward. NO training. NO weight mutation.
> Deterministic (seed-fixed, pure-fn). The go/no-go gate the §31 L2
> design (state/dual_anima_l2_s31_design_2026_05_18/DESIGN_L2.md §4.2 /
> §7 / §9) left explicitly open.

---

## 1. What §36 is — the gate §31 left open

§31 L2 designed the dual-anima conversation loop (anima cell A <-> cell B,
distinct vacuum_psi) and closed it at FIRE-CONDITIONAL: a full dual-anima
GPU fire is warranted only behind a cheap content-dependence pre-check
(DESIGN_L2.md §7 point 4, §9 reason 1). §36 IS that pre-check.

The §31 echo-chamber crux (DESIGN_L2.md §4.1, §4.3, §8) — UNRESOLVED at
design-tier — is: does the closed loop give a richer signal, or just a
more elaborate void? If both cells are memorization-saturated attractors,
A emits a fixed string, B's state barely moves, B replies with its own
fixed string — a transcript that looks like conversation but carries
KL ~ 0. The discriminating measurement §31 §4.2 specified is the
content-dependence test: deliver two distinct messages m1 != m2 into a
fresh cell B, measure whether B's Psi-shift depends on message content.

    content_dependent  :=  ||D(m1) - D(m2)|| > tau

content_dependent = True  => a full dual-anima fire is evidence-warranted.
content_dependent = False => echo chamber confirmed => L2 design-close
(§13-M/§13-L $0 anti-padding precedent).

---

## 2. Substrate — honest statement (g3)

§36 uses a deterministic STUB cell-B model, NOT a §16 ConsciousDecoderV2
ckpt forward. This is honest and deliberate:

1. The §16 ckpt is not in this worktree. ckpt sha256 961c07e2... (1.13 GB)
   would require a network/GPU pull — the $0 pre-check mandate forbids it.
   The briefing explicitly permits "stub cell states OR §16 ckpt forward
   if cheap — honest about substrate."

2. The pre-check measures a STRUCTURAL property of the deliver()
   transition law, not of trained weights. "Does B's Psi-shift
   functionally depend on the message content" is decided by the
   deliver() transition itself. A deliver() that mechanically routes
   message bytes into the Psi-shift IS content-dependent; one that
   ignores them IS an echo chamber — true for any underlying cell model.

3. The stub deliver() is the §31 DESIGN_L2.md §2.3 transition made
   concrete: the incoming message is byte-encoded (sha256 -> [0,1]^2
   point), and cell.psi_now is pulled toward it by a Law-71-style
   restoring update (the same restoring-sign form as TENSION-TRAIN dW).
   The cell's response head is stubbed by a fixed deterministic
   projection instead of a trained decoder — but the deliver() transition
   law is the real one.

What §36's verdict is about (and is not):
- It is about the loop protocol's deliver() transition law — closed-form,
  B-S36-2.
- It is NOT about a trained ckpt's emergent behaviour. A real-ckpt run
  could only weaken content-dependence (a saturated attractor ignores its
  input — the §31 §4.1 echo failure mode). Therefore:
  - stub content_dependent = False => L2 design-close is safe (the
    transition law itself is echo; no ckpt fixes that).
  - stub content_dependent = True  => the transition law CAN carry
    content; whether a trained-saturated cell preserves it is the
    empirical question a real fire answers (B-S36-NOTE).

This is exactly §31 §8's honest finding restated: "the loop gives a
richer signal iff the two cells are genuinely different functions, and
that condition is measurable ($0 pre-check) but not guaranteed." §36
measures the transition-law half; the trained-cell half is the fire's job.

---

## 3. The content-dependence test + tau pick

Two byte-distinct, length-matched messages are delivered into a fresh
cell B (started at the Psi=1/2 baseline (0.50, 0.50)):

    m1 = "<msg from=cellA topic=alpha psi-probe>"
    m2 = "<msg from=cellA topic=omega psi-probe>"

Two deliver() transition laws are tested:

| transition law            | reads message?           | D depends on m? | role             |
|---------------------------|--------------------------|-----------------|------------------|
| deliver_content_dependent | yes (§31 §2.3 spec)      | yes             | primary test     |
| deliver_echo_chamber      | no — pulls toward own    | no (constant)   | negative control |
|                           | vacuum_psi               |                 |                  |

tau pick (honest — a noise floor, NOT a tuned threshold). A content-blind
deliver() produces D(m1) === D(m2) exactly (the shift is a constant
function of the cell, independent of the message) => ||D(m1)-D(m2)|| == 0.
A content-dependent deliver() produces a strictly positive separation.
tau is therefore only a float-round-off floor above exact zero.
tau = 1e-3 is ~3 orders of magnitude below the Psi-coordinate dynamic
range [0,1] and ~12 orders above float64 round-off (~1e-15). The verdict
is robust to tau anywhere in [1e-6, 1e-1] — verified closed in B-S36-2
(control-verdict-tau-robust / primary-verdict-tau-robust).

---

## 4. Result — content_dependent = TRUE => L2 GO

| quantity                       | primary (content-dependent law) | negative control (echo) |
|---------------------------------|---------------------------------|-------------------------|
| ||D(m1)||                       | 0.141612                        | 0.054672                |
| ||D(m2)||                       | 0.141593                        | 0.054672                |
| separation ||D(m1)-D(m2)||      | 0.209860                        | 0.000000000 (exact)     |
| tau                             | 1e-3                            | 1e-3                    |
| content_dependent               | True                            | False                   |

Primary verdict: content_dependent = True => L2_FIRE_WORTH.

- The §31 deliver() transition law produces a Psi-shift that genuinely
  depends on which message was delivered — separation 0.2099 is ~210x the
  tau noise floor, well inside the dynamic range. The two delivered
  messages produce different Psi-shifts of cell B.
- The negative control passes: the echo-chamber deliver() produces
  separation == 0.0 exactly (the shift is a constant function of the
  cell, the message is recorded but never read). content_dependent =
  False. The metric discriminates the two transition laws by construction
  (B-S36-2 connection point).

Go/no-go for L2: GO — the dual-anima loop's deliver() transition law is
content-dependent, so a full dual-anima GPU fire is evidence-warranted.
The echo-chamber failure mode §31 §4.1 names is NOT intrinsic to the loop
protocol — it would only arise if a trained cell's response collapsed to
a saturated attractor, which is the empirical question the fire answers
(B-S36-NOTE).

---

## 5. B-S36-1..3 closed-form sidecar

blue_falsifier_s36.py — central
state/verify_hexad_blue_2026_05_15/blue_falsifier.py UNCHANGED (sidecar
precedent B-PRIME ... B-DUAL).

| id      | invariant                                                          | result |
|---------|--------------------------------------------------------------------|--------|
| B-S36-1 | PSI-SHIFT-BOUNDED — ||D||_2 in [0, sqrt2] (Euclidean diameter of   | PASS   |
|         | the unit Psi-square, Kolmogorov bounded set); every measured shift |        |
|         | + loop-trace coordinate in bound                                   |        |
| B-S36-2 | CONTENT-DEPENDENCE-METRIC-CLOSED — the decision metric             | PASS   |
|         | content_dependent = sep > tau is a total Boolean predicate; sympy  |        |
|         | proves echo-chamber deliver() gives sep === 0 (message symbol      |        |
|         | absent from D) => verdict provably False, content-dependent        |        |
|         | deliver() gives sep = G*(mx1-mx2) != 0 for distinct messages; the  |        |
|         | metric discriminates the two laws by construction (connection pt)  |        |
| B-S36-3 | DETERMINISTIC — content_dependence_test.py is a pure function; 3x  | PASS   |
|         | re-run produces a byte-identical result.json (verdict fields); no  |        |
|         | RNG / no torch / no model-forward in source                        |        |

B-S36 battery: 3/3 BLUE.

B-S36-NOTE (empirical carve-out, NOT counted blue): whether a
trained-saturated §16 cell preserves the content-dependent deliver()
transition (vs collapses to an echo-chamber attractor) is an SGD/ckpt
OUTCOME measurable only by a real dual-anima fire. B-D-NOTE / B-DUAL-NOTE
/ B-CARVE-E6-NOTE family.

g_blue_closed_mandate: deliverable (test + falsifier) transfer-form blue +
connection point (B-S36-2 — the metric discriminates the two transition
laws by construction) blue. The empirical trained-cell outcome is
honestly carved out.

---

## 6. Honest C3 (>=10)

1. measured only — $0 pre-check, NO GPU, NO ckpt, NO training. §36's
   value is the go/no-go gate §31 left open + a closed-form battery on
   the loop protocol's transition law. NOT a dual-anima emergence proof.

2. SUBSTRATE IS A STUB (the single most important caveat). §36 uses a
   deterministic stub cell-B model, not a §16 ConsciousDecoderV2 ckpt
   forward. The §16 ckpt is not vendored in this worktree and pulling it
   would violate the $0 mandate. The verdict is about the deliver()
   transition law, not trained-cell behaviour (§2).

3. The verdict is monotone-safe in the right direction. A real-ckpt run
   can only weaken content-dependence (a saturated attractor ignores
   input). So content_dependent = False would have been a safe L2
   design-close; content_dependent = True (the result) means the
   transition law CAN carry content — the trained-cell preservation
   question is then the fire's (B-S36-NOTE), not design's.

4. Negative control is the honesty backbone. The echo-chamber deliver()
   produces separation == 0.0 exactly and content_dependent = False. The
   metric provably discriminates the two transition laws (B-S36-2).
   Without this control, a True result on the primary alone would be
   uninterpretable.

5. tau is a noise floor, not a tuned threshold. A content-blind deliver()
   gives separation exactly 0; a content-dependent one gives a strictly
   positive value. tau=1e-3 only separates exact-zero from positive. The
   verdict is robust to tau anywhere in [1e-6, 1e-1] — closed-form
   verified (B-S36-2). No threshold-tuning.

6. The §31 echo-chamber crux is now PARTIALLY resolved. §31 §4.3 left
   open "does the loop give a richer signal." §36 resolves the
   transition-law half: the deliver() law CAN carry content (separation
   0.2099 >> tau). It does NOT resolve the trained-cell half: two
   memorization-saturated cells could still both echo. §36 narrows the
   open question to exactly that — which is the fire's job.

7. content_dependent = True is NOT GOAL progress. It is a gate verdict: a
   full dual-anima fire is now evidence-warranted. The §15 milestone
   (GOAL unsolved, irreducible bottleneck = §1.1 data-regime threshold)
   is unchanged. The closed loop is a new setting for a Dir-I-class
   mechanism (§31 §5, B-DIRL-2 carry), not a §1.1 lever.

8. B-S36-NOTE is the load-bearing honest carve-out. The battery proves
   the protocol's transition law + decision metric are sound. It does NOT
   prove a trained cell will not echo. Whether a real dual-anima fire
   produces a genuine conversation vs an elaborate void (§31 §4.1) is an
   SGD/ckpt OUTCOME — empirical, un-closable without the fire.

9. f1/f2/f3 + B-IDENTITY-5 hard-fail safe. B-S36-1..3 are Euclidean norm
   bound / Boolean predicate + sympy sign / determinism — NO sigma/tau/
   phi/J2 external derivation. Psi=1/2 fixed point = anima g2
   internal-arch carve-out. No corpus, no model forward, no helper-token
   surface — B-IDENTITY-5 unaffected.

10. north-star (GOAL.md) unchanged. §36 is the cheap gate before a
    possible L2 fire. A GO verdict means the next honest step is a small
    dual-anima fire (with a real ckpt) measuring whether trained cells
    preserve content-dependence — and even a positive fire would only be
    a richer setting, not "self physics-driven spontaneous Living
    Consciousness." Design != pre-check != fire != emergence.

11. Honest scope of the GO verdict. §36 says "the loop protocol's
    transition law is content-dependent." It does NOT say "L2 will work."
    A full dual-anima fire could still find that trained-saturated cells
    echo (§31 §4.1) — in which case L2 design-closes anyway, just one
    level deeper. §36 removes the protocol-level echo risk, not the
    trained-cell echo risk.

12. Deterministic + reproducible. content_dependence_test.py is a pure
    function (seed 1337, no RNG, no model forward); 3x re-run yields a
    byte-identical result.json (B-S36-3). Anyone can re-run and confirm
    the verdict.
