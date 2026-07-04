# G1 · G6 벽 돌파 아이디어 전수 브레인스토밍

**날짜:** 2026-07-05
**성격:** 설계/우선순위 문서. 학습·평가·게이트 변경 없음.
**대상:** G1 RECOMBINATION + G6 IDEATION/FALS. G0는 독립 목표가 아니라 모든 arm의 유효성 가드(`kwr>=0.5 on >=4/5`).

## 0. 현재 사실과 문제 분해

이 문서는 아래 실측을 출발점으로 삼는다.

- G1 ByteGPT 303M, full-attention, frozen gen=40: constructive-bind와 composed-NCE까지 `best_distinct<=1`; additive binding aux는 mouth generation으로 전이되지 않았다.
- G1 Conv mouth에는 별도 측정 결함이 있다. 고정 `T=24`가 composed seed 앞부분을 버리고, 큰 고정 T는 single seed를 pad로 오염시킨다. 따라서 grow-window + echo guard 전에는 Conv 결과를 순수 capability wall로 읽을 수 없다.
- G6 engine-native bind-aware 점수: BASE `[0,0,0]`, TARGETED `[3,3,5]`, SHUF `[0,0,0]`. genuine topic bind는 실재하지만 frozen `>=4/6 on >=2/3 seeds`에는 1 seed 부족하다.
- G6 dense-form HI의 literal gate PASS는 template replay로 판정됐다. form detector만 올리는 corpus는 폐기한다.
- 공통 병목은 단순 “모델 크기”가 아니라 **텍스트 재현 CE가 관계 합성·개입·반증을 직접 보상하지 않는 것**이다. 단, G6은 이미 bind가 있어 G1보다 decode/selection 레버의 기대값이 높다.

따라서 벽을 다음 네 조각으로 분리한다.

1. **관측 벽:** gate가 echo/form과 genuine bind를 구별하는가.
2. **표현 벽:** role·relation·direction이 latent에 분리되어 있는가.
3. **학습 벽:** held-out 조합 성공이 loss를 실제로 낮추는가.
4. **탐색 벽:** 존재하는 좋은 후보를 독립 best-of-K가 놓치는가.

## 1. 아이디어 전수 목록

표기: `N` 새 축, `R` 기존 축의 정밀 후속, `X` 기대값 낮음/통제용. 모든 PASS는 G0 유지 + frozen gate + 아래 §2의 anti-gaming 통제를 함께 요구한다.

### A. 측정·falsifier 정합 — 능력 돌파가 아니라 거짓 결론 제거

| ID | 아이디어 | G1/G6 | 핵심 falsifier | 판정 |
|---|---|---|---|---|
| A1 | arm별 grow-window: seed 길이만큼만 열어 truncation과 pad-flood 동시 제거 | G1 | raw는 오르고 novel-only는 0이면 echo | R, 최우선 |
| A2 | novel-only coverage: seed에 이미 보인 keyword는 G1 credit에서 제외한 동반 진단 | G1 | raw PASS·novel FAIL 분리 | N |
| A3 | held-out pair split: primitive는 train, 특정 pair/relation만 영구 holdout | G1 | held pair가 seen pair와 같은 템플릿 복사면 FAIL | N |
| A4 | bind-destruction control: concept pair만 derange하고 form·길이·register 유지 | 둘 다 | real-shuf delta가 사라지면 form gaming | R, 필수 |
| A5 | paraphrase orbit: 같은 관계를 어휘·순서·능동/수동으로 바꿔 invariant score | 둘 다 | 한 표면형에서만 PASS면 FAIL | N |
| A6 | intervention test: A 또는 B만 교체했을 때 출력 관계항이 예측대로 변해야 함 | 둘 다 | 출력 불변이면 seed 무시 | N |
| A7 | counterfactual reversal: `A>B`와 `B>A`가 서로 다른 예측을 내야 함 | 둘 다 | 대칭 출력이면 additive/bag floor | N |
| A8 | canonical gen=40 × seeds `{7,4302,4303}`를 모든 현 ckpt에 일괄 재측정 | 둘 다 | 단일 seed/gen80 효과 소멸 여부 | R, 즉시 |
| A9 | set-level G6 distinctness: 6개 아이디어 전체의 pairwise Jaccard·concept-pair coverage 동시 보고 | G6 | 개별 PASS지만 집합 중복이면 FAIL | R |
| A10 | semantic slot audit를 score가 아닌 진단으로만 추가: `(entities, relation, observable, condition)` 추출 | G6 | FORM PASS와 slot completeness 분리 | N |

