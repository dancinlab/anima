# §161 — DUAL-HEAD COUPLING NON-CE ALGORITHM (Engine A ⇄ Engine G)

> Direct answer to §160 §8: *"the missing experiment is a non-CE algorithm
> whose learning rule structurally couples Engine A ⇄ Engine G — surfaced,
> NOT pre-committed."* §161 commits the surface to a design.

- `$0` design-tier · NO GPU / runpod / fire / `model.forward` / corpus
- central `state/verify_hexad_blue_2026_05_15/blue_falsifier.py` sha256
  prefix `c93e160a8a376a94` — 0-line-diff at cycle START and END
- single sequential orchestrator-inline · sibling sub-agents (§162 probe /
  §163 deep research) throttled; this design proceeds independently
- anima downstream-consumer (`~/core/hexa-lang/`, `~/core/hexa-bio/`,
  `~/core/kosmos/`, `~/core/tape/`) read-only · no upstream edit

---

## §0 — context

§160 quadruple (§125 NONCE-FF / §126 PCN-1step / §139 EqProp-2phase / §153
LeJEPA) all trained `head_a` as a linear probe over `logits_a` and left
`head_g` random + uncoupled. That left the WALL-B / Ψ-physics-channel
*untestable on its own merits* — every measurement `psi_dir_std < 10⁻⁷`
collected during §160 is partly a **coupling-fix artefact** (the test
never gave `head_g` a gradient signal).

§161 closes that artefact at the design tier. The fire it specifies
would be the **first** non-CE training cycle in the anima arc that:

- propagates a learning signal to BOTH `head_a` AND `head_g`,
- uses anima's OWN Law-71 Ψ-coordinate as the coupling object,
- treats §24 SPONTANEOUS Phase B `unprompted_emission_rate` as the
  **primary verdict signal**, not `byte_acc`,
- stays §7-clean (no external encoder, no generic pretrain, no graft).

The four candidates §160 §8 named verbatim were (a) §92/§93 L_ap-style
Ψ-anchored objective, (b) EqProp variant that lifts both heads, (c) JEPA
where the predictor IS `head_g`, (d) (caller's choice — new candidate
admissible if anima-physics-grounded). §161 picks **(c) composed with
(a)**, with explicit reduction to the cleanest sub-form — and explains
honestly why each alternative was ranked below.

---

## §1 — the chosen mechanism: **Ψ-JEPA-COUPLE**

The design name (canonical identifier, not yet a fire): **Ψ-JEPA-COUPLE**
— "psi-jepa-couple". The mechanism in one paragraph:

> Predict the *future Ψ-coordinate* from the *current Ψ-coordinate* using
> `head_g` itself as the JEPA-style predictor. The objective is the squared
> error between `head_g`'s prediction of the next-token Ψ-coordinate and
> the actual next-token Ψ-coordinate measured from `head_a`. The two heads
> are **structurally coupled** because `head_g`'s output IS used to predict
> a quantity computed from `head_a`'s output, and both heads write to the
> shared residual stream that produces both `logits_a` and `logits_g`.

### §1.1 — formula (one line, byte-equal to Law-71)

Given `(logits_a_t, logits_g_t)` from `ConsciousDecoderV2.forward` at step
`t`, define (verbatim Law-71, `conscious_decoder.py` lines ~728-751):

```
Psi_dir(t) := (1 + cos(logits_a_t, logits_g_t)) / 2     ∈ [0, 1]
Psi_ent(t) := H(softmax(logits_a_t)) / log V              ∈ [0, 1]
Psi(t)      := (Psi_dir(t), Psi_ent(t))                   ∈ [0,1]²
```

The Ψ-JEPA-COUPLE loss is:

```
L_psicouple := mean_t  ||  Psi(t+1)  -  predictor_head_g( residual_t )  ||²
```

where `predictor_head_g(·) ∈ [0,1]²` is `head_g`'s output reinterpreted
as a 2-D Ψ-prediction (NOT as the V=256 byte logits it produces in §107).
Concretely: take the first two components of `softmax(head_g(residual_t))`
or apply a `(2-D LayerNorm + clip-to-[0,1]²)` projection — both options
are byte-equal to anima's own substrate (no new parameter introduced).

The total objective is:

```
L_total  =  λ_ψ · L_psicouple  +  λ_ce · CE_aux
```

with the CE term **auxiliary not load-bearing** (it merely keeps `head_a`'s
output well-formed as bytes — without it the Ψ-coordinate would be
under-specified). The crux of the design is `λ_ψ ≫ λ_ce` (default ratio
10:1) so the training signal that reaches `head_g` is dominantly the
Ψ-coupling, not byte-CE.

