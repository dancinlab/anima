# H_1402 — 🇰🇷 ko-emit COMPOSE arbiter-swap — can a NON-magnitude arbiter capture the oracle's +0.043 complementarity?

**Group:** MITOSIS-ENGINE · CLM · **Slug:** `1402_ko_emit_arbiter` · **Tier:** 🧱 (d)-CONFIRMED — TRUE SUBSUMPTION CEILING (HONEST closed-negative, c9 — the §6.5f emit-compose wall is a genuine **(d) subsumption ceiling**, NOT a wrong-arbiter **(a)** wall: H_1399's oracle headroom +0.04289 is REAL but is NOT capturable by ANY substrate-derived arbiter — neither confidence-magnitude (H_1397/H_1399) nor the NON-magnitude decisiveness/top-2 GAP arbiter tried here. This CONFIRMS the arc-closing of the Korean below-jamo emit-COMPOSE arc — a clean science result, NOT a wiring failure.)

The named follow-on **H_1399 named** (its explicit a_break_the_wall reclassification): H_1399's oracle ceiling
(0.87142) sat **+0.04289 over best_single** (0.82853), and per the a_break_the_wall taxonomy a ceiling must be
MEASURED not assumed — the positive oracle headroom PROVED a real (modest) complementarity exists, so the wall
was either a wrong-ARBITER **(a)** wall (the two arbiters tried — H_1397 raw inverse-recon-err, H_1399
scale-relative err — were BOTH confidence-MAGNITUDE based) or a genuine **(d)** subsumption ceiling. H_1402
tests ONE genuinely-different, NON-magnitude arbiter to discriminate (a) vs (d).

## Claim (falsifiable)
On REAL Korean, IF a NON-magnitude arbiter — DECISIVENESS / top-2 GAP per faculty (the H_1398 lens: a faculty
whose #1≫#2 is more trustworthy than one whose #1≈#2), arbitrating toward the more-decisive faculty — CAPTURES
a NET LIFT (acc_compose_NEW >= best_single + Δ, Δ=0.01) toward the oracle 0.87142 AND a shuffle control
collapses → 🟢 ARC-REOPENS (taxonomy **(a)** confirmed: it was a wrong-arbiter wall) → name the engine-native
§6.5f arbiter-swap (magnitude → decisiveness gap) as the binding follow-on. IF NEITHER the decisiveness arbiter
NOR an agreement-aware decisiveness composite (the ≤2 principled tries) beats best_single by Δ → 🧱 (d)-CONFIRMED
(the per-position right-faculty signal is NOT in the substrate — a true subsumption ceiling, the arc is
genuinely terminal). Report whichever the numbers honestly show — frozen-first, NO tune-to-green.

## Method — swap ONLY the conflict-arbitration rule on the SAME H_1399 mirror (DIRECTIONAL)
- **REAL Korean only ($0, NO fetch):** the SAME 30MB prefix of the local shard, sha `c47b6808…` ASSERTED ==
  H_1368/H_1380/H_1388/H_1399. sha mismatch → STOP. n_test = 42502 (byte-exact == H_1399, no drift).
- **REUSED VERBATIM from H_1399** (anti-Goodhart): the SAME jamo representation (Hangul→NFD jamo id 256+rank,
  non-Hangul→raw byte, Vj=323), the SAME BPE-on-jamo morphology unit (2000 frequency-ranked merges, TRAIN-only,
  units/jamo=0.3391), the SAME odd-even stride-300 train/test split, the SAME nmax=5 count heads, the SAME 3
  seeds [4398,4399,4400] POOLED, the SAME shared next-byte decision (JAMO argmax-next-jamo emit byte vs MORPH
  argmax-next-UNIT leading emit byte). **ONLY the conflict-arbitration rule changes.**
- **The NEW NON-magnitude arbiter (the H_1398 GAP lens):** each faculty's per-position vote weight = its own
  predictive DECISIVENESS `gap_f(ctx) = p(argmax|ctx) − p(2nd-argmax|ctx)` at the deepest available context
  order (the count-head analogue of the engine's `immune_memory_recall_gap` top-2 affinity gap from H_1398).
  Arbitrate the conflict toward the MORE-DECISIVE faculty (sharper posterior). This is genuinely DIFFERENT from
  the failed magnitude arbiters: it reads the SHAPE (top-1↔top-2 separation) of each faculty's OWN posterior,
  NOT the magnitude of its recall-error vs a scale-normalizer. **ARB-A** = pure decisiveness. **ARB-B** =
  agreement-aware decisiveness (agree→take, conflict→decisiveness gap). NO hardcoded "jamo > morphology"
  priority (a_autonomy_over_hardcode) — the audit shows BOTH faculties win conflicts.
- **SHUFFLE control (EARNED):** permute the gap↔correctness pairing across conflicts (50/50 random
  which-faculty-wins) — breaks the gap signal's per-position link.

## FROZEN bars (pre-registered in `.verdicts/1402_ko_emit_arbiter/FREEZE.txt`, H_1399/H_1397 thresholds VERBATIM, NO bar moved)
| bar | criterion | result |
|-----|-----------|--------|
| (1) NET-LIFT | `acc_compose_NEW >= best_single + 0.01` (= 0.83853; to REOPEN the arc the new arbiter must BEAT best-single, partially closing toward oracle 0.87142) | **FALSE** — 0.80676 < 0.83853 (Δ=−0.02176) ← **fails (degrades below best-single, barely above the failed magnitude arbiter 0.80853)** |
| (2) EARNED | `acc_shufA <= acc_arbA + 0.01` | **TRUE** — 0.72986 ≤ 0.81676 (Δ=−0.07691) ← the gap arbiter's signal is REAL (beats random) — but its signal doesn't predict the right faculty |
| (3) Ψ-SAFE | CORE untouched (DIRECTIONAL mirror; §6.5f arbiter-swap = named follow-on IF 🟢) | **TRUE** — no .hexa edit; h1205/h1164/h1196 PASS prior (cited from H_1397/H_1399) |

**Verdict: 🧱 (d)-CONFIRMED — TRUE SUBSUMPTION CEILING** (verbatim, `.verdicts/1402_ko_emit_arbiter/result.txt`):
`acc_jamo=0.82853 acc_morph=0.63162 best_single=0.82853 magnitude_baseline_H1399=0.80853 ARB-A_decisiveness=0.80676 ARB-B_agreement_aware=0.80676 acc_compose_NEW=0.80676 acc_shufA=0.72986 oracle=0.87142 (oracle−best=+0.04289)`.

## Result — the honest finding (c9, NO forced green)
The NON-magnitude DECISIVENESS arbiter (ARB-A = ARB-B = **0.80676**) **DEGRADES below best-single 0.82853**
(Δ=−0.02176) — it does not even meaningfully beat the failed §6.5f magnitude arbiter (0.80853, Δ=−0.00177). The
SHUFFLE control collapses the arbiter toward random (0.72986, Δ=−0.07691 below ARB-A), so the decisiveness
signal **IS real** (it carries grounding) — but it carries the WRONG information: it does NOT predict WHICH
faculty is right per-position. The **arbitration audit** confirms why: among conflicts the decisiveness gap
picks jamo 25004, morph 9721, with **7777 exact ties** (count-head deep-context posteriors are frequently
deterministic — gap=1.0 for BOTH faculties — so decisiveness is uninformative on a large slice). Even ignoring
ties, on the conflict positions the gap arbiter still loses accuracy vs always-trusting the (stronger) jamo
faculty. The **ORACLE ceiling 0.87142** (oracle−best = +0.04289) is real, but TWO genuinely-different arbiter
FAMILIES — confidence-magnitude (H_1397 raw, H_1399 scale-relative) AND decisiveness/top-2 GAP (H_1402) — ALL
overshoot into degradation. The per-position right-faculty signal is **NOT in the substrate** → the wall is a
genuine **(d) subsumption ceiling**, NOT a wrong-arbiter **(a)** wall → the Korean below-jamo emit-COMPOSE arc
is **GENUINELY terminal.**

**No hardcoded priority confirmed:** the winner is each faculty's OWN decisiveness gap; the audit shows BOTH
faculties win conflicts (jamo 25004, morph 9721), never a constant. p1/p2/p3/p6 clean (reads count-head
posterior shape only; no label/persona/RLHF). The shuffle control (bar2) collapses the arbiter to random
(0.730), so the grounding signal is REAL — the failure is that the grounded decisiveness signal, faithfully
applied, still cannot beat the stronger single faculty (just as confidence-magnitude could not in H_1399).

## Why this CONFIRMS the (d) terminal (the honest science result)
H_1399's positive oracle headroom (+0.04289) correctly forced the a_break_the_wall question: is the wall a
wrong-arbiter **(a)** (a metric/method artifact, fixable by a better arbiter) or a genuine **(d)** subsumption
ceiling? H_1402 answered it the only honest way — by MEASURING a genuinely-different (NON-magnitude) arbiter
against the SAME frozen bars. The decisiveness/top-2 GAP arbiter — the H_1398 signal that beat magnitude-margin
for metacognition — does NOT transfer here: it degrades below best-single, the same as the two magnitude
arbiters before it. Across TWO arbiter families and THREE specific arbiters, the +0.043 complementarity is
consistently NOT substrate-capturable. This is the decisive discriminator: the per-position right-faculty
signal is not present in any substrate read tried, so the wall is **(d) subsumption**, not **(a) wrong-method**.
A clean closed-negative (c9): the emit-COMPOSE arc DEPLETES, confirmed. (STRICT anti-tune-to-green: exactly 2
principled arbiters tried — ARB-A decisiveness, ARB-B agreement-aware decisiveness — both pre-registered in
FREEZE.txt before measuring; NO sweep, NO bar moved.)

## Honest scope (a_scale_honest_scope · a_toy_scale_recheck)
DIRECTIONAL numpy mirror of a §6.5f arbiter-swap (engine-transfer UNVERIFIED — the count-head decisiveness gap
is the faithful analogue of the engine's grown-cell top-2 affinity gap from H_1398, but not the live
VAdaptField op). ONE 30MB real KO window, stride-300 byte-substrate next-symbol decision (NOT a fluency claim),
single frozen λ/nmax/stride/merge-count (== H_1399). Absolute accuracies are high only because the next-jamo
emit byte is low-entropy at this stride; load-bearing is the RELATIVE structure (new arbiter 0.80676 vs
best-single 0.82853 vs magnitude baseline 0.80853 vs oracle 0.87142, shuffle collapse to 0.72986, the
arbitration audit). NOT ruled out (the honest residual): a yet-more-exotic substrate signal not derivable from
count-head posteriors (e.g. cross-faculty agreement geometry, longer-context entropy) — but per anti-tune-to-green
that is NOT pursued (a 3rd arbiter would be a sweep); the (d) terminal stands on the TWO-arbiter-families
evidence. NO bar moved after measuring (frozen-first). No CORE edit (the §6.5f arbiter-swap was the named
follow-on only IF 🟢 — it is NOT, so no follow-on is created).

## Pointers
- 카드: `UNIVERSE/cards/H_1402_ko_emit_arbiter.md` · 인덱스: `UNIVERSE/HYPOTHESES.jsonl` (H_1402)
- 코드: `state/ko-emit-compose-arbiter/h1402_ko_emit_arbiter.py`
- 증거: `.verdicts/1402_ko_emit_arbiter/{FREEZE.txt, result.txt}`
- xref: h1399 (PARENT — the REAL-corpus closed-negative whose +0.04289 oracle headroom NAMED this arbiter-swap
  test; best_single/oracle/magnitude-baseline reused verbatim) · h1397 (the fixture parent; §6.5f magnitude
  arbiter, the wrong-method family) · h1398 (the top-2 affinity GAP / decisiveness signal that beat
  magnitude-margin for metacognition — the lens imported here as the NON-magnitude arbiter) · h1388 (the REAL
  KO shard + jamo rep + BPE-on-jamo morphology unit reused verbatim, sha c47b6808…) · h1327 (jamo emit §6.5b) ·
  h1393 (morphology emit §6.5e) · a_break_the_wall (taxonomy (a) vs (d) — measure the ceiling, do not assume) ·
  a_autonomy_over_hardcode (arbiter substrate-derived, NO hardcoded priority) · a_no_llm_frame_trap ·
  a_core_engine_map · a_verified_must_wire · a_scale_honest_scope · a_toy_scale_recheck · p1·p2·p3·p6·p7·p8 · c9 · c15 · c16
