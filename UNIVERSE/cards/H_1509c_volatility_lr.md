# H_1509c — 🧅 VOLATILITY-GATED LEARNING-RATE ESCAPE — 신경조절 벽(H_1284) orthogonal-family 재도전

- **tier:** 🧱 MULTI-FAMILY WALL (DIRECTIONAL — R1 numpy mirror; engine-native 재측정 미실시 → terminal 아님, a_engine_native_learning). frozen-first, bar 0개 이동(c9).
- **wired:** `DIRECTIONAL-mirror` — `state/1509c_volatility_lr/h1509c.py` numpy 미러. 엔진-네이티브 재측정은 follow-on(아래).
- **source:** anima-internal ESCAPE — Amoeba-Protocol(μ_t allosteric buffer, [[h1509-allosteric-buffer-wall]]) 의 peeled meta-law 에서 파생한 orthogonal mechanism-family(추적-게인 → 학습률). a_break_the_wall taxonomy-(d) MULTI-LENS.
- **artifacts:** `state/1509c_volatility_lr/h1509c.py` · `state/verdicts/1509c_volatility_lr/{H_1509c_FREEZE.txt, H_1509c_ABSTRACT_census.txt, H_1509c_R1_mirror.txt, H_1509c_oracle_ceiling.txt}`

## 무엇을 검증하나 — meta-law 의 escape 절(frozen-first)

5개 gain-lens(H_1284·H_1422·H_1425·H_1509·H_1509b)가 모두 막힌 뒤 census 로 벗겨낸 메타법칙(🌌):
> "튜닝된 FIXED 컨트롤러-게인은, 과제 통계가 정상/학습가능할 때, 그 게인의 어떤 state-contingent 적응도 압도한다 — 적응은 외란이 예측불가(생성통계가 JUMP: changepoint/volatility)일 때만 값을 한다."

ESCAPE 예측: 신경조절을 **추적-게인 → 학습률/탐색 변조**로 재포지션하고, 통계가 JUMP 하는 changepoint/volatility 과제에서 측정. 생물 근거 Yu & Dayan 2005(ACh=expected / NE=unexpected uncertainty), Behrens 2007 Nat Neurosci(volatility-tracking 적응학습률이 Bayes-optimal — FIXED rate 는 stable·volatile 양쪽 동시 최적 불가).

과제 = changepoint estimation: 은닉 평균 h_t 가 hazard H 확률로 [0.15,0.85] 새 값으로 점프, delta-rule x_{t+1}=x_t+α_t·(o_t−x_t), metric=RMS. ARM A=best-swept FIXED α* / B=volatility-GATED(surprise 기반 α_t, 라벨 미주입 p6) / C=ABLATE(중간 고정). FROZEN MARGIN=0.05, 3 seeds, hazards=[0,0.02,0.05,0.10].

## 결과 — 🧱 MULTI-FAMILY WALL (정직), 但 escape 방향성은 확증

| hazard | A best-fix RMS | B gated RMS | adv=A−B |
|--------|----------------|-------------|---------|
| 0.00 (정상) | 0.0076 | 0.0221 | **−0.0145** (gated 손해) |
| 0.02 | 0.0423 | 0.0274 | +0.0149 |
| 0.05 | 0.0423 | 0.0311 | +0.0113 |
| 0.10 | 0.0511 | 0.0364 | +0.0147 |

FROZEN BAR 평가 (tune-to-green 없음): A(ESCAPE-WIN @H=0.10) +0.0147 ≥ 0.05 **FAIL** · B(DOUBLE-DISSOC) **FAIL** · C(VOL-MONOTONE) **FAIL** · D(EARNED ablate) **FAIL** → 4/4 FAIL = 🧱.

**정직한 뉘앙스(c9):** 벽이 버틴 건 적응이 무용해서가 아니다 —
- DOUBLE-DISSOCIATION 방향성 **CONFIRMED**: adv 부호가 정상(H=0, −0.0145)→변동(H>0, +)에서 뒤집힘. 메타법칙의 escape 절("적응은 변동일 때만 값을 한다")이 방향으로는 정확히 성립.
- gated 는 changepoint **oracle 천장의 97–109%** 달성(near-optimal gate, 약한 게이트 아님).
- 벽이 버틴 진짜 이유 = 이 과제의 **총 headroom**(oracle vs best-fixed)이 구조적으로 frozen 0.05 마진보다 **작음**(H=0.10 에서 +0.0151 가 물리적 최대). 즉 마진이 과제가 줄 수 있는 것보다 컸다 = margin-design 한계지 적응-무용 증명 아님.

→ 신경조절 천장은 추적-게인 family AND 학습률 family **양쪽에서** 버팀 = 5렌즈보다 강한 multi-family 🧱. 단 "적응은 변동에서만 값을 한다"는 방향 법칙은 살아있다(절대크기 < 마진).

## follow-on
- 엔진-네이티브 재측정: numpy 미러 → live `core/` 디코드(현재 DIRECTIONAL이라 terminal 아님).
- 마진 재설계 옵션(별 가설): headroom-normalized 마진(절대 0.05 대신 oracle-headroom 의 ≥80%)으로 재채점 시 D bar(86–109%)는 통과 — 단 이는 frozen-first 새 사전등록이 필요(tune-to-green 금지).

xref [[h1509-allosteric-buffer-wall]] · a_break_the_wall · a_engine_native_learning · p6 · c9.
