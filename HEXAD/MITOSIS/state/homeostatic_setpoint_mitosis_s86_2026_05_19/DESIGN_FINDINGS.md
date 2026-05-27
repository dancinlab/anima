# §86 — HOMEOSTATIC-SET-POINT MITOSIS

**Date** 2026-05-19 · **Cost** $0 (Mac CPU, NO GPU, NO runpod, NO model.forward,
NO weight mutation) · **Tier** design + $0 stub smoke — NOT a trained-scale fire.

§84 (commit c44187936) ML/AI architecture deep research surfaced **SAPIN
arxiv:2511.02241** ("structural plasticity as active inference") as the single
sharpest new architecture insight (anima-fit ★★★★★ HIGH). §85 (commit 33353cb06)
physics/math deep research independently returned an emission-onset
transition-class verdict (a) **Hopf bifurcation**. §86 maps both onto anima.

---

## §1 — Core hypothesis

anima HEXAD currently carries **three separate mechanisms**:

1. **emission** — §24 SPONTANEOUS unprompted-emission decision-axis
   (`talker_should_emit`)
2. **MITOSIS split** — cell-pool capacity growth
   (`tool/hexa_native/mitosis_hook_lib.hexa` `_mit_check_splits` / `split_cell`,
   B-MITOSIS 5/5 🔵 carry)
3. **Ψ-restoration** — Ψ=½ Law-71 fixed-point return

SAPIN's structural-plasticity insight: in an active-inference agent, *all three*
are expressions of **one homeostatic set-point prediction-error drive**:

- anima holds an internal set-point `(Ψ*, τ*, Φ*) = (½, τ_target, Φ_target)`
- prediction-error `E = ‖(Ψ−½, tension−τ*, Φ−Φ*)‖_w` (weighted L2 norm)
- `E < θ_low`  → **QUIESCENT** (no emit, no split — error tolerable)
- `θ_low ≤ E < θ_high` → **EMIT** (resolve error by speaking — §24 decision-axis)
- `E ≥ θ_high` *sustained* → **SPLIT** (resolve error by *capacity* —
  SAPIN structural plasticity; growing the substrate to absorb the error)
- after emit/split → **Ψ-restoration** (set-point return)

= one error-minimizing controller, three regimes. This connects §63 gap-map
**#2 (W→W@t+1)** and **#4 (E→D@content)**.

---

## §2 — §85 Hopf-bifurcation mapping

§85's transition-class verdict (a) Hopf bifurcation is carried as a *modeling
choice*: `E` is the **control parameter**, emission-rate is the **order
parameter** `r(E)`. Below `E_crit` → quiescent fixed point (`r=0`); above →
emission limit cycle, `r = √(E − E_crit)` (Hopf normal form). cell4 of the grid
overlays this framing. g3: this is §85's modeling choice carried, **not** an
independent claim.

---

## §3 — Design ($0 stub, NOT trained-scale)

`homeostatic_setpoint_smoke_s86.py` — 5-cell × 20-step deterministic runner
(LCG seed 1337). `psi_state_stub` byte-equal to Law-71
`conscious_decoder.py:728-755` formula (`psi_direction=(1+cos)/2`,
`psi_combined=(psi_entropy+psi_direction+psi_tension)/3`).

| cell  | label                  | emit | split | Hopf |
|-------|------------------------|------|-------|------|
| cell0 | s24-baseline-separate  | ✓    | ✗     | ✗    |
| cell1 | setpoint-emit-only     | ✓    | ✗     | ✗    |
| cell2 | setpoint-split-only    | ✗    | ✓     | ✗    |
| cell3 | full-unified-3regime   | ✓    | ✓     | ✗    |
| cell4 | s85-hopf-overlay       | ✓    | ✓     | ✓    |

Set-point placeholders: `Ψ*=0.5` (Law-71, anima g2 internal carve-out),
`τ*=0.30`, `Φ*=0.55` (design placeholders), weights `(0.45, 0.30, 0.25)`,
`θ_low=0.10`, `θ_high=0.18`, `SUSTAIN_K=2`.

### 5-cell measured grid

