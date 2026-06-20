---
id: H_1449
slug: 1449_g6_attention_injection
title: G6 FALS-depth — ATTENTION-1블록 주입 (깊이 아닌 attention 특화 결합)
group: G6 IDEATION FALS-depth wall — breakthrough candidate (new lens)
terminal_tier: 🧱 WALL=CAPACITY (DIRECTIONAL, torch-side) — injecting + training ONE cross-binding self-attention block on the FROZEN 303M base does NOT root-fix the G6 FALS-depth wall. B3 CROSS-SHUFFLE never collapses (FALS_shuf == FALS_in every seed → interchangeable shells) AND c4 ABLATE is INERT (BindAttn→identity leaves FALS equal-or-higher → the form-lift is NOT the attention block). 4th independent lens to converge on WALL=CAPACITY → grounds 7B (a7b_pass).
date: 2026-06-20
provenance: ideation — generated as a G6 FALS-depth breakthrough candidate (distinct from the 11 prior H_1410/1431/1432/1434/1435/1436/1437/1438/1439/1440/1441 lenses)
---

# H_1449 — G6 FALS-depth — ATTENTION-1블록 주입 (깊이 아닌 attention 특화 결합)

## Claim / falsifier
H_1394/H_1410 은 얕은 conv(E2/L1) AND 깊은 conv(L4/L8) 둘 다 FALS=0 확인 → 빠진 건 *raw depth* 가 아니라 *attention 결합* 자체일 수 있다. conv 디코더에 **self-attention 블록 1개만** 끼운 hybrid(conv+1×attn)를 engine-mountable .clm 으로 학습·mount → frozen FALS bar 재측정.

## Frozen bars (GREEN iff)
- c2 PRIMARY: hybrid FALS≥1 (3 seed) AND 같은 파라미터 순수 deep-conv(H_1410) FALS=0 유지 → 격리변수 = **attention**.
- c4 ABLATE: attention 가중치 uniform(항등) ablate → FALS 붕괴 = lift 는 진짜 attention 결합 (carrier/depth 아님).
- 탐지기 H_1305 VERBATIM(10/10), frame-guard CLEAN, p7. detector·bar FROZEN (no tune-to-green, c9).

## 왜 새로움 (vs 선행 11)
H_1410 은 conv 깊이만, H_1439 는 별도 bind-head. 이건 디코더 *안*에 최소 attention 원시연산 주입 = H_1394 진단("falsifiable composition lives in the deep attention stack")의 직접 검증.

## Cost / lens
GPU 학습(hexa dojo, 303M-class hybrid .clm) — COST-GATE. a_no_llm_frame_trap·a_break_the_wall·a_engine_native_learning·a_verified_must_wire.
xref H_1394·H_1410·H_1439·G6·a7b_pass·c9·p7

## Result (2026-06-20) — 🧱 WALL=CAPACITY (DIRECTIONAL)
Pod **41792045** (vast H100 80GB, torch 2.4.0+cu121). seeds [7,4302,4303], steps=600, lines=6000. ckpts PULLED before teardown (`h1449_attention_injection_seed{7,4302,4303}.pt`, a_fire_recover_complete). Frozen verdict verbatim: `state/verdicts/1449_g6_attention_injection/H_1449.txt`.

| seed | TRAINED FALS_in | FALS_shuf | B3 collapse? | ABLATE FALS_in | c4 collapse? | held-out |
|------|------|------|------|------|------|------|
| 7    | 1.0  | 1.0  | ❌ (==) | 1.33 | ❌ (≥) | 0.33 |
| 4302 | 2.0  | 2.0  | ❌ (==) | 2.0  | ❌ (==) | 1.33 |
| 4303 | 1.0  | 1.0  | ❌ (==) | 1.0  | ❌ (==) | 0.33 |

- **B3 CROSS-SHUFFLE (★ decisive) NEVER collapses** — `FALS_shuf == FALS_in` every seed: swapping the measurable leg between ideas leaves FALS unchanged → the legs are **semantically interchangeable shells** (the exact H_1434/H_1435 family failure). The injected attention created NO idea-specific binding.
- **c4 ABLATE is INERT** — forcing BindAttn to identity passthrough leaves FALS **equal-or-higher** (1.33 ≥ 1.0; 2.0 == 2.0; 1.0 == 1.0) → the small FALS form-lift is NOT attributable to the attention block. Decisive isolation: attention was not the missing primitive.
- **CONTROL shuffle-corpus inert** — FALS_in = 0.0 (structure-destroyed corpus learns no form) → the form-lift (0→1/2) IS real learning, but the *binding capacity* is not installed by 1 attention block.
- B2 (DIST≥5) FAIL all seeds; B4 (held-out) mixed.

