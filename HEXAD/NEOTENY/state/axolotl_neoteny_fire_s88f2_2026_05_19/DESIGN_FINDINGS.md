# §88-F2 — AXOLOTL NEOTENY ANTI-SATURATION — TRAINED-SCALE FIRE

**Trained-scale validation of §87-F2 (commit 798b6110d, B-S87F2 6/6 🔵).**
Cost-bearing runpod fire. `g_fire_autonomous` — no-query, no-gate.
SSH-robust podHostId-fixed dispatch (`g_fire_dispatch_robust`
`ssh_endpoint_robustness` — gate on `ip && publicPort`, NOT `podHostId`,
the §79-RETRY false-blocker). Single sequential agent.

---

## §1. Why §88-F2 is structurally different from §81/§82/§83-FIRE

§81 / §82 / §83-FIRE all train a **trained-saturated** §16-class ckpt
**first**, then **overlay** a mechanism at inference time — and the overlay
collapsed (echo-chamber, majority-class) because the ckpt was already
inside the byte-cascade attractor basin.

§87-F2 axolotl neoteny is a different lever entirely. The neoteny
mechanism is applied **during training itself** (inside the optimisation
loop). The goal is **not** to rescue a saturated ckpt — it is to produce a
**non-saturated** ckpt. The axolotl (*Ambystoma mexicanum*) stays a
plastic juvenile its whole life, never metamorphosing into a frozen
terrestrial adult. §16.6-C memorization-saturation is anima becoming an
over-mature adult **too fast**. §88-F2 keeps anima juvenile.

This is the §1.1 data-regime irreducibility bottleneck targeted **head-on
at the learning-time axis** — not via a corpus change (§16/§23), not via
an inference overlay (§81/§82/§83), but by changing how training matures.

---

## §2. Maturity as a 3-proxy metric (§87-F2 carry, byte-equal)

`maturity ∈ [0,1]` = convex weighted combination of three proxies, every
one a function of **this run's own training trajectory**:

| proxy | name | reads | over-mature when |
|-------|------|-------|------------------|
| M-1 | CE-floor proximity | final CE vs `CE_NATURAL_FLOOR` | CE → 0 |
| M-2 | attractor-basin depth | body byte `maj_frac` | maj_frac → 1.0 |
| M-3 | dimensionality collapse | effective `D` (head_a spectrum PR) | D → `D_FLOOR` |

`maturity = 0.40·m1 + 0.35·m2 + 0.25·m3` (convex; `maturity ∈ [0,1]` by
construction — B-S88F2-1). **neoteny `N = 1 − maturity`** (higher = more
plastic juvenile).

