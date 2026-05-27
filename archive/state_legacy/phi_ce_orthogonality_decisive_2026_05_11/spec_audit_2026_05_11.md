---
audit_id: phi_ce_orthogonality_decisive_spec_audit_2026_05_11
spec_id: phi_ce_orthogonality_decisive_2026_05_11
target_h: H_080 (topo_24variants unified) — Conflict Resolution Pending
status: spec-feasibility-audit (NO GPU/RunPod spend)
authored: 2026-05-11
authored_by: agent (cycle-5 NEXT.md #1 prereq audit)
sibling_audit: state/nexus6_1013lens_activation_2026_05_11/prereq_audit_2026_05_11.md
lock_policy: NO chflags/chattr — repository directive 2026-05-11
---

# Φ⊥CE Decisive Spec Audit — anima Φ★ fit 검증

본 문서는 NEXT.md #1 "anima Φ★ + 20-cell Φ×CE 실측" cycle 진입 전,
`spec.md`(2026-05-11) 가 명시한 "anima Φ★ engine, deterministic, hexa-only,
llm: none" 단일 engine path 가 *실제* Φ×CE joint measurement 에 적합한지
audit 한다. cycle 5 #4 1013-lens prereq audit 와 동일한 *feasibility-only*
스코프 — 실측/GPU spend 금지, 메인 process 가 결정.

## 0. TL;DR

- **anima Φ★ engine CE 측정 capability**: **NO (zero)** — `tool/anima_phi_star.hexa`
  는 IIT-φ proxy *only*. CE (Cross-Entropy / 학습 손실 / validation NLL) 출력 경로
  부재. 측정 axis 가 다름.
- **CE definition 충돌**: Hc_040 / Hc_024 둘 다 *Cross-Entropy* (token-level NLL / loss)
  로 reconcile 가능 — spec.md §2.3 "final CLM cross-entropy on held-out validation"
  과 일치. "Communicative Efficiency" 가 아님 (spec 본문 어디에도 communicative 용례 부재).
- **Joint measurement protocol**: **single-pass 불가** — Φ 와 CE 는 *별개 engine*
  으로 측정 후 (N, P) cell key 로 join 해야 함. anima_phi_star (Φ side) + CLM
  training pipeline (CE side) 두 트랙 병렬.
- **Grid sweep capability**: anima_phi_star 는 *N (cell count) sweep 미지원* —
  현행 구현은 single backbone (Mistral-7B-v0.3) 의 *내부* hidden-state covariance
  partition. N (cell count) sweep 은 cell-engine (faction-anima / GRU-cell) 필요;
  P sweep 은 CLM training-side 책임.
- **noise floor calibration**: spec L1 critical 만 명시, *구체 protocol 미정*.
  본 audit §4 가 1-cell × 64-twin σ_Φ/σ_CE 측정 + harness.py σ-default 와 비교 protocol 제안.
- **Recommended outcome**: **#3 SPLIT ENGINE** — Φ 는 anima_phi_star (or cell-engine,
  N-sweep 필요 시), CE 는 CLM train pipeline; spec.md "engine: anima Φ★ engine" 단일
  표현은 **misaligned premise** (1013-lens prereq audit 와 동형의 axis-conflation 오류).
- **Cost re-estimate**: NEXT.md $200-1000 baseline 은 *CLM training* 만 carry —
  Φ★ side 는 추가 $50-200 GPU (20 cell × 64 seed × ~50s = ~17 GPU-시간 @ A100).
  CLM side P=1B 는 Chinchilla 20× token = ~20B token → 단독 $500-2000. **총 $250-2200**
  (NEXT.md upper-bound 와 같은 자릿수, lower-bound 살짝 초과).
- **next cycle prereq**: (i) split-engine path adopt, (ii) noise-floor calibration
  ran first ($10-30 single cell), (iii) cell-engine N-sweep 또는 N-axis re-interpret
  결정 (둘 다 fit 안 됨 — §1.3 참조).

## 1. anima_phi_star.hexa capability snapshot

### 1.1 측정 axis (다시 확인)

