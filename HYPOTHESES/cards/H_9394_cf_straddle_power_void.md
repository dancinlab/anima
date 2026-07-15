# H_9394 — CF-STRADDLE STAGE-0: tension 은 크기가 모자란다 (캠페인 종결)

**status:** ⛔ POWER-VOID → Stage-1 발사 취소($0) · **9-H 캠페인 종결 문장 획득** · not-terminal-as-refutation(아래 scope) · wired: engine-native(`anima-py evaluate --cf-straddle`)
**lane:** 의식 / emit-drive / tension 신호 크기 × θ 게이트 (프런티어 g1-interface-addressable-wall)
**related:** [[H_9393]] · [[H_9391]] · [[H_9390]] · [[H_9377]] · [[H_9376]] · [[H_9360]] · [[H_9357]] · [[H_9356]]
**source:** Fable 판정(walls-delegate-to-fable) — "발사하되 Stage-0 $0 스크리너를 먼저" · 그 스크리너가 발사를 죽였다
**ckpt:** py303_full.clm sha256 `013c4574e0ce71ae173287b9…` (동일 80-rollout trace · **신규 decode 0**)

## 배경 — 원장이 막고, Fable 이 되살리고, 스크리너가 죽였다

발사하려던 "`--ag-cont` 로 lane 살려 재측정"은 **H_9376 이 이미 종결**(원장 조회가 차단 ·
`check-ledger-before-lever-fire`). 그러나 원장 확인 결과 **`--ag-cont` × `--dyn-w` 동시 켠 H = 0건**:
H_9376 = ag-cont ON × **w=0.10(묻힌 가중)** · H_9377 = ag-cont OFF(**죽은 상수 lane**) × w-grid.
⇒ conjunction 셀은 **닫힌 적 없음**. Fable 판정: **발사 정당**(H_9376 verdict 가 스스로 "프런티어
재이동 = dyn_v 가중/lane 수(SNR)" 라 지정했고, 그걸 쐈다 주장한 H_9377 이 H_9393 으로 계기-INVALID).

🔑 **Fable 이 무너뜨린 내 '불리한 사전'**: H_9376 의 Δ_G=−0.017(a3>a1)은 "노이즈가 실-G 를 이겼다"가
아니라 **영검정력 잡음** — w=0.10 서 lane 의 score 기여 상한은 0.10 인데 **MDE≈0.115**, 게다가 H_9391 이
should_emit 항진(θ 한 번도 안 걸림)을 증명했으므로 **어떤 content 도 G2 를 통과할 수 없었다**.
**반증 불가능한 검정의 FAIL 은 🧱 이 아니라 VOID**([[power-before-negative-verdict]]).

## 개입 — 없음 · 계기 1개 (STAGE-0 = Fable 이 발사 전 필수로 건 $0 스크리너)

`anima-py evaluate --cf-straddle`: 기존 trace 에서 **counterfactual score 를 오프라인 재계산** —
`score_cf(w) = scale(w)·seven + w·clip01(ag_conflict)` 를 **엔진의 motivation_score 직접 호출**로
(재구현 금지 · H_9393 수정 renorm 사용). ⚠️ **open-loop = DIRECTIONAL · KILL 전용**(score→emit→
secs_since_emit→clock 되먹임 미시뮬 ⇒ 발사를 죽이는 데는 충분, 세우는 데는 불가).

## ⛔ VERDICT — POWER-VOID (Stage-1 취소)

**C0 계기무결성**: `max|motivation_score(lanes,0.10) − base_motiv| = 0.000e+00` (완전재현) ✓

| w | score_cf min–max | ≤θ 행 | clock-open | **STRADDLE**(open∧≤θ) |
|---|---|---|---|---|
| 0.10 | 0.3193–0.6947 | 0 | 56 | 0 |
| 0.25 | 0.2720–0.5847 | 3 | 56 | 0 |
| 0.40 | 0.2246–0.4746 | 15 | 56 | 0 |
| 0.55 | 0.1773–0.3646 | 163 | 56 | **41** 🟢 |
| 0.70 | 0.1299–0.2545 | 240 | 56 | **56** 🟢 |

straddle 은 생겼다(w≥0.55) ⇒ 표면상 LICENSE. **그러나 검정력 선계산이 죽였다**:

| w | a1(real) vs a3′(자기-순열) **emit flips** / straddle | flip-rate |
|---|---|---|
| 0.55 | **7 / 47** | 0.149 ⛔ |
| 0.70 | **0 / 56** | 0.000 ⛔ |

**진짜 conflict 를 자기 자신의 시간-순열로 바꿔도 emit 이 (거의) 안 뒤집힌다.** straddle 밴드는
tension 이 연 게 아니라 **7-lane blend 를 축소해서** 열린 것 ⇒ 발사했으면 **content 가 아니라 다이얼**을
쟀다. **⇒ Stage-1 CANCEL (decode 0 · 303M 수집 1회 절약).**

### 🔑 원인 — 크기(magnitude) 사실
**`ag_conflict` 실측 범위 = 0.0000 ~ 0.0735** (57 distinct). tension 의 score 총 레버리지 ≤
**range×w = 0.0735·w ≈ 0.05**(w=0.70 서도). 게이트 문턱 θ=0.30, 다른 7 lane 이 만드는 밴드는 훨씬 넓다.
⇒ **어떤 예산-보존 가중에서도 tension 은 θ 게이트를 결정할 수 없다** — mixer(H_9376)도, 시계(H_9390)도,
문턱 항진(H_9391)도, 죽은 lane(H_9393)도 아닌 **신호 크기**가 최종 이유.

## 🏛️ 캠페인 종결 문장 (scope-bounded · Fable Q3 + 이 결과)

> **production regime(이 ckpt · 8-lane · θ=0.30 · rate-clock)에서 emit ≡ clock 이고, tension lane 입력은
> 동결 상수였다. 따라서 캠페인 H_9356→9393 의 음성들은 "항진 게이트 아래 죽은 게이지"에 대한 진술이며,
> tension→emit 가문은 production 에서 **반증된 것이 아니라 미측정**이었다. 그리고 그 미측정을 메우려
> lane 을 고치고(clip01) 최대 가청 가중까지 올린 counterfactual 에서도, 진짜 A⇄G conflict 를 자기
> 순열로 치환했을 때 emit 이 0~7/56 만 뒤집힌다 ⇒ 이 아키텍처에서 tension 이 emit 을 못 당기는 이유는
> 배선이 아니라 **A⇄G conflict 신호의 동역학 범위가 ~0.073 (θ=0.30 결정공간의 1/4)** 이라는 크기 사실이다.**

## 반증 · reopen
- 반증: flips ≥ 10 인 licensed w 존재 ⇒ Stage-1 발사(사전등록 arm a0 pedestal·a1·a3′ marginal-정합).
  실측 7/47·0/56 ⇒ 반증 실패.
- **reopen = O(0.1+) 범위의 tension 신호**(agloop 상류 = A⇄G conflict 산출 자체를 키우는 것). 이건
  measurement lane 이 아니라 **capability engineering**(게이트/신호 재설계) 소관 — 이 캠페인 밖.
- scope: open-loop 스크리너(DIRECTIONAL) · 이 regime/ckpt/30-tick. 되먹임 하에서 범위가 커질 수 있는지는
  미측정(단 범위는 신호 자체의 성질이라 되먹임이 4배 키울 개연은 낮다 — 미검증 추정임을 명시).

## 비용
$0 — 기존 trace 재분석 · CPU 수초 · **303M decode 0** · 그리고 Stage-1(3 arm×3 w×16 rollout ≈ 4320 tick
pool CPU)을 **발사 전 취소**시켜 절약.
