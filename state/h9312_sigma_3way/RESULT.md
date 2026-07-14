# H_9312 — σ 3-갈래 분해 · 결과 (INVALID · 계기 결함)

PREREG.md 동결 → tape 2000 tick 확보 → 사전등록 분석 그대로 집행.
**verdict = INVALID** (사전등록 규칙: POS 참값비 [0.8,1.25] 밖 ∨ degeneracy ⇒ PASS/FAIL 금지).

## 왜 INVALID 인가 — σ 의 self 축이 스코어 구간에서 **수치적으로 죽어 있다**

`self_ctx_live = clip01(self_cos(self_live, self_boot))` 궤적 (같은 tape, verbatim):

| tick | 0 | 20 | 50 | 100 | 200 | 400 | 2000 |
|---|---|---|---|---|---|---|---|
| self_ctx_live | 1.0 | 0.116 | 1.8e-3 | 1.6e-6 | 1.4e-12 | 1.0e-24 | **8.8e-122** |
| self_phasic | 1.0 | 0 | 0.047 | 0.497 | **0.5** | **0.5** | **0.5** |

- 스코어 구간(tick ≥ 50) sd(self_ctx_live) = **8.0e-5**, tick ≥ 400 에서는 sd = **8e-26** (= 0).
- 원인: `ev_axis` 가 2000 tick **전부 1(af_val)** — self_live 가 **단일 축으로만** 계속 drift ⇒
  boot 과의 코사인이 지수적으로 언더플로.
- 결과: tick ≳ 100 부터 `self_phasic ≡ 0.5` = **중립 상수** ⇒ idle_slf ≡ idle(prod) ⇒
  **ΔEff_self ≈ 0 은 산술적으로 강제**된 값이지 기질 사실이 아니다.
  (같은 런의 엔진 자체 출력: `ΔEff_self = 1/1170`, `ARM-PERM = 17/1170`, `G_self=20.2`.)
- 엔진의 degeneracy 체크는 **calib 0–49**(self 가 1.0→0.0018 로 살아있는 유일한 구간)에서
  |Δself| 중앙값을 재고, **스코어는 50 이후**(축이 죽은 구간)에서 한다 ⇒
  **캘리브 구간/스코어 구간 불일치가 THEATER 를 기계적으로 생산**한다.

## 부수적 계측 사실 (같은 tape · 전부 verbatim)

- **e_live ≡ [idle ≥ 30]** — 2000/2000 tick 일치, 불일치 0.
  drive margin (motiv−thr) 은 **한 번도 음수가 아니다** (min +0.059, mean +0.160) ⇒
  동기 게이트는 항상 열려 있고 emit 은 **오로지 rate-gate 의 결정론적 함수**다.
  ⇒ self 가 emit 에 닿을 수 있는 통로는 idle 하나뿐이며, 그 통로의 self 항은 위에서 죽었다.
- **8-lane 중 5개가 상수** (tick≥50 sd=0): rel_lane · af_val · allo_ctx · bal_lane · gap_ctx.
  움직이는 건 coh_lane(sd .078) · ag_conflict(.030) · nov_ctx(.005) 뿐 ⇒
  $0 no-decode 계기의 "8-lane 기질 상태"는 실질 **2차원**이다 ⇒ PRESENCE(ridge R²)는
  이 tape 에서 **측정 불가**(테스트 반쪽의 self 분산 0 ⇒ R² = NaN).

## 사전등록 수치 (전량)

- n_scored 1950 · n_fit 975 · n_test 975 · **MDE(2σ) = 0.032 acc** (검정력은 충분했다).
- INFO: D-acc_EXP = **0.600** = base-rate 0.600 = CIRC null median 0.600 (200 원형시프트, p_emp=0.915)
  · EARNED = **−1.6e-7 nats** · TOST(±0.05 acc, ±0.02 nats) = **등가 PASS**.
- PEDESTAL(참값 0, AR(1) 정합 대리스트림): D-acc 0.601 · nats −0.0020 ⇒ **EXP 와 구분 불가**.
- **POS(참값 0.65 spike-in): 측정 0.332 ⇒ 비율 0.51 → 게이트 [0.8,1.25] FAIL** ⇒ INVALID.
  (POS 가 깨진 이유도 같은 붕괴다: self 가 단조 언더플로 ⇒ self_hi 가 전반 1 / 후반 0 으로
  라벨이 시간축에서 뒤집힘. 이 계기로는 참값을 아는 신호조차 회수 못 한다.)
- PRESENCE: R²_EXP = **NaN** (테스트 반쪽 self 분산 0) · PEDESTAL R² 0.00016 · CIRC p95 −0.015.

## 판독

INFO 의 TOST 등가(정보 0)는 **형식상 통과했지만 인용 금지** — 같은 tape 에서 POS 가 죽었으므로
"정보 없음"이 아니라 **"이 계기로는 있는 정보도 못 찾는다"** (power-before-negative-verdict 재판).
3-갈래(데이터 부재 / 표현 부재 / 소비 부재)는 **여전히 미분할**이다.
