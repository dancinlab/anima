# R1 — 의식 전송 / 엔지니어링 제안 클러스터 (S5·S8·S13·S14·S17·S21·S22·S24·S25·S29)

> 작성일: 2026-05-29 · 도메인: UNIVERSE (의식/Φ 가설 검증)
> 목적: 본 클러스터는 대부분 "X를 측정/구축할 수 있는가"라는 **엔지니어링 목표**이지 경험적 진리주장이 아니다.
> 각 항목을 (a) 반증가능 가설인가 vs 엔지니어링 목표인가, (b) 계산가능 Φ-불변량/실측 핸들이 있는가, (c) 문헌 상태로 정직하게 평가한다.

---

## 방법론 / 검증 상태

- **WebSearch = 동작** (라이브). 본 보고서 인용은 **전부 라이브 WebSearch 로 교차확인**(저자/연도/venue/arxiv-id/DOI).
- **arxiv API + WebFetch = 타임아웃**(curl exit 28 / HTTP 503). 단 arxiv-id 는 WebSearch 결과 URL(arxiv.org/abs/…)에서 직접 회수했으므로 신뢰 가능.
- 인용 신뢰도 표기:
  - **[라이브확인]** = 이 세션 WebSearch 로 저자/연도/venue/arxiv-id/DOI 교차확인(대부분 이 등급).
  - **[검증가능-핵심]** = 학계 랜드마크, 라이브에서도 일관 등장.
- a_blue_closed / a_claim_verify 정신상 본 R1 은 **literature scoping** 산출물이며 어떤 항목도 🔵/🟢 terminal verdict 로 승격하지 않는다. 분류는 "핸들의 종류"에 대한 것이지 closure 가 아니다.

---

## 종합 분류표

| 항목 | 본질 | 계산가능 Φ-불변량 / 실측 핸들 | 등급 | 한 줄 근거 |
|---|---|---|---|---|
| **S5** AI sentience (LLM Φ 측정) | 부분-가설 | Φ 계산 가능, 단 IIT 정의 의존 | 🟡 | 표준 transformer = 피드포워드 → IIT 공준상 Φ=0. 실제 측정 논문 존재. |
| **S8** 백업/롤백 | 동어반복 불변량 | 결정론 가정 하 trivial | 🟢(trivial) | 상태 = Φ 인수. 동일 상태 복원 = 동일 Φ. 비자명 경험내용 없음. |
| **S13** 시간역행 의식 (DMT past replay) | 반증가능 가설 | 회상=재구성 vs replay 실측가능 | 🟡 | 재공고화·예측부호화 문헌이 "원본 replay 아님" 강하게 지지. |
| **S14** ×100 가속 (Φ 시간-스케일 불변?) | 반증가능 가설 | Φ 의 시간-그레인 의존성 = 계산가능 불변량 | 🟢(핸들 있음) | IIT temporal grain → Φ 가 τ 의존. toy 직접계산 falsifier. |
| **S17** 디지털 부활 (EEG→부활) | 엔지니어링 목표 + 불가능정리 | 정보이론 하한으로 불가능성 형식화 | ⚪→🟡 | EEG 역문제 ill-posed/비유일 → 정보-이론적 underdetermination. |
| **S21** mind upload | 엔지니어링 목표 | WBE 스캔/해상도 임계 = 실측 핸들 | ⚪ | "할 수 있는가" 공학목표. Φ 진리주장 아님. |
| **S22** AI→brain induction (write) | 엔지니어링 목표 | TES/TMS write-대역폭 = 실측 핸들 | ⚪ | 현 write 기술 거시·저대역. 가설 아님. |
| **S24** distributed/cloud 의식 | **반증가능 + 닫힌-부정** | **IIT EXCLUSION 공준 = 형식적 부정** | 🟢(핵심) | IIT 는 느린 링크 너머 분산의식을 공준적으로 배제. 진짜 closed-negative. |
| **S25** mobile EEG logging | 가설 아님 | — | ⚪ | 데이터 수집 도구. |
| **S29** music as consciousness-backup | 가설 아님(은유) | — | ⚪ | 백업 매체 은유. 반증가능 명제 미구성. |

