# SPEC — G-0k harness adaptation to the F-6 bin-quantized register (Fable adjudication, 2026-07-18)

> **SSOT**: repo-root `ARCHITECTURE.json` → `next-gate.ladder.g0k-harness` (design tree). This SPEC is a
> read-only seed of record; live design/verdicts are distilled into the tree, never tracked here.

Adjudicates the four design questions for adapting the v4 trunk/probe harness contract to the v5
F-6 panels, BEFORE any compute. v4 sources are cited read-only at file:line
(`anima-v4/state/h004_parser_duel_tension_rank_drill_2026-07-16/`); per the inheritance rule
(anima-v5 CLAUDE.md: verdicts, never code) the v5 harness is FRESH code implementing these contracts —
it never imports `train_h004.py`/`train_g3a.py`. Upstream shared infra (`anima/core/model.py` trunk,
NSMC corpus path) is allowed exactly as v4 used it.

## 0. Verdicts, one line each

1. **Byte→node map**: option (b) — the BUILDER emits `node_spans`; the harness never re-parses.
   Option (a) (substring-in-region re-derivation) becomes the closed-form AUDIT of (b): both
   derivations must agree on every item of every panel of every δ, or the build exits non-zero.
   Filler/prefix/tail bytes → a NULL context id (26) whose struct row is `node_embed` of a zero
   support row = `rmlp(0)` — NOT the v4 default-to-ANS rule, and NOT a literal zeros row.
2. **Probe**: pool ONLY the core CONTESTED_V node (id 4k+1); target = `int(c["hp"])` (the stored
   post-flip = realized surface bit; matches train_g3a.py:356). The ADV/mirror node is EXCLUDED —
   including it makes the pooled 시-content the F-1 constant, not hp.
3. **Support**: item-independent 26-node frame; contested edge per conjunct
   `HEAD_A[4k+1]=4k+2` vs `HEAD_G[4k+1]=4k+3`; the ADV edge is AGREED (→ TAIL) hence support-inert.
   Builder emits `support_edges` (closing the card promise); harness re-derives closed-form from
   `node_roles` and asserts equality (A-sup).
4. **Padding vs learnability**: NOT un-learnable by construction — no fold pre-diagnosis. Filler is
   benign for readout, loss, and probe (mechanisms §5). Cost is compute only (~3.1× tokens/step at
   W=120). A $0 d=64 smoke IS the right cheapest-first gate; green bars in §6.

## 1. Measured findings that change the G-0k plan (name-the-disagreement section)

- **F-A. δ3 = δ4 = δ5 are byte-identical.** Measured this session: surfaces equal across
  drill/f2d/f1d for δ∈{3,4,5} (file MD5s differ only via the embedded `"delta"` field). Cause:
  `order`/`jitter` are declared in `DELTA` (build_deleaked_register.py:120-125) but never read by
  `build_delta`. Further: `jitter` (D=(1,3), variable mirror count) is INCOMPATIBLE with the F-1
  anti-parity audit as designed — the single hp-complement mirror is what pins regional 시-count to a
  constant (build:199, audit build:474-481); extra mirrors change `si_total` per item ⇒ audit fails.
  `order` is already subsumed by the F-5 slot orbit at every δ≥1 (build:207-213). The card promises
  "sweep δ over ≥5 spaced settings" (H5_001 card:68). **Ruling**: differentiate the top rungs on the
  one F-1-safe hardness axis already in the builder — W (filler fraction): δ4 → W=144, δ5 → W=168
  (F stays 4); DELETE the dead `order`/`jitter` keys. This changes δ4/δ5 surfaces ⇒ **G-0 re-runs
  and must re-PASS** (deterministic, minutes, before any training — a build fix, not δ-fishing);
  δ≤3 surfaces must be byte-identical before/after the patch (asserted, §7). Counting δ4/δ5 as
  extra window confirmations while byte-identical to δ3 would have been a fake knee (G5 violation).
