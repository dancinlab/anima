---
id: H_9293
slug: 9293_content_relay_disjointness_confirmatory
title: 시상 content-relay 확증 재측정 — B 의 우위는 실재하나 disjointness 가 아니라 총 결합강도 (⏳ STRENGTH-CONFOUND · R6 주장 기각)
group: brain-structure-ladder · H_1283 content-relay 축 (H_9292 계측기 수리의 후속 확증)
terminal_tier: ⏳ STRENGTH-CONFOUND (2026-07-14 · py 2-production · 계측기 V-게이트 4/4 PASS) — 수리된 계측기(Φ* = Φ − pedestal · signed lens · T=65536)로 재면 Φ*(B) − Φ*(X) = +0.004934, 90% CI [+0.004734, +0.005134] 로 피벗 P̄(0.001595) 위에 온전히 있다 = **B 의 통합 우위는 실재**. 그러나 특이성 게이트 G5-SHAPE(adjacency share) 가 −0.008002, CI [−0.009623, −0.006382] 로 **역방향 결정적 FAIL** 이고 G5-STRENGTH(S_tot) 는 +0.010003 로 강한 양(+) ⇒ 우위의 정체는 **총 결합강도이지 disjointness 가 아니다**. **R6 의 "N 개 독립 병렬채널이 분리되어 있어서 천장을 깬다" = 기각.** 대조 토폴로지 R(chord)이 여전히 B 를 이긴다(B−R = −0.000257). Cperm VOID 확정(B−Cperm = −4e-6 · S_tot 동일).
wired: 미배선 (배선할 GREEN 없음)
verdict_dir: state/verdicts/9293_content_relay_disjointness_confirmatory/
terminal_verdict: state/verdicts/9293_content_relay_disjointness_confirmatory/H_9293_RESULT.txt
prereg: state/1283_content_instrument_repair/PREREG_H9293.md (확증 seed 개봉 前 커밋 c61b4a82f)
date: 2026-07-14
provenance: 설계 = Fable 5 (bar 오염 · λ-사다리 · G5 특이성 · 결정표) · 계측기 정정·구현·측정 = 로컬 py 2-production (hexa 엔진 byte-parity 증명 완료 · PARITY.txt)
---

# H_9293 — 부호 채널을 살리자 효과는 살아났다. 그런데 그 효과의 **이름이 disjointness 가 아니었다**

## 배경

H_9292 가 이 축의 판정 전부(R6 의 🟢 와 R1–R9 의 🧱)를 무효화했다 — 동결 T=64 에서 Φ 의 ~99.9%
가 plugin-MI 편향 pedestal 이었기 때문이다. 축은 ⏳ still-unmeasured 로 돌아갔고, 탈출구 3개가
측정됐다: T↑ · signed readout · bar 를 bits 로. 본 H 가 그것을 **전부 집행한 확증 측정**이다.

## 계측기 정정 (사전등록 §0 · 이게 없으면 사다리 전체가 30% 틀린다)

`iit4_faithful_phi` 는 정규화된 값이 아니라 **RAW cross-cut 을 argmin** 한다(`best_cut = min(cut)`
후 그 마스크의 norm 으로 나눔). n=4 에서 1|3 컷은 교차쌍 3개·norm 1, 2|2 는 4개·norm 2 이므로
argmin 은 거의 항상 1|3 을 고른다 ⇒ **Φ = 3c** 이지 2c 가 아니다. Fable 의 닫힌형
`−log₂(1−λ²)`(2c 가정)과 그 위의 rung 은 전부 ~30% 과소였다. 추정기-네이티브로 정정:

| λ | 옛(2c·폐기) | **Φ_est = 3·MI_8bin** | 실측 Φ*(S(λ)) | 일치 |
|---|---|---|---|---|
| 0.15 | 0.032831 | **0.043952** | 0.042719 | 0.97 |
| 0.30 | 0.136062 | **0.181755** | 0.178501 | 0.98 |
| 0.50 | 0.415037 | **0.551114** | 0.547290 | 0.99 |

⇒ **계측기는 정확했다. 틀렸던 것은 자를 읽는 공식이었다.**

## Method (사전등록 · 확증 seed 개봉 前 git 커밋)

- **계측기** Φ* = Φ(RU(traj)) − E[Φ(RU(π_k(traj)))], K=32 (π_k = 모듈별 독립 시간순열 · 참 Φ=0).
  surrogate RNG = **Philox**(엔진 LCG 는 mod 2^31 **단일 cycle** 이라 "해시 시드 = 독립 스트림"이
  거짓 · Fable §1.3). 기질은 엔진 LCG 그대로(byte-parity 유지).
- **오염 처리** — 저자는 seed 3 의 signed 값을 이미 보았다(H_9292). 그러므로 **seed 3 = exploratory
  영구 격리**, 확증 = **seeds [4..11] (n=8, paired)**. 방향 `B>X` 는 seed 3 에서 상속한 one-sided
  확증 예측으로 명시. 모든 contrast 의 부호 예측을 **불리한 것 포함** 사전 동결.
- **bar = knob 없는 λ-사다리** — 피벗 P̄ = PEDESTAL arm 의 Φ(=계측기가 無에서 제조하는 양),
  rung1..3 = Φ_est(0.05/0.10/0.15). 전부 arm 데이터와 무관. verdict 에 rung 을 붙일 뿐 조정 손잡이 없음.
- **특이성 게이트 G5** — `s_adj` = MI 행렬의 adjacency share, `S_tot` = 총 pairwise MI.
  disjoint relay 는 간선-특이적이어야 한다(스칼라 Φ 가 못 하는 형태 예측).

