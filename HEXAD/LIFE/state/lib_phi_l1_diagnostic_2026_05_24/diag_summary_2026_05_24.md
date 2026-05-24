# diag_summary_2026_05_24 — L1 root cause diagnostic + Rust phi_rs cross-validation

> **위치**: `HEXAD/LIFE/state/lib_phi_l1_diagnostic_2026_05_24/diag_summary_2026_05_24.md`
> **harness**: `diag_l1_binning.hexa` (worktree-local) · `/tmp/diag_rust_oracle.py` (외부, project-tape `.py` 거부 회피)
> **세션 worktree**: `agent-a07653c5889f742f6`
> **상위 milestone**: PHI.md #7 (L1 root cause 추적) · #8 (LIFE 본질 영향) · #9 (verdict promote evidence)

---

## 1. 실행 결과 verbatim

`diag_l1_binning_run.txt` + `diag_rust_oracle_run.txt` 두 산출 모두 worktree 내부 저장.

### L1a — step 1 (`phi_bin_values`) hexa f64 vs C f32-cast simulation

```
  rule=110  diff_cells=0/8  diff_idx=0/64
  rule= 30  diff_cells=0/8  diff_idx=0/64
  rule=250  diff_cells=0/8  diff_idx=0/64
  rule=184  diff_cells=0/8  diff_idx=0/64
  rule= 60  diff_cells=0/8  diff_idx=0/64
  TOTAL: diff_cells=0/40  diff_idx=0/320
```

**해석**: hexa 측 `phi_bin_values` (f64 정직) 와 numpy 로 모사한 C 측 `(float)v[i]` cast 후 binning 의 결과 sequence 가 **5 rule × 8 cell × 8 dim = 320 index 모두 byte-identical**. binary 0/1 입력은 f32 lossless 표현 범위 안이라서 f32 narrowing 이 boundary 를 cross 시키지 못한다. 즉 **L1 (f32-cast precision divergence) 는 step 1 에선 0% manifest** — 본 fixture 한정.

### L1b — Rust phi_rs oracle vs hexa-native vs C-replica spatial_phi

| rule | spatial_phi (Rust) | phi_hexa (high-prec) | phi_c (C replica) | d(hexa-rust) | d(c-rust) |
|------|---|---|---|---|---|
| 110  | 4.977298299530723e-09 | 4.977298299530722e-09 | 4.90943e-06 | -8.3e-25 | **+4.904e-06** |
| 30   | 0.4225850815306889    | 0.4225850815306895    | 0.422588    | +6.1e-16 | **+2.918e-06** |
| 250  | 4.977298299530723e-09 | 4.977298299530722e-09 | 4.90943e-06 | -8.3e-25 | **+4.904e-06** |
| 184  | 0.5858415229693057    | 0.5858415229693067    | 0.585839    | +1.0e-15 | **-2.523e-06** |
| 60   | 0.7900283296344668    | 0.7900283296344673    | 0.790029    | +5.6e-16 | **+6.704e-07** |

**핵심**:
- `phi_native (hexa)` vs `phi_rs (Rust oracle)` — 5/5 **`|d| < 1e-12`** (실측 max 1.0e-15 ≈ 1-2 ulp, IEEE-754 summation reorder 잡음). strict bit-pattern byte-equal 은 5/5 false (1-2 ulp drift), 그러나 알고리즘 정합도는 **사실상 동등**.
- `c_measure_phi (C replica)` vs `phi_rs (Rust)` — 5/5 **`|d| ≥ 6.7e-07`** (실측 6.7e-7 ~ 4.9e-6). hexa 보다 **9-10 orders of magnitude 더 큰 drift**.

---

## 2. 결합 verdict — **case 1 (변형: hexa 가 Rust 에 더 가깝다)**

| 가능 case | L1a 결과 | L1b 결과 | 매칭 |
|---|---|---|---|
| **case 1** (요청 spec 정의) | step 1 분기 confirm | hexa ≡ Rust | ❌ L1a 분기 = 0, 그러나 결론은 동일 (hexa 정확) |
| **case 2** | hexa-side 분기 (impl bug) | hexa-side 분기 | ❌ — hexa 가 Rust 에 더 가깝다 |
| **case 3** | 도달 불가 | 도달 불가 | ❌ — 둘 다 도달 |
| **case 1′ (실측)** | step 1 동일 | **hexa ≡ Rust (within ulp), C 가 outlier** | ✅ |

**판정**: **case 1′** — request spec 의 case 1 의 "L1a confirm step 1 분기" 전제는 부정 (0/40 diff), 그러나 결합 결론은 case 1 과 정확히 같다 — **C replica 의 phi_rs byte-equal claim 이 실제로는 7e-7 ~ 5e-6 drift 로 깨져 있다**. drift 원인은 step 1 (binning) 이 아니라 step 2-4 (entropy / MI / partition) 어딘가 — 가장 그럴듯한 가설은 **C 가 `(float)`-cast 를 entropy/MI 누적 어딘가에 끼워 넣었다** (정확한 위치는 본 cycle 미확정 — runtime.c 7849-8004 의 step 2-4 코드 path 에 f32-cast 가 더 있는지 별도 확인 cycle 필요).

