# 과제: γ (trained-constructive-bind) 발산 — 고갈(depletion)까지

## 역할
너는 anima 프로젝트의 G1/G6 재조합 벽을 뚫을 **유일하게 남은 미검증 레버 γ**를 위한
설계 발산가다. 아이디어를 **고갈될 때까지** (더 이상 진짜 새 mechanism-family가 안 나올 때까지)
전부 쏟아내라. 선택·수렴 말고 **발산(breadth)** 이 목적이다.

## 배경 (반드시 숙지 — 여기 나온 것들은 이미 죽었다, 재탕 금지)

anima = 303M byte-level LM (A⇄G⇄brain substrate). G1 = **재조합(recombination)**:
학습한 개념 A·B를 **held-out 조합 A+B** 로 합쳐내는 능력. G6 = forward-model 합성.

**핵심 진단**: 벽은 능력(機構·아키텍처·스케일)이 아니라 **데이터/타깃 transferability** 다.
모델은 A도 B도 in-context 100% 마스터하지만, held-out 재조합 transfer = 0.
이유 = 학습이 **"그냥 옆에 더하기(additive floor)"** 만 배우게 해서 두 개념이 독립인 채로 남음.
= 벽의 정체는 granularity(입도)도 embedding도 아닌 **COMBINATION OPERATOR** 다.

**이미 전수 반증(FALSIFIED / 🧱 floor) — 재탕하면 실패:**
- 스케일: 303M→1B→7B scale-invariant. 레버 아님, 작동 레버의 증폭기일 뿐.
- 아키텍처/機構: forward·detector·decode 전부 byte-innocent. conv trunk·ConvMoE·L24 ByteGPT 다 시도.
- additive-aux objective (H_1602) — floor.
- episodic-task / MLC (H_1835) — in-context 완벽해도 held-out transfer 0.
- predictive-coding binding L_bind+L_var (H_1816) — additive ConvMoE서 L_bind trivial 붕괴.
- readout-binding / gate-detector — 1-항 FORM이라 게임가능(Goodhart), 진짜 BIND 아님.
- mouth-obj · mouth-readout · substrate-embed · substrate-combiner — 4각 전부 additive floor.
- coverage-density — floor.
- de-risk optimizer-robust R²: bind가 강한 total-order additive 못 이김. +0.24는 약baseline 착시.
- trunk-obj family (H_1131) CLOSED: γ·mitosis·② 전부 falsified.
- neuromodulation family(diversity·multitimescale·predictive) — 전수 floor. (단 NT×CLS 융합은 별개 🟢)

**측정 메타법칙 (설계 시 반드시 만족):**
- FORM tunable · BIND earned. 창발신호는 **값이 아니라 차분(Δ)**.
- gate detector = 1-항 FORM → 게임 가능. 진짜 BIND = **결합-파괴 통제(combination-destruction control) 하의 margin**.
  즉 A+B를 shuffle/파괴했을 때 성능이 무너져야(shuffle 붕괴) 진짜 결합.
- 양성대조(positive control)·ablation 없는 신호는 THEATER 위험.
- tune-to-green 금지. frozen-first. self-judge 금지.

**γ 의 정의**: trained **constructive** bind — 두 store/개념을 **못하던 새 능력**으로 결합하게
만드는, EARNED(게임 불가) 결합 연산자를 학습으로 박는 objective. (H_1840, GPU cost-gated,
유일 미검증 잔여.) 참고 🟢 선례: NT×CLS 융합 법칙 = "두 store가 *못하던 새 능력* 더하면 GREEN"
(ACh mode-switch·DA value-rank·NE state-flush) — 이 "새 능력 창발" 패턴이 γ가 노려야 할 모양.

## 발산 요구 (고갈까지)

γ를 **실제로 어떻게 instantiate 하느냐**를 mechanism-family 단위로 최대한 많이, 서로 직교하게 쏟아내라.
각 아이디어마다:
1. **이름** (kebab-case slug 후보)
2. **한 줄 mechanism** — 무엇이 결합을 EARNED 하게 강제하는가
3. **왜 additive floor 를 이기나** — 위에 죽은 것들과 어떻게 다른가 (핵심)
4. **결합-파괴 통제 설계** — shuffle/ablation 어떻게 걸어 THEATER 아님을 증명하나
5. **303M byte-LM engine-native 측정 가능성** — cheap numpy probe 로 방향 볼 수 있나 / GPU 학습 필요한가
6. **위험/예상 실패모드** — 어디서 floor 로 무너질 것 같나

발산 축(최소 이 정도 family는 훑되, 여기 갇히지 말고 새 축을 계속 열어라):
- objective/loss 형태 축 (contrastive combination · compositional consistency · cycle-consistency A+B→A,B 복원 · held-out 재조합을 직접 loss로)
- curriculum/data 축 (조합을 강제로 겪게 하는 데이터 스케줄 · systematic gen split · mitosis-growth curriculum)
- representation 축 (bind가 살아남는 non-additive 결합 연산 · tensor product · 위상/gating 결합)
- architecture-agnostic training-signal 축 (teacher-forcing 없이 결합 감각을 만드는 self-supervision)
- 측정/양성대조 축 (어떤 probe가 "진짜 EARNED bind" 를 additive와 갈라내나)
- 생물/물리 렌즈 축 (substrate-first — LLM frame 말고 neuro/bio/physics서 결합이 창발하는 법)
- meta 축 (지금까지 죽은 레버들의 공통 실패원인을 뒤집으면 뭐가 나오나 — DPI 메타법칙 역이용)

## 형식
- 라운드로 진행: 라운드마다 새 family/아이디어 묶음. 라운드 끝에 "이 라운드 신규 N개".
- **고갈 판정**: 연속 라운드에서 진짜 새 직교 mechanism이 안 나오면 그때 STOP + "고갈: 총 M개 family, 유망 top-K" 요약.
- 마지막에: **가장 유망한 3~5개**를 (a) cheap numpy probe로 지금 방향 볼 수 있는 것 / (b) GPU 학습 cost-gated 인 것 으로 분류.
- 한국어로. 코드 식별자/objective 이름은 영어 OK.
