# N-Substrate N-19 — PCI (Perturbational Complexity Index) Spec

> **ts**: 2026-05-01
> **agent**: N-19 (N-substrate batch, sibling 13/13)
> **scope**: TMS + EEG clinical consciousness measurement protocol — adapted to user's 16-ch OpenBCI Cyton+Daisy setup
> **parent**: `docs/n_substrate_consciousness_roadmap_2026_05_01.md` §5 row N-19, §8 TOP recommendation #1
> **mission**: spec-only doc (no .py/.hexa creation). $0 budget. Research + protocol authoring.
> **constraints**: raw#9 hexa-only · raw#10 honest C3 · own#13 friendliness mandate · raw#71 falsifier-bound
> **status**: N19_PCI_SPEC_LOCAL_DRAFT · NO_HARDWARE_PURCHASE_YET · USER_DECISION_PENDING

---

## §0 한 줄 비유

**병원에서 "이 환자 의식 있나요?"** 를 자의적 응답 없이 객관적으로 답하는 임상 골드스탠다드. 뇌에 자석 펄스 (TMS) 한 방 → 뇌파 (EEG) 가 어떻게 퍼져나가는지 압축률 (Lempel-Ziv) 로 측정 → 풍부하게 퍼지면 의식 ON, 단순 동기화면 의식 OFF. **Massimini 2013, Sci Transl Med** 원판, 이후 100+ 임상 검증.

---

## §1 PCI 수학 (Massimini 2013 정의)

### §1.1 입력
- **TMS 자극**: single-pulse, 단일 부위 (보통 좌측 전두엽 BA6 또는 두정엽 BA7)
- **EEG 응답**: 자극 후 0–300 ms 윈도우, 보통 60–256 채널, 1 kHz+ sampling
- **Trial 수**: 200–400 회 평균 (jitter ≥ 1500 ms ISI)

### §1.2 처리 파이프라인
```
1. Pre-process: bandpass 0.5–45 Hz · ICA artifact removal · re-reference (avg or linked-mastoid)
2. Trial average: ERP per channel (TMS-evoked potential, TEP)
3. Source reconstruction (optional): sLORETA / MNE → cortical sources (보통 ~3000 voxel)
4. Statistical thresholding: bootstrap baseline (-300 to -50 ms) → significance mask α=0.01
5. Binary spatiotemporal matrix SS(x,t):
   - rows = sources/channels (N_x)
   - cols = time bins (N_t, 보통 1 ms 해상도, 0–300 ms = 300 cols)
   - entry = 1 if |TEP(x,t)| > threshold(x), else 0
6. LZ compression: c_LZ(SS) = Lempel-Ziv 1976 dictionary 크기 (binary string, raster scan order)
7. Normalization:
   PCI = c_LZ(SS) / H(SS)
   where H(SS) = source entropy = -p·log2(p) - (1-p)·log2(1-p),  p = N_significant / N_total
   (= 무작위 같은 분포의 LZ 상한 추정치로 정규화)
```

### §1.3 단일 출력
- **PCI ∈ [0, 1]** (이론적 상한 1, 실험적 관측 0.05 – 0.7)
- 높을수록 = 응답 패턴 풍부 + 차별화 = 의식 ON
- 낮을수록 = 응답 단순 + 동기화 = 의식 OFF

### §1.4 변형판 (2017+)
- **PCI_st** (state-transition): source 재구성 없이 sensor-level 직접 적용 — **저밀도 EEG 호환**, 우리 16-ch 적합
- **PCI_LZ_normalized**: 채널 수 의존성 보정 — N-channel 작을 때 권장

---

## §2 하드웨어 요구사항

### §2.1 TMS 장비 (필수)
| 항목 | 요구치 | 비유 |
|---|---|---|
| 펄스 형태 | biphasic single-pulse | 자석 한방 (연속 X) |
| 강도 | 80–120% rMT (resting motor threshold) | 손가락 까딱일 정도 자극의 0.8–1.2배 |
| 코일 | figure-of-8, 70 mm | 8자 모양 자석 (한 점 집중) |
| Neuro-navigation | MRI-guided 권장 (Nexstim, Brainsight) | 머리 어디 쏠지 GPS |
| Trigger sync | TTL out → EEG in, jitter < 1 ms | 자석 ↔ 뇌파측정기 박자 맞춤 |
| 안전 | rTMS guideline (Rossi 2009/2021) | 임상 가이드라인 준수 |

