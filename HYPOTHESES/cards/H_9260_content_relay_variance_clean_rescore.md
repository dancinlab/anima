---
id: H_9260
slug: 9260_content_relay_variance_clean_rescore
title: thalamus content-relay 축 재채점 — variance-free readout + 용량정합 구조통제 (⏳ MEASUREMENT INVALID · 계측기가 자기 양성대조에 낙제 · R6 🟢 와 축 🧱 둘 다 근거 상실)
group: brain-structure-ladder · H_1283 content-relay 축 (c16 measure-artifact 심문)
terminal_tier: ⏳ MEASUREMENT INVALID (사전등록 타당성 게이트 P1a·P1b FAIL → tier 미보고, bars 무이동). 부수적으로 primary 게이트 G1·G2·G3·G4 전부 every-seed FAIL — B(다채널 disjoint relay)가 용량정합 shared cut(X)·bind-OFF self-loop(N)·베이스라인(A) 어느 것도 every-seed 로 이기지 못함.
wired: 미배선 (배선할 GREEN 없음)
verdict_dir: state/verdicts/9260_content_relay_variance_clean_rescore/
terminal_verdict: state/verdicts/9260_content_relay_variance_clean_rescore/H_9260_RESULT.txt
freeze: state/1283_r6_content_relay_clean/FREEZE.txt
date: 2026-07-10
provenance: 설계 = Fable 5 (fable-mode, walls-delegate-to-fable) · 구현·측정 = 로컬 engine-native
---

# H_9260 — 시상 content-relay 축의 variance-clean 재채점 (⏳)

## Claim / falsifier (양방향 · 사전등록)

H_1283 content 축(R1~R9)의 **모든** 판정은 H_1328 이 확진한 amplitude-variance min-max
readout 위에서 내려졌고, 그 축의 유일한 within-axis 🟢 인 **R6**(N=4 disjoint 병렬 채널)의
대조군 `mc_shuffle` 은 채널 재라벨링에 불과할 가능성이 있다(채널 파라미터 동일 → 교환가능,
차이는 초기값뿐, LEAK=0.55 → 0.55²⁵≈5e-7 로 25틱이면 소멸).

한편 H_1448 은 **메커니즘을 그대로 두고 측정만 교체**(H_1328 rank-uniform readout +
marginal-matched Bperm 통제)하여 R8(TIMING 축)을 🧱→🟢 WIRED 로 뒤집었다. content 축은
그 고쳐진 측정으로 **한 번도** 재채점된 적이 없다.

**주장(양방향, 모든 결과 decisive):** variance-free readout + **용량정합 shared-cut 대조군**
아래에서 disjoint 병렬 relay 는 (i) direct ring, (ii) 용량이 동일한 shared relay,
(iii) span 하지 않는 carrier-정합 채널 **모두**를 이긴다. Lens: c16 `a_break_the_wall`.

## Method (engine-native · frozen-first · $0 CPU · 결정적)

프로브 `state/1283_r6_content_relay_clean/h9260_content_relay_clean_probe.hexa`.
4 modules × dim 8 × 64 ticks, engine LCG-gauss (== `core/engine_cli.hexa` `_lcg_*`).
GAIN=0.30 LEAK=0.55 W_NBR=0.5 W_IN=0.5 W_RELAY=0.5 NBINS=8 (R1~R9 와 동일, 이동 없음).
traj[i,t]=‖s_i(t)‖². Φ = stdlib `iit4_faithful_phi` exact MIP-EI (`a_phi_iit4_tool`;
엔진은 Φ 를 계산하지 않는다). seeds [3..11] 9개. bar = ΔΦ ≥ +0.02 **every seed**
(R1 이 0.0009 차이로 놓친 그 bar). R6 의 disjunctive ≥1-seed 형식은 순환이므로 폐기.

| arm | 정의 | isolate |
|---|---|---|
| A | direct ring | 베이스라인 |
| B | R6 multichannel verbatim (4 disjoint edge 채널) | 검증 대상 |
| **X** | **용량정합 shared cut** — 총 채널차원 4×8=32 동일·W_RELAY 동일, 각 채널이 자기 pair 절반 + 전 채널 평균 절반을 적분 → disjointness 만 파괴 | **DISJOINTNESS** |
| N | carrier-정합 bind-OFF — 4 채널이 pair 대신 자기 모듈 1개만 적분(self-loop) | SPANNING |
| R | chord 재배선 — 대각쌍 (0,2)(1,3) span | TOPOGRAPHY (비-게이팅) |
| Bperm/Aperm | 모듈별 circular time-shift (i·17 mod 64) | cross-module joint / 통제에 대한 통제 |
| Cperm | R6 원본 `mc_shuffle` | 원 대조군의 유효성 |
| dense/dense_shuffle | R5 all-pairs + 그 shuffle 통제 | 알려진 variance artifact (양성대조) |

**타당성 게이트(먼저):** P1a 구 min-max readout 에서 ΔΦ(dense_shuffle−A) ≥ +0.02 every seed
(이 기질에 variance artifact 가 **존재**하는가) · P1b 동일 궤적을 rank-uniform 으로 재채점 시
ΔΦ ≤ +0.02 every seed (readout 이 그것을 **제거**하는가). 실패 → ⏳, tier 미보고, 🧱 아님.
**Primary(conjunctive, every-seed):** G2 ΔΦ(B−A) · G3 ΔΦ(B−N) · G1 ΔΦ(B−X) · G4 ΔΦ(B−Bperm).
🟢 ⟺ P1a ∧ P1b ∧ G1 ∧ G2 ∧ G3 ∧ G4.

