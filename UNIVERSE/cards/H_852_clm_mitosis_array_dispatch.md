---
id: H_852
slug: clm-mitosis-array-dispatch
title: scale 축을 expert-COUNT 로 옮기면(MITOSIS-ARRAY DISSOLVE) inter-expert dispatch entropy 의 monopoly-escape 가 칩-수(E)로 scale 하는가 — z(E) 단조 상승 ∧ z(64)−z(4)≥1.0 ∧ 전 expert chip-fit (F-CLM-MONO-ARRAY 사전등록)
domain: clm · moe · mitosis-array · dissolve · dispatch-entropy · expert-count · falsifier
source: CLM/P0_ARCHITECTURE.md §11 (MITOSIS-ARRAY · DISSOLVE) · CLM/CLM.breakthrough.mining.md (depleted-both) · sibling H_847 (F-CLM-MONO 고정 z 임계)
status: CLOSED-NEGATIVE (P-ARRAY 측정 완료 2026-05-30 · E sweep {4,8,16,32,64} × seed{42,43,44} · 사전등록 frozen 임계 미달)
exploration_method: arch redesign (scale 축 model-dim → expert-COUNT reframe · chip-native dispatch entropy)
verification_method: W2 (pre-registered numerical threshold · z 단조성 + z-rise + chip-fit · post-tuning 0)
raw_rank: 9
hexa_only: false
deterministic: false
llm: none
pre_register_frozen: true
frozen_at: 2026-05-30
since: 2026-05-30
sister: CLM/P0_ARCHITECTURE.md §11, UNIVERSE/H_847, .verdicts/852_clm_mitosis_array_dispatch/F-CLM-MONO-ARRAY_prereg.txt
verdict: 🔴 CLOSED-NEGATIVE (E 증가 시 raw dispatch entropy H 는 상승[1.19→3.17 nats] 하나 uniform-null 대비 z 는 급락[+0.53→−7.61] · monotone non-decreasing FAIL · z-rise −8.14 < +1.0 임계 FAIL · 전 expert chip-fit PASS · "scale=expert-count 가 z-척도 상 monopoly-escape 를 scale 시키지 못함", a_paper_negative_ok)
---

# H_852 — CLM MITOSIS-ARRAY dispatch-entropy scaling (DISSOLVE)

## 1. 가설

CLM 의 **측정-타당성 ⊥ AKIDA 온칩** 충돌(H_847 routing-z 가 tiny~small 한정인 근본 이유 · a_scale_honest_scope)을 돌파엔진 **MITOSIS-ARRAY(DISSOLVE)** 가 해소한다 — scale 축을 model-dim 이 아니라 **expert-COUNT** 로 옮기면(각 expert chip-fit ≤1.2M), inter-expert(=inter-chip surrogate) dispatch entropy 의 monopoly-escape 가 **칩 수 E 로 scale** 한다. 사전등록 3조건 동시 PASS 시:

- **DISSOLVE SUPPORTED** — dispatch-entropy z(E) 단조 비감소 ∧ z(64)−z(4)≥1.0 ∧ 전 expert chip-fit
- → SUPPORTED-NUMERICAL · "측정이 chip-native 가 되어 충돌이 dissolve, escape 가 칩 추가로 scale"

조건 미달 시:

- **DISSOLVE FALSIFIED** — z 가 E 로 상승하지 않음(또는 비단조)
- → 🔴 CLOSED-NEGATIVE · "expert-count reframe 가 z-척도 상 escape 를 scale 시키지 못함" (a_paper_negative_ok)

## 2. 동기

- H_847 (F-CLM-MONO) 🔴 = byte-vocab+3-arm 단독으로 routing z>3.0 미달 (tiny/small 고정 rung). routing-diversity 가 model-dim 의존량이라 측정엔 3B GPU 필요 → AKD1000(≤1.2M) 충돌.
- mining DISSOLVE (L1·L5·L6·L13·E1·E2·E3·E6): scale 가정("scale=per-model size")을 깨고 expert-COUNT 로 이동하면 big=Σ chip-fit expert, routing-diversity=inter-expert dispatch entropy(chip-native + scalable). 칩 제약 자체가 specialization 강제(chip-as-regularizer).
- H_847(고정 z 임계) ⊥ H_852(z 의 scale 단조성) = 별개 falsifier. H_852 는 "scale 축을 바꾸면 escape 가 살아나는가"를 묻는다.

