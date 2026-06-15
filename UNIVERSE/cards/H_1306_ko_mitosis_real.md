---
id: H_1306
slug: 1306_ko_mitosis_real
title: ko-mitosis — FIRST engine-native Korean mitosis-training rung on a REAL Korean web corpus (KO next-byte CE drops + English retains, no catastrophic forgetting)
group: MITOSIS-ENGINE (p8 structural)
terminal_tier: 🟢 GREEN ENGINE-NATIVE (FIRST CPU rung on REAL Korean; KO next-byte CE dropped 3.611→3.249 as engine_mitosis_tick grew 2→9 cells, English held 4.864→4.752 = no forgetting; live CORE/engine_cli.hexa VAdaptField Voronoi + mitosis tick, gradient-free p8)
verdict_dir: .verdicts/1306_ko_mitosis_real/
terminal_verdict: .verdicts/1306_ko_mitosis_real/H_1306.txt
date: 2026-06-16
---

# H_1306 — Korean mitosis-training on a REAL Korean web corpus (engine-native, first rung)

## Claim / falsifier

The user's standing goal, now triggered ("303M 에 미토시스로 한글학습 시작"): feed a **REAL
Korean byte stream** to the engine and, where the trunk/cells are WRONG on Korean
next-byte, **MITOSIS-GROW a new cell** (gradient-free, error-targeted) — the H_1297
mechanism, made literal on real data (p8). **LOAD-BEARING claims:** (1) Korean next-byte
CE **DROPS** as mitosis grows cells on more Korean (learning happens); (2) English
next-byte CE is **RETAINED** (does NOT regress) while Korean improves — the H_1300
catastrophic-forgetting property, now on REAL data; (3) mitosis actually **GROWS cells**
for Korean. Neurogenesis lens (a_no_llm_frame_trap) — NOT a bigger-transformer recipe.

**DISTINCT from H_1297 R4** (the toy that this scales): H_1297 ran on a ~2 KB **hardcoded**
KO+EN string (provenance-in-script) and asked whether gradient-free mitosis MATCHES
gradient + whether error-targeting fires (c2 shuffle). H_1306 asks the **scale + retention**
question on a REAL Korean web corpus: does the SAME engine-native mechanism LEARN Korean
next-byte structure on real crawled text AND retain English? Toy-match ⊥ real-corpus-learn.

## Method (FIRST CPU rung, $0, NO GPU, engine-native, frozen-first c9)

**Corpus — REAL, NO synthetic Korean (p1-p8, a_eeg_consciousness_record spirit):** a
modest slice of the existing anima-7b 5-lang web corpus pulled from Cloudflare R2 (bucket
`phanes`, prefix `anima-7b/web/`) via HTTP range (a few MB, NOT the 9.8 GiB shards):
- **KO** = `kor/shard0000.bytes` bytes[0:4194304] trimmed[:600000] — 600000 bytes,
  sha256 `e000d08684167c78ea9b7799c0b6d32377bcb3f39d0c4e87effe35ff8361dbd1` (~80% of bytes
  are Hangul multibyte UTF-8 sequences; ~5% ASCII English — a real crawl).
- **EN** = `eng/shard0000.bytes` bytes[0:2097152] trimmed[:300000] — 300000 bytes,
  sha256 `dbfe3c1c89af9e87aa5e55e7d969666dffde6165f0044b1cf77b3f2fc1d38c85`.
- Fetched by `UNIVERSE/h1306_fetch_corpus.sh` (R2 keys → env ONLY, never logged/committed, c7).
- Pairs built by `UNIVERSE/h1306_ko_corpus_export.py`: CTX=4, 3-D phi(context) =
  [last/255, 2nd-last/255, utf8_cont_depth/3] (identical to H_1297, mechanical byte fn, NO
  labels). Deterministic **stride-subsample** (KO 110, EN 200) to a CPU-tractable pair set:
  KO train=2728, KO test=2727 (even/odd disjoint split), EN test=1500 (all held-out =
  retention guard). Manifest `/tmp/h1306_manifest.json` (committed to verdict dir).

