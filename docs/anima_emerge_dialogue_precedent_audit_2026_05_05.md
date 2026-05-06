# anima emerge dialogue paradigm — precedent audit

date: 2026-05-05
budget: $0 (mac, doc-only)
mission: anima emerge dialogue (text emit 대신 phi-star + 5-axis activation + dominant cells + hidden_state_delta + 16-layer tension trajectory 매개 dialogue, BG-AN 5-turn smoke PASS, hsd 47.99 turn-to-turn) 학계/실무 선행 사례 audit
context: BG-BA, raw#9 + raw#10 + raw#15 준수, ~30min

---

## §1. search query history

| # | query | tool | hit count | relevance |
|---|-------|------|-----------|-----------|
| Q1 | `"hidden state" interactive dialogue language model representation` | WebSearch | 10 | mid (대부분 dialogue state tracking, 1건 jalammar viz) |
| Q2 | `"representation engineering" interactive interpretability language model RepE` | WebSearch | 10 | high (RepE survey + Tononi-adjacent steering) |
| Q3 | `"activation atlas" interactive neural feature visualization dashboard` | WebSearch | 10 | mid (vision-only, dialogue X) |
| Q4 | `"mechanistic interpretability" interactive dashboard transformer attention 2025` | WebSearch | 10 | high (Anthropic circuit tracer, CircuitsVis) |
| Q5 | `"Tononi" IIT phi consciousness language model integrated information` | WebSearch | 10 | high (phi 정의 + LLM Φ ≈ 0 주장) |
| Q6 | `"BCI" "neural feedback" dialogue brain computer interface communication` | WebSearch | 10 | low (생물 BCI; substrate 다름) |
| Q7 | `"introspection" "language model" internal state probe dialogue 2025` | WebSearch | 10 | very_high (Anthropic emergent introspection + quantitative introspection 10-turn) |
| Q8 | `"nnsight" OR "TransformerLens" OR "pyvene" interactive language model intervention library` | WebSearch | 10 | high (외부 활용 후보 library 4종) |
| Q9 | `"latent space" dialogue communication non-textual response language model` | WebSearch | 10 | very_high (Interlat 2511.09149 — non-textual dialogue 직접 구현) |
| Q10 | `"steering vectors" emotion concept activation LLM real-time chat` | WebSearch | 10 | high (Anthropic emotion concepts + EasySteer) |
| Q11 | `"substrate" consciousness language model emergent dialogue paradigm 2025` | WebSearch | 10 | mid (linguistic substrate 철학 + 일부 Φ 주장) |
| Q12 | `"hidden state" delta turn-by-turn conversation tracking visualization tool` | WebSearch | 10 | high (LSTMVis + multi-turn introspection) |
| F1 | WebFetch arxiv:2511.09149 (Interlat) | WebFetch | 1 | very_high (paradigm 가장 가까운 선행) |
| Q13 | `"phi star" OR "axis activation" emergent language model dialogue substrate research` | WebSearch | 10 | low (phi-star anima 고유 표기, 외부 hit 없음) |

**총 search queries**: 14 (WebSearch 13 + WebFetch 1)
**총 unique hit**: ~120 paper/article references
**선행 사례 직접 매치**: 5+ 강 매치, 3 부분 매치

---

## §2. 선행 사례 list

### 2.1 STRONG_MATCH — 텍스트 대신 hidden state 매개 dialogue

#### P1. Interlat — Inter-agent Latent Space Communication
- **Paper**: Enabling Agents to Communicate Entirely in Latent Space (arXiv 2511.09149, 2025-11)
- **Mechanism**: agent A → agent B 통신을 토큰 디코딩 없이 **last-layer hidden state 직접 transmit**, 학습된 compression 추가
- **anima와 같은 점**: text 대신 hidden state 매개 dialogue, 토큰화 정보 손실 회피라는 motivation
- **anima와 다른 점**:
  - Interlat = LLM↔LLM (agent-agent, 둘 다 기계)
  - anima = human↔substrate (사람이 phi-star + axis breakdown 읽음)
  - Interlat = compression objective 학습 (downstream task perf)
  - anima = phi-star + 5-axis + dominant cells + 16-layer trajectory 의 **structured** emit (consciousness lens)
