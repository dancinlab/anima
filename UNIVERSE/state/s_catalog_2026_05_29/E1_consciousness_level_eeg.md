# E1 — 의식-수준 EEG 클러스터: Φ-proxy ↔ 의식 수준 그라운딩

**작성일**: 2026-05-29
**클러스터**: consciousness-LEVEL EEG — Φ-proxy 측도(LZ76 / PCI / spectral)가 의식 수준(level of consciousness)을 추적하는가
**대상 가설**: S20 약물(psychedelic) · S33 마취(anesthesia) · S16 NDE/dying-brain
**범위**: 실제 발표 논문 + 다운로드 가능 공개 데이터셋 + 정직한 verdict-readiness 평가

> ⚠️ arxiv API(`export.arxiv.org`)는 이 클러스터에 해당 논문이 거의 없음 — 세 가설 모두 저널 발표(Nature/Science/PNAS/PLOS)이므로 **arxiv-id 대신 DOI/PMID가 정식 식별자**. arxiv 쿼리는 HTTP 301(→HTTPS)만 반환, preprint 없음 확인.

---

## 0. 한 줄 요약 verdict 매트릭스

| 가설 | Φ-proxy 측도 | 문헌 effect 방향 | 문헌 verdict | 데이터 readiness |
|---|---|---|---|---|
| **S33 마취** | LZ76 / PCI / spectral | 의식상실 시 **DECREASE** (강하고 일관) | 🟢 **SUPPORTED** | 🟢 **data-ready** (OpenNeuro ds005620) |
| **S20 약물** | LZ76 (single-channel temporal) | psychedelic 시 **INCREASE** | 🟡 **SUPPORTED-but-CONTESTED** (스펙트럼 confound 논쟁) | 🟡 **partial** (psychedelic raw EEG/MEG 공개 드뭄) |
| **S16 NDE/dying** | gamma power / connectivity / coherence | 사망 직후 일시적 **SURGE** (2/4 인간, 9/9 쥐) | 🟡 **MIXED** (n 극소 · LZ 직접측정 아님) | ⚪ **no-data** (인간 dying-brain raw EEG 비공개) |

---

## 1. S33 마취(anesthesia) — Φ-proxy DECREASE

### 1.1 핵심 논문

| 논문 | 저자 / 연도 | 식별자 | 핵심 측도 · 결과 |
|---|---|---|---|
| A Theoretically Based Index of Consciousness Independent of Sensory Processing and Behavior | Casali, Gosseries, Rosanova, Boly, Sarasso, … Tononi, Massimini, 2013 | DOI **10.1126/scitranslmed.3006294** · PMID **23946194** · *Sci. Transl. Med.* 5(198):198ra105 | **PCI 도입.** 깨어있음 PCI=0.44–0.67 → NREM 수면 0.18–0.28. propofol·midazolam·xenon 마취에서 PCI 하락. **컷오프 PCI\*=0.31**이 의식/무의식 완벽 분리 |
| Complexity of Multi-Dimensional Spontaneous EEG Decreases during Propofol Induced General Anaesthesia | Schartner, Seth, … Barrett, 2015 | DOI **10.1371/journal.pone.0133532** · PMID(PMC4529106) · *PLOS ONE* | **TMS 없이 spontaneous EEG의 LZ류 복잡도**가 propofol 전신마취 유도 중 **감소**. PCI 패러다임을 perturbation 없이 EEG로 확장한 핵심 선례 |
| Consciousness and Complexity during Unresponsiveness Induced by Propofol, Xenon, and Ketamine | Sarasso et al., 2015 | *Current Biology* 25(23):3099-3105 · DOI **10.1016/j.cub.2015.09.060** · PMID **26752078** | propofol/xenon = PCI 낮음(무의식, 보고 없음), **ketamine = PCI 깨어있음 수준 유지**(unresponsive지만 vivid ketamine-dream 사후보고). 즉 PCI는 "행동적 반응"이 아니라 "의식 경험 유무"를 추적 → **disconnected consciousness** |
| Stratification of unresponsive patients by an independently validated index of brain complexity (PCI 임상검증) | Casarotto et al., 2016 | *Ann. Neurol.* 80(5):718-729 · DOI **10.1002/ana.24779** | 150 양성 대조군에서 PCI\* 경험적 컷오프 도출·검증, 환자 stratify |

