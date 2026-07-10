# H_1584 — deep ConvMoE depth/RF 확장이 G1 재조합 벽을 여는가 (L4→L8 · engine-native 303M)

**tier**: 🧱 FALSIFIED (engine-native 303M · `anima-py evaluate` G-battery · a_eval_py_canonical TERMINAL) — depth/RF 확장(L4→L8)이 G1 재조합 bar 를 못 움직임 (2026-07-10)

## Claim
[[H_1394]] 격리(302.6M ConvMoE-L1 FALS=0 vs 303M L24 ByteGPT FALS=1.0)와 numpy RF-reachability probe
(conv_L1 reach=0 벽재현 · conv_L8 reach=1.47e-3 REACHABLE)가 시사한 가설: **G1 재조합 벽은 receptive-field-bound
이지 arch-class 천장이 아니다.** 프로덕션 `.clm`이 얕은 L4(단일 conv-trunk 계열)라 RF=L(K−1)+1 이 작아 거리 D>RF 인
두 개념이 수학적으로 독립 → 재조합 불가(capacity 무관). ⟹ **depth L≥8 로 RF 를 2배 확장해 같은 코퍼스로 학습하면
G1 재조합(ρ·weave)이 열린다.**

## Why (substrate-first · RF isolation)
CLMConvMoE 는 attention/K/V 없는 residual dilated-conv 트렁크. RF = 층수에 선형 → L4→L8 이 RF 를 ~2배 확장.
공정 격리 = **L4 vs L8, SAME 4-cell 코퍼스**(H_1394 style) 로 depth 만이 유일 변수. numpy probe 는 확장 RF 로
distal 두 개념 사이 정보 *흐름*이 존재함을 증명했으나(reach 1.47e-3 REACHABLE), 학습된 모델이 그 흐름을 재조합에
*쓰도록* 학습하는지는 미측정 → 이 카드가 engine-native 로 종결.

## Test (pre-registered · 단일 실행 · engine-native)
- 학습: `anima-py train --arch clm --L 8 --d 3784 --e0 3 --emax 3 --slw --corpus <4-cell> --seq-len 1024 --steps 2000`
  (프로덕션 recipe = L 만 4→8 교체 · A100 pool · rent=spend owner go).
- 측정: `anima-py evaluate e1_slw_deep_L8.clm --corpus <4-cell>` G-battery (ρ·weave = G1 재조합 bar · gen=40 default).
- **CRACK** = ρ·weave PASS (best_distinct≥2 & >max_single) · **🧱** = best_distinct=1 (L4 floor 재현).

## Verdict — 🧱 FALSIFIED (2026-07-10 · verified merge)
학습 **CLEAN**(verdict-integrity clear): loss 5.63603→1.55177 DESCENT · registers_DESCENT=4/4
(cell0 1.492 · cell1 1.412 · cell2 1.691 · cell3 2.248 · uniform=5.5452) · val_CE(pooled)=1.711 ≪ uniform ·
savant_latched · expert_div=0.551(3 experts 활성) · clm_decodable=True · SLW trailer appended.
모델은 건강하게 학습됨.

그러나 **ρ·weave RECOMBINATION 🔴 FAIL — best_distinct=1 (need ≥2 & >max_single=0)** = **프로덕션 L4 와 동일 floor**.
ρ·form 🟢 PASS(coherent) · σ 전축 9/9 LIVE(Θ Δ0.46·bind Φ1.45·gate Δ0.81 …) → 모델 무결, 재조합만 벽.

**함의:** depth/RF 확장은 engine-native 303M-class byte-LM 에서 G1 재조합을 **못 연다.** numpy reachability(정보흐름
존재)와 trained-model 재조합(정보 *사용*)이 괴리 = **[[fleet-g1g6-nativemouth-dpi-convergence]] DPI 메타법칙** 정합
(additive-solvable loss → 레버·용량·RF 무관하게 additive floor 로 탈출). H_1394 의 "arch-class 아닌 RF-bound" 재프레임은
FALSIFIED — L1 과 L8 모두 재조합 floor 이므로 벽은 depth/RF 축이 아니다.

이로써 **G1 재조합 frontier 의 마지막 측정가능 레버가 소진**: read-side 6 lane 🧱 + γ en/STEP-0 🧱 + γ ko instrument-invalid
+ census 🧱 + **depth-RF(H_1584) 🧱**. 유일 잔여 = [[gamma-trunk-bake-step0-killed-not-unmeasured]] γ trunk-bake
(STEP-0 frozen-gate 이미 차단 · tune-to-green 금지).

- ckpt: `dancinlab/anima-deep-convmoe-L8` (HF PUBLIC · sha256 7d221ec8…) + `~/anima-weights/deep_convmoe_L8/`.
- raw: `state/1580_convmoe_g1_wall/deep_L8_verdict/` (gbat_L8.log · deep2.log · GATE_RESULT.md).
