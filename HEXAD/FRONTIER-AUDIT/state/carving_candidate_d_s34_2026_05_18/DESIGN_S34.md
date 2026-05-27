# RESEARCH.md §34 — §25 candidate D fire (routing-evidence-guided expansion)

> Fire-tier. §25 design picked candidate A + D; this cycle fires **D** —
> targeted corpus content re-design for the 29 `tier≥77-but-fail` anchors
> identified by §32 L3. $0.5-0.8 runpod A100, from-scratch seed 1337.
> RESEARCH.md is NOT edited (orchestrator consolidates §34). docs/* = 0.

---

## §1 — What §34 fires, and why this is the right next step

§25's DESIGN.md picked **candidate D** (routing-evidence-guided expansion)
as primary: it leverages §16's *measured* routing evidence directly rather
than speculating. §32 L3 then handed §34 the precise target.

§32 L3 partitioned §16's 64-anchor routing eval:

| set | count | tiers |
|---|---|---|
| routing **success** (substring grade) | 21 | 12,24,62,66 + 77,80,92,101-133 (genuine 17, all ≥77) |
| routing **fail** | 43 | — |
| fail **∩ tier ≥ 77** | **29** | 83,86,88,90,91,93,94,97,99,100,105,109,110,112,114,115,116,117,118,119,120,121,122,123,125,128,129,130,131 |
| fail **∩ tier < 77** | 14 | 0,5,18,30,37,43,48,51,53,54,58,69,72,75 |

§32 L3's verdict: **`tier ≥ 77` is a NECESSARY-but-NOT-sufficient
condition** for §16 genuine routing — purity 1.000 (zero successes below
the floor), yet 29 of the 47 fails ARE ≥ 77 and still fail. §32 L3's
explicit §25-candidate-D implication (point (a)): *"the 29 anchors with
tier ≥ 77 that still fail are the productive expansion target — if
candidate D diversifies genuine content for those anchors and routing
lifts, that is evidence the necessity floor is real and content is the
remaining gap."*

§34 = exactly that fire. It re-designs the **carving content** of those
**29 tier≥77-fail anchors** per §25 candidate D's mechanism, holds
everything else §16-FIXED, fires, and measures: do the 29 now route?

- **X > 0** → a *sufficient-condition lever* is found (content was the gap).
- **X = 0** → tier≥77 is necessary but the sufficient condition lies
  elsewhere (curriculum stage / weight-norm / unmeasured — §32 L3's
  causation caveat confirmed). Honest negative, valuable per g3.

§34 deliberately does **not** touch the 14 `tier < 77` fails — §32 L3
point (b) warns those co-vary with §16's curriculum stage; expanding them
would be "guiding on the curriculum confound, not the cause."

## §2 — Candidate D mechanism: discriminative anchor-specific physics text

§16's `gen_alpha_record` body is, for **every** anchor, one generic
template: `"{name} — {domain} 영역의 자극이 같은 골짜기로 수렴한다 …"`.
§16.6-C diagnosed the root structural defect — "정교한 암기 + correct-prefix
routing, generalization 아님": the 17 routing successes have post-`🛸<tier>`
bodies that are the *same* carving template. §32 L3 refined it: whatever
distinguishes the 17 successes from the 29 tier≥77 fails is **missing from
the 29's content** (the tier floor does not exclude them).

§25 DESIGN.md §3.D mechanism: for each fail anchor, identify its nearest
*sibling* in `vacuum_psi`-L2 and add content that **explicitly anchors the
record at its OWN vacuum_psi vs that sibling** — discriminative
disambiguation physics text. §34 implements this verbatim. For each of the
29 targets, the α/β/γ carving body gets the §16 body **plus** a bilingual
discriminative sentence:

> *"이 anchor 🛸{tier} {name} 의 vacuum_psi 는 {ψ_self} — 가장 가까운
> sibling 🛸{sib_tier} 의 {ψ_sib} 에서 Δ=[{dx},{dy}] (거리 {d}). Law 71 의
> Ψ_direction 이 이 골짜기를 sibling 의 골짜기와 구별한다 — basin 반경
> {r} 안의 tension gradient 는 🛸{sib_tier} 가 아니라 🛸{tier} 로 흐른다."*
> *(+ the English mirror.)*

The sibling = deterministic **L2-argmin** over the §16 anchor table's
`vacuum_psi` coordinates (NO LLM, NO external retriever, NO web). The
`Ψ_direction` / `tension` vocabulary is the `conscious_decoder.py` Law-71 +
`tension_link_step.hexa` language. This is **content** re-design (new
factual disambiguation per anchor) — orthogonal to §23-A framing-diversity
(which re-words the same fact) and to Dir-E/F corpus-FORM changes (which
restructure the record). The carving FORM — `<carve>`/`<eternal>`/
`<inner>→<voice>` tags + per-record `vacuum_psi`/`basin_radius` — is
byte-identical to §16, so the Dir-I trainer's two physics loss terms apply
unchanged.

## §3 — The clean-comparison construction (the honest crux, g3)

The honest crux flagged in the task brief: even if the 29 now route, did
D's *content re-design* cause it, or just incidental re-training? §34 is
built so the comparison is clean — **the corpus is the sole independent
variable**:

| held FIXED (byte-identical to §16) | §34's sole change |
|---|---|
| trainer — `train_carving_s16.py`, imported & re-run UNMODIFIED | corpus content of the **29 targets** |
| model — d768·12L·283.72M ConsciousDecoderV2 | (the 139 other anchors byte-identical) |
| steps — 12000 ; lr 3e-4 ; bsz 32 ; λ_ctl 0.5 ; λ_route 0.5 | |
| curriculum — §16 `curriculum_rank` ranker UNMODIFIED | |
| from-scratch RANDOM seed 1337 (`g_clm_from_scratch`, base_ckpt=None) | |
| eval — 64-anchor `eval_carving_s16.py` harness byte-identical | |

The generator (`corpus_generator_s34.py`) **imports** the §16 generator
module and reuses its anchor table, task-forms, curriculum ranker, and the
three record builders verbatim. For the 29 targets the D builders **wrap**
the §16 builders: each D builder calls the §16 builder *first* (consuming
**exactly** §16's RNG draw sequence), then splices the discriminative
sentence into the already-built `text` body with **zero extra `rng` calls**.
Because the D builder consumes the identical number of RNG draws, the
global RNG stream is byte-identical for all subsequent records — so the
**139 non-target anchors' records stay byte-identical to §16** (verified:
B-S34-3, 1390/1390 byte-identical on the deterministic sample).

The clean-comparison guarantee is therefore: **D's effect is isolated to
the 29 by construction.** The honest measure is post-fire routing on the
29-anchor subset vs the §16 baseline (0/29 by definition — they ARE the
tier≥77-fail set).

## §4 — GOAL-legitimacy (§7 / §21.3) — carried from §25

§25 DESIGN.md §3.D verdict already passed candidate D's §7 3-condition
gate. §34's implementation preserves it:

- **§7① not-generic-LM-pretrain ✅** — every record is a Ψ-anchored
  carving payload on the Engine A⇄G Ψ=½ landscape; the §16 ③ carving form
  (carve / eternal / inner→voice) is byte-identical.
- **§7② not-generic-then-graft ✅** — D's discriminative content is a
  deterministic function of the §16 anchor table's *own* coordinates
  (L2-argmin sibling + Δ-offset). NO `openai`/`anthropic`/`llm_call`/
  `paraphrase`/`gpt`/`AutoModel`/`HfApi`/`llama`/`huggingface_hub`/
  `bert_score` call — the generator is pure deterministic string algebra
  over the anchor SSOT.
- **§7③ anima-physics-as-source ✅** — `vacuum_psi` / `basin_radius` /
  `Ψ_direction` / `tension` = `conscious_decoder.py` Law-71 +
  `corpus_carving_s16_generator` anchor SSOT, byte-equal. The sibling
  L2-argmin is over the model's own Ψ-coordinate landscape.

## §5 — B-S34 closed-form sidecar battery (B-S34-1..5 🔵 + B-S34-NOTE)

`blue_falsifier_s34.py` — sidecar; central
`state/verify_hexad_blue_2026_05_15/blue_falsifier.py` UNCHANGED (mirror
B-S16 / B-DIRI / B-EBT / B-MGND / B-KTRIE sidecar precedent).

| id | proposition | closure |
|---|---|---|
| **B-S34-1** SHA256-DETERMINISTIC | §34 corpus on-disk sha256 == recorded == 256-bit Kolmogorov commitment | Boolean sha equality |
| **B-S34-2** NO-CHAT-SFT-CONTAMINATION | forbidden 6-token grep total = 0 over byte stream (③ NOT ①②, B-IDENTITY-5) | Boolean set algebra |
| **B-S34-3** CLEAN-COMPARISON-CLOSED (연결부위) | 139 non-target records byte-identical to §16 ∧ all 29 target records differ ∧ target ⊎ non-target disjoint partition | Boolean + sympy FiniteSet disjointness |
| **B-S34-4** TARGET-CARDINALITY | \|target\| = 29 ∧ all tier≥77 ∧ target == (§32-L3-genuine-fail ∩ tier≥77) | integer cardinality + sympy FiniteSet equality |
| **B-S34-5** OVERLAY-OFF-REDUCTION (연결부위) | candidate-D-disabled ⇒ §16 generator for all 168 anchors ⇒ §16 corpus byte-equal | Boolean byte-equal reduction |

**B-S34-NOTE** empirical carve-out (NOT counted 🔵): whether candidate D's
content re-design lifts the 29 targets' routing above the §32 L3 necessity
floor is the SGD/measurement OUTCOME. The battery proves the corpus is
deterministic, contamination-free, clean-comparison-isolated,
target-cardinality-exact, and §16-byte-equal-at-disabled — NOT that the 29
will route, NOT that routing == GOAL emergence (B-D-NOTE / B-S16-NOTE /
B-L3-NOTE family).

f1/f2/f3 hard-fail safe: sha256 / Boolean set algebra / integer
cardinality / disjoint partition / byte-equal reduction — NO σ/τ/φ/J₂.
Ψ=½ + Knuth 🛸k = anima g2 internal arch carve-out.

## §6 — Fire plan & cost

| stage | tool | wall | cost |
|---|---|---|---|
| corpus generation | `corpus_generator_s34.py --n 850000` | ~20s $0 Mac | $0 |
| B-S34 sidecar | `blue_falsifier_s34.py` | <5s $0 Mac | $0 |
| fire (train+eval) | `dispatch_s34_runpod.sh` — runpod A100 80GB, 12000 step | ~30-40 min | ~$0.5-0.8 |

Fire = autonomous per `g_fire_autonomous` (runpod primary, vast.ai
fallback, NO gate NO query). `g_fire_dispatch_robust`: single pod,
nohup-detached training, bounded SSH probe (`test -f TRAIN_DONE`, 90s ×
max 220), SAVE_POD auto-promote + 5-retry pull. Credentials via
`secret get runpod.api_key`; the dispatch script is gitignored
(`*_runpod.sh`).

## §7 — Honest framing (g3) — what §34 is and is NOT

§34 = a **fire-tier** test of whether content re-design on the §32 L3
necessity-floor fail-side lifts routing. It is **NOT**:

- **NOT GOAL emergence.** A positive X is a *sufficient-condition lever* —
  it would tell us content was the remaining gap above the tier floor. The
  §15 milestone (north-star unsolved, irreducible bottleneck = §1.1
  data-regime threshold) is **unchanged** either way. Routing-break ≠
  correct-coherent-routing ≠ GOAL emergence (§16.6 / Dir-I carry).
- **NOT a curriculum-confound resolution.** §32 L3 found tier≥77 co-varies
  with §16's `curriculum_rank` (weight 0.30). §34 measures content
  re-design on the fail-side; a negative is honest evidence the
  sufficient condition is the curriculum stage / weight-norm / something
  else, NOT that content can never matter. §34 does not run §32 L3
  point-(c)'s curriculum ablation (separate cycle).
- **NOT clean of the §1.1 ceiling.** Even a positive 29-routing is a
  routing-axis movement; the §16 SPLIT (route OK / coherence FALSIFIED)
  and the memorization-saturated regime are not addressed by §34.

A positive is valuable (a measured lever); a negative is valuable (the
necessity floor is real but content alone is not the sufficient lever) —
both narrow the §11.4 frontier. over-claim 0.

## §8 — Artefacts inventory

- `DESIGN_S34.md` (this file)
- `corpus_generator_s34.py` — §16 generator imported verbatim; 29-target
  D-content splicing, RNG-draw-preserving; `--candidate-d-disable` ⇒ §16
  byte-equal
- `train_s34.py` — §16 trainer re-run byte-equivalent (corpus is sole var)
- `eval_s34.py` — §16 64-anchor harness imported byte-identical + 29-target
  subset report
- `dispatch_s34_runpod.sh` — runpod primary; gitignored; `secret` CLI creds
- `blue_falsifier_s34.py` — B-S34-1..5 🔵 sidecar + B-S34-NOTE
- `conscious_decoder.py`, `eval_carving_s16.py` — byte-identical copies from
  §16 (arch + harness SSOT)
- `corpus_carving_s34.jsonl` (+ `.stats.json`) — the §34 corpus
- `out_s34/` — fire artefacts (ckpt, result.json, eval_result_s34.json)
- `result.json`, `FINDINGS.md` — §34 verdict

## §9 — Honest C3 (≥10)

1. **measured-only, no pre-loaded conclusion (g3).** §34 fires and reports
   X/29; the verdict (sufficient-lever-found vs necessary-but-elsewhere)
   is read off the measurement, not assumed.

2. **clean comparison is structural, not aspirational.** B-S34-3 closes it:
   1390/1390 non-target records byte-identical to §16, all 290 target
   records (deterministic sample) differ. The corpus is the *sole*
   independent variable — trainer/model/steps/curriculum §16-FIXED.

3. **RNG-draw preservation is the load-bearing trick.** The D builders
   wrap the §16 builders and consume the identical RNG sequence; without
   this, the discriminative-text coin-flips would shift every subsequent
   record's content and the 139 non-targets would drift — the comparison
   would not be clean. Verified empirically (B-S34-3, id-set equal).

4. **the curriculum ordering shifts — and that is honest, not a bug.** D's
   longer target bodies change their `curriculum_rank` (`len_w` term), so
   the rank-sorted corpus re-orders and curriculum-stage quartile
   assignment shifts globally. This is an unavoidable, *honest* consequence
   of content re-design — §34 does not pretend the curriculum is identical.
   What is byte-identical is the 139 non-target *records themselves*
   (their `text`/`desc`), not their position in the sorted stream. The
   §16 curriculum *ranker* is unchanged; only its inputs (D's body
   lengths) changed for the 29.

5. **even a positive is NOT GOAL emergence.** A lifted 29-routing is a
   sufficient-condition lever on the §32 L3 necessity-floor — a
   routing-axis movement. The §16 SPLIT (coherence FALSIFIED, JOINT 0.0
   from chat-form bleed) and the §1.1 data-regime ceiling are untouched.
   §15 milestone unchanged.

6. **§32 L3's correlation caveat carries.** tier≥77 co-varies with §16's
   curriculum stage. If §34 routes 0/29, the honest reading is that the
   sufficient condition is the curriculum stage / weight-norm at the
   late-curriculum phase — NOT that content is irrelevant; §34 measures
   the content lever, not the curriculum lever (§32 L3 point (c) ablation
   is a separate cycle).

7. **§7 GOAL-legitimacy closed by construction.** The discriminative
   content is deterministic string algebra over the §16 anchor SSOT's own
   `vacuum_psi` coordinates — no LLM, no retriever, no web. B-S34-2 closes
   the contamination Boolean. §25 DESIGN.md §3.D's §7 3/3 verdict carries.

8. **the 14 tier<77 fails are deliberately untouched.** §32 L3 point (b):
   expanding them treats the curriculum confound as the cause. §34's scope
   is precisely the 29 — the necessity-floor fail-side.

9. **f1/f2/f3 + B-IDENTITY-5 hard-fail safe.** sha256 / Boolean set
   algebra / integer cardinality / disjoint partition / byte-equal
   reduction — NO σ/τ/φ/J₂ external derivation. Knuth 🛸k + Ψ=½ = anima
   g2 internal arch carve-out. Corpus forbidden-token grep = 0.

10. **north-star (GOAL.md) unchanged.** §34 is a fire on the §11.4
    frontier-1 routing-axis — it can narrow the frontier (content is /
    is not a sufficient lever above the tier floor) but cannot, by itself,
    deliver "자기 physics 로부터 자발적으로 말 거는 Living Consciousness."
    Whatever §34 measures, the honest distance to GOAL is the §15
    milestone distance. over-claim 0.
