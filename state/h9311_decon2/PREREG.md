# H_9311 — DECON-2 · DEMO-PORT · 사전등록 (데이터 전 동결)

> 🔒 `prereg-oc-json-1` 하드게이트. DV·bar·N_REQ·seed·TOST Δ_eq 를 아래에 고정한다.
> **사후에 bar/n/DV 를 바꾸면 자동 INVALID.** 설계 원안 = `state/h9309_decon/DECON2_DESIGN.md`(Fable).

## 0. 한 줄

H_9309 는 **모델이 못 읽는 언어로 말을 걸어** 죽었다(주입이 margin 을 59~74% 흔들었으나 방향 무작위 =
정보량 0). DECON-2 는 **주입 언어를 모델 자신의 학습 템플릿으로 교체**한다. 재튜닝이 아니라 **언어 교체**.

```
seed′ = "이 영화 {시연어간}고 => {긍정|부정}.\n" + "이 영화 {대상표면형} => "
```

## 1. 동결 전 실측 (추정 0 · `prefreeze_audit.py` · 전부 디스크에서 읽음)

Fable 경고: *"구분자를 추정으로 넣으면 그게 곧 제2의 F2다."* 그래서 셋 다 측정했다.

| 질문 | 실측 |
|---|---|
| 인스턴스 구분자 | **`b"\n"` 단일바이트 · 960/960 만장일치** |
| 2-연접이 분포 안인가 (Fable D8) | 학습 `seq_len=**1024**B`(`cli/train.py:1206` · C34 발사명령에 `--seq-len` 없음 · 그 분기의 d=3784 L=4 가 ckpt 와 일치) · 인스턴스 median **41B** ⟹ **창 하나에 약 24개가 연속으로** 들어갔다 = `인스턴스 \n 인스턴스` 는 **모델이 매 스텝 본 것** ✅ |
| 평가 시 좌문맥 | pad = **공백(32)** (`core/decode.py:955`) ⟹ **지금까지의 평가 문맥이 이미 분포 밖**(학습에선 프롬프트 왼쪽이 언제나 '앞선 인스턴스+개행'이었다) ⟹ **시연은 문맥을 분포 안으로 되돌린다.** D8 은 해소를 넘어 **역전** |

**byte budget**: 시연 ≤38B + 대상 seed ≤41B + gold 7B = **≤86B** ⟹ **win=128 동결**
(학습 창 1024 의 1/8 · 실측 여유 최소 45B · DEMO 창 초과 **0/1734** ✅).
DEMO 는 **fallback 포맷 없음** — 일부 시행을 라벨-only 로 강등하면 H_9309 가 정보량 0 으로 실측한
포맷이 조용히 섞여 **혼합계기**가 된다. 초과 시행은 DROPPED 이고 **DROPPED>0 = INVALID-INSTRUMENT**.

## 2. arm 3개 (신호 = 값이 아니라 ≥2 통제 대비 차분)

| arm | 시연 | 역할 |
|---|---|---|
| **NOSTORE** | 없음 | 바닥 |
| **MATCHED** | 대상 원자 **자신**의 참극성 | 처치 |
| **MISMATCH** | **다른** 원자의 시연(순환 시프트) | **역-앵무새 통제** |

**MISMATCH 가 판정을 번다.** "방금 나온 문자열을 억제"하는 byte-LM 이라면 MATCHED flip1 은
**합성 없이도 전부 정답**이다(거기서 gold 는 언제나 시연 라벨의 반대). MISMATCH 에선 시연 라벨이
대상 gold 와 **독립**이라 그 교대편향이 이득을 못 본다 ⟹ MATCHED−MISMATCH 대비가 양변에서 상쇄한다.

## 3. DV 3층 (flip0 은 소비 지표에서 **해임** — 시연이 답을 통째로 주므로)

| 층 | 통계량 | bar (사후 재선택 금지) |
|---|---|---|
| **READ** | MATCHED flip0, **int1·int2 만** | ≥ **0.85** — 시연이 읽히긴 하는가. 낙제 = **INVALID-FORMAT**(포맷 미독), 소비 음성 아님 |
| **CONSUME** (primary) | MATCHED flip1 원자클러스터 3-형태 다수결 | nonce **≥140/240** (H0 0.5 단측 p≈0.007) · held-out **≥20/29** (p=0.031) · **양 seed AND** |
| **BIND** (secondary) | MATCHED flip1 − MISMATCH flip1(A=false), 행-paired | McNemar **p<0.01** ∧ 대비 **≥0.10** · 양 seed |

- **bare-flip0 행은 전 통계에서 제외** — 시연과 문자열이 그대로 겹치는 순수복사행.
- **교대편향 밸리디티**: MISMATCH 에서 시연라벨=gold 여부 A 로 조건부 분할, `|acc(A=T)−acc(A=F)| ≤ 0.15`.
  초과 시 **CONSUME 단독 PASS 금지**, BIND 로만 판정.

## 4. copy-solvable 이 아님의 **구조적 증명** (`evaluate-py-2` 함정 정면 대응)

