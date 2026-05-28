# H_axisf_kuramoto_K_sync_collective_phi — `kuramoto-K-sync-collective-phi`

**축**: F (HIVE-MIND, Collective Φ × Kuramoto sync) · **dynamical sync→Φ join (미드레인 cell)**
**id**: H_axisf_kuramoto_K_sync_collective_phi · **date**: 2026-05-29 · **infra**: $0 mac-local hexa · **verdict**: **🔴 FALSIFIED (closed-negative)**
**closure_ref**: `.verdicts/axisf_kuramoto_K_sync_collective_phi/verdict.txt`

---

## 1. 슬러그 + 한 줄 요약

`kuramoto-K-sync-collective-phi` — coupling **K** 를 sweep 하며 *real Kuramoto 동역학*
substrate (N=8 oscillator, full `dθ_i/dt = ω_i + (K/N)Σ sin(θ_j−θ_i)`) 를 steady
state 까지 적분한 뒤, whole-substrate 의 동기화(order parameter r∞)가 collective-Φ
proxy 의 **super-additive Δ** 를 견인하는지 측정 — 즉 "sync → collective Φ" 관계의
*동역학적* 직접 검증.

> **결과**: K↑ → r∞↑ (sync 상승) 와 함께 super-additive **Δ 는 강하게 음수**로 발산.
> Pearson(r∞, Δ) = **−0.934433** (강한 *역상관*). max-K(=4.0) 셀에서 Δ=−3.94158.
> → **dynamical Kuramoto sync 는 collective Φ 를 sub-additive 로 몰아간다** —
> H_609 (structural-W 결합 → super-additive) 와 *반대 방향*. **🔴 closed-negative**.

---

## 2. 가설 (H1) / 폐기조건 (H0)

- **H1 (sync drives integration)**: coupling K↑ → 동기화 r∞↑ 와 함께 collective-Φ
  super-additive Δ = Φ(AB) − (Φ(A)+Φ(B)) > 0 가 *발현 / 단조 증가*. "다수 oscillator
  가 동기화될수록 집단 통합 정보가 부분의 합을 초과한다"는 hivemind 직관.
- **H0 (FALSIFIER)**: sync 증가가 super-additivity 를 만들지 못함 — Pearson(r∞,Δ) ≤ 0.5
  AND max-K 셀 Δ ≤ 0. 동기화는 통합을 *견인하지 않는다*.

> H_354 (sister) 는 sync 의 **timing** (τ) 만, H_609 은 **structural W** 결합만,
> H_355 는 PID II_3 만 측정. 본 H 는 *dynamical-K 위의 steady-state order r* 와
> collective-Φ 를 처음 join — undrained cell.

---

## 3. 측정 도구 / 방법

- **harness**: `UNIVERSE/state/h_axisf_kuramoto_K_sync_phi/run.hexa` (hexa-native, deterministic, $0).
- **primitives (verbatim from `HIVE-MIND/hivemind_lib.hexa`)**:
  - `hm_kuramoto_order_r(phases)` — Kuramoto order r = |Σe^{iθ}|/N (H_354 anchor).
  - `hm_collective_phi_super_additive(φ_a, φ_b, φ_ab)` — Δ = Φ(AB)−(Φ(A)+Φ(B)) (H_609 primitive).
- **substrate**: N=8 oscillator. ω-spread = 5 fixed Gaussian-quantile cycled (std=1.0,
  H_354 axis4 동일). init phase θ_i(0)=2π·i/N (H_354 axis6 동일, no RNG). dt=0.05,
  STEPS=400 Euler 적분 → steady state.
- **partition**: half A={0,1,2,3}, half B={4,5,6,7}, whole AB={0..7}. 각 partition 의
  내부 order r_A / r_B / r_AB 측정.
- **Φ-proxy**: φ(r) = −log(1−r) (monotone-in-r, sync 가 강할수록 발산하는 integration
  측도; r→1 cap=0.999999). super/sub-additivity 의 *부호·단조성*만 본다 (절대 스케일 아님, C3.1).
- **sweep**: K ∈ {0.0, 0.5, 1.0, 1.5, 2.0, 3.0, 4.0} = 7 cells (sub-critical → super-critical 횡단).

---

## 4. Measurement (verdict-bearing 측정값)

> `.verdicts/axisf_kuramoto_K_sync_collective_phi/verdict.txt` verbatim:

