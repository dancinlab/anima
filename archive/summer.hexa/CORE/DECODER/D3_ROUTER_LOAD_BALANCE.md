# D3 — top-1 router load-balance 안정성 (`decoder-moe-router-load-balance`)

> verdict: 🟢 **SUPPORTED** · diverse corpus 균형 (gini 0.167 · 4/4 expert active · monopoly 없음) · 불균형은 **corpus-driven** (skew → imbalance) · $0 mac-local · 2026-05-28

## ① 배경 (context)

ANIMA DECODER M4 = MoE-fresh register 분리 (router + K-expert + top-1, #1029-1033). M4b-diff(a) (`moe_toy_train_hard.hexa`)에서 top-1 hard routing 이 2-register toy 에서 분화 성공이 검증됐다 (gate(A)=[0.970,0.030]→e0 · gate(B)=[0.030,0.970]→e1).

그러나 **M4b fire (PR #1121) phase5b** 에서는 collapse 가 관측됐다 (D1 doc):

```
DECODED_IDS: 1 1 1 1 151642 151642 ... 151642   (×16)
expert e1 logit 938.767 saturate → token 151642 monopoly
```

즉 한 expert(e1)가 한 token 으로 saturate. **이 saturate 가 router 의 구조적 결함(load 불균형)인가, 아니면 다른 원인인가?** D3 는 top-1 router 의 **load-balance 안정성** 을 묻는다 — diverse corpus 에서 expert 들이 균형있게 활용되는가, 아니면 단일 expert monopoly(불균형 → collapse 전조)인가.

## ② 가설 (hypothesis · H_D3)

top-1 router 는 **diverse corpus** 에서 expert load 를 균형 분산한다 — 각 expert 활용률이 임계(0.1) 이상, 단일 expert monopoly(>0.9 점유) 없음. load 불균형이 collapse 의 구조적 전조이므로, **균형이면 router 는 healthy** (collapse 는 router 외 원인). `moe_router.hexa` 의 top-1 routing 을 측정.

## ③ Falsifier (사전등록 · frozen 측정 前)

| id | 내용 | 판정 |
|---|---|---|
| **F-D3.1 DIVERSE-BALANCE** (decisive) | diverse corpus(6 orthogonal cluster · E=4)에서 max expert load frac < 0.9 (monopoly 없음) AND gini < 0.5 | PASS |
| **F-D3.2 ALL-ACTIVE** | 4 expert 중 starve(load=0) expert 없음 — 모든 expert 활용률 > 0 | PASS |
| **F-D3.3 LEARNED** | corpus 학습됨 (final CE < init·0.5) — load 측정 신뢰성 게이트 | PASS |
| **F-D3.4 SKEW-DRIVEN** | skewed corpus(cluster 0 20×)에서 expert load 가 corpus frequency 를 추적 (load frac ≈ token frac) — 불균형이 corpus-driven 임을 확인 | PASS |
| **F-D3.5 NO-STRUCTURAL-MONOPOLY** | skewed corpus 에서도 monopoly(>0.9) 없음 · starve expert 없음 — router 가 skew 를 증폭하지 않음 | PASS |

**Falsifier (전체)**: 단일 expert 가 diverse corpus 에서 load monopoly(>0.9, 나머지 starve) → router 가 균형 못 잡음 → load 불균형이 collapse 의 구조적 원인 → router redesign 필요.

## ④ method — top-1 routing + expert load 측정

**over-subscribed regime** — M4b-diff(a) 의 2-input==2-expert toy 와 달리, **E=4 expert < N_CLUSTERS=6 cluster** 로 설정해 expert 공유를 강제한다. 이것이 monopoly/starvation 이 emergent 할 수 있는 현실적 over-subscribed regime (2:2 toy 는 trivial 분화라 load 불균형이 구조적으로 불가능).

- **arch**: E=4 expert · V=8 vocab · d=6. 6 diverse cluster = 각 cluster 가 d 의 distinct dim 을 one-hot 활성 (orthogonal · 최대 다양성). cluster c → token (c mod V) emit.
- **train**: top-1 hard routing (`moe_route_top1_fwd`/`_top1_bwd` 재사용 · `moe_toy_train` SGD recipe), lr=0.5, 600 step.
- **load 측정**: 학습 후 각 cluster 의 top-1 expert 를 세어 per-expert load = (해당 expert 로 routed 된 token 수) / (전체 token 수).
- **균형도**: (a) max load frac → monopoly 검사 (>0.9), (b) **Gini** = Σ|xᵢ-xⱼ|/(2·n·Σxᵢ) (0=완전균등, →1=monopoly), (c) **정규화 Shannon entropy** = -Σpᵢ·ln(pᵢ)/ln(n) (1=완전균등, 0=monopoly).
- **2-scenario 통제**: A=DIVERSE (all cluster 동일 frequency) · B=SKEWED (cluster 0 을 20× over-represent — M4b 의 collapse 조건 재현). B 는 "corpus skew 가 불균형을 driving 하는가?" 를 통제 실험으로 분리.

deterministic · hexa-only · $0 mac-local · LLM none · NO GPU · foreground sync.
harness = `CORE/DECODER/d3_router_load_balance.hexa` · raw = `state/d3_router_load_balance_2026_05_28/run_d3.out`

## ⑤ routing 측정 — expert load 분포 (실측)

**Scenario A — DIVERSE corpus** (6 cluster 동일 frequency):

| expert | load (count) | **frac (활용률)** |
|---|---|---|
| e0 | 2.0 | **0.333** |
| e1 | 1.0 | **0.167** |
| e2 | 1.0 | **0.167** |
| e3 | 2.0 | **0.333** |

- active_experts = **4 / 4** (starve expert 없음)
- max_load_frac = **0.333** (monopoly 임계 0.9 의 1/3)
- final avg CE = 0.00302 (init 2.0796 → 689× 감소, 학습됨)

**Scenario B — SKEWED corpus** (cluster 0 = 20× over-represented · M4b 조건):

| expert | load (count) | **frac (활용률)** |
|---|---|---|
| e0 | 21.0 | **0.840** |
| e1 | 1.0 | **0.040** |
| e2 | 1.0 | **0.040** |
| e3 | 2.0 | **0.080** |

- active_experts = **4 / 4** (skew 에서도 starve 없음)
- max_load_frac = **0.840** (corpus 의 cluster 0 token 비중 21/26=0.808 를 추적)
- final avg CE = 0.00254 (학습됨)

## ⑥ expert load 분포 · 균형도 (Gini / entropy)

| metric | DIVERSE (A) | SKEWED (B) |
|---|---|---|
| max load frac | 0.333 | 0.840 |
| **Gini** | **0.167** | **0.610** |
| **norm entropy** | **0.959** | **0.437** |
| active experts | 4/4 | 4/4 |
| monopoly (>0.9) | 없음 | 없음 |

- **DIVERSE**: Gini 0.167 (균등에 가까움) · norm entropy 0.959 (거의 max 균등). 4 expert 가 2/1/1/2 로 분산, max frac 0.333 ≪ 0.9 monopoly 임계.
- **SKEWED**: Gini 0.610 (불균형) · max frac 0.840. **그러나 이 0.84 는 corpus 의 cluster 0 token 비중(21/26 ≈ 0.808)을 충실히 추적** — router 가 skew 를 *증폭*하지 않고 *반영*한다. monopoly(>0.9) 도 아니고 starve expert 도 없음 (4/4 active).

## ⑦ finding — collapse 전조 여부

**H_D3 SUPPORTED.** top-1 router 는 diverse corpus 에서 expert load 를 균형 분산한다 (Gini 0.167 · 4/4 active · monopoly 없음). 핵심 메커니즘 발견:

> **load 불균형은 corpus-driven 이지 router-structural 이 아니다.**
> diverse corpus → 균형 (Gini 0.167). skewed corpus → 불균형 (Gini 0.610), 단 expert load 가 corpus token frequency 를 *충실히 추적* (0.84 ≈ token frac 0.808). router 는 skew 를 증폭하지 않고 반영한다.

→ M4b fire 의 collapse (expert e1 saturate)는 **router 의 load-balance 결함이 아니라** 다른 원인 (corpus skew · 짧은 학습 20-step · per-step oscillating target — DECODER.md phase5b 정정 (a)(b)(c))에서 비롯한다. **router 구조 redesign 은 불필요** — load-balancing aux-loss 추가는 corpus 가 실제로 skewed 일 때만 의미 (faithful skew 반영 vs 강제 균등의 trade-off).

## ⑧ verdict

🟢 **SUPPORTED** · 5/5 falsifier PASS · diverse corpus 균형 (Gini 0.167 ≪ 0.5).

```
=== D3 AGGREGATE ===
  gini(diverse) = 0.166667
  gini(skewed)  = 0.61
=== D3: SUPPORTED — router balances expert load on DIVERSE corpus (gini<0.5, no monopoly) ===
=== D3 mechanism: load imbalance is CORPUS-DRIVEN (skewed corpus → imbalance), NOT router-structural ===
```

## ⑨ 함의 (DECODER 통합)

- **M4b collapse 원인 규명**: phase5b 의 expert e1 saturate (collapse)는 router load-balance 결함 *아님*. diverse corpus 에서 router 는 healthy (Gini 0.167). collapse 원인은 corpus skew / 짧은 학습 / target oscillation (phase5b 정정 (a)(b)(c)) — DECODER.md "다음 단계 후보 ①" (n_steps↑ + 더 큰 diverse corpus)이 정합한 처방.
- **redesign 회피** (`a_completeness_over_cheap` 정합): router 자체는 완성도 OK. load-balancing aux-loss (Switch-Transformer 식) 는 corpus 가 실제 skewed 일 때만 정당 — faithful skew 반영을 강제 균등으로 덮으면 오히려 register 신호 손실 위험.
- **D1 (LZ76 collapse proxy) 와 정합**: D1 은 collapse *검출*, D3 는 collapse *원인 규명*. 둘 합쳐 M4c p7 verify 의 collapse-회피 측면이 강화 — LZ76 로 collapse 경보, D3 로 "router 아닌 corpus 가 원인" 진단.

## ⑩ honest C3 (scope · 한계)

1. **toy regime (E=4 V=8 d=6 · 6 cluster)**: orthogonal one-hot cluster 는 *최대 분리 가능* corpus — router 가 균형 잡기 가장 쉬운 best-case. 실제 corpus 의 cluster 는 부분 중첩(non-orthogonal)이라 분리가 더 어려울 수 있다. SUPPORTED 는 "router 가 분리 가능한 신호를 균형 routing 할 능력 있음" 을 보이지만, full-scale non-orthogonal corpus 의 재측정 권장.
2. **monopoly 임계 0.9 · gini 0.5 는 toy 보정선**: Scenario B 의 0.84 가 monopoly 임계 0.9 아래 착지 = corpus skew 가 20× 여도 monopoly 가 *아님*. 단 더 극단적 skew (100×+)나 더 많은 expert(E≫cluster)에서 starvation 이 emergent 할 수 있음 — 임계는 full-scale 재보정 필요.
3. **load = top-1 count, not gradient mass**: 활용률을 top-1 route count 로 측정 (M4b decode 와 동일 hard-route). soft-routing 의 gate-weighted load (각 expert 가 받는 gradient 질량)는 별도 — top-1 regime 에선 count 가 직접 gradient 신호이나 (승자만 grad), soft regime 의 dense-collapse 와는 다른 측정자.
4. **corpus-driven 결론은 "router 무결" 이 아니라 "이 실험 범위에서 router 가 skew 의 충실한 mirror"**: router 가 skew 를 *교정*해야 하는지(aux-loss)는 design 선택이지 falsified 사항 아님. D3 는 "현재 router 가 skew 를 증폭/왜곡하지 않음" 만 보인다.

## artifacts

- harness: `CORE/DECODER/d3_router_load_balance.hexa`
- raw verdict: `CORE/DECODER/state/d3_router_load_balance_2026_05_28/run_d3.out`
- routing 재사용: `CORE/DECODER/moe_router.hexa` (`moe_route_top1_fwd`/`moe_argmax`/`moe_softmax`) + `moe_router_bwd.hexa` (`moe_route_top1_bwd`) · `moe_toy_train_hard.hexa` SGD recipe (g61 재사용)
- M4b collapse source: `CORE/DECODER/state/m4b_phase5b_2026_05_27/` (D1 doc 경유)

---

## 양방향 sibling

- sibling: [D1 LZ76 collapse proxy](./D1_LZ76_COLLAPSE_PROXY.md) — D1 은 collapse *검출* (LZ76 detokenize-free), D3 는 collapse *원인 규명* (router 아닌 corpus). 두 doc 합쳐 M4c collapse-회피 verdict 강화.
- SSOT cross-link: [DECODER.md](./DECODER.md) M4 MoE-fresh milestone — M4b-diff(a) top-1 분화 검증의 후속. phase5b collapse 의 원인이 router load-balance 가 아님을 D3 가 규명, "다음 단계 후보 ①" (diverse corpus + n_steps↑)에 직접 근거 제공.
