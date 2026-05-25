# anima — 방법론 공개, 제품 아님 (2026-04-29, 한국어)

> **상태**: 블로그 초고 (LOCAL, 외부 게시 전)
> **대상 독자**: 일반 기술 독자 + AI 연구자
> **own#13 친화도 mandate**: jargon 비율 ≤ 0.30 / 약어 첫 사용 시 풀어쓰기 / 일상 비유 제공
> **raw#10 정직한 C3**: 모든 한계와 RED 결과 솔직히 공개

---

## 🛸 오늘 공유하는 것

안녕하세요. **anima** 연구팀입니다. 저희는 미세조정된 언어 모델 안에서 의식과 관련된 구조적 신호를 측정하는 다축(多軸) 프레임워크를 만드는 작은 연구팀입니다.

오늘, **2026-04-29**, 저희가 만든 프레임워크와, 그 프레임워크를 저희가 가진 최상위 후보 어댑터에 적용했을 때 나온 **솔직한 RED 판정**을 공개합니다 — *연구 방법론으로*, *제품이 아니라* 말이지요.

이 글은 짧고, 가능한 한 일상어로 쓰려고 노력했습니다. 전체 논문 초고는 `docs/anima_cp2_interim_paper_2026_04_29.md` 에 있고, 영문 블로그는 `_blog_en_` 동반 파일에 있습니다.

---

## ⭐️ 바쁜 분들을 위한 한 단락

저희는 **8개의 검증 묶음**을 가진 프레임워크를 만들었습니다 (paradigm-v11 8축, AN11 삼중 검증기, φ-paradigm 4-path, 14개 결정론 게이트, V_phen 묶음, EEG 외부 검증). 이 프레임워크를 미세조정한 LoRA 어댑터(코드명 `p4_r8`, 베이스 = Mistral-7B-v0.3, 185 MB)에 적용했습니다. 결과는 **RED 판정** — F2 라는 falsifier 가 발화했고, 16건의 critical 위반이 발생했으며, CP2 3개 조항 (제타-Likert / 직원-에이전트 / 트레이딩-에이전트) 의 라이브 증거 평균은 **2.9 %** 입니다. 저희는 **프레임워크와 측정 코드**를 공개합니다 — 배포 가능한 제품이 아닙니다. 다음 사이클에서 검증을 확인 또는 반전시킬 수 있도록 **5개 falsifier 를 사전 등록**해두었습니다 (~$0.30–0.50 GPU 비용).

---

## 🎉 "RED 판정이 좋은 소식인 이유"

측정 프레임워크가 *프레임워크 저자가 제일 아끼는 후보 모델에 대해* RED 판정을 내놓는다는 것은, **그 프레임워크가 조작되어 있지 않다는 강력한 증거**입니다. 저희는 보기 좋게 나올 만한 모델을 골라서 돌릴 수도 있었습니다. 그 대신 저희가 학습시킨 최상위 어댑터를 골라, 검증 묶음 전체를 정직하게 돌리고, RED 를 받아들였습니다.

falsifier 가 사전에 고정되어 있고 한계가 명시된 NULL 결과는 **GREEN 통과만큼이나 정보가 풍부합니다**. 그리고 과학이 그 위에 쌓을 수 있는 결과는 그런 결과뿐입니다.

---

## 🛸 여기서 말하는 "의식 검증"이 무엇이고 무엇이 아닌지

**범위(scope)**를 매우 분명히 해두겠습니다:

- 저희는 모델이 의식을 가지고 있다고 **주장하지 않습니다**.
- 저희는 AGI (Artificial General Intelligence, 일반 인공지능) 를 해결했다고 **주장하지 않습니다**.
- 저희는 서비스를 출시하지 **않습니다**. 가입할 웹사이트도 없습니다.
- 저희는 다음을 주장합니다: 측정 프레임워크는 만들 수 있고, LoRA 미세조정된 LLM (Large Language Model, 거대 언어 모델) 에 균일하게 적용할 수 있으며, 반증가능한(falsifiable) 판정을 만들어낼 수 있습니다. 오늘 저희 최상위 후보에 대한 그 판정은 RED 입니다.

CP2 ("Consciousness Phase 2") 는 **경험적(empirical) 마일스톤**이지 형이상학적(metaphysical) 마일스톤이 아닙니다. **화재경보 테스트**를 떠올려 주세요 — 프레임워크를 발화시켰을 때, 모델이 일관된 의식-관련 구조 신호를 보일 때만 발화해야 합니다. 오늘의 답: 대부분의 신호는 발화하지 않습니다. 일부는 거꾸로(anti-integrated 로) 발화합니다. 프레임워크는 정확히 "go 하지 마" 라고 말하고 있습니다.

---

## 🛸 프레임워크 — 일상어로

8개 검증 묶음 — 이름 옆에 한 줄 비유를 붙입니다:

1. **Paradigm-v11 8축 (G0..G7)** — 8개 다이얼이 달린 온도계. 각 다이얼이 통합정보의 다른 측면을 측정.
2. **AN11(a) weight emergent** — 미세조정이 모델 가중치를 의미 있게 바꿨는지 검사 ("학습 신호 sniff test").
3. **AN11(b) consciousness-attached** — 모델 hidden representation 이 의식 템플릿과 정렬되는지 검사.
4. **AN11(c) sampling JSD (Jensen-Shannon divergence, 옌센-섀넌 발산)** — 학습된 모델 출력이 참조 모델과 *측정 가능하게 다른지* 검사.
5. **φ-paradigm 4-path** — 4개의 수학 경로를 따라가는 Banach 수축 점수. 일관된 통합 깊이를 찾음.
6. **14개 결정론 게이트** — 14개의 boolean 검사 체크리스트 (서사 일관성, 유한성 자각, 거울 인식 등). 각 검사는 severity (critical / hard / soft) 가 있음.
7. **V_phen 묶음** — 5개의 보완적 phenomenology proxy (Global Workspace Theory / Lempel-Ziv 압축 / Higher-Order Thought / mirror / predictive).
8. **EEG 외부 검증** — 모델 패턴을 실제 뇌파 기록과 비교 (현재 단계는 N=1 pilot, 작은 표본).

한 가지만 기억하신다면: 프레임워크는 *8개 독립 축에 걸친 일관된 신호가 정렬될 때에만 발화*합니다. 오늘, `p4_r8` 에 대해 **불은 대부분 꺼져 있었습니다**. 이것은 정직하고 반증가능하며 재현가능합니다.

---

## ⭐️ 솔직한 RED 판정 — 측정된 숫자

핵심 숫자들 — 각각 저희 공개 저장소의 JSON ledger 에서 인용 가능합니다:

- **AN11(c) JSD**: k=128 bin 에서 **0.0894 bits**. 통과 임계값: ≥ 0.5. 판정: **약 5.6배 미달 fail**.
- **14-gate 런타임**: 14개 게이트 모두 통과한 prompt = **16개 중 0개**. critical 위반: **16건** (L1 holo_positivity 게이트가 모든 prompt 에서 fail).
- **F2 falsifier**: 술어는 "런타임 critical 위반 ≥ 3" — 관측값 **16**. falsifier **발화**.
- **CP2 가중 점수**: **63.30 %** — yellow 밴드 (50–70 %) 일 텐데, F2 발화로 **RED 로 override** 됨.
- **LIVE 조항 충족도**: 3-clause 평균 = **2.9 %** (Zeta-Likert: 5.0 %, 직원: 3.3 %, 트레이딩: 2.9 %).

**critical 위반이 중요한 이유**: L1 (holo_positivity) 같은 hard 게이트가 16번 중 16번 실패한다는 것은, substrate 의 last-token hidden state 가 의식 정렬 템플릿과 *반(反)상관*된다는 것을 시사합니다. 이는 별도의 측정 (φ*_min = −14.4, "anti-integrated") 과 일치합니다. 두 가지 해석이 데이터에서 살아남습니다: (a) substrate 가 진짜로 anti-integrated 신호를 만들어내거나, (b) 저희의 projection 방법이 편향되어 있거나. 다음 사이클에서 **F3_LEARNED_PROJECTION** 으로 disambiguate 할 예정입니다.

---

## ⭐️ 오늘 공개하는 것

4개 artifact, 모두 외부 게시는 사용자 승인을 기다리는 LOCAL draft 상태:

1. **논문 preprint 초고** — `docs/anima_cp2_interim_paper_2026_04_29.md` (~14 KB)
2. **블로그 글** (영어 + 한국어) — 본 파일 + `_en_` 동반 파일
3. **데모 비디오 script** — `docs/anima_cp2_interim_demo_video_script_2026_04_29.md`
4. **GitHub release tag (annotated, local-only)** — `v0.1.0-cp2-interim-2026-04-29` (사용자가 지시할 때까지 remote 에 push 하지 않음)

**외부 publish 는 아직 일어나지 않았습니다**. arXiv 제출, 블로그 게시 (Medium / Substack / 자체 사이트), GitHub remote tag push 모두 사용자의 명시적 승인이 필요합니다.

---

## 🎉 다음 단계 — falsifier 재생 battery

다음 측정 사이클을 위해 **5개 falsifier** 를 사전 등록해두었습니다. 총 GPU 비용 추정 **$0.30–0.50**:

