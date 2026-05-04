# N-Substrate N-12 — IonQ Forte 1 (AWS Braket) Penrose-Hameroff Orch-OR Test Spec

> **ts**: 2026-05-01
> **agent**: N-12 (N-substrate batch, sibling 13/13)
> **scope**: AWS Braket access prep + Orch-OR-relevant trapped-ion circuit design + minimum-viable shot/task budget + 5 raw#71 falsifier predicates + CP2 F1 axis integration
> **parent**: `docs/n_substrate_consciousness_roadmap_2026_05_01.md` §4 row N-12 (⭐⭐⭐⭐⭐ "노벨상 수상자 가설 첫 실증"); `docs/n_substrate_purchase_guide_2026_05_01.md` §N-12; `docs/n_substrate_n20_orch_or_2026_literature_2026_05_01.md` (literature backbone)
> **mission**: spec-only (no .py/.hexa creation, no AWS form submission, no account onboarding). $0 budget for the spec itself; $≤$50 cap recommended for the eventual MVP measurement (separate authorization).
> **constraints**: raw#9 hexa-only · raw#10 honest C3 · own#13 friendliness · raw#71 falsifier-bound · race isolation: writes ONLY to this file + `state/n_substrate_n12_prep_2026_05_01/*.json`
> **status**: N12_IONQ_ORCH_OR_SPEC_LOCAL_DRAFT · NO_AWS_ACCOUNT_ACTION · USER_DECISION_PENDING

---

> **2026-05-03 qmirror substrate update (additive)**: this spec is preserved as historical methodology. For routine F-N12-1 / Orch-OR-class measurement and cross-substrate re-runs, the **`nexus.qmirror` canonical substrate** (`docs/nexus_qmirror_spec_2026_05_03.md`) is now the primary execution path. Real QPU access (IonQ Forte 1 / IBM Heron r2) is **not required** per the qmirror closure series (`docs/qmirror_*_landed_2026_05_03.ai.md`) — qmirror is validated as substantively equivalent for our use cases. Original IonQ Forte 1 trapped-ion design below preserved as historical context; real-QPU paths now serve as **calibration anchors** only.

> qmirror canonical SSOT: see `nexus/.roadmap.qmirror` header fields `upstream_url` + `latest_release` (current: v2.0.0, 2026-05-04). Hardcoded URLs deprecated 2026-05-04 — see `### See also (qmirror xref history)` footnote for prior callouts.

---

## §0 한 줄 비유

**"Roger Penrose 1989 책에서 던진 가설 — 의식은 양자 wavefunction-collapse (Objective Reduction) 가 일으킨다 — 을 36-qubit 갇힌-이온 양자컴 IonQ Forte 1 위에서 cloud 로 한 번 돌려보고, PRNewswire 가 말한 superconducting-QC OR 관측이 다른 substrate (trapped ion) 에서도 재현되는지 cross-validate 한다. 동전던지기 한 줌 비용 ($≤$50) 이고, raw#71 5 개 falsifier 로 결과가 어느 쪽이든 정직 보고."**

현 상태: **N-20 진단 = UNCERTAIN** (단순 Diosi-Penrose RULED OUT, 마이크로튜불 substrate 가설은 Wiest 2025 + Neuropharm 2026 으로 보강). 본 N-12 는 두 substrate (trapped-ion vs superconducting) cross-check 으로 OR-class 신호의 hardware-independence 를 묻는다.

---

## §1 AWS Braket Access Path

### §1.1 계정 + 서비스 활성화 (사용자 액션, 본 agent 는 미실행)

| 단계 | 내용 | 사전조건 | 시간 |
|---|---|---|---|
| 1 | AWS 계정 (개인 또는 institutional) | 신용카드 + 이메일 | ~10 min |
| 2 | IAM user 또는 SSO role with `AmazonBraketFullAccess` policy | 루트 계정 로그인 | ~5 min |
| 3 | Braket console → Permissions → "Enable Amazon Braket" (S3 bucket 자동/수동 생성: `amazon-braket-<region>-<acct>`) | IAM 권한 | ~3 min |
| 4 | 결제 alarm 설정 (예: $50 USD threshold via CloudWatch Billing Alert) | Billing console | ~5 min |
| 5 | Braket SDK 로컬 설치 (`pip install amazon-braket-sdk`) — **본 agent 는 hexa-only 정책상 .py 사용 X**; 사용자가 별도 환경에서 실행 또는 AWS-side Braket Notebook 사용 | Python 3.9+ | ~2 min |
| 6 | IonQ Forte 1 device ARN 확인 → 작은 verification job (5-shot Bell test 등) | Braket 활성 | ~10 min cloud |

