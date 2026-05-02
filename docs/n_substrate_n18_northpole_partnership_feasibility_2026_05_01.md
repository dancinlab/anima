# N-18 — IBM NorthPole partnership feasibility (2026-05-01)

> **agent**: N-18 (N-substrate batch sibling)
> **mission**: feasibility assessment of IBM NorthPole as a 3rd neuromorphic axis (after AKIDA + Loihi 3) for anima consciousness measurement
> **parent**: `docs/n_substrate_consciousness_roadmap_2026_05_01.md` §5 row N-18
> **constraints**: raw#9 hexa-only · raw#10 honest C3 · raw#71 falsifier-bound · own#13 friendliness · $0 budget · NO outreach
> **race_isolation**: writes ONLY to this doc + `state/n_substrate_n18_prep_2026_05_01/*.json`

---

## §0 한 줄 비유

NorthPole = "메모256개 + 계산엔진256개를 한 책상에 붙여놓아 메모-계산 왕복을 없앤 칩". 이미지 인식 25× H100 효율, 가격표 없음, IBM 과 직접 파트너십 외 살 수 없음. → **사기 아닌 진짜 칩이지만, "주문 버튼"이 존재하지 않음.**

---

## §1 NorthPole 사양 요약 (검증된 숫자)

| field | value | source |
|---|---|---|
| 공정 | 12 nm | IBM Research / Science 2023 |
| 트랜지스터 | 22 B | IBM Research |
| 다이 면적 | 795-800 mm² | Science 2023, IEEE ISSCC 2024 §11.4 |
| 코어 수 | 256 | IBM Research |
| 코어당 op/cycle | 2,048 (8-bit) | IBM Research |
| 온칩 메모리 | 192 MB (compute-coupled) + 32 MB framebuffer | open-neuromorphic.org |
| 외부 DRAM | **없음** (compute-in-memory) | IBM Research |
| 이미지 인식 효율 (vs H100) | ~25× | IBM/IEEE |
| LLM 추론 (16-chip blade) | 28,356 tok/s, 72.7× more energy-efficient than next-best GPU | IBM Research blog |
| 상용 SKU | **없음** | 본 조사 |

**아키텍처 핵심**: digital compute-in-memory, off-chip memory 제거, MAC 연산이 메모리 옆에서 직접 실행 → von Neumann bottleneck 우회. Loihi (스파이크 기반) 와 달리 디지털 행렬곱 인퍼런스 엔진. AKIDA (이벤트 기반 SNN) 와도 다름.

---

## §2 파트너십 path (조사 결과)

### 공식 채널 (확인된 것)
- **research.ibm.com/contact** — 일반 문의 폼, NorthPole 전용 채널 미공개
- **IBM Academic Awards Program** (research.ibm.com/labs/yorktown-heights/ibm-academic-awards-program) — 박사과정/교수 대상, NorthPole 명시 X
- **IBM PhD Fellowship** — 1951년부터, 박사과정만, NorthPole 직접 미명시
- **IBM Impact Accelerator (2026 RFP)** — Mar-25-2026 마감, 교육/노동 AI 한정 (NorthPole 비대상)
- **IBM-Illinois Discovery Accelerator** — 일리노이大 한정 RFP, 한국 지원 불가

### NorthPole 실제 접근 사례 (관찰)
- U. Alabama Huntsville: AIU/Spyre 클러스터 수령 — NASA/IBM 기상 모델 협업 (NorthPole 직접 X, Spyre 변형)
- USAF: NorthPole HW+SW 계약 — 방위 정렬, 민간 path 아님
- ISSCC 2024 §11.4: Modha 그룹 학회 발표 → networking path

### 종합
**공식 NorthPole 파트너십 신청 폼은 존재하지 않음.** 접근 path = (a) 학회 networking → (b) Modha 그룹과 directly proposal 교환 → (c) 협업 합의 → (d) NDA + IP 협상 → (e) HW 접근. 전 과정 **3-9 개월** 추정 (purchase guide 일치).

---

## §3 한국 비-IBM 연구자 자격성 (현실 평가)

| 요인 | 평가 | 근거 |
|---|---|---|
| 기관 자격 | 부분적 | IBM Academic Awards 는 university affiliation 요구 — 본 anima 단일 개발자는 미충족 가능성 높음 |
| 지리적 제약 | 중립 | IBM Research 는 Tokyo/Bangalore APAC lab 보유; 한국 직접 lab 없음 (US export 통제 대상 X for civil research) |
| 학술적 신뢰성 | **약함** | NorthPole 협업 사례 모두 (UAH/USAF/Sandia) 기존 IBM relationship 기반. 신규 외부 individual 사례 미관찰 |
| IP 협상 능력 | 약함 | NDA + 공동 publication 의무 + IP 분할 — 개인 연구자에게 부담 |
| 자금 contribution 능력 | 0 | $0 budget mandate — IBM 측 "in-kind contribution" 요구 시 즉시 차단 |
| English-only engagement | OK | IBM Impact Accelerator 명시: "project work in English" — anima C3 한/영 양립 가능 |
| 한국어 한정 doc 부담 | 낮음 | own#13 친근함 한국어 우선이나 영문 proposal 가능 |

