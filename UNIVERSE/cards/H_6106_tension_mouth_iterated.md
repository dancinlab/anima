# H_6106 — TENSION-MOUTH ITERATED (deep-equilibrium temporal escape)

**follow-on:** H_1834 (tension-mouth single-shot → INERT, composed_distinct=0, tension contributes 0)
**tier:** 🧱 DIRECTIONAL WALL (numpy toy; temporal iteration INERT — DPI meta-law confirmed, NOT engine-native)
**wired:** DIRECTIONAL-mirror only (numpy). 배선 없음 — lift 미발생이라 engine-native 재측정 unwarranted (사다리 (2)~(4) 미진입).
**source:** fleet-full IMPLEMENT lane — frontier `native-mouth-reframe`, temporal-equilibrium depth escape.
**artifacts:** `state/1837_tension_mouth_iterated/{tension_mouth_iterated_probe.py, results.md, H_6106_result.json, run.log}` · `state/verdicts/1837_tension_mouth_iterated/H_6106_FREEZE.txt`

## 메타법칙 (SSOT 기록)

floored 전 mouth = CE-trained feed-forward trunk-state 의 **SINGLE-SHOT 함수** → data-processing
inequality(DPI)가 출력연산자·readout penalty·배치·retrieval 을 **모두 한 좌표**로 묶는다 (trunk-state 에
없는 조합 MI 를 주입 불가). H_1834 가 이 1-shot 좌표를 확정했고, 유일한 미검 직교축 = 학습신호 geometry 의
**temporal(시간축)** 변경. 이 카드가 그 temporal 축의 첫 측정.

**결과: temporal 축도 DPI 벽을 넘지 못함 → 메타법칙이 1-shot 에서 temporal-equilibrium 으로 확장된다.**
가중치공유 사상을 fixed point 까지 반복해도 `h* = f_A(h*,x,e*) − g_G(h*,x,e*)` 는 여전히 같은 trunk-derived
정보의 함수 = 새 단일좌표일 뿐 새 정보원 아님. prefix e_k 는 trunk 자신의 readout 파생이라 재주입해도
trunk 에 없는 것을 재조건화하지 못함. **iteration count 는 lever 가 아니다.**

## 가설 (falsifiable)

mouth 를 1-shot readout 이 아니라 A(forward 예측장)⇄G(reverse 제약장) 텐션이 Ψ=½ 로 수렴하는
**입력-재주입 반복사상(deep-equilibrium)** 으로 보고, 조합깊이를 iteration count 에서 얻는다:
`h_{k+1} = f_A(h_k,x,e_k) − g_G(h_k,x,e_k)` (weight-shared, 매 step 입력 x + emit prefix e_k 재주입).
H_1834 는 이 반복사상을 1-shot bilinear 로 붕괴시켜 INERT 였음 — load-bearing = **매 step 입력 재주입**
(단순 반복 아님). 주장: byte-production 을 K-step tension-resolution 으로 *만들면* G1 `composed_distinct`
가 K≥2 에서 held-out floor(0) 위로 올라가고 Ψ=½ 이 보존된다.

## frozen bar (pre-registered `H_6106_FREEZE.txt`, p7, c9, tune-to-green 금지)

- 앵커: `composed_distinct = 0 @ K=1` (H_1834 single-shot floor 재현).
- 🟢 DIRECTIONAL iff **ALL**: (1) cd≥1 on ≥2/3 seed at some K≥2 (reinject ON) ∧ (2) K 단조 비감소 ∧
  (3) reinject ON 에서만 lift (**same-state ablation cd=0** = 재조건화가 소스임을 격리; INERT=DPI 확증) ∧
  (4) shuffle-control cd=0.
- 🧱 WALL (유효 negative): 수렴까지 K 올려도 cd=0 flat → DPI 메타법칙 확증, temporal iteration INERT =
  trunk-objective-bound 재확인 → γ trained-constructive-bind(HRR/circconv, cost-gated)이 유일 잔여경로.

## 측정 (numpy from-scratch, $0, seeds {7,4302,4303}, d=128, epochs=2500, K_MAX=16, KT=4.0)

gradcheck PASS (max|num−ana| through unroll = **1.49e-10**), train_acc = **1.00** 전 arm/K/seed (구현결함 배제).

**composed_distinct(K) — FULL deep-equilibrium (input-reinject ON):**

| K | cd (7 / 4302 / 4303) | mean | \|Ψ−0.5\| |
|---|:---:|:---:|:---:|
| **1** (=H_1834 anchor) | 0 / 0 / 0 | **0.00** | 0.007–0.011 |
| 2 | 0 / 0 / 0 | **0.00** | 0.017–0.031 |
| 4 | 0 / 0 / 0 | **0.00** | 0.014–0.042 |
| 8 | 0 / 0 / 0 | **0.00** | 0.014–0.022 |
| converge | 0 / 0 / 0 (stop_k 3/1/2) | **0.00** | 0.017–0.020 |

**cd = 0 flat, K=1→converge.** Ψ(K) 궤적(seed7, K16): 0.044,0.017,0.014,0.021,…,0.013 —
Ψ 가 **1–3 step 안에 ½ 에 앉고 유지** (equilibrium 즉시 도달, 추가 반복이 깊이를 안 더함).

**controls:** (a) K=1 anchor cd=0 ✓ · (b) **same-state ablation (reinject OFF) cd=0 all K/seed (INERT)** —
reinject ON 도 0 이라 재조건화도 lift 아님 · shuffle-control cd=0 all seed.

## Verdict

**🧱 WALL-DIRECTIONAL (DPI confirmed) — numpy toy, NOT terminal (`a_engine_native_learning`).**
lift=False (cd=0 @ 모든 K≥2). 앵커·monotone(flat)·ablation=0·shuffle=0 은 성립하나 load-bearing lift 부재 →
**temporal iteration INERT.** genuine deep-equilibrium 이 Ψ=½ 고정점에 실제 도달(1–3 step)해도 held-out
조합생성 = 0, single-shot floor·same-state ablation 과 동일.

**"시간-반복이 DPI 1-shot 벽을 넘었나 → NO."** DPI 메타법칙이 1-shot → temporal-equilibrium 으로 확장:
출력연산자·readout penalty·retrieval·**반복 재주입** 모두 CE-trained trunk-state 에 조합 MI 를 못 더한다.
G1 벽 lever = **trunk training OBJECTIVE (구성적 재조합 보상)**, mouth 의 temporal/spatial readout 구조 아님.
standing engine-native 기록(`substrate-framebreak-g1-combination-operator`·`g1-lever-multilens-objective`·
`h1816-predcoding-binding-not-supported`)과 정합. 잔여 유일경로 = **γ trained-constructive-bind**
(HRR/circular-convolution, recombination-rewarding objective 하 학습, cost-gated). Bar frozen pre-run, 미이동.

**next phase:** γ trained-constructive-bind (HRR/circconv binding operator × recomb-objective, cost-gated) —
operator/penalty/retrieval/temporal 4축 전수 floor 후 남은 마지막 잔여 lever. lift 발생 시에만 engine-native
core/ A⇄G iterate 재측정(a_toy_scale_recheck).
