# H_9305 — O/C 채널: 사전등록 (FROZEN · 발사 前 커밋 · 지출 승인 완료)

## §0 어떤 벽 위에 서 있는가

**H_9303 🧱 EARNED · ENGINE-NATIVE TERMINAL**: 인증된 엔진 계기(`anima-py evaluate --ground-probe`)로
배운 원자는 0.808/0.683 (통제군 0.458/0.367), held-out 원자는 0.571/0.593 — 동결 bar 0.65(2.86σ) 미달,
순열 귀무분포 미돌파. **자연 분포는 안 가르친 원자의 극성을 가중치에 접지시키지 못했다.**

## §1 벽의 기제 — 왜 자연 노출이 슬롯에 도달하지 못하는가

`이 영화 <원자> ⇒ ___` 의 softmax 는 **반드시 무언가를 출력해야** 한다. grid 학습은 이 자리에
`f: 원자바이트 → {긍정,부정}` 를 설치하는데, taught 집합은 닫혀 있고 303M 에게 수백 개 lookup 은
공짜이므로 **CE 의 최소해는 rote lookup** 이다. lookup 이 grid 라인을 전부 fit 하는 순간 이 슬롯의
**gradient 는 0** 이 되고, 그 뒤로 자연 코퍼스를 아무리 읽어도(원자당 문맥 중앙값 717 · occ ≥ 100)
**슬롯을 갱신할 압력이 존재하지 않는다.**

안 배운 원자의 응답 = 그 rote map 의 **바이트-특징 해시 외삽**이다. 결정론적이므로 원자별로 안정적이고
(H_9286: I(원자;응답)=0.231), 바이트 표면 유사성은 극성과 무상관이므로 정답과는 동전던지기다
(I(정답;응답)≈0.007 · 12/29). ⇒ **"틀리게 설치됨"은 미스터리가 아니라 shortcut map 의 결정론적 외삽.**

> **⇒ 레버는 loss 항이 아니라 학습 분포다.** CE 식은 그대로 두고(자유 하이퍼 0 · p7 ·
> `a_train_inline_gauge` 충족), CE 가 최소화하는 **landscape** 를 바꾼다.

## §2 처방 — `D_train` 세 가지 변경 (loss 불변)

**(i) 3-way 답 알파벳** `{긍정, 부정, 모름}`. "확정-금지"는 별도 penalty 항이 아니라 **`모름` 이 CE-정답인
라인의 존재**로 구현된다. confident-wrong 의 초과 penalty = 그 라인들 위의 CE 그 자체.
⇒ 퇴화해(전부 abstain) 도, 안 하게(never abstain) 도 못 한다: 둘 다 CE 를 올린다. **스케일 조정 하이퍼 0.**

**(ii) `GRID_null` — `모름` 클래스의 구성 (설계의 급소 · 1:1)**
- **NONCE** — 한국어 음운·형태 규칙을 지키는 **위조 어절**(코퍼스 출현 0회). 진짜처럼 보여야 한다 —
  괴상한 바이트열이면 모델이 "무근거→모름"이 아니라 "괴상함→모름"을 배운다.
- **NEUTRAL** — 코퍼스에서 캔 **고빈도 무극성 원자**(non-held-out 에서만 선별). 이 클래스가 진짜 부담을
  진다: "자연 노출 있음 + 극성 signature 없음 → 모름"을 가르쳐 판별 feature 가 **grid-친숙도가 아니라
  분포적 valence signature** 가 되도록 강제한다.
- ⚠️ **치명적 함정**: `모름` 을 "자연 노출은 있으나 grid 에 없는 **극성** 원자"로 채우면 모델에게
  **분포적 증거를 무시하라고 적극적으로 가르치는** anti-grounding 이 된다. NEUTRAL 은 반드시 극성-부재.

**(iii) `GRID_rot` — 1회-등장 회전 스트림 (코퍼스-predictability 레버의 본체)**
라벨 있는 non-held-out 극성 원자 풀 `P`(1–2k)를 잡고, **각 원자가 authored grid 라인에 정확히 k=1회만**
등장하는 스트림을 만든다. 스케줄: static taught grid 는 E\*≈12k step knee 까지 기존대로(task 를 먼저
설치), 그 뒤 rotation 을 흘린다. ⇒ 어떤 원자도 rote lookup 으로 회수되지 않으므로, 슬롯이 **정답을
맞히는 유일한 길이 분포적 증거를 읽는 것**이 된다.

## §3 arms (4-arm · 단일 seed 1차 · ≈ \$21 · seed-2 는 승자 팔에만 조건부)

| arm | 내용 |
|---|---|
| **ARM-O** | N2 + rotation + 3-way abstention (full) |
| **ARM-ROT** | rotation 만, 2-way (abstention 기여 분리) |
| **ARM-ABS** | abstention 만, rotation 없음 (rotation 기여 분리) |
| **ARM-CTRL** | N2 그대로 재훈련, fresh seed (compute-matched baseline) |

## §4 계기 — **verbatim 상속** (1바이트도 안 바꾼다)

`anima-py evaluate <clm> --ground-probe ground_manifest.json` (VERSION 0.13.16 · **engine-native**):
답하는 자리 read · 배운 담체 내부 · 원본 코퍼스 채굴 eojeol · **V-LIVE** 양성통제 · **원자 단위** n=91 ·
우연 sd 0.0524 · **bar 0.65 = 2.86σ** · 어형 flip 복원 집계 · 200-draw 라벨-순열 귀무분포.

