# H5_001 G-0 — F1: the gold 0.667 "floor" is the SAME straddle class (bar stays 0.5+ε, no codebook change) · F2: conjunct-scramble REJECTED, the op is BIN-QUANTIZED LAYOUT (Fable 5, 2026-07-18)

> **SSOT**: `ARCHITECTURE.json` → `defect-encoding` · `lever.g0-construction`. Seed of record,
> read-only after ratification. Ruled against HEAD 70b4b37 with the builder RE-RUN in place
> (the committed `g0_verdict.json` was stale — pre-F-5 numbers; the re-run regenerated
> `{drill,f2d,f1d}_d*.json` + `g0_verdict.json` to HEAD truth; commit them in lockstep).
> All numbers below are from that re-run or from the measurement snippets in §1/§2 (rerunnable
> against the committed `f2d_d1.json`/`f1d_d1.json`).

## 0. The two calls in one paragraph

**F1 — the census bar stays ≤ 0.5+ε on ALL 18 targets, gold included** (panels ε = 1/48 = 0.0208,
drill ε = 1/128 = 0.0078, exactly as SPEC §5 registers). The proposed per-family split
(gold at ceiling 0.667+ε) is REJECTED on a measurement: the 0.6667 gold entries are NOT the
codebook's field-blind completion — they are the SAME residual posbin-straddle class at partial
strength, and they die with the same fix. Crucially this does NOT force the codebook change the
fork feared: the F-2 orbit indeed cannot balance gold (diagonal verified, §1), but gold balance
never needed the orbit — it needs (a) supports closed over complement-pairs (already installed by
the A4 balanced-subset fix) and (b) label-inert bin geometry (the F2 recipe). **F2 — conjunct-order
permutation is REJECTED** (out of SPEC §2.3's license and A2-fatal on held-out panels, §3.1);
K-fold-1 is NOT indicated — the answer-adjacent edge is delocalizable because the e-bins pin region
5's byte INTERVAL (label-independent, measured) and only the boundary∩window incidence leaks. The
op that closes the whole class exactly, solver-free, is **F-6: bin-quantized layout** — pad every
region to exactly L/8 bytes so every bin boundary coincides with a region boundary; then every
(g,bin) key degenerates to a per-region presence key, which the F-2×F-5 orbit already balances
exactly (§3.2). δ then dials variety inside a fixed bin frame, and §10.1's "census PINNED at every
δ ≥ 1" becomes constructively true — including δ1/δ2.

## 1. F1 — the measurement that settles it (rerunnable)

1. **Diagonal confirmed**: per (msg,k) on committed f2d_d1, the 8-orbit realizes exactly 2 of 4
   (hp,pos) combos — {2: 144}, e.g. msg (0,0,0) k=0 → {(1,1),(0,2)}. The user's verification is
   correct: ι preserves hp⊕(pos−1), so the orbit moves inside gold's level set and can never
   balance gold. (The builder comment at `build_deleaked_register.py:233-236` claiming "all 4
   combinations" is WRONG as written — fix the comment with the build.)
2. **But the 0.6667 keys are straddles, not structure.** The f1d top gold key (posbin, gram
   […도], s3 → gold_2, support 48, score 0.6667 exactly) has support covering ALL 8 panel messages
   with orbit counts {gold_2=0 msgs: 8/8 items, gold_2=1 msgs: 4/8}. Score = 32/48 = 2/3 — an
   8-vs-4 ORBIT-SPLIT number (bin membership is orbit-constant for one diagonal class and
   slot/flip-dependent for the other), not (4·0.5 + 2·1.0)/6. The equality with the ceiling is a
   numeric coincidence.
3. **The slot pattern says the same**: gold floors sit on gold_2/3/5 with gold_0/1/4 at 0.5000
   EXACT (f2d and f1d both). The codebook-completion story would floor the determined slots {3,5}
   and free the free slots {0,1,2,4}; the measured pattern instead tracks which regions have a
   boundary in a sensitive window. gold_2 is a FREE slot at 0.6667 — under the proposed
   ceiling-bar, a field-blind read of a free slot at 2/3 would have been WAVED THROUGH while
   eating exactly the headroom the G-1 arithmetic (C-trained f2d ≤ 0.80, A-hand − C-trained ≥
   0.20) needs. That is the H_005 shape — a gram beating structure — not the code's own completion.
4. **Ruling**: one bar, all 18 targets, per SPEC §5 verbatim. No per-family split, no codebook
   replacement, no second lever. Pre-registered escape (ADJUDICATION §4 pattern, carried): if
   AFTER F-6 a gold family survives > bar with a decoded support that is provably orbit- AND
   pair-CLOSED, that specific gram is structural fold evidence — bring it back with byte decode +
   support. Prediction: post-F-6 gold census = 0.5 exact up to odd strata (the current 0.5000s on
   gold_0/1/4 already show the pair-closure machinery pins gold wherever geometry is inert).

## 2. The residual class, mechanically (why edges, why δ-invariant)

- δ3–δ5 are byte-identical to δ1 because `_emit_one` reads only `conf["D"]`; `order`/`jitter`
  are wired only into the dead `_adv_pool`/`_adv_clause` path (never called by `build_delta`).
- Geometry facts (measured, f2d_d1, rot 0): region starts are label-STABLE singletons
  (0/79/155/237/316/392); L = 490 constant; chunk1 byte-length varies {29,42}/{32,45}/{35,48}
  with (slot, si-of-chunk1) — i.e. all label-dependent variation is INTRA-region.
- The pos_4 = 1.0 key ([의␣동-head], s6): occurrence offset 380 when pos_4=1 vs 367 when
  pos_4=2; the s5/s6 boundary is at 6·490/8 = 367.5. Bin membership IS the label — support 32/0.
  Same anatomy for hp_1/hp_5/pos_0 (s-side) and the drill's larger set (frame_id × rot grids put
  more boundaries into more windows). Middle conjuncts were partially smeared by slot⊥flip only
  because their windows happen to straddle less; that is luck, not construction.

## 3. F2 — the delocalization ruling

### 3.1 Conjunct-order permutation: REJECTED (do not build it)

- **License**: SPEC §2.3 licenses ADJUNCT scrambling only — "the contested core stays contiguous
  and order-frozen"; conjunct-level permutation was never a registered op.
- **$0 pre-diagnosis (the H_008-cliff shape on the order axis, stated without spending)**: with
  logically-indexed targets, a permuted surface carries NO recoverable logical index on f2d —
  the only k-correlates are the (k+rot)-keyed lexeme assignments, and the held-out pools' index
  order is unlearnable from drill by construction ⇒ A-hand itself collapses on the panel (the
  task becomes un-posed, worse than an A2 cliff). With surface-indexed targets, the permutation
  changes nothing: the straddle read is (geometry ↔ label-of-the-region-at-that-bin) and is
  index-free. Either way the op buys zero census and risks the comparator.

### 3.2 The accepted op — F-6 bin-quantized layout (exact, solver-free)

**Invariant**: every item satisfies L = 8W bytes with byte-intervals
`[0,W) = matrix prefix · [W·(k+1), W·(k+2)) = conjunct region k (k=0..5) · [7W, 8W) = tail+" => "`.
Every s-boundary ⌈mL/8⌉ = mW and every e-boundary L−mW then coincides with a region edge
(L ≡ 0 mod 8 makes both bin systems share the same 7 interior points), so NO boundary cuts any
region interior. Consequences, closed-form:

- A (g, s/e-bin) key degenerates to "g occurs in region r" — a per-region presence key. Region
  content as a chunk-multiset is exactly balanced by the existing F-2 (flip) × F-5 (slot) orbit
  at every k, and support selection by lexeme/geometry is (k,rot)-keyed = whole rot-groups =
  complement-pair-closed (bal24 groups are 4 pairs each; f1d = 4 pairs; drill = all 64 = closed).
  So every (g,bin) support is a union of pair×orbit blocks and slot-halves — all 18 targets
  exactly 0.5 on it. The intra-region ±3/±6/±13B label-dependent shifts become bin-INERT: content
  moves inside its own bin, never across a boundary.
- The 'a'-anchor key stays trivially safe (only the tail sits after "=> "); char-len is constant
  per geometry class and ⊥ gold (§3.3 keying), satisfying the SPEC §2.4 A4 assert.
- **Edge answer (fork question 2)**: pos_5/hp_5 are NOT un-delocalizable. e-bins and the "=>"
  anchor pin region 5's INTERVAL — which is label-independent (measured stable) — not its labels.
  Adjacency to "=> " is geometry, and geometry is now everywhere label-inert. No K-fold-1 here.

**Builder recipe (δ-dial preserved, all keys deterministic):**

1. **F-6a uniform 시-width**: replace 웃 (consonant stem, 으시 = +6B) with a vowel stem
   (만나/보내-family: 시 = +3B uniformly) in `VERBS`. Register machinery — in-lever. Shrinks every
   sensitive span; not load-bearing after quantization but cheap insurance + simpler padding
   arithmetic. (Optional F-6a′, NOT required: 3-syllable plain argument pools to kill the ±3B
   noun-order shifts — a pool amendment needing ratification + native pass; skip unless padding
   arithmetic wants it.)
2. **F-6b quantization**: per (panel, δ, geometry class), W = max natural region width + padding
   headroom; pad each region to exactly W bytes via frame-word length choice (2- vs 3-syllable
   frame pools) plus a block-keyed filler adverb inside the MIRROR chunk (never the core — core
   stays byte-frozen); prefix = one W-byte matrix scene-setter (licensed by SPEC §2.3
   "matrix-level adjuncts in frame-defined positions"); tail padded to W including " => ".
   **A4_geom assert (exit-blocking, closed-form)**: per item, `len == 8·W` and region k's byte
   interval == [W(k+1), W(k+2)) exactly; boundary set ∩ region interiors = ∅ by construction.
3. **F-6c keying discipline (the balance answer, fork question (b))**: scramble/jitter must NOT
   be orbits over labels and must NOT key on mi/msg (measured: mi-keyed frame counts read gold at
   1.0) nor on flip/slot (they correlate with realized hp/pos). Key every geometry choice —
   prefix content, frame lengths, filler, D_k, adjunct rotation — on **(k, rot, complement-pair
   index)** only, CONSTANT on each pair×8-orbit block of 16 items. Then geometry is identical
   within every block, blocks are gold/hp/pos-balanced internally, and every census support
   decomposes into balanced unions. Label balance stays where it lives: the flip×slot orbit.
   The permutation needs no orbit of its own.
4. **F-6d the dial**: δ1/δ2 = quantized fixed layout (now constructively census-clean — §10.1
   restored; no build-infeasibility retreat needed); δ3 adds intra-region adjunct-slot scrambling
   (D=2: mirror + one F-5-closed adverbial, rotation pair-keyed); δ4/δ5 add geometry-class
   multiplication (D_k ∈ {1,2}, prefix/frame variation — all pair-keyed, W re-solved per class).
   Extra (non-mirror) adjuncts carry 시 on a block-constant schedule that keeps the regional
   시-count CONSTANT (simplest: always plain; `anti_parity_si_constant` audits it unchanged).
5. Fix the wrong orbit comment at :233-236 (diagonal, not 4-combo) and delete the dead
   `_adv_pool`/`_adv_clause` path with the build.

### 3.3 Fallback + sharpened fold criteria

If the native pass vetoes W-scale padding material (prefix ~60-80B scene-setter, frame variants),
the fallback is the ADJUDICATION2 §2 steering solver (choose per-geometry lengths so no boundary
lands in a sensitive window — feasible-looking at ~2 3B-windows/region but NOT guaranteed; the
solver run is the $0 measurement). K-fold-1 evidence, post-F-6, is exactly: (1) quantization AND
steering both native-vetoed or infeasible at every δ; (2) a surviving > bar family whose decoded
support is orbit- and pair-closed (§1.4); (3) G-0k finds no ≥2-consecutive window — the gate's own
referee, untouched. The current 4 edge leaks + gold floors are NONE of these: they measure the
emitter's distance from a layout invariant no one had yet registered.

## 4. Record

- Re-run of HEAD 70b4b37 confirms: f2d worst 1.0, 1.0-targets [hp_1, hp_5, pos_0, pos_4],
  byte-identical δ1..δ5; f1d worst 0.6667 with zero 1.0s; A4 f2d/f1d = 0.5000; free [0,1,2,4],
  rank 4, ceiling 0.6667, si-constant [1], unit-test CAUGHT — all as the fork stated. The stale
  committed artifacts were regenerated in place; commit with the F-6 build (changelog lockstep).
- G-0k decision rule, panel sizes, ε arithmetic, key family: all untouched. No new δ, no new seed.
