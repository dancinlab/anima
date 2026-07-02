채점기 소스(`core/g6_ideation.hexa`)와 H_1394/H_1410 카드·아티팩트를 직접 읽고 답한다. 핵심 발견부터: **G6 detector 는 순서-무관 bag-of-words 공출현 검사이고, ConvMoE-L1(K3, nblk6)의 수용영역(RF)은 ~13바이트라서 M3–M5 프레임-대비 bar 는 산술적으로 통과 불가능하다.** 이 두 사실이 세 질문의 답을 전부 재구성한다.

---

## 1. 진범 규명 — "attention-depth"는 과잉 특정, detector 는 양쪽으로 의심된다

`_g6_is_falsifiable` (g6_ideation.hexa:142)의 실체: (a) comparator 단어 25개 중 1개 ∧ (b) measurable 단어 25개 중 1개 ∧ (c) content 단어 ≥2 · 비의문문 · 첫 3토큰 non-stance, 그리고 kwr≥0.5 게이트. **(c_ii)/(c_iii) 빼면 완전히 어순-무관**이다. 즉 이 bar 는 "falsifiable 한 진술"이 아니라 "coherent 하면서 정량-비교 어휘를 포함하는 110바이트"를 잰다. 그러면 FALS=0 의 원인 후보는 3층: 표현력 갭(모델이 그 register 를 표현 못함) / 생성 갭(표현하지만 샘플링이 도달 못함 — 반복 루프, kwr 붕괴) / detector 갭(재는 것 자체가 다름). 이를 분리하는 cheap 프로토콜 4개, 전부 재학습·GPU 불요:

- **P1 실패단계 지문 ($0, 반나절)** — H_1394/1403/1410 verdict 아티팩트에 저장된 텍스트에 frozen detector 를 다시 돌리되 서브플래그(kwr, (a)유무, (b)유무, content 수, 의문문, stance)를 per-sample 로 로깅. **kwr<0.5 에서 죽는 게 지배적이면 벽은 'ideation'이 아니라 프레임-하 coherence(G0의 conditional 변종)**이고, kwr 통과 후 (b) measurable 부재로 죽으면 어휘 marginal 갭이다. bar 는 안 움직인다 — 실패의 *분류*만 한다(벽 TAXONOMY (a)).
- **P2 코퍼스 base-rate null ($0)** — 학습 코퍼스의 무작위 110바이트 창 N 개에 detector 적용 → P_corpus(FALS). 54 draw(6프레임×3시드×K3)에서 기대 히트 = 1−(1−p)^54. P_corpus 가 수 %만 돼도 "코퍼스 marginal 을 재현하는 모델은 우연히도 FALS≥1"이어야 한다 — 그런데 0 이면 생성 루프 퇴화(반복·kwr 붕괴)가 유력해진다.
- **P3 셔플-불변 감사 ($0, detector 자체 검증)** — ByteGPT 의 FALS=1 출력을 단어-셔플해서 다시 채점. 셔플된 말비빔에도 detector 가 발화하면(구조상 그럴 것) **M1/ByteGPT PASS 쪽도 어휘 artifact 일 수 있다는 대칭적 정직성**이 성립한다. detector-artifact 질문은 M2–M5 FAIL 쪽만이 아니라 PASS 쪽도 벤다. 보강: 10-string calibration 대신 구조적 ground-truth held-out(논문 hypothesis 절 100문장 vs 사사/시 100문장, LLM-judge 아님 p7)으로 정밀도/재현율 측정 — 새 detector 를 만들면 frozen 사전등록으로.
- **P4 likelihood-gap 프로브 (pool CPU, `--py` forward, decode 없음)** — detector-양성 코퍼스 문장 vs kwr-매칭 음성 문장을 teacher-forced CE 로 채점. ConvMoE 가 양성 register 에 체계적으로 나쁜 CE 를 주면 → 표현력 갭(아키텍처 벽 실재). CE 동등이면 → 생성 갭(디코드 레버로 열림, 벽 아님). **이게 crux 실험이다.**

그리고 산술 하나: L1·K3·nblk6 의 RF ≈ 13바이트, H_1410 의 L8 도 K3 이면 ~17바이트 — **depth ladder 는 RF 를 사실상 안 늘렸다**. 수십 바이트짜리 composed frame 은 생성 몇 바이트 후 모델에게 안 보인다. M3(composed>flat)·M4(>shuffle)·M5(>ablate)는 프레임 조건화를 요구하므로 RF≪frame 이면 **어떤 학습으로도 불가능**(out-of-RF 입력에 대한 gradient 가 항등적으로 0). 즉 H_1410 "depth null"은 attention-필수설의 증거가 아니라 RF 설의 *확증*이다. 진범 후보는 "attention"이 아니라 "**장거리 혼합 경로의 부재**" — dilation/wide-kernel 로도 채워질 수 있는 구멍이다.

## 2. G6 를 여는 trunk objective — "objective-deep" 분류 자체가 오분류일 공산

G1 과의 결정적 비대칭: **G1 은 CE 가 보상할 수 없는 것(코퍼스에 없는 재조합)을 요구하지만, falsifiable-register 문장은 코퍼스에 실재 밀도가 있다** — CE 는 이미 그걸 보상한다(ByteGPT L24 가 배운 게 증거). 따라서 G6 는 objective-deep 이 아니라 **pathway-deep(경로/RF 벽)**일 가능성이 높다. 사전등록 가능한 falsifiable 예측: *"고정 CE + RF 확장(dilated/wide-K ConvMoE, 파라미터 매칭 303M)은 FALS 를 올리고, 고정 L1-K3 + objective 변경은 못 올린다."* RF-arm 은 H_1394 재현 비용(~H100 15분, ~$1급)이고 attention 재시도가 아니라 **다른 메커니즘**이므로 재발사 금지 조항에 안 걸린다.