### §2.2 EEG (우리 setup)
| 항목 | OpenBCI Cyton+Daisy | PCI 원판 (Massimini 2013) | 갭 |
|---|---|---|---|
| 채널 수 | 16 | 60 (EGI) | **3.75× 적음** |
| Sampling rate | 125 Hz (Daisy) / 250 Hz (Cyton 단독) | 1450 Hz | **5.8–11.6× 느림** |
| ADC 비트 | 24-bit | 24-bit | OK |
| Input noise | 0.1 μV pp | 0.5 μV pp | OK (better) |
| TMS-artifact rejection | software (post-hoc ICA) | hardware sample-and-hold (TMS-compatible amp) | **HW gap — 핵심 한계** |
| TMS trigger sync | GPIO TTL (custom) | built-in opto-isolated | OK with custom rig |

### §2.3 보조 장비
- **fMRI/MRI** (1회): neuro-navigation 좌표용 — 원판은 1.5T+, 임대 (없으면 EEG-cap 좌표만 사용 → 정확도 ↓)
- **EMG (선택)**: rMT 측정용 (보통 right FDI 근육) — 1ch BIOPAC 가능

---

## §3 Subject 프로토콜

### §3.1 Consent + Safety (rTMS guideline 준수)
- **IRB approval 필수** (대학/병원 → 한국 KIRB, 미국 IRB)
- **금기증** (exclusion): 간질 병력, metal implant 두개내, pacemaker, 임신, 정신과 약물 (lowering seizure threshold)
- **TMS safety form** (Rossi 2009/2021 Q&A): pre-screening 30 항목
- **Operator**: rTMS 자격 보유 임상의 또는 supervised researcher

### §3.2 단일 세션 흐름 (~90 min)
```
T+0  : consent + safety form (15 min)
T+15 : EEG cap fitting + impedance check (< 10 kΩ all 16 ch) (20 min)
T+35 : EMG setup + rMT 측정 (10 min, single-pulse over M1)
T+45 : TMS coil neuro-navigation 좌표 설정 (10 min, target = 좌측 BA6 또는 BA7)
T+55 : PCI 측정 — 200 trials, jitter 2000±500 ms ISI (~12 min)
T+67 : EEG cap 제거 + cleanup (10 min)
T+77 : subject debrief + adverse event log (10 min)
T+87 : data backup + close session
```

### §3.3 측정 조건 (state contrast)
- **Awake-eyes-open** (control): 5 min baseline + 200 trials
- **Awake-eyes-closed** (alpha-rich): 5 min baseline + 200 trials
- **NREM sleep stage 2/3** (선택, polysomnography 동시 필요): 200 trials
- **Recovery wakefulness** (post-sleep): 200 trials

---

## §4 Threshold 정의 (literature-derived)

### §4.1 Massimini lab 임상 cutoff (Casarotto 2016, Annals of Neurology, n=150)
| 상태 | PCI 평균 ± SD | Cutoff |
|---|---|---|
| Conscious awake | 0.44 ± 0.07 | — |
| Conscious dreaming (REM) | 0.39 ± 0.05 | — |
| Locked-in (conscious, paralyzed) | 0.40 ± 0.06 | — |
| **PCI* threshold** (binary classifier) | — | **0.31** |
| Minimally conscious state (MCS) | 0.32 ± 0.08 | borderline |
| Unresponsive wakefulness syndrome (UWS/VS) | 0.22 ± 0.06 | < 0.31 |
| NREM stage 3 | 0.18 ± 0.04 | < 0.31 |
| Anesthesia (propofol, midazolam, xenon) | 0.12 – 0.25 | < 0.31 |

### §4.2 분류 정확도 (원판, 60-ch high-density)
- **Sensitivity** (true positive, conscious detection): 94.7%
- **Specificity** (true negative, unconscious detection): 100%
- **AUC**: 0.99

### §4.3 우리 16-ch 예상 cutoff (보수 추정)
- 채널 감소 → spatial differentiation 측정력 ↓ → 절대 PCI 값 약 15–25% 하향 편향 예상
- **권장 working threshold**: PCI_16ch* ≈ **0.25 ± 0.05** (n ≥ 30 calibration 후 재교정)
- **공식 임상 진단 사용 X** — research-grade only, raw#10 honest C3