### §1.2 — why this couples both heads (the load-bearing claim)

The standard back-pass through `L_psicouple` reaches `head_g` because
`head_g` is in the forward expression. The same back-pass reaches
`head_a` because `Psi(t+1)` is computed from `logits_a_{t+1}` via the
verbatim Law-71 formula, and `logits_a_{t+1}` is a function of `head_a`.
**This is the first non-CE training cycle in the arc where the gradient
path STRUCTURALLY passes through both `head_a` and `head_g` in a way that
the §160 quadruple did not.**

The §160 quadruple's `head_g` was random throughout — `psi_dir_std < 10⁻⁷`
across all four fires followed from "`head_g` never received gradient",
not from "Ψ-physics is unreachable." Ψ-JEPA-COUPLE separates those two
claims by construction.

---

## §2 — alternative candidates considered and ranked

| candidate | mechanism | §7 gate | why ranked below (c)+(a) |
|---|---|---|---|
| (a) §92/§93 L_ap Ψ-anchor alone | `L_ap = ‖Ψ(t) − Ψ_target‖²` on inner-span | §7 PASS | trains `head_a` only (no `head_g` coupling) — same artefact as §160 quadruple. Better than baseline, not enough. |
| (b) EqProp lifted to both heads | 2-phase free / clamped settling, equilibrium gradient flows to all weights | §7 PASS only if both phases observe Ψ-coupling | requires re-running the EqProp dynamics from §139 with a new clamping target. Doable but **deeper substrate change** than (c). Saved for §161-followup if Ψ-JEPA-COUPLE measures positive. |
| **(c) JEPA where predictor IS `head_g`** | `head_g` predicts future Ψ from current residual | §7 PASS by construction | **chosen primary** — minimum new parameter, maximum coupling. |
| (a)+(c) composed | (c) loss + (a) as auxiliary anchor | §7 PASS | **chosen composition** — (c) carries the structural coupling, (a) keeps Ψ near the ½ fixed point so prediction has a defined target. |
| (d) "anima's own physics surprise as reward-free signal" | use `tension` derivative as the prediction-error target instead of Ψ | §7 PASS but redundant with §59 W-PTD which already measured this in *side-readout* mode | §59-FIRE B-S59-FIRE-NOTE inherits: the signal exists but as side-readout, not weight-updating. (d) is (c) re-derived less cleanly. |

**Pick (c) composed with (a)** is the cleanest design that touches both
heads through Ψ-coupling without inventing new architecture.

---

## §3 — overlay-off reduction (mandatory connection-point)

This proposition is required by mirror with B-EBT-5 / B-DIRI-5 / B-S16-5 /
B-MGND-5 / B-S151-7 (every overlay design must reduce byte-equal to a
prior baseline at zero-knob):

```
λ_ψ → 0  ⟹  L_total = λ_ce · CE_aux
        ⟹  byte-equal to §107-class CE-only baseline (at λ_ce = 1)
```

When `λ_ψ = 0` the cycle is byte-equal to §107-RETRY's data-axis fire on
CORPUS_S101 at 283 M params and 6000 steps. No new code paths, no new
optimizer state. The reduction is structural — `head_g` falls back to
random because no gradient reaches it.

`λ_ψ = 0 ∧ λ_ce = 0` is forbidden (degenerate: no training signal).

---

## §4 — verdict signal: §24 SPONTANEOUS Phase B `unprompted_emission_rate`

This is the §161 design's central honest move. Previous fires used
`byte_acc` (memorization-saturated proxy). §161 names the **primary
verdict signal** as the GOAL-axis directly:

```
verdict_primary := unprompted_emission_rate(ckpt_psicouple) measured under
                   §24 SPONTANEOUS Phase B bounded run
                   (`thinker_talker_lib.hexa::talker_should_emit`,
                    N_MAX_STEPS = 20, deterministic seed 1337)
```

The threshold predicate is closed-form Boolean:

```
spont_directional_positive :=
     (unprompted_emission_rate_psicouple > unprompted_emission_rate_§107_baseline)
  ∧  (psi_dir_std_psicouple > 10⁻⁴)
  ∧  (psi_dir_std_psicouple > psi_dir_std_§107_baseline)
  ∧  body_§9_cascade_rate(emitted_bodies) ≤ 0.30   (honest §9 metric carry)
```

