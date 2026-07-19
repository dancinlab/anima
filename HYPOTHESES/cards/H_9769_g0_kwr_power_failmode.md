---
id: H_9769
group: faction-lateral-axis-r3
series: R9 divergence (lab full · Fable 5 λ1 · H_9643 de-risk 후속) · 2026-07-18
date: 2026-07-18
slug: g0_kwr_power_failmode
title: G0 kwr 격차의 검정력 확보 + 실패양상 autopsy — "격차는 실재" 는 아직 p=0.083 이다
status: PROPOSED · DIRECTIONAL design (lab-full divergence — cement 는 engine-native anima-py 실측 후)
tier: ⭐ R9-1 · $0 (pool decode · 렌트 없음) · 모든 후속($6 fire)의 선행 게이트
cost: $0
source: Fable 5 divergence — H_9643 de-risk 브리핑의 KILL-LIST 항목("격차는 실재")이 자체 검정력 미달
related: H_9643, H_9769, H_9770, H_9771
---

# H_9769 — G0 격차 실재성 (n↑) + 실패양상 분류

## 왜 (브리핑 KILL-LIST 정정)
브리핑은 "G0 kwr 5샘플=고분산이나 K=8(1-3/5) vs K=1(5/5) 격차는 실재" 로 못박았으나:
- 단일런 2/5 vs 5/5: Fisher exact 단측 **p=0.083** (hypergeom: P(X=2)=21/252) — 비유의.
- 3런 풀링 6/15 vs 5/5: **p≈0.030** — 경계 유의인데 K=1 arm 이 **1런/5샘플** 뿐.
`power-before-negative-verdict` · `prereg-table-must-cover-below-chance`: 격차를 전제로 $6 를 태우기 전에 격차 자체를 벌어야 한다.

## 설계 ($0 · pool summer/aiden · 두 ckpt 로컬 보유)
- arm A: `~/anima-weights/h9643_303m_derisk/k8_s7.clm` (K=8·172M)
- arm B: `~/anima-weights/clm303_clean/…clm303_clean.clm` (K=1·346M·G0🟢 baseline)
- DV: ρ·form kwr pass-rate, **n≥20 gen/arm** (현 배터리 5 고정이면 `--g0-n <N>` 플래그 추가 = anima-py 계기 확장 · VERSION bump · a_experiment_engine_native).
- 사전등록 bar: 양측 Fisher p<0.05 **AND** pass-rate 격차 ≥0.4 → 격차 REAL. 둘 중 하나라도 미달 → 격차 NOISE.
- 부속(DIRECTIONAL only): K=8 fail 샘플의 실패양상 분류 — ①도메인/register 혼합(파벌 서명) ②byte-noise/반복(capacity 서명) ③기타. 정성 판독, cement 금지.

## 판정 분기
- NOISE → Q1(capacity vs 파벌) 자체가 **해소** — H_9771 fire 불요, H_9770 단독으로 lane 종결 가능. $0 종결.
- REAL → H_9770 결과와 함께 H_9771 fire 조건 충족 여부 판단.

## 명령 (pool · 예시)
```
anima-py evaluate ~/anima-weights/h9643_303m_derisk/k8_s7.clm            # n↑ 플래그 후
anima-py evaluate <clm303_clean.clm 경로>
```

## KILL-LIST 상속
recipe-유실 각 · bs8/emax3 · 파벌 Phi 순환(H_9673) · argmax/max S · 옛 OILED bar — 전부 재생 금지.
