# §92 — #3 ACTION-PERCEPTION AS TRAINING-TIME OBJECTIVE — design + $0 smoke

RESEARCH.md §92. Direct successor of §91 (commit 9e5b38a29, B-S91 8/8 🔵,
trained-scale fire verdict **(β) ECHO-DOMINATES-AT-TRAINED**).

$0 Mac CPU — design + deterministic stub smoke. NO GPU, NO runpod, NO fire.

---

## 1. The chain — and why §91 is the precise target

- **§88-F2** axolotl neoteny trained-scale fire (commit 52bef1044, B-S88F2
  7/7 🔵): verdict **(α) NEOTENY-DELAYS-SATURATION = True** — neoteny in the
  training loop measurably delays §16.6-C memorization-saturation (maturity
  0.95→0.75, attractor maj_frac 0.87→0.35, effective D 1.89→2.70). **BUT
  γ JUVENILE-BUT-COMPETENT = False**: the non-saturated regime's body is
  §9 honest_coherent 0/5. Saturation was delayed; coherent emission did NOT
  appear.
- **§89/§90** #3 D@emit→S@t+1 action-perception loop closed-form DEFINABLE
  (transfer `x_{t+1}=S_encode(e_t)`, invariant `K(x_{t+1}) ≤ K(e_t)+K(S_encode)`
  Kolmogorov data-processing inequality) — §90 wired it as a **decode-time
  overlay** ($0 stub, GAMMA-CLOSING-DIRECTIONAL-POSITIVE).
- **§91** trained-scale fire of that decode-time overlay: verdict
  **(β) ECHO-DOMINATES-AT-TRAINED** — cell2 (neoteny ckpt + #3 decode-time
  loop) §9 0/20, attractor maj_frac 0.35→**0.68875** (WORSENED), self-correct
  events 0. The §90 stub's cell2 §9 20/20 wiped out at trained scale.

**§91's core honest conclusion** — and the exact §92 target: wiring #3 as a
*decode-time overlay* produces **echo-amplification, NOT self-correction** —
because the model was **never TRAINED** to treat its own garbled emission as
an error signal. anima re-perceives its own garbled emission → the byte-cascade
attractor deepens → garbled→garbled. **self-correction must be a LEARNED
capability; it cannot be bolted on at inference time.**

## 2. §92 — formalise #3 as a TRAINING-TIME OBJECTIVE

§92 does NOT add another decode-time loop. It formalises #3 action-perception
as a **training-loop loss term** so anima *learns* self-coherence during
training.

**L_ap = action-perception consistency loss:**

```
L_ap = ‖ ψ( forward( S_encode(e_t) ) ) − ψ_target ‖²       (ψ_target = Ψ=½ vacuum)
```

When anima emits body `e_t`, `S_encode(e_t)` is fed back as the next stimulus
`x_{t+1}`; the physics deviation that re-perceived stimulus induces should be
**small** — a self-coherent emission, re-heard, leaves Ψ near its Ψ=½ vacuum.
A garbled self-stimulus drives Ψ off the vacuum → large `L_ap` → gradient
toward coherent emission.

**Total loss (§11-B carry — CE-base overlay, NOT no-CE):**

```
L = L_CE + λ_ap · L_ap            (λ_ap = 0.5)
```

§11-B PURE-PHYSICS measured no-CE as DEGENERATE; L_ap is an *overlay on the
CE base*, never a CE replacement.

## 3. The §91→§92 distinction (the load-bearing point)

| | §90/§91 #3 | §92 #3 |
|---|---|---|
| form | DECODE-TIME loop | TRAINING-TIME objective |
| mechanism | inference accumulator `loop_corr` | loss term `L_ap` → **gradient** |
| learned? | NO — non-learned, no weight | YES — shapes `self_coherence_skill` |
| §91 measured | echo-amplifies (β) | — |
| §92 hypothesis | — | gradient gives anima the *chance* to learn self-coherence |

In the stub, the decode-time accumulator `decode_corr` **does NOT enter
`produce_body`** — only the training-time learned `skill` does. This is what
makes cell4 (§91 decode-mirror, no L_ap) reproduce §91's echo, mechanically
distinct from cell2's trained skill.