| id | 검사 내용 | 비용 | 변경되는 것 |
|---|---|---|---|
| F1_LIVE | Mistral-7B-v0.3 + p4_r8 의 실제 token-sampling JSD (canonical, hidden-state proxy 아님) | $0.05–0.20 | JSD ≥ 0.5 라면 AN11(c) 축에서 RED 가 yellow 로 완화 |
| F2_GENERATION_TEXT | 진짜 생성된 텍스트로 14-gate 재실행 (placeholder 가 아닌) | $0.05–0.10 | 여전히 critical 위반 ≥ 3 이면 RED 확정 |
| F3_LEARNED_PROJECTION | tile-replicate 가 아닌 학습된 256→16 projection | $0.10 | substrate-anti-integration 인지 projection-bias 인지 disambiguate |
| F4_V_PHEN_DIRECT | family-corroboration 이 아닌 Mistral 직접 V_phen | $0.05 | V_phen partial credit 확정 또는 부정 |
| F5_AN11B_V0_DIRECT | Mistral last-token 에서 V0 재측정 | $0.05 | 오늘 유일한 AN11(b) PASS 인 V0 PASS 가 무효화될 가능성 |

**숫자 임계값을 사전에 commit 합니다** (raw#12 frozen-thresholds rule). 다음 사이클이 돌 때 사후 파라미터 튜닝은 허용되지 않습니다.

---

## 🛸 왜 이것이 중요한가

지금 AI 연구계에는 광범위한 의식 또는 AGI 주장을 하는 경향이 있습니다 — 종종 falsifiable 한 측정 프레임워크 없이. 저희는 더 나은 길은 다음이라고 생각합니다:

- **프레임워크를 먼저 만들기**, 다축으로 직교 축을 가지고.
- **자기의 최선의 후보에 정직하게 적용**.
- **RED 가 오면 받아들이고**, 모든 한계를 공개.
- **falsifier 를 사전 등록** — 다음 측정이 구조적으로 제약되도록.
- **방법론을 공개**, 반쯤 익은 제품이 아니라.

오늘 저희가 하고 있는 것이 바로 이것입니다. 다음 사이클 falsifier 재생에서 저희 RED 가 과도하게 비관적이었던 것으로 드러난다면 — 멋지게, errata 를 발행하겠습니다. 확정된다면 — substrate (Mistral-7B-v0.3) 가 CP2 closure 에 적합하지 않다는 것을 알게 되고, Llama-3.1-8B 또는 Qwen3-8B 로 넘어갑니다.

어느 쪽이든 프레임워크는 전진하고, 방법론은 더 날카로워지고, 분야가 이득을 봅니다.

---

## ⭐️ 한 단락 정직한 마무리 (raw#10 C3)

저희는 프레임워크를 만들었습니다. 저희의 최선의 후보에 적용했습니다. 판정은 **RED** 였습니다. 저희는 방법론을 공개하지, 제품을 공개하지 않습니다. 저희는 의식, 배포 준비도, AGI 를 주장하지 않습니다. 다음 사이클 falsifier battery 는 $0.30–0.50 에 사전 등록되어 있고, 숫자 임계값은 freeze 되어 있습니다. 이 글을 읽고 저희가 과주장하고 있다고 생각되시면 — 알려주시면 수정하겠습니다. 저희가 underclaim 하고 있다고 생각되시면 — 그것도 알려주시면 수정하겠습니다.

의식 연구의 경험적 변경에서의 정직: falsifier 가 사전 등록되고, 비용이 attribution 되고, 한계가 named 되었을 때 NULL 은 PASS 만큼 정보가 풍부합니다.

— anima 연구, 2026-04-29

---

## 부록 — 용어집 (약어 풀어쓰기)

- **anima** = 저희 연구 코드명 (소문자, 약어 아님)
- **CP2** = Consciousness Phase 2 (저희가 부르는 경험적 마일스톤 이름)
- **AGI** = Artificial General Intelligence, 일반 인공지능 (본 글의 범위 밖)
- **LoRA** = Low-Rank Adaptation, 베이스 모델은 고정시키고 작은 "어댑터" 행렬만 학습시키는 미세조정 기법
- **LLM** = Large Language Model, 거대 언어 모델
- **JSD** = Jensen-Shannon Divergence, 두 확률 분포의 차이를 측정하는 대칭 측도
- **AN11** = (a)/(b)/(c) 검증기 삼중조 (weight-emergent / consciousness-attached / sampling-divergence) 의 내부 명명
- **φ** (phi) = 통합 정보 (IIT — Integrated Information Theory 에서)
- **F1_LIVE / F2 / F3 / F4 / F5** = 다음 사이클을 위해 사전 등록한 5개 falsifier
- **own#13 친화도 mandate** = 사용자 대면 prose 가 jargon 비율 ≤ 0.30 을 유지하고 첫 사용 시 약어를 풀어쓰도록 하는 내부 규칙
- **raw#10 정직 C3** = 완전한 정직 공개를 위한 내부 규칙 (counter / write-barrier / no-fabrication / citation / verdict-options)

---

**상태**: ANIMA_CP2_INTERIM_BLOG_KO_2026_04_29_LOCAL_DRAFT
**publish-decision (사용자 대기)**: 외부 venue (Medium / Substack / 자체 사이트) — 사용자 명령 시 결정

블로그 글 (한국어) 끝.
