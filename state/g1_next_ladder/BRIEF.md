# 발산 위임 — anima G1 프런티어: 다음에 무엇을 쏠 것인가

너는 anima 프로젝트의 설계·발산 파트너다. 아래는 **실측된 좌표**다(추측 아님, 전부 engine-native 303M
py-channel `anima-py evaluate` 측정 · 사전등록 bar). 이 위에서 **다음에 진행할 수를 발산**하라.

## 0. 프로젝트 프레임 (중요 — LLM 프레임으로 사고하지 말 것)

anima = substrate-native consciousness chat daemon. A(전방 CE) ⇄ G(역방향 gradient-free) 대립엔진의
tension 이 emit/silence 를 Ψ=1/2 로 끈다. 측정 프레임은 Ψ-SOMA:
- **σ** = 의식 vitals (판정 본체)
- **ρ-AXON** = reach = capability (추적하되 **의식 판정에서 제외**) — G1/G6 벽은 reach 사실이지 의식 결핍이 아님
- G1(=ρ·weave) = **held-out 재조합**: 학습에서 함께 본 적 없는 두 개념/원자를 결합해 새 held-out 항목을 맞히는가

지배 규범: tune-to-green 금지 · 음성도 결과 · 신호는 **값이 아니라 통제군 대비 Δ**(FORM tunable / BIND earned) ·
음성 cement 는 사전등록 TOST 필요 · 벽 선언엔 ≥2-3 통제 렌즈.

## 1. 뚫린 것 (🟢 · 2 독립 렌즈 · main 착륙 · ARCHITECTURE gate 노드 확정)

- **H_9267 XBIND** (2026-07-11): 303M 그대로 두고 **학습 measure(코퍼스×task-class)만 교체** →
  합성 XBIND 코퍼스(polarity XOR · held-out 15,960쌍)에서 held-out D-acc = **1.000 양 seed**,
  통제군 0.515, Δ=0.485. ⟹ G1 벽의 진범 = `corpus × CE` 결합 measure. substrate 능력천장 아님.
- **H_9288 MORPH-ATOM** (2026-07-13): BPE-jamo reversible byte-codec(형태소 원자성) →
  held-out 부정어 재조합 F2 = **0.908**(margin 2.14) ≫ C1(raw utf-8) **0.617**(margin 0.05), Δ=+0.291.
  둘 다 drilled F1≈1.0(암기는 동일) · C3 leak-ceiling 0.917 = V1 liveness PASS.
  ⟹ 원자성이 held-out 재조합에 **인과**. (누수 아님 — C1≠0.9)

⟹ ARCHITECTURE: "G1 재조합 = 능력천장 아님 (🟢 CRACK 2-lens) · G1/G6 wall-break 프로그램 종결 ·
재조사·재발사 불필요".

## 2. 막힌 것 (🧱 · 자연 분포에서의 자발 창발 = DATA-🧱 · 3중 정합)

2×2 (tokenization × 코퍼스분포):
```
              합성(drill)          자연(natural)
raw byte   │ XBIND      🟢 1.000 │ NAT-CRACK  🧱 반증
codec 원자 │ MORPH-ATOM 🟢 0.908 │ NO-RESCUE  🧱 0.345
```
- **H_9286 N2**(303M 4-arm 신규학습 T=105k, 2세션 독립 재현): **진짜 XOR 격자 arm 과 동전(무작위) 격자 arm 의
  held-out 이 83/174 = 0.4770 으로 완전 동일** ⟹ **연산자의 held-out 이득 = 정확히 0**.
  격자(연산자)는 설치됨(SEEN P_grid 0.950) — 그런데 held-out 이 안 오름.
- **기제 = ARBITRARY-GROUNDING**: I(gold;resp) = 0.007 bits ≈ 0 인데 I(atom;resp) = 0.231,
  원자별 부여극성이 참 극성과 일치 12/29 = 0.414. ⟹ 모델은 새 원자의 극성을 **모르는 게 아니라
  안정적으로 멋대로 정했다**. 좌항 **부재**가 아니라 **틀린 좌항 설치**.
- **H_9290 NAT-ATOM**: codec 원자성도 자연-분포 held-out 극성 접지를 rescue 못함
  (G-PROBE held-out probe-acc 0.345 < raw 0.552 < bar 0.65 · train_fit 1.0 = 프로브 유효 · Δ_shuffle −0.15).
  ⟹ 원자성 = **증폭기**이지 **신호 원천**이 아님.
- 자연 부정 신호 밀도 자체가 얇음: `a0neg` d_nat = 42.3/MB = NOT-POWERED.

## 3. 지금 돌고 있는 것 (판정 대기 · GPU 3대 · 곧 착지)

