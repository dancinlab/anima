# E2 — 임상적 의식장애 + 발달 클러스터 (S32 · S27 · S34)

> deep-research 산출 · 2026-05-29 · UNIVERSE 도메인 의식/Φ(IIT) 가설 실측 검증 준비도 평가
> 정직성 원칙: 실제 인용만, 조작 없음. 직접 확인 못 한 항목은 `[미확인]`으로 표기.

---

## 0. 한눈 요약 (per-hypothesis 준비도)

| 가설 | 주제 | 측정가능성 verdict | 핵심 marker | 공개 데이터 | 준비도 |
|------|------|-------------------|-------------|-------------|--------|
| **S32** | 식물인간 vs locked-in vs MCS vs 의식 | **operationalizable, 임상검증 완료** | PCI (TMS-EEG, Lempel-Ziv) | 환자 raw 제한적, PCIcalc 코드 공개 | 🟡 |
| **S27** | DID (해리성 정체성) | **약하게 operationalizable / 대부분 임상** | fMRI 상태대비 (Φ proxy 없음) | 공개 raw 부재 | ⚪ |
| **S34** | 영아 의식 발달 | **operationalizable, marker 명확** | late slow wave (P3-유사 비선형 신경응답) | 영아 EEG OpenNeuro + 신생아 EEG Zenodo | 🟡→🟢(데이터有) |

준비도 범례: 🟢 = 공개데이터+검증 marker로 즉시 로컬 재현 가능 / 🟡 = marker·일부 데이터 존재하나 완전 재현엔 gap / ⚪ = Φ-proxy 미정의·falsifiable 신경지표 부재.

**핵심 결론**:
- **S32(PCI)** = 이 클러스터의 강자. Casarotto 2016이 의식 benchmark에서 **PCI\* cutoff = 0.31, 100% sensitivity + 100% specificity**로 의식↔무의식 분리, MCS 검출 **94.7% sensitivity**, VS 환자 중 **9/43**이 의식 분포와 겹치는 고-PCI(은닉의식 시사). locked-in은 행동무반응이나 PCI 高 → 의식으로 정확 분류.
- **S34** = Kouider 2013이 영아 지각적 의식의 **late slow wave** marker를 5~15개월에서 측정 — 발현 시점 질문에 falsifiable 지표 존재. **OpenNeuro ds005106 영아 EEG 공개** → 로컬 파이프라인 구축 가능.
- **S27** = 신경영상 상태대비는 있으나 "한 뇌 속 다중 의식"을 정량화하는 Φ-proxy 부재 → 현 상태 ⚪.

---

## 1. S32 — 식물인간 vs locked-in: PCI로 의식수준 구분 가능한가?

### 1.1 핵심 논문

| 역할 | 인용 | 연도 | DOI / ID |
|------|------|------|----------|
| **PCI 원논문** | Casali AG, Gosseries O, Rosanova M, Boly M, Sarasso S, Casali KR, Casarotto S, Bruno MA, Laureys S, Tononi G, Massimini M. "A theoretically based index of consciousness independent of sensory processing and behavior." *Science Translational Medicine* 5(198):198ra105 | 2013 | **10.1126/scitranslmed.3006294** · PMID 23946194 |
| **임상 stratification** | Casarotto S, Comanducci A, Rosanova M, Sarasso S, Fecchio M, Napolitani M, et al. "Stratification of unresponsive patients by an independently validated index of brain complexity." *Annals of Neurology* 80(5):718-729 | 2016 | **10.1002/ana.24779** · PMID 27717082 |
| (도구) PCIcalc | iTCf/PCIcalc — Casarotto 2016 PCI(LZ) 계산 공개 모듈 | — | github.com/iTCf/PCIcalc |

### 1.2 측정 방식