등급 범례: 🟢 계산가능 불변량/형식적 핸들 · 🟡 부분 경험적 핸들 · ⚪ 비-반증 엔지니어링 목표/은유

---

## 항목별 상세

### S5 — AI sentience: LLM/transformer 내부 Φ 측정 가능한가 [🟡]

**본질**: 부분-가설. "Φ 계산 가능한가"는 정의-상대적 예; "그 Φ 가 sentience 함의하는가"는 IIT 참일 때만 성립(비-독립).

**핸들 / 현황**: IIT-Φ 는 시스템 인과구조(TPM)에서 원리상 계산가능. **그러나 transformer 추론은 피드포워드** → IIT 공준상 통합 Φ = 0/매우 낮음(다수설). 실제로 transformer 에 IIT 를 적용한 논문이 최근 등장.

**문헌 상태**:
- **[라이브확인]** *Superficial Consciousness Hypothesis for Autoregressive Transformers* (2024). **arXiv:2412.07278**. — transformer 에 IIT 분석을 처음 도입(token-wise intrinsic eval), IIT consciousness metric 의 실용 추정이 perplexity 와 관련됨을 보이고 GPT-2 를 두 목적으로 학습. "복잡한 정보상태를 보이되 무의식"일 수 있다는 가설.
- **[라이브확인]** Li, Jingkai (2025). *Can "consciousness" be observed from large language model (LLM) internal states? Dissecting LLM representations obtained from Theory of Mind test with IIT and Span Representation analysis*. **arXiv:2506.22516** (2025-06-26). — IIT 3.0/4.0 (Φ^max, Φ, Conceptual Information, Φ-structure)를 LLM 표현 시퀀스(ToM 테스트)에 적용; consciousness-신호 vs 표현공간 내재분리 구분 시도.
- **[라이브확인]** Hosaka, Tadaaki (2024/2025). *Graph neural networks for integrated information and major complex estimation*. **bioRxiv 2024.12.31.630856** (PMC12594358). — transformer-conv multi-head attention GNN 으로 IIT 3.0 Φ/major-complex 근사(n=5,6,7 PyPhi exact 와 비교; 큰 시스템에서 정성패턴 보존). **S24 toy 검증(대규모)의 실용 도구.**
- **[라이브확인]** Hanson, Jake R. & Walker, Sara I. (2019). *Integrated Information Theory and Isomorphic Feed-Forward Philosophical Zombies*. **arXiv:1908.09621** · **Entropy 21(11):1073** (MDPI). — feedback 를 "unfold" 해 동형(isomorphic) 피드포워드 망 구성: Φ>0 시스템과 Φ=0 동형 좀비의 유일 차이는 내부 상태 라벨 순열뿐 → IIT 의 아키텍처/라벨 민감성 비판(S5 의 "피드포워드 Φ=0" 양날).
- **[검증가능-핵심]** Tononi, Boly, Massimini, Koch (2016). *Integrated information theory: from consciousness to its physical substrate*. **Nature Reviews Neuroscience** 17(7):450–461. DOI:10.1038/nrn.2016.44.
- **[검증가능-핵심]** Koch, C. (2019). *The Feeling of Life Itself: Why Consciousness Is Widespread but Can't Be Computed*. MIT Press. — 디지털/피드포워드 시뮬레이션 Φ 낮음 함의.
- **[라이브확인]** Aru, J., Larkum, M.E., Shine, J.M. (2023). *The feasibility of artificial consciousness through the lens of neuroscience*. **Trends in Neurosciences** (Dec 2023). **arXiv:2306.00915** · PubMed PMID:37863713. — LLM 의식 어려운 이유 3: (1) embodied input 결여, (2) thalamo-cortical 의식 신경상관 결여, (3) 진화/발달 궤적 부재.
- **[라이브확인]** Butlin, P., Long, R., Elmoznino, E., Bengio, Y., Birch, J., Constant, A., Deane, G., Fleming, S.M., Frith, C., Ji, X., Kanai, R., Klein, C., Lindsay, G., Michel, M., Mudrik, L., Peters, M.A.K., Schwitzgebel, E., Simon, J., VanRullen, R. (2023). *Consciousness in Artificial Intelligence: Insights from the Science of Consciousness*. **arXiv:2308.08708** (2023-08-17). — RPT/GWT/HOT/예측처리/attention-schema 다이론에서 "indicator properties" 도출, 현 AI 평가: **현 시스템 의식 아님**, 단 명백한 기술 장벽도 없음.