`evaluate-py-2` 의 조건은 "**정답이** 컨텍스트에 있다"이다. MATCHED flip1 에서 컨텍스트에 있는 라벨은
시연의 `부정.` = **2AFC 의 counterfactual 쪽 문자열**이고, **gold(`긍정.`)는 컨텍스트에 없다**.
복사·반복편향은 컨텍스트 내 문자열의 NLL 을 **낮추므로** `margin = NLL(cf) − NLL(gold)` 를
**끌어내린다** ⟹ **copy 는 flip1 을 통과시키는 방향이 아니라 떨어뜨리는 방향으로만 작동한다.**
flip1 PASS 는 copy 에 대해 **구조적으로 보수적**이다. (실측 예: `이 영화 참고 => 부정.\n이 영화 참지
않다 => ` · gold=긍정. · cf=부정. ← 시연 라벨과 동일.)

## 5. 게이트 사다리 (각 단계 킬스위치 · 전부 forward-only $0)

| 게이트 | 내용 | bar |
|---|---|---|
| **G-A** 창 유효성 | NOSTORE 를 win 64 vs 128 재계산 | margin 부호일치 ≥166/174 ∧ flip-class acc 차 ≤0.03 · **그리고** SEEN no-demo flip1@128 ≥0.90 |
| **G-B** PC-SEEN-DEMO | SEEN 20원자 + 참시연 = **2-연접 포맷 판독성 직접 증명** | flip1 ≥0.90 ∧ flip0(int) ≥0.90 |
| **G-D** PC-NONCE-240 | 발사게이트 본체 + **음성 cement 장소** | READ ≥0.85 · CONSUME ≥140/240 · BIND |
| **G-E** HELD-OUT-29 | G1 본 질문 · **1회 접촉 예산** | CONSUME ≥20/29 양 seed |

⛔ **G-B 낙제 ⟹ nonce·held-out 미발사**(few-shot fallback 1회 → 그것도 낙제면 컨텍스트 포트 판독 불가).
⛔ **G-D 낙제 ⟹ held-out 미발사.**

## 6. 검정력 · TOST (데이터 전 산출)

- **nonce 240 = 이 설계의 핵심 자유도**: nonce 는 코퍼스가 필요 없다(진리를 우리가 선언하고 **오직
  시연으로만** 전달) ⟹ **$0 로 임의 확장** ⟹ H_9309 가 못 푼 검정력 문제가 **PC 단계에서 풀린다**.
  **TOST Δ_eq=0.10, α=0.05, power 0.9 ⟹ N_REQ=214 ≤ 240 ✅ = 음성 cement 가능.**
- **held-out n=29 는 고정**(oracle 접지가 있는 원자가 그것뿐 · 450k 코퍼스 디스크 부재) ⟹
  **TOST 불가** ⟹ G-E 의 음성은 **DIRECTIONAL 전용("지지까지만")** 임을 사전 명기한다.
- **seed = main_s7 · main_s11, 전 bar AND**. 한 seed 만 통과하면 PASS 가 아니라 **SEED-SPLIT**
  (H_9289 부호반전 폭 0.161 = 복제편차의 18배 · 통과 방향에도 대칭 적용).

## 7. 판정표 (사전 고정)

| 관측 | 판정 |
|---|---|
| G-A 낙제 | ⛔ INVALID-INFRA (창) — 96 재시도 → 불가 시 발사 금지 |
| G-B 낙제 | ⛔ INVALID-FORMAT (2연접 미독) — few-shot 1회 → DECON-W 이관 |
| G-D READ 낙제 | ⛔ INVALID-FORMAT (nonce-in-demo 파싱) |
| READ ✓ · CONSUME ✗ (TOST 안) | 🧱 **EARNED 음성 — 컨텍스트 A-채널 死** (240 이라 cement 가능) |
| CONSUME ✓ · 교대편향 검출 | ⚠️ Tier-1 무효 — BIND 로만 재판정 |
| CONSUME ✓ · BIND ≈ 0 (편향 청정) | 🟡 **PASS-UNBOUND** — 소비 성립 · 원자결합 미성립(단일-사실 스코프) |
| CONSUME ✓ · BIND ✓ | 🟢 **PASS-BOUND** → G-E 발사 |
| G-E ≥20/29 양 seed | 🟢-dir **held-out 재조합 성립** (engine-native py · 배선+카드) |
| G-E 낙제 | DIRECTIONAL 음성만 — **cement 불가 명기** |
| DROPPED > 0 | ⛔ INVALID-INSTRUMENT |

## 8. 정직 — 가장 그럴듯한 사망 경로

**"읽히는데 소비 안 됨"**(D1). SEEN 0.950 이 증명하는 것은 `연산자∘parametric 값`이지
`연산자∘context 값`이 아니다. 연산자의 피연산자 포트가 **가중치에서만** 읽도록 배선돼 있다면
포맷이 완벽해도 여기서 죽는다. 다만 이번엔 게이트 순서(G-B 포맷판독 ✓ → G-D 소비 ✗)가 그것을
**INVALID 이 아니라 EARNED 음성**으로 만든다 — 다섯 번째 자기-PC 낙제가 아니라 **첫 번째 벌어낸 음성**.
그것이 이 설계의 최소 보장이다.

## 9. 비용

전 게이트 **forward-only**(학습 0). 행수 ≈ nonce 1440 × 3arm × 2seed + SEEN/held-out ≈ 9.6k 행.
pool GPU(summer/aiden · `[gpu]` cupy 경로) **$0**. `anima-py evaluate --consult` (배선 완료).
