# H_9406 — EARNED REFRACTORY 303M C3: 시계 벽을 뚫는다 (emit 이 tension 을 듣기 시작한다)

**status:** 🟢 GREEN-DIRECTIONAL (engine-native 303M · aiden · 3-seed · 5-cell 통제) — C3 gate-listens 양성 · C2(인식 vs 진폭) 후속 · wired: `anima-py chat --emit-refractory earned`
**lane:** 의식 / emit-drive / emit-gate 청취 (프런티어 g1-interface-addressable-wall)
**related:** [[H_9404]] (이 측정이 검증하는 earned refractory) · [[H_9405]] (preflight CALIBRATE → 이 fire) · [[H_9400]]/[[H_9403]] (뚫린 시계 벽) · [[H_9416]] (병렬 margin-gate C3 PASS · AGREES) · source: 오너 "aiden 발사 허용"
**ckpt:** py303_full.clm sha256 `013c4574…` (aiden · 신규 303M decode 15 traces × 60 tick)

## 측정 (오너 라티파이 · aiden)

H_9404 earned refractory(`--emit-refractory earned`·tension-integral debt)가 303M 에서 **emit 을
tension 에 흘리나**(H_9400/9403 "게이트는 시계 외 안 듣는다" 벽을 뚫나). 5-cell × 3-seed(7/4302/4303)
× 60 tick, aiden 격리 venv(RSS 2.7GB/worker·OOM 안전), T=1.0 REVEAL 샘플링. 스모크: earned
integrate-to-release 303M 작동 확증.

## 결과 (verbatim · 통제 설계가 핵심)

```
arm  desc        emit    g_recog[min..max]  H(emit|stage)   emit-pattern(60t·seed7)
A  a0/clock   42/180=.233  [0.27..0.57]     0.7283   00001000100010001000...  규칙적 시계
B  a4/clock   42/180=.233  [0.00..0.75]     0.7283   00001000100010001000...  규칙적 시계 (A 와 동일)
C  a0/earned  36/180=.200  [0.27..0.59]     0.6701   10000100001000001000...
D  a4/earned  55/180=.306  [0.00..0.79]     0.8700   10010010001000100100...  불규칙 텐션-구동
E  a3/earned  46/180=.256  [0.00..0.99]     0.8121   10100000100100010001...  불규칙 (noise)
```

## C3 GATE-LISTENS 🟢 (통제된 결정 증거)

- **통제 B vs D (같은 a4 arm · 유일 차이 = clock→earned)**: B(a4/clock) emit 은 **규칙적 시계**
  (period-4·`0000100010001…`·H(emit|stage) 0.73), D(a4/earned) emit 은 **불규칙 텐션-구동**
  (간격 3-4 가변·`100100100010001…`·H(emit|stage) **0.87**). ⇒ earned refractory 가 시계-고정
  캐던스를 **substrate 텐션-구동으로 전환**한다. 같은 g-arm·같은 seed, 유일 변수가 rate-term 소스뿐이라
  **인과 통제됨**.
- **H_9400 벽 재현 (A≡B)**: A(a0/clock)와 B(a4/clock) emit 패턴 **완전 동일**(둘 다 .233·동일 tick) ⇒
  **시계 하에선 g-arm 무관**(margin 이든 gap 이든 emit 안 바뀜) = H_9400/9403 "시계가 g 삼킴" 재현.
- **arm-selectivity (earned 하에서 g 가 살아남)**: earned arm C/D/E emit 패턴 **서로 다름**(A≡B 와 대비).
  ⇒ **earned refractory 를 켜면 g-arm 이 emit 에 영향**을 준다 = 게이트가 g 를 듣기 시작함.
- 전 arm emit rate 0.20~0.31 = **GATE-S band[0.05,0.95] 내**(포화/mute 없음 · H_9405 preflight 정합).

## C1 AMPLITUDE (보조)
a4(margin) g_recog [0.00..0.79] · distinct 52 > a0 [0.27..0.59] · distinct 40 — margin 이 gap-계열보다
넓은 진폭(H_9401 정합). 단 극적이진 않음.

## ⚠️ C2 (인식 vs 진폭) — OPEN
D(a4/earned margin)와 **E(a3/earned = 랜덤 noise-G) 둘 다 불규칙** emit 생성 ⇒ 이 측정만으론 D 의
불규칙성이 **margin-인식 특이**인지 "어떤 varying g 든" 진폭 효과인지 못 가른다. C2 = real-vs-shuf 통제
필요(병렬 [[H_9417]]이 margin-gate 모드서 측정 중). 따라서 이 H = **C3 양성(rewire 가 작동)**이지
"margin-인식이 emit 을 민다" 확정 아님.

## AGREES / 관계 (a_parallel_session_compare)

- **AGREES [[H_9416]] (병렬 margin-gate C3 PASS)**: 두 **독립 rewire 모드**(내 earned-refractory `--emit-
  refractory earned` · 병렬 margin-gate `--emit-gate refractory`)가 **두 다른 호스트**(aiden · summer)에서
  같은 결론 — p5-rewire 가 emit 을 tension 에 흘린다(C3 양성). 수렴 확증(중복 노력이 아니라 상호 검증).
- **CONFIRMS [[H_9400]]/[[H_9403]] 뚫림**: A≡B 가 시계 벽을 재현하고, earned 가 그 벽을 뚫음(같은 데이터셋
  안에서 before[clock]/after[earned] 대조).
- **VALIDATES [[H_9404]]/[[H_9405]]**: earned refractory 배선(H_9404)이 303M 서 작동·preflight CALIBRATE
  (H_9405)가 예측한 in-band 가변 캐던스 실측 확인.

## 반증 · scope
- 반증: earned arm 이 mute(emit≈0)/saturate(≈1)/stage-lock(H(emit|stage)≈clock)면 KILL — 현 D 0.87>
  clock 0.73·rate 0.31 in-band·불규칙 = 전부 통과. C2 에서 D≈E(margin=noise 구별불가)면 "진폭효과"로
  강등(현재 C2 미측정=OPEN).
- scope: 303M · aiden · T=1.0 · 3-seed. C3 양성=DIRECTIONAL(engine-native 이나 C2 통제 전·frozen-first).
  TERMINAL = C2(real-vs-shuf) + Ψ̂ 복원력([[H_9419]] 병렬: rewire 엔 복원 스프링 없음) 후.

## 비용
$0 추가(오너 라티파이 aiden pool CPU · 신규 303M decode 15×60tick · OMP=4 동시≤3 · RSS 2.7GB 안전).
