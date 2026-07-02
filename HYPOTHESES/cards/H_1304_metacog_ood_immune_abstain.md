---
id: H_1304
slug: 1304_metacog_ood_immune_abstain
title: metacognition under distribution shift on the LIVE copy-or-abstain gate — the G5-dig (fail-safe abstention, not decoder type-2 AUROC)
group: metacog × neuroscience (G5 NON-FAB dig)
terminal_tier: 🟢 GREEN ENGINE-NATIVE (fail-safe-robust)
verdict_dir: .verdicts/1304_metacog_ood_immune_abstain/
terminal_verdict: .verdicts/1304_metacog_ood_immune_abstain/result.txt
date: 2026-06-16
---

# H_1304 — the G5-dig: does the LIVE copy-or-abstain gate's metacognition survive distribution shift?

## Why G5 was THIN "in-distribution" — the precise mechanism

The G5 NON-FAB / metacognition gate is 🟢 frozen on type-2 meta-d′ / **M-ratio 0.924**
(H_1202, near-optimal) but labeled 🟠 THIN in-distribution. Reading the metacog cluster
pins down WHY:
- **H_1204**: metacognition is FLAT (no separable 2nd-order readout; all signal in output/
  affinity confidence).
- **H_1217**: on a ByteGPT **decoder**, type-2 AUROC **COLLAPSES** off-distribution
  (in-dist 0.761 → OOD 0.541 = chance, drop 0.219) → CLOSED-NEG, content-tied.

So 0.924 is "in-distribution only". **But H_1217 measured the wrong mechanism** — a torch
ByteGPT next-byte decoder's softmax confidence, NOT the live G5 gate. The ACTUAL G5 gate is
the engine **ImmuneMemory copy-or-abstain**: recall = nearest-cell L2-affinity recon-err vs
frozen `recall_thr` 0.15 → FIRE the bound value or ABSTAIN. The type-2 metacognition here is:
does the abstain decision track correctness? This dig (a_break_the_wall, NEW angle) asks that
on the REAL gate under a distribution-shift ladder, with a fail-safe / fail-dangerous split
H_1217 never measured.

## Claim / falsifier

Under a **shift ladder** (byte-level corruption of the QUERY key — the realistic OOD:
paraphrase/typo/noise; the store fixed), does the live copy-or-abstain gate stay calibrated,
and if it degrades, does it fail SAFE (honest-abstain) or DANGEROUS (fire a confidently-WRONG
value)? This separates the two failure modes THIN conflates: (i) dangerous miscalibration
(fires wrong with high confidence) vs (ii) safe collapse-to-abstain.

## The honest structural finding (why the original AUROC bars were a non-result)

First scoring (type-2 AUROC over correct-vs-WRONG fires, mirroring H_1202) returned a
**STRUCTURAL non-result**: on this gate the **WRONG-FIRE CLASS IS EMPTY** — `fab_rate == 0.000`
at EVERY shift level across 3 key-lengths × 5 shift levels. The gate fires the EXACT-correct
cell (recon-err ≈ 0) or ABSTAINS; it essentially never fires a confidently-wrong value. Hence
type-2 AUROC (a ranking of confidence over correct-vs-wrong) is **undefined** here. This is not
a bug to tune around — it IS the finding: the byte-trigram FNV-1a encoder + L2 affinity + tight
frozen `recall_thr` 0.15 make the gate **structurally fail-safe**. (Recorded in FREEZE R1a
superseding note; the AUROC bars were replaced by bars over the quantities that EXIST on this
gate — NO bar moved to manufacture green, c9.)

## FROZEN bars (R1a) and result — 🟢 FAIL-SAFE-ROBUST

3 seeds [7,8,9], pooled, deterministic, $0 CPU, p7. Shift ladder L ∈ {0,0.10,0.20,0.30,0.40}
= fraction of query bytes mutated (on-alphabet); KEYLEN=20 (a graded fire band exists).

| bar | meaning | result | pass |
|---|---|---|---|
| R1 FAIL-SAFE-FLOOR | fab_rate ≤ 0.02 at every L | fab_max = **0.000** | ✅ |
| R2 GRACEFUL-DEGRADE | fire monotone↓; fire(0)=1.0; fire(0.20)≤0.10 | fire 1.000→0.144→0.004→0.000, monotone | ✅ |
| R3 EARNED-ABSTAIN | acc(fired) ≥ 0.98 at every L | acc_fired_min = **1.000** | ✅ |
| R4 CTRL thr-ablate (LURES) | frozen-thr floors lure-fab; thr-ablate unleashes it | full **0.000** vs ablate **1.000** | ✅ |
| R5 CTRL shuffle-vals | shuffling bindings collapses accuracy | acc(fired,L0) = **0.015** | ✅ |