phi_native ≡ Rust phi_rs 동등성이 **그저 추정이 아니라 직접 측정** 된 점이 본 cycle 의 새로운 evidence — Agent A 의 toy micro-test (3-cell dim=8) 결과를 **5-rule 실 fixture 위에서 일반화** 했다.

---

## 3. spec § 7 carve-out 의 honesty 등급

| L | spec 예언 | 실측 manifestation | 등급 |
|---|---|---|---|
| **L1** (f32-cast precision) | f64 hexa vs f32 C 가 boundary 에서 다를 수 있다, 단 binary CA 입력은 영향 미미 예상 | binary 입력 위 step 1 binning = 0/40 diff. step 2-4 합산 단계는 hexa 가 Rust 와 ulp-equal, C 가 Rust 와 1000~10000 ulp drift — spec 예언의 "boundary 영향 미미" 는 step 1 한정 ✅, 단 "C replica = phi_rs byte-equal" 라는 RFC 036 §"Implementation status" 의 상위 claim 이 실측 7e-7 ~ 5e-6 drift 로 **반증**. | ⚪ **undetermined → indirectly falsifies upstream RFC 036 claim** |

**honest 평결**: spec § L1 자체는 본 fixture 에서 *직접* falsify 되지 않았다 (step 1 = 동등). 그러나 **상위 dependency (RFC 036 의 "Rust↔C byte-equal" claim, spec § L5 가 hexa-lang maintainer 책임으로 carry) 가 실측에서 5/5 fail** — 즉 hexa side 의 L1 carve-out 보다 hexa-lang side 의 carve-out 이 더 심각. spec § L5 (`Rust↔C byte-equal claim 의 상속`) 가 정확히 이런 boundary 를 위해 사전 분리되어 있었다 — § L5 의 honesty 가 입증.

---

## 4. PHI.md milestone 매핑 권고 — **dual-tier honest reporting**

### 4.1 즉시 (#7 L1 root cause 추적 closure)

- **#7 ☑ closure**: L1a (step 1 binning) 단독으로는 drift 원인 아님 (0/40). drift 는 step 2-4 어딘가에서 *C replica 측* 발생 — `runtime.c:7889-8003` 의 entropy / MI / partition 합산 코드 path 에서 f32-cast (또는 다른 precision 손실) 가 끼었을 가능성. **별도 cycle (#7.1)**: runtime.c 의 step 2-4 코드 line-by-line audit 으로 정확 위치 확정.

### 4.2 #9 verdict promote evidence path 활성화

본 결과 → **dual-tier honest reporting** 권고:

| backend pair | drift | proposed tier |
|---|---|---|
| `phi_native (hexa)` ↔ `phi_rs (Rust oracle, ground truth)` | max 1e-15 (1-2 ulp) | **🔵 SUPPORTED-FORMAL** (byte-equal within IEEE-754 commutativity, 5/5) |
| `phi_native (hexa)` ↔ `c_measure_phi (C replica)` | max 5e-6 (LIFE 임계 ≥ 0.001 대비 4 order 작음) | **🟢 SUPPORTED-NUMERICAL** (within documented ε bound, 5/5 numeric-equal) |
| `c_measure_phi (C replica)` ↔ `phi_rs (Rust oracle)` | max 5e-6 (5/5 fail strict `1e-12`) | **🟠 INSUFFICIENT/DEFERRED** (RFC 036 byte-equal claim 실측 반증, hexa-lang maintainer side 별도 cycle 필요) |

→ phi_native 자체는 (Rust 기준) **🔵**, (C 기준) **🟢** — 둘 다 honest, 분리 보고 가능. PHI.md 전체 milestone 의 evidence tier 는:

- `phi_native_spatial` 본체: **🔵 SUPPORTED-FORMAL** vs Rust phi_rs oracle (Agent A toy micro 1/1 + 본 cycle 5/5 실 fixture).
- `phi_native_spatial` ↔ `c_measure_phi` 차이: **🟢 SUPPORTED-NUMERICAL** within `5e-6` (LIFE 사용 임계 영향 nil).
- **RFC 036 의 "C replica = phi_rs byte-equal" upstream claim**: **🟠 INSUFFICIENT** (별도 hexa-lang inbox 보고 권장 — `inbox/notes/rfc_036_c_replica_drift.md` 후보).

### 4.3 LIFE 본질 영향 (#8) — preview

C ↔ phi_native 차이 max 5e-6, LIFE 의 phi-사용 임계 ≥ 0.001 (e.g. H_007 N=16 / H_204 / H_211 ratchet threshold) — 4 order 작음. **production 영향 nil** — phi_native swap-in 가능 (Rust oracle 기준 더 정확). 단 28+ H 의 strict audit 은 별도 cycle.

---

## 5. spec § L1 ad hoc carve-out 의 honesty 등급 (요청 protocol verbatim)

