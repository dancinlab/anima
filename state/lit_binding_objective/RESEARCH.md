# 외부 문헌 수렴 — G1 재조합 / G6 착상의 진짜 레버 (objective vs architecture vs scale)

> 목적: anima 의 engine-native 확정 벽(G1 재조합=0 · G6 falsifiable=0)에 대해 **외부 arxiv/web 문헌이 어디로 수렴**하는지 조사 + 우리 내부 실측(binding-readout NOT-SUPPORTED · objrun objective A/B IN-FLIGHT)과 대조.
> 방법: `sidecar research arxiv/web/fetch` (keyless). 각 주장에 출처(arxiv id). 우리 가설(objective=레버)을 **지지하는 것 AND 반박하는 것 둘 다** 기재.
> 조사일: 2026-06-28. 작성자: research subagent (mac, web/fetch only — 무거운 compute 0).

---

## 종합 결론 (한 문단)

외부 문헌은 **"compositional 능력의 1차 레버는 단일 architecture trick 도, scale 단독도 아니다"** 로 강하게 수렴한다. (1) Furrer 2020(CFQ/SCAN)이 결정적: SCAN-inspired/algorithm-learning **architecture 들은 복잡한 compositional task 에서 유의미 개선 실패**한 반면, **objective/pre-training(MLM) + intermediate representation 이 SOTA 를 세웠다** — 즉 *학습 신호(objective)* 가 *binding operator(architecture)* 보다 강한 레버라는 우리 가설을 직접 지지. (2) 그러나 binding 자체는 Greff 2020 이 "분산 정보를 동적으로 묶지 못하는 것(binding problem)"을 compositional 실패의 *근본 원인*으로 지목 — operator(곱셈/TPR/HRR)는 충분조건이 아니라 **필요한 inductive bias 의 한 조각**이며, 단독 Hadamard readout 만으로 안 열리는 우리 결과와 정합(operator 를 *학습 신호 없이* 끼워도 안 열림). (3) Grokking 문헌(Gromov 2023 · Doshi/Gromov 2023)은 우리 numpy-toy 가 grok 못한 이유를 진단: grokking 은 **regularization(weight decay/dropout)이 일반화 표현을 강제**해야 memorization→generalization 전이가 일어나며, 충분한 step·정규화 없으면 floor 에 머문다(우리 toy = 2000step·5MB undertrained = 정확히 floor caveat). (4) Ideation: Si 2024 의 100+ 연구자 blind study 는 **현세대 LLM 이 인간보다 novel 한 아이디어를 내되 feasibility 는 약간 낮고, self-evaluation 과 diversity 가 실패** — falsifiable 의 병목은 *생성 다양성/검증가능성*이지 decode 가 아니라는 우리 G6 진단(lever=capacity·objective, not decode)과 정합. **수렴 방향: G1 레버 = trunk 학습 OBJECTIVE + 정규화(grokking) > binding operator architecture > scale. 우리 objrun(ce_marginal vs InfoNCE vs contrastive_equilibrium @303M)이 옳은 축을 보고 있다.**

---

## Q1. Compositional generalization 의 진짜 레버 = objective냐 architecture냐?