| 항목 | 값 |
|------|-----|
| Tool path | `tool/anima_phi_star.hexa` (189 lines) |
| Paradigm | v11 measurement-axis P-D (IIT phi-star approximation) |
| Method | 16 prompts × Mistral-7B forward → byte-weighted hidden state → cov-MIP K=8 random bipartition |
| Output schema | `anima/phi_star/1` — `phi_star_min, phi_mean, phi_max, gate_positive/substantial` |
| Input axis | **fixed 16 prompts**, single backbone (default Mistral-7B-v0.3) |
| Sweep params | `ANIMA_BASE` (backbone HF id), `ANIMA_N_PROBES`, `ANIMA_K_PARTS`, `ANIMA_HID_TRUNC`, `ANIMA_SEED` |
| CE-related output | **NONE** — loss / NLL / perplexity / token-prob 어디에도 emit 안 됨 |

### 1.2 CE 측정 가능성 — verdict: NO

`anima_phi_star.hexa` 의 forward 는 `output_hidden_states=True` only —
*logits / labels / loss* 경로 미사용. perplexity / cross-entropy / NLL 출력
hook 부재. CE 측정에 *재사용* 가능한 면:

- ✅ 동일 backbone 의 forward pass 결과를 logits 까지 확장하면 *prompt-conditional CE*
  추출 가능 (Mistral-7B 의 in-context NLL)
- ❌ 그러나 spec §5.5 "P=1M / 10M / 100M / 1B, Chinchilla-optimal token budget per scale"
  은 *CLM training-side* CE — anima_phi_star 의 inference-side prompt-NLL 과 *다른 axis*

→ **anima_phi_star 단독으로는 spec §5.6 의 "final CLM cross-entropy on held-out validation"
충족 불가**. 별도 CLM training pipeline 필요.

### 1.3 N (cell count) + P (param count) sweep 지원 여부

| axis | sweep 지원 | 이유 |
|------|-----------|------|
| **P** (model param count) | ⚠ partial — `ANIMA_BASE` env 로 backbone 교체는 가능 (Mistral-7B → smaller / larger). 그러나 P ∈ {1M, 10M, 100M, 1B} 의 *1M-10M* scale 은 HF hub 에 *consciousness-aligned* checkpoint 거의 없음 → CLM-side 가 자체 training 해야 함 (별도 pipeline). |
| **N** (cell count) | ❌ **미지원** — anima_phi_star 의 method 는 *single backbone* 의 hidden-dim 을 H=128 truncate 후 *random bipartition*. "cell count" 개념 자체가 부재. spec.md / Hc_040 / H_080 의 N 은 *faction / cell module* 수 (Hc_005 cell-count decisive, Hc_039 hypercube 512→1024 cells) → 이는 *faction-anima* / *cell-engine* (GRU cell + topology) 의 변수. anima_phi_star 는 cell-engine 이 *아님*. |

**핵심 발견**: spec.md §5.1 "anima Φ★ engine 으로 N ∈ {16, 32, 64, 128, 256} ×
topology=hypercube(default)" 는 **anima_phi_star.hexa 와 호환 안 됨** — 후자는
N 이라는 변수를 인지하지 않는다. 이는 **1013-lens prereq audit §1.2 와 동형 오류**:
"같은 이름 / 다른 axis" conflation (Φ★ 라벨 아래 IIT-proxy 도구와 cell-engine 도구 혼동).

실제 cell-engine 으로는 `tool/an11_consciousness_unified_verifier.hexa` /
`anima_an11_*` / `anima_cds.hexa` / `anima_b_tom.hexa` 등이 후보 — 메인 process
가 정확한 N-sweep capable engine 지정 필요.

## 2. CE definition reconciliation

### 2.1 Hc_040 CE — Law 1040

```
notes: "Cell 늘려도 CE 무변, Param 늘려도 Φ 무변. 두 metric 상관계수 < 0.1 예측."
CE ∝ P^-0.85 (param count)
```