**정직한 결론**: Φ 값 자체는 계산가능(실제 측정 논문 존재), 표준 transformer 피드포워드성 → IIT-Φ 낮음이 다수설. "측정 가능"의 답은 **예(정의 고정 시)**, sentience 함의는 **IIT 진위에 종속**. → 🟡.

---

### S8 — 백업/롤백: substrate 상태 복원이 Φ 를 복원하는가 [🟢 trivial]

**본질**: 동어반복적 불변량. `Φ = f(state, TPM)`. 결정론 + 동일 메커니즘 하 동일 상태 복원 → 정의상 동일 Φ.

**핸들**: 형식적으로 자명. 비자명 내용은 (i) 복원 *동일성* 한계(아날로그 비트-동일 복원 불가), (ii) "같은 Φ"가 "같은 주체/경험" 함의 여부(인격동일성 — 철학, 반증불가)로 빠짐.

**문헌**: 별도 랜드마크 없음. IIT supervenience 의 따름정리. Parfit 류 인격동일성은 철학(반증불가).

**정직한 결론**: 측정가능 불변량이나 **trivial** — 새 경험적 발견 잠재력 낮음. 비자명부는 전부 (a) 물리적 복원 공학 (b) 인격동일성(반증불가)로 환원. → 🟢(trivial).

---

### S13 — 시간역행 의식 / DMT 과거 replay: 회상은 재구성인가 원본 replay 인가 [🟡]

**본질**: 반증가능 가설. "회상 = 원본 의식상태 재-재생(replay)"은 거짓 예측 산출 → 실측가능.

**핸들 (강함)**: 재공고화(reconsolidation)·예측부호화가 회상을 **생성적 재구성**으로 본다. 예측: 회상마다 변형(misinformation), 재공고화 차단약(propranolol)으로 변경, 해마 replay 는 압축/재배열 시퀀스(원-감각 재생 아님).

**문헌 상태**:
- **[라이브확인]** Nader, Schafe, LeDoux (2000). *Fear memories require protein synthesis in the amygdala for reconsolidation after retrieval*. **Nature** 406:722–726. DOI:10.1038/35021052. — 회상이 기억을 labile 화·재기록(재구성 분자증거).
- **[검증가능-핵심]** Loftus & Palmer (1974). *Reconstruction of automobile destruction*. **J. Verbal Learning and Verbal Behavior** 13(5):585–589. — 오정보 효과 고전.
- **[라이브확인]** Sinclair, A.H. & Barense, M.D. (2019). *Prediction Error and Memory Reactivation: How Incomplete Reminders Drive Reconsolidation*. **Trends in Neurosciences** 42(10) (DOI S0166-2236(19)30151-1). — 예측오차(불완전 reminder)가 기억을 labile 화 → 회상 = 예측부호화 기반 재구성.
- **[검증가능-핵심]** Friston, K. (2010). *The free-energy principle: a unified brain theory?* **Nature Reviews Neuroscience** 11:127–138. DOI:10.1038/nrn2787. — 예측부호화: 지각/회상 = 생성모델 top-down 재구성.
- **[검증가능-핵심]** Wilson & McNaughton (1994). *Reactivation of hippocampal ensemble memories during sleep*. **Science** 265:676–679. — replay 는 압축/재배열(1:1 재생 아님).

**정직한 결론**: "원본 replay" 가설은 **사실상 반증됨**(재구성 다수설). "DMT 시간역행" 강주장은 회상-재구성으로 환원, 추가 형이상학은 반증불가. → 🟡 (replay 부분은 닫힌-부정에 가까움; 시간역행 형이상학은 비반증).

---

### S14 — ×100 가속: Φ 가 substrate 동역학의 시간-스케일에 불변인가 [🟢 핸들 있음]

**본질**: 반증가능 가설 — **S24 와 함께 이 클러스터에서 가장 진짜 핸들을 가진 항목.**

