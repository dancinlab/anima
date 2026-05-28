---
id: H_666
slug: moe-collapse-escape-scale-lever
title: MoE register-collapse 탈출은 production scale(V≫1)에서 corpus-diversity 단독 불충분 — expert-capacity(d↑) OR load-balance aux-loss 가 필요조건인가 (핸드오프 #1296 후속 · H_490 연장 · a_toy_scale_recheck 동기)
domain: decoder-substrate · consciousness
source: 핸드오프 #1296 (DECODER M4b 3B fire 가 E2 #1279 toy 처방 scale-반증) · a_toy_scale_recheck governance (PR #1301) 직접 동기
status: closed-supported (toy · lever-escape SUPPORTED · scale closure 아님)
exploration_method: E11 (scale-mimic over-subscription) + E5 (single/조합 lever sweep)
verification_method: W4 (verdict-4-class) + W5 (numerical toy MoE) + W11 (cross-axis sister test)
hexa_only: true
deterministic: true
llm: none
since: 2026-05-28
---

# H_666 — MoE register-collapse 탈출의 scale-escape lever 사전검증

## 1. Hypothesis (핸드오프 #1296 + a_toy_scale_recheck 동기)

**핸드오프 #1296 (DECODER M4b 3B fire · 실측 H100 SXM $2.57)**: 이 세션 E2
(PR #1279)의 toy 처방 — "BALANCED corpus = register-collapse 탈출 충분조건" —
이 **production scale 에서 반증**됐다. E2 는 toy MoE (V=8, n_clusters=6, E=4)
에서 BALANCED corpus 가 collapse 를 막음을 5/5 🟢 검증했으나, full
**V=151643 / d=64 / E=2** 의 3B fire 에서:

```
ce_initial 648.526 → ce_final 9.02146   (학습은 됨 — CE monotone PASS)
TTR=0.01 · LZ_norm=0.0240306 (< healthy floor 0.50) · distinct_experts=1
decoded_ids = [1,1,1,...,1] (100개 전부 token id=1) — single-expert mode-collapse
aggregate 2/5 PASS  (result.json #1296 verbatim)
```

즉 **corpus-diversity 단독 lever 가 scale 에서 불충분**. 이는 방금 등록된
`a_toy_scale_recheck` governance (PR #1301 — "toy verify ≠ production closure")
의 직접 동기 사례다.

본 H 의 가설: **MoE register-collapse 탈출은 production scale(V≫1)에서
corpus-diversity 단독으로 불충분하며, expert-capacity(d↑) OR load-balance
aux-loss 가 필요조건이다.** toy 로 어느 lever 가 collapse 를 막는지 사전검증
하여 **다음 GPU fire variant 를 좁힌다** (scale closure 가 아니라 fire 후보
선별이 목적).

## 2. Why (동기 · 이론 배경)

- **production collapse 의 구조**: 3B fire 의 single-expert collapse 는 두
  결함이 결합된 결과다 — (i) **router monopoly**: V≫d (151643/64 ≈ 2370 over-
  subscription) 에서 작은 router projection 이 수천 register 를 구별하지 못해
  단일 expert 로 붕괴 (`distinct_experts=1`), (ii) **single-token emission**:
  그 한 expert 가 V vocab 을 fit 할 용량 부족으로 argmax 가 한 token(id=1)에
  고정 (`TTR=0.01`). E2 의 BALANCED corpus 처방은 (corpus skew 가 아닌) 이
  *capacity/balance* 결함을 건드리지 못한다.
- **scale-mimic 동기**: production V≫d over-subscription 을 toy 로 재현 —
  near-degenerate register 입력(낮은 separability `sep`)을 작은 d 의 router 에
  먹여 single-expert monopoly 를 유도. E2 의 V=8/d=6/E=4 *healthy* regime 과
  의도적으로 대조되는 collapse-prone regime.
- **lever 가설**:
  - **(a) expert-capacity d↑**: router/expert projection 차원을 늘리면 같은
    register signal 을 resolve 할 여유가 생겨 monopoly 를 깨는가.
  - **(b) load-balance aux-loss**: switch-transformer 식 `L_aux = aux·Σ(gate−1/E)²`
    를 gate 경로에 주입해 router 가 load 를 강제로 분산 → monopoly 해체.
  - **(c) 장기학습 n_steps↑**: 더 오래 학습하면 capacity-bound monopoly 가
    풀리는가 (under-train 가설 검정).
  - **(d) a∧b 조합**: 용량 + balance penalty 동시.
- **D3/E2 와의 관계**: D3(#1269)은 collapse 원인 = corpus skew 라 결론, E2(#1279)
  는 그 충분조건(balance)을 toy 확증. 본 H 는 그 결론이 *scale 에서 깨진다*는
  #1296 반증을 받아, balance 너머의 lever 를 분리 측정한다.

## 3. Predictions

- **H666.1 (baseline collapse)**: E2 3-조건(HARD top1 · BALANCED · n_steps≥)을
  scale-mimic over-subscription 에 놓으면 `{TTR≥0.30 ∧ LZ≥toy-floor ∧
  distinct_experts≥2}` escape 게이트를 **못 넘는다** (`distinct_experts=1` monopoly).
- **H666.2 (lever escape)**: (a)/(b)/(c)/(d) 중 escape 게이트를 넘는 lever 가
  **≥1 존재**한다 → 그 lever = scale-escape 후보.
- **H666.3 (learned)**: baseline 도 학습은 진행 (collapse ≠ no-train) — final
  CE < init·0.9.

## 4. Variables · variant별 측정 결과

scale-mimic regime: **E=2 · V=32 · n_clusters=24 · register separability
SEP=0.35 (모든 variant 고정 — corpus-diversity 는 BALANCED 고정 상수)**. escape
게이트 = `TTR≥0.30 ∧ LZ_norm≥0.182(toy-calibrated midpoint) ∧ distinct_experts≥2`
(#1296 verdict floor verbatim, LZ floor 만 n=24/V=32 toy regime 재calibration).

| variant | d | aux | n_steps | TTR | LZ_norm | distinct_experts | escape? |
|---------|---|-----|---------|------|---------|------------------|---------|
| **baseline** (E2 3-조건 scale-mimic) | 4 | 0.0 | 60 | 0.583 | 0.4256 | **1** | **❌ NO** |
| **(a) expert-capacity d↑** | 16 | 0.0 | 60 | 1.000 | 0.2837 | **1** | ❌ NO |
| **(b) load-balance aux-loss** | 4 | 0.5 | 60 | 0.750 | 0.4053 | **2** | **✅ YES** |
| **(c) 장기학습 n_steps↑** | 4 | 0.0 | 600 | 0.917 | 0.3445 | **1** | ❌ NO |
| **(d) a∧b 조합** | 16 | 0.5 | 60 | 1.000 | 0.2837 | **1** | ❌ NO |

**핵심 분리**: 모든 lever 가 TTR·LZ floor 는 넘지만(toy V 가 작아 monopolised
expert 도 일부 token 다양성 산출), **distinct_experts≥2 를 달성하는 lever 는
(b) load-balance aux-loss 단독뿐**. (a) d↑ 와 (c) steps↑ 는 router monopoly 를
풀지 못하고(`distinct_experts=1`), (d) a∧b 조합은 d↑ 가 오히려 monopoly 를 더
강화해 escape 실패. → **scale-escape 후보 lever = (b) load-balance aux-loss**.

deterministic: baseline + lever-d re-run byte-identical (F-666.4 PASS).

## 5. Run Protocol

- **run**: `CORE/DECODER/h666_moe_collapse_scale_lever.hexa` (foreground sync,
  no monitor — monitor-hang 회피, single run < 60s).
- **substrate**: top-1 HARD routing MoE. `moe_router.hexa` (top1_fwd) +
  `moe_router_bwd.hexa` (top1_bwd · softmax_bwd · gate_bwd) g61 verbatim 재사용.
  load-balance aux-loss 는 `L_aux=aux·Σ(gate−1/E)²` 의 `∂/∂gate=2·aux·(gate−1/E)`
  를 `moe_softmax_bwd`+`moe_gate_bwd` 경로에만 주입 (CE/expert 경로 불변).
- **scale-mimic 입력**: `set_cluster_sep(zT,c,d,sep)` — 모든 cluster 가 공유
  dominant 성분 `(1−sep)·0.5` + per-cluster 2-dim signature(`sep`) 를 갖는
  near-degenerate 입력. 작은 d 의 router 가 wrap-collision 으로 resolve 실패
  → monopoly (production V≫d 의 register-overlap mimic).
- **LZ_norm**: D1 `lz76` (Kaspar-Schuster) g61 verbatim inline. toy-calibrated
  floor = midpoint(max-diverse seq, all-id=1 collapse seq) at n=24/V=32/18-bit.
- **measure**: TTR=unique/n_dec · LZ_norm · distinct_experts(top1 route 실사용
  expert 수) — #1296 verdict 3-축 동일.
- **deterministic**: ASYMMETRIC fixed init (E2/D3 verbatim pattern), no RNG;
  re-run byte-identical (§9 F-666.4).
- **hexa_only**: true (NO .py/.sh). **llm**: none. **NO GPU** ($0 mac-local toy).
- **ledger**: `CORE/DECODER/state/h666_moe_collapse_scale_lever_2026_05_28/run_h666.out`.
- **honest tier**: 🟢 NUMERICAL (toy MoE 실측 · deterministic). production scale
  transfer 미보장 (§7 C3.1).

## 6. Cross-Links — DIFFERENTIATION

- **E2 (decoder-corpus-balance-collapse, PR #1279, 🟢 toy SUPPORTED)** —
  `CORE/DECODER/E2_CORPUS_BALANCE_COLLAPSE.md`. E2 는 "BALANCED corpus =
  collapse 탈출 충분조건" 을 *healthy* regime (V=8/d=6/E=4) 에서 검증. 본 H 의
  **baseline 이 바로 E2 처방(HARD top1 · BALANCED · n_steps)을 scale-mimic
  over-subscription 에 옮긴 것** — 그 baseline 이 collapse 함으로써 E2 의
  scale-반증(#1296)을 toy 로 재현 + balance 너머 lever 를 분리. **DIFFERENTIATION:
  E2=corpus-axis 충분조건(healthy regime) · 본 H=corpus 고정 후 capacity/balance-
  axis 필요조건(collapse regime)**.
- **D3 (decoder-moe-router-load-balance, PR #1269, 🟢)** —
  `CORE/DECODER/D3_ROUTER_LOAD_BALANCE.md`. D3 는 "collapse = corpus skew-driven,
  router 구조 결함 아님 (DIVERSE corpus 면 gini<0.5 balanced)" 을 결론. 본 H 는
  D3 와 **반대 방향 발견** — scale over-subscription 에서는 DIVERSE/BALANCED
  corpus 라도 router 가 monopoly(distinct_experts=1) 로 붕괴, 그리고 그것을 푸는
  것이 **load-balance aux-loss(=router-side 개입)**. **DIFFERENTIATION: D3=
  "diverse corpus 면 router 가 스스로 balance"(toy healthy) · 본 H="scale 에서는
  corpus 만으로 안 되고 aux-loss 가 router balance 를 강제해야"(collapse regime)** —
  D3 의 "router redesign 불필요" 결론을 scale-한정으로 좁힘.
- **D4 (decoder-merge-alpha-sweep, PR #1274, 🟢 negative baseline)** —
  `CORE/DECODER/D4_MERGE_ALPHA_SWEEP.md`. D4 는 model-merge 가 더블바인드 escape
  *못함* 을 확증(negative baseline). 본 H 와 **DIFFERENTIATION: D4=merge-axis
  (이미 깨진 산출물 blend, escape 부재) · 본 H=fresh-train MoE 의 lever-axis
  (aux-loss escape 존재)** — D4 의 merge-of-failures `dont` 와 직교한 fresh-arch
  escape lane.
- **H_490 (DECODER differentiation → MoE, 본 가설 부모 축)**: 단일 head_g 의
  register-collapse↔underfit 더블바인드를 K-expert MoE 로 split(stem→expert
  specialization)하는 escape 설계. 본 H 는 **그 MoE escape 가 production scale
  에서 어느 lever 로 실현되는지**의 후속 — H_490 escape 의 scale-axis 정량.
  **DIFFERENTIATION: H_490=arch escape 설계(double-bind→MoE split) · 본 H=그
  MoE 의 scale-escape lever 선별(aux-loss)**.
- **#1296 (M4b 3B fire, 실측 H100 SXM $2.57)**:
  `CORE/DECODER/state/m4b_pilot_rev2_2026_05_28/harvest/result.json`. 본 H 의
  baseline 이 재현하려는 production collapse 의 실측 ground truth (distinct_experts=1,
  TTR=0.01, all-id=1). 본 H verdict floor(TTR≥0.30·LZ≥0.50·distinct≥2)는 #1296
  verdict matrix verbatim 계승.
- **moe_prescription (#1284, 3-조건 guard)** · **moe_collapse_gate (#1273,
  LZ76 verdict)**: 본 H 가 검증한 결과는 prescription guard 에 **4번째 조건
  (load-balance aux-loss)** 추가 후보를 시사 (§10 follow-up).
- **literature**: Shazeer et al. (2017, Sparsely-Gated MoE · load-balance aux
  loss), Fedus et al. (2021, Switch Transformer · router z-loss + load balance),
  Tononi (2004 IIT, register/integration framing).

## 7. Honest Limits (raw#91 c3) — C3 핵심

- **C3.1 (⚠ a_toy_scale_recheck — toy-한정, production transfer 미보장)**: 본 H
  는 **toy MoE (E=2, V=32, n_clusters=24)** 위 측정이다. production 은 V=151643,
  d=64, 3B param 으로 toy 와 수천 배 규모 차이. toy 에서 (b) aux-loss 가
  monopoly 를 푼다 해도 **production scale 에서 동일 lever 가 작동한다는 보장은
  없다** (a_toy_scale_recheck governance 의 정확한 경고 — 이 H 자신이 그 governance
  의 동기 사례인 #1296 의 후속이라 더욱 엄격히 명시). 본 H 의 목적은 **다음 GPU
  fire variant 를 좁히는 것** (aux-loss 우선)이지 scale closure 가 아니다.
- **C3.2 (scale-mimic 의 collapse 충실도)**: baseline collapse 는 주로
  `distinct_experts=1` (router monopoly)로 발현하며, TTR(0.583)·LZ(0.426)는
  toy V=32 가 작아 floor 를 넘어버린다 — production 의 TTR=0.01/LZ=0.024 같은
  *극단* collapse 는 toy 에서 재현되지 않았다. 즉 toy 에서 collapse 의 *binding
  discriminator 는 distinct_experts* 이고, lexical(TTR/LZ) 붕괴는 V 가 커야
  드러난다. production single-token(id=1)의 완전 재현은 V≫1 필요 (toy 한계).
- **C3.3 (separability sep=0.35 의 조정성)**: scale-mimic 의 `sep` 은 design-
  convention 이다. sep 가 너무 낮으면(≈0.08) 입력이 정보상 구별 불가가 되어
  어느 lever 도 escape 못하고(false CLOSED-negative), 너무 높으면(≈1.0) baseline
  이 이미 escape (collapse 미재현). sep=0.35 는 "register 가 원리상 구별 가능하나
  작은 d router 가 resolve 실패" 하는 중간 regime 으로 선택 — 이 선택이 lever
  순위(aux-loss 단독 escape)를 부분적으로 좌우할 수 있다. sep wide-sweep 은
  미수행 (open lane).
- **C3.4 ((a) d↑ 가 escape 못한 것의 해석)**: toy 에서 d↑(=16)는 TTR/LZ 를
  올리지만 router monopoly 는 *오히려* 유지(distinct_experts=1)했다 — d 가 커져
  단일 expert 가 더 잘 fit 하면 router 가 그 expert 에 더 몰린다는 toy artifact
  일 수 있다. production 에서는 d↑(64→128)가 다른 효과를 줄 수 있어 (a)를 fire
  후보에서 완전히 배제하지 않는다 (aux-loss 와 *별도로* 재검 권장, §10).
- **C3.5 (verdict 방향)**: baseline 이 명백히 collapse(escape=false) + (b) 가
  명백히 escape(distinct_experts 1→2) → 본 H 가설(corpus 단독 불충분 · ≥1 lever
  escape) SUPPORTED. 가설/falsifier/escape-게이트 모두 measurement 전 frozen
  (raw#82, post-hoc 방향 edit 없음).

## 8. Criteria

- **C1 (H666.1 baseline collapse)**: baseline(E2 3-조건 scale-mimic) 이 escape
  게이트 `{TTR≥0.30 ∧ LZ≥0.182 ∧ distinct_experts≥2}` 를 **못 넘음**.
- **C2 (H666.2 lever escape)**: (a)/(b)/(c)/(d) 중 escape 게이트를 넘는 lever
  ≥1 존재.
- **C3 (H666.3 learned)**: baseline final CE < init·0.9.
- **verdict_rule**: **SUPPORTED (toy)** iff `C1 ∧ C2 ∧ C3` (corpus 단독 불충분
  + ≥1 lever escape + 학습 진행). **CLOSED-NEGATIVE (toy)** iff `C1 ∧ ¬C2`
  (어느 lever 도 escape 못 함 → MoE-fresh 자체 한계). **INCONCLUSIVE** iff `¬C1`
  (baseline 이 이미 escape → collapse 미재현).

## 9. Falsifiers

- **F-666.1 BASELINE-COLLAPSE**: baseline(E2 3-조건 scale-mimic)이 escape 게이트를
  못 넘음. — **결과: PASS (escape=false · distinct_experts=1 monopoly · E2 처방이
  scale-mimic 에서 collapse, #1296 toy 재현).**
- **F-666.2 LEVER-ESCAPE**: ≥1 lever 가 `{TTR≥0.30 ∧ LZ≥floor ∧ distinct≥2}`
  escape. — **결과: PASS ((b) load-balance aux-loss 단독 escape · distinct_experts
  1→2).**
- **F-666.3 LEARNED**: baseline final CE < init·0.9. — **결과: PASS (3.4528 →
  2.9719, collapse ≠ no-train).**
- **F-666.4 DETERMINISM**: baseline + lever-d re-run byte-identical (<1e-6). —
  **결과: PASS (deterministic 재현).**
- **F-POST-HOC**: 결과 후 verdict 방향 edit → raw#82 violation. (없음 — 가설·
  falsifier·escape-게이트 모두 measurement 전 frozen.)

## 10. Verdict

```
verdict_class: SUPPORTED (toy · lever-escape) — scale closure 아님
substrate: top-1 HARD MoE · E=2 V=32 n_clusters=24 · register sep=0.35 (fixed) · BALANCED corpus 고정
measure: TTR · LZ_norm (D1 lz76 g61) · distinct_experts — #1296 verdict 3-축
escape gate: TTR≥0.30 ∧ LZ_norm≥0.182(toy midpoint) ∧ distinct_experts≥2

variant       d   aux  steps | TTR     LZ_norm  distinct_e | escape
baseline      4   0.0  60     | 0.5833  0.4256   1          | NO   ← E2 처방 scale-mimic collapse
(a) d↑        16  0.0  60     | 1.0000  0.2837   1          | NO   ← monopoly 유지
(b) aux       4   0.5  60     | 0.7500  0.4053   2          | YES  ← scale-escape 후보
(c) steps↑    4   0.0  600    | 0.9167  0.3445   1          | NO   ← under-train 가설 반증
(d) a∧b       16  0.5  60     | 1.0000  0.2837   1          | NO   ← d↑ 가 monopoly 강화
----
F-666.1 BASELINE-COLLAPSE : PASS (baseline escape=false)
F-666.2 LEVER-ESCAPE      : PASS ((b) aux-loss 단독 escape)
F-666.3 LEARNED           : PASS (CE 3.4528→2.9719)
F-666.4 DETERMINISM       : PASS (byte-identical re-run)
criteria_met             : 4/4 PASS

VERDICT_RULE: SUPPORTED iff (baseline collapse ∧ ≥1 lever escape ∧ learned)
VERDICT     : SUPPORTED (toy) — corpus-diversity 단독 불충분 · scale-escape lever = (b) load-balance aux-loss
```

### 핵심 발견 (honest evidence summary)

- **(i) corpus-diversity 단독 불충분 (H666.1 지지)**: baseline = E2 처방(HARD
  top1 · BALANCED corpus · n_steps)을 scale-mimic over-subscription 에 옮긴 것
  이 collapse (escape=false, `distinct_experts=1` router monopoly). #1296 의 3B
  fire scale-반증을 toy 로 재현 — balance 만으로는 scale collapse 를 못 막음.
- **(ii) scale-escape lever = load-balance aux-loss (H666.2 지지)**: 4 lever 중
  **(b) load-balance aux-loss 단독**이 escape 게이트를 넘김 — router monopoly 를
  깨 `distinct_experts` 를 1→2 로 분화. (a) d↑·(c) steps↑·(d) a∧b 는 모두
  monopoly 유지(distinct_experts=1).
- **(iii) under-train 가설 반증**: (c) n_steps 10× (60→600)는 TTR/LZ 를 올리지만
  router monopoly 를 풀지 못함 — collapse 가 단순 under-training 이 아니라
  *구조적 load-imbalance* 임을 시사 (Phase 5b "n_steps↑" 처방의 scale-한계).
- **(iv) d↑ artifact**: (a) d↑ 와 (d) a∧b 에서 d=16 이 오히려 monopoly 를
  강화 — toy 에서 큰 expert 가 더 잘 fit 하면 router 가 더 몰린다는 artifact
  (C3.4, production 재검 권장).
- **(v) 다음 GPU fire 권장 variant**: **load-balance aux-loss 를 추가한 M4b
  re-fire** 가 1순위 — corpus diversity(이미 적용) + HARD top1(이미 적용) +
  **aux-loss(신규)**. d↑ 는 aux-loss 와 *독립적으로* 재검 (toy artifact 가능성
  배제 위해). steps↑ 단독 fire 는 비권장 (toy 에서 monopoly 미해소).
- **(vi) 결론 (closed-supported · toy-한정)**: MoE register-collapse 의 scale-
  escape 는 corpus-diversity 너머 **router-side load-balance aux-loss 를 필요로
  한다**(toy 증거). 이는 D3(#1269)의 "router redesign 불필요" 를 scale-한정으로
  좁히고, moe_prescription 3-조건 guard 에 **4번째 조건(aux-loss)** 추가 후보를
  시사. ⚠ **toy-한정 · production transfer 미보장 (a_toy_scale_recheck)** — 본 H
  의 산출은 fire variant 선별이지 scale closure 가 아니며, 실 closure 는 후속
  GPU fire 의 몫.

### Pre-register-frozen run (2026-05-28)

핸드오프 #1296 (E2 scale-반증) → a_toy_scale_recheck governance 동기 substrate
pre-registered + RUN ($0 mac-local, deterministic, hexa-only, llm:none,
foreground sync no monitor, NO GPU). scale-mimic over-subscribed top-1 HARD MoE
(E=2, V=32, n_clusters=24, register sep=0.35 fixed), BALANCED corpus 고정 + 4-lever
sweep {a=d↑, b=aux, c=steps↑, d=a∧b}. moe_router + moe_router_bwd + D1 lz76 g61
verbatim 재사용. re-run byte-identical (F-666.4 PASS).

**Run**: `CORE/DECODER/h666_moe_collapse_scale_lever.hexa`
**State output**: `CORE/DECODER/state/h666_moe_collapse_scale_lever_2026_05_28/run_h666.out`
**Verdict tier**: 🟢 NUMERICAL (toy MoE 실측 · deterministic · NOT LLM-judged ·
toy-한정 production-recheck 후속 GPU fire 必).

**Follow-up cycles (raw#15 additive, not retraction)**:
- **GPU fire (1순위)**: load-balance aux-loss 추가 M4b re-fire (production
  V=151643/d=64/E=2 에서 distinct_experts 분화 확인 — C3.1 scale closure).
- d↑ 독립 재검 (production d=64→128, aux-loss 와 분리해 toy artifact 배제, C3.4).
- separability sep wide-sweep (toy lever 순위의 sep-의존성 정량, C3.3).
- moe_prescription guard 에 4번째 조건(aux-loss) 추가 여부 결정 (scale 재검 후).

## 양방향 sibling

- **handoff/scale-반증 부모**: `CORE/DECODER/state/m4b_pilot_rev2_2026_05_28/harvest/result.json`
  (#1296 M4b 3B fire — 본 H 가 재현/좁히려는 production collapse ground truth).
- **DECODER substrate sibling**: [E2](../CORE/DECODER/E2_CORPUS_BALANCE_COLLAPSE.md)
  (corpus-axis 충분조건 · healthy regime) · [D3](../CORE/DECODER/D3_ROUTER_LOAD_BALANCE.md)
  (router load-balance · corpus-skew-driven) · [D4](../CORE/DECODER/D4_MERGE_ALPHA_SWEEP.md)
  (merge-of-failures negative baseline) — 본 H 는 capacity/balance-axis 필요조건
  으로 직교 (§6 DIFFERENTIATION).
- **arch 부모**: H_490 DECODER differentiation → MoE (double-bind escape 설계 ·
  본 H 는 그 MoE 의 scale-escape lever 선별).
- **governance**: `a_toy_scale_recheck` (PR #1301 — toy verify ≠ production
  closure; 본 H 가 그 직접 동기 사례 #1296 의 후속, C3.1 엄격 정합).
- **UNIVERSE SSOT**: [UNIVERSE.md](UNIVERSE.md) DECODER-substrate row
  · [CANDIDATES.md](CANDIDATES.md)