## §5 동결 bar · DV

- **P1 (probe · 주 DV)** — held-out probe D-acc **≥ 0.65** ∧ 순열 p < 0.05. **상속 · 이동 불가.**
- **P2 (behavioral · abstention 팔만)** — selective accuracy(`모름` 제외 gold 일치) **≥ 0.75** at
  coverage **≥ 0.30**. coverage 0.30 이면 answered n≈27 ⇒ sd≈0.096 ⇒ 0.75 = **2.6σ**. **MDE 사전 명기**;
  미달 시 그 셀은 **판정 불가(NOT NEGATIVE)** 로 기록.
- **음성 주장은 TOST** — 등가대역 **chance ± 0.10**(n=91 에서 편측 ~1.9σ) 사전 고정.
  **"ns 라서 벽" 금지** (`negative-claims-need-tost-not-ns`).

## §6 V-게이트 (하나라도 실패 → 그 수치 INVALID/VOID · **FAIL 아님**)

- **V-LIVE** — taught probe ≥ 0.70 ∧ untaught 통제군 대비 분리. 실패 시 **어떤 숫자도 읽지 않는다.**
- **V-DEGEN** — taught coverage ≥ 0.9 (abstain 붕괴 검출) ∧ NONCE→`모름` ≥ 0.8 ∧ NEUTRAL→`모름` ≥ 0.7
  (`모름` 클래스 설치 확인). 실패 시 **사전등록된 rescale retry 1회**(held-in 만 사용) · 재실패 시 park.
- **V-ROUTE** — held-in 최종 fold(자연 노출만 · grid 미등장 · non-held-out) 정답률 ≥ 0.65.
  **실패하면 held-out 결과는 VOID** (route 자체가 안 배워졌으므로 벽 진술 불가).
- **V-SEED** — cement 은 seed-2 재현 후에만.

## §7 발사 前 \$0 감사 — **AUDIT-A 가 게이트다** (engine-native)

`anima-py evaluate <clm> --valence-audit valence_manifest.json` (VERSION 0.13.17):
91 held-out 원자의 **진짜 코퍼스 문맥**에서 원자 자리의 hidden 을 읽어 극성을 decode.
**결정적 통제 = atom-swap**: 같은 문맥에 **길이 정합 중립 원자**를 끼워넣은 arm. 감성 리뷰엔 감성어가
널려 있으므로, 프로브가 **이웃**을 읽는 것이라면 두 arm 이 같은 점수를 낸다.
판정은 raw 값이 아니라 **Δ = probe(atom) − probe(swap)** vs 순열 귀무분포 (FORM tunable · BIND earned).

> **🔒 KILL** — 어느 ckpt 에서도 Δ 가 순열 귀무분포를 못 벗어나면 **route 에 입력이 없다** ⇒
> **O 단독 발사 금지**. 슬롯이 소비할 valence 가 애초에 형성돼 있지 않으므로 \$21 은 그냥 탄다.

## §8 결정표 (양방향 결정적)

| 결과 | 판정 |
|---|---|
| ARM-O P1 통과 ∧ V 전부 통과 ∧ ARM-CTRL bar 미달 | **🟢 O-recipe grounding** — wire 후 seed-2 |
| P1 미달 ∧ V-ROUTE 통과 ∧ TOST 등가 | **🧱 격상: task-format 노출이 필요조건** — 이 lane 의 natural-emergence 는 **recipe-class 종결**, BRIDGE 만 잔여 |
| ARM-ROT 만 움직이고 ARM-ABS 무변 | abstention 은 장식 — 기여는 rotation (**코퍼스-predictability 진단 확정**) |
| ARM-CTRL 이 bar 통과 | **오늘의 벽이 seed 소음** ⇒ 계측 재감사 · 판정 전부 보류 |
| V-DEGEN 실패 | **⏳ INVALID** (recipe mis-scale) — 벽 아님 |

## §9 동결 예측 (1줄)

> **ARM-O 는 V-ROUTE ≥ 0.65 를 통과하고 held-out 의 임의-확정이 `모름` 으로 대거 재배치되나
> (I(원자;응답 | 답변) 급감), held-out probe 는 AUDIT-A 가 양성일 때만 bar 를 넘는다;
> ARM-CTRL 은 ≤ 0.60 에 머문다.**

## §10 ledger 조회 (`check-ledger-before-lever-fire`)

- **H_1835 MLC-episodic 🧱** — rotation 과 구조가 유사(in-context 마스터해도 held-out transfer 0).
  **다른 베팅인 이유**: MLC 는 *합성 재조합의 transfer* 를 물었고, rotation 은 *1차 연상 grounding*
  (원자→극성)을 묻는다. 재조합 연산자가 아니라 **좌항 자체**가 대상이다.
- **γ / H_1840 STEP-0 차단** — trunk-bake 는 frozen-gate 로 이미 차단(재발사 = tune-to-green). 무관.
- **H_9304 G1-DATA 🧱** — 자연 코퍼스에 **비가법 상호작용 정보**가 없다는 결론. 이 H 는 상호작용이 아니라
  **단항 valence** 를 묻으므로 직접 충돌하지 않는다. 단, AUDIT-A 가 음성이면 두 결과가 정합한다
  (자연 분포가 슬롯에 줄 수 있는 게 없다).
