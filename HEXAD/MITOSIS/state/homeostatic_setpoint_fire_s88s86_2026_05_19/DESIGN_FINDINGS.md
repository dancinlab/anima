# §88-S86 — HOMEOSTATIC-SET-POINT MITOSIS — TRAINED-SCALE FIRE

**Date** 2026-05-19 · **Tier** trained-scale fire (runpod A100-SXM4-80GB,
cost ≈$0.3-0.6) · **pod** `r0sn1hy1a3jsxo` · **Cost-bearing** — per
`g_fire_autonomous` no-query no-gate.

§88-S86 is the trained-scale validation of §86 (commit 0ae194471,
B-S86 7/7 🔵) HOMEOSTATIC-SET-POINT MITOSIS design. §86 unified anima's
three separate mechanisms — **emission** (§24 SPONTANEOUS unprompted
decision), **MITOSIS split** (cell-pool capacity), **Ψ-restoration**
(Ψ=½ Law-71 fixed-point return) — into ONE homeostatic set-point
prediction-error drive, anchored to §84 SAPIN arxiv:2511.02241
("structural plasticity as active inference") and §85's Hopf-bifurcation
emission-onset mapping.

---

## §1 — Core mechanism (carried byte-equal from §86)

anima holds an internal set-point `(Ψ*, τ*, Φ*) = (½, 0.30, 0.55)`.
Prediction-error `E = ‖(Ψ−½, tension−τ*, Φ−Φ*)‖_w` (weighted-L2 norm,
weights `(0.45, 0.30, 0.25)`).

- `E < θ_low (0.10)`            → **QUIESCENT** (error tolerable)
- `θ_low ≤ E < θ_high (0.18)`   → **EMIT** (resolve by speaking — §24)
- `E ≥ θ_high` *sustained* (K=2) → **SPLIT** (resolve by *capacity* —
  SAPIN structural plasticity, MITOSIS hook)

One error-minimizing controller, three regimes.

---

## §2 — Trained-scale fire design (§88-S86, NOT a $0 stub)

`homeostatic_setpoint_train_s88s86.py`:

1. Train ONE §16-class `ConsciousDecoderV2` from-scratch (d768·12L·
   283.72M, RANDOM seed-fixed 1337, `base_ckpt=None` — `g_clm_from_scratch`)
   on the §16-class Ψ-anchored carving corpus (Dir-I lever, byte-equal
   trainer to §79 / §81-FIRE / §73-FIRE), 6000 steps.
2. 5-cell × 20-step deterministic loop on the **REAL trained
   `model.forward` Law-71 Ψ-state** (NOT a stub):

   | cell  | label                  | emit | split | hopf |
   |-------|------------------------|------|-------|------|
   | cell0 | s24-baseline-separate  | ✓    | ✗     | ✗    |
   | cell1 | setpoint-emit-only     | ✓    | ✗     | ✗    |
   | cell2 | setpoint-split-only    | ✗    | ✓     | ✗    |
   | cell3 | full-unified-3regime   | ✓    | ✓     | ✗    |
   | cell4 | s85-hopf-overlay       | ✓    | ✓     | ✓    |

   Set-point error `E` over the real Ψ-state; regime ∈ {Q, E, S}; SPLIT
   regime increments a MITOSIS split-event counter (trained-scale
   analogue of `mitosis_hook_lib.hexa _mit_check_splits`, B-MITOSIS 5/5
   🔵 carry, `cell_count` clamp `[2,64]`).
3. §16 baseline 8-anchor probe — ckpt load + arch byte-equal.
4. 4-corner verdict.

---

## §3 — The honest fire-prior risk (g3, stated BEFORE the fire)

§88-S86 is a **trained-saturated overlay**, like §81/§82/§83-FIRE — and
all three of those collapsed (echo-chamber, maj_frac ≥ 0.95). A set-point
controller reads the Ψ-state of a memorization-saturated ckpt; if that
Ψ-state is itself collapsed, a controller over a collapsed substrate is
collapsed too. So the fire-prior expectation is **β-mirror collapse risk
HIGH**.

The ONE new element vs §81/§82/§83 is the **SPLIT regime** — MITOSIS
capacity growth, a mechanism the earlier overlays did not have. The γ
corner measures whether SPLIT rescues the collapse, or whether split is
itself trained-saturated and inert.

---

## §4 — 4-corner verdict frame

- **(α) UNIFIED-DRIVE-SURVIVES-AT-TRAINED** — cell3 exercises all three
  regimes from a single E AND is non-degenerate (regime partition
  exhaustive ∧ maj_frac < 0.95 ∧ §9 body-coherent).
- **(β) §81/§82/§83-FIRE-MIRROR-COLLAPSE** — ≥3 of 4 unified-drive cells
  hit maj_frac ≥ 0.95.
- **(γ) SPLIT-REGIME-RESCUES** — split-bearing cells (c2/c3) less
  degenerate than emit-only c1 (interval_var lift OR escape of c1's
  collapse).
