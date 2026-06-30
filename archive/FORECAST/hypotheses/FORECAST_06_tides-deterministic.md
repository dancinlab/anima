---
id: FORECAST_06
slug: tides-deterministic
title: 결정론 성분 시계열은 미래 fetchable (조석 대조 BTC) — 합성 6분조(M2/S2/N2/K1/O1/P1) 조석을 전반부 조화분해 fit→후반부 미래 FETCH skill 0.945·err/signal 0.06 🟢; 같은 파이프라인을 실 BTC 90일에 걸면 skill −4.21 (조화 RMSE $38k≫naive $7.3k) 🔴; 지평은 조석 외삽 임의로 안정 vs 카오스(r=4) Lyapunov ~30step 폭발 🟡. 미래는 결정론/주기성이 있는 만큼만 가져올 수 있다.
domain: forecast tides harmonic-analysis determinism random-walk lyapunov non-anima
exploration_method: 합성-사실적 조석계열(천문 분조 합+잡음) 조화분해 + 실 BTC 대조 + logistic 카오스 지평
verification_method: 전반부 fit→후반부 held-out RMSE vs naive-persistence skill; 동일 파이프라인 BTC 적용; 외삽 진폭 안정성 + Lyapunov 지평; p7 /bin/zsh stdlib-only; 데이터 snapshot 공유
since: 2026-06-14
sister: FORECAST_01, FORECAST_03, UNIVERSE/cards/H_6012
verdict: 🟢🔴🟡 조석 미래는 진짜 fetchable — 합성 6분조 조화분해로 후반부(미래) FETCH skill 0.945·err/signal 0.06 (실 tide table 처럼 수년 앞 예측 가능); 같은 조화 fit 을 실 BTC 90일에 걸면 skill −4.21 (random walk 외삽 발산, FORECAST_03 재확인) 🔴; 조석 외삽은 1×~10× 미래까지 진폭비 ~1 유지하나 카오스(r=4)는 Lyapunov ~30step 너머 폭발 🟡. 결정론 축이 fetchability 를 가른다 — 미래는 시스템이 결정론적/주기적인 만큼만 가져올 수 있다.
---
# FORECAST_06 — 결정론 성분 시계열은 미래 fetchable (조석 대조 BTC)

> **질문.** FORECAST_03 은 BTC 미래가 random walk 라 가져올 수 없다고 닫았다. 그렇다면 **강한 결정론 성분**을 가진 실세계 계열은 미래를 진짜로 가져올 수 있는가? 가장 깨끗한 예 = **해양 조석(ocean tides)**. 조석은 천문 상수 정현파(M2 12.42h, S2 12.00h, K1 23.93h, O1 25.82h ...)의 합이라, 인류는 실제로 **tide table 을 몇 년~몇 세기 앞까지 출판한다.** 이것을 FORECAST 축(결정론 fetchable / 카오스 지평 / 법칙밖 무작위 unfetchable)에 엮으면?

## 가설
미래의 fetchability 는 시스템의 **결정론/주기성 정도**에 비례한다 (anima time-arc · FORECAST_01).
조석처럼 천문 정현파 합으로 구성된 계열은 조화분해(harmonic analysis)로 임의로 먼 미래까지 낮은 오차로 fetch 가능하고, BTC 처럼 법칙밖 random walk 는 같은 도구로도 fetch 불가다.

## FROZEN FALSIFIER (사전 등록, 코드측정 p7)
- **F1 (조석 fetchable):** 합성-사실적 조석계열(6분조 + 잡음 0.05m)을 **전반부에서만** 조화 fit 한 뒤 **후반부(held-out 미래)** 를 예측 → `skill_vs_naive = 1 − RMSE_harmonic/RMSE_naive > 0.5` **AND** `err/signal < 0.3` 이면 fetchable 🟢. (둘 다 미달 시 가설 반증.)
- **F2 (BTC unfetchable):** **동일한** 조화 fit/forecast 파이프라인을 실 BTC 90일(FORECAST_03 snapshot)에 적용 → `skill_vs_naive ≤ 0` (naive-persistence 도 못 이김)이면 unfetchable 🔴 (결정론 축 확인). skill>0 면 BTC 에 주기 신호가 있다는 뜻 → 가설 약화.
- **F3 (지평):** 조석 fit 모델의 외삽 진폭이 학습창 너머 1×~10× 미래까지 `진폭비 ∈ [0.7,1.4]` 로 안정(주기적 결정론) **AND** 카오스(logistic r=4)의 두 근접 궤도가 Lyapunov 지평(~ln(1/ε)/ln2) 안에서 O(1) 로 발산(지평-한정)이면 🟢, 한쪽만이면 🟡.

## 측정 (FORECAST/harness/forecast_tides.py · stdlib-only · seed 606)
| 파트 | 측정 | 결과 | 판정 |
|---|---|---|---|
| **[1] 조석** | 조화 RMSE 0.0537 m vs naive 0.9775 m, **skill 0.945**, err/signal **0.060** | 전반부 fit→미래 FETCH 성공 | 🟢 |
| **[2] BTC** | 조화 RMSE **$38,036** vs naive **$7,301**, **skill −4.21** | 같은 조화 fit 이 random walk 외삽서 발산 | 🔴 |
| **[3] 지평** | 조석 외삽 진폭비 1.13/1.11/1.19/1.35 (1×~10×) · 카오스 발산포화 28 step vs Lyapunov 지평 29.9 step | 조석 임의 미래 안정, 카오스 지평 너머 폭발 | 🟢 |

조화분해는 numpy 없이 정규방정식 최소제곱(가우스 소거)으로 직접 구현 — 6분조 × (cos,sin) + DC = 13계수. BTC 에는 동일 분조 주기를 일 단위로 환산해 그대로 적용했다(공정 대조).

## 결론
🟢🔴🟡 **조석의 미래는 진짜로 가져올 수 있다.** 합성 6분조 조석을 전반부만 보고 후반부(미래)를 skill 0.945·신호대비 6% 오차로 FETCH 했다 — 실세계에서 인류가 tide table 을 수년~수세기 앞까지 출판하는 바로 그 메커니즘(조화분해). 같은 조화 fit/forecast 파이프라인을 실 BTC 90일에 걸면 skill −4.21 로 naive-persistence 조차 못 이기고 외삽이 발산한다(🔴, FORECAST_03 의 random walk 결론을 **다른 도구로 독립 재확인**). 지평에서는 조석 외삽이 1×~10× 미래까지 진폭을 보존하는 반면 카오스(r=4)는 Lyapunov ~30 step 너머로 폭발한다(🟡, 지평-한정 fetchable).

**시간-arc 원리 확정:** 미래는 시스템이 **결정론적/주기적인 만큼만** fetchable 하다 — 조석(천문 정현파 합)=강한 결정론 → fetchable, BTC=법칙밖 무작위 → unfetchable, 카오스=결정론이나 Lyapunov 지평-한정. FORECAST_01(결정론) ↔ FORECAST_03(BTC 무작위) 사이를 잇는 양성 사례.

verdict: `FORECAST/verdicts/forecast_tides.txt` · 데이터: `FORECAST/verdicts/btc_hist_snapshot.json`(실 BTC) · 재현: `python3 FORECAST/harness/forecast_tides.py`