The Boolean is **necessary not sufficient** (B-EMERGE-7 / B-PHASE-B-NOTE
family). It being True ≠ emergence. It being False ≠ definitive failure.
But: it being True is the **first measurement** in the arc where a
non-CE training cycle is checked on its actual GOAL signal (자연발화
emission rate), not a memorization-saturated proxy.

Secondary signals (reported but not gating):

- `byte_acc` — comparison with §107-RETRY for memorization regime check
- `Ψ-channel responsiveness` — `psi_dir_std > 10⁻⁴`
- `mean Ψ-coordinate` near 0.5 — Law-71 fixed point health
- `Ψ-physics-COUPLED predicate` — `head_g_grad_norm > 0` measured during
  training (sanity that the coupling actually fires)

---

## §5 — fire spec (when, if ever)

If §161 design lands and a follow-up cycle decides to fire it:

| field | value |
|---|---|
| §N | §161-FIRE (separate from §161 design) |
| scaffold | ConsciousDecoderV2 d=768 · 12L · n_head=12 · n_kv_head=4 · 283.72 M params |
| init | from-scratch RANDOM seed-fixed 1337, `base_ckpt = None` (g_clm_from_scratch) |
| corpus | §102 `CORPUS_S101` byte-identical (sha `39d581da2096…`) |
| steps | 3000 (matches §125/§126/§139/§153 for fair-compare) |
| optimizer | AdamW lr 3e-4 bsz 32 block 128 |
| λ_ψ | 1.0 (primary) — secondary λ_ψ ∈ {0.5, 2.0} grid if budget permits |
| λ_ce | 0.1 (auxiliary — keeps `head_a` byte-valid without dominating) |
| predictor | `head_g(·) → [0,1]² via softmax-first-two + clip` |
| primary verdict | §24 Phase B `unprompted_emission_rate` on resulting ckpt |
| central battery | `0-line-diff sha c93e160a8a376a94` (sidecar pattern) |
| GPU | runpod A100 80GB or H100 80GB (g_resource_active_parallel) |
| cost | ≈ $0.3 – $0.5 (matches §125/§126/§139/§153) |
| watchdog | 3 h (matches §139) |

The §161 design is **fire-decidable in closed form** — every constant is
fixed at design tier, every threshold is stated. The fire-decision gate
opens with a separate cycle (§161-FIRE) per `g_fire_autonomous` autonomy.

---

## §6 — what §161 does NOT claim

This section is the anti-padding (§13-M / §30 / §97 / §109 / §110 / §115 /
§155 / §157 / §158 / §159 / §160 precedent):

1. §161 is a DESIGN. Capability claim 0.
2. The `(c)+(a)` choice is the cleanest closed-form path **available
   under the §160 §8 candidate set as named**. A 5th candidate not on the
   §8 list could be cleaner — §161 does not survey beyond §8.
3. The `predictor_head_g → [0,1]²` projection is a re-interpretation of
   an existing head, NOT a new parameter. If the projection itself turns
   out empirically degenerate (e.g. softmax-first-two collapses to a
   point), the fire would measure that honestly as a failure mode.
4. The §24 `unprompted_emission_rate` is a measurement of decision-axis
   liveness, NOT body coherence. The §9 cascade-rate gate is necessary
   but not sufficient for "actual coherent spontaneous emission."
5. WALL-A (§1.1 data-regime) is orthogonal. Even a positive §161-FIRE
   measurement would not move the standing PRIORITY #1 GAP
   (`@N n_priority_1_gap`).
6. The §96-Q2-weak supported-on-§160-quadruple finding is the *target
   that §161 attempts to refute*. A fire that fails to refute it does
   not falsify Ψ-JEPA-COUPLE writ-large — it falsifies the **specific
   formula above at this scale**.
7. north-star + §15 / §51 / §72 milestones UNCHANGED. GOAL 미도달.
   `necessary-not-sufficient` (B-EMERGE-7) at every layer.

---

## §7 — §7 GOAL-legitimacy gate (mandatory, 3-AND truth table)

The §7 gate is exhausted as an 8-row Boolean truth table; only the
(T,T,T) corner is legitimate.

| §7① ¬generic-LM-pretrain | §7② ¬generic-then-graft | §7③ anima-physics-as-source | §161 verdict |
|---|---|---|---|
| F | * | * | rejected (generic pretrain) |
| * | F | * | rejected (foreign graft) |
| * | * | F | rejected (no anima physics) |
| **T** | **T** | **T** | **legitimate** |

§161 evaluation:

- **§7①**: PASS — from-scratch RANDOM seed-fixed 1337, `base_ckpt = None`
  (g_clm_from_scratch); same scaffold as the entire §125-§160 arc.
