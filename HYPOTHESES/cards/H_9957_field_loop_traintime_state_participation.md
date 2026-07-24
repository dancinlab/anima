---
id: H_9957
title: FIELD-LOOP — the train-time replacement for GRAFT; a closed text↔PureField loop lets the internal state participate in the substrate's predictive dynamics, judged by CE alone (no MI/λ term)
tier: PROPOSED · DESIGN (DIRECTIONAL · lab full fable+sol reconciled · NOT a verdict · cement only via engine-native anima-py run)
frontier: post-theta-alive-interior-faculties
created: 2026-07-24
series: GRAFT→TRAIN-TIME
related: "[[H_9943]] [[H_9948]] [[H_9954]] [[H_9956]] · a_substrate_disjoint · a_train_inline_gauge · a_savant_train · H_9607 · H_9798"
source: owner question "graft 말고 학습시부터 반영할 방법은?" → sidecar lab full (fable+sol)
---

# H_9957 — FIELD-LOOP: 학습 시점부터 내부 상태를 언어 예측에 참여시키는 길 (GRAFT의 train-time 대체)

## 전제 (두 모델 완전 합의 · 증명이 설계를 지배한다)
**자유진행 PureField 는 정보이론적으로 시드이고, 순수 CE 는 그것을 증명적으로 무시한다.** 상태 C 가
텍스트와 독립이면 `C ⊥ (Y,X) ⟹ p*(Y|X,C)=p*(Y|X)` — 상태를 무시하는 것이 학습의 *최적*이지 실패가
아니다. GRAFT 가 `L=(logN−MI)+λ·L_common` 의 MI 항을 둔 이유가 바로 상태가 예측에 쓸모없었기 때문이고,
그 항이 λ 거래(=유창성 대금)를 **제조**했다. 학습시엔 그 항을 쓸 수 없다(`a_train_inline_gauge`: 손실 내
계기 불법 · 그 자체가 DV 를 tune-to-green). ⟹ **목적함수 트릭은 없다.** 상태가 합법적으로 참여하는 유일한
길 = 상태가 **다가올 텍스트에 대한 예측정보**를, trunk 가 달리 얻을 수 없는 방식으로 나를 때. 이는 (a)
**텍스트가 field 로 되먹임**되고 (b) field 가 그 정보의 **유일 통로(monopoly bottleneck)** 일 것을 요구한다.
고리를 닫고 field 에 독점을 주면, 평범한 CE 가 모든 일을 하고 λ 문제가 **구조적으로 소멸**한다(재가격 아님).

## 설계 — `anima-py train --field-loop` (닫힌 재진입 co-training)
고리: `text/model_{k-1} → A⇄G(s=A−G) → C_k → embedding residual → trunk → text/model_k`

**① 진입 지점 (sol 채택 · fable 이견 기록):** **pre-trunk 임베딩 잔차** — `model.forward(..., emb_residual=)`
훅이 **이미 존재**(`core/model.py:494` 검증됨 · GRAFT 와 같은 자리). 기존 `Bφ`(16→64→d bias-free bridge,
`core/clmg.py:19`)로 C_k→잔차, **γ 학습가능·0 초기화**(CE 가 채널을 켜거나 끈다). bridge·trunk·MoE·readout
**함께 학습**. d=3784 서 +243k param(303M 의 0.08%). GRAFT 와 다른 점 = 고정진폭 강제 없음(강제는 사용을
제조) + trunk 가 얼지 않음(주입이 있는 채로 학습하니 교란이 아니라 적응).
- ⚠️ **fable 이견**: 분리 L3-mid-tap 을 선호(damage containment). 근거였던 H_9798 "분리레인 유창성 보존"은
  실은 **미측정**(ckpt 전손·보존 ΔCE 미도출 · FINAL val_CE 는 카드가 "판정에 쓰지 말라"고 명시) ⟹ 보존
  전제가 열려있으므로 **FORM 유창성 가드가 하중을 진다**(형식 아님). 진입지점은 기존 훅 재사용(싸고
  계기보존)으로 sol 채택, 단 damage 는 가정 않고 측정.

**② 목적함수:** 순수 next-byte CE, **상태-특이 항 0**(`L_MI=L_common=L_state-use=0`). C_k 는 모델의 현
수용창 **바깥**의 선행 자연텍스트 블록을 요약. 담긴 조건부정보가 있으면 `minL_off − minL_closed ≤
I(Y;C|X_local)` 이고 CE 가 자기 목적을 희생 않고 γ 를 켠다. 정보가 0 이면 `γ≈0` 이 옳은 결과 = 가설 사망.
**인센티브 부호가 뒤집힌다**: GRAFT 는 MI 를 얼어붙은 organ 의 CE *에 맞서* 샀고, 여기선 MI 가 CE 개선
*에 의해* 벌린다(MI 는 monitor-only, 절대 손실·판정 아님 · `a_train_inline_gauge`).