### 1.2 공개 데이터셋 (다운로드 가능)

| 데이터셋 | accession / URL | 내용 | 포맷 · 크기 | license |
|---|---|---|---|---|
| **OpenNeuro ds005620** ✅검증 | https://openneuro.org/datasets/ds005620 · DOI 10.18112/openneuro.ds005620.v1.0.0 · (EEG Dash mirror: https://eegdash.org/api/dataset/eegdash.dataset.DS005620.html) · 논문 *Sci. Rep.* https://www.nature.com/articles/s41598-025-12695-z | "A repeated awakening study exploring the capacity of complexity measures to capture dreaming during propofol sedation" — **3 task condition: `awake`(EC/EO wakefulness) / `sed`(propofol rest) / `sed2`(각성 직전 1-min rest)** | **BrainVision (.eeg/.vhdr/.vmrk)**; **21 subjects** (12F/8M/1NR), **202 EEG sessions**, 64/65 ch, **5000 Hz**, **총 77.3 GB**, ~17.9h | **CC0 (public domain)** — **마취-축 검증의 1순위, awake vs sed 라벨 명시** |
| **Chennu propofol sedation set** | Cambridge(Chennu) — 정식 공개 SSOT 별도 확인 필요 | 20 healthy, baseline / mild(0.6µg/mL) / moderate(1.2µg/mL) / recovery | EEG | 문헌서 널리 재사용; 단일 OpenNeuro accession은 미확정(저자 배포) |

> ✅ ds005620 사양은 WebFetch(EEG Dash 메타)로 직접 검증: 21 subjects / 202 sessions / BrainVision / 5000 Hz / 77.3 GB / CC0. `awake` vs `sed` condition 라벨이 events에 명시되어 LZ awake>sed 검증에 즉시 적합.
> ⚠️ 단, 동반 논문(Sci. Rep. 2025)의 결론: **awake→sed 복잡도는 유의 감소(가설 지지)** 하지만 **sed 내 dreaming vs no-experience는 복잡도로 구분 안 됨** — "low complexity ≠ no consciousness". 즉 S33의 거시 방향(의식 유/무)은 지지, 미세 구분(경험 내용)은 한계.

### 1.3 verdict
**🟢 SUPPORTED** — LZ류 복잡도와 PCI 모두 propofol/xenon/midazolam 의식상실에서 **감소**, ketamine 예외는 오히려 "PCI=의식경험 추적" 가설을 강화(disconnected consciousness). 단일 개인 단위 판별 가능(PCI\*=0.31). **데이터 readiness 🟢**.

---

## 2. S20 약물(psychedelic) — Φ-proxy INCREASE

### 2.1 핵심 논문

| 논문 | 저자 / 연도 | 식별자 | 핵심 측도 · 결과 |
|---|---|---|---|
| Increased spontaneous MEG signal diversity for psychoactive doses of ketamine, LSD and psilocybin | Schartner, Carhart-Harris, Barrett, Seth, Muthukumaraswamy, 2017 | DOI **10.1038/srep46421** · PMID **28422113** · *Sci. Rep.* 7:46421 | **psilocybin·LSD·ketamine 모두 spontaneous LZ 복잡도 INCREASE** — 스펙트럼 변화 통제(phase-randomised surrogate) 후에도 유지. **single-channel temporal LZ가 가장 강함**. 정상 각성보다 높은 값 → "elevated level of consciousness". 증가폭이 trip 주관강도와 상관 |
| Neural correlates of the DMT experience assessed with multivariate EEG | Timmermann, Roseman, Schartner, Millière, … Carhart-Harris, 2019 | DOI **10.1038/s41598-019-51974-4** · *Sci. Rep.* 9:16324 | IV DMT: alpha·beta power 현저 감소 + **spontaneous LZ 복잡도 robust 증가**. **LZc 시계열이 주관 trip 강도와 시간적으로 동기** |
| Increased signal diversity/complexity of spontaneous EEG, but not evoked EEG responses, in ketamine-induced psychedelic state | Farnes, Juel, … Storm, 2020 | DOI **10.1371/journal.pone.0242056** · *PLOS ONE* | spontaneous EEG LZ 증가 재현. **단 evoked 응답은 증가 안 함** — spontaneous vs evoked 구분이 해석에 중요. 스펙트럼 통제 후에도 subanesthetic ketamine LZ↑ |
| The entropic brain – revisited | Carhart-Harris, 2018 | DOI **10.1016/j.neuropharm.2018.03.010** · *Neuropharmacology* | "Entropic Brain" 이론 프레임 — LZ/엔트로피 = 의식 경험의 richness |

