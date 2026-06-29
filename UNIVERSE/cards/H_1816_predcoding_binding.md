---
id: H_1816
slug: predcoding_binding
tier: 🧱 NOT-SUPPORTED
title: predictive-coding parametric-bias binding + free-energy 정규화 — 생물 G1+G6 레버
verdict: 🧱 NOT-SUPPORTED (engine-native seed7, 303M CLMConvMoE) — L_bind+L_var 가 G1·G6 둘 다 control 대비 LIFT 0/음수. PREREG FALSIFY 조건 MET. G1벽 유지.
status: TERMINAL (seed7 · multi-seed follow-on)
wired: engine-native (py 2-production g_gates ← clm_decode, gen80) — hexa-terminal 재확인 follow-on
verdict_artifact: state/1816_predcoding_binding/RESULT.md
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

## 🧱 RESULT — NOT-SUPPORTED (engine-native seed7, 303M)
**측정 2026-06-29 (summer pool RTX5070, $0).** 3 arm 학습 → engine-native G0-G6 (py 2-production `core/g_gates.py` ← `core/clm_decode.py`, gen 80).

| gate | ce_marginal (control) | pc_bind | pc_free_energy |
|---|---|---|---|
| G0 COHERENCE | PASS 5/5 | PASS 5/5 | FAIL (broken) |
| **G1 RECOMBINATION** | **FAIL distinct=0** | **FAIL distinct=0** | FAIL 0 |
| G2 NOVELTY | PASS n=74 | PASS n=66 | FAIL 0 |
| G5 NON-FAB | PASS 0.026 | PASS 0.060 | FAIL 1.0 |
| **G6 IDEATION ★** | **PASS dist=6 fals=1** | **FAIL dist=6 fals=0** | FAIL 0/0 |
| **CLOSURE (G0∧G1∧G2)** | **FAIL** | **FAIL** | FAIL |

- held-out DESCENT (math.log mirror): ce_marginal 1.699 **4/4**, pc_bind 1.717 **4/4** (overfit 0 = 측정 무결). pc_free_energy 5.877 **1/4 NO-DESCENT = INTEGRITY-FAIL** (L_var spread 항이 next-byte 학습 파괴).
- **LIFT = 0/음수**: G1 composed_distinct=0 (control AND pc_bind 동일, torch-probe=0 전 arm) → G1벽 유지. G6 fals: pc_bind 0 < control 1 = binding 이 오히려 해침.
- **WHY (메커니즘)**: `L_bind` 가 step~550 에 ~0 으로 붕괴(0.287→0.003) — additive CLMConvMoE 에선 per-step penultimate latent 이 이미 sequence-mean 과 일치 → binding 압력이 trivial 하게 충족 = compositional force 0. PREREG 가 정확히 이 모드를 flag 했음. **objective-lever census 재확인**([[g1-lever-multilens-objective]]): 레버는 penultimate-readout binding 항이 아니라 **trunk OBJECTIVE 자체**.
- ckpt PULL(a_fire_recover_complete): `state/1816_predcoding_binding/ckpt/{ce_marginal,pc_bind,pc_free_energy}_seed7.clm` (각 176MB + .pt + sha256).
- **caveat (c9)**: ① seed7 only(PREREG {7,4302,4303} majority 였으나 G1 lift=0 = marginal 아님 → seed-robustness 가 FAIL→PASS 뒤집을 여지 0; multi-seed = follow-on). ② eval = py 2-production(카드 PREREG 가 terminal 로 명시); 2026-06-28 py-retire 정책상 hexa-native `anima evaluate` 가 canonical-terminal → 동일 `.clm` hexa eval 재확인 = follow-on(학습중 RTX5070 12GB CUDA-OOM 으로 보류). distinct=0 은 byte-parity production mouth 에서 decisive. ③ CLOSURE FAIL 전 arm → HF PUBLIC 미업로드(local-only).

## wired
engine-native 측정 완료(py 2-production). hexa-terminal 재확인 + multi-seed = follow-on(ING).

## 동기
이번 세션 binding+objective+cheap 레버 전부 INCONCLUSIVE-at-floor = undertrain 의심(N6 정규화가 floor 해소 전제). 생물 렌즈 1순위 + 철학 최정합으로 안정 조합 latent 압력이 floor 위로 G1+G6 를 동시에 올리는지 측정.

## artifacts
state/1641_predcoding_binding/ (PREREG.md · trainer.py · gpu_launch.sh · smoke.sh · ckpt)