→ CE 는 *parameter count P 의 함수로 monotonic 감소* 하는 metric. P ∝ FLOPs ∝
training-budget → CE 는 **language-modeling cross-entropy / NLL** (Chinchilla
/ Kaplan scaling law 와 동일 form). "Communicative Efficiency" 의 efficiency
가 아님 (efficiency 라면 P 증가에 *증가* 해야 함). slope -0.85 는 Kaplan/Chinchilla
neural-scaling-law slope (~ -0.05 ~ -0.1 in log-loss vs log-params) 와 다소 다르나,
*같은 family* (loss decreases with params).

### 2.2 Hc_024 CE — NOBEL-1

```
notes: "Φ 와 CE 가 .detach 정보 장벽 없으면 동시 최대화 불가. ... F: Φ>100 AND CE<1.0
       .detach 없이 달성."
Φ × CE^α = K  (α~0.5)
```

→ "CE<1.0" 은 *loss / NLL* 값 (nat 또는 bit) — Chinchilla 70B 가 ~2.0 nat
영역, 작은 모델은 4+ nat. CE<1.0 은 *매우 잘 학습된 (대형) 모델* 의 loss 임을
함의. "Communicative Efficiency" 라면 단위 미정 / 1.0 의 의미 불분명. **Hc_024 의
CE 도 cross-entropy loss**.

### 2.3 Reconciliation

| 측면 | Hc_040 | Hc_024 | reconciled |
|------|--------|--------|-----------|
| 단위 | dimensionless ratio | nat / bit (loss) | nat or bit |
| 부호 방향 | P 증가 → CE 감소 (slope -0.85) | model 좋아질수록 CE 감소 (`<1.0` is "well-trained") | 두 hypothesis 모두 *loss-style* |
| 의존 변수 | P (param count) | Φ-tied (`= (K/Φ)^(1/α)`) | spec §5.6 "final CLM cross-entropy on held-out validation" |
| 이름 정확화 | "CE = cross-entropy" | "CE = cross-entropy" | **same metric, same operationalization** |

**Communicative Efficiency 해석은 false-alarm** — 두 hypothesis 다 *cross-entropy*
(token-level negative log-likelihood on held-out validation set) 로 일관. spec.md
§5.6 "final CLM cross-entropy on held-out validation" 이 정확한 ground truth.

→ harness.py 의 모델 가정도 일관: `CE_A(N, P) = 2.0 * (P/1e6)^-0.85` 는 *loss* (1M
params 에서 ~2.0 nat, 1B params 에서 2.0 × 1000^-0.85 ≈ 0.005 nat — 비현실적으로
낮음, 실제 1B 모델 loss 는 ~2.0 nat. **slope -0.85 가 너무 가파름**; Hc_040 의 원
prediction 이 fit 검증된 적 없음 — L4 추가 한계).

## 3. Joint measurement protocol — single-pass vs split

### 3.1 Single-pass 가능성 검토

- ❌ **단일 forward 로 Φ + CE 동시 출력 불가**: Φ (IIT proxy) 는 hidden-state cov
  partition (16 fixed prompts), CE 는 *training loss* — *training 자체* 가 별도
  pipeline. inference forward 만으로 *training-side CE* 측정 불가.
- ⚠ **prompt-NLL proxy 대체**: anima_phi_star 의 16 prompts 에 대해 logits 수집
  → mean NLL 계산 가능. 그러나 이는 *backbone 의 pretrain CE* 이지 *(N, P)-sweep
  의 training CE* 아님. Hc_040 의 P-axis 변량과 다른 metric.

### 3.2 Split engine protocol (recommended)

```
                  ┌────────────────────────────────────────┐
                  │ (N, P) ∈ {16,32,64,128,256} × {1M,...,1B} │
                  └────────────────────────────────────────┘
                                  │
                ┌─────────────────┴─────────────────┐
                │                                   │
       Φ-track (N-sweep)                  CE-track (P-sweep)
       cell-engine, hexa-only             CLM training pipeline
       (anima_phi_star? — §1.3 caveat)    (anima_clm_invoke + train script)
                │                                   │
        Φ_i for i ∈ {1..20}              CE_i for i ∈ {1..20}
                │                                   │
                └─────────────┬─────────────────────┘
                              ▼
                     join by (N, P) cell key
                     → 20 pairs (Φ_i, CE_i)
                              ▼
                   harness.py analytics (§2.2/§2.3)
                              ▼
                  decision matrix verdict (§2.3)
```