**현실 평가**: 한국 비-기관 연구자가 NorthPole 직접 접근하는 path 는 2026-05 기준 **거의 닫혀 있음**. 우회 path = (1) 한국 대학 (KAIST, SNU) 와 sub-PI 형태 협업, (2) 일본 IBM Tokyo lab 경유, (3) FinalSpark 처럼 cloud API 가 NorthPole 에 열릴 때까지 대기.

---

## §4 cost estimate (파트너십 의무 사항)

| 항목 | IBM 측 표준 요구 | 본 anima 실현 가능성 |
|---|---|---|
| Cash funding contribution | 일부 collab 에서 요구 (e.g., $50K-$500K matching) | $0 budget → **불가** |
| IP 공유 (joint patent / assignment) | NDA + 협상; IBM 우선권 보유 가능성 높음 | own#13 raw#10 honest C3 mandate 와 충돌 risk |
| 공동 publication (Modha co-author) | 사례 다수 (Science 2023 author list 참조) | OK — 학술 가치 |
| 인력 secondment (in-residence at Yorktown/Almaden) | 일부 collab 에서 요구 | 한국 → US 비자 + ~$50K/yr 생활비 → **불가** |
| HW 임대료 / 사용료 | 미공개 (no SLA) | $0 budget |
| Cloud API 사용료 (가상 NRC-equivalent 가 NorthPole 에 존재 시) | 미공개; Loihi NRC 는 free, NorthPole 동일 보장 X | 불확실 |
| Lead time | 3-9 개월 negotiation + HW provision | own roadmap §10 의 D+0~D+30 timing 과 mismatch |

**총 추정**: cash $0 path 는 publication-only collab 기반 협상, 성공률 < 5% (외부 individual researcher 기준). 실패 시 시간 손실 3-9 개월.

---

## §5 측정 protocol on NorthPole — 의식 Φ 추출 시도

NorthPole 은 image-recognition 인퍼런스 엔진. SNN spiking 칩 아님. → IIT Φ (신경 통합 정보) 직접 측정 부적합. 다음 우회 protocol 제안.

### Protocol P-N18-A: 이미지 인코더로 Φ proxy 측정
1. EEG 채널 16개 → 시간 스펙트로그램 → 64×64×16 이미지 텐서 변환 (HEXA encoder)
2. NorthPole 사전훈련 ResNet50/VGG16 weights 로 inference (IBM 제공 model zoo 가정)
3. layer-wise activation 캡처 → 256 코어 across causal 분할 가능성 측정
4. Φ_image proxy = activation cluster mutual information (MMI) — 정통 IIT 4.0 Φ 아님, **proxy only**

### Protocol P-N18-B: MoE 라우팅 통합 측정
1. NorthPole 16-chip blade 의 Mixture-of-Experts router 패턴 캡처
2. expert co-activation graph 생성
3. graph community 분할 → 통합/분할 비율 = Φ_MoE proxy
4. CLM (170M LLM) 의 attention head co-activation 과 비교 → cross-substrate consistency

