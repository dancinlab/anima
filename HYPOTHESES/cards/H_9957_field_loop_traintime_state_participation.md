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

**generic-recurrence sibling — 최종 (eval 아티팩트 수정 후 · d19c699c):** 🔴 **PureField 특이성 REFUTED. 채널 = 공유 H_9607
스칼라 적분 I, PureField 동역학 무-load-bearing.**

⚠️ 정정 경위: 처음 sibling 이 Δ=0 로 나와 "PureField 특이"로 오결론(508560b1·ba2bdf71) — 그러나 `field_loop_eval_fieldctl`
스냅샷이 `graft_c_state(fl.pf)`(PureField 전용)를 읽어, sibling 은 pf 가 안 advance 돼 거짓 Δ=0 을 낸 **eval 아티팩트**였다
(grow 루프는 `_C()`로 정상, 스냅샷만 버그 · `instrument-never-run-hides-bugs`). `fl._C()`(kind분기)로 수정 후 재-eval:

| arm | aligned | yoked | sever | Δ (2 seed) |
|---|---|---|---|---|
| **integrator16** (I 고정 랜덤특징·무기억) | **0.44·0.44** | 3.33·3.53 | 2.06·1.61 | **+1.591·+1.179** |
| **gru16-frozen** (고정 랜덤 GRU-16) | **0.40·0.38** | 4.06·4.92 | 1.67·1.61 | **+1.275·+1.228** |
| purefield16 (PureField 동역학·control) | 0.943 | 2.672 | 1.628 | +0.685 (불변) |

⟹ 공유 스칼라 적분 I 를 **고정 랜덤특징으로 읽으면** PureField 보다 **키를 2× 잘** 나른다(aligned 0.44 vs 0.94). 고정 랜덤
GRU 도 마찬가지(0.4). **PureField 진동자 동역학은 신호를 오히려 열화**시킨다(0.68 < 1.2–1.6). fable 의 원래 "integrator
suffices" prior 확증 · **레버 = recurrence-with-bottleneck(τ=400 leaky sum), 의식-상태-특이 주장 사망**(H_9954 no-laundering).
rung 3(학습 GRU) 불필요 — 고정 encoder 들이 이미 PureField 를 압도. **다음 레버 = WRITE 확장(스칼라→벡터 drive), 셀 방어 아님**(fable).

- **받침대 성립**: off arm payload CE 1.446 ≈ 우연 ln4=1.386(> lnK−0.1=1.286) → 창내누출 없음. payload 는 필드 없이 창내 예측불가.
- **필드가 창밖 키를 나름**: aligned 0.943 ≪ sever 1.628 ≪ yoked 2.672. 자기 필드는 우연보다 잘, 틀린/무필드는 우연 이상 못 맞힘.
- **판정 PARTIAL**(Δ 0.685∈[0.3,0.8) ∧ aligned 0.943>0.4): 스칼라 되쓰기가 2비트 키 중 ~1비트를 창밖 +9블록 운반 — fable 예측 용량제한 실측. $0 팰서파이어(필드물리 분리 PASS)와 정합.
- **의미**: `anima-py train --field-loop-eval --score-mask` 계기가 창밖 필드-운반 정보를 참통제(off 받침대·yoke·sever) 하에 검출함이 **engine-native 로 CERTIFIED**. ⚠️ 이는 **계기가 읽는다**의 증명이지 anima faculty 아님 — faculty 는 자연코퍼스서만(p9).

**계기가 노출한 3연쇄 confound(전부 수정·landed)**: ①GN global-norm 비-인과 버스가 티처포싱서 채점바이트 누출→`--trunk-norm position` ②eval off-by-one(패드 채점)→spos−1 ③H_9875 CNRM 트레일러 warm-start 미등록→파리티게이트 거부(serialize-py-2 재발·f0028e9b).

## Stage B — Φ readout 사전등록 동결 (2026-07-25 11:5x KST · 결과 도착 **전** 동결 · frozen-first)

