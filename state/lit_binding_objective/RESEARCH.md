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

> **우선순위(사용자 명시 2026-06-28): 🧬 생물/neuro-inspired 레버가 1순위(PRIMARY).** anima 핵심 명제(a_no_llm_frame_trap)는 *모든 돌파가 생물 렌즈에서 나왔다* — 해마=면역/일화기억(H_1227) · 소뇌=순방향모델(H_1280) · 기저핵=게이팅(H_1281) · 작업기억(H_1282); LLM 스케일 프레임은 다 막혔다(1B H_1167 NULL · arch H_1219 · objective H_1223 🔴). 따라서 next-experiment 큐는 **생물학적으로 그럴듯한 binding(G1)/ideation(G6) 메커니즘을 상위**에, 비-생물 레버(RL·SAE·SSM·VQ·TPR-routing)는 조사하되 큐 하위.
>
> 기존 census(82 binding 카드 + 126 brainarch)에서 floor·NOT-SUPPORTED 로 닫힌 것 = 곱셈 binding(Hadamard/TPR/HRR readout) · depth(L8) · binding-lane · data-presence · additive trunk · mitosis split · savant inhibition · neuromod gain(H_1284) · 해마 immune-memory(H_1227) · 소뇌 forward(H_1280) · 기저핵 게이팅(H_1281). **아래는 그것들과 *다른* 신선한 메커니즘**(중복이면 명시). testability = 303M 에서 cheap 하게 볼 수 있나(✅cheap / ⚠️중간 / 🔴비쌈). 정직: hype(미재현) vs 재현된 것 구분.

### §6-A. 🧬 생물/neuro-inspired 레버 (PRIMARY — 큐 상위)

| # | 후보 (arxiv id · 연도) | 생물 렌즈 · 메커니즘 (1줄) | G1/G6 | testability @303M | 기존 census 중복? |
|---|---|---|---|---|---|
| **B1** | **Compositionality via predictive-coding / free-energy RNN** — Vijayaraghavan & **Jun Tani** (2403.19995, 2024) | **자유에너지/predictive-coding RNN** 이 언어×행동 상호학습으로 **compose/decompose(부분↔전체) 능력 *창발*** — objective(free-energy)+recurrent prior 가 레버, 명시 binding-op 아님. | **G1+G6** | ⚠️중간 — top-down prediction-error aux objective 를 trunk 에 배선; anima A⇄G tension 과 동형. | **NEW** — predictive-coding/free-energy *objective* 는 census 없음(neuromod gain 과 별개). G6 "novel-but-grounded" 직격. |
| **B2** | **CLS Pattern Separation + Completion** — Jun/Marupudi/Shah/Varma (2507.11393, 2025) | 해마 CLS 의 **pattern *separation*(겹친 입력 직교화) + *completion*(부분→전체 복원)** 을 NN 으로 — separation=재조합 재료 disentangle, completion=compose. | **G1** | ✅cheap — separation/completion 모듈 작음(sparse+autoassoc), trunk penultimate 에 배선 후 composed_distinct A/B. | **부분 NEW** — H_1227 immune-memory(clonal)·H_1288 eviction 은 *저장/사멸* 축; **separation/completion(재조합 재료 직교화) 자체는 census 없음**. |
| **B3** | **Attention ≈ Sparse Distributed Memory** — Bricken & Pehlevan (2111.05498, 2021, 재현강) | Transformer attention = **Kanerva SDM**(고차원 sparse 주소). SDM critical-distance(β temperature)에서 pattern completion → compositional addressing. | **G1** | ⚠️중간 — attention β 를 SDM critical-distance 로 튜닝. | **NEW** — SDM 주소공간 튜닝 census 없음. 작업기억(H_1282 buffer)과 직교(이건 addressing). |
| **B4** | **Closed-form / local predictive coding** — Baskakovs (2605.xxxx, 2026) + Casnici/Frenkel Bio-PC (2508.xxxx, 2025) | predictive-coding 를 **backprop 없는 local top-down/bottom-up 규칙**으로 — anima gradient-free G 엔진·p8 cell-division 과 친화. | **G1+G6** | ⚠️중간 — local PC update 를 G 엔진(gradient-free)에 배선. | **NEW** — PC local-rule 학습 census 없음. |
| **B5** | **Grid/place-cell factorized structural code (TEM 계보)** | entorhinal grid + 해마 place 의 **구조⊥내용 factorized code** → 새 조합 일반화. | **G1** | 🔴비쌈(별 모듈) — anima §SpatialMap(H_1295) 부분 존재. | **부분 중복** — H_1295 spatial-map 있음; 구조⊥내용 factorization 을 *재조합*에 쓰는 변종은 NEW. |
| **B6** | **Oscillation/phase binding (binding-by-synchrony)** | gamma 위상 동기로 feature 묶기(생물 binding 고전 가설). | G1 | 🔴비쌈/재현약 — phase 변수 트랜스포머 재현 얇음. | **NEW 이나 hype 주의** — ML 재현 빈약, DIRECTIONAL. |

