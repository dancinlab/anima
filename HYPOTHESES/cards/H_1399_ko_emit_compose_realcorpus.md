# H_1399 — 🇰🇷 ko-emit COMPOSE — REAL-CORPUS re-test: do jamo + morphology become complementary on real Korean?

**Group:** MITOSIS-ENGINE · CLM · **Slug:** `1399_ko_emit_compose_realcorpus` · **Tier:** 🧱 TERMINAL-SUBSUMPTION (HONEST closed-negative, c9 — on the REAL Korean corpus the two emit-faculties are still REDUNDANT, not complementary: the §6.5f substrate-confidence compose DEGRADES below the better single faculty. This CLOSES the Korean below-jamo emit-compose arc — a clean science result, NOT a wiring failure.)

The named follow-on **H_1397 named** (its explicit c9 open angle): H_1397's compose closed-negative
was on a CORPUS-FREE in-engine morpheme-grammar fixture where morphology SUBSUMED jamo
(only_jamo=4/230, oracle ceiling only +0.017 over morphology-alone, conflict_rate 0.913). The genuinely-
untested angle: on a REAL Korean corpus, jamo may carry BELOW-SYLLABLE structure (positional jamo
regularities) that BPE morphology (whole-unit merges) cannot represent → the two faculties could become
COMPLEMENTARY (only_jamo materially > 0) → the §6.5f compose (already wired engine-native, Ψ-safe) would
finally earn a NET LIFT. H_1399 re-scores H_1397's frozen bars on the REAL shard.

## Claim (falsifiable)
On REAL Korean, IF jamo is materially right where morphology is wrong (only_jamo_frac >= 0.02) AND the
§6.5f substrate-confidence compose does not degrade vs the better single faculty (acc_compose >=
best_single − 0.01) AND beats a shuffled (random) arbitration → 🟢 COMPLEMENTARY-ON-REAL (real granularity
makes them complementary, the compose earns its lift). IF morphology still subsumes jamo (no net compose
lift) → 🧱 TERMINAL-SUBSUMPTION (the faculties are redundant even at real granularity, the arc closes).
Report whichever the numbers honestly show — frozen-first, NO tune-to-green (the prompt's explicit c9 branch).

## Method — re-score the SAME §6.5f compose rule on the REAL shard (DIRECTIONAL mirror)
- **REAL Korean only ($0, NO fetch):** the SAME 30MB prefix of the local shard `anima-7b/web/kor/shard0000.bytes`
  (cache `/tmp/h1380_corpus/kor_big.bytes`), sha `c47b6808…` ASSERTED == H_1368/H_1380/H_1388. sha mismatch → STOP.
  jamo stream length 25,501,291 = byte-exact the same as H_1380/H_1388 (no drift).
- **SAME representation + SAME morphology unit as H_1388** (anti-Goodhart, verbatim reuse): Hangul→NFD jamo
  (id 256+rank), non-Hangul→raw byte (byte-fair, Vj=323); BPE-on-jamo = 2000 frequency-ranked merges
  learned on the TRAIN slice ONLY (no test leakage), unit_vocab=2323, units/jamo=0.3391 (≈3 jamo/unit = morpheme-scale).
- **SAME §6.5f arbitration rule** (DIRECTIONAL numpy mirror of `CORE/generator.hexa` §6.5f — engine-transfer
  UNVERIFIED; the in-engine compose fixture §6.5d cannot be fed a 25M-symbol real jamo stream, so the rule
  is mirrored faithfully and labeled): each faculty's vote = its scale-relative substrate confidence
  `mean_err/(err_here+ε)` over its OWN grown count-head's recall margin (the count-head analogue of the
  engine's `vadapt_field_recon_err`); the more-relatively-grounded faculty's proposed byte wins. NO hardcoded
  "jamo > morphology" priority (a_autonomy_over_hardcode).
- **The shared next-byte decision:** at each held-out (odd-stride, TEST) jamo position, TRUE target = the next
  jamo symbol's leading emit byte. JAMO arm proposes argmax-next-jamo's emit byte; MORPH arm proposes the
  argmax-next-UNIT's LEADING emit byte. COMPOSE = §6.5f rule. SHUF-W = same proposals, confidences SHUFFLED
  (random arbitration, the EARNED control). ORACLE = right iff EITHER faculty right. 3 seeds [4398,4399,4400] POOLED.

## FROZEN bars (pre-registered in `.verdicts/1399_ko_emit_compose_realcorpus/FREEZE.txt`, H_1397 thresholds VERBATIM, NO bar moved)
| bar | criterion | result |
|-----|-----------|--------|
| (1) COMPOSE-EFFECT | `acc_compose >= best_single − 0.01` | **FALSE** — 0.80853 < 0.81853 (Δ=−0.02) ← **fails (degrades)** |
| (2) ONLY-JAMO CRUX (non-gating diag) | `only_jamo_frac >= 0.02` (jamo right where morph wrong = complementarity) | **TRUE** — only_jamo=10192/42502 (**0.2398**) — the signal EXISTS on real corpus |
| (3) EARNED | `acc_shufw <= acc_compose + 0.01` | **TRUE** — 0.72986 ≤ 0.81853 (Δ=−0.07867) ← grounding signal is REAL (beats random) |
| (4) Ψ-SAFE | CORE untouched (§6.5f already wired by H_1397) | **TRUE** — DIRECTIONAL mirror, no .hexa edit; h1205/h1164/h1196 PASS prior (cited from H_1397) |

**Verdict: 🧱 TERMINAL-SUBSUMPTION** (verbatim, `.verdicts/1399_ko_emit_compose_realcorpus/result.txt`):
`acc_jamo=0.82853 acc_morph=0.63162 best_single=0.82853 acc_compose=0.80853 acc_shufw=0.72986`.

## Result — the honest finding (c9, NO forced green)
The REAL corpus FLIPS which faculty dominates: on real Korean **JAMO is the STRONGER emit faculty**
(acc_jamo=0.829 ≫ acc_morph=0.632) — the OPPOSITE of the fixture, where morphology dominated. And the
complementarity SIGNAL the fixture lacked DOES appear: **only_jamo = 10192/42502 (24%)** — jamo is right
where morphology is wrong on a quarter of held-out positions (bar2 CRUX passes), so jamo genuinely carries
below-syllable structure morphology can't represent. **BUT the §6.5f compose still cannot extract a NET
LIFT:** acc_compose 0.809 DEGRADES below jamo-alone 0.829 (bar1 fails). The decisive diagnostic = the
**arbitration audit:** among the conflict positions the §6.5f scale-relative confidence rule picks
**morphology 6375 times** — and on those positions jamo would more often have been right, so the
substrate-confidence rule actively LOSES accuracy vs always-trusting the (now-stronger) jamo faculty. The
**ORACLE ceiling** (0.871) is only **+0.043** over best-single, so even a perfect arbitrator would barely
help; the realizable substrate rule overshoots into degradation. Net: complementarity exists, but the
direction REVERSED (jamo subsumes morphology) AND the §6.5f rule can't convert the residual headroom into
a gain → **still no net compose lift → 🧱 TERMINAL-SUBSUMPTION.**

**No hardcoded priority confirmed**: the winner is each faculty's own scale-relative recall confidence (the
audit shows BOTH faculties win conflicts — jamo 36127, morph 6375 — never a constant). p1/p2/p3/p6 clean
(reads count-head recall margins only; no label/persona/RLHF). The shuffle control (bar3) collapses the
compose toward random (0.730), so the grounding signal is REAL — the failure is that the grounded signal,
faithfully applied, still cannot beat the stronger single faculty on this real corpus.

