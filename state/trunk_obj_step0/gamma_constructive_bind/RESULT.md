# γ trained-constructive-bind — STEP-0 RESULT (DIRECTIONAL · torch-free numpy · $0 mini)

**Verdict: 🧱 REFRIED / DPI-FLOOR — candidate ① does NOT warrant a STEP-1 engine-native GPU run.**
The γ contrastive-trunk objective (i) earns NO recombination over plain CE, and (ii) its sole
claimed structural distinction from the already-floored H_1602 (grad → *trunk* not *readout*) is
**measured-null** (G_trunk ≈ G_read). Autograd finite-diff gradchecked (max|ana−num| ≤ 1.7e-6).

## Two pre-registered screens (bars frozen before run — FREEZE.md / FREEZE2.md, no post-run edits)

### Screen A — S_4 pure group (FREEZE.md): INCONCLUSIVE-at-floor (no headroom)
All four arms held-out ≈ chance (1/24 = 0.042), train = 1.000. A concat-MLP does not grok S_4
composition from 40% of pairs in 4000 steps for ANY loss → zero headroom → cannot isolate γ.
Frozen bar: c1 0/4, c2a 0/4, c3 0/4 → FAIL, but uninformative (all arms floor identically).

### Screen B — factored non-symmetric interaction table (FREEZE2.md): FAIL, headroom present
World = 24 symbols, hidden factor f(s)∈{0..5} (4/factor), target = R[f(a),f(b)] with R a random
NON-symmetric 6×6→12 table (order-sensitive; non-commutativity lives in R, a WORLD property, not a
planted input feature). Held-out generalization possible (every symbol + factor-pair covered in
train). Mean over seeds [0,1,2,3], held-out acc:

| arm | ho_acc (s0/s1/s2/s3) | ho_noncomm | reach | unreach |
|---|---|---|---|---|
| ADD (order-blind DPI floor) | .249/.332/.332/.355 | .20–.27 | .22–.32 | .030–.034 |
| CE (γ=0, "echo" baseline)   | .876/.873/.821/.925 | .82–.91 | .81–.91 | .004–.008 |
| **G_trunk (candidate ①)**   | **.697/.760/.867/.841** | .78–.90 | .68–.84 | .007–.014 |
| G_read (H_1602 readout repro) | .777/.896/.850/.919 | .76–.90 | .77–.91 | .004–.010 |

Frozen bar (FREEZE2.md):
- **c1 reach earned (G_trunk ≥ CE+.10): 0/4 FAIL** — γ is WORSE than plain CE on 3/4 seeds. The
  contrastive term does not earn recombination; it mildly distorts the geometry CE learns unaided.
- c2a (G_trunk ≥ ADD+.15): 4/4 · c2b (noncomm ADD≤.55 ∧ G_trunk>ADD+.15): 4/4 — **PASS but NOT
  γ-driven**: every order-capable arm (CE, G_read) also beats order-blind ADD. The DPI escape here
  is supplied by the ARCHITECTURE (order-capable MLP), not by the γ objective.
- **c3 trunk ≠ readout (G_trunk ≥ G_read+.08): 0/4 FAIL** — the decisive test. Routing γ into the
  trunk gives held-out statistically indistinguishable from (slightly worse than) routing it only
  to the readout. The one mechanism that was supposed to make γ ≠ H_1602 does not exist.
- c4 headroom (any arm ≥ .20): 4/4 — world is genuinely learnable (screen is informative).
- c5 SHUFFLE advantage vanishes: 0/4 — trivially met; γ has no advantage to lose (SHUFFLE all ≈ chance).

## What this falsifies (mechanism-level)
1. **The trunk-vs-readout distinction is null.** Candidate ①'s whole thesis over H_1602 was
   "γ grad flows to the trunk → non-commutative geometry, unlike readout-aux." Directly isolated
   (G_trunk vs G_read, identical loss, only the detach differs): **no difference** (c3 0/4). The
   InfoNCE anti-swap/anti-additive pressure ends up shaping the readout either way → same G1 as
   H_1602's readout-aux (which is already 🧱 NOT-SUPPORTED at 303M engine-native).
2. **CE is not echo-limited where a lever could show.** In the one world with headroom, plain CE
   already recombines at .82–.93; γ has nothing to add and slightly hurts. In the world where CE
   fails (S_4), NO arm generalizes — no headroom for γ. There is no regime in this screen where
   γ's contrastive term uniquely opens recombination.

## Distinct-from-falsified?  NO — this is a re-fry, and I measured the exact distinction claim.
- H_1602 (🧱): infonce + contrastive_equilibrium *objective* already floored 303M engine-native
  (composed_distinct=0, 9/9). Candidate ① = same contrastive-objective family; c3 shows the
  "trunk-routing" that was meant to differentiate it is measured-null.
- H_1840 (🧱 DIRECTIONAL): γ trained-constructive bind, bypass-denied bilinear bottleneck STAGE-1
  FAIR gate FAILED 0/3 (bilinear = WORST bottleneck; bypass-OPEN did not floor). That was an
  ARCHITECTURE sweep under pure CE; this screen is the complementary LOSS-form axis under a fixed
  order-capable arch — and it also fails. Neither the bind-op nor the contrastive loss opens G1
  beyond a plain order-capable CE MLP.

## By-construction honesty
- Non-commutativity is in the WORLD target (R non-symmetric / S_4 Cayley), NOT a planted input
  interaction feature — model must infer factor from symbol id and learn R (no v_a⊙v_b handed in).
- reach NEVER 1.000-exact on held-out (.68–.93 < train 1.000) → no table-leak / handed advantage.
- Caveat (a_toy_scale_recheck): the factored world is EASY for CE (grok .82–.93), so it does not
  represent the 303M NL regime where CE fails; the S_4 world matches the "CE fails" regime but has
  no headroom. The bracketing itself is the finding — γ has no regime of unique benefit. torch-free
  numpy ⇒ DIRECTIONAL; NOT an engine-native TERMINAL verdict.

## Decision (p7 · a_break_the_wall · a_fire_autonomous)
STEP-1 engine-native GPU run **NOT authorized** (bar FAIL as frozen; c1 & c3 both 0/4 — not a
marginal miss). Consistent with H_1602/H_1840 and the DPI meta-law: the lever is a non-commutative
TARGET the CE-capable trunk does not already capture, NOT a readout/objective contrastive term.

## Artifacts
- FREEZE.md / FREEZE2.md — pre-registrations · toy_gamma_contrastive.py (autograd+S_4) ·
  toy_gamma_factored.py (headroom world) · run.log / run_factored.log · result.json / result_factored.json