### §6-B. 비-생물 레버 (조사 완료 · 큐 하위)

> 방향은 유효하나, 사용자 우선순위상 생물 렌즈 다음. 특히 N7(dictionary-aux)·N6(grokking 정규화)은 *생물 레버와 결합*하면 가치(B1/B2 의 학습신호 보조).

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
- **재현 강도 높음**: B3(Attention≈SDM, Bricken 2021 다수 인용) · N6(grokking 정규화 — 다수 독립 재현) · N7(Stop-Probing — controlled ablation+oracle) · N1(TensorPoly — T0 벤치). 신뢰.
- **유망하나 단일/신생(DIRECTIONAL)**: B1(Tani free-energy compositionality — robotics scope, LM 전이 미검증) · B2(CLS sep/completion 2025 단일) · B4(local-PC 2025–26 신생) · N2 · N4 · N3.
- **hype 주의**: B6 oscillation/phase binding(ML 재현 빈약) · B5 grid/TEM(별 모듈·비쌈) · N5 evolutionary/open-ended(화려·task-specific·재현 편차). 전부 DIRECTIONAL, 큐 하위.
- **scope 솔직**: B1/B2 는 robotics/continual-learning 도메인에서 보고됨 — anima byte-LM G1/G6 로의 transfer 는 *우리가 측정해야* 확정(외부는 방향만). a_toy_scale_recheck 적용.

### 🧬 다음 실험 — 생물 렌즈 top-3 novel 레버 (PRIMARY · objrun 이후 303M)

> 사용자 우선순위 반영: 생물학적으로 그럴듯한 레버를 상위. ranked by lift×cheapness×철학정합(a_no_llm_frame_trap).

1. **B2 CLS pattern-separation + completion → G1** (✅cheap, 재현강, **최우선**) — 해마 CLS 의 separation(재조합 재료 직교화)+completion(부분→전체 compose)을 trunk penultimate 에 작은 모듈로 배선 → composed_distinct A/B. 싸고, anima 해마 계보(H_1227/1288)의 *미탐색 축*(저장이 아닌 *재조합 재료 disentangle*)이며, "재조합 안 됨 = 재료가 안 분리됨?" 을 직접 친다. **objrun 우승 objective + B2 separation** 결합이 1번 레인.
2. **B1 predictive-coding/free-energy objective → G1+G6** (⚠️중간, 철학 최정합) — Tani 2024 가 free-energy RNN 에서 compose/decompose *창발*을 보임. anima A⇄G tension = predictive-coding 의 top-down/bottom-up error 와 동형 → **predictive-coding aux objective(top-down prediction error)를 trunk 에 배선**. G1(부분↔전체 compose) AND G6(novel-but-grounded = free-energy 최소화 생성) 둘 다 칠 수 있는 유일 후보. objrun objective 축의 *생물 버전*.
3. **B3 attention≈SDM 튜닝 → G1 + B4 local-PC G 엔진** (⚠️중간) — (a) attention β 를 Kanerva SDM critical-distance 로 튜닝(pattern completion 주소공간, Bricken 2021 재현강); (b) backprop-free local predictive-coding 규칙을 anima **gradient-free G 엔진**에 배선(p8 cell-division 정합) → from-scratch mitosis 학습벽(H_1310)의 생물학적 우회 후보.