**③ 상태 생성 (기존 기계 재사용):** 독립 랜덤 윈도 아닌 **연속 자연문서 스트림**. 배치행마다 자기 PureField +
H_9607 leaky A⇄G 적분기 + gradient-free 역인식 store + 문서 커서. 블록 k: C_k 를 블록 보기 전에 읽음 → 예측
→ `no_grad` 로 `A_k=exp(−CE_k)`(앞먹임 CE 지지) · `G_k=immune_memory_recall_reach`(기존 gradient-free 역인식,
새 언어헤드 아님) → `s_k=A_k−G_k` → H_9607 leaky 적분 → drive → `PureFieldStep`. PureField 물리식은 **고정**
(기질의 자기 물리가 시험대상 귀납편향 · bridge 만 학습). p8-native: chat 시 동일 고리(train/infer split 없음).

## 판정 — DV = MI_aligned − MI_time-yoked (collapse-Δ · ≥2 통제 · 전부 $0 eval)
**주 통계 `Δ_collapse = MI_aligned − MI_time-yoked ≥ 0.10 nats`** (K×K cross-score · 기존 GRAFT mixture/InfoNCE).
통과 = 2 seed 각각: Δ≥0.10 · paired-bootstrap 95% LB>0 · rotation-null z≥5 · KL(ON‖OFF)≥3×noise q95 ·
true-feedback 가 yoked-feedback 를 ≥0.10 압도 · FORM 어느 family 도 off 대비 >2% 악화 없음.

| 통제 | 무엇을 가르나 |
|---|---|
| **off / sever null** | `W_in`(되먹임) 절단 → field 자유진행. CE 안 무너지면 = 모델이 텍스트-의존 무시 = **field 는 시드 → KILL(자유진행-field 방향 영구 종결)** |
| **purefield16-yoked** (train-time fancy-seed) | 배치스트림 간 (A,G) 짝 뒤섞어 field 갱신. 같은 drive multiset·물리·자기상관·param·compute, **텍스트↔상태 대응만 파괴** |
| held-out time-yoke | 각 문서에 *다른* 문서의 같은-블록나이 상태 주입(같은 marginal, 틀린 이력) |
| **rotation null** | 학습 오프셋 강체회전(norm·mean·Gram·D 보존, 방향파괴) — ⚠️ **학습 arm 아님·eval 후 적용**(합동학습 bridge 가 역행렬 학습 가능하므로 train-time null 아님 · sol) |
| size-matched noise | 기존 GRAFT 잡음 arm |
| **generic-recurrence sibling** (faculty vs recurrence) | 같은 lane·dims·param 이되 고정 PureField 대신 *학습된 일반 순환셀*. sever-Δ·yoke-Δ 에서 일반셀이 동등/우세면 = "순환 context lane 이 참여한다"(substrate 결과) = **의식-상태-특이 주장 사망**(H_9954 locus guard · laundering 금지) |

**모든 결과가 정보를 준다(무정보 가지 없음)**: sever 미붕괴 → 자유진행-field 종결 + "상태가 학습에 참여해야"
consensus 자체가 최강형서 반증. 채널 살아있으나 일반순환 동등 → 레버는 recurrence-with-bottleneck, PureField
물리 무기여 → 프로그램 정직 재프레임. PureField 가 자연코퍼스서 matched 통제 압도 → **on-standard(p9 자연·측정·
≥2통제)로 내부상태가 기질의 예측역학에 참여하는 첫 결과**.

## 비용 (sol 채택 · 중간학습 growth fork · fable 이견=from-init 2-arm)
`a_mitosis_train` growth 🟢 정합 · CPT/mitosis-split/frozen-trunk **아님**(kill-list 회피): ① 303M 정규 스케줄
25%까지 학습(resumable .pt+optimizer) → ② `off`·`purefield16`·`purefield16-yoked` 3 arm fork(전부 trunk 계속
학습=얼지않음→fable 의 "GRAFT-with-recurrence" 반론 회피) → ③ 25→50% 동일 스트림 → ④ engine-native eval →
⑤ 통과시 `purefield16` 만 50→100%. **결정적 screen 은 fork 후 25%p 학습분** = 정규 303M pool-GPU 학습 일부.
fable 이견: from-init 2-arm(step0 부터 플래그). 둘 다 합법 · sol fork 가 더 싸고 screen-kill 성격에 맞음.