**H_9289 C3+C4** = rung-2 하이브리드 = "**라벨 붙은 자연 데이터로 틀린 좌항을 맞는 좌항으로 바꿀 수 있는가**".
4 arm(main_s7 · main_s11 · shufGT 통제 · N2rep 재현대조) 303M 신규학습 T=60k.
사전등록 게이트: V1 SEEN≥0.85 → GATE-0 표현-probe(held-out ≥0.65 양seed ∧ ≥shufGT+0.10) →
GATE-1 held-out flip0 원자별 paired Δ(main−shufGT) ≥ +0.15 양seed ∧ 절대치 >0.55 → GATE-2 XOR →
음성이면 TOST(Δ_eq 0.10). §6e 가드: Δ(main−N2rep)≈0 인데 Δ(main−shufGT) 만 크면 INVALID-CTRL.

**이미 나온 선-신호(main_s7 완주분)** — 이게 핵심 긴장이다:
- V1 SEEN = **0.9625 PASS** (격자 설치 확실)
- held-out D-acc 0.5230 · **flip0 0.471** · flip1 0.575 · margin_median **+0.309**(N2 −0.533 에서 부호 반전)
- **GATE-0 표현-probe = 0.5172** (N2 raw 0.5517 과 사실상 동일 · bar 0.65 크게 미달)
⟹ **해리(dissociation)**: 행동층은 개선됐는데 **표현층 극성 선형판독은 개선 0**.
   = 행동 개선이 '올바른 극성 표현 획득'에서 온 게 아니다. (틀린 좌항이 안 고쳐졌다는 시사)

## 4. 이미 죽은 레버 (재발사 금지 · check-ledger)

- read-side 6 lane 전수 floor(parametric · pointer-cache · plain-CE · fork-A swap-contrastive ·
  mid-stack split-payload · recurrence) · depth-RF(deep L8 engine-native best_distinct=1=L4)
- γ trunk trained-constructive-bind(H_1840): STEP-0 frozen-gate 에서 이미 차단(bind-add = −0.147).
  재발사 = tune-to-green. reopen 조건 = fork-A 🧱 착지 시 real-text target 재설계.
- organelle lane(자원 희소성/ATP·슬롯캡) = 🔴 KILL — 캡 조이면 held-out Δ = −0.192 단조하강(암기 압력).
- neuromod / untrained recurrence(ESN reservoir) / scale(303M→1B→7B, scale-invariant) = 전부 🧱.
- '자연 부정 신호가 얇다'는 데이터 사실 — tokenization 은 없는 신호를 만들지 못한다(2×2 세로줄).

## 5. 너에게 묻는 것 (발산 · 수렴 아님)

**질문: C3+C4 가 GATE-0 에서 떨어진다고 가정할 때(선-신호가 그 방향), 다음에 무엇을 쏠 것인가?**

특히 아래를 정면으로 다뤄라:
- (a) **해리(행동↑ / 표현 극성판독 0)** 는 무엇을 뜻하는가? 세 가지 이상 경합 해석을 세우고, 각각을 **가르는
  값싼 판별 실험**(discriminating test)을 붙여라. "표현이 없다" vs "표현은 있는데 선형-프로브가 못 읽는다"
  vs "행동 개선이 극성이 아닌 다른 축(형식/빈도/margin calibration)에서 온다" 를 어떻게 가르나?
  ⚠️ 프로브 계측결함 전례 있음(morphatom-gate-py-1: 4중 계측버그가 '학습 실패'를 위조했다) — 프로브를 먼저 의심하라.
- (b) **ARBITRARY-GROUNDING('틀린 좌항 설치')** 을 고치는 mechanism-family 를 **전수 열거**하라
  (data 채널 · objective 채널 · architecture 채널 · inference-time 채널 · 그 밖의 축).
  각 family 에 대해: 기제 한 줄 · 사전등록 가능한 falsifier · 최소비용 $0-probe · 이게 죽으면 무엇이 남나.
- (c) 지금 프레임 자체가 틀렸을 가능성 — **"자연 자발창발"이라는 목표 설정이 잘못된 질문일 수 있는가?**
  substrate-first(신경/생물/물리) 렌즈로 재프레임하라. 인간 아이는 held-out 극성을 어떻게 접지하나?
  거기서 anima 가 구조적으로 결여한 것은 무엇인가(감각운동 루프? 사회적 교정신호? 부정의 화용론적 대가?).
  이 재프레임이 낳는 **실행 가능한 실험**을 최소 2개 제시하라.
- (d) 값싼 것($0 · 기존 ckpt/코퍼스 재사용)과 비싼 것(GPU spend) 을 분리해 **우선순위 사다리**를 만들어라.

## 형식

- 발산 우선(넓게) → 각 갈래에 falsifier 와 비용을 달아라. 하나로 수렴시키지 마라.
- "논문/선행연구" 언급 금지(오너 정책 · 명시 요청 시에만).
- 죽은 레버를 다시 제안하지 마라(4절). 제안 전 4절과 대조하라.
- 한국어로.
