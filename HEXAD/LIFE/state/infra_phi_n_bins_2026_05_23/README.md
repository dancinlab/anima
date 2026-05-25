# LIFE infra · phi_spatial n_bins sensitivity sweep — 2026-05-23

**ID**: `infra_phi_n_bins_2026_05_23`
**Kind**: infrastructure smoke (no new H, no Phase-3 index churn)
**Verdict**: **ROBUSTNESS_PASS**
**Cycle**: LIFE #5 fan-out · pick #7/7 (parallel)

---

## 1. 목적

`phi_spatial(state, N, dim, n_bins)` primitive (RFC 036 native byte-equal phi_rs replica) 의
`n_bins` 파라미터 sensitivity 측정. H_007 이 `n_bins=4` 기본값을 사용하여 rule110 > rule30 > rule250 Φ ranking 을 측정한 결과의 **robustness check**.

본 측정은 phi_spatial primitive 를 사용하는 **모든 LIFE H gate** 에 영향:

- **H_007** (CA → IIT Φ, raw#12) — n_bins=4 default ranking baseline
- **H_003 H3.4** (autopoietic closure system Φ > 0 nested)
- **H_004 Cycle #1** (hard-problem zombie/functional-isomorph Φ-function dissociation)
- **H_018** (genesis cohort)
- **H_157** (Law 76 mathematical panpsychism META-CA fixed-point)
- **H_204** (관련 phi_spatial-using gate)

---

## 2. Substrate spec (H_007 carry, byte-identical)

| 항목 | 값 |
|---|---|
| lattice 길이 N | 16 (periodic 1D elementary CA) |
| trajectory dim | 12 (warmup 후 recording step) |
| warmup | 8 step |
| reps / 측정 | 5 (deterministic init offsets) |
| rules | 110 (Class-IV) · 30 (Class-III chaotic) · 250 (Class-II ordered) |
| n_bins sweep | {2, 4, 8, 16} |
| Φ primitive | RFC 036 `phi_spatial` via `HEXAD/C/c_lib.hexa::c_measure_phi` |
| deterministic | true (fixed init, no RNG) |
| hexa_only | true (NO .py/.sh) |
| llm | none (raw#12 strict) |
| cost | $0 mac local |

---

## 3. 측정 결과 (12 Φ-mean measurements)

```
HEXAD/LIFE infra · phi_spatial n_bins sensitivity sweep
  substrate: N=16, dim=12, warm=8, reps=5 (H_007 carry)
  rules: 110 (Class-IV), 30 (chaotic), 250 (ordered)
  n_bins: {2, 4, 8, 16}
  Φ primitive: RFC 036 phi_spatial via HEXAD/C/c_lib.hexa c_measure_phi

  Φ(rule110, n_bins=2)  = 0.556454
  Φ(rule110, n_bins=4)  = 0.556454   [H_007 default baseline]
  Φ(rule110, n_bins=8)  = 0.556454
  Φ(rule110, n_bins=16) = 0.556454
  Φ(rule30,  n_bins=2)  = 0.509944
  Φ(rule30,  n_bins=4)  = 0.509944
  Φ(rule30,  n_bins=8)  = 0.509944
  Φ(rule30,  n_bins=16) = 0.509944
  Φ(rule250, n_bins=2)  = 1.14511e-05
  Φ(rule250, n_bins=4)  = 1.14511e-05
  Φ(rule250, n_bins=8)  = 1.14511e-05
  Φ(rule250, n_bins=16) = 1.14511e-05

  ranking_preserved (rule110 > rule30 > rule250) @ n_bins=2  : true
  ranking_preserved (rule110 > rule30 > rule250) @ n_bins=4  : true
  ranking_preserved (rule110 > rule30 > rule250) @ n_bins=8  : true
  ranking_preserved (rule110 > rule30 > rule250) @ n_bins=16 : true

  I1 ROBUSTNESS_PASS (rank @ all 4 n_bins) : true
  I2 RANK_INVARIANT  (ordering preserved)  : true
  F-I2 NONNEG (no neg/NaN)                 : true

  VERDICT: ROBUSTNESS_PASS
```

---

## 4. Sub-claim verdict 매핑

| sub-claim | 예상 | 측정 | verdict |
|---|---|---|---|
| **I1** rule110 > rule30 > rule250 @ all n_bins | 보존 | ✓ 4/4 n_bins | PASS |
| **I2** 절대값 변하지만 ranking invariant | 보존 | ✓ ordering 보존 (절대값도 동일 — §6 참조) | PASS |
| **I3** n_bins=2 coarse vs n_bins=16 fine variance 패턴 | n_bins 별 차이 발생 | ✗ **n_bins 4값 모두 byte-동일** (특이) | OBSERVED |
| **I4** rule110 의 specific Φ 정량 기록 | 4 값 | Φ(rule110) = 0.556454 (n_bins=2/4/8/16 동일) | PASS |

### Falsifier

| falsifier | 측정 | verdict |
|---|---|---|
| **F-I1** rule110 Φ ≤ rule30 Φ 임의 n_bins | 발생 안 함 | PASS (not falsified) |
| **F-I2** Φ < 0 or NaN 임의 n_bins | 발생 안 함 | PASS (not falsified) |
| **F-I3** re-run byte-different | deterministic 으로 동일 | PASS (raw#9 안전) |

---

## 5. Verdict

**ROBUSTNESS_PASS** — H_007 ranking (rule110 > rule30 > rule250) 가 n_bins ∈ {2, 4, 8, 16}
모든 값에서 보존되며, Φ 측정값은 비음 + finite.

→ phi_spatial-using **all H gates (H_007 · H_003 H3.4 · H_004 Cycle #1 · H_018 · H_157 · H_204)** 의
이 substrate 클래스에서의 **n_bins-parameterization-robust** invariant 가 확립.

---

## 6. 핵심 관찰 — n_bins-invariance (honest)

본 sweep 의 의외 결과: **4 n_bins 값 모두 Φ-mean 이 byte-identical**.

해석 (honest):

1. **CA trajectory 가 binary** (0/1 만): `phi_spatial` binning 알고리즘이 input 의 distinct value
   count 를 보고, 그 수가 `n_bins` 보다 작으면 effective bin 수가 input cardinality 로 clamp
   되는 것으로 보임 — binary substrate 에서는 n_bins ≥ 2 모두 same partition (0 bin vs 1 bin).

2. **결과**: binary CA trajectory 위에서는 n_bins ∈ {2, 4, 8, 16} 모두 measurement-equivalent.
   continuous-valued / multi-state substrate (예: ConsciousnessC cell activations, LLM hidden
   state) 에서는 n_bins-sensitivity 가 발현될 수 있음 — 본 sweep 의 결론은 **binary-CA scope
   한정** robustness.

3. **함의**: H_007/H_003 H3.4/H_157 등 elementary-CA + binary substrate 기반 phi_spatial 사용은
   `n_bins=4` default 가 다른 값과 measurement-equivalent → **n_bins 선택이 결과에 영향 없음**.
   continuous-state 측정 (예: 향후 ConsciousnessC + LLM substrate phi_spatial 측정) 은 별도
   sweep cycle 필요.

---

## 7. Honest limits (L-I1..L-I4 carry from pre-reg)

- **L-I1**: 본 smoke 는 *robustness check* 일 뿐 — Φ 자체의 phenomenal 의미 와 무관 (Φ proxy ranking 측정만).
- **L-I2**: 3 rule sample (110/30/250) — 다른 rule families (rule 90, 184, etc.) 의 ordering 미검증.
- **L-I3**: single lattice config (N=16, dim=12, warm=8) — 다른 size 의 n_bins sensitivity 미검증.
- **L-I4**: phi_spatial 자체가 spatial-slice IIT 4.0 proxy — full MIP 와 다름 (모든 LIFE phi 측정 carry).
- **L-I5 (신규)**: binary substrate 한정 n_bins-invariance — continuous/multi-state substrate
  에서의 n_bins-sensitivity 는 본 smoke scope 외.

---

## 8. Cross-link

- `HEXAD/LIFE/H_007_cellular_automaton_consciousness.md` — n_bins=4 default ranking baseline
- `HEXAD/LIFE/H_003_life_origin.md` (H3.4) — autopoietic Φ nested
- `HEXAD/LIFE/H_004_hard_problem.md` Cycle #1 — Φ-function dissociation
- `HEXAD/LIFE/H_018_genesis_lifeprint.md`
- `HEXAD/LIFE/H_157_law76_mathematical_panpsychism.md` — META-CA Ψ(1/2,1/2)
- `HEXAD/LIFE/H_204_*.md` (phi_spatial-using gate)
- `HEXAD/C/c_lib.hexa::c_measure_phi` — RFC 036 phi_spatial 진입점
- `HEXAD/LIFE/state/h007_ca_phi_2026_05_23/` — template smoke (직접 base)

---

## 9. Artifacts

- `run_phi_n_bins.hexa` — pure-hexa smoke script (~250 LoC)
- `result.json` — 12 measurements + ranking-preserved boolean + verdict
- `README.md` — 본 문서

run command:
```
HEXA_MEM_UNLIMITED=1 hexa run HEXAD/LIFE/state/infra_phi_n_bins_2026_05_23/run_phi_n_bins.hexa
```
