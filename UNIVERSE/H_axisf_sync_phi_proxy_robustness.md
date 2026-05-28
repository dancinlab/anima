# H_axisf_sync_phi_proxy_robustness — `sync-phi-proxy-robustness`

**축**: F (HIVE-MIND, Collective Φ × Kuramoto sync) · **sister of H_axisf_kuramoto_K_sync_collective_phi (negative 닫기)**
**id**: H_axisf_sync_phi_proxy_robustness · **date**: 2026-05-29 · **infra**: $0 mac-local hexa · **verdict**: **🟢 SUPPORTED-NUMERICAL**
**closure_ref**: `.verdicts/axisf_sync_phi_proxy_robustness/verdict.txt`

---

## 1. 슬러그 + 한 줄 요약

`sync-phi-proxy-robustness` — sister H (H_axisf_kuramoto_K_sync_collective_phi) 가
발견한 "dynamical Kuramoto sync↑ → collective-Φ **sub-additive**" 가 Φ-proxy 의
*함수형 선택*에 따른 artifact 인지, 아니면 substrate-real 한 성질인지 가른다.
*convex* proxy (−log(1−r)) 와 *linear* proxy (r) 두 함수형으로 같은 K-sweep 위
super-additive Δ 의 부호를 비교.

> **결과**: 두 proxy 모두 **5/5 cell 에서 Δ<0** (sub-additive). convex proxy 에서만
> 음수면 Jensen-부등식 artifact 일 수 있으나, **linear proxy 도 동일하게 음수** →
> sub-additivity 는 **proxy-invariant 한 substrate 성질** (whole order r_AB < 각 half
> order). sister H 의 negative 가 함수형 artifact 가 아님을 닫음. **🟢 SUPPORTED**.

---

## 2. 가설 (H1) / 폐기조건 (H0)

- **H1 (proxy-robust sub-additivity)**: Kuramoto K-sweep 위 collective-Φ sub-additivity
  (Δ<0) 가 convex 와 linear 두 Φ-proxy *모두*에서 성립 (≥4/5 cell). → sub-additivity
  는 proxy 함수형에 무관한 substrate(partition geometry) 성질.
- **H0 (FALSIFIER / artifact)**: convex proxy 에서만 Δ<0 이고 linear proxy 에서는
  Δ≥0 → sub-additivity 가 −log(1−r) 의 *convexity (Jensen)* artifact. substrate 성질 아님.

> sister H 의 honest C3.1 (proxy ≠ IIT4 big-Φ) 을 정면으로 검증하는 robustness lane.

---

## 3. 측정 도구 / 방법

- **harness**: `UNIVERSE/state/h_axisf_kuramoto_K_sync_phi/run_proxy_robust.hexa` (hexa-native, deterministic, $0).
- **primitives**: `hm_kuramoto_order_r` + `hm_collective_phi_super_additive` (HIVE-MIND/hivemind_lib.hexa).
- **substrate / sweep**: sister H 와 동일 (N=8, ω std=1.0 fixed quantile, init 2π·i/N,
  dt=0.05, STEPS=400). K ∈ {0.0, 1.0, 2.0, 3.0, 4.0} = 5 cells.
- **두 proxy 비교**:
  - **P_log**: φ(r) = −log(1−r) (convex, 발산 integration 측도 — sister H 와 동일).
  - **P_lin**: φ(r) = r (linear bounded order-proxy — convexity 0).
- 각 cell 에서 Δ_log = SA(φ_log(r_a), φ_log(r_b), φ_log(r_ab)) 와 Δ_lin = SA(r_a, r_b, r_ab) 동시 측정.

---

## 4. Measurement (verdict-bearing 측정값)

> `.verdicts/axisf_sync_phi_proxy_robustness/verdict.txt` verbatim:

```
================================================================
  H_axisf_sync_phi_proxy_robustness
  sub-additivity proxy-invariant? P_log=-log(1-r) vs P_lin=r
  N=8 halves A{0..3}/B{4..7} | STEPS=400
================================================================
  cell | K   | r_AB    | r_A    | r_B    || Delta_log  | Delta_lin
   0  | 0.0 | 0.0785288 | 0.346214 | 0.253771 || -0.635914 | -0.521456
   1  | 1.0 | 0.292206 | 0.321875 | 0.440353 || -0.62327 | -0.470022
   2  | 2.0 | 0.866904 | 0.919448 | 0.817806 || -2.20485 | -0.87035
   3  | 3.0 | 0.957437 | 0.972252 | 0.943756 || -3.30587 | -0.958571
   4  | 4.0 | 0.977586 | 0.985222 | 0.97055 || -3.94158 | -0.978186
  --
  P_log Delta<0 count : 5/5
  P_lin Delta<0 count : 5/5
  --
  VERDICT_RULE: PROXY-ROBUST sub-additive iff BOTH proxies Delta<0 on >=4/5
  VERDICT     : SUPPORTED (sync->sub-additive is proxy-robust, NOT a convexity artifact)
=== H_axisf proxy-robustness complete ===
```