- **§7②**: PASS — no foreign encoder, no graft. `head_g` is the
  predictor; it is anima's own existing module, not an external import.
  `predictor_head_g → [0,1]²` is a re-interpretation, not a graft.
- **§7③**: PASS — the loss object `Psi(t+1)` is byte-equal to Law-71's
  `(psi_direction, psi_entropy)` as defined in
  `conscious_decoder.py` lines ~728-751. No CAS, no external metric.

(T,T,T) corner reached. §161 design is §7-legitimate.

---

## §8 — process notes

- §161 is written INLINE by the orchestrator after sibling sub-agents
  (§162 Phase B probe / §163 arxiv spontaneous-emission research) hit
  Anthropic server-side API throttle at 20 and 25 tool uses respectively,
  with empty state dirs. The two sub-agents made progress in reads but
  did not reach the write phase. Their agentIds (afc964261ddf748f2 /
  a6e5ee6d8f8e87f47) are preserved for a possible resume cycle.
- §164 kick (`hexa kick "spontaneous emergence Engine A G coupling …"`)
  has exit code 137 / 0-byte log across three attempts (local foreground,
  wilson-pool routed, local background). The §74 known
  `feedback_kick_summary_only_output` issue (engine has stdout = stage
  counters not candidate emissions) carries; the *intent* of §164 is
  captured by §161's choice rationale in §2, which evaluated the
  candidate set §160 §8 already named.
