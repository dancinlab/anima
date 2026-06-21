# H_1524 — 🧱 MODULATOR DIVERSITY (신경조절 다양성) vs the H_1284 wall

**tier:** 🧱 WALL HOLDS (CLOSED-NEGATIVE) · **verdict:** 🔴/🧱 DIRECTIONAL
**wired:** DIRECTIONAL-mirror (numpy; HARD-GATE-1) — engine-native R2 = ING follow-on
**source:** UNIVERSE (fleet-full wall-break lane) · **lens:** neuromodulation specificity (c15, a_no_llm_frame_trap)

## Claim
The H_1284 NEUROMODULATION wall (a SINGLE global context-adaptive gain never
beats a single well-tuned FIXED operating point — no-free-lunch, general) can be
broken by a DIFFERENT mechanism-family: **MODULATOR DIVERSITY** — N independent,
axis-targeted modulators (DA→abstain/consolidate, NE/ACh→split-rate from a
recall-noise floor, ACh→LR from fast-vs-slow surprise), each with its OWN signal
and OWN EMA (no sharing), mirroring real separate-nuclei neuromodulation
(the H_1284 FREEZE cites exactly DA/NE/ACh; anima's §Neuropharm already realizes
the per-axis structure). Hypothesis: **specificity** beats both a single global
gain AND best-fixed across regimes.

## Result — 🔴/🧱 WALL HOLDS
Grid-tuned best-fixed LR0*=0.1, TH0*=0.2 (disjoint tune seed 7); seeds [11,22,33];
MARGIN 0.05 frozen.

| regime | A fixed | S global | **D diversity** | D-collapse | D−A | D−collapse |
|--------|--------:|---------:|----------------:|-----------:|----:|-----------:|
| R1_STABLE | 0.5744 | 0.5678 | 0.5733 | 0.5733 | −0.0011 | **0.0000** |
| R2_DRIFT  | 0.4389 | 0.3589 | 0.4333 | 0.4333 | −0.0056 | **0.0000** |
| R3_NOISE  | 0.4156 | 0.3200 | 0.4156 | 0.4156 | +0.0000 | **0.0000** |

- **(c1)** D beats A+MARGIN on **0/3** regimes (wins=[]) → not GREEN.
- **(c2) DECISIVE specificity ablation:** D − D-COLLAPSE = **0.0000 on every
  regime**. Collapsing the N=3 independent modulators onto ONE global signal
  produces the EXACT same capability → **specificity is INERT**. Per-channel
  marginals (ACh/split/DA) all ≈0.0 — no channel contributes.
- **(c3)** S (H_1284's global controller) loses on every regime (S−A =
  −0.007/−0.080/−0.096) — reproduces the wall faithfully.
- fab_ok TRUE · never_much_worse TRUE.

**Mechanism of the no-free-lunch:** at the grid-tuned best-fixed operating point
the substrate signals (fast-vs-slow surprise, recall-noise floor, reward) stay
near their own baselines, so the knobs barely deviate from best-fixed — and any
deviation buys nothing over a single global gain. Independence/specificity adds
zero exploitable structure when one constant point is already adequate.

**Wall class (a_break_the_wall TAXONOMY):** (d) GENUINE no-free-lunch ceiling
(not metric-artifact/confound/infra). This is the **Nth independent lens** in a
multi-lens depletion: H_1284 (global gain) · H_1284_R2 (ideation) · H_1284_R3
(regime-switch) · Amoeba homeostatic-buffer (H_1509/b/c) · **now
diversity/specificity**. The strongest biological argument FOR neuromodulation
(separate nuclei → separate targets) ALSO fails, with a decisive specificity
ablation (D≡D-COLLAPSE). The wall holds **more confidently** after this lens.

## Honesty / scope (c9)
- DIRECTIONAL only (numpy mirror of CORE/engine_cli.hexa VAdaptField; host no
  torch). **HARD-GATE-1**: .py+numpy → verdict cannot be terminal; engine-native
  R2 (.hexa via CORE) = binding ING follow-on (for a RED/🧱 the directional
  result already strongly supports the wall).
- TOY: 30 facts / 3 seeds / one paradigm / DIM=16 — scale/paraphrase/real-corpus/
  engine-transfer UNVERIFIED (a_scale_honest_scope, a_toy_scale_recheck).
- frozen-first: MARGIN 0.05 + all bars pre-registered; NO tune-to-green (RED
  reported RED, c9). Environment byte-reused from H_1284 (no env change). live
  CORE/*.hexa UNTOUCHED. $0 CPU.

## Artifacts
- `state/1524_neuromod_diversity/h1524_diversity.py`
- `state/verdicts/1524_neuromod_diversity/H_1524_FREEZE.txt` (pre-registration)
- `state/verdicts/1524_neuromod_diversity/H_1524.txt` (result)
- `state/verdicts/1524_neuromod_diversity/H_1524_R1.json` (raw)

## xref
H_1284 · H_1284_R2 · H_1284_R3 · H_1509/b/c · H_1228 · H_1230 · H_1281 · H_1285 ·
H_1290 · §Neuropharm(H_1502) · a_break_the_wall · a_no_llm_frame_trap ·
a_engine_native_learning · a_verified_must_wire · a_autonomy_over_hardcode ·
a_paper_negative_ok · a_scale_honest_scope · a_toy_scale_recheck ·
p1·p2·p3·p6·p7·p8·c9·c15.
