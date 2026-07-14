# H_9305 — O/C 채널: 학습 **분포**를 바꿔 rote-lookup 슬롯을 깨는가

- **tier**: ⏳ PENDING (사전등록 동결 · 발사 前 · 지출 승인 완료 \$21)
- **prereg**: `state/nbindg_grounding/PREREG_H9305.md`
- **선행 벽**: **H_9303 🧱 EARNED · ENGINE-NATIVE** (자연 분포는 held-out 원자의 극성을 접지 못함)
- **설계**: `state/nbindg_grounding/DESIGN_OC_fable.md` (Fable 5)
- **🔒 발사 게이트**: **AUDIT-A** (`anima-py evaluate --valence-audit` · engine-native · \$0) — 음성이면 발사 금지

## 진단 (왜 자연 노출이 슬롯에 도달 못하나)

`이 영화 <원자> ⇒ ___` 슬롯의 CE 최소해는 **rote lookup** 이다. grid 라인을 다 맞히는 순간 이 슬롯의
**gradient 가 0** 이 되고, 그 뒤 자연 코퍼스는 슬롯을 갱신할 압력을 전혀 만들지 못한다. 안 배운 원자의
답 = 그 암기 표의 **바이트-해시 외삽** ⇒ 원자별로 안정적(I=0.231)이면서 정답과는 무관(I≈0) —
H_9286 ARBITRARY-GROUNDING 관측과 정확히 일치.

⇒ **레버는 loss 항이 아니라 학습 분포.** CE 는 그대로(자유 하이퍼 0 · p7 충족), landscape 를 바꾼다.

## 처방 (D_train 3변경 · loss 불변)

1. **3-way 답 알파벳** `{긍정,부정,모름}` — 확정-금지를 penalty 가 아니라 **`모름` 이 정답인 라인**으로 구현
2. **`모름` 클래스** = NONCE(위조 어절) + NEUTRAL(코퍼스 무극성 원자) 1:1 — 판별 feature 를
   grid-친숙도가 아니라 **분포적 valence signature** 로 강제 (⚠️ `모름` 에 극성 원자를 넣으면 anti-grounding)
3. **1회-등장 회전 스트림** — 극성 원자 풀 1–2k 를 각 **정확히 1회**만 grid 에 등장 ⇒ rote 회수 불가 ⇒
   정답을 맞히는 유일한 길이 **분포적 증거를 읽는 것**이 됨

## arms · 계기

ARM-O(full) · ARM-ROT · ARM-ABS · ARM-CTRL(compute-matched). 계기는 H_9303 **verbatim 상속**:
`anima-py evaluate --ground-probe` (engine-native · 답하는 자리 · 배운 담체 · V-LIVE · 원자단위 n=91 ·
bar 0.65=2.86σ · flip 복원 · 순열 200).

## 동결 예측

**ARM-O 는 V-ROUTE 를 통과하고 임의-확정이 `모름` 으로 재배치되나, held-out probe 는 AUDIT-A 가 양성일
때만 bar 를 넘는다. ARM-CTRL 은 ≤0.60.**