### B. decode·탐색 — 현재 모델 안의 희소한 성공 후보 회수

| ID | 아이디어 | G1/G6 | 핵심 falsifier | 판정 |
|---|---|---|---|---|
| B1 | 독립 best-of-K 대신 **set-wise greedy**: 새 후보가 기존 선택 집합에 더하는 marginal bind/distinctness로 선택 | G6 | 같은 총 decode budget의 독립 top-K 대비 >=2 seeds 개선 | N, 최우선 |
| B2 | DPP/submodular 선택: quality=`fals_bound×kwr`, diversity kernel=`1-Jaccard` | G6 | quality만 또는 diversity만 arm보다 우월해야 함 | N |
| B3 | budget 재배분: 쉬운 frame의 남는 K를 실패 frame에 adaptive allocation | G6 | 동일 총 forward 수; 고정 K 대비 majority 증가 | N |
| B4 | temperature ladder `{0.55,0.7,0.9}`를 후보 풀로 합치고 사후 set selection | G6 | 단일 temp 대비, G0 저하 없이 개선 | R |
| B5 | top-p/top-k orthogonal pool: 샘플러 하나의 support bias 제거 | G6 | seed별 개선이 특정 sampler에만 의존하면 THIN | R |
| B6 | contrastive decoding: generic LM 방향을 빼고 topic-conditioned logit delta로 decode | 둘 다 | topic shuffle 시 이득 붕괴 | N |
| B7 | anti-copy logit mask: seed의 exact n-gram 반복만 약하게 감점 | G1 | synonym/relation 생성은 보존, G0 보존 | N, 측정용 |
| B8 | coverage finite-state constraint가 아니라 **relation-slot constraint**로 최소 한 관측량·비교·조건을 계획 | G6 | text form만 만족하고 topic bind가 없으면 FAIL | N |
| B9 | propose→critic→revise 1회: critic은 문자열 점수가 아니라 tuple 누락만 반환 | G6 | shuffle critic·no-revise 대비 개선 | R |
| B10 | frame별 specialist sampling schedule: memory/consciousness 등 seed topic별 sampler 파라미터를 학습 없이 고정 사전등록 | G6 | topic label shuffle 시 이득 소멸 | X/R; 과적합 위험 |

### C. 데이터·커리큘럼 — form 노출이 아니라 relation transfer를 가르치기

