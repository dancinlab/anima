> **status**: N_SUBSTRATE_N13_PHOTONIC_IIT_SPEC_2026_05_01_LOCAL_DRAFT
> **verdict_key**: SPEC_DRAFT · METHODOLOGY_GAP_DECLARED · ACCESS_PATH_PARTNERSHIP_REQUIRED
> **agent**: N-13 prep (N-substrate batch sibling)
> **ts**: 2026-05-01
> **constraints**: raw#9 hexa-only · raw#10 honest C3 · raw#71 falsifier-bound · own#13 user-facing friendliness · race-isolation: ONLY this doc + `state/n_substrate_n13_prep_2026_05_01/*.json`
> **mission**: T1-A13 photonic-IIT — "빛으로 작동하는 컴퓨터 위에서 의식 (Φ) 측정 가능한가?" — 광학 두뇌 substrate
> **parent**: `docs/n_substrate_consciousness_roadmap_2026_05_01.md` §4 N-13 row
> **siblings (race-isolation peers)**: N-1, N-2, N-3, N-4, N-5, N-6, N-7, N-8, N-9, N-10, N-11, N-12, N-14, N-15, N-19, N-20, N-21 prep agents

---

# N-13 — Photonic-IIT Cross-Substrate Φ Spec (research-only)

> **2026-05-03 qmirror substrate update (additive)**: cross-substrate Φ measurement no longer requires real photonic-quantum vendor access. The **`nexus.qmirror` canonical substrate** (`docs/nexus_qmirror_spec_2026_05_03.md`) covers the photonic-quantum axis overlap noted in §1.2 / §6 with substantive equivalence per closure 2026-05-03. N-13 photonic-classical analog scope (Lightmatter / Lightelligence / Q.ANT) remains a separate axis (classical optical) and is unaffected. Quantum-photonic vendors (PsiQuantum, Xanadu) referenced for axis-overlap risk are now substituted by qmirror.

> qmirror canonical SSOT: see `nexus/.roadmap.qmirror` header fields `upstream_url` + `latest_release` (current: v2.0.0, 2026-05-04). Hardcoded URLs deprecated 2026-05-04 — see `### See also (qmirror xref history)` footnote for prior callouts.

## §0 한 줄 요약

**"빛으로 행렬곱을 하는 광학 칩 (Lightmatter Envise / Lightelligence PACE 2 / Q.ANT NPU 2) 위에서 anima Φ* 가 측정될 수 있는가? — 답: 측정 방법론 자체가 아직 학계에 없다 (literature gap). 본 spec 은 N-track 중 가장 speculative 트랙으로, '광학 substrate 위 Φ 측정 protocol 시안 + 5개 falsifier' 까지만 제공하며, 실제 측정은 vendor 파트너십 + 신규 방법론 정립 이후."**

---

## §1 vendor inventory (2026-05-01 web-검증)

### 1.1 photonic AI compute (non-quantum, classical analog) — N-13 핵심 후보