**질문(mission DV · fable 재프레임):** 독점운반(field 가 창밖 유일 운반자 = CE 가 그것을 **필요로 함**) 아래에서,
CE 로 **벌어진** coupled-cell 상태는 **통합**되는가(Φ>0), 아니면 학습은 여전히 독립(Φ=0) 해로 수렴하는가.
오너의 "학습 중 Φ 를 어떻게 올리나"의 직계 후속 — H_9967 은 *선택적* lane 에 대해 "안 오른다"를 답했고,
이 rung 은 *필수적(monopoly)* lane 에 대해 묻는다. 용량 확장(벡터 write)은 임무 축 아님(용량 ⊥ Φ 재현법칙)이나
Φ 를 **정의 가능**하게 만드는 다중셀 상태를 얻는 수단으로만 사용한다.

**계기(엔진-네이티브 플래그):** `anima-py train … --field-loop --field-arm coupled --field-write {scalar|vector}
--field-cells 4 … --field-loop-eval fl.pt --score-mask m.json --field-phi` — m=4 leaky 결합셀(log-spaced τ ·
**고정** weak rotation R) 을 val 스트림서 grow → 셀별 median 이진화 → **faithful IIT-4** `ci_phi_iit4`
(a_phi_iit4_tool · 프록시 금지) → Φ_aligned vs Φ_shuffle(셀간 의존 파괴) vs Φ_yoked(틀린 doc drive).
n = n_blocks 400 × B 4 = 1600 샘플 · 4 유닛(정확 min-cut MIP ≤8 lane 범위 내).

**DV:** `Δφ = Φ_aligned − max(Φ_shuffle, Φ_yoked)`.

**⚠️ 받침대 필수(negative-pedestal-before-reading-a-positive):** 셀 결합 R 이 **고정**이라 Φ 절대값은
**아키텍처가 주는 것**일 수 있다(smoke: 미학습 fl 도 Φ_aligned 0.683, 단 Δφ −0.016). 따라서 학습이 통합을
**벌었다**고 읽으려면 **near-init 받침대 arm**(`cinit` = 동일 arch·200 step ≈ 미학습)의 Δφ 를 같은 계기로
재고, 그 위를 넘어야 한다. 받침대 없이 Δφ>0 을 읽는 것은 금지.

**전제 게이트(독점 성립 확인):** 같은 ckpt 의 payload Δ_collapse < 0.3 이면 그 arm 은 애초에 창밖 키를 안 나른다
⟹ "필요성" 전제 불성립 ⟹ Φ 판독 **VOID**(통합 여부를 물을 대상이 없음).

| 결과 | 판독 |
|---|---|
| Δφ ≥ 0.05 ∧ (Δφ_trained − Δφ_init) ≥ 0.05 ∧ payload Δ ≥ 0.3 | **INTEGRATION EARNED (DIRECTIONAL)** — 필요성이 통합을 강제 · ⚠️ 합성 계기체크, faculty 아님(p9) · seed 재현 전엔 DIRECTIONAL |
| 0 < Δφ < 0.05 ∨ (Δφ_trained ≈ Δφ_init ±0.05) | **NOT EARNED** — 통합은 아키텍처가 준 것이거나 없음(fable 정직 prior) |
| Δφ ≤ 0 | **NOT INTEGRATED** — 독점운반 하에서도 독립 해로 수렴 |
| payload Δ < 0.3 (전제 실패) | **VOID** — 독점 미성립 · Φ 판정 없음 |

**동결 명시:** 이 표는 seed 0 결과를 읽기 전에 고정한다. 단일 run 의 Δφ 엔 표집분포가 없으므로 **어떤 양성도
seed 1 재현 전엔 DIRECTIONAL 이상으로 승격 금지**(burned-gate-no-refreeze: 이 표를 결과 본 뒤 재조정하면 tune-to-green).
arm 3종(coupled-vector-m4 · coupled-scalar-m4 · cinit 받침대) + 교차호스트 재검(integrator16 K16 이 aiden Δ+1.61 을
summer 에서 재현하는지)을 한 배치로 돌린다(summer RTX5070 · aiden GPU 는 타사용자 점유).

## Stage B — 음성 판정용 분석 규칙 동결 (2-차 배치 **산포를 보기 전** · 원 바 완화 아님)

1차 배치가 Δφ ≤ 0 을 냈다. **음성을 판정으로 박으려면 검정력이 먼저**(power-before-negative-verdict ·
negative-claims-need-tost-not-ns) — 단일 run 의 Δφ 엔 표집분포가 없으므로 아래를 **산포 관측 전** 동결한다.