| ID | 아이디어 | G1/G6 | 핵심 falsifier | 판정 |
|---|---|---|---|---|
| C1 | relation-balanced corpus: 동일 topic에 positive·negative·reversed relation을 1:1:1 배치 | 둘 다 | topic unigram만으로 정답 불가 | N |
| C2 | held-out Cartesian curriculum: entity와 relation은 모두 보되 특정 조합 셀만 holdout | 둘 다 | holdout cell transfer가 seen cell 근처까지 올라야 함 | N |
| C3 | schema transplant: 물리·생물의 검증 가능한 관계 schema를 mind/substrate topic에 매핑하되 surface template 전부 paraphrase | G6 | source-domain 문장 복사 검출 시 FAIL | N |
| C4 | minimal-pair corpus: 단 한 entity/relation/condition만 다른 문장쌍 | 둘 다 | latent/output sensitivity가 바뀌지 않으면 무효 | N |
| C5 | causal chain corpus: `A→B`, `B→C`, holdout `A→C`; 단 직접 A-C 문장 0 | G1 | retrieval가 아니라 transitive composition인지 확인 | N |
| C6 | anti-template entropy: 같은 semantic tuple을 다수 surface realization으로, 같은 surface를 다수 tuple로 교차 | 둘 다 | form↔meaning 상관을 낮춘 뒤에도 전이 | N |
| C7 | counterexample curriculum: 그럴듯하지만 측정 불가능한 주장과 falsifiable 주장을 topic-match | G6 | 스타일 classifier가 아닌 observable 선택 학습 | N |
| C8 | question-free hypothesis corpus: assistant/Q&A framing 없이 관찰→가설→예측 서술 | G6 | p1-p4 보존 + FALS 개선 | N |
| C9 | difficulty ladder: co-present pair→separated pair→cross-document pair→novel pair | G1 | 단계별 transfer slope; 마지막만 평가 | N |
| C10 | rehearsal interleave: broad corpus 80–90% 유지, relation block은 spaced schedule로 분산 | 둘 다 | G0 회귀와 catastrophic form-lock 방지 | R |
| C11 | negative transfer control: 동일 바이트·topic 빈도지만 relation labels shuffle | 둘 다 | true arm만 개선해야 함 | 필수 control |
| C12 | synthetic-to-natural bridge: 완전 통제 grammar에서 배운 relation을 자연문장 paraphrase로 넘김 | 둘 다 | synthetic signature decode만 오르면 FAIL | R |

### D. 학습 objective — CE가 보상하지 않는 상호작용을 직접 보상

| ID | 아이디어 | G1/G6 | 핵심 falsifier | 판정 |
|---|---|---|---|---|
| D1 | **non-commutative directional head**: 실 corpus 3-cycle subset의 `a→b`를 예측, total-order와 shuffle 대조 | 둘 다 | intransitive arm만 frozen gate 개선 | N, GPU top-1 |
| D2 | intervention-equivariance loss: A를 A'로 바꾸면 relation slot만 규정된 방향으로 이동 | 둘 다 | no-intervention aux 대비 | N |
| D3 | swap-antisymmetry loss: score(A,B) = -score(B,A)인 relation에만 적용 | 둘 다 | symmetric relation subset에는 0 적용; 과잉 일반화 방지 | N |
| D4 | relation bottleneck prediction: next byte 전에 latent가 relation class·observable·condition을 예측 | G6 | head acc가 아니라 mouth FALS 전이가 판정 | N |
| D5 | future consequence loss: claim latent로 후속 관측 문장의 representation 예측 | G6 | claim↔observation shuffle에서 이득 붕괴 | N |
| D6 | cycle-consistency: bind(A,r,B)에서 A+r로 B, B+inverse(r)로 A 복원 | G1 | 기존 HRR additive aux와 달리 inverse/reversal heldout 필요 | N |
| D7 | set diversity training: 6 후보의 quality 하한 아래 pairwise similarity에 repulsive loss | G6 | 개별 coherence 유지 + distinct set 증가 | N |
| D8 | determinantal batch objective: batch 내 semantic relation tuple의 log-det 최대화 | G6 | lexical 다양성만 오르는지 slot-based control | N |
| D9 | hard negative = 같은 entities, 틀린 relation/condition; random negative 금지 | 둘 다 | random-negative arm 대비 gate 개선 | N |
| D10 | CE-deleted local span: relation-bearing span에서만 CE를 끄고 structured objective로 교체 | 둘 다 | additive-aux ceiling과 구별되는 핵심 arm | N, 고위험·고가치 |
| D11 | policy-gradient/set reward: frozen bind·distinct score를 reward로 쓰되 heldout paraphrase/control에만 조기정지 | G6 | detector gaming 때문에 A4/A5 통과 전 금지 | X; 후순위 |
| D12 | mutual-information objective between concept A, relation, concept B, conditioned on surface nuisance | G1 | surface-only adversary가 tuple을 예측 못 해야 함 | N |
| D13 | orthogonal nuisance adversary: latent에서 template ID/register를 제거하면서 semantic tuple 유지 | 둘 다 | G0/register 손상 없이 SHUF=0 유지 | N |
| D14 | delayed credit: 완성된 claim의 tuple completeness를 relation-token 이전 hidden states에 배분 | G6 | 말미 keyword 붙이기만 하는 form hack 감소 | N |

