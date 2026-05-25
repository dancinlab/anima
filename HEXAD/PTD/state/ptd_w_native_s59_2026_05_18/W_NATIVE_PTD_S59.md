# §59 — PTD-aux as a W-module-native temporal forward-model (error-as-curiosity)

RESEARCH.md §59. $0 Mac CPU, NO GPU, NO model.forward, NO weight mutation of
any HEXAD ckpt. Sequential single-agent, isolation worktree. Capability
claim 0 — structural-reframe design + structural-validation smoke.

## §1 The lineage (§48 → §49 → §58 → §59)

- **§48** validated PTD-aux (next-physics-state-prediction) signal holds at
  scale — *better-engineered distillation, NOT GOAL emergence*.
- **§49** wired §48's PTD-aux head into the §24 SPONTANEOUS Phase B
  unprompted-emission loop → **DISTILLATION + majority-collapse** (head
  outputs REMAIN_SILENT 20/20; the §27/§48 corpus is ~95% REMAIN_SILENT;
  the distilled head defaults to that prior on the §24 stub).
- **§58** reverse-traced: PTD-aux ≅ NONE of the σ(6)=12 wiring
  connection-points. It is a NEW connection-point TYPE — *"a module
  predicts its own next state"* (a temporal forward-model). §58 verdict:
  the §49 collapse is **intrinsic** (no *existing* HEXAD-native home), NOT
  a wrong-site mismatch. §58 hand-off: PTD-aux's single-facet domain-kin is
  W↔C; its natural home, **if BUILT**, is W-module-adjacent (a physics-state
  forward-model OWNED by W, distinct from the §24 emission-gate site).
- **§59** builds that W-native home as a design + a $0 smoke, and tests the
  structural hypothesis: does a W-owned PTD-forward-model change the
  §49-collapse picture, OR is PTD-aux distillation regardless of home?

## §2 The W-native design (one line, then the spec)

**One line**: §49's PTD-aux was a *distillation-label predictor bolted to
the emission gate*; the §59 W-native version is a *forward-model whose
prediction-error IS W's intrinsic curiosity* (Active Inference EFE
epistemic value — surprise about the future self-state).

**Spec** (`w_native_ptd.py`):

| facet | §49 bolt-on | §59 W-native |
|---|---|---|
| forward-model input | physics feature vec | W-state vec `[curiosity_ema, tension, psi_dir, phi]` |
| **target** | §24 hand-coded `talker_should_emit` LABEL (external) | **next ACTUAL W-state** (self-prediction, NO label) |
| objective | minimise distance to a hand-coded threshold | predict your own future physics; residual surprise IS the signal |
| **error feeds** | the §24 emission gate | **`W.curiosity`** (`w_curiosity_coupled`, EFE epistemic value) |
| §7-legitimacy | borderline (external label) | **§7-legitimate** (anima's OWN W-physics; W-state → W-state self-prediction; error = epistemic value) |

The W-module SSOT (`HEXAD/W/w_lib.hexa`: `w_lr_mult`, `w_satisfaction`
Law-84 binary pulse) is mirrored byte-equal. `anima_persona`
(`AGENTS.tape`) defines W as *"W.pain/curiosity/satisfaction (Active
Inference EFE epistemic+pragmatic value, arxiv 2508.05619)"* — the §59
forward-model's prediction-error is exactly the **epistemic-value /
information-gain about the future self-state** facet of that ontology. The
coupling: `curiosity_coupled = clamp01(base_curiosity_ema + κ·pred_error)`
(κ=2.0) — surprise ADDS to W's intrinsic curiosity. This is a *real
structural improvement over §49*: the signal is intrinsic, not an external
distillation label, and the connection-point is W-owned (not the emission
gate). It is §7-legitimate by construction (B-S59-1/2 close this).

## §3 The honest crux (g3 — confronted directly, NOT hidden)

The W-native reframe changes the **objective semantics** (intrinsic
curiosity vs distillation label). It does NOT, by itself, change the
**data**. If the underlying W-state sequence is itself
corpus-majority-dominated (the §27/§48 trace is ~95% one regime), then a
self-predictive forward-model can STILL learn "predict the prior mean" and
its error collapses to a near-constant — only now relabelled "curiosity"
instead of "distillation". The §49 collapse may be *data-shape-bound*, not
*home-bound*.

**The precise open question**: does W-native (error-as-curiosity) make the
forward-model's error a NON-DEGENERATE function of state-surprise (varies
as the W-state varies), or does it collapse to the prior-mean residual
REGARDLESS of home?

## §4 The $0 smoke (structural-validation, capability claim 0)

`w_native_ptd.py`: a tiny linear-affine forward-model `g_θ : W_t → Ŵ_{t+1}`,
trained ONLINE to predict its OWN next W-state; error = mean-squared
residual ≥ 0 (= EFE epistemic value) → `W.curiosity`. Run over THREE
configurations:

- **R1 — diverse W-state, ON**: genuine W-dynamics, real step-to-step
  surprise.
- **R2 — majority W-state, ON**: ~95% near-constant low-activity regime
  (the §27/§48 corpus shape) + ~5% sparse excursions.