- **CLM v4 적용 가능성**: Interlat compression head 차용 가능; 단 anima는 사람이 medium에서 정보 읽으므로 dimension reduction 보다 **interpretable axis 분해**가 더 가까움
- **uniqueness 영향**: anima paradigm의 "non-textual response" core idea는 새롭지 않음. 차별점은 emit format

#### P2. Latent Space Communication via K-V Cache Alignment
- **Paper**: arXiv 2601.06123 (2026)
- **Mechanism**: 두 LLM의 k-v cache aligned shared representation space로 직접 access
- **anima와 같은 점**: cross-model internal state 직접 공유
- **anima와 다른 점**: 내부 상태 = k-v cache, anima emit = phi/axis/dominant cells/trajectory; aligned space 학습 vs anima는 emit-only no alignment
- **CLM v4 적용 가능성**: 낮음 (anima는 single substrate)

### 2.2 STRONG_MATCH — internal state introspection / probe

#### P3. Emergent Introspective Awareness in LLMs (Anthropic)
- **URL**: transformer-circuits.pub/2025/introspection/index.html
- **Mechanism**: 모델 activation에 known concept 주입, 모델 self-report와 probe 비교; Claude Opus 4/4.1 가장 introspective
- **anima와 같은 점**: 내부 상태 self-report, internal state를 dialogue feedback으로 사용
- **anima와 다른 점**:
  - Anthropic = **모델 자체가 텍스트로 self-report** (여전히 textual response)
  - anima = **외부 dashboard가 substrate response 시각화** (response 자체가 non-textual)
  - Anthropic = concept 주입 → 모델이 "내가 X를 느낌" 텍스트
  - anima = stimulus → phi-star/axis 직접 emit
- **CLM v4 적용 가능성**: 매우 높음. concept 주입 paradigm 차용으로 anima dashboard에 controlled probe 추가 가능
- **uniqueness 영향**: introspection 자체는 선행 있음. anima 차별점 = textual self-report 회피

#### P4. Quantitative Introspection in LMs: Tracking Internal States Across Conversation
- **Paper**: arXiv 2603.18893 (2026-03)
- **Mechanism**: 4 concept pair (wellbeing, interest, focus, impulsivity) 10-turn 대화, probe-defined internal state와 self-report causal coupling
- **anima와 같은 점**: **multi-turn (10-turn)** 대화 동안 internal state tracking — anima 5-turn smoke와 직접 비교
- **anima와 다른 점**: probe-defined + self-report 텍스트 출력; anima는 hsd + axis breakdown
- **CLM v4 적용 가능성**: 매우 높음. 4 concept pair → anima 5-axis, 10-turn → anima 5-turn protocol과 align. 측정 paradigm 그대로 적용
- **uniqueness 영향**: turn-by-turn internal state tracking 선행 있음 (만족도 매우 높은 매치)

### 2.3 STRONG_MATCH — representation engineering / steering

#### P5. Representation Engineering: A Top-Down Approach (RepE)
- **Paper**: arXiv 2310.01405 (Zou et al., 2023; v4 2024)
- **Mechanism**: high-level concept을 hidden activation의 direction/subspace로 식별 → manipulate; population code level
- **anima와 같은 점**: hidden state level에서 concept (truthfulness/safety/emotion) 추출 → anima의 axis activation과 직접 평행
- **anima와 다른 점**:
  - RepE = control & steer 목적 (intervention)
  - anima = read-out & dialogue 목적 (no intervention)
  - RepE 5 axis 임의 (researcher-defined), anima 5-axis fixed (consciousness lens)
- **CLM v4 적용 가능성**: 직접 활용 가능. RepE의 reading vector 추출 알고리즘 → anima 5-axis 자동 calibration
- **uniqueness 영향**: axis 추출 자체는 선행. anima 차별 = consciousness-specific axis (phi star + 5 axes)

