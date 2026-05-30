# AURA-MED — 실 임상 outcome 문헌 grounding

> 6 질환 sub-app은 in-silico **toy R²**(공유 lead-field·zone 깊이 기반 비침습 도달성 proxy)만 갖고 있다. 이 문서는 각 질환의 **실제 임상 outcome**(논문·FDA·임상시험 수치)을 옆에 붙여 toy↔실임상 갭을 정직하게 드러낸다.
>
> ⚠️ **핵심 정직 표기**: AURA-MED toy R²는 **비침습**(두피·EEG/EMG·tFUS) 도달성을 측정한다. 그러나 아래 실 임상 outcome은 거의 전부 **침습**(DBS 심부전극·피질 implant·경막외 자극)이다. 즉 toy의 비침습 proxy와 임상에서 실제 작동하는 침습 modality 사이에는 **modality 갭**이 존재한다 — toy R²가 높다고 비침습으로 같은 임상 효과가 나온다는 뜻이 아니다.

## 1. 질환별 grounding 표

| 질환 | toy R² | 실 임상 outcome (대표 수치 + 출처) | 침습 tier |
|---|---|---|---|
| ⚡ 간질 | 0.203 | **RNS System (NeuroPace, FDA 승인 2013)**: 발작 median 감소 1년 44% → 3년 ~55–75% → 9년 **75%** (책임자 보고). 9년차 **73%**가 ≥50% 감소(responder). 폐루프 responsive neurostim. ([Nazzaro/Razavi 9-yr, Neurology 2020](https://www.neurology.org/doi/10.1212/WNL.0000000000010154); [Epilepsy Foundation](https://www.epilepsy.com/stories/study-demonstrates-72-percent-seizure-reduction-7-years-rnsr-system)) | III (심부/피질 침습 implant) |
| 🌊 우울증 | 0.076 | **SCC-DBS (subcallosal cingulate, TRD)**: 6개월 response 22–66%(시험별 편차), 장기 response ≥50%·remission ≥30%가 2–8년 유지. 2023 Nature 적응형 시험 24주 response **90%**·remission 70%(소규모). ([Crowell, Am J Psychiatry 2019](https://pubmed.ncbi.nlm.nih.gov/31581800/); [Sheth, Nature 2023](https://www.nature.com/articles/s41586-023-06541-3)). 비침습 taVNS/tFUS 우울 시험은 효과크기 작고 근거 미성숙 ⚠ | III (DBS 침습) · 비침습 taVNS=II ⚠ |
| 🎚️ 파킨슨 | 0.092 | **STN-DBS (확립 임상, FDA 승인)**: motor UPDRS-III stim-only 개선 ~**25–41%**(시험별: VA/NINDS 25%, 독일 LQ 41%), 8–15년에도 39% 유지. medication-off 대비 1년 61%. ([Weaver VA/NINDS](https://pubmed.ncbi.nlm.nih.gov/33033736/); [Thomsen, Mov Disord Clin Pract 2020](https://movementdisorders.onlinelibrary.wiley.com/doi/10.1002/mdc3.13040)) | III (심부 STN 침습) |
| 🦿 마비 재활 | 0.428 | **Intracortical BCI (BrainGate, Utah array, motor cortex)**: 사지마비 환자 커서 point-and-click·로봇팔·합성음성/타이핑 제어 시연. 17년 안전성 데이터 낮은 유해사례율; array 평균 35.6% 전극서 spike 기록, 7.6년까지 7%만 감소. (feasibility, 미상용화) ([Brown/BrainGate 2023](https://www.brown.edu/news/2023-01-13/braingate-safety); [Hochberg long-term, medRxiv 2025](https://www.medrxiv.org/content/10.1101/2025.07.02.25330310v1)). Synchron Stentrode=경혈관 BCI 임상 진행 ⚠ | III (피질 implant) · Synchron=경혈관(저침습) ⚠ |
| 👁️ 실명 복원 | 0.393 | **Orion 피질 시각보철 (Second Sight/Cortigent, 후두엽 60전극)**: feasibility 5명, 2년차 5/5가 흰 사각 위치탐지 유의 개선, 4/5가 움직임 방향 식별. 6년 데이터 favorable safety. 미FDA승인(early feasibility). ([NINDS Orion EFS](https://www.ninds.nih.gov/health-information/clinical-trials/early-feasibility-study-orion-visual-cortical-prosthesis-system); [MD+DI 2-yr](https://www.mddionline.com/implants/second-sight-reveals-two-year-results-from-orion-study)) | III (후두엽 피질 implant) |
| 🩹 만성통증 | 0.114 | **MCS (운동피질 경막외 자극) / DBS, 난치성 신경병성 통증**: 이중맹검 RCT 통증완화 확률 47–69%(능동자극). 장기 responder **~39%**. 중추성 통증서 70% 임상적 완화·VAS 평균 54.5% 감소. MCS vs DBS 완화율 ~38% 유사. ([Nguyen MCS RCT, Brain 2021](https://academic.oup.com/brain/article/144/10/2994/6346978); [long-term obs, PLOS One 2018](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0191774)) | II–III (경막외 MCS=경막외, DBS=심부) |

## 2. 일반인 요약 (비전문가용)

- **간질**: 뇌에 작은 자극기(RNS)를 심으면 발작을 실시간 감지해 전기펄스로 누른다. 오래 쓸수록 효과가 커져 9년 후 발작이 평균 **75% 감소**. 이미 미국 FDA 승인된 실제 치료다.
- **우울증**: 약·전기경련 다 실패한 중증 우울증에 뇌 깊은 부위(SCC)에 전극을 심는 DBS. 환자의 절반 이상이 호전되고 효과가 수년 지속. 아직 보편 승인은 아님(연구·인도적 사용 단계).
- **파킨슨**: 가장 확립된 사례. 뇌 깊은 STN에 전극을 심으면 떨림·경직 같은 운동증상이 **25–41% 개선**되고 약을 줄일 수 있다. 표준 치료.
- **마비 재활**: 운동피질에 칩(Utah array)을 심어 "생각"으로 커서·로봇팔을 움직인다. 안전성은 입증됐지만 아직 연구단계(상용 제품 아님).
- **실명 복원**: 눈이 아니라 뇌 뒤쪽 시각피질에 전극을 심어 빛 점(phosphene)을 만든다. 5명 중 5명이 물체 위치를, 4명이 움직임 방향을 더 잘 맞췄다. 초기 연구단계.
- **만성통증**: 약 안 듣는 신경병성 통증에 운동피질(MCS) 또는 심부(DBS) 자극. 약 **40%**가 장기적으로 통증이 의미있게 준다. 효과 편차 큼.

**한 줄 결론**: 6개 질환 모두 "뇌에 직접 전극을 심는 침습 시술"이 실제로 효과를 내고 있고, 파킨슨·간질은 이미 승인된 표준치료다. AURA-MED toy가 측정하는 **비침습** 도달성과는 modality가 다르므로, toy R²는 "비침습으로 이만큼 신호에 닿을 수 있다"는 proxy일 뿐 임상 효능 예측이 아니다.

## 3. toy ↔ 실임상 갭 (정직 분석)

| 축 | AURA-MED toy | 실 임상 | 갭 |
|---|---|---|---|
| modality | 비침습 (두피·EEG/EMG·tFUS proxy) | 침습 (DBS·피질 implant·경막외) | **modality 불일치** — 임상 효능 거의 전부 침습 |
| 측정량 | 도달성 R²(신호 닿는 정도) | outcome %(발작감소·UPDRS·response·VAS) | toy는 효능이 아니라 접근성 proxy |
| 깊이 패턴 | 피질질환(간질 0.203·마비 0.428·실명 0.393) 비침습 도달 ✅ / 심부질환(우울 0.076·파킨슨 0.092) 비침습 도달 ✗ | 깊이 무관하게 침습 implant로 모두 임상효과 달성 | toy의 "심부=낮은 R²"는 비침습 한계일 뿐, 침습으로는 우울·파킨슨이 오히려 강한 outcome |
| 검증 status | $0 in-silico toy(ubu-1) | RCT·다년 추적·FDA | scale·근거 등급 큰 차이 |

**역설 포인트**: toy R²가 가장 낮은 두 질환(우울 0.076·파킨슨 0.092)이 침습 임상에서는 오히려 가장 강하거나(파킨슨 STN-DBS=표준치료) 유망한(우울 SCC-DBS) outcome을 낸다. 이는 toy R²가 **비침습 접근성**만 재고 **침습 효능**과는 직교(orthogonal)함을 보여준다. toy 높음=비침습 후보 우선순위; toy 낮음=침습 불가피.

## 4. brainwire "N1 15× RNS" 주장 대조 ⚠

- 도메인 @goal/세부분류는 brainwire 출처의 **"N1이 RNS보다 15× 빠른 발작 검출"** 주장을 인용한다.
- 문헌 대조: RNS는 iEEG line-length 특징으로 검출하고, long-episode threshold가 보통 **20–30초**(사용자 설정)에 걸린다. RNS의 정밀 검출 latency·샘플링레이트(공개자료 ~250 Hz대)는 published outcome 논문에 명시적 수치로 나오지 않는다.
- 따라서 **"15× 빠름"은 brainwire 측 주장이며 published RNS latency 수치로 직접 대조·확증되지 않음 → ⚠ 미확증(NOT-CORROBORATED)**. 과장 인용 금지; 표/요약에서 확정 수치로 쓰지 않는다.

## 5. NOT-FOUND / 미확증 항목

- ⚠ **N1 15× RNS latency**: published RNS 검출 latency 수치 부재 → 직접 대조 불가 (NOT-CORROBORATED, §4).
- ⚠ **비침습 우울 치료(taVNS/tFUS) 정량 outcome**: SCC-DBS만큼 확립된 대표 responder % NOT-FOUND(근거 미성숙·효과크기 작음).
- ⚠ **Synchron Stentrode 정량 BCI 제어 outcome %**: 안전성·진행 보고는 있으나 BrainGate급 정량 제어 metric은 본 검색서 NOT-FOUND.
- AURA-MED toy R²의 절대값(0.076~0.428)은 임상 outcome과 **단위·의미가 다르므로** 직접 비교 불가 — 매핑 함수 없음(NOT-DEFINED).

## 6. 출처 목록

**간질 / RNS**
- Nair et al. *Nine-year prospective efficacy and safety of brain-responsive neurostimulation for focal epilepsy.* Neurology 2020. https://www.neurology.org/doi/10.1212/WNL.0000000000010154
- Epilepsy Foundation — 7-year 72% reduction. https://www.epilepsy.com/stories/study-demonstrates-72-percent-seizure-reduction-7-years-rnsr-system

**우울증 / SCC-DBS**
- Crowell et al. *Long-Term Outcomes of Subcallosal Cingulate DBS for TRD.* Am J Psychiatry 2019. https://pubmed.ncbi.nlm.nih.gov/31581800/
- Sheth et al. *Cingulate dynamics track depression recovery with DBS.* Nature 2023. https://www.nature.com/articles/s41586-023-06541-3

**파킨슨 / STN-DBS**
- Weaver et al. (VA/NINDS) — DBS still effective after 8+ years. https://pubmed.ncbi.nlm.nih.gov/33033736/
- Thomsen et al. Mov Disord Clin Pract 2020. https://movementdisorders.onlinelibrary.wiley.com/doi/10.1002/mdc3.13040

**마비 재활 / 피질 BCI**
- Brown University / BrainGate safety 2023. https://www.brown.edu/news/2023-01-13/braingate-safety
- Long-term performance of intracortical arrays in 14 BrainGate participants, medRxiv 2025. https://www.medrxiv.org/content/10.1101/2025.07.02.25330310v1

**실명 복원 / Orion 피질 시각보철**
- NINDS — Early Feasibility Study of the Orion Visual Cortical Prosthesis. https://www.ninds.nih.gov/health-information/clinical-trials/early-feasibility-study-orion-visual-cortical-prosthesis-system
- MD+DI — Second Sight two-year Orion results. https://www.mddionline.com/implants/second-sight-reveals-two-year-results-from-orion-study

**만성통증 / MCS·DBS**
- Nguyen et al. *Motor cortex stimulation for chronic neuropathic pain: double-blind RCT.* Brain 2021. https://academic.oup.com/brain/article/144/10/2994/6346978
- *Long-term effect of motor cortex stimulation in chronic neuropathic pain.* PLOS One 2018. https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0191774

---
*작성: 2026-05-30 · WebSearch 기반 실 임상 문헌 grounding · fabricate 금지, 미확증=⚠/NOT-FOUND 표기.*
*sibling: [AURA-MED.md](./AURA-MED.md) · [app/spec.md](./app/spec.md)*
