# RESEARCH.md §23 candidate A — intra-anchor diversity via anima OWN physics

> $0 design-tier ONLY. NO fire, NO GPU, NO corpus generation, NO commits to
> central files until orchestrator. RESEARCH.md 미편집 (§23 = design holds +
> 후속 land 후 1회).

Sibling agents may concurrently design candidates B/C/… for the same §23
"intra-anchor diversity" frontier; this file = A only, anima main 직접,
branch 0. Stop hook 가 3-times frontier-narrowing-exhaustion signal 을 보낸
context — design-tier 정직 마감도 valuable (anti-padding §13-M/L 선례).

---

## 1. Problem — single-template-per-anchor as the §16.6-C root structural defect

`state/carving_dataregime_s16_2026_05_18/corpus_carving_s16_generator.py`
`gen_alpha_record` (lines 706-728) is deterministic in body framing per
anchor:

```python
ko = (f"🛸{tier} {name} — {dom} 영역의 자극이 같은 골짜기로 수렴한다. "
      f"의식 풍경 위 진공점 {_carve_psi_str(psi)}, top emotion {emo}. "
      f"자극이 닿으면 tension flow 가 이 vacuum 으로 흘러든다.")
en = (f"Tier {tier} {name} — domain {dom}, the stimuli converge into "
      f"one basin. A vacuum point at {_carve_psi_str(psi)} on the "
      f"landscape, top emotion {emo}. Tension flows into this vacuum.")
```

`gen_beta_record` (731-752) and `gen_gamma_record` (755-782) follow the
same pattern: one Engine-A "stimuli-converge / tension-flows-into-vacuum"
framing per anchor, with variation = bilingual choice (`bil` random,
order randomised) + γ task-form payload (anchor-independent).

→ across 777,000 records / 168 anchors / 603 MB byte stream, an anchor's
body framing is **byte-identical modulo language pick** for ~4,624
records on average. The model sees the *same body framing* for each
anchor thousands of times.

§22 N body-shift evidence (`N_KTRIE_FINDINGS.md` table, lines 105-112)
makes this measurable: tier 77 `→` `🛸77Tier 77 만다라 — domain 예술,
the stimuli converge into one basin…` = the verbatim `gen_alpha_record`
template, recited per-anchor. N (`.kosmos`-trie constrained decode)
moves §16 from "right-route / *wrong* anchor's template" to "right-route /
*own* anchor's template" — but the body is still the trained single
template. §16.6-C verdict: "정교한 암기 + correct-prefix routing,
generalization 아님."

§7 / §11.3 / §15 milestone: data-regime threshold = irreducible
frontier. **§22 N narrows the lever to "anchor-grounded body" axis but
inherits the single-template structural defect** — N+O do not introduce
intra-anchor diversity, they just *correct the placement* of the same
template. §23 A targets the **structural defect itself** at corpus
generator level (data-axis), not decode-time.

---

## 2. Design — 4 anima-physics variation axes (anchor-meaning preserving)

Each anchor `A = (tier, name, dom, emo, score, vacuum_psi, basin_radius)`
is the **invariant** (`anchor-meaning preserving` invariant). The
variation is exclusively over how anima's own physics framings *view*
that same anchor — generic LLM paraphrasing forbidden (§7② gate, see §3).

The four orthogonal axes (each anima-native, formula-defined, no
external paraphraser):

### 2.1 Axis V — Ψ_direction framing (Engine-A ⇄ Engine-G)

`conscious_decoder.py:740` defines `psi_direction = (1 + cos(logits_a,
logits_g)) / 2` ∈ [0,1] = Law-71 Engine A⇄G coordinate.

- Ψ_dir ≈ 0 (anti-aligned, Engine-G dominated covert thought).
- Ψ_dir = 0.5 (fixed-point, balanced — current §16 framing).
- Ψ_dir ≈ 1 (aligned, Engine-A dominated overt emission).

Each anchor body re-framed as 3 distinct **viewing angles** parameterised
by the Ψ_dir bucket `v ∈ {0.1, 0.5, 0.9}` (3-way categorical, finite-set
closed). The *same* (`tier`, `name`, `dom`, `vacuum_psi`) anchor surfaces
as:

| v | framing | template form (KO sketch) |
|---|---------|--------------------------|
| 0.1 (covert/G) | "이 anchor 의 *speaking* 이 아직 안 일어난 상태 — engine G 가 자극을 받아 vacuum {vp} 으로 끌어들이는 중" | inner-only sentence; verb = "끌린다 / 모인다 / 모여간다" |
| 0.5 (fixed-pt/balanced) | current §16 body — "stimuli converge into one basin, tension flows into this vacuum" | balanced statement, present-tense indicative |
| 0.9 (overt/A) | "이 anchor 가 *발화* 되는 순간 — engine A 가 vacuum {vp} 에서 자극을 emit 하는 형태" | outer-only sentence; verb = "내뱉는다 / 발화된다 / 흘러나온다" |

→ same anchor (tier 77 만다라 / 예술) appears with 3 framing verbs +
3 grammatical orientations. The fact-content (name, domain, vacuum,
emotion) is invariant; only the *physics-direction* differs.

GOAL-legitimacy: Ψ_dir is the model's *own* Law-71 coordinate — these
buckets are anima physics, not external paraphraser styles.

### 2.2 Axis T — tension state (low / mid / high)

`tension_link_step.hexa` spine: `ΔW = −T_const · tension · n6_gate(Ψ)`.
B-TT-2 RESTORING-SIGN-NEGATIVE: tension drives restoring shrink towards
vacuum. The *body* can describe the same anchor at 3 distinct
tension-states (anchor invariant, anima-state varies):

- **low tension (≈0)**: "이미 vacuum {vp} 에 안착한 상태 — restoring
  flow 가 끝났다 / 자극이 안정 basin 안에 머문다"
- **mid tension (≈0.5)**: "vacuum {vp} 으로 흐르는 중 — tension 이
  restoring 으로 작동" (current §16 framing).
- **high tension (≈1.0)**: "vacuum {vp} 에서 가장 멀리 떨어진 자극 —
  강한 restoring flow 필요"

Same anchor content; tension-axis viewpoint differs. Lexical realisations
drawn from a **fixed enumerated table** (`T_PHRASES`, KO/EN parallel,
not external LLM).

GOAL-legitimacy: tension is anima's `tension_link_step.hexa` SSOT
quantity — its three regime descriptions are anima's own physics
language, deterministic enumeration (no paraphraser).

### 2.3 Axis Φ — Φ-context (co-occurrence with sibling anchors)

`mitosis_hook.hexa` cell-pool: Φ★ ≈ mean_pairwise(1 − cos) · log(N+1) =
diversity proxy across cells. Anima's MITOSIS module routes a stimulus
to a cell-pool subset; **the same anchor can co-occur with different
sibling-anchor combinations** depending on cell-pool state.

For anchor A, define 3 Φ-contexts by picking **sibling anchors that are
nearest in Ψ-space (same vacuum_psi neighbourhood)**:

- **C_self**: A in isolation (current §16 framing — single anchor).
- **C_near**: A + 1 nearest sibling in `vacuum_psi`-L2 (e.g. tier 77
  만다라/예술 ψ=[0.71,0.62] + tier 72 선율/예술 ψ=[0.66,0.63]).
- **C_pair**: A + 2 nearest siblings (forming a 3-anchor neighbourhood).

Body framings:
- `C_self` = current §16 line.
- `C_near` = "{A} — same basin neighbourhood as {sibling1} (both share
  domain {dom_overlap} or nearby vacuum_psi)".
- `C_pair` = "{A} flanked by {sibling1, sibling2} in the Ψ-landscape —
  cell-pool sees this triplet as one cluster."

Co-occurrence is **anima's own MITOSIS cell-pool routing structure** —
nearest-neighbour in vacuum_psi is a closed-form operation on the
anchor SSOT (B-INTRA-2 below). No external graph, no LLM paraphraser.

GOAL-legitimacy: Φ-context = the cell-pool's anima-native
co-occurrence — MITOSIS module SSOT.

