---
id: Hc_1297
slug: phi-emergence-link-substrate-independence
title: Φ→emergence 매핑의 substrate-독립성 — big-Φ 가 같은(matched) 두 이질 substrate 는 같은 emergence(LZ/EI)를 보이는가, 아니면 링크가 substrate-의존인가
domain: meta · substrate · consciousness · information
status: candidate-unverified
seed: H_011/H_022/H_215 (Φ *값*의 다중실현/substrate-독립) · H_670 (Φ-복잡도 *순서* family 일반화) — Φ↔emergence *링크 자체*의 substrate-전이성은 미검정 (matched-Φ controlled pair)
axes_seed: UNIVERSE/AXES.md R8 (meta) · substrate-independence 축
exploration_method: E5 (matched-Φ controlled-pair probe) + E16 (cross-substrate family: ECA vs random Boolean net vs Kuramoto-discretized)
verdict_tier_target: 🟢 SUPPORTED (matched-Φ → matched-emergence across substrates) OR 🔴 CLOSED-NEGATIVE (matched-Φ 인데 emergence 발산 → 링크 substrate-의존)
hexa_only: true
deterministic: true
llm: none
---

## Hypothesis

H_011/H_022 는 Φ *값*이 substrate-독립(다중실현)임을 다뤘고 H_670 은 Φ-복잡도 *순서*가 family 전반 일반화됨을 다뤘다. 미검정 빈틈: **Φ→emergence 매핑 자체가 substrate-독립인가?** 가설 H1: big-Φ 값을 *맞춘*(matched) 두 이질 substrate(예: ECA 룰 vs random Boolean network vs 이산화 Kuramoto)는 *같은 emergence 측도*(LZ-복잡도 또는 EI-gain)를 보인다 — `|emergence_A − emergence_B|` 이 matched-Φ 쌍에서 unmatched-Φ 쌍보다 유의하게 작다. 즉 "Φ 가 같으면 창발도 같다"가 substrate 를 넘어 성립.

## Why

이것은 H_912 의 가장 깊은 일반화 질문이다 — Φ↔emergence 관계가 *법칙*이라면 substrate 를 바꿔도 같은 Φ 는 같은 emergence 를 줘야 한다(다중실현). 링크가 substrate-의존이면 "Φ↔emergence" 는 ECA-국소 artifact(H_670 의 'ECA 전용 ordinal' 우려, EVOL/SPATIAL tail 의 detector-artifact 계열)이고, substrate-독립이면 진짜 법칙. matched-Φ controlled pair 는 H_289(위상 confound)·H_670(순서) 이 못 한 *직접 통제 비교*. engine: eca_tpm + random-Boolean-net TPM + big_phi + LZ/EI 재사용.

## Pre-Registered Falsifier

- **F1297.1 (MATCHED-PHI-MATCHED-EMERGENCE)**: matched-Φ 쌍의 평균 `|Δemergence|` 이 unmatched-Φ 쌍의 평균 `|Δemergence|` 보다 작지 않음(또는 차이 < 측정 noise) → H1 FALSIFIED (링크 substrate-의존, closed-negative).
- **F1297.2 (PHI-MATCH-VALID)**: "matched-Φ" 쌍의 실제 Φ 차이가 사전 tolerance(예: |ΔΦ| < 0.05×range) 밖이면 → 매칭 무효(vacuous), 측정 재설계.
- **F1297.3 (TWO-SUBSTRATE-MIN)**: 최소 2개 이질 substrate-family(ECA + random Boolean net) 측정 — 단일 family 면 substrate-독립 주장 vacuous.
- **F1297.4 (DETERMINISM)**: re-run byte-identical (확률 net 이면 seed-고정 다중-seed 결정 재현).

## Circularity Guard

Φ-매칭(통제변수)과 emergence(종속변수, LZ/EI)는 독립 정의 — Φ 로 짝짓고 *다른* 축(emergence)의 일치를 보는 것이라 동어반복 아님. emergence 를 Φ 로 정의하면 자명-참이 되므로 emergence 는 반드시 LZ 또는 EI(Φ 와 독립 측도)로 고정, 결과에 명시.

## Migration TODO
- [ ] random Boolean network TPM 하네스(ECA 와 동일 n, big_phi 호환)
- [ ] matched-Φ 쌍 vs unmatched-Φ 쌍 sampling + |Δemergence| 비교, ≥2 substrate-family