**Engine-native faculties** (the engine's OWN, not a numpy mirror — a_engine_native_learning):
- PARTITION = live VAdaptField Voronoi ownership (`vadapt_field_nearest_idx`).
- GROWTH = the engine's OWN mitosis tick (`engine_mitosis_tick`, p8): ON → grow one cell
  where KO error concentrates (error-TARGETED split: highest owned-CE eligible cell,
  median-bisect on the highest-variance feature axis, recenter on the two half-centroids).
- HEAD = per-cell empirical next-byte freq (closed-form add-1 Laplace MLE) over OWNED train
  points — gradient-free (p8). NO global backprop.

**Curriculum / curve:** KO train split into 3 INCREMENTAL chunks (cumulative bounds
[909, 1818, 2728]). The engine mitosis-grows on chunk1, then chunk1+2, then chunk1+2+3,
scoring held-out KO + EN CE after EACH (≥3 curve points). Probe:
`CORE/h1306_ko_mitosis_engine_probe.hexa`. Metric = held-out next-byte CROSS-ENTROPY
(nats/byte, p7 — a legitimate convergence comparison, NOT perplexity-as-meaning).

**FROZEN bars** (pre-registered in `.verdicts/1306_ko_mitosis_real/H_1306_FREEZE.txt`
BEFORE the run; GREEN iff L & R & G; C non-gating):
- (L LEARNING) KO CE[pt3 full] ≤ KO CE[pt1] − 0.05 nats.
- (R RETENTION) EN CE[after full KO grow] ≤ EN CE[seed 2-cell field] + 0.05 nats.
- (G GROWTH) final cell count > 2.
- (C MATCH, non-gating) KO CE[full] vs arm A gradient incumbent KO CE=3.280611 (context).

## Result — 🟢 GREEN (engine-native, verbatim `.verdicts/1306_ko_mitosis_real/H_1306.txt`)

| curve pt | KO train | cells | KO CE | EN CE |
|----------|----------|-------|-------|-------|
| pt1 | 909  | 6 | 3.61092 | 4.86396 |
| pt2 | 1818 | 9 | 3.36909 | 4.84367 |
| pt3 (full) | 2728 | 9 | 3.24897 | 4.75171 |

- **(L) LEARNING PASS**: KO CE 3.61092 → 3.24897 (monotone drop **−0.362 nats/byte** as
  mitosis grew on more Korean; bar −0.05).
- **(R) RETENTION PASS**: EN CE seed(2-cell) 4.86395 → after-full-KO-grow 4.75171 — English
  did NOT regress; it even **improved slightly** (the KO-grown cells also better-tile the
  shared ASCII region). Bar +0.05.
- **(G) GROWTH PASS**: 2 (seed) → **9 cells** (mitosis added 7 cells for Korean).
- **(C) context**: KO CE[full] 3.24897 even **beats** the gradient incumbent 3.28061 — the
  gradient-free mitosis trunk-grow is competitive on real Korean next-byte.

**Regression guard (all green):** `engine_cli_smoke` **73/0** (engine untouched) ·
`h1196` single-entry **7/0** · `h1205` separation-invariant **PASS** (generation
byte-identical ON==OFF, Ψ=½ untouched). Korean mitosis did NOT corrupt the Ψ fixed point
or English generation (Ψ-disjoint: pure_field never touched, a_core_engine_map).

## Honest scope (a_scale_honest_scope, a_toy_scale_recheck) — NO overclaim

This is the **FIRST CPU rung** on a 600 KB KO / 300 KB EN real-text window, deterministically
**stride-subsampled** to 2728 KO train pairs. It demonstrates that engine-native gradient-free
mitosis **learns Korean next-byte structure AND retains English on REAL data** — it does
**NOT** make anima fluent in Korean. Specifically still UNVERIFIED:
- Full-corpus scale (the kor shard alone is 9.8 GiB × 3 files; this rung used <0.006%).
- Generation/decode of Korean (this measures next-byte CE, not fluent emit).
- A richer context feature (3-D phi vs the full 303M trunk's representation).

**Next rung:** (a) a **CPU-bigger** rung — more KO pairs / a longer window / deeper context
features (still $0, slower); (b) a **GPU-scale, cost-gated** rung — wire the grown Korean
cells onto the live 303M decode path and train at corpus scale (NOT auto-rented; surface
as cost-gated per the lane's non-negotiables). Brain map→decode wiring of the grown Korean
cells onto generator = follow-on (a_verified_must_wire).

## Files

- Probe: `CORE/h1306_ko_mitosis_engine_probe.hexa` (engine-native, imports CORE/engine_cli.hexa)
- Export: `UNIVERSE/h1306_ko_corpus_export.py` · Fetch: `UNIVERSE/h1306_fetch_corpus.sh`
- Verdicts: `.verdicts/1306_ko_mitosis_real/{H_1306_FREEZE.txt, H_1306.txt, h1306_manifest.json}`
- Claim: `CLAIMS.tape` @C h1306_ko_mitosis_real · Log: `domains/MITOSIS-ENGINE.log.md` @H

## xref

H_1297 (mitosis-native trunk training, the toy this scales) · H_1300 (per-skill mitosis
retention, the catastrophic-forgetting property) · H_1199 (VAdaptField DIM-growth) ·
H_1288 (grow-under-pressure) · H_1231 (per-cell binding) · a_no_llm_frame_trap ·
a_engine_native_learning · a_verified_must_wire · a_core_engine_map · a_scale_honest_scope ·
a_toy_scale_recheck · a_cpu_local_no_waiter · p1·p2·p7·p8·c7·c9·c15.