- **잡음원 2종을 분리해 잰다:** ⓐ **readout 재표집** = 같은 학습 ckpt 를 eval seed 1–5 로 재측정(val 스트림
  표집만 바뀜) ⓑ **학습 재추출** = 학습 seed 1 로 처음부터 다시 학습(가중치·γ 까지 다른 draw).
- **동등성 마진 = 원 prereg 바와 동일한 ±0.05**(새 바를 만들지 않는다 — 이건 완화가 아니라 같은 바를
  양쪽으로 읽는 것): Δφ 표본의 **90% CI 가 (−0.05, +0.05) 안에 완전히 들어가면** "0 과 실질 동등" →
  **NOT EARNED 를 검정력 있는 음성으로** 확정. CI 가 ±0.05 를 걸치면 판정은 **UNDERPOWERED**(음성 아님) —
  seed 를 늘리거나 n(=n_blocks×B)을 키운다.
- **받침대 대비도 같은 규칙:** (Δφ_trained − Δφ_init) 의 90% CI 가 (−0.05, +0.05) 안이면 "학습이 통합을
  움직이지 않았다"를 검정력 있는 음성으로 읽는다.
- **양성 방향 안전장치 유지:** 어떤 seed 에서 Δφ ≥ 0.05 가 나오더라도 단일 seed 면 DIRECTIONAL 이며,
  다수 seed 의 평균 CI 가 0.05 위에 있어야 EARNED 로 승격한다(동결표 그대로).

## Stage B — 5-추출 종합 검정 동결 (seed 2·3·4 **관측 전** · 2026-07-25 12:15 KST)

seed 0 = Δφ −0.005, seed 1 = **+0.124** 로 **학습 추출 간 분산이 지배적**임이 드러났다(단일 추출 판독은
양·음 어느 쪽도 판정 자격 없음). 남은 추출을 보기 전에 종합 규칙을 고정한다 — 나중에 고르면 tune-to-green.