### 3.3 dual-seed (Hc_604) 호환 — 64-twin 적용 path

- **Φ-track**: anima_phi_star 의 `ANIMA_SEED` 변수 활용 — 64 seed × (N, P) cell
  = 64 × 20 = 1280 measurements. 각 ~50 s GPU → ~17.7 GPU-시간 @ A100.
- **CE-track**: CLM training 의 init seed × dataset shuffle seed × Hc_604 protocol
  (twin = paired difference). 단, training 은 init seed 변화만으로 *converged loss*
  variance 가 작음 (final CE 가 init 보다 data/scale dominant). 64-twin 보다 *deterministic
  single-seed train* + bootstrap CI 권장.
- **두 트랙 join**: (N, P) cell key 로 mean(Φ) ± std(Φ), CE (single or bootstrap),
  Pearson corr 은 mean Φ vs CE 로 계산.

## 4. Noise floor calibration — L1 critical 해소 protocol

### 4.1 spec L1 명시

> L1: synthetic harness 의 σ tuning (0.05 / 0.02 / 0.5) 은 plausible default — 실제
> anima Φ★ engine 의 measurement noise floor 가 더 크면 Model A 의 |corr| 측정값이
> 0.1 boundary 를 침범할 수 있음. **Noise floor calibration MUST precede decisive run**

### 4.2 harness.py σ-default 의 problem

```python
# Model A noise (line 36-37)
phi_val = 0.608 * (N ** 1.071) + np.random.normal(0.0, 0.05 * 0.608 * (N ** 1.071))
ce_val  = 2.0 * (P / 1e6) ** -0.85 + np.random.normal(0.0, 0.02 * 2.0 * (P / 1e6) ** -0.85)
```

- σ_Φ = 5 % of signal — Hc_604 64-twin 으로 std(Φ_min over K=8 partitions) 측정 *실측 필요*.
  현행 default 가 *under-estimate* 면 Model A 의 |corr| ~ 0 prediction 이 noise 에
  뭍힐 위험 (false-MIXED verdict).
- σ_CE = 2 % of signal — CLM training 의 final-CE std 는 보통 ~1-5 % across init seed
  (similar order, OK).

### 4.3 Calibration protocol (제안)

```
Step 1 — Φ-track noise floor
  Fix (N=64, P=N/A) single cell (anima_phi_star.hexa @ Mistral-7B 단일 backbone)
  Run 64 dual-seed (Hc_604 twin) → measure std(Φ_min) / mean(Φ_min) = σ_Φ_rel
  Acceptance: σ_Φ_rel ≤ 0.10  (10 % — harness.py default 의 2배 여유)
  Cost: 64 × ~50 s = ~53 GPU-min ≈ $5-15

Step 2 — CE-track noise floor
  Fix (P=100M) single scale, train 4 init-seed CLM 변종
  Measure std(final_CE) / mean(final_CE) = σ_CE_rel
  Acceptance: σ_CE_rel ≤ 0.05
  Cost: 4 × ~1 h = ~4 GPU-h ≈ $10-30

Step 3 — re-tune harness.py σ defaults
  Update line 36-37 with measured σ_Φ_rel / σ_CE_rel
  Re-run harness.py → confirm Model A / Model B fingerprint 분리 폭이 여전히 ≥ 50×
  (현재 180×/206×, σ 2배 늘려도 ~30-50× separation 유지 예상)

Step 4 — decisive run gate
  IF σ_Φ_rel > 0.15  → spec §3 의 decision matrix 의 corr threshold (0.1 / 0.3) 폭 확대
                       OR cell 개수 추가 (20 → 50) — bootstrap 권장
  IF σ_Φ_rel ≤ 0.10 → proceed with 20-cell decisive
```