### 2.2 contested 측면 (정직 보고)
- **스펙트럼 confound 논쟁**: LZ76은 신호의 power spectrum(특히 고주파 비중)에 민감. psychedelic은 alpha 억제 + 고주파 상대증가를 일으키므로, LZ 증가 일부가 "의식 수준↑"이 아니라 **단순 스펙트럼 평탄화의 부산물**일 수 있다는 비판. Schartner 2017은 phase-randomised surrogate로 일부 통제했으나, 후속 비평(Frohlich 등 complexity-as-consciousness 회의론)은 LZ를 normalize/detrend 없이 쓰면 confound 잔존을 지적.
- **방향성 자체는 일관**(여러 약물·여러 연구실 재현)이나 "**LZ 증가 = 의식 수준 증가**"라는 인과 해석은 논쟁 중. 약물 상태가 마취보다 "높은 수준"이라는 주장은 IIT의 level 정의와도 긴장 관계.

### 2.3 공개 데이터셋
| 데이터셋 | accession / URL | 내용 | 비고 |
|---|---|---|---|
| OpenNeuro ds006110 (PsiConnect) | https://openneuro.org/datasets/ds006110 | psilocybin 멀티모달 신경영상 | **주로 fMRI/멀티모달** — resting EEG epoch 포함 여부 페이지 확인 필요 |
| OpenNeuro ds006072 | https://openneuro.org/datasets/ds006072 | "Psilocybin Precision Functional Mapping" | **fMRI 중심** — EEG 아님 |
| PsiConnect (Monash) | biorxiv 2025.04.11.643415 · OpenNeuro accession은 검색상 ds006110로 인용되나 페이지 직접확인 필요 | psilocybin 멀티모달, **62 participants, EEG+fMRI** (rest/meditation/music/movie) | **EEG epoch 포함** — placebo vs psilocybin resting EEG로 LZ 재계산 가장 유망. 단 accession·포맷·라이선스 직접확인 미완(WebFetch 429 차단) |

> ⚠️ **Schartner 2017의 원천 MEG는 공개 raw 형태로 일반 배포되지 않음**(Imperial/Cardiff IRB). 깨끗한 공개 psychedelic raw EEG는 드물지만 **PsiConnect(62명, EEG 포함)가 가장 유력한 후보** — accession/포맷 확정 시 🟡→🟢 승격 가능. 현재는 페이지 직접검증 미완으로 partial 유지.

### 2.4 verdict
**🟡 SUPPORTED-but-CONTESTED** — effect 방향(LZ INCREASE)은 다수 재현으로 견고하나, 스펙트럼 confound로 "의식 수준↑" 인과 해석은 논쟁. **데이터 readiness 🟡** (psilocybin EEG 공개셋은 부분적, raw MEG 비공개).

---

## 3. S16 NDE/dying-brain — gamma/complexity SURGE

### 3.1 핵심 논문

| 논문 | 저자 / 연도 | 식별자 | 핵심 측도 · 결과 |
|---|---|---|---|
| Surge of neurophysiological coherence and connectivity in the dying brain (**쥐**) | Borjigin et al., 2013 | DOI **10.1073/pnas.1308285110** · PMID **23940340** · *PNAS* 110(35):14432 | 심정지 **30초 이내** 동기적 gamma 진동·기능적 연결성의 일시적 surge, isoelectric EEG에 선행. n=9 쥐 일관 |
| Surge of neurophysiological coupling and connectivity of gamma oscillations in the dying human brain (**인간**) | Xu, Mihaylova, Li, Tian, Farrehi, Parent, Mashour, Wang, Borjigin, 2023 | DOI **10.1073/pnas.2216268120** · *PNAS* 120(19):e2216268120 · PMC10175832 | 인공호흡기 제거 후 hypoxia가 **4명 중 2명**에서 gamma 활동 자극. TPO junction 국소 + TPO↔대측 전두 전역 gamma 연결성 surge |