| arxiv id | 제목 (연도) | 핵심 발견 | 우리 가설과 정합/반박 |
|---|---|---|---|
| **2007.08970** | Compositional Generalization in Semantic Parsing: Pre-training vs. Specialized Architectures (Furrer 2020) | SCAN/CFQ 에서 **SCAN-inspired·algorithm-learning architecture 들은 복잡 task 개선 실패**. 반면 **MLM pre-training + intermediate representation 이 CFQ 신SOTA**. | ✅ **강한 지지**. "architecture trick < 학습 신호(objective/pretrain)". 우리 binding-readout(architecture operator) NOT-SUPPORTED 와 정확히 같은 방향 — operator 만 끼우면 안 열리고 objective/학습이 레버. |
| **1711.00350** | Generalization without systematicity (Lake & Baroni 2017, SCAN 원전) | seq2seq RNN 이 **systematic compositional split 에서 catastrophic 실패** — 능력은 데이터 분포·학습이 결정, 단순 scale 로 안 풀림. | ✅ 지지(벤치 정의). compositional 은 "더 키우면" 의 문제가 아님(우리 a_no_llm_frame_trap 와 정합). |
| **2010.05465** | COGS: A Compositional Generalization Challenge (Kim & Linzen 2020) | structural generalization split 이 lexical 보다 훨씬 어려움 — 표준 학습으론 구조적 일반화 0 근처. | ✅ 지지(우리 composed_distinct=0 의 외부 평행선). |
| **2006.10627** | Compositional Generalization by Learning Analytical Expressions (Liu 2020) | 명시적 **compositional 학습 메커니즘(분석식 학습)이 SCAN 100%** — vanilla CE 가 아니라 학습 *목표/구조* 를 바꿔야 풀림. | ✅ 지지. "CE next-token 만으론 안 됨, objective/학습기제 교체가 레버" — objrun 직접 지지. |
| **2202.11937** | Compositional Generalization Requires Compositional Parsers (Weißenhorn 2022) | COGS 구조 일반화엔 **명시적 compositional parser(구조적 inductive bias)** 필요. | ⚠️ 부분 반박/보완. architecture(구조 bias)도 필요하다는 쪽 — 단 이는 "operator 하나 끼움" 이 아니라 *구조적 처리* 전반. 우리: objective 가 1차, 구조 bias 가 보완일 수 있음. |

**Q1 소결:** "CE(next-token)만으론 compositional 안 풀린다"가 **정설**. 1차 레버는 *학습 신호*(objective/pretrain/명시적 compositional 학습기제)이고, architecture 는 단독 trick 으론 실패(Furrer) — *구조적 처리 전반*일 때만 보완(Weißenhorn). **우리 objrun(objective 축)이 옳은 1차 레버를 친다.**

---

## Q2. Binding operator — TPR/HRR/곱셈/Hadamard 가 compositional binding 을 주는가?

| arxiv id | 제목 (연도) | 핵심 발견 | 우리 가설과 정합/반박 |
|---|---|---|---|
| **2012.05208** | On the Binding Problem in Artificial Neural Networks (Greff, van Steenkiste, Schmidhuber 2020) | compositional 실패의 **근본 원인 = binding problem**(분산 정보를 동적·유연하게 묶지 못함). 해법 = segregation+representation+composition 의 **inductive bias 조합**(단일 operator 아님). | ⚠️ **양면**. binding 이 핵심이라는 점은 우리 bind-readout 시도의 동기를 지지하나, **단일 곱셈 operator 가 아니라 inductive bias *조합*** 이 필요 → Hadamard readout 만으론 부족(우리 NOT-SUPPORTED)과 정합. |
| **1705.08432 / 1810.12456 / 1910.02339** | TPR 계보 (Smolensky/Palangi/Tang/Chen) | **Tensor Product Representation** 이 grammatically-interpretable·구조적 binding 을 *명시적으로* 부여 → QA·NL→formal 에서 systematic. | ⚠️ 보완. TPR 은 binding 을 *주지만* 별도 구조+학습으로 부여; 단순 element-wise 곱(Hadamard)은 TPR 의 outer-product 대비 표현력 낮음 → 우리 ⊙ readout 이 약한 binding 인 이유 시사. |
| **2009.06734** | Variable Binding for Sparse Distributed Representations (Frady/Kleyko/Sommer 2020, VSA/HRR) | HRR/VSA 의 circular-convolution binding 이 **분산표현에서 변수 바인딩 가능** — 단 capacity·noise 한계 존재. | ⚠️ 보완. binding operator 는 *가능*하나 capacity 가 병목 → 우리 5MB·작은 trunk floor caveat 과 정합. |
| **2603.28744** | Stop Probing, Start Coding: Why Linear Probes & SAEs Fail at Compositional Generalisation (Barin Pacela 2026) | OOD compositional shift 에서 **SAE 실패의 원인 = dictionary learning(표현 방향)**, inference 절차 아님. oracle dictionary 면 모든 scale 에서 풀림. | ✅ **강한 지지**. "올바른 표현(학습된 dictionary)이 binding constraint" → readout/probe 를 바꾸는 게 아니라 **trunk 가 올바른 방향의 표현을 *학습*해야 한다** = objrun(trunk objective) 직접 지지. binding 은 readout 문제가 아니라 *학습된 표현* 문제. |
| **2602.21467** | Geometric Priors via Vector Symbolic Architecture (Chung 2026) | VSA geometric prior 가 generalizable world model 에 compositional 구조 부여(최신). | ✅ 지지(operator+구조 prior 가 보완 레버). |