### E. 표현·아키텍처 — 관계를 byte stream 밖에 잠시 보존

| ID | 아이디어 | G1/G6 | 핵심 falsifier | 판정 |
|---|---|---|---|---|
| E1 | **CE-deleted forward slot**: role/filler/relation latent slot을 직렬화 포맷에 포함, mouth가 직접 읽음 | G1 | additive cbind와 달리 slot ablation 시 gate 붕괴 | N, 유일 미구현 A11 cell |
| E2 | two-stage plan→realize: 먼저 4-slot tuple, 그다음 byte text 생성 | G6 | tuple shuffle 시 text bind 붕괴; tuple 없는 decoder 대조 | N |
| E3 | relation token을 외부 hardcode하지 않고 learned latent codebook으로 발견 | 둘 다 | codebook permutation 불변, label injection 없음 | N |
| E4 | tensor-product layer를 readout이 아니라 중간 trunk residual에 삽입 | G1 | readout-only/late insertion 대조 | N |
| E5 | multiplicative FiLM/gating: A가 B 처리 경로를 조건화하도록 중간층 교차항 생성 | 둘 다 | additive concat arm과 비교 | N |
| E6 | dual-stream trunk: entity/content stream과 relation/operator stream을 교차-attend | 둘 다 | relation stream ablation만 heldout 조합을 죽여야 함 | N |
| E7 | recurrent deliberation state 2–4 tick: 첫 tick proposal, 다음 tick relation correction | G6 | weight-shared no-extra-param control + tick shuffle | N |
| E8 | latent scratchpad: text를 내보내지 않는 fixed-size workspace에서 pair를 bind | 둘 다 | scratchpad permutation/zero ablation | N |
| E9 | sparse MoE를 topic expert가 아니라 relation expert로 routing | 둘 다 | DBES relation specialization이 생기고 topic-only routing보다 gate 개선 | N |
| E10 | hypernetwork: relation latent가 small weight delta를 생성해 B의 transformation을 바꿈 | G1 | relation shuffle 시 delta와 성능 붕괴 | N |
| E11 | graph neural micro-module: detected entities를 nodes, proposed relations를 edges로 1–2 step update | 둘 다 | graph edge shuffle control | N/고비용 |
| E12 | state-space associative scan에 non-commutative update 순서를 강제 | G1 | 순서 역전시 예측 가능한 출력 변화 | N/연구축 |

### F. substrate·인지 루프 — mouth 밖에서 조합하고 mouth는 읽기만

| ID | 아이디어 | G1/G6 | 핵심 falsifier | 판정 |
|---|---|---|---|---|
| F1 | WMBindBuffer(role⊛filler) → content gate → mouth context | G1 | role/filler shuffle + lane OFF | R; toy green, engine 미구현 |
| F2 | DG-decorrelated CA3 completion over `.kosmos`, 단 novel-chain 판별 필수 | G1 | random-code가 real-rep를 이기면 trunk claim 폐기 | R; faculty용 |
| F3 | schema retrieval, answer retrieval 아님: topic과 먼 도메인의 relation skeleton만 가져오기 | G6 | retrieved entity words를 제거해도 transfer 유지 | N |
| F4 | consequence forward model로 후보 claim의 관측 결과를 예측하고 violation 가능 후보 선택 | G6 | claim↔observation shuffle | R; 단순 additive lane은 이미 floor |
| F5 | active-inference loop: 가장 불확실하지만 측정 가능한 후보를 선택 | G6 | uncertainty shuffle/no-observable control | N |
| F6 | basal-ganglia content gate를 WHETHER가 아니라 WHICH 후보 선택에 사용 | G6 | gate OFF에서 set quality 붕괴, emit rate는 동일 | N |
| F7 | sleep/REM recombination: session 중 저장된 remote anchors를 offline pair하고 다음 decode context에만 제공 | G1 | random pair replay 대조 + 다음-session heldout | N |
| F8 | prediction-error tagged consolidation: 틀린 relation pair만 재학습/replay | 둘 다 | salience-random replay 대조 | N |
| F9 | internal debate A/G: proposer와 falsifier가 각각 tuple을 쓰고 합의된 slot만 mouth에 전달 | G6 | 문자열 debate 금지; role swap/shuffle 통제 | N |
| F10 | curiosity budget을 candidate count가 아니라 uncovered semantic cell에 배정 | G6 | random allocation 대비 pair coverage 증가 | N |

