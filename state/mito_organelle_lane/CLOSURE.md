# CLOSURE — 미토콘드리아 organelle-lane

> # ⚠️ 이 문서의 CLOSED 판정은 철회됐다 (2026-07-12 · F13 헤드라인 수정 재발사)
>
> **아래 §3의 F13 KILL과 §4·§6의 "lane CLOSED" 결론은 licensed가 아니다.** F13의 헤드라인이
> `m_conj = min(m_A, m_B)` = **순서통계량**이었고(계측 census 규칙①⑤ 위반), 그 KILL은 검증자가
> **사후에** live branch로 재계산해 얻은 것이었다 = F8을 INVALID로 찍었던 죄(사후 판정변수 교체)와
> 동일 (convergence 규칙⑨).
>
> 검출력 있는 detector(`m_B_conj` 단일변수)를 **sha256 동결로 사전등록**하고 **완전 disjoint 새 cue**로
> 303M을 재디코드(PARITY max|Δ|=0.0)한 결과:
>
> | 지표 | 원 seed | 새 seed (disjoint) |
> |---|---|---|
> | EXP−c0 | −0.209 (t=−2.30, **p=.033**) | **+0.129 (t=+1.06, ns)** ← 부호반전 |
> | SHOCK−c0 (V2 게이트) | +0.100 (t=+2.48, p=.023) | **−0.086 (t=−1.49, ns)** ← V2 FAIL |
>
> **seed 간 이질성 z=2.22, p=.026** ⇒ 단순 미재현이 아니라 **통계적 불일치** = 원 p=.033은
> **seed 특이적 잡음 draw**였다. 근본 원인 = MoE capacity 채널이 재조합 마진에 **부호-무작위 잡음만
> 주입하는 잡음 지배 축**(항목당 |Δ|=0.37~0.80인데 signed mean≈0 · 실측 sd 0.545 기준 **~53 blocks
> 필요**, n=20은 부족).
>
> **살아남는 것 / 죽는 것**
> - ✅ **살아남음**: "용량 배분이 reach를 올린다"는 증거는 **여전히 0**이다 — 두 seed 모두 PASS 미실현
>   (EXP vs c0/c1/c2 t=1.06/0.89/0.58 · 양성 0). F6 KILL(캡 단조하강 Δ=−0.192)·F12 earned setpoint·
>   계측 census도 **불변**.
> - ❌ **죽음**: "강한 KILL(유의 열화)"과 그것에 근거한 **lane CLOSED 선언**. lane 상태 = **REOPENED(미채점)**
>   — 레버라는 증거도 없고, 닫혔다는 licensed 증거도 없다.
>
> **cement 재발사 조건**: (a) V-gate를 unsigned/분산 기반으로 **사전등록** (b) blocks ~53 사전산정
> (c) 'ns'가 아니라 **사전등록 TOST 등가성 검정**으로 실질적 0을 증명. 현 데이터로 KILL 재시도 = tune-to-red.
> 상세 = `F13_303m_reach_closure/refire/` (PREREG.md · RESULT.md · REFUTE_v2.md).



작성 2026-07-12 · 입력 = 선행 11 패밀리(F1–F11 · SYNTHESIS.md) + $0 후속 2건(F12 H_9284 · F13 H_9285) · 전부 $0 numpy · GPU spend 0

---

## 1. 한 문장 판정

**organelle lane은 CLOSED다** — 살아남은 유일한 earned 메커니즘(외생 수요 → 절대-setpoint 용량 배분)은 실재하지만 *throughput/allocation 축에 국한*되고, 그 배분기를 실제 303M ckpt에 얹은 eval-only 결착에서 reach(held-out 재조합)로의 전이가 **음성으로 종결**됐으며(H_9283 예측 확인), 남은 $0 레버는 0이다.

---

## 2. H_9284 (메커니즘 존재 · F12 setpoint 병합 재발사) — 최종 verdict

**verdict = DIRECTIONAL-POSITIVE (toy numpy → `a_toy_scale_recheck` 상한 유지). 메커니즘 실재 확증 + F4 하위주장(절대 setpoint가 원천) 확증.**