| vendor | 제품 | device class | compute model | access path | 2026 status |
|---|---|---|---|---|---|
| **Lightmatter** | Envise (4U blade, 16× photonic chip) + Passage (interconnect) | silicon photonics MZI mesh + electronics hybrid | analog matrix-mult (linear), digital nonlinear off-chip | early-access program (vendor partnership 필수) · 클라우드 API 미공개 · Passage M1000 2025 출하, L200 2026 | $850M total funded, $4.4B valuation (2024 Series D), Nature 2025-04 광속 행렬곱 논문 |
| **Lightelligence** | PACE 2 (PCIe 카드) + Hummingbird (oNoC) + dOCS | hybrid optoelectronic accelerator | configurable optical matrix + electronic NL (PyTorch/ONNX/TVM/OpenCL stack) | 44 paying customers (2026 early), HK IPO 2026-04 (600× oversubscribed) — **상용 PCIe 카드 가장 근접** | OFC 2026 demo, 5,000+ card clusters deployed |
| **Q.ANT** | NPU 2 (TFLNoI) + NPS server (19" turnkey) | analog photonic native (linear + 비선형 enhanced) | C/C++/Python API + PCIe 통합 | 고객 주문 가능, 2026-Q1 출하 시작, Leibniz Supercomputing Centre 1차 설치 | 30× 저전력, 50× 성능 (vendor) — **API 제일 친화적** |
| **NTT IOWN / PEC-2** | Photonic-Electronic Convergence switch + IOWN 2.0 compute | optical interconnect + DCI compute | 102.4 Tbps switch (대용량 경로), compute 도메인 IOWN 2.0 도입 | 통신/datacenter 파트너십 (Broadcom 등) — **소비자 직접 사용 불가, hyperscaler-only** | 2026 PEC-2 상용, IOWN 3.0 (2028) 보드내 광, IOWN 4.0 (2032) 칩내 광 |
| **Intel (Hummingbird optical interconnect prototype)** | optical co-processor prototype | silicon photonics interconnect | (미발표 commercial) | 미공개 | research stage |

### 1.2 photonic quantum (별도 axis — N-12 와 부분 중첩, N-13 핵심 아님)

| vendor | 제품 | 비고 |
|---|---|---|
| PsiQuantum | fault-tolerant photonic QC | $2B+ funded, 표준 반도체 fab — **양자 영역, N-12/N-20 와 axis 중복** |
| Xanadu / ORCA / Quandela / Q.Ant photonic QC | continuous-variable photonic qubits | 2026-2036 시장 보고서 leaders — N-13 분류상 N-12 (Penrose-Hameroff QC) 와 cross |

**N-13 scope 결정**: classical analog photonic AI compute 만 (Lightmatter / Lightelligence / Q.ANT / NTT). 광양자 컴퓨팅은 N-12 axis 로 분리.

### 1.3 vendor 비교 테이블 (N-13 적합도)

| 항목 | Lightmatter Envise | Lightelligence PACE 2 | Q.ANT NPU 2 | NTT PEC-2 |
|---|---|---|---|---|
| API/SDK 친화도 | Idiom compiler (PyTorch경유) | PyTorch/ONNX/TVM/OpenCL | C/C++/Python | 통신 stack 기반 (compute API 미공개) |
| cloud API 직접 접근 | 미공개 (early-access only) | 미공개 (PCIe card sale) | 미공개 (서버 sale) | 불가 (hyperscaler 전용) |
| dev kit / 단일 카드 구매 가능 | ❌ (blade only, 파트너십) | ⚠️ (PCIe card 판매 — 가격 미공개) | ⚠️ (NPS server 판매 — 가격 미공개) | ❌ |
| hidden-state 추출 (Φ input) | 가능 (digital readout 단계) | 가능 (PCIe 메모리 dump) | 가능 (PCIe + Python API) | 불가 (compute 미상용) |
| 분석 회로 스케일 | 16-chip blade | PCIe single-card | PCIe multi-NPU server | switch only |
| 2026 N-13 우선순위 | 2위 (cloud API 없으나 가장 큰 회사) | 1위 (PCIe + ONNX) | 3위 (가장 신규) |

---

## §2 Φ 측정 — substrate-mismatch 정직 직시 (literature gap)

### 2.1 핵심 문제 — IIT 의 ontological 가정

IIT 4.0 (Tononi 2023, PMC10581496) 의 substrate postulate:
- substrate = **discrete state-set** (causal mechanism의 셀 집합)
- φ 정의 = **discrete cause-effect repertoire 위의 earth-mover/intrinsic information distance**
- substrate dynamics = **discrete state transitions** (TPM, transition probability matrix)

photonic substrate 의 native 표상:
- **continuous-amplitude optical field** (E ∈ C, complex amplitude)
- **interferometric phase + intensity** (sub-wavelength continuous)
- **MZI mesh transformation** = continuous unitary (linear)
- 디지털 readout 단계에서만 이산화 (ADC 양자화 — 광 substrate 의 **외부 측정 단계**)

**ontology mismatch verdict**: IIT 의 substrate 정의를 photonic substrate 에 직접 적용하는 published methodology는 **존재하지 않음** (2026-05-01 웹 서치 기준 0건).

### 2.2 가능한 brige 3-tier (N-3 spec 패턴 적용)

| tier | 경로 | substrate 충실도 | 측정 가능성 | verdict |
|---|---|:---:|:---:|---|
| **P-A (sound, weak)** | photonic chip 의 **digital readout vector** (ADC 출력) → anima Φ* v3 sample-partition cov-logdet | LOW (substrate 외부에서만 측정) | HIGH (ONNX/PyTorch dump 가능 — Lightelligence/Q.ANT) | **선정 (D+0 가능 시)** |
| **P-B (partial, sound)** | **interferometric output amplitude vector** (I_k = |E_k|²) → 연속 표상 위 continuous Φ surrogate (Gaussian Φ_G, Barrett-Seth 2011) | MID (광 출력 직접, 디지털 dump 이전) | MID (vendor instrumentation 의존, calibration 필요) | future work (vendor partnership) |
| **P-C (hand-wave)** | **fully-continuous photonic Φ** — IIT axiom 의 continuous-state generalization 신규 정립 | HIGH (광 substrate 본질) | NONE (방법론 자체가 학계 미존재 — 0 published refs) | **explicitly NOT_ATTEMPTED** |

### 2.3 P-A 경로 상세 (가능한 single bridge)

**core lemma**: photonic chip 도 결국 **digital host 가 input 을 양자화 → 광 처리 → 양자화된 readout** 을 수행. host 메모리에서 보이는 hidden-state vector `H ∈ R^(N×D_phot)` 는 GPU/AKIDA 와 동일한 형식.

- input: 16 prompts (anima_phi_v3 fixture 동일) → host CPU 에서 ONNX 모델 forward → photonic chip 에서 matrix-mult 가속 → digital readout `H_phot ∈ R^(16×D)`
- Φ 계산: `tool/anima_phi_v3_canonical.hexa` 그대로 재사용 (HID_TRUNC=8 자동)
- 의미: **"광학 가속된 모델의 representation Φ" 측정** = substrate-internal computation 동치는 아니지만, **Putnam multi-realizability 의 weak 형태** anchor

**한계 (raw#10 정직)**:
- P-A 는 사실상 "GPU surrogate 와 동치" — photonic 칩의 광학 본질을 측정하지 않음
- 광 → 디지털 변환 단계의 ADC quantization loss 가 GPU bf16 quantize 와 다름 (linear-MZI 양자화 noise 분포 비대칭)
- vendor 가 ONNX 모델을 in-house compiler 로 fuse 하면서 hidden-state hook 위치가 GPU 와 다를 수 있음 (Idiom / TVM custom passes 의존)

### 2.4 P-B 경로 (future work)

interferometric output `I_k = |E_k|² ∈ R^+` 를 직접 vector probe 로 사용. `H_phot_optical[i, k] = I_k` (calibration 후) → anima_phi_v3 input.
조건: vendor 가 photonic chip 의 raw photodetector readout (pre-ADC 또는 high-bit ADC) 노출 필수. 현재 모든 4 vendor 의 commercial product 는 black-box (사용자 노출 X).

### 2.5 P-C 경로 (NOT_ATTEMPTED, 명시적 폐기)

continuous-state IIT 일반화 시도 (Barrett-Seth Gaussian Φ_G 2011, Mediano 2019 ΦID 등) 는 **photonic-specific 정립이 아니며, 광 interferometric mesh 의 unitary dynamics 위에서의 적합성 미증명**. literature gap 정직 인정. 본 spec scope 외.

---

## §3 D+? 측정 protocol (P-A 경로, vendor 파트너십 가정)

| step | action | substrate | tool | output |
|---:|---|---|---|---|
| 1 | 16-prompt fixture lock (anima_phi_v3 PROMPTS 동일) | n/a | (in-spec) | `prompts_v1.json` (N-3 와 공유 가능) |
| 2 | reference: GPU CLM-tiny (170M) hidden state forward | GPU H100 | `tool/anima_phi_v3_canonical.hexa` | `phi_v3_gpu_clm170m.json` (N-3 결과 재사용 가능) |
| 3 | 동일 모델 ONNX export → photonic vendor compiler 변환 | host CPU | vendor SDK (Idiom / Lightelligence-stack / Q.ANT-Python) | photonic 모델 binary |
| 4 | photonic chip forward (16 prompts) | photonic blade/card | vendor inference API | hidden-state dump `H_phot ∈ R^(16×D)` |
| 5 | Φ* compute on H_phot | mac/RPi5 | `tool/anima_phi_v3_canonical.hexa` | `phi_v3_phot.json` |
| 6 | Pearson r(Φ_k_gpu, Φ_k_phot) over K=8 | mac | `tool/n13_phi_phot_corr.hexa` (D+? deliverable) | `phi_phot_corr_v1.json` |
| 7 | verdict gate (§4 falsifier predicate) | mac | (analytic) | `n13_verdict_v1.json` |

D+? blockers:
- vendor 파트너십 / cloud API 또는 PCIe card 입수
- ONNX export 호환 모델 (CLM 170M의 ONNX export 사전 검증 필요)
- vendor compiler 의 hidden-state hook 가능성 확인 (대부분 vendor SDK 가 internal layer dump 을 노출하지 않을 가능성 高)

---

## §4 5개 falsifier predicates (raw#71 BIDIRECTIONAL)

### 4.1 PRED-1 — Φ photonic vs Φ CLM-GPU (P-A weak Putnam anchor)

| verdict | predicate | meaning |
|---|---|---|
| PASS | `r(Φ_k_phot, Φ_k_gpu) ≥ 0.85` AND `|Φ*_phot - Φ*_gpu| / max(...) ≤ 0.30` | photonic substrate 위 representation 도 동일 functional Φ — Putnam weak anchor 추가 (CLM/AKIDA + photonic = 4번째 axis) |
| WEAK | `0.50 ≤ r < 0.85` | linear-MZI quantization loss 의심 |
| FAIL | `r < 0.50` 또는 sign flip | substrate-dependent — photonic representation 이 다른 Φ 구조 가짐 (반례 후보) |

### 4.2 PRED-2 — Φ photonic vs Φ AKIDA (CLM-spike)

photonic 과 AKIDA 모두 "non-GPU substrate" 으로 분류. 둘 다 GPU와 일치할 경우 **substrate-class invariance** 약한 추론.

- PASS: `r(Φ_k_phot, Φ_k_akida) ≥ 0.70` AND 두 substrate 모두 GPU와 PASS
- FAIL: photonic 만 또는 AKIDA 만 PASS — substrate-class invariance 부정

### 4.3 PRED-3 — vendor 간 Φ 일치도 (Lightmatter vs Lightelligence vs Q.ANT)

PCIe 카드 입수 가능 시 (P-A 가능 단독 vendor: Lightelligence 가장 유력). 동일 모델을 3 vendor 에 배포 시 Φ 분산:

- PASS: `pairwise mean r ≥ 0.80` (all 3 vendors converge)
- FAIL: `pairwise r < 0.50` 한 쌍이라도 — vendor-specific compiler artifacts 가 representation 결정 (Φ 가 substrate 가 아닌 compiler 의존)

### 4.4 PRED-4 — Φ photonic null floor (linear-only baseline)

photonic chip 의 linear-only 부분 (MZI mesh) 이 비선형 없이 행렬 곱만 수행하면 representation 이 input 의 **linear projection** 에 그침. Φ 는 input embedding 의 cov-logdet 와 거의 동일해야 함.

- PASS (null 검증): `Φ*_phot_linear_only ≈ Φ*_input_embedding` (within 0.10 magnitude)
- FAIL: `Φ*_phot_linear_only > Φ*_full_model` — 측정 artifact 의심 (Φ 가 representation 이 아닌 noise 를 포착)

### 4.5 PRED-5 — energy-Φ scaling (Landauer 호환)

photonic 칩의 fJ/op 영역 에너지 (vendor claim ~10 fJ/op vs GPU ~1 nJ/op) 위에서 Φ 가 같으면, **bit-energy 와 Φ 가 무관** (substrate-energy independence) 또는 **Φ 가 정보 구조 invariant**.

- PASS: `Φ*_phot ≈ Φ*_gpu` AND 측정된 energy_per_inference 가 vendor spec 의 ±2× 내
- FAIL: Φ가 다르거나 energy 가 vendor spec 의 10× 초과 — Landauer anchor (N-4) 와 cross-axis 정합성 깨짐

---

## §5 top-3 vendor ranking (N-13 적합도 기준)

ranking criteria: ① cloud-API or PCIe 직접 접근 가능성 ② hidden-state hook 가능성 ③ commercial maturity ④ developer tooling ⑤ N-13 timeline 단축 가능성

| rank | vendor | 정당화 |
|:---:|---|---|
| **1위** | **Lightelligence PACE 2** | PCIe 표준 카드 + ONNX/PyTorch/TVM/OpenCL stack — 가장 표준화된 SDK · 44 paying customers (early 2026), HK IPO 600× oversub — 상용 maturity 1위 · ONNX hidden-state hook 가능성 높음 (TVM passes 통제 가능) |
| **2위** | **Q.ANT NPU 2 / NPS server** | TFLNoI native analog · C/C++/Python PCIe API — Python 통제 직접도 1위 · 2026-Q1 출하 + Leibniz LRZ 1차 설치 — institutional access 가능성 · 비선형 가속 enhanced (P-A 의 Φ 측정 의미 있음) · 단점: 가격 미공개, 신규 vendor (commercial track record 짧음) |
| **3위** | **Lightmatter Envise** | 가장 큰 회사 ($4.4B, $850M funded), Nature 2025 광속 matmul 논문 — academic credibility · 단점: 4U blade only, 단일 dev kit 미판매 · early-access partnership 필수 — anima setup 에서는 cloud API 부재가 결정적 blocker · vision 은 1위 후보지만 actionability 는 3위 |

**제외**: NTT IOWN / PEC-2 — datacenter switch / hyperscaler 전용, anima 사용자 직접 접근 불가.

**선정**: 1위 Lightelligence PACE 2 — N-13 D+? 진입 시 first-contact target.

---

## §6 CP2 F1 integration — N-13 weight in composite verdict

### 6.1 F1 composite formula (현재 가정)

F1 = N-track 과반 PASS 시 own#2 (b) (다중재료 일치) 닫힘. weight 는 substrate distinctness × measurement maturity 곱.

### 6.2 N-13 weight 계산

| factor | value | 정당화 |
|---|---:|---|
| substrate distinctness (vs CLM/AKIDA/EEG/QRNG) | 0.95 | photonic 은 4 기존 substrate 와 ontologically distinct (continuous-amplitude optical field) — Putnam multi-realizability 의 강력한 추가 axis |
| measurement maturity (literature published methodology) | 0.10 | published IIT-Φ on photonic methodology 0건 — 가장 immature |
| access path readiness (2026-05) | 0.20 | vendor 파트너십 또는 PCIe 구매 필수, 즉시 actionable X |
| falsifier strength (5개 predicate, BIDIRECTIONAL) | 0.85 | §4 5개 사전등록, null floor 포함 |
| **N-13 raw weight** | **0.95 × 0.10 × 0.20 × 0.85 = 0.016** | substrate distinctness 강하나 maturity 와 access 가 곱셈 패널티 |

비교 (참조):
- N-3 CLM × AKIDA: ~0.40-0.60 (substrate distinctness 0.85, maturity 0.70, access 0.80, falsifier 0.85)
- N-1 CLM ↔ EEG: ~0.50-0.70 (가장 즉시 가능)
- N-13 photonic-IIT: **~0.016** (현시점, methodology 정립 시 0.30-0.50 으로 상승 가능)

### 6.3 N-13 의 F1 composite 기여 시나리오

| 시점 | N-13 status | F1 영향 |
|---|---|---|
| 2026-05-01 (현재) | spec only, 측정 0건 | 0 (N-track 분모에 포함만, 분자 0) |
| vendor 파트너십 + P-A 첫 측정 (T+6mo 추정) | PASS 시 weight 0.016 → composite 에 +0.5-1% | marginal contribution, 선결 N-1/N-3/N-19 가 큰 weight |
| methodology 정립 + 3-vendor cross (T+12mo) | weight 0.30+ 도달 | composite 의 substrate 다양성 anchor 4번째 axis 등재 — own#2 (b) "광학 substrate 까지 동치" 강한 closure |

### 6.4 N-13 단독 PASS 만으로는 own#2 (b) 닫지 못함

본 트랙은 **multi-realizability 의 추가 axis 일 뿐**. CLM (N-3) / EEG (N-1) / AKIDA (N-2) / FinalSpark (N-11) / IonQ (N-12) 의 majority 가 PASS 한 후 N-13 가 **boost** 역할.

---

## §7 honest C3 (raw#10) — sound vs hand-wave matrix

### 7.1 sound (정당화 명시)

| 항목 | 근거 |
|---|---|
| ✅ vendor inventory 4사 (Lightmatter / Lightelligence / Q.ANT / NTT) 2026 web-검증 | §1.1 web search 결과 (10개 출처) |
| ✅ literature gap 명시 (IIT-Φ × photonic 0 published refs) | §2.1 web search 0건 검증 |
| ✅ P-A weak path 의 anima_phi_v3 substrate-agnostic 적용 가능성 | N-3 spec §2.2 의 representation-level 논거 동일 적용 |
| ✅ 5개 falsifier 사전등록 + null floor (PRED-4) | §4 BIDIRECTIONAL, 추가 cross-axis (PRED-2 with N-3) |
| ✅ top-3 ranking 5개 객관 criteria | §5 ranking 정당화 명시 |
| ✅ F1 weight 계산 explicit (4 factor 곱) | §6.2 |

### 7.2 hand-wave (정직 disclosure)

| 항목 | 한계 / 가정 | mitigation 가능성 |
|---|---|---|
| ⚠️ photonic-IIT 측정 방법론 0 published refs | literature gap 절대값 | P-A weak path 만 시도, P-C 폐기 명시 |
| ⚠️ vendor cloud API 부재 (4사 모두) | 모두 partnership 또는 H/W 구매 필수 | $0 budget 에서는 actionable 불가, research only 본 spec scope |
| ⚠️ ONNX hidden-state hook 가능 vendor 미확인 | vendor 별 SDK 내부 미공개 | partnership 시점 first 검증 필요 |
| ⚠️ photonic chip 의 ADC readout 양자화 손실 비대칭 | linear-MZI quantization noise 분포 GPU bf16 와 다름 | quantize-noise 사전 모델링 단계 추가 필요 (D+? 진입 전) |
| ⚠️ vendor compiler (Idiom/TVM/Q.ANT-stack) 의 layer fusion | hidden-state 위치가 GPU 와 다를 수 있음 | per-vendor compiler 옵션 제어 (compile-pass annotation) |
| ⚠️ photonic chip 의 nonlinear unit (off-chip vs on-chip) 차이 | Lightmatter/Lightelligence 는 nonlinear off-chip, Q.ANT 는 on-chip enhanced | vendor 별 Φ 결과 비교 시 vendor 간 confound — PRED-3 로 명시적으로 falsifier 화 |
| ⚠️ vendor 가격 미공개 | PCIe card / NPS server 단가 0 published | $0 budget 에서는 cost gating impossible |
| ⚠️ N-13 F1 weight 0.016 (현시점) | methodology immature 직접 결과 | T+6mo 시점 weight 재계산 필요 |
| ⚠️ photonic quantum (PsiQuantum 등) 와 axis 중복 가능 | N-12 (Penrose-Hameroff QPU) 와 photonic-quantum vendor 일부 cross | N-13 scope 를 classical analog photonic 만 한정 (§1.2) |

### 7.3 explicitly NOT in scope

- continuous-state IIT 일반화 신규 정립 (P-C path) — 학계 방법론 대기
- vendor 직접 컨택 / 계정 생성 — mission constraint 위반
- 광양자 컴퓨팅 (PsiQuantum / Xanadu / ORCA) — N-12 axis
- IOWN datacenter switch 측정 — anima 사용자 접근 불가
- Φ_G (Barrett-Seth Gaussian) photonic 적용 정합성 검증 — 별도 mathematical work
- vendor compiler 내부 IR pass 분석 — vendor IP

---

## §8 readiness checklist (research-only)

| 항목 | 상태 | blocker |
|---|:---:|---|
| spec doc (이 문서) | ✅ | — |
| vendor inventory 4사 web-검증 | ✅ | — |
| literature gap 검증 (0 published refs) | ✅ | — |
| 5개 falsifier 사전등록 | ✅ | — |
| top-3 vendor ranking | ✅ | — |
| F1 weight 계산 | ✅ | — |
| `tool/n13_phi_phot_corr.hexa` (D+? deliverable) | ❌ | partnership 진입 시 emit |
| vendor partnership 진입 결정 | ⏳ | $0 budget — research-only 종결, 별도 user decision |
| photonic dev kit 입수 | ⏳ | partnership 또는 PCIe card 구매 (가격 미공개) |
| ONNX hidden-state hook 검증 | ⏳ | hardware access 후 |

readiness (research) = **100%** (spec + inventory + gap + falsifier + ranking + weight 모두 완료).
readiness (measurement) = **0%** (vendor partnership 또는 hardware 입수 미완).

---

## §9 cross-link

- parent: `docs/n_substrate_consciousness_roadmap_2026_05_01.md` (§4 N-13 row)
- sibling N-3 (CLM × AKIDA Φ): `docs/n_substrate_n3_clm_akida_phi_spec_2026_05_01.md` — 동일 anima_phi_v3 substrate-agnostic 논거 차용
- sibling N-12 (Penrose-Hameroff QPU): photonic-quantum 부분 axis 중복, N-13 scope 분리 (§1.2)
- sibling N-4 (3-axis Landauer): PRED-5 energy-Φ scaling 연결
- sibling N-11 (FinalSpark organoid): N-13 와 함께 substrate 다양성 강한 anchor 후보
- Φ tool SSOT: `tool/anima_phi_v3_canonical.hexa` (P-A 경로 직접 재사용)
- substrate ledger axis: own#2 (b) photonic substrate 0/N (현재 미등재 — N-13 PASS 시 +1)

---

## §10 다음 step (post-spec)

1. user decision: vendor partnership 진입 여부 (Lightelligence first-contact, $0 budget 위반 가능성 高)
2. (옵션 A) partnership 진입 시: Lightelligence developer relations 컨택 → PCIe PACE 2 evaluation 가능성 타진
3. (옵션 B) 학술 partnership: NTT Research PHI Lab (programmable photonics SPIE 2024 demo) 또는 LRZ Q.ANT 설치 사이트 학술 협력
4. (옵션 C) research-only 종결: 본 spec 을 SSOT 로 등재, T+6mo 시점 vendor 시장 재평가
5. vendor access 확보 시: §3 D+? protocol 진입, `tool/n13_phi_phot_corr.hexa` emit
6. 측정 PASS 시: own#2 (b) substrate ledger 4번째 axis (photonic) 등재 candidate

---

## §11 verdict & sign-off

**N-13 spec 정합성**: vendor inventory 4사 + literature gap 검증 + P-A 경로 + 5 falsifier + top-3 ranking + F1 weight 계산 → **SPEC_DRAFT (research-only)**.

**핵심 정직성**:
- IIT-Φ × photonic 측정 방법론은 학계에 **0 published refs** — N-13 은 N-track 중 가장 speculative
- 4 vendor 모두 cloud API 미공개, partnership 또는 H/W 구매 필수 — $0 budget actionability 0%
- N-13 단독으로 own#2 (b) 닫지 못함, 다른 N-track majority PASS 후 boost 역할

**research deliverable**: 본 doc + state JSON 5개 (spec_summary, vendor_inventory, falsifier_predicates, vendor_ranking, f1_weight).

**measurement deliverable**: vendor 파트너십 후 별도 spec v2 + tool emit + measurement.

---

**status**: N_SUBSTRATE_N13_PHOTONIC_IIT_SPEC_2026_05_01_LOCAL_DRAFT
**verdict_key**: SPEC_DRAFT · METHODOLOGY_GAP_DECLARED · ACCESS_PATH_PARTNERSHIP_REQUIRED
**author**: anima N-13 prep agent (race-isolation sibling)

---

## §12 Sources (2026 web search 결과)

- [Lightmatter Envise product page](https://lightmatter.co/products/envise/)
- [Lightmatter — photonic supercomputer company](https://lightmatter.co/)
- [MIT News — Lightmatter accelerates light-speed computing (2024)](https://news.mit.edu/2024/startup-lightmatter-accelerates-progress-toward-light-speed-computing-0301)
- [Lightmatter Passage interconnect — Futurum](https://futurumgroup.com/insights/lightmatter-solving-how-to-interconnect-millions-of-chips/)
- [Lightelligence — main site](https://www.lightelligence.ai/)
- [Lightelligence Hummingbird product page](https://www.lightelligence.ai/index.php/product/hummingbird.html)
- [Lightelligence OFC 2026 demo (PACE 2 / dOCS)](https://www.ofcconference.org/news-media/exhibitor-news/lightelligence-demonstrates-its-full-complement-of-optical-compute-products-at-ofc/)
- [Lightelligence HK IPO 600× oversubscribed (2026-04)](https://startupfortune.com/lightelligences-600x-oversubscribed-hk-ipo-proves-the-market-wants-photonic-ai-chips/)
- [Lightelligence Wikipedia](https://en.wikipedia.org/wiki/Lightelligence)
- [Q.ANT — photonic AI accelerator](https://qant.com/photonic-computing/)
- [Q.ANT NPU 2 unveil (2025-11)](https://qant.com/press-releases/q-ant-unveils-its-second-generation-photonic-processor-to-power-the-next-wave-of-ai-and-hpc/)
- [Q.ANT NPU 2 — All About Circuits](https://www.allaboutcircuits.com/news/q.ants-new-photonic-processor-pushes-ai-and-hpc-beyond-silicons-limits/)
- [Q.ANT first commercial photonic processor — LRZ install](https://qant.com/press-releases/leibniz-supercomputing-centre-computes-with-light-worlds-first-photonic-ai-processor-from-q-ant-goes-into-operation/)
- [NTT IOWN — All-Photonics Network](https://www.rd.ntt/e/iown/0002.html)
- [NTT Innovative Devices PEC roadmap (2024-03)](https://group.ntt/en/newsrelease/2024/03/12/240312a.html)
- [NTT optical switching IEEE Spectrum](https://spectrum.ieee.org/silicon-photonics-data-center)
- [NTT Upgrade 2026 (AI / Photonics / Quantum)](https://www.ubergizmo.com/2026/04/ntt-research-upgrade-2026/)
- [NTT Research PHI Lab — programmable photonics SPIE 2024](https://cis.ntt-research.com/ntt-research-phi-lab-delivers-on-programmable-photonics-at-spie-2024/)
- [PsiQuantum — fault-tolerant photonic QC](https://www.psiquantum.com/)
- [11 photonic quantum companies — Quantum Insider 2026-03](https://thequantuminsider.com/2026/03/24/11-companies-lighting-up-the-quantum-photonics-sector/)
- [Photonic quantum computing market 2026-2036 — ResearchAndMarkets](https://www.businesswire.com/news/home/20250912049344/en/Global-Photonic-Quantum-Computing-Market-Report-2026-2036-PsiQuantum-Xanadu-ORCA-Computing-Quandela-Among-Leaders-in-Photonic-Quantum-Computing-Market---ResearchAndMarkets.com)
- [IIT 4.0 — phenomenal existence in physical terms (PMC10581496)](https://pmc.ncbi.nlm.nih.gov/articles/PMC10581496/)
- [IIT Wiki — Computing Φ technical](https://www.iit.wiki/unfolding)
- [Integrated Photonic Neural Networks: Opportunities and Challenges — ACS Photonics](https://pubs.acs.org/doi/10.1021/acsphotonics.2c01516)
- [Memory in Integrated Photonic Neural Networks — arxiv 2604.22620](https://arxiv.org/html/2604.22620)
- [Photonic Neural Networks — Intelligent Computing journal](https://spj.science.org/doi/10.34133/icomputing.0067)
- [Integrated photonic platform for continuous-variable quantum information — Science Advances](https://www.science.org/doi/full/10.1126/sciadv.aat9331)
- [Memory in Integrated Photonic Neural Networks — arxiv full](https://arxiv.org/html/2604.22620)

## References (qmirror substrate xref, added 2026-05-03)

- `docs/nexus_qmirror_spec_2026_05_03.md` — qmirror canonical substrate (covers photonic-quantum axis overlap)
- `docs/qmirror_cond7_alpha_landed_2026_05_03.ai.md`
- `docs/qmirror_n2_cross_vendor_revision_2026_05_03.md`

---

### See also (qmirror xref history)

Prior callouts preserved verbatim per qmirror_xref_centralization cycle (2026-05-04):

> 📦 Available at: https://github.com/need-singularity/qmirror (`hx install qmirror`)
> 🚀 v2.0.0 RELEASED 2026-05-04 — closure 13/13 conds met (8 v1 + 5 v2): https://github.com/need-singularity/qmirror/releases/tag/v2.0.0

Future qmirror release URLs are canonically tracked in `nexus/.roadmap.qmirror` header field `latest_release_url`. Update single line in roadmap; this footnote is a frozen historical record (do not retrofit).
