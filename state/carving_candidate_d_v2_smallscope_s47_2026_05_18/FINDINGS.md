# RESEARCH.md §47 — §40 small-scope candidate D per-anchor-distinct retry

> Fire-tier. §25 candidate D v2 (anchor-DISTINCT content) on the 29
> `tier>=77-but-fail` anchors (§32 L3). runpod A100-SXM4-80GB (A100 80GB
> PCIe stock-exhausted -> SXM4 fallback), small-scope 3000 steps (0.25x
> §16/§34), from-scratch seed 1337. Measured NULL — §42's weak/null
> prediction CONFIRMED. NOT GOAL emergence (g3). over-claim 0.

---

## §1 — Headline result

| metric | §16 baseline | §34 (shared template) | §47 (anchor-distinct) |
|---|---|---|---|
| routing on the 29 tier>=77-fail TARGET anchors | 0/29 | 2/29 (99,112) | 0/29 |
| routing on the full 64-anchor set | 21/64 (genuine 17) | 4/64 | 1/64 (tier 111 = digit-cascade artifact, NOT genuine) |
| semantic recall (29-target) | 0/29 | — | 0/29 |
| JOINT (full 64) | 0.0 | 0.0297 | 0.0156 |
| axis2 chat-uncontaminated | 0.0 | 0.6 | 1.0 |
| axis3 lane-separation | 0.5 | 0.79 | 1.0 |
| axis4 V-SPONT (lenient) | 1/5 | 1/5 | 1/5 |
| delta vs §16 baseline (29-target) | — | +2 | 0 |
| delta vs §34 baseline (29-target) | — | — | -2 |

Verdict: NULL. Anchor-distinct discriminative content routed 0 of the 29
tier>=77-fail anchors — worse than §34's shared-template 2/29, identical
to the §16 baseline 0/29. §42's pre-registered weak/null prediction (the
17-vs-29 lottery is internal to the tier>=77 band and is NOT an
anchor-property / content-distinctness lever) is confirmed by
measurement. The single full-64 "routed" anchor (tier 111) is a
"&#x1F6F8;1111111..." digit-cascade artifact (§16.6 substring-attractor
family — "111" subset of "&#x1F6F8;1111..."), NOT genuine own-tier
routing.

## §2 — The fire

- corpus corpus_carving_s47.jsonl — sha256
  19242b2701637996a4c0fb3f18cafa237f59c1fa80c26997ba6126843108384a,
  199,920 records, 175 MB, 34,510 anchor-distinct target records (29
  anchors x 1,190), 165,410 §16-byte-identical non-target records (139
  anchors x 1,190), forbidden-token grep 0 (B-IDENTITY-5).
- trainer = §16 train_carving_s16.py (Dir-I lever — Psi-anchored CTL +
  tension-supervised routing + §12.1 Q1-c curriculum) byte-equivalent,
  invoked via train_s47.py with ONLY --steps 3000 changed (§16/§34 use
  12000 — 0.25x per §47 small-scope mandate).
- model d768.12L.283.72M ConsciousDecoderV2, lr 3e-4, bsz 32,
  lambda_ctl 0.5, lambda_route 0.5, blend_frac 0.15 — §16 FIXED.
  from-scratch RANDOM seed 1337, base_ckpt=None (g_clm_from_scratch).
- runpod A100-SXM4-80GB pod t7mbkoq25mrb5i (A100 80GB PCIe stock-
  exhausted -> SXM4 fallback within the same runpod sweep), single pod
  train+eval, train wall 372.05 s (~6.2 min), init CE 5.668285 ->
  final CE 0.004921 (descent 5.663), final l_psi_ctl 0.008115, final
  l_tension_route 1e-06, peak GPU mem 9.692 GB. curriculum step-gate
  histogram {1:638, 2:637, 3:638, 4:1087}. ckpt ckpt_carving_s47.pt
  sha256 f9e4233bce63eaef4cf043ae29b64f1b659389f966cc1a0787be309e5185b870,
  1,135,845,186 B, pulled try 1 (g_fire_dispatch_robust SAVE_POD
  auto-promote + 5-retry). Pod terminated on PULL SUCCESS — orphan 0.
  Cost ~ $0.10-0.20. Training trajectory mirrors §16/§34 (final CE
  ~0.005) — corpus + step-budget the only variables, both held by
  construction (B-S47-4/-5 closed).

