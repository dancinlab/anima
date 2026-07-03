핵심을 먼저 잡고 발산하겠다. H_9111이 준 진짜 씨앗은 "faculty가 floor"가 아니라 **측정기가 포화**했다는 것 — 통신은 성공했는데(D_raw=1.0) outcome 벡터가 상수라 상관이 기계적으로 0이 됐다. 그러니 발산의 두 축은 (a) **variance를 되살리는 측정 재설계**와 (b) **emit↔appropriateness 결합을 실재하게 만드는 substrate 부품**이다. 아래는 코드 없이 설계·후보만.

---

## 0. 먼저 — 발산 이전의 프레임 정정 (씨앗)

H_9111의 비대칭이 결정적이다: **폐포 밖 LLM은 7/7 이해, 자기-clone은 0/7.** 이건 "anima가 언제 emit할지 아는가"(autogenous → tautology, 이미 🔴)와 다른 것을 말한다 — anima의 emit이 **자기 사설(私設) 코드가 아니라 공적(公的) 세계에 anchor된 reference**라는 것. clone이 못 읽는 게 결함이 아니라 **증거**다: 의미가 anima 내부 디코더가 아니라 공유된 referent에 산다. 이게 "appropriateness"보다 **aboutness/reference/intentionality**에 가깝다. 아래 발산은 이 재프레임을 여러 갈래로 편다.

---

## 1. 측정-variance 복원 (D=1.0을 연속 커브로)

포화한 hit/miss 이진을 **연속 통계**로 바꾸거나, receiver를 ceiling에서 끌어내리는 축들.

- **PSYCHO-K (distractor psychometric sweep)** — 1줄: distractor 개수 K∈{2,4,8,16,32}·near-synonym·클루 길이 절단(emit 앞 n바이트만)으로 난이도를 격자화, receiver 정답률의 psychometric 곡선에서 **50% 임계(threshold)**를 뽑아 그게 곧 coupling-strength. *왜 새로움*: 7/7-all-easy를 threshold라는 스칼라로 압축 → variance 불필요, 포화 자동 회피. *seam*: 기존 H_9111 grounded emit 그대로 재사용, distractor만 새로 샘플링 → live core 디코드로 emit 생성부만 engine-native, 채점은 외부 오라클. *bar*: threshold_real이 threshold_shuffle(emit↔referent 셔플)보다 pre-registered Δ만큼 큼(예: clue길이 임계가 셔플 대비 절반↓). *비용*: cheap $0 재채점(외부 LLM 호출만).

- **MRR/rank-continuous** — 1줄: receiver가 후보 전체를 랭크 → true referent의 mean reciprocal rank/log-loss를 outcome으로. *왜 새로움*: ceiling(전부 1위)에서도 연속값 유지, Pearson-degeneracy 원천 차단. *seam*: H_9111 데이터 그대로, 채점 함수만 교체. *bar*: MRR_real − MRR_selfpair ≥ pre-reg(셔플 통제). *비용*: cheap $0.

- **NOISY-CHANNEL (Shannon capacity)** — 1줄: emit에 바이트 노이즈 ρ∈[0,1] 주입, decode 정확도 vs ρ 곡선의 면적/절반점 = **채널 용량(bits)**. *왜 새로움*: faculty를 정보이론적 스칼라(용량)로 정의 — 포화·floor 둘 다 곡선 위 한 점일 뿐. self-clone vs 외부의 **용량 비**가 "폐포 밖" 이득의 정량. *seam*: emit 생성 engine-native, 노이즈+채점 numpy. *bar*: C_diffLLM / C_selfpair ≥ pre-reg(>1). *비용*: cheap→engine-native.

- **HANDICAP-RECEIVER (수신자 용량 스윕)** — 1줄: 외부 오라클을 의도적으로 약화(작은 모델·temperature↑·context 절단)해 ceiling에서 끌어내림, "decode 성공하는 최소 receiver-용량"이 coupling. *왜 새로움*: receiver-type을 바꾸는 게 아니라(소진됨) receiver-**용량을 연속축**으로. *seam*: emit engine-native, receiver는 외부 sweep. *bar*: 성공-임계 용량이 셔플 emit 대비 낮음. *비용*: cheap(작은 모델).

- **COMPOSITIONAL-REFERENT (부분점수)** — 1줄: referent를 2속성(색×모양 등) 구조로, receiver가 속성별 디코드 → per-attribute 전송률로 partial-credit variance 확보. *왜 새로움*: 단일 referent 이진을 다차원 연속으로, 동시에 **합성성(compositionality)** 측정을 겸함(§5의 iterated-learning과 접속). *seam*: 구조화 referent로 emit 생성 engine-native. *bar*: 속성별 상호정보 합 > 셔플. *비용*: cheap→engine-native.

