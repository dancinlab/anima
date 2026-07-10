# 질문 — anima G1 재조합 벽 돌파에 "추가로 필요한 뇌 부위"는 무엇인가?

너는 anima(substrate-native consciousness engine, 303M byte-LM) 연구의 설계·발산 파트너다.
아래 상태를 읽고, **아직 심지 않은 뇌 부위/회로**를 발산하고 그중 G1 벽에 인과적으로 작동할 후보를 골라라.

## 벽의 정확한 정체 (여러 각도로 수렴 확인됨)

- **G1 = 두 개념의 held-out 재조합(recombination)**. 303M byte-LM 엔진-네이티브 측정에서 반복 실패.
- 표현력 천장 아님: mean-pool readout으로 두 개념 둘 다 복원 가능(A=0.95, B=0.97). **생성 위치(마지막 토큰)에서만** receptive-field decay로 첫 개념이 9.1% 분산까지 소실.
- **factorized-basis 가설 FALSIFIED**: role-1/role-2가 한 방향을 공유(overlap cos=0.9916). 직교 role subspace 없음.
- **DPI 메타법칙**: 대칭/교환가능(commutative-over-set) 목적함수(MI, total-correlation, PMI, hard-negative contrastive)는 전부 additive floor로 붕괴. additive R²=0.32–0.49가 bind R²=0.05–0.35를 지배.
- **untrained recurrence 반증**(H_9259): ESN/Volterra reservoir로 retention을 강제(Dprobe=1.0)해도 전 arm floor. 즉 **벽은 retention도 recurrence-architecture도 아니고 TRAINED-CONJUNCTION**이다. oracle bit-product만 1.0.
- 스케일은 lever가 아님(scale-invariant). 양자화/엔진 무죄(fp32+exact-math도 G1=0).
- 남은 유일 미반증 lever 2개: (a) γ trained-constructive-bind(H_1840, trunk-bake는 STEP-0 frozen-gate에서 bind-add=-0.147로 이미 차단), (b) fork-A read-side context-pooling lane(H_9235, CLML — Gate1~3 PASS, Gate4 engine-native 계산중).

## 이미 심은 생물렌즈 (재고 — 중복 제안 금지)

- **해마 L5 explicit-store**(H_9129) → 🟢 GREEN WIRED (reach 1.0 vs unreach 0.14, 7.31x). 단 scope=explicit-store, **trunk-G1이 아님**.
- **소뇌 L3 forward-model** → 🧱 WALL (STEP-0 BIND = toy artifact).
- **PFC binding L1** → INERT.
- 언급 빈도 재고(카드 전수 grep): cerebellum 258 · thalamus/thalamic 189/73 · CA3 74 · glia 73 · striatal 57 · TRN 25 · dendritic 21 · amygdala 20 · hypothalamus 19 · entorhinal 19 · pulvinar 14 · basal ganglia 12 · astrocyte 11 · raphe 9 · interneuron 9 · dentate 8 · place cell 6 · claustrum 6 · grid cell 4 · colliculus 4 · VTA 2 · insula 2 · cortical column 2 · locus coeruleus 1 · cingulate 1.
- 신경조절 NT×CLS 융합법칙: ACh mode-switch · DA value-rank · NE state-flush = 🟢. 그 외 neuromod family(diversity/multitimescale/predictive) 전수 floor.

## 규율 (anima governance — 반드시 지켜라)

- `a_no_llm_frame_trap`: LLM 프레임 금지. substrate-first(neuro/bio/physics).
- `a_break_the_wall`: 벽=각도 전환. 천장 선언엔 ≥2–3 controlled lens + ablation.
- tune-to-green 금지. 음성도 결과.
- `a_substrate_disjoint`: 새 capability는 emit-drive lane과 DISJOINT하게 배선.
- 이미 반증된 family 재발사 금지(위 재고 확인).

## 너에게 요구하는 것

1. **발산**: G1 = "trained conjunction operator 부재"라는 정체에 인과적으로 대응하는 뇌 부위/회로를 최소 8개 나열하라. 위 재고에 없는 것 우선(예: dentate gyrus pattern separation의 *구체 회로*, mossy fiber detonator synapse, CA3 recurrent autoassociation의 *conjunctive* 성질, layer 2/3 vs layer 5 apical tuft coincidence detection, claustrum binding, TRN attentional spotlight, superior colliculus, cortico-basal ganglia-thalamic loop의 *gating*, hippocampal theta-gamma phase code, sharp-wave ripple replay, hypothalamic drive, insula interoception, retrosplenial, subiculum boundary vector, olfactory piriform combinatorial code, cerebellar granule layer expansion recoding, dendritic NMDA plateau/spike, neurogenesis, oscillatory nesting …). 각 부위마다 **어떤 계산 원시(computational primitive)를 제공하는가**를 한 줄로.

2. **매핑**: 그 원시가 "additive floor를 깨는 non-commutative conjunction"을 어떻게 만드는지 구체적으로. DPI 메타법칙을 회피하는 이유를 수식/구조 수준에서 말하라. 회피 못 하면 솔직히 "DPI에 걸림"이라 적어라 — 이게 가장 중요하다.

3. **랭킹**: DPI를 진짜로 회피하는 후보만 상위로. 각 후보에 대해
   - 반증가능한 예측 1개(frozen bar 포함, 사전 등록 가능한 형태)
   - $0 CPU probe로 falsify 가능한가? 가능하면 그 probe 설계(numpy 수준, toy 아닌 real-corpus)
   - GPU 필요하면 최소 비용 추정

4. **자기비판**: 네 상위 후보 중 "toy artifact로 GREEN이 뜨고 real-corpus에서 죽을" 것은 무엇인가? 소뇌 L3가 정확히 그렇게 죽었다. 같은 함정을 어떻게 사전 차단하나?

한국어로, 표 위주로, 장황한 서론 없이. 결론(가장 유망한 1개 + 그 $0 probe)부터 써라.