PCI = 피질을 **TMS**로 교란(perturbation) → EEG 응답의 **Lempel-Ziv(LZ76) 복잡도**(유의성 thresholding 후 binary 시공간 행렬의 압축률, 정규화) 측정. IIT 두 축 — **통합(integration)**(여러 피질 영역이 *함께* 반응) × **정보/분화(differentiation)**(서로 *다른* 반응) — 공존 시 PCI 최대.

### 1.3 정량 결과 (Casali 2013 benchmark)

- TMS-evoked potential을 각성·꿈·NREM 수면·진정(midazolam·xenon·propofol)·혼수회복 환자에서 측정.
- 의식 상태(각성·REM 꿈·ketamine) → **PCI 높음**; 무의식(NREM·midazolam·xenon·propofol) → **PCI 낮음**.
- **"PCI가 단일 개인 수준에서 의식수준을 신뢰성 있게 판별"** — VS·MCS·locked-in 구분 포함. *(abstract verbatim, PMID 23946194)*
- 본 세션에서 full-text PDF의 상태별 PCI *수치 구간*은 추출 차단 → `[수치구간 미확인, full-text 재확인 권장]`.

### 1.4 임상 정확도 (Casarotto 2016) — **verbatim 확정**

| 항목 | 값 | 출처 |
|------|-----|------|
| Benchmark 모집단 | **150** (건강대조 + 의사소통가능 뇌손상자; 각성·disconnected·무의식 상태) | 다수 2차 verbatim |
| ROC 분석 PCImax | **AUC 100%** | verbatim |
| 경험적 cutoff **PCI\*** | **0.31** | verbatim |
| 의식↔무의식 분리 (benchmark) | **sensitivity 100% · specificity 100%** | verbatim |
| 적용 환자군 | **MCS 38명 + VS 43명** (noncommunicative DOC) | verbatim |
| MCS 검출 sensitivity | **94.7%** | verbatim |
| 고-PCI VS 환자 | **9 / 43** VS가 의식 benchmark 분포와 겹치는 고-PCI → **은닉의식(covert consciousness / CMD) 시사** | verbatim |
| locked-in syndrome | 행동 무반응이나 **PCI 高 → 의식으로 분류** (PCI가 행동·감각처리와 독립) | 원논문 설계 주장 |

> 메모: 일부 2차 문헌은 MCS 적용 코호트를 "12명 중 11명이 0.31 초과"로 인용(다른 하위 분석/연구). 본 표의 38/43·94.7%·9/43이 Casarotto 2016 main 결과로 가장 일관되게 인용됨.

### 1.5 측정가능성 verdict — 🟡 (operationalizable + 임상검증 완료)

PCI는 행동·감각과 독립이라 *locked-in을 의식으로, 진짜 무의식 UWS를 무의식으로* 구분 — 이 클러스터 최강 Φ-proxy. **gap**: navigated TMS-EEG 장비 + DoC 환자 raw가 공개 부족(Milano iTCf 그룹 요청기반). PCIcalc 코드는 공개 → 자체 TMS-EEG raw만 있으면 즉시 재현 가능.

---

## 2. S27 — DID: "한 뇌 속 다중 의식"의 신경/Φ 서명?

### 2.1 핵심 논문

| 인용 | 연도 | DOI / ID | 검증 |
|------|------|----------|------|
| Reinders AATS, Marquand AF, Schlumpf YR, Chalavi S, Vissia EM, Nijenhuis ERS, Dazzan P, Jäncke L, Veltman DJ. "Aiding the diagnosis of dissociative identity disorder: pattern recognition study of brain biomarkers." *British Journal of Psychiatry* 215(3):536-544 | 2019 | **10.1192/bjp.2018.255** · PMID 30523772 | ✅ WebFetch verbatim (n=32 DID + 43 HC, 구조 MRI) |
| Reinders AATS, Veltman DJ. "Dissociative identity disorder: out of the shadows at last?" (editorial) *British Journal of Psychiatry* 219(2):413-414 | 2021 | **10.1192/bjp.2020.168** | ✅ 검색 확정 |
| Reinders AATS, et al. "Opposite brain emotion-regulation patterns in identity states of DID: A PET study and neurobiological model." *Psychiatry Research: Neuroimaging* 223:236-243 | 2014 | **10.1016/j.pscychresns.2014.05.005** | ✅ Crossref verbatim |
| Schlumpf YR, Reinders AATS, et al. "Dissociative part-dependent resting-state activity in DID: a controlled fMRI perfusion study." *PLOS ONE* 9(6):e98795 | 2014 | **10.1371/journal.pone.0098795** · PMID 24922512 | ✅ 검색 확정 |