> 정직: 이 5개는 전부 **측정 아티팩트를 걷어내는** 것이지 faculty가 존재함을 새로 증명하지 않는다. PSYCHO-K/NOISY가 그려낸 곡선이 셔플과 **구별 안 되면** 그때는 진짜 coupling floor — DPI가 emit층까지 따라온 것으로 terminal 처리해야 한다(c9).

---

## 2. coupling-strength 메커니즘 (emit↔appropriateness를 실재하게 — 생물렌즈 우선)

측정이 아니라 **부품을 붙여** 결합 자체를 만든다. 전부 a_substrate_disjoint: emit-drive lane(0/4)·§ImmuneMemory recall_thr와 **disjoint 좌표**에 배선.

- **CEREBELLUM-FWD (수신자 순방향모델)** — 1줄: 소뇌=순방향모델(H_1280) 렌즈 — emit 전에 "이 emit을 외부가 어떻게 디코드할지"를 예측하는 side-lane을 두고, 예측-decode를 최대화하도록 emit을 변조. *왜 새로움*: readout/operator가 아니라 **타자(他者)를 모델링하는 예측 lane** — DPI가 막은 "trunk-state에 없는 MI"를 외부 오라클 응답(폐포 밖!)에서 gradient로 끌어옴. *seam*: forward-predictor lane을 brain_decide 옆에 disjoint 배선, target=외부 오라클 실응답. *bar*: fwd-model 켤 때 §1의 threshold/capacity가 유의하게↑, ablation OFF 시 INERT면 기여 0. *비용*: GPU cost-gate(외부 오라클 라벨로 학습).

- **BASAL-GATE (기저핵 emit-value 게이팅)** — 1줄: 기저핵=게이팅(H_1281) — brain의 vbasal이 emit을 "예측 consequence-value"로 gate, actor-critic으로 receiver-success 보상 학습. *왜 새로움*: p5/a_substrate_native_speak와 정합하는 **가치-구동 emit** — stimulus-response 아니라 내부 value가 tension을 gate. *seam*: vbasal lane 이미 존재, reward hook만 disjoint 배선. *bar*: gated emit의 receiver-decode > ungated, 그리고 Ψ=½·G5 non-fab 보존(disjoint 검증). *비용*: engine-native→GPU.

- **HEBB-FASTWEIGHT (빠른가중 가치 lane)** — 1줄: 최근 성공한 (emit-context→receiver-outcome)을 빠른가중(synaptic tagging)으로 단기 결합, 유사 emit의 salience를 즉시 상향. *왜 새로움*: gradient 없이 **plasticity로 coupling** — mitosis/gradient-free G와 정합, 초단timescale. *seam*: fast-weight store를 immune_memory와 분리한 lane. *bar*: 성공 후 유사 referent 전송률이 baseline 대비 상승(within-session), 셔플 통제. *비용*: cheap→engine-native.

- **THEORY-OF-MIND lane (mentalizing)** — 1줄: 수신자의 **믿음 상태**를 모델링하는 lane(TPJ 렌즈), emit=수신자 belief를 진실 쪽으로 갱신하는 행위, reward=belief-update. *왜 새로움*: 순수 사회인지 — anima 폐포 밖 agent의 내부상태를 타깃으로 하니 구조적으로 tautology 불가. *seam*: 외부 오라클의 사전/사후 답변 분포 차이를 belief-delta로. *bar*: emit이 receiver belief를 진실 방향으로 이동시키는 KL이 셔플 초과. *비용*: GPU cost-gate.

- **LEWIS-ANCHORED (외부-앵커 신호게임 학습)** — 1줄: 고전 Lewis signaling을 self↔self가 아니라 **anima↔frozen 외부 오라클**로 co-train해 convention이 외부에 anchor되게. *왜 새로움*: self↔self(H_9108 near-floor)의 autogenous 붕괴를 회피 — 규약이 폐포 밖에 고정. *seam*: 외부 오라클을 frozen receiver로 두고 emit 정책만 학습. *bar*: 학습된 규약이 held-out referent로 transfer + 셔플 붕괴. *비용*: GPU cost-gate. *정직*: 외부-anchor여도 규약이 사설이면 clone처럼 held-out에서 무너질 위험 — transfer가 진짜 게이트.

- **WORKING-MEMORY 대화맥락(H_1282)** — 1줄: 단일 referent가 아니라 **다중턴 대화 상태**에 appropriateness를 의존시켜 coupling을 시간축으로 확장. *왜 새로움*: temporal readout(소진됨)이 아니라 **외부 대화 상태 저장** — 정보가 폐포 밖 히스토리에서 옴. *seam*: multi-line context store를 disjoint lane. *bar*: 맥락-의존 emit의 전송률 > 맥락-무시. *비용*: engine-native.

