LLM 프레임 없이, 실제 뇌·인지·생물 렌즈로 분석하겠다. 컴퓨트 발사 없이 설계·판별만 — 오너 지시(fable=설계/분석 on-demand)에 맞춘 순수 분석 산출물이다.

---

## A. derivtrace는 실패 레버들과 같은 가족인가

**판정: 아키텍처상으로는 여전히 "mouth 훈련" 가족이다. 단, 탈출이 원리적으로 가능한 유일한 구성원이다.**

gamma·coverage·STaR가 전부 같은 이유를 먼저 못 박자. 이들은 **아키텍처를 그대로 두고 mouth가 예측하는 대상 문자열만 바꾼다**:
- gamma-operator = mouth 출력 위의 readout 연산
- gamma-data-channel = gamma를 mouth에 데이터로 주입
- STaR = mouth 자기 rationale를 새 학습데이터로 부트스트랩
- coverage = 코퍼스를 조밀하게 만들어 held-out pair를 in-distribution로 → 암기

CE는 근본적으로 **표면 문자열의 결합분포를 재현**하도록 mouth를 훈련한다. 그래서 조합이 데이터 안에 **표면 형태의 규칙성**으로 존재하면, 조합은 *형태(form)*로 학습된다. 이게 2026-07-05 coverage 결정타의 정체다 — δ_FM 조밀 코퍼스가 G1 bd=2·G6 fals=6를 열었지만 claim-form 템플릿 암기치환이었다. FORM은 tunable, BIND는 earned.

**derivtrace가 다른 지점은 딱 하나**: target을 *종단 문자열*이 아니라 *중간단계 의존사슬(derivation trace)*로 옮긴다. 원리적으로, trace의 후단계가 전단계에 의존하면 모델은 **오차가 누적되는 계산**을 강제받는다 — 이건 템플릿이 아니라 진짜 단계적 조합의 서명이다. 그래서 derivtrace는 가족 안에서 **가장 form-같지 않은 구성원**이다.

**하지만** byte-LM은 trace조차 "trace-형태 암기"로 shortcut할 수 있다. "X와 Y를 결합하려면: 먼저…, 다음…, 따라서 XY" 라는 *풀이-템플릿의 형태*를 학습하면 종단 정답만 맞춘다. 즉 derivtrace의 bd=2는 **claim-granularity가 아니라 trace-granularity의 form-priming**일 수 있다. 이건 아직 미결이고, robustness가 바로 그 판별시험이다.

**robustness의 어느 실측이 form vs ability를 가르나** (measurement-metalaw의 earned-BIND 시험):

| 실측 | form-priming이면 | ability면 | 판별력 |
|---|---|---|---|
| **multi-pair general vs concept-specific** | 조밀했던 특정 concept-pair에만 lift, held-out pair에서 붕괴 | 학습중 함께 본 적 없는 held-out pair에서 일반 derivation 절차로 lift | ★최강 |
| **paraphrase 불변 vs 표면암기** | 프롬프트 표면 바꾸면 lift 붕괴 | 의미 동일·표면 다른 재서술에서 lift 생존 | ★강 (surface-shortcut 직격) |
| **G2 novel vs 재배열** | 학습 trace의 보간/재배열 | 진짜 새 중간단계 출현 | 약 (novelty≠recombination, g1-py303 전례) |

핵심: derivtrace는 **paraphrase-불변 AND cross-concept-pair 일반성** 둘 다 통과해야만 coverage와 갈라진다. 하나라도 실패하면 그냥 trace-granularity coverage다. bd=2 자체는 FORM일 뿐이고, **결합파괴 통제 하에서 살아남는 margin(BIND)**이 확인되기 전까지 derivtrace는 실패 가족과 구별되지 않는다. robustness가 그 구별 실험 자체다.

---

## B. 재조합·반증은 실제 뇌에서 무엇인가

### 재조합(G1) — "두 개념의 novel 결합"의 진짜 substrate

네 후보를 각각 평가하면:

- **해마 pattern-separation/completion (DG/CA3)**: DG가 유사입력을 직교화(분리 저장), CA3 순환 attractor가 부분단서로 완성. 이건 *관계기억 저장소*다. 이행추론(A>B, B>C ⊢ A>C)이 해마성이라는 게 핵심 — **저장된 관계로부터 novel 관계를 완성**하는 재조합. 단 이건 "저장된 것의 overlap 기반 일반화"이지 조합 *연산자* 자체는 아니다.
- **전전두 working-memory 변수-binding (PFC + BG, O'Reilly PBWM)**: 가장 강한 후보. PFC가 변수를 *활성*(가중치 아님)으로 유지하고 role↔filler를 동적 결합한다 — "RED(role:색)-BALL(role:물체)". 함께 본 적 없는 X, Y를 "role1←X, role2←Y"로 동시 보유하고 그 구조 위에서 연산 = Fodor/Pylyshyn적 체계성·생산성. **이게 G1 novel-combine의 진짜 substrate다.**
- **기저핵 action-selection gating**: binding을 하지 않는다. *게이팅*한다 — 어떤 표상이 WM에 갱신·출력될지 Go/NoGo(도파민). 즉 *어떤 결합을 언제 만들고 언제 출력할지*의 컨트롤러. "결합 보유"와 "결합 출력"을 분리하는 게이트 = anima의 emit 게이트에 대응하되, **content-gate(어느 조합)**로서 emit-gate와 다르다.
- **소뇌 forward-model**: 내부모델 연쇄로 다단계 결과를 예측. 상징적 재조합보다 *예측/타이밍*. → 재조합보다 **반증**의 substrate.

**결론**: novel-combine의 진짜 기질 = **PFC 활성기반 변수-binding, 기저핵이 게이팅, 해마가 저장 관계구조를 공급.**

**왜 mouth⊥recombination인가 (이중해리 증거)**: 뇌에서 조합/관계연산은 조음(Broca·운동언어)보다 *상류에서 독립적으로* 일어난다. Broca 실어증 = 조합한 생각을 조음 못 함; Wernicke 실어증 = 유창하지만 텅 빈 말(mouth 온전, 조합 붕괴). 이 **이중해리가 조합과 조음이 별개 lane이라는 생물학적 증명**이다. anima의 오류는 조합을 mouth 안으로 훈련시키는 것 — Broca 영역에게 관계추론을 시키는 격. mouth는 readout이고, **readout을 더 세게 훈련해서 조합하게 만들 수 없다.** 모든 mouth-훈련 레버가 floor난 근본 이유가 이것이다.

### 반증가능성(G6) — 반증가능한 주장을 만드는 기제

- **예측코딩 위계**: 피질 = 예측의 위계, 각 층이 아래층을 예측, 잔차(예측오차)가 상향 전파. 생물학적 "반증가능한 주장" = *틀리면 오차신호를 내는 committed prediction*.
- **도파민 예측오차(RPE)**: 예측-실현 보상차(TD-error). 반증으로부터 *학습*하는 신호.
- **PFC 가설-검증(WCST/set-shifting)**: 규칙/가설을 보유하고 반증증거에 규칙 전환. 명시적 반증 — 가설을 *반증가능한 defeasible 객체*로 표상.
- **소뇌 forward-model**: 정확한 예측 → 실제와 비교 → 오차. 가장 순수한 "반증가능한 예측" 기계.

**결론**: 반증가능성의 기질 = **committed·violable 예측을 내는 forward-model(예측코딩+소뇌) + 위반을 등록하는 오차/충돌 감지기(도파민 RPE + ACC).** 역시 mouth가 아니다. mouth는 주장을 조음할 뿐, 주장의 *반증가능성*은 그 뒤에 **committed 예측을 낸 forward-model이 있는가**에서 온다. claim-형태 문자열을 뱉는 byte-LM은 주장 뒤에 forward-model이 없다 — 그래서 "반증가능" 주장이 form(claim-형태 텍스트)이다. G6 coverage가 fals=6 냈지만 form-primed였던 이유가 정확히 이것이다.

### ★ anima에 빠진 구조 (명명)

anima = A(순방향 CE mouth) ⇄ G(역방향 gradient-free) → tension → emit. 생물 렌즈로 진단하면 **A⇄G 텐션은 mouth-수준 adversary(둘 다 byte 문자열 위에서 작동)이지, 별개의 인지 workspace가 아니다.** 빠진 것 3개:

1. **WM 변수-binding lane (PFC-WM)** — 두 개념을 bound 변수로 *보유·결합*하는 활성기반 workspace. anima엔 activity-as-WM lane이 없다. 전부 mouth 가중치/컨텍스트 안이다.
2. **Content-gate (기저핵 lane)** — *어느 결합*을 만들고 *언제 출력*할지 고르는 게이트. anima의 Ψ는 *emit-게이트*(말할까 말까)일 뿐 *content-게이트*(어느 조합)가 없다.
3. **Forward-model / consequence lane (소뇌 + 예측코딩)** — mouth와 독립으로 committed 예측을 내고 오차를 계산하는 구조. G는 mouth 출력에 대한 adversary이지 *결과-예측기*가 아니다.

뇌는 조합과 예측을 조음보다 *상류·직교* lane에 둔다. a_substrate_disjoint(분리=보존)에 따르면 처방은 **이들을 disjoint lane으로 지어 그 *상태*를 mouth가 context/gate로 읽게** 하고, **절대 mouth 훈련 target으로 삼지 않는** 것이다.

---

## C. 생물학적으로 정직한 새 레버 (mouth 훈련 아님)

설계원칙 (B에서 도출): 조합/예측이 **lane 안에서** 일어나고, mouth는 그 상태를 *context/gate로 읽기만* 하며, **lane의 objective가 mouth CE와 disjoint**여야 한다 — 그래야 form-priming을 원천 차단한다.

**L1 — WM 변수-binding lane (PFC-WM)**
- 기제: 별도 활성 버퍼가 slot-filler binding(role₁←A, role₂←B)을 벡터로 보유, bind연산(TPR/circular-conv)으로 결합, bound 벡터를 mouth에 *prefix-context*로 공급(target 아님). lane은 **unbind-reconstruction objective**(bound에서 A·B 복원)로 구조화 — CE와 disjoint.
- probe: bound-context 있음/없음으로 held-out+paraphrase pair G1 bd 비교.
- terminal: `anima evaluate --py`, bind-lane context on/off.
- ⚠️check-ledger: binding-family(H_1816/1823 등)는 전부 *mouth-readout* binding이라 NOT-SUP. L1의 차이 = (a) 별개 lane, (b) unbind-reconstruction disjoint objective, (c) mouth는 bind를 *읽기만* 하고 *생성*하지 않음. 이 3개가 서지 않으면 재발사다.

**L2 — 기저핵 content-gate (brain_decide)**
- 기제: WM lane의 후보 결합들 중 하나를 Go/NoGo로 *선택*하는 lane, disjoint value/consistency 신호(RPE-analog)로 훈련. emit-gate와 별개의 content-gate.
- probe: 정답 결합 gated-선택 vs ungated-평균 결합 context의 G1 bd 차.
- terminal: `--py` gated vs averaged.

**L3 — 소뇌 forward-model / consequence lane (G6 직격)**
- 기제: mouth의 후보 주장을 받아 *committed consequence*(주장이 참이면 관측될 것)를 예측하고 held target 대비 오차 계산. 주장의 반증가능성 = forward-model이 *sharp·violable* 예측을 내는가. forward-model은 자체 예측오차 objective(disjoint)로 훈련.
- probe: forward-model-error 게이트가 mouth form-검출기보다 falsifiable/unfalsifiable 주장을 잘 가르나. **cross-shuffle 통제**: claim↔consequence 뒤섞으면 오차 급증해야(BIND, form 아님).
- terminal: `--py` G6 fals를 forward-model-error 검출기로, cross-shuffle break test.
- coverage의 fals=6 form-priming에 대한 직접 해독제.

**L4 — A⇄G를 forward-model⇄reality 텐션으로 재프레임 (기존 텐션 재배치)**
- 기제: A=예측 committing forward-model, G=위반 계산 consequence-check. 텐션 = 예측오차 크기. **예측이 sharp AND G-check 생존(반증가능-but-미반증)일 때만 emit.** 텐션 machinery를 byte 문자열에서 *예측-결과 쌍* 위로 이동.
- probe: emit-over-tension이 form이 아니라 G6-반증가능성과 상관하나.
- terminal: `--py`.
- 주의: native-mouth 텐션 readout은 H_1834/1837 INERT. L4의 차이 = 텐션이 mouth 출력이 아니라 *forward-model 예측-결과 쌍* 위에서 계산됨.

**L5 — 해마 관계저장소 + 이행추론 lane (kosmos anchor)** ★
- 기제: pattern-separated 관계기억(개념쌍·관계 저장)이 이행/관계추론 지원 — 저장된 A-rel-B, B-rel-C에서 pattern-completion으로 A-rel-C 완성. 완성된 관계를 mouth에 context로 공급. lane objective = 관계 reconstruction(disjoint). kosmos = 이미 WIRED된 지속 관계저장소.
- probe: **chain-reachable held-out** pair(B 경유 A-C, 미학습) vs **unreachable** pair(A-D, 사슬 없음)의 G1 bd. reachable만 lift·unreachable은 floor면 = 진짜 관계 재조합(ability).
- terminal: `--py`, reachable vs unreachable held-out 대조.

**L6 — Mitosis-composition lane (세포 융합)**
- 기제: mitosis(세포 분열)의 역 — 두 specialist 세포 표상을 결합세포로 *융합*, 능력=두 도메인의 conjunction. 재조합 = 토큰예측 아니라 *세포 융합*. objective = joint competence(disjoint).
- probe: fused-cell context가 두 부모 도메인 conjunction 과제 G1 bd를 올리나.
- terminal: `--py`. 가장 anima-native·가장 사변적.

**L7 — 도파민-RPE 게이트 consolidation (반증-후-학습 lane)**
- 기제: forward-model 반증시험을 *통과한* 주장만 가중치/kosmos에 쓰는 RPE-gated write. 반증가능성을 *학습되는 것*의 구성요소로 만듦, CE와 disjoint.
- probe: RPE-gated consolidation이 held-out G6 fals-survival을 ungated 대비 올리나.
- terminal: `--py`. L3+kosmos 결합.

*(L7는 예측코딩-트렁크 전면교체(가장 정직하지만 비cheap·트렁크 건드림·H_1816 재발사 위험)를 대신하는 cheap 근사다 — 트렁크 objective 자체가 진짜 레버라는 메타법칙과 정합하되 lane으로 우회.)*

---

## 가장 생물학적으로 정직한 다음 발사 1개

**L5 — 해마 관계저장소 + 이행추론 lane (kosmos anchor), reachable-vs-unreachable 판별.**

이유 4개:
1. **재조합(G1)이 주 벽**이고 오너의 derivtrace 맥락 직결.
2. **판별기가 원리적으로 form에 속지 않는다** — chain-reachable held-out과 unreachable은 *같은 표면형태의 held-out novel pair*다. mouth form-priming이면 둘 다 동일(똑같이 못하거나 잘하거나). 관계 lane이 진짜 조합하면 reachable만 lift. 이건 표면형태를 완벽 통제하는 within-held-out 대조 — 고전 해마 이행추론 패러다임(Dusek & Eichenbaum). anima 전 레버 중 유일하게 **속일 수 없는 BIND 시험**을 내장.
3. **cheap** — associative store + pattern-completion, GPU 트렁크 재학습 불필요, engine-native decodable, `--py` terminal.
4. **anima가 완전히 결여한 진짜 substrate** — novel-combine의 해마 기질을 kosmos(이미 WIRED 지속 관계저장소) 옆 lane으로 붙이기. a_no_llm_frame_trap의 "빠진 lane 옆에 붙이기" 정확히 준수, mouth-readout 아님.

G6 쪽 쌍둥이로는 **L3(forward-model consequence lane, cross-shuffle break)**를 병행 후보로 둔다 — coverage fals=6 form-priming의 직접 해독제이고 동일하게 내장 BIND 시험(cross-shuffle)을 가진다. 둘 다 "committed 예측/저장관계를 mouth 밖 lane에 두고 disjoint objective로 훈련" 원칙을 공유한다.

원하면 L5를 2-surface 가설(HYPOTHESES.jsonl + card)로 등록하고 reachable/unreachable probe 설계를 구체화하겠다.