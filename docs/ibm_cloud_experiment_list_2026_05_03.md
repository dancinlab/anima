# IBM Cloud $200 — nexus.qmirror Calibration Burst Plan

- ts_utc: 2026-05-03
- credit: $200 USD (IBM Cloud signup)
- module: **nexus.qmirror** (see `docs/nexus_qmirror_spec_2026_05_03.md`)
- roadmap registration: `nexus/.roadmap.qmirror` (cond.3 + entry `qmirror.calibration_plan` + entry `qmirror.phase3_calibration`)
- author preset: friendly (raw#272)
- gate: doc-only; per-experiment EXEC requires explicit user OK
- raw#9: NO .py on Mac repo; Qiskit code lives on cloud / pod / ubu1
- **REVISION 2026-05-03 11:00 KST**: scope pivoted from 8 one-off experiments to **single one-shot $200 burst for nexus.qmirror calibration**. See §1.

## Doc composition (core / modular / ai-native)

- **core**: `docs/nexus_qmirror_spec_2026_05_03.md` — module architecture (14 sections, hexa-strict layout)
- **modular** (calibration plan): **this doc** — IBM $200 burst allocation (N1-N5 axes)
- **ai-native** (post-impl landing): `docs/qmirror_phase1_landed_*.ai.md` (planned, when impl done)
- **roadmap registration**: `nexus/.roadmap.qmirror` (domain SSOT, 6 conditions, 5 entries)

---

## 0. Revision history

| ts_utc | revision | reason |
|---|---|---|
| 2026-05-03 (initial) | 8 quantum + 3 watsonx experiment 후보 | scoping survey |
| 2026-05-03 (R1) | nexus.qmirror module 도입 → IBM credit을 qmirror 정확도 향상 anchor에 재할당 | user feedback: "0,1 + qrng = 진짜 양자컴 흉내" + "ANU only architecture" |
| **2026-05-03 (R2 current)** | **분기별 → one-shot all-in $200 burst** | user: "분기당이 아니라 바로 다 쓸꺼야" |

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
$40   N2 cross-vendor (Heron + Eagle + Falcon — Bell × 5 each, vendor-independent)
$40   N3 process tomography validation (5 standard circuits, real QPU vs qmirror)
$20   N4 random circuit fidelity (depth 5/10/20, verify qmirror noise mid-depth)
$30   N5 scale-up validation (12 + 16 + 20 qubit Bell on Heron, qmirror N-limit anchor)
$10   buffer (queue retry / unexpected)
─────
$200  (one-shot, qmirror v2.0/v3.0 anchor finalized)
```

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

#### N2 cross-vendor anchor

| 항목 | 값 |
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
