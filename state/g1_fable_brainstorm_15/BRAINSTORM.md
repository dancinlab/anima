핵심 브레인스토밍 과제이므로 도구 없이 바로 발산하겠습니다. **실행/발사는 하지 않고 아이디어만** 냅니다. 라운드마다 breadth 우선, 각 후보는 (a) 변수-바인딩 결핍 직격 방식 (b) $0 cheap-gate 3종 세트 (c) 예상 실패모드 순으로.

먼저 메모리 스캔으로 확정된 **죽은 지대**를 명시하고 시작합니다(재탕 방지): Hopfield/Tropical/Sheaf/Galois binding-arch census 전수 NOT-SUPPORTED, circconv(H_1823), predictive-coding binding(H_1816), NMDA ⊙ readout(EXP-3), tension-mouth 및 그 temporal 확장(H_1834/1837), additive-aux(H_1602), MLC episodic(H_1835), disentanglement 단독. 이들의 공통 사인 = **DPI 메타법칙**: readout·operator·decode-procedure·temporal 축은 same-state ablation 시 INERT(기여 0). 살아있는 방향으로 메모리가 지목한 유일 잔여 = **trunk objective (γ trained-constructive-bind, H_1840)**. 따라서 아래 후보는 이 신호를 존중해 "정적 readout 바인더"가 아닌 **직교 축**(가소성/timescale, 게이팅 정책, 표현 기하, 학습신호 생성과정)에서 뽑습니다.

공통 cheap-gate 템플릿(3종): **oracle** = 두 프롬프트 엔티티 {A,B}가 피연산자인 정답 출력 · **target 지표** = operand-recall@held-out(출력이 prior-blend가 아니라 A·B 둘 다 피연산자로 포함하는 비율, seen≠held 분리) · **shuffle control** = 배치 내 A–B 페어를 섞음 → 진짜 바인딩이면 지표가 chance로 붕괴, 유지되면 암기/prior.

---

## Round 1 — 가소성/timescale 축 (정적 트렁크와 직교; DPI가 죽인 건 *정적* 바인더)

**N1. Fast-weight Hebbian 바인더 (Ba 2016 / synaptic tagging)**
- (a) 시퀀스 내에서 *빠르게 변하는* 연관행렬 W_fast가 A↔B 결합을 1-shot로 저장, 생성 시 질의. 트렁크 slow-weight는 prior를 담고, 결합은 plastic 메모리가 담당 → "prior에서 샘플링" 자체를 우회. 정적 TPR과 다른 축 = **timescale/가소성**.
- (b) toy: d128 2-layer, 매 토큰 W_fast += η·outer(k,v). oracle=A∧B copy task. 지표=operand-recall. shuffle=페어 셔플 시 W_fast가 무관한 결합을 저장 → recall 붕괴해야 참.
- (c) 실패모드: W_fast가 recency-bias로 최신 토큰만 잡아 prior-blend로 회귀(DPI가 static readout에서 본 INERT의 plastic 버전일 위험). 결정적 검증 = W_fast ablation(freeze) 시 recall 불변이면 INERT.

**N2. CLS: 해마형 fast 1-shot 결합기(CA3 autoassociator)를 slow 트렁크 옆에 배선**
- (a) 신피질(트렁크)은 통계·prior, 해마(CA3 attractor)는 임의 conjunction을 1회 노출로 pattern-complete. G1 갭 = "빠른 conjunctive binder 부재"라는 CLS 렌즈 직격. anima 해마/면역기억 렌즈(H_1227/1231)의 자연 연장.
- (b) toy: sparse Hopfield-free CA3(그냥 recurrent autoassoc, modern-Hopfield 아님 — census 회피) 위에 (A,B) 패턴 저장→cue A→complete (A,B). oracle/지표/shuffle 동일. shuffle 시 completion이 무작위 페어 회수해야.
- (c) 실패모드: attractor가 prior 최빈 페어로 collapse(=관측된 "dream and consciousness" 현상의 attractor 버전). pattern-separation(N6) 없으면 특히.