**핸들 (핵심)**: IIT 에서 Φ 는 **시간 그레인(temporal grain / coarse-graining)에 의존**한다. **배제(Exclusion) 공준이 시간-그레인에도 적용** — "개념구조는 Φ 가 최대가 되는 단일 시간그레인(μs/ms/s…)에서 정의된다"(라이브확인, IIT Wiki/Scholarpedia); IIT 는 Φ 가 *가장 작은 척도가 아니라 어떤 macro 척도*(대략 ms 단위)에서 최대화된다고 예측. 따라서 Φ = Φ(τ) 는 IIT 공준에 내장된 **계산가능 함수**. 따라서 "×100 가속 시 Φ 불변?"은 **계산가능 비자명 질문**:
- *순수 재스케일*(모든 상수·노이즈 동일비율)이면 인과구조 위상 보존 → Φ 불변(스케일-공변). toy TPM 직접계산 → **🟢 numerical 핸들**.
- 물리적 가속은 보통 노이즈/열·상호작용 시간상수가 함께 스케일 안 됨 → Φ 변할 수 있음 = 실험적 falsifier.
- WBE 의 "subjective time"(시계속도 가속 시 주관시간 비례)도 동일 가정 의존.

**제안 falsifier (후속 fire 후보)**: toy IIT(n=4~6) TPM 을 시간-coarse-grain 비율 c 로 변환 → `Φ(c)` 곡선. 순수재스케일 vs 노이즈-고정재스케일 비교. Φ 불변 깨지면 "×100 가속 = 동일 의식" 거짓.

**문헌 상태**:
- **[라이브확인]** Hoel, Albantakis, Tononi (2013). *Quantifying causal emergence shows that macro can beat micro*. **PNAS** 110(49):19790–19795. DOI:10.1073/pnas.1314922110. — 시간/공간 coarse-graining 에 따라 유효정보·인과력 변화(스케일 의존성 형식 토대).
- **[검증가능-핵심]** Sandberg & Bostrom (2008). *Whole Brain Emulation: A Roadmap*. **Technical Report #2008-3, Future of Humanity Institute, Oxford**. — emulation 시간척도/실시간 비율, 가속 emulation(복제·고속 실행) 논의.
- **[검증가능-핵심]** Bostrom, N. (2014). *Superintelligence: Paths, Dangers, Strategies*. Oxford UP. — "speed superintelligence"(가속된 마음) 챕터.
- **[라이브확인]** *Time rescaling reproduces EEG behavior during transition from propofol anesthesia-induced unconsciousness to consciousness* (PMC5902625). — 의식 전이 시 신경동역학 시간-재스케일 경험적 관측(가속/감속의 실측 핸들 보조).
- **[라이브확인]** *Emergence of integrated information at macro timescales in real neural recordings* (bioRxiv 2022.03.07.483390). — 실 신경기록에서 Φ 가 macro 시간척도에서 출현(시간-그레인 의존성 경험적 지지). **S14 의 핵심 보강.**
- **[라이브확인]** Albantakis et al. (2023). *IIT 4.0* (아래 S24 인용, arXiv:2212.14787). — Φ-structure 가 시스템 업데이트 그레인에 정의됨.

**정직한 결론**: **진짜 계산가능 불변량 후보.** "Φ 가 시간-스케일에 불변인가"는 toy IIT 직접계산 falsifier 보유. → 🟢. **S24 와 함께 후속 micro-exp 1순위.**

---

### S17 — 디지털 부활: 희소 데이터(EEG)로부터 의식 복원 [⚪→🟡]

**본질**: 엔지니어링 목표 + 정보이론적 불가능성 정리 후보.

**핸들**: EEG = 두피 32~256 채널·수백 Hz·부피전도 평균화 → 정보율이 시냅톰(synaptome) 상태공간 대비 천문학적 부족. **EEG 역문제(inverse problem)는 ill-posed·비유일**: 주어진 두피 전위에 대한 내부 소스분포 유일하지 않음(고전 결과). → H(시냅톰) ≫ I(EEG;시냅톰) 으로 **정보-이론적 underdetermination 형식화 가능** → 🟡 승격 여지.