- **F-B. CPT is δ-independent ⇒ 2 CPTs total, not 10.** The probe's φ encoder of record is the
  post-CPT NSMC trunk, struct=None, drill NEVER in CPT (train_g3a.py:263-266 `phi_enc` = post-CPT
  frozen copy; g3_0d trains CPT on NSMC windows only, train_g3a.py:346-350, then probes drill items).
  The gate phrasing "train one CPT/seed on the drill" would be a NEW probe definition — the card
  retains "the G3-0d build gate" (card:88), so keep v4's: **one CPT per seed (d=384, 8000 steps,
  512-byte NSMC windows), reused across all δ**; the per-δ probe is a cheap forward + logistic fit.
  Only the CONTROL fit (drill training) is per-δ.
- **F-C. Receptive field ≈ 35 bytes.** kernel 3, dilations 1,2,4,8 (core/model.py:60-63,299) +
  embed_conv + expert conv ⇒ the answer position never saw the regions from surface even in v4
  (~250B items). The field reaches the answer ONLY via the struct injection at the prediction
  position (train_h004.py:147-149). This defuses most padding-dilution worry (§5) and re-confirms
  that a wrong byte→node map is the single point of failure it was flagged as.

## 2. The byte→node map under F-6

### 2.1 Node ids (26 + NULL)

Conjunct k (k=0..5): `ADV=4k` · `CONTESTED_V=4k+1` · `N1=4k+2` · `N2=4k+3`; `TAIL=24`; `ANS=25`.
This matches the emission order of `_node_roles` (build:287-294: ADV appended before
CONTESTED_V/N1/N2). Harness-internal `NULL=26` — never in `node_roles`, never probed, never pooled.
NOTE: node-id order ≠ surface order — the slot orbit puts the core after the mirror half the time
(build:213 `chunks = [mirror, core] if core_last else [core, mirror]`). This is the concrete reason
the v4 eojeol-walk (`_node_of_byte`, train_h004.py:80-93, `assert len(toks)==n` at :85) cannot be
"fixed" in place: position no longer determines role. Spans must come from construction.

### 2.2 Builder emits `node_spans`

Per item: `node_spans = [[start, end, node_id], ...]`, absolute byte offsets into `surface`
(end-exclusive), computed at emit time where every offset is exact by construction:

- region k occupies `[W(k+1), W(k+2))` (audited: A4_geom, build:437-447); within `region_nat`,
  chunk offsets follow from `" ".join(chunks)`; within the core, eojeol offsets follow from
  `f"{vf} {n1}의 {n2}도"`.
