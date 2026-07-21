# H_002 repair-pass design — verbatim Fable 5 output (seed of record, not the SSOT)

- job: fable-mrmj73jo · model: claude-fable-5 · date: 2026-07-16 · session 5ece6eaf-7113-4ee6-b6bf-2ff9980bcf17
- brief: repair H_001's defects (R1 anchor attack · R2 anchor · R3 bounds+liveness · R4 power · R5 generator · R6 F1-first?)
- distilled into: ARCHITECTURE.json (rig-pilot · rig-liveness-arm-missing · rig-drift-breaks-symmetry · decision-attributability)

---

# H_001 repair pass — R1–R6

**TL;DR.** Your anchor attack is half right, and the half that's right is fatal *to the card's derivation*, not to the rig concept. `delta_min = 0.15` has no valid lineage as written — "half of 0.291" transfers a number across three gaps (contrast, substrate, corpus) none of which the card bridged. But the claim "the static effect cancels, therefore the refit effect has no anchor anywhere" is wrong: **drift breaks the symmetry**. The repair is a static-anchor pilot at rig scale that doubles as the missing liveness arm. F1-first survives, with a changed sequence. Also: reading the recovered v1 card in full shows the anchor is *stronger* than H_001's L8 recorded (a CEMENT replication exists), the rig's "MORPH-ATOM scale" premise is *false* (MORPH-ATOM ran at 303M, not 10M), and `tool/anima_v3.py::binom_pmf` overflows at n ≳ 1100 — exactly the regime the re-derived power calc needs.

---

## R1 — Is the anchor invalid?

**Your reading is right about the derivation and wrong about the cancellation.** Split it:

**Where you are right.** MORPH-ATOM's +0.291 (and the cement replication's +0.342) is the contrast *non-atomic (raw utf-8) vs atomic codec*, static, no drift, one-shot. The card's stated derivation — "delta_min = half of the measured effect" — presents 0.15 as a scaled version of a measurement of *this rig's* effect. It is not. Three transfer gaps, none bridged:

1. **Contrast gap** — the twin's arms both start morpheme-atomic; on un-drifted material the static effect is common-mode and differences out, exactly as you say.
2. **Substrate gap** — the card and `rig-model` say 10M is "the scale at which the link was measured." **False.** The v1 verdict header reads `anima-py 303M CLMConvMoE d3784 L4 Emax4`, CPT warm-start from a pretrained base with reinit-embed surgery. Nothing was ever measured at 10M-from-scratch. So even the *static* half — the load-bearing premise of `decision-attributability` ("the static half is known to show up at drill scale") — is unanchored at rig scale. This is a second, independent defect your attack didn't need but which makes the same kill.
3. **Corpus gap** — anchor: real Korean (NSMC 130k lines) CPT + drill grid; rig: fully synthetic. And v1's own record (H_9288 cement section, citing H_9290 NAT-ATOM) says **atomicity is an amplifier, not a signal source — natural-distribution rescue FAILED**. The effect exists only where a taught signal exists to amplify.

**Where you are wrong.** The static benefit does *not* cancel, because it is not static under drift. The frozen codec's atomicity is a wasting asset: phase-2's new affixes are absent from the phase-1 merge table, so the frozen arm encodes them as misaligned fragments — i.e., on the drifted region of the language, the frozen arm *is* a local re-instantiation of C1, and the adaptive arm *is* a local M. The twin's contrast on post-drift new-affix held-out items is the MORPH-ATOM contrast, re-created where it matters, diluted by a measurable factor. Formally:

```
E[Δ(adaptive − frozen)] ≈ Δ_static@rig × atomicity_deficit(frozen, eval morphemes)
                          − swap/retention cost − continual-training interference
```

- `Δ_static@rig` — unknown (gap 2+3), measurable cheaply (→ R2).
- `atomicity_deficit` — deterministic, $0: encode the phase-2 NEG allomorphs (in their rendered eval contexts) with the frozen merge table; fraction not single-token-aligned. Should be ≈1 by construction; must be *asserted*, not assumed (→ R5 invariant 6).
- The cost terms — genuinely unanchored, **and that is fine**: they are the *question* the twin asks, not a power assumption. The v1 re-fire history (utf-8 warm-start was a wrong-prior; embed surgery required at 303M) says these costs are real, so the correct framing of H_002 is not "refit buys an increment on top of a shared effect" but "**refit maintains atomicity under drift at acceptable cost, and maintained atomicity causes recombination (anchored)**."