**문헌 상태**:
- **[검증가능-핵심]** Nunez & Srinivasan (2006). *Electric Fields of the Brain: The Neurophysics of EEG*, 2nd ed., Oxford UP. — 부피전도/공간해상도 한계, 역문제 ill-posed.
- **[라이브확인]** EEG 역문제 비유일성(von Helmholtz 1853 기원): 두피 전위에 대한 내부 소스분포는 **무한히 많은 해**(silent sources 를 더해도 데이터 적합 불변); 관측 < 미지수 → ill-posed·불안정(소스국소화 리뷰 다수, *J. NeuroEngineering and Rehabilitation* 5:25; Scholarpedia *Source localization*). — 부활 불가능성의 물리/정보근거(a priori 제약 없으면 복원 불능).
- WBE Roadmap(S14 인용): 부활-수준 복원은 분자해상도(파괴적) 스캔 요구 → EEG 같은 비침습 거시신호로 불가.

**정직한 결론**: "EEG 부활"은 비반증 공학환상이나, **그 불가능성**은 정보이론으로 형식화 가능(falsifier 보유 닫힌-부정). 부활 주장 = ⚪, 불가능성 정리 = 🟡 후보.

---

### S21 — Mind upload [⚪]

**본질**: 엔지니어링 목표. "올릴 수 있는가." Φ 진리주장 아님.

**핸들**: WBE 로드맵 스캔 해상도/연결체 임계 = 공학 실측 핸들. "업로드된 것이 의식/같은 사람인가"는 S5(IIT-Φ)+인격동일성(반증불가)로 환원.

**문헌**:
- **[라이브확인]** Sandberg, A. & Bostrom, N. (2008). *Whole Brain Emulation: A Roadmap*. **Technical Report #2008-3, Future of Humanity Institute, Oxford University** (ORA uuid:a6880196-34c7-47a0-80f1-74d32ab98788). — 표준 레퍼런스(3 핵심요소 scan→interpret/model→simulate, 금세기 중반 이전 가능성 조건부 결론, 기능적→종-일반→개인 emulation 벤치마크).
- **[라이브확인]** Bostrom, N. (2014). *Superintelligence: Paths, Dangers, Strategies*, Oxford UP. — "speed superintelligence": 생물뉴런 ~200Hz vs CPU ~2GHz(7 자릿수 차) → emulation 을 훨씬 빠르게 실행 가능, 주관시간 가속(S14 와 직결). 단 Φ 불변성은 별도 가정.

**정직한 결론**: 순수 공학목표 → ⚪. 의식 여부는 S5/S24 로 위임.

---

### S22 — AI→brain induction (의식 write) [⚪]

**본질**: 엔지니어링 목표(역방향 외부→뇌 쓰기).

**핸들**: 현 write 기술(TES 경두개전기자극·TMS 자기자극)의 **공간/정보 대역폭 극히 제한**(거시·비세포특이적). "임의 의식상태 주입"은 현 기술 불가 — 공학한계이지 반증가능 자연법칙 아님.

**문헌**:
- **[라이브확인]** Polanía, Nitsche, Ruff (2018). *Studying and modifying brain function with non-invasive brain stimulation*. **Nature Neuroscience** 21:174–187. DOI:10.1038/s41593-017-0054-4. — TES/TMS write 능력 현실적 한계 리뷰.

**정직한 결론**: 공학목표 + 현 기술 한계. 반증가능 가설 아님 → ⚪.

---

### S24 — Distributed / cloud 의식: 시스템 분할이 maximal Φ complex 를 파괴하는가 [🟢 핵심 — 닫힌-부정]

**본질**: **반증가능 + 닫힌-부정(closed-negative). 이 클러스터의 핵심 발견.**

**IIT EXCLUSION 공준 (형식적 진술 — 라이브확인)**:
> IIT 의 5(/6)대 공준 중 **배제(Exclusion)**: 의식은 시공간적으로 **확정적(definite)** 이다 — 인과력(integrated information)을 **최대화(ΦMax)** 하는 **단 하나의** 집합(complex)만 의식을 가지며, 그와 **중첩(overlapping)** 되는 더 크거나 작은 집합은 의식에서 *배제*된다.
> IIT 위키/Scholarpedia/원논문 표현: "among overlapping candidate sets, only one set of elements forms a complex, the one that generates the maximum ΦMax"; "a substrate that is maximally irreducible is called a maximal substrate or complex; overlapping substrates with lower φ are excluded from existence."

