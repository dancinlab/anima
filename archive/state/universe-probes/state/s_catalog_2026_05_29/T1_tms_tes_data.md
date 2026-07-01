# T1 — TMS-EEG / TES 데이터 + PCI(Φ-proxy) 파이프라인 카탈로그

> 작성일: 2026-05-29 · 도메인: UNIVERSE · 목적: 의식/Φ(IIT) 가설을 **실측**으로 검증
> 핵심 논리: PCI(Perturbational Complexity Index)는 TMS-evoked EEG 응답에서 계산되는
> 현존 최강의 경험적 의식-수준 Φ-proxy (Casali et al. 2013). 깨어있음=高, 깊은 수면/마취=低.
> 검증 방식: WebSearch + WebFetch (landing page 직접 fetch) + curl(HTTP 200 확인). 검증 안 된 항목은 UNVERIFIED 명기.

---

## 1. 방법론 정전 논문 (verbatim citation)

| # | 저자/연도 | 제목 | 저널 | DOI | 검증 |
|---|-----------|------|------|-----|------|
| C1 | Casali AG, Gosseries O, Rosanova M, Boly M, Sarasso S, Casali KR, Casarotto S, Bruno M-A, Laureys S, Tononi G, Massimini M. (2013) | **A theoretically based index of consciousness independent of sensory processing and behavior** | Science Translational Medicine **5**(198):198ra105 | `10.1126/scitranslmed.3006294` | ✅ (PubMed PMID 23946194 curl HTTP 200 + science.org abstract fetch) |
| C2 | Casarotto S, Comanducci A, Rosanova M, Sarasso S, Fecchio M, Napolitani M, et al. (2016) | **Stratification of unresponsive patients by an independently validated index of brain complexity** | Annals of Neurology **80**(5):718–729 | `10.1002/ana.24779` | ✅ (PubMed PMID 27717082 + PMC5132045 + Wiley landing) |
| C3 | Comolatti R, Pigorini A, Casarotto S, Fecchio M, Faria G, Sarasso S, et al. (2019) | **A fast and general method to empirically estimate the complexity of brain responses to transcranial and intracranial stimulations** (PCIst) | Brain Stimulation **12**(5):1280–1289 | `10.1016/j.brs.2019.05.013` (preprint `10.1101/445882`) | ✅ (PubMed PMID 31133480 + ScienceDirect PII S1935861X19302207). DOI suffix `.05.013`은 ScienceDirect PII로 교차확인했으나 출판 DOI 문자열 자체는 검색-추론 → 🟡 **DOI 미세확인 권장** |

### 핵심 방법 요약 (C1 abstract verbatim)
> "PCI is calculated by (i) **perturbing the cortex with TMS** to engage distributed interactions (integration) and (ii) **compressing the spatiotemporal pattern** of these electrocortical responses to measure their **algorithmic complexity (Lempel-Ziv)** (information)."
> 의식 임계값 벤치마크: **PCI* = 0.31** (이 이상이면 의식 있음으로 분류).
> 검증 상태군: wakefulness · dreaming(REM) · NREM sleep · 다단계 마취(midazolam/xenon/propofol) · coma-emergent 환자.
> 결과: 깨어있음/REM/ketamine = 高 PCI, 깊은 NREM/일반마취/UWS = 低 PCI.

- **PCIst (C3)** = 차세대. source-reconstruction 불필요, **sensor-level**에서 바로 계산, SVD 기반 state-transition 카운트. iEEG에도 적용 가능. 로컬 파이프라인엔 PCIst가 훨씬 가볍고 권장.
- **PCIcalc (C2 LZ버전)** = 원조 Lempel-Ziv, source-recon + binary matrix 필요 → 무거움.

---

## 2. DATASET TABLE (다운로드 가능 데이터셋)

