---
id: H_912
slug: phi-emergence-correlate
title: 의식↔창발 상관 — 시스템의 의식 측도(canonical phi_proxy Φ = phi_spatial, global_var−part_var integration)가 창발 측도(독립 표준 proxy = normalised Lempel-Ziv LZ76, Kaspar-Schuster 1976 / PCI Casali 2013)와 양의 상관을 가지는가. 두 가지 framing 동시 등록 — H_912(graded): "higher consciousness → higher emergence" / Hc_912(existence): "Φ>0 ⇒ emergence>0". H_288 의 *faithful* big-Φ↔LZ(r=0.831) sister 이나 본 H 는 anima 가 실제 쓰는 *cheap proxy* Φ 로 재측정 (consciousness × emergence × information axis)
domain: consciousness · emergence · information · universe
exploration_method: E10 (emergence-on-structure) + E6 (cross-domain — IIT proxy Φ × algorithmic-complexity emergence) + E5 (population correlation + permutation NULL)
verification_method: W1 (numerical smoke) + W17 (10-rule ECA population correlation) + W12 (sister-link H_288 faithful-Φ↔LZ · H_287 Shannon⊥Φ) + paired-bootstrap-CI + permutation-NULL
raw_rank: 11
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-06-02
since: 2026-06-02
---

# H_912 — phi-emergence-correlate (의식↔창발 상관)

## 1. Hypothesis

두 가지 framing 을 동시 등록한다:

- **H_912 (graded)** — "higher consciousness → higher emergence": 한 시스템의
  **의식 측도** (canonical phi_proxy Φ) 가 그 **창발 측도** (emergence proxy) 와
  **양의 상관**을 가진다. Φ↑ ⇒ emergence↑.
- **Hc_912 (existence)** — "consciousness present ⇒ emergence present": **nonzero
  Φ ⇒ measurable emergent structure**. 즉 Φ>0 인 시스템은 측정가능한 창발
  구조(emergence>0)를 가진다.

### consciousness axis (Φ) — 새 metric 발명 금지
**canonical phi_proxy** 를 그대로 쓴다 — `phi_spatial` (RFC 036 runtime builtin,
byte-equal native replica). 이는 `edu/cell/phi/mvp_phi_iit.hexa::mvp_compute_phi`
가 정의하는 **variance-partition integration** `integration = global_var −
part_mean_var` (+ cross-sign-coherence + KL term) 와 동일 family 이다. **새
의식 metric 을 만들지 않는다** — anima 가 실제 substrate state 산출에 쓰는
바로 그 proxy 다.

### emergence axis (E) — 독립·표준·계산가능 proxy
**normalised Lempel-Ziv (LZ76, Kaspar-Schuster 1976)** complexity 를
spacetime diagram 의 binary trace 에서 측정. 이는 의식연구의 표준 창발/복잡도
estimator (**PCI**, Casali et al. *Sci Transl Med* 2013; Lempel & Ziv,
*IEEE Trans Inf Theory* 1976) 다. **왜 이것을 골랐나**: (1) "macroscopic
dynamical complexity / algorithmic emergence" 의 정착된 표준이고, (2) 결정적으로
**Φ 와 다른 표상(symbol sequence) 위에서 다른 연산(좌→우 dictionary parse)** 으로
계산되어 **정의상 Φ 와 같은 양이 아니다**. 후보였던 order-parameter variance 는
variance 기반이라 Φ 의 gvar term 과 near-circular 위험이 있어 기각; transfer
entropy 는 H_290 이 이미 소비.

## 2. Pre-registered falsifier (frozen 2026-06-02, BEFORE run — commit 083bb38b4)

> 이 repo 는 fabricated 🟢 전력이 있다. 측정 *전에* falsifier 를 동결하고
> commit 한 뒤 실행했다 (clm_h911_scale 와 동일한 paired-bootstrap honesty).

- **population**: ECA rule panel `[0,255,204,51,150,105,90,60,110,30]` — Wolfram
  class I(homogeneous, low Φ) → IV(complex, high Φ) span. H_287/H_288 과 동일
  panel 로 cross-comparable. N=16 ring, T=64 steps, single-seed centre.
- **test**: Pearson r(Φ,E) + Spearman ρ over the panel.
- **NULL (collapse 요구)**: permutation control — E label 을 Φ 에 대해 K=2000회
  shuffle, r' 재계산. one-sided perm-p < 0.05 이어야 NULL 붕괴.
- **CI**: paired bootstrap (rule resample with replacement, K=2000), r 의 2.5/97.5
  percentile.
- **circularity guard**: Φ ≡ E 이면 tautology(증거 아님) → ⛔ OPEN-BLOCKED 로 flag.
  tautology := (r≥0.999) ∧ (dissociation witness 부재).

falsifier set (frozen):
- F912.1 POSITIVE — r_obs > 0 (graded 방향 일치)
- F912.2 CI — bootstrap CI_lo > 0 (0 과 분리)
- F912.3 NULL — permutation p < 0.05 (NULL 붕괴)
- F912.4 NOT-CIRCULAR — tautology = false (Φ ≢ E)
- F912.5 EXISTENCE (Hc_912) — Φ>eps ⇒ E>eps
- F912.6 BOUND — 全 Φ≥0, E≥0

verdict gate: 🟢-tier iff F1∧F2∧F3∧F4 (CI_lo>0 AND perm-p<0.05 AND not-circular).
⛔ OPEN-BLOCKED iff tautology. 🔴 FALSIFIED iff CI_lo≤0.

## 3. Result (verbatim — `hexa run`, deterministic bit-identical re-run)