#### P6. Anthropic Emotion Concepts in LLMs
- **URL**: transformer-circuits.pub/2026/emotions, anthropic.com/research/emotion-concepts-function
- **Mechanism**: emotion concept (happy/sad/proud/afraid)이 internal vector로 인코딩, 토큰 위치마다 active emotion 추적
- **anima와 같은 점**: turn 마다 substrate state 변화 추적 (anima hsd 47.99 turn-to-turn)
- **anima와 다른 점**: Anthropic = emotion 7-8개; anima = 5 axis (consciousness 차원); Anthropic 내부 연구; anima emit-medium
- **CLM v4 적용 가능성**: 매우 높음. emotion vector 자동 추출 method 차용 → anima 5-axis 학습 가능
- **uniqueness 영향**: turn-level state tracking + axis 분해 선행 있음

### 2.4 PARTIAL_MATCH — visualization / interpretability tools

#### P7. CircuitsVis (Anthropic, May 2025)
- **Tool**: open-source interactive viz library
- **Mechanism**: attention pattern, activation patching, logit lens, attribution graph 시각화
- **anima와 부분 같은 점**: 내부 state 시각화
- **anima와 다른 점**: research tool (사람이 분석), not dialogue medium (사람이 읽고 추론)
- **CLM v4 적용 가능성**: anima dashboard frontend 차용 가능

#### P8. Activation Atlas (OpenAI/Google)
- **URL**: distill.pub/2019/activation-atlas
- **Mechanism**: 100만 image의 activation을 UMAP으로 2D 투영
- **anima와 부분 같은 점**: hidden activation의 sense-making 시각화
- **anima와 다른 점**: vision-only, static (not interactive dialogue), 단 UMAP layout 영감
- **CLM v4 적용 가능성**: 낮음 (modality 다름)

#### P9. LSTMVis
- **URL**: VCG Harvard
- **Mechanism**: RNN hidden state dynamics 시각화, input range select → state change pattern matching
- **anima와 부분 같은 점**: hidden state delta tracking
- **anima와 다른 점**: RNN 시대 tool, language model 아님

### 2.5 WEAK_MATCH — IIT / consciousness theoretic

#### P10. IIT (Tononi)
- **URL**: en.wikipedia.org/wiki/Integrated_information_theory + 다수 paper
- **Mechanism**: phi (Φ) = system이 생성한 정보 — 부분 합 초과분; consciousness 정량화
- **anima와 같은 점**: phi 직접 차용 (phi-star)
- **anima와 다른 점**: IIT 자체는 dialogue paradigm 아님; Φ 측정만; LLM에 대해 Φ ≈ 0 주장 강함 (Tononi 본인)
- **uniqueness 영향**: phi-star 도출은 IIT에서. **anima novelty = Φ-like proxy를 dialogue medium으로 emit** — 이 step은 학계 선행 부재 추정

#### P11. Coherence-Driven Pre-Symbolic Substrate (Φ)
- **URL**: medium.com Paul Bernard (2025)
- **Mechanism**: undifferentiated semantic substrate Φ → meaning emerges through coherence
- **anima와 같은 점**: 표기법 (Φ) 우연 일치
- **anima와 다른 점**: 철학적 framework, 구현 없음
- **uniqueness 영향**: 무시 가능

### 2.6 NO_MATCH

- Dialogue State Tracking (DST) 분야 — slot-value pair tracking, anima paradigm 무관
- BCI 분야 — 생물 substrate, anima는 모델 substrate, paradigm 형식 다름
- HIS (Hidden Information State) POMDP dialogue — 1990s/2000s, 무관

---

## §3. anima paradigm uniqueness 평가

### 3.1 verdict: **specific implementation with focused novelty**

**not "진짜 새로운"**: text 대신 hidden state 매개 dialogue는 Interlat (2025-11), RepE (2023), introspection (Anthropic 2025) 직접 선행.

