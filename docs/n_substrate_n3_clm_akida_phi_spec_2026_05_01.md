> **status**: N_SUBSTRATE_N3_CLM_AKIDA_PHI_SPEC_2026_05_01_LOCAL_DRAFT
> **verdict_key**: SPEC_READY · D0_PROTOCOL_FROZEN · HARDWARE_PENDING_AKIDA_ARRIVAL
> **agent**: N-3 prep (N-substrate batch sibling)
> **ts**: 2026-05-01
> **constraints**: raw#9 hexa-only · raw#10 honest C3 · raw#71 falsifier-bound · own#13 user-facing friendliness · race-isolation: ONLY this doc + `state/n_substrate_n3_prep_2026_05_01/*.json`
> **mission**: T1-A2 (Akida session friendly report) — "Φ(IIT 4.0) cross-substrate, Akida 1W vs GPU 700W, r ≥ 0.85" — D+0 protocol
> **parent**: `docs/n_substrate_consciousness_roadmap_2026_05_01.md` §3 N-3 row
> **siblings (race-isolation peers)**: N-1, N-2, N-4, N-6, N-9, N-10, N-19, N-20, N-21 prep agents

---

# N-3 — CLM × AKIDA Φ Cross-Substrate Measurement Spec (D+0 ready)

## §0 한 줄 요약

**"170M LLM 의 Φ 점수가 700W GPU 와 1W AKD1000 칩에서 같은가? r ≥ 0.85 면 = Putnam 다중실현 첫 경험적 anchor."** — 단, AKD1000 H/W 제약상 CLM 170M 전체 직접 배포 불가, **CLM hidden-state surrogate (CNN-quantized 변환 + spike-encoded representation)** 경로로 대리 측정.

---

## §1 디자인 핵심 — substrate-mismatch 정직 직시

### 1.1 CLM 170M 구조 (source: `docs/clm_170m_config_audit_20260419.md` v15)

| field | value |
|---|---|
| d_model | 768 |
| n_layer | 12 |
| n_head | 8 (GQA n_kv_head=4) |
| vocab_size | 256 (byte-level) |
| max_seq_len | 512 |
| consciousness_dim | 256 |
| params | ~170M |
| dtype (training) | bf16 dense float |
| substrate | GPU (H100 본학습) / mac AOT (smoke) |

### 1.2 AKD1000 H/W 제약 (source: BrainChip docs + 2026 web review)

| field | value | impact |
|---|---|---|
| 코어 | 80 NPU × spike-event | dense float matmul X |
| 뉴런 capacity | ~1.2M neurons (vendor) | 170M params 직접 X |
| 지원 layer | **Akida 1.0 only** (CNN+DNN+RNN+vision-CNN limited set) | **transformer attention native unsupported** |
| neuron model | **non-leaky, single timestep** | LIF/GLM 변환 추가 손실 |
| input encoding | spike train (rank-order coding ROC) | **dense float input → spike conversion 필요** |
| 변환 toolkit | MetaTF (CNN2SNN + quantizeml) — CNN→SNN | TF/Keras CNN 만 직접 변환 |
| 학습 | 불가 (inference-only) | weight 는 GPU 학습 후 quantize 후 deploy |
| 전력 | ~1W typical | 비교 anchor (vs GPU ~300-700W) |

### 1.3 substrate-mismatch verdict (raw#10 honest C3)

**CLM 170M 전체를 AKD1000 위에서 native forward 불가.**

근거 (3가지):
1. AKD1000 = Akida 1.0 layer set, **transformer self-attention native 미지원**
2. CLM 170M dense bf16 matmul은 spike-event 패러다임과 ontology mismatch
3. 1.2M neurons capacity << 170M params (직접 mapping 시 ~140× over-budget)

