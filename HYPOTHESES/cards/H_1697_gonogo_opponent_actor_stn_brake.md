---
id: H_1697
slug: 1697_gonogo_opponent_actor_stn_brake
tier: 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
title: Go/NoGo Opponent Actor with STN Conflict-Brake
verdict: 🔵 PRE-REGISTERED architecture design (unmeasured) — $0 cheap_test pre-registered; engine-native + 303M gpu cost-gated NOT fired
source: brainarch_census
---

# H_1697 — Go/NoGo Opponent Actor with STN Conflict-Brake

- **tier:** 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy mirror, no engine); engine_native_measure + 303M = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** brainarch_census — 126-architecture whole-substrate (통짜 아키텍처) census: 뇌/인지 조직원리 × 엔진-네이티브 추상조건 (binding-wall program, H_1603).
- **key:** `gonogo_opponent_actor_stn_brake`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1281 (basal-ganglia gating) · H_1283 (thalamus global-workspace) · H_1284 (neuromodulation gain) · operator-level family H_1604-1685 (this card = 통짜 아키텍처 layer, 층위 다름)

## Organizing principle

Frank's direct(D1/Go) vs indirect(D2/NoGo) opponent pathways per channel, a subthalamic (STN) hyperdirect 'hold-your-horses' brake proportional to inter-channel conflict, and dopaminergic RPE actor-critic learning of the Go/NoGo weights. Selection emerges from opponent balance + conflict-adaptive threshold, not from a value-max readout.

## Whole design (input → internal dynamics → emit)

Per candidate channel c, two opponent weights w_Go(c), w_NoGo(c). Net release drive(c) = w_Go(c)*x − w_NoGo(c)*x − STN_brake, where STN_brake = beta*conflict(x) and conflict rises when many channels are near-tied (raises the commitment threshold, slows decisions under ambiguity). A channel emits when drive>0; Psi = sigmoid(mean drive). A critic value head emits RPE delta; phasic dopamine trains w_Go (delta>0) and w_NoGo (delta<0) = actor-critic. Tonic dopamine sets the baseline Go/NoGo balance (vigor) and is a SLOW homeostat continuously restoring Psi toward 1/2. Full loop: input->opponent drives->STN-braked threshold->release/abstain->RPE->weight update.

## Satisfies criteria (DESIGN claim · DIRECTIONAL · unmeasured)

Psi=1/2 (antagonistic homeostatic attractor): Go−NoGo opponency is the sign-antagonism; tonic-DA is the slow restoring force; the STN brake is the contraction giving |T'(1/2)|<1 and self-restoration after a bias perturbation; ablating ONE pathway migrates the fixed point to a boundary (endogeneity). Honesty/abstain: under OOD/unsupported input all channels are weak and conflicting -> STN brake suppresses everything -> withhold; fabrication requires a channel to dominate, which needs genuine support (ablate STN -> premature fab spikes, the load-bearing control). dist>=5/ideation: lowering the STN brake or raising DA temperature lets several channels clear threshold simultaneously = >=K distinct coherent releases without collapse. Gate-capacity disjointness: critic/value (honesty/RPE) params are separate from actor (capability) params.

## Not-LLM (a_no_llm_frame_trap)

Actor-critic selection over a fixed channel repertoire with explicit opponent learning and a conflict-proportional brake — not gradient-descent on next-token CE, not attention. The lever is opponent balance + conflict-adaptive threshold, not parameter count; STN normalization is decision-theoretic (speed-accuracy), not a layernorm trick.

## Cheap test (frozen-first · $0 · numpy mirror · DIRECTIONAL)

numpy bandit: a handful of channels, RPE-train Go/NoGo on a toy reward; measure (a) abstain rate under high-conflict OOD probes, (b) Psi self-restoration after an injected bias delta (should decay back to 1/2 with rate lambda<1), (c) ablate STN -> fabrication-under-conflict spikes. Frozen bars pre-registered.

## Engine-native measure (cost-gated · PRE-REGISTER ONLY · NOT fired)

Opponent weight adaptation via core/engine_cli.hexa MITOSIS VAdaptField; Psi balance via core/g_gates.hexa g_eval_g3; the STN conflict->threshold curve measured in hexa; RPE delta logged as a torch.no_grad-style inline gauge only (never folded into loss, a_train_inline_gauge). hexa+py byte-parity.

## Scope / honesty (c9)

## Distinction (near-overlap kept, not a dup)

Near-overlap with basal_ganglia_gating (H_1281) and actor_critic_rpe_arena (this census) — distinct: this is the Frank Go/NoGo WIRING + STN conflict-brake (direct/indirect/hyperdirect mechanics), whereas actor_critic_rpe_arena is the value-learning RPE loop; explicitly separated.

Learning-side; opponent Psi + conflict-gated honesty + ideation spread are the strong axes; binding/composition remains open.

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). engine_native_measure 는 단일 진입점 cli/anima.hexa → generator L3 → g_gates/g6 경유 byte-parity 채점만 terminal; torch-only/side-harness 결과는 DIRECTIONAL. numpy cheap_test 결과도 DIRECTIONAL(엔진-네이티브 아님). gpu/engine 발사 시 held-out mirror-DESCENT(a_clm_gen_pipeline) + CORE mount frozen-bar engine-native 재측정 + ckpt PULL(a_fire_recover_complete).