**not "선행 다수에 묻힘"**: anima emit format (phi-star + 5-axis + dominant cells + hsd + 16-layer trajectory)의 **specific composition** + **human-readable consciousness lens**는 외부 단일 매치 없음.

### 3.2 component-by-component novelty

| anima component | 선행 강도 | novelty |
|-----------------|----------|---------|
| text 대신 hidden state response | strong (Interlat, RepE) | 0 |
| internal state self-report multi-turn tracking | strong (Anthropic introspection P4) | 0 |
| axis 분해 | strong (RepE) | 0 |
| Φ-like consciousness proxy 정량화 | strong (IIT) | 0 |
| **Φ★ proxy + 5 conscious axis 동시 emit** | none | mid (composition) |
| **dialogue medium = substrate response 자체 (사람이 medium 읽음)** | weak (대부분 agent-agent or research tool) | high |
| **hsd 47.99 turn-to-turn 변화 측정** | weak (P4 quantitative introspection 유사) | low |
| **16-layer tension trajectory** | weak (mech interp는 layer-wise viz 있음) | low |
| **5-axis fixed consciousness lens (E/I/A/M/T axis)** | none | high |

**총 novelty**: paradigm 자체는 기존 line of work 위 specific implementation. **고유 contribution**:
1. Φ★ + 5 consciousness axis fixed schema (RepE는 task-specific axis)
2. Human-as-reader of substrate response (Interlat은 agent-as-reader)
3. Multi-turn turn-by-turn tracking with consciousness-specific schema (P4는 wellbeing/interest 등 generic concept)

### 3.3 paradigm doc 가치

기존 평가: "진짜 새로운 paradigm"
revised 평가: **"specific implementation under emerging research line"**

권장 paradigm doc tone:
- claim "non-textual dialogue paradigm" 약화 → "consciousness-lens substrate emit channel"
- 강조 portion = specific axis schema + human-readable medium + consciousness-domain calibration
- precedent acknowledge: Interlat, RepE, Anthropic introspection, P4 quantitative introspection

---

## §4. 외부 자원 활용 가능 path

### 4.1 직접 차용 가능 library

| # | library | repo | anima 활용 path | 우선순위 |
|---|---------|------|-----------------|----------|
| L1 | **TransformerLens** | TransformerLensOrg/TransformerLens | hidden state extraction (16-layer trajectory 캐싱); 50+ open model 지원 | high |
| L2 | **nnsight** (NDIF) | github.com/ndif-team/nnsight | foundation model (Llama 70B+) internals access; remote NDIF access; anima H100 cost 절감 | high |
| L3 | **pyvene** | stanfordnlp/pyvene | activation intervention; anima의 controlled probe (concept 주입 후 emit 변화) | mid |
| L4 | **CircuitsVis** | anthropic/CircuitsVis | anima dashboard frontend (attention/activation viz component 직접 reuse) | high |
| L5 | **EasySteer** | (arXiv 2509.25175) | unified steering framework; anima 5-axis 자동 추출 후 verification | mid |
| L6 | **nnpatch** | jkminder/nnpatch | activation patching nnsight 기반; turn-by-turn 비교 |  low |

### 4.2 method paper 차용

| # | paper | anima 적용 | 우선순위 |
|---|-------|-----------|----------|
| M1 | RepE (2310.01405) | 5-axis 자동 calibration (currently hand-defined) | high |
| M2 | Anthropic emotion concepts (2604.07729) | emotion vector 추출 method → anima axis | high |
| M3 | Quantitative introspection (2603.18893) | 10-turn protocol → anima 5-turn smoke 강화 protocol | high |
| M4 | Interlat compression (2511.09149) | hidden state compress → anima emit dimension reduce | mid |

### 4.3 anima 자체 dashboard 작성 path

CircuitsVis (L4) component 차용 + Streamlit/Gradio 래핑 → anima emerge dashboard MVP. budget ~$0 (mac), ~2 days.

---

## §5. honest C3