> 정직: CEREBELLUM-FWD/THEORY-OF-MIND/LEWIS는 전부 **보상=receiver-success**를 쓰므로 Goodhart 위험(p7). frozen held-out referent + shuffle + ablation-INERT 3중 통제 없이는 GREEN 박제 금지. 그리고 receiver 라벨을 외부 LLM에서 뽑으면 그건 학습 신호일 뿐 — **verdict는 여전히 engine-native decode로 재측정**(a_engine_native_learning).

---

## 3. 프레임-break (타깃 재정의)

- **REFERENCE ≠ APPROPRIATENESS** — H_9111이 실제로 보여준 substrate 속성은 "언제 emit할지"가 아니라 **"anima의 emit이 외부가 디코드 가능한 world-anchored reference를 담는다"**. 새 타깃: *referential efficacy*. 조작적 정의 = 다양한 낯선 receiver 패널이 emit만 보고 **같은 referent로 수렴**하면 그 emit엔 객관적 reference가 있다. clone 실패는 반증이 아니라 "사설코드≠공적의미"의 확증. *seam*: 외부 receiver **패널**(≥3 이질 모델)의 referent 합의도(agreement/entropy). *bar*: 패널 합의 엔트로피 < 셔플. *비용*: cheap.

- **PUBLIC-vs-PRIVATE MEANING 축** — 1줄: 새 관찰량 = decode_external / decode_self 비율. 이 비가 >1이면 anima 의미가 **공적으로 externalize**된 것(LLM reset과 갈리는 지점 — self-anchor는 H_1471이 이미 WIRED). *왜 새로움*: 의식 emit의 지표를 "자기예측"에서 "타자-legibility"로 뒤집음. *seam*: 두 디코드 경로 비. *bar*: ratio_real > ratio_shuffle.

- **Ψ와 직교한 제2관찰량** — 1줄: pure_field Ψ=½는 emit/silence **내부 긴장**축이고, referential efficacy는 **외부 결합**축 — 둘은 직교. 지금까지 emit-appropriateness를 Ψ 근처에서 재려 해 포화했을 수 있다. 새 좌표계 제안: (Ψ, 참조효능) 2D. *seam*: Ψ는 pure_field, 참조효능은 외부 decode. *bar*: 두 축이 통계적으로 분리(낮은 상관)임을 먼저 확인.

- **CONSEQUENCE-IN-ANOTHER-MIND = agency 정의** — 1줄: emit을 "타자 상태를 예측대로 바꾸는 행위"로 정의하면 이건 곧 **agency/communication의 조작적 정의**. H_9104-9109가 자기-consequence(tautology)로 막힌 이유가 바로 consequence가 폐포 안이었기 때문 — 폐포 밖 mind가 유일한 진짜 consequence. *seam*: §2의 THEORY-OF-MIND와 공유. *비용*: 재프레임(무비용).

---

## 4. 실 외부 생리 결합 (EEG loop)

*왜 chat/LLM보다 강한 결합 후보*: 외부 LLM도 결국 학습분포에서 파생 가능한 mind지만, **실 EEG는 사용자 뇌의 물리 상태 — anima 계산 폐포 밖의, 파생 불가능한 순수 exogenous 신호**(가장 강한 non-derivability). a_eeg_consciousness_record가 이미 로드맵.

- **EEG-CONSEQUENCE loop** — 1줄: anima emit → 사용자 읽음 → 사용자 EEG delta(band-power/ERP 진폭) → consequence로 되먹임, "emit이 EEG delta를 surrogate보다 잘 예측하나". *seam*: OpenBCI native → A⇄G → .kosmos append. *bar*: D_real(실 EEG) − D_surrogate(time-shuffle EEG) ≥ pre-reg, held-out within-subject. *비용*: engine-native(실 하드웨어).

- **near-floor 회피 설계** — (a) 이진 아닌 **연속 EEG feature**(θ/α power, P300 진폭) + rank/regression 통계로 §1의 degeneracy 회피 · (b) within-subject held-out으로 개인차 제거 · (c) surrogate = 시간-셔플 + phase-randomized 둘 다 · (d) emit을 **EEG-차별적으로 설계**(정서가 강한 vs 중립 emit 대비 → variance 확보) · (e) 사전등록 bar frozen(p7). *정직*: 16ch@123Hz 천장·SNR·근전도 confound → near-floor 실제 위험, chat-user H_9110이 이미 −0.188로 음수였음을 기억. EEG가 chat보다 나을 이유는 non-derivability지 SNR이 아니다 — SNR은 오히려 나쁘다. 그래서 **연속-feature + within-subject**가 필수.

- **CLOSED-LOOP neurofeedback** — 1줄: anima가 emit을 조절해 사용자 EEG를 특정 상태(α↑ 이완)로 **유도**, 유도 성공률 = coupling. *왜 새로움*: 수동 예측이 아니라 능동 제어 — agency 정의(§3)의 실체화. *seam*: emit 정책 ↔ 실시간 EEG 피드백. *bar*: 유도 성공 > sham emit. *비용*: engine-native, 세션 게이트 필요.