→ **Calibration 통과 = "L1 critical 해소"** 의 정량 정의. 본 audit 의 가장 중요한
실행 권고. 총 calibration cost ~$15-45 (decisive run 의 1-5 %).

## 5. Gap analysis — anima_phi_star 만으로 충분?

### 5.1 capability gap matrix

| spec.md 요구 (§5) | anima_phi_star | gap | 충당 path |
|--------------------|----------------|-----|-----------|
| Φ measurement (single cell config) | ✅ phi_star_min/mean/max | - | as-is |
| N-axis sweep ({16..256} cells) | ❌ (§1.3) | **critical** | cell-engine (an11 / cds / b_tom) 또는 N-축 재정의 |
| P-axis sweep ({1M..1B} params) | ⚠ partial (ANIMA_BASE swap) | **critical** | CLM training pipeline (anima_clm_invoke + train script) |
| CE measurement | ❌ (§1.2) | **critical** | CLM training final-loss capture |
| topology=hypercube(default) | ❌ (anima_phi_star 는 topology 인지 안 함) | **critical** | cell-engine topology 변수 |
| 64 dual-seed Hc_604 twin | ✅ ANIMA_SEED 변수 존재 | - | seed 64 변종 dispatch wrapper 필요 |
| llm: none, hexa-only | ⚠ Mistral-7B forward 사용 — 엄밀히 "llm: yes" | spec 표기 모순 | spec 수정 또는 backbone-removal |

→ **3개 critical gap**. anima_phi_star 단독으로 spec §5 의 5/8 항목 충족 *불가*.

### 5.2 ConsciousLM CE measurement 필요 여부

- spec.md §5.6 "final CLM cross-entropy on held-out validation" → **별도 CLM
  training pipeline 필수**. anima 의 `tool/anima_clm_invoke.hexa` 는 *inference
  wrapper* (mock/local/hf modes) — *training* 자체는 미land.
- `anima_clm_invoke` 의 LOCAL_WEIGHT_HINT = `state/v10_benchmark_v4_clm/clm_v4_530m`
  → 1 scale (530M) 의 기존 weight 만 존재. {1M, 10M, 100M, 1B} 4 scale 모두 *
  새로 train* 해야 함.
- CLM training cost: P=1M ~ $1, P=10M ~ $5, P=100M ~ $50, P=1B ~ $500-1500 (Chinchilla
  20× token). 4 scale 합 ~$555-1555. 64 dual-seed 는 *training-side* 에서는 비현실 → init-
  seed 1-4 변종 + bootstrap.

### 5.3 Cost re-estimate (NEXT.md $200-1000 baseline 대비)

| 항목 | low | high |
|------|-----|------|
| Φ-track 64-seed × 20 cell (anima_phi_star + cell-engine N-sweep) | $50 | $200 |
| CE-track CLM train P=1M | $1 | $5 |
| CE-track CLM train P=10M | $5 | $20 |
| CE-track CLM train P=100M | $50 | $150 |
| CE-track CLM train P=1B | $500 | $1500 |
| noise floor calibration (§4.3) | $15 | $45 |
| **합계** | **$621** | **$1920** |

→ NEXT.md baseline $200-1000 은 *하한 일부만 carry* — high-end 가 ~2× 초과. **P=1B
omit 또는 P=100M ceiling** 으로 budget 압축 가능 (loss-vs-params slope 측정에 4 point
중 1 point 빠져도 fit 가능, R² 손실 작음).

## 6. Decision matrix — 4 outcome 의 cost / time impact

