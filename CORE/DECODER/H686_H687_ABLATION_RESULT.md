# H_686 + H_687 aux-loss 토이 ablation 결과 (2026-05-29)

**status**: ⚪ TOY-NULL — toy regime 이 M4b production collapse 를 재현하지 못함
**source**: UNIVERSE Cycle #24 (PR #1391) H_686 + H_687 의 본선 후보 검증 후속
**harness**: `CORE/DECODER/h686_h687_aux_ablation.hexa`
**raw output**: `CORE/DECODER/state/h686_h687_ablation_2026_05_29/run.out`
**cost**: $0 mac-local, 600 step × 4 cell × 2 (determinism re-run) wall ~수십 초

---

## 1. 배경

UNIVERSE Cycle #24 가 H_686 (router entropy regularization, `H(p_gate) ≥ ln(K)/2`)
+ H_687 (KL(softmax(logits) || uniform_V) output regularization) 두 가설을 ⚪
SPECULATION-FENCED 로 land 했음 (#1391). 둘 다 closed-form band 는 PASS 였으나,
production fire 는 별 H 로 deferred. 이 ablation 은 그 toy-scale 검증.

본 ablation 의 목적: $0 mac-local 에서 4-cell ablation 으로 두 aux-loss 가
실제로 expert collapse 를 탈출시키는지 toy regime 에서 falsifier-PASS 가능한지.

## 2. 방법

E2 (`CORE/DECODER/e2_corpus_balance_collapse.hexa`, PR #1279 🟢) verbatim base:

- E=4 expert · V=8 vocab · d=6 hidden · 6 cluster · top-1 hard routing
- corpus = SKEWED (cluster 0 = 20× over-rep, E2 Scenario B — M4b 실 decode 분포 mirror)
- 600 training step · lr=0.5 · `moe_router.hexa` + `moe_router_bwd.hexa` g61 verbatim

4-cell ablation (cell switch == aux-loss config):

| cell | aux 항목 | 수식 |
|---|---|---|
| **A: none** (baseline) | CE only | `L = L_ce` |
| **B: ent** (H_686 only) | router entropy reg | `L = L_ce − λ_ent · H(p_gate)`, λ_ent=0.1 |
| **C: kl** (H_687 only) | KL-to-uniform output reg | `L = L_ce + λ_kl · KL(softmax(logits) ∥ uniform_V)`, λ_kl=0.1 |
| **D: both** | 둘 다 | `L = L_ce − λ_ent · H(p_gate) + λ_kl · KL(softmax(logits) ∥ uniform_V)` |

각 aux 항의 closed-form gradient 는 harness 주석에 상세 (entropy: `∂(-H)/∂p_e = ln p_e + 1`,
KL: `∂KL/∂logits_j = q_j · (ln q_j + H(q))`). `moe_route_top1_bwd` 의 hard top-1
chain 을 inline unroll 해서 `d_gate` 에 `λ_ent · (ln p_e + 1)` 을 ALL expert slot 에
inject (softmax_bwd 가 jacobian 처리). `d_logits` 에는 KL term 을 V slot 마다 추가.

## 3. 결과 (verbatim run output 핵심 발췌)

```
================================================================
  SUMMARY (4-cell ablation @ SKEWED corpus, E=4 V=8 d=6, 600 step)
================================================================
  HEALTHY_FLOOR = 0.0240306
  | cell                  | LZ_norm  | distinct_e | mean H(gate) | final CE | init CE |
  | none  (baseline)      | 0.0360459 | 4.0        | 0.145866 | 0.00253984 | 2.0796 |
  | ent   (H_686 only)    | 0.0360459 | 4.0        | 1.15225 | 0.0122568 | 2.0796 |
  | kl    (H_687 only)    | 0.0360459 | 4.0        | 0.169797 | 0.00487494 | 2.0796 |
  | both  (H_686+H_687)   | 0.0360459 | 4.0        | 1.18533 | 0.0228222 | 2.0796 |
--- falsifier verdicts ---
  [FAIL] F-ABL-1 BASELINE-COLLAPSE: cell-a distinct_e<2 OR LZ<HEALTHY_FLOOR (sanity)
  [PASS] F-ABL-2 ENT-ESCAPE: cell-b (H_686) distinct_e>=2 AND LZ>HEALTHY_FLOOR
  [PASS] F-ABL-3 KL-ESCAPE: cell-c (H_687) distinct_e>=2 AND LZ>HEALTHY_FLOOR
  [PASS] F-ABL-4 BOTH-ESCAPE: cell-d (both) distinct_e>=2 AND LZ>HEALTHY_FLOOR
  [PASS] F-ABL-5 LEARNED: all 4 cells final CE < init·0.5
  [PASS] F-ABL-6 DETERMINISM: all 4 cells LZ_norm re-run identical (<1e-6)
================================================================
  RESULT: 5 PASS / 1 FAIL
================================================================
```

전체 decoded sequence (모든 4 cell 동일):
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 2 3 4 5
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 2 3 4 5
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 2 3 4 5
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 2 3 4 5
```

각 cluster c → expert e → token id (모든 4 cell 동일):
```
cluster c0 → expert e0 → token 0
cluster c1 → expert e3 → token 1
cluster c2 → expert e3 → token 2
cluster c3 → expert e2 → token 3
cluster c4 → expert e1 → token 4
cluster c5 → expert e0 → token 5
```

## 4. 해석

### 핵심 발견 — TOY-NULL

**4 cell 모두가 byte-identical 한 decode 결과** 를 산출 (`LZ_norm = 0.0360459`).
baseline (cell A) 도 이미 `distinct_experts = 4` 와 identity decode 를 달성해서,
**collapse 자체가 발생하지 않은 regime**. 따라서 H_686/H_687 aux-loss 가 어떤
escape 효과를 가지는지 ablation 으로 discriminate 불가능.

F-ABL-2/3/4 가 "PASS" 인 것은 LZ_norm > HEALTHY_FLOOR 조건 자체는 만족하기 때문
(0.036 > 0.024) — 하지만 baseline 도 정확히 같은 값이므로 **aux-loss 의 marginal
contribution 은 zero**.

### 기계적 검증 (aux gradient 작동 확인)

```
cell-a  none  H(gate) = 0.146 (uniform = 1.386)
cell-b  ent   H(gate) = 1.152 ← H_686 가 router 를 uniform 쪽으로 +1.006 nats 밀어냄 ✓
cell-c  kl    H(gate) = 0.170 (KL 는 output 측에 작용, router 측엔 영향 미미)
cell-d  both  H(gate) = 1.185 ← combined ent+kl ✓
```

H_686 aux gradient 가 closed-form 대로 router gate distribution 을 균등화하는 것
은 명확히 확인됨 (cell A 0.146 → cell B 1.152, 7.9× 증가). KL term 은 expected 대로
output 측에 작용해서 router-H 에 큰 영향 없음.

→ **aux gradient 의 구현은 옳다. 다만 toy regime 의 inductive bias (M init pattern
`s%2 sign-flip + s%3·0.015 + s%5·0.01` + CE convergence 압도) 가 너무 강해서
SGD 가 동일한 minimum 으로 수렴**.

### 왜 toy 가 collapse 안 하는가

- E=4 expert · V=8 token · 6 cluster — cluster 6 > expert 4 이므로 일부 expert 는
  여러 cluster 를 처리하지만, identity decode (cluster c → token c) 가 이미 충분히
  쉬운 mapping. 600 step 학습이 overtrain regime.
- M4b production (V=151643 · d=64 · E=2 · 200 step) 의 collapse 는 step-deficit + V
  large + E=2 winner-take-all + corpus diversity 가 모두 합쳐진 regime — toy 규모
  에서 동일 dynamics 발생 안 함 (memory `feedback_toy_scale_transfer`).

## 5. 4-cell 결과 표

| cell | LZ_norm | distinct_experts | mean H(gate) | final CE | toy verdict |
|---|---|---|---|---|---|
| **A: none** (baseline) | 0.0360459 | 4 / 4 | 0.146 | 0.00254 | collapse 미발생 |
| **B: ent** (H_686 only) | 0.0360459 | 4 / 4 | **1.152** | 0.0123 | aux 작동 OK / decode 영향 0 |
| **C: kl** (H_687 only) | 0.0360459 | 4 / 4 | 0.170 | 0.00487 | aux 작동 OK / decode 영향 0 |
| **D: both** | 0.0360459 | 4 / 4 | **1.185** | 0.0228 | additive H(gate), decode 영향 0 |

- baseline collapse 확인? **NO** (toy regime 미재현)
- H_686 toy escape? **INDETERMINATE** (collapse 가 없어 escape 가 vacuous)
- H_687 toy escape? **INDETERMINATE** (동일)
- combined effect? **anti-synergy 형식적** (LZ_d ≤ LZ_b = LZ_c — 4 cell 모두 동일 minimum)

## 6. 결론 + 후속

### toy-scale 결론

**INDETERMINATE — neither confirms nor refutes production escape.** toy regime
은 H_686/H_687 의 decode 변화를 측정할 수 있는 진단판이 아님. aux gradient 의
mechanistic correctness 는 H(gate) 변화로 확인.

### 본선 fire 권장

UNIVERSE H_686/H_687 의 production-scale fire 가 closure 의 유일한 path.
**recommended config**:

- M4 MoE-fresh 본선의 aux-loss 통합: `L_total = L_ce + λ_kl · KL(p_out ∥ u_V) − λ_ent · H(p_gate)`
- λ_ent = 0.1, λ_kl = 0.1 default — production 에서 sweep 필요 (별 H)
- ablation: aux-on vs aux-off (cell-D vs cell-A 의 production equivalent)
- V=151643, d=64, E=2 또는 E=4, n_steps ≥ 1 epoch (≥ 151643 token 제시) — `dec_undertrain`
  discovery 가 step-deficit 을 collapse driver 로 지정한 것에 맞추어

### toy → production 미보장 명시

memory `feedback_toy_scale_transfer` 한대로 — toy ($0·small-n·V=8) 의 PASS/FAIL
이 production 으로 자동 transfer 안 됨. 본 ablation 의 INDETERMINATE 은 **toy
가 production 의 false-negative 일 수 있다는 신호** — H_686/H_687 가 production
에서 작동할 수도 안 할 수도 있고, toy 만으로 결론 불가능.

## 7. honest C3

- C3-1: toy regime 의 M init pattern (E2 verbatim deterministic init) 이 우연히
  4 expert 모두에 reasonable weight 부여해서 baseline 이 escape 했을 가능성.
  random init 을 여러 seed 로 swept 하면 일부 seed 에서 collapse 가 발생할 수 있음
  — 본 ablation 은 1 seed (E2 verbatim) 만 검증.
- C3-2: λ_ent = λ_kl = 0.1 이 toy 의 CE magnitude 대비 너무 작아 압도된 가능성.
  λ ∈ {1.0, 10.0} sweep 이 미실시.
- C3-3: 600 step 이 overtrain — 20 step under-trained regime 도 확인했으나 거기서도
  4 cell 동일 결과 (HEALTHY_FLOOR 0.024 모두 충족 · run-1 에서 확인). step-axis
  full sweep 미실시.
- C3-4: SKEWED 의 20× multiplicity 는 corpus-level skew 일 뿐 router-level
  collapse 와 직교. M4b 의 production collapse 는 router-level (E=2 winner-take-all
  + step deficit). toy 의 E=4 + non-deficit 은 본질적으로 다른 regime.

## 8. 양방향 sibling

- ⇄ [UNIVERSE/H_686 router entropy reg](../../UNIVERSE/H_686_router_entropy_regularization.md) — 본 ablation 의 토이 검증 대상 #1
- ⇄ [UNIVERSE/H_687 KL-to-uniform output reg](../../UNIVERSE/H_687_kl_to_uniform_output_reg.md) — 본 ablation 의 토이 검증 대상 #2
- ⇄ [E2 corpus-balance collapse](./E2_CORPUS_BALANCE_COLLAPSE.md) — 본 harness 의 base recipe (verbatim 재사용)
- ⇄ [D1 LZ76 collapse proxy](./D1_LZ76_COLLAPSE_PROXY.md) — `lz_norm` 측정자 출처
- ⇄ [.discoveries/decoder_collapse_undertrain.tape](../../.discoveries/decoder_collapse_undertrain.tape) — `dec_undertrain` 이 collapse driver 라는 prior

## 9. raw run output 전체

전체 stdout 은 `CORE/DECODER/state/h686_h687_ablation_2026_05_29/run.out` 에 보관.