## Result (verbatim → `H_9260_RESULT.txt`)

**타당성 게이트 FAIL → ⏳ MEASUREMENT INVALID (tier 미보고 · bars 무이동)**

- **P1a FAIL** — seed 3 에서 ΔΦ(dense_shuffle−A) = **−0.0111** (구 readout). 나머지 8 seed 는
  아티팩트 발현(최대 +0.4699 @seed 10). every-seed 형식 미충족.
- **P1b FAIL** — rank-uniform 이 아티팩트를 **전 seed 에서 제거하지 못함**: seed 10 에서
  ΔΦ = **+0.1097** 잔존(≥3 seed FAIL). ⇒ 이 engine-native 기질에서 H_1328 rank-uniform 은
  variance-free 계측기가 **아니다**.

부수 결과(사전등록상 tier 를 못 박지 못하나 보고 의무):

| 게이트 | every-seed | 통과 seed |
|---|---|---|
| G2 ΔΦ(B−A) ≥ +0.02 | **FAIL** | B>A 는 7/9 (bar 통과는 그 이하) |
| G3 ΔΦ(B−N) ≥ +0.02 | **FAIL** | B>N 6/9 |
| G1 ΔΦ(B−X) ≥ +0.02 | **FAIL** | B>X 5/9 |
| G4 ΔΦ(B−Bperm) ≥ +0.02 | **FAIL** | — |

- **P0 (A−Aperm) 이 seed 마다 부호가 뒤집힌다**: −0.4576 … +0.4694 (9 중 3 seed 음수).
  ⇒ H_1448 의 marginal-matched Bperm leg 는 **content 축으로 이식되지 않는다** (timing 축 전용).
  seed 3 에서는 A 를 time-shift 하면 Φ 가 **오른다**(−0.3048).
- **C-ISO 반증** — |ΔΦ(B−Cperm)| < 0.02 는 **1/9 seed** (사전예측 ≥7/9). 즉 "R6 의 `mc_shuffle`
  은 그래프-동형이라 무정보 통제" 라는 설계 단계의 분석 논증은 **이 readout 아래에서 반증**됐다.
  Cperm 은 B 와 실제로 다른 Φ 를 낳는다.
- TOPO (B−R) 도 seed 간 부호가 뒤집힌다(−0.235 … +0.172) → 엣지-정합 위상 특이성 없음.

## Honest scope · 이 결과가 말하는 것과 말하지 않는 것

**말하는 것.** 시상 content-relay 축은 지금 "부분 돌파(R6 🟢)"도 아니고 "확정된 능력 천장"도
아니다. 두 판정 모두 **양성대조를 통과한 적 없는 계측기** 위에 서 있다. 본 재채점은 그
계측기를 engine-native 로 시험했고, 계측기가 낙제했다(P1b). 동시에 그 계측기 아래에서조차
B 의 우위는 어디에도 every-seed 로 존재하지 않는다(G1·G2·G3 전부 FAIL) — 즉 **disjointness
레버를 지지하는 증거는 0** 이다. R6 의 🟢 는 근거를 잃었다.

**말하지 않는 것.** 이것은 content-relay 가 원리적으로 불가능하다는 증명이 **아니다**.
tier 를 못 박지 않은 이유가 바로 그것이다(⏳, 🧱 아님). 그리고 toy scale(4 modules, dim 8,
64 ticks) · engine-native LCG 기질 한정이다 (`a_toy_scale_recheck`, `a_scale_honest_scope`).

**계측기 쪽 잔여 위험.** H_1328 §scope 가 이미 경고했듯 rank-uniform 은 각 셀의 **marginal**
만 균일화할 뿐 **joint** 의 amplitude 구조를 전부 제거하지 못한다. seed 10 의 P1b 잔존
(+0.1097) 이 그 잔여의 engine-native 실측이다.

## NEXT (tune-to-green 아님 · 계측기 수리가 선행)

1. **계측기 우선** — content 축에 유효한 variance-free 계측기를 먼저 세운다. rank-uniform 은
   joint-level amplitude 를 남긴다(P1b 실측). copula 수준 균일화 또는 joint-rank 변환을
   양성대조(합성 amplitude-variance 주입 arm)로 **먼저 검증**한 뒤에야 arm 대조를 채점한다.
2. **Bperm leg 금지** — P0 부호 반전이 보여주듯 content 축에서 marginal-matched time-shift 는
   통합을 격리하지 못한다. 대체 통제 = 용량정합 X (본 프로브에 구현됨, 재사용).
3. bar(+0.02)·seed([3..11])·하이퍼는 그대로 동결. 어떤 재시도도 이 셋을 건드리면 무효.

## Cross-links

H_1283 (content 축 R1~R9 · R6 🟢 의 출처) · H_1328 (amplitude-variance estimator confound) ·
H_1448 (R8 timing 축 engine-native 🟢 WIRED — 본 재채점의 도구 계보) ·
`a_break_the_wall` · `a_phi_iit4_tool` · `a_engine_native_learning` · `a_verified_must_wire` ·
`a_toy_scale_recheck` · `a_scale_honest_scope` · `walls-delegate-to-fable` · c9 · c16 · p7