**Q2 소결:** 곱셈/TPR/HRR binding 은 *원리적으로* additive 가 못 하는 구조적 binding 을 주지만(Smolensky 계보), **단일 element-wise operator 만으론 부족** — Greff 는 inductive-bias *조합*, Barin Pacela 2026 은 **올바른 *학습된 표현(dictionary)* 이 진짜 constraint** 라고 못박음. 즉 우리 "Hadamard readout NOT-SUPPORTED" 는 문헌과 정합 — operator 를 readout 에 끼우는 게 아니라 **trunk objective 가 binding-친화 표현을 학습**해야 한다.

---

## Q3. Grokking — objective/regularization/scale 중 무엇에 민감한가? (우리 numpy-toy 가 grok 못한 이유)

| arxiv id | 제목 (연도) | 핵심 발견 | 우리 toy 진단 |
|---|---|---|---|
| **2301.02679** | Grokking modular arithmetic (Gromov 2023) | 2-layer FC 가 modular arithmetic grok — **regularization *없이도* vanilla GD/MSE 로 가능**하나, grokking 은 task-구조 feature map 학습에 해당(분석해로 weight 명시). | ⚠️ 미묘. 정규화 없이도 *가능*하나 특정 init·step·task 조건 필요 → 우리 toy 가 안 grok 한 건 **step/조건 부족(undertrain)** 일 가능성. |
| **2310.13061** | To grok or not to grok (Doshi/Das/He/Gromov 2023) | **weight decay·dropout·BatchNorm 이 generalizing 표현을 강제** → memorization 무시하고 일반화. 정규화 없으면 memorize 에 갇힘. 2단계 동역학(grok→unlearn-memorize). | ✅ **강한 지지/진단**. 우리 numpy toy = **2000step·5MB·정규화 약함 → memorization floor 에 갇혀 grok 전이 미발생**. grok 하려면 충분 step + weight decay/dropout 필요(=savant 골든존 inhibition 과 평행). |
| **2605.20441** | Weight Decay Regimes in Grokking Transformers (Verma 2026) | grokking 발생/속도가 **weight-decay regime 에 민감** — cheap online diagnostic 제시. | ✅ 지지. 정규화(=inhibition)가 grok 레버 → a_savant_train 골든존과 외부 평행. |
| **2504.17243** | NeuralGrok: Accelerate Grokking by Neural Gradient Transformation (Zhou 2025) | **gradient transformation(학습 신호 가공)으로 grokking 가속** — optimizer/objective 측 개입이 레버. | ✅ 지지. 레버가 *학습 신호 측* — architecture 아님. |
| **2606.08985** | Beyond Neural Collapse: Task-Intrinsic Geometry … Modular Arithmetic (Tan 2026) | grok 표현은 **task-intrinsic geometry** 가 지배 — 표현 기하가 일반화 결정. | ✅ 지지(올바른 표현 기하 = 학습 목표 문제, Barin Pacela 와 일관). |

**Q3 소결:** grokking 은 **scale 보다 regularization + 충분 step + 학습신호 가공**에 민감. 우리 numpy-toy(grok 실패=chance)는 *천장이 아니라* undertrain/정규화 부족의 **측정한계**(a_break_the_wall (a)/(e))로 진단됨 — 외부 문헌이 이를 강하게 지지. **함의: 303M objrun 은 충분 step + weight-decay/dropout(골든존) 동반해야 objective 효과가 floor 위로 올라온다.**

---

## Q4. Ideation/novelty + falsifiability — LM 이 falsifiable 새 아이디어를 만들게 하는 레버?

