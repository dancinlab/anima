# H_1834 TENSION-MOUTH — DIRECTIONAL toy probe results

**Ladder rung:** (1) DIRECTIONAL toy. **Harness:** `tension_mouth_probe.py` (numpy,
from-scratch reverse-mode autograd + Adam; torch/gauge_lib NOT used).

> ⚠️ **DIRECTIONAL ONLY (numpy mirror, NOT engine-native).** Per CLAUDE.md
> `a_engine_native_learning` this is a `.py`+numpy mirror → auto-DIRECTIONAL, NOT
> terminal / NOT a 🟢-engine or 🧱-engine verdict. Any 🟢/🧱 closure requires
> engine-native re-measurement on live `core/*.hexa` A⇄G (pure_field⇄engine_g),
> byte-exact, before it can be stamped. Self-check: `grep -lE 'import torch|gauge_lib|numpy'`
> → matches (numpy) → verdict recorded DIRECTIONAL, engine-native re-measure = ING follow-on.

Autograd validated: **gradcheck PASS**, max |numeric−analytic| = 5.25e-11 over all 3 arms.

## composed_distinct — measurement definition

`composed_distinct` = number of DISTINCT correct composed target bytes produced by
greedy argmax next-byte prediction over the **held-out (unseen-combination)** pairs.
Toy: concept A_m (byte 10+m) at one slot, concept B_n (byte 50+n) at another,
compose(A_m,B_n) → distinct byte `100+m*K+n` (K=4, 16 pairs → composed bytes 100..115).
Held-out = diagonal compositional split `{(0,0),(1,1),(2,2),(3,3)}` (each m and each n
IS seen in training with other partners; the specific combo is novel and its target byte
is absent from training). Distance between the two concept slots is varied but binding is
RF-free (bag pooling of the two concept embeddings). Range 0..4 (4 held-out pairs).
Repo convention: ByteGPT floor=2, conv floor=0; pre-registered bar = distinct≥3.

## 3-arm × 3-seed table (frozen bar, p7, no post-hoc move)

| seed | arm | composed_distinct | heldout_acc | train_acc | \|Ψ−0.5\| |
|------|-----|:---:|:---:|:---:|:---:|
| 7    | FULL        | 0/4 | 0.00 | 1.00 | 0.0892 |
| 7    | TENSION-OFF | 0/4 | 0.00 | 1.00 | —      |
| 7    | ADDITIVE    | 0/4 | 0.00 | 1.00 | —      |
| 4302 | FULL        | 0/4 | 0.00 | 1.00 | 0.3042 |
| 4302 | TENSION-OFF | 0/4 | 0.00 | 1.00 | —      |
| 4302 | ADDITIVE    | 0/4 | 0.00 | 1.00 | —      |
| 4303 | FULL        | 0/4 | 0.00 | 1.00 | 0.2355 |
| 4303 | TENSION-OFF | 0/4 | 0.00 | 1.00 | —      |
| 4303 | ADDITIVE    | 0/4 | 0.00 | 1.00 | —      |

**Aggregate (mean over seeds 7 / 4302 / 4303):**

| arm | composed_distinct mean | \|Ψ−0.5\| mean |
|-----|:---:|:---:|
| FULL        | **0.00** (0,0,0) | 0.2096 |
| TENSION-OFF | **0.00** (0,0,0) | — |
| ADDITIVE    | **0.00** (0,0,0) | — |

(Ψ reported only for FULL, where the tension scalar t=‖a‖/‖g‖ is computed; TENSION-OFF
removes g entirely, ADDITIVE uses a+g with no tension resolution — Ψ N/A for both.)

## Verdict (DIRECTIONAL) — pre-registered frozen bar §6

Bar: 🟢 iff composed_distinct≥3 AND |Ψ−0.5|≤0.05 · 🟠 distinct≥3 & Ψdev>0.05 · 🧱/🔴 distinct≤2.

**Every arm, every seed: composed_distinct = 0 ≤ 2 → 🧱/🔴 WALL (DIRECTIONAL).**
train_acc = 1.00 everywhere = perfect memorization of the 12 training pairs but **zero
compositional generalization** to the 4 held-out unseen combinations. FULL Ψ also fails
the ½ fixed-point (|Ψ−0.5| = 0.09–0.30, driven off ½ despite the L_psi=(mean ψ−0.5)² term,
because CE dominates and does not reward the recombination that would pin the tension).

## Control conclusions (deterministic ablation §5)

- **tension causal? → NO. INERT (contribution 0).** FULL (a·softmax(g)+ψ·bilinear) does
  **not** beat TENSION-OFF (a only): both = 0. Removing the entire G / tension / global-
  bilinear machinery changes composed_distinct by 0. On this task the tension mechanism is
  INERT — it neither helps nor hurts held-out recombination. Honest report: **contribution 0.**
- **structural > additive? → NO.** FULL (multiplicative bilinear binding) does **not**
  exceed ADDITIVE (a+g): both = 0. No structural-vs-additive separation is isolable at floor.

## Interpretation (honest, no tune-to-green)

The TENSION-MOUTH forward is faithfully implemented (gradcheck-verified) and trains fine
(train_acc 1.00), but under a plain CE objective it hits the **same G1 recombination floor**
the repo has repeatedly measured: the *combination operator / readout structure* (here the
ψ-gated global bilinear binding) is **not the lever** — it collapses to memorization and
generalizes 0 on the held-out compositional split, identical to the additive control. This
is consistent with the standing engine-native record (memory: `substrate-framebreak-g1-
combination-operator`, `h1816-predcoding-binding-not-supported`, `g1-lever-multilens-
objective`): the G1 wall lever is the **trunk training OBJECTIVE** (CE does not reward
constructive recombination), NOT the mouth/readout binding operator. The tension-mouth
readout, as a DIRECTIONAL numpy probe, does not break the wall.

**This is a DIRECTIONAL floor, not a terminal 🧱.** Engine-native re-measurement on live
core/ A⇄G is the required next rung before any confident wall/GREEN closure; and an
objective-side variant (recomb-reward, cf. H_1602) is the more promising untried lever than
this readout-only test — but that is a separate hypothesis. Bar was frozen pre-run and not
moved.

## Ladder / follow-on (a_verified_must_wire / a_toy_scale_recheck)

- (0) design [README.md] ✅
- (1) DIRECTIONAL toy [this] ✅ → **🧱/🔴 floor, DIRECTIONAL, tension INERT** (no lift over controls)
- (2) engine-native re-measure on live core/ A⇄G — **NOT done** (would only be warranted if
  the toy had lifted; at floor with tension INERT there is nothing to wire). Recorded as the
  gating rung per `a_engine_native_learning`.
- (3)/(4) generator L3 3rd mouth-kind wire-in + ARCHITECTURE.json lockstep — **not reached**
  (gated on (1) lift, which did not occur).