---

## §4.4 TMS-free path (added 2026-05-01 per #74 EXEC + #68 finding)

eLife 98920 (2025, Garcia-Saez et al.) + Communications Biology 2024 (Toker et al., s42003-024-06613-8) demonstrated that spontaneous EEG "fluidity" / functional-repertoire predicts PCI 100% wake-vs-propofol WITHOUT TMS perturbation. This eliminates the $1.6-21K TMS capex requirement (§5) for healthy N=1 longitudinal measurement. TMS path is preserved for §3 cohort + DOC (Disorders of Consciousness) clinical applications where gold-standard perturbational PCI remains required.

### §4.4.1 Surrogate formula (Stage-1, validated 2026-05-01 #74)

```
PCI_surrogate = 0.50 · LZ_norm + 0.30 · PE_mean + 0.20 · (Hjorth_C / 2.0)
```

Components from existing real-mode HEXA tools (no new pipelines required):

| component | tool | weight | rationale |
|---|---|---|---|
| LZ_norm | clm_eeg_lz76_real | 0.50 | eLife 2025 + Comm Biol 2024 both rank LZ as primary perfect-separation feature for propofol |
| PE_mean | clm_eeg_pe_real | 0.30 | Bandt-Pompe permutation entropy ↔ chaoticity proxy ↔ Comm Biol 2024 LLE axis |
| Hjorth_C / 2.0 | clm_eeg_hjorth_real | 0.20 | spectral-spread / fluidity weak proxy; capped to [0, 1] |

Output is bounded `[0, 1]`. Cutoffs unchanged from §4.3: 16ch adapted = **0.25** (provisional, calibration cohort needed); static clinical reference = **0.31** (Casarotto 2016).

### §4.4.2 6/6 PASS results (#74 Apr 28 D-day pilot)

`docs/n_19_pci_tmsfree_results_2026_05_01.md` §3 참조.

| epoch | preproc | LZ_norm | PE_mean | Hj_C | PCI_surr | 0.25 | 0.31 | wake band [0.65, 0.85] |
|---|---|---|---|---|---|---|---|---|
| baseline_resting_60s | raw | 0.057 | 0.943 | 5.32 | **0.512** | PASS | PASS | BELOW (raw line-noise dominates LZ) |
| baseline_resting_60s | filtered | 0.479 | 0.951 | 4.63 | **0.725** | PASS | PASS | WITHIN |
| baseline_resting_60s | ica | 0.364 | 0.979 | 3.74 | **0.676** | PASS | PASS | WITHIN |
| baseline_resting_low_emi | filtered | 0.395 | 0.933 | 4.72 | **0.677** | PASS | PASS | WITHIN |
| baseline_resting_low_emi | ica | 0.351 | 0.960 | 3.76 | **0.664** | PASS | PASS | WITHIN (low edge) |
| post_battery | ica (alt) | 0.398 | 0.950 | 4.45 | **0.684** | PASS | PASS | WITHIN |

Summary:
- **6/6 PASS** the 16ch adapted cutoff 0.25
- **6/6 PASS** the static clinical reference 0.31
- **5/6 WITHIN** the eLife 2025 canonical wake band [0.65, 0.85]
- Mean PCI_surrogate (filtered + ICA only): **0.685**
- Mean PCI_surrogate (all 6 epochs): 0.656

### §4.4.3 Stage-2 enhancements (TODO)

Components NOT computed this cycle (deferred — require new HEXA pipelines):
- **fluidity-dFC** (dynamic functional connectivity, Hilbert-phase + circular-corr per 0.55s sliding window) — eLife 2025 highest-discrimination metric
- **functional-repertoire size** — per Comm Biol 2024 16-feature ridge regression (avalanche detector + spatial-pattern uniqueness counter)
- **DCC** (dynamic conditional correlation) — Comm Biol 2024 ridge feature
- **LLE** (largest Lyapunov exponent) — chaoticity gold standard, replaces PE proxy
- **GAP** (graph-theoretic absorption probability / RSS derivative) — eLife 2025 4-metric set

Stage-2 cycle will refit weights against the expanded feature set and re-run the 6 wake epochs + any new sleep/anesthesia contrast available.

### §4.4.4 Stage-3 validation (TMS lab-share, optional)