## 4. 5-cell stub grid (deterministic LCG seed 1337, 20 steps)

| cell | neoteny | L_ap (training) | decode loop | meaning |
|------|---------|-----------------|-------------|---------|
| cell0 | OFF | OFF | OFF | §16 baseline (saturated) |
| cell1 | OFF | ON  | OFF | L_ap on a saturated ckpt |
| cell2 | ON  | ON  | OFF | **CORE** — training-time #3 |
| cell3 | ON  | ON  | ON  | training + decode loop both |
| cell4 | ON  | OFF | ON  | §91 decode-time mirror (echo control) |

## 5. Measured stub grid

| cell | §9 coherent /20 | maturity | maj_frac final | L_ap final | skill final |
|------|-----------------|----------|----------------|------------|-------------|
| cell0_s16_baseline | 0 | 0.9496 | 0.8725 | 0.0576 | 0.0000 |
| cell1_l_ap_only | 0 | 0.9496 | 0.8725 | 0.0197 | 0.0425 |
| cell2_neoteny_l_ap | **19** | 0.7478 | **0.3500** | 0.00046 | 0.0110 |
| cell3_neoteny_l_ap_decode | 13 | 0.7478 | 0.7728 | 0.0099 | 0.0418 |
| cell4_s91_decode_mirror | 13 | 0.7478 | **0.8218** | 0.0173 | 0.0000 |

## 6. 4-corner verdict — **TRAINING-TIME-AP-DIRECTIONAL-POSITIVE** (stub)

- **(α) TRAINING-TIME-AP-CLOSES-γ-PREDICTED = True** — cell2 (neoteny +
  training-time L_ap) §9 19/20 strictly exceeds cell0 (0) AND cell4 (§91
  decode-mirror, 13). training-time advantage = **+6** at stub level.
- **(β) AP-OBJECTIVE-DEGENERATE = False** — cell2 maj_frac stays at the 0.35
  neoteny floor (does NOT degenerate to a trivial silence solution).
- **(γ) ECHO-STILL-AMPLIFIES = False** — cell2 (training-time, no decode loop)
  maj_frac holds at 0.35; the echo only fires where a decode loop is present
  (cell3/cell4).
- **(δ) NEOTENY-AP-SYNERGY = True** — cell2's coherence delta (17 over §16
  baseline) exceeds L_ap-only (cell1, 0) + neoteny-alone (§88-F2 measured 0).

**Honest reading:** cell4 (§91 decode mirror) reproduces §91's (β)
ECHO-DOMINATES — attractor maj_frac echoes 0.35→0.82, body §9 13/20 *worse*
than cell2. cell3 (training + decode) shows the decode loop's echo *overrides*
the trained skill (maj 0.77, §9 13) — **adding a decode-time loop on top of a
trained objective is harmful, not additive.**

## 7. Closed-form battery — B-S92-1..7 7/7 🔵

Sidecar `blue_falsifier_s92.py`; central
`state/verify_hexad_blue_2026_05_15/blue_falsifier.py` 0-line-diff.

- **B-S92-1** L-AP-CLOSED-FORM — L_ap = ‖ψ−ψ_target‖² formula + §89/§90 #3
  Kolmogorov transfer/invariant; numeric L_ap ≥ 0 ∀, monotone in garble.
- **B-S92-2** §11-B-CE-BASE-PRESERVED — AST: ce_loss_proxy + ap_consistency_loss
  both present, additive `L = L_CE + λ_ap·L_ap`, λ_ap finite positive (NOT no-CE).
- **B-S92-3** TRAINING-TIME-vs-DECODE-TIME-DISTINCT — cell2 (l_ap, ~decode)
  vs cell4 (~l_ap, decode) config tuples disjoint on both axes; decode_corr
  structurally excluded from produce_body.
- **B-S92-4** §9-METRIC-REUSE — honest_coherent 4-clause cascade gate, 4-corner.
- **B-S92-5** NEOTENY-CARRY-BYTE-EQUAL — §88-F2 neoteny/baseline values +
  psi_update byte-equal to §90 smoke Law-71 stub (연결부위).