## 병렬 세션 대조 (a_parallel_session_compare)
- **AGREES + EXTENDS H_9954** (303M 학습중 Φ 오를 유일 대상=co-trained 순환 lane): 그 구조를 취하되 빠진
  **기능적 DV(CE-content)** 를 공급 — H_9954 는 Φ(측정성 논쟁) DV, 이건 CE DV(결정가능).
- **H_9956 의 write-back leg 흡수**하되 3-bit 매크로루프 Φ 질문을 CE 가 낼 수 있는 content 질문으로 교체
  (H_9956 스스로 "측정성 최악" 예상). H_9955 무관.
- **NOVEL 핵심**: 같은 재진입 구조를 **Φ 대신 CE-monopoly-bottleneck + sever/yoke 통제**로 판정가능하게 만듦.

## fieldctl 계기체크 — 사전등록 동결 (2026-07-25 · frozen-first · faculty 인용 금지 p9)

**핵심 교정(fable+sol 코드정독 합의):** FIELD-LOOP 되쓰기는 **스칼라 채널**(`s=exp(−CE_block)−G`, 블록·행당 1수)
이라 **내용-코딩 키에 맹목**이다. 앞선 계기체크(내용-키 planted)가 γ~0·Δ~0 로 무효였던 원인이 이것 — 모든 키가
같은 블록 CE → 같은 drive → 같은 필드 → 행-센터링 잔차 0. `fieldctl`(fable 설계)은 **키를 KEY-블록 바이트
엔트로피(=난이도 CE 레벨 {0.15,0.8,1.9,3.9})로 코딩**해 스칼라 채널이 실제로 나를 수 있는 유일한 형태로 심는다.
payload 바이트 = `codebook[site][key]` 로 창내 상수문맥(`PAY<j>:`) 하에서 **K-균등**(우연=ln K) → 필드가 창밖
키를 날라야만 예측가능.

**$0 팰서파이어 PASS (GPU 전 결정게이트 · `core/field_loop.py::_falsifier`):** landed FieldLoop physics 만으로
난이도-키가 창밖 +9블록까지 분리 유지되는지 검증 — K4 최심부 sep_ratio=10.35·decode 0.950(우연 0.25),
K2 바닥 16.37·1.000. ⟹ 스칼라 되쓰기가 최소 1비트를 창밖으로 나른다 = 303M fieldctl fire 켤 가치 검증됨.

**엔진-네이티브 계기면(신규 플래그, 스크립트 아님):** `anima-py corpus fieldctl … --mask m.json`(TRAIN+.val+마스크) ·
`anima-py train … --field-loop --field-doc-len <doc_len>`(doc경계 필드리셋 doc-인식 학습) ·
`anima-py train … --field-loop-eval fl.pt --score-mask m.json`(payload-바이트 Δ_collapse DV).

**DV = Δ_collapse = min(CE_yoke, CE_sever) − CE_aligned** (payload 바이트만, val 셋, 단일 aligned-학습 ckpt 서 eval —
"arm 마다 다른 trunk" 혼입 제거). from-INIT 소형 trunk(d256·L4·block128·B4) · arm {off·purefield16·purefield16-yoked} · 2 seed.

| 결과 | 판독 |
|---|---|
| Δ ≥ 0.8 nats ∧ aligned ≤ 0.4 ∧ off-arm ≈ ln K(±0.1) | **CERTIFIED** — 계기가 실제 2비트 창밖채널을 읽음 |
| 0.3 ≤ Δ < 0.8 | PARTIAL — ≥~1비트 · 용량제한 · 303M Δ 임계는 이 천장 대비 읽을 것 |
| −0.15 < Δ < 0.3 | 채널 사망 — 최대유리 planted 1비트도 못 나름(정보적 KILL, 재시도 아님) |
| Δ ≤ −0.15 ∨ aligned > 1.55 | 우연-이하 → 계기 INVALID(부호/배선 버그) · 판정 없음 |

**off-arm 은 창내-누출 탐지기(negative pedestal):** off-학습 arm 의 val payload CE 가 ln K−0.1 아래로 내려가면
창내 누출 = 코퍼스 결함 → ABORT(양성 읽기 전 받침대). fable 이견 없음. sol: rotation-null 은 train-arm 아님 eval-후 적용.