## §3 — Honest inspection of the failed routing

The 29-target probes ALL bled into a single foreign tier: 29/29 ->
tier 111. No target anchor surfaced its own tier prefix. The model
collapsed the 29 anchor-distinct contents into one shared attractor
anyway — the "&#x1F6F8;11111111111..." digit-cascade (B-ATTRACTOR /
feedback_clm_colon_attractor family). This is the OPPOSITE of the §47
hypothesis: even though each of the 29 targets received a pairwise-byte-
distinct discriminative paragraph (B-S47-3 closed: C(29,2)=406 pair
byte-distinct, 0 collision), the trained model did NOT learn 29 distinct
per-anchor basins — it learned one collapse basin. Anchor-distinct
content did not produce anchor-distinct routing.

## §4 — Why anchor-distinct content did NOT help (g3, measured)

§34 found a SHARED discriminative template became one new shared
attractor (2 anchors escaped via own prefix, 17 §16-successes lost).
§47's hypothesis was that anchor-DISTINCT content would avoid that
failure mode. Measured outcome: anchor-distinct content STILL collapsed
into a single attractor (tier 111), and routed FEWER targets than §34
(0 vs 2). Two honest reads, both consistent with the data:

1. Small-scope confound (dominant honest caveat). §47 used 3000 steps
   (0.25x §16/§34's 12000) and a 175 MB corpus (vs §34's 774 MB). §34's
   2/29 came at 12000 steps. The reduced scale plausibly denies §47 the
   training signal §34 had — the small-scope design (mandated by §47
   for faster turnaround / less rate-limit risk) trades fidelity for
   cost. So §47's 0/29 < §34's 2/29 is partly a SCALE effect, not
   purely an anchor-distinct-content effect. Honestly disclosed: §47
   measures "anchor-distinct content AT small-scope," answer NULL. The
   clean comparison (B-S47-4/-5) isolates the corpus content change but
   does NOT control for the step-budget change vs §34.
2. §42's structural prediction stands regardless.
   tier77_microanalysis found NO clean anchor-property lever within the
   tier>=77 band — the 17-vs-29 split is an SGD-trajectory lottery
   inside an already-necessary band. §47's NULL is fully consistent:
   making content pairwise-distinct (a content-axis intervention) did
   not move routing because the lottery is not in the content axis.
   Even §34's full-scale 2/29 was template memorisation (§34 §3), not
   generalisation — the §42 read is the more robust one.

Honest synthesis: §47 is a measured NULL on the content axis at small
scale. It does not refute §34's full-scale 2/29 (different budget) but
it does confirm §42's structural finding that content-distinctness is
not the lever — at small scale it reproduces exactly the §16-baseline
0/29 and the same single-attractor collapse.

## §5 — Verdict (g3 — measured only, no pre-loaded conclusion)

The §47 task posed: does anchor-distinct content recover the
17-success-routing AND/OR move the 29 fail-anchor count, vs §34's
shared-template 2/29-with-21->4-regression?