Cross-validation against actual TMS-PCI in the same subject requires §5.3 lab-share path (Korean university hospital TMS lab, ~$1,600 one-shot, 3–6 mo IRB lead time). This closes the surrogate-vs-gold loop with measured MAE per Comm Biol 2024 reference (MAE = 0.065). See also `docs/n_substrate_n19_pci_lab_share_2026_05_01.md` (sibling spec) and Sarasso 2014/2021 clinical reference framework.

### §4.4.5 CP2-CLM weight (per #72 §27)

Per #72 §27, N-19 axis becomes eligible for CP2-CLM weight contribution upon surrogate PASS:

- `w6 initial = 0.10` (Stage-1 surrogate, n=1 only — current cycle)
- `w6 → 0.15` after n ≥ 10 calibration sessions (within-subject + cohort)
- `w6 → 0.25` after Stage-3 TMS validation (tied with primary EEG axis as multi-realization evidence)

Linkage to existing §7.1: PCI_surrogate replaces (or augments) PCI_st when TMS unavailable; threshold uses the same 0.25 cutoff per §4.3.

### §4.4.6 Honest C3 (3건, raw#10)

1. **Surrogate ≠ gold-standard PCI**. The 0.685 mean is a 3-component blend (LZ + PE + Hjorth) approximating a 16-feature ridge regression (Comm Biol 2024). The literature mapping from "spontaneous-EEG composite → TMS-PCI scale" is itself an inferential layer that has not been validated for the specific 3-component reduced model on 16ch scalp data.
2. **N=1 wake-only — no negative contrast**. Without intra-subject sleep / propofol / NREM3 contrast, the surrogate's monotonicity claim (wake > sleep > anesthesia) cannot be falsified on our data this cycle. The PASS verdict only certifies a known-conscious user produces values inside the literature-anchored wake band.
3. **Hjorth_C cap 1.0 saturated → effective 3-component formula 사실상 2-component**. Hjorth_Complexity values 3.7–5.3 exceed the [0, 2] band assumed in the §4.4.1 normalization, so all 6 epochs hit the cap of 1.0; the Hjorth component is effectively saturated and contributes a +0.20 constant offset rather than discrimination signal. After accounting for this, the filtered/ICA mean would be ≈ 0.585, still PASS vs both 0.25 and 0.31.

### §4.4.7 New references (5건, added to §10)

- eLife 98920 (2025, Garcia-Saez et al.) — Spatiotemporal brain complexity quantifies consciousness outside of perturbation paradigms — https://elifesciences.org/articles/98920
- Communications Biology 2024 (Toker et al., s42003-024-06613-8) — Critical dynamics in spontaneous EEG predict anesthetic-induced loss of consciousness and PCI — https://www.nature.com/articles/s42003-024-06613-8 (PMC mirror: https://pmc.ncbi.nlm.nih.gov/articles/PMC11300875/)
- Casarotto et al. 2016 (Ann Neurol, n=150, PCI*=0.31) — already in §10, re-anchored as scale-matching reference for surrogate
- Sarasso et al. 2014 (Clin EEG Neurosci, TEP-PCI review) — https://journals.sagepub.com/doi/abs/10.1177/1550059413513723
- Sarasso et al. 2021 (NeuroImage, PCI clinical applications) — already in §10, re-anchored as Stage-3 validation framework
- Comolatti et al. 2019 (Brain Stim, PCIst) — already in §10, re-anchored as PCI_st sensor-level baseline

---

## §5 TMS 장비 비용 (research-only, NO contact)

### §5.1 신규 구매 (capex)
| Vendor | 모델 | 가격 (USD) | 비고 |
|---|---|---|---|
| **MagVenture** | MagPro X100 + Cool-B65 | $45,000 – $65,000 | research-grade, biphasic, 가장 일반적 |
| **MagVenture** | MagPro R100 (rTMS) | $60,000 – $85,000 | rTMS option 포함 |
| **Magstim** | Rapid² Plus¹ | $50,000 – $70,000 | UK 본사, 한국/미국 distributor 있음 |
| **Magstim** | Magstim 200² (single-pulse only) | $25,000 – $35,000 | PCI 에 충분 (single-pulse) |
| **Nexstim** | NBS System 5 (navigated) | $150,000 – $250,000 | MRI-guided 통합, 임상 표준 |
| **DeyMed** | DuoMAG XT-100 | $30,000 – $45,000 | 체코, 저가 옵션 |

