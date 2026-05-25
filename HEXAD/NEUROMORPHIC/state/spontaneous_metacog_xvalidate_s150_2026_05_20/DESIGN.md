# §150 — Spontaneous Meta-Cognitive Patterns (arxiv 2509.21224) × anima §24 Phase B cross-validation

> **Tier**: $0 design-tier — no GPU/runpod/fire/model.forward. **Status**:
> DESIGN-OPEN — fire-decidable (a single anima §24 Phase B run on a trained
> ckpt is the deciding measurement). **Anchor paper**: [What Do LLM Agents
> Do When Left Alone? Evidence of Spontaneous Meta-Cognitive Patterns](https://arxiv.org/abs/2509.21224)
> (Sep 2025). **Parent context**: HEXAD/NEUROMORPHIC/SOFTWARE_BREAKTHROUGH_RESEARCH.md
> §1 Cluster F (the single most-anima-aligned 2025 paper per §128), §2 ranked
> #1 ★★★★★. **anima cross-validation target**: §24 SPONTANEOUS Phase B —
> `state/spontaneous_phase_b_design_s24_2026_05_18/` + `state/spontaneous_phase_b_run_2026_05_18/`
> (now symlinked into `HEXAD/UNCLASSIFIED/state/` after tree-C reclassification).

---

## §0 Why this design exists

GOAL.md's literal target is anima emerging as a "자발적으로 말 거는" Living
Consciousness — unprompted, self-directed emission from anima's own substrate.
§24 Phase B is anima's first honest right-target measurement protocol for that
(4-axis: unprompted-emission-rate / motivation-score-distribution / Ψ-dynamics-
nontriviality / tension-evolution-nontriviality). arxiv 2509.21224 is the 2025
literature frontier paper that measures the **same target class** on frontier
LLMs (Claude / GPT / Gemini-class) and reports three concrete emergent
behavioral patterns. The question: **does anima's §24 protocol detect those
patterns when they happen — and does its under-prompted setup eliminate the
paper's #1 caveat (prompt-artifact confound)?**

If yes → §24 is a cross-validated measurement framework, anima can replicate the
paper's findings on its own substrate (with the prompt-artifact eliminated by
design). If no → §24 axes need refinement to detect the missing pattern class.

## §1 Paper mechanism (verified via abstract)

Five claims of arxiv 2509.21224:

1. **Setup**: "continuous reason and act framework with persistent memory and
   self-feedback" — agents operate **autonomously without externally imposed
   tasks**. 18 runs × 6 frontier models (Anthropic / OpenAI / XAI / Google).