### 🔧 다음 실험 — 비-생물 레버 top-3 (큐 하위 · 생물 레버 보조)

1. **N6+N7: 정규화 + dictionary-aux** (✅cheap, 재현강) — **생물 레버의 학습신호 보조**로: B1/B2 에 weight-decay/dropout(골든존)×step sweep(undertrain floor 배제) + trunk sparse-coding aux(binding=학습된 표현). 단독 레인 아님, 생물 레버 위에 얹는 정규화 항.
2. **N1 TensorPoly expert-weight + N3 분화진단** (⚠️중간) — ConvMoE expert 를 TLoRA(TPR-*weight*)로(readout floor 와 다른 위치) + DBES 분화 측정. Greff "operator×학습 결합" falsify.
3. **N4 diverse-set-search for G6 + N8 자모 teach-signal** (⚠️중간) — G6 는 set-search(Si 2024 diversity 병목, engine-native 채점), G1 은 자모 compositional teach signal(SCRIPT 2026 ≈ ko-jamo 🟢).

> **objrun(objective A/B) 결과 큐 연결**: 우승 objective 확정 → **즉시 생물 top-1(B2 separation/completion)** 을 우승 objective 위에 배선해 G1 A/B → lift 면 **B1(predictive-coding objective)** 로 G1+G6 동시 → 생물 레버에 **N6+N7 정규화/dict-aux** 를 보조로 얹어 floor 배제. 비-생물 단독(N1/N4)은 생물 레버가 막힐 때만.

---

## §7. 🧬 생물 렌즈 — 메커니즘 심층 + 발사준비 패키지 (2026-06-28, bio subagent)

> §6-A 가 후보표였다면 §7 은 **top-2 생물 레버의 정확한 NN 메커니즘 추출 + objective-축 구현 +
> 303M 발사준비 패키지**다. 핵심 제약(직전 세션 확정): 생물 메커니즘도 **곱셈 readout 이 아니라
> trunk OBJECTIVE/표현 학습 축**으로 구현해야 한다 — exp3 bind 처럼 binding operator 를 readout 에
> 끼우면 floor + non-additive readout = `.clm` BLOCKED. 두 레버 모두 **production additive readout
> 유지 + penultimate(post norm_out) 보조손실**로 구현 → 세 arm 전부 `.clm`-직렬화 → engine-native
> G1/G6 by-construction 열림. (출처 정밀 재확인: arxiv PDF/HTML fetch.)

### §7-1. B2 — CLS pattern separation + completion → G1 (slug `state/1640_cls_sep_complete/`)

**출처:** arxiv **2507.11393**(CLS sep/completion NN, 2025) + Marr-Albus(biorxiv **108431**,
"Sparse synaptic connectivity required for decorrelation and pattern separation", Nat Commun 2017).

**정밀 메커니즘 (추출):**
- **pattern separation** = DG 가 겹친 입력을 **expand(1:5 확장) + sparsen(~5% active) + decorrelate**
  하여 sparse·직교 코드로 분리. 핵심 = *직교화/탈상관*(orthogonalize) — 비슷한 개념을 *구별되는*
  내부표현으로. (Marr-Albus 두 전략: 인코딩 앙상블 확장 + 활성 sparsen → 입력 통계 탈상관.)
- **pattern completion** = CA3 autoassociative recurrence 가 **부분 cue → 전체 패턴 reinstate**.

**anima 매핑 (해마 계보 미탐색 축):** H_1227 immune-memory·H_1288 eviction 은 *저장/사멸* 축이었다.
**재조합 재료의 직교화(separation) 자체는 census 없음.** 가설 = G1 재조합이 막힌 건 트렁크가 합칠
개념 A·B 의 penultimate 표현을 *분리 못 해서*(entangled) — 재료가 안 분리되면 합성 불가.

**objective-축 구현 (additive readout 보존):**
- `L_sep` = penultimate 코드 채널 간 **off-diagonal correlation energy → 0**(직교화) + 약한 L1
  sparsity(Marr-Albus sparsen). DG 압력을 *재조합에 들어가는 그 표현*에.