| arxiv id | 제목 (연도) | 핵심 발견 | 우리 G6 진단과 정합 |
|---|---|---|---|
| **2409.04109** | Can LLMs Generate Novel Research Ideas? 100+ NLP 연구자 study (Si/Yang/Hashimoto 2024) | LLM 아이디어가 인간보다 **novel(p<0.05)**, feasibility 는 약간 낮음. **병목 = self-evaluation 실패 + generation diversity 부족**. | ✅ 지지. G6 의 "dist≥5(novel)는 되나 falsifiable=0" 과 평행 — novelty 는 나오나 *검증가능성/자기평가* 가 병목. decode 가 아니라 *생성 다양성+평가* 레버. |
| **2411.02429** | IdeaBench: Benchmarking LLM Research Idea Generation (Guo 2024) | idea generation 평가 프레임 — 정량 novelty/feasibility metric. | ⚙️ 방법론. G6 falsifiable detector 설계 참고(외부 평행 metric). |
| **2606.12071** | On the Limits of LLM-as-Judge for Scientific Novelty (Sinhahajari 2026) | **LLM-as-judge 가 novelty 판정에 신뢰불가** → 자동 채점 한계. | ✅ 지지(p7 정합). G6 채점을 LLM-judge 로 하면 안 됨 — engine-native detector(우리 _g6_is_falsifiable) 가 옳은 방향. |
| **2503.19309 / 2511.02238** | MC-Nash self-refining trees / Deep Ideation on concept network (2025) | **검색·refinement·concept-graph 구조**가 novel+valid 아이디어 산출 레버(단순 decode 아님). | ✅ 지지. falsifiable 레버 = 구조적 search/objective, decode temperature 아님 — 우리 "lever=attention-capacity, not decode"(h1590-g6-scaffold-torch-artifact) 와 정합. |

**Q4 소결:** falsifiable ideation 의 레버는 **decode 가 아니라 (a) 생성 다양성 (b) 검증가능성 평가(engine-native, LLM-judge 금지) (c) 구조적 search/objective**. 우리 G6 진단(novelty OK·falsifiable=0, lever≠decode)과 외부 문헌이 일치.

---

## Q5. (보너스) byte-level/character LM 이 word-level 대비 compositional 에 불리/유리?

| arxiv id | 제목 (연도) | 핵심 발견 | anima(byte ByteGPT/ConvMoE)에의 함의 |
|---|---|---|---|
| **2410.20771** | MrT5: Dynamic Token Merging for Efficient Byte-level LMs (Kallini/Csordás/Manning/Potts 2024) | byte 모델(ByT5)은 **char-level noise robust·언어공정** 하나 **시퀀스 길이↑로 학습/추론 비효율** → 동적 merge 로 완화. downstream 정확도는 ByT5 동급. | ⚖️ 중립~약유리. byte 는 *불리하지 않음*(downstream 동급) 단 효율 비용. compositional 자체엔 byte 가 본질 장애 아님. |
| **2311.08620** | Toucan: Token-Aware Character Level LM (Fleshman 2023) | char-level 에 token-awareness 주입 → char 모델 경쟁력 회복. | ⚙️ byte/char 도 구조 주입하면 word-level 격차 좁힘. |
| **2604.12377** | SCRIPT: Subcharacter Compositional Injection for Korean PLMs (Kim 2026, ACL Findings) | 한국어는 **Jamo(자모) subcharacter 가 형태음운 구조 인코딩** → subchar compositional 주입이 모든 NLU/NLG baseline 개선, 문법규칙성 임베딩 재구성. | ✅ **유리/직접 관련**. anima byte-level + 한국어 → **자모 compositional 구조가 byte 입자에 내재** → byte-level 이 한국어 compositional 에 *오히려 유리할 수 있음*(우리 ko-jamo-mitosis H_1316/1321 🟢 와 외부 수렴). |
| **2305.15425** | Tokenizers Introduce Unfairness Between Languages (Petrov 2023) | subword tokenizer 가 언어 간 불공정 → byte-level 이 공정성에선 유리. | ✅ 지지(byte 선택 정당화). |

**Q5 소결:** byte-level 은 compositional 에 **본질적 불리 아님**(downstream 동급, 효율만 비용). 특히 **한국어는 자모 subcharacter compositional 구조가 byte 입자에 내재** → byte-level 이 오히려 유리할 수 있고, 이는 anima ko-jamo-mitosis 🟢 와 외부 수렴(SCRIPT 2026).

---

