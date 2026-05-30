# AURA-TFUS — 문헌 closure (2 마일스톤)

> AURA-TFUS의 두 문헌 마일스톤을 실 출처로 grounding. tFUS는 AURA 읽기/쓰기 비대칭의 유일 비침습 심부 *write* 갈래 — 이 문서는 (1) 성인 비침습 음향-imaging(fUS read) 성숙도와 (2) tFUS 신경조절(write) 안전·심부 심도 한계를 문헌으로 닫는다. honest: 문헌 인용(2026-05-30 WebSearch), toy 측정 아님.

## 1. 성인 비침습 음향-imaging(fUS read) 성숙도

핵심 결론: **functional ultrasound imaging(fUS read)는 신생아·동물·개두창(craniotomy/craniectomy) 성인이 주력. 두개골 온전한 성인의 완전-비침습 경두개 fUS는 아직 미성숙 — 두개골 감쇠·수차가 본질 장벽.**

| 대상 | fUS read 가능성 | 근거 |
|---|---|---|
| 신생아 | ✅ 임상 가능 (천문 acoustic window) | 2D fUS bedside neonate 모니터 시연 |
| 동물(쥐/young rat) | ✅ 비침습 가능 (얇은 두개골) | freely-moving awake mice·anesthetized young rat transcranial fUS (무조영제). 단 노화·두개골 발달 시 다른 해법 필요 |
| 비인간 영장류(NHP) | ⚠ craniectomy 또는 ultrafast 기법 | 개두창 또는 in-depth ultrafast 접근 |
| 성인 인간 — 개두창/수술중 | ✅ 시연됨 | 종양 절제 수술 중 intraoperative fUS(두개골 제거 상태) |
| 성인 인간 — 두개골 온전 | ⚠ 미성숙 (조영제·acoustic-window·adaptive 필요) | microbubble 조영제 enhanced Doppler·polymeric skull-replacement acoustic window·adaptive transcranial Doppler 등 우회책 |

- **두개골 장벽 정량**: 15 MHz서 6.9 dB/cm 감쇠. 두개골은 multiple scattering·mode conversion·absorption·refraction로 transcranial 영상을 심하게 열화.
- **현 우회책**: 대부분 연구는 두개골 제거/thinning(임상 fUS/BMI 비호환). 비침습 대안 = ultrasound 조영제(microbubble) 또는 polymeric skull-replacement acoustic window(=implant·반-침습) 또는 adaptive aberration 보정.
- ⭐ AURA 정합: 성인 두개골 온전 비침습 fUS *read*는 여전히 미성숙 → C15 "읽기 벽"을 문헌이 뒷받침. fUS는 read보다 신생아/동물/개두창에 묶임.