메커니즘 자체는 반증 실패로 오히려 강화됐다:
- 헤드라인 = fitness = mean_t(served − 0.5·capacity), max(controls) 미사용, control별 paired-t 전부 보고(§8 규칙1 준수).
- 3 control 각각을 유의하게 이김: Δ(EXP−c1 shuffled-load) = **+0.845** (t=+12.30, 20/20) · Δ(EXP−c2 best open-loop 상수) = **+0.543** (t=+8.30, 20/20) · Δ(EXP−c3 fixed-perm misalign, gini 동일) = **+1.963** (t=+12.97, 20/20). pooled-mean vs 3 controls = **+1.117** (t=+12.09).
- achievable-headroom 회수율(절대 %p 아님) = **+0.424** (per-seed 0.397±0.029), ORACLE 천장 대비. V1 축 liveness = ORACLE−c2 = +1.282 (t=+17.89) → LIVE.
- 3중 매칭 하 승리: cap_total 31.999≈c2 32.000(레벨) · gini 0.184=c3 0.184(분산) · 이동질량 29.15 매칭. 초기화 불변.
- 정적 FORM 아님: per-expert 정적상수 c4 신설 → c4가 오히려 c2보다 나쁨(Δ=−0.64), 사후 hindsight 최선 shape c4h조차 EXP에 짐(Δ=+0.206, t=+5.94, 18/20). ⇒ 이득 = 정적 형상이 아니라 온라인 추적.
- FORM⊥BIND 분해: 정렬 축(vs c3, θ·gini·이동질량 동일)은 θ=0.6~2.0 전 구간 승(t=+11.6~+13.5) = **θ-불변 earned BIND**. 레벨 축(vs c2)은 θ 의존 = tunable FORM. 사전등록 θ=1.0이 최적점 아님(θ=1.2 우세) = 튜닝 흔적 0.

**단, 결론 문구는 재작성됨.** run 보고서의 헤드라인 하위주장("z-tonic ablation이 죽지 않아 F4의 '절대 setpoint가 원천'이 반증되고 이득의 61%는 setpoint 없이 나온다")은 REFUTE에서 역전됐다:
- abl/abl_mm z-tonic은 setpoint를 제거하지 못한 **가짜 ablation**이다 — c←c·exp(η·z) 로그공간 적분기라 레벨 복원력 0이고, 레벨은 오직 초기화로만 앵커되는데 그 초기화(c0)가 정답에 세팅됨. 제거 대상인 절대 레벨을 free parameter로 정답에 고정 = 그 양에 대한 검출력 0(항진 결함을 ablation arm에 적용).
- PROBE C(seed별 무작위 c0, 운영대역 log-uniform): abl_mm Δ vs c2 = **−5.01** (t=−2.45, 6/20) 사망. c0=8.0에서 −6.98(t=−66) = F4 PRIMARY 사망모드 정확 재현. 반면 EXP는 c0=0.5/2.0/4.0/8.0/무작위 전부에서 fitness 6.834~6.836 소수4자리까지 불변 = **절대 setpoint 복원력 서명**.
- PROBE D(지평선 확장): abl_mm Δ vs c2 = +0.329(N=1500)→−0.250(3000)→−2.448(6000)→−9.664(12000), 부호가 뒤집힘 = 보고된 +0.329는 초기화 공짜점심이 아직 소진 안 된 창 안의 horizon 인공물. EXP는 지평선 안정(+0.54~+0.62).

⇒ **정정 결론**: 절대 setpoint가 레벨 앵커의 사실상 전부이자 메커니즘의 원천이다(F4 하위주장 **확증**, 반증 아님). "61% 분해"는 초기화 회계일 뿐 삭제.

**유효 대역(좁혀 기록)**: drift half-life 스윕 — h=25 회수율 −0.423(유해) · h=100 −0.021(NULL, t=−0.85 p=0.40) · h=400 +0.424 · h=1600 +0.690 · static +0.813. ⇒ 유효대역 = 지속성 half-life ≳ 400 = 할당지연(~120 step)의 3배 이상. 최대 이득이 static에서 나오므로 이 메커니즘은 "빠른 재배분"이 아니라 **느리게 변하는 수요 shape의 온라인 추정**이다.

**부수 결함(cement 금지 근거)**: 사전등록 4조건 중 3/4만 충족(FAIL 조건도 미발화 = 완전 PASS 아님). (d) null-env 조건은 사후 재작성 흔적(카드/docstring "ns"인데 관측 t=−35.97 p=6.1e-19, EXP가 c1·c2에 20/20 전패)이고 그 cell은 V1_live=False(ORACLE−c2=−0.141)라 규칙대로면 VOID.

