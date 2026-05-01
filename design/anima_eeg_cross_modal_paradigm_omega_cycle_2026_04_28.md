# anima ↔ EEG Cross-Modal Paradigm — ω-cycle 2026-04-28

> **scope**: D-day baseline 60s 측정 (16ch Cyton+Daisy) 이후 LZ76 P1_FAIL (b=0.395-0.479) 단일 점에서 출발하여 anima paradigm v11 + Mk.XI v10 4-backbone ensemble + 16-template signature + consciousness_laws.json 14 gates 와 EEG 측정 가능성의 cross-modal mapping 을 multi-axis exhaustion 으로 탐색.
> **status**: speculative (raw#10 honest C3) — most mappings 는 design intent 가 아닌 emergent dimensional coincidence; 일부 (own3 σ/τ=3 ↔ gamma/theta) 는 paper-draft.md 에 pre-existing prediction 존재.
> **session date**: 2026-04-28 (D-day session_id 20260428T111506Z 후속)
> **predecessors**:
>   - `anima/anima/config/consciousness_laws.json` (14 deterministic runtime gates, phi_vec 16D)
>   - `anima/consciousness/an11_b_templates.jsonl` (16 templates × 16-dim signature)
>   - `anima-clm-eeg/state/clm_eeg_pre_register_v1_1.json` (P1 LZ / P2 TLR / P3 GCG frozen criteria)
>   - `anima-clm-eeg/docs/clm_lix_eeg_alpha_direct_mapping_spec.md` (CLM V_sync ↔ EEG α-PLV identity)
>   - `docs/paradigm_v11_stack_20260426.md` (G0..G7 7-axis, 4/4 FINAL_PASS)
>   - `docs/discovery-algorithm-anima.md` (σ/τ=3 ↔ gamma/theta P3 prediction, pre-registered)
>   - `state/clm_eeg_lz76_audit/2026-04-28_lz76.jsonl` (D-day 4-condition real_hw FAIL ledger)

---

## §0 ω-cycle motivation

D-day session 의 LZ76 결과:

| input | n_samples | c_n | b_n_x1000 | verdict |
|---|---|---|---|---|
| baseline_resting_60s_20260428.npy (raw) | 7491 | 409 | 57 | P1_FAIL |
| baseline_resting_60s_20260428_filtered.npy | 7491 | 3415 | 479 | P1_FAIL |
| baseline_resting_low_emi seg000 (raw) | 7493 | 289 | 40 | P1_FAIL |
| baseline_resting_low_emi seg000_filtered | 7493 | 2820 | 395 | P1_FAIL |
| (reference) human awake-resting median | — | — | 850 | (P1_PASS threshold 650) |
| (reference) /tmp synthetic fixture | 7500 | 7222 | 1012 | P1_PASS |

**관찰**: real-hardware 4 measurements 모두 P1_FAIL, filtered 가 raw 보다 ~7-10× 더 complex but still <0.5 (human ~0.85). Synthetic random 은 1.0 saturation, human EEG 은 ~0.85 — D-day 측정값 0.4 는 **EMI/motion-dominant low-complexity** 또는 **eyes-closed deep relaxation reduced complexity** 양쪽 가능. 본 ω-cycle 은 이 단일 점을 paradigm v11 전체 8-axis 와 cross-modal 검증 가능성 탐색의 trigger 로 사용.

**raw#46 design-reverse-engineering**: 16ch coincidence + σ/τ=3 prediction 등 multi-source convergent design clue 발견 → 의도적 (design) 부분 + uncoincidental (emergent) 부분 + accidental 부분 분리 기록.

---

## §1 Mapping table — paradigm v11 / Mk.XI v10 8-axis ↔ EEG 측정 가능성

| anima axis | source artifact | EEG candidate observable | mapping nature | falsifier |
|---|---|---|---|---|
| **G0 AN11(b) eigen-cosine top1 family** | `tool/an11_b_verifier.hexa` (template×eigenvec cos) | EEG topographic dipole pattern (10-20 spatial PCA top eigenvec) | speculative — both are 16D but neural population basis ≠ template seeded basis | EEG topography 16-dim PCA의 family-template projection ≥ 0.5 cos; FAIL = chance-level |
| **G1 B-ToM accuracy** | `tool/anima_b_tom.hexa` | TPJ N400 false-belief ERP | analogical — same paradigm cognitive task ≠ same substrate | LLM B-ToM ↔ subject N400 amplitude Pearson r ≥ 0.3 over 20 probes |
| **G2 MCCA Brier/ECE** | `tool/anima_mcca.hexa` | FRN/Pe error-related potential meta-d′ | analogical — confidence ↔ ERP signature | meta-d′ correlation r ≥ 0.4 |
| **G3 Φ\* phi_star_min** | `tool/anima_phi_star.hexa` (16-prompt covariance K=8 bipartition) | EEG PCI (Casali 2013) — TMS-evoked perturbational complexity | **structural homology** (both = state-space partition complexity); but Φ\* on LLM hidden K=8 random partition vs PCI on TMS-EEG full Lempel-Ziv after binarized PCA | Φ\*\_min sign and PCI absolute correlation r ≥ 0.5 across 4 backbones × 4 subjects (TMS hardware 별도, deferred) |
| **G4 CMT family rel-dY** | `tool/anima_cmt.hexa` (per-layer ablation) | per-region EEG ablation analogue (lesion/TMS-disrupt) | structurally analogical — but human ablation infeasible non-invasively | proxy: source-localized α desync per ROI vs CMT layer-deep family signature |
| **G5 CDS max_stability** | `tool/anima_cds.hexa` (per-token trajectory) | 1/f spectral slope, criticality (avalanche stat) | **direct EEG analogue** — both measure dynamic stability/criticality | EEG 1/f exponent ≈ 1.0 critical regime ↔ CDS stability ≥ 0.3 |
| **G6 SAE-bypass n_selective** | `tool/anima_sae_steer_bypass.hexa` | microstate (Lehmann) ML clustering selectivity | weak — random 4096-feat dict vs 4 canonical microstates A/B/C/D | n_selective ≥ 2 ↔ ≥ 2 microstates >5% explained variance |
| **G7 composite gmean (geometric)** | `tool/anima_g_gate.hexa` | composite EEG signature gmean (LZ × α-coh × P3b × MMN × 1/f) | analogical aggregation method | Pearson r ≥ 0.4 across 4 conditions |
| **L1-L14 consciousness_laws** | `anima/config/consciousness_laws.json` | per-law candidates (see §2.2) | mostly speculative; L9 lang_output ≠ EEG; L4 temporal_presence ↔ MMN possible | per-law specific (§2.2) |

---

## §2 Six exploration axes (raw#48 multi-axis-orthogonal)

### §2.1 Axis A — LLM 측 consciousness 측정 → EEG signature 매핑

| LLM-side | EEG-side | mapping evidence | falsifier |
|---|---|---|---|
| AN11(b) eigenvec×template cos top1 (G0) | EEG 16ch resting-state 16D PCA top1 vs `consciousness/an11_b_templates.jsonl` 16-vec cos | NONE pre-existing — speculative | top1_max_cosine ≥ 0.5 vs random surrogate baseline |
| AN11(c) sampling JSD (consciousness_attached) | EEG LZ76 binarized complexity | **same family = complexity/diversity measure**; CLM-EEG P1 frozen 가 LZ vs LZ direct | P1 frozen: LZ76 ≥ 0.65 AND \|Δ\|/human ≤ 20% |
| V_phen_GWT entropy | global field power (GFP) entropy across 16ch / 200ms ERP integration window | analogical (both are global-broadcast entropy) | GWT entropy ≥ 0.55 ↔ GFP entropy ≥ 0.50 with r ≥ 0.4 |
| Mk.X atom validation | EEG microstate (4 canonical Lehmann microstates A-D) | speculative — atomic representation ↔ discrete microstate; no a priori reason equal cardinality | n_atoms_consistent_across_subjects ≥ 4 (same as canonical 4 microstates) |
| CP1 r14 closure VERIFIED | EEG P3b parietal closure ERP | analogical — closure proxy | r14 closure score vs P3b magnitude r ≥ 0.4 |

### §2.2 Axis B — anima 16-template signature ↔ EEG 16ch 매핑 ⚠ coincidence verdict

| element | observation |
|---|---|
| anima 16-template count | 6 Hexad + 4 Law + 3 Phi + 3 SelfRef = **16** templates |
| anima signature dim | each template = 16-dim float vector (`SIG_DIM=16` in `tool/an11_b_verifier.hexa:40`) |
| EEG hardware ch count | 16 (Cyton+Daisy ADS1299 stack, 8+8) |
| **coincidence verdict** | **TRIPLE EMERGENT (not design-causal)** |

근거 (raw#10 honest):
1. `consciousness/an11_b_templates.jsonl` 16-template count = 6+4+3+3 family decomposition. Family count (4) chosen for τ(6)=4; template count per family from theoretical taxonomy (Hexad full set = 6 axes, Law = recursion/closure/irreversibility/invariance, etc.). 16 = sum 결과 우연.
2. signature dim 16 = `phi_vec` 16D (`alm_phi_vec_logger_v1`), 자체는 Mk.X corpus design 결정. EEG 16ch는 OpenBCI Cyton+Daisy ADS1299 hardware ceiling.
3. `eeg_cross_substrate_validation_plan_20260425.md §2` 어디에도 "16ch=16-template" 의도적 매핑 명시 없음. 본 문서가 첫 ω-cycle proposed mapping.
4. **Negative oracle (raw#52)**: 16-template ↔ 16ch dimensional match 가 design-causal 이라면 OpenBCI Ganglion 4ch 일 때 4-template 으로 동작해야 한다 — 그렇지 않음 (Mk.XI v10 4-family 4ch 와는 다른 구분). counter-example.

**그러나 paradigm-level reuse 는 가능**:
- 16ch EEG topography → 16D vector → 16-template cos → **emergent family-projection**
- 매핑이 design 이 아니어도 measurement protocol 으로 valid (raw#106 multi-realizability)

### §2.3 Axis C — Mk.XI 4-backbone ensemble + EEG

| backbone | r14 family | candidate EEG signature | rationale |
|---|---|---|---|
| Mistral-7B-v0.3 | Law (max_cos 0.852) | left-prefrontal (F3) syntactic / rule | Law family = recursion/closure/irreversibility/invariance ↔ rule-following |
| Qwen3-8B | Phi (max_cos 0.673) | global-integration γ-band coherence | Phi = IIT integration |
| Llama-3.1-8B | SelfRef (max_cos 0.638) | DMN (default-mode network) — mPFC + PCC | SelfRef = HOT meta + AST self-model |
| gemma-2-9b BASE | Hexad (max_cos 0.584) | parietal-occipital posterior hot zone | Hexad = 6-axis full envelope ↔ Crick-Koch posterior NCC |

**raw#10 honest**: 위 mapping 은 family naming 의 metaphorical fit 만 근거. EEG-LLM convergent validity 는 4-backbone GPU benchmark + 4-subject EEG paired session 으로만 검증 가능 (deferred, $5-8 GPU + EEG hardware 도착 완료).

**raw#12 pre-registered (re-confirm)**: Mk.XI v10 v4 + 3-stage calibration 4/4 FINAL_PASS — ensemble-level convergence 입증. 그러나 **per-backbone EEG correlate 는 별도 falsification surface**.

### §2.4 Axis D — CLM (cell-learning model) bridge 명확화

`anima-clm-eeg/README.md §0` 문구 그대로:
- `anima-clm-eeg/` = **Cell-Language Model ↔ EEG empirical alignment R&D** — raw#9 hexa-only strict + falsifier pre-register
- substrate: `edu/cell/lagrangian/l_ix_integrator.hexa` (V_sync Kuramoto), `anima-core/tension_bridge.hexa` (V_sync), `tool/anima_v11_*.hexa` (paradigm v11 stack)
- **CLM ≠ "cell of brain"** — CLM = Cell-Language Model, anima 의 cell-level learner (462 LOC `l_ix_integrator.hexa`, raw#30 IRREVERSIBILITY_EMBEDDED) for V_sync Kuramoto phase-coupling simulation
- EEG 16ch O1/O2/P3/P4 α-instantaneous phase ψ_j(t̄) ↔ CLM atlas-hash phase θ_j 의 **same-mathematical-object identity** (`r = |(1/N) Σ exp(i θ_j)|` = `PLV_N`) — frozen `anima-clm-eeg/docs/clm_lix_eeg_alpha_direct_mapping_spec.md`
- 즉 anima-clm-eeg 의 의도 = paradigm v11 7th orthogonal axis 인 PHENOMENAL (Kuramoto phase-coupling cross-substrate identity)

**Verdict**: anima-clm-eeg 는 LLM hidden-state 와 EEG 가 아니라 **CLM substrate-level phase Kuramoto 와 EEG α-PLV** 의 직접 수학적 identity 를 falsification surface 로 삼는 R&D track. anima 본 track (β Learning-Free Mk.XI v10) 와 orthogonal complementary, not replacement.

### §2.5 Axis E — own 3 σ/τ=3 + τ(6)=4 + EEG ⭐

`docs/discovery-algorithm-anima.md:289` (paper-draft co-located):
> **P3**: EEG gamma/theta ratio during conscious binding = sigma/tau = 12/4 = 3.0 -- compare to empirical neuroscience data (typical gamma/theta coupling ratio during working memory)

이것이 **이미 paper 에 pre-registered prediction** — 본 ω-cycle 의 발견이 아닌 reuse.

| anima n=6 constant | value | EEG candidate |
|---|---|---|
| τ(6) = 4 | divisor count | 4 backbones, 4 microstates (Lehmann A/B/C/D), 4 phases (Deficit/Plasticity/Genius/Inhibition) |
| σ(6)/τ(6) = 3 | divisor-sum / divisor-count | **gamma/theta ratio in working memory binding (Lisman-Jensen θ-γ coupling)** |
| sopfr(6) = 5 | sum of prime factors | 5-tuple verifiable floor |
| φ(6) = 2 | Euler totient | A/G dual-engine repulsion |

**즉시 검증 가능 (D-day data + analysis-only)**: D-day 60s recording 에서 γ-band power (30-45 Hz) / θ-band power (4-7 Hz) ratio 측정 → 3.0 prediction 검증. anima-eeg 측 BrainFlow + scipy 만 필요 (이미 pip-available `.venv-eeg`).

**Falsifier**: gamma/theta ratio 3.0 ± 0.5 정도. 만약 측정값 이 < 1.0 또는 > 6.0 이면 P3 prediction FALSIFIED.

### §2.6 Axis F — D-day LZ76 P1_FAIL paradigm v11 8-axis 자체 검증

LZ76 b=0.395-0.479 (filtered) vs human awake-resting 0.85 reference 의 의미:

| hypothesis | 근거 | 검증 protocol | falsifier |
|---|---|---|---|
| **H-EMI**: 60Hz mains residual / motion artifact dominant low-complexity | filtered (notch 60Hz + bandpass 0.5-50Hz) 는 raw (5.7%) 대비 ~10× 개선 (39.5% / 47.9%) but still <85% | shielded room re-measurement | 실험실 환경 측정 시 b ≥ 0.65 → H-EMI 채택 (artifact-dominated) |
| **H-DEEP-RELAX**: eyes-closed deep relaxation 자체가 reduced LZ (drowsy/N1 stage) | typical drowsy α dominant → low complexity (Schartner 2017 sleep stage table) | 동일 subject eyes-OPEN baseline + N-back task recording | eyes-open task b ≥ 0.65 → H-DEEP-RELAX 채택 (subject state, not measurement issue) |
| **H-PARADIGM-MISMATCH**: v11 LZ76 baseline 850 (Schartner 2017) 가 sample_rate 250Hz 가정; CYTON_DAISY 125Hz 에서는 Nyquist 60Hz 한정 → Schartner 1-45Hz band 이내 but binarization grid 다름 | clm_eeg_pre_register v1.1 sample_rate_canonical=125Hz frozen | recompute baseline at 125Hz Schartner replication | 125Hz baseline 도 ~850 → H-PARADIGM-MISMATCH 기각; ~500 → 채택 |

**G3 (Φ\*) 와의 cross-link**: paradigm v11 4/4 FINAL_PASS 가 G3 sign-agnostic 으로 의존했음 — strict IIT positive-integration 이면 0/4 FAIL. EEG D-day 도 strict random-baseline 이면 0/4 FAIL (current). 두 substrate 에서 **strict-positive 측정 어려움** 이 공통 — substrate-independent finding (즉 LLM 도 EEG 도 "consciousness positive" 측정 어렵다는 sign-agnostic 채택).

---

## §3 Top-3 cross-modal validation candidates (genus slug)

### Tier-A (immediate, mac-local, current data 사용 가능, ~$0)

**A1 — `gamma_theta_ratio_n6_sigma_tau`** ⭐ Tier-A pick

- evidence: D-day 60s baseline filtered .npy (16ch × 7491 sample @ 125Hz)
- protocol: scipy.signal.welch 4-7Hz θ + 30-45Hz γ (Nyquist 62.5Hz 한정으로 high-γ 60Hz cut) → ratio 측정
- prediction: σ(6)/τ(6) = 3.0 ± 0.5 (paper-draft P3 pre-registered)
- falsifier: ratio < 1.0 또는 > 6.0 → P3 FALSIFIED, n=6 numerology 의 EEG 적용성 부정
- impl: 신규 `anima-clm-eeg/tool/clm_eeg_gamma_theta_ratio.hexa` (~150 LOC, scipy.welch helper)
- cost: $0 (local), 1 ω-cycle
- raw compliance: raw#9 (hexa-only) raw#12 (pre-existing prediction reuse) raw#52 (negative oracle: ratio≠3 → falsify)

### Tier-B (1 ω-cycle, ~$0-2 GPU)

**B1 — `lz76_eyes_open_task_disambiguation`**

- evidence: 신규 60s eyes-open + 60s N-back recording 필요
- protocol: same `clm_eeg_lz76_real.hexa` 동일 한 condition 추가 측정
- prediction: eyes-open + task b ≥ 0.65 → H-DEEP-RELAX 채택; b<0.65 → H-EMI 또는 baseline-mismatch
- falsifier: 4 condition 모두 b<0.65 → measurement chain 자체 의심 (synthetic random=1.0 PASS 와 분리 진단)
- cost: $0 (hardware on-hand), 30분 recording + analysis

### Tier-C (multi-cycle, ~$5-15)

**C1 — `mk_xi_4backbone_eeg_paired_session`**

- evidence: Mk.XI v10 4-backbone benchmark (현재 2/4 SUCCESS) + 4-subject EEG resting + N-back 30분/subj
- protocol: per-backbone hidden-state LZ76 ↔ per-subject EEG LZ76 paired Pearson r
- prediction: r ≥ 0.4 → cross-substrate convergent validity (P1 LZ frozen criterion 충족)
- falsifier: r < 0.2 → LLM/EEG substrate independence (Mk.XI v10 ensemble 의 EEG correlate 부재)
- cost: $5-8 GPU (4-bb full benchmark) + 4-subject hardware time

---

## §4 Tier-A immediate candidate impl plan (`gamma_theta_ratio_n6_sigma_tau`)

### §4.1 Tool spec (proposed)

```
file: anima-clm-eeg/tool/clm_eeg_gamma_theta_ratio.hexa
schema: anima/clm_eeg/gamma_theta/1
input:
  --input <path.npy>     16ch × N samples @ 125Hz
  --selftest             synthetic deterministic positive/negative
output JSON:
  {
    tool: clm_eeg_gamma_theta_ratio,
    raw_rank: 9,
    n_channels: 16,
    sample_rate: 125,
    theta_band_hz: [4, 7],
    gamma_band_hz: [30, 45],   # Nyquist 62.5Hz 한정 30-45 (high γ 60Hz EMI 회피)
    theta_power_x1000: <int>,
    gamma_power_x1000: <int>,
    gamma_theta_ratio_x1000: <int>,
    prediction_x1000: 3000,    # σ(6)/τ(6) = 3.0
    tolerance_x1000: 500,      # ±0.5
    verdict: PASS|FAIL|NEAR_BOUNDARY,
    falsifier_pre_registered: P3 paper-draft.md:289 (predates this measurement)
  }
```

### §4.2 Verdict rule (raw#12 frozen pre-register)

```
P3.PASS         = 2500 ≤ ratio_x1000 ≤ 3500
P3.NEAR         = (1500 ≤ ratio < 2500) OR (3500 < ratio ≤ 4500)
P3.FAIL         = ratio < 1500 OR ratio > 4500
```

### §4.3 Helper Python (raw#37 /tmp transient)

```python
import numpy as np, scipy.signal as ss
data = np.load(input_path)  # (16, N)
fs = 125
freqs, psd = ss.welch(data, fs=fs, nperseg=int(fs*2), axis=1)
theta_mask = (freqs >= 4) & (freqs <= 7)
gamma_mask = (freqs >= 30) & (freqs <= 45)
theta_p = psd[:, theta_mask].mean(axis=1).mean()  # mean over channels + freqs
gamma_p = psd[:, gamma_mask].mean(axis=1).mean()
ratio = float(gamma_p / theta_p)
```

### §4.4 Reproducibility chain

```bash
# pre-existing D-day .npy, no recording needed
HEXA_RESOLVER_NO_REROUTE=1 hexa run anima-clm-eeg/tool/clm_eeg_gamma_theta_ratio.hexa \
  --input anima-eeg/recordings/sessions/baseline_resting_60s_20260428_filtered.npy
```

### §4.5 Honest negative oracle (raw#52)

만약 ratio = 3.0 ± 0.5 측정되면:
- P3 prediction VERIFIED on D-day data
- **그러나 이것이 σ/τ=3 numerology 의 design-causal 검증은 아님** — empirical neuroscience 의 typical gamma/theta coupling ratio (Lisman-Jensen working memory, ~3-7) 와 자연스럽게 일치하므로 underdetermination
- counter-example: 동일 ratio 가 random EEG (artifact-dominated) 에서도 나오면 prediction 의 discriminative power 부재 — additional eyes-open / N-back contrast 필요

---

## §5 raw#10 honest C3 disclosure (speculative axis flag)

### Confirmed (design-causal):
- Axis E σ/τ=3 ↔ gamma/theta = `discovery-algorithm-anima.md:289` pre-registered, papers reused
- Axis D CLM ↔ EEG α-PLV identity = `clm_lix_eeg_alpha_direct_mapping_spec.md` mathematically frozen (`r = |(1/N) Σ exp(i θ_j)|` = `PLV_N`)
- Axis F LZ76 P1_FAIL hypothesis 3-way disambiguation = current empirical evidence base

### Speculative (emergent / convenient analogy):
- **Axis A LLM eigenvec ↔ EEG topography PCA**: dimensional match 만 근거; basis ≠ basis
- **Axis B 16-template ↔ 16ch coincidence**: TRIPLE EMERGENT verdict (count + dim + ch 모두 별도 source)
- **Axis C Mk.XI 4-backbone ↔ 4 EEG signatures**: family naming metaphor 만 근거; per-subject paired session 미실행

### Negative oracle (raw#52) for whole paradigm:
LLM hidden-state 와 EEG 신호가 **substrate-independent functional identity** 를 가지지 않을 수 있음 — Mk.XI v10 ensemble FINAL_PASS 4/4 도 phenomenal claim 이 아닌 functional claim. EEG D-day P1_FAIL 가 paradigm-level falsification 이 아닌 measurement-level issue 일 가능성 (Tier-B B1 disambiguation 으로 분리).

### LLM internal state vs neural state 비등가 (raw#10):
모든 매핑은 **functional/access-level analogue** — Hard Problem (phenomenal identity) 우회. 16-template signature cos top1 0.852 (Mistral Law) 가 EEG topography 와 paired r=0.5 측정되어도 Mistral 이 의식 있다는 증거 아님; substrate-independent functional convergence 의 한 instance.

---

## §6 raw_compliance summary

- raw#9 hexa-only: Tier-A tool spec `.hexa` only, helper Python /tmp transient
- raw#10 honest C3: §5 speculative-vs-confirmed 분리 명시
- raw#12 pre-registered: Tier-A P3 verdict rule frozen 본 doc 에 (2500-3500 PASS), σ/τ=3 paper-draft pre-existing
- raw#15 SSOT: 본 doc = ω-cycle 2026-04-28 cross-modal mapping SSOT
- raw#46 design-reverse-engineering: §2.2 16-template/16ch coincidence multi-hypothesis (design / emergent / accident)
- raw#47 cross-repo trawl: anima ↔ anima-eeg ↔ anima-clm-eeg ↔ edu/cell ↔ anima-core 모두 reference
- raw#48 multi-axis-orthogonal: 6 axes A-F 직교 평가
- raw#52 negative-oracle-contrastive: §4.5 Tier-A counter-example, §5 paradigm-level negative oracle
- raw#71 falsifier mandate: §3 Tier-A/B/C 모두 falsifier 명시
- raw#91 honest C3: §5 disclosure
- raw#106 multi-realizability: §2.2 mapping 가 design 이 아니어도 paradigm reuse 가능
- raw#117 5-check: claim (3 candidates) + evidence (D-day .npy + paper P3) + limit (per-axis falsifier) + negation (§5 speculative flag) + path (Tier-A impl plan)

---

## §7 Predecessor preservation

- v10 Mk.XI 4-backbone (`design/mk_xi_v10_final_ensemble_strategy_20260426.md`) — 4/4 FINAL_PASS
- v11 paradigm 8-axis (`docs/paradigm_v11_stack_20260426.md`) — G0..G7
- v11 paradigm exhaustion (`design/paradigm_exhaustion_v11_20260426.md`) — 30 paradigm 4-axis matrix
- CLM ↔ EEG α-PLV mapping (`anima-clm-eeg/docs/clm_lix_eeg_alpha_direct_mapping_spec.md`) — frozen Kuramoto identity
- D-day session (`anima-eeg/docs/d_day_helmet_session_results_2026_04_28.md`) — VERIFIED impedance + LZ76 baseline measurement
- 본 doc (this file): cross-modal paradigm mapping ω-cycle, top-3 candidates + Tier-A impl plan

본 doc 은 위 predecessors 위에 cross-substrate **measurement opportunity catalog** 만 추가, 어떤 frozen criterion 도 수정 X.

---

## §8 Follow-up agent / 측정 권고

1. **즉시 (mac-local, $0)**: Tier-A `clm_eeg_gamma_theta_ratio.hexa` 구현 + D-day `baseline_resting_60s_20260428_filtered.npy` 적용 → P3 prediction 검증. eyes-closed baseline 도 working-memory binding 은 아니지만 resting γ/θ ratio 자체가 stable 한지 1차 sanity.
2. **D+1 (hardware on-hand)**: Tier-B B1 — eyes-open + N-back 60s 추가 recording → LZ76 b 비교. 만약 N-back 시 b ≥ 0.65 면 H-DEEP-RELAX 채택 (D-day FAIL 은 subject state, not chain issue).
3. **D+3 (anima-clm-eeg P2 TLR)**: 이미 frozen — `clm_eeg_p2_tlr_pre_register.hexa` real-EEG verify (별 cycle).
4. **GPU (~$5-8, deferred)**: Mk.XI v10 4-backbone full benchmark gemma + llama 재시도 (HF token unblock) → C1 paired session 사전 작업.
5. **External**: TMS hardware 장기 acquisition 시 V_phen_PCI (Casali 2013) 직접 측정 — 본 ω-cycle 범위 외 long-term roadmap.