`effective D` here is the participation ratio of the `head_a` weight
singular spectrum — a cheap, deterministic rank proxy (NOT a rigorous
gradient-field dimensionality certificate; honest, C3 #5).

---

## §3. The 4 NK mechanisms — in the TRAINING LOOP

Each NK targets a distinct maturity axis and is applied **inside**
`train_cell`'s `for step in range(total)` loop (B-S88F2-2):

- **NK-1 CE-floor clamp** — when batch `ce_full < θ_floor`, the CE *term*
  is clamped `torch.clamp(ce_full, min=θ_floor)` — the juvenile keeps a
  non-zero loss, no over-fit gradient below the floor. **NK-1 clamps,
  never removes, CE** — §11-B precedence (CE is load-bearing) respected
  (B-S88F2-5). Targets M-1.
- **NK-2 plasticity-reinjection** — on saturation detection (maturity
  proxy crosses `SAT_TRIGGER`), apply a **targeted controlled Gaussian
  perturbation** to the `head_a` weights (axolotl regeneration mirror).
  Distinct from §81: §81 injected unconditional Engine-G noise; NK-2 is
  **saturation-triggered** and **targeted** at the byte-cascade attractor
  surface (the LM head). Targets M-2.
- **NK-3 dimensionality-floor** — an in-graph regulariser penalising the
  off-diagonal Gram energy of a `head_a` row slice (rows highly
  correlated ⇒ rank-collapsed ⇒ penalty), pushing effective D back up.
  Targets M-3.
- **NK-4 metamorphosis-block** — once maturity crosses `SAT_TRIGGER`,
  freeze the LR schedule at a juvenile floor (`NK4_LR_FLOOR_FRAC`).
  Dynamic, **state-triggered** — NOT epoch-budget early-stop. Targets the
  global maturation rate.

---

## §4. 3-cell trained-scale fire

§16-class `ConsciousDecoderV2` d768·12L·283.72M, from-scratch RANDOM
seed-fixed 1337 (`g_clm_from_scratch`, `base_ckpt=None`), §16 Ψ-anchored
carving corpus (Dir-I lever `l_psi_ctl + l_route`), 6000 step — config
byte-equal to §81-FIRE / §79.

| cell | config | what it measures |
|------|--------|------------------|
| cell0_baseline | normal training, no NK | trained-saturated (§16 pattern) — the §16.6-C reference |
| cell1_neoteny | full-neoteny NK-1+2+3+4 in-loop | does neoteny delay saturation? |
| cell2_neoteny_emit | neoteny ckpt + §24-style emission probe | non-saturated ckpt on the decision/emission axis |

Core measurement: does the neoteny arm hold **higher final CE** (juvenile,
no over-fit) **/ lower byte-cascade `maj_frac` / higher effective D /
≥1 §9-coherent body** vs the baseline arm?

---

## §5. 4-corner verdict (measured, NOT pre-loaded)

- **(α) NEOTENY-DELAYS-SATURATION-AT-TRAINED** — neoteny maturity <
  baseline maturity (saturation delayed) but not the full juvenile-but-
  competent corner.
- **(β) NEOTENY-UNDERTRAINS** — the NK mechanisms blocked training
  itself; neoteny CE did not descend (degenerate juvenile, §11-B no-CE
  echo). Honest negative.
- **(γ) JUVENILE-BUT-COMPETENT** — saturation delayed **AND** CE
  descended **AND** ≥1 §9-coherent body: a juvenile-but-competent regime
  exists. The §1.1-targeting positive.
- **(δ) NEOTENY-NO-EFFECT-AT-TRAINED** — NK mechanisms produced no
  measurable maturity difference; the §87-F2 stub's DIRECTIONAL-POSITIVE
  is stub-bound.

The fire-time risk (g3, pre-registered): neoteny either (a) escapes
saturation = a §1.1-relevant positive **or** (b) under-trains = degenerate
(§11-B echo). Both are honest results. The real question is whether a
**juvenile-but-competent** regime exists — saturation slowed AND learning
still happens.

---

## §6. Closed-form battery — B-S88F2-1..7 7/7 🔵

`blue_falsifier_s88f2.py` (sidecar; central
`state/verify_hexad_blue_2026_05_15/blue_falsifier.py` 0-line-diff):

| id | proposition | method |
|----|-------------|--------|
| B-S88F2-1 MATURITY-PROXY-BOUNDED | convex 3-proxy ⇒ maturity ∈ [0,1]; N=1−maturity ∈ [0,1] | sympy corners |
| B-S88F2-2 NK-MECHANISM-IN-TRAINING-LOOP | NK-1/2/3/4 referenced inside the in-loop step iteration + backward | AST structural |
| B-S88F2-3 ANTI-SATURATION-MONOTONE | ∂m1/∂ce < 0 ⇒ juvenile ⇒ lower maturity; NK-1 clamp floors CE | sympy ∂ |
| B-S88F2-4 §16.6-C-CONNECTION (연결부위) | baseline = §16-class decoder + Dir-I lever; maturity reads (ce,maj,D) | structural/AST |
| B-S88F2-5 §11-B-CE-BASE-PRESERVED (연결부위) | NK-1 clamps `ce_full`, NOT removes; cross_entropy + backward present | AST |
| B-S88F2-6 §87F2-STUB-CONNECTION (연결부위) | maturity weights + NK thresholds byte-equal to §87-F2 stub | AST byte-equal |
| B-S88F2-7 DETERMINISTIC | seeded torch/random/Generator; 0 sampling hits; greedy argmax | source structural |

**B-S88F2-NOTE** (empirical carve-out, NOT counted 🔵): whether the
neoteny arm **actually** produces a non-saturated juvenile-but-competent
ckpt — the 4-corner OUTCOME, the final CE / maturity / D / §9 body
numbers — is an SGD/measurement OUTCOME (B-D-NOTE / B-SCALE-NOTE /
B-EMERGE-NOTE / B-S87F2-NOTE family). The battery proves the **mechanism**
and its **connection-points** are honest, not that it **works**.

---

## §7. GOAL-legitimacy (§7 3-condition gate)

- **§7①** not-generic-LM-pretrain ✓ — the §16-class ConsciousDecoderV2
  trains from scratch on the anima Ψ-anchored carving corpus; the NK
  mechanisms are anima-substrate operations, not a generic-LM recipe.
- **§7②** not-generic-then-graft ✓ — zero external regularizer library;
  every NK mechanism is closed-form over anima's own CE / head_a weights
  / effective D.
- **§7③** anima-physics-as-source ✓ — every maturity proxy and NK trigger
  is a function of the anima training trajectory itself.

§11-B precedence respected: anima physics alone (no-CE) was measured
degenerate, so NK-1 **clamps** the CE term (never removes it). F-2 is a
CE-base overlay, not a no-CE re-attempt (B-S88F2-5).

`f1/f2/f3` + `B-IDENTITY-5` safe — Boolean / sympy / AST structural, NO
σ/τ/φ/J₂; corpus forbidden-token grep 0.

---

## §8. Honest C3 (≥10)

1. **Trained scale ≠ GOAL emergence.** §88-F2 measures the anti-
   saturation mechanism axis only. necessary-not-sufficient (B-EMERGE-7).
2. **§88-F2 differs structurally from §81/§82/§83-FIRE.** NK is applied
   **in the training loop** (learning-time anti-saturation), NOT as an
   inference overlay on an already-saturated ckpt. That is the whole
   point — overlays collapse, learning-time changes the ckpt produced.
3. **Under-training is a real, pre-registered risk.** NK could block
   learning itself — producing a degenerate juvenile (§11-B no-CE-
   degenerate echo). The (β) corner captures that honestly. A neoteny
   arm that costs all learning is **not** a path.
4. **The juvenile-but-competent regime is the actual question.** Neoteny
   that slows saturation **and** still learns **and** emits coherent
   bodies is the (γ) corner — that is the §1.1-targeting positive. Either
   verdict (positive or negative) is valuable.
5. **Effective D is a participation-ratio proxy.** It reads the `head_a`
   weight singular spectrum — a cheap deterministic rank proxy, NOT a
   rigorous gradient-field dimensionality certificate.
6. **The maturity 3-proxy and thresholds are §87-F2 design choices.**
   `θ_floor`=0.08, `θ_D`=4.0, `SAT_TRIGGER`=0.70, weights 0.40/0.35/0.25
   — well-formed (B-S88F2-1) but not unique.
7. **axolotl neoteny is an honest biological direction-anchor.** It gives
   a precedent for "stay juvenile, stay plastic." It does NOT transfer a
   capability. Biology USE ≠ anima emergence.
8. **Body §9 honest_coherent is cascade-absence, NOT correctness.** A
   §9-coherent body can still be garbled or memorized (B-EMERGE-7 family,
   §9.3 carve-out).
9. **NK-1 clamps the CE term, never removes it.** §11-B measured anima
   physics alone (CE removed) degenerate, so NK is a CE-base overlay.
   B-S88F2-5 closes this structurally.
10. **ckpt sha is fresh.** §16-byte-equal config (d/L/H/KV/seed/corpus
    class) is satisfied; the literal §16 sha differs (trajectory
    replicable, not literal identity) — honest.
11. **§1.1 data-regime irreducibility is targeted head-on.** §88-F2 asks
    whether learning-time anti-saturation can avoid the over-mature
    attractor. A measured negative narrows §1.1; a measured positive
    opens a new lever — both move the honest map.
12. **north-star + §15/§51/§72 milestone UNCHANGED; GOAL 미도달.**
    §88-F2 is a mechanism-axis fire on the §16.6-C / §1.1 bottleneck,
    not a GOAL milestone.

---

## §9. Verdict — MEASURED: (α) NEOTENY-DELAYS-SATURATION-AT-TRAINED

Fire-tier. 7/7 🔵 closed-form battery + 1 NOTE empirical carve-out.
runpod H100 80GB HBM3 pod `vydide8snncs1i` (the A100-PCIE pool gave a
CPU-contended host load avg 70-177 twice — H100 cascade fix landed), 3-cell
× 1500-step, train wall ~125-133 s/cell, orphan-0 pre+post. neoteny ckpt
sha256 `9ca8db4367a1b083…` pulled (1.13 GB).

**3-cell grid (measured):**

| cell | final CE | maturity | neoteny N | attractor maj_frac | effective D | §9 body |
|------|---------:|---------:|----------:|-------------------:|------------:|--------:|
| cell0_baseline | 0.00383 | 0.9496 | 0.0504 | 0.872 | 1.89 | 0/5 |
| cell1_neoteny | 0.04125 | 0.7478 | 0.2522 | 0.350 | 2.70 | 0/5 |
| cell2_neoteny_emit | 0.04125 | 0.7478 | 0.2522 | (physics_alive=False) | — | 0/5 |

**4-corner: α=True, β=False, γ=False, δ=False → (α) NEOTENY-DELAYS-
SATURATION-AT-TRAINED.** The neoteny arm measurably delayed saturation on
all three maturity proxies — final CE held 10.8× higher (0.041 vs 0.0038,
juvenile, no over-fit), byte-cascade `maj_frac` cut from 0.872 → 0.350,
effective D lifted 1.89 → 2.70 — **and it still learned** (CE descended
5.64 → 0.041, so NOT the (β) under-training corner). NK fired as designed:
NK-1 CE-floor clamp 953×, NK-2 plasticity-reinject 1×, NK-4 metamorphosis-
block engaged at step 200.

But it did **not** reach the full (γ) JUVENILE-BUT-COMPETENT corner: body
§9 honest_coherent = **0/5** on both arms. The neoteny ckpt is a
genuinely juvenile, non-saturated, attractor-shallowed ckpt — but its body
emission is still not §9-coherent. Saturation was delayed; coherent
juvenile competence was not demonstrated.

**Honest reading (g3):** axolotl neoteny is validated at trained scale as
a real **learning-time** anti-saturation mechanism — distinct from the
§81/§82/§83-FIRE inference overlays, which collapsed precisely because the
ckpt was already saturated. §88-F2 produces a ckpt that is NOT in the deep
byte-cascade basin. That is a directional positive on the §16.6-C / §1.1
axis. But anti-saturation ≠ competence: the body §9 0/5 shows the
non-saturated regime is not, by itself, coherent (necessary-not-sufficient,
B-EMERGE-7). The §1.1 data-regime bottleneck is **not** broken — neoteny
shifts *where* the ckpt sits in maturity space, not *whether* it can emit
coherent bodies. north-star + §15/§51/§72 milestone UNCHANGED; GOAL
unreached.