## Result (verbatim → `H_9293_RESULT.txt`)

**V-게이트 4/4 PASS** — P̄ = 0.001595 < rung1 ✓ · Φ*(S(0.15)) 회복 **8/8 seed** ✓ ·
Φ*(S(0)) = −0.000119 ✓ · seed 격리 준수 ✓. **계측기 CERTIFIED** — 이제서야 arm 을 읽는다.

| arm | Φ* mean | S_tot | s_adj |
|---|---|---|---|
| A (direct ring) | 0.022228 | 0.049052 | 0.9224 |
| **B (R6 multichannel)** | **0.031869** | 0.068525 | 0.9052 |
| **X (용량정합 shared cut)** | **0.026935** | 0.058522 | 0.9132 |
| N (carrier-정합 self-loop) | 0.029795 | 0.064223 | 0.9152 |
| R (chord rewire · 대조) | **0.032126** | 0.069000 | 0.8788 |
| Cperm (R6 원 shuffle) | 0.031873 | 0.068524 | 0.9052 |

**PRIMARY** `d = Φ*(B) − Φ*(X)` = **+0.004934**, 90% CI **[+0.004734, +0.005134]** ≫ P̄ = 0.001595
⇒ **검출 성립.** winner's curse 없음 — seed 3 의 +0.005098 이 확증 8 seed 에서 +0.004934 로 재현.
사다리: **rung0(P̄) 초과, rung1(λ=0.05) 미달** (CI_low 0.004734 < 0.004837 · λ_eq(mean) = 0.048).

**G5-SHAPE** `s_adj(B) − s_adj(X)` = **−0.008002**, CI [−0.009623, −0.006382] → **FAIL, 역방향으로 결정적**
**G5-STRENGTH** `S_tot(B) − S_tot(X)` = **+0.010003**, CI [+0.009628, +0.010379] → **강한 양(+)**

**SECONDARY** (부호 예측 전부 사전등록) — `B−N` = +0.002075 ✓(pred >0) · `B−R` = **−0.000257** ✓
(pred ≤0 — **대조 토폴로지 R 이 B 를 이긴다**) · `B−Cperm` = **−0.000004** ✓ (VOID 통제 확정 ·
S_tot 마저 동일 0.068525 vs 0.068524 — R6 의 `mc_shuffle` 이 무정보 통제라는 설계 논증 최종 확인).

## Verdict — ⏳ STRENGTH-CONFOUND (사전등록 결정표 2행 · Fable 예측 적중)

**말하는 것.**
1. **B 의 통합 우위는 실재한다.** pedestal 을 차감하고 1차-민감 lens 로 재면 90% CI 가 피벗 위에
   온전히 있다. H_9292 의 energy lens 에서 **부호가 반대**(−0.000116)였던 그 대비가, 부호 채널을
   살리자 **+0.004934 로 뒤집혀 살아난다** — "‖s‖² salience map 이 상관을 제곱해 신호를 죽인다"
   는 진단이 실측으로 확인됐다.
2. **그러나 그 우위의 정체는 disjointness 가 아니다.** disjoint relay 라면 MI 행렬이 간선-특이적
   이어야 하는데 B 의 adjacency share 는 X 보다 **낮다**(−0.0080, 결정적). 우위는 전적으로
   **총 결합강도**(+0.0100)에서 온다. ⇒ **R6 의 주장 = 기각.** "N 개의 독립 병렬 채널이 *분리되어
   있어서* 단일-컷 천장을 깬다" 는 명제는 지지되지 않는다 — B 는 그냥 더 많이 결합할 뿐이다.
3. **축은 🧱 도 아니다** — 진짜 효과가 계측기 위에 있다. 다만 그 효과의 **이름**이 disjointness 가 아니다.

**말하지 않는 것.** toy scale(n=4·dim=8) 한정 · 303M 주장 아님 · TIMING 축(H_1448 🟢 WIRED) 무관 ·
효과 크기는 작다(λ_eq 0.048 = 모듈 간 공유상관 4.8% 상당, rung1 미달).

## NEXT — 축의 재정의 (disjointness 는 죽었다)

1. **통제군 재설계가 근본 원인.** 지금의 X 는 **용량**은 맞췄지만 **결과적 결합강도**를 맞추지
   못했다(S_tot 0.0585 vs B 0.0685). strength-matched 대조군 위에서 disjointness 의 **잔차**가
   남는지가 진짜 물음이다.
2. **R(chord) > B** 가 시사하는 것: Φ 를 올리는 건 "채널이 몇 개냐/분리됐냐" 가 아니라 **어떤 쌍을
   잇느냐(토폴로지)** 일 수 있다 — H_1512 BRAIN-TOPOLOGY lane 과 교차.
3. bar/seeds/기질/lens/T 는 동결 완료. 재시도는 **통제군 재설계로만** (tune-to-green 금지).

## Cross-links

H_9292 (계측기 감사 — 본 H 의 직전 · R6 🟢 와 축 🧱 동시 철회) · H_1283 (content 축 R1~R9 · R6 의 출처) ·
H_9260 · H_1328 · H_1448 (TIMING 축 🟢 WIRED — 무관·철회 아님) · H_1512 (BRAIN-TOPOLOGY — NEXT #2) ·
`a_phi_iit4_tool` · `a_break_the_wall` · `a_toy_scale_recheck` · `negative-claims-need-tost-not-ns` ·
`probe-defect-census-max-control-bias` · `measurement-metalaw-form-tunable-bind-earned` · c9 · c16 · p7