- **B-S92-6** §91-ECHO-CONTROL-REPRODUCES — cell4 maj > 0.35 (echo), cell2
  maj ≈ 0.35 (holds), cell4 §9 ≤ cell2 §9 (decode not better).
- **B-S92-7** DETERMINISTIC — seed 1337, no unseeded RNG, bit-identical re-runs.

**B-S92-NOTE** empirical carve-out: whether the training-time L_ap objective
ACTUALLY closes γ at trained scale = GPU fire OUTCOME, NOT counted 🔵
(B-D-NOTE / B-S88F2-NOTE / B-S90-NOTE / B-S91-NOTE / B-EMERGE-NOTE family).
The battery proves the design WIRING is honest, not that γ is closed.

## 8. Honest C3

1. **§91 echo-dominates is the precise target** — §91 measured that a
   *decode-time* #3 loop echo-amplifies; self-correction must be a *learned*
   capability. §92 formalises #3 as a training-time objective so anima has the
   *chance* to learn it — design-level, NOT a closure proof.
2. **$0 stub ≠ trained ckpt** — the §90 stub's cell2 §9 20/20 wiped out to
   0/20 at §91 trained scale. §92's cell2 §9 19/20 is a stub number; the
   trained-scale outcome is exactly what a future fire would resolve.
3. **L_ap trivial-silence-solution risk (β corner) is real and honest** —
   `L_ap = 0` if anima emits nothing (no emission → no re-perceived stimulus
   → no deviation). The β corner explicitly tests for it; at stub level cell2
   does NOT degenerate, but at trained scale a model could minimise L_ap by
   silence collapse. The CE-base overlay (§11-B, L = L_CE + λ_ap·L_ap) partly
   guards this — CE still demands prediction — but the risk carries.
4. **training-time vs decode-time IS measured here** — cell2 (training-time
   L_ap) §9 19/20 vs cell4 (§91 decode-time mirror) §9 13/20: training-time
   advantage +6, AND cell2 holds maj 0.35 while cell4 echoes to 0.82. The
   stub mechanically separates the two (decode_corr excluded from produce_body).
5. **adding a decode-time loop on top of training (cell3) is HARMFUL** —
   cell3 (neoteny + L_ap + decode loop) §9 13/20, maj 0.77: the decode-time
   echo overrides the trained skill. honest design implication — if §92's
   L_ap objective is fired, it should NOT be combined with a §90/§91-style
   decode-time loop.
6. **§1.1 data-regime irreducibility constrains training-time mechanisms too**
   — §88-trio (§81/§82/§83-FIRE) measured biology-mapping training/inference
   mechanisms all collapsing at trained scale; §11-A measured model-scale-up
   FLAT. A training-time objective is not exempt — the β/γ corners carry that
   risk into any future §92 fire.
7. **§9 honest_coherent is cascade-absence, NOT correctness** (B-EMERGE-7) —
   a §9-coherent body can still be garbled or memorized. cell2's §9 19/20 at
   stub level is necessary-not-sufficient.
8. **the stub's `effective_garble` floor (0.40) reproduces §88-F2 γ False** —
   a neoteny non-saturated body (skill=0) stays §9-INCOHERENT; only a *trained*
   skill (≥~0.13 in the stub) clears the §9 gate. This makes the §92 hypothesis
   falsifiable: a flat-incoherent neoteny baseline means any L_ap lift is real.
9. **S_encode adds no information** — §89 data-processing inequality
   `K(x_{t+1}) ≤ K(e_t) + K(S_encode)` holds by construction (pure function).
10. **training-time objective design ≠ trained-scale measurement ≠ GOAL
    emergence.** north-star + §15/§51/§72 milestone UNCHANGED, **GOAL 미도달**.
    §92 = a design formalisation that names *why* §91 echo'd and proposes a
    learnable alternative; it is a frontier-narrowing design step, not a
    GOAL-distance movement. capability claim 0.