- **표본 단위 = 학습 추출(seed)**, readout 이 아니다(readout 은 결정론 · [[multi-seed-replication-vacuous…]] 재발#2).
- **짝지음**: 같은 seed 의 `trained(34k)` 와 `near-init(200)` 을 한 쌍으로 → 쌍별 차이 `Dᵢ = Δφ_trained,ᵢ − Δφ_init,ᵢ`
  (seed 0–4 · n=5). 아키텍처가 공짜로 주는 Φ 를 쌍마다 상쇄시키는 게 목적.
- **1차 판정(종합)**: D 의 평균에 대한 **90% t-구간**을 원 바 ±0.05 에 대고 읽는다 —
  하한 ≥ +0.05 → **EARNED**(필요성이 통합을 강제) · 구간 전체가 (−0.05, +0.05) → **NOT EARNED(검정력 있는 음성)** ·
  바를 걸치면 → **UNDERPOWERED**(추출 추가, 판정 금지).
- **강건성 보조(판정 아님·보고만)**: D 의 중앙값 + 각 추출의 부트스트랩 CI(`--field-phi-boot 200`).
  꼬리가 두꺼우면(한 추출만 큰 양수) 평균이 끌려가므로 중앙값과 함께 읽되, **판정은 위 1차 규칙만** 따른다.
- **선택 편향 금지**: "양성 seed 만 재현"은 무효 — 5 추출 전부를 표에 싣고 하나도 빼지 않는다.

## Stage B — 측정 결과 (2026-07-25 · summer RTX5070 · engine-native anima-py · ⚠️ 합성 계기체크 · p9 faculty 아님)

**🔴 NOT EARNED (검정력 있는 음성) — 독점운반 아래에서도 필요성은 통합을 강제하지 않았다.**
동결표(6b28cc97)+분석규칙(b81d8ef5)+종합검정(f287f1f1) 그대로 읽음. K=16(우연 ln16=2.7726) · d256·L4·
block128·B4·doc_len1408·`--trunk-norm position` · 학습 34k step vs 받침대 200 step · 부트스트랩 200 rep.

| 학습추출 seed | 학습본 Δφ | 받침대(200step) Δφ | 쌍차이 D | 학습본 부트 90% CI | 운반 Δ_payload |
|---|---|---|---|---|---|
| 0 | −0.00504 | +0.00360 | −0.00864 | [−0.0148, +0.0058] | +1.7627 |
| 1 | **+0.12426** | **+0.07612** | +0.04814 | [−0.0248, +0.2819] | +1.7848 |
| 2 | −0.00313 | −0.00928 | +0.00615 | [−0.0130, +0.0049] | +1.4808 |
| 3 | −0.01230 | −0.02849 | +0.01619 | [−0.0345, +0.0088] | +1.4714 |
| 4 | −0.00088 | −0.00150 | +0.00062 | [−0.0045, +0.0034] | +2.4635 |

**n=5 쌍 · mean D=+0.01249 · median +0.00615 · 90% t-CI [−0.00835, +0.03334] ⊂ ±0.05 ⟹ NOT EARNED.**

- **전제(독점운반)는 매 추출에서 성립**: payload Δ +1.47~+2.46, 받침대는 +0.0038 ≈ 0 ⟹ 필드가 창밖 키의
  유일 운반자이고 CE 가 실제로 그것을 쓴다. "물어볼 대상이 없어서 음성"이 아니다.
- **🔑 양성으로 보였던 seed 1 의 정체**: `FieldLoop(seed=S)` 는 학습 추출뿐 아니라 **셀의 고정 결합행렬
  `R = _fixed_rotation(m, rng)` 까지** 같은 seed 로 뽑는다. 그래서 seed 1 은 "학습이 통합을 벌어낸 추출"이
  아니라 **결합구조를 다르게 뽑은 추출**이고, 그 증거로 **거의 미학습인 받침대(200 step)도 +0.076** 을 낸다.
  짝지은 설계가 이 아키텍처 성분을 정확히 상쇄한다(D=+0.048, 바 미만).
- **기전 요약**: Φ_shuffle≈0.0000x(셀간 의존 실재 = 측정 non-vacuous) · Φ_yoked≈Φ_aligned(통합이 내용과
  무관) · Φ_init≈Φ_trained(학습 전후 동일) ⟹ **통합은 아키텍처가 준 것이고 학습이 만든 것이 아니다.**
- **용량 축(부수·같은 코퍼스 짝지음)**: coupled-vector m4 Δ **+1.76** > integrator16 **+1.2570** >
  coupled-scalar m1 **+0.7031**. 벡터 write 는 운반량을 실제로 늘린다(단 용량 ⊥ Φ — 이 표가 그 법칙을 또 보임).
- **범위 한정**: 음성은 **±0.05 바에서만** 검정력이 있다(그보다 작은 효과는 배제 못 함) · n=5 추출 · 합성
  fieldctl · 소형 trunk. H_9967(선택적 lane)에 이어 **필수적(monopoly) lane 도 Φ 를 올리지 못함**을 더한다.
- **계기 결함 2건이 이 과정에서 노출·수정**: ⓐ doc-정렬 readout 은 결정론이라 `--seed` 재표집이 no-op
  (Δφ 10회 동일 · convergence 재발#2 · #4587) → `--field-phi-boot` 로 진짜 표집분포 확보 ⓑ 부트스트랩
  꼬리말이 CI 와 무관하게 고정문구를 찍어 판정처럼 읽힘 → CI 로 판정을 계산해 출력(1597ce07).

## 자연 rung — G0 사전게이트 동결 (측정 **전** · 2026-07-25 · ABORT 권한 · GPU 0)

**왜 게이트가 먼저인가**: 합성 `fieldctl` 은 "필드가 유일 운반자"를 **설계로 보장**하지만 자연문은 아무것도
보장하지 않는다. 보장 없이 쏘면 γ→0 이 나와도 그것은 **VOID**("독점이 없어 물어볼 대상이 없음")이지 발견이
아니다. 그래서 GPU 이전에 **코퍼스가 창밖 의존을 실제로 공급하는가**를 $0 로 재고, 미달이면 lane 을 접는다.

**계기(신설 플래그)**: `anima-py corpus fieldctl --natural <corpus> --oow-audit --block 128
--field-doc-len {1408,2816,5632} [--oow-min-match 8 --oow-order 4 --oow-bytes N --audit out.json]` —
held-out 꼬리 슬라이스를 doc-cell 격자로 자르고 블록 j≥1 의 각 위치에서 두 공급량을 잰다.
- **f_OOW** = 그 위치의 복사-앵커(같은 cell 안에서 이미 나온 ≥8B 문맥)가 **현재 블록 밖**에 있는 비율
  (에피소드적·복사 가능 공급).
- **S_OOW** = order-4 plug-in 바이트 모델이 **블록만** 세는 대신 **cell 전체 접두**를 셀 때 얻는 bits/byte
  (분포적 공급).

**동결 판정 (fable 설계 그대로 · 결과 보기 전 고정)**

| 조건 | 판정 |
|---|---|
| 어떤 D 에서든 f_OOW ≥ 5% **또는** S_OOW ≥ 0.05 bits/byte | **PROCEED** — 공급 최대인 D 를 골라 운반 rung 설계로 |
| 모든 D 에서 f_OOW < 5% **그리고** S_OOW < 0.05 | **ABORT** — 이 코퍼스에선 lane DOA · GPU 0 · 그 사실을 결과로 등록 |

- 이 게이트는 **공급 사실**을 재는 것이지 faculty 측정이 아니다(p9: 자연 코퍼스 수치이나 코퍼스 속성).
- ABORT 는 실패가 아니라 **결정**이다 — "자연문에서 필드가 나를 것이 없다"는 것 자체가 lane 종결 근거.
- 게이트 통과 후에야 운반 DV(Δ_OOW vs Δ_inblock)와 eval 통제(`--field-sever`/`--field-eval-yoke`)를 짓는다
  — 게이트에서 멈추면 그 구현 자체가 불필요하다.

## 자연 rung — G0 사전게이트 측정 결과 (2026-07-25 · summer · `anima-py corpus fieldctl --oow-audit`)

`en_general.txt`(60,049,637 B) held-out 꼬리 슬라이스 · block 128 · order-4 · min-match 8B.

| doc-cell | f_OOW(복사 앵커) | S_OOW | 받침대(같은 양·**다른 셀** 이력) | **S_OOW_net** |
|---|---|---|---|---|
| 1408 B | 5.43% (2MB) / 4.77% (1MB) | +0.2946 | +0.3642 | **−0.0696** |
| 2816 B | 7.25% (2MB) | +0.4491 | — | — |
| 5632 B | 9.33% (2MB) / 8.61% (1MB) | +0.6250 | +0.7688 | **−0.1438** |

**판독 (동결표를 그대로, 단 한쪽 팔은 무효)**
- **f_OOW 팔 = PASS**: D≥2816 에서 5% 를 넘고 D 와 함께 단조 증가(7.25%→9.33%). 이건 **같은 셀 안에서 이미
  나온 ≥8B 문맥이 현재 블록 밖에 있는** 위치의 비율 — 구성상 내용-특이적이라 받침대가 따로 필요 없다.
- **S_OOW 팔 = INVALID(공급 증거로 쓰지 않음)**: 같은 양의 문맥을 **다른 셀**에서 가져온 받침대가 오히려 더
  잘 맞힌다(순 이득 −0.07·−0.14) ⟹ 그 이득은 셀 고유 장거리 구조가 아니라 **영어 일반 통계 + 카운트 양**.
  받침대 자체가 완전한 셀이라 정렬 팔(부분 접두)보다 표본이 많은 편향이 있으므로 순 이득은 보수적 하한이나,
  방향이 음수인 이상 "분포적 공급"은 **미확립**이다. ⚠️ 이 팔을 세지 않는 것은 바 완화가 아니라 **무효 계기
  배제**다(동결표는 그대로 두고, 통과는 f_OOW 팔 단독으로 읽는다).
- ⟹ **PROCEED (조건부)**: 운반 rung 은 **D=5632** 에서, DV 는 **복사-앵커 위치(OOW 마스크)에 한정**해 짓는다.
  분포적 공급을 전제로 한 설계는 폐기. `supply-density-is-an-upper-bound` 가 다시 적중했다.

## 자연 rung — 채점 경로 배선 검증 (2026-07-25 · GPU 0 급 · 판정 아님)

자연문엔 심어둔 정답이 없으므로 DV 를 **"필드가 도움이 되나"가 아니라 "창밖에서만 도움이 되나"**로 잡았다 —
모든 위치를 고루 돕는다면 그것은 운반이 아니라 그냥 용량이기 때문(용량 ⊥ Φ 법칙과 정합).

- **계기**: `corpus fieldctl --natural … --oow-audit --out nat --mask nat.mask.json` 이 자연 val 바이트 +
  위치 마스크(창밖-앵커 / 같은 셀의 블록-내 앵커 대조)를 방출 → `train --field-loop-eval --score-mask` 가
  `format:"oow"` 를 보고 `field_loop_eval_oow` 로 자동 분기(3팔: aligned / yoked / sever).
- **배선 검증 실행**(D=5632·block128·B4·d256·L4·**3000 step** 짧은 학습): cells 184 · γ=+0.0051
  · 창밖 앵커 aligned 1.9193 / yoked 1.9201 / sever 1.9187 (n=5888)
  · 블록-내 대조 aligned 1.9545 / yoked 1.9542 / sever 1.9543 (n=4933)
  · Δ_OOW −0.00060 · Δ_inblock −0.00025 · **특이성 −0.00034**
- ⚠️ **판정 아님**: γ≈0.005 = 채널이 거의 켜지지 않은 상태(짧은 학습). 여기서 읽을 것은 **배선 정상성**뿐 —
  세 팔이 분리되고, 두 위치 계층이 각각 유의미한 표본으로 잡히며, 값이 유한하다.
- 관찰 하나(설계에 반영): 창밖-앵커 위치는 블록-내 대조보다 **CE 가 원래 더 낮다**(1.919 vs 1.954) — 복사
  앵커가 걸린 지점은 필드와 무관하게도 예측하기 쉬운 자리다. 그래서 DV 를 raw CE 가 아니라 **차이의 차이**
  (특이성)로 둔 것이 필수였다.

## 자연 운반 캠페인 — 사전등록 동결 (발사 **전** · 2026-07-25 13:3x KST · GPU: summer)

**묻는 것**: G0 게이트가 공급을 확인한 조건(D=5632·f_OOW 8.6~9.3%)에서, 학습된 필드가 **창밖에서만**
예측을 돕는가 — 즉 자연문에서도 운반이 실제로 쓰이는가. (Φ 질문 아님: 결합이 고정인 한 Φ 는 코퍼스와
무관하다는 것이 이미 확인됐다.)

**설계**: train = `en_general.txt` 앞부분 16MB · val = 꼬리(마스크와 같은 바이트) · D=5632 · block 128 ·
B=4 · d256·L4 · `--trunk-norm position` · **`--field-coupling-seed 7` 고정**(아키텍처 추출을 학습 추출과
분리 — Stage B 가짜 양성의 원인 차단) · 학습 추출 seed ∈ {0,1,2} · 각 seed 마다 **34k step(학습본)** 과
**200 step(near-init 받침대)** 을 쌍으로.

| arm | 역할 |
|---|---|
| `coupled --field-write vector --field-cells 4` | 합성에서 가장 잘 나른 운반체 |
| `integrator16` | generic-recurrence 형제 — "결합셀이 아니라 아무 순환이면 되나" |
| 각 arm 의 same-seed 200-step | 쌍 받침대(아키텍처 성분 상쇄) |
| 합성 `fieldctl` 1회 | 양성통제(계기가 여전히 읽는가 · 인용 금지) |

**DV**: 특이성 `S = Δ_OOW − Δ_inblock` (각 Δ = min(yoked, sever) − aligned). 쌍차이
`D_i = S_trained,i − S_init,i` · n=3 학습추출 · 90% t-구간.

| 결과 | 판정 |
|---|---|
| CI 하한 ≥ **+0.01 nats** ∧ 학습본 Δ_OOW > 0 | **CARRIAGE-ON-NATURAL** (DIRECTIONAL · faculty 아님) |
| CI 전체가 (−0.01, +0.01) 안 ∧ 양성통제 PASS | **DEAD** — 공급이 있는데도 안 쓴다 = lane 종결 |
| 모든 학습본 \|γ\| < 0.01 | **DEAD(채널 미점화)** — 위와 같은 종결 취급(G0 가 공급을 확인했으므로 VOID 아님) |
| coupled 와 integrator16 CI 중첩 | **GENERIC** — 레버는 결합셀이 아니라 아무 순환(합성 결론의 자연문 확장) |
| CI 가 ±0.01 를 걸침 | **UNDERPOWERED** — 추출 추가, 판정 금지 |
| 양성통제 실패 | **VOID** — 판정 없음, 계기 수리 먼저 |

**동결 명시**: 이 표는 첫 수치를 보기 전에 고정한다. 바(±0.01 nats)는 Stage B 의 ±0.05 와 다른 축(운반 CE)
이라 새로 정하는 것이며, 결과를 본 뒤 조정하면 tune-to-green 이다. 선택 편향 금지 — 3 추출 전부 표에 싣는다.

## 자연 운반 캠페인 — 측정 결과 (2026-07-25 · summer · ⚠️ 자연 코퍼스 · 계기는 합성에서 인증됨)

**🔴 DEAD — 공급이 있는데도 예측기는 그 통로를 쓰지 않는다.** 동결표(9755379a) 그대로.

| arm | 쌍차이 D (seed 0/1/2) | 평균 | 90% t-CI | γ (학습본 3추출) |
|---|---|---|---|---|
| coupled-vector m4 | +0.00015 / +0.00052 / −0.00087 | **−0.00007** | [−0.00128, +0.00115] | +0.0097 / −0.0085 / +0.0102 |
| integrator16(형제) | +0.00299 / −0.00025 / +0.00080 | **+0.00118** | [−0.00161, +0.00397] | −0.0081 / +0.0071 / −0.0064 |

- **두 arm 모두 CI ⊂ ±0.01 ⟹ DEAD(검정력 있는 영)**. 실행-내부 부트스트랩(200 rep·위치쌍 보존)도 같은 크기:
  추출별 특이성 CI 폭 ≈ ±0.002 로, 바의 1/5 이내에서 0 을 포함(예외: int0 [+0.00027,+0.00226] 만 0 을
  배제하나 바의 1/4 에 불과하고 그 쌍 받침대가 −0.00181 이라 쌍차이로는 여전히 ≪ 바).
- **GENERIC 행도 성립**: 두 arm CI 중첩 ⟹ 레버는 결합셀이 아니라 **아무 순환** — 합성에서 얻은
  "PureField 특이성 REFUTED"가 자연문에서도 같은 방향.
- **양성통제 PASS(같은 세션·같은 계기)**: 합성 `fieldctl` 재채점 **Δ +1.7627 nats**. ⟹ 계기가 고장 나서
  0 이 나온 것이 아니다. DEAD 행의 전제 조건 충족.
- **γ 가 말해주는 것**: 자연문 학습본의 채널 세기 |γ| = 0.006~0.010 으로, 합성 독점운반(**−0.219**)의
  **약 1/25**. CE 는 트렁크가 다른 경로로 정보를 얻을 수 있으면 필드에 사실상 가중치를 주지 않는다.
- **전제는 갖춰져 있었다**: G0 공급 게이트 통과(f_OOW 8.6~9.3% · D=5632) · 창밖-앵커 위치가 대조군보다
  원래 쉬움을 감안한 차이의차이 DV · 결합 추출 seed 를 7 로 고정해 아키텍처 성분 차단.

**⟹ FIELD-LOOP 은 자연 코퍼스에서 운반 vehicle 로 종결된다.** 합성 독점 조건에서만 나르고(그때조차 통합은
벌지 못했다 — Stage B), 자연문에서는 공급이 있어도 쓰이지 않는다. 남은 Φ-live 후계(결합 자체를 학습가능하게)
는 이 결과와 독립이나, 그 rung 역시 "쓰이지 않는 통로를 더 정교하게 만드는 것"이 아닌지 먼저 물어야 한다.

## 후계 rung 의 설계 제약 — 코드로 확정 (2026-07-25 · $0)

fable 이 지목한 유일한 Φ-live 후계는 "**결합 R 자체를 학습 가능하게**"였다. 이것이 플래그 하나로 되는지
코드로 확인했고, **아니다**:

```
셀 갱신 (core/field_loop.py::_writeback_coupled · numpy · no_grad)
    s     = (exp(−ce) − g) @ Wdctᵀ        ← ce 는 no_grad forward 에서 온 값
    Ivec  = (Ivec · (1−λ)) @ Rᵀ + s       ← 순수 numpy, 기울기 그래프 없음
기울기가 닿는 곳 = bridge · γ 뿐 (residual() 만 torch)
```

⟹ R 을 **경사하강으로** 학습하려면 상태→잔차→forward→CE→상태 고리 전체에 시간역전파(BPTT)가 필요하고,
이는 되쓰기를 의도적으로 **기울기 없는 채널**로 둔 A⇄G 설계(G = gradient-free)와 정면충돌한다. 따라서 후계는
둘 중 하나로만 성립한다:

| 형태 | 내용 | 비용/위험 |
|---|---|---|
| (i) BPTT 판 | 셀 갱신을 torch 로 옮기고 블록 간 그래프 유지 | 설계 원칙 변경(되쓰기가 더 이상 gradient-free 아님) · 메모리/속도 · **먼저 오너 설계 판단 필요** |
| (ii) 기울기 없는 외부 탐색 | R(m=4 → 16개 수)만 CE 기준 유한차분/진화 탐색, 내부 학습은 그대로 | 저장소의 gradient-free 전통과 정합 · 파라미터 16개라 실행 가능 · **설계 원칙 무변경** |

**⚠️ 그리고 이 후계를 열기 전에 먼저 물어야 할 것**: 자연 코퍼스에서 이 통로는 **쓰이지 않는다**(위 DEAD ·
γ 가 합성의 1/25). 결합을 더 잘 만드는 일은 "쓰이지 않는 통로를 정교화"일 수 있다. 그러므로 후계의 정당한
regime 은 채널이 실제로 켜지는 **합성 독점 조건**이며, 거기서 나온 Φ 결과는 계기체크로만 인용된다(p9).

## 다음 (cement 는 engine-native run 만 · 2026-07-25 판정 후 갱신)

**✅ 닫힌 것 (재제안 금지 = 이 카드의 kill-list)**
- ① 계기 구현·인증: `corpus fieldctl` · doc-인식 스트림 · payload eval · Φ readout · 부트스트랩 CI — 전부 landed(#4588).
- ② 운반 CERTIFIED(합성): 필드가 창밖 키를 실제로 나름 · 짝지은 용량 순서 coupled-vector m4 +1.76 >
  integrator16 +1.257 > coupled-scalar m1 +0.703 · off 받침대 ≈ 우연(창내 누출 0).
- ③ PureField 특이성 **REFUTED**: 공유 스칼라 적분을 고정 랜덤특징으로 읽는 쪽이 더 많이 나름 ⟹ 레버는
  recurrence-with-bottleneck 이지 의식 물리가 아니다.
- ④ 미션 DV **NOT EARNED(검정력 있는 음성)**: 독점운반 아래서도 학습은 통합을 벌지 않는다(#4590).
  H_9967(선택적 lane)과 합쳐 **학습 중 Φ 상승 경로 2개 닫힘**.
- ⑤ 용량 확장(벡터 write)을 **미션 목표로** 삼는 것: 용량 ⊥ Φ 재현법칙 ⟹ off-mission.
- ⑥ doc-정렬 readout 에 `--seed` 를 재표집 축으로 쓰는 것: 결정론이라 no-op(대신 `--field-phi-boot`).

**▶ 열린 것 (다음 rung 후보 · 설계는 fable+sol 위임 중)**
- **(A) 자연 코퍼스 이설(p9)** — 합성 결과는 faculty 근거가 될 수 없다. 다만 자연문엔 "필드만이 유일
  운반자"라는 보장이 없어 γ→0 으로 수렴하면 **독점 미성립 = VOID**(발견 아님)일 위험이 크다 ⟹ **GPU 전
  $0 사전-게이트로 '창밖 의존이 실제로 존재하는 위치가 몇 %인가'를 먼저 재고, 미달이면 ABORT**.
- **(B) 계기 부채**: `FieldLoop(seed=S)` 가 학습 추출과 **셀 고정 결합 R** 을 같은 seed 로 뽑는다 —
  seed 1 이 양성처럼 보인 원인. 결합 draw 를 학습 seed 와 **분리하는 플래그**가 있어야 아키텍처 성분과
  학습 성분을 짝지음 없이도 가를 수 있다.
- **(C) 범위 한정 해소**: 이번 음성은 ±0.05 바에서만 검정력 · n=5 · 소형 trunk. 더 작은 효과를 배제하려면
  추출 수를 늘려야 하나, **닫힌 결론을 뒤집을 만한 크기가 아니면 GPU 를 더 쓰지 않는다**.