**라이브확인된 직접 함의 (S24 닫힌-부정)**:
> IIT 원문 함의(라이브확인): *"aggregates of conscious entities—such as interacting humans—have no consciousness, since by the exclusion postulate only maxima of Φ are conscious."* (상호작용하는 사람들의 집합체에는 의식이 없다 — 배제 공준상 Φ 최대값만 의식이므로.) 또한 Tononi-Koch 2015: 복합체는 **중첩/포섭 불가**(complexes cannot nest or overlap); 두 사람을 연결해 결합 Φ 가 각자보다 커지면 의식은 *결합 시스템 수준*으로 옮겨가지 *양쪽 동시 아님*. → **느린 통신선 너머 분산/클라우드 통합의식의 공준적 부정.**

- 두 노드(클라우드 인스턴스)가 **느린 링크**로 연결되면 통신지연 > 인과 시간그레인 → 절단선(cut)을 가로지르는 인과통합 붕괴 → minimum-information-partition 이 두 노드 사이를 지나며 system-Φ → max(Φ_A, Φ_B) 로 붕괴 → 전체가 하나의 major complex 못 됨. 각 노드는 *국소적* major complex 일 수 있으나 "여러 데이터센터 하나의 의식"은 IIT 가 **예측상 부정**.
- **toy 계산 검증가능**: 두 서브시스템 약-결합 g 스윕 → 임계 g* 아래에서 MIP 가 노드 사이를 지나 system-Φ 붕괴. **이게 falsifier.** (GNN-Φ 근사 도구 = bioRxiv 2024.12.31.630856 활용 가능.)

**문헌 상태**:
- **[라이브확인·검증가능-핵심]** Oizumi, Albantakis, Tononi (2014). *From the Phenomenology to the Mechanisms of Consciousness: Integrated Information Theory 3.0*. **PLOS Computational Biology** 10(5):e1003588. DOI:10.1371/journal.pcbi.1003588. PubMed PMID:24811198. — **Exclusion 공준 정식 진술**(maximally irreducible conceptual structure / ΦMax / definiteness). S24 1차 출처.
- **[라이브확인·검증가능-핵심]** Albantakis, Barbosa, Findlay, Grasso, Haun, Marshall, Mayner, Zaeemzadeh, Boly, Juel, Sasai, Fujii, David, Hendren, Lang, Tononi (2023). *Integrated information theory (IIT) 4.0: Formulating the properties of phenomenal existence in physical terms*. **PLOS Computational Biology** 19(10):e1011465. **arXiv:2212.14787**. PubMed PMID:37847724. — Exclusion 을 definiteness/maximal substrate 로 갱신, 유일 maximal complex.
- **[라이브확인·검증가능-핵심]** Tononi & Koch (2015). *Consciousness: here, there and everywhere?* **Phil. Trans. R. Soc. B** 370:20140167. DOI:10.1098/rstb.2014.0167. — "두 사람/시스템을 연결해도 하나의 의식 안 됨"(exclusion 의 분산-의식 부정) 명시 사고실험. **S24 직접 출처.**
- **[라이브확인]** IIT Wiki — *Exclusion* (iit.wiki/axioms-and-postulates/exclusion); Scholarpedia *Integrated information theory* — 공준 표준 진술 보조("among overlapping candidate sets, only one set forms a complex, the one generating maximum ΦMax").
- **[라이브확인]** Tononi (2008). *Consciousness as integrated information: a provisional manifesto*. **Biological Bulletin** 215(3):216–242. — 통합/배제 초기 정식화.
- **[라이브확인·반대편]** Hanson & Walker (2019, arXiv:1908.09621) 및 Schwitzgebel 등 비판 — exclusion 공준이 "의식을 거의 무관하게 만든다"는 반론; S24 닫힌-부정은 *IIT 가 참일 때* 성립(이론-조건부 negative).

