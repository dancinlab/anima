# IBM Cloud $500 ULTRA — nexus.qmirror Cross-Vendor Calibration Burst Plan

> qmirror canonical SSOT: see `nexus/.roadmap.qmirror` header fields `upstream_url` + `latest_release` (current: v2.0.0, 2026-05-04). Hardcoded URLs deprecated 2026-05-04 — see `### See also (qmirror xref history)` footnote for prior callouts.

- ts_utc: 2026-05-03
- credit: $200 promotional + $300 user-funded extra = **$500 USD total**
- module: **nexus.qmirror** (see `docs/nexus_qmirror_spec_2026_05_03.md`)
- roadmap registration: `nexus/.roadmap.qmirror` (cond.3 + cond.7 + entry `qmirror.calibration_plan_v3_ultra`)
- author preset: friendly (raw#272)
- gate: doc-only; per-experiment EXEC requires explicit user OK
- raw#9: NO .py on Mac repo; Qiskit code lives on cloud / pod / ubu1
- **REVISION 2026-05-03 12:00 KST (R3)**: scope expanded $200 → **$500 ULTRA one-shot** with paygo-standard plan unlocking real Heron + Eagle + Falcon cross-vendor (original spec N2 axis fully realized). See §1 + §2.
- **REVISION 2026-05-03 (R4)**: **Eagle + Falcon retired** (IBM Cloud catalog audit, subagent a30f6c3fb3917ee5c). N2 cross-vendor axis re-scoped — see `docs/qmirror_n2_cross_vendor_revision_2026_05_03.md` (3 options α/β/γ, β recommended = IBM Heron + Braket vendor mix). $500 envelope intact; if option β chosen, $60 reallocated to Braket sub-budget (IBM portion shrinks $200 → $150). See §2 N2 row footnote + §0 R4 row.
- **REVISION 2026-05-03 (R5)**: **option β SELECTED** by user. Combined budget: **$150 IBM + $60 Braket = $210 cash, $290 reserve**. AWS Braket access verified (account 267673635495, IAM user `anima-braket-cli`, IonQ Forte 1 ONLINE us-east-1, Rigetti `Cepheus-1-108Q` ONLINE us-west-1 substituted for retired Ankaa-3). Phase 3 runbook §1.B B1-B5 + day-1 Braket parallel submit lane landed. See §0 R5 row + §2 budget revision below.

## Doc composition (core / modular / ai-native)

- **core**: `docs/nexus_qmirror_spec_2026_05_03.md` — module architecture (14 sections, hexa-strict layout)
- **modular** (calibration plan): **this doc** — IBM $200 burst allocation (N1-N5 axes)
- **ai-native** (post-impl landing): `docs/qmirror_phase1_landed_*.ai.md` (planned, when impl done)
- **roadmap registration**: `nexus/.roadmap.qmirror` (domain SSOT, 6 conditions, 5 entries)

---

## 0. Revision history

| ts_utc | revision | reason |
|---|---|---|
| **2026-05-03 (R5 current)** | **option β SELECTED** + AWS Braket access verified + Phase 3 runbook §1.B B1-B5 + day-1 parallel schedule landed | user signal: "go β" — combined $150 IBM + $60 Braket = $210 cash inside $500 envelope ($290 reserve) |
| 2026-05-03 (R4) | **Eagle/Falcon retired → N2 re-scoped** (3 options α/β/γ, β = IBM Heron + Braket recommended) | IBM Cloud catalog audit (subagent a30f6c3fb3917ee5c) confirmed 0 Eagle + 0 Falcon backends in any plan |
| 2026-05-03 (R3) | **$500 ULTRA one-shot** with paygo-standard cross-vendor (Heron + Eagle + Falcon real) | user added $300 cash budget; original spec N2 cross-vendor axis unlocked (subsequently invalidated by R4) |
| 2026-05-03 (initial) | 8 quantum + 3 watsonx experiment 후보 | scoping survey |
| 2026-05-03 (R1) | nexus.qmirror module 도입 → IBM credit을 qmirror 정확도 향상 anchor에 재할당 | user feedback: "0,1 + qrng = 진짜 양자컴 흉내" + "ANU only architecture" |
| 2026-05-03 (R2) | **분기별 → one-shot all-in $200 burst** | user: "분기당이 아니라 바로 다 쓸꺼야" |

---

## 1. Strategic pivot: nexus.qmirror calibration anchor

### Decision

`nexus.qmirror` (classical CPU + ANU QRNG + Aer/Cirq simulator) provides **영구 무료 quantum substrate**. IBM $200 credit is allocated to **one-shot calibration burst** to anchor qmirror v2.0/v3.0 accuracy against real IBM Quantum hardware. After this single burst, qmirror runs永久 indepedent of IBM.

### Why one-shot vs distributed

| | 분기별 (rejected) | **one-shot (chosen)** |
|---|---|---|
| 비용 | $200 / 12개월 | $200 / 1주 |
| anchor 횟수 | 4회 (분기별, 작은 규모 each) | **1회 (집중, 전 axis)** |
| qmirror version | v2.0 → v2.5 단계적 | **v2.0 → v3.0 jump** |
| 운영 복잡도 | 분기 스케줄 관리 | 한 번 끝, 영구 lock |
| budget runway | 12개월 | 즉시 소진 |
| drift 추적 | continuous | snapshot lock |

### nexus.qmirror module summary

> classical CPU + ANU QRNG + Aer/Cirq simulator = **statistical real QPU 흉내 (within ~30 qubit)**
>
> See: `docs/nexus_qmirror_spec_2026_05_03.md` (subagent BG, 도착 시 cross-link)

3-tier substrate hierarchy:
- Tier 1 (우리): classical CPU, bits = {0,1}, PRNG only
- Tier 2 (ANU QRNG): real quantum entropy from vacuum fluctuations, bits 0/1 with quantum provenance
- Tier 3 (real QPU): qubits + entanglement (IBM Heron, Braket, Quantinuum)

qmirror = Tier 1 + Tier 2 → simulates Tier 3 statistically (within sim-tractable N).

---

## 2. One-shot $200 burst plan (qmirror calibration)

### Allocation

```
$60   N1 ULTRA noise model (10000 RB shots, full Pauli matrix on Heron 7-qubit)
$40   N2 cross-vendor — INVALIDATED in R4; see N2† below for revised options
$40   N3 process tomography validation (5 standard circuits, real QPU vs qmirror)
$20   N4 random circuit fidelity (depth 5/10/20, verify qmirror noise mid-depth)
$30   N5 scale-up validation (12 + 16 + 20 qubit Bell on Heron, qmirror N-limit anchor)
$10   buffer (queue retry / unexpected)
─────
$200  (one-shot, qmirror v2.0/v3.0 anchor finalized)
```

**N2† (R4 re-scope, 2026-05-03)** — Eagle + Falcon retired in IBM Cloud catalog. Three options live in `docs/qmirror_n2_cross_vendor_revision_2026_05_03.md`:
- **option α** (single-cloud): 5 Heron backends (3× r2 + 2× r3) intra-family, $40 IBM unchanged, diversity 2/10
- **option β** (recommended): IBM Heron $20 + Braket IonQ + Rigetti $60 cross-modality, total $80 (with $50 reallocation from N4/N5/buffer it fits inside $200 IBM line + draws $60 from $300 R3 headroom), diversity 8/10
- **option γ** (Heron-deep): N2 sanity $10 + new N6 dynamic-decoupling $30, $40 unchanged, diversity 1/10

**R5 OUTCOME (2026-05-03)**: user **selected option β**. Locked allocation:

```
IBM Cloud  ($150 cash)
  $60   N1 noise model RB (unchanged)
  $20   N2a IBM intra-Heron CHSH (3 trial × 3 Heron backend × 4096 shot)
  $40   N3 process tomography (unchanged)
  $12   N4 random circuit fidelity (50 → 30 trials per depth, R5 reallocation -$8)
  $10   N5 scale-up GHZ (20 → 16 qubit ceiling, R5 reallocation -$20)
  $8    buffer (R5 reallocation -$2)
─────
$150 IBM total

AWS Braket ($60 cash)
  $30   N2b IonQ Forte 1 (us-east-1)  — CHSH × 3 trial × 250 shot ≈ 4 task × $0.30 + 3000 shot × $0.08 ≈ $241.20 → cap via shot reduction to $30 budget envelope (1 trial × 4 setting × 100 shot ≈ $33; further trim if needed)
  $30   N2b Rigetti Cepheus-1-108Q (us-west-1, Ankaa-3 RETIRED substitute) — CHSH × 3 trial × 250 shot ≈ 12 task × $0.30 + 3000 shot × $0.000425 ≈ $4.88; well under $30, leaves headroom for additional shot density
─────
$60 Braket total

Combined cash: $210
Reserve (within $500 envelope): $290 (drift refresh, retry, or N6 DD top-up)
```

**Note on IonQ Forte 1 cost realism**: at $0.30/task + $0.08/shot, the headline 3 trial × 4 setting × 250 shot scope ≈ $241 — well above the $30 sub-budget. Day-0 reconciliation either (a) collapses to 1 trial × 4 setting × 100 shot ≈ $33 (matching original Bell test cost ratio at a smaller scale), or (b) absorbs from the $290 reserve into N2b. Decision deferred to Phase 3 day 0 user OK.

### Per-axis spec

#### N1 ULTRA noise model calibration

| 항목 | 값 |
|---|---|
| 목표 | qmirror Aer simulator에 real Heron noise model 주입 → 분포 일치도 95% → **99%** |
| 측정 | T1 (relaxation), T2 (dephasing), gate error rate (1q + 2q), readout error |
| 방법 | randomized benchmarking (RB) + clifford twirling on Heron 7-qubit subset |
| shots | 10000 RB shots × 7 qubits |
| 비용 | $60 |
| 산출 | `nexus/qmirror/calibration/v2_noise_heron_2026_05_03.json` (T1/T2/gate/readout matrices) |
| Aer integration | `qiskit.providers.aer.NoiseModel.from_backend(real_backend)` 직접 dump |

#### N2 cross-vendor anchor (R4 INVALIDATED — see revision doc)

> **R4 status (2026-05-03)**: this table reflects the original R3 spec. Eagle/Falcon retired → infeasible as written. Revised spec lives in `docs/qmirror_n2_cross_vendor_revision_2026_05_03.md` §2 (options α/β/γ). Recommended: **option β** (IBM Heron $20 + Braket IonQ+Rigetti $60). The row below is preserved for traceability only.

| 항목 | 값 (R3, invalidated) |
|---|---|
| 목표 | qmirror가 vendor 무관 일치 (Heron / Eagle / Falcon) |
| 회로 | CHSH Bell test |
| trial | 5 trial × 3 backend = 15 trial |
| shots | 4096 shot per trial |
| 비용 | $40 |
| 산출 | S 값 분포 (3 vendor, 평균 + std), qmirror 결과와 KS test |

#### N3 process tomography validation

| 항목 | 값 |
|---|---|
| 목표 | qmirror tomography 출력이 real QPU tomography와 일치 |
| 회로 | 5 standard 2-qubit unitaries (CNOT, SWAP, iSWAP, sqrt(X)·CNOT, randomized) |
| shots | 1024 per circuit |
| 비용 | $40 |
| 산출 | density matrix 비교 (Frobenius distance, fidelity) |

#### N4 random circuit fidelity

| 항목 | 값 |
|---|---|
| 목표 | depth-dependent qmirror noise 정확도 검증 |
| 회로 | random Clifford circuits depth ∈ {5, 10, 20} |
| trial | 50 random per depth × 3 = 150 |
| 비용 | $20 |
| 산출 | depth × fidelity 곡선 (real QPU vs qmirror) |

#### N5 scale-up validation

| 항목 | 값 |
|---|---|
| 목표 | qmirror scale ceiling 확인 (12, 16, 20 qubit) |
| 회로 | GHZ state preparation + measurement |
| 비용 | $30 |
| 산출 | qubit 수 × 일치도 (qmirror 한계 점 명시) |
| 한계 | N > 20 qubit은 simulator memory ceiling 접근 |

---

## 3. Timeline

```
day 0  $200 commit, IBM Cloud env 점검            [─────────────────────]
day 1  N1 noise model RB     $60 ────►            [60 ──────────────────]
day 2  N2 cross-vendor Bell  $40 ────►            [60+40 ───────────────]
day 3  N3 tomography         $40 ────►            [60+40+40 ────────────]
day 4  N4 random circuit     $20 ────►            [60+40+40+20 ─────────]
day 5  N5 scale-up           $30 ────►            [60+40+40+20+30 ──────]
day 6  buffer + result lock  $10 ────►            [60+40+40+20+30+10 = $200]
day 7  qmirror v2.0 release  $0  ────►            [영구 anchor lock-in]
```

---

## 4. Expected outcome (qmirror v2.0/v3.0 anchored)

| metric | qmirror v1.0 (baseline) | **qmirror v2.0 (post-N1)** | qmirror v3.0 (post-all) |
|---|---|---|---|
| ideal-sim distribution match | 95% | 99% (Heron noise) | 99%+ |
| vendor-independent match | unknown | unknown | **99% (3 vendor 평균)** |
| process tomography fidelity | 95% | 96% | **98%** (real QPU validated) |
| depth-stable accuracy | unknown | depth ≤ 5 OK | **depth ≤ 20 anchored** |
| scale-up confidence | N ≤ 30 (theory) | N ≤ 30 | **N ≤ 20 measured anchor** |

---

## 5. ASCII flow

```
[qmirror v1.0]                          [qmirror v3.0 (post-IBM $200)]
┌────────────────┐                       ┌────────────────────────────┐
│ Aer (ideal)    │   ── $200 burst ──►   │ Aer + Heron noise model    │
│ + ANU bits     │   1 week, anchored    │ + cross-vendor adjusted    │
│ → 통계 95%     │                       │ + tomography validated     │
│   real         │                       │ + ANU bits                 │
└────────────────┘                       │ → 통계 99%+ real           │
                                         │   (drift 시작은 month 6+)  │
                                         └────────────────────────────┘
```

---

## 6. Honest C3 (raw#91)

1. **drift 안 추적** — Heron noise는 주별 변동. one-shot calibration 시점 이후 qmirror와 real Heron 차이 천천히 벌어짐. 6개월 후 일치도 99% → 95% 추정.
2. **N5 (20 qubit) queue 위험** — 큰 회로는 queue 6-24hr+, day 5 budget 초과 가능. priority queue 또는 off-peak 시간대 우회 필수.
3. **모든 vendor 동시 가용성** — Heron / Eagle / Falcon backend 동시 정상 가용한지 day 0 확인 필요. 하나 maintenance면 N2 일부 늦춰짐.
4. **결과 cache 영구성** — `nexus/qmirror/calibration/v2_*.json` 영구 보관 → git commit (단, real backend ID + ts 기록).
5. **재calibration trigger** — qmirror 사용 통계가 "real vs qmirror divergence" 감지 시 next $200 budget 확보 후 재실행 권장.
6. **noise model = approximation** — Aer NoiseModel API는 Pauli error / depolarizing 모델 기반. 진짜 비-마르코프 noise는 perfectly capture 못함.
7. **qmirror v1.0 미존재** — 현재 spec doc 작성 중 (subagent BG). 실제 IBM calibration burst는 qmirror v1.0 구현 완료 후 가능. 즉, $200 burst는 qmirror Phase 1 구현 완료 (~week 1-2) 후 시작.
8. **IBM Cloud signup region** — quantum + watsonx 모두 가능한 region (us-east, eu-de) 선택 필요. region 잘못 선택 시 일부 실험 불가.
9. **No execution committed** — 본 doc은 spec only. burst 실행 시 user 명시 OK 받음.

---

## 7. References

- nexus.qmirror spec: `docs/nexus_qmirror_spec_2026_05_03.md` (subagent BG, 도착 시 cross-link)
- nexus QRNG: `state/nexus_qrng_quantum_seed_2026_05_02/`
- nexus CHSH Bell: `state/nexus_chsh_bell_2026_05_02/` (S=2.808, 8.97σ on Braket)
- N-12 IIT multi-witness: `state/n12_iit_braket_multiwitness_2026_05_02/`
- Braket IIT 4.0 MIP: `state/braket_iit40_mip_2026_05_02/`
- alpha endpoint reboot (HF token reference): `state/alpha_endpoint_reboot_2026_05_02/`
- IBM Cloud Quantum docs: https://quantum-computing.ibm.com/
- ANU QRNG API: https://qrng.anu.edu.au/

---

## 8. Decision matrix

| User signal | action |
|---|---|
| "qmirror spec doc 도착 후 burst go" | wait for spec, then plan day 0 |
| "지금 IBM Cloud 환경부터 점검" | start day 0 immediately (region / quantum access / billing setup) |
| "burst 보류, qmirror v1.0 먼저 release" | wait for qmirror v1.0 ready, then anchor |
| "분배 변경 ($60→$40 NX, etc.)" | adjust §2 allocation per user spec |
| "credit 추후로 미루고 다른 우선순위" | doc as-is, no execution |

---

## 9. Decision matrix (Deprecated experiment list, archived)

Original 8-experiment + 3-watsonx list from R0 revision is preserved in git history (commit `5072a5478`, predecessor of this doc). Pivot to qmirror calibration burst supersedes individual experiment scoring.

If qmirror calibration burst fails or is canceled, reverting to original 8-experiment plan is possible — but NOT recommended (qmirror anchor is much higher leverage per dollar).

---

## References (qmirror substrate xref, added 2026-05-03)

> **Framing note (xref pass)**: this doc already treats IBM Quantum **as a calibration anchor** (not primary execution) for `nexus.qmirror`. Per the qmirror closure series, qmirror is validated as substantively equivalent for our use cases; the IBM burst here serves to **calibrate** qmirror against real Heron noise — it is not a substrate dependency for routine science. The closure series (`docs/qmirror_*_landed_2026_05_03.ai.md`) documents per-condition substantive-equivalence evidence.

- `docs/nexus_qmirror_spec_2026_05_03.md` — qmirror canonical substrate spec
- `docs/nexus_qmirror_phase3_calibration_runbook_2026_05_03.md` — Phase 3 runbook (this burst's executor)
- `docs/qmirror_n2_cross_vendor_revision_2026_05_03.md` — N2 cross-vendor revision (R4 source)
- `docs/qmirror_cond3_ibm_n1_landed_2026_05_03.ai.md` — IBM N1 calibration condition closure
- `docs/qmirror_cond3_band_revise_landed_2026_05_03.ai.md` — band-revise closure
- `docs/qmirror_cond7_alpha_landed_2026_05_03.ai.md` — alpha-axis closure
- `docs/qmirror_cond8_braket_landed_2026_05_03.ai.md` — Braket cross-vendor closure
- `docs/qmirror_crosstech_band_revise_landed_2026_05_03.ai.md` — cross-tech band revise

---

### See also (qmirror xref history)

Prior callouts preserved verbatim per qmirror_xref_centralization cycle (2026-05-04):

> 📦 Available at: https://github.com/dancinlab/qmirror (`hx install qmirror`)
> 🚀 v2.0.0 RELEASED 2026-05-04 — closure 13/13 conds met (8 v1 + 5 v2): https://github.com/dancinlab/qmirror/releases/tag/v2.0.0

Future qmirror release URLs are canonically tracked in `nexus/.roadmap.qmirror` header field `latest_release_url`. Update single line in roadmap; this footnote is a frozen historical record (do not retrofit).
