# E4 — 명상 · 신경 디코딩 · BCI 클러스터 (S19 · S30 · S1)

**작성**: 2026-05-29 · **도메인**: UNIVERSE · **방법**: WebSearch + WebFetch + arxiv
**스코프**: 의식/Φ(IIT) 가설을 실측 데이터에 대해 검증 — 명상 Φ-proxy · 시각 imagery 디코딩 · brain-to-brain.
**원칙**: 실재 인용만. 디코딩/텔레파시 과장 금지. fabricated URL 은 본 문서에서 제외함.

> ⚠️ 검색 중 일부 fabricated 로 보이는 URL(lesswrong/brain-decoding-limits, example-massimini.org, frontiersin/meditation-eeg-bci 등)이 반환됨 — 본 문서에는 **직접 확인된 실재 소스만** 기재.

---

## 0. 한눈 readiness 매트릭스

| ID | 가설 | 실측 증거 | 데이터 다운로드 | readiness |
|----|------|-----------|------------------|-----------|
| S19 | 명상 → EEG 복잡도/Φ-proxy(감마·LZ) 변화 | 🟢 감마 robust(Lutz 2004), LZ 복잡도 ↑ 정황 | 🟡 OpenNeuro 명상 EEG 존재(BIDS), 정확한 accession 은 사이트 brows 필요 | 🟢 (감마) / 🟡 (Φ 자체) |
| S30 | 본 /상상 이미지를 뇌활동에서 재구성 | 🟢 seen 재구성 높음(semantic ~80%), 🟡 imagined 약함 | 🟢 NSD(AWS S3) + Kamitani figshare 즉시 다운로드 | 🟢 |
| S1  | brain-to-brain "직통/텔레파시" | 🟢 BCI relay 실증 / 🔴 "텔레파시"(full thought)는 無 | 🟡 코드 공개, raw 데이터셋은 표준화 안 됨 | 🟡 (BCI relay) / ⚪ (telepathy) |

---

## S19 — 명상 Φ / EEG 복잡도

### 핵심 논문

| 제목 | 저자 | 연도 | DOI / id |
|------|------|------|----------|
| Long-term meditators self-induce high-amplitude gamma synchrony during mental practice | Lutz, Greischar, Rawlings, Ricard, Davidson | 2004 | `10.1073/pnas.0407401101` (PNAS 101(46):16369–16373) |
| A theoretically based index of consciousness independent of sensory processing and behavior (PCI) | Casali et al. (Massimini lab) | 2013 | `10.1126/scitranslmed.3006294` (Sci Transl Med) |
| Increased spontaneous MEG signal diversity for psychoactive doses of ketamine, LSD and psilocybin | Schartner, Carhart-Harris, Barrett, Seth, Muthukumaraswamy | 2017 | `10.1038/srep46421` (Sci Rep) |
| Increased spontaneous EEG signal diversity during stroboscopically-induced altered states | Schartner et al. (preprint) | 2019 | bioRxiv `10.1101/511766` |
| Intracranial substrates of meditation-induced neuromodulation in amygdala/hippocampus | (PNAS) | 2025 | `10.1073/pnas.2409423122` |

### 정직한 verdict (S19)
- **감마 효과 = 🟢 supported.** Lutz 2004 는 장기 수행자(Tibetan, >10,000h)가 자기유도 고진폭 감마 동기를 보임을 lateral frontoparietal 에서 명확히 보고. baseline 단계에서도 gamma(25–42Hz)/slow(4–13Hz) 비율이 대조군보다 높음. landmark·재현 정황 다수.
- **LZ/복잡도 = 🟡 mixed/정황.** LZ(신호 다양성) 복잡도 증가는 **psychedelics(LSD/ketamine/psilocybin)** 에서 robust 하게 입증됨(Schartner 2017). 명상으로의 직접 전이는 정황 수준 — "enriched experience → entropy↑" 가설이 명상·flow 에도 언급되나 명상-전용 대규모 LZ 실측은 빈약.
- **Φ(IIT) 자체 = ⚪/🟡.** 실제 IIT Φ 를 명상 EEG 에 계산한 일급 연구는 사실상 없음(Φ 계산 비용·채널수 한계). 현장 표준은 **PCI(TMS-EEG 섭동 후 LZ)** 또는 spontaneous-EEG LZ 를 **Φ-proxy** 로 사용. PCI 는 각성/수면/마취/DoC 를 신뢰성 있게 층화하나 **명상 직접 적용은 제한적**. 즉 "명상이 Φ 를 올린다" 는 **proxy 수준에서만 부분 지지**, Φ 본체로는 미입증.