> ⚠️ 정직성 정정: 초기 초안에 "Dimitrova … Neuroimaging distinct identity states … *Psychological Medicine* 53(7) DOI 10.1017/S0033291721005225 (PMID 34244752)"로 적었던 항목은 **검증 실패 → 삭제**함. 근거: (1) Crossref title/저자 검색에서 해당 제목 논문이 surface 안 됨, (2) PMID 34244752 직접 조회가 무관 논문(대장암 메타분석)을 반환 → **PMID 자체가 신뢰 불가(hallucination 의심)**. 위 표는 Crossref/WebFetch로 verbatim 확인된 DID 신경영상 논문만 등재. (Dimitrova 2021/2023 *Psychological Medicine* 해마 CA1 biomarker 논문 10.1017/S0033291721002154은 별개 주제(해리성 기억상실)로 존재하나 "정체성 상태 대비"가 아님.)

### 2.2 무엇이 측정되었나 / 정직한 평가

- **modality**: PET/fMRI 상태대비 — 서로 다른 정체성 상태(trauma-avoidant TAIS vs trauma-related TRIS). 정체성 상태 간 신경활동 차이 *측정됨* (Reinders 2014 PET에서 정체성 상태별 emotion-regulation 반대 패턴; Schlumpf 2014에서 EP vs ANP rCBF 차이 보고).
- **진짜 DID vs 건강대조 분류**: Reinders 2019 BJP가 **구조 MRI 기반 패턴인식(ML) 분류기로 DID 환자(n=32)를 건강대조(n=43)와 구분** — **sensitivity 72% · specificity 74% · AUC 0.74** (verbatim). chance 이상이나 임상 진단 수준(>90%)엔 미달. → "DID에 측정가능한 뇌 차이 존재"는 근거 있으나 약함.
- **그러나 Φ 관점**: 측정된 것은 "정신상태 전환에 따른 BOLD/구조 차이"이지, **"두 개 이상의 의식이 한 뇌에 (동시) 존재"를 정량화한 통합정보(Φ) 측정이 아님.** DID에 PCI류 측정을 한 연구 0건.

### 2.3 측정가능성 verdict — ⚪

**현 상태 Φ-proxy로 operationalize 불가.** "다중 의식" 명제를 falsify할 신경지표 미정의. 신경영상 상태대비·ML 분류는 존재하나 의식 *수준/개수*가 아닌 상태 *전환/진단*을 측정. → IIT/Φ 가설로서는 ⚪ (정직하게: 이 클러스터에서 측정 불가능 판정).

> 가능한 재구성(미래): 단일 뇌 내 *동시* 다중 통합정보 코어 존재 = IIT **exclusion 공준** 위반 테스트. 단 in-vivo 측정 경로 부재.

---

## 3. S34 — 영아 의식 발달: 언제 의식/Φ가 발현하는가?

### 3.1 핵심 논문

| 인용 | 연도 | DOI / ID |
|------|------|----------|
| Kouider S, Stahlhut C, Gelskov SV, Barbosa LS, Dutat M, de Gardelle V, Christophe A, Dehaene S, Dehaene-Lambertz G. "A neural marker of perceptual consciousness in infants." *Science* 340(6130):376-380 | 2013 | **10.1126/science.1232509** · PMID 23599498 |
| (배경) Passos-Ferreira C. "Can we detect consciousness in newborn infants?" *Neuron* (review) | 2024 | DOI = `[Neuron review, S0896-6273(24)00285-X]` |

