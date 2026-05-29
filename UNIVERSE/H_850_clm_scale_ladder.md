---
id: H_850
slug: clm-scale-ladder
title: CLM monopoly-escape 가 scale ladder rung 을 따라 유지되는가 (전이곡선) - tiny(d64)→small(d256)→target(≤AKD1000) 각 rung 에서 distinct_experts>1 ∧ dual-axis z>3.0 (CLM P0 F-CLM-SCALE 사전등록)
domain: clm · scale-ladder · transition-curve · monopoly-escape · falsifier
source: CLM/P0_ARCHITECTURE.md §4·§5 (Q4 scale ladder) · sibling H_847 (F-CLM-MONO) · H_666 (toy🟢 scale🔴)
status: pre-registered (P2 multi-rung 판정 대기 · 측정 0)
exploration_method: E2 (scale ladder sweep · transition curve 1급 산출)
verification_method: W2 (per-rung pre-registered threshold · post-tuning 0)
raw_rank: 8
hexa_only: false
deterministic: false
llm: none
pre_register_frozen: true
frozen_at: 2026-05-30
since: 2026-05-30
sister: CLM/P0_ARCHITECTURE.md, UNIVERSE/H_847, UNIVERSE/H_666, .verdicts/850_clm_scale_ladder/F-CLM-SCALE_prereg.txt
verdict: 🟠 PRE-REGISTERED (P2 multi-rung 미실행 · 전이곡선 측정 후 판정 · toy≠scale H_666 직접 검정)
---

# H_850 — CLM F-CLM-SCALE monopoly-escape 전이곡선

## 1. 가설

CLM 의 monopoly-escape (F-CLM-MONO, H_847) 가 **scale ladder rung 을 따라 유지**된다 (단일 point 가 아닌 전이곡선). tiny(d64) → small(d256) → target(≤AKD1000 fit).

- → 🟢 SUPPORTED-NUMERICAL · "byte-vocab escape 가 scale-stable (전이곡선)"
- FAIL → 🔴 CLOSED-NEGATIVE · "escape 가 toy-scale artifact (rung N 에서 collapse)"

## 2. 동기

- CLM P0 Q4 + 학습된 교훈 **toy≠scale (H_666 toy🟢 scale🔴 재반증)**: toy 의 monopoly-escape 가 scale 에서 무너진 전례. 이 falsifier 가 그 lesson 을 CLM byte-vocab lever 에 직접 적용 검정.
- 전이곡선(distinct_experts & dual-axis z vs scale) 자체가 P0 §5 의 1급 산출물 — 어느 rung 에서 escape 가 collapse 하는지(있다면) 가 핵심 발견.

## 3. falsifier (사전등록, frozen pre-run)

```
F-CLM-SCALE : distinct_experts>1 ∧ dual-axis z>3.0 가 EACH rung {tiny,small,target}
              에서 성립 (escape 가 scale 로 collapse 안 함)
PASS → 🟢 · byte-vocab escape scale-stable (전이곡선)
FAIL → 🔴 CLOSED-NEGATIVE · escape = toy artifact (rung N collapse)
```

verdict 영속: `.verdicts/850_clm_scale_ladder/F-CLM-SCALE_prereg.txt`

## 4. 방법

```
1. H_847 3-arm × ladder full-fire 의 per-rung 측정을 입력.
2. 각 rung {tiny(d64/L2/E4), small(d256/L4/E8), target(≤AKD1000)} 에서
   distinct_experts + routing z + content z 추출.
3. 전이곡선 = (rung) → (escape metric) plot.
4. per-rung pre-registered threshold check · collapse rung 식별 · 정직 보고.
```

## 5. 측정 (P2 multi-rung 후 채움)

```
[PENDING — P2 ladder full-fire]
rung tiny/small/target → distinct_experts · dual-axis z · 전이곡선
micro-exp 토이 = 직관 non-gate · full-fire 전부 = 판정 (Q4 wall-first 무캡)
```

## 6. 결과

🟠 **PRE-REGISTERED** — P2 multi-rung 미실행. 전이곡선 측정 0. 임계만 frozen.

## 7. 해석

[PENDING — ladder full-fire 후]

- 전 rung PASS → byte-vocab escape 가 H_666 의 toy🟢scale🔴 패턴을 깬 첫 사례 = scale-stable.
- rung N collapse → escape 는 toy artifact, collapse rung 이 byte-vocab lever 의 scale 한계 (closed-negative · AXIS_MAP 입력).

## 8. 논의

- **toy≠scale 정합 (H_666)**: 이 falsifier 가 정확히 그 lesson 의 CLM 적용 검정.
- **a_completeness_over_cheap 정합**: 전 rung full-fire = 본선 · toy 로 prune 금지.
- **a_wall_first 정합**: 병렬 rung fire (더 많은 H100) 로 wall time 단축.
- **a_paper_negative_ok**: collapse rung 식별 = closed-negative 발견, publishable.

## 9. 양방향 sibling

- sibling: [CLM/P0_ARCHITECTURE.md](../CLM/P0_ARCHITECTURE.md) §4·§5 (scale ladder 매트릭스)
- depends on: H_847 (F-CLM-MONO per-rung 측정 = 입력)
- prior art: H_666 (toy🟢 scale🔴 = 이 falsifier 의 검정 대상 패턴)
- UNIVERSE SSOT: [CANDIDATES.md](./CANDIDATES.md)
- 형제 falsifier: H_847 · H_848 · H_849 · H_851