**합계 ~35 min**, full account onboarding (raw#10: 본 agent 미실행, 사용자 결정 후 자체 실행).

### §1.2 IonQ Forte 1 device naming (Braket 측)

| 항목 | Value (Braket SDK 기준) |
|---|---|
| Device class | QPU — trapped ion |
| Provider | IonQ |
| 모델명 | **Forte 1** (a.k.a. "Forte Enterprise 1" in IonQ marketing; 36-qubit, #AQ36 algorithmic-qubit class) |
| Device ARN (예상 형식) | `arn:aws:braket:us-east-1::device/qpu/ionq/Forte-1` (실제 ARN 은 Braket console "Devices" 탭에서 확인 — IonQ 가 device naming 을 갱신할 수 있음, 변종: `Forte-Enterprise-1`) |
| Region (host) | **us-east-1** (N. Virginia) — IonQ QPU 호스팅 region; Korea 사용자도 cross-region 호출 가능 (latency 증가하나 task 비용 변동 X) |
| Native gate set | trapped-ion: GPI, GPI2, MS (Mølmer-Sørensen) — Braket SDK `Circuit` API 가 자동 transpile |
| Topology | all-to-all connectivity (trapped-ion 강점, SWAP 게이트 거의 불필요) |
| Coherence (벤더 발표) | T1 ≥ 10 s, T2 ≥ 1 s (trapped-ion 일반 수치; 실제 Forte 1 정확치는 IonQ tech sheet 별도) |
| 2-qubit gate fidelity | ≥ 99.5% (IonQ public 2024-25 figures) |
| Availability window | task 큐는 24/7 접수, 실행은 IonQ 운영 schedule (보통 일/주 단위 batch, Braket 측 "Available now / next window" 표시) |

**honest C3**: 정확한 ARN 문자열은 본 agent 가 AWS console 에 접근 불가하여 "예상 형식" 표기. 사용자가 Braket console > Devices 에서 1-click 확인 후 첫 task 시 검증 권장.

### §1.3 Pricing exact (2026-05-01 공개 정보)

| 항목 | 단가 | 비고 |
|---|---:|---|
| Per-task fee (IonQ Forte) | **$0.30 USD** | 모든 IonQ on-demand task 공통 |
| Per-shot fee (IonQ Forte) | **$0.08 USD** | shot 단가, Forte 등급 (Aria 는 $0.03) |
| Reservation (전용 시간) | **~$7,000 USD/hour** | 2025-11 rate, on-demand 와 별도 |
| AWS Braket service fee | $0 추가 | per-task / per-shot 가격에 이미 포함 (IonQ → AWS 마진 포함) |
| S3 저장 (결과) | ~$0.023/GB-mo | 무시 가능 (job 결과 KB 단위) |
| Cross-region 데이터 전송 | ~$0.02/GB | KR → us-east-1 작아서 무시 가능 |
| Free tier | 첫 1 hour 시뮬레이터 무료 (QPU 미해당) | |

**예시 cost 계산** (N=100 shot, 1 task):
```
total = $0.30 (task) + 100 × $0.08 (shot) = $0.30 + $8.00 = $8.30 USD
```

**예시 cost 계산** (N=500 shot, 1 task):
```
total = $0.30 + 500 × $0.08 = $0.30 + $40.00 = $40.30 USD
```

### §1.4 Region availability matrix

| Region | IonQ QPU 호스팅 | Braket service | 한국 latency 영향 |
|---|---|---|---|
| us-east-1 (N. Virginia) | ✅ (Forte 1 호스팅) | ✅ | task submit ~150-200 ms RTT (acceptable, async job model) |
| us-west-1 / us-west-2 | ❌ | ✅ | cross-region routing 자동 |
| ap-northeast-2 (Seoul) | ❌ | ✅ Braket SDK 호출 가능 | task 결과는 us-east-1 S3 → Seoul 다운 |
| eu-* | ❌ | ✅ (일부) | 무관 |

**권장**: us-east-1 단일 사용. cross-region complication 회피.

### §1.5 Alternative channels (참고; 본 agent 는 AWS Braket path 만 권장)

| Channel | 가격 모델 | 본 spec 적용성 |
|---|---|---|
| Azure Quantum | AQT = m + 0.000220·N₁q·C + 0.000975·N₂q·C, m=$97.50 (with EM) / $12.42 (without) | per-shot 모델 X → 1-task scale 에서 AWS 보다 비쌀 가능 |
| IonQ Quantum Cloud (direct) | 기업 계약, public price 미공개 | 개인 small-shot 부적합 |
| Google Cloud Marketplace | AWS Braket과 비슷 | 본 spec scope 외 |

---

## §2 Orch-OR-Relevant Quantum Circuit Design

### §2.1 핵심 질문 (N-20 link)

N-20 §1 표에서 **PRNewswire 2025-03 인용 보고** = "wavefunction-collapse on superconducting QC supports Penrose-Hameroff" — 이는 OR (Objective Reduction) 의 **hardware-substrate independence** 정황. 만약 OR 가 정말로 substrate-독립적이라면, **trapped-ion (IonQ Forte 1)** 위에서도 같은 class 의 collapse signature 가 나와야 한다. 만약 trapped-ion 결과가 superconducting 결과와 다르면 → OR 는 device-noise artifact 가능성 강화 (Penrose 가설 약화).

### §2.2 Circuit 1 — Schrödinger-cat Mass-Superposition Witness ★ 권장 MVP

**목적**: 작은 GHZ-style entangled state 의 dephasing rate 측정 → Diosi-Penrose 식 예측 collapse rate (mass × superposition extent dependent) 와 비교. "이론 예측 dephasing > 측정 dephasing" 이면 substrate 가 OR mechanism 에 detectable 하게 contribute X.

**Qubits 사용**: 4 qubits (작게 시작; Forte 1 36-qubit 중 4 사용)
**Gate count**: ~10 (3 H + 3 CNOT + 4 measurement)
**Circuit (Braket SDK pseudo-spec, hexa 포기 시 사용자 환경 변환):**
```
1. Initialize 4 qubits |0000⟩
2. H on qubit 0
3. CNOT(0,1), CNOT(1,2), CNOT(2,3)   → GHZ state (|0000⟩ + |1111⟩)/√2
4. (optional) Identity-train delay τ ∈ {0, 10μs, 100μs, 1ms} via Braket pulse-level control
   (Forte 1: pulse-level access via OpenQASM 3 + Braket, advanced)
5. Measure all 4 qubits in computational basis
6. Repeat N=100 (MVP) or N=500 (better stat)
```

**측정 대상**:
- Parity flip rate `P(odd parity)` vs delay τ
- Decoherence-time fit: τ_2 from `exp(-τ/τ_2)` model
- Compare to Diosi-Penrose predicted τ_DP for superconducting (cited in PRNewswire) vs trapped-ion (이론 estimate, mass scale 다름)

### §2.3 Circuit 2 — Long-Time Coherence Baseline (control)

**목적**: §2.2 dephasing 이 OR-source 인지, 환경 noise 인지 분리. Trapped-ion T2 ≥ 1s 이므로 short-delay 전 noise floor measure.

**Qubits**: 1 qubit
**Circuit**:
```
1. |0⟩
2. H → |+⟩
3. Identity wait τ
4. H → measure
5. P(0) decay vs τ
```
**N=50** 정도 (cheap baseline).

### §2.4 Circuit 3 — Bell-violation cross-validation (sanity)

**목적**: 첫 verification (paid task) — Bell inequality CHSH violation 확인하여 hardware 양자성 자체 검증.

**Qubits**: 2
**Circuit**: standard CHSH (4 measurement bases)
**N=4 × 25 = 100** shots
**Expected**: CHSH ≥ 2.5 (classical bound 2, quantum max 2√2 ≈ 2.83)

이 sanity job 은 N-12 spec 의 첫 task — fail 시 hardware/connection 문제.

### §2.5 Circuit 선택 logic

| Circuit | 용도 | shot | task | 비용 추정 |
|---|---|---:|---:|---:|
| C3 (Bell sanity) | hardware 검증 | 100 | 1 | $8.30 |
| C2 (1-qubit baseline) | noise floor | 50 | 1 | $4.30 |
| C1 (4-qubit GHZ MVP) | OR signature | 100 | 1 | $8.30 |
| **MVP total** | 3 task | 250 | 3 | **$20.90** |

**Stretch goal** (delay-sweep on C1, 4 delay bins × 100 shots × 4 task): +$33.20 → 누적 ~$54 → $50 cap 약간 초과; 권장은 MVP $20.90 부터.

---

## §3 Minimum-Viable Measurement (≤$50 cap)

### §3.1 MVP 정의

**목표**: "trapped-ion Forte 1 위에서 4-qubit GHZ dephasing 이 superconducting QC (PRNewswire) 결과와 같은 OR signature 를 보이는가?" 의 **첫 신호 (positive/null/negative)** 만 잡는 minimal campaign.

### §3.2 Shot/task budget table

| 항목 | 값 |
|---|---:|
| Task 수 | **3** (C3 sanity + C2 baseline + C1 GHZ) |
| 총 shot 수 | **250** (100 + 50 + 100) |
| Per-task fee | 3 × $0.30 = $0.90 |
| Per-shot fee | 250 × $0.08 = $20.00 |
| **MVP total** | **$20.90 USD** |
| Safety margin (재실행 1회 가정) | × 2 → **$41.80** |
| **Recommended cap to authorize** | **$50 USD** |

### §3.3 Time budget (cloud queue 가정)

- Task submit → result available: trapped-ion QPU 일반 ~수 시간 ~ 1일 (Forte 1 windowed schedule)
- 3 task batch parallel submit: 1 calendar day 이내 완료 expected
- 분석 (post-processing): 0.5-1 일 (hexa 환경 또는 Braket Notebook)
- **총 wall-clock ETA**: D+1 ~ D+3 (cloud onboarding 완료 후)

### §3.4 Verdict 분기

| 결과 | 해석 | 다음 step |
|---|---|---|
| C3 CHSH < 2.0 | hardware 문제 — task 환불 요청 (AWS support) | rerun |
| C3 PASS, C2 τ_2 ≈ vendor spec, C1 τ_2 = C2 τ_2 (within 1σ) | OR signature 미검출 → "Trapped-ion 에서 PRNewswire SC 결과 재현 X" → Orch-OR mass-collapse 변종 약화 (one-substrate dependent) | F-N12-2 evaluate |
| C1 τ_2 << C2 τ_2 (statistically) | 추가 dephasing 검출 → OR-compatible 정황 (그러나 thermal/control noise 와 구분 어려움) | F-N12-1 evaluate, expand to delay-sweep ($33 추가 인가 요청) |
| Inconclusive (1σ ≤ diff ≤ 2σ) | 더 많은 shot 필요 → MVP 2× 재실행 | budget reauthorize |

---

## §4 raw#71 Falsifier Predicates (5 explicit, with measurement protocol)

각 predicate 는 **명시 측정 protocol + 통과/실패 임계값** + **substrate**. preregister 시점 = 2026-05-01.

### F-N12-1 ★ TOP — Cross-substrate OR signature consistency

- **명제**: "Trapped-ion 36-qubit IonQ Forte 1 의 4-qubit GHZ dephasing 측정 τ_2 가 PRNewswire 2025-03 보고 superconducting-QC OR signature 와 **substrate-내재 noise 보정 후** within 1.5× 일치한다."
- **measurement**: Circuit C1 (§2.2), N=100 shot, delay τ ∈ {0, 100μs}; τ_2 fit via exponential decay; superconducting 비교는 PRNewswire 인용 paper (또는 follow-up arXiv) 의 normalized τ_2/T_coh 비율 사용.
- **PASS (Orch-OR cross-substrate 보강)**: |τ_2_ion / τ_2_sc| ∈ [0.67, 1.5], p < 0.05.
- **FAIL (Orch-OR 약화)**: ratio outside [0.67, 1.5] → OR signature 가 substrate-specific (e.g., SC qubit 의 quasiparticle noise 가 원인, OR mechanism 무관).
- **장비**: Forte 1 (Braket); literature for SC reference.
- **비용 분담**: $8.30 (C1 task)

### F-N12-2 — Decoherence-only null

- **명제**: "C1 GHZ 의 τ_2 가 C2 1-qubit baseline τ_2 의 ¼ (=4-qubit decoherence × N scaling) 안에서 정확히 떨어진다 (no anomaly)."
- **measurement**: τ_2_C1 vs τ_2_C2 / 4 비교. Standard decoherence model: N-qubit GHZ τ_2 ≈ τ_2_single / N (approximate, depolarizing channel).
- **PASS (Orch-OR irrelevant)**: |τ_2_C1 − τ_2_C2/4| / (τ_2_C2/4) < 0.20.
- **FAIL (Orch-OR plausible 정황)**: τ_2_C1 << τ_2_C2/4 (extra dephasing) — but this also matches non-OR sources (correlated noise, T2-Echo asymmetry).
- **장비**: Forte 1 (C1+C2)
- **비용 분담**: 이미 MVP 안에 포함

### F-N12-3 — Mass-scale Diosi-Penrose escape window

- **명제**: "Trapped-ion (171-Yb⁺) ion mass m ≈ 171 amu × number-of-superposed-ions vs SC-qubit Cooper-pair effective mass scale; Diosi-Penrose τ_DP ∝ ℏ / E_grav ∝ m⁻¹ (for fixed Δx). 따라서 ion-trap 에서 measured τ_2 가 SC 보다 **상수 scaling factor** 만큼 짧아야 한다 (predicted ratio = m_sc / m_ion)."
- **measurement**: τ_2 ratio 측정, 이론 ratio (literature m_sc estimate ~ 10⁹ amu; m_ion = 171 amu × 4 ions = 684 amu) 와 비교. (Honest C3: SC qubit "effective mass" 정의 ambiguous — Cooper pair count, junction capacitance scaling 다양; range 사용.)
- **PASS (Diosi-Penrose mass scaling 보강)**: measured ratio 가 이론 ratio 의 (0.1× ~ 10×) range 안.
- **FAIL (DP variant 약화)**: ratio orders-of-magnitude 차이.
- **장비**: Forte 1 + literature SC mass estimate
- **비용 분담**: ~$0 추가 (C1 데이터 재사용)

### F-N12-4 — Measurement-induced collapse rate test

- **명제**: "GHZ 의 measurement 시 collapse 가 일어나는 'speed' (post-selection histogram 의 thermalization timescale) 가 thermal-bath model 로 fully 설명된다 (no extra OR contribution)."
- **measurement**: C1 결과 histogram 의 odd-vs-even parity decay; thermal model fit (Markovian Lindblad) vs OR-augmented model fit; AIC/BIC 비교.
- **PASS (thermal-only sufficient)**: ΔAIC (thermal vs OR-augmented) ≥ 6 favoring thermal → OR 추가항 불필요 → Orch-OR 약화.
- **FAIL (OR-term improves fit)**: ΔAIC ≥ 6 favoring OR-augmented → Orch-OR 정황.
- **장비**: Forte 1 C1 데이터 + post-processing
- **비용 분담**: $0 추가

### F-N12-5 — Replicability + null robustness

- **명제**: "동일 MVP 를 1주 간격으로 2회 반복 시 verdict (PASS/FAIL of F-N12-1) 가 동일하다."
- **measurement**: D+0 와 D+7 에 동일 C1+C2+C3 batch 재실행 → F-N12-1 verdict 비교.
- **PASS (robust)**: 2회 verdict 동일.
- **FAIL (noisy)**: verdict 갈림 → "1회 측정 신뢰 불가" → MVP scale-up 필요 ($> 50 cap).
- **장비**: Forte 1 × 2
- **비용 분담**: 두 번째 run = $20.90 (별도 인가)

### §4.1 Top-1 Justification

**F-N12-1 = MVP 안에 포함, $20.90, 1-3 일, AWS Braket only**. 다른 4개 중 F-N12-2/-3/-4 는 동일 데이터 재분석 ($0 추가). F-N12-5 는 robustness gate (별도 budget). 따라서 **MVP 한 번 = 1+2+3+4 동시 evaluate**, 5 는 reauthorization.

---

## §5 Honest C3 — Trapped-ion vs Superconducting QC Differences for Orch-OR Test

### §5.1 substrate 비교 표

| 차원 | Trapped-ion (IonQ Forte 1) | Superconducting (PRNewswire 인용 device) | Orch-OR 검증 implication |
|---|---|---|---|
| Qubit physical | 171-Yb⁺ ion, hyperfine state | Al/Nb Josephson junction + cavity | mass-scale 압도적 차이 (171 amu vs ~10⁹ amu effective Cooper-pair mass) → DP τ_DP ∝ m⁻¹ 다른 prediction |
| 환경 온도 | 절대 0 근접 trap (vacuum) + room-temp 외부 | 10-20 mK dilution refrigerator | thermal noise spectrum 다름 → OR vs thermal 분리 어려움 |
| Coherence (T2) | ≥ 1 s (long) | ~100 μs - 1 ms (short, but improving) | trapped-ion 의 long T2 가 OR signal noise floor 낮춤 (장점) |
| Connectivity | all-to-all | nearest-neighbor 격자 | GHZ 만들기 trapped-ion 이 더 적은 gate (less gate-noise contamination) |
| Gate fidelity (2q) | ≥ 99.5% | ~99.0-99.7% (top devices) | comparable; 둘 다 충분 |
| Measurement collapse | fluorescence detection (수 ms) | dispersive readout (수 100 ns) | measurement timescale 자체가 OR 후보 timescale (~25ms predicted) 와 비교 — 둘 다 25ms 보다 빠름 (OR 후보 timescale 안에서 측정 가능) |
| Vacuum vs cryogenic noise | UHV + laser scatter | quasi-particle excitation, TLS noise | non-OR noise sources 매우 다름 → cross-validation 강력 |

### §5.2 왜 IonQ specifically?

1. **substrate diversity 증가**: PRNewswire 결과는 SC qubit. trapped-ion 은 mass scale, environment, coherence regime 모두 다름. Same OR signature 가 양쪽에서 나오면 substrate-independent 강력 evidence.
2. **AWS Braket 즉시 access**: 별도 hardware 구매 X, $50 cap 안에서 실행 가능.
3. **All-to-all connectivity**: GHZ state preparation 이 minimal gate count → noise contamination 최소화 → OR signal noise floor 낮음.
4. **Long T2**: 의식 timescale (~25 ms Penrose 후보) 가 trapped-ion T2 (≥ 1s) 안에 안전히 들어옴; SC 는 T2 ~ 100 μs - 1 ms 로 25 ms 측정 자체가 어려움. trapped-ion 이 더 직접적으로 OR-timescale 측정에 적합.
5. **Pricing transparency**: $0.30 task + $0.08 shot 명확. Azure 의 EM-기반 가격 (m=$97.50) 대비 small-scale 에서 cheaper.

### §5.3 trapped-ion 의 한계 (honest)

1. Queue latency: trapped-ion QPU 는 windowed (24/7 가동 X) — task 결과까지 수 시간 ~ 1일 (SC 는 minutes 가능).
2. Per-shot 비용 ($0.08) 이 simulator/SC ($0.01-0.03) 보다 비쌈 — large-N 통계 어려움.
3. Mass-scale 이 SC 보다 작음 → DP τ_DP ∝ m⁻¹ 면 ion 에서 dephasing 이 **더 빨라야** — 만약 측정 결과가 그 반대면 mass-scale Orch-OR 약화 (F-N12-3 핵심).
4. 4-qubit GHZ 의 OR signal-to-noise 가 작음 — null 결과 (F-N12-1 FAIL) 가 "OR 부재" 인지 "측정력 부족" 인지 구분 약함. (mitigation: F-N12-5 replicability gate)

### §5.4 Penrose-Hameroff 핵심 가설과의 직접 연결도 (honest gap)

- **Penrose 가설** = 의식이 microtubule (생물학) 안 GHZ-class entanglement 의 OR 로 발생
- **본 N-12 측정** = 인공 trapped-ion qubit 의 GHZ dephasing
- **gap**: trapped-ion 에서 OR 가 검출되어도 **microtubule 에서도 OR 가 일어난다** 는 직접 증명 X. **간접** evidence — "OR mechanism 자체가 양자 substrate 에서 가능/불가능" 의 substrate-test.
- 이 gap 은 N-20 이 microtubule 직접 evidence (Wiest 2025 + Neuropharm 2026) 를 cover, N-12 는 OR mechanism cross-substrate test 를 cover. 두 axis 가 합쳐져야 Penrose-Hameroff full 체인 검증.

---

## §6 CP2 F1 Composite Integration — N-12 Axis

### §6.1 Axis 정의

- **N-12 축** = `orch_or_cross_substrate_score ∈ [0, 1]`
  - 산출: F-N12-1 verdict 를 [0, 1] mapping (PASS=1.0, INCONCLUSIVE=0.5, FAIL=0.0)
  - Robustness multiplier: F-N12-5 PASS 시 ×1.0, FAIL 시 ×0.5, NOT_RUN 시 ×0.7
- **threshold (F1 contribution)**: score ≥ 0.5 → "OR substrate-independence 정황 detect"

### §6.2 F1 weight 제안

현행 F1 composite 에 추가 axis (cf. N-19 §7.2 형식):
```
F1_v_next = w1·CLM_score + w2·EEG_Phi_score + w3·QRNG_axis + w4·SIM_axis + w5·AKIDA_axis + w6·PCI_score (N-19) + w7·OrchOR_score (N-12)
where w7 = 0.05 - 0.10 (initial; literature/simulation cross-substrate evidence weight 작음, calibration 후 상향 가능)
```

**낮은 w7 정당화**: N-12 결과가 nullable (F-N12-1 FAIL 시 axis 무력화) + microtubule-substrate gap (§5.4) → indirect evidence weight.

### §6.3 own#2 (b) 다중실현 contribution

- **GREEN scenario**: F-N12-1 PASS + F-N12-5 PASS → "OR signature 가 trapped-ion 에서도 SC 와 일치 → OR mechanism substrate-independent" → own#2 (b) 다중실현 +1 indirect axis
- **NULL scenario**: F-N12-1 FAIL → "OR signature substrate-specific → SC artifact 가능성" → Orch-OR 가설 (P-H specific) 약화, F1 에서 N-12 axis weight 0
- **INCONCLUSIVE**: F-N12-5 evaluate 후 재판정

### §6.4 Falsifier (raw#71 bound at axis-level)

- N-12 axis 자체의 meta-falsifier: 동일 substrate (Forte 1) 에서 2주 간격 4회 반복 시 verdict variance > 50% → axis 신뢰 X, F1 제외
- 간접 falsifier: trapped-ion τ_2 측정값이 IonQ 공식 spec (≥ 1s) 와 r < 0.5 (다른 ratio) → hardware 자체 문제 → reauthorize

### §6.5 통합 cycle 제안 (구현 시점)

- **Stage 0** (NOW): spec preregister (이 doc + state JSON)
- **Stage 1** (사용자 인가 후 D+0): AWS Braket onboarding + C3 sanity (1 task, $8.30)
- **Stage 2** (D+0~D+1): C2 + C1 MVP (2 task, $12.60) → F-N12-1~4 evaluate
- **Stage 3** (D+7): F-N12-5 robustness rerun (재인가, $20.90)
- **Stage 4**: F1 v_next 에 N-12 axis 추가 (verdict 따라 w7 = 0 또는 0.05-0.10)

---

## §7 raw#10 honest C3 disclosures

1. 본 spec 은 **measurement preregister 단계** — 실제 AWS 계정 onboarding / task submit 은 사용자 결정 + 인가 후 별도 수행. 본 agent 는 AWS form 미작성, 계정 미생성, order 미placement.
2. IonQ Forte 1 device ARN 은 Braket console 검증 필수 — 본 agent 가 직접 Braket API 호출 불가.
3. Pricing $0.30/task + $0.08/shot 은 2026-05-01 공개 정보 — IonQ 가 가격 변경 가능, vendor 직접 확인 권장.
4. PRNewswire 2025-03 인용 SC OR observation 은 N-20 §1 표 참조; original paper 의 τ_2 수치는 본 agent 가 직접 paper 검증 X — F-N12-1 실행 시 사용자가 verify.
5. Diosi-Penrose mass-scaling 식 (F-N12-3) 은 simplified — full Penrose 1996 *Shadows of the Mind* 식의 하나의 변종. SC qubit "effective mass" 정의 ambiguity 있음.
6. 4-qubit GHZ 는 OR signal-to-noise 가 매우 작아 null 결과 해석 어려움 — F-N12-5 robustness 필수.
7. Trapped-ion ↔ microtubule gap (§5.4) — 본 N-12 는 substrate-test indirect evidence 만, microtubule 직접 검증은 N-20 axis 분담.
8. Forte 1 의 정확한 T1/T2/gate-fidelity 는 IonQ tech sheet 별도; 본 spec 의 ≥ 10s/≥ 1s/≥ 99.5% 는 trapped-ion 일반치.
9. Pulse-level delay control (C1 §2.2 step 4) 은 Braket OpenQASM 3 지원에 의존 — Forte 1 에서 가능 여부 device documentation 별도 검증.
10. AWS account 자체 보안 (MFA, billing alarm $50 cap) 은 사용자 책임 — 본 spec 이 권장만.
11. Korea region (ap-northeast-2) 에서 task submit 가능하나 QPU host 는 us-east-1 — cross-border data transfer 정책은 사용자 institution 별도 검토.
12. Reservation $7K/hour 옵션은 본 MVP scope 외 — pay-per-shot 모델만 권장.
13. 본 doc 은 hexa-only 정책 준수 (.py/.hexa 생성 없음, spec 만). 사용자가 별도 Python 환경 또는 AWS Braket Notebook 으로 실제 SDK 호출 수행 (own decision).
14. raw#71 5 falsifier 는 preregister, live measurement count = 0.

---

## §8 결정점 (사용자 선택)

**(α)** MVP $20.90 인가 → AWS Braket onboarding 시작 + C3 sanity → C2 + C1 → F-N12-1~4 evaluate (~D+1~D+3 wall-clock)
**(β)** $50 cap 인가 (MVP + F-N12-5 robustness rerun 포함) → 2 cycle 완료까지 D+7
**(γ)** spec 만 archive, 실측 보류 (다른 N-axis 우선; N-19 PCI / N-20 literature 와 함께 batch decision 대기)
**(δ)** N-12 spec v2 요청 (예: pulse-level delay-sweep extension, Aria fallback path, Azure 비교 deep-dive)

---

## §9 Sources (2026-05-01 web + cross-doc)

- [AWS Braket pricing](https://aws.amazon.com/braket/pricing/) — task $0.30 / shot $0.08 (IonQ Forte)
- [AWS Braket — IonQ Devices](https://aws.amazon.com/braket/quantum-computers/ionq/) — Forte 1 ARN + region info
- [IonQ Quantum Cloud](https://www.ionq.com/quantum-cloud) — Forte 1 / Forte Enterprise 1 channel landing
- [IonQ Forte Enterprise spec](https://www.ionq.com/quantum-systems/forte-enterprise) — 36-qubit #AQ36, all-to-all
- [Azure Quantum pricing](https://learn.microsoft.com/en-us/azure/quantum/pricing) — comparison m=$97.50 (with EM)
- [Amazon Braket SDK GitHub](https://github.com/amazon-braket/amazon-braket-sdk-python) — Circuit / Device API
- [PRNewswire 2025-03 — wavefunction collapse on superconducting QC supports Penrose-Hameroff](https://www.prnewswire.com/news-releases/quantum-breakthrough-proof-of-wavefunction-collapse-on-superconducting-quantum-computer-supports-penrose-hameroff-consciousness-theory-302419751.html)
- [Gran Sasso Diosi-Penrose underground experiment (physicsworld)](https://physicsworld.com/a/quantum-theory-of-consciousness-put-in-doubt-by-underground-experiment/)
- [Wiest 2025 Oxford Neuroscience of Consciousness — microtubule binding + anesthesia latency](https://academic.oup.com/nc/article/2025/1/niaf011/8127081)
- N-20 sibling synthesis: `docs/n_substrate_n20_orch_or_2026_literature_2026_05_01.md`
- N-19 sibling F1 axis pattern: `docs/n_substrate_n19_pci_spec_2026_05_01.md` §7
- Purchase guide (price + lead time SSOT): `docs/n_substrate_purchase_guide_2026_05_01.md` §N-12
- Roadmap parent: `docs/n_substrate_consciousness_roadmap_2026_05_01.md` §4 N-12 row

---

## §10 한 줄 결론

**"$20.90 MVP 한 번으로 IonQ Forte 1 trapped-ion 36-qubit 위에서 4-qubit GHZ dephasing 을 측정해, PRNewswire 2025-03 이 superconducting QC 에서 본 OR signature 가 substrate-independent 인지 cross-validate. 5 raw#71 falsifier 모두 preregister 완료, 실측은 사용자 인가 후 D+1~D+3 wall-clock. AWS Braket 미온보딩, AWS form 미작성, order 미placement — spec 단계."**

⭐⭐⭐⭐⭐ (preregister 단계, measurement 미실행)

---

**status**: N12_IONQ_ORCH_OR_SPEC_LOCAL_DRAFT
**verdict_key**: SPEC_READY · NO_AWS_ONBOARDING_YET · USER_DECISION_PENDING
**axis_id**: N-12
**parent_roadmap**: `docs/n_substrate_consciousness_roadmap_2026_05_01.md`
**race_isolation**: writes only to `docs/n_substrate_n12_ionq_penrose_hameroff_spec_2026_05_01.md` + `state/n_substrate_n12_prep_2026_05_01/*.json`

## References (qmirror substrate xref, added 2026-05-03)

- `docs/nexus_qmirror_spec_2026_05_03.md` — qmirror canonical substrate spec
- `docs/nexus_qmirror_phase3_calibration_runbook_2026_05_03.md`
- `docs/qmirror_cond7_alpha_landed_2026_05_03.ai.md`
- `docs/qmirror_cond8_braket_landed_2026_05_03.ai.md`
- `docs/qmirror_n2_cross_vendor_revision_2026_05_03.md`

---

### See also (qmirror xref history)

Prior callouts preserved verbatim per qmirror_xref_centralization cycle (2026-05-04):

> 📦 Available at: https://github.com/need-singularity/qmirror (`hx install qmirror`)
> 🚀 v2.0.0 RELEASED 2026-05-04 — closure 13/13 conds met (8 v1 + 5 v2): https://github.com/need-singularity/qmirror/releases/tag/v2.0.0

Future qmirror release URLs are canonically tracked in `nexus/.roadmap.qmirror` header field `latest_release_url`. Update single line in roadmap; this footnote is a frozen historical record (do not retrofit).