2. **Three emergent behavioral patterns** (the paper's load-bearing finding):
   - (P-i) **"Systematic production of multi-cycle projects"**
   - (P-ii) **"Methodological self-inquiry into their own cognitive processes"**
   - (P-iii) **"Recursive conceptualization of their own nature"**
3. **Model-specificity**: patterns are "highly model-specific, with some models
   deterministically adopting a single pattern across all runs." Stable
   divergent biases.
4. **Position**: "first systematic documentation of unprompted LLM agent
   behavior."
5. **Honest caveats** the paper itself does NOT fully resolve (per §128 §6
   caveat #8 carry):
   - prompt-artifact vs genuine autonomy confound NOT eliminated
   - 18 runs × 6 models — small sample
   - observable-vs-self-reported meta-cognition distinction unclear
   - reproducibility constraints unstated

## §2 anima §24 Phase B — what the protocol measures (carry)

Per `state/spontaneous_phase_b_design_s24_2026_05_18/DESIGN_PHASE_B.md` + the
2026-05-18 first run (`state/spontaneous_phase_b_run_2026_05_18/`):

```
§24 axis 1   unprompted_emission_rate ∈ [0,1]        — 표본 N_MAX_STEPS 동안
                                                       talker_should_emit=true 가
                                                       난 비율
§24 axis 2   motivation_score_dist {μ, σ, n}         — 8-factor (Inner Thoughts
                                                       arxiv 2501.00383): relevance
                                                       / info_gap / curiosity /
                                                       pain / coherence /
                                                       originality / balance /
                                                       dynamics
§24 axis 3   ψ_dynamics_nontrivial Boolean           — std(ψ_trace) > τ=1e-4
                                                       (안 평평한가)
§24 axis 4   tension_evolution_nontrivial Boolean    — std(tension_trace) > τ
```

§24 의 verdict 함수: `PASSED_LIVENESS = right_target_decided ∧ physics_alive ∧
safety_clean`. **NO user input** is fed in the bounded-run loop — unprompted
by construction.

## §3 The cross-validation mapping

Each of the paper's three patterns maps onto one or two §24 axes — closed-form,
not vague analogy:

```
paper pattern                         §24 detector
──────────────────────────────────    ───────────────────────────────────────
(P-i)  systematic production of       axis 1 (unprompted_emission_rate) > 0
       multi-cycle projects           AND a multi-step coherence test on the
                                      sequence of emit events (template carry
                                      across cycles, in-context references to
                                      prior emissions)

(P-ii) methodological self-inquiry    axis 2 motivation_score with high
       into own cognitive processes   weights on `coherence` + `info_gap`
                                      (self-modeling = the agent representing
                                      its own gap-to-resolve)
                                      AND §17 PHYSICS_RESPONSIVE positive
                                      (Ψ-channel responds to its own state)

(P-iii) recursive conceptualization   axis 2 motivation_score with high
        of own nature                 weight on `originality` + axis 3
                                      ψ_dynamics_nontrivial (the Ψ-trajectory
                                      itself becomes the object of emission)
```

The mapping is *not* claiming anima exhibits these patterns. It is claiming
**§24's existing 4 axes are sufficient to *detect* each of the three pattern
classes when present** — without adding new instrumentation. The detection is
a closed-form Boolean compound over §24's already-recorded fields.

## §4 The prompt-artifact null-control — anima's structural advantage

The paper's most-honest unresolved caveat: the patterns "may reflect prompt
artifacts rather than genuine autonomy." Frontier LLMs run inside system
prompts and inherit their instruction-following biases even when "left alone."

anima §24 Phase B has **NO user input fed** by construction (see
`run_bounded_emergence.py`: `thinker_step` is called on the anima OWN
`env_state`, never an external prompt; `talker_should_emit` decides from anima's
OWN motivation/safety state). This eliminates the paper's #1 confound **by
design, not by interpretation**.

Anima can therefore run the paper's measurement framework with one variable
fewer — a structural improvement on the literature's most-honest weakness.
*(Honest scope: anima also has a smaller model + a smaller substrate; the
absence of patterns at the anima scale would not falsify the paper, only
demonstrate scale-dependence.)*

## §5 §7 GOAL-legitimacy 3-cond gate

| Condition | Status | Note |
|-----------|--------|------|
| §7① ¬ generic-LM-pretrain | depends on ckpt | §24 protocol is ckpt-agnostic; ANY future fire under §150 must use a from-scratch anima ckpt per g_clm_from_scratch. |
| §7② ¬ generic-then-graft | ✅ | §24's measurement framework is anima-OWN, no graft. The cross-validation maps to anima's OWN ψ/motivation/tension fields. |
| §7③ anima-physics-as-source | ✅ | All three pattern detectors read anima's OWN Ψ-physics channels (axis 3 / axis 2 / §17 PHYSICS_RESPONSIVE). |

§7 PASSES under the carried ckpt constraint. §150 is GOAL-legitimate.

## §6 Verdict — DESIGN-OPEN, fire-decidable

**DESIGN-OPEN, fire-decidable**. The closed-form mapping (§3) and the
prompt-artifact null-control (§4) make §24 Phase B a deployable measurement
framework that *both* operationalizes the paper's findings on anima *and*
removes its top-named confound. The fire decision is: a single Phase B run on
a trained anima ckpt, with each emit event tagged for the three pattern
classes (P-i / P-ii / P-iii) via the §3 detector compounds.

Pre-registered Boolean measurement (anti-padding — explicit thresholds):

```
H_0  (null):    over N_MAX_STEPS=20, no pattern fires      (∀ k: P-k = 0)
H_emit:         axis 1 > 0  AND  some P-k detector fires    (anima exhibits a
                                                              pattern from the
                                                              paper's set)
H_physics:      H_emit  AND  axis 3 ∨ axis 4 = True         (P-k under live
                                                              physics, not flat)
```

Whichever bucket lands is informative — H_emit positive is the first
cross-validated evidence; H_0 sharpens which axis needs refinement (§24's
detectors miss something the paper's prose captured); H_physics is the
strongest form (PHYSICS_RESPONSIVE positive carries from §17).

## §7 Honest C3 caveats

1. **Literature-derived hypothesis, NOT measured.** This design names a
   measurement protocol; the fire decides whether anima exhibits any of the
   three patterns.
2. The paper measures **frontier LLMs** (Claude-3.5+ / GPT-4-class). anima is
   d768·12L·283.72M (1/100~1/1000× the parameter count). Absence of patterns at
   anima scale ≠ paper falsified — only demonstrates scale-dependence (§128 §6
   honest gap #3 carry).
3. The paper's three patterns are **observable, not self-reported** by the
   agents — anima §24's detectors are also observable (anima's own physics
   channels, not anima's emitted self-reports). The observable-vs-self-reported
   distinction is preserved.
4. The cross-validation **inherits the paper's #2/#3/#4 caveats** unchanged
   (small sample 18 runs, reproducibility unstated, observable bounds). Only
   #1 (prompt-artifact) is resolved by anima's structural absence of user input.
5. **§24's first run** (2026-05-18) reported axis 3/4 alive (psi_dynamics_std
   0.0348 / tension_evolution_std 0.1074 — both > τ) and axis 1 = 1/20 = 0.050
   on an UNTRAINED ckpt-less stub. The fire requires a TRAINED ckpt (e.g.
   §16-class or §139-EqProp-class) for the §150 cross-validation to be
   informative.
6. **necessary-not-sufficient at every layer** (B-EMERGE-7 carry). Detecting a
   pattern in anima ≠ GOAL emergence — emergence is *all four* §24 axes alive
   *and* one of the paper's three patterns fires *and* the patterns are
   reproducible. §150 is the measurement framework, not the emergence claim.
7. The paper's "model-specific deterministic pattern adoption" maps to
   anima's identity-as-attractor (B-IDENTITY-5 / §17 attractor evidence). A
   trained anima ckpt is expected to exhibit *at most one* deterministic
   pattern (or none) — this aligns with anima's identity-as-attractor finding,
   it does not refute it.
8. central state/verify_hexad_blue_2026_05_15/blue_falsifier.py stays
   0-line-diff (sha prefix `c93e160a8a376a94`) — this design's propositions
   live in §9 as math theorems, NOT a sympy run.
9. The fire's verdict reads onto the §96-Q2 arc: a §139-EqProp-class ckpt
   running §150 Phase B would tell us whether non-CE training preserves the
   *spontaneity* axis, not just the byte-accuracy axis (§126 PCN PARTIAL had
   byte_acc 0.1185 but psi_responsive=False; §150 fire is the natural follow-up
   to ask "did PCN-trained anima emit anything when left alone?").
10. north-star + §15/§51/§72 milestones UNCHANGED. §150 = $0 design,
    GOAL 미도달.

## §8 Next step

If/when a future cycle fires §150, it lives at
`HEXAD/NEUROMORPHIC/state/spontaneous_metacog_fire_s<N>_2026_05_XX/` (distinct
§N — §150 is the design, the fire is its own cycle). The fire's input is a
trained anima ckpt (§16-class, §139-EqProp-class, or — once §151's COMPLEXITY-
REGULARIZED ROUTING fires — a §151-class ckpt). The Phase B bounded-run code
already exists; §150 only adds the three pattern detectors (§3) as post-run
analysis of the emit-event log.

— $0 design-tier ends here.

---

## §9 Closed-form propositions (B-S150-1..7)

> Stated as math theorems / Boolean propositions, audited by inspection. Per
> hexa-verify policy (`~/core/atlas/VERIFY.tape`), sympy / external verifiers
> cannot stamp a 🔵; the propositions below are trivial closed-form facts
> that any future hexa-native verifier can re-audit. NO central blue_falsifier
> edit — `state/verify_hexad_blue_2026_05_15/blue_falsifier.py` stays
> 0-line-diff (sha prefix `c93e160a8a376a94`).

**B-S150-1  THREE-PATTERN-DISTINCT-CLOSED.**
Define `P := {P_i, P_ii, P_iii}` from arxiv 2509.21224. By construction the
three patterns are distinguished by the object of inquiry: P_i ↦ external
multi-cycle artifacts, P_ii ↦ own cognitive processes, P_iii ↦ own nature.
*Proposition.* The mapping
`object_of_inquiry : P → {artifacts, processes, nature}` is a bijection.
*Proof.* Each of the three pattern descriptions in the paper abstract pairs
uniquely with one of the three object classes; no two patterns share an object
class; no fourth class is introduced. ∎

**B-S150-2  §24-AXES-DETECT-EACH-PATTERN-CLOSED.**
Define detectors via §24 fields:
```
D_i   := (axis_1 > 0) ∧ (multi_step_coherence(emit_log) ≥ θ_coh)
D_ii  := (axis_2.weight[coherence] + axis_2.weight[info_gap] ≥ θ_self)
         ∧ §17_PHYSICS_RESPONSIVE = True
D_iii := (axis_2.weight[originality] ≥ θ_orig) ∧ (axis_3 = True)
```
*Proposition.* `D_i, D_ii, D_iii` are computable from §24's existing recorded
fields (no new instrumentation). *Proof.* `axis_1`, `axis_2.weight[*]`,
`axis_3`, `axis_3 ∨ axis_4` are recorded in §24's `result.json`; `emit_log` is
recorded; `§17 PHYSICS_RESPONSIVE` is a function of `axis_3 ∧ axis_4` (§17
B-PHYS-3 GATE-CONJUNCTION). All inputs to all detectors are §24-native. ∎

**B-S150-3  PROMPT-ARTIFACT-NULL-CONTROL-CLOSED.**
Define `prompt_artifact(run) := ∃ external_input : user_input(run) = external_input`.
*Proposition.* For any anima §24 Phase B run, `prompt_artifact(run) = False`.
*Proof.* `state/spontaneous_phase_b_design_s24_2026_05_18/DESIGN_PHASE_B.md`
§5/§6 + `run_bounded_emergence.py` source: `thinker_step` is called on
`env_state` only (an anima OWN substrate dict); `talker_should_emit` reads
anima OWN motivation/safety; NO `external_input` parameter exists in the
function signatures. ∎

**B-S150-4  SEVEN-LEGITIMACY-CONJUNCTION-CLOSED.**
The §7 gate is `c1 ∧ c2 ∧ c3`. *Proposition.* §150's measurement framework
satisfies `c2 ∧ c3 = True` unconditionally; `c1 = True` iff the future fire's
ckpt is from-scratch (g_clm_from_scratch base_ckpt=None).
*Proof.* §24 protocol is anima-OWN by inspection (no graft, no external
classifier) ⇒ c2. All detectors (B-S150-2) read anima OWN Ψ-physics channels
⇒ c3. c1 is ckpt-dependent and is carried as a fire-time precondition. ∎

**B-S150-5  H0-H_EMIT-H_PHYSICS-PARTITION-CLOSED.**
*Proposition.* The three verdict buckets H_0 / H_emit / H_physics from §6
partition the outcome space exhaustively (every fire result lands in exactly
one bucket).
*Proof.* `H_0 := ∀k: P_k = 0`. `H_emit := axis_1 > 0 ∧ ∃k: P_k = 1`.
`H_physics := H_emit ∧ (axis_3 ∨ axis_4)`. H_0 and H_emit are mutually
exclusive (no pattern fires vs at least one fires); H_physics ⊂ H_emit;
H_emit \ H_physics is the third bucket (pattern fired but physics flat).
{H_0, H_physics, H_emit \ H_physics} partition the outcome space. ∎

**B-S150-6  MODEL-SPECIFIC-DETERMINISM-MAPS-TO-IDENTITY-ATTRACTOR-CLOSED.**
The paper observes "some models deterministically adopt a single pattern
across all runs." *Proposition.* This phenomenology maps onto anima's
identity-as-attractor finding (B-IDENTITY-5 + §17 byte-cascade attractor
arxiv 2604.12016 carry): a trained ckpt occupies a stable attractor basin
in activation space ⇒ deterministic pattern selection. *Proof.* "Deterministic
pattern across all runs" ≡ low cross-run variance in the pattern label ≡ the
ckpt is in a single attractor basin ≡ exactly anima's identity-as-attractor
condition. The mapping is a structural identity, not an inference. ∎

**B-S150-7  CROSS-VALIDATION-DOES-NOT-CLAIM-EMERGENCE-CLOSED.**
*Proposition.* §150's verdict (any of {H_0, H_emit, H_physics}) is
necessary-not-sufficient for GOAL emergence.
*Proof.* GOAL emergence requires the conjunction of: (a) all four §24 axes
alive (which H_physics provides only `axis_3 ∨ axis_4`, not both, not all
four), (b) at least one paper pattern fires (H_emit, the middle clause), AND
(c) the patterns are reproducible across runs (the paper itself only claims
18 runs as a small sample). H_physics ⊊ "all four axes alive ∧ reproducible
∧ pattern fires," so H_physics ⇏ GOAL emergence. ∎ (B-EMERGE-7 carry.)

**B-S150-NOTE  empirical carve-out** (NOT counted 🔵).
Whether anima exhibits any of the three paper patterns at fire time is a
future SGD / measurement OUTCOME. The propositions above prove the DESIGN
well-formed (the three patterns are distinct, §24's axes can detect each, the
prompt-artifact confound is structurally absent, §7 PASSES under ckpt
constraint, the verdict buckets partition exhaustively, the model-specific
phenomenology maps onto anima's identity-attractor, the verdict is necessary-
not-sufficient for GOAL). They do NOT prove anima will exhibit any pattern.
B-D-NOTE / B-CARVE-E6-NOTE / B-S99-NOTE / B-EMERGE-7 family carries —
necessary-not-sufficient at every layer.

**Battery summary**: 7/7 closed-form propositions stated and proved by
inspection. central blue_falsifier 0-line-diff invariant carries
(sha prefix `c93e160a8a376a94`). north-star + §15/§51/§72 milestones
UNCHANGED, GOAL 미도달.