### 3.2 marker + 발현 연령

- **marker**: 의식적 접근(conscious access)의 **늦은 느린파(late slow wave)** — 성인 P3b(P300)의 비선형 "all-or-none" 서명에 대응. 자극 가시성 임계 부근에서 비선형적으로 출현(가시성 조작 = masking).
- **연령**: 영아 **5 / 12 / 15개월** 검사.
  - 5개월에도 의식적 접근 신경 서명 **존재하나 성인보다 훨씬 느리고 미성숙**.
  - 발달에 따라 잠복기 단축·성인-유사 성숙.
- (태아) 별도 MEG 연구: **재태 35주+ 태아에서 global oddball P300-유사 효과** 재현 보고 → 의식적 자극처리 가능성 시사(Neuron review 인용).
- **함의**: 지각적 의식의 신경 인프라가 생후 ~5개월에 이미 작동(느림). 의식 *발현 하한*이 영아기 초기 EEG marker로 측정 가능.

### 3.3 측정가능성 verdict — 🟡 (데이터 확보 시 🟢)

"의식 발현 시점"에 late-slow-wave라는 falsifiable EEG 지표 존재. **공개 영아 EEG 데이터 확보**(아래 §4)로 신경응답 검출 파이프라인 로컬 재현 가능. gap: Kouider 원논문 raw(masking oddball)는 공개 accession 미확인 → 발현*시점* 직접 재현엔 동일 패러다임 raw 필요.

---

## 4. 공개 다운로드 데이터셋

| 데이터셋 | 대상 | accession / DOI | 포맷 | 규모 | 가설 |
|----------|------|-----------------|------|------|------|
| **200 Objects Infants EEG** (Nature Sci Data 2025) | 영아 **42명, 2~12개월**, 200 객체이미지 rapid visual stream | OpenNeuro **ds005106** · **10.18112/OPENNEURO.DS005106.v1.5.0** · 논문 10.1038/s41597-025-04744-z | **BIDS** (raw EEG) | `[수GB, 페이지상 미명시]` | **S34** (영아 시각 신경응답 — 1순위) |
| **Neonatal EEG with seizure annotations** (Stevenson, Tapani, Lauronen, Vanhatalo, Sci Data 2019) | 만삭 신생아 **79명**, 19ch 10-20, 256Hz, 중앙 74min | Zenodo **10.5281/zenodo.4940267** (and .2547147) · 논문 10.1038/sdata.2019.39 | **EDF + CSV** | **4.3 GB** | S34 (신생아 EEG baseline·전처리) |
| **PCIcalc** | TMS-EEG PCI 계산 코드 | github.com/iTCf/PCIcalc | Python | code | S32 (PCI 재현 도구) |
| (참조) Casali/Casarotto DoC TMS-EEG raw | DoC 환자 | **공개 raw 미발견** (요청기반, Milano iTCf) | — | — | S32 (환자측 gap) |

> 신생아 데이터셋은 본래 *발작* 검출용(재태연령 정보 없음) → 의식 marker 직결은 아니나 신생아 EEG 처리·baseline엔 사용 가능. **S34 1순위는 OpenNeuro ds005106** (영아 시각 신경응답, BIDS 공개).

---

## 5. 최소 로컬 검증 파이프라인 (데이터 있는 곳)

### S34 — 영아 시각 신경응답 (ds005106, 즉시 가능)
1. OpenNeuro **ds005106** 다운로드 (BIDS, 영아 42명).
2. 전처리: filter → epoch (이미지 onset) → bad-channel/ICA.
3. ERP 평균 → **late component / slow wave** 검출 → 연령(2~12개월) 회귀로 잠복기 성숙 추적.
4. (확장) Kouider masking oddball raw 입수 시 의식적-접근 비선형 서명 직접 재현.
5. anima 측: LZ/복잡도 측도는 repo 내 LZ76 verdict 경로(`M4b rev2`) 재활용 가능.

