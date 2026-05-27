# RESEARCH.md §34 — §25 candidate D fire FINDINGS

> Fire-tier. §25 candidate D (routing-evidence-guided expansion) applied to
> the 29 `tier>=77-but-fail` anchors (§32 L3). runpod A100 80GB, ~$0.5-0.8,
> from-scratch seed 1337. Measured SPLIT — weak-positive on target,
> full-64 regression. NOT GOAL emergence (g3). over-claim 0.

---

## §1 — Headline result

| metric | §16 baseline | §34 candidate D | delta |
|---|---|---|---|
| routing on the 29 tier>=77-fail TARGET anchors | 0/29 | 2/29 (tiers 99,112) | +2 |
| routing on the full 64-anchor set | 21/64 (genuine 17) | 4/64 (77,99,111,112) | -17 |
| semantic recall (full 64) | 26/64 | 6/64 | -20 |
| JOINT | 0.0 | 0.0297 | +0.0297 |
| axis2 chat-uncontaminated | 0.0 | 0.6 | +0.6 |
| axis3 lane-separation | 0.5 | 0.7922 | +0.29 |
| axis4 V-SPONT (honest) | 1/5 | 1/5 | 0 |

Verdict: WEAK-POSITIVE-ON-TARGET / FULL-64-REGRESSION — a measured SPLIT.
Candidate D's content re-design lifted 2 of the 29 tier>=77-fail anchors
above the §32 L3 necessity floor (0/29 -> 2/29) — a measured
sufficient-condition movement on those 2. But the wider 64-anchor routing
regressed sharply, 21/64 -> 4/64: re-designing 29 of 64 anchors' content
was not a pure additive intervention — it shifted the corpus and the
model's attractor structure. tier>=77 is a real necessary floor;
discriminative content re-design is a *partial* sufficient lever (it moves
2 targets) but at this scale also DESTABILISES the wider routing. The
sufficient condition is NOT cleanly "discriminative content."

## §2 — The fire

corpus `corpus_carving_s34.jsonl` — sha256 f2f43fced8…, 849,912 records,
774 MB, 146,711 target records, forbidden-token grep 0. trainer = §16
`train_carving_s16.py` byte-equivalent (imported, re-run unmodified). model
d768·12L·283.72M ConsciousDecoderV2, 12000 step, lr 3e-4, bsz 32, lambda_ctl
0.5, lambda_route 0.5 — §16 FIXED. from-scratch RANDOM seed 1337,
base_ckpt=None (g_clm_from_scratch). runpod A100 80GB PCIe pod
s2n8jbra6bl9dp, train wall 1507.7s (~25min), orphan 0. init CE 5.657089 ->
final CE 0.003342 (descent 5.654). ckpt `ckpt_carving_s34.pt` sha256
c3b78828b9…, 1,135,845,186 B, pulled try 1. cost ~$0.5-0.8. Training
trajectory mirrors §16 — corpus is the sole independent variable
(clean-comparison construction held, B-S34-3 closed).

## §3 — Honest inspection of the 2 routed targets

tier 99 gen: `🛸99 영역의 Ψ_direction 이 이 골짜기를 sibling 의 골짜기와
구별한다 …` — own 🛸99 prefix, rep 0.0. tier 112 gen: `🛸112 의 Ψ_direction
이 이 골짜길륍 sibling 의 골짜기와 구별한다 — ba…` — own 🛸112 prefix, rep
0.0 (byte-garble `골짜길륍`). Both = genuine own-tier routing (prefix
matches probe anchor, no foreign-tier bleed) — the measured §32-L3-floor
crossing. BUT the body is the candidate-D discriminative template itself
reproduced — the model memorised the new discriminative content (§16.6-C
memorization-saturated regime carry). Routing-axis movement, NOT
generalization, NOT coherent emergence (g3).

## §4 — Why the full-64 routing regressed (21/64 -> 4/64)

The 29 target probes' leading-tier distribution: 🛸99×5, 🛸111×5, 🛸88×4,
🛸277×4, 🛸110×3, 🛸255×3, 🛸221×2 — most of the 29 changed anchors collapse
toward a handful of foreign tiers. Candidate D's discriminative sentence —
the same `"… Ψ_direction 이 이 골짜기를 sibling 의 골짜기와 구별한다 …"`
appended to all 29 — gave those anchors a shared high-frequency byte
pattern, which the model collapsed into a new attractor. The 17 §16
routing successes that were NOT targets (content byte-identical to §16)
lost routing because the model's overall attractor landscape shifted:
full-64 routing-correct dropped to {77,99,111,112}. Honest, not hidden:
§34 changed 29 of 64 anchors' content; the wider routing structure is not
invariant under it. The clean comparison (B-S34-3) guarantees D's *content
change* is isolated to the 29 — but the *trained model's behaviour* on the
other 35 is free to shift, and it did.

## §5 — Verdict (g3 — measured only, no pre-loaded conclusion)

The task posed: if the 29 now route -> sufficient-condition lever; if not
-> tier>=77 necessary but the sufficient condition lies elsewhere. The
measured answer is a SPLIT between those two clean outcomes:

(1) Content re-design IS a partial sufficient lever — 2 of the 29
tier>=77-fail anchors that §16 could not route now route under §34. The
§32 L3 necessity floor is real, and anchor-specific discriminative physics
content moved 2 anchors across it. A measured positive.