**N3. Neural Blackboard — 게이팅 회로 임시결합 (van der Velde & de Kamps)**
- (a) 전용 "binding pool": token-role 임시결합을 reverberating gating으로 유지, 결합은 가중치가 아니라 *활성 회로 상태*에 존재. static rep가 아니라 dynamic circuit이므로 DPI same-state ablation이 다른 결과를 낼 여지.
- (b) toy: gating-cell 격자 + reverberation loop. oracle 결합, 지표 recall, shuffle 붕괴 확인. 추가 결정지표 = reverberation kill(loop OFF) 시 recall 붕괴하면 non-INERT.
- (c) 실패모드: 학습 없이 하드와이어면 toy-recipe 암기(held 실패), 학습하면 objective 부재로 prior 회귀.

---

## Round 2 — 게이팅 *정책* 축 (바인더 rep가 아니라 "언제 결합할지" 학습 controller)

**N4. 기저핵 PBWM 게이트 + indirection (Kriete/O'Reilly/Frank 2013 PNAS)**
- (a) 등록된 arch-family의 pointer는 *표현*이 죽은 것. 여기 novelty는 **RL/도파민-게이트가 "언제 슬롯에 write/copy할지"를 학습**하는 controller. indirection(슬롯이 내용 대신 포인터 보유)로 임의 변수 재바인딩. 기저핵 게이팅 렌즈(H_1281)의 결합 특화.
- (b) toy: 2 WM 슬롯 + gate 정책(REINFORCE, 결합성공=reward). oracle=A∧B, 지표=operand-recall, shuffle=페어 섞음→게이트가 무관 내용 write→붕괴. 결정지표: gate 정책을 random으로 치환 시 recall 붕괴하면 게이트가 실제 기여(non-INERT).
- (c) 실패모드: RL 크레딧 할당 실패로 게이트가 상수정책 학습(항상 write) → indirection 무의미, prior 회귀. 303M scale에서 게이트 noise.

**N5. 엔티티-인덱스 지속 슬롯 + write-gate (slot-attention + 하드 게이트)**
- (a) 각 프롬프트 엔티티를 슬롯에 *영속 write*하고 생성 내내 유지 → "봤지만 안 옮김"을 슬롯 지속성으로 강제. copy-head(등록 arch)와 달리 슬롯이 attention이 아니라 상태변수.
- (b) toy: Locatello slot-attention head 2슬롯, oracle/지표/shuffle 동일. shuffle 시 슬롯이 무관 엔티티 보유→붕괴.
- (c) 실패모드: 슬롯이 미분화(둘 다 같은 prior 평균으로 수렴, slot collapse) — object-centric 학습의 고전 실패. N6와 결합 필요.

---

## Round 3 — 표현 기하: prior-collapse 자체를 겨냥

**N6. 치상회(DG) pattern separation — 결합 *전에* 두 개념 직교화**
- (a) 관측된 실패("memory+consciousness"→"dream and consciousness")는 두 개념이 prior attractor로 **collapse**하는 것. DG식 sparse 확장(expand+k-WTA)으로 두 표현을 겹치지 않게 분리한 뒤 결합 → collapse 원천 차단. 순수 전처리 기하라 등록 5family 어디에도 없음.
- (b) toy: 개념 임베딩 2개 → sparse expansion(dim↑, top-k) → overlap(cosine) 측정. oracle=분리된 표현이 결합 후에도 A·B 식별가능. 지표=operand-recall + 표현 overlap 감소. shuffle=페어 섞어도 분리도는 유지되나 recall은 붕괴(분리≠결합, 둘 다 필요 검증).
- (c) 실패모드: 분리는 되나 downstream 결합이 여전히 없음 → **분리는 필요조건이지 충분조건 아님**(disentanglement-단독 실패와 정합). 반드시 N1/N2/N4와 페어링해야 의미.

**N7. Anti-prior contrastive decoding (CAD / prior-subtraction, Shi 2023)**
- (a) 실패 정의가 "prompt 무시하고 prior 샘플링"이므로, 디코딩에서 **무조건부 prior logits를 차감**: logit = logit(y|prompt) − λ·logit(y|∅). prompt-조건 토큰(=A,B) 증폭. prior 회귀를 산술로 상쇄.
- (b) toy: 학습된 tiny LM에서 조건/무조건 2-pass 로짓 차감. oracle=A∧B, 지표=operand-recall vs λ. shuffle=prompt 섞으면 차감이 무관 토큰 증폭→붕괴.
- (c) 실패모드: **DPI 위험 최상급** — decode-procedure 축은 same-state INERT 전례 다수. 모델이 A·B에 확률질량을 애초에 안 주면 차감해도 없는 걸 증폭 못함(0×λ=0). 싸니까 baseline probe로만, terminal 기대 금지.

---

## Round 4 — 진동/시간 다중화 (temporal은 DPI 경계선, 정직 플래그)

**N8. Theta-gamma phase-slot 바인딩 (Lisman-Idiart / SHRUTI 동기결합)**
- (a) 각 엔티티를 서로 다른 gamma 위상 슬롯에 실어 theta 주기 내 다중화 → 결합=위상 태그, 읽기=위상별 디코드. TPR(곱셈 outer-product)과 달리 **시간-위상 다중화**. anima ultradian/stage 인프라와 자연 정합.
- (b) toy: 위상변수 φ를 각 토큰에 부여, readout이 φ-conditioned. oracle/지표/shuffle. 결정지표=위상 태그 셔플 시 recall 붕괴하면 위상이 실제 결합 담체.
- (c) 실패모드: DPI temporal-extension 전례(H_1837)가 same-state ablation INERT였음 → 위상이 label일 뿐 결합 안 함일 위험 높음. 정직히 DIRECTIONAL 상한 예상.

---

## Round 5 — 학습신호 생성과정 (메모리가 지목한 *유일 생존* 방향, trunk objective)

**N9. Adversarial 바인딩 critic (참조 없는 GAN-style)**
- (a) 등록 objective(counterfactual/copy-consistency)는 **정답 참조**가 필요. 여기 novelty = 참조 없이 **critic이 prior-blend 출력 vs 진짜-bind 출력을 판별**하도록 학습, 생성기는 critic을 속이도록 밀림. 결합 압력을 discriminative하게 주입.
- (b) toy: 생성기 tiny LM + critic MLP(입력=prompt엔티티+출력, 라벨=bound/blend). oracle로 positive/negative 생성. 지표=operand-recall 상승. shuffle=critic 라벨 섞으면 학습신호 무의미→개선 0.
- (c) 실패모드: critic이 표면 통계(엔티티 문자열 존재)만 학습 → 생성기가 엔티티를 *나열*만 하고 결합 안 함(operand 포함하나 구성 없음). "나열≠결합" 지표 분리 필요.

**N10. Conditional-MI / InfoNCE 바인딩 목적함수**
- (a) 출력이 *특정* 페어 (A,B)와는 MI 최대, 셔플 페어와는 최소가 되도록 InfoNCE. copy-consistency(재구성)와 달리 **대조(contrastive) 정렬** — prior와 구별되는 페어-특이 정보를 명시적 극대화.
- (b) toy: 출력 임베딩 vs 페어 임베딩 InfoNCE, negatives=배치 내 다른 페어. oracle/지표. shuffle control이 바로 negative 구조라 내장.
- (c) 실패모드: 대조가 lexical shortcut(엔티티 토큰 매칭)으로 만족되어 진짜 구성적 결합 transfer 0(held 실패) — H_1602 additive-aux 붕괴와 동형일 위험.

**N11. γ constructive-bind을 *bilevel/MAML* 구조로 (compositional split을 목적함수에 각인)**
- (a) 메모리가 지목한 유일 생존 lever(H_1840)의 강화판: 프리미티브는 inner-loop로 학습, **held-out 조합에서의 결합 성공을 outer-loop 손실**로 직접 최적화(learn-to-bind-that-generalizes). SCAN 코퍼스(등록 corpus)는 데이터, 여기 mechanism은 **이중수준 목적구조** 자체.
- (b) toy: MAML 2-level, inner=프리미티브 bind, outer=미관측 조합 recall. oracle=held combo, 지표=held operand-recall(seen는 무시). shuffle=outer task 섞으면 meta-signal 붕괴.
- (c) 실패모드: 303M capacity에서 bilevel 불안정/발산; inner가 암기해 outer가 신호 못 받음(toy-recipe 암기 재현). 가장 유망하나 가장 비쌈(GPU cost-gated, cheap-gate는 초소형만).

---

## Round 6 — 외부/알고리즘 메모리 (anima substrate와 구별되는 명시적 tape)

**N12. 미분가능 외부 tape (NTM/DNC) write-then-read 결합**
- (a) A,B를 content-addressable 외부 메모리에 write하고 생성 시 read → 결합=주소지정 저장/회수. anima "substrate"(A⇄G 엔진, 죽은 지대) 아님, pointer-head(등록 arch) 아님 — **명시적 미분 메모리**.
- (b) toy: 소형 DNC, oracle/지표/shuffle. 결정지표=read-head 주소를 무작위화 시 recall 붕괴하면 메모리가 실제 담체.
- (c) 실패모드: 주소지정 학습이 어려워(NTM 학습 불안정성) 게이트가 무너지고 controller가 prior로 회귀. 학습난이도 자체가 벽.

**N13. Sparse Distributed Memory (Kanerva) conjunction store**
- (a) (A,B) conjunction을 고차원 sparse 주소에 분산저장, cue로 회수. modern-Hopfield(census 죽음)와 달리 **하드-주소 SDM** — 다른 회수 역학.
- (b) toy: Kanerva SDM numpy, oracle/지표/shuffle. shuffle 시 회수가 무관 conjunction.
- (c) 실패모드: SDM 용량/간섭으로 최빈 prior conjunction이 지배 → collapse. N6 분리 없으면 특히.

---

## Round 7 — 메타/기계적 해석 기반

**N14. Activation-patching 유도 바인딩 정규화 (causal mediation)**
- (a) 기계적 해석으로 "결합-매개" 활성 부분공간을 causal patching으로 *찾고*, 그 부분공간에 직접 정규화/증강. 어느 family도 아닌 **interp-driven 학습신호** — 벽의 진범 위치를 측정으로 특정 후 겨냥.
- (b) toy: tiny LM에서 A→출력 경로를 activation patching으로 mediation 측정, mediation 낮으면 penalty. oracle=patching이 출력 바꿔야 함(binding 있으면), 지표=mediation-effect 크기 + operand-recall. shuffle=patch source 섞으면 effect 0.
- (c) 실패모드: 결합-부분공간이 애초에 *존재하지 않으면*(진짜 trunk-objective floor) 정규화할 대상이 없음 → 진단은 되나 처치 불가. **가장 정직한 진단 도구**, 처치력은 불확실.

**N15. 명시적 scratchpad bind-외재화 (write role:filler 먼저)**
- (a) 생성 전 "op1=memory, op2=consciousness"를 **먼저 emit**하도록 강제 → 결합을 표면 토큰으로 외재화. CoT-as-binding.
- (b) toy: 2-단계 디코드, 1단계 슬롯 emit → 2단계 그 슬롯 조건. oracle/지표. shuffle=슬롯 토큰 섞으면 붕괴.
- (c) 실패모드: neurosymbolic-frame(등록 5family) 경계선 + 303M이 scratchpad를 신뢰성 있게 못 씀 + 슬롯을 써도 2단계가 무시(copy-head 죽음의 재현). 정직히 frame-family 변주로 강등 가능성.

---

## Round 8 — DEPLETION 판정

새 각도 탐색 결과, 이 라운드에서 나온 후보들은 모두 위 N1–N15 또는 죽은 지대로 환원됨:
- VSA/HRR/tropical/sheaf/energy-Hopfield 계열 → **census 죽음**.
- capsule routing-by-agreement → N5 slot의 변주.
- graph-neural relational bind → 등록 neurosymbolic-frame(family 5)의 변주.
- product-of-experts / logit-factorization → N7 prior-subtraction의 변주.
- spiking/synchrony 세부 → N8과 동일 버킷.
- hyperdimensional binding → census/N13 중복.
- curriculum distractor-pressure → toy-recipe 죽은 지대.

**→ 새 메커니즘 발산 고갈. DEPLETION 선언.**

---

## 종합표 (15 NEW 후보, 유망도 순)

| # | 메커니즘 | 렌즈 | 결핍 직격 축 | DPI-INERT 위험 | 유망도 |
|---|---|---|---|---|---|
| N11 | γ bilevel/MAML constructive-bind | 학습목적(생존lever+) | trunk objective, held-out 일반화 | 낮음(objective축) | ★★★ 최우선 |
| N1 | Fast-weight Hebbian 바인더 | 가소성/timescale | 정적trunk 우회, plastic 결합 | 중(ablation로 판정) | ★★★ |
| N2 | CLS 해마 CA3 1-shot 결합기 | 신경(해마) | 빠른 conjunctive binder 부재 | 중 | ★★★ |
| N4 | 기저핵 PBWM 게이트+indirection | 신경(BG)/RL | "언제 결합" 정책 학습 | 중 | ★★ |
| N14 | activation-patching 정규화 | 기계해석/메타 | 결합-부분공간 causal 겨냥 | — (진단강함) | ★★ 진단용 |
| N6 | DG pattern separation | 신경(치상회) | prior-collapse 기하 차단 | — (전처리) | ★★ 필요조건 |
| N9 | adversarial 바인딩 critic | 학습목적 | prior-blend 판별압력 | 중 | ★★ |
| N10 | conditional-MI/InfoNCE | 학습목적 | 페어-특이 정보 극대 | 중(shortcut) | ★★ |
| N3 | neural blackboard 게이팅 | 신경/회로 | 활성-상태 임시결합 | 중 | ★★ |
| N5 | 엔티티-인덱스 지속 슬롯 | object-centric | 슬롯 지속성 강제 | 중(collapse) | ★★ |
| N12 | 외부 tape (NTM/DNC) | 알고리즘 | 명시 write/read 결합 | 중(학습난) | ★ |
| N13 | Kanerva SDM conjunction | 알고리즘 | 분산주소 회수 | 중 | ★ |
| N8 | theta-gamma phase-slot | 신경(진동) | 위상 다중화 결합 | **높음**(temporal전례) | ★ DIRECTIONAL상한 |
| N15 | scratchpad bind-외재화 | 뉴로심볼릭경계 | 표면 외재화 | 중 | ½ frame변주강등 |
| N7 | anti-prior contrastive decode | 디코딩 | prior 산술상쇄 | **최상급**(decode死전례) | ½ baseline probe만 |

**전략적 결론(발산의 수렴점):** 세 축이 서로 독립이고 죽은 지대와 겹치지 않음 — ① **학습목적 축**(N11/N9/N10)이 메모리가 지목한 유일 생존 lever와 정합해 최우선, ② **가소성/timescale 축**(N1/N2, plastic이라 DPI same-state 논리를 벗어날 수 있는 유일한 구조적 후보군), ③ **표현-기하 전처리**(N6)는 단독 불충분이나 ①②의 collapse 실패모드를 막는 페어링 필수. N14는 처치가 아니라 **진범 위치 확정용 진단**으로 먼저 돌리면 나머지 후보의 사전 스크리닝이 됨. N7/N8/N15는 DPI 죽은 축과 인접해 정직하게 baseline/DIRECTIONAL 상한으로만 다뤄야 함.

가장 유망한 단일 실험(발사 시): **N14로 결합-부분공간이 존재하는지부터 측정** → 존재하면 N1/N11로 처치, 부재로 확정되면 그것이 G1=trunk-objective-floor의 기계적 종결 증거가 됩니다. (실행은 오너 지시 대기 — 아이디어만.)