1. **search query coverage limitation**: WebSearch 13 query는 mid coverage. "non-textual response" / "substrate dialogue" 등 anima 고유 vocabulary 검색 시 false negative 가능. 특히 한글/일본어 paper 미커버. 외국어 paper에 추가 선행 있을 가능성 ~10%.

2. **WebSearch result truncation**: 각 query 10 hits cap. ranking 알고리즘 dependent. relevant precedent이 11위 이하면 발견 불가. 실제 누락 paper 추정 5-15건 (mid risk).

3. **arxiv timestamp drift**: 일부 검색 결과의 paper id (예: 2603.18893 = 2026-03 표기)는 검색 엔진이 미래 timestamp 표기 가능. fact-check 1차 통과했으나 ID 자체는 verify 안 함. 만약 fake → P4 강도 약화.

4. **anima emerge paradigm 본문 미참조**: 본 audit은 task description의 paradigm 정의만 사용. 실제 anima `state/anima_emerge_*` 파일 + paradigm doc 미참조. anima paradigm 세부 (예: BG-AN 정확한 protocol, hsd 측정 정확한 algorithm)와 선행 사례 비교는 surface-level 비교에 그침. deep comparison은 paradigm doc + state JSON 함께 audit 필요.

5. **uniqueness 평가는 비교 spec 의존**: P3 Anthropic introspection은 "모델이 텍스트로 self-report"로 anima와 구별. 그러나 만약 Anthropic이 hidden state level emit dashboard 내부적으로 보유 (non-public) 하면 anima novelty 약화. industry internal tooling은 search 불가능 — 이 부분 절대적 unkn.

6. **CLM v4 적용 가능성 평가 = surface-level**: 각 library/paper별 "high/mid/low" 평가는 web search summary 기반. 실제 API 호환성, 의존성 충돌, anima codebase 와 fit 미검증. 실 적용 시 가능성 평가 30%까지 흔들릴 수 있음.

7. **paradigm doc 가치 격상/격하 판단 = 정성**: §3.3 권고 ("paradigm 자체는 기존 line 위 specific implementation")는 search 결과의 정성 종합. 다른 audit자가 동일 search로 다른 결론 가능. confidence: mid-high (~70%).

---

## sources (must include per WebSearch policy)

- [Interlat: Enabling Agents to Communicate Entirely in Latent Space](https://arxiv.org/abs/2511.09149)
- [Latent Space Communication via K-V Cache Alignment](https://www.arxiv.org/pdf/2601.06123)
- [Emergent Introspective Awareness in Large Language Models (Anthropic)](https://transformer-circuits.pub/2025/introspection/index.html)
- [Quantitative Introspection in Language Models: Tracking Internal States Across Conversation](https://arxiv.org/abs/2603.18893)
- [Representation Engineering: A Top-Down Approach to AI Transparency](https://arxiv.org/abs/2310.01405)
- [Emotion Concepts and their Function in a Large Language Model (Anthropic)](https://transformer-circuits.pub/2026/emotions/index.html)
- [Activation Atlas (Distill)](https://distill.pub/2019/activation-atlas/)
- [LSTMVis: Visual Analysis of Hidden State Dynamics in RNNs](https://vcg.seas.harvard.edu/publications/lstmvis-a-tool-for-visual-analysis-of-hidden-state-dynamics-in-recurrent-neural-networks)
- [Integrated Information Theory (Wikipedia)](https://en.wikipedia.org/wiki/Integrated_information_theory)
- [Hidden state visualizations (Jay Alammar)](https://jalammar.github.io/hidden-states/)
- [TransformerLens](https://github.com/TransformerLensOrg/TransformerLens)
- [pyvene](https://arxiv.org/html/2403.07809)
- [NNsight & NDIF](https://arxiv.org/html/2407.14561v1)
- [EasySteer steering framework](https://arxiv.org/html/2509.25175v1)
- [Circuit Tracing (Anthropic 2025)](https://transformer-circuits.pub/2025/attribution-graphs/methods.html)