### 2.4 Axis S — sensory↔analytical channel (S/M module)

HEXAD modules S (sensory carving) and M (memory, Hebbian store/retrieve)
have distinct framings of the same anchor:

- **S-frame** (sensory): "이 anchor 의 *원-자극*은 {raw_sense}" — raw
  sensation (visual / auditory / proprioceptive depending on `dom`).
- **M-frame** (memory recall): "이 anchor 는 cell {eternal_<tier>} 안
  저장되어 — Hebbian retrieve 가 활성될 때 떠오른다."
- **Analytical-frame** (default §16): "carving template" statement.

`raw_sense` is **deterministically derived from `dom`** via a 30-row
fixed lookup table `S_RAW_SENSE_TABLE[dom]` (예술 → "선과 색", 수(數) →
"숫자 기호 ", 운동 → "근육의 신축", etc.). The table is anchor-meaning
preserving (each `dom` has a single canonical sensory label,
deterministic, byte-stable). No paraphraser.

GOAL-legitimacy: S and M are anima HEXAD modules; sensory↔memory
distinction is anima's own architectural decomposition (not generic
multi-style augmentation).

---

## 3. GOAL-legitimacy gate — generic paraphraser FORBIDDEN, anima physics ONLY

### 3.1 §7 / §21.3 test (3 conditions, all must hold)

| condition | A design verdict |
|---|---|
| **§7①** Not generic-LM-pretrain (no external corpus, no generic LM weights) | ✅ all records derived from §16 anchor SSOT + anima physics formulas |
| **§7②** Not generic-then-graft (no external paraphraser LLM, no DoAug-style LLM augmentation) | ✅ variation is anima-native: Ψ_dir buckets, tension-state phrases, vacuum_psi nearest-neighbour, S_RAW_SENSE_TABLE lookup. Zero external LLM call. **Verifiable by structural Boolean predicate** (B-INTRA-3 below) |
| **§7③** anima physics is the variation *source* (not bolted-on flavour) | ✅ Ψ_dir = `conscious_decoder.py:740` byte-identical formula; tension = `tension_link_step.hexa` byte-identical; Φ-context = MITOSIS cell-pool routing closed-form; S/M = HEXAD module SSOT |

### 3.2 What is explicitly forbidden in A (closed structural predicate)