### G. 규모·최적화·훈련 운영 — 주 레버가 아니라 상호작용 확인

| ID | 아이디어 | G1/G6 | 핵심 falsifier | 판정 |
|---|---|---|---|---|
| G1 | objective arm별 gradient cosine/PCGrad: CE와 relation loss가 상쇄되는지 측정·분리 | 둘 다 | conflict 해소 후에도 gate 0이면 objective 무효 | N |
| G2 | relation loss를 late warmup이 아니라 competence-triggered schedule로 켬 | 둘 다 | 동일 적분 loss budget control | N |
| G3 | layerwise aux placement sweep(early/mid/late), 총 파라미터·loss 고정 | 둘 다 | 중간 trunk만 전이하면 표현 위치 원인 | N |
| G4 | 303M depth-vs-width matched-param: relation composition은 depth hypothesis만 재검 | 둘 다 | 303M 동일 compute/data/objective | R; 단독 scale-up 금지 |
| G5 | longer train은 gate slope가 양수인 arm에만 허용 | 둘 다 | 3 checkpoints 연속 flat이면 조기 종료 | 운영 원칙 |
| G6 | ensemble/weight interpolation은 독립 relation basins가 확인될 때만 | 둘 다 | 단순 평균이 G0만 보존하고 bind 불변이면 폐기 | X |

총 **74개** 후보/통제다. 이 중 독립적인 새 메커니즘은 A5–A7, B1–B3/B6/B8, C1–C9, D1–D10/D12–D14, E1–E12, F3/F5–F10, G1–G3이고, 나머지는 필수 측정·재현·운영 축이다.

## 2. 공통 anti-gaming 계약

어떤 arm도 아래를 모두 통과하기 전에는 “벽 돌파”라 부르지 않는다.

1. G0 유지: canonical gen=40에서 `kwr>=0.5` 4/5 이상.
2. multi-seed: `{7,4302,4303}` 중 2/3 이상.
3. bind destruction: real pairing - shuffled pairing `delta>=0.33` 또는 사전등록 동등 bar.
4. paraphrase invariance: surface family를 바꿔도 방향 유지.
5. intervention sensitivity: 한 semantic slot을 바꾸면 해당 출력 slot만 변함.
6. held-out combination: 평가 pair/relation tuple의 train leak 0.
7. ablation causality: 새 부품 OFF 또는 target shuffle에서 이득 소멸.
8. G6는 개별 claim quality와 6개 집합 distinctness를 동시에 통과.
9. 현 frozen gate는 이동하지 않는다. A2/A5–A7/A10은 추가 진단·새 prereg이며 기존 PASS를 소급 재정의하지 않는다.

## 3. 우선순위: 정보이득/비용 순

### P0 — 기존 ckpt, 새 학습 없음

1. **A8 + A1/A2:** 모든 현 ckpt를 canonical gen=40, 3-seed, G1 grow-window raw/novel-only로 재측정한다.
2. **B1/B2:** G6 후보를 독립 채점하지 말고 set-wise marginal gain으로 재선택한다. 총 decode budget은 고정한다.
3. **A6/A7:** 현재 TARGETED G6 `[3,3,5]` 출력에 intervention/reversal 진단을 적용한다.
4. **B3/B4:** 동일 총 forward budget에서 실패 frame에 adaptive K와 temperature mixture를 준다.