### 3.2 contested / 한계 (정직 보고)
- **표본 극소**: 인간 n=4 중 2명만 surge. 통계적 일반화 불가, 사례연구 수준.
- **측도 불일치**: 이 가설들은 **gamma power·coherence·connectivity**를 측정 — S20/S33의 LZ76/PCI와 **직접 동일 측도가 아님**. "complexity surge"는 간접 추론.
- **의식 경험 입증 불가**: surge가 실제 주관 경험(NDE)과 연결된다는 직접 증거 없음 — 환자 모두 사망, 보고 불가.
- 따라서 "Φ-proxy↔의식수준" 명제 검증으로는 **가장 약한 고리**.

### 3.3 공개 데이터셋
| 데이터셋 | 상태 |
|---|---|
| Borjigin 2023 인간 dying-brain EEG | **공개 raw 데이터 미확인** — ICU 사망환자 IRB 제약, PNAS supplement도 raw EDF 미배포 추정 |
| Borjigin 2013 쥐 EEG | 공개 raw 미확인 |

> ⚠️ **검증 가능 공개 raw EEG를 확인하지 못함**. 데이터 존재 확인 불가 → no-data로 정직 보고.

### 3.4 verdict
**🟡 MIXED (문헌)** / **⚪ no-data (검증 readiness)** — surge 현상은 보고됐으나 n 극소 + LZ 직접측정 아님 + 공개 raw 부재. 로컬 검증 불가.

---

## 4. 로컬 최소 검증 파이프라인 (computable)

### 4.1 S33 마취 — 🟢 즉시 실행 가능 (1순위)
```
1. OpenNeuro ds005620 다운로드 (BrainVision .eeg/.vhdr/.vmrk; aws s3 sync s3://openneuro.org/ds005620 또는 datalad). 77.3 GB → 일부 subject만 받아 toy 가능
2. condition 분리: task-`awake` (EC/EO 각성) vs task-`sed` (propofol rest) — 파일명/events에 라벨 명시
3. 각 epoch LZ76:
   - 5000 Hz → downsample(예: 250 Hz) + bandpass 후
   - binarize: 채널별 Hilbert amplitude > median → 0/1
   - Lempel-Ziv 1976 complexity → 길이 정규화 LZc
4. 사전등록 falsifier: LZc_awake > LZc_sed (paired, per-subject; sign-test / Wilcoxon)
   기대: 다수 subject에서 awake 우세 (Schartner 2015 + ds005620 동반논문 재현)
5. (옵션) spectral confound 통제: phase-randomised surrogate 대비 정규화
주의: sed 내 dreaming-구분은 시도 말 것(동반논문서 복잡도로 구분 불가 확정) — 거시 awake/sed 방향만 검증
```
검증 tier 목표: 🟢 numerical (per-subject paired effect 방향 + 부호검정).

### 4.2 S20 약물 — 🟡 제약 하 실행
```
psilocybin 공개 EEG epoch 확보 가능 시:
- placebo vs drug resting EEG에 동일 LZ76
- falsifier: LZc_drug > LZc_placebo
- 필수: phase-randomised surrogate로 스펙트럼 confound 통제 (contested 축 직접 대응)
제약: 깨끗한 공개 psychedelic raw EEG 부재 → 우선 ds006110 EEG epoch 유무 확인 선행
```

### 4.3 S16 NDE — ⚪ 검증 보류
```
공개 raw 부재로 LZ 재계산 불가.
대안: 문헌의 gamma power/connectivity 수치를 메타-인용만 (측정 불가, 🟡 citation tier).
```

---

## 5. 종합 verdict-readiness

| 가설 | 문헌 verdict | 로컬 검증 readiness | 권장 다음 수 |
|---|---|---|---|
| **S33 마취** | 🟢 SUPPORTED | 🟢 **data-ready** | ds005620 받아 LZ76 awake>sedated 즉시 fire |
| **S20 약물** | 🟡 SUPPORTED-CONTESTED | 🟡 partial | psychedelic EEG 공개셋 확보 우선, surrogate 통제 필수 |
| **S16 NDE** | 🟡 MIXED | ⚪ no-data | 문헌 인용만, raw 부재로 검증 보류 |

---

## 양방향 sibling
- sibling cluster: UNIVERSE/state/s_catalog_2026_05_29/ 내 타 E_* 카탈로그 (작성 시 cross-link)
- SSOT: UNIVERSE/CANDIDATES.md (S16/S20/S33 후보 등록 행과 연결 — 등록 시 본 파일 포인터 추가)