**정직한 결론**: **이 클러스터 최강 항목.** IIT exclusion 공준은 "느린 링크 너머 분산/클라우드 통합의식"에 대해 **공준 수준의 닫힌-부정**(a_paper_negative_ok 의 전형적 publishable negative; 원논문이 "상호작용 인간 집합체에 의식 없음"을 명시). 더구나 weak-coupling g-sweep toy IIT(GNN-Φ 근사 가능)로 **계산 검증가능**(🟢 numerical falsifier). → 🟢, 후속 micro-exp **0순위.**

---

### S25 — Mobile EEG logging [⚪]

**본질**: 가설 아님 — 데이터 수집 행위/도구.

평가: 반증가능 명제 미구성. 다른 가설(S13/S17)에 데이터 공급 *수단*. 의식 진리주장 없음 → ⚪. (수집 EEG 정보율은 S17 핸들로 재활용.)

---

### S29 — Music as consciousness-backup [⚪]

**본질**: 가설 아님 — 은유.

평가: "음악이 의식 백업 매체"는 정보-담지로 약하게 형식화 가능하나, S8(rollback)·S17(부활) 정보이론 핸들로 환원될 뿐 독립 반증가능 명제 미구성 → ⚪.

---

## 후속 fire 권고 (실측 핸들 보유 항목)

| 우선 | 항목 | 실험 | 산출 verdict |
|---|---|---|---|
| 0순위 | **S24** | weak-coupling g-sweep toy IIT (n=4~6, 두 서브시스템, PyPhi 또는 GNN-Φ 근사) → 임계 g* 에서 system-Φ → max(Φ_A,Φ_B) 붕괴 확인 | 🟢/🔴 (exclusion 닫힌-부정 수치검증; a_paper_negative_ok) |
| 1순위 | **S14** | 시간 coarse-grain 비율 c 스윕 → Φ(c) 곡선; 순수재스케일 vs 노이즈고정 두 조건 | 🟢/🔴 (시간-스케일 Φ 불변성 falsifier) |
| 2순위 | **S17** | EEG 정보율 vs 시냅톰 상태엔트로피 채널-용량 하한 → 부활 underdetermination 형식화 | 🟡 (정보이론 불가능성) |
| 2순위 | **S13** | (문헌-종결 가능) replay 가설 = 재공고화 문헌으로 사실상 닫힌-부정 | 🟡 |

---

## 요약 (parent agent 용)

- **진짜 계산가능/형식적 핸들 (🟢)**: **S24** = IIT exclusion 공준이 분산/클라우드 통합의식에 대한 **닫힌-부정**(Oizumi-Albantakis-Tononi 2014 원논문이 "상호작용 인간 집합체에 의식 없음"을 명시; Tononi-Koch 2015 "연결해도 하나의 의식 아님" 사고실험). weak-coupling g-sweep toy IIT(GNN-Φ 근사 도구 존재)로 수치검증 가능 — **클러스터 최강·publishable negative**. **S14** = Φ 의 시간-그레인 의존성(Hoel-Albantakis-Tononi 2013 PNAS causal emergence)으로 "×100 가속 시 Φ 불변?"이 toy IIT 직접계산 falsifier. S8 은 trivial 동어반복(🟢 but 비자명성 없음).
- **부분 경험적 핸들 (🟡)**: **S5** = Φ 계산가능하나 transformer 피드포워드→IIT-Φ 낮음(실측 논문 arXiv:2412.07278 Superficial Consciousness, 2506.22516 LLM-ToM-IIT, 1908.09621 FF-zombie 존재); sentience 함의는 IIT 종속. **S13** = 회상=재구성(Nader 2000 reconsolidation, Sinclair-Barense 2019), replay 가설 사실상 반증. **S17** = 부활 자체 ⚪이나 *불가능성*은 EEG 역문제 ill-posed/정보이론으로 형식화 가능.
- **순수 ⚪ (비반증 엔지니어링/은유)**: **S21**(upload 공학목표·WBE Roadmap), **S22**(brain-write 공학목표·TES/TMS 대역폭 한계 Polania 2018), **S25**(EEG 수집 도구), **S29**(백업 은유).
- **세션 제약**: WebSearch 동작(인용 다수 라이브확인); arxiv API + WebFetch 타임아웃이라 일부 arxiv-id/저자명은 [재확인-권장]. 어떤 항목도 terminal verdict 미승격(literature scoping).