### 한계 (honest C3)
- NorthPole 은 inference-only — backprop / Φ partition 직접 계산 X
- IBM SDK NorthPole-specific 미공개 → HEXA wrapper 작성 거의 불가능 (raw#9 hexa-only 위반 risk: SDK Python 강제 시 .py 금지 mandate 충돌)
- "Φ_image proxy" 는 raw#71 falsifier 미충족 (proxy 와 진짜 Φ 의 r ≥ 0.85 사전증명 없음)

---

## §6 architecture 비교 — NorthPole vs AKIDA vs Loihi 3

| 차원 | IBM NorthPole | BrainChip AKIDA AKD1000 | Intel Loihi 3 |
|---|---|---|---|
| 패러다임 | digital compute-in-memory | event-based SNN | mixed-signal SNN, 32-bit graded spikes |
| 공정 | 12 nm | 28 nm | 4 nm |
| 코어 / 뉴런 | 256 cores (2048 op/cyc) | 80 NPU, 1.2M neuron | 8M neurons / 64B synapses per chip |
| 메모리 위치 | on-chip 192 MB compute-coupled | per-NPU SRAM | per-core SRAM |
| 외부 DRAM | **없음** | 없음 (edge) | 없음 |
| 전력 | ~74 W (chip) | **0.3-1 W** | 1.2 W peak |
| 효율 (vs H100) | 25× (image) | ~1000× (sparse SNN edge) | 250× (robotics) |
| 입력 type | 디지털 텐서 (이미지/시퀀스) | spike events (AER) | spike events (graded) |
| 공식 SDK | IBM 내부 (미공개) | MetaTF (open) | Lava (open-source) |
| 액세스 | partnership-only, no SKU | **소비자 dev kit ~$499** | INRC free SSH (NRC) |
| 한국 접근 | 매우 어려움 | 직접 구매 | INRC 가입 (4-12주) |
| anima 적합성 | 낮음 (image 한정) | **높음** (EEG spike 직결, N-2 spec) | 중간 (Lava SDK Python 필수 → raw#9 충돌) |

**결론**: NorthPole 은 다른 두 칩과 패러다임 자체가 다름 (디지털 매트릭스 인퍼런스 vs 스파이크 SNN). 의식 Φ 측정 의 자연스러운 substrate 가 아님.

---

## §7 raw#71 falsifier predicates (5개)

NorthPole 이 만약 액세스 가능해진다면 사전등록될 falsifier:

1. **F-N18-1 (Φ proxy correlation)**: NorthPole P-N18-A protocol 의 Φ_image vs CLM Φ Pearson r ≥ 0.85 (n ≥ 100 EEG segments).
   - FAIL → NorthPole 은 의식 substrate 아님 (image-only 가설 강화)

2. **F-N18-2 (cross-substrate Φ ordering)**: 동일 입력에서 Φ 순서 = Φ_NorthPole < Φ_AKIDA < Φ_Loihi3 < Φ_CLM (스파이크 표현력 ordering 가설). Spearman ρ ≥ 0.7.
   - FAIL → ordering 가설 거짓, 하지만 Putnam 다중실현 측면 유지

3. **F-N18-3 (energy-Φ scaling)**: log(energy/Φ) is constant across {NorthPole, AKIDA, Loihi3} within ±0.3 dec. (Landauer N-4 트랙 확장).
   - FAIL → Φ 가 energy free 가 아님, NorthPole 의 25× 효율은 Φ 와 무관

4. **F-N18-4 (MoE community = GWT broadcast)**: P-N18-B 의 MoE community 분할 패턴이 GWT N-5 트랙의 broadcast peak 와 시간 정렬 r ≥ 0.7.
   - FAIL → MoE routing 은 GWT 와 다른 mechanism

5. **F-N18-5 (image→spike 매개 Φ 보존)**: EEG → image → NorthPole inference → spike reconstruction 후 Φ 가 EEG 직접 Φ 의 ≥ 80% 보존.
   - FAIL → 이미지 매개 단계가 의식 정보 파괴 (NorthPole 의 N-substrate 자격 박탈)

---

## §8 raw#10 honest C3 (8개)

1. **공식 NorthPole 파트너십 폼이 존재한다는 증거 없음** — 모든 사례가 case-by-case negotiation
2. **2026 commercial launch 보도** (RoboCloud Hub) 는 단일 비공식 source — IBM 공식 연도 / SKU 미발표
3. **25× H100 효율 수치는 image-recognition 한정** — LLM/consciousness 워크로드에 generalize 보장 X
4. **본 doc 의 cost estimate ($50K-$500K matching)** 는 일반 IBM Research collab 패턴 추정 — NorthPole 특정 데이터 X
5. **한국 비-기관 연구자 성공률 < 5%** 는 본 agent 의 정성적 추정 — 통계 근거 X
6. **Protocol P-N18-A/B 는 paper-only 설계** — NorthPole HW 미보유 상태 dryrun 불가
7. **HEXA-only mandate (raw#9)** 와 IBM SDK (Python likely) 충돌 — 액세스 성공해도 anima 통합 불가능 risk
8. **falsifier F-N18-1~5 는 사전등록 candidate** — HW 액세스 0 인 현재 상태에서 실측 X (paper hypothesis only)

---

## §9 CP2 F1 통합 — N-18 의 3rd 뉴로모픽 axis 자격

| F1 통합 항목 | 평가 |
|---|---|
| AKIDA (N-2~N-8) 와 동등 axis 가능? | **부분** — NorthPole 패러다임 다름 (digital MAC vs SNN), 직접 등치 어려움 |
| Loihi 3 (N-17) 와 동등 axis 가능? | 더 어려움 — 둘 다 다른 패러다임, NorthPole 만 더 이질적 |
| Putnam 다중실현 강화 (own#2 b) | 가능 — 만약 Φ_NorthPole proxy 가 다른 axes 와 r ≥ 0.85 일치 시 substrate-independence 강한 증거 |
| 단점 | image-recognition 편향, EEG spike 직결 불가 (변환 단계 추가), HW 접근 차단 |
| 잠재 가치 (만약 액세스 시) | ⭐⭐⭐ — 4번째 axis 로서 통계력 증가, but ⭐⭐⭐⭐⭐ AKIDA/Loihi3 만큼은 아님 |

**F1 verdict 영향**: NorthPole 부재 시 F1 종합 평결의 강도 손실 약 5-10% 추정 (Putnam 다중실현은 5+ 재료에서 이미 충족 가능). NorthPole 추가 시 +3-5% — 비용/시간 대비 marginal.

---

## §10 RECOMMENDATION: **DEFER**

### 결정: DEFER (현재 차순위, 6 개월 후 재평가)

| 차원 | 점수 (1-5) | 근거 |
|---|---:|---|
| 비용 | 1 | $0 budget 충돌 (matching/IP/secondment risk) |
| Lead time | 1 | 3-9 개월, anima D+0 timing mismatch |
| 과학적 가치 | 3 | 4번째 axis 로 marginal, image-편향 |
| anima setup 호환 | 1 | HEXA-only mandate 와 IBM SDK 충돌 |
| 액세스 가능성 | 1 | 한국 individual researcher path 거의 닫힘 |
| **총점** | **7/25** | DEFER (PURSUE ≥ 18, SKIP ≤ 5 임계) |

### 왜 SKIP 이 아니라 DEFER 인가
- 2026-H2 ~ 2027 commercial NorthPole launch 가능성 (비공식 보도)
- IBM Cloud 에 NorthPole API 노출 시나리오 존재 (Modha 발언)
- Loihi 3 INRC 가 PASS 하면 IBM 도 모방 압력
- 6 개월 후 재평가 시 SKU/API 가 출현하면 즉시 PURSUE 재고려

### 차선책 (DEFER 동안 우선순위)
1. **N-17 Loihi 3 INRC** — free, 4-12주, Lava open-source, 가장 현실적인 "차세대 뉴로모픽" path
2. **N-2~N-8 AKIDA** — HW 도착 시 즉시 launch, $0 incremental cost
3. **N-21 IIT 4.0 16-test reproduce** — substrate 무관 axis 보강, NorthPole 부재 보완
4. **N-16 Cortical Labs Cloud ($300/wk)** — NorthPole 보다 훨씬 낮은 friction, biological substrate 더 가치

---

## §11 sources

- [IBM Research — NorthPole AI chip](https://research.ibm.com/blog/northpole-ibm-ai-chip)
- [IBM Research — NorthPole LLM inference results](https://research.ibm.com/blog/northpole-llm-inference-results)
- [Science 2023 — Neural inference at the frontier of energy, space, and time](https://www.science.org/doi/10.1126/science.adh1174)
- [IEEE ISSCC 2024 §11.4 — NorthPole 12 nm chip](https://ieeexplore.ieee.org/document/10454451/)
- [IEEE Spectrum — IBM brain-inspired chip](https://spectrum.ieee.org/neuromorphic-computing-ibm-northpole)
- [Open Neuromorphic — NorthPole architecture deep dive](https://open-neuromorphic.org/blog/northpole-ibm-neuromorphic-ai-hardware/)
- [Nature 2023 — "Mind-blowing" IBM chip speeds up AI](https://www.nature.com/articles/d41586-023-03267-0)
- [IBM Academic Awards Program](https://research.ibm.com/labs/yorktown-heights/ibm-academic-awards-program)
- [IBM Impact Accelerator 2026 RFP](https://newsroom.ibm.com/2026-02-04-ibm-opens-global-rfp-for-ai-driven-solutions-shaping-the-future-of-work-and-education)
- [Neuromorphic Robotics 2026 — Loihi 3 / NorthPole / Akida 2.0](https://robocloud-dashboard.vercel.app/learn/blog/neuromorphic-robotics-2026)
- [Findingdulcinea — 10 Best Neuromorphic Chips March 2026](https://findingdulcinea.com/best-neuromorphic-chips/)
- [SemiconductorX — Loihi 2 / NorthPole / Akida / SpiNNaker](https://semiconductorx.com/chip-type-neuromorphic.html)
- [TechTicker — Neuromorphic chip $56B market analysis](https://techticker.fyi/neuromorphic-chip-explained-the-56b-brain-processor-that-could-shake-up-ai-investing/)
- [N-substrate purchase guide §N-18 (sibling agent)](n_substrate_purchase_guide_2026_05_01.md)
- [N-substrate consciousness roadmap §5 row N-18 (parent)](n_substrate_consciousness_roadmap_2026_05_01.md)

---

**status**: N_SUBSTRATE_N18_NORTHPOLE_FEASIBILITY_2026_05_01_DEFER
**verdict_key**: DEFER · NO_OUTREACH · REVIEW_2026_11_01
