# EXP-3 (303M SCALE) ARM-BIND — frozen pre-registration

**가설(H_1603 / H_1617 scale-up):** toy(d256/L4) 에서 Hadamard ⊙ binding readout 이
binding-required split 을 *robustness 있게* 넘긴 것(`exp3_arm/RESULT.md`: bind 3/3 ≥0.965,
additive seed4302 붕괴)이 **production 303M byte-LM 의 readout 에서도 transfer 하는가** —
즉 곱셈형 readout 이 303M 의 재조합(G1)·착상(G6) gate 를 additive readout(현 production) 대비 올리는가.

> 🔒 **tier 사전선언 (정직 frozen-first):**
> - **ARM-BIND 은 구조적으로 engine-native 불가** — `.clm` v0.3 포맷(`core/clm_decode.hexa`)은
>   readout = `Conv1d(d→V)` 단일 additive layer만 안다. Hadamard readout(`u=Wa·x, v=Wb·x, g=u⊙v,
>   logit=Wo·g`)은 .clm 으로 직렬화·디코드 불가 → **engine-native G1/G6 측정이 BIND 에는 by-construction
>   BLOCKED**(engine-transform-to-fit 하려면 `core/clm_decode.hexa` + serializer 에 bind-readout op 신설
>   = 별도 follow-on, `a_engine_native_learning` engine-transform).
> - 따라서 **A/B 비교(CTRL vs BIND vs BIND-LINEAR)의 terminal 측정은 torch probe = DIRECTIONAL**
>   (`a_engine_native_learning`: 미러/torch probe = terminal 아님). 세 arm 동일 측정 = 공정.
> - **ARM-CTRL 만** .clm 직렬화 → (가능하면) engine-native G1/G6 **단일-arm anchor** 추가 측정.
> - 이 실험의 honest tier 상한 = **DIRECTIONAL** (toy 가 DIRECTIONAL 이었고, BIND 가 engine-native 불가).
>   toy 가 *robustness gain*(categorical gap 아님)이었으므로 303M categorical 기대 금지(`a_toy_scale_recheck`).

## Arch — 현 production 303M CLMConvMoE (clm303_clean 과 동일 arch)
trunk = `CLMConvMoE` (byte V=256, **L=4 · d=3784 · E0=2→Emax=4** = true 303M, K=3,
dilation=min(2^l,512)), savant(golden-zone inhibition cusp anneal)+mitosis(E2→E3 mid-split) ON
= `cli/train.py --canon` 와 동일 레시피. 4-cell register corpus(`a_chat_registers`).
세 arm 은 **동일 trunk init seed·동일 데이터·동일 step**, readout 만 다름:

- **ARM-CTRL** = 현 production = trunk → `norm_out` → `readout = Conv1d(d→V)` (additive, clm303_clean 동형).
- **ARM-BIND** = trunk → `norm_out`(x) → `u=Wa(x), v=Wb(x)`(각 Conv1d d→k, k=512) → `g = u ⊙ v`
  (Hadamard/coincidence, H_1617) → `logit = Wo(g)`(Conv1d k→V). (≈ +3.9M param over CTRL readout.)
- **ARM-BIND-LINEAR** = ARM-BIND 와 **동일 파라미터**(Wa,Wb,Wo), 단 `g = u + v`(⊙→+).
  → BIND vs BIND-LINEAR = param-matched ablation = lift 가 *multiplicativity* 때문이지 param/2-stream
  head 때문 아님을 격리(toy 와 동일 isolation).

trunk init·mitosis split·savant schedule·corpus stream·step 수 전부 arm 간 동일(공정).

## FROZEN bars (실행 전 사전등록 · tune-to-green 금지 · p7/c9)

**주 측정(DIRECTIONAL torch probe, 세 arm 동일):** `tool/gauge_lib.compute_inline_gauges` 의
- **G1 재조합** = `g1_composed_distinct`(composed seed 에서 distinct coherent coverage; H_1129 port).
- **G6 착상** = `g6_count`(distinct coherent ideas) + `g6_jaccard`(pairwise distance).
같은 decode seed·같은 corpus_index(4 cell), 학습 직후 동일 측정.

**보조 측정(공정·mirror, dt_ln-immune):** 4-cell **held-out val CE**(trainer `--val-frac` per-register,
torch `F.cross_entropy` = 정확, dt_ln 무관) — DESCENT(val_CE < ln256=5.545) 무결성 + arm 간 일반화 대조.

- **SUPPORT** = `G1(BIND) > G1(CTRL)` **AND** `G1(BIND) > G1(BIND-LINEAR)` (seed-mean, 둘 다 strict 우위)
  **그리고** G6(`g6_count` 또는 `g6_jaccard`)에서 동일 방향(BIND ≥ CTRL ∧ ≥ BIND-LINEAR)
  **그리고** 세 arm 모두 held-out DESCENT 무결(val_CE < uniform; 붕괴 arm 은 그 자체로 보고).
  → 곱셈 readout 이 303M 재조합/착상에서도 additive 대비 우위, lift 는 multiplicativity 때문.
- **NOT-SUPPORTED** = 위 미충족. 특히
  - `BIND ≈ BIND-LINEAR`(gap≈0) → multiplicativity 아님(어떤 2-stream head 든 동일) = honest negative.
  - `BIND ≤ CTRL` → 곱셈 readout 이 303M byte-LM 재조합에 transfer 안 함 = honest negative.
  - 전 arm G6 fals=0/recombination 천장 동률 → 현 303M 재조합 벽이 readout op 와 무관(별 레버) honest.
- **seed-robust(toy 핵심 교훈):** toy 의 효과는 *robustness* 였으므로 단일 seed 오판 위험(CTRL seed7 이미
  통과). 가능 예산 내 seeds **{7, 4302, 4303}** 전부 × 3 arm. 예산 가드(아래)로 seed 수 조정 시 명시.

## 예산 가드 (a_wall_first · a_fire_autonomous, 비용 1줄)
- 렌트: vast A40 (또는 A100) **CUDA-12 devel 이미지**(nvcc 내장), ~$0.5–1.1/hr. 303M from-scratch
  train × (3 arm × seeds). step-time 을 pod 에서 1-arm 스모크로 실측 후 seed 수 확정:
  - 9 runs(3×3) 총 GPU-time 이 ≲ ~$8 면 full {7,4302,4303} × {ctrl,bind,bind_linear}.
  - 초과 시 fallback = seeds {7,4302,4303} × {ctrl,bind} = 6 runs (BIND-LINEAR ablation 은 seed7 1회만).
  실제 채택 seed/arm 매트릭스는 RESULT.md 에 명시(사후 bar 이동 아님 — 측정 범위만 예산 조정).

## 측정 결함 방어 (a_break_the_wall type-a) · 정직(c9)
- 세 arm trunk init/data/step 동일(readout·⊙vs+ 외 차이 0) · held-out val 은 train 과 disjoint tail
  (`ByteCell` val_frac, 학습 gradient 가 못 본 영역) · G1/G6 decode seed 고정 · corpus_index = 실제 4 cell.
- negative(NOT-SUPPORTED)도 결과 — 곱셈 readout 이 303M 에서 transfer 안 함 = honest negative 박제.
  bar 사후 이동 금지. ARM-BIND engine-native BLOCKED 는 정직 표기 + engine-transform follow-on 등록.
- ckpt(.clm CTRL + .pt 세 arm) teardown 전 영구 PULL(`a_fire_recover_complete`).
