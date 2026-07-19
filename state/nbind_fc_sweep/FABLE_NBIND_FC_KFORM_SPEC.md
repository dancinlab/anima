# NBIND-FC K-form expansion — Fable decision-grade spec (2026-07-12)

Design for the negation Form-Coverage sweep: F2 (lexeme-novel flip1) as a function of K
(number of drilled flip1 negation form-families), fixed data budget. Grounded in the live
pod code (/workspace/nbind/gen_nbind.py + build_nbind_fc_eval.py, pod 44562888).

## 0. Axis + unit fix (read first)

- K ≡ **count of flip1 negation form-families drilled** (surface-family granularity, same
  granularity as the existing grid's 3: negL/negS/negE). The existing "K=6" ckpt is K=3 in
  these units (6 = total forms incl flip0). Sweep = fresh K∈{3,12,24} × 2 seeds; the fresh
  K=3 arm is a byte-protocol replication of A2seed → regression anchor (expect F1≈0.70,
  F2a≈0.20 at seed 4302).
- flip0 side FIXED at 3 forms (bare/정말/너무) at every K; flip marginal 0.5 held by row
  weighting (see §3). Only flip1 family diversity varies.
- Secondary covariate L = distinct negator LEXEME classes: K=3→L=2 {않,안} · K=12→L=10 ·
  K=24→L=10 (K24 adds surface variants only). Designed contrast: lexeme-diversity effect
  shows at 3→12; raw-surface-count effect shows at 12→24.

## 1. Family inventory (trained ≤24 + reserved 2)

All renders are **concatenation-only on non-past stems** (mining already excludes ㅆ-past
stems) — template = PRE + BASE + POST, BASE ∈ {stem s, attested eojeol e}. No jamo
composition, no irregular handling needed. Excluded for morphology (need ㄹ/ㄴ adnominal +
irregular stems): -ㄹ 리(가) 없다, -ㄴ/은 게 아니다, -ㄹ 턱이 없다, -ㄹ 리 만무하다.

Nested order is FROZEN: K=3 = ids 1–3, K=12 = ids 1–12, K=24 = ids 1–24.

| # | id | render (PRE+BASE+POST) | base | lexeme | note |
|---|----|------------------------|------|--------|------|
| 1 | jian | s+"지 않다" | s | 않 | existing negL |
| 2 | an | "안 "+e | e | 안 | existing negS (e may be conjugated/past — grammatical) |
| 3 | jeonhyeo | "전혀 "+s+"지 않다" | s | 않 | existing negE |
| 4 | sueop | s+"다고 할 수 없다" | s | 없 | quotative periphrasis; verbs colloquial -다고 OK |
| 5 | bogi_eoryeop | s+"다고 보기 어렵다" | s | 어렵 | attenuated neg → still flip1 |
| 6 | bogi_himdeul | s+"다고 보기 힘들다" | s | 힘들 | |
| 7 | keonyeong | s+"기는커녕" | s | 커녕 | elliptical fragment — fine for byte drill |
| 8 | geori_meol | s+"다는 것과는 거리가 멀다" | s | 멀 | longest form (byte-drift report) |
| 9 | geon_anida | s+"다는 건 아니다" | s | 아니 | hedged/partial negation, gold still pol^1 |
| 10 | teullyeo | s+"기는 틀렸다" | s | 틀렸 | prospective; colloquially OK on evaluatives |
| 11 | geulleo | s+"기는 글렀다" | s | 글렀 | ditto |
| 12 | byeollo_jian | "별로 "+s+"지 않다" | s | 않 | NPI |
| 13 | bolsueop | s+"다고 볼 수 없다" | s | 없 | surface variant of 4 |
| 14 | jineun | s+"지는 않다" | s | 않 | contrastive long-form |
| 15 | jiga | s+"지가 않다" | s | 않 | emphatic colloquial |
| 16 | gyeolko_jian | "결코 "+s+"지 않다" | s | 않 | NPI, formal |
| 17 | jeoldae_jian | "절대 "+s+"지 않다" | s | 않 | NPI |
| 18 | geudaji_jian | "그다지 "+s+"지 않다" | s | 않 | NPI |
| 19 | geuri_jian | "그리 "+s+"지 않다" | s | 않 | NPI (chosen over 도무지/통/좀처럼 — those prefer eventives) |
| 20 | jogeumdo_jian | "조금도 "+s+"지 않다" | s | 않 | NPI strong |
| 21 | hanado_jian | "하나도 "+s+"지 않다" | s | 않 | NPI, very natural in reviews |
| 22 | ttakhi_jian | "딱히 "+s+"지 않다" | s | 않 | NPI |
| 23 | jeonhyeo_an | "전혀 안 "+e | e | 안 | NPI×short-form |
| 24 | hanado_an | "하나도 안 "+e | e | 안 | NPI×short-form, extremely common |

Spares (swap-ins if a family collides/fails audit): byeollo_an "별로 안 "+e ·
jeoldae_an "절대 안 "+e · hagi_eoryeop s+"다고 하기 어렵다".

**RESERVED — never trained at any K (F2 verdict panels):**
- **F2a mos**: "못 "+e — [못]. Continuity yardstick (K=3 anchor already measured 0.200).
  Grammaticality caveat: 못+adjective is nonstandard Korean → biased toward FAIL; that is
  why it is SECONDARY.
- **F2b ji_mot**: s+"지 못하다" (+conjugations 지 못했다/지 못해요/지 못하네/지 못함) — novel
  negator lexeme [못하] inside the TRAINED scaffold slot (X지 __다). Grammatical with
  evaluative adjectives (아름답지 못하다-type; mildly odd pragmatically for pol=0 stems —
  report acc split by pol). **PRIMARY verdict axis**: sharpest test of slot-abstraction.

Byte-disjointness is defined at the **syllable level** (full UTF-8 triples; Hangul blocks
trivially share lead bytes — 안 EC9588 vs 않 EC958A share EC95; 못 EBAABB is fully
disjoint). Guarantee needed: syllable 못 appears NOWHERE in any train line at any K.

## 2. Generator deltas (gen_nbind.py)

1. Replace NEG_FORMS with a FAMILIES table: `(id, flip, base∈{"s","e"}, pre, post)` —
   flip0 rows unchanged (bare/정말/너무), flip1 rows = frozen table above. `render()`
   becomes `pre + (stem if base=="s" else span_eojeol) + post`.
2. `--K {3,12,24}` CLI flag; flip1 set = first K table rows (nested). K recorded in
   AUDIT.json meta.
3. Latin-square holdout: `held[p] = {flip0[i%3], flip1_K[i%K]}` (unchanged shape; 2 held
   cells/predicate, 1 per flip class).
4. Rep allocation (fixed budget): per predicate flip0 = 2 trained cells × 12 = 24 rows;
   flip1 = 24 rows over (K−1) trained cells: base ⌊24/(K−1)⌋ + remainder round-robin,
   rotation offset by predicate index i so per-FAMILY corpus totals equalize (audit field:
   per-family total within ±10% of mean). K=3→12/cell (byte-protocol = A2seed), K=12→2/cell
   +2 rot, K=24→1/cell +1 rot. Total main rows/arm = P×48 = identical to A2seed.
5. Ctrl twin: unchanged machinery (independent coin per trained cell, seed+1000).
6. New asserts (extend audit): **V-F2** = 못 syllable absent from every main+ctrl line AND
   from every plist stem/eojeol (drop 못-containing stems e.g. 못생기 at mining); report
   (not assert) stems containing 안/않; assert no plist stem equals a negator content
   lexeme stem {없, 어렵, 힘들, 멀, 틀리, 그르, 아니}? — NO: report-only (재미없/안타깝
   are legitimately in-pool; only the 못 guarantee is validity-bearing). Existing
   V-C/V-D'/V-E/V-F/V-G/COGS run unchanged with dynamic K (COGS: flip1 trained ≥2 ✓ at K=3).
7. Byte budget: rows exactly fixed; bytes drift (long periphrastics) ≈ +10% at K=24 —
   report bytes_main per arm; training steps FIXED across arms (same protocol as A2seed);
   drift is a reported covariate, bound ≤ +25% else flag.

## 3. Eval panels (freeze once, reuse across ALL arms — plist mining is deterministic, so
panels are seed-invariant)