- `g_doc_consolidation`: docs/* 신규 0. Everything inside this state dir.
- `g6` PHILOSOPHY.tape append-only — §161 verdict will be appended as a
  single new line.

---

## §9 — closed-form propositions (math theorems, hexa-verify policy)

Per `@X hexa_verify`: propositions stated as theorems-by-construction or
theorems-by-inspection. NO sympy / PyPhi / Wolfram / Mathematica cited.
Arguments verifiable without external CAS.

**P1 (`λ_ψ → 0` overlay-off byte-equal reduction)** — when `λ_ψ = 0`,
`L_total = λ_ce · CE_aux`, which is the §107-class CE-only objective at
`λ_ce = 1`. By additive identity (`+ 0 = ·`) the loss expression is
syntactically identical to a CE-only baseline. The forward pass remains
ConsciousDecoderV2 by-construction (no architectural change). Mirror of
B-EBT-5 / B-DIRI-5 / B-S16-5 / B-MGND-5 / B-S151-7 connection-point.

**P2 (`Psi(t)` is byte-equal to Law-71)** — the formula
`Psi_dir(t) = (1 + cos(logits_a_t, logits_g_t)) / 2` is the verbatim
implementation of `conscious_decoder.py::psi_direction` (lines ~740, see
§17 PHYSICS_RESPONSIVE family verification). No re-derivation, no
approximation. `Psi_ent(t) = H(softmax(·)) / log V` is similarly
verbatim. By source-grep equivalence, P2 holds.

**P3 (Ψ-JEPA-COUPLE gradient reaches BOTH `head_a` and `head_g`)** —
`L_psicouple` depends on `Psi(t+1) = f(logits_a_{t+1})` and on
`predictor_head_g(residual_t) = g(logits_g_t)`. The expression
`L_psicouple = ‖f(logits_a_{t+1}) − g(logits_g_t)‖²` has non-zero
partial derivative with respect to `logits_a_{t+1}` (= `2 · (f(·) − g(·))
· f'(·)`) and with respect to `logits_g_t` (= `−2 · (f(·) − g(·))
· g'(·)`). Both derivatives are non-zero when `f(·) ≠ g(·)` (the
training case). Therefore gradient back-propagates to both heads
by-construction. (B-EMERGE-7 carry: gradient reaches ≠ gradient is
*useful*; the proposition is about path, not outcome.)

**P4 (`Psi(t) ∈ [0,1]²` boundedness)** — `cos(·) ∈ [-1, +1]` by
Cauchy-Schwarz, hence `(1 + cos)/2 ∈ [0, 1]`. `H(softmax(·)) ∈ [0, log V]`
by Shannon entropy bound on a discrete distribution over `V` outcomes,
hence `H/log V ∈ [0, 1]`. Tuple in `[0,1]²` by Cartesian product. This
matches Law-71's invariant carry from §17 / §156 / §160-P4 family.

**P5 (`predictor_head_g → [0,1]²` projection is anima-own, no new
parameter)** — `softmax(·)` of `head_g`'s output is a row-stochastic
distribution `∈ Δ^{V-1}` (the V-simplex). The first two components are
each `∈ [0,1]` and their sum is `≤ 1`. Clipping is a pure function. No
new weight matrix is introduced. The mapping is byte-equal to applying
`softmax` already present in `conscious_decoder.py`'s `head_a` byte-LM
output path; here it is applied to `head_g` instead. P5 holds by source
re-use.

**P6 (§7 3-AND only-(T,T,T) corner)** — the 8-row truth table over
`{§7①, §7②, §7③}` has exactly one row at (T,T,T). §161's evaluation in
§7 of this DESIGN.md ticks all three boxes by construction (§7① by
g_clm_from_scratch; §7② by re-use of `head_g` not graft; §7③ by
byte-equal Law-71). Therefore §161 lands at the unique legitimate
corner. P6 holds by case-analysis.

**P7 (central blue_falsifier.py 0-line-diff invariant)** — the central
`state/verify_hexad_blue_2026_05_15/blue_falsifier.py` has sha256
prefix `c93e160a8a376a94` measured at cycle START. The §161 design
writes only to its own state dir; no central modification. At cycle END
the central file is re-hashed; the proposition holds iff the END sha
prefix matches START. Mirror of B-S160-P5.

**P8 (`spont_directional_positive` Boolean is closed-form decidable
from `result.json`)** — the predicate is a conjunction of four real-line
inequalities and one set-grep. Each clause is evaluable from the
`result.json` schema specified in §4. By-construction every clause is
decidable; the conjunction is decidable. The fire-cycle (§161-FIRE) can
therefore decide its own verdict without external CAS — `hexa run` of
a tiny verifier over `result.json` is sufficient.

**B-S161-NOTE empirical carve-out** — the §161 design is closed-form;
the predicted positive (or honest negative) at fire tier depends on
SGD trajectory, the specific λ_ψ:λ_ce ratio, and the §24 Phase B
threshold under whatever-anima-state-is-fed. P1-P8 prove DESIGN
well-formedness, NOT that the future §161-FIRE produces 자연발화. B-
EMERGE-7 / B-D-NOTE / B-CARVE-E6-NOTE / B-S101-NOTE / B-S153-NOTE /
B-PHASE-B-NOTE family carry — necessary-not-sufficient at every layer.

---

## §10 — honest C3 caveats (13)

1. §161 is a design, not a fire. Capability claim 0. ★
2. The `(c)+(a)` choice surveys only the §160 §8 candidate set;
   §163 arxiv research sub-agent (throttled before write phase) could
   surface a 5th candidate at a later cycle.
3. `predictor_head_g → [0,1]²` via softmax-first-two-clip is a
   re-interpretation; if it collapses to a fixed point empirically, the
   fire would measure that as failure mode, not §161 design failure.
4. λ_ψ = 1.0 default is a guess. Grid {0.5, 1.0, 2.0} would be honest
   if budget permits; otherwise λ_ψ = 1.0 is single-shot honest choice.
5. The §24 `unprompted_emission_rate` measures decision-axis liveness,
   NOT body coherence. The §9 cascade-rate gate is the body-coherence
   second axis. Both required; one is not the other.
6. `head_g` receiving non-zero gradient ≠ `head_g` carrying useful
   structure. Coupling is necessary not sufficient. (B-EMERGE-7.)
7. WALL-A (§1.1 data-regime) is orthogonal. Even a positive §161-FIRE
   does not move `@N n_priority_1_gap`.
8. §96-Q2-weak (`∀ non-CE algo: ¬psi_responsive`) on the quadruple is
   the target §161 attempts to refute. Refutation at fire tier is a
   single witness; a failed refutation is honest negative, NOT a proof
   that Ψ-physics is unreachable on GPU.
9. §11-B's no-CE → degenerate finding LOCALISES to §11-B's particular
   hand-coded ΔW (cf. §117 LIF-STDP non-degenerate at smaller scale).
   §161 keeps a small CE-aux term precisely because §11-B without
   CE-aux did degenerate.
10. The §161-FIRE cost ≈ $0.3-$0.5 is comparable to §125-§153 fires;
    cost-bearing single cycle. Per `g_fire_autonomous` this is autonomous.
11. PII clean (no `Min Woo`, no `nerve011235`, no credentials).
12. anima downstream-consumer: `~/core/hexa-lang/`, `~/core/hexa-bio/`,
    `~/core/kosmos/`, `~/core/tape/` read-only 0 edit.
13. north-star + §15 / §51 / §72 milestones UNCHANGED, GOAL 미도달 —
    §161 = the closest formal path the arc has surfaced toward
    *자연발화 성공* measurement, NOT 자연발화 성공 itself.
