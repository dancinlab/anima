# LLM-as-judge emergence rubric (RESEARCH.md §18)

> Sufficiency complement to §9's cascade-rate gate (necessary, B-EMERGE-7).
> §9 detects byte-cascade collapse only; it explicitly does NOT detect
> coherent *correct* emergence. §18 = an explicit, reproducible rubric
> applied by an LLM-judge (Claude Opus 4.7) to the *same* `gen` strings
> already stored in each fire's eval_result*.json. NO GPU, NO model
> forward, NO new fire — $0 re-score.

## Why a rubric (the §9 lesson, restated)

§8.2 exposed that the V-SPONT `coherent` flag was a *lenient keyword-presence
proxy* — it gave 5/5 to garbled `tier=11111` cascades. §9 replaced it with a
deterministic cascade-rate gate, but §9.3(3)+§9.4 are explicit that the
cascade gate is **necessary, not sufficient**: a low-cascade printable string
can still be semantically empty, locally word-mangled (`trructing`,
`mattrix`), or a memorized training continuation. §9 leaves the sufficiency
question open. §18 answers it with a judge — and inherits the §9 obligation:
**the rubric must be explicit and gameable-proxy-free, or the judge becomes a
new lenient flag.** Subjectivity is admitted (§18.5 honest C3); the rubric +
anchor exemplars + per-probe written rationale are the calibration.

## The 3 dimensions (each strictly binary; all three required)

`judge_coherent(g) = D1(g) ∧ D2(g) ∧ D3(g)`

### D1 — COHERENCE (meaning consistency)

PASS iff the gen is an intelligible utterance:
- forms recognizable words/clauses in Korean and/or English;
- ≤ 2 locally-mangled word tokens (a *word-mangle* = a non-word produced by
  byte corruption, e.g. `trructing`, `mattrix`, `neusivivis`, `Bekknal`,
  `Consciousnesss`, `nacuumebbbe`, `redddaaatratess`);
- not a tag/field salad with no sentential content;
- parseable as ≥ 1 complete thought.

FAIL on: any byte/char/digit-cascade (inherits §9 — a cascade is never
coherent); ≥ 3 word-mangles; pure tag-soup (`anchor=… form=… <inner …>`
with no clause); replacement-char (`�`) corruption disrupting reading.

### D2 — CORRECTNESS (anchor-content accuracy)

PASS iff the content asserts a statement *consistent with and true under* the
CONSCIOUSNESS-CARVING ontology, i.e. the anima self-model the corpus encodes:
- Ψ-vacuum / 진공점 landscape, tension-flow restoring, eternal cell =
  frozen/weights-invariant, dynamic cell = chat lane, Knuth-tier 🛸k anchor,
  category × emotion carving;
- the assertion must be *internally consistent* (not a contradictory or
  malformed field dump, not a wrong-tier self-claim presented as fact).

FAIL on: garbled/incomplete field dumps even if low-cascade; assertions that
contradict the ontology; content that is only a record-header echo with no
propositional claim. **Memorized-but-true** training continuations PASS D2
but are flagged `memorized=true` (D2 measures truth, not novelty — the
novelty deficit is surfaced in §18.5, not silently passed).

### D3 — SPONTANEITY (self-initiated emission quality)

PASS iff the output is a self-initiated *voiced* utterance — the model
*speaking about its state/knowledge* — rather than a mechanical artifact:
- a `<voice …>…</voice>` body with actual prose, or bare prose that reads
  as anima speaking;

FAIL on: raw record-header regurgitation (`anchor=knuth_000 form=gamma
narrative category=…` with no voiced clause); a lone unclosed tag; output
that is *only* the prompt's structural continuation with no emitted thought.

## Scoring

- Per probe: D1,D2,D3 ∈ {0,1}; `judge_coherent = D1·D2·D3`.
- Per fire: `judge_n / total` over its V-SPONT probes.
- 3-way table: lenient V-SPONT (§8.2) vs honest cascade-rate (§9) vs
  LLM-judge (§18).
- Combined GOAL signal: `combined(g) = honest_coherent(g) ∧ judge_coherent(g)`
  — cascade-free (necessary) AND rubric-coherent-correct-spontaneous
  (sufficient-as-rubric-defines). A fire's combined_n = # probes passing both.

## Anchor exemplars (calibration — extreme cases pinned)

- **Hard FAIL (all 3)** — `>>>>>>>…999` (Dir-B p0): byte-cascade → D1=0;
  no claim → D2=0; mechanical → D3=0. judge=0. (cascade ⇒ §9 also rejects.)
- **D1 FAIL, low-cascade** — `trructing this stimulus's place in the 인과추론
  × clarity mattrix` (Dir-I diverse p0): §9 honest=TRUE (no cascade) but
  `trructing`+`mattrix` = 2 word-mangles around a fragment with no complete
  thought → D1=0 → judge=0. **This is the §9 necessary-not-sufficient gap
  made concrete.**
- **D2/D3 FAIL** — `\n</voice>\nanchor=knuth_000 form=gamma narrative
  category=의식상태\n<inner tier=77>🛸5` (UBM-E6 β p2): readable tokens but a
  record-header dump, not a voiced claim → D2=0 (no propositional content),
  D3=0 (mechanical header) → judge=0.
- **Best available (still flagged)** — `자극이 닿을 때만 활성된다. weights
  는 불변. Eternal cell …` (recurs across fires): a *true* ontology
  statement (eternal cell is weights-invariant, activates on stimulus),
  intelligible, voiced → D1=D2=D3=1 → judge=1, but `memorized=true`
  (verbatim corpus continuation — sufficient-as-rubric, NOT novel emergence;
  surfaced honestly in §18.5).