### S32 — PCI 재현 (PCIcalc + 자체 TMS-EEG)
1. **PCIcalc** (iTCf) 설치.
2. TMS-EEG raw → artifact 제거 → epoch → source/sensor 시공간 행렬.
3. bootstrap 유의성 thresholding → binary 행렬 → **LZ76 복잡도** → 정규화 = PCI.
4. 검증: 각성 vs 무의식 조건에서 **PCI\* ≈ 0.31** 분리 재현. → anima `hexa verify`로 LZ76 closed-form 확인.
5. gap: DoC 환자 raw 비공개 → 건강 대조 wake/anesthesia raw로 대체 검증.

### S27 — 해당 없음
- Φ-proxy 미정의 + 공개 raw 부재 → 로컬 검증 불가. ⚪.

---

## 6. 양방향 sibling

- sibling: E2 cluster (S32·S27·S34) ↔ 다른 catalog 클러스터 (E1/E3 등) — `UNIVERSE/state/s_catalog_2026_05_29/` 하위 형제 .md
- SSOT link: `UNIVERSE/CANDIDATES.md` (S-축 가설 카탈로그) — 본 verdict 반영 필요
- 상위: `MATRIX.tape` 축 등록 (S32 = PCI 임상검증 🟡, S34 = 발달 marker 🟡, S27 = ⚪ 측정불가)

---

## 7. 정직성 footnote

- **fetch 성공·verbatim 확정**:
  - Casali 2013 — DOI·저자 전원·권호 (PMID 23946194, full citation fetched).
  - Casarotto 2016 — **PCI\*=0.31 / AUC 100% / sens 100% spec 100% / MCS 94.7% / VS 9-of-43 / 코호트 MCS38+VS43 / benchmark 150** = 4개 독립 검색 결과에서 일관 verbatim. 권호 80(5):718-729, DOI 10.1002/ana.24779, PMID 27717082.
  - Kouider 2013 — DOI 10.1126/science.1232509, 저자 전원, Science 340(6130):376-380, 5/12/15개월.
  - OpenNeuro ds005106 — DOI 10.18112/OPENNEURO.DS005106.v1.5.0, 영아 42명 2~12개월, BIDS (논문 10.1038/s41597-025-04744-z).
  - Zenodo 신생아셋 — DOI 10.5281/zenodo.4940267, 79명, 19ch, 4.3GB, EDF+CSV, CC-BY-4.0.
  - Reinders 2019 BJP DID 분류기 — DOI 10.1192/bjp.2018.255, **n=32 DID + 43 HC, sens 72% spec 74% AUC 0.74** (WebFetch verbatim).
  - Reinders 2014 PET (10.1016/j.pscychresns.2014.05.005) · Reinders&Veltman 2021 BJP editorial (10.1192/bjp.2020.168) · Schlumpf 2014 PLOS ONE (10.1371/journal.pone.0098795) — 모두 검색/Crossref 확정.
- **검증 실패 → 삭제한 항목 (조작 방지)**:
  - 초안의 "Dimitrova … Neuroimaging distinct identity states … Psych Med 53(7) DOI 10.1017/S0033291721005225 PMID 34244752" = **삭제**. PMID 34244752는 무관 논문(대장암)을 반환 → 신뢰 불가. 해당 DOI/권호는 어떤 소스에서도 확정 못 함.
- **검증됐으나 full-fetch 차단 → 근사 표기**:
  - Casali 2013 상태별 PCI *수치 구간* (full-text PDF 추출 차단) → `[수치구간 미확인]`.
- **조작·추정 없음**: 미확인 항목 전부 `[미확인]`/`[확인 필요]` 명시. CLAIMS.tape 등재 전 차단 항목 원문 1회 재확인 권장 (anima a_claim_verify 준수).