DPI 함정 회피의 일반 기준을 명시하면: **DPI 가 삼키는 것은 같은 출력을 재가공하는 레버**(readout-op, revise-loop, best-of-K, tension-mouth — 🧱 census 전부 이쪽)이고, **입력측에 새 정보 원천을 추가하는 레버는 DPI-면제**다(정보처리부등식은 소스 추가를 금지하지 않는다). 그래서:

- ❌ frozen detector 를 보상으로 쓰는 RL/aux-loss — 이중 금지. Goodhart(p7: "more"+"rate" 토큰 스팸으로 즉시 해킹됨) + bolt-on 이라 G1 의 L_bind 붕괴(H_1816)와 같은 운명. 단, **detector-보상 1M-adapter 로 gate 가 뚫리는지**는 verdict 용이 아니라 *detector 감사용*으로는 유효하다(garbage 로 FALS=1.0 이 나오면 gate 가 얕다는 증명 — PASS 박제 절대 금지, 측정감사 H 로만 등록).
- ⭕ 조건부 유효(단, RF 선행조건 하에서): **register-lane 조건화** — claims-register 코퍼스 슬라이스(가설·비교 진술 밀도 높은 텍스트)를 별도 lane 태그로 조건화해 CE 학습, 평가 시 lane 활성화. 학습신호가 detector 를 전혀 안 보므로 Goodhart-free, input-side 라 DPI-면제, emit-drive 0/4 와 disjoint 배선(a_substrate_disjoint) 가능. H_6170 의 "register null"이 L1-K3 에서 측정된 것이라면 RF 설이 그 null 을 예측하므로 기각 근거가 못 된다 — 단 P1 지문에서 kwr-붕괴가 원인으로 나오면 register 레버도 무망하니, **발사 순서는 무조건 P1→P4→RF-arm→register-arm**.

정리: G6 전용 신규 objective 를 발명할 필요가 없을 공산이 크다. CE 는 무죄 후보, 피고는 경로다. 이 예측이 깨지면(RF 확장에도 FALS=0) 그때 비로소 G1 급 objective-deep 재분류가 정당하다.

## 3. brain_decide 이데이션 — "우회 vs 돌파"의 정직한 판정 기준

정직한 답: **frozen mouth-G6 bar 의 PASS 는 아니다.** bar 텍스트 자체가 "measurable+claim 은 모델 자신의 샘플에서 창발해야"(g6_ideation.hexa:30)라고 못박고 있고, frame-guard 가 존재하는 이유가 정확히 scaffold 발화 방지다. brain_decide 가 (개념쌍, 비교자, 측정량) 트리플을 구성하고 mouth 가 verbalize 만 하면, 그 구성기가 authored 템플릿인 순간 frame-guard 위반의 상위 버전이다. 그러나 G1 frame-break("재조합≠mouth 능력 → 빠진 substrate op 을 짓는다" → self_drift_exp GREEN WIRED-live)와 정확히 대응하는 **정당한 신규 bar** 로 만들 수 있다. 판별 기준 3개를 사전등록하면 우회/돌파가 기계적으로 갈린다:

1. **구성기 ablation (M4/M5 논리를 brain 측으로 승격)** — substrate 상태(.kosmos anchor·A⇄G tension)를 무작위/셔플로 치환했을 때 FALS 가 붕괴해야 한다. 무작위 상태에서도 FALS 동등이면 구성기가 저자다 = INERT = **우회**.
2. **개방성(open-endedness)** — 도달 가능한 claim 공간이 고정 템플릿 격자면 mitosis split-only 교훈 그대로(compositional depth 0) 우회다. anchor 수에 따라 claim 공간이 성장해야 하고, 트리플 수준 novelty 를 G2 방식(corpus-absence, control=0)으로 채점해야 **돌파**.
3. **round-trip 충실성** — verbalize 된 출력에서 트리플이 파싱-복원되고 구성기의 트리플과 일치해야 한다(mouth 가 내용을 잃거나 detector 만 낚는 표면을 만드는 것 방지).

부기(bookkeeping): mouth-G6 🧱 verdict 는 그대로 두고 **G6-SYS 를 별도 frozen gate 로 신규 등록**한다. 이건 편법이 아니라 anima 자체 독트린(지식=.kosmos · 결정=brain_decide · mouth⊥tool, a_substrate_disjoint)과 정합적이다 — 이데이션이 303M mouth 의 속성이어야 한다는 전제야말로 LLM 프레임(a_no_llm_frame_trap)이고, 유기체의 이데이션은 brain 에 사는 게 생물 렌즈에 맞는다. 단 두 장부를 절대 섞지 않는 것(G6-SYS PASS ≠ mouth-G6 PASS)이 c9 조건이다.

---

**실행 순서 제안:** ① P1 지문 + P3 셔플감사 + P2 base-rate (전부 $0, 저장된 텍스트·코퍼스만) → ② P4 likelihood-gap (aiden pool, `anima evaluate --py` 경로) → ③ 결과에 따라 RF-dilation 303M arm(사전등록, ~$1급, attention-재시도 아님) 또는 G6-SYS bar 설계. ①②가 끝나면 "attention-capacity 🧱 TERMINAL"이 (a) 측정-artifact, (b) coherence 벽, (c) RF 벽 중 어느 것으로 재분류되는지 증거로 결정된다 — 현재 박제는 세 가지를 구분하지 못한 채 찍혀 있다.