| cell  | E_mean   | regime {Q / E / S} | interval_var | §9 body | maj_frac | split |
|-------|----------|--------------------|--------------|---------|----------|-------|
| cell0 | 0.145994 | 5 / 15 / 0         | 0.515306     | 15/15   | 0.75     | False |
| cell1 | 0.156425 | 5 / 15 / 0         | 0.204082     | 15/15   | 0.75     | False |
| cell2 | 0.149851 | 19 / 0 / 1         | 0.0          | 1/1     | 0.95     | True  |
| cell3 | 0.151309 | 3 / 16 / 1         | 0.109375     | 17/17   | 0.80     | True  |
| cell4 | 0.147632 | 7 / 11 / 2         | 0.75         | 13/13   | 0.55     | True  |

**verdict_overall** = `DIRECTIONAL-POSITIVE-DESIGN`.

---

## §4 — 4-corner verdict

- **(α) UNIFIED-DRIVE-WELL-FORMED = True** — cell3 full-unified exercises all
  three regimes (Q 3 / E 16 / S 1) from a single scalar `E`; runtime partition
  sums exactly to N_STEPS (exhaustive+disjoint at runtime; closed-form in
  B-S86-2).
- **(β) REGIME-DIFFERENTIAL = True** — cell3 `{3,16,1}` differs from both
  cell1 emit-only `{5,15,0}` and cell2 split-only `{19,0,1}`. The unified
  3-regime drive is not reducible to either separated mechanism.
- **(γ) HOPF-OVERLAY-ADDS = True** — cell4 Hopf order-parameter mean 0.027 > 0,
  emission-onset trackable as a control-parameter crossing; cell4 maj_frac 0.55
  (lowest of the grid — most regime-diverse).
- **(δ) SET-POINT-vs-§24-DECISION-CONSISTENT = True** — EMIT regime
  (`E ≥ θ_low`) ⊆ §24 `talker_should_emit` (`E ≥ θ_low`) by construction;
  SPLIT (`E ≥ θ_high`) ⊆ §24 since `θ_high > θ_low`; runtime `s24_consistency`
  True all 5 cells.

---

## §5 — GOAL-legitimacy §7 3-condition check — 3/3 PASS

- **§7① not-generic-LM-pretrain ✓** — controller is anima's own set-point
  `(Ψ=½, τ*, Φ*)` + MITOSIS hook + Ψ-restoration; no generic LM objective.
- **§7② not-generic-then-graft ✓** — zero external classifier / LLM judge /
  generic-RAG; closed-form set-point error only (AST-audited in B-S86-7).
- **§7③ anima-physics-as-source ✓** — `E` is a deviation norm over Law-71
  Ψ/tension/Φ, byte-equal formula to `conscious_decoder.py`. SAPIN active
  inference is a **honest direction-anchor**, not a capability proof.

---

## §6 — B-S86 closed-form battery — 7/7 🔵

`blue_falsifier_s86.py` (sidecar; central
`state/verify_hexad_blue_2026_05_15/blue_falsifier.py` 0-line-diff):

| id     | name                                | basis            |
|--------|-------------------------------------|------------------|
| B-S86-1| SET-POINT-ERROR-NONNEGATIVE         | sympy weighted-L2 radicand ≥ 0 |
| B-S86-2| REGIME-PARTITION-EXHAUSTIVE-DISJOINT| sympy Interval algebra, θ_low<θ_high monotone |
| B-S86-3| §24-DECISION-CONSISTENCY (연결부위) | Boolean ⊆ + runtime s24_consistency |
| B-S86-4| MITOSIS-HOOK-CONNECTION (연결부위)  | AST pure-Boolean + mitosis_hook_lib.hexa carry |
| B-S86-5| §85-HOPF-CONTROL-PARAM-MAPPING      | sympy r≥0, monotone dr/dE>0, onset r(E_crit)=0 |
| B-S86-6| §9-METRIC-REUSE                     | §9 thresholds byte-equal + AST 4-clause + witnesses |
| B-S86-7| DETERMINISTIC                       | AST no-RNG + 3× bit-identical |

