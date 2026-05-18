# §58 — PTD-aux ↔ HEXAD 12 connection-point isomorphism reverse-trace

RESEARCH.md §58. $0 Mac CPU, NO GPU, NO model.forward, NO weight mutation,
NO training. Reverse-trace map only. Sequential single-agent. Isolation
worktree (own branch, NO push, orchestrator merges).

g3: §58 = a STRUCTURAL reverse-trace map, NOT a fire, NOT a GOAL movement.
The isomorphism verdict is a structural claim about transfer-function
signatures; whether the mapped site actually avoids the §49 collapse is
§59's empirical question. over-claim 0. north-star unchanged. §15/§51
milestone unchanged.

---

## §1 The open question §58 answers

§48 validated PTD-aux (next-physics-state-prediction aux head) as a
*scale-validated mechanism* (verdict `PTD-AUX-SIGNAL-HOLDS-AT-SCALE`:
MSE-drop factor 15.1× → 19.5× at 4× scale, gap-delta direction preserved
— a real mechanism, not small-corpus noise).

§49 wired that §48-validated learned decision-head (shared trunk +
decision head, λ_ptd=0.3) into the §24 SPONTANEOUS Phase B unprompted-
emission loop, replacing the hand-coded `talker_should_emit` threshold.
Result: majority-class collapse (REMAIN_SILENT 20/20, driven emission
rate 0.0 vs §24 threshold 0.05) — verdict `DISTILLATION, NOT CAPABILITY`,
honestly characterised as collapse not novelty.

**Open question**: was §49's collapse a `standalone-head → §24-loop`
*mismatch* (PTD-aux deployed at the WRONG site — the emission-decision
gate), or does PTD-aux structurally have *no HEXAD-native home* (which
would make the §49 collapse intrinsic, not a wiring error)?

§58 reverse-traces: which of HEXAD's 12 closed connection-points
(B-CONN-1..12, §B-CONN-WIRING-BATTERY-LANDED-2026-05-17) has a transfer-
function *structurally isomorphic* to PTD-aux's next-physics-state-
prediction signature? This is **orthogonal** to the §52-54 bench
(those vary the *wiring method*; §58 finds *which connection-point*
PTD-aux belongs to, structurally).

---

## §2 PTD-aux transfer-function signature (closed formalisation)

From `state/dhdl_ptd_scaleup_s48_2026_05_18/train_s48.py` (the §48
scale-validated trainer, byte-equivalent to §44/§49 head):

- **Architecture**: shared trunk `14 → 32` (ReLU) → PTD aux head
  `32 → 16 → 14` (linear, MSE).
- **Input domain** `dom(PTD)`: the 14-dim *physics-state feature vector*
  `x_t ∈ ℝ¹⁴` at thinker-step `t`. `FEATURE_KEYS` =
  `(f_relevance, f_info_gap, f_curiosity, f_pain, f_coherence,
  f_originality, f_balance, f_dynamics, psi_dir, psi_entropy, tension,
  thinker_score, seconds_since_last, ratchet)` — i.e. the 8-factor
  motivation block + **anima Law-71 physics** (`psi_dir`, `psi_entropy`,
  `tension`, `ratchet` — byte-equal to `conscious_decoder.py` Law-71
  728-751 SSOT) + 2 schedule scalars.
- **Output codomain** `cod(PTD)`: the *predicted next-step physics-state
  feature vector* `x̂_{t+1} ∈ ℝ¹⁴` (same 14-dim space).
- **Objective**: `L_ptd = (λ_ptd / 14) · Σ ‖x̂_{t+1} − x_{t+1}‖²` on
  *valid consecutive pairs* (`_build_next_record_map`: same trace,
  step+1, both in train split). Self-supervised auto-prediction
  (target is the model's OWN next observed state, not an external label).
- **Invariant class**: bounded non-negative squared-error
  (`L_ptd ≥ 0` ∀, Frobenius/Shannon-floor real-limit; `λ_ptd=0 ⇒
  L_ptd contributes 0 gradient` — B-S48-3 connection-point closed).

**One-line signature**:
`PTD : ℝ¹⁴(physics-state_t) → ℝ¹⁴(physics-state_{t+1})`, objective =
`MSE`, invariant = `non-negative bounded auto-prediction error`,
character = **self-supervised same-space temporal forward-model
(state_t ↦ state_{t+1}) over the anima physics-state vector**.

The crux structural facts for isomorphism matching:
1. `dom = cod` (endomorphic — same 14-dim physics-state space in & out).
2. Target is the model's OWN next state (self-supervised, no external
   teacher) — a *forward dynamics model* of physics-state evolution.