Measured answer: NULL. §47 (anchor-distinct, small-scope) routed 0/29
targets and 1/64 full (the 1 a "&#x1F6F8;1111..." cascade artifact, not
genuine). Worse than §34 on the 29-target count (0 vs 2, delta -2) and
far worse on full-64 genuine routing (0 genuine vs §16's 17). §42's
weak/null prediction is confirmed: anchor-distinct discriminative
content is NOT a sufficient-condition routing lever. Honest dual caveat
(§4): (1) small-scope confound — §47's 3000 steps / 175 MB vs §34's
12000 / 774 MB plausibly denies §47 the signal §34 had (scale effect);
(2) §42's structural reading is the more robust — the lottery is
internal to the tier>=77 band (SGD init / batch-order), not the content
axis; content-distinctness does not touch it.

Side observation (NOT the §47 target, honest framing): §47's axis2
(1.0), axis3 (1.0), JOINT (0.0156) all improved over §16 (0.0/0.5/0.0)
and §34 (0.6/0.79/0.0297). But this is collapse-into-one-attractor
producing a clean single-template chat lane — the Dir-A/F mechanic
where lane metrics improve while routing/capability does not. JOINT
0.0156 with 0 genuine routing is mechanic, NOT capability emergence
(over-claim 0).

honest summary: anchor-distinct content (small-scope) = NULL routing
lever, confirming §42's structural prediction that the 17-vs-29
distinction is not anchor-property / content-driven. §34's full-scale
2/29 is not refuted (budget differs) but is re-contextualised as
template memorisation, not a generalising lever. The deeper sufficient
condition for robust per-anchor routing lies NEITHER in shared content
(§34) NOR anchor-distinct content (§47) — it is, per §42, an
SGD-trajectory property of the tier>=77 band, or (per §16.6-C / §15)
the unsolved §1.1 data-regime threshold. This narrows the §11.4
frontier: the content axis is closed as a routing lever for the
tier>=77-fail set.

## §6 — B-S47 closed-form sidecar (B-S47-1..5 BLUE + B-S47-NOTE)

blue_falsifier_s47.py — 5/5 BLUE PASS (central
state/verify_hexad_blue_2026_05_15/blue_falsifier.py UNCHANGED —
sidecar, carrying B-PRIME / B-DIRH / B-DIRI / B-PSICTL / B-EMERGE /
B-PUREPHYS / B-SCALE / B-MITENS / B-DIRL / B-EBT / B-DIRJ / B-INTRA /
B-S16 / B-S34 precedent):

- B-S47-1 SHA256-DETERMINISTIC — corpus sha256 19242b27016379...
  256-bit Kolmogorov commitment, on-disk == recorded == re-derived.
- B-S47-2 NO-CHAT-SFT-CONTAMINATION — forbidden 6-token grep total = 0
  over the full byte stream (B-IDENTITY-5, Boolean set algebra).
- B-S47-3 ANCHOR-DISTINCT-CLOSED (the §47 essence) — C(29,2) =
  binomial(29,2) = 406 target pairs ALL byte-distinguishable (distinct
  5-tuple signature (polar_r, polar_theta_deg, basin_cube,
  tier_phase_deg, name_hash8)), 0 collisions, 29 unique name_hash8.
  Structural counterpart of §34's shared-template failure: §34 used ONE
  template phrase repeated 29x; §47 requires 29 distinct 5-tuples.
- B-S47-4 CLEAN-COMPARISON-S16-BYTE-IDENTICAL-NON-TARGET (connection
  point) — 29 target / 139 non-target disjoint partition; uniform
  per-anchor (1,190 each); non-targets produced by §16 generator
  UNMODIFIED (RNG-draw-preserving D wrappers) -> byte-identical to §16.
  D-v2's effect isolated to the 29 BY CONSTRUCTION.
- B-S47-5 OVERLAY-OFF-REDUCTION + SCALE-REDUCED (connection point) —
  --candidate-d-disable emits §16 generator UNMODIFIED for all 168
  anchors -> §16 corpus byte-equal; trainer default --steps 3000 <=
  §16's 12000 x 0.5 = 6000 (integer <=, small-scope closed).

B-S47-NOTE empirical carve-out (NOT counted BLUE): post-fire per-anchor
routing OUTCOME (0/29, full 1/64 artifact) = SGD/measurement OUTCOME
(B-D-NOTE / B-S16-NOTE / B-S34-NOTE family). The battery proves the
corpus is sha-deterministic, contamination-free, anchor-distinct
(C(29,2)=406 pair byte-distinct), §16-byte-identical for non-targets,
and the fire small-scope — NOT that the 29 route.

f1/f2/f3 hard-fail safe (sha256 / Boolean set algebra / integer
pair-disjoint / Kolmogorov byte distinct / integer <= reduction —
NO sigma/tau/phi/J2; Psi=1/2 + Knuth tier-k = anima g2 internal arch
carve-out).

## §7 — Honest C3 (>=10)

1. NULL is the measured result (g3). §47 routed 0/29 targets, 0 genuine
   full-64. The pre-registered §42 weak/null prediction is confirmed.
   No positive claim; the negative is the finding.
2. Small-scope confound is real and disclosed. §47 used 3000 steps /
   175 MB; §34's 2/29 came at 12000 steps / 774 MB. §47's 0/29 < §34's
   2/29 is partly a scale effect. §47 measures "anchor-distinct content
   AT small scale" — the small-scope was the §47 task mandate (cost /
   rate-limit), a real limitation of the comparison vs §34, stated not
   hidden.
