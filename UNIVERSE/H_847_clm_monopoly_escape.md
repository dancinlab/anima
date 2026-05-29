---
id: H_847
slug: clm-monopoly-escape
title: byte-vocab(V=256) conv-native MoE 가 expert monopoly 를 탈출하는가 - distinct_experts>1 ∧ routing z>3.0 ∧ content z>3.0 ∧ multi-seed{base,43,44} 재현 (CLM P0 F-CLM-MONO 사전등록)
domain: clm · moe · mitosis · monopoly-escape · byte-vocab · falsifier
source: CLM/P0_ARCHITECTURE.md §3·§4 (Q2·Q3·d6) · sibling H_666 (MoE collapse toy🟢 scale🔴) · v5-mitosis v1~v7 (v7 routing z=2.75 marginal)
status: pre-registered (P2 full-fire 판정 대기 · threshold frozen pre-run · 측정 0)
exploration_method: E2 (corpus 2-source ↔ MoE 2-lane) · arch redesign (byte-vocab lever)
verification_method: W2 (pre-registered numerical threshold · z>3.0 양축 · multi-seed 재현 · post-tuning 0)
raw_rank: 9
hexa_only: false
deterministic: false
llm: none
pre_register_frozen: true
frozen_at: 2026-05-30
since: 2026-05-30
sister: CLM/P0_ARCHITECTURE.md, UNIVERSE/H_666, .verdicts/847_clm_monopoly_escape/F-CLM-MONO_prereg.txt
verdict: 🟠 PRE-REGISTERED (P2 full-fire 미실행 · 3-arm × ladder PyTorch fp 학습 후 판정 · z>3.0 양축 + seed{base,43,44} 재현 게이트)
---

# H_847 — CLM F-CLM-MONO monopoly escape

## 1. 가설

CLM P0 의 **byte-vocab(V=256) + conv-native + MoE(=mitosis cell)** 토대가 expert monopoly(단일 expert 독점 = mode collapse) 를 탈출한다. 사전등록 임계 4개 동시 PASS 시:

- **monopoly escape SUPPORTED** — distinct_experts>1 ∧ routing z>3.0 ∧ content z>3.0 ∧ seed{base,43,44} 재현
- → 🟢 SUPPORTED-NUMERICAL · "byte-vocab lever 가 V≫d monopoly 근원 직격"

임계 중 하나라도 FAIL 시:

- **monopoly escape FALSIFIED** — byte-vocab 으로도 collapse · 또는 single-seed artifact
- → 🔴 CLOSED-NEGATIVE · "byte-vocab 축 ⊥ register isolation" (a_paper_negative_ok)

## 2. 동기

- CLM P0 Q2 = 더블바인드(anima→register collapse · no-anima→Chinchilla underfit) 탈출을 MoE conv-expert=mitosis cell 로 시도. register 격리(cell1) = 메인 coherent(cell0) 유지.
- Q3 = monopoly 근원 가설 **V≫d** (15만/64 = 2370배). byte-vocab(V=256) 은 V/d = 4배로 근원 직격 — prior art 미시도 lever.
- prior art: H_666 (MoE collapse toy🟢 scale🔴 · scale-up 재반증) · v5-mitosis v1~v7 (v7 routing z=2.75 single-seed marginal · content 후퇴). d6 임계 = v7 marginal 교훈으로 z>3.0 양축 + multi-seed 강화.

## 3. falsifier (사전등록, 임계 frozen pre-run)

```
F-CLM-MONO-EXPERTS  : distinct_experts > 1            (단일 expert 독점 아님)
F-CLM-MONO-ROUTE    : routing diversity z > 3.0       (routing 축 · v7 z=2.75 marginal 초과)
F-CLM-MONO-CONTENT  : content separation z > 3.0      (content 축 · v7 후퇴 극복)
F-CLM-MONO-SEED     : seed{base,43,44} 전부 재현       (single-seed artifact 차단)
```

4 PASS → 🟢 SUPPORTED-NUMERICAL · "byte-vocab monopoly escape"
임의 FAIL → 🔴 CLOSED-NEGATIVE · "byte-vocab 축 단독 ⊥ register isolation"

verdict 영속: `.verdicts/847_clm_monopoly_escape/F-CLM-MONO_prereg.txt` (frozen threshold verbatim)

## 4. 방법

```
1. CLM P0 3-arm ablation (P0_ARCHITECTURE §3·§5):
   - ARM A   : entropy-reg          (content 축)
   - ARM B   : topK + load-balance  (routing 축)
   - ARM A+B : 합본 (dual-axis ★untried)
2. scale ladder: tiny(d64/L2/E4) · small(d256/L4/E8) · target(≤AKD1000 fit)
3. PyTorch fp16 학습 (d5 2-track · 추론 AKIDA-only 불변) · GPU pod full-fire
4. seed{base,43,44} 각각 학습 → distinct_experts + routing z + content z 측정
5. 4 pre-registered falsifier 동시 평가 · 정직 보고 (threshold 재조정 0)
```

## 5. 측정 (P2 full-fire 후 채움)

```
[PENDING — P2 full-fire]
3-arm × ladder × seed{base,43,44} → distinct_experts · routing z · content z
micro-exp 토이 = 직관(non-gate) · full-fire 전부 = 판정 (Q4 toy≠scale H_666 실증)
wall-first · 무캡 (a_fire_autonomous · a_wall_first)
```

## 6. 결과

🟠 **PRE-REGISTERED** — P2 full-fire 미실행. 측정값 0. 임계만 frozen (`.verdicts/847_clm_monopoly_escape/`).

## 7. 해석

[PENDING — full-fire 후]

- 4 PASS → byte-vocab lever 가 V≫d monopoly 근원을 직격한 첫 사례 (prior art 미시도).
- 임의 FAIL → byte-vocab 축 단독으로는 register isolation 부족 = closed-negative (corpus-axis ⊥ register 계열 후속, AXIS_MAP 재설계 입력).

## 8. 논의

- **a_completeness_over_cheap 정합**: byte-vocab fresh re-design = 근본 원인(V≫d) 직격 본선 경로. merge-of-failures(v7 ckpt 블렌딩) 거부.
- **d6 정합**: z>3.0 양축 + multi-seed = v7 z=2.75 single-seed marginal 교훈 차단.
- **toy≠scale 정합 (H_666)**: toy 로 prune 금지 · 3-arm 전부 full-fire 가 판정.
- **p8 정합**: MoE expert = mitosis cell (train=infer 연속체). monopoly escape = cell-pool 분화 성공.
- **a_paper_negative_ok**: 🔴 FALSIFIED 도 publishable (byte-vocab 축 ⊥ register 를 deterministically rule out 시).

## 9. 양방향 sibling

- sibling: [CLM/P0_ARCHITECTURE.md](../CLM/P0_ARCHITECTURE.md) §3·§4 (F-CLM-MONO SSOT) · §5 (3-arm × ladder 매트릭스)
- prior art: H_666 (MoE collapse toy🟢 scale🔴) · v5-mitosis v1~v7
- UNIVERSE SSOT: [CANDIDATES.md](./CANDIDATES.md)
- 형제 falsifier: H_848 (F-CLM-AKIDA-MAP) · H_849 (F-CLM-QUANT) · H_850 (F-CLM-SCALE) · H_851 (F-CLM-MITOSIS)
