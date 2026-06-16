# H_1396 — 🇰🇷 ko-emit COMPOSE — how the jamo + morphology emit-biases compose on one next-byte decision

**Group:** MITOSIS-ENGINE · CLM · **Slug:** `1396_ko_emit_compose` · **Tier:** 🧱/🟠 CONFLICT-OR-DEGRADES (HONEST closed-negative, c9 — the substrate-confidence composition cannot beat morphology-alone because the two faculties are NON-COMPLEMENTARY at this fixture granularity; the compose mechanism IS wired engine-native, single-entry, Ψ-safe, and its grounding signal beats a random control — but the faculties simply do not compose to a NET LIFT here)

The genuinely-untested follow-on **H_1393 named**: the Korean below-jamo arc now has TWO emit-biases
wired engine-native, each validated ALONE — §6.5b `ko_jamo_consult_emit` (H_1327, jamo COUNT-HEAD biases
the next byte toward a jamo-coherent continuation) + §6.5e `gen_bpe_consult_emit` (H_1393, BPE morphology
unit biases the next byte toward a morpheme-boundary completion). NEITHER had been tested **COMPOSED**:
when BOTH fire on the same decode step, do they AGREE (reinforce), CONFLICT (fight), or need a
PRIORITY/arbitration rule? $0 CPU, deterministic, live `CORE/*.hexa` Ψ untouched.