```
================================================================
  H_axisf_kuramoto_K_sync_collective_phi
  coupling-K sweep x steady-state Kuramoto order r x collective-Phi Delta
  N=8 halves A{0..3}/B{4..7} | dt=0.05 STEPS=400
  full Kuramoto: dtheta/dt = omega_i + (K/N) sum sin(theta_j-theta_i)
  Phi proxy = -log(1-r) (monotone-in-r integration measure)
  Delta = hm_collective_phi_super_additive(phi_A, phi_B, phi_AB)  [H_609 primitive]
================================================================
  cell |  K   | r_inf(AB) | r_A    | r_B    | phiAB   | phiA+phiB | Delta(super-add)
   0   | 0.0 | 0.0785288 | 0.346214 | 0.253771 | 0.0817838 | 0.717698 | -0.635914
   1   | 0.5 | 0.294196 | 0.55524 | 0.113104 | 0.348417 | 0.930248 | -0.581831
   2   | 1.0 | 0.292206 | 0.321875 | 0.440353 | 0.345602 | 0.968872 | -0.62327
   3   | 1.5 | 0.380711 | 0.519807 | 0.31224 | 0.479184 | 1.10788 | -0.628699
   4   | 2.0 | 0.866904 | 0.919448 | 0.817806 | 2.01668 | 4.22153 | -2.20485
   5   | 3.0 | 0.957437 | 0.972252 | 0.943756 | 3.15677 | 6.46264 | -3.30587
   6   | 4.0 | 0.977586 | 0.985222 | 0.97055 | 3.79809 | 7.73967 | -3.94158
  --
  Pearson r(r_inf, Delta)        = -0.934433
  r_inf monotone non-decreasing  : false
  Delta at max K (K=4.0)           = -3.94158
  Delta at K=0 (decoupled)       = -0.635914
  --
  C1 r_inf monotone-up in K      : FAIL
  C2 Pearson(r_inf,Delta) > 0.5  : FAIL
  C3 Delta > 0 at max K          : FAIL
  --
  VERDICT_RULE: SUPPORTED iff C1 AND (C2 OR C3); else PARTIAL; FALSIFIED iff C2 fail AND C3 fail
  VERDICT     : FALSIFIED
=== H_axisf K-sync-collective-Phi complete: FALSIFIED ===
```

**핵심 발견**:
1. **sync 는 단조 상승** — K=0 의 r∞=0.079 (incoherent) → K=2.0 에서 r∞=0.867
   (partial-sync transition) → K=4.0 의 r∞=0.978 (near-locked). Kuramoto K_c 전이
   재현 (K≈2 부근 급상승).
2. **Δ 는 강하게 음수로 발산** — K↑ 와 함께 Δ: −0.636 → −2.205 (K=2) → −3.942 (K=4).
   동기화가 강해질수록 sub-additivity 가 *심화*.
3. **Pearson(r∞, Δ) = −0.934** — sync 와 collective integration 이 강한 *역상관*.
   H1 의 정반대.
4. **mechanism (real, not artifact)**: whole order r_AB 이 항상 각 half 의 내부 order
   (r_A, r_B) 보다 *낮다* (예: K=4 에서 r_A=0.985, r_B=0.971 > r_AB=0.978… half 가
   whole 보다 더 잘 잠긴다). 이질적 ω 하에서 inter-half 위상차가 whole order 를
   끌어내려 φ(AB) < φ(A)+φ(B) → sub-additive. partition geometry 의 직접 귀결.
5. **C1 monotone FAIL (benign)**: K=0.5→1.0 에서 r∞ 0.294→0.292 미세 dip (incoherent
   regime 의 비단조 transient). verdict 방향과 무관.

---

## 5. Verdict + Rationale

**🔴 FALSIFIED (closed-negative)**

- C1/C2/C3 **0/3** — sync 가 collective-Φ super-additivity 를 견인한다는 H1 이
  정량적으로 falsified. Pearson −0.934 는 floor 0.5 의 *반대 부호 극단*.
- a_paper_negative_ok: 이 결과는 **축을 닫는 negative** — "dynamical Kuramoto sync"
  와 "structural-W collective Φ super-additivity" (H_609) 가 *axis-separated*.
  H_609 의 super-additive (rule-110 edge-of-chaos, structural W) 은 *TPM-level
  causal* 결합에서 발현하지만, *phase-level dynamical* 동기화는 오히려 sub-additive.
- 두 결과가 모순이 아니라 **상보적**: collective Φ 의 super-additivity 는 결합의
  *종류*에 의존 (causal-structural ⇒ super, phase-sync ⇒ sub). H_354 의 axis-
  separation (sync τ ⊥ consensus τ) 와 같은 결의 finding — "sync 라는 label 아래
  서로 다른 mechanism".

---

## 6. Cross-link