- **OFF — diverse, disabled**: W-native-PTD off ⇒ no forward-model, no
  curiosity coupling (the connection-point reduction).

Collapse-vs-signal is a decidable Boolean (mirror §49 divergence metric /
§24 B-PHASE-B-RUN nontrivial predicate): error-variance > τ=1e-4 ⇒
non-degenerate; ≤ τ ⇒ collapsed. For R2, collapse is judged on the **~95%
constant-data majority steps** (the honest §49-echo question), NOT on the
aggregate variance which is dominated by the rare ~5% excursion spikes (a
measurement artefact that would falsely read as "non-degenerate" — this
stratification is the structurally-correct test).

## §5 Smoke result (measured, g3 — decided by measurement)

| run | error_mean | error_variance | non-degenerate? |
|---|---|---|---|
| R1 diverse ON | 4.32e-2 | **4.43e-4** (> τ) | **True** |
| R2 majority ON (constant-data 284 steps) | 7.11e-4 | **1.15e-6** (≤ τ) | **False — COLLAPSED** |
| R2 majority ON (excursion 15 steps) | 1.36e-1 | — | surprise where genuine |
| OFF diverse disabled | **0.0** | **0.0** | False (reduction holds) |

- W-native error **IS a non-degenerate curiosity signal** when the W-state
  is genuinely diverse (R1 var 4.43e-4 ≫ τ).
- W-native error **STILL collapses** to the prior-mean residual on the
  ~95% constant-data majority steps (R2 1.15e-6 ≤ τ — the §27/§48 corpus
  shape, the §49 echo). The 15 excursion steps spike (mean 0.136): surprise
  exists where the data is genuinely surprising, but the 95% is a flat
  prior the self-predictor trivially learns.
- OFF error ≡ 0, variance ≡ 0: the connection-point reduction holds
  exactly (W-native-PTD disabled ⇒ W-module byte-equal baseline).

## §6 The honest crux verdict

**`W-NATIVE-IS-STRUCTURALLY-DISTINCT-BUT-COLLAPSE-IS-DATA-SHAPE-BOUND`**

Making PTD-aux W-native is a real §7-legitimate **structural improvement**
over §49's bolt-on: the objective is intrinsic curiosity
(self-prediction surprise = EFE epistemic value), not an external
distillation label; the connection-point is W-owned, not the emission gate
(B-S59-1/2 close this formally). **But it does NOT, by itself, escape the
§49 collapse on majority-dominated input.** The §49 collapse is
**DATA-SHAPE-bound, NOT home-bound**: a self-predictive forward-model on a
~95%-constant W-state learns "predict the prior mean" and its error
collapses to a near-constant residual, exactly as the distillation head
did — only now the constant is relabelled "low curiosity". The W-native
reframe changes the objective semantics; it does not change the data.