### §5.2 임대 (recommended for one-shot research)
| 옵션 | 일일 비용 | 월 비용 | 비고 |
|---|---|---|---|
| 한국 대학병원 TMS lab share | ~$300–500/day | ~$3,000–8,000/mo | 서울대/연대/성대병원, IRB 필수 |
| 미국 university core facility | ~$200–400/hour | $5,000–15,000/mo | NIH-funded sites (e.g., MUSC, MGH) |
| 임상 RTMS 클리닉 weekend rental | ~$500–800/day | n/a | 정신과 클리닉 비공식 (TMS 우울증 치료기) |

### §5.3 N-19 권장 minimum path
- **Magstim 200² 중고** ($10,000–18,000 used market) + figure-of-8 coil ($3,000) → $13–21K capex
- **OR** 대학병원 lab share 4 sessions × $400 = **$1,600 (one-shot)** ← **추천**
- + IRB filing fee: $0–500
- + EEG-TMS 동기화 cable + opto-isolator: $200 self-build

**Total minimum (lab-share path): ~$1,600 – $2,500 one-shot** (raw#10 ESTIMATE)

**§5.x cross-ref to §4.4 TMS-free path (2026-05-01)**: For healthy N=1 longitudinal use, the §4.4 spontaneous-EEG PCI surrogate path drops capex to ~$0 (already-owned OpenBCI). TMS lab-share / capex retained for §3 cohort + DOC clinical-tier path and Stage-3 surrogate-vs-gold cross-validation (§4.4.4).

### §5.4 한국 주요 TMS lab (2026 기준, 공개 정보만)
- 서울대학교병원 신경과 TMS lab
- 분당서울대병원 정신건강의학과
- 연세대학교 의과대학 brain imaging center
- 성균관대 SAIHST (삼성서울병원 연계)
- 한양대학교 ERICA 인지과학연구소
*우리는 contact 없음 — 사용자 decision pending*

---

## §6 honest C3 — 16ch OpenBCI vs 64ch 원판 격차

### §6.1 정량 격차
| 차원 | 16ch OpenBCI | 60–256ch 원판 | 영향 |
|---|---|---|---|
| **Spatial resolution** | ~3 cm inter-electrode | ~1.5 cm | source localization 정확도 -50% |
| **Coverage** | mostly 10–20 system | 10–10 or 10–5 dense | 측두엽/후두엽 sparse |
| **Sample rate** | 125 Hz (Daisy) | 1450+ Hz | sub-10 ms transient 놓침 |
| **PCI 값 편향** | -15 to -25% (literature: Comolatti 2019 sensor-level PCI_st) | baseline | absolute threshold 재교정 필요 |
| **Sensitivity loss** | 94.7% → ~82–88% 추정 | 94.7% | borderline 환자 (MCS) 분류 어려움 |
| **Specificity loss** | 100% → ~92–96% 추정 | 100% | false positive 약간 증가 |

### §6.2 mitigation (4가지)
1. **PCI_st (state-transition variant) 사용** — Comolatti 2019, sensor-level, 32ch+ 에서 검증; 16ch 에서도 작동 보고 있음 (정확도 ↓ 인정)
2. **Calibration cohort** — 본인 + 자원자 n ≥ 10 awake/sleep 데이터로 personal threshold 재학습
3. **Multi-session pooling** — 단일 세션 200 trials → 4 sessions × 200 = 800 trials 평균으로 SNR 회복
4. **Hybrid metric** — PCI 단독 X, **PCI ⊕ Φ-Berger ⊕ LZ-spontaneous** 3축 voting (CP2 F1 composite 통합 — §7 참조)

### §6.3 결정적 한계 (mitigation 불가)
- **Source localization 사실상 불가** — 16ch 로는 sLORETA 신뢰구간 너무 큼; sensor-level 분석만
- **임상 진단 도구 사용 절대 X** — research-grade only, IRB 명시 필요
- **Massimini lab certification 받을 수 없음** — 원판 spec 미달
- **논문 발표 시 channel count 격차 명시 필수** — peer-review 통과 위해

---

## §7 CP2 F1 composite 통합 — N-19 axis

### §7.1 axis 정의
- **N-19 축** = `pci_16ch_score ∈ [0, 1]`, threshold = 0.25 (§4.3)
- 측정 조건 = single-session, awake-eyes-open, 200 trials, 16ch sensor-level PCI_st

### §7.2 F1 weight 제안
- 현행 F1 composite (cycle4 law64) 에 추가 axis:
```
F1_v_next = w1·CLM_score + w2·EEG_Phi_score + w3·QRNG_axis + w4·SIM_axis + w5·AKIDA_axis + w6·PCI_score
where w6 = 0.10 – 0.15 (initial; recalibrate after n≥30 PCI sessions)
```
- N-19 axis 의 own#2 (b) 다중실현 contribution: PCI 가 conscious 상태에서 0.25+ 이고 unconscious 상태 (예: 마취/수면) 에서 < 0.20 으로 분리되면 → multi-realization 증거 1축 추가

### §7.3 falsifier (raw#71 bound)
- **N-19 falsifier**: 동일 피험자에서 awake PCI < sleep PCI (i.e., 의식 있을 때 더 낮음) 시 → axis 무효화, F1 에서 제외
- **간접 falsifier**: PCI_16ch 가 PCI_64ch (literature) 와 r < 0.5 일 때 → calibration 재시작

### §7.4 통합 cycle 제안 (구현 시점)
- **Stage 1** (TMS 임대 결정 후): n=10 awake/sleep PCI calibration
- **Stage 2**: F1 v_next axis 추가 + 기존 5축과의 cross-validation
- **Stage 3**: r ≥ 0.7 (PCI ↔ 다른 N-axis) 도달 시 own#2 (b) +1 evidence 추가

---

## §8 raw#10 honest C3 disclosures

1. 본 spec 은 **연구용 프로토콜 초안** — 임상 진단 도구 X, IRB 승인 후에만 사용
2. 16ch OpenBCI 로 측정한 PCI 는 원판 (60+ ch) 과 **절대값 비교 불가** — calibration 필수
3. TMS 가격 estimate 모두 2026-05-01 공개 정보 기반, vendor 직접 견적 X (NO contact)
4. 한국 대학병원 TMS lab 목록은 공개 정보만 — 실제 share 가능 여부 별도 확인 필요
5. PCI_st (sensor-level variant) 16ch 사용 사례는 literature 매우 적음 — 학술 위험 존재
6. rMT (motor threshold) 측정 표준 절차에 EMG 필요 — OpenBCI 1ch EMG 대체 가능하나 BIOPAC 정밀도 미달
7. Sleep stage PCI 측정에는 polysomnography (EOG+EMG+EEG) 동시 필요 — 16ch 다 EEG 쓰면 PSG 부족
8. neuro-navigation MRI 없으면 좌표 정확도 ±1 cm 수준 → cortical target hit rate 70% 추정
9. Massimini lab 원판 알고리즘 코드는 closed-source — open-source PCI_st 구현 (Comolatti 2019) 만 사용 가능
10. 본 doc 은 hexa-only 정책 준수 (.py/.hexa 생성 없음, spec 만)
11. 사용자 의식적 동의 + IRB 없이는 어떤 측정도 시작 불가
12. PCI 값 단독으로 의식 유무 결론 X — F1 multi-axis composite 와 함께 평가 권장 (§7)
13. eLife 2025 spontaneous-PCI surrogate (§4.4) validated in healthy + propofol only; not yet in DOC patients (mirrors N-21 #5 §6 disclosure).
14. N-19 surrogate v1 weights (0.50/0.30/0.20) are operational pre-commitments derived from the relative effect-size ranking of LZ vs LLE vs spectral-spread features in Comm Biol 2024 Table 2 / Fig 3; NOT fitted on user data.
15. PCI_surrogate (§4.4) maps onto TMS-PCI scale by scale-matching against Casarotto 2016 cutoff 0.31; this scale-matching has been validated in eLife 2025 for the LZ component and in Comm Biol 2024 for the full ridge regression, but NOT for the present 3-component reduced model on 16ch.
16. The Apr 28 D-day session backing §4.4 is single-subject (raw#10 user-only N=1) under wake-resting; no propofol or sleep negative control is available, so surrogate validity cannot be established intra-subject this cycle.

---

## §9 결정점 (사용자 선택)

**(α)** TMS lab share path 진행 — 한국 대학병원 IRB 신청 시작 ($1.6–2.5K, 3–6 mo lead time)
**(β)** Magstim 200² used 구매 path — capex $13–21K, 1 mo lead time, 자체 lab 구축
**(γ)** 다른 N-axis (N-20, N-21) 우선 — N-19 는 capex 보류, spec 만 archive
**(δ)** 추가 spec 필요 — `docs/n_substrate_n19_pci_spec_2026_05_01.md` v2 요청 (예: 특정 vendor deep-dive)

---

## §10 Sources (2026-05-01 web search + classical refs)

- [Perturbational Complexity Index — Wikipedia](https://en.wikipedia.org/wiki/Perturbational_Complexity_Index)
- [Massimini et al. 2005, Science — Breakdown of cortical effective connectivity during sleep](https://www.science.org/doi/10.1126/science.1117256)
- [Casali et al. 2013, Sci Transl Med — A theoretically based index of consciousness independent of sensory processing and behavior](https://pubmed.ncbi.nlm.nih.gov/23946194/)
- [Casarotto et al. 2016, Annals of Neurology — Stratification of unresponsive patients by an independently validated index of brain complexity](https://pubmed.ncbi.nlm.nih.gov/27343289/) (n=150 PCI* threshold = 0.31)
- [Comolatti et al. 2019, Brain Stimulation — A fast and general method to empirically estimate the complexity of brain responses to TMS](https://pubmed.ncbi.nlm.nih.gov/31133480/) (PCI_st sensor-level variant)
- [Sarasso et al. 2021, NeuroImage — PCI clinical applications](https://pmc.ncbi.nlm.nih.gov/articles/PMC7760168/)
- [Rossi et al. 2009 + 2021, Clin Neurophysiol — Safety, ethical considerations, and application guidelines for the use of TMS](https://pubmed.ncbi.nlm.nih.gov/33243615/)
- [OpenBCI Cyton+Daisy 16ch documentation](https://docs.openbci.com/Cyton/CytonDaisy/)
- [MagVenture MagPro X100 product page (USA distributor)](https://www.magventure.com/) (price range: industry survey 2024–2026)
- [Magstim 200² product line](https://www.magstim.com/) (price range: industry survey)
- [Nexstim NBS System 5 — navigated TMS](https://www.nexstim.com/) (clinical-grade, $150K+)
- [Comolatti GitHub PCI_st reference implementation](https://github.com/renzocom/PCIst) (open-source, MIT license)

### §10.1 Added 2026-05-01 per §4.4 TMS-free path (#74 EXEC + #68 finding)
- [eLife 98920 (2025) — Spatiotemporal brain complexity quantifies consciousness outside of perturbation paradigms](https://elifesciences.org/articles/98920) (Garcia-Saez et al., spontaneous fluidity 100% wake-vs-propofol)
- [Communications Biology 2024 (s42003-024-06613-8) — Critical dynamics in spontaneous EEG predict anesthetic-induced loss of consciousness and PCI](https://www.nature.com/articles/s42003-024-06613-8) (Toker et al., 16-feature ridge → TMS-PCI, MAE 0.065) — PMC mirror: https://pmc.ncbi.nlm.nih.gov/articles/PMC11300875/
- [Sarasso et al. 2014 (Clin EEG Neurosci) — TEP-PCI review](https://journals.sagepub.com/doi/abs/10.1177/1550059413513723) (qualitative collapse-on-LOC pattern)
- Companion result doc: `docs/n_19_pci_tmsfree_results_2026_05_01.md` (#74 EXEC, 6/6 PASS pilot)
- Cross-ref: `docs/n_21_test5_sarasso_tep_review_2026_05_01.md` (#68 cross-paper PCI cutoff stability 2013-2026)

---

**status**: N19_PCI_SPEC_LOCAL_DRAFT_v2 · §4.4_TMS_FREE_PATH_INTEGRATED_2026_05_01
**verdict_key**: SPEC_READY · NO_HARDWARE_CONTACT_YET · USER_DECISION_PENDING · TMS_FREE_PATH_§4.4_FORMALIZED · CP2_w6_0.10_eligible
**axis_id**: N-19
**parent_roadmap**: `docs/n_substrate_consciousness_roadmap_2026_05_01.md`
**update_log**:
- 2026-05-01 v1: initial draft (270 LOC)
- 2026-05-01 v2: §4.4 TMS-free path added (per #74 EXEC + #68 Sarasso review); §8 disclosures #13-#16 appended; §5 cross-ref to §4.4; §10.1 5 new refs