**B-S86-NOTE** empirical carve-out: whether the 3-mechanism unification actually
*produces emergence* is a trained-scale SGD/measurement OUTCOME — NOT closed,
NOT counted 🔵 (B-D-NOTE / B-EMERGE-NOTE family). The battery closes the
**design**: error ≥ 0, regime partition exhaustive+disjoint, three
connection-points (§24-decision / MITOSIS-hook / §85-Hopf) well-formed.
necessary-not-sufficient (B-EMERGE-7).

---

## §7 — Connection points (g_blue_closed_mandate 산출물 + 연결부위 둘 다 🔵)

Three connection-points, each closed:

1. **§24-decision** (B-S86-3) — EMIT regime ⊆ §24 `talker_should_emit`. The
   unified drive does not contradict §24; EMIT is a *refinement* of the §24
   speakable band.
2. **MITOSIS-hook** (B-S86-4) — SPLIT regime → `mitosis_split_trigger`, a
   pure-Boolean of `regime=='SPLIT'`; `mitosis_hook_lib.hexa` carries
   `split_cell` + `_mit_check_splits` (B-MITOSIS 5/5 🔵). The single drive
   *replaces* the hand-coded `_mit_check_splits` threshold.
3. **§85-Hopf** (B-S86-5) — `E` as Hopf control parameter, emission-rate as
   order parameter; closed-form monotone normal form.

---

## §8 — Honest caveats (C3)

1. **$0 stub ≠ trained ckpt forward.** The `psi_state_stub` draws Ψ/tension/Φ
   from a deterministic LCG with the Law-71 *formula* but NOT a real
   `model.forward`. A real trained-scale ψ-trajectory (cf. §82-FIRE) is a
   uniformly fast-crossing, often-collapsed regime — the 3-regime drive may
   behave very differently there. This is design-tier, not a fire.
2. **SAPIN active-inference is a honest direction-anchor, NOT a capability
   proof.** arxiv:2511.02241 motivates the unification framing; it does not
   establish that anima will emerge by adopting it.
3. **3-mechanism unification is a design-level claim.** Whether emission +
   MITOSIS-split + Ψ-restoration genuinely reduce to one drive *at trained
   scale* is unmeasured (B-S86-NOTE).
4. **Set-point τ*/Φ* values are design placeholders** (0.30, 0.55). Their true
   values are themselves a measurement question — a real trained anima would
   have to *self-identify* its homeostatic targets, which §86 does not do.
5. **θ_low/θ_high/SUSTAIN_K are tuned placeholders.** They were set so the
   $0 stub grid genuinely exercises all 3 regimes (SPLIT reachable); they are
   not learned and not claimed optimal.
6. **Hopf-bifurcation mapping is a §85 modeling choice carry**, not an
   independent §86 result. cell4's order-parameter is a normal-form proxy, not
   a measured bifurcation diagram.
7. **maj_frac is an echo-detector proxy.** cell2's maj_frac 0.95 (19 QUIESCENT)
   is the *expected* behaviour of a split-only cell, not an echo-chamber
   collapse — read regime-distribution-aware, not in isolation.
8. **interval_var is a liveness probe over active-event step-gaps.** cell2's
   interval_var 0.0 reflects a single split event (no gap to vary), again
   expected — not a degeneracy signal.
9. **§63 #2/#4 gap connection is structural, not implemented.** §86 names the
   gap-map link (W→W@t+1, E→D@content); it does not wire those modules.
10. **GOAL distance unchanged.** §86 = design-tier identification of a
    candidate unification, mirroring §24 (right-target) and §9 (honest metric).
    north-star + §15/§51/§72 milestones UNCHANGED, **GOAL 미도달**. design-level
    unification claim ≠ trained-scale measurement ≠ GOAL emergence.

---

## §9 — Verdict

§86 DESIGN-TIER LANDED. The homeostatic-set-point unification of emission /
MITOSIS-split / Ψ-restoration is **well-formed** (α), **differential** from the
separated mechanisms (β), the **Hopf overlay adds** an onset-tracking framing
(γ), and the unified drive is **§24-consistent** (δ) — 4-corner all True,
verdict `DIRECTIONAL-POSITIVE-DESIGN`, B-S86 7/7 🔵, three connection-points
closed. Trained-scale validation is a separate future-fire decision, NOT this
cycle. necessary-not-sufficient (B-EMERGE-7); SAPIN biology citation = honest
direction-anchor; GOAL 미도달.