- **F1** (conjugation-novel, trained-stem 않): existing manifest byte-identical
  (않아요/않았다/않네). Still surface-held at all K (all trained 않-forms end "않다").
- **F2a** (lexeme-novel, 못+e): existing manifest + n-boost to 3 attested spans/predicate
  (~100 items).
- **F2b** (slot-novel lexeme, s+지 못하다 ×5 conjugations): NEW manifest (~170 items).
  **$0 backfill required before the sweep**: run F2b (+boosted F2a) on existing
  nbind_A2seed{,_ctrl}.clm → K=3 anchor for the primary axis. Pod is UP; no training.
- **GRID** (per-arm within-grid held-out cells + seen): per-arm generator output — V1
  liveness + memorization check, unchanged --xbind protocol (gen 8, win 64, n 200).
- Power: F2b n≈170 → se≈0.038/arm; Δ=0.15 ≈ 2.8·se, ~0.85 power per seed (pre-registered
  MDE per probe-defect-census rule; no max-of-controls anywhere — all comparisons are
  main-vs-own-ctrl or main-vs-own-K3, paired by item where applicable).

## 4. Frozen bars (registered NOW; 1 byte immutable post-fire)

Per-arm validity gate (else that K point = VOID, not FAIL):
- gen AUDIT ALL_PASS, and **V1 liveness**: GRID held-out D-acc(main) ≥ 0.65 AND
  main − ctrl ≥ 0.20 (per-K ctrl where trained; K=3 uses backfilled A2seed_ctrl).
  If K=24 fails V1 → verdict INVALID-BUDGET (coverage/depth tradeoff below learnability),
  fire contingency (§6), do NOT count as ceiling FAIL.