출처:
- [Demené et al., transcranial fUS microbubble-enhanced ultrasensitive Doppler (NeuroImage / PMC4686564)](https://pmc.ncbi.nlm.nih.gov/articles/PMC4686564/)
- [Transcranial fUS in freely-moving awake mice & young rats, no contrast (PMC5754333)](https://pmc.ncbi.nlm.nih.gov/articles/PMC5754333/)
- [Non-invasive 4D transcranial fUS + ULM neurovascular imaging (PMC11697013)](https://pmc.ncbi.nlm.nih.gov/articles/PMC11697013/)
- [Functional ultrasound imaging of human brain activity — skull-replacement acoustic window (Caltech / scitranslmed.adj3143)](https://www.vis.caltech.edu/documents/28341/scitranslmed.adj3143.pdf)
- [Adaptive transcranial ultrasound Doppler imaging (bioRxiv 2025.05.27.656275)](https://www.biorxiv.org/content/10.1101/2025.05.27.656275.full.pdf)

## 2. 안전성·심부 심도 한계 (tFUS write)

핵심 결론: **tFUS 신경조절(write)은 ITRUSST/FDA 안전 한계 내에서 비침습 심부 도달 가능. 그러나 주파수-심도 tradeoff(저주파=깊지만 focal 큼)·두개골 감쇠/수차·열(Pennes bioheat)이 심부 도달의 본질 제약.**

### 2.1 안전 가이드 (ITRUSST 합의 + FDA)

| 항목 | 한계값 | 출처 |
|---|---|---|
| Mechanical Index (MI / MItc) | ≤ 1.9 | ITRUSST 합의 |
| 온도 상승 | < 2 ℃ | ITRUSST 열 안전 |
| 열 dose | < 0.25 CEM43 (cumulative equiv. min @43℃) | ITRUSST |
| 노출시간 (TI 기준) | TI≤2.0→80min · TI≤2.5→40min · TI≤3.0→10min | ITRUSST |
| FDA 진단초음파 ISPTA.derated | 0.720 mW/cm² (≈720 mW/cm²) | FDA diagnostic |
| FDA Isppa free-field | 190 W/cm² | FDA |
| FDA MI | 1.9 | FDA |

⚠ ITRUSST는 ISPTA를 thermal-dose·TI 대비 열등하다고 보아 열 안전 metric에서 **제외** (AIUM 결론 동조). 즉 현대 합의는 ISPTA 단독 한계보다 thermal dose/TI 기반.

### 2.2 심부 심도 한계 (주파수 tradeoff · 열)

- **주파수-심도 tradeoff**: 저주파(긴 파장)=두개골 투과·심부 도달 ↑, focal 해상도 ↓ / 고주파=focal 정밀 ↑, 두개골 감쇠 ↑. 뇌 자극은 통상 200–700 kHz (영상용 3–4 MHz보다 훨씬 낮음 — 경두개 투과 위해).
- **두개골 감쇠·수차**: 두개골 음향임피던스 > 뇌조직 → 도달 강도·에너지 감소, focal shift, thermal gain 감소. 이질적 두개골이 에너지 deposition 왜곡.
- **열(Pennes bioheat)**: Pennes 방정식(전도+대사열+혈류 perfusion 균형)으로 transcranial 온도 FDTD 모델링. 중심주파수↑ → 작용부위 온도↑ → 조직 열손상 위험. 두개골이 thermal hotspot이 되기 쉬움.
- ⭐ AURA 정합: tFUS는 음향이라 두개골 전기-LPF를 우회해 심부 *write*는 가능(C17 심부핵 신경조절)하나, 안전 한계·주파수 tradeoff·열이 "무한 심부 고해상" 을 막음. 비침습 심부 read 폐루프는 여전히 불가(C15).

출처:
- [ITRUSST consensus on biophysical safety for transcranial ultrasound stimulation (Brain Stimulation 2025 / S1935-861X(25)00353-5)](https://www.brainstimjrnl.com/article/S1935-861X(25)00353-5/fulltext) · [arXiv preprint 2311.05359](https://arxiv.org/pdf/2311.05359)
- [Panoramic review of tFUS neuromodulation: basic→clinical (PMC12570825)](https://pmc.ncbi.nlm.nih.gov/articles/PMC12570825/)
- [Safety of Clinical Ultrasound Neuromodulation (PMC9599299)](https://pmc.ncbi.nlm.nih.gov/articles/PMC9599299/)
- [Ultrasound system for precise neuromodulation of human deep brain circuits (Nat Commun 2025, s41467-025-63020-1)](https://www.nature.com/articles/s41467-025-63020-1)
- [Focused ultrasound heating in brain tissue/skull phantoms, 1 MHz single-element (PMC11178743)](https://pmc.ncbi.nlm.nih.gov/articles/PMC11178743/)
- [Full-wave acoustic + thermal modeling of transcranial US propagation, skull aberration (PMC4521448)](https://pmc.ncbi.nlm.nih.gov/articles/PMC4521448/)

## honest / 잔여

- 본 문서 = 문헌 인용(WebSearch 2026-05-30), in-silico toy 측정 아님. 절대 안전값은 device·montage·소스별 변동 — 실 적용 전 ITRUSST/IEC/FDA 원문 재확인 필요.
- external 잔여(닫지 않음): 실 fUS read 두개골-온전 성인 데이터 입수, 실 tFUS device 열 측정.

## sibling
- 도메인: [AURA-TFUS.md](./AURA-TFUS.md) · 깊이 벽: [C15-depth-wall-terminal.md](../C15-depth-wall-terminal.md) · 심부핵 역량: [C17-deep-nuclei-capability-map.md](../C17-deep-nuclei-capability-map.md) · 트리: [AURA-TREE.md](../AURA-TREE.md)
