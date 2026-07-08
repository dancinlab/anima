# GATE 결과 — fork-A CLML lane (recomb-routing-lane · 2026-07-09)

no-copy 재설계(Fable 4-gate) 후 실 303M(e1_slw_303m) 측정 · aiden/summer anima-py · $0-pool.

## 🟢 Gate 1/2 PASS — 신호벽 아님 (clml_gate12_RESULT.json)
- **Gate 1** base(lane-OFF) CE=**1.044 nat** · next-byte acc=0.65 → 잔차 EXISTS (copy-format의 CE 0.0003과 대조 = 트렁크가 no-copy 위치는 못 함).
- **Gate 2** probe pool_yn→word-id: TRAIN **0.825** · held **0.600** (chance 0.04) → frozen pool이 name→word 라우팅을 담고 **일반화**.
- ⟹ 🟢 TRAINABLE — fork-A route가 학습가능(H_1840 신호벽 아님). copy-trap(#3210)이 진짜 원인이었고 no-copy 형식이 그걸 해소.

## 🟢 Gate 3 PASS — lane 실제 학습 (clml_train_RESULT.json · clml_lane.npz)
- word-initial CE로 lane {W1,b1,W2,w_g,b_g} 학습: CE lane-ON **1.044→0.718**(Δ-0.33)·acc 0.65→0.73·gate 0.05-0.10 열림. copy-format(Δ≈0 死)과 대조.
- ⚠ train-CE 개선(seen)이지 held 생성 아님 — Gate 4가 진짜 바.

## ⏳ Gate 4 (TERMINAL) — engine-native system-G1 held-out lane-ON vs lane-OFF (LIVE aiden)
학습 lane을 e1_slw_303m.clm에 append_clml_trailer(→e1_slw_303m_clml.clm r=128) · anima-py evaluate --py --system-g1 lane-ON(lane.clm) vs lane-OFF(base). 통제: surfacing(ON>OFF)·concept-ablation 특이성·G0 no-regress. **이 결과만이 fork-A 성공/실패 verdict**(route≠generation·Fable §6).
