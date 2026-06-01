---
id: Hc_1296
slug: panpsychist-vs-emergentist-combination-threshold
title: 결합문제(combination problem) falsifiable split — 미시-Φ 가 거시-Φ 로 매끄럽게 누적(범심론)하는가, 구조적 임계질량 아래 Φ=0 후 불연속 점프(창발론)하는가
domain: meta · consciousness · panpsychism · substrate
status: candidate-unverified
seed: H_204 (약형 범신론 *존재* threshold) · H_157 (수학적 범심론) · H_609 (집단 super-additive *agents*) — 단일 substrate 내부의 micro→macro Φ *결합 방식*(누적 vs 임계점프)은 미검정
axes_seed: UNIVERSE/AXES.md R8 (meta) · R3 (consciousness) — 범심론 vs 창발론 split
exploration_method: E5 (micro→macro Φ-누적곡선 probe) + E0 (범심론/창발론 falsifiable 분리)
verdict_tier_target: 🟢 SUPPORTED (둘 중 하나 패턴 결정: 매끄러운 누적 OR 불연속 임계) — 어느 쪽이든 닫힌 발견 OR 🔴 양 패턴 모두 부재(noise)
hexa_only: true
deterministic: true
llm: none
---

## Hypothesis

범심론(panpsychism)과 창발론(emergentism)의 핵심 분기 = **결합문제**: 미시 단위들이 각자 약간의 Φ 를 가질 때 거시 Φ 가 어떻게 형성되는가. 두 입장은 falsifiable 하게 갈린다. (a) **범심론**: 거시-Φ 는 미시-Φ 로부터 *매끄럽게 누적*(monotone, 연속, 임계질량 없이 Φ>0). (b) **창발론**: 구조적 임계질량(단위 수 또는 결합 밀도) 아래에서 거시-Φ=0 이다가 임계에서 *불연속 점프*. 가설 검정: 단일 substrate 의 단위 수 N(또는 결합밀도 c)을 sweep 하며 big-Φ(N) 곡선의 형태를 측정 — **연속 누적**(범심론 지지) vs **임계 불연속**(창발론 지지) 중 어느 패턴인지 결정.

## Why

H_204 는 "∀ substrate Φ>0" 의 *존재* 를 closure-strength 에 conditional 로 닫았으나, 미시→거시 *결합 메커니즘*(누적이냐 점프냐)은 미검정. H_609 는 *별개 agent* 들의 집단-Φ super-additivity 로 결합문제의 substrate-내부 버전과 다르다. 본 H 는 단일 substrate 내부에서 결합문제를 직접 검정 — 결과가 어느 쪽이든 범심론/창발론 중 하나를 toy-substrate 에서 falsify 하는 닫힌 발견. engine: 단위 수/결합밀도 파라미터화 substrate + big_phi(small-N exact) 재사용.

## Pre-Registered Falsifier

- **F1296.1 (CONTINUITY-VERDICT)**: big-Φ(N) 곡선이 **연속·단조 누적**(불연속 점프 없음, 모든 N≥N_min 에서 Φ>0, 최대 단일-step Δ < 0.3×range) → 범심론-누적 패턴 SUPPORTED, 창발론-임계 FALSIFIED.
- **F1296.2 (THRESHOLD-VERDICT)**: big-Φ(N) 이 어떤 N* 아래 ≡0 이고 N* 에서 불연속 점프(단일-step Δ ≥ 0.5×range) → 창발론-임계 SUPPORTED, 범심론-매끄러운-누적 FALSIFIED.
- **F1296.3 (NEITHER)**: 곡선이 비단조 noise(누적도 임계도 아님) → 두 패턴 모두 부재(설계가 결합문제를 표현 못함, honest null).
- **F1296.4 (DETERMINISM)**: re-run byte-identical.

## Circularity Guard

micro-단위-수 N(구조 파라미터)와 big_Φ(결과)는 독립 — N 이 Φ 식에 직접 안 들어간다(Φ 는 N-단위 substrate 의 통합을 계산). 범심론/창발론 라벨은 곡선 *형태*에 사후-부착이 아니라 사전등록(F1296.1/2 가 형태를 미리 정의)하므로 동어반복 회피.

## Migration TODO
- [ ] N-sweep(또는 결합밀도 c-sweep) substrate 하네스, 동일 룰 family 고정
- [ ] big-Φ(N) 곡선 + 연속/불연속 판정 통계(최대 step Δ vs range)
