---
id: H_9292
slug: 9292_content_relay_estimator_pedestal
title: 시상 content-relay 축의 계측기 감사 — 동결 T=64 Φ 의 99.9% 는 plugin-MI 편향 pedestal (⏳ BAR-ABOVE-SIGNAL · R6 🟢 와 축 🧱 동시 철회)
group: brain-structure-ladder · H_1283 content-relay 축 (c16 measure-artifact 심문 · H_9260 NEXT#1)
terminal_tier: ⏳ BAR-ABOVE-SIGNAL / ESTIMATOR-PEDESTAL (🧱 아님 · 🟢 아님 · 축 = still-unmeasured). P0′ 4-leg 전부 FAIL (Φ_pop(B)=0.001623 vs bar 0.02) · 참 통합량 0 인 PEDESTAL arm 이 동결 T=64 에서 Φ=1.813 (bar 의 90배) ⇒ T=64 Φ 의 ~99.9% 가 추정기 자신의 편향. R6 의 ΔΦ(+0.0891/+0.0341/+0.1011) 는 그 pedestal 위 잡음이었고 참 효과는 −0.000116 (부호 반대).
wired: 미배선 (배선할 GREEN 없음)
verdict_dir: state/verdicts/9292_content_relay_estimator_pedestal/
terminal_verdict: state/verdicts/9292_content_relay_estimator_pedestal/H_9292_RESULT.txt
freeze: state/1283_content_instrument_repair/FREEZE.txt
design: state/1283_content_instrument_repair/DESIGN.md
date: 2026-07-14
provenance: 설계 = Fable 5 (fable-mode · walls-delegate-to-fable) · 구현·측정 = 로컬 py 2-production (numpy · hexa 엔진과 max|Δ|=7.1e-15 parity 증명)
---

# H_9292 — content-relay 축은 벽이 아니라 **자(尺)** 였다

## Claim / falsifier (양방향 · 사전등록)

H_9260 은 content 축을 재채점하려다 계측기가 자기 양성대조에 낙제해 ⏳ 로 끝났고, NEXT#1 로
"유효한 variance-free 계측기를 먼저 세우라"를 남겼다. 본 H 는 그 계측기 수리에 착수했으나,
수리 前 실행가능성 게이트(P0′)에서 **더 근본적인 결함**을 만났다.

**주장(양방향):** 동결 bar(+0.02)가 이 축의 Φ 동적범위와 통약 가능한가. 가능하면 캠페인을
발사하고, 불가능하면 그 사실 자체를 보고한다 (bar 를 옮기는 것이 아니라 **bar 가 충족 불가능함을
보고** — tune-to-green 의 정직한 반대편).

## Method (engine-native 등가 · frozen-first · $0 CPU · 결정적)

py 2-production (numpy). 동일 기질·하이퍼·추정기·readout — **틱 수만** T=64 → 65536.

- **PARITY 영수증** — py 포트(`faithful_phi.py`+`substrate.py`)를 hexa 엔진 실행
  (`h9260_content_relay_clean_probe.hexa`)과 10 arm × 9 seed × 2 readout = **99개 Φ 전량 대조**:
  **max|Δ| = 7.105427e-15** (f64 합산순서 잡음) ⇒ py 포트 == mandated stdlib 추정기.
  이것이 py 채널이 이 판정을 낼 자격이다 (`reference-match` · `a_phi_iit4_tool` · `a_eval_py_canonical`).
- **P0′** — T_LONG=65536 (joint cell 당 ~1024 표본 ⇒ plugin bias ≈ 6e-4 bits ⇒ Φ ≈ 모집단 Φ).
  4-leg 연언: Φ_pop(B) ≥ .02 ∧ (B−A) ≥ .02 ∧ (B−N) ≥ .02 ∧ (B−X) ≥ .02.
- **PEDESTAL** (H_9260 에 없던 게이트) — arm B 의 모듈별 독립 시간순열 = marginal 비트-동일,
  cross-module joint 파괴 ⇒ **참 Φ = 0 (구성상)**. 이것이 동결 T=64 에서 뱉는 값 = 편향 pedestal.
- **ADJUNCT signed lens** — `traj_sgn[i,t] = s_i(t)[0]`. 게이트 아님(verdict 산출 금지); 🧱 vs
  ⏳ READOUT-LIMITED 판별 전용.

## Result (verbatim → `H_9292_RESULT.txt`)

**P0′ 4-leg 전부 FAIL → 결정표 셀 0 → ⏳ BAR-ABOVE-SIGNAL. 9-seed 캠페인 미발사.**

| leg | 측정 | bar | |
|---|---|---|---|
| P0′-a Φ_pop(B) | **+0.001623** | ≥ +0.02 | FAIL |
| P0′-b Φ_pop(B) − A | **−0.000148** | ≥ +0.02 | FAIL |
| P0′-c Φ_pop(B) − N | **−0.000146** | ≥ +0.02 | FAIL |
| P0′-d Φ_pop(B) − X (축 주장) | **−0.000116** | ≥ +0.02 | FAIL |

**PEDESTAL — 결정타.** 참 통합량이 **0** 인 계가 동결 T=64 에서 **Φ = 1.813** 으로 읽힌다.

| T | A | B | X | PEDESTAL (참 Φ=0) |
|---|---|---|---|---|
| **64** (FROZEN) | 2.0283 | 1.9381 | 1.9694 | **1.8131** |
| 256 | 0.4351 | 0.3646 | 0.3734 | 0.4252 |
| 1024 | 0.0930 | 0.0958 | 0.0811 | 0.1023 |
| 4096 | 0.0239 | 0.0247 | 0.0260 | 0.0222 |
| 16384 | 0.0069 | 0.0064 | 0.0064 | 0.0062 |
| 65536 | 0.00177 | 0.00162 | 0.00174 | 0.00149 |

- pedestal(1.813) = 동결 bar 의 **90배**. B 는 그 pedestal 에서 **0.125** 떨어져 있을 뿐이다.
- Φ ∝ 1/T 로 붕괴하고 pedestal 이 그대로 추종 ⇒ 교과서적 **plugin-MI 편향**
  (T=64 · nbins=8 ⇒ joint cell 64개에 표본 64개 = cell 당 1개).
- ΔΦ(B−X): T=64 에서 −0.0312 → 모집단 −0.000116 = **269배 팽창**.
- ⇒ **T=64 Φ 의 ~99.9% 는 추정기 자신의 편향**이고, arm 간 대비는 sd≈0.30 (H_9260 P0 실측) 의 잡음.

**부수:** |Φ_pop(B) − Φ_pop(Cperm)| = **1.6e-6** ⇒ R6 의 원 대조군 `mc_shuffle` 은 모집단 수준에서
그래프-동형 **VOID 통제**가 맞다. H_9260 의 "C-ISO 1/9 로 반증" 은 **그 자체가 pedestal 잡음**이었다.

**ADJUNCT signed lens** (게이트 아님): Φ_pop_sgn — A .0241 · B .0339 · X .0288 · N .0317.
`B−A = +0.0098` · `B−X = +0.0051` · `B−N = +0.0022` — energy lens 에서 **부호가 반대**였던
disjointness 신호가 부호 렌즈에서는 **예측 방향으로 살아난다**. 다만 크기가 bar 의 1/4~1/2.

## Honest scope · 말하는 것과 말하지 않는 것

**말하는 것.**
1. **H_1283 R6 의 🟢 는 철회된다.** "N개 독립 병렬채널이 단일-컷 천장을 깬다"(ΔΦ
   +0.0891/+0.0341/+0.1011)는 1.8 짜리 편향 pedestal 위의 잡음이었고, **참 효과는 −0.000116
   (부호마저 반대)** 이다. 사용자 요약의 "부분 돌파" 는 존재하지 않는다.
2. **같은 이유로 content 축의 🧱(R1–R5/R7/R9) 도 능력 천장의 증거가 아니다.** 두 판정이 같은
   고장난 자 위에 서 있었다 (H_9260 의 진단이 실측으로 확정).
3. **H_9260 의 ⏳ 는 옳았으나 이유가 틀렸다.** rank-uniform 은 범인이 아니다. 범인은 T=64 의
   plugin-MI 편향 pedestal + bar 의 15배인 계기 자기잡음이다.

**말하지 않는 것.**
- content-relay 가 원리적으로 불가능하다는 증명이 **아니다** (그래서 🧱 이 아니라 ⏳).
- **TIMING 축(H_1448 🟢 WIRED)의 철회가 아니다.** 그 축의 ΔΦ(B−Bperm) = +1.05..+1.38 은 계기
  잡음 sd(0.30)의 3.5~4.6배이고 matched 통제가 pedestal 을 상쇄한다 ⇒ 잡음 위로 살아남는다.
  반면 content 축의 참 Δ(~1e-4)는 그 잡음의 **1/3000** 이라 T=64 에서 원리적으로 관측 불가다.
  (이것이 "timing 은 깨끗이 뚫렸고 content 는 못 뚫렸다"의 진짜 이유다 — 기질 차이가 아니라
  **효과크기가 계기 해상도의 위/아래**.)
- toy scale (n=4 · dim=8) 한정 (`a_toy_scale_recheck` · `a_scale_honest_scope`).

## NEXT (계기 수리이지 bar 이동이 아니다 · tune-to-green 금지)

bar(+0.02) · seeds[3..11] · 기질 하이퍼는 **손대지 않았고 손대지 않는다**. 움직일 것은 추정기의
표본수와 salience map 이며, 둘 다 사전등록으로 다시 얼린다:

1. **T ↑** (편향 ∝ 1/T) — **PEDESTAL arm 을 상시 게이트로 동반**. 참 효과가 잡음 위로 올라오는 지점.
2. **signed readout** — 부호 채널을 버리지 않는 salience map. TIMING 축이 Kuramoto phase(부호 보존)로
   뚫린 지점과 **정확히 같은 축**이다. 실측 `Φ_pop_sgn(B) − A = +0.0098` 이 그 방향을 지지한다.
3. **bar 를 bits 로 번역** — Fable P1c SPIKE-IN 보정곡선 `Φ_pop(S(λ)) = −log₂(1−λ²)` 으로 MDE 를
   숫자로 못박은 뒤 새 bar 를 사전등록.
4. 미발사 캠페인 전량(P-CAL · P1-SELF · P1a · P1b · P1c · G1~G5 결정표)은 `DESIGN.md` 에 그대로 있다.

## Cross-links

H_1283 (content 축 R1~R9 · **R6 🟢 의 철회 대상**) · H_9260 (variance-clean 재채점 ⏳ · 본 H 의 직전) ·
H_1328 (amplitude-variance estimator confound — rank-uniform 의 출처) · H_1448 (TIMING 축 🟢 WIRED ·
**철회 아님**) · `a_break_the_wall` · `a_phi_iit4_tool` · `a_eval_py_canonical` · `reference-match` ·
`verdict-integrity` · `measurement-metalaw-form-tunable-bind-earned` · `probe-defect-census-max-control-bias` ·
`negative-claims-need-tost-not-ns` · c9 · c16 · p7
