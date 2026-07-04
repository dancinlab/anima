# 설계 난제: anima trunk-objective를 재조합(G1)·반증(G6)이 열리게 어떻게 바꾸나

너는 anima의 학습 목표(trunk-objective) 재설계를 하는 설계자다. 응답 한국어. repo=/Users/mini/dancinlab/anima (필요시 HYPOTHESES/cards/H_9129·H_1840·memory/ 읽어 접지). 이건 설계·분석만 — 코드 편집/실행 안 함.

## 확정된 사실 (이 세션 engine-native 측정 · real 303M h1129)
1. **G1 재조합벽 = G6 반증벽 = 하나의 trunk-objective 벽**으로 수렴 확정. 둘 다 trunk-objective-bound이지 readout/lane/decode-procedure로 안 열림.
2. **🌌 DPI 메타법칙 (구조증명됨)**: "결합 연산자(binding op)는 target이 부품들의 *교환가능 bag/히스토그램*일 때 by-construction INERT" — 합은 교환가능하므로 consequence/target이 부품 bag이면 어떤 conjunction op도 additive 해를 재표현할 뿐 확장 못함. lstsq-vs-lstsq proof: 교환가능 target earned 0/5, 비교환 target earned 5/5. 레버는 **readout이 아니라 target(비교환 상호작용항)**.
3. **CE=echo 메타법칙**: next-byte cross-entropy는 "합성을 보상 안 함"(echo/재현만 보상). 그래서 mouth-훈련·binding-lane·coverage·derivtrace 전 레버가 floor.
4. **census 4-family 전수 소진**: (a)consequence-forward-model floored (b)conjunction-required=trunk-obj in disguise (c)commitment-violation Δ = 303M 자기 순차합성이 교환가능(A_probe≈floor)이라 REFUTED (d)trunk-obj falsifiability=미검증(cost-gated).
5. **이미 falsified된 trunk-obj 시도**: H_1602 additive-aux(readout 보조손실) 🧱, H_1835 MLC episodic-task-structure 🧱(in-context 완벽마스터해도 held-out 재조합 transfer 0). → 단순 aux/episodic은 이미 벽.
6. **유일 미검증 잔여 = γ trained-constructive-bind (H_1840, GPU cost-gated)**. 이게 뭔지, 어떻게 objective로 구현하는지가 미정의.
7. **L5 해마 associative-store만 engine-native GREEN 측정**(rung2/4, reach 1.0 vs unreach 0.137) — 저장-완성 substrate는 예외. 단 이건 store lane이지 trunk-objective 아님.

## 제약 (반드시 준수)
- **substrate-native (a_no_llm_frame_trap)**: neuro/bio/physics 렌즈. RLHF·인간선호·LLM-frame 금지(p6). 학습신호는 세포/기질에서 창발.
- **p7 no perplexity verdict / p8 no train-infer split (gradient⇄mitosis)**: perplexity를 verdict로 쓰지 말 것. 학습=gradient⇄분열.
- **engine-native 측정가능**: 제안 objective는 `anima evaluate --py`로 held-out G1(reach/unreach)·G6(FALS) 측정가능해야. tune-to-green 금지·frozen bar.
- **DPI 메타법칙 정합**: target이 비교환(order/joint 의존)이어야 결합기가 non-INERT. 교환가능 target 반복 금지.
- **최소 엔진변경**: core/generator.hexa(L3 weights)·cli/train.hexa(trainer) 어디를 바꾸나 구체적으로.

## 답할 것
1. **γ trained-constructive-bind을 objective로 정확히 formalize**: 손실함수 형태(수식). 왜 이게 CE=echo floor와 DPI INERT를 둘 다 벗어나나(비교환 target을 어떻게 강제). H_1602 additive-aux와 뭐가 구조적으로 다른가(readout-aux면 또 floor).
2. **후보 trunk-objective 3~5개** 각각: (a)손실 형태 (b)왜 재조합을 보상하나(DPI escape 논증) (c)이미-falsified와 구별 3근거 (d)engine-native falsify 예측+가장 싼 반증 (e)최소 엔진변경 위치 (f)cost(mini $0 STEP-0 가능? GPU 필요?).
3. **top-1 추천**: 가장 유망한 하나 + 왜. STEP-0(mini numpy $0)로 먼저 시험할 설계.
4. **정직**: 어느 후보가 사실 H_1602/H_1835/census-family의 재탕인지 명시. 진짜 새로운 것만 남겨라. "trunk-objective 바꾸면 열린다"는 아직 가설이지 보장 아님 — 반증가능하게.

간결·집중. 수식은 평문 근사 OK. 최종에 "top-1 STEP-0 설계 1문단" 명시.