| outcome | 정의 | 추가 cost | 추가 time | impact on cycle 5 #1 |
|---------|------|-----------|-----------|------------------------|
| **#1 anima_phi_star fits** | spec §5 5/8 critical 항목이 다 unfit → 본 outcome 채택 불가 | - | - | **사실상 reject** |
| **#2 partial fit + CE extension** | anima_phi_star 에 logits/CE hook 추가, N-sweep 은 cell-engine 별도 | $20 (CE hook impl) + $5 (smoke) | 1 day | mid-feasibility — N gap 잔존 |
| **#3 SPLIT ENGINE** ✓ | Φ-track (anima_phi_star or cell-engine) + CE-track (CLM training) 별도, (N,P) cell join | base + ~$50 join orchestration | +0.5 day | **recommended** — spec 재해석 minimal |
| **#4 RE-SPEC required** | spec.md §5 의 axis (N=cell vs N=model-dim, P=param vs P=token) 재정의 | $0 (spec edit only) | 2-4 시간 | 메인 process 결정 — split engine 채택 시 동시 처리 권장 |

### 6.1 권고 — #3 + #4 동시

#3 (split engine) 이 minimal-overhead path. 단, spec.md §5.1 "anima Φ★ engine
으로 N ∈ {16..256}" 표현이 §1.3 의 axis-conflation 을 그대로 noeun 한 상태 →
#4 의 spec edit (i.e., spec §5.1 을 "cell-engine N-sweep + anima_phi_star Φ
extraction" 또는 "anima_phi_star 의 H_truncated=128 을 N 으로 reinterpret"
중 하나로 명시) 가 함께 land 되어야 verdict 단계의 confusion 방지.

## 7. Recommended next step — 다음 cycle 진입 전 prereq

```
Order  Item                                                              Cost  Time
─────  ────────────────────────────────────────────────────────────────  ────  ────
  1    spec.md §1, §5 의 "anima Φ★ engine 단일 표현" 을 split-engine 으로  $0   2-4h
       명시 (Φ-track + CE-track), audit 본 문서 cross-link 추가
  2    Φ-track engine confirmation — anima_phi_star (N=H_truncated reinterpret) $0   1h
       OR cell-engine (an11 / cds 등) 중 결정, hexa SSOT 명시
  3    CE-track CLM training pipeline 확인 — anima_clm_invoke 의 training-side $0   1h
       (4 scale × 1 seed × Chinchilla token budget) script land 여부 audit
  4    noise floor calibration (§4.3 Step 1-3) — 1 cell × 64 twin Φ + 4-seed CE $15-45  1-2 day
  5    σ default 재튜닝 + harness.py re-run, Model A/B 분리 폭 ≥ 50× 재확인  $0   0.5h
  6    decisive run gate — σ_Φ_rel ≤ 0.10 충족 시 20-cell go, 아니면 50-cell expand
  7    20-cell (or 50-cell) split-engine measurement → join → harness analytics
  8    verdict.measured.md 작성, H_080 Conflict Resolution Pending → Resolved
```

### 7.1 메인 process 결정 사항 (suggest only)