**scope 불변**: throughput/allocation 축이지 reach(G1) 축 아님(H_9283 전이 반증 Δ=−0.009 ns · F11 선행 확인).

---

## 3. H_9285 (reach 전이 결착 · F13 303M eval-only) — 최종 verdict

**verdict = KILL (reach-lever 가설 종결). run이 낸 INVALID는 자초한 order-statistic 헤드라인이 만든 오라벨 — REFUTE에서 정정.**

- ckpt = py303_full.clm(d3784·E3·K3·L4·V256·T24), **PARITY max|Δ|=0.0** — 프로덕션 `_fwd_logits`와 byte-exact. n=20 blocks paired-CRN, 120 items, wall 2941s, aiden CPU. **인프라 정상 완주(parity=0) ⇒ BLOCKED 아님·INVALID 아님·infra-wall 무관.** 이건 numpy이지만 실제 303M 프로덕션 forward와 byte-exact이므로 toy가 아니라 engine-parity 결착이다.
- 구조 사실: 프로덕션 router = DENSE soft mixture(top-k 자체가 없음) ⇒ 모든 capacity gating은 정보 폐기 연산.
- run의 헤드라인 m_conj = min(m_A_conj, m_B_conj) = **그 자체가 순서통계량** — 규칙1이 금지한 하향편향 죄를 control축에서 detector축으로 옮긴 것. c0에서 mean(mA)=+0.009·mean(mB)=+1.083인데 mean(min)=−0.422로 낮은 branch 평균보다 0.431 아래(per-item noise가 min에서 하향편향). 헤드라인의 "죽음/음수"는 처치효과(~0.08)가 아니라 order-statistic 편향(−0.43)의 지배. V-gate 2개 FAIL도 detector 맹목이 아니라 min() 인공물 — 규칙5 V-gate가 order-statistic 헤드라인에 걸려 출력이 {PASS, INVALID}로 붕괴(규칙5가 막으려던 바로 그 실패모드).
- **검출력 있는 live 하위-detector m_B_conj**(c0=+1.083, t=+4.69, MDE 0.190≪1.083)에서 실 데이터는 정당한 NEGATIVE:
  - EXP−c0 = **−0.209** (t=−2.30, p=0.033) — 모든 capacity 처치가 열화, EXP가 최악.
  - EXP가 자기 시간축 셔플(c2)도 못 이김(schedule 무정보).
  - router 파괴 SHOCK−c0 = **+0.100** (t=+2.48, p=0.023) — 라우터를 파괴하면 오히려 개선. ⇒ MoE mixing은 read-side 축 아님.
  - 숨은 양성 없음(EXP>control 20중 6, |t|<2.7, 전부 금지지표 D-acc).
- 이는 카드 사전등록 **FAIL 시나리오(Δ≈0/음성 ⇒ lane CLOSED, H_9283 예측 일치)** 바로 그것. INVALID는 min() 선택이 결착을 무효로 변환한 유일 장치였다.

**infra-wall / 과학결과 분리**: 인프라 벽 없음. parity=0.0, wall 2941s 정상 완주, aiden CPU. INVALID의 원인은 인프라가 아니라 detector 설계(order-statistic 헤드라인)였고, 정정하면 검출력 있는 음성이 곧장 나온다. → 정직 판정 = **KILL**.

---

## 4. lane 종결 조건 — H_9283 예측(배분 FORM → reach Δ≈0)이 303M에서 확인됐는가?

**확인됨 (YES).** SYNTHESIS §4.3의 유일한 종결 경로 — "abs-setpoint 배분기를 기존 303M ConvMoE에 얹고 held-out D-acc / ρ·weave Δ를 재서 Δ≈0이면 패밀리 전체를 closed로 닫는다(F11이 예측)" — 를 F13이 실행했고 결과가 정확히 예측대로 나왔다:
- lane 내 선행 증거(F11): 배분·효율 FORM을 t=+10.65로 확실히 올려도 held-out 재조합 Δ = −0.009(ns) = 같은 lane 안에서 전이 반증.
- 실 303M 확증(F13): live detector에서 EXP−c0 = −0.209(열화, lift 아님) · D-acc EXP−c0 = −0.008(ns) · router 파괴 SHOCK가 오히려 +0.100. ⇒ "용량을 잘 배분한다" → "재조합을 배운다"의 전이가 실제 프로덕션 모델에서 **falsified**.