- span conventions (v4's each-eojeol-owns-its-trailing-space, train_h004.py:90, carried):
  - CONTESTED_V = `vf` bytes + 1 trailing space; N1 = `{n1}의` + space; N2 = `{n2}도` + space
    (the space always exists: `_pad_to` inserts `" "` before filler, build:109-112).
  - ADV = the WHOLE mirror chunk (4 eojeols incl. `{frame}에서`, internal spaces) + trailing space.
    The mirror's internal nouns/verb are NOT nodes — one clause, one node.
  - TAIL = `mtail` bytes + trailing space (inside `[7W, 8W)`).
  - ANS = the final 3 bytes `"=> "` (the v4 ANS-eojeol analog, train_h004.py:83).
  - Everything else — prefix incl. the scene-setter, all filler adverbs, pad spaces, the space
    before `"=>"` — is UNMAPPED ⇒ NULL. The scene-setter is deliberately not a node: the sealed
    26-node frame has no v4 analog for it and it is label-inert context.
- spans are disjoint, sorted, and cover exactly the non-NULL bytes; `len(spans) == 26` per item
  at δ≥1 (20 at the δ0 anchor, which has no ADV nodes — harness derives arity from `node_roles`,
  never hardcodes 26).

### 2.3 The audit (A-map, closed-form, $0, runs in the build before exit)

Re-derive every span independently and assert equality with the emitted spans:
reconstruct `core = f"{vf} {n1}의 {n2}도"` from conjunct fields (`vf` = `VERBS[k%3]` hf/pf by
`c["hp"]`), `mirror = c["advs"][0]`; search ONLY inside `[W(k+1), W(k+2))`; assert find-count == 1
for each (the same verb form recurs in region k±3 — k%3 stem cycling, build:185 — which is exactly
why the search must be region-bounded); assert reconstructed offsets == emitted; assert coverage/
disjointness; assert TAIL/ANS spans. Any mismatch ⇒ build exit 1. This makes the silent-corruption
hazard (wrong map ⇒ wrong probe ⇒ wrong verdict) a loud $0 failure.

### 2.4 Harness layout (answer region + scatter)

`base = 8W`; `seq = surface + gold_pattern` (answer 18B; `_seq_bytes` contract unchanged,
train_h004.py:172-174). Per-byte node array: init NULL(26); fill from `node_spans`; then the v4
answer rule with the off-by-one lesson carried (train-h004-py-1, train_h004.py:146-158):
`full[max(base+3k-1, 0) : base+3k+3] = 4k+1` for k=0..5 — answer slot k reads conjunct k's
CONTESTED node at its prediction position (v4's `3k` → v5's `4k+1`); later k overwrites the 1-byte
overlap exactly as in v4 (position base+3k+2 predicts slot k+1's first byte).

### 2.5 NULL struct row = `rmlp(0)`, via a zero-padded T

Arm tensors are computed on the REAL 26×26 T first (`_arm_tensor` semantics unchanged,
train_h004.py:65-76; C-plc permutes the 26 real nodes only — NULL stays NULL), then padded with a
zero row+col to 27×27 before `node_embed`. A zero-support node yields h=0 ⇒ `rmlp(0)`
(train_h004.py:112-120), so:
- C-scaf (T≡0) stays EXACTLY position-constant across ALL bytes incl. filler — the v4 wiring
  invariant (train_h004.py:435) carries verbatim;
- filler injection is arm-blind and label-inert (filler bytes are (k,rot)-keyed, build:94-105);
- d_acc readout is untouched: answer prediction positions carry `emb[4k+1]`, same as v4's `emb[3k]`.
Never map filler to ANS (v4's default at train_h004.py:87): ~45% of bytes would pool garbage into
ANS's φ and inject ANS structure across the whole prefix.

### 2.6 φ pooling

`_node_phi` v5: encode SURFACE only (never answer bytes; train_g3a.py:74-88 contract), mean-pool
per real node over its span bytes; NULL bytes enter NO pool. φ shape (26, d).

## 3. The probe (G-0k A2, the retained G3-0d gate)

- **Rows**: per item, per conjunct k: `X = φ[4k+1]`, `y = int(c["hp"])`. The stored `hp` is
  post-F-2-flip (build:179, 224) = the bit the surface realizes = the raw bit the v4 probe read
  (train_g3a.py:356).
- **Excluded**: ADV (4k) — F-1 makes 시 sit on exactly one of {core, mirror} (mirror_hp = 1−hp,
  build:199), so a pool over both sites has hp-INVARIANT 시-content; the probe would measure slot
  order (the F-1 constant), not concord. N1/N2 also excluded (v4 precedent: head node only).
- **Protocol verbatim from g3_0d** (train_g3a.py:352-371): drill[:200] of the δ under test,
  6 rows/item, rng(0) permutation, 70/30 split, logistic probe (Linear→BCE, 500 steps, L2 1e-3),
  bar held-out ≥ 0.90 — **per seed's CPT trunk; a δ passes only if BOTH seeds pass** (G5 "across
  seeds").
- **Report-only diagnostic** (not a gate): a second probe `φ[4k] → 1−hp` should track the main
  probe (same mechanism at the mirror site); divergence flags a span bug. Do not gate on it (no
  new anchors).
- Honest caveats to record with the result: (i) RF ≈ 35B means φ[4k+1] absorbs neighboring-chunk
  bytes — not a pure site measurement (was also true in v4); (ii) F-6a makes hp=1 verb spans
  uniformly +3B, so mean-pooling can carry the bit partly as a span-length artifact — either channel
  counts for A2 ("the bit is linearly present in φ"), but say so.

## 4. Support / `support_edges` for [ADV, CONTESTED_V, N1, N2]

Item-independent (the frame never varies at δ≥1); v4 3-node source: build_tension.py:34-42 and
g1_core_check.py:29-30,141-150.

```
HEAD_A = { 4k+1: 4k+2,  4k+2: 4k+3,  4k+3: 24,  4k: 24,  25: 24 }   # k = 0..5
HEAD_G = { 4k+1: 4k+3,  4k+2: 4k+3,  4k+3: 24,  4k: 24,  25: 24 }
```

- The ONLY disagreement is the RC edge (CONTESTED_V: N1 vs N2) — one contested edge per conjunct,
  as sealed. The ADV adjunct attaches AGREED to the matrix verb (TAIL): ruling — the registered
  ambiguity family is the RC-attachment duel only; making the adjunct contested would double the
  contested-edge count and change the sealed field format (a second lever). Agreed edges vanish in
  `t_struct` (g1_core_check.py:32-40 skips ha==hg), so ADV is support-inert by construction.
- hon vector: `hon[4k+1]=hp, hon[4k+2]=pos1, hon[4k+3]=1−pos1, hon[4k]=0.0` (field-inert: zero
  support row; χ is never sampled there, and the later χ̂ is support-masked, train_g3a.py:125).
- Preserved consequences (assert in the audit): T has exactly 6 contested rows;
  `offtop(t_struct) = 5/6` (v4 [C], g1_core_check.py:9-14); per-conjunct the field collapses to
  `s_k = 1 − 2·gold_k` at cells (4k+1,4k+2)=(+s) and (4k+1,4k+3)=(+s after χ) — the same one-scalar
  algebra as v4 [B] (g1_core_check.py:108-112).
- **Emission**: builder emits per-item `support_edges = {"head_a": {...}, "head_g": {...}}`
  (string keys — JSON), closing the card's promise. **A-sup audit**: harness re-derives the maps
  closed-form from `node_roles` alone and asserts equality per item, then asserts the two numeric
  consequences above.
- Free slots / GF(2) rank / ceiling: recomputed per panel exactly as already audited in the build
  (build:384-414, 453-459); the harness recomputes per panel at load (G3), never imports a set.

## 5. F-6 padding vs learnability — why there is no $0 fold pre-diagnosis

Three mechanisms, each grounded:

1. **Readout**: RF ≈ 35 bytes (§1 F-C) — the answer position could not read the regions from
   surface even in v4; the binding signal arrives via the struct injection at the prediction
   position (train_h004.py:147-149). Filler cannot dilute a path that was never surface-borne.
   The last ~35 bytes before the answer are tail filler + `" => "` — label-inert by construction.
2. **Objective**: `ce_surf` and `ce_ans` are separately mean-normalized and combined as
   `ce_surf + λ·ce_ans` (train_h004.py:368-373) — the loss geometry is L-invariant; the run-1
   dilution failure (train_h004.py:289-293) does not scale back in with longer items.
3. **Probe**: pooling is site-local (~9-12B span, 시 inside it); prefix/filler never enter the pool.

So no CPT-budget or d scaling is REQUIRED by construction. What long items DO cost: compute
(pad 320 → 8W+32: 800/992/1184/1376 for W=96/120/144/168 ⇒ ~2.5-4.3× tokens per drill step), MPS
memory (pre-register bs 16→8 NOW if needed — before data, not after), and two note-only unknowns:
optimization at longer L, and GroupNorm's sequence-global stats at eval L ≠ CPT window 512 (v4
also evaluated off-window-length at ~250B). These are empirical — exactly what the smoke and the
control bars measure. **No mechanism predicts probe < 0.90 or control < 0.95 by construction ⇒
G-0k must be run, not folded on paper.**

## 6. Staging — cheapest first

**Stage 0 — builder patch + G-0 re-run ($0, minutes).**
Patch `build_deleaked_register.py`: (a) emit `node_spans` + `support_edges`; (b) A-map + A-sup
audits added to the build's exit-blocking checks; (c) DELTA: δ4 W=144, δ5 W=168, delete dead
`order`/`jitter` keys; (d) regression guard: δ≤3 surfaces byte-identical to the committed
artifacts (compare against the existing `*_d{0..3}.json` before overwriting; any drift ⇒ exit 1,
because G-0's census PASS is pinned to those bytes). Re-run → must exit 0 (census re-certified at
the new δ4/δ5 W).

**Stage 1 — $0 smoke (d=64, δ1 only, CPU/MPS, ~20 min).** Green bars:
- S1 (already exit-blocking in Stage 0, re-asserted here): A-map/A-sup exact on ALL items, ALL
  panels, ALL δ.
- S2 WIRING-4 analog (train_h004.py:449-460): A-hand-analog overfits 16 drill-δ1 items × 600 steps
  at d=64 ⇒ drill-subset d_acc ≥ 0.9. THE injection/alignment liveness check at L=786 — a wrong
  map or answer-rule off-by-one fails here for $0, not after the d=384 sweep.
- S3 probe plumbing end-to-end at d=64: runs, emits a number — REPORT-ONLY, no bar (G1: no anchors
  from a smoke; H_007's d=64→384 inversion).
- S4 C-scaf struct position-constant, verbatim v4 check (train_h004.py:435) — certifies §2.5.

**Stage 2 — G-0k full (d=384, MPS).** Pre-registered NOW, before any training data:
- 2 CPTs (seeds 0,1; 8000 steps, 512-byte NSMC windows — v4 g3_0d config), checkpointed once and
  reused across δ (F-B). Declared deviation from v4's monolithic per-arm RNG stream: drill fits
  resume from the seed's CPT checkpoint (same weights, different RNG draw order than a monolithic
  run — acceptable, declared here).
- Per δ, ascending δ1→δ5, per seed: (i) probe (cheap; §3); (ii) CONTROL = A-hand-analog drill fit
  + C-perm harness co-certification at TARGET scale d=384, bars carried from fit_check
  (train_h004.py:599-604): A-hand drill d_acc(free) ≥ 0.95 both seeds AND spread ≤ 0.03;
  ce_ans < 0.05 both; C-perm drill-vs-true-gold ∈ [0.40,0.60] AND f2d held-out ∈ [0.45,0.55] AND
  teacher-forced parity slots ≥ 0.9. (Heuristic-chance is certified ONLY jointly — G2.)
- δ PASS = census (pinned at G-0) AND probe ≥ 0.90 both seeds AND control bars. Window = ≥2
  CONSECUTIVE δ PASS; δ* = the easier (lower) of the two. Pre-registered early-stop: ascending
  order, stop after 2 consecutive PASS (a measured knee, declared before data). No window after
  δ5 ⇒ K-fold-1 fires (the mount/fold referee).
- Cost: 2 CPT + up-to 2 seeds × 5 δ × 2 arms × 1500-step drill at 2.5-4.3× v4 token cost ≈ 6-9h
  MPS wall-clock (the card's ~5h is the floor if the window closes early at δ2).

**Files**: builder patch in place (`state/h5_001_g0_deleaked_register_2026-07-18/`); new
`state/h5_001_g0k_window_precheck_2026-07-18/train_g0k.py` (+ the smoke entry) — fresh v5 code per
the inheritance rule; experiment-local, not `tool/` (item-specific, not a shared primitive).

## 7. What this spec refuses

- No harness-side re-parsing as the source of truth (it is the audit, §2.3).
- No probe over {core ∪ mirror} (§3), no probe bar from the d=64 smoke, no third seed, no
  δ-midpoints, no re-tuning any dial after Stage 2 data exists.
- No counting δ4/δ5 as window confirmations while byte-identical to δ3 (fixed at Stage 0 instead).
- No import of v4 code; no inherited free-slot set; no inherited 0.667 ceiling (recomputed §4).