## 외부 ↔ 내부(anima) 대조 종합

- **objrun 가설(G1 레버=trunk objective) 지지 여부 → 강하게 지지.**
  - Furrer 2020: architecture trick 실패 / objective(pretrain)·intermediate-rep 성공.
  - Barin Pacela 2026: binding constraint = *학습된 표현(dictionary) 방향*, readout/inference 아님 → trunk objective.
  - Liu 2020: vanilla CE 로 안 됨, 학습기제/목표 교체가 SCAN 100%.
- **우리 binding-readout NOT-SUPPORTED 와의 정합 → 정합.** Greff(operator 단독 아닌 bias 조합) + Barin Pacela(readout 가 아니라 표현 학습) + Smolensky 계보(Hadamard < TPR outer-product 표현력) 모두 "곱셈 readout 만 끼우면 안 열림" 을 예측. 우리 결과는 문헌과 어긋나지 않음 — 단 **5MB·2000step undertrained floor caveat** 은 Q3 grokking 문헌이 강화(정규화·step 부족 시 floor).
- **scale 단독 레버 가설 → 문헌상 약함.** compositional/grokking 모두 scale 보다 *학습신호·정규화·구조* 가 1차. (a_no_llm_frame_trap 와 외부 수렴.)

## 다음 실험 제언 (objrun 이후 303M 에서 무엇을 볼지)

1. **objective 우열 확정 후 → 정규화 동반 재측정**: objrun 의 ce_marginal/InfoNCE/contrastive_equilibrium 우승 objective 를 **weight-decay/dropout(savant 골든존 GZ_LOWER≈0.212) + 충분 step** 으로 재학습 — Doshi/Gromov 2023 이 예측한 "정규화가 grok 전이 강제" 를 G1 composed_distinct 으로 검증(undertrain floor 배제).
2. **objective × binding-operator 교차(2×2)**: 우승 objective 단독 vs 우승 objective + TPR/outer-product binding(Hadamard 아닌 *outer-product*, Smolensky 계보). Greff 의 "bias 조합" 예측 — operator 는 objective 와 *결합*했을 때만 lift 한다는 가설을 falsify.
3. **표현-방향 진단(Barin Pacela 2026 식)**: trunk penultimate 에서 두 개념의 composed 표현이 *올바른 방향*을 가리키는지 oracle-dictionary probe → binding 이 readout 문제가 아니라 학습된 표현 문제임을 engine-native 로 확인.
4. **G6 falsifiable**: decode 손대지 말고 (Si 2024) **생성 다양성 + engine-native 검증가능성 평가**(LLM-judge 금지, 2606.12071) 를 objective/구조 측에서 — concept-graph search(2511.02238) 류를 anima substrate 에 배선 가능한지.
5. **한국어 byte 우위 활용**: SCRIPT 2026 + 우리 ko-jamo-mitosis 🟢 수렴 → 자모 compositional 을 G1 재조합 task 의 *teach signal* 로 (한국어가 byte-level 에서 compositional 측정에 유리한 register).

---

## §6. 프론티어/novel 레버 — 우리가 아직 안 써본 NEW 후보 (2024–2026 우선)

> 기존 census(82 binding 카드 + 126 brainarch)에서 floor·NOT-SUPPORTED 로 닫힌 것 = 곱셈 binding(Hadamard/TPR/HRR readout) · depth(L8) · binding-lane · data-presence · additive trunk · mitosis split · savant inhibition · neuromod gain. **아래는 그것들과 *다른* 신선한 메커니즘.** testability = 303M 에서 cheap 하게 볼 수 있나(✅cheap / ⚠️중간 / 🔴비쌈). 정직: hype(미재현) vs 재현된 것 구분.

