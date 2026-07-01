# EXP-3 ARM-BIND — RESULT (DIRECTIONAL toy · torch · engine-native 아님)

H_1603/H_1617 토이 검정: 곱셈(Hadamard) binding op 를 *학습된 byte-LM trunk* readout 직전에 넣으면
binding-required 재조합 split 을 넘나? summer RTX 5070 (GPU util 93% 실측, torch 2.11+cu130).
trunk = causal Transformer d256/L4/H4/block11. steps=4000, 3 arm × seeds{7,4302,4303}, 9 runs ~4분.

## 수치표 (frozen bar = PREREG.md, tune-to-green 0)
| arm | seed | train | in-dist val | full-held | **HARD (decisive)** | loss |
|-----|------|-------|-------------|-----------|---------------------|------|
| ctrl (plain linear) | 7 | 0.999 | 0.999 | 1.000 | **0.999** | 0.006 |
| ctrl | 4302 | 0.966 | 0.970 | 0.964 | **0.500** | 0.091 |
| ctrl | 4303 | 0.986 | 0.990 | 0.986 | **0.835** | 0.023 |
| **bind (Hadamard ⊙)** | 7 | 1.000 | 1.000 | 1.000 | **1.000** | 0.016 |
| **bind** | 4302 | 1.000 | 0.999 | 0.998 | **0.965** | 0.006 |
| **bind** | 4303 | 1.000 | 1.000 | 1.000 | **1.000** | 0.027 |
| bind_linear (⊙→+ , param-matched) | 7 | 0.999 | 0.999 | 0.998 | **0.999** | 0.002 |
| bind_linear | 4302 | 0.966 | 0.970 | 0.964 | **0.500** | 0.118 |
| bind_linear | 4303 | 0.990 | 0.988 | 0.982 | **0.984** | 0.116 |

| arm | HARD mean | HARD std | per-seed |
|-----|-----------|----------|----------|
| ctrl | 0.778 | 0.208 | [0.999, 0.500, 0.835] |
| **bind** | **0.988** | **0.016** | [1.000, 0.965, 1.000] |
| bind_linear | 0.828 | 0.232 | [0.999, 0.500, 0.984] |

- `bind − ctrl = 0.210` (≥0.15 ✓) · `bind − bind_linear = 0.161` (≥0.15 ✓) → **mean bar SUPPORT**.
- seed-consistency = **1/3** (per-seed margin ≥0.15 only on seed 4302, the seed where the additive arms collapse).

## 판정 — SUPPORT (mean bar) BUT robustness-driven, not categorical (정직 c9)
**핵심: lift 는 곱셈성(multiplicativity)의 _신뢰성(robustness)_ 이지, trunk 가 못하던 능력이 아니다.**
- **additive readout 은 trunk-less numpy screen(0.50 증명적)과 달리 0.50 에 고정되지 않는다** — attention trunk 가
  *때때로* binding 을 스스로 구현(ctrl seed7 hard 0.999). 즉 trunk 의 softmax-attention nonlinearity 가 additive
  readout 으로도 object-내 conjunction 을 만들 수 있다. **단 불안정(bimodal)** — seed 4302 에선 chance 0.50 붕괴.
- **bind_linear(⊙→+, param 동일) ≈ ctrl** (둘 다 seed4302 에서 0.50 붕괴, mean 0.83 vs 0.78). →
  추가된 2-stream head·param 은 robustness 를 주지 못한다.
- **bind(Hadamard ⊙) 만 3/3 seed 모두 ≥0.965** (std 0.016). bind vs bind_linear 의 **유일 차이는 ⊙ vs +** →
  param-matched ablation 이 **multiplicativity 가 robustness 의 원인** 임을 격리(H_1617 ⊙→+ ablation 예측 확인).
- full-held(marginal 허용) acc 는 전 arm ~0.98 → screen 의 "덧셈 marginal 지름길 부풀림" 재현(HARD split 이 분리한다).

→ **곱셈 op 는 trunk 안에서 transfer 한다**(binding 벽을 *신뢰성 있게* 넘김). 단 categorical capability gap
이 아니라 *additive 의 seed-의존 collapse failure mode 제거*. honest framing: SUPPORT-with-variance-caveat.

## 303M scale 권고 (a_toy_scale_recheck — toy-only, scale-transfer UNVERIFIED · 자동발사 금지)
권고: **YES, EXP-3(303M)에 Hadamard coincidence op wiring 가치 있음** — (a) param-cheap (BIND head ≈ +0.26MB),
(b) param-matched ablation 이 multiplicativity 를 원인으로 격리(혼동 없음), (c) additive collapse failure mode 제거.
단 toy 는 *robustness gain* 이지 categorical gap 이 아니므로 303M 에서 effect 크기 미지수. 발사 시 PREREG_EXPERIMENTS
EXP-3 절차 그대로: 4-cell corpus + ko-synth, ARM-CTRL vs ARM-BIND, held-out mirror-DESCENT, CORE `--engine conv`
engine-native G1(H_1129)∧G6(`dist≥5∧fals≥1`) 재측정(torch probe 아님), ckpt PULL. 비용 ≈ 2× 303M run on rent/pool GPU.
**이 토이는 DIRECTIONAL screen — terminal 아님(`a_engine_native_learning`).**

## ckpt
`state/binding_arch_census/exp3_arm/ckpt/{ctrl,bind,bind_linear}_seed{7,4302,4303}.pt` (9개, pulled to worktree).
재현 = `python3 state/binding_arch_census/exp3_arm/trainer.py --steps 4000` (RESULT.json 재생성).