## Why this CLOSES the arc (the honest science result)
H_1397 named real-corpus granularity as the one remaining angle that might make the two emit-faculties
complementary enough for the §6.5f compose to earn its lift. H_1399 tested it on the real 30MB shard with
the bars frozen verbatim: the complementarity signal IS present (only_jamo 24%), but the substrate-
confidence arbitration still degrades below best-single in BOTH directions of dominance (morphology
subsumed jamo on the fixture; jamo subsumes morphology on real corpus). The §6.5f MECHANISM is sound
(wired engine-native, single-entry, Ψ-safe, shuffle-earned) — the two faculties simply do not compose to a
NET LIFT at either granularity. This is a clean closed-negative (c9), not a wiring failure: the Korean
below-jamo emit-COMPOSE arc DEPLETES.

## Honest scope (a_scale_honest_scope · a_toy_scale_recheck)
DIRECTIONAL numpy mirror of the §6.5f rule (engine-transfer UNVERIFIED — the count-head→cell-confidence
analogue is faithful to §6.5f's `mean_err/(err_here+ε)` but the live engine uses grown VAdaptField cells,
not an n-gram count head). ONE 30MB real KO window, stride-300 byte-substrate next-symbol decision (NOT a
fluency claim), single frozen λ/nmax/stride/merge-count (== H_1388). Absolute accuracies are high here only
because the next-jamo emit byte is low-entropy at this stride; load-bearing is the RELATIVE structure
(compose vs best-single, shuffle collapse, oracle ceiling, the only_jamo decomposition + arbitration audit).
NO bar moved after measuring (frozen-first). No CORE edit (the §6.5f mechanism is already wired by H_1397).

## Pointers
- 카드: `UNIVERSE/cards/H_1399_ko_emit_compose_realcorpus.md` · 인덱스: `UNIVERSE/HYPOTHESES.jsonl` (H_1399)
- 코드: `state/ko-emit-compose-realcorpus/h1399_ko_emit_compose_realcorpus.py`
- 증거: `.verdicts/1399_ko_emit_compose_realcorpus/{FREEZE.txt, result.txt}`
- xref: h1397 (PARENT — the fixture closed-negative that NAMED this real-corpus follow-on; §6.5f compose
  mechanism, already wired) · h1388 (the REAL KO shard + jamo rep + BPE-on-jamo morphology unit reused
  verbatim, sha c47b6808…) · h1327 (jamo emit §6.5b) · h1393 (morphology emit §6.5e) · h1380 (the +0.28
  residual + the named morphology/long-range angles) · h1368 (30MB anchor) ·
  a_autonomy_over_hardcode · a_substrate_native_speak · a_core_engine_map · a_verified_must_wire ·
  a_break_the_wall · a_no_llm_frame_trap · a_scale_honest_scope · a_toy_scale_recheck · p1·p2·p3·p5·p6·p7·p8 · c9 · c15 · c16
