# H_6164 — G6 IDEATION★ FALS 벽: 7B-class SINGLE-SHOT capacity 재학습 (Occam ②)

> DESIGN + PRE-REGISTRATION ONLY. commit·wire·fire 금지. GPU 는 explicit-go cost-gate.
> 다음 id = H_6164 (origin/main HYPOTHESES.jsonl tail = H_6163, stale-branch 회피 확인).

## 가설 (한 줄)
H_1449 verdict "WALL=CAPACITY, grounds 7B(a7b_pass)" 를 **가장 적은 변수**로 직접 시험:
303M-scale 이 G6 FALS 벽의 유일 한계자라면, **동일 4-cell 코퍼스**에서 warm-FT 한
7B-class CLMConvMoE trunk 은 G0🟢 전제 하에 h1305 5-bar 를 넘는가?

## 메커니즘
- base = `anima-clm-chat-7b` (registry 등록됨: 7B chat, chat-mix 레시피; CLMConvMoE = engine-mountable `.clm`, `CLM\x01` magic + CLMX trailer → generator L3 mouth → `clm_decode`). **warm-FT**(from-scratch 아님).
- 학습 진입 = `cli/train.hexa`(`anima train <7b.clm> <4cell-corpus> --savant`), golden-zone inhibition, engine-native(a_engine_native_learning). torch-side = DIRECTIONAL only.
- 산출 = 7B `.clm` (engine-mountable). H_1381 caveat 정면 회피: 303M ByteGPT ref 는 `.pt` 였고 engine path 는 ConvMoE `.clm` — 여기선 **처음부터 CLMConvMoE `.clm`** 로 만들어 mount 불일치 제거.
- 단일 변수 = trunk capacity(303M→7B). 코퍼스·objective·detector 전부 고정.

## FROZEN 5-bar (h1305 VERBATIM, 이동 0) + controls
검출기 = `core/g6_ideation.hexa:142 _g6_is_falsifiable` (FROZEN, calib 10/10): (a) comparator/conditional mark(`:44 _g6_comparator`) ∧ (b) measurable/quantity mark(`:50 _g6_measurable`) ∧ content≥2 ∧ non-question. **절대 완화 금지(p7).** fals 카운트 게이트 = kwr≥0.5 (`core/g6_ideation.hexa:272,:299`).
- **B1 FALS≥1** — 7B 생성 continuation 중 ≥1 개가 comparator+measurable 공동 emit.
- **B2 DIST≥5** — distinctness ≥5 (form-collapse 방지; H_1449 는 여기서 0~0.33 붕괴).
- **B3 X-SHUFFLE** — FALS_shuf < FALS_in (cross-shuffle 시 붕괴해야 진짜 결합; H_1449 는 shuf==in = interchangeable shell).
- **B4 HELD-OUT** — held-out prompt 에서 FALS≥1.
- **B5 vs-BASE** — 7B FALS > 303M ref(`anima-bytegpt-303m-h1129` = PRIVATE frozen bench, G1/G6 벽 reference).
- **c4 ABLATE** — capacity 기여를 격리: 7B lift 가 exposure(추가 학습노출) 때문이면 INERT. matched-exposure 통제 = 303M 을 동일 step/코퍼스로 warm-FT 한 arm 과 7B 를 비교; 7B 만 FALS 를 올리면 capacity, 둘 다면 INERT.
- **SHUF-CORP** — shuffled-corpus 로 warm-FT 한 7B lift < real-corpus lift (form-lift 아닌 실 capacity 확인).

측정 = **engine-native TERMINAL**:
```
anima evaluate --py state/6164.../<7b>.clm --corpus <4cell...> --gen N
```
`cli/evaluate.py`(numpy, torch/gauge grep-clean = TERMINAL; mouth = gen_auto_ideate → clm_decode). torch 학습 로그는 DIRECTIONAL, 최종 read 는 live core/ decode 재실행.

## 전제 게이트 (G6 측정 이전 필수)
**G0🟢 COHERENCE(known-word-ratio≥0.50) 선통과** 없이는 G6 측정 무의미. broad-7b 전례 = byte-garble G0 FAIL. G0🔴 이면 verdict 는 **INCONCLUSIVE-at-floor**(undertrain), 벽 아님 — G1 8000-step undertrain(g1-fromscratch-blocked-by-g0-undertrain) 과 동형. from-scratch 는 이 위험 극대(303M 8000-step 도 G0-undertrain) → **warm-FT 강제, from-scratch 금지**.