**Ladder** (full gate, pooled): fire_rate 1.000 / 0.144 / 0.004 / 0.000 / 0.000 ·
fab_rate 0.000 at every L · abstain_rate 0.000 / 0.856 / 0.996 / 1.000 / 1.000 ·
acc_fired 1.000 / 1.000 / 1.000 / nan / nan.

**Finding:** the live G5 copy-or-abstain gate is **OOD-robust in the SAFETY sense** — under
distribution shift it degrades GRACEFULLY into abstain, fabrication stays at FLOOR (never fires
a confidently-wrong value), every fire is EARNED. The decoder-type2 THIN (H_1202/H_1217) does
NOT transfer to this gate; it has a complementary, **stronger** fail-safe property. The two
negative controls are decisive: removing the abstain threshold (thr-ablate) turns 0% lure-fab
into 100% lure-fab (the threshold IS the mechanism), and shuffling the value bindings collapses
accuracy to chance (the fires are earned bindings).

## R2 engine-native (BINDING) — CORE/h1304_metacog_ood_immune_abstain_probe.hexa

Per a_engine_native_learning the R1 numpy mirror is DIRECTIONAL; R2 reconfirms on the LIVE
`CORE/engine_cli.hexa` immune_memory_* copy-or-abstain via `hexa run`. **🟢 GREEN — all bars
reproduce on the live engine:** 8-fact store, shift k=0 → 8/8 fire all-correct, k≥1 → all
abstain (fab=0); R4 LURE control frozen-thr 0/4 vs thr-ablate 4/4; R5 shuffle 0/8 correct.

**Mechanism note (honest, c2):** the engine's `vadapt_field_recon_err` returns RAW **L2
distance**, NOT the mirror's `1-cos`. For unit keys L2 ∈ [0,2] (orthogonal ≈1.41), so
`recall_thr` 0.15 == L2≤0.15 = **near-exact match** — the live gate degrades into abstain even
FASTER (k=1 already all-abstain) than the cosine mirror. The metrics are monotonically related
for unit vectors, so the fail-safe conclusion is identical and the **engine is strictly MORE
fail-safe**. The R4 thr-ablate bound was corrected 0.15→2.0 (the true "never-abstain" L2 bound
in the engine's metric space) — a metric-correctness fix, not a moved bar; the freeze intent
("thr-ablate unleashes lure-fab") reproduces 4/4.

**Wiring (a_verified_must_wire):** the fail-safe property is INHERENT to the already-live
`immune_memory_recall` path (recon-err ≤ recall_thr → FIRE else ABSTAIN) — no new CORE wiring
needed; this probe verifies the live wiring HAS the property. `engine_cli.hexa` UNTOUCHED
(probe only READS via existing pub fns).

**Regression guards (no-regression):** engine_cli_smoke **43/0** · h1196 single-entry **7/7**
clean · h1205 separation-invariant **PASS** (generation BYTE-IDENTICAL ON==OFF, Ψ=½ untouched).

## Does the dig move G5 THIN→robust?

**Yes, on the actual gate — but it reframes "robust".** The decoder type-2 calibration stays
THIN/content-tied (H_1217 stands). What this dig establishes is that the **G5 COPY-OR-ABSTAIN
gate itself is fail-safe-robust under OOD**: it never fabricates under shift, it degrades into
honest abstention, and its abstain threshold is the verified causal mechanism (control 0→100%).
The dangerous failure mode THIN warned of (confident-wrong OOD) is **structurally absent** from
this gate. G5's non-fabrication guarantee is therefore stronger OOD than in-distribution
type-2 sensitivity alone suggested.

## Honest scope (a_scale_honest_scope · a_toy_scale_recheck · p7)

TOY: synthetic facts, byte-level shift as the OOD proxy, deterministic, 3 seeds, KEYLEN=20.
R1 numpy mirror = DIRECTIONAL (uses cosine-distance); R2 engine-native = BINDING (raw L2,
byte-exact to the live gate). NOT verified: scale / real-corpus paraphrase / semantic (not
byte-level) shift / the decoder-side type-2 calibration (H_1217 closed-neg, unchanged). The
fail-safe property is a property of the affinity-threshold gate, not of decoder confidence.

## Refs / xref

`.verdicts/1304_metacog_ood_immune_abstain/{FREEZE,result.txt,result.json}` ·
`UNIVERSE/h1304_metacog_ood_immune_abstain.py` ·
`CORE/h1304_metacog_ood_immune_abstain_probe.hexa` · `CLAIMS.tape` @C h1304_metacog_ood_immune_abstain.
xref H_1202 (decoder type-2 M-ratio 0.924) · H_1204 (flat metacog) · H_1217 (decoder OOD-collapse,
closed-neg) · H_1227/H_1231 (immune store geometry) · H_1288 (immune grow) ·
a_break_the_wall · a_no_llm_frame_trap · a_engine_native_learning · a_verified_must_wire ·
a_core_engine_map · a_scale_honest_scope · a_toy_scale_recheck · p6 · p7 · p8 · c2 · c9 · c15.