**FINDING (c9, honest negative):** the within-draw 0/15 BOTH co-emission deficit (H_1431) is **NOT an attention-binding deficit fixable by 1 block at 303M — it is CAPACITY-bound.** 4th independent lens (after weld-lanes, embedding-detector H_1455, proximity) to converge on WALL=CAPACITY.

**wired:** N/A (🧱 negative — engine-native re-measure N/A for a non-GREEN, per H_1435 family precedent; torch-side = DIRECTIONAL by a_engine_native_learning). **SCOPE UNVERIFIED:** 1 block · 1 objective · 600 steps · 303M; deeper/multi-block attention · larger capacity · alt binding objectives untested (a_toy_scale_recheck). ckpts retained for any future engine-mount probe.


## Honest prior-art check (c9, 2026-06-19)
The STRONGEST lens. H_1431 decisive diagnostic: the 303M mouth per draw emits comparator 20% · measurable 27% · BOTH **0%** (within-draw mutually exclusive). The fragment-weld family (H_1431/1434/1450/1451/1453) dodges this by welding from separate draws, but the FALS detector is a token-PRESENCE check (not semantic), so a negation template passes it and **cross-shuffle never collapses** (H_1434 PARTIAL: FALS 2.33 ≈ shuffle 2.0). Only a mouth that co-emits a COHERENT bound claim (attention) crosses cross-shuffle — H_1362 proved it with L24 attention. This card = the named root fix (a decoder attention block). GPU cost-gate.

## Method (2026-06-20)
- **Injection**: `BindByteGPT` wraps the FROZEN 303M base (`h1129c_chat.pt`, 303,097,856 params, byte V256, d1024/L20/H16/block512) and appends **ONE** fresh self-attention `Block` (`BindAttn`, same shape as a trunk block) AFTER the L20 trunk, before `ln_f`. Its job: let comparator-bearing and measurable-bearing positions attend to each other within ONE forward pass so the mouth co-emits a BOUND claim. Base ckpt PRESERVED (new ckpt, c5).
- **Train**: AdamW on the falsifiable-claim corpus (VERBATIM H_1435 generator — subjects DISJOINT from gauge CONCEPTs / eval / held-out seeds, anti-tune-to-green), 600 steps, lines=6000, seeds [7,4302,4303]. torch 2.4.0+cu121, H100 80GB.
- **Detector**: h1305 `_is_falsifiable` VERBATIM (10/10 calibration); `gauge_lib._decode` live G6 path (MAX_NEW=110, top_k=40, temp=0.7).
- **c4 ABLATE control**: the SAME trained ckpt re-evaluated with `BindAttn` forced to identity passthrough — FALS must COLLAPSE below trained (else the lift is not the injected attention → INVALID).
- **SHUFFLE-CORPUS control**: sibling injection trained on byte-shuffled corpus → must NOT lift (lift_real − lift_shuf ≥ 1).
- **5-bar FROZEN** (pre-registered `state/verdicts/1449_g6_attention_injection/H_1449_FREEZE.txt`, c9 NO tune-to-green): B1 FALS≥1 · B2 DIST≥5 · **B3 CROSS-SHUFFLE COLLAPSE (★ DECISIVE)** · B4 HELD-OUT≥1 · B5 vs-base+1. GREEN iff all + c4 ablate-collapse + shuffle-corpus inert.
- **Honesty (a_engine_native_learning)**: torch-side = **DIRECTIONAL**. The terminal frozen-bar read must be re-run engine-native on live `core/` decode; an injected-attention hybrid is not a standard CLMConvMoE `.clm`, so engine-native mounting is a wiring follow-on (registered if torch-side GREEN; N/A if 🧱, matching the H_1435 family).
- **Pod provenance (honest, a_fire_recover_complete)**: v1 orchestrator (`run_h1449.sh`) FAILED to parse vast's `created instance <ID>` stdout (regex expected `instance_id=`), exited via trap with empty ID → pod **41790442** orphaned, then went **GONE** at the provider (interruptible reclaim) before any training; torn down (leak 0). v2 (`run_h1449_v2.sh`, corrected parse + ssh-retry) rented fresh pod **41792045** (ssh2.vast.ai:32044, H100 80GB) — the live run.