## 3. falsifier (사전등록, 임계 frozen pre-run)

```
F-CLM-MONO-ARRAY-MONO  : dispatch-entropy z(E) 단조 비감소 (z(E_{i+1}) >= z(E_i) - 0.50)
F-CLM-MONO-ARRAY-RISE  : z(64) - z(4) >= 1.0          (escape 가 칩 수로 genuinely scale)
F-CLM-MONO-ARRAY-FIT   : 전 expert chip-fit (expert_param_count <= 1,200,000)
```

3 PASS → SUPPORTED-NUMERICAL · "DISSOLVE: expert-count 가 escape 를 scale"
임의 FAIL → 🔴 CLOSED-NEGATIVE · "expert-count reframe ⊥ z-척도 escape scaling"

verdict 영속: `.verdicts/852_clm_mitosis_array_dispatch/F-CLM-MONO-ARRAY_prereg.txt` (frozen threshold verbatim) · raw run = `.../F-CLM-MONO-ARRAY_p_array_2026_05_30.txt`

## 4. 방법

```
1. sparse-MoE expert-array (CLM/model/array_moe.py · model.py 스켈레톤 확장):
   - top-k(=2) sparse dispatch · expert = conv mitosis cell = AKD1000 칩(@L3)
   - scale 축 = n_experts E in {4,8,16,32,64} (각 chip-fit <=1.2M)
2. 각 (E, seed{42,43,44}) → toy 2-lane 합성 corpus 로 120-step 학습(router DYNAMICS)
3. held-out eval 에서 inter-expert top-1 dispatch counts → H_obs
4. Dirichlet(1) uniform-simplex null(4000 draws) → mu/sigma → z = (H_obs−mu)/sigma
5. z(E) sweep 의 단조성 + z-rise + chip-fit 3조건 동시 평가 · 정직 보고(임계 재조정 0)
```

## 5. 측정 (P-ARRAY 완료 · 2026-05-30)

expert-count sweep E∈{4,8,16,32,64} × seed{42,43,44} = 15-run. toy d64/L2 · toy 2-lane 합성 corpus · 120-step train · $0 Mac CPU(torch 2.10.0). 코드 = `CLM/model/{array_moe,run_array_sweep}.py`. raw verdict = `.verdicts/852_clm_mitosis_array_dispatch/F-CLM-MONO-ARRAY_p_array_2026_05_30.txt` (+ harness smoke `.verdicts/clm-mitosis-array/array_smoke_2026_05_30.json`).

| E | mean_z | min_z | max_z | mean_H (nats) | chip_fit |
|---|---|---|---|---|---|
| 4  | **+0.526** | +0.158 | +0.899 | 1.186 | PASS |
| 8  | **+0.072** | −0.137 | +0.479 | 1.726 | PASS |
| 16 | **−0.884** | −2.532 | +0.817 | 2.259 | PASS |
| 32 | **−2.040** | −3.154 | −1.009 | 2.846 | PASS |
| 64 | **−7.614** | −8.930 | −5.964 | 3.171 | PASS |

- **raw dispatch entropy H 는 E 로 상승** (1.186→3.171 nats) — 절대 다양성은 expert 수와 함께 증가.
- **uniform-null 대비 z 는 E 로 급락** (+0.526→−7.614) — 판정자. monotone non-decreasing FAIL · z-rise = −8.140 (임계 ≥+1.0 미달).
- **전 expert chip-fit PASS** (12,352 params ≤ 1.2M 전 E).

## 6. 결과

🔴 **CLOSED-NEGATIVE** — P-ARRAY 측정 완료(15-run, 2026-05-30). 사전등록 3조건 중 단조성·z-rise 2개 FAIL(chip-fit 1개만 PASS). 사전등록 frozen 임계는 **변조 없음**. raw verbatim = `.verdicts/852_clm_mitosis_array_dispatch/F-CLM-MONO-ARRAY_p_array_2026_05_30.txt`.