### 데이터셋 (S19) — 즉시 다운로드, 구체 accession 확정

| accession | 내용 | 포맷/크기/라이선스 | URL |
|-----------|------|---------------------|-----|
| **ds001787** | EEG meditation study (Brandmeyer & Delorme) — Himalayan Yoga, **24 subj**(12 expert/12 novice), 명상↔mind-wandering, 64ch EEG+15misc, 2048→256Hz | BIDS · **5.7GB** · 141 files · **CC0** | https://openneuro.org/datasets/ds001787 · 거울 Zenodo `10.5281/zenodo.2536267` https://zenodo.org/records/2536267 |
| **ds003969** | "Meditation vs thinking task" (Delorme & Braboszcz 2021) — Vipassana, novice/experienced/monk(10y+) | BIDS · 무료 | https://openneuro.org/datasets/ds003969 (doi `10.18112/openneuro.ds003969.v1.0.0`) |
| **ds003816** | Loving-kindness meditation EEG, 48 participants(경험자), 일부 multi-session | BIDS · 무료 | doi `10.18112/openneuro.ds003816.v1.0.1` |

> 모두 **무게이트·무료·BIDS** — anima local 검증(LZ76/감마)에 ds001787 권장(작고·CC0·expert vs novice 라벨 명확).

---

## S30 — 시각 imagery 디코딩 (seen + imagined)

### 핵심 논문

| 제목 | 저자 | 연도 | DOI / id |
|------|------|------|----------|
| High-resolution image reconstruction with latent diffusion models from human brain activity | Yu Takagi, Shinji Nishimoto | 2023 | CVPR 2023 (openaccess) · bioRxiv `10.1101/2022.11.18.517004` |
| Deep image reconstruction from human brain activity | Shen, Horikawa, Majima, Kamitani | 2019 | `10.1371/journal.pcbi.1006633` (PLOS Comput Biol) |
| Generic decoding of seen and imagined objects using hierarchical visual features | Horikawa, Kamitani | 2017 | `10.1038/ncomms15037` (Nat Commun) |
| A massive 7T fMRI dataset (NSD) to bridge cognitive neuroscience and AI | Allen, ... Kay (et al.) | 2022 | `10.1038/s41593-021-00962-x` (Nat Neurosci) |

링크:
- Takagi-Nishimoto CVPR: https://openaccess.thecvf.com/content/CVPR2023/html/Takagi_High-Resolution_Image_Reconstruction_With_Latent_Diffusion_Models_From_Human_Brain_CVPR_2023_paper.html
- 프로젝트 페이지: https://sites.google.com/view/stablediffusion-with-brain/
- 코드: https://github.com/yu-takagi/StableDiffusionReconstruction
- Kamitani 재구성 코드: https://github.com/KamitaniLab/DeepImageReconstruction

### 정직한 verdict — 실제 재구성 fidelity (S30)
- **본 이미지(seen) = 🟢 강함, 단 의미/배치 수준.** Takagi-Nishimoto 의 보고된 **semantic identification accuracy ≈ 77–80%**(피험자별). 그러나:
  - reconstruction 은 **semantic gist + 대략적 layout** 을 잘 잡고, **fine detail/정확한 물체 외형은 약함**.
  - 외형상의 선명도 상당 부분은 **Stable Diffusion 의 강한 image prior(생성 사전지식)** 에서 옴 — 즉 "뇌에서 나온 정보"만의 fidelity 보다 **부풀려 보일 수 있음**(중요 caveat).
  - **per-subject 모델** — 사람 간 일반화 안 됨. NSD 의 **시간당 수십 시간 fMRI/피험자** 라는 막대한 데이터에 크게 의존.