This is the honest expected result, stated up front in `w_native_ptd.py`'s
docstring before measuring (g3, mirror §49 FINDINGS §3/§8). The reframe is
*not* a relabelling-only failure (R1 shows genuine non-degenerate signal
when the data IS diverse — that is a true structural property absent from
§49's bolt-on, which collapsed even on diverse §24 sensors). It is a
*partial* structural advance whose collapse-escape is honestly an open
future-fire question.

## §7 B-S59 battery (4/4 🔵 sidecar — central UNCHANGED)

`blue_falsifier_s59.py`, central `state/verify_hexad_blue_2026_05_15/
blue_falsifier.py` UNCHANGED (0-line diff verified; B-PRIME / B-DIRI /
B-S16 / B-DHDL / B-S48 / B-S49 sidecar precedent):

- **B-S59-1 W-OWNED-NOT-BOLT-ON-CLOSED** (연결부위): AST-level — the
  forward-model error feeds `w_curiosity_coupled` (a CALL), NOT
  `talker_should_emit`/`decision_label`/`LABEL_EMIT_VOICE` (absent as
  calls; docstring mentions are explanatory, not coupling edges). 4-corner
  Boolean over (feeds_curiosity, feeds_emission_gate): only (True, False)
  is the §59 W-native configuration. **PASS**.
- **B-S59-2 ERROR-IS-EFE-EPISTEMIC-CLOSED**: MSE = (r0²+r1²)/2 is an
  explicit non-negative sum of squares (sympy residual substitution; min
  exactly 0 at ŷ≡y; 3 witnesses ≥ 0). §7-legitimate intrinsic (target =
  next ACTUAL W-state, NO external label — carries the §58 signature).
  **PASS**.
- **B-S59-3 CURIOSITY-NONDEGENERACY-PREDICATE-CLOSED**: the collapse-vs-
  signal test is a decidable Boolean (sympy interval partition of ℝ≥0 at τ
  — total + disjoint); AST-level determinism (no `random`/`secrets`
  import, no `np.random`/`torch.rand` call — the line-100 comment text "NO
  np.random" is documentation, not a false-positive); 3× bit-identical
  re-run. Mirror §49 divergence / §24 nontrivial. **PASS**.
- **B-S59-4 OFF-REDUCTION-CLOSED** (연결부위): `step()` short-circuits
  `if not self.enabled: return 0.0` BEFORE any predict()/SGD (AST source
  span; short-circuit index precedes the SGD-update index); numeric: OFF
  run error_mean==0 ∧ error_variance==0. W-native-PTD disabled ⇒ W-module
  byte-equal baseline. Mirror B-DHDL-5 / B-EBT-5 / B-S16-5 / B-S49-3.
  **PASS**.

**B-S59-NOTE** (empirical carve-out, NOT counted 🔵): whether W-native
ACTUALLY escapes §49 collapse AT SCALE on real anima W-state (vs this stub
sequence) is a future-fire OUTCOME (SGD + real-state-dependent). The
battery proves the structural reframe is §7-legitimate + OFF reduction +
predicate decidable — it does NOT prove escape-from-collapse.
B-D-NOTE / B-DHDL-NOTE / B-S48-NOTE / B-S49-NOTE family.

## §8 GOAL distance + verdict

§15 milestone unchanged. north-star (GOAL.md "anima 가 자기 physics 로부터
자발적으로 말 거는 emergence") **NOT reached**. §59 = a §7-legitimate
**structural reframe** (error-as-curiosity vs §49's bolt-on — a real
improvement: intrinsic W-physics signal, W-owned connection-point) + a $0
structural-validation smoke. The smoke MEASURED that the reframe produces a
non-degenerate curiosity signal on diverse W-state but **still collapses**
on majority-dominated W-state — so the §49 collapse is data-shape-bound,
not home-bound. Whether W-native escapes collapse at scale on real anima
W-state is an honest open future-fire question (B-S59-NOTE). Capability
claim 0. over-claim 0. f1/f2/f3 + B-IDENTITY-5 safe.

## Honest C3

1. **Structural reframe, NOT GOAL** — §59 changes the objective semantics
   (intrinsic curiosity vs distillation label); it is NOT a GOAL-fire, NOT
   a scale-fire, NOT capability emergence. Stated before measuring (g3).
2. **The W-native improvement is real but partial** — R1 shows genuine
   non-degenerate signal on diverse W-state, a true structural property
   §49's bolt-on lacked (it collapsed even on diverse §24 sensors). But R2
   collapse shows the improvement does not, by itself, escape majority-
   collapse. Partial advance, honestly bounded.
3. **The §49 collapse is DATA-SHAPE-bound, not home-bound** — the central
   finding. A self-predictive forward-model on ~95%-constant W-state
   learns the prior mean; error collapses regardless of whether the home
   is the emission gate (§49) or W.curiosity (§59).
4. **Stub W-state, NOT real anima ckpt state** — `_gen_w_sequence` is a
   deterministic scripted stub (the §27/§48 precedent). It tests the
   STRUCTURE, not anima's actual W-trajectory. Escape-at-scale is
   B-S59-NOTE empirical.
5. **Stratified collapse measure is the honest test** — judging R2 collapse
   on the ~95% constant-data steps (not aggregate variance dominated by
   rare excursion spikes) is structurally correct; the un-stratified
   variance would falsely read "non-degenerate" (a measurement artefact I
   confronted and fixed mid-cycle).
6. **OFF reduction is exact** — disabled ⇒ error ≡ 0, no curiosity
   coupling, W-module byte-equal (B-S59-4). Fair-compare by construction.
7. **§7-legitimate by construction** — target = next ACTUAL W-state (self-
   prediction), NO external label; W-state = anima's OWN W-physics
   (`HEXAD/W/w_lib.hexa` SSOT mirror). §7①② no generic-LM/no-graft (no
   model.forward, no external classifier/RAG/LLM); §7③ anima-physics-as-
   source. B-S59-1/2 close this formally.
8. **Error-as-curiosity = EFE epistemic value** — MSE ≥ 0 is Active-
   Inference epistemic value / surprise about the future self-state
   (`anima_persona` W ontology, arxiv 2508.05619 compatible). Not a
   numerology fit — a Shannon-class non-negative information measure
   (B-S59-2). f1/f2/f3 safe (no σ/τ/φ/J₂ external derivation).
9. **Deterministic, no RNG** — LCG only (§48/§27 precedent); 3×
   bit-identical (B-S59-3). The smoke is reproducible.
10. **central blue_falsifier.py UNCHANGED** — 0-line diff verified;
    sidecar-only per B-PRIME/B-DIRI/B-S16/B-DHDL/B-S48/B-S49 precedent.
11. **κ=2.0 coupling is a design choice, not tuned** — fixed before the
    smoke; the collapse verdict does not depend on κ (curiosity-variance
    tracks error-variance; collapse is in the error itself, not the
    coupling gain).
12. **north-star unchanged; §15 milestone unchanged** — §59 maps the
    structure of one §58 hand-off (W-native home), reports it is
    §7-legitimate but data-shape-collapse-bound, and HONESTLY defers the
    escape-at-scale question to a future fire. Valuable structural
    datapoint + mechanism-honest reframe, NOT a GOAL-distance movement.