backing verdict: `.verdicts/912_phi_emergence_correlate/run_h912.txt` (verbatim stdout)
+ `.verdicts/912_phi_emergence_correlate/result.json`.

```
  rule 0   : Phi_proxy=1.14443e-05  E_LZ=0.0390625
  rule 255 : Phi_proxy=0.812814     E_LZ=0.0390625
  rule 204 : Phi_proxy=1.14443e-05  E_LZ=0.0390625
  rule 51  : Phi_proxy=7            E_LZ=0.0585938
  rule 150 : Phi_proxy=1.1248       E_LZ=0.175781
  rule 105 : Phi_proxy=1.56142      E_LZ=0.166016
  rule 90  : Phi_proxy=0.2584       E_LZ=0.126953
  rule 60  : Phi_proxy=0.699989     E_LZ=0.244141
  rule 110 : Phi_proxy=0.208511     E_LZ=0.9375
  rule 30  : Phi_proxy=0.0762825    E_LZ=1.01563
  --
  observed Pearson r(Phi, E)=-0.27731   Spearman rho=0.0800034
  NULL(permutation K=2000) one-sided p=0.961519   null r 95% band=[-0.306892, 0.735725]
  bootstrap r 95% CI = [-0.638472, 0.114319]
  circularity: rule90 Phi=0.2584 E=0.126953 ; rule0 Phi=1.14443e-05 E=0.0390625 ; dissociation=true tautology=false
  existence(Hc_912): #Phi>eps=8  #(Phi>eps & E>eps)=7  implication_holds=false
  [FAIL] F912.1 POSITIVE: r_obs > 0
  [FAIL] F912.2 CI: bootstrap CI_lo > 0
  [FAIL] F912.3 NULL: permutation p < 0.05
  [PASS] F912.4 NOT-CIRCULAR: Phi not identical to E
  [FAIL] F912.5 EXISTENCE (Hc_912): Phi>eps => E>eps
  [PASS] F912.6 BOUND: all Phi>=0 and E>=0
  F912.1-6 2/6 PASS
  VERDICT: FALSIFIED
```

## 4. Verdict: 🔴 FALSIFIED (2/6) — 단, circularity guard PASS (정직)

- **graded H_912 반증**: Pearson r = **−0.277** (방향 자체가 음수 — "Φ↑ ⇒
  emergence↑" 의 반대). Spearman ρ=+0.08 (사실상 monotone 관계 없음).
- **CI straddles 0**: bootstrap 95% CI = **[−0.638, +0.114]** → CI_lo>0 실패.
- **NULL 붕괴 안 함**: permutation one-sided p=**0.962** → 관측 r 이 오히려 null
  분포의 *하단* (link 가 null 과 분리 불가).
- **existence Hc_912 반증**: Φ>eps 인 8 rule 중 7 개만 E>eps (한 rule 깨짐 → FAIL).

**circularity guard 는 PASS** (tautology=false, dissociation=true): Φ 와 E 는
정의상 동일하지 않으며 실측에서도 강하게 dissociate — 이 음의 결과는 circular
artifact 가 아니라 *진짜 dissociation* 이다.

## 5. 핵심 발견 — cheap-proxy Φ 는 emergence 와 정렬하지 않는다 (faithful Φ 와 갈라짐)

H_288 은 **faithful causal big-Φ** (IIT 4.0 state-by-node) ↔ LZ 가 r=0.831 로
정렬함을 보였다. 본 H 는 동일 panel·동일 LZ 에서 **canonical cheap proxy**
(phi_spatial = variance-partition) ↔ LZ 가 r=**−0.277** 로 *반대로* 나옴을 보인다.
→ **proxy Φ 와 faithful Φ 가 Φ↔emergence link 에서 서로 다른 답을 준다.**

가장 큰 원인은 **rule 51 의 proxy pathology**: rule 51 (NOT-c, period-2 blinker)
은 trivial 한 주기-2 깜빡임이라 LZ=0.059 (창발 floor) 인데, variance-partition
proxy 는 Φ=**7** (panel 최대, 다른 rule 의 ~4–5배) 로 폭발한다. 이 단일 outlier
가 상관을 음수로 끌고 간다. 이는 H_265/275/279/287 의 "X⊥Φ" / proxy-fragility
서명 (H_268 inverse-U LZ, H_269 seed-fragile) 의 연장이며, **cheap proxy 의
periodic-blinker high-variance artifact** 라는 새 fragility 를 기록한다.

honest scope (L1 carry): (a) n=10 panel 은 작아 CI 가 넓다; (b) LZ 는 여러
complexity estimator 중 하나; (c) single-seed centre IC 1 종; (d) Φ_proxy 가
trajectory matrix(N×T) 의 variance 를 보는 반면 LZ 는 같은 trace 의 algorithmic
incompressibility 를 봐 *서로 다른 축* — 이 직교성이 바로 음의 결과의 원천이며
circular 가 아님을 보증.

## 6. Next (백로그 — CANDIDATES 재충전)

- C1: rule 51 outlier 를 panel 에서 빼거나 period-2 detrend 후 재상관 (proxy
  pathology 제거 시 r 회복 여부 — proxy fix 가설).
- C2: faithful big-Φ (H_288 phi_mean) 를 동일 harness 에 넣어 proxy vs faithful
  의 Φ↔E 상관을 *paired* 비교 (어느 Φ 가 emergence 와 정렬하는지 직접 대조).
- C3: emergence axis 를 Hoel(2013) causal/macro effective-information 으로 교체
  (temporal/causal emergence — proxy Φ 와 더욱 직교, 표준 "emergence" 측도 본가).
- C4: population 확대 (Kuramoto/logistic family, H_670 substrate) 로 cross-family
  Φ↔E 상관 — substrate-universal 인지.