판정 요약: **chip-fit PASS · z 단조 비감소 FAIL · z(64)−z(4)≥1.0 FAIL**. z-척도가 단독 판정자로 작동.

## 7. 해석

- **raw 다양성은 살아있다** (H 1.19→3.17 nats, E 로 단조 상승) — expert 를 늘리면 절대 dispatch entropy 는 커진다. monopoly collapse(단일 expert 독점) 자체는 아니다.
- **z-척도가 닫혔다**: uniform-null 의 entropy ceiling 이 ln(E) 로 함께 커지므로, 학습 router 가 균형(uniform)으로부터 **상대적으로 점점 더 멀어진다** — E 가 클수록 router 가 ln(E) 균형 천장을 따라가지 못해 z 가 음으로 깊어진다. 즉 "escape 가 칩 수로 scale" 이라는 DISSOLVE 주장은 **z-척도(uniform 대비 상대 다양성)에서는 성립하지 않는다**.
- **충돌은 z-척도 상 dissolve 되지 않았다**: scale 축을 expert-count 로 옮겨도, uniform-null 대비 상대 척도에서는 큰 array 일수록 더 monopoly-prone 으로 측정된다 (큰 router 가 짧은 학습으로 ln(E) 균형을 못 채움). H_847 의 z>3.0 부재가 expert-count 축으로도 재현 — 오히려 악화.
- **결론**: expert-count reframe 은 raw dispatch entropy 를 scale 시키지만 (절대 다양성 axis 는 살아있음), z-정규화 척도(escape vs uniform)에서는 closed-negative. 후속 재설계 입력 = (1) null 척도 재정의(ln(E)-정규화 H/ln(E) 를 직접 측정 = norm_entropy, smoke 에서 0.77~0.87 로 안정) · (2) 더 긴 학습으로 큰 array 의 균형 수렴 · (3) capacity-factor / 강한 load-balance lever (H_847 AXIS_MAP 와 합류).
- **honest 척도 caveat (p7)**: z-null = Dirichlet(1) uniform-simplex. 균형 router 는 z≈0, z>0 은 초-uniform 을 요구하는 엄격한 bar. 큰 E 에서 짧은 학습은 구조적으로 sub-uniform → z 음수. 이 frozen 척도는 **post-run 변조하지 않았다**. norm_entropy(H/ln E) 라는 다른 척도는 별도 신규 falsifier 로 분리해야 하며, 본 H_852 는 frozen z-척도 그대로 🔴.

## 8. 논의

- **a_completeness_over_cheap 정합**: scale 축 fresh reframe = 충돌 근원(scale=per-model size 가정) 직격 본선 경로.
- **a_scale_honest_scope 정합**: verdict 를 측정 axis(toy expert-count sweep, d64/L2)에 한정. expert-count 축은 deploy-relevant 하나 per-unit d_model/corpus 는 toy.
- **toy≠scale 정합 (H_666)**: toy 2-lane corpus 측정 = intuition; 본 결과는 toy scope 한정.
- **p8 정합**: MoE expert = mitosis cell = AKD1000 칩. dispatch entropy = cell-pool 분화 측정.
- **a_paper_negative_ok**: 🔴 도 publishable — "expert-count reframe ⊥ z-척도 escape scaling" 을 deterministically rule out.

## 9. 양방향 sibling

- sibling: [CLM/P0_ARCHITECTURE.md](../CLM/P0_ARCHITECTURE.md) §11 (MITOSIS-ARRAY · DISSOLVE SSOT)
- prior art: H_847 (F-CLM-MONO 🔴 고정 z 임계) · H_850 (F-CLM-SCALE) · H_666 (MoE collapse toy🟢 scale🔴)
- 형제 falsifier: F-CLM-BRIDGE-XFER (BRIDGE transfer · §11.6, PR4/5)
- UNIVERSE SSOT: [CANDIDATES.md](./CANDIDATES.md)