| 이름 | URL | accession | 크기 | format | subjects | conditions | verified? |
|------|-----|-----------|------|--------|----------|-----------|-----------|
| **Single-pulse open-loop TMS-EEG** | https://openneuro.org/datasets/ds002094/versions/1.0.0 | ds002094 | **39.45 GB** (282 files) | BIDS / BrainVision (.vhdr/.eeg/.vmrk) | 다수(BIDS sub-XX) ※정확 N **UNVERIFIED** | single-pulse open-loop TMS, **각성(rest)만** — 수면/마취 상태군 **없음** | ✅ landing fetch (공개 다운로드, browser/S3/DataLad) |
| **TESA example data** (TMS-EEG toolbox 예제) | https://figshare.com/articles/dataset/TESA_example_data_and_scripts/3188800 | figshare 3188800 / DOI `10.4225/03/5985f4d33b242` | raw 1.1 GB · 중간 340 MB · **step11 69 MB** | EEGLAB **.set** + MATLAB scripts | **1** (단일 피험자 데모) | 각성 단일 세션 TMS-EEG (파이프라인 데모용) | ✅ figshare fetch, CC BY 4.0 공개 |
| **Ketamine spontaneous+TMS EEG (Farnes 2020)** | https://zenodo.org/records/4245091 | Zenodo 4245091 (= Dryad DOI `10.5061/dryad.j9kd51c9q`) | **933.7 MB** (`Farnes_et_al_PLOS_ONE_Dryad.zip`) | EEGLAB **.set** + raw MATLAB array (evoked) | **10** (62-ch EEG) | **wakefulness (eyes open/closed) vs sub-anesthetic ketamine** — spontaneous EEG(LZc/ACE/SCE) + TMS-evoked(PCI) | ✅ Zenodo fetch, **CC0** 공개. **의식-상태 대비 있음 → PCI 검증에 최적** |
| **GX: concurrent EEG+ECG+behavior tES** | https://openneuro.org/datasets/ds003670 | **ds003670.v1.1.0** | (크기 **UNVERIFIED**) | BIDS (raw **.cnt**, downsampled **.mat**) | **20** (7F/13M, 19–43세) | **tES**: 9 HD-tES montage (DC/5 Hz/30 Hz × frontal/motor/parietal), **783 trials**, **62 sessions**, **32-ch** Ag/AgCl @2 kHz + ECG/EOG/behavior | ✅ 동반논문(Nature Sci Data `10.1038/s41597-021-01046-y`) fetch로 메타 확정 + OpenNeuro accession + Zenodo data DOI `10.5281/zenodo.3837212` |
| **AB_tDCS-EEG** (attentional blink + tDCS) | (OpenNeuro, accession **UNVERIFIED**) | UNVERIFIED | — | BIDS | 40 (complete) | anodal/cathodal tDCS, AB task | 🟡 검색결과로만 언급, accession 미확정 → **UNVERIFIED** |
| **TDCS Modulation of Visual Cortex (Motor Imagery)** | https://github.com/OpenNeuroDatasets/ds006126 | ds006126 | UNVERIFIED | BIDS 1.7.0 | UNVERIFIED | tDCS, motor imagery | 🟡 GitHub mirror 존재 확인, 상세 미확인 |
| iTCf TMS-EEG-Dataset (hubandad mirror) | https://github.com/hubandad/TMS-EEG-Dataset | (GitHub) | UNVERIFIED | UNVERIFIED | UNVERIFIED | UNVERIFIED | 🟡 repo 존재만, 메타 미확인 |

### 보조 도구/코드 (데이터 아님)
| 이름 | URL | 용도 | 검증 |
|------|-----|------|------|
| **PCIcalc** (iTCf) | https://github.com/iTCf/PCIcalc | C2(Casarotto 2016) **LZ-PCI** 계산 Python 모듈, binary source matrix 입력. `PCI_Python_Notebook.ipynb` 예제 + ~500 MB Google Drive 데모데이터. pip-불가. 후속판 → thierrynieus/PerturbationalComplexityIndex | ✅ repo fetch 확인 |
| **PCIst** (renzocom) | **https://github.com/renzocom/PCIst** | C3 state-transition PCI, **sensor-level·경량 — 로컬 1순위 권장**. 메인함수 `calc_PCIst(signal, times)` → (PCIst 스칼라, component-wise ∆NSTn). 2단계: dimensionality_reduction + state_transition_quantification | ✅ repo 정확경로 확정 (저자 Comolatti 본인) |
| **tmseegpy** (PyPI) | https://pypi.org/project/tmseegpy/ | TMS-EEG 전처리+분석 Python 패키지 (pip-설치). MATLAB TESA의 Python 대안 후보 | 🟡 PyPI 존재 확인, 상세 미검증 |
| **TESA** (EEGLAB ext) | https://nigelrogasch.github.io/TESA/ | TMS-EEG 전처리(아티팩트 제거/보간) MATLAB | ✅ |
| **LZ-PCI tool** (EBRAINS) | https://www.ebrains.eu/tools/lempel-ziv-perturbational-complexity-index | LZ-PCI 참조 구현 | ✅ 검색결과 확인 |