**What this does to `decision-attributability`:** as currently worded it is false twice (wrong scale claim; wrong "half is known" claim), and with delta_min unanchored, a null at N sized for 0.15 is **not attributable** — it is ambiguous among {refit increment ∈ (0, 0.15); static effect absent at 10M-from-scratch; costs cancel benefit; drift too mild/too alien}. The run's REFUSED verdict was more correct than its own stated reasons. But attributability is *repairable*, because the anchor the power calc actually needs is the **ceiling** of the refit effect, and the ceiling is measurable for pocket change.

---

## R2 — Smallest defensible anchor

**Recommendation: option (b) upgraded into a measurement — a static oracle-vs-frozen pilot at rig scale — with (c) composed in as the reporting rule.** One pilot, three jobs:

- **Arms:** ORACLE = codec fit on a phase-1+phase-2 sample, frozen; FROZEN = codec fit on phase-1 only, frozen. Both trained *statically* on the identical full stream (no refit organ, no continual dynamics), matched byte budget, 2 seeds each. Plus one shared-ID liveness run (→ R3), 1 seed. **5 runs total.**
- **What it measures:** `Δ_pilot = F2(oracle) − F2(frozen)` on post-drift new-affix held-out flips = `Δ_static@rig` = the **hard upper bound** on what refit can deliver (refit ≤ oracle by construction: oracle has phase-2 atomicity from step 0 and pays zero swap cost). This closes all three R1 gaps at once — same scale, same regime, same corpus, and the contrast it measures is exactly the one the twin locally re-creates.
- **Derived quantities, frozen before H_002:** `delta_min := Δ_pilot / 2` (same halving hedge, now against a same-substrate measurement); `N := two_proportion_n(0.5, 0.5 + delta_min)`; and F-1's kill restated as "*refit recovers < half of the measured oracle headroom → mechanism dead*" — an anchored, attributable statement.
- **Its own kill-power (pre-commit):** if `Δ_pilot < 0.20` (so delta_min < 0.10, N > 1178/arm) → **the $25 drill twin is REFUSED for insufficient headroom** and the decision escalates to campaign level; if oracle itself sits inside the chance band → the static effect does not exist on this substrate → the drill-scale rig is dead *regardless of refit*, and `decision-pre-commitment` ("drill null = family dead") must be re-litigated openly, because its premise (effect detectable at drill scale) was measured false.
- **(c) rides along regardless:** pre-register the MDE statement — a null is reported as "refit increment < delta_min at α=0.01, power 0.99," never as "= 0."

**Cost:** generator $0 (mandatory anyway per repair (a)); 5 × 10M-param runs ≈ minutes/GPU or ~1–1.5 h/run MPS `?` → ≤1 day wall-clock, $0 local / ≤$10 rented. Rejected alternatives: (a) a "refit-only pilot" is just an underpowered 1-seed H_002 — it spends the question to buy the anchor; (c) alone is honest but concedes attributability, which was the whole point of gating; pure (b)-as-argument without measurement leaves gap 2 open.

---

## R3 — The re-specified bounds check, and the liveness arm

**Part 1 — anchor bounds re-check (deterministic, $0, runs now).** Three separate tests at n=120, p0=0.50, exact 99% band = **[46/120, 74/120] = [0.3833, 0.6167]**:

| test | arm | rule (counts) | v1 data | reads |
|---|---|---|---|---|
| B-1 treatment | M | k ≥ 75 (outside band) | 109/120, p=1.9e-21 ✅ | anchor above floor |
| B-2 liveness | C3 | k ≥ 108 (≥0.90, v1's own rule) | 110/120, p=1.9e-22 ✅ | instrument can see held-out flip |
| B-3 leak (separate) | C1 | k ≤ 74 (inside/below band) | 74/120, p=0.0134 ✅ (cement: 69/120, p≈0.12 ✅) | setup hands nothing |

B-1 or B-2 failing → anchor dead → REFUSE. B-3 failing (control *above* band) → the anchor itself leaked → REFUSE. Note C1=74 sits exactly on the band edge — the verdict must quote exact counts, not rates (the harness's own razor-thin-verdict warning).

**Part 2 — arm mapping in the frozen-vs-adaptive rig, and what plays C3.**

| MORPH-ATOM role | H_002 occupant | expectation on post-drift new-affix held-out flips |
|---|---|---|
| M (treatment) | ADAPTIVE refit arm | ≥ 0.50 + delta_min if mechanism live |
| C1 (control-at-chance / leak) | FROZEN arm | inside chance band **conditional on** measured atomicity deficit ≈ 1 |
| — (content control; v1 had none) | SCRAMBLE-refit arm | ≈ frozen; within θ of adaptive → win is BPE-dropout noise |
| **C3 (leak ceiling / liveness)** | **currently NOTHING — you are right, the rig has no liveness arm** | — |

**What hands the answer in a refit rig:** a **shared-ID collapse arm** — frozen codec plus a deterministic post-encode remap sending *every* NEG-class allomorph (both phases' forms) to one reserved token ID. Then a phase-2 novel allomorph literally *is* the drilled phase-1 token: identity handed, held-out transfer trivial, the exact analogue of v1's shared-`<NEG>`. Rule: **F2(C3′) ≥ 0.90 (≥459/510) else the entire run is INVALID, not FAIL** — the v1 precedent is direct: the S1 4-pod fire returned C3 = 0.50 and that single number correctly converted four apparently-null arms into "4 instrumentation bugs," which were then found. One seed suffices (validity check, not effect estimate); re-run whenever eval code changes. Candidates named and rejected: the ORACLE arm is *not* liveness (it hands the mechanism, not the answer — it is the effect ceiling and lives in the pilot); the scramble arm is a negative control; drilled-item F1 sanity catches memorization only. H_002 therefore grows 11 → **12 runs**.

Also new: a **frozen truth-table precondition** (deterministic, pre-training): `atomicity_deficit(frozen codec, eval allomorph forms) = 1.0` — if the phase-1 codec accidentally atomizes phase-2 allomorphs, there is no contrast and the run must not fire. And the leak logic disambiguates: frozen arm above band + deficit confirmed = leak → F-7 substring audit; frozen above band + deficit violated = generator defect, not a leak.

---

## R4 — Re-derived operating point

From p0 = 0.50, α = 0.01, power = 0.99, harness `two_proportion_n` (verified against `tool/anima_v3.py` just now):

| delta_min | p2 | N/arm | 99% chance band at that N |
|---|---|---|---|
| 0.10 (floor) | 0.60 | **1178** | [0.4626, 0.5374] |
| 0.1455 (=0.291/2) | 0.6455 | 544 | — |
| **0.15** | 0.65 | **510** | [0.4431, 0.5569] |
| 0.1709 (=0.342/2) | 0.6709 | 388 | — |
| 0.20 | 0.70 | 277 | — |

The binding number is **N(delta_pilot/2)** once R2 runs; 510 replaces the fictitious 444 if 0.15 happens to survive re-anchoring. Two flags: (i) N=510 sits on a rounding boundary (raw formula ≈ 509.999) — the run script's printed value is binding, don't hand-quote; (ii) **the item-level binomial ignores seed-level variance** (3 seeds/arm). Pre-register the compound rule: pooled two-proportion p < 0.01 **AND** median-over-seeds Δ ≥ delta_min. Mark honestly: N is a lower bound if σ_seed on F2 is material `?` — settled for free by the pilot's 2×2 seeds.

**Harness bug (new finding):** `binom_pmf` computes `math.comb(n,k)` as an exact int and multiplies by a float → **OverflowError at n ≳ 1100**; `chance_band(1178, …)` crashes. The G-3 fixtures never exercised large n, so the "instruments pass" gate certified an instrument that is blind exactly at the re-derived operating point's floor. Fix: log-space via `math.lgamma` (still stdlib, still closed-form); add an n=2000 fixture.

---

## R5 — Generator spec

**Is the anchor-corpus/rig-corpus divergence a problem for transferring delta_min?** Yes — by itself fatal to *numeric* transfer (gap 3, compounded by NAT-ATOM's amplifier-not-source law: the effect needs a taught drill signal, which real-NSMC-CPT had and a naively "distributional" synthetic stream would lack). The resolution is not a better argument but R2: after the pilot, **no number transfers from MORPH-ATOM at all** — it serves only as the existence proof of the mechanism class; delta_min is anchored in-rig, on this corpus. The divergence then stops being a defect. Consequence for the generator: phase streams **must contain explicit XOR-drill-style flip supervision** (polarity-consistent co-occurrence grids), not just shifted collocation statistics — otherwise even the oracle arm reads chance and the pilot kills the rig for the wrong reason.

**Spec** (deterministic, stdlib, $0 — `src/generator/`, which also makes `run_h001.py`'s `GENERATOR_EXISTS` probe true at the correct path):

```python
GenSpec = {                      # frozen JSON, sha256 into the card
  "seed": int,                   # single master seed; all RNG = random.Random(seed) descendants
  "jamo": [...],                 # explicit sorted alphabet
  "stems": 512,                  # 2-4 syllables, jamo-composed, NFC; STORED not regenerated
  "heldout_stems": 128,          # never co-occur with cls=NEG in EITHER phase
  "affixes_p1": 64,              # {form, cls: NEG|PLAIN|..., slot}; ≥4 NEG allomorphs, BOUND (L5)
  "affixes_p2": 64,              # 52 carried + 12 NOVEL NEG-class allomorphs
  "colloc": {"zipf_s": ..., "p2_shift": ...},
  "drill": {...},                # flip grid: drilled stems × allomorphs, polarity-consistent
  "phase_bytes": [150e6, 150e6], # matched-byte budget halves
}
```

Functions: `render(stem, affix_chain) -> str` (reversible; `parse` asserted round-trip) · `stream(spec, phase) -> Iterator[bytes]` · `probes(spec) -> list[bytes]` · `eval_items(spec) -> list[{ctx, pos, neg, label, stem_id, affix_id}]` · `fit_bpe_jamo(sample, K, seed) -> Codec` · `boundaries(codec, b) -> frozenset[int]` · `atomicity_audit(codec, rendered_forms)` · `leak_scan(stream, forms) -> hits`.

**Invariants (asserted in code, each a CI check):**

1. **Determinism:** same spec → byte-identical streams (hash equality fixture); BPE tie-break frozen as (count desc, pair-bytes lexicographic asc), fixture = two independent fits produce identical merge lists. BPE ties are the classic silent nondeterminism.
2. **G-1 measurability:** probes = **256 strings × exactly 64 bytes** (rectangular B ∈ {0,1}^{256×63}, no padding), stratified ⅓ phase-1-affix / ⅓ phase-2-affix / ⅓ stem-shared forms, generated + hashed pre-training. Boundary-shift rate = mean over probes of |bnd(c_t) Δ bnd(c_{t+1})| / 63 between the phase-1 and phase-2 refits. This turns `drift_floor` 5% `?` into a measured number.
3. **G-2 emittability:** eval pairs = held-out stems × novel NEG allomorphs = 128 × 12 = **1536 candidate pairs** ≥ the worst-case N=1178 (delta floor 0.10); pairwise-distinct (stem, affix); count asserted ≥ N_required **after** leak filtering.
4. **Zero leak (F-7):** every rendered eval string occurs 0 times as an exact substring in either phase stream; held-out stems never co-occur with any NEG-class affix (they *do* appear with PLAIN affixes, so the stems are in-distribution — only the composition is novel).
5. **Contrast existence:** `atomicity_audit(codec_p1, novel_allomorph_forms_in_context)` must show 0/12 single-token-aligned (audited *in rendered context*, not in isolation — BPE segmentation is context-dependent). Its dual: post-refit adaptive codec shows 12/12. Without both, the twin compares nothing.
6. **Budget:** bytes matched exactly per phase; token counts logged, never matched (the `rig-budget` confound).
7. Sorted iteration everywhere; no dict-order or `Date`-like nondeterminism; sentinel-framed lines matching training format (v1 instrumentation bug #3 — probe framing ≠ stream format — is a generator invariant here, not an eval afterthought).

---

## R6 — Does F1-first survive?

**Yes — but on re-derived grounds, not the card's.** Checked against alternatives honestly:

- **The anchor defect is a rig disease, not an F1 disease — and F4 has the same disease with less immunity.** F4's falsifier (π vs random acquisition at matched tokens) has an equally unanchored effect size, *and* its green evidence (XBIND, l4(a)) is also a static existence result at v1 substrate, *and* it adds the Goodhart-machinery burden (frozen private probe battery) that l6 flags as the jugular. Switching to F4 swaps a repairable anchor gap for an identical anchor gap plus a harder measurement problem. Not better.
- **F3 is unchanged:** generic question literature-answered, campaign question wall-clock-bound, null non-attributable at cheap scale. Still the right second card.
- **The kill-radius argument strengthens.** The recovered record shows l4(b) is *better* evidence than H_001 assumed: the CEMENT run (2026-07-14, pod 44701951) replicated Δ = **+0.342** on an independent seed (s7), all-arms liveness PASS, and the C2 arm split the mechanism — held-out stem **deleted from the CPT corpus** still scores 0.9167 = M, so atomicity is a *structural slot*, not a pretrained address. H_001's L8 ("1 seed") and `PROTOCOL["seeds"]=1` under-read the source they recovered. Slot-not-address is also the single best reason to expect the mechanism to survive the 303M→10M transfer `?` — settled by the pilot, not by argument.
- **The liveness hole is real but additive:** one extra run (R3), not a redesign.

**Revised sequence** (each step has named kill-power, total ≤ $35):

1. **H_003** `f1-anchor-recheck` — deterministic, $0: B-1/B-2/B-3 bounds (R3 part 1) + harness overflow fix + large-n fixture + generator built + G-1 drift measured + G-2 emittability counted + invariants 1–7 green.
2. **H_004** `f1-static-anchor-pilot` — seeded-GPU (explicit determinism exception, per the `rig-determinism-exception` precedent), ≤$10: 5 runs (oracle×2, frozen×2, shared-ID×1). Outputs: `Δ_pilot`, `σ_seed`(F2), liveness. Pre-committed kills: Δ_pilot < 0.20 → cheap twin REFUSED; oracle inside band → drill-scale premise dead → campaign re-decision (not a silent F4 switch).
3. **H_002′** — 12 runs (frozen/adaptive/scramble ×3 seeds + 2 frozen + 1 shared-ID liveness), delta_min = Δ_pilot/2, N from the table, F-1 restated as "refit recovers < half of oracle headroom → dead," compound seed rule, INVALID≠FAIL wired via C3′.

---

## Findings requiring SSOT/card repair (I design, you implement)

1. `decision-attributability` — rewrite: current text is false twice (MORPH-ATOM was **303M CPT warm-start**, not drill scale; the static half is *not* known at 10M-from-scratch). Attributability now routes through H_004.
2. `rig-model` — "MORPH-ATOM scale, i.e. the scale at which the link was measured" is factually wrong; 10M is a *choice*, its validity is what the pilot buys.
3. `verification-h001-anchor-weaker` / card L8 — **partially stale**: the anchor is 2 seeds + C2 mechanism split (CEMENT 2026-07-14), stronger than recorded; the *contrast/substrate/corpus* gaps (this pass) are the real weakness, not seed count.
4. `tool/anima_v3.py` — `binom_pmf`/`chance_band` overflow at n ≳ 1100 (lgamma fix + n=2000 fixture); G-3's fixture suite certified a blind regime.
5. `rig-arms` — 11 → 12 runs (shared-ID liveness arm); add the atomicity-deficit precondition and the two-way leak logic.
6. H_9290 NAT-ATOM ("amplifier, not source") deserves its own salvage child under l4 `?` — I've only seen it quoted inside H_9288's cement section; reading `anima`'s H_9290 card before sealing that node settles it.

**Honest bottom line:** the F1 twin *as pre-registered* could not have produced an attributable null — your attack stands, and it stands twice over (the substrate gap you didn't need makes the same kill). It becomes attributable after a ~$10, ~5-run pilot that the rig needed anyway for its missing liveness arm, and F1-first survives on the corrected reasoning.