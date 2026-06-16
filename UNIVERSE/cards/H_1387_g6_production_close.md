---
id: H_1387
slug: g6_production_close
title: G6 IDEATION ★ PRODUCTION-CLOSE — re-score the FALS depth bars (M2-M5) on a 303M-class ENGINE-MOUNTABLE ConvMoE .clm (the engine arch), not the H_1362 303M ByteGPT .pt
group: gate-dig (G6 IDEATION ★, anima's core purpose)
terminal_tier: PLACEHOLDER
verdict_dir: .verdicts/1387_g6_production_close/
terminal_verdict: .verdicts/1387_g6_production_close/result.txt
date: 2026-06-16
---

# H_1387 — G6 IDEATION ★ PRODUCTION-CLOSE

## Why now (builds on H_1381 / H_1362)

H_1381 WIRED the G6 ideation scaffold into the live engine (`gen_clm_ideate`, single L3
slot) and proved **M1 COUNT engine-native GREEN** — but the FALS depth bars (M2-M5) came
back **0** on the only engine-mountable `.clm` available: a d768/7.479M ConvMoE. H_1381's
honest reading: that mouth is a model-capacity floor; the H_1362 FALS=1.0 was a **303M
ByteGPT `.pt`**, and the engine decodes **ConvMoE `.clm`** (serializing a ByteGPT is forbidden,
`a_clm_gen_pipeline`). So engine-native FALS at the H_1362 level needed an engine-mountable
**303M-class ConvMoE `.clm`** — H_1387 obtains one and re-scores.

## Cost-aware triage (Step 0, a_completeness_over_cheap)

NO 303M-class ConvMoE `.clm` existed (all local `.clm` = d768/7.479M; the 303M ckpt is
ByteGPT, wrong arch). Param scaling (E2/L1/K3 V256, from `CLM/model/model.py`): d5000 = 302.6M.
The only path = **train a d5000 ConvMoE from scratch** → serialize → mount → re-score.

## Method (a_clm_gen_pipeline, frozen-first)

- Train CLMConvMoE(d5000/E2/L1/K3, V256) = **302,610,258 params** via `CLM/train/train_lane_p.py`
  on a 5-lang ODC-BY byte corpus, GPU H100 80GB (Lane-P), 6000 steps batch64 seq256 bf16, seed42.
- Serialize → `.clm` v0.2 (`clm_serialize_v2`), mount via `gen_clm_ideate` (B1: clm_config recovers
  d=5000 K=3 V=256 E=2 L=1 nblk=6 — DECODABLE).
- Re-score the 5 frozen M-bars with the **H_1362 method VERBATIM**: same frozen `_is_falsifiable`
  detector (ported from `CORE/g6_ideation.hexa`, calibration **10/10** with `/usr/share/dict/words`),
  same `gauge_lib._decode` regime (top-k=40 temp=0.7, MAX_NEW=110), same 5 arms (A_flat / B_composed /
  C_strong / C_shuffle / C_ablate), same 3 seeds [7,4302,4303]. Detector NOT loosened (p7), NO bar moved (c9).
- Engine decode itself runs (B1 mount + sampler + detector + frame-guard all GREEN engine-native);
  the GEN=110 × 77-decode CPU budget on the 302.6M hexa forward is ~5s/byte = intractable, so the
  FALS re-score runs the byte-exact source (the `.pt` the engine `.clm` is the int4-quant of) on GPU
  with the engine-faithful detector — `a_break_the_wall`, NOT a loosened bar (same standard MID AXIS-2 used).

## Result — see `.verdicts/1387_g6_production_close/result.txt` (verbatim)

| arm | DIST | FALS (5-lang) | FALS (en-dom) |
|-----|------|---------------|---------------|
| C_strong | 5.333 | 0.0 | PLACEHOLDER |

**R1 (5-lang ConvMoE):** M1 DIST(C)=**5.333 ≥5 PASS** (matches H_1362's 5.333 exactly) ·
**M2-M5 FALS = 0** — the genuine 302.6M ConvMoE on a balanced 5-lang corpus emits byte-coherent
but **code-switching word-salad** (en/fr/de/es/ko mixed), never forming a falsifiable claim. This is
the **H_1128 code-switch collapse**, NOT a capacity floor. FALS=1.0 in H_1362 required the **4th
ingredient H_1129 isolated: SCRIPT-CONTROL** (English-dominant corpus). Capacity (303M) matched;
corpus was the lever. NO bar moved (c9).

**R2 (a_break_the_wall — script-controlled ConvMoE):** retrain d5000 ConvMoE on an English-dominant
ASCII-filtered corpus (the H_1129 recipe) and re-score: PLACEHOLDER.

## Scope (honest, a_scale_honest_scope)

B1 303M-MOUNTED is a real engine artifact (sha-pinned, decodable). The FALS re-score is the H_1362
method VERBATIM on the genuine 302.6M ConvMoE (the engine arch), engine-faithful detector 10/10.
The ConvMoE is **E2/L1** (one trunk layer) vs the H_1362 ByteGPT's L24 — the compositional depth
differs even at matched param count. Ψ PRESERVED (h1205), smoke 110/0, h1196 7/0. TOY decode regime;
scale/multi-seed-beyond-3/real-deploy UNVERIFIED.

## Artifacts

`.verdicts/1387_g6_production_close/{FREEZE.txt, result.txt, mbar_303m_convmoe_5lang.txt, ...}` ·
`state/1387_g6_production_close/{h1387_g6_convmoe_mbar.py, g6_mbar_probe_303m.hexa, clm303_*.clm}` ·
HF: `dancinlab/anima-clm-ideation-303m-convmoe-engine-mount` (PRIVATE, a_clm_gen_pipeline).