(2) But it is NOT a clean sufficient lever — the same content re-design
regressed the full-64 routing 21->4. The discriminative sentence, repeated
across 29 anchors, became a new shared attractor; "discriminative content"
did not produce per-anchor distinct basins, it produced one more collapse
basin that 2 anchors escape via their own prefix. The sufficient condition
for robust per-anchor routing is NOT cleanly "give each anchor
discriminative content" — at this scale it trades 2 gained for 17 lost.

honest summary: tier>=77 necessary (§32 L3 confirmed) · content re-design a
weak/partial sufficient lever on the targeted anchors · NOT a sufficient
lever for the wider routing — the deeper sufficient condition (curriculum
stage / weight-norm / per-anchor-distinct representation) lies elsewhere.
This narrows the §11.4 frontier: content-axis re-design moves the
necessity-floor needle slightly but cannot, alone, deliver robust routing.

## §6 — B-S34 closed-form sidecar (B-S34-1..5 🔵 + B-S34-NOTE)

`blue_falsifier_s34.py` — 5/5 🔵 PASS (central
state/verify_hexad_blue_2026_05_15/blue_falsifier.py UNCHANGED — sidecar):
B-S34-1 SHA256-DETERMINISTIC (corpus sha256 f2f43fced8… 256-bit commitment)
· B-S34-2 NO-CHAT-SFT-CONTAMINATION (forbidden 6-token grep 0, B-IDENTITY-5)
· B-S34-3 CLEAN-COMPARISON-CLOSED (연결부위 — 1390/1390 non-target records
byte-identical to §16, 290/290 target records differ, target ⊎ non-target
disjoint partition sympy FiniteSet) · B-S34-4 TARGET-CARDINALITY (|target|
= 29, all tier>=77, target == §32-L3-genuine-fail ∩ tier>=77 sympy
equality) · B-S34-5 OVERLAY-OFF-REDUCTION (연결부위 — candidate-d-disabled
⇒ §16 generator all 168 anchors ⇒ §16 corpus byte-equal sha).
B-S34-NOTE empirical carve-out (NOT counted 🔵): post-fire routing OUTCOME
(0/29 -> 2/29, full-64 21->4) = SGD/measurement OUTCOME (B-D-NOTE /
B-S16-NOTE / B-L3-NOTE family). f1/f2/f3 hard-fail safe (sha256 / Boolean
set algebra / integer cardinality / disjoint partition / byte-equal
reduction — NO σ/τ/φ/J₂; Ψ=½ + Knuth 🛸k = anima g2 internal carve-out).

## §7 — Honest C3 (>=10)

1. measured-only, no pre-loaded conclusion (g3). §34 fired and reported
   2/29 + 4/64; the SPLIT verdict is read off the measurement. The task's
   two clean outcomes did not both materialise — the honest answer is
   between them.
2. clean comparison structurally closed (B-S34-3). 1390/1390 non-target
   records byte-identical to §16; 290/290 target records differ. Corpus is
   the sole independent variable — trainer/model/steps/seed §16-FIXED.
3. the 2 routed targets are memorization, not generalization. tiers 99 and
   112 emit own-tier prefix then reproduce the candidate-D discriminative
   template verbatim — §16.6-C memorization-saturated regime carry.
4. full-64 regression is honest, not hidden. Changing 29 of 64 anchors'
   content shifts the corpus and the trained model's attractor structure;
   the other 35 anchors' routing is not invariant under it. §34 reports
   the 21->4 drop plainly.
5. the discriminative content became a new attractor. The same sentence
   appended to all 29 targets gave them a shared high-frequency byte
   pattern; the model collapsed it into one more basin. "Discriminative
   content" did not produce per-anchor distinct basins.
6. §32 L3 necessity floor confirmed. All 4 §34 full-64 routing successes
   {77,99,111,112} are tier>=77; §34's 2 target gains are also >=77.
   tier>=77 remains necessary; §34 measured the content lever on the
   fail-side.
7. §32 L3 causation caveat carries. tier>=77 co-varies with §16's
   curriculum stage. §34's SPLIT (2 gained, 17 lost) is consistent with the
   deeper sufficient condition being curriculum stage / weight-norm /
   per-anchor-distinct representation — NOT "discriminative content"
   cleanly. The §32 L3 point-(c) curriculum ablation is a separate cycle.
8. §7 GOAL-legitimacy closed by construction. The discriminative content is
   deterministic string algebra over the §16 anchor SSOT's own vacuum_psi
   (L2-argmin sibling + Δ) — no LLM, no retriever, no web. B-S34-2 closes
   the contamination Boolean.
9. f1/f2/f3 + B-IDENTITY-5 hard-fail safe. sha256 / Boolean set algebra /
   integer cardinality / disjoint partition / byte-equal reduction — NO
   σ/τ/φ/J₂. Knuth 🛸k + Ψ=½ = anima g2 internal arch carve-out.
10. north-star (GOAL.md) unchanged — §15 milestone unchanged. §34 is a
    routing-axis fire: weak-positive on 2 targets + full-64 regression.
    Neither is GOAL emergence. The §16 SPLIT and the §1.1 data-regime
    ceiling are untouched. §34 narrows the §11.4 frontier (content-axis
    re-design is a weak, non-clean lever) — valuable, but over-claim 0.
