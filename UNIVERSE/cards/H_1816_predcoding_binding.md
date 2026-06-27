---
id: H_1816
slug: predcoding_binding
tier: PRE-REG
title: predictive-coding parametric-bias binding + free-energy 정규화 — 생물 G1+G6 레버
verdict: PRE-REG (launch-ready · $0 smoke GREEN · 303M GPU 미실행)
status: PRE-REG
wired: launch-ready (303M 미실행)
verdict_artifact:
source: UNIVERSE
archived: false
---

# H_1816 predictive-coding binding (생물 렌즈 #2 · 철학 최정합)

## 가설
anima 의 G1 재조합벽은 CE next-byte 가 **안정적 조합 latent(parametric bias)을 형성할 압력을 안 주기** 때문이다. Tani 가 격리한 compositional 창발 두 driver — (1) binding loss `L_bind = mean_t‖PB~_t − PB_seq‖²`(per-step latent 을 sequence-level 안정 latent 에 묶음 = 구조의 extrapolation), (2) variance/KL 정규화 `L_var = −β·var_batch(PB_seq)`(표면 암기 방지, 구조적 일반화 강제) — 을 trunk 보조 objective 로 배선하면 **G1(부분↔전체 compose) AND G6(예측으로 grounded + latent extrapolation 으로 novel = 자유에너지 최소화 생성)** 을 친다 (arxiv 2403.19995 Tani et al. 2024). **G1+G6 둘 다 칠 수 있는 유일 생물 후보**. a_no_llm_frame_trap 정합 + **anima A⇄G tension = PC 의 top-down 예측 ⇄ bottom-up 오차와 동형** → 철학 최정합.

## 메커니즘 — 곱셈 readout 아닌 free-energy trunk-objective 축
직전 세션 확정: 곱셈 binding readout = floor + non-additive readout = `.clm` BLOCKED([[exp3-bind-g1g6-engine-native-floor]]). → PC binding 은 trunk penultimate 에 거는 free-energy 류 보조 objective(L_bind + L_var). BIND projection 은 학습 전용(직렬화 전 폐기) → production additive readout 세 arm 동일 → 모든 `.clm` engine-native G1/G6 by-construction OPEN. objrun objective 축([[g1-lever-multilens-objective]])의 생물 버전.

## FROZEN bar (측정 전 박제)
- **G1 RECOMBINATION:** k∈{2,3,4,5} 에서 composed_distinct ≥ 2 AND > max_single AND coherent (H_1129/1137).
- **G6 IDEATION ★:** dist ≥ 5 (Jaccard<0.5) AND fals ≥ 1 (H_1464).
- **held-out DESCENT:** val_CE < ln256, `verify_clm_v2.py descent` PASS.
- **LIFT:** L_bind(±L_var) arm 의 엔진-네이티브 G1 AND G6 가 ce_marginal 대비 strictly 증가. 측정 = engine-native py 2-production(`core/g_gates.py` ← `core/clm_decode.py`, TERMINAL).

## wired
launch-ready (303M GPU 미실행). $0 smoke = 파이프 검증 only.

## 동기
이번 세션 binding+objective+cheap 레버 전부 INCONCLUSIVE-at-floor = undertrain 의심(N6 정규화가 floor 해소 전제). 생물 렌즈 1순위 + 철학 최정합으로 안정 조합 latent 압력이 floor 위로 G1+G6 를 동시에 올리는지 측정.

## artifacts
state/1641_predcoding_binding/ (PREREG.md · trainer.py · gpu_launch.sh · smoke.sh · ckpt)