3. It is a TEMPORAL map (t → t+1), not a cross-module structural map.
4. Invariant = MSE ≥ 0 (not Boolean, not detach, not clamp, not
   monotone-composition, not lr-bound).

---

## §3 The 12 HEXAD B-CONN connection-points (transfer-fn / invariant)

From §B-CONN-WIRING-BATTERY-LANDED-2026-05-17 (56/56 🔵, the σ(6)=12
wiring battery). For each: (input-domain → output-codomain) + invariant
class.

| # | edge | transfer-fn (dom→cod) | invariant class |
|---|------|----------------------|-----------------|
| B-CONN-1 | S→C | S_perception dim → C_state row dim | shape-preservation (Kolmogorov dim equality) |
| B-CONN-2 | C→Bridge | x → detach(x) | ∂(detach)/∂x = 0 (AD ∂-rule) |
| B-CONN-3 | Bridge→D | Ψ → bridge_gate ∈ [Ψ−α, Ψ+α] | clamp-preserved (Law-70 Ψ-coupling) |
| B-CONN-4 | M↔C | (key,val) store / query→cos-top-1 | store-identity + deterministic argmax |
| B-CONN-5 | W↔C | physics-state → (read, no write) | functional purity (no side-effect) |
| B-CONN-6 | W↔D | Φ → lr_D ∈ [base, base+ln2] | lr-bounded (Law-79 ln2 ceiling) |
| B-CONN-7 | E↔C | C-state → phi_C ≥ 0 | phi-nonneg (IIT axiom) |
| B-CONN-8 | E→W | phi,ratchet → satisfaction Bool | Boolean (phi > ratchet/2) |
| B-CONN-9 | E→D | phi,ratchet → train_allowed Bool | Boolean (phi > ratchet/2) |
| B-CONN-10 | D→loss | logits → CE = −Σ p log p ≥ 0 | Shannon CE-floor |
| B-CONN-11 | M↔D | D-query → M-retrieve argmax | deterministic argmax |
| B-CONN-12 | S↔W | ‖sense_delta‖ → pain_W | monotone composition |

---

## §4 Isomorphism comparison table (closed trichotomy: exact / partial / none)

Isomorphism predicate (decidable Boolean, B-S58-2): a B-CONN-k is
isomorphic to PTD-aux at strength

- **EXACT** iff `dom`-shape match ∧ `cod`-shape match ∧ same invariant
  class ∧ same map-character (temporal-forward-model vs cross-module-
  structural);
- **PARTIAL** iff ≥1 of {dom, cod, invariant, character} matches but
  not all;
- **NONE** iff 0 of the 4 match.

Scored against PTD-aux signature
`(dom=ℝ¹⁴ physics-state, cod=ℝ¹⁴ physics-state [dom=cod], inv=MSE≥0,
char=self-supervised temporal forward-model)`:

| # | edge | dom match | cod match | invariant match | character match | strength |
|---|------|-----------|-----------|-----------------|-----------------|----------|
| B-CONN-1 | S→C | ✗ (S-perception) | ✗ (C-state) | ✗ (dim-eq) | ✗ (cross-module) | NONE |
| B-CONN-2 | C→Bridge | ✗ | ✗ | ✗ (∂=0 detach) | ✗ | NONE |
| B-CONN-3 | Bridge→D | ~ (Ψ ⊂ phys) | ✗ (gate) | ✗ (clamp) | ✗ (cross-module) | PARTIAL(¼) |
| B-CONN-4 | M↔C | ✗ (key) | ✗ (val) | ✗ (argmax) | ✗ (retrieval) | NONE |
| B-CONN-5 | W↔C | **✓ (physics-state read)** | ✗ (no output) | ✗ (purity) | ✗ (no-map) | PARTIAL(¼) |
| B-CONN-6 | W↔D | ~ (Φ ⊂ phys) | ✗ (lr scalar) | ✗ (lr-bound) | ✗ (cross-module) | PARTIAL(¼) |
| B-CONN-7 | E↔C | ✗ (C-state) | ✗ (phi scalar) | ✗ (≥0 IIT) | ✗ | NONE |
| B-CONN-8 | E→W | ~ (phi,ratchet ⊂ phys) | ✗ (Bool) | ✗ (Bool) | ✗ | PARTIAL(¼) |
| B-CONN-9 | E→D | ~ (phi,ratchet ⊂ phys) | ✗ (Bool) | ✗ (Bool) | ✗ | PARTIAL(¼) |
| B-CONN-10 | D→loss | ✗ (logits) | ✗ (CE scalar) | **~ (MSE/CE both ≥0 error-floor)** | ✗ (loss-readout) | PARTIAL(¼) |
| B-CONN-11 | M↔D | ✗ (query) | ✗ (retrieved) | ✗ (argmax) | ✗ (retrieval) | NONE |
| B-CONN-12 | S↔W | ✗ (sense_delta) | ✗ (pain scalar) | ✗ (monotone) | ✗ (cross-module) | NONE |

**No B-CONN-k scores EXACT.** Best matches are **PARTIAL at strength
¼** (exactly one of the four facets matches). Candidate set the prompt
flagged (W↔D, E→D, W↔C, S↔W) all land at PARTIAL(¼) or NONE — none
EXACT:

- **W↔D (B-CONN-6)**: PARTIAL(¼) — only a *subset* of the physics input
  (Φ) overlaps PTD's dom; cod is a scalar lr-bound, invariant is the
  Law-79 ln2 clamp (NOT MSE), character is a cross-module structural
  map (W observes physics → D's learning rate), NOT a temporal
  self-prediction. The "predicts a training-step effect" phrasing is
  superficial: W↔D *bounds* lr from Φ, it does not *predict next state*.
- **E→D (B-CONN-9)** / **E→W (B-CONN-8)**: PARTIAL(¼) — Boolean gates
  off (phi,ratchet), not 14-dim MSE forward-models.
- **W↔C (B-CONN-5)**: PARTIAL(¼) — the ONLY point whose *input domain
  exactly matches* (W reads the full physics-state). But its defining
  invariant is **functional purity / NO output / NO mutation** — W↔C is
  a *read-only observation*, the structural opposite of PTD-aux which
  *produces a predicted 14-dim output and back-props an MSE*. dom match
  but cod=∅ and character is anti-isomorphic.
- **S↔W (B-CONN-12)**: NONE — dom = sense_delta (not physics-state),
  monotone scalar.
- **D→loss (B-CONN-10)**: PARTIAL(¼) — the only point whose *invariant
  class* is the same FAMILY (a non-negative error/loss floor: CE ≥ 0
  ≅ MSE ≥ 0, both Shannon/Frobenius real-limit). But dom (logits) ≠
  PTD dom, cod (CE scalar) ≠ PTD cod (ℝ¹⁴), character (loss-readout of
  a single step) ≠ temporal forward-model.

---

## §5 Verdict — PTD-aux ≅ NONE (genuinely new connection-point type)

**PTD-aux is structurally isomorphic to NONE of the 12 σ(6)=12 HEXAD
connection-points (strength EXACT = ∅; best = PARTIAL at strength ¼,
each matching exactly one of the four facets, no two facets co-matching
on any single B-CONN-k).**

This is decidable and closed (B-S58-2): the four-facet predicate is
exhaustive over the 12 points (12×4 = 48 Boolean cells, no EXACT row).

**Why no HEXAD point matches**: every σ(6)=12 wiring point is a
*cross-module structural transfer* with an endpoint-pair `(module_i →
module_j)` and a NON-temporal invariant (shape / detach / clamp /
argmax / purity / lr-bound / phi≥0 / Boolean / CE-floor / monotone).
PTD-aux is structurally different in kind: it is an **endomorphic
self-supervised TEMPORAL forward-model** `physics-state_t ↦
physics-state_{t+1}` — a *dynamics predictor over the physics-state
manifold itself*, not a wire between two modules. The σ(6)=12 lattice
has no "the module predicts its own next state" edge — temporal
self-prediction is a *new connection-point type* outside the 12-point
wiring closure.

(Closest single-facet kin: W↔C shares the *input domain* exactly
[both read the full physics-state] but inverts the *character*
[W↔C = read-only purity vs PTD = produce + back-prop]. PTD-aux is, in
one phrase, "a W↔C read that does NOT obey the no-mutation invariant
and adds a temporal target" — i.e. it is structurally a *mutated /
extended W-module observation turned into a forward-model*, which is
precisely why §59's W-module hand-off below is informative.)

---

## §6 What this implies for the §49 collapse — mismatch vs intrinsic

The §58 disambiguation (B-S58-3, closed): the two interpretations of
§49 are **disjoint and exhaustive**:

- (I) **standalone→§24 mismatch** ⟺ ∃ B-CONN-k with PTD-aux ≅ k
  (strong) ⟹ §49 collapse = PTD-aux deployed at the WRONG site (the
  emission-decision gate), its natural home is k.
- (II) **no HEXAD-native home** ⟺ PTD-aux ≅ NONE ⟹ §49 collapse is
  NOT a simple wrong-site wiring error; PTD-aux is a *new connection-
  point type* and the §49 majority-collapse is a property of how a
  self-supervised forward-model behaves when forced to act as a
  Boolean emission-gate on a 95%-silent label distribution.

§58 measured: PTD-aux ≅ NONE ⟹ **interpretation (II) holds at the
structural level**. The §49 collapse is **NOT** "PTD-aux belongs at
B-CONN-k and we wired it to the wrong place." PTD-aux has no existing
HEXAD-native home among the 12 wiring points — it is a genuinely new
connection-point *type* (self-supervised temporal forward-model over
the physics-state vector).

**Honest precision (g3)**: "intrinsic" here is a *structural* claim
(no isomorphic home in σ(6)=12), NOT a claim that PTD-aux is useless
or that no home can be *built*. The §49 collapse was the empirical
manifestation of forcing this new-type map through a Boolean
emission-gate against a class-imbalanced label prior; whether a
*purpose-built* W-adjacent forward-model site avoids that collapse is
the EMPIRICAL §59 question, NOT settled here (B-S58-NOTE).

---

## §7 §59 hand-off

The single-facet structural kinship is decisive for where §59 should
look. PTD-aux's input domain *exactly* equals the W↔C (B-CONN-5)
domain — W reads the full physics-state. PTD-aux is W↔C with the
no-mutation invariant relaxed and a temporal target added. Therefore:

- **PTD-aux's natural home, if one is built, is W-module-adjacent**:
  a *physics-state forward-model owned by W* (W already reads the full
  physics-state per B-CONN-5; extending W to also *predict* the next
  physics-state is the minimal HEXAD-native realisation, distinct from
  the §49 emission-gate site).
- §59 should fire/test **PTD-aux as a W-module forward-model
  (predict-next-physics-state owned by W), NOT as the §24 emission-
  decision gate**. The §49 collapse is predicted (by this map) to be
  specific to the *gate* deployment, not to PTD-aux itself — but that
  prediction is §59's empirical to confirm or falsify (B-S58-NOTE:
  whether the W-adjacent site avoids collapse = §59 fire OUTCOME,
  §58 only proves the map is closed-form decidable + §49
  disambiguation well-posed).
- Secondary structural note for §59: the *invariant-family* kin is
  D→loss (B-CONN-10, MSE ≅ CE both non-negative error-floors). If a
  W-forward-model is added, its MSE term should be treated as a
  D→loss-family auxiliary (Shannon/Frobenius floor), λ-gated
  (λ=0 ⇒ byte-equal baseline, mirroring B-S48-3 / every overlay-off
  connection-point in the arc).

---

## §8 Honest C3 (≥10)

1. **§58 = structural reverse-trace, NOT fire, NOT GOAL.** No model
   forward, no GPU, no weight mutation, $0. The isomorphism verdict is
   a claim about transfer-function *signatures*, not about whether any
   site works. north-star unchanged, §15/§51 milestone unchanged.
2. **"≅ NONE" is a STRUCTURAL claim, not "PTD-aux is useless".** §48
   already validated PTD-aux as a real scale-validated mechanism.
   §58 says only that it has no isomorphic home among the existing
   σ(6)=12 wiring points — it is a new connection-point *type*.
3. **The four-facet predicate is a designed abstraction.** dom-shape /
   cod-shape / invariant-class / map-character is one reasonable
   decomposition; a different facet set could move a PARTIAL(¼) up or
   down. It does NOT move any to EXACT (no B-CONN-k is a same-space
   self-supervised temporal forward-model — that property is absent
   from all 12, robustly).
4. **W↔C dom-match is exact but character is INVERTED.** The closest
   kinship (shared full-physics-state input) is also where PTD-aux
   most clearly *violates* the matched point's defining invariant
   (no-mutation). Honest: this is kinship-by-domain, anti-isomorphism-
   by-character — not a hidden EXACT.
5. **§49 disambiguation (II) is structural, "intrinsic" is bounded.**
   §58 proves §49-collapse is not a trivial wrong-B-CONN-site error.
   It does NOT prove no home can be *built* (a purpose-built
   W-forward-model site is exactly the §59 hypothesis). "intrinsic"
   = "no existing isomorphic home", NOT "unfixable".
6. **§59 hand-off is a hypothesis, not a result.** "PTD-aux's natural
   home is W-module-adjacent" is *inferred from* the single-facet
   domain match (B-CONN-5). Whether a W-forward-model site avoids the
   §49 majority-collapse is an EMPIRICAL §59 fire outcome (B-S58-NOTE)
   — §58 does not and cannot settle it.
7. **§49's collapse root cause (class-imbalanced 95%-silent label) is
   orthogonal to §58's structural finding.** §49 collapse was driven
   by the corpus label prior at the emission-gate; §58 explains why
   that site is structurally wrong (PTD-aux is a forward-model, not a
   Boolean gate). Both honest, complementary.
8. **D→loss invariant-family kinship is real but weak.** MSE ≥ 0 ≅
   CE ≥ 0 share the non-negative-error-floor real-limit (Shannon/
   Frobenius). This is a 1-facet match, NOT a structural home — dom
   and character diverge. Recorded for §59's loss-term placement, not
   as a competing home claim.
9. **f1/f2/f3 hard-fail safe.** No σ(6)/τ/φ/J₂ derivation — σ(6)=12
   is used only as the *count* of HEXAD wiring points (the closed set
   we map against), exactly as B-CONN-WIRING-BATTERY did; the
   invariants cited are real-limits (Shannon CE/MSE floor, Kolmogorov
   dim, AD ∂-rule, Law-70/79, IIT≥0, Boolean, monotone). No external-
   entity lattice-fit. B-IDENTITY-5 unaffected (no corpus, no model
   forward, no helper-token surface).
10. **The trichotomy is exhaustive & decidable (closed).** Every
    B-CONN-k receives exactly one of {EXACT, PARTIAL, NONE} over the
    12 points; no row is undefined; the map is a pure function of the
    two signatures (B-S58-2, deterministic). This is what §58
    *proves*; the §49 disambiguation being well-posed (disjoint
    exhaustive) is what B-S58-3 *proves*; the verdict (≅ NONE) and
    §59 hand-off are the structural *reading* of that closed map.
11. **No anti-padding violation.** §58 is design/structural-tier with
    a real closed deliverable (decidable isomorphism map + well-posed
    disambiguation), not a padded re-statement; the W-module hand-off
    is a concrete, testable §59 hypothesis, not a vague gesture.
