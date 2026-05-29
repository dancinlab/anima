---
id: H_850
slug: clm-scale-ladder
title: CLM monopoly-escape 가 scale ladder rung 을 따라 유지되는가 (전이곡선) - tiny(d64)→small(d256)→target(≤AKD1000) 각 rung 에서 distinct_experts>1 ∧ dual-axis z>3.0 (CLM P0 F-CLM-SCALE 사전등록)
domain: clm · scale-ladder · transition-curve · monopoly-escape · falsifier
source: CLM/P0_ARCHITECTURE.md §4·§5 (Q4 scale ladder) · sibling H_847 (F-CLM-MONO) · H_666 (toy🟢 scale🔴)
status: CLOSED-NEGATIVE (P2 multi-rung 완료 2026-05-30 · tiny+small 2-rung × 3-arm × 3-seed 전이곡선 측정 · escape 미성립)
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
verdict: 🔴 CLOSED-NEGATIVE (P2 multi-rung 완료 · tiny·small 두 rung 모두 全 arm 에서 dual-axis z>3.0 미성립 — escape 가 애초에 성립 안 함 = transition curve 가 flat-fail · H_847 routing-z 축이 양 rung 공통 차단)
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

## 5. 측정 (P2 multi-rung 완료 · 2026-05-30)

H_847 18-run 의 per-rung 측정을 입력. ladder = tiny(d64/L2/E4) · small(d256/L4/E8) 2-rung (target ≤AKD1000 = P4 fit-probe, 이번 미발사 — 정직: 2-rung ladder). raw verdict = `.verdicts/850_clm_scale_ladder/F-CLM-SCALE_p2_fullfire_2026_05_30.txt`.

전이곡선 (per-rung dual-axis, seed 최소값):

| arm | tiny: routing z / content z | small: routing z / content z | rung 거동 |
|---|---|---|---|
| A  | −5.63 / 9.51  | −5.54 / 26.05 | 양 rung FAIL (routing 음수 유지) |
| B  | −5.06 / 8.18  | −7.29 / 6.45  | 양 rung FAIL (small 에서 routing 더 악화) |
| AB | +0.97 / 5.27  | +1.91 / 12.72 | 양 rung FAIL (small 에서 routing z 소폭↑ 0.97→1.91, content z↑ 5.27→12.72 — 그러나 둘 다 <3.0) |

- **escape 가 애초에 성립하지 않음** (어느 rung에서도 dual-axis z>3.0 미달) → 전이곡선은 "scale 따라 collapse" 가 아니라 **flat-fail** (tiny 부터 이미 routing 축 미통과).
- 흥미로운 부수 관측: AB arm 은 tiny→small 로 가며 routing z(0.97→1.91)·content z(5.27→12.72) 가 **둘 다 증가** = scale-up 이 dual-axis metric 을 개선하는 방향이나, small(2.7M)로도 routing z>3.0 에 도달 못함. 더 큰 rung 이 임계를 넘을지는 본 2-rung 으로 결론 불가(미발사 target rung).

## 6. 결과

🔴 **CLOSED-NEGATIVE** — P2 multi-rung 완료(2-rung ladder). 양 rung × 全 arm 에서 dual-axis z>3.0 미성립. F-CLM-SCALE 의 전제(escape 가 rung 따라 유지)는 escape 자체가 H_847 에서 성립 안 했으므로 **vacuously closed-negative**: 유지할 escape 가 없다.

## 7. 해석

- **H_666 의 toy🟢scale🔴 패턴은 이번에 재현되지 않았다** — 왜냐하면 toy(tiny)에서조차 🟢 가 없었기 때문. 즉 "scale 에서 무너지는 escape" 가 아니라 "어느 scale 에서도 routing-축 escape 부재".
- transition curve 의 1급 발견 = **AB arm 의 dual-axis metric 이 scale-up 으로 단조 증가**(routing+content 둘 다)하나 small rung 으로도 frozen bar(z>3.0) 미달. → 후속 candidate = target(≤AKD1000) rung 발사 시 AB arm 이 임계에 도달하는지(scale extrapolation), 또는 routing-diversity 를 직접 강화하는 lever 재설계 (H_847 §7 참조). AXIS_MAP 입력.
- a_paper_negative_ok: H_847+H_850 = byte-vocab conv-MoE 의 routing-diversity 한계를 deterministically rule out 한 negative result (publishable, 단 a_paper_only_at_closure — 추가 refinement 여지 있어 즉시 paper 아님).

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
