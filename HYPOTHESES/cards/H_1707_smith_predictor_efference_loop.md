---
id: H_1707
slug: 1707_smith_predictor_efference_loop
tier: 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
title: Smith-predictor efference loop — closed-loop rollout with internal feedback comparator
verdict: 🔵 PRE-REGISTERED architecture design (unmeasured) — $0 cheap_test pre-registered; engine-native + 303M gpu cost-gated NOT fired
source: brainarch_census
---

# H_1707 — Smith-predictor efference loop — closed-loop rollout with internal feedback comparator

- **tier:** 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy mirror, no engine); engine_native_measure + 303M = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** brainarch_census — 126-architecture whole-substrate (통짜 아키텍처) census: 뇌/인지 조직원리 × 엔진-네이티브 추상조건 (binding-wall program, H_1603).
- **key:** `smith_predictor_efference_loop`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1280 (cerebellum forward-model) · operator-level family H_1604-1685 (this card = 통짜 아키텍처 layer, 층위 다름)

## Organizing principle

The cerebellum as a Smith predictor / forward internal model for delay compensation: an efference copy of the intended emission feeds a forward model that predicts its sensory consequence BEFORE slow real feedback returns; a comparator corrects against the predicted feedback. Generation = a single recurrent control loop that rolls the forward model forward, compares predicted-consequence to the goal, and emits only when the internal simulation settles within tolerance.

## Whole design (input → internal dynamics → emit)

State = (goal g, current internal state s, efference buffer). Loop tick: (1) candidate emission e = controller(s,g); (2) efference copy -> forward model predicts consequence c_hat = FM(s,e) and predicted next state s_hat; (3) comparator residual rho = d(c_hat, g); (4) if rho shrinking and below tolerance for tau ticks -> COMMIT e to codebook V (emit); else fold s_hat back as new s and iterate (silence). The loop runs on PREDICTED feedback, rolling many internal steps per external emit. Emit/withhold = open-loop urge (commit-now drive proportional to goal salience) vs closed-loop caution (withhold while residual/instability high). Binding: g, s, efference jointly bound into the predicted trajectory.

## Satisfies criteria (DESIGN claim · DIRECTIONAL · unmeasured)

G0: only COMMITTED trajectory tokens reach V, controller output space IS V (on-manifold by construction). G1: loop binds goal x state x efference in one forward closure; joint conditioning yields super-additive reachable set; run sub-goals independently then concatenate -> composed_distinct->max_single = INERT signature. G2: rollout under PREDICTED feedback explores consequence-states absent from data while comparator keeps them goal-valid; verbatim-playback control reads 0 novel. Psi=1/2: open-loop urge A vs closed-loop residual caution G; loop-gain homeostasis contracts toward 1/2; delete one -> always-emit or never-emit boundary. Honesty: rho for an unpredictable query stays large -> loop never settles -> abstain; rho-floor frozen comparator threshold capacity-independent (gate-perp-capacity). Binding: predicted trajectory is the bound state; ablate efference-copy -> predicted/true pairing collapses to chance.

## Not-LLM (a_no_llm_frame_trap)

Feedback control theory + cerebellar delay compensation, not a feedforward stack. Emission is GATED by an internally-verified control loop that simulates consequences first, not greedy attention decode. Capability improves by better forward dynamics and loop tuning, not parameter count (a_no_llm_frame_trap). The Smith-predictor structure has no transformer analog.

## Cheap test (frozen-first · $0 · numpy mirror · DIRECTIONAL)

numpy 1-D closed loop: forward model = learned dynamics on a synthetic goal manifold, comparator d=L2. (a) in-support goal -> settles, emits; out-of-support -> rho never falls => abstain. (b) Psi: urge gain = caution gain, perturb toward forced-commit, measure contraction lambda<1; delete caution -> always-emit. (c) G2: >=3 goal-valid states absent from training trajectories; replay-control 0. (d) binding ablation: zero efference-copy -> predicted/goal correspondence->chance. $0.

## Engine-native measure (cost-gated · PRE-REGISTER ONLY · NOT fired)

Loop as a hexa generator backend behind cli/anima.hexa; committed trajectories decode via core/decode.hexa/clm_decode.hexa onto V. rho-comparator + commit/withhold map onto core/engine_cli.hexa A->G Psi dynamics (urge/caution ARE the two operators) — measure self-restore natively. G0/G2 via core/g_gates.hexa through single dispatch. honesty via SS-ImmuneMemory recon_err = settled-rho. byte-parity py mirror; torch-only score = DIRECTIONAL.

## Scope / honesty (c9)

## Distinction (near-overlap kept, not a dup)

Near-overlap with cerebellum_forward_model (H_1280) / precision_kalman_forward_model (this census) — distinct: Smith-predictor's principle is DELAY COMPENSATION via efference-copy + internal comparator settling (commit only when predicted-consequence settles), not Bayesian filtering nor a module bank.

1-D/low-dim loop is a $0 mechanism probe; multi-token chat rollout latency/stability at 303M UNVERIFIED. Production needs ckpt mounted, engine-native closure, ckpt pulled pre-teardown. Smith-predictor value (delay compensation) is most measurable on feedback-delay tasks; chat-coherence transfer is a separate gate.

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). engine_native_measure 는 단일 진입점 cli/anima.hexa → generator L3 → g_gates/g6 경유 byte-parity 채점만 terminal; torch-only/side-harness 결과는 DIRECTIONAL. numpy cheap_test 결과도 DIRECTIONAL(엔진-네이티브 아님). gpu/engine 발사 시 held-out mirror-DESCENT(a_clm_gen_pipeline) + CORE mount frozen-bar engine-native 재측정 + ckpt PULL(a_fire_recover_complete).