Verdict on **F2b flip-acc over fresh K∈{3,12,24}**, both seeds independently:
- **PASS (coverage-limit · crack-able)**: non-decreasing over K (tolerance −0.05) AND
  F2b(K24) − F2b(K3) ≥ +0.15 AND F2b(K24) main − ctrl(K24) ≥ +0.15. (Both seeds.)
- **FAIL (surface-invariant-binding ceiling · terminal candidate)**: all arms V1-live AND
  F2b(K24) − F2b(K3) ≤ +0.05 AND F2b(K24) main − ctrl(K24) ≤ +0.05. (Both seeds.)
  Scope: 303M, this budget/scale — a_scale_honest_scope.
- Anything else = DIRECTIONAL/MIXED (e.g. rise but still ≤ ctrl = unbinding-without-flip;
  seed split; F2a/F2b divergence). Note: main−ctrl clause already blocks the false-PASS
  where acc rises 0.20→0.35 but stays below the ctrl's ~0.45.
- F2a reported with identical clauses as SECONDARY (its K3 anchor = 0.200 measured;
  ungrammatical-form caveat noted in verdict).
- Tracked, non-verdict: F1 ≥ 0.60 at all K (drop with K → capacity-dilution flag);
  F2b acc split by pol (pragmatic asymmetry check); L covariate readout (3→12 vs 12→24
  slope shape = lexeme-diversity vs surface-count attribution).

## 5. Runs (8 fires + 1 optional, single dedicated 4090 pod ≈1.6h/run)

| run | arm | seed | panels |
|-----|-----|------|--------|
| 0 | $0 backfill on A2seed{,_ctrl} | — | F2b, F2a-boosted |
| 1–2 | K=3 main | 4302, 9011 | GRID+F1+F2a+F2b |
| 3–4 | K=12 main | 4302, 9011 | 〃 |
| 5–6 | K=24 main | 4302, 9011 | 〃 |
| 7 | K=12 ctrl | 4302 | 〃 |
| 8 | K=24 ctrl | 4302 | 〃 |
| (9 opt) | K=3 ctrl fresh | 4302 | purity replication of A2seed_ctrl |

Cost ≈ 13–14.5h sequential on the UP pod (~$5); halve wall by renting a 2nd dedicated pod
(a_wall_first; pod-dedicated-host rule — no host sharing). Run-1 (K3 s4302) must
reproduce F1≈0.70/F2a≈0.20 (±0.08) else generator-regression stop-the-line.

Contingency if K=24 V1-VOID: fire K=18 (drop ids 19–24) same budget, OR 2×budget K=24
(labeled off-curve, budget-confounded — report separately).

## 6. Implementation checklist (executor)

1. gen_nbind.py: FAMILIES table + --K + rep-rotation + V-F2 못-scan + per-family-total
   audit (§2). Smoke: --smoke at K=3/12/24, AUDIT ALL_PASS ×3.
2. build_nbind_fc_eval.py: add F2b (5 conj) + F2a 3-span boost; echo-guard unchanged;
   freeze manifests, sha256 into AUDIT.
3. Backfill run 0 → cement K3 anchors.
4. Fire runs 1–8, eval, slope table, verdict per §4 bars verbatim.
5. Register H (2 surfaces) + land code in state/nbind_fc_sweep/ via pr-cycle.