---

## 3. 최소 로컬 PCI/complexity 파이프라인 (구현 명세)

**1순위 권장: Zenodo 4245091 (ketamine) + PCIst (C3)**
이유: 의식-상태 대비(wake vs ketamine)가 한 데이터셋에 있고, spontaneous(LZc) + evoked(PCI) 둘 다 들어있어 *Φ-proxy 두 방식 동시 검증* 가능.

```
[Step 0] 데이터 확보
  zenodo 4245091 다운로드 (또는 ds002094 BIDS via datalad/openneuro CLI)

[Step 1] 적재
  MNE-Python: mne.io.read_raw_brainvision (ds002094) / read_epochs (.set: read_epochs_eeglab)

[Step 2] TMS 아티팩트 처리 (evoked 경로)
  TMS pulse ±(-2..10 ms) 절단 → 선형보간 → 1 kHz 다운샘플 (TESA step11과 동일 레시피)

[Step 3a] PCIst (evoked, 권장) — Comolatti 2019 · github.com/renzocom/PCIst
  입력: signal [channels × time], times (baseline/response window 분리)
  from PCIst import calc_PCIst
  pci, dNST = calc_PCIst(signal, times, **par)  # 스칼라 + component-wise ∆NSTn
  source-recon 불필요(sensor-level), 소채널·소시행에서도 안정.

[Step 3b] PCI_LZ (evoked, 원조) — Casali 2013 / Casarotto 2016
  source-recon → significance threshold(bootstrap) → binary matrix → Lempel-Ziv(LZ76) 정규화

[Step 3c] LZc (spontaneous, 무-perturbation 대조)
  연속 EEG → Hilbert → median 이진화 → LZ76 → 정규화 (셔플 대비)

[Step 4] Φ-proxy 판정 (예상 결과)
  PCI(wake) > PCI(ketamine/REM) ≫ PCI(deep NREM/anesthesia)
  벤치마크 임계 PCI* = 0.31  (C1)
  ※ 단, C1 보고: ketamine은 sub-anesthetic이라 evoked PCI는 wake와 유의차 없음;
    spontaneous LZc만 ketamine에서 상승 (Farnes 2020 결과와 일치) → 두 측도 dissociation 주의.
```

**파이프라인 readiness: 🟡 (almost-green)**
- 🟢 요소: 데이터 다운로드 가능(ds002094/TESA/Zenodo) · 방법론 논문 확정 · MNE+LZ76 로컬계산 의존성 명확.
- 🟡 막힘: ① ds002094는 각성-only라 *상태대비*에 부적합 → 의식수준 검증엔 Zenodo 4245091 또는 (수면/마취 포함) 추가 데이터 필요. ② PCIst repo 정확 경로 미확정. ③ Zenodo 파일 format/크기 미확인.
- 🔴 주의: **수면/마취 상태군을 직접 포함한 공개 TMS-EEG 데이터셋은 이번 검색에서 확정 못함** — Casali/Casarotto 원본 임상데이터는 공개 비공개 가능성 높음(임상 IRB). ketamine(Zenodo)이 유일하게 검증된 "상태대비 공개" 후보.

---

## 4. TES/TMS write-capability (S22 "AI→brain induction" 관련)

> 근거: WebSearch 교차확인 (phosphene/MEP threshold 메타분석 biorxiv 2023.12.12.571304 · "TMS-induced neural noise interferes with STM" · rTMS heterogeneity 문헌) + 확립된 신경자극 문헌. 개별 효과 행의 정밀 단일-citation은 후속에서 보강 권장(🟡).