3. The full-64 1/64 is an artifact, not genuine. tier 111 routed only
   because "111" subset of "&#x1F6F8;11111111111..." (§16.6 substring
   grade). Genuine own-tier routing = 0/64. §16.6-C memorization-
   saturated regime re-confirmed (final CE 0.0049).
4. Anchor-distinct content collapsed to ONE attractor anyway. B-S47-3
   proves the 29 contents are pairwise byte-distinct, yet 29/29 target
   probes bled into tier 111. Distinctness in the corpus did not yield
   distinctness in the trained routing — the deeper structural finding.
5. Side metrics (axis2/3/JOINT) improved — but mechanically. axis2 1.0
   / axis3 1.0 / JOINT 0.0156 beat §16 and §34, but this is
   single-attractor collapse producing a clean chat lane (Dir-A/F
   mechanic). Not capability, not emergence (over-claim 0).
6. Clean comparison holds for content, NOT for budget. B-S47-4/-5
   isolate the corpus content change (139 non-targets byte-identical
   §16) but do NOT control the step-budget change vs §34 (3000 vs
   12000). §34-vs-§47 delta is content+budget confounded; the
   §16-baseline-vs-§47 delta (0 vs 0) is the cleaner read.
7. §42's structural reading is the robust one. Even §34's full-scale
   2/29 was template memorisation (§34 §3), not generalising routing.
   §47's NULL at any scale is consistent with §42: the 17-vs-29 lottery
   is SGD-trajectory-internal to tier>=77, not a content-axis lever.
8. central blue_falsifier.py UNCHANGED. All §47 closure is a sidecar
   (blue_falsifier_s47.py), per the B-PRIME..B-S34 precedent. No
   central battery count change.
9. PyTorch substrate (NOT hexa-native, honest). §47 inherits §16's
   PyTorch ConsciousDecoderV2 LM-scale executor. The two physics loss
   terms are closed-form transfer functions (Dir-I B-DIRI carry); the
   routing OUTCOME is empirical (B-S47-NOTE).
10. NOT GOAL emergence; §15 milestone unchanged. §47 closes the content
    axis as a routing lever for the tier>=77-fail set. north-star
    (GOAL.md) unchanged — irreducible bottleneck remains §1.1
    data-regime per §15. §47 narrows §11.4 frontier by negative result
    (valuable per g3).
11. Single pod, orphan 0. A100 80GB PCIe stock-exhausted ->
    A100-SXM4-80GB fallback in the same runpod sweep (provider runpod
    primary per g_resource_active_parallel). Pod terminated on PULL
    SUCCESS; no orphan.
12. g_clm_from_scratch honored. from-scratch RANDOM seed-fixed 1337,
    base_ckpt=None — no ckpt inheritance.