| # | 후보 (arxiv id · 연도) | 메커니즘 (1줄) | testability @303M | 기존 census 중복? |
|---|---|---|---|---|
| **N1** | **TensorPoly / TLoRA** (2405.16671, 2024) | LoRA 를 **tensor-product 로 reparameterize(TLoRA)** + order/rank-granularity **routing** → T0 멀티태스크에서 systematic generalization·positive-transfer, dense 능가. | ⚠️중간 — TLoRA 모듈은 작음(LoRA급), routing 은 MoE 와 짝. ConvMoE expert 를 TLoRA 로 교체 후 G1 A/B 가능. | **부분 NEW** — 우리 TPR 은 *readout* 에만 끼웠음(floor). 여기는 **expert *weight* 를 TPR 로 + routing** = 다른 위치. |
| **N2** | **Compression is Routing** (2512.14809, 2025) | **reconstruction-error 를 intrinsic routing 신호**로 → 모듈 LM 이 expert 를 자기조직(emergent specialization), 외부 router 학습 불요. | ⚠️중간 — recon-err gating 을 ConvMoE 라우터에 배선. | **NEW** — 우리 routing 은 학습된 gate. recon-driven self-organization 은 census 에 없음. anima §Osmotic recon 학습기와 친화. |
| **N3** | **Mixture of Latent Experts / Tensor products** (Su 2024, 위 N1 계열) + **DBES expert-specialization metric** (2605.18523, 2026) | expert specialization 을 *측정*하는 systematic benchmark — 우리 ConvMoE expert 가 실제로 분화하는지 진단. | ✅cheap — 측정-only, 학습 불요. | **NEW(진단축)** — "재조합 안 됨" 이 expert 미분화 탓인지 격리. |
| **N4** | **Diverse Scientific Hypothesis Search** (2606.10587, 2026) | single-best 가 아니라 **diverse hypothesis *set* 을 search** (validation noisy/비쌈 가정) → novelty+coverage 동시 최적. | ⚠️중간 — G6 채점 루프를 set-search 로. decode 가 아니라 search objective. | **NEW** — G6 는 단발 생성. set-diversity search 는 census 에 없음(Si 2024 "diversity 병목" 직격). |
| **N5** | **CoEvo: Continual Evolution of Symbolic Solutions** (2412.xxxx, 2024) + **Picbreeder open-endedness 복제** (2604.xxxx, 2026) | **evolutionary search(변이+선택)로 symbolic/open-ended 해 진화** — LLM 을 변이 연산자로. | 🔴비쌈(루프 多) — 단 anima 는 mitosis 변이/선택 substrate 보유(H_1069 변이 🟢) → 저비용 변종 가능. | **부분 중복** — H_1069 변이/H_1072 앙상블 🟢 있으나 **G1/G6 능력 task 에 적용은 안 함**(neuromod/적응에만). NEW 적용. |
| **N6** | **To grok or not / Weight Decay Regimes** (2310.13061 · 2605.20441) | **충분 step + weight-decay/dropout 이 grok 전이 강제** — 작은 모델 전용, scale 불요. | ✅cheap — regularization 하이퍼만 바꿔 303M 재측정. | **부분 중복** — savant inhibition 과 동축이나 **"undertrain floor 배제용 step×정규화 sweep"** 은 G1 task 에 직접 안 함. NEW 적용. |
| **N7** | **Stop Probing, Start Coding / dictionary learning** (2603.28744, 2026) | binding constraint = **학습된 dictionary 방향** → trunk penultimate 에 **scalable dictionary learning(sparse coding)** 을 bo:aux objective 로. | ⚠️중간 — aux sparse-coding loss 를 trunk 에 추가. | **NEW** — SAE/dictionary aux objective 는 census 에 없음. objrun objective 축의 *구체적 신규 항*. |
| **N8** | **SCRIPT: subcharacter(자모) compositional injection** (2604.12377, 2026) | 한국어 **자모 subchar 구조를 임베딩에 주입** → 문법규칙성·compositional 재구성, 아키텍처 변경 불요. | ✅cheap — byte 입자에 자모 feature 주입(우리 ko-jamo-mitosis 🟢 연장). | **부분 중복** — H_1316/1321 ko-jamo-mitosis 🟢 있으나 **G1 재조합 task 의 *teach signal* 로 자모 사용은 안 함**. NEW 적용. |