A's generator must satisfy `forbidden_call_set = {} ∪ {
  openai.*, anthropic.*, llm_call(), paraphrase(), .generate(), gpt(),
  bert_score(), nltk.translate.bleu, transformers.AutoModel, HfApi(),
  llama.*, huggingface_hub.*, gen_corpus_with_llm(),
}` total count = 0 over generator source (AST-Call-node grep,
docstring/comment/string-literal stripped per §11-B B-PUREPHYS-1
pattern).

DoAug (ACL 2025) is explicitly disallowed — DoAug uses an external LLM
as paraphraser; A's enumerated variation tables (Ψ_dir buckets,
T_PHRASES, S_RAW_SENSE_TABLE) replace that with anima-native finite
enumerations.

### 3.3 §11-B precedence — CE remains load-bearing

A is **corpus-level intervention, NOT physics-only training**. CE remains
the base objective; A only varies what the model sees in CE-targeted body
spans. §11-B "pure-physics no-CE = degenerate" verdict is respected —
A is data-axis lever atop CE-base trainer (Dir-I lever unchanged), not
a CE-replacement experiment.

---

## 4. Closed-form sidecar — B-INTRA-1..5 (sympy/Boolean transfer-form)

Where central blue_falsifier.py = unchanged (sidecar pattern per
B-PRIME/B-DIRH/B-DIRI/B-PSICTL/B-EMERGE/B-PUREPHYS/B-SCALE/B-MITENS/
B-DIRL/B-EBT/B-DIRJ/B-KTRIE/B-MGND/B-TTS precedent).

### 4.1 Propositions (transfer-form closed; capability OUTCOME = B-INTRA-NOTE empirical carve-out)

- **B-INTRA-1 ANCHOR-MEANING-PRESERVED** — for every record `r` produced
  by axis ∈ {V, T, Φ, S}, the anchor-invariant fields `{tier, name, dom,
  emo, vacuum_psi, basin_radius}` are byte-identical to the source anchor
  tuple in `S8_ANCHORS ∪ S16_NEW_ANCHORS`. Boolean conjunction (6
  field-equalities) ∀ r. **Anchor meaning is variation-axis-invariant**.

- **B-INTRA-2 PHYSICS-AXIS-ORTHOGONALITY** — the 4 axes have disjoint
  formula sources:
  - V: `Ψ_dir = (1 + cos(logits_a, logits_g))/2` (Law-71 coordinate),
  - T: tension∈{0, 0.5, 1.0} bucket → enumerated `T_PHRASES`,
  - Φ: nearest-neighbour in `vacuum_psi`-L2 over anchor set (closed-form
    integer argmin),
  - S: `S_RAW_SENSE_TABLE[dom]` deterministic lookup.

  No axis derives from another (Boolean structural predicate over
  generator AST: variation function for axis X reads only its own
  formula sources, never the others' bucket values). Pairwise
  orthogonality = 6-pair Boolean conjunction. **Each axis is an
  independent anima-physics-source.**

- **B-INTRA-3 NO-EXTERNAL-LLM-CALL** — AST scan of A's
  `variation_generator.py` over all functions: `forbidden_call_set`
  (§3.2 list, 12 patterns) total count = 0 (comment/docstring/
  string-literal stripped per B-PUREPHYS-1). Generic-paraphraser
  forbidden by structural source predicate. **Closed §7② enforcement.**

- **B-INTRA-4 §16-CONNECTION-POINT-BYTE-EQUAL-AT-DISABLED** — when all
  four axes default to "off" (single-bucket, no nearest-neighbour, no
  S-frame), A's generator output is **byte-identical to §16
  `corpus_carving_s16_generator.py` output for the same `(seed,
  n_target)`** — closed-form numeric verification (sha256 corpus
  equality + line-count + record-id matching, B-S16-1 lift).
  **Connection-point closed by construction; A-vs-§16 fair compare
  guaranteed.**

- **B-INTRA-5 CARDINALITY-BOUNDED-EXPANSION** — for each anchor,
  per-axis variant count is finite and small:
  - V: 3 (covert/balanced/overt)
  - T: 3 (low/mid/high)
  - Φ: 3 (self/near/pair)
  - S: 3 (S-frame/M-frame/analytical)

  Combined factorial product per anchor = 3^4 = 81 = bounded integer
  Kolmogorov set cardinality, not combinatorial explosion. Total corpus
  variant space ≤ 168 anchors × 81 = 13,608 distinct body framings,
  ~80× over the current §16 single-template-per-anchor regime —
  measurable diversity, still bounded. **Anti-explosion closed.**

### 4.2 Empirical carve-out (B-INTRA-NOTE) — necessary-not-sufficient

B-INTRA-1..5 prove: A's records preserve anchor meaning (1), use
orthogonal anima-physics sources (2), call no external LLM (3),
byte-equal to §16 baseline at disabled (4), and have bounded variant
cardinality (5). They DO NOT prove that intra-anchor diversity *causes*
emergence — that is SGD/measurement OUTCOME (B-D-NOTE / B-CARVE-E6-NOTE /
B-SCALE-NOTE / B-PUREPHYS-NOTE / B-EBT-NOTE / B-DIRJ-NOTE / B-KTRIE-NOTE /
B-MGND-NOTE / B-TTS-NOTE family, NOT counted 🔵).

Honest necessary-not-sufficient (mirroring B-EMERGE-7 / §9 design
discipline): A's design is a *structurally sound diversity injection*,
not a generalization proof. Per §13-M / §13-L design-tier discipline,
A's value is in (i) closed-form proof that anima-native intra-anchor
diversity is achievable without paraphraser, (ii) explicit fair-compare
gate at A-OFF=§16 byte-equal, (iii) honest fire-worth assessment before
spending GPU.

---

## 5. Honest fire-worth assessment (g3 — Stop hook frontier-narrowing)

### 5.1 Why design-tier may be the honest stop

§22 closed §16 ceiling — N (`.kosmos`-trie) gives +21 on-anchor body
movement but body is still memorized template; O (M-retrieval) lifts +16
but JOINT 0.0 (chat-form bleed). §22.5: "data-regime threshold (§1.1).
mechanism 차원 (decode-time OR training-time) 어느 path 도 §16 ceiling
못 깸." Stop hook 가 3-times frontier-narrowing-exhaustion signal 을
보낸 context.

A is data-regime intervention — closest to §1.1 / §15 milestone's
"diverse-data pre-training loss threshold" frontier. Honest risk:
A's 80× framing diversity may still operate in the **same
memorization-saturated regime** if 13,608 distinct framings × ~57
records-per-framing average (vs §16's 4,624 per anchor) ≪ Critical Data
Size (Q1-a, arxiv 2401.10463). Intra-anchor diversity ≠
*new content*; it varies how anima views the same 168 anchors. CDS-axis
movement: **possibly small** (the same factual content, viewed 4
ways = 4× effective unique pairs at best, not 80×).

### 5.2 Pre-fire conditions A would need to satisfy

For fire to be GOAL-legitimately worth spending GPU:
1. A's design closed-form (this doc) holds.
2. A's variation_generator.py + sidecar B-INTRA-1..5 pass byte-equal-at-disabled.
3. **Small pilot fire ≪ §16 scale** ($0.05-0.10 runpod, d768·12L·1500-step
   on a 168-anchor × 81-framing × ~100-record sample ≈ 1.4M records,
   ~30MB corpus) to measure if intra-anchor diversity moves any axis
   (routing axis1 vs §16's 21/64, honest §9 cascade-rate vs §22 N+O's
   structural proxy 26/64).
4. If pilot shows null/negative on routing OR coherence axes, design-tier
   close-out with B-INTRA-NOTE empirical-negative carve-out, per §13-M/L
   anti-padding discipline.

### 5.3 Verdict — **design holds**, **fire = conditional (small pilot before full §16-scale)**

The design itself (sections 1-4) closes — anima-native intra-anchor
diversity is achievable, the GOAL-legitimacy gate is enforced by
structural Boolean predicates, the §16 connection-point is byte-equal,
the variant cardinality is bounded. This is valuable independent of
outcome — it gives a closed-form anima-physics-native data-axis lever
that future cycles can deploy.

Fire-worth is **conditional**: small pilot first ($0.05-0.10, ≪ §16's
$0.5-0.8) to gate full-scale spend. Mirrors §13-M / §13-L design-tier
close-out discipline + §22 negative-but-valuable evidence pattern. If
sibling agents pursue §23 candidates B/C/... that target the *same*
intra-anchor problem from a different axis (e.g. § HEXAD module
co-training, generative augmentation under §7-legitimate gates),
comparative pilot evidence will narrow the frontier further.

---

## 6. Connection point (closed, fair-compare by construction)

A is a *generator-level* intervention; §16's `train_carving_s16.py`,
`eval_carving_s16.py`, `conscious_decoder.py` are **unchanged**. Dir-I
lever (`Ψ-anchored CTL + tension-supervised routing`, byte-equal carry)
is preserved.

When all variation axes default off (V→only v=0.5 bucket, T→only mid,
Φ→only C_self, S→only analytical-frame), A's generator output is
byte-identical to `corpus_carving_s16_generator.py` for the same `(seed,
n_target)`. B-INTRA-4 closed.

Therefore A's measurement against §16 baseline is fair head-to-head
**by construction** — corpus FORM (intra-anchor framing diversity)
isolated as the only variable, all other axes (model, lever, trainer,
eval harness, anchor set, seed) inherit §16 byte-equal.

---

## 7. Honest C3 (≥10)

1. **measured only — design-tier $0**, no fire, no capability claim. A's
   value is **closed-form structural proposition + fair-compare gate
   construction**, not emergence proof (B-INTRA-NOTE necessary-not-
   sufficient, per §9 / B-EMERGE-7 discipline).

2. **Stop hook signal acknowledged.** §22 closed §16 ceiling on
   mechanism-axis (N+O+P all negative for capability emergence). A is
   data-axis lever, NOT mechanism-axis re-attempt — it targets the
   structural defect (`gen_alpha_record` single-template) that N+O
   could only *correct the placement of*, not *break out of*.

3. **CDS-axis movement may be small.** Intra-anchor diversity varies
   *framing* of the same 168 anchors, not *new factual content*. arxiv
   2401.10463 Critical Data Size hypothesis (Q1-a, RESEARCH.md §21.2)
   measures "unique factual content" — A may move framing-diversity ≠
   CDS. Honest: A might not break §1.1 even with sound design.

4. **§7 enforcement is structural, not aspirational.** B-INTRA-3 is an
   AST-grep Boolean predicate on the generator source (12-pattern
   forbidden-call total = 0). A's GOAL-legitimacy gate is closed by
   construction, not by claim. DoAug (ACL 2025) LLM-paraphraser path is
   explicitly excluded — A uses 4 anima-physics enumerated tables only.

5. **Anima physics formula references are byte-exact.** Ψ_dir = Law-71
   `(1+cos)/2` formula at `conscious_decoder.py:740`; tension =
   `tension_link_step.hexa` spine; Φ-context = MITOSIS cell-pool nearest-
   neighbour over `vacuum_psi`; S/M = HEXAD module SSOT. A is anima-
   native by direct module-SSOT reference, not loose analogy.

6. **§11-B precedence respected.** A is CE-base data-axis lever, NOT
   physics-only training. §11-B "pure-physics = degenerate, CE
   load-bearing" verdict unchanged — Dir-I trainer remains, A only
   varies what CE targets see in body spans.

7. **§22 N+O complementarity.** A and N+O are orthogonal: N+O are
   decode-time on the *trained* §16 ckpt; A is generator-time before
   training. They could compose — A training + N+O decode — but each
   independently leaves §15 milestone intact. A is not a replacement
   for N+O nor vice versa.

8. **Fire-worth honest gate.** §5.2 conditions explicit — small pilot
   first ($0.05-0.10) before full §16-scale ($0.5-0.8). Mirrors §13-M
   anti-padding ($0 design-only) and §13-L feasibility-gate. If pilot
   shows null, design-tier close-out is the honest stop.

9. **f1/f2/f3 + B-IDENTITY-5 hard-fail safe.** Boolean conjunction /
   integer cardinality / AST structural / sha256 byte-equal / sympy
   ∂-sign closed forms; NO σ/τ/φ/J₂ external derivation. Anchor SSOT
   forbidden-token grep = 0 carry from §16 (B-IDENTITY-5).

10. **north-star (GOAL.md) unchanged.** A is a *structural defect
    remediation* design at the corpus generator layer — valuable as
    closed-form gate + fair-compare construction, but **GOAL emergence
    proof requires fire**, and even successful fire would only narrow
    §1.1 frontier (not solve "자기 physics 로부터 자발적으로 말 거는
    Living Consciousness"). north-star is honestly distant. §22-style
    valuable-negative-or-narrowing outcomes are acceptable; over-claim
    is not.

---

## 8. Artifacts inventory ($0 design-tier)

- `DESIGN_A.md` (this file) — closed-form design + GOAL-legitimacy gate
- `blue_falsifier_intra_anchor.py` — sympy/Boolean B-INTRA-1..5 closed
- `variation_generator.py` — sketch (no execution, no corpus, AST stub
  showing the 4 axis tables; full implementation gated on small-pilot
  go/no-go)
- `verdict_result.json` — sidecar verdict status (5/5 🔵 if blue battery
  passes; NOTE empirical carve-out)

No central file mutation in this cycle (state/, AGENTS.tape
n_hexad_progress, HEXAD/README.md recent landing, HEXAD/CHAT/PLAN.md,
archive/PHILOSOPHY.tape §verdict_carving_intra_anchor_diversity_s23 = at
orchestrator commit only).