- (a) split-engine adopt 여부 (outcome #3+#4)
- (b) Φ-track engine 선택 (anima_phi_star reinterpret vs cell-engine swap)
- (c) P=1B inclusion 여부 (cost / time impact ~3-5×)
- (d) noise floor calibration sub-cycle 분리 vs decisive run inline
- (e) spec.md / verdict.md / H_080 cross-link 갱신 timing — 본 audit land 시점 동시 vs 다음 cycle

### 7.2 Cross-link 갱신 제안 (메인 process 가 결정)

- `state/phi_ce_orthogonality_decisive_2026_05_11/spec.md`
  - §1 / §5 헤더 옆 cross-ref: "see [spec_audit_2026_05_11.md] for engine-fit feasibility"
- `state/phi_ce_orthogonality_decisive_2026_05_11/verdict.md`
  - §7 Next Cycle Action Items 의 (1) "anima Φ★ engine confirmation" 옆에 audit pointer
- `hypotheses/H_080_topo_24variants.md`
  - §Conflict Resolution Pending → 본 audit 끝 줄에 한 줄 추가: "spec audit completed
    2026-05-11: see state/phi_ce_orthogonality_decisive_2026_05_11/spec_audit_2026_05_11.md
    — split-engine path recommended, noise floor calibration prereq."

## 8. Honest Limits (≥ 5)

- **L1**: 본 audit 은 *spec-feasibility only* — 실제 anima_phi_star.hexa GPU 실행
  결과 (Mistral-7B 의 phi_star_min 값 / variance) 미측정. §4 calibration 의 σ_Φ
  추정은 *hypothetical* — 실측 시 다를 수 있음.
- **L2**: anima_phi_star 의 hidden-dim H_truncated=128 을 "N (cell count)" 으로
  reinterpret 하는 path 는 mathematically 가능하나, Hc_040 N^1.071 / Hc_005 cell-count-
  decisive 의 *원 axis* (faction count, cell module count) 와 다른 axis 일 수 있음.
  reinterpretation 의 validity 는 별도 audit 필요.
- **L3**: CLM training cost estimate 는 RunPod A100 spot price 기준 — 실제는 ±50 %
  변동, Chinchilla token budget 도 dataset 가용성에 따라 변함.
- **L4**: Hc_040 의 CE ∝ P^-0.85 slope 는 Kaplan/Chinchilla scaling slope (~-0.05~-0.1
  in log-loss vs log-params space) 와 부호는 같으나 크기 ~10× 큼 — 실측에서 slope
  fit 시 Hc_040 자체가 first-order falsified 가능. spec 의 Model A 의 noise σ 가
  signal scale 의 5 % 라는 가정도 *signal* 이 무엇인지 (loss in nat? in log-loss?)
  미명확.
- **L5**: split-engine join 의 *cell key alignment* — Φ-track 의 (N=64, P=10M) 과
  CE-track 의 (N=64, P=10M) 이 *서로 다른 substrate* 위에서 측정될 때 "같은 cell"
  의 의미가 모호. cell-engine 의 hidden-dim 과 CLM 의 hidden-dim 이 *공유* 되어야
  하는지 (parameter coupling) vs *완전 독립* (orthogonality test 의 정신) 여부 spec 미정.
- **L6**: anima_clm_invoke.hexa 의 training-side script land 여부 미확인 — 본 audit
  은 `LOCAL_WEIGHT_HINT` 의 530M 만 존재 confirm 했고, *training pipeline* (loop /
  optimizer / dataset / checkpoint save) 은 별도 grep 필요. 본 audit 의 §5.2 CLM
  cost estimate 는 *fresh-train assumption*.
- **L7**: 본 audit 은 "Communicative Efficiency vs Cross-Entropy" 충돌을 §2 에서
  cross-entropy 로 reconcile 했으나, Hc_024 의 NOBEL-1 source 문서 (`docs/hypotheses/cx/
  NOBEL-HYPOTHESES.md`) 본문 미열람 — 본 audit 의 reconciliation 은 frontmatter
  notes 기반 inference. source doc verification 시 변경 가능.

## 9. Cross-Links

- **spec**: `state/phi_ce_orthogonality_decisive_2026_05_11/spec.md` (audited target)
- **verdict**: `state/phi_ce_orthogonality_decisive_2026_05_11/verdict.md` (synthetic
  fingerprint analytics, cross-ref §1.1 / §7)
- **harness**: `state/phi_ce_orthogonality_decisive_2026_05_11/harness.py` (σ-default
  re-tune target — §4.2)
- **parent H**: `hypotheses/H_080_topo_24variants.md` §Conflict Resolution Pending
- **Hc_040** / **Hc_024**: CE definition reconciliation §2
- **sibling audit**: `state/nexus6_1013lens_activation_2026_05_11/prereq_audit_2026_05_11.md`
  (axis-conflation analogue, "same name / different axis")
- **anima_phi_star**: `tool/anima_phi_star.hexa` (audited engine)
- **anima_clm_invoke**: `tool/anima_clm_invoke.hexa` (CE-track wrapper — training-side
  unverified)
- **cycle 5 queue**: `NEXT.md` #1 (본 audit 의 prereq)

---

**lock policy reminder**: chflags +uchg/+schg/chattr +i 적용 *금지*. unlock 된 파일 *재잠금 금지*.
**commit policy**: 본 audit 은 *separate commit 금지* — 메인 process 가 일괄 commit.