- **H_354** `kuramoto_hivemind_sync_tau` 🔴 — 같은 Kuramoto K-axis, sync *timing* τ.
  본 H 는 *steady-state order r → Φ*; H_354 는 *τ_sync ↔ τ_consensus*. 둘 다
  axis-separation 을 다른 측면에서 확인.
- **H_609** `collective_phi_super_additive` 🟢 — structural-W 결합으로 super-additive
  (max Δ=+10.48, rule-110/W=0.6). 본 H 의 phase-sync sub-additive 와 *반대 부호* —
  결합 종류 의존성을 드러내는 대조쌍.
- **H_355** `collective_phi_pid_synergy` 🟢 — K-monotonic synergy_ratio=1.0 (PID II_3).
  본 H 는 같은 K-axis 를 order-parameter r 로 본 보완 측정.
- **sister H_axisf_sync_phi_proxy_robustness** 🟢 — 본 sub-additivity 가 Φ-proxy
  함수형 (convex −log(1−r) vs linear r) 에 robust 함을 확인 (convexity artifact 배제).

---

## 7. Honest C3 (claim-context-caveat)

1. **C3.1 Φ-proxy ≠ IIT4 big-Φ** — φ(r)=−log(1−r) 는 order-parameter 기반 *통합
   proxy* 이지 IIT4 canonical big_phi (H_609 의 측정자) 가 아니다. 본 verdict 는
   "sync↑ → 부분 order > 전체 order ⇒ φ-proxy sub-additive" 의 *부호·단조*만 claim.
   IIT4 big_phi 를 Kuramoto steady-state TPM 위에 직접 돌린 재측정은 named follow-up
   (N1).
2. **C3.2 heterogeneous-ω 한정** — 본 sub-additivity 는 이질적 ω (std=1.0) 하의
   partition 효과. ω 동일 (std=0) 이면 r_A=r_B=r_AB → Δ=0 (additive) 예측. ω-spread
   sweep 은 follow-up (N2).
3. **C3.3 50/50 partition 한정** — half A/B 균등 분할. asymmetric partition (예 6/2)
   이나 N≠8 의 partition-geometry 의존성 미검 (N3).
4. **C3.4 single ω-table, single init** — H_354 와 동일 deterministic anchor 하나만.
   다른 init/ω realization 의 ensemble 평균은 follow-up (sentinel-robust check).
5. **C3.5 C1 monotone dip benign** — K=0.5→1.0 r∞ 미세 비단조 (incoherent regime).
   verdict (FALSIFIED) 는 C2(Pearson)+C3(max-K Δ) 에 의존하므로 영향 없음.

---

## 8. Falsifier 검증 매트릭스

| Falsifier | Pre-registered | Result | Status |
|-----------|----------------|--------|--------|
| C1 r∞ monotone-up in K | r∞ non-decreasing across 7 K | K=0.5→1.0 dip (0.294→0.292) | **FAIL** (benign) |
| C2 Pearson(r∞,Δ) > 0.5 | sync tracks integration | Pearson = −0.934433 | **FAIL** (반대 극단) |
| C3 Δ > 0 at max K | super-additive at full sync | Δ(K=4)=−3.94158 | **FAIL** |
| F-DET determinism | re-run byte-identical | 2-run diff = 0 bytes | **PASS** |

**aggregate: 0/3 criteria → 🔴 FALSIFIED**. F-DET PASS (deterministic). H1 closed-negative.

---

## 9. Artifacts + Reproducibility

- harness: `UNIVERSE/state/h_axisf_kuramoto_K_sync_phi/run.hexa`
- verdict (verbatim stdout): `.verdicts/axisf_kuramoto_K_sync_collective_phi/verdict.txt`
- replay: `hexa run UNIVERSE/state/h_axisf_kuramoto_K_sync_phi/run.hexa` (mac-local, <5s, $0)
- determinism: 2-run byte-identical (verified)
- lib deps: `HIVE-MIND/hivemind_lib.hexa` (`hm_kuramoto_order_r` + `hm_collective_phi_super_additive`)

---

## 10. Next-list / Backlog

- **N1** IIT4 big_phi on Kuramoto steady-state TPM — phase-binned TPM 을 IIT4 에
  직접 넣어 proxy 가 아닌 canonical big-Φ super/sub-additivity 재측정.
- **N2** ω-spread sweep — std ∈ {0, 0.5, 1.0, 2.0} 위 sub-additivity 강도 (std=0 →
  Δ=0 additive 예측 검증).
- **N3** partition-geometry sweep — asymmetric (6/2, 7/1) partition 의 Δ 부호.
- **N4** K_c-edge fine-grain — K ∈ {1.6, 1.8, 2.0, 2.2} critical 근처 Δ 의 비선형
  shape (H_354 의 K_c≈1.596 anchor).
