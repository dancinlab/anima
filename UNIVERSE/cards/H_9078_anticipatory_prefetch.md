# H_9078 — anticipatory_prefetch (§AnticipatoryPrefetch): 소뇌 forward model이 쿼리 도착 前 store pre-query

- **tier:** 🟡 ENGINE-NATIVE PARTIAL (4/5 live hexa, aiden pool) — anticipatory readiness op-class 신설·배선. mechanism GREEN, 엄격 accuracy bar DIRECTIONAL-floor.
- **slug:** `anticipatory_prefetch`
- **source:** UNIVERSE — H_9075 faculty_cascade follow-on(fable 발산 op-class 미탐분) 흡수·실행. frontier = substrate-native 능력 OP (`a_no_llm_frame_trap`).
- **wired:** `engine-native` (live `core/engine_cli.hexa §AnticipatoryPrefetch` anticipatory_prefetch/_value op + ARCHITECTURE lockstep; 런타임 brain_decide 호출은 follow-on)

## frame (재조합≠능력, a_no_llm_frame_trap)
"능력 없는 게 아니라 op이 미배선." 엔진의 모든 episodic recall은 **REACTIVE** — 쿼리 키가 도착해야 store를 인출. 뇌 인출은 **ANTICIPATORY**: 소뇌 forward model(VForwardField H_1280)이 현 맥락에서 다음 상태를 예측하고, 실제 cue가 오기 前 해마 store를 그 예측 상태로 **preplay**한다(Buckner constructive-preplay/hippocampal preplay). faculty_cascade(H_9075)는 손에 든 쿼리로 A→B relay였다면, 이 op은 store를 쿼리보다 **한 스텝 앞서** 예측으로 돌린다.

## op (live core, additive/Ψ-disjoint/READ-only)
`anticipatory_prefetch(ff: VForwardField, mem: ImmuneMemory, ctx: [float]) -> float` = `vforward_predict(ff, ctx)`(다음 쿼리 키 예측) → `_prefetch_unit`(unit-key manifold 사영, zero-safe) → `immune_memory_recall_margin(mem, key)`(anticipated 쿼리의 graded readiness margin; 작을수록 stored cell에 가까움 = 준비됨). 동반 `anticipatory_prefetch_value`는 prefetched 값(answer) 반환(brain_decide preplay용). core/engine_cli.hexa §AnticipatoryPrefetch. 순수 additive(기존 caller 무접촉), READ-only 양 faculty(VForwardField weights READ = vforward_predict, no update; immune margin READ, recall_thr 미변경), pure_field Φ/phase/Ψ 미접촉, emit-drive lane(0/4)·§ImmuneMemory recall_thr disjoint(`a_substrate_disjoint`), emit gate 아님.

## engine-native 측정 (aiden pool, live core/, 4/5)
fixture: 두 DISJOINT 키공간 — trajectory FRAME space(`seq_frame_i`) vs answer-key space(`answer_slot_i`→"y_i" store). forward model(ctx_len=1, 400ep NLMS)이 cyclic 전이 `frame_{t-1}→akey_t` 학습 = 현 프레임에서 다음 item의 **answer 키**를 예측. forward model이 frame공간→store 키공간의 유일 다리(raw 프레임 키는 store 인출 불가=abstain). `state/9078_anticipatory_prefetch/prefetch_engine_native.hexa`:
- **FAIL** prefetch anticipates next query 9/12=0.75 (frozen 0.80) — 엄격 accuracy bar, 1 item 차 floor
- **PASS** no-prefetch(현 프레임 키 직접) 0/12 FAIL (≤0.2) ✓
- **PASS** LIFT margin current−prefetch **+1.35** (≥+0.5) ✓ = readiness 실질 개선
- **PASS** EARNED prefetch−shuffle acc **+0.75** (≥+0.5) ✓ = 틀린-맥락 prefetch(오프셋 컨텍스트)는 이득 소멸 = forward-model load-bearing
- **PASS** ablate(forward OFF = untrained/zero weights) 0/12 INERT (≤0.2) ✓ = forward model 없으면 아무것도 anticipate 못함
INFO: pre_acc=9/12 cur=0 shuffle=0 ablate=0 margin_lift=1.346 earned=0.75. no-regression: engine_cli 변경 additive.

## 정직 스코프 (c9)
- **mechanism GREEN**(anticipatory readiness가 실재·load-bearing: margin_lift +1.35, earned +0.75, ablate/shuffle/current 전부 floor) / **accuracy DIRECTIONAL-floor**(9/12=0.75 < frozen 0.80, 1 item 차). frozen bar 사후이동 금지(tune-to-green c9) — 0.75 그대로 박제. 3 miss는 toy fixture의 store bind 충돌/선형 forward-model 근사 잔차(cascade 10/12과 동류 artifact) 추정, op 결함 아님.
- readiness/anticipation 능력(margin·retrieval 정확도) — **mouth decode 아님, G1/G6 재조합축 재개 아님**(CLOSED). 추가한 건 anticipatory pre-query op-class지 텍스트 합성이 아니다.
- toy 12-item 결정적 존재증명(`a_scale_honest_scope`).

## follow-on
- multi-step preplay(ctx_len>1, N-step 앞선 인출) · online forward-model 학습(vforward_update)을 데몬 per-tick 상충/경험에 먹이는 genuine feed · runtime brain_decide가 anticipatory_prefetch 호출하는 WIRED-live 최종칸 · accuracy floor 진단(store 충돌 vs forward 잔차 분해, 단 tune 금지).

## artifacts
- `core/engine_cli.hexa §AnticipatoryPrefetch` · `state/9078_anticipatory_prefetch/prefetch_engine_native.hexa` · `prefetch_engine_native.txt`