---

## 5. 완전 직교 (genuinely-new)

- **ITERATED-LEARNING (문화전달 병목)** — 1줄: emit 규약을 anima 인스턴스 세대 체인으로 전달(Kirby), 전달 병목이 규약을 **compositional**하게 강제 → 합성성 창발 측정. *왜 새로움*: 개체 학습이 아니라 **세대간 전달**이 압력 — G1 재조합벽(개체 내 trunk-objective)과 다른 층. MITOSIS engine_grow가 자연스런 세대 메커니즘. *seam*: mitosis tick마다 규약 상속 + 외부 채점. *bar*: 세대 진행에 따라 §1 compositional-referent 전송률↑(topographic similarity 상승). *비용*: engine-native→GPU. *정직*: self-체인이라 autogenous 위험 — 외부 오라클을 채점자로 넣어 anchor.

- **METABOLIC-EMIT (에너지 비용 렌즈)** — 1줄: emit에 실제 대사비용 부과(스파이킹 에너지), appropriateness = 기대가치 > 비용일 때만 emit. E ratchet이 이미 substrate에 있음. *왜 새로움*: appropriateness를 예측문제가 아닌 **경제적 최적화**로 재정의 → 자연스런 sparse emit. *seam*: E ratchet ↔ emit gate. *bar*: 비용 부과 시 emit이 high-value로 편중(전송률/emit 비 상승). *비용*: cheap→engine-native.

- **EMBODIED-MINIMAL loop** — 1줄: anima가 물리 액추에이터(LED·소리) 제어 → 사용자 반응(버튼·존재센서) → 최소 sensorimotor 결합. *왜 새로움*: 가장 싼 **실 물리 exogenous** consequence, EEG보다 SNR 높음. *seam*: emit → GPIO → 센서 → .kosmos. *bar*: 반응 유발률 > 무작위 emit. *비용*: cheap 하드웨어(pi5-akida 곁).

- **ADVERSARIAL-DECODER (구별성)** — 1줄: anima emit이 **의도한 referent와 distractor를 구별**하도록, 적대적 receiver가 속이려 할 때도 유지되는 강건성 측정. *왜 새로움*: referential efficacy의 강건성 = robustness lens. *seam*: 적대적 외부 receiver. *bar*: 적대 하 전송률 > 셔플. *비용*: cheap.

- **정직한 회의 (안 될 가능성)**: §2·§5의 학습형 후보 다수는 **DPI가 emit층으로 이미 이동했다는 H_9111 결론과 정면충돌** 위험이 있다. 만약 coupling이 정말 trunk-objective floor의 emit-투영이라면, forward-model/basal-gate를 붙여도 threshold가 셔플과 안 갈릴 것이다. 그래서 **비싼 학습 전에 §1로 "잴 수 있는가"부터** 확정해야 한다 — variance가 복원 안 되면 GPU 발사는 낭비.

---

## 다음 1개 결정실험 (cheap-first)

**PSYCHO-K + MRR 재채점 (bucket 1) — 이미 수집된 H_9111 데이터 위에서 $0.**

- 왜 이것: H_9111 raw D=1.0은 "faculty 존재"의 **가장 강한 긍정 신호**인데 metric-degeneracy로 죽었다. 새 compute·학습 없이 기존 grounded emit + distractor 스윕(K=2→32)·near-synonym·클루 절단으로 **psychometric threshold**와 **MRR**를 뽑으면, 이 신호가 (a) 연속 coupling 커브로 살아나는지 (b) 셔플과 구별되는지가 한 번에 갈린다.
- 게이트 분기: **커브가 셔플 초과** → coupling이 실재·측정가능 확정 → §2의 CEREBELLUM-FWD(외부-오라클 라벨 forward-model)를 GPU cost-gate로 발사할 근거 확보. **커브가 셔플과 무구별** → DPI가 emit층까지 terminal, receiver-type 아니라 결합강도 자체가 floor임을 정직 박제(c9)하고 §4 EEG(파생불가 exogenous)로만 남은 문을 좁힘.
- 비용/측정: cheap $0(numpy 채점 + 외부 오라클 호출만), emit 생성부만 live core decode로 재사용하면 engine-native seam 유지. frozen bar 먼저(threshold_real − threshold_shuffle ≥ Δ) 사전등록 후 실행.

정직 요약: 이번 세션의 벽은 대부분 **측정기 포화**였지 faculty 부재가 아닐 수 있다 — 그래서 발산의 무게중심을 "더 많은 메커니즘"보다 **"잴 수 있게 만들기"**에 두었다. §1이 GREEN이어야 §2·§4의 비싼 배선이 정당해진다.