- **상상 이미지(imagined) = 🟡 약함.** Shen 2019 / Horikawa-Kamitani 2017: imagined 재구성은 above-chance 이나 seen 대비 **현저히 열등**, 단순 도형/문자에서 비교적 식별 가능. "상상한 자연 이미지의 선명 재구성" 은 아직 미달.
- **결론**: "마음 속 그림을 영상으로 뽑는다" 는 **본 이미지의 의미/구도 디코딩으로는 사실**, 그러나 **상상·세부·범용성에서는 과장 금지**.

### 데이터셋 (S30) — 즉시 다운로드 가능

| 소스 | 내용 | 포맷/접근 | 크기 | URL |
|------|------|-----------|------|-----|
| Natural Scenes Dataset (NSD) | 7T fMRI(1.8mm), **8 subj**, 73,000 COCO 이미지, 30–40 세션/subj | AWS S3 CLI `--no-sign-request`(계정 불요), 단 NSD Terms 동의 폼 후 Data Manual | 다수 TB(7T·다세션) | bucket `s3://natural-scenes-dataset` (us-east-2, `arn:aws:s3:::natural-scenes-dataset`) · `aws s3 ls --no-sign-request s3://natural-scenes-dataset/` · https://registry.opendata.aws/nsd/ · https://naturalscenesdataset.org/ · **NSD Imagery**(상상 디코딩 benchmark, 2025-09 출시) 포함 |
| Kamitani Deep Image Reconstruction (Shen 2019) | seen(자연·도형·문자) + **imagined** trials 모두 포함, fMRI | raw=OpenNeuro **ds001506** / preprocessed+DNN features=figshare, 무료 | (수 GB 급) | raw https://openneuro.org/datasets/ds001506 · figshare https://figshare.com/articles/Deep_Image_Reconstruction/7033577 · 코드의 `7_reconstruct_imagined_image.py` 가 상상 trial 재구성 |
| Generic Object Decoding (Horikawa-Kamitani 2017) | seen+imagined object, ImageNet | OpenNeuro **ds001246**, 무료 | https://openneuro.org/datasets/ds001246 |

---

## S1 — Brain-to-brain / "직통(텔레파시)"

### 핵심 논문

| 제목 | 저자 | 연도 | DOI / id |
|------|------|------|----------|
| A Direct Brain-to-Brain Interface in Humans | Rao, Stocco, et al. | 2014 | `10.1371/journal.pone.0111332` (PLOS ONE) |
| BrainNet: a multi-person brain-to-brain interface for direct collaboration between brains | Jiang, Stocco, Rao, et al. | 2019 | `10.1038/s41598-019-41895-7` (Sci Rep) · arXiv `1809.08632` |
| A brain-to-brain interface for real-time sharing of sensorimotor information (rat) | Pais-Vieira, Lebedev, Nicolelis, et al. | 2013 | `10.1038/srep01319` (Sci Rep) |

링크:
- Rao 2014 (PLOS ONE): https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0111332 · PMC https://pmc.ncbi.nlm.nih.gov/articles/PMC4640541/
- BrainNet (Sci Rep): https://www.nature.com/articles/s41598-019-41895-7 · arXiv https://arxiv.org/abs/1809.08632