## disjointness (a_substrate_disjoint)
capacity/attention 은 mouth-internal(L24 trunk 이후, ln_f 이전) = emit-drive lane(15-state 0/4) 및 §ImmuneMemory recall_thr 와 disjoint → Ψ=½·G5 non-fab 보존. H_1381 h1205 separation-invariant guard 재사용. 7B ckpt 산출 후 Ψ-checksum + G5 non-fab guard 로 큰 mouth 가 emit/정직 lane 미교란 확인(mouth ⊥ identity/tool).

## 정직한 confound (a_no_llm_frame_trap) — "단순"이 받아들이는 것
동일 web-prose 4-cell 코퍼스에는 falsifiable-claim register 가 거의 없다(H_1596e/H_1597, corpus-grounded Hangul detector 도 0/18). 그래서 이 single-shot 은 **capacity 와 register 를 분리하지 못한다** — 7B 가 그냥 "더 큰 web-prose" 를 낼 위험. ②단순은 이 confound 를 의도적으로 수용: 답하는 질문은 *"303M-scale 이 한계자인가?"*(이진, 깨끗) 이지 *"capacity냐 register냐"* 가 아니다. 후자 분해는 register-enriched arm(비-Occam 설계)이 필요.

## scale 정직 스코프 (a_scale_honest_scope / break-walls)
단일 7B rung = **DIRECTIONAL only**. scale LAW 주장은 ≥3-rung ladder(303M ref · 1B · 7B) + 통제 필요. 이 H 는 1-rung 이므로 "capacity 축이 방향성 있나" 만 준다.

## 정직한 결정규칙 (GREEN vs 🧱 vs INCONCLUSIVE)
- **INCONCLUSIVE-at-floor** — G0🔴(byte-garble/undertrain). 벽 아님, step↑ 재발사(infra).
- **DIRECTIONAL-GREEN(capacity 는 한계자였다)** — G0🟢 ∧ B1–B5 ∧ SHUF-CORP(real>shuf) ∧ c4 not-INERT. 단, 동일 코퍼스라 capacity×register **confounded** → "303M-scale 은 한계자였다=YES" 는 깨끗하나 "capacity vs register" 는 미분해. wired=DIRECTIONAL; 배선 follow-on(register arm + ≥3-rung ladder) ING 등록.
- **🧱 WALL-NOT-CAPACITY-ALONE** — G0🟢 인데 FALS 여전히 0/N. 7B 로도 안 열림 → capacity 단독 아님, H_1597 register cause 와 수렴 → corpus-register lane 으로 pivot. 정직한 유효 결과(c9).
- **c4 INERT / SHUF-CORP 실패** — lift 가 exposure/form 이면 capacity 주장 기각(H_1449 재현).

## host / cost (explicit-go gate)
- warm-FT 7B CLMConvMoE, 수천 step, 4-cell 코퍼스: 대략 **1–3 H100-day**(a_wall_first: 다중 H100 병렬로 wall↓ 가능). from-scratch = ~10–50 H100-day + G0-undertrain 위험 → 배제.
- GPU = `hexa cloud`/`hexa dojo`, cost-gate: **owner explicit go 필요**(a_fire_autonomous vs cost-gate 미해결 충돌 → 사용자 명시 지시 우선). mini 금지, pool/렌트만(heavy).
- teardown 전 `.clm` ckpt PULL 필수(a_fire_recover_complete) → HF 업로드(G0∧G1∧G2 = a7b_pass closure PASS 면 PUBLIC, 아니면 PRIVATE/WIP) → ARCHITECTURE.json models 노드 1줄 등록(a_hf_registry) → 그 다음 teardown. JSON 만 받고 ckpt 버림 금지.

## 배선 사다리 (a_verified_must_wire)
GREEN 시: (1) DIRECTIONAL 7B → (2) engine-native byte-exact 재검증(anima evaluate --py) → (3) live core/ mount 확인 → (4) ARCHITECTURE.json models lockstep. 각 미완 = ING follow-on.

## 참조 벽 (재발사 금지 = tune-to-green)
scaffold/best-of-K(H_1590🔴·H_1381 REFUTED), revise-loop/deep-eq/MLC(H_1836/1837/1835🧱), $0 detector-coherence(weld·embedding H_1455·proximity 🧱), **H_1449 1-block attn @303M 🧱 CAPACITY**(driver state/1449_g6_attention_injection/h1449_attention_injection.py). 본 H 의 신규 축 = trunk **scale**(303M→7B), 위 축들과 다른 배선.