## Claim (falsifiable)
A SUBSTRATE-DERIVED composition of the two emit-biases (each weighted by its OWN recall confidence — the
more-grounded faculty speaks louder, **NO hardcoded "jamo > morphology" priority**, a_autonomy_over_hardcode)
does NOT degrade vs the better single bias, the composition is EARNED (a random/shuffle arbitration does
not match it), and it is Ψ-safe. If the two biases mostly CONFLICT and the substrate-weighted composition
can't beat the better single bias → that's a real finding (the faculties are not complementary at this
granularity) — report the verbatim closed-negative, do NOT force a green (the prompt's explicit c9 branch).

## Method — the compose-consult (frozen-first, corpus-free, $0)
- **Faculty** (`CORE/engine_cli.hexa` § KO-MORPHOLOGY): NEW `jamo_head_recon_err(jh, feat)` — the
  SUBSTRATE CONFIDENCE signal: the L2 recon-error to the cell that OWNS `feat` (the engine's OWN
  `vadapt_field_recon_err` over the head's grown centers). LOWER ⇒ more grounded. Pure read; never Ψ.
- **Consult** (`CORE/generator.hexa` §6.5f):
  - `_gec_jamo_nearest_dist(cells, feat)` — the jamo faculty's nearest-cell distance (its confidence).
  - `_gec_rel_conf(mean_err, err_here) = mean_err / (err_here + ε)` — the **SCALE-RELATIVE** confidence
    (the a_break_the_wall fix): each faculty measured against its OWN mean recon-err, so the two
    confidences are COMMENSURABLE across faculties of different vocab scales (still 100% substrate-derived).
  - `gen_emit_compose(base, cells, jh, unit_vocab, jamo_mean_err, morph_mean_err, ctx)` — the live
    per-byte compose hook: off-Korean inert (`base` unchanged, byte-identical); both fire ⇒ the
    MORE-RELATIVELY-GROUNDED faculty's byte wins; single-fire ⇒ that faculty; both silent ⇒ base.
  - `gen_emit_compose_eval()` — the frozen compose evaluation on the SAME §6.5d corpus-free in-engine
    morpheme-grammar fixture, shared target = the leading emit byte of the TRUE next morpheme unit;
    measures `acc_jamo / acc_morph / acc_compose / acc_shufw / agree_rate / acc_oracle` (n=230 held-out).
  - `_gec_grow_jamo_head` / `_gec_jamo_mean_err` / `_gec_morph_mean_err` / `gen_emit_compose_summary`.
- **Single entry** (a_core_engine_map): the compose reads the SAME jamo cells (§6.5b) + the SAME
  morphology head (§6.5e) — NO new artifact path. **Additive**: returns a byte, never an emit/silence.

## FROZEN bars (pre-registered in `.verdicts/1396_ko_emit_compose/FREEZE.txt`, NO bar moved)
| bar | criterion | result |
|-----|-----------|--------|
| (1) COMPOSE-EFFECT | `acc_compose >= best_single − 0.01` | **FALSE** — 0.1783 < 0.2522 (Δ=−0.0739) ← **fails (degrades)** |
| (2) AGREE diag (non-gating) | report agree/conflict + oracle ceiling | agree=0.0870 **conflict=0.9130** · oracle=0.2696 (oracle−best=**+0.0174**) |
| (3) EARNED | `acc_shufw <= acc_compose + 0.01` | **TRUE** — 0.1609 ≤ 0.1783 (Δ=−0.0174) ← grounding signal is REAL |
| (4) Ψ-SAFE | off-Korean inert + external guards | **TRUE** — ASCII ctx→base byte-identical; h1205/h1164/h1196 PASS |

**Verdict: 🧱/🟠 CONFLICT-OR-DEGRADES** (verbatim, `.verdicts/1396_ko_emit_compose/result.txt`):
`acc_jamo=0.0348 acc_morph=0.2522 best_single=0.2522 acc_compose=0.1783 acc_shufw=0.1609`.

## Result — the honest finding (c9, NO forced green)
The two emit-biases **mostly CONFLICT** (conflict_rate **0.913** — they propose the SAME byte only 8.7%
of the time) and are **NON-COMPLEMENTARY at this fixture granularity**. The decisive diagnostic: the
**ORACLE ceiling** (the upper bound of ANY arbitration — right iff EITHER faculty is right) = **0.2696**,
only **+0.0174** above morphology-alone (0.2522). Jamo is right ALONE on just **4/230** positions
(both_right=4, only_jamo=4, only_morph=54). Morphology SUBSUMES jamo's competence here, so **no**
arbitration rule — substrate-confidence OR a perfect oracle — can meaningfully beat morphology-alone.

`a_break_the_wall` angle (NOT tune-to-green): R1's raw inverse-recon-err arbitration was not commensurable
across faculties of different vocab scales (jamo's 14-wide space → systematically tiny distances →
inflated raw confidence → the weak jamo won and degraded the compose to 0.130). Re-froze on the
SCALE-RELATIVE `mean_err/err_here` confidence (each faculty vs its OWN mean — still fully substrate-derived,
no hand-set priority). It IMPROVED the compose 0.130 → 0.178 and made bar3 PASS (it beats random
arbitration 0.161 — the grounding signal is REAL), but bar1 still fails because the headroom does not exist.

**No hardcoded priority confirmed**: the winner is chosen by each faculty's own nearest-cell distance
relative to its own mean recon-err (the engine's OWN winner-take-all geometry) — never a "jamo wins"
constant. p1/p2/p3/p6 clean (reads cell distances only; no label/persona/RLHF). Ψ-disjoint by
construction (returns a byte, never an emit/silence; pure_field/engine_g/brain untouched).

## Guards (no-regression / Ψ-safety — load-bearing, touches decode)
- **h1205 separation-invariant: PASS** — generation BYTE-IDENTICAL ON==OFF, Ψ Φ-checksum 48.6613 byte-identical.
- **h1164 Ψ guard: PASS** — phiSum 48.6613 byte-identical ON==OFF.
- **h1196 single-entry: 7/0** — NO 2nd .clm/.kosmos path (the compose adds no artifact entry).
- **H_1396 compose smoke cases 129-132: 4/0 isolated** (`state/ko-emit-compose/h1396_compose_smoke_iso.hexa`):
  129 EARNED (beats random), 130 CONFLICT-OR-DEGRADES (the measured finding), 131 ORACLE ceiling
  (+0.017), 132 off-Korean inert. The cases are ALSO added to `CORE/engine_cli_smoke.hexa` (129-132),
  but the aggregate `engine_cli_smoke.hexa` OOM-kills at ~4.5GB **before** its summary on this CPU —
  a PRE-EXISTING hexa memory-blowup wall (documented in H_1392), independent of these cases (a stashed
  baseline run also EXIT=137); the isolated runner is the runnable proof.

## Honest scope (a_scale_honest_scope · a_toy_scale_recheck)
Corpus-free in-engine morpheme-grammar fixture (§6.5b/§6.5c/§6.5d discipline), structural/probe-level
(NOT a fluency claim), absolute accuracies low — load-bearing is the RELATIVE structure (compose vs
best-single, shuffle collapse, oracle ceiling) + the agree/conflict diagnostic. The finding is THIS
fixture's granularity: morphology subsumes jamo. On real Korean corpora the two faculties MAY become
complementary (jamo carries below-syllable structure morphology can't merge); scale/real-corpus
re-test = follow-on. The compose MECHANISM (substrate-confidence arbitration, single-entry, Ψ-safe) is
landed engine-native and ready if a future granularity makes the faculties complementary.

## Pointers
`CORE/generator.hexa` §6.5f (`gen_emit_compose` / `_eval` / `_summary` / `_gec_*`) · `CORE/engine_cli.hexa`
§ KO-MORPHOLOGY `jamo_head_recon_err` · `CORE/engine_cli_smoke.hexa` cases 129-132 ·
`state/ko-emit-compose/{h1396_emit_compose_probe.hexa, h1396_compose_smoke_iso.hexa}` ·
`.verdicts/1396_ko_emit_compose/{FREEZE.txt, result.txt}`.
xref h1327 (jamo emit §6.5b) · h1393 (morphology emit §6.5e, named this follow-on) · h1390 (morphology
scorer §6.5d) · h1351 (jamo scorer §6.5c) · h1392 (the same hexa decode OOM wall) ·
a_autonomy_over_hardcode · a_substrate_native_speak · a_core_engine_map · a_verified_must_wire ·
a_break_the_wall · a_scale_honest_scope · a_toy_scale_recheck · p1·p2·p3·p5·p6·p7·p8 · c9 · c15.