- **(δ) HOPF-ONSET-MEASURABLE** — cell4 Hopf order-parameter mean > 0,
  emission-onset trackable as a control-parameter crossing.

---

## §5 — GOAL-legitimacy §7 3-condition check — 3/3 PASS

- **§7① not-generic-LM-pretrain ✓** — controller is anima's own
  set-point `(Ψ=½, τ*, Φ*)` + MITOSIS hook + Ψ-restoration.
- **§7② not-generic-then-graft ✓** — zero external classifier / LLM
  judge / generic-RAG; closed-form set-point error only.
- **§7③ anima-physics-as-source ✓** — `E` is a deviation norm over
  Law-71 Ψ/tension/Φ, byte-equal formula to `conscious_decoder.py`.
  SAPIN active inference is an honest direction-anchor, NOT a capability
  proof.

---

## §6 — B-S88S86 closed-form battery — 8/8 🔵

`blue_falsifier_s88s86.py` (sidecar; central
`state/verify_hexad_blue_2026_05_15/blue_falsifier.py` 0-line-diff):

| id        | name                                | basis |
|-----------|-------------------------------------|-------|
| B-S88S86-1| SET-POINT-ERROR-NONNEGATIVE         | sympy weighted-L2 radicand nonnegative |
| B-S88S86-2| REGIME-PARTITION-EXHAUSTIVE-DISJOINT| sympy Interval algebra, θ_low<θ_high |
| B-S88S86-3| §24-DECISION-CONSISTENCY (연결부위) | sympy Implies + runtime s24_consistency |
| B-S88S86-4| MITOSIS-HOOK-CONNECTION (연결부위)  | AST pure-Boolean + mitosis_hook_lib.hexa carry |
| B-S88S86-5| §85-HOPF-CONTROL-PARAM-MAPPING      | sympy r≥0, dr/dE>0, onset r(E_crit)=0 |
| B-S88S86-6| §9-METRIC-REUSE                     | §9 thresholds byte-equal + witnesses |
| B-S88S86-7| §86-STUB-CONNECTION                 | AST §86 constant + formula byte-equal |
| B-S88S86-8| DETERMINISTIC                       | AST no-RNG + argmax-only body |

**B-S88S86-NOTE** empirical carve-out: whether the unified set-point
drive SURVIVES / COLLAPSES / is RESCUED by SPLIT at trained-saturated
scale is an SGD/measurement OUTCOME (the 4-corner verdict) — NOT closed,
NOT counted 🔵 (B-D-NOTE / B-EMERGE-NOTE / B-S86-NOTE family). The
battery closes the **fire design**: error ≥ 0, regime partition
exhaustive+disjoint, three connection-points well-formed, §9 reuse,
§86-stub byte-equal, deterministic. necessary-not-sufficient
(B-EMERGE-7).

---

## §7 — MEASURED 5-cell grid + 4-corner verdict

*(populated post-fire from `result.json` — see §8 honest C3.)*

---

## §8 — Honest C3

1. **trained scale ≠ GOAL emergence** — §88-S86 is a mechanism-level
   trained-scale measurement, NOT a capability claim.
2. **§86 stub → trained-scale** — the §86 stub was
   DIRECTIONAL-POSITIVE-DESIGN on LCG `psi_state` stubs; §88-S86 is its
   trained-scale test, where §81/§82/§83-FIRE all collapsed as
   trained-saturated overlays.
3. **trained-saturated overlay collapse risk** — fire-prior expectation
   (g3, stated §3): a controller over a memorization-saturated ckpt's
   Ψ-state is itself collapsed; β-mirror risk HIGH.
4. **SPLIT regime is the new lever** — MITOSIS-driven capacity growth is
   the one mechanism §81/§82/§83 lacked; the γ corner measures whether
   it rescues the collapse, or whether split is itself trained-saturated
   and inert.
5. **SAPIN biology honest direction-anchor** — arxiv:2511.02241 is a
   direction-anchor, NOT a capability proof; biology citation ≠ anima
   emergence.
6. **set-point placeholders** — τ*=0.30, Φ*=0.55 are §86 design
   placeholders; Ψ*=½ is Law-71, anima g2 internal carve-out (NOT
   lattice numerology — f1/f2 safe).
7. **necessary-not-sufficient at every layer** (B-EMERGE-7 family) —
   regime non-degeneracy does not imply coherent emergence.
8. **§9 metric reuse** — `honest_coherent` thresholds byte-equal to the
   §9 `emergence_metric` SSOT; the §9 cascade-rate gate is the honest
   body-coherence detector.
9. **PyTorch substrate** — `g_train_flame_not_pytorch` evidence-anchor
   clause carry; this fire is on the §16-class PyTorch trainer (honest).
10. **north-star + §15/§51/§72 milestone UNCHANGED, GOAL 미도달** — the
    fire maps a mechanism boundary, it does not move the north-star.