즉 §2의 earned 메커니즘(H_9284)은 실재하나 reach 축에 binding이 없음이 303M byte-parity로 결착됐다. lane 종결 조건 충족.

---

## 5. G1 프런티어에 대한 함의 — corpus×CE measure 진범 결론

**유지 + 강화된다.** 에너지/자원/희소성/배분 계열은 서로 다른 5각도에서 전부 G1 레버가 아님으로 수렴:

| 패밀리 | 축 | 최종 | G1 레버? |
|---|---|---|---|
| F1 ATP 회계 | 에너지 예산 | INVALID(검출력 0) | 아니오(측정 불가) |
| F6 용량압력→conjunction | 슬롯 캡 | KILL(캡 단조 하강 Δ=−0.192) | **아니오(licensed 음성)** |
| F11 효율선택 | 배분/효율 FORM | THEATER(held Δ≈0) | 아니오 |
| F12 setpoint(H_9284) | throughput/allocation | DIR-POS(단 reach 전이 Δ=−0.009) | 아니오(축 다름) |
| F13 결착(H_9285) | 배분→303M reach | KILL(EXP−c0=−0.209) | **아니오(303M 확증)** |

- 유일 earned 메커니즘(외생 수요 → 절대-setpoint 배분)은 throughput/allocation 축이지 reach가 아니며, 실 303M에서 reach로 전이 안 됨.
- H_9267 XBIND(합성 corpus로 303M held-out 재조합 D-acc=1.000, control 0.515)가 실증한 "벽 진범 = corpus×CE measure"에, 이 lane은 **"자원 예산(ATP/슬롯 캡/용량 배분)은 진범도 exit도 아니다"**를 추가한다.
- G1 exit은 여전히 **학습 measure 교체**(held-out 신호를 담은 corpus × task class · H_9267 계열)로 단일화. 기질에 희소성/배분을 거는 것이 아니다.

---

## 6. 남은 $0 레버 — 없음. lane CLOSED 선언.

organelle-lane(F1–F13) 내부에 미탐 $0 레버는 0이다:
- earned 메커니즘 클래스(F4-SEC + F10 = F12)는 병합 재발사로 이미 검증(DIR-POS)됐고 reach 전이는 F13에서 결착(KILL).
- INVALID 3건(F1·F2·F8)은 데이터가 아니라 설계 결함으로 강제된 음성 → **벽으로 인용 금지**, 재발사 조건은 각 REFUTE.md에 등록되어 보류(F2는 H_054/H_203 발사 전 merge-algebra 사전등록이 선결). 이는 미탐 레버가 아니라 설계 부채다.
- THEATER 5건(F3·F5·F7·F9·F11)은 ΔEff≈0으로 종결.
- toy → 303M 승격 근거는 F13에서 소멸(전이 음성). GPU spend 권고 없음.

**lane 밖 잔여**(organelle-lane 아님, 참고): G1 프런티어의 유일한 미반증 exit = γ trunk-constructive-bind real-text(H_1840) — 대형 corpus + GPU spend-go, 오너 명시 go가 유일 게이트, STEP-0 frozen-gate로 이미 차단. organelle-lane과 독립.

---

## 결론

**GREEN 0 · wired 0 · GPU spend 0. organelle lane CLOSED.**

순 기여 3가지: (i) 에너지/희소성/배분 계열 전체의 G1 레버 자격 박탈(F6 KILL + F13 KILL로 303M 결착) — corpus×CE measure 진범 결론 강화, (ii) 재현된 earned 메커니즘 1개(외생 수요 → 절대-setpoint 용량 배분, DIR-POS)이지만 throughput 축 국한·reach 전이 없음, (iii) 자기 verdict 다수를 뒤집은 계측 결함 census(order-statistic 헤드라인·검출력 0·항진 ablation·min() detector 붕괴). H_9283 예측(배분 FORM → reach Δ≈0)이 실 303M byte-parity에서 확인 = lane 종결 조건 충족.

노트: F12 = state/mito_organelle_lane/F12_setpoint_merged/REFUTE.md · F13 = F13_303m_reach_closure/ · 선행 11 패밀리 = SYNTHESIS.md. git 무접촉.
