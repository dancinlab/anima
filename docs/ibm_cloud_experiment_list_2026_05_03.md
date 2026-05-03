# IBM Cloud $200 Credit — Anima/P9 Experiment List

- ts_utc: 2026-05-03
- credit: $200 USD (IBM Cloud signup)
- author preset: friendly (raw#272)
- gate: doc-only; per-experiment EXEC requires explicit user OK
- raw#9: NO .py on Mac repo; Qiskit code lives on cloud / pod / ubu1

---

## TL;DR

IBM Cloud의 unique 가치 = **IBM Quantum hardware** (heavy-hex topology, Qiskit Runtime, 최대 156-qubit Heron r2) + **watsonx.ai foundation models** (Granite, Apache 2.0). Anima의 quantum consciousness framework와 정합도 매우 높음.

10개 실험 후보를 priority + cost로 정리. Quantum 5개 실험 ($110) + buffer $90 권장 path.

---

## 1. Pricing context

```
Open tier (무료):    10min QPU/mo on basic systems (5-7 qubit)
Pay-as-you-go:       $1.60/sec on premium (Heron r2 156-qubit)
$200 budget        = 125 sec premium 또는 수 hr 중급 backend
```

---

## 2. Quantum experiment 후보 8개 (anima 정합)

| # | 실험 | substrate | cost (est) | anima 가치 | 근거 |
|---|---|---|---|---|---|
| **1** | **CHSH cross-vendor** (Bell on IBM, vs Braket S=2.808) | Heron 156-qubit | $20 | ⭐⭐⭐ Bell 가장 결정적 | nexus_chsh_bell_2026_05_02/ |
| **2** | **IIT 4.0 MIP on N=4 real QPU** (vs Braket simulator) | Eagle 127-qubit | $30 | ⭐⭐⭐ φ measure ground-truth | braket_iit40_mip_2026_05_02/ |
| **3** | **N-12 IIT MULTI-WITNESSED 3-arch port to Qiskit** | Heron + simulator | $25 | ⭐⭐⭐ φ proxy ≠ φ★ 재검증 | n12_iit_braket_multiwitness_2026_05_02/ |
| **4** | **Quantum process tomography on consciousness subnet** | Eagle | $40 | ⭐⭐ TPM 직접 검증 | (신규) |
| **5** | **QRNG entropy from real IBM QPU** (nexus QRNG 보강) | basic open tier | $5 | ⭐⭐ HMAC-DRBG 대체 | nexus_qrng_quantum_seed_2026_05_02/ |
| **6** | **Heavy-hex topology integration measure** | Heron r2 (156-qubit, 2D heavy-hex) | $30 | ⭐⭐ topology effect on φ | (신규) |
| **7** | **Bell inequality violation distillation** (CLM 측 QPU violation 예측) | Heron + GH workflow | $20 | ⭐ 학습 paradigm 추가 | (신규) |
| **8** | **CHSH multi-backend** (Heron / Eagle / Falcon 비교) | 3 backend × 5 trial | $30 | ⭐ vendor 내부 일관성 | (신규) |

**Quantum 합계**: ~$200 (8개 모두) ← budget 정확 매칭

---

## 3. AI 대안: watsonx.ai 활용 (quantum 안 가는 path)

| # | 실험 | substrate | cost (est) | anima 가치 |
|---|---|---|---|---|
| **W1** | **watsonx Granite 3B/8B teacher** (Paradigm D 대체 7B) | watsonx.ai | $30 | ⭐⭐ Apache 2.0 teacher 대안 |
| **W2** | **Watson NLP baseline F1** (vs Llama anchor 0.1555) | Watson NLP | $20 | ⭐⭐ F1 cross-vendor anchor |
| **W3** | **Watson Discovery + anima paper corpus** (semantic search infra) | Discovery | $30 | ⭐ 검색 backbone |

---

## 4. Top experiment 상세 spec

### 4.1 #1 CHSH cross-vendor (가장 추천)

| 항목 | 값 |
|---|---|
| 목적 | Braket S=2.808 (8.97σ) → IBM에서도 동일 violation 검증, vendor-bias 배제 |
| hardware | IBM Heron r2 156-qubit (heavy-hex topology) |
| trials | 1000 trial × 4 measurement basis = 4000 shot |
| cost | ~$20 ($1.60/sec × ~12sec actual QPU time) |
| wall | 3-5min (queue + execute) |
| output | S 값 + 표준편차 → Braket S=2.808 비교 |
| risk | IBM queue 대기 변동 (peak hours 1hr+) |
| code base | anima/state/nexus_chsh_bell_2026_05_02/ Bell circuit Qiskit port |

### 4.2 #2 IIT 4.0 MIP on N=4 real QPU

| 항목 | 값 |
|---|---|
| 목적 | braket_iit40_mip_2026_05_02 simulator 결과를 real QPU로 재측정 |
| hardware | Eagle r3 127-qubit (4-qubit subset) |
| circuit | TPM 측정용 process tomography circuit (4-qubit, depth ~20) |
| trials | 100 partition combinations × 1024 shots |
| cost | ~$30 |
| anima 정합 | φ★ baseline +41.86 (HID=8) anchor 와 cross-substrate 일치 검증 |

### 4.3 #5 QRNG IBM QPU (cheapest)

| 항목 | 값 |
|---|---|
| 목적 | nexus QRNG의 HMAC-DRBG → 진짜 quantum hardware entropy로 보강 |
| hardware | open tier (Hadamard + measurement) |
| trials | 1024 × 100 batch = 102K bits |
| cost | ~$5 |
| 통합 | nexus QRNG 측 entropy provenance 강화 |

---

## 5. Path 옵션

| path | 실험 | 비용 | 의미 |
|---|---|---|---|
| **Path X (quantum-focus)** | #1, #2, #3, #5, #6 | ~$110 | anima 정합 최강 5개, $90 buffer |
| **Path Y (quantum-full)** | #1-#8 | ~$200 | 8개 모두, budget 정확 소진 |
| **Path Z (mixed)** | #1, #2, W1, W2 | ~$100 | quantum 핵심 + AI 대안 |
| **Path W (AI-only)** | W1, W2, W3 + GPU | ~$200 | watsonx 깊게, quantum skip |

---

## 6. ASCII priority matrix

```
H ┃ #1 CHSH cross    #3 N-12 IIT      │
i ┃ #2 IIT 4.0 MIP                    │  ← anima quantum framework 직접
g ┃                                   │     검증 path
h ┃ ──────────────────────────────────┤
  ┃ #4 process tom    #6 heavy-hex    │
M ┃ #5 QRNG IBM       #7 distillation │
  ┃                                   │
L ┃ #8 multi-backend  W1 watsonx      │  ← 보조 / 다양성
  ┃ W2 NLP            W3 Discovery    │
  ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   $5     $20     $30     $40+ cost
```

---

## 7. Honest C3 (raw#91)

1. **$200 IBM Quantum = 매우 적음** (premium QPU $1.60/sec). 큰 회로/긴 shot 불가. 작은 N=4-8 회로 다수 권장.
2. **Queue 대기 변동** — 무료/저가 backend는 1-24hr 대기 가능. budget 압박 시 priority queue ($/extra) 고려.
3. **Heron r2 156-qubit ≠ 156 qubit usable** — heavy-hex connectivity 제약으로 실제 entangle 가능 qubit 수 적음.
4. **Cross-vendor 검증 결정성** — Braket과 IBM 결과 일치 시 hardware-independent quantum violation 확인. 불일치 시 vendor 의존성 증거.
5. **$200은 1회성 credit** — 결과 안 좋아도 추가 spend는 본 budget 외. priority sort 권장.
6. **IBM Cloud signup 시 정책 확인 필요** — 일부 region은 Quantum 미지원, watsonx도 region 의존.
7. **B3 CHSH cross-vendor**가 가장 결정적. 단 1개만 하면 #1 추천.
8. **Cost 추정치** — 실제 QPU runtime은 circuit depth + queue variability 따라 변동 ±50%.
9. **anima quantum 모듈 (Qiskit) 미설치** — 첫 실험 시 dev env 셋업 wall 1-2hr 추가.
10. **No execution committed** — 본 doc은 spec only. 각 실험 EXEC 시 user 명시 OK 받음.

---

## 8. References

- nexus QRNG: `state/nexus_qrng_quantum_seed_2026_05_02/`
- nexus CHSH Bell: `state/nexus_chsh_bell_2026_05_02/` (S=2.808, 8.97σ)
- N-12 IIT multi-witness: `state/n12_iit_braket_multiwitness_2026_05_02/` (φ proxy ≠ φ★)
- Braket IIT 4.0 MIP: `state/braket_iit40_mip_2026_05_02/` (proper φ★ = 0 with marginalized TPM)
- alpha endpoint reboot (HF token reference): `state/alpha_endpoint_reboot_2026_05_02/`
- IBM Cloud Quantum docs: https://quantum-computing.ibm.com/
- watsonx.ai: https://www.ibm.com/products/watsonx-ai

---

## 9. Decision matrix

| User signal | action |
|---|---|
| "Path X go" | spec out 5 quantum experiments + IBM Quantum env setup BG |
| "Path Y go" | spec out 8 + budget allocation + queue scheduling |
| "Path Z go" | quantum + watsonx hybrid spec |
| "Path W go" | watsonx-only spec |
| "#1 go" | CHSH cross-vendor only (cheapest decisive experiment) |
| "보류" | doc only, EXEC 결정 후일 진행 |