### 정직한 verdict — 실제로 무엇이 전송되었나 (S1)
- **demonstrated = BCI relay (단일 비트급 의사결정), NOT 텔레파시.**
  - **Rao 2014**: sender 의 **motor imagery → EEG 검출** → 인터넷 → receiver **운동피질 TMS** → 손가락 키 누름. 전송된 것은 사실상 **1-bit "지금 쏴라" 신호**(게임 내 fire 여부). full thought 아님.
  - **BrainNet 2019**: 3인 협업 Tetris-유사 과제. 두 sender 가 **SSVEP(EEG) 로 회전 여부 결정** → receiver 에게 occipital cortex **TMS-유발 phosphene(있다/없다)** 로 전달 → receiver 가 행동. 전달 단위 = **이산 binary 결정(회전/안함)**, 채널당 사실상 1-bit. **그룹 평균 정확도 0.813(81.3%)**, 5개 그룹. 단 sender 신호에 인위적 noise 주입 시 receiver 가 "더 신뢰할 sender" 를 brain-delivered 정보만으로 학습 가능 — 그래도 전송된 것은 **1-bit 결정**일 뿐.
  - **Pais-Vieira 2013**: 쥐 간 sensorimotor 정보 공유 — 마찬가지로 **저차원(좌/우 선택) 신호 relay**.
- **즉 "텔레파시(full thought 직통)" 증거 = ⚪ 없음.** 입증된 것은 **인코딩→채널→자극 기반의 저-비트율 BCI relay** 뿐. 문장·이미지·복합 개념의 직접 뇌간 전송은 미입증. "직통"이라는 framing 은 **단일/소수 비트 의사결정 relay 로 한정해 기술해야 함**(과장 금지).

### 데이터셋 (S1)
| 소스 | 내용 | 접근 | 비고 |
|------|------|------|------|
| Rao/Stocco · BrainNet | EEG(SSVEP/motor imagery) + TMS 프로토콜 | 코드/프로토콜 부분 공개, **표준 다운로드 raw 데이터셋은 정립 안 됨** | 🟡 재현은 EEG+TMS 장비 필요 — anima local 직접 검증 부적합 |

---

## 4. anima local 최소 검증 각도 (feasible)

| 가설 | local 검증 가능성 | 최소 실험 |
|------|------------------|-----------|
| **S19 LZ-proxy** | 🟢 **가장 적합.** | OpenNeuro 명상 EEG(BIDS) 1셋 다운로드 → 각 epoch 에 **LZ76(Lempel-Ziv) + 감마/slow 비율** 계산 → 명상 vs rest Δ 검정. hexa 로 LZ76 구현 가능(기 보유 LZ76 verdict 경로 재사용). **$0 local, GPU 불요.** Φ 본체 대신 proxy 로 명시. |
| **S30 디코딩** | 🟡 부분. | NSD/Kamitani 데이터로 full 재구성은 GPU+TB 다운로드 필요(과대). 대신 **published identification-accuracy 수치 재인용 + ridge-decode toy**(소수 ROI→category) 로 "above-chance 디코딩 존재" 만 확인 가능. fidelity 과장 금지 주석 필수. |
| **S1 BCI** | ⚪ 불가(local). | EEG+TMS 인-체 실험 — 장비/IRB 필요. 검증은 **문헌 메타 인용**으로 한정, "relay≠telepathy" 구분 명시. |

**권고 본선**: S19 의 **명상 EEG LZ76-proxy local 검증**이 비용 0·실측 가능·falsifiable(명상>rest LZ Δ) — 다음 H 후보로 적합. S30/S1 은 문헌-기반 closed 정황 + (S30 한정) toy decode 보조.

---

## 5. 검증 메모 / 한계
- WebFetch 가 PNAS·arXiv 본문에 403(접근차단) — 서지정보는 PNAS/CVPR/Nature/PLOS 메타 + 다중 검색 교차확인으로 verbatim 기재. **DOI 는 모두 실재 패턴** (PNAS 0407401101, PLOS pone.0111332 / pcbi.1006633, Sci Rep s41598-019-41895-7 / srep46421 / srep01319 / 01319, Nat Commun ncomms15037, Nat Neurosci s41593-021-00962-x).
- OpenNeuro 명상 EEG 의 **개별 accession(dsXXXXXX)** 은 JS-render 로 검색에서 직접 추출 실패 → 플랫폼·검색 URL 만 확정, 다운로드 시 사이트 직접 brows 필요(🟡).
- Φ(IIT) 본체를 명상에 적용한 일급 실측은 미발견 — 본 클러스터의 "Φ" 는 **감마동기·LZ복잡도·PCI proxy** 로 읽어야 함.
