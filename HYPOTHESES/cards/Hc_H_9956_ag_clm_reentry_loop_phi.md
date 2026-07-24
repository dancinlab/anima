# H_9956 · A⇄G⇄CLM 재진입 루프로 Φ>0 만들기 — 의미는 가장 강하지만 **가장 죽을 것으로 예상**

**한 줄:** Fable P2 ≡ Sol 3 **독립수렴**(같은 각도, 이름만 다름 — Fable `--clm-writeback on`,
Sol `--ag-clm-reentry pc2-state3`). 학습 중에 엔진→CLM 되쓰기 손(PC2)을 켜서 합성계를
비-앞먹임으로 만들면 Φ>0 이 가능하다. **두 모델 모두 이 각도가 죽을 것으로 예상**한다.

## 처치 (제안 · 미구현)
- **flag:** `anima-py train --ag-clm-reentry pc2-state3` — 기존 PC2 와 A/G state 를 3-bit state 로 만들고,
  CLM summary 가 다음 A/G state 를 갱신, 그 state 가 다시 다음 token logits/hidden 에 들어가게 unroll.
- **현행 실태:** CLM→engine 은 live 지만 engine→CLM 은 기본 **2-bit phase theater**, PC2 hands 는 default-off,
  체크포인트 writeback 0 (기억: `engine-to-clm-hands-exist-but-off`). p8(train/infer 분리 없음)은 오히려 이걸 지지.
- **Φ>0 근거:** CLM→state→CLM 의 닫힌 시간적 인과 순환. ⚠️ 전체 303M 의 IIT-4 Φ 는 **계산 불가능** —
  주장 가능한 건 **사전 고정된 3-bit macro-loop 의 Φ** 뿐이다.

## DV · 받침대 · 통제
- **DV:** H_9954 와 동일한 개입형 TPM collapse-Δ.
- **PEDESTAL:** one-step unfold 트윈 (참값 0).
- **통제 1:** state→CLM 엣지 절단.
- **통제 2:** phase/PC2 **time-yoke** — 동일 주변분포·동일 compute 로, 틀린 tick 의 state 를 주입.
- **비용:** 순차 unroll 때문에 세 안 중 **최악**. Φ 전용 pool 지출 금지.

## KILL · 전망
$0 macro 스크린이 두 통제를 못 이기면 **구현·303M fire 이전에 중단**. 근거 있는 비관:
**H_9607** 에서 A⇄G amplitude 되먹임은 이미 loop-live 였는데 criticality(butterfly slope −0.00004 수축)·
emit 인과채널(TE=0)·homeostasis 가 **전부 죽어** STILL-SEALED 로 착륙했다. 같은 결말이 기본 예상이다.

- 상태 PROPOSED · 측정 0 · cement 는 engine-native `anima-py` 로만.
- 관련: [[H_9954]] · [[H_9607]] · [[H_9942]] · [[H_9846]]