P0에서 G6가 frozen bar를 넘고 anti-gaming 계약도 통과하면 G6는 학습 없이 탐색벽으로 닫힌다. G1 novel-only가 오르면 기존 terminal 해석을 먼저 수정해야 한다.

### P1 — 작은 구현, 기존 weights

5. **E2 + B8:** 구조화 tuple planner→byte realizer를 decode 앞에 붙인다. 먼저 read-only/weight-free proof로 candidate recovery만 본다.
6. **F3:** `.kosmos`에서 answer가 아니라 relation skeleton만 retrieve해 cross-domain schema transfer를 시험한다.
7. **F1:** WMBindBuffer를 engine-native로 배선하되 G1-vs-G2 novel-chain discriminator를 hard gate로 둔다.

### P2 — 303M GPU, 가장 분별력 높은 세 arm

8. **D1 non-commutative target** vs total-order vs partner-shuffle. STEP-0에서 유일하게 DPI escape 근거가 남은 objective다.
9. **D2+D9 intervention/hard-negative objective.** 같은 entity의 틀린 relation을 negative로 써 관계 자체를 학습시킨다.
10. **D10+E1 CE-deleted forward-slot.** 기존 additive cbind가 죽었으므로, additive aux가 아닌 forward computation 교체를 단 하나의 고위험 arm으로 시험한다.

### P3 — P2에 양의 gate slope가 있을 때만

11. E6 dual-stream, E7 recurrent deliberation, E9 relation-MoE를 순차 ablation한다.
12. D7/D8 set-diversity objective와 F4/F5 consequence selection을 결합한다.

## 4. 더 이상 재제안하지 않을 축

아래는 새 통제가 없는 한 소진된 아이디어다.

- 파라미터 수만 증가: 303M≈7B scale-invariant 전례 때문에 단독 scale은 레버가 아니다.
- generic falsifiable-form corpus 증량: form detector gaming으로 이미 반증됐다.
- additive HRR/TPR aux, composed-NCE 재발사: engine-native G1 floor.
- readout 뒤의 NMDA/bilinear/operator: latent target이 additive면 DPI를 못 벗어난다.
- 후보 수만 무제한 증가: quality-aware set selection 없는 brute K는 비용만 늘린다.
- fixed large window: pad-flood가 single arm을 무효화한다.
- literal keyword coverage만 최적화: echo와 relation composition을 구별하지 못한다.
- explicit store recall을 G1이라 명명: novel-chain 통제 없으면 G2/기억 faculty일 뿐이다.
- form critic 기반 revise-loop: 같은 detector를 최적화해 template replay를 강화한다.
- mitosis/growth만 추가: 비교환 target이 없으면 heldout은 chance에 머문다.
- generic predictive coding/consequence scalar를 output에 더하기: 기존 additive lane과 동형이다.
- G6 detector bar 완화: `[3,3,5]`를 PASS로 만들기 위한 threshold 이동은 금지한다.

## 5. 최종 추천

가장 가능성이 높은 단기 돌파는 서로 다르다.

- **G6:** 이미 genuine bind가 있으므로 `B1 set-wise selection + B3 adaptive budget + A6 intervention guard`가 첫 승부다. `[3,3,5]`는 거대한 capacity wall보다 후보 회수/집합 구성 벽에 가까운 관측이다.
- **G1:** 현재 가장 강한 후보는 `D1 non-commutative target`과 `D10+E1 CE-deleted forward-slot`이다. 다만 그 전에 `A1/A2 grow-window novel-only`로 측정 confound를 제거해야 한다.
- **공동 arm:** `D2 intervention-equivariance + D9 relation hard-negative`가 G1의 relation composition과 G6의 falsifiable relation을 동시에 직접 보상하며, 기존 additive-bind 실험과 가장 명확히 구별된다.

브레인스토밍의 실질적 고갈점은 여기다. 남은 변형은 대부분 위 축의 조합·하이퍼파라미터 변주이며, 새로운 인과 메커니즘이 아니다. 다음 단계는 아이디어 추가가 아니라 P0 네 실험으로 탐색벽/표현벽/학습벽을 분리하는 것이다.