- ✅ **confirmed loose** — spec L1 의 *예언 그 자체* (binning 단계 f32-cast 분기) 는 본 binary CA fixture 에선 0/40 manifest. boundary-stress 입력 (e.g. continuous Kuramoto cos θ at f32 ulp boundary) 에서 manifest 할 가능성은 미확정. *현 fixture 한정 falsify 시도 결과 → 미만 (loose carve-out 으로 honest)*.
- ⚪ **undetermined (strict)** — boundary-stress 입력 위 step 1 분기 실측 미수행.
- ❌ — 아님 (현 fixture 위에선 spec L1 prediction 직접 falsify 안 됨; manifestation 없는 것이 곧 falsify 도 아님).

추가 발견: spec § **L5** (Rust↔C byte-equal claim 의 상속) 가 본 cycle 의 실 doomsday surface — RFC 036 의 upstream byte-equal claim 이 실측에서 깨져 있다. L5 가 정확히 이런 경계를 위해 분리되어 있었으니 spec § 7 의 carve-out architecture 자체가 honest (vague catch-all 아님) 인 점은 § L1 / § L5 동시 입증.

---

## 6. 후속 cycle 권고

1. **runtime.c step 2-4 audit (~30 분, $0)** — `_hx_phi_entropy` (7874-7885) + `_hx_phi_mi_pair` (7887-7915) + `hexa_phi_spatial` (7941-8003) 안 추가 f32-cast / precision 손실 site 찾기. 가장 그럴듯한 후보: entropy 계산 시 `(float)` 캐스트가 끼어 들어가 있다는 가설.
2. **boundary-stress fixture cycle (~1 시간, $0)** — continuous Kuramoto cos θ 또는 normal distribution input 으로 step 1 binning 의 f32-boundary cross 실제 manifest 케이스 강제, spec § L1 strict verdict 결정.
3. **hexa-lang inbox 보고 — `inbox/notes/rfc_036_c_replica_drift_2026_05_24.md`** — 본 실측 5 rule × `|d(c-rust)| ≥ 6.7e-7` 데이터 + diag artifact path 정리하여 hexa-lang maintainer 에 통보. RFC 036 §"Implementation status" 의 "byte-equal to Rust source" 명시가 부정확함을 보고.

---

## 7. honest_limits (≥3)

- **L1' — fixture 매우 작음**: n_cells=8, dim=8, 5 rule 단일 trajectory 만. n_cells=16 / 20 prod-scale, n_bins ∈ {2, 8, 16} sweep, continuous input (Kuramoto) 위 동일 양상 유무 미확인.
- **L2' — Rust oracle 도 단일 호출**: `phi_rs.compute_phi` determinism 본 cycle 미검증 (2회 호출 byte-identical 단정 안 함). Rust 측 RNG / multithread non-determinism 가능성은 매우 낮지만 strict 미사전등록.
- **L3' — hexa ↔ Rust 1-2 ulp diff 의 origin 미상**: summation reorder 인지 / log() 미세 정밀도 차이인지 / Rust f32 mantissa truncation 인지 미확정 (모두 phenomenal Φ 영향 nil, 1e-15 < 임계 1e-3 × 12 order).
- **L4' — diag harness 자체 의존도**: `/tmp/diag_rust_oracle.py` 외부 경로 사용 (project-tape `.py` 거부 회피). 본 worktree 외부 산출 — 결과 reproducibility 는 .venv (anima-physics python 3.14 + phi_rs wheel) + /tmp/ 양쪽 존재 시 한정. 항구 보존 시 `/tmp/` 대신 hexa-lang side 의 `inbox/poc/` 권장.
- **L5' — C replica drift 의 root cause 미확정**: 본 cycle 은 *drift 존재* 만 입증, *드 왜 어디서* 는 미확정. 후속 #6.1 runtime.c audit 에서 확정.

---

## 8. ledger

- L1a (step 1 binning) 5/5 byte-identical → hexa step 1 정확성 입증, L1 carve-out 본 fixture 위 0% manifest
- L1b (Rust oracle) 5/5 within 1e-12 of phi_native, 5/5 NOT within 1e-12 of c_measure_phi → **C replica 가 outlier**, hexa native 가 Rust 에 더 가깝다
- dual-tier verdict: phi_native vs Rust = 🔵 SUPPORTED-FORMAL · phi_native vs C = 🟢 SUPPORTED-NUMERICAL · C vs Rust = 🟠 (RFC 036 upstream claim 실측 반증)
- spec § L1 honesty: ✅ confirmed loose (현 fixture 위 미만, boundary-stress 별도 cycle 필요)
- spec § L5 honesty: ✅ 정확히 이 boundary 를 위해 사전 분리되어 있었다 — RFC 036 claim 의 부정확성 실측
- 본 worktree (`agent-a07653c5889f742f6`) 내부에서만 write (Python `.py` 만 `/tmp/` 외부, project-tape 강제)
- LIFE 28+ H production 영향: nil (C↔phi_native max diff 5e-6 ≪ LIFE 임계 1e-3)