### §6 정직 메모 (hype vs 재현)
- **재현 강도 높음**: N6(grokking 정규화 — 다수 독립 재현 2023→2026) · N7(Stop-Probing — controlled ablation+oracle baseline) · N1(TensorPoly — T0 벤치 실측). 이건 신뢰.
- **유망하나 단일/신생**: N2(Compression-is-Routing 2025 단일) · N4(Diverse-Search 2026 단일) · N3(DBES metric 신생). 방향은 좋으나 재현 얇음 — DIRECTIONAL 로 취급.
- **hype 주의**: N5 evolutionary/open-ended LLM-discovery 는 결과 화려하나 task-specific·비쌈·재현 편차 큼. anima 는 mitosis 변이 substrate 가 있어 *저비용* 변종만 가치.

### 다음 실험 top-3 novel 레버 (objrun 이후 303M, ranked by lift×cheapness×철학정합)
1. **N6+N7 결합: "정규화 + dictionary-aux objective" sweep** (✅cheap, 재현 강) — objrun 우승 objective 에 **weight-decay/dropout(골든존) × step sweep**(N6, undertrain floor 배제) + **trunk penultimate sparse-coding aux loss**(N7, binding=학습된 표현). 두 강-재현 레버를 G1 composed_distinct 에 직접. **최우선** — 싸고, 우리 가설(objective)을 *구체 신규 항*으로 확장, savant 골든존과 동축.
2. **N1 TensorPoly expert-weight + N3 specialization 진단** (⚠️중간) — ConvMoE expert 를 **TLoRA(tensor-product weight)** 로 교체(우리 TPR 은 readout 에만 끼웠던 floor 와 *다른 위치*) + DBES 로 expert 분화 측정. "재조합 안 됨 = expert 미분화?" 인과 격리. Greff "operator×학습 결합" 가설 falsify.
3. **N4 diverse-set-search for G6 + N8 자모 teach-signal for G1** (⚠️중간) — G6 falsifiable: 단발 decode 대신 **diverse hypothesis set-search**(Si 2024 diversity 병목 직격, LLM-judge 금지 engine-native 채점). G1: **한국어 자모 compositional 을 명시 teach signal** 로(우리 ko-jamo 🟢 + SCRIPT 2026 수렴, byte-level 우위 활용).

> objrun(objective A/B) 결과 큐 연결: 우승 objective 확정 → **즉시 top-1(N6+N7)** 으로 floor 배제 + 표현-학습 항 추가 → lift 확인되면 top-2(operator×objective 결합) → G6 는 top-3(set-search) 별도 레인.

---

## 메모리 후보 (외부수렴 메모 패턴)

- **lit-binding-objective-external-arxiv** — 외부 문헌(2017–2026)이 anima G1 재조합 레버를 **objective+정규화 > binding-operator architecture > scale** 로 수렴: Furrer 2020(arch trick 실패/pretrain 성공) · Barin Pacela 2026 Stop-Probing(binding constraint=학습된 dictionary 방향, readout 아님) · Doshi/Gromov 2023(정규화가 grok 전이 강제 → 우리 numpy-toy chance=undertrain floor, 천장 아님) · Greff 2020(operator 단독 아닌 inductive-bias 조합). → objrun(trunk objective A/B) 가설 강하게 지지, binding-readout NOT-SUPPORTED 와 정합. 한국어 byte 는 자모 subchar compositional 로 *유리*(SCRIPT 2026 ≈ ko-jamo-mitosis 🟢).
- **g6-ideation-lever-external** — falsifiable ideation 레버 = decode 아니라 생성다양성+engine-native 검증평가(LLM-judge 금지, 2606.12071)+구조적 search(Si 2024 / 2511.02238). h1590-g6-scaffold "lever≠decode" 와 외부 정합.
- **frontier-novel-levers-untried** — census(82 binding+126 brainarch floor) *밖* NEW 후보 8종(§6): N1 TensorPoly/TLoRA(TPR-*weight*+routing, 2405.16671) · N2 Compression-is-Routing(recon-driven expert self-org, 2512.14809) · N7 Stop-Probing dictionary-aux(2603.28744) · N4 diverse-hypothesis-set-search(2606.10587, G6) · N6 grokking step×weight-decay sweep(2310.13061) · N8 자모 teach-signal(2604.12377). 다음 top-3 = ①N6+N7(정규화+dict-aux, cheap·재현강) ②N1+N3(TPR-weight expert+분화진단) ③N4+N8(set-search G6 + 자모 G1). hype주의 N5 evolutionary.