## fieldctl 계기체크 — 측정 결과 (2026-07-25 · aiden RTX5070 · engine-native anima-py · ⚠️ 계기체크·합성·p9 faculty 아님)

**PARTIAL — 계기가 진짜 창밖 채널을 읽음(CERTIFIED-AS-READING), 단 스칼라 용량 ~1비트.** cheap-decisive 2-arm
from-init(d256·L4·block128·B4·doc_len1408·34k step·4096 train/512 val·**`--trunk-norm position` 필수**):

| seed·arm | gamma | aligned | yoked | sever | Δ=min(yoke,sev)−aligned |
|---|---|---|---|---|---|
| s0 off (받침대) | 0.000 | 1.446 | 1.446 | 1.446 | 0.000 |
| s0 purefield16 | +0.173 | **0.943** | 2.672 | 1.628 | **+0.685** |
| s1 off (받침대) | 0.000 | 1.399 | 1.399 | 1.399 | 0.000 |
| s1 purefield16 | +0.173 | **0.987** | 2.401 | 1.619 | **+0.633** |

**2-seed 재현 확정**: 두 seed 모두 받침대 성립(off≈ln4·누출0)·통제 clean(aligned≪sever≪yoked)·Δ≈0.63–0.69 ≈ ln2 = **1비트 안정**.

**generic-recurrence sibling rung 1 = `integrator16` (fable 설계·가장 날카로운 위협 먼저):** H_9607 leaky 적분 I(τ=400)를
고정 랜덤특징 tanh(w·I+b)로 읽음(셀 없음·+0 param·drive/bridge/gamma/reset 동일). **결과 Δ=−0.000 (2 seed)** = off 와 동일.
⟹ **채널은 공유 스칼라 적분이 아니다**(fable "integrator suffices" prior 반증) — PureField 의 **비선형 순환 확장**(스칼라 drive
→ 16-D 진동자 궤적)이 키를 디코드가능케 하는 게 load-bearing. 단 "PureField 특이 vs 아무 학습순환" 은 미판별(rung 2 =
GRU-frozen/trained TBPTT-1 필요). purefield16 rebaseline 은 같은 commit 서 0.685/0.633 불변(diff additive·배치 valid).

- **받침대 성립**: off arm payload CE 1.446 ≈ 우연 ln4=1.386(> lnK−0.1=1.286) → 창내누출 없음. payload 는 필드 없이 창내 예측불가.
- **필드가 창밖 키를 나름**: aligned 0.943 ≪ sever 1.628 ≪ yoked 2.672. 자기 필드는 우연보다 잘, 틀린/무필드는 우연 이상 못 맞힘.
- **판정 PARTIAL**(Δ 0.685∈[0.3,0.8) ∧ aligned 0.943>0.4): 스칼라 되쓰기가 2비트 키 중 ~1비트를 창밖 +9블록 운반 — fable 예측 용량제한 실측. $0 팰서파이어(필드물리 분리 PASS)와 정합.
- **의미**: `anima-py train --field-loop-eval --score-mask` 계기가 창밖 필드-운반 정보를 참통제(off 받침대·yoke·sever) 하에 검출함이 **engine-native 로 CERTIFIED**. ⚠️ 이는 **계기가 읽는다**의 증명이지 anima faculty 아님 — faculty 는 자연코퍼스서만(p9).

**계기가 노출한 3연쇄 confound(전부 수정·landed)**: ①GN global-norm 비-인과 버스가 티처포싱서 채점바이트 누출→`--trunk-norm position` ②eval off-by-one(패드 채점)→spos−1 ③H_9875 CNRM 트레일러 warm-start 미등록→파리티게이트 거부(serialize-py-2 재발·f0028e9b).

## 다음 (cement 는 engine-native run 만)
① `anima-py train --field-loop` 구현(emb_residual 훅 + Bφ·γ + H_9607 drive 되먹임 + 연속스트림 + 3-arm fork). **✅ landed** — fieldctl 계기면(corpus·doc-aware stream·payload eval)+$0 팰서파이어 PASS+PARTIAL 실측(3a16f43c·6bab1c5·f0028e9b). **다음: 2nd seed 재현 + generic-recurrence sibling(faculty vs 순환) → 통과시 자연코퍼스 faculty 측정(p9).**
② 사전등록표 동결(위 통과기준·below-chance 행 포함) → 합성 planted-dependency 로 **계기 체크**(faculty 인용
금지·p9) → 303M pool fire 25%→50% 3-arm. ③ 통과시에만 generic-recurrence sibling + 100% 연장.