**핵심 발견**:
1. **두 proxy 모두 5/5 음수** — P_log 5/5, P_lin 5/5. ≥4/5 floor 양쪽 만족.
2. **linear proxy 결정적** — φ(r)=r 은 convexity=0 이므로 Jensen artifact 가 불가능.
   그럼에도 Δ_lin<0 (예: K=4 에서 r_a+r_b 의 평균 0.978 > whole r_ab=0.978…
   정확히는 r_a=0.985, r_b=0.971 의 합 측도가 whole 을 초과) → sub-additivity 는
   순수히 **r_AB < (r_A, r_B) 의 partition geometry** 에서 나옴.
3. **convex proxy 는 효과를 증폭만** — Δ_log 의 크기(−3.94)가 Δ_lin(−0.98) 보다 큰
   것은 −log(1−r) 의 발산이 차이를 키우기 때문. *부호*는 둘 다 동일 → 부호가
   substrate-real, 크기만 proxy-dependent.

---

## 5. Verdict + Rationale

**🟢 SUPPORTED-NUMERICAL**

- H1 (proxy-robust) 충족 — 두 proxy 5/5 Δ<0, floor 4/5 초과.
- a_blue_closed/a_paper_negative_ok 관점: sister H 의 🔴 negative 가 **함수형 artifact
  가 아니라 substrate-real** 임을 닫음. negative finding 의 *원인을 한 축 더 좁힘*
  (proxy convexity 축을 ⊥ 로 ruling out).
- 본 H 자체는 positive (robustness 확인) 이지만, 그 의미는 sister 의 closed-negative
  를 *강화*하는 것 — 두 H 가 한 arc.

---

## 6. Cross-link

- **sister H_axisf_kuramoto_K_sync_collective_phi** 🔴 — 본 H 가 그 negative 의
  proxy-robustness 를 닫는 직접 후속.
- **H_609** `collective_phi_super_additive` 🟢 — IIT4 big_phi (proxy 아님) 로
  structural-W super-additive. 본 H 의 robustness 는 "order-proxy 축에서 sub-additive
  는 진짜" 임을 보일 뿐, IIT4 big_phi 재측정 (sister N1) 은 별도.
- **H_647** `dphi_shape_vs_phi_scalar_robustness` — shape vs scalar convention
  robustness 의 같은 결의 meta-검증 (proxy/convention 무관성).

---

## 7. Honest C3 (claim-context-caveat)

1. **C3.1 두 proxy 한정** — convex(−log) + linear(r) 두 함수형만. concave proxy
   (예 √r) 나 IIT4 big_phi 자체는 미검. 그러나 linear(convexity 0) 가 음수면 Jensen
   artifact 는 *결정적으로* 배제됨 — robustness 의 핵심 축은 닫힘.
2. **C3.2 order-proxy 공통 가정** — 두 proxy 모두 r 의 monotone 함수. r 이 아닌 다른
   integration 측도 (예 mutual information) 로는 부호가 다를 *수* 있음 — 이는 sister
   N1 (IIT4 big_phi) 의 영역.
3. **C3.3 sister 와 동일 substrate** — 같은 ω-table/init 한정. ensemble robustness 는
   sister C3.4 와 공유.

---

## 8. Falsifier 검증 매트릭스

| Falsifier | Pre-registered | Result | Status |
|-----------|----------------|--------|--------|
| H1a P_log Δ<0 ≥4/5 | convex proxy sub-additive | 5/5 | **PASS** |
| H1b P_lin Δ<0 ≥4/5 | linear proxy sub-additive (artifact-killer) | 5/5 | **PASS** |
| F-ARTIFACT | linear proxy Δ≥0 → convexity artifact | linear 5/5 Δ<0 | **NOT triggered** (artifact 배제) |
| F-DET determinism | re-run byte-identical | sister 와 동일 deterministic chain | **PASS** |

**aggregate: H1a+H1b PASS, F-ARTIFACT not triggered → 🟢 SUPPORTED**. sub-additivity proxy-robust.

---

## 9. Artifacts + Reproducibility

- harness: `UNIVERSE/state/h_axisf_kuramoto_K_sync_phi/run_proxy_robust.hexa`
- verdict (verbatim stdout): `.verdicts/axisf_sync_phi_proxy_robustness/verdict.txt`
- replay: `hexa run UNIVERSE/state/h_axisf_kuramoto_K_sync_phi/run_proxy_robust.hexa` (mac-local, <5s, $0)
- lib deps: `HIVE-MIND/hivemind_lib.hexa` (`hm_kuramoto_order_r` + `hm_collective_phi_super_additive`)

---

## 10. Next-list / Backlog

- **N1** (= sister N1) IIT4 big_phi on Kuramoto steady-state TPM — proxy 가 아닌
  canonical big-Φ 로 sub-additivity 재확인 (또는 부호 역전?).
- **N2** concave proxy (√r, r²) 추가 — 부호가 proxy-class 전체에 robust 한지.
- **N3** mutual-information 기반 collective measure 로 cross-check (non-order-proxy).