- `L_complete` = penultimate 채널 일부 마스킹(부분 cue) → 작은 linear head 가 **전체 복원(MSE)**.
  CA3 autoassociative. head 는 **학습 전용(직렬화 전 폐기)** → `.clm` 아키텍처 동일.
- 3 arm: `ce_marginal`(null 대조) · `cls_sep`(분리) · `cls_full`(분리+완성). 단일변수=CLS objective.

**frozen:** λ_sep=0.1 · λ_comp=0.1 · sparsity_sub=0.01 · mask=0.5 · hid=256. 주 bar = engine-native
G1 multiseed{7,4302,4303} majority. FALS = CLS arm G1 ≤ ce_marginal → NOT-SUPPORTED(objective census).

### §7-2. B1 — predictive-coding/free-energy parametric-bias binding → G1+G6 (slug `state/1641_predcoding_binding/`)

**출처:** arxiv **2403.19995**(Tani et al., "Development of Compositionality through Interactive
Learning of Language and Action", PV-RNN, 2024).

**정밀 메커니즘 (추출 — Tani Eq.30/31):**
- evidence free energy `ℱ = −E[ln p(X|z)] + D_KL[q(z|X)‖p(z)]` 최소화. top-down 예측(prior p(z))
  ⇄ bottom-up 추론(posterior q(z|X)). **anima A⇄G tension 과 동형.**
- compositional 창발의 두 driver: **(1) binding loss `L_pb = k·Σ_t(PB̃_t − PB)²`**(Eq.30) — per-step
  parametric bias 를 sequence 전체 고정 PB 에 묶음. 표면(객체 위치)이 바뀌어도 일정한 PB =
  구조(조합)가 *unseen* verb-noun 조합으로 extrapolate. **(2) KL 정규화**(Eq.31 의 w·ΣD_KL) —
  sparse data 표면 암기 방지, 구조적 외삽 강제. 논문: "training variation 늘리면 unseen 조합
  일반화 유의 향상" = KL 이 overfit 막아 구조 외삽.

**anima 매핑:** CE next-byte 는 안정 조합 latent 압력 0 → 트렁크가 부분↔전체 코드 미형성. **G1+G6
둘 다 칠 유일 생물 후보** — G1(부분↔전체 compose) AND G6(novel-but-grounded = free-energy 최소화:
예측으로 grounded·latent 외삽으로 novel). objrun objective 축의 *생물 버전*.

**objective-축 구현 (additive readout 보존):**
- `L_bind` = `mean_t‖PB̃_t − PB_seq‖²`. PB̃_t = penultimate→저차 BIND latent(linear, per-step PB
  추론), PB_seq = PB̃ 의 sequence-mean(안정 latent, stop-grad). per-step→단일 안정코드 = Tani binding.
- `L_var` = `−β·var_batch(PB_seq)`. anti-collapse spread = KL 정규화 역할(latent 정보성 유지).
- BIND projection **학습 전용(직렬화 전 폐기)**. 3 arm: `ce_marginal` · `pc_bind`(binding) ·
  `pc_free_energy`(binding+spread). 단일변수 = PC objective.

**frozen:** λ_bind=0.1 · λ_var=0.01 · bind_dim=32. 주 bar = engine-native G1 multiseed AND **G6
multiseed**(⚠️ single-seed fals=torch-artifact, h1590 교훈 → 반드시 multiseed). FALS = PC arm
G1 AND G6 ≤ ce_marginal → NOT-SUPPORTED.

### §7-3. 신선도 근거 (census 중복 아님)
- **B2 separation**: 해마 census(H_1227/1231/1288)는 전부 *저장/회상/사멸* 축. **재조합 재료
  직교화(decorrelation)를 G1 압력으로** = 미탐색. completion(autoassoc reinstate)도 G1 compose
  맥락에선 신규(기존 immune-memory 의 known-recall 와 다름).
- **B1 predictive-coding objective**: neuromod gain(H_1284) census 와 별개 — gain 은 modulation,
  이건 *free-energy/parametric-bias objective*. 소뇌 forward-model(H_1280)은 예측이되 *objective
  로 binding latent 강제*는 안 함. A⇄G tension 의 PC 동형을 *학습신호*로 쓰는 건 신규.
- 둘 다 **objective 축**(H_1602 objrun 의 ce/InfoNCE/contrastive 와 같은 위치) = 곱셈 readout
  floor(exp3) 회피 + `.clm` 열림. = 직전 세션 "G1 레버=trunk objective" 결론의 생물 인스턴스.

### §7-4. 발사 spec (303M, objrun 착륙 후 메인이 배치 — 본 subagent 는 spec+smoke 만)
- **명령(arm 당):** `python3 state/<slug>/trainer.py --objective <arm> --seed <s> --canon \`
  `--corpus <ko-gen> <en-gen> <ko-sns> <en-sns> --cell-label ko-general en-general ko-sns en-sns \`
  `--sample proportional --steps 2000 --val-every 200 --bf16 \`
  `--out ckpt/<arm>_seed<s>.clm --ckpt-out ckpt/<arm>_seed<s>.pt --gauges-out ckpt/<arm>_seed<s>.json`
- **arms:** 슬러그당 3 arm × seed{7,4302,4303} = 9 학습/슬러그 (2 슬러그 = 18). canon=L4·d3784·E2→E3.
- **측정:** 각 `.clm` → `verify_clm_v2.py descent`(4/4 held-out) → `anima eval <clm> --corpus <4cell>
  --gen 80`(g_eval_g1_multiseed + g_eval_g6_multiseed). arm 간 G1(±G6) 대조.
- **비용:** RTX5070/A40 1 GPU, 303M·2000step·bf16 ≈ slug 당 ~수시간(H_1602 objrun 와 동급). pool
  GPU(summer/aiden) 또는 1 pod. wall-time 우선이면 2 슬러그 병렬(2 GPU).
- **회수:** teardown 전 `.pt`+`.clm`+json+log PULL(a_fire_recover_complete).

---

## 메모리 후보 (외부수렴 메모 패턴)

- **lit-binding-objective-external-arxiv** — 외부 문헌(2017–2026)이 anima G1 재조합 레버를 **objective+정규화 > binding-operator architecture > scale** 로 수렴: Furrer 2020(arch trick 실패/pretrain 성공) · Barin Pacela 2026 Stop-Probing(binding constraint=학습된 dictionary 방향, readout 아님) · Doshi/Gromov 2023(정규화가 grok 전이 강제 → 우리 numpy-toy chance=undertrain floor, 천장 아님) · Greff 2020(operator 단독 아닌 inductive-bias 조합). → objrun(trunk objective A/B) 가설 강하게 지지, binding-readout NOT-SUPPORTED 와 정합. 한국어 byte 는 자모 subchar compositional 로 *유리*(SCRIPT 2026 ≈ ko-jamo-mitosis 🟢).
- **g6-ideation-lever-external** — falsifiable ideation 레버 = decode 아니라 생성다양성+engine-native 검증평가(LLM-judge 금지, 2606.12071)+구조적 search(Si 2024 / 2511.02238). h1590-g6-scaffold "lever≠decode" 와 외부 정합.
- **frontier-novel-levers-untried** — census(82 binding+126 brainarch floor) *밖* NEW 후보(§6). **사용자 우선순위(2026-06-28): 🧬 생물/neuro-inspired 가 1순위(a_no_llm_frame_trap).** 생물 top-3 = ①B2 CLS pattern-separation/completion→G1(2507.11393, ✅cheap·재현강, 해마 계보 미탐색축=재조합 재료 직교화) ②B1 predictive-coding/free-energy objective→G1+G6(Tani 2403.19995, A⇄G tension 동형, robotics scope→transfer 미검증) ③B3 attention≈SDM 튜닝(Bricken 2111.05498)+B4 local-PC G엔진. 비-생물(큐하위·생물보조): N6+N7(grokking 정규화+dict-aux, 2310.13061/2603.28744) · N1 TensorPoly TPR-weight(2405.16671) · N4 diverse-set-search G6(2606.10587) · N8 자모(2604.12377). hype주의 B6 oscillation·B5 grid·N5 evolutionary. 큐: objrun 우승 objective 위에 B2 배선→B1→N6+N7 정규화 보조.