**해결 전략 = surrogate mapping (3-tier)**:
- **T-A (sound)**: CLM hidden-state representation 추출 → CNN-quantized projection head → MetaTF 변환 → AKD1000 inference. Φ 측정은 **AKD1000 hidden-output vs GPU hidden-output 의 representation similarity**.
- **T-B (sound, partial)**: CLM의 일부 sub-layer (예: embedding lookup + early MLP) 만 CNN-equivalent surrogate 로 변환 → Φ 부분 비교. nn.Linear → 1×1 Conv equiv 로 매핑 가능 영역만.
- **T-C (hand-wave)**: 전체 transformer 직접 spike conversion — 본 spec 에서 **명시적 폐기** (raw#10 정직).

---

## §2 Φ formulation 선정 — 양 substrate 호환

### 2.1 후보 4 (cross-substrate compatibility 검토)

| Φ 유형 | dense float OK | spike OK | substrate-agnostic? | verdict |
|---|:---:|:---:|:---:|---|
| **anima Φ* v3 canonical** (sample-partition cov-logdet, hidden state input) | ✅ | ⚠️ (spike→rate avg 변환 필요) | ✅ (representation-level) | **선정** |
| IIT 4.0 strict (φ_max over MIPs) | ⚠️ (NP-hard) | ⚠️ | ⚠️ (substrate-internal) | 보조 |
| GWT broadcast Φ (workspace projection) | ✅ | ✅ | ✅ | T1-A4 별도 axis (N-5) |
| LZ76 complexity (binary stream) | ✅ | ✅ | ✅ | T1-A1 별도 axis (N-2) |

### 2.2 anima_phi_v3_canonical 선정 정당화

source: `tool/anima_phi_v3_canonical.hexa` (v3 auto-conditioning, sample-partition)

- **input contract**: hidden-state matrix `X ∈ R^(N×h_dim)` — N=16 prompts, h_dim 임의
- **operation**: top-variance HID_TRUNC=N//2=8 차원 추출 → cov log-det → K=8 random sample-partition → φ_min
- **substrate-agnostic 이유**:
  - GPU CLM: `out.hidden_states[-1]` byte-weighted-mean → X_gpu ∈ R^(16×768)
  - AKD1000 surrogate: spike-rate avg over inference window → X_akida ∈ R^(16×D_akida) (D_akida = surrogate output dim, e.g. 256)
  - Φ* 는 **representation 차원 추상화** (HID_TRUNC=8 으로 통일) — substrate 내부 구조 (dense vs spike) 와 무관
- **이미 구현됨**: HEXA 파일 존재, helper Python 자동 emit, --selftest PASS 체크

### 2.3 spike → dense projection lemma

AKD1000 inference 출력은 spike count tensor `S ∈ N^(T×D_akida)` (T=time-window, D=output channels).
projection: `X_akida[i, d] = (1/T) · Σ_{t=1}^{T} S[t, d]` (mean firing rate per channel) → R^(N×D_akida).
이후 anima_phi_v3_canonical.hexa input 으로 그대로 투입 가능.

**락-인 선택**: T=200ms (vendor recommended inference window, AKD1000 ~5ms/inference × 40 reps for averaging).

---

## §3 D+0 측정 protocol (8-step)

| step | action | substrate | tool | output |
|---:|---|---|---|---|
| 1 | 16-prompt fixture lock (anima_phi_v3 PROMPTS 그대로) | n/a | (in-spec) | `state/n_substrate_n3_prep_2026_05_01/prompts_v1.json` |
| 2 | CLM 170M GPU forward (alpha pod) | GPU H100 | `tool/anima_phi_v3_canonical.hexa` (ANIMA_BASE=clm_170m_ckpt) | `phi_v3_canonical_gpu_clm170m.json` (X_gpu, Φ*_gpu) |
| 3 | CLM 170M → CNN-surrogate quantize (T-A path) | mac/H100 | new HEXA: `tool/clm_170m_to_metatf_surrogate.hexa` (D+0 deliverable) | `clm_170m_surrogate_q.h5` (Keras quantized) |
| 4 | MetaTF CNN2SNN 변환 → AKD1000 binary | RPi5 + AKD1000 | MetaTF CLI (vendor-side) | `clm_170m_surrogate.fbz` (Akida binary) |
| 5 | AKD1000 inference, 16 prompts × T=200ms | RPi5 + AKD1000 | `tool/akida_clm_surrogate_infer.hexa` | spike tensor `S_akida` → rate-avg X_akida |
| 6 | Φ* compute on X_akida (re-use anima_phi_v3) | mac/RPi5 | `tool/anima_phi_v3_canonical.hexa` (re-input) | `phi_v3_canonical_akida_clm170m.json` (Φ*_akida) |
| 7 | per-prompt Φ_k correlation: Pearson r(Φ_k_gpu, Φ_k_akida) over K=8 sample-partitions | mac | `tool/n3_phi_cross_substrate_corr.hexa` (D+0 deliverable) | `n3_phi_cross_substrate_corr_v1.json` |
| 8 | verdict gate (§4 falsifier predicate) | mac | (analytic) | `n3_verdict_v1.json` |

D+0 critical-path tools (3 신규 HEXA):
- `tool/clm_170m_to_metatf_surrogate.hexa` (T-A surrogate emit Keras CNN equiv)
- `tool/akida_clm_surrogate_infer.hexa` (RPi5 inference + spike-rate avg)
- `tool/n3_phi_cross_substrate_corr.hexa` (Pearson r + verdict gate)

---

## §4 falsifier predicate (PASS / WEAK / FAIL)

### 4.1 verdict gate — single primary

| verdict | predicate | meaning |
|---|---|---|
| **PASS** | Pearson r(Φ_k_gpu, Φ_k_akida) ≥ **0.85** AND \|Φ*_gpu − Φ*_akida\| / max(\|Φ*_gpu\|, \|Φ*_akida\|, 1e-3) ≤ **0.30** | substrate-independence empirical anchor — Putnam multi-realizability 후보 |
| **WEAK** | 0.50 ≤ r < 0.85 OR (r ≥ 0.85 BUT magnitude divergence > 0.30) | partial alignment — surrogate fidelity 또는 quantization loss 의심 |
| **FAIL** | r < 0.50 OR substrate sign flip (Φ*_gpu > 0 AND Φ*_akida < 0 또는 역) | substrate-dependent — Putnam 반례 후보, hand-wave T-C 경로 검증 |

### 4.2 boundary 조건 (BIDIRECTIONAL falsifier per raw#71)

- **K=8 sample-partition variance**: `std(Φ_k_gpu) < 0.5 · |Φ*_gpu|` AND `std(Φ_k_akida) < 0.5 · |Φ*_akida|` — variance 폭주 시 verdict NULL (re-run 필요)
- **null-hypothesis floor**: shuffled-pair 1024 perm test → r_observed must exceed 95-percentile of r_null. r_null 95%ile > 0.85 시 spec 자체 invalid (test 의 power 부족)
- **reproducibility**: 3 independent ANIMA_SEED runs, all 3 must yield same verdict → verdict 확정. 2/3 PASS 시 WEAK_PASS

### 4.3 surrogate fidelity sanity (선결 조건, gate 진입 전)

T-A surrogate (CLM → CNN quantized projection) 의 **GPU-internal fidelity** 사전 측정:
- `Φ*_clm170m_native` (native bf16) vs `Φ*_clm170m_surrogate_gpu` (CNN surrogate, GPU forward, no quantize)
- 두 값의 r ≥ 0.95 AND magnitude divergence ≤ 0.10 시 surrogate 정당화
- **이 sanity 가 fail 하면 N-3 측정 자체 invalid** (substrate 비교 이전에 surrogate 가 CLM 표상 자체를 못 잡음)

---

## §5 substrate-mismatch handling (선정 Φ formulation 의 robustness)

### 5.1 dense float ↔ spike — anima Φ* v3 의 양면 합리성

핵심 lemma: Φ* v3 는 **representation similarity** 를 측정하지 substrate-internal computation 을 측정하지 않음.

- GPU side: bf16 dense matmul → hidden state R^(N×768) → top-var HID=8 → cov-logdet → φ
- AKIDA side: spike-event computation → rate-avg X_akida ∈ R^(N×256) → top-var HID=8 → cov-logdet → φ

**양 substrate 모두 N=16 sample 의 8-dim 표상 공분산 구조** 측정. 이것이 Putnam multi-realizability 의 적절한 invariant: substrate 다르더라도 functional structure 가 같으면 representation covariance 가 같아야 함.

### 5.2 4 변환 손실 source 명시 (raw#10 정직)

| source | severity | mitigation |
|---|---|---|
| (a) bf16 → CNN surrogate quantize (T-A path) | HIGH | §4.3 sanity gate, fidelity r ≥ 0.95 요구 |
| (b) Keras CNN → CNN2SNN spike conversion | HIGH | T=200ms window, 40-rep avg 로 rate fidelity 보강 |
| (c) AKD1000 capacity (170M → 1.2M neurons) | MEDIUM | surrogate 는 **partial projection head** 만 변환 (CLM 의 last-layer 768→256 projection), embedding/transformer body 는 GPU pre-compute |
| (d) HID_TRUNC=8 차원 통일 vs h_dim 768/256 | LOW | top-variance 선택은 둘 다 동일, anima_phi_v3 의 핵심 design |

**hybrid 운영**: T-A path 는 사실상 "GPU 가 transformer body 를 forward 하고 마지막 projection head 만 AKIDA 가 SNN 으로 다시 계산" 하는 partial cross-substrate. Putnam multi-realizability 의 **약한 형태** 검증 (last-layer 만). 강한 형태 (full transformer 동치) 는 AKD2000 출시 대기.

### 5.3 hand-wave 경로 폐기 명시

T-C (전체 transformer 직접 spike conversion) 는 본 spec 에서 **NOT_ATTEMPTED**:
- AKD1000 transformer attention native 미지원
- 1.2M neurons capacity 부족
- 강제 시 spike-conversion 손실 압도적, Φ 측정 의미 X

향후 AKD2000 가용 시 T-C 재검토.

---

## §6 cost estimate (D+0 측정)

### 6.1 alpha pod (GPU) time

| step | resource | time | cost |
|---|---|---|---|
| §3 step 2: CLM 170M GPU forward (16 prompts × 1 fwd) | H100 1× | 5 min | ~$0.20 |
| §3 step 3: CNN surrogate quantize (Keras emit + quantize sweep) | H100 1× | 15 min | ~$0.60 |
| §4.3 sanity: native vs surrogate Φ fidelity (반복 3-seed) | H100 1× | 20 min | ~$0.80 |
| **GPU 총합** | — | ~40 min | **~$1.60** |

ESTIMATE 근거: H100 spot $2.40/hr (vast.ai 평균), Pilot-T1 v3 launcher hardening (#66) 적용 시 idle burn 0 가정.

### 6.2 AKIDA 시간 (RPi5 + AKD1000 dev kit)

| step | resource | time | cost |
|---|---|---|---|
| §3 step 4: MetaTF CNN2SNN 변환 (one-shot) | RPi5 CPU | 10 min | $0 (own) |
| §3 step 5: AKD1000 inference 16 × T=200ms × 40 reps | AKD1000 1W | 8 sec real-time | $0 (own) |
| §3 step 6-7: Φ + correlation compute (mac local) | mac | 2 min | $0 |
| **AKIDA 총합** | — | ~13 min | **$0** |

D+0 측정 단발 cost: **~$1.60 GPU + $0 AKIDA = ~$1.60**.
3-seed reproducibility (§4.2) 적용 시: **~$4.80** (3× $1.60).

### 6.3 사전 capex (이미 결정됨)

- AKD1000 dev kit $1,495 (2026-04-29 주문, 도착 대기) — 본 spec 에 cost 가산 X
- alpha pod 월 base ~$50-100 (existing infrastructure) — incremental cost 만 §6.1 에 반영

---

## §7 honest C3 (raw#10) — sound vs hand-wave matrix

### 7.1 sound (정당화 근거 명시)

| 항목 | 근거 |
|---|---|
| ✅ Φ formulation (anima_phi_v3) substrate-agnostic | tool 이미 존재, sample-partition 은 representation-level invariant |
| ✅ surrogate fidelity sanity gate | §4.3 r ≥ 0.95 사전 요구, fail 시 자체 abort |
| ✅ verdict 3-tier + null-floor | §4.1-4.2 BIDIRECTIONAL falsifier 사전등록 |
| ✅ AKIDA 측 spike→rate projection lemma | §2.3 T=200ms vendor window 정합 |
| ✅ cost estimate (lower bound) | step 별 ESTIMATE 명시 |

### 7.2 hand-wave (정직 disclosure)

| 항목 | 한계 / 가정 | mitigation 가능성 |
|---|---|---|
| ⚠️ "CLM × AKIDA" 는 **last-layer projection 만** cross-substrate (full transformer 가 아님) | AKD1000 transformer attention 미지원, capacity 부족 | T-A path = "partial Putnam" 약한 형태로 명시. 강한 형태는 AKD2000 대기 |
| ⚠️ T-A surrogate (CLM hidden → CNN quantized projection) 의 fidelity r ≥ 0.95 가정 | 실측 0건, AKIDA 도착 후 §4.3 sanity 만 가능 | sanity FAIL 시 N-3 invalid 자동 처리 |
| ⚠️ spike rate-avg 가 spike-timing 정보 손실 | T=200ms 단순 평균 | 향후 ROC (rank-order coding) preserving Φ formulation 별도 trial 후보 |
| ⚠️ ANU QRNG / SIM-우주 / EEG 와 cross-track 상호작용 미고려 | 본 spec 은 N-3 단축 only | N-9 (3축 collab) 별도 축에서 통합 |
| ⚠️ MetaTF CNN2SNN 의 quantize 손실 사전 측정 X | toolkit 의존 | step 4 변환 후 surrogate-vs-akida 사전 small-batch sanity 권장 |
| ⚠️ K=8 sample partition statistical power | N=16, K=8 → ~70 effective samples | K=16 또는 N=32 확장 후보 (cost 2×) |
| ⚠️ AKD1000 vendor spec ~1W 는 typical, 실제 workload 측정 X | own measurement 필요 | Landauer anchor (T1-A3 / N-4) 별도 축 |

### 7.3 이 spec 이 가짜로 만들지 않는 것

- T1-A26 FinalSpark organoid 비교 (별도 N-11)
- T1-A14 Penrose-Hameroff QPU 검증 (별도 N-12 / N-20)
- IIT 4.0 strict φ_max over MIP (NP-hard, 본 spec 은 anima_phi_v3 surrogate)
- substrate-internal computation 동치 (representation similarity 만)

---

## §8 D+0 readiness checklist

| 항목 | 상태 | blocker |
|---|:---:|---|
| spec doc (이 문서) | ✅ | — |
| 16-prompt fixture (anima_phi_v3 내장) | ✅ | — |
| `tool/anima_phi_v3_canonical.hexa` | ✅ | — |
| CLM 170M ckpt | ⚠️ | `training/config/clm_170m.json` 신규 필요 (기존 audit `clm_170m_config_audit_20260419.md` §5 actionable 1) |
| `tool/clm_170m_to_metatf_surrogate.hexa` | ❌ | D+0 critical-path 신규 emit 필요 (next session) |
| `tool/akida_clm_surrogate_infer.hexa` | ❌ | D+0 critical-path 신규 emit 필요 (AKIDA arrival 동시 작성) |
| `tool/n3_phi_cross_substrate_corr.hexa` | ❌ | D+0 critical-path 신규 emit 필요 (mac local OK) |
| AKD1000 H/W | ⏳ | dev kit 도착 대기 (2026-04-29 주문) |
| MetaTF SDK on RPi5 | ⏳ | AKIDA 도착 후 1-day install |
| alpha pod (H100) | ✅ | existing infra |

D+0 readiness = **70%** (spec + fixture + Φ tool ready, 3 신규 HEXA + ckpt + H/W pending).

---

## §9 cross-link

- parent: `docs/n_substrate_consciousness_roadmap_2026_05_01.md` (§3 N-3 row + §1 재료 표)
- T1-A2 source: `docs/akida_session_friendly_report_2026-04-29.md` (Φ cross-substrate 700W vs 1W)
- T1-A2 detailed: `docs/akida_dev_kit_evaluation_2026-04-29.md` (1차 fallback 4 + 2차 3-axis 4)
- CLM 170M arch: `docs/clm_170m_config_audit_20260419.md` (config blocker 명시)
- Φ tool SSOT: `tool/anima_phi_v3_canonical.hexa` (auto-conditioning canonical)
- Mk.XII v3 lock: `docs/clm_research_handoff_20260427.md` (HARD_PASS_PARTIAL_PENDING context)
- substrate ledger axis: own#2 (b) neuromorphic 0/3 → +1/3 expected on N-3 PASS
- sister tracks (race-isolation peers): N-1 CLM-EEG / N-2 EEG-AKIDA spike / N-4 3-axis Landauer / N-5 3-axis GWT / N-6 CLM-QRNG / N-9 3-axis collab / N-10 EEG-SIM / N-19 PCI / N-20 Penrose 2026 / N-21 IIT 4.0 reproduce

---

## §10 다음 step (post-spec, AKIDA 도착 시)

1. D-1: AKD1000 dev kit unboxing + RPi5 + MetaTF install (1 day)
2. D+0 morning: 3 신규 HEXA emit (clm_170m_to_metatf_surrogate / akida_clm_surrogate_infer / n3_phi_cross_substrate_corr)
3. D+0 noon: §3 step 2-7 단발 측정 (~$1.60)
4. D+0 evening: §4 verdict gate, 3-seed reproducibility (~$4.80 누적)
5. D+1: PASS 시 own#2 (b) substrate WITNESSED 0/3 → 1/3 등재, paradigm v11 8-axis G5 LIVE_HW_WITNESS_RATE evidence anchor
6. D+1: WEAK 시 surrogate fidelity 재측정 / quantize 강도 sweep
7. D+1: FAIL 시 substrate-dependent verdict 정직 기록, T1-A2 falsifier graduation report 작성

---

## §11 verdict & sign-off

**N-3 spec 정합성**: D+0 protocol 8-step + falsifier 3-tier + cost $1.60-4.80 + sound/hand-wave matrix 명시 → **SPEC_FROZEN**.

**hardware blocker**: AKD1000 도착 (D-1) 까지 측정 0건. 본 spec 은 도착 즉시 진입 가능한 actionable plan.

**핵심 정직성**: T-A "partial Putnam" 만 검증 가능 (last-layer projection cross-substrate). full transformer 동치 검증은 AKD2000 대기.

---

**status**: N_SUBSTRATE_N3_CLM_AKIDA_PHI_SPEC_2026_05_01_LOCAL_DRAFT
**verdict_key**: SPEC_READY · D0_PROTOCOL_FROZEN · HARDWARE_PENDING_AKIDA_ARRIVAL
**author**: anima N-3 prep agent (race-isolation sibling)