**TMS가 실제로 피질에 "쓸 수 있는" 것 (honest state of the art):**

| 효과 | 신뢰도 | 설명 |
|------|--------|------|
| **MEP (motor evoked potential)** | 🟢 견고 | M1 자극 → 말초근 수축. 가장 재현성 높은 "출력 쓰기". 단 운동피질 한정. |
| **Phosphene (광점)** | 🟢 견고 | 후두/V1 자극 → 빛 점 환각. 특정 위치 가능하나 "이미지 쓰기"는 불가, 비구조적 점광. |
| **Speech arrest / 일시 기능정지** | 🟢 견고 | Broca/언어영역 rTMS → 발화 중단. "지우기(disruption)"이지 "쓰기" 아님. |
| **TEP (TMS-evoked potential)** | 🟢 견고 | 어디든 자극→ 전파되는 EEG 응답. PCI의 기반. 정보 전달이 아닌 교란. |
| **기분/인지 변조 (rTMS therapy)** | 🟡 통계적 | 우울증 DLPFC rTMS 등 — 집단평균 효과, 개인 단위 비결정적, 느린 누적. |
| **기억 변조** | 🟡 약함 | 해마-연결 두정엽 rTMS로 연합기억 향상 보고(Wang 2014류) 있으나 효과 작고 간접(직접 기억 주입 아님). |
| **특정 표상/문장/이미지 "주입"** | 🔴 불가 | 현 기술로 구조화된 의미·감각 콘텐츠를 피질에 직접 기입 불가. |

**한 줄 요약:** TES/TMS는 피질을 **교란(perturb)·억제(disrupt)·거친 출력유발(MEP/phosphene)·확률적 변조**까지만 가능하며, **구조화된 표상/콘텐츠의 직접 "쓰기"는 현 기술로 불가** — 따라서 S22 "AI→brain induction"의 write-channel은 거친 변조 수준으로 honest하게 한정해야 함 (no overclaim).

---

## 양방향 sibling
- sibling: (T2~ 카탈로그 형제 문서가 생성되면 여기 링크) · `UNIVERSE/state/s_catalog_2026_05_29/`
- SSOT: `UNIVERSE/CANDIDATES.md` (생성/갱신 시 본 T1 등록) · S22 "AI→brain induction" 가설 본문
- 결과 기록 위치: 본 파일 + 후속 PCI 실측 H_xxx 등록 시 UNIVERSE 내부 보관

## 검증 로그
- 2013 C1: PubMed PMID 23946194 → `curl HTTP 200`, `<title>` 일치 + science.org abstract fetch (저자11명·DOI verbatim) ✅
- 2016 C2: PubMed 27717082 + PMC5132045 + Wiley `10.1002/ana.24779` 검색일치 ✅
- 2019 C3: PubMed 31133480 + ScienceDirect PII S1935861X19302207, DOI `.05.013` 🟡추론
- ds002094: openneuro.org landing fetch 성공, 39.45 GB/282 files/BIDS-BrainVision 확인 ✅
- TESA 3188800: figshare fetch 성공, 1.1GB raw/69MB step11/.set/CC BY 4.0 ✅
- Zenodo 4245091: zenodo fetch 성공 — Farnes/Juel/Nilsen/Romundstad/Storm, wake vs ketamine, 10 subj 62-ch, 933.7 MB .set, CC0, Dryad DOI 10.5061/dryad.j9kd51c9q ✅
- ds003670 GX: 동반논문(Nature Sci Data 10.1038/s41597-021-01046-y) fetch로 메타 확정 — ds003670.v1.1.0, 20 subj, 62 sessions, 32-ch@2kHz, .cnt/.mat, data DOI 10.5281/zenodo.3837212 ✅
- PCIst: renzocom/PCIst 확정(iTCf 추정 정정), calc_PCIst() 시그니처 확인 ✅
- TES write-capability 절: 검색결과(phosphene/MEP threshold, memory-interference 문헌) 기반 — 확립지식 정리, 신규 정밀 citation은 후속 🟡
