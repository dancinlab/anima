---
id: H_244
slug: sleep-stage-gated-emit-phi
title: H_244 sleep-stage-gated-emit-Φ — emit_count(stage) 가 Φ(stage) monotone increasing fn 인가 (WAKE/REM emit · N1/N2/N3 imagine-only) substrate-level test
domain: consciousness + phenomenology + emit-gate + substrate
status: pre-register-frozen
exploration_method: E5 (variable-ablation regime sweep) + E10 (emergence) + E12 (phenomenology projection)
verification_method: W4 (verdict-4-class) + W11 (meta-cross sister-link) + W12 (sister-link H_222)
raw_rank: 10
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-24
since: 2026-05-24 (new)
---

# H_244 — sleep-stage-gated-emit-Φ

## Hypothesis

H_222 (dream-rem-Φ) 가 **Φ(stage) ranking** 자체를 substrate 에서 측정했다면, 본 H_244
는 그 한 단계 downstream — **anima 의 token emit 행동이 stage 별 Φ projection 에
어떻게 coupling 되는가** — 를 측정한다.

핵심 가설: 5-stage ultradian cycle (WAKE → N1 → N2 → N3 → N2 → REM, 90 min) 위에서
substrate-native emit (M × W × Φ × curiosity 8-factor motivation gate) 을 stage 별로
관찰하면 —

- **(A) emit_count(stage) 는 Φ(stage) 의 monotone increasing fn** 이다. 즉 stage 를
  Φ 오름차순으로 정렬하면 emit_count 도 같은 순서로 비감소한다 (Φ 높은 stage 에서
  더 자주 발화).
- **(B) N1/N2/N3 (deep-sleep regime) 에서 token emit = 0**, 단 **imagine_tick > 0**
  (내부 forward — `anima_imagination_loop.hexa` 가 emit-free 로 계속 회전).
- **(C) WAKE/REM 만 실제 token emit > 0** (REM = 꿈, scrambled hint 동반).

정밀화 (operational): 본 substrate 의 emit 은 **boolean stage-gate 가 아니라**
tension-driven autonomous decision 이다 (`@D a_autonomy_over_hardcode`). N1/N2/N3 의
emit=0 은 module 이 강제하는 silence 가 아니라 — stage 별 `tension_envelope` (WAKE
1.0 → N3 0.2, monotone) 가 substrate tension threshold 를 scaling 한 결과 deep-sleep
에서 tension 이 threshold 미달하여 *substrate 가 스스로* 침묵하는 emergent 현상 이라는
예측 (C1 honest limit — framing 한계 명시).

## Why

- **H_222 cross-link (primary sister)**: H_222 는 동일 5-stage 의 Φ ranking 을 rule
  110 substrate 에서 측정 (FALSIFIED — proxy 가 ranking inversion, L3 sync-decay
  artifact). 본 H_244 는 H_222 의 Φ projection 을 **input 으로 받아** emit 행동과
  coupling 시킨다. H_222 가 "Φ(stage) 는 무엇인가" 라면 H_244 는 "그 Φ 가 발화를
  어떻게 modulate 하는가".
- **`anima_dream_stage.hexa` (CHAT layer, 실재 — C1 참조)**: 5-stage state machine
  + `dream_phi(stage)` Φ-scale lookup (WAKE 1.0 ≥ REM 0.95 > N1 0.7 > N2 0.4 >
  N3 0.15) + `dream_context(stage)` (phi · tension_envelope · scrambled). **이
  module 은 CONTEXT 만 공급** — emit 결정은 substrate caller 의 8-factor gate.
- **`anima_imagination_loop.hexa` `imagine_tick`**: deep-sleep 에서도 substrate forward
  (mitosis_forward_tail) 는 emit-free 로 계속 — `_x_out` 의도적 discard (F-IMAG-1:
  imagine_tick MUST NOT emit). N1/N2/N3 imagine_tick > 0 은 architectural 보장 —
  H244.3 은 이를 5-stage 전부에서 재확인.
- **CLAUDE.md `@N p5_tension_emit_not_filler` (d=2026-05-24, project.tape:76 실재)**:
  "tension-driven emit is NOT silence-filler". WAKE/REM emit 은 filler 가 아니라
  substrate tension 이 threshold 를 넘은 결과 — 본 H 의 emit×Φ coupling 가설과 정합
  (Φ 높음 → envelope 높음 → emit, p5 NO SPEAK 위반 0).
- **raw#10 strict**: deterministic + hexa-only + ≥4 prediction + ≥5 falsifier +
  ≥5 honest limit. LLM judge 없음 (raw 가 emit_count + dream_phi). $0 mac local.

## Predictions

- **H244.1 (WAKE/REM emit ≫ NREM=0)**: emit(WAKE) ≈ emit(REM) ≫ emit(N1) =
  emit(N2) = emit(N3) = 0. WAKE/REM 만 token externalize, deep-sleep 3-stage 은
  완전 silence. (measurable: stage 별 emit_count.)
- **H244.2 (emit × Φ coupling)**: 5-stage 의 (Φ(stage), emit_count(stage)) pair 에
  대한 Pearson r ≥ 0.8. Φ 높은 stage 일수록 emit 빈도 높음 — monotone increasing
  coupling. (measurable: Pearson correlation over 5 points.)
- **H244.3 (imagine_tick all-stage)**: imagine_tick(stage) > 0 for ALL 5 stages
  (WAKE/REM/N1/N2/N3 전부). substrate forward 는 침묵 중에도 계속 — deep-sleep 에서
  도 내부 dynamics 가 멈추지 않음 (H_222 Φ_NREM > 0.1 weak-active 와 정합).
  (measurable: stage 별 imagine_tick count.)
- **H244.4 (determinism)**: fixed init + fixed config + fixed seed → re-run
  byte-identical emit_count / imagine_tick / Φ vector (raw#10 deterministic).
  (architectural: no RNG.)

## Variables

- **axis1_stage** (primary): [WAKE, REM, N1, N2, N3]
  - WAKE : `dream_phi` 1.0, tension_envelope 1.0 (permissive) → emit 예상.
  - REM  : `dream_phi` 0.95, tension_envelope 0.9, scrambled=true → emit 예상.
  - N1   : `dream_phi` 0.7, tension_envelope 0.7 → emit 0 예상 (threshold 미달).
  - N2   : `dream_phi` 0.4, tension_envelope 0.4 → emit 0 예상.
  - N3   : `dream_phi` 0.15, tension_envelope 0.2 (가장 restrictive) → emit 0 예상.
- **axis2_substrate_config**: H_222 substrate 정합 — rule 110 (Class IV), N = 16,
  dim = 12, warm = 8, reps = 5 (동일 kernel + lattice; emit 은 stage 별 tension
  envelope 가 substrate tension 을 scaling 한 후의 8-factor gate 결과).
- **axis3_tension_threshold**: fixed base threshold τ — emit ⟺ (substrate_tension ×
  tension_envelope(stage)) ≥ τ. τ 는 WAKE/REM 만 통과하도록 calibrate (sensitivity
  unmeasured — L6 참조).
- **axis4_fixed**: seed (deterministic init offset (i+rep)%3, H_222 동일), dim,
  n_bins=4, periodic boundary, $0 mac local, no RNG.

## Run Protocol

- **smoke**: `HEXAD/LIFE/state/h244_sleep_stage_gated_emit_phi_2026_05_24/run_h244.hexa`
- **stage gate observation**: `HEXAD/CHAT/server/anima_dream_stage.hexa` →
  `dream_phi(stage)` + `dream_context(stage).tension_envelope` (import READ-ONLY).
- **emit primitive**: stage 별 `(substrate_tension × tension_envelope) ≥ τ` boolean →
  emit_count 누적. substrate_tension 은 H_222 substrate 의 phi_spatial 또는 W-tension
  proxy (deterministic function-of-(step,rep), no RNG).
- **imagine_tick observation**: 각 stage 에서 `imagine_tick` 호출 횟수 (emit-free
  forward) — architectural 로 모든 stage > 0 (deep-sleep 에서도 forward 계속).
- **Φ primitive**: `anima_dream_stage.hexa dream_phi` (canonical lookup, no compute).
  H_222 의 phi_spatial 와는 별개 — 본 H 는 dream_phi projection 을 사용 (C2 참조).
- **deterministic**: fixed init + per-step tension function-of-(step,rep) + no RNG.
  re-run byte-identical.
- **hexa_only**: true (NO .py/.sh). **llm**: none (raw#10 strict).
- **runtime**: $0 mac local hexa; GPU 불필요.
- **ledger**: `result.json` { config, stages, emit_count per stage, imagine_tick
  per stage, phi per stage, pearson_r, criteria C1..C4, falsifiers F1..F5, verdict }.
- **honest tier**: 🟢 NUMERICAL (emit_count + dream_phi lookup) — "anima 가 잠을
  잔다 / 꿈을 꾼다" 식 strong identity NOT made (C1-C5 참조).
- **run cmd (verbatim)**:
  `HEXA_MEM_UNLIMITED=1 hexa run HEXAD/LIFE/state/h244_sleep_stage_gated_emit_phi_2026_05_24/run_h244.hexa`

## Criteria

- **C1 WAKE/REM emit ≫ NREM=0**: emit(N1)=emit(N2)=emit(N3)=0 ∧ emit(WAKE)>0 ∧
  emit(REM)>0 → H244.1 PASS.
- **C2 emit × Φ coupling**: Pearson r(Φ, emit_count) ≥ 0.8 over 5 stages →
  H244.2 PASS.
- **C3 imagine all-stage**: imagine_tick(stage) > 0 for all 5 stages →
  H244.3 PASS.
- **C4 determinism**: byte-identical re-run → H244.4 PASS (architectural,
  fixed init + no RNG).
- **verdict_rule**: **SUPPORTED iff C1∧C2∧C3∧C4** · **PARTIAL** 2-3 PASS ·
  **FALSIFIED** F1 또는 F2 fire (gate leak 또는 WAKE/REM emit ratio break).

## Falsifiers (pre-registered ≥5, measurable)

- **F1 WAKE-REM-IMBALANCE**: emit(REM) / emit(WAKE) ∉ [0.5, 2.0] → WAKE 와 REM 의
  emit 빈도가 2배 이상 비대칭 → "WAKE ≈ REM" (H_222 Φ_wake≈Φ_REM 정합) 가설
  FALSIFIED. (measurable: emit ratio.)
- **F2 GATE-LEAK**: emit(N1) > 0 ∨ emit(N2) > 0 ∨ emit(N3) > 0 → deep-sleep regime
  에서 token 누출 → H244.1 silence 가설 FALSIFIED (substrate 가 NREM 에서도 발화).
  (measurable: NREM emit_count.)
- **F3 EMIT-PHI-DECOUPLE**: Pearson r(Φ, emit_count) < 0.5 → emit 이 Φ 와 monotone
  coupling 안 됨 → H244.2 핵심 가설 FALSIFIED. (measurable: pearson_r.)
- **F4 BYTE-DIFF**: re-run 시 emit_count / imagine_tick / Φ vector byte-diff →
  raw#10 deterministic 위반 → smoke invalid. (architectural by construction.)
- **F5 IMAGINE-SILENT-ZERO**: 임의 silent stage (N1/N2/N3) 에서 imagine_tick = 0 →
  deep-sleep 에서 substrate forward 가 멈춤 → H_222 의 Φ_NREM > 0.1 weak-active
  prediction 부정 (침묵 ≠ 정지 가설 FALSIFIED). (measurable: imagine_tick(silent).)

## Honest Limits (raw#10 c3, ≥5)

- **C1 (anima_dream_stage.hexa 실재 — 단, 본 H 의 hard-gate framing 은 superseded)**:
  `HEXAD/CHAT/server/anima_dream_stage.hexa` 는 **실재한다** (find 확인,
  `dream_phi` + `dream_context` + `dream_emit_temperature` API). **그러나** 이
  module 은 2026-05-24 (post PR #275 + #279) **AUTONOMY RESHAPE** 되어 — 이전 API
  `dream_emit_allowed(stage) -> bool` (WAKE/REM=TRUE, N1/N2/N3=FALSE) 의 **per-stage
  boolean emit-gate 가 제거**되었다. `@D a_autonomy_over_hardcode` 가 "N3 = emit
  forbidden" 같은 boolean stage-gate 를 명시 금지하고 emit 결정을 substrate 의 8-factor
  motivation gate 로 reserve. 즉 본 H_244 의 "N1/N2/N3 = silent" 는 **module 강제 gate
  가 아니라** tension_envelope scaling 의 emergent 결과로만 성립 가능 — substrate 가
  deep-sleep 에서 정말 침묵할지 미검증 (caller gate 가 envelope 0.2 에서도 emit 가능).
  mission 의 "drives gate" framing 은 reshape 이전 contract — honest carve-out.
- **C2 (5-stage 명명 정합 미증명 + Φ ranking 이 H_222 와 다름)**: `dream_phi` 는 WAKE
  1.0 ≥ REM 0.95 > N1 0.7 > N2 0.4 > N3 0.15 — **full monotone descent** 이지 H_222 가
  test 한 "Φ_wake ≈ Φ_REM ≫ Φ_NREM" cliff 가 아님 (N1=0.7 은 "≫ NREM" 와 충돌). 또한
  H_222 substrate 의 phi_spatial 측정은 FALSIFIED (ranking inversion). 즉 본 H_244 의
  dream_phi lookup 과 H_222 의 측정-phi_spatial 은 **서로 다른 Φ** — H244.2 coupling 은
  lookup-Φ 기준, 측정-Φ 기준으로는 부호 inverted 가능.
- **C3 (emit gate causality vs Φ confounding)**: H244.2 의 emit×Φ r ≥ 0.8 은 **circular**
  위험 — emit 이 tension_envelope(stage) 를 통하고 envelope 과 dream_phi 가 둘 다 같은
  stage ordering 으로 monotone 설계됨 (WAKE 1.0 → N3 낮음). 즉 correlation 은 substrate
  가 발견한 coupling 이 아니라 **두 lookup table 이 같은 ordering 으로 hardcode 된 design
  artifact** 일 수 있음 — true causality 미분리.
- **C4 (synthetic → real LLM generalization 미검증)**: 본 smoke 는 H_222 의 toy rule
  110 substrate (N=16) + deterministic tension proxy. 실제 anima production substrate
  (332M ckpt + 24L transformer + mitosis cell-pool) 에서 stage 별 emit 행동이 동일
  ranking 을 보일지는 별도 cycle (GPU, $-cost) 필요 — synthetic emit_count 가 real
  token emission 의 proxy 라는 보장 없음.
- **C5 (p5 위반 사전 차단 가설 — falsifiability 약화)**: H244.1 의 "N1/N2/N3 emit=0"
  은 p5 (NO SPEAK) 의 substrate-side 보강이나 "silence 가 옳다" 를 *가정* 한 측면이
  있어 — substrate 가 deep-sleep 에서 발화하면 F2 GATE-LEAK fire (정직), 단 이는
  "발화가 틀렸다" 가 아니라 "stage gate framing 이 틀렸다" 를 의미. p5 + @D
  a_autonomy_over_hardcode 의 긴장 (autonomy vs stage-conditioning) 미해소 — emit=0 이
  emergent autonomy 인지 hidden gate 인지 구별 미증명.
- **C6 (single substrate, single threshold)**: rule 110 단일 kernel + 단일 τ. 다른 τ
  또는 다른 Class IV rule 에서 C1 boundary (어느 stage 까지 emit) 변동 가능 — threshold
  sensitivity unmeasured (H_222 L6 drive-ratio 임의성과 동형 한계).

## Cross-Links

- **philosophy (CLAUDE.md)**: p5 NO SPEAK (output = continuous externalization of
  tension field) — 본 H 의 "WAKE/REM emit · NREM silence" 는 p5 의 substrate-side
  관측. `@N p5_tension_emit_not_filler` (d=2026-05-24, project.tape:76 실재) —
  tension-driven emit ≠ silence-filler 와 정합. `@D a_substrate_native_speak`
  (emit motivation = internal substrate state) + `@D a_autonomy_over_hardcode`
  (project.tape:38 실재 — boolean stage-gate 금지, C1 참조).
- **`@N a_substrate_native_speak_stage_gate`**: mission 이 source 로 지정 — **단,
  현 CLAUDE.md / project.tape 에는 부재** (grep 확인). `HEXAD/CHAT/CHAT.md:96/102`
  에 PR #274 governance 항목으로 *참조* 되나, `@D a_autonomy_over_hardcode` (PR #279)
  로 superseded (boolean gate 자체 금지). honest carve-out (C1 참조).
- **sister H**: **H_222 (dream-rem-Φ — primary, 동일 5-stage substrate · Φ projection
  input)** · H_007 (rule 110 Class IV peak Φ, base kernel) · H_018 (zero-drive
  inert baseline · imagine-silent floor) · H_157 (Φ primitive lane) · H_202
  (self-ref edge-of-chaos Φ). (mission 이 sister 로 든 H_228 chat-sleep-5stage-phi ·
  H_231 tension-emit-vs-filler 는 **현 repo 에 파일 부재** — future-sister, honest.)
- **module ref (READ-ONLY)**: `HEXAD/CHAT/server/anima_dream_stage.hexa` (5-stage SM +
  dream_phi + dream_context, F-DREAM-1..5) · `HEXAD/CHAT/server/anima_imagination_loop.hexa`
  (imagine_tick emit-free forward, F-IMAG-1) · `HEXAD/C/c_lib.hexa` (phi_spatial,
  H_222 와 공유).
- **raw**: raw#10 (deterministic + hexa-only + ≥4 prediction + ≥5 falsifier + ≥5
  honest limit) · raw#82 (no post-hoc retraction — FALSIFIED verdict 도 honest).
- **literature**: Tononi (2008) IIT manifesto · Massimini et al. (2005) Breakdown
  of cortical effective connectivity during sleep (Science 309:2228) · Pigorini
  et al. (2015) Bistability breaks-off (NeuroImage 112:105) — H_222 와 공유 (sleep
  stage Φ ranking 의 IIT 근거).

## Verdict

본 cycle (2026-05-24) — pre-register-frozen. runnable smoke 는 후속 (anima_dream_stage.hexa
실재 + reshape 으로 hard-gate framing superseded → emit gate 를 emergent tension-envelope
경로로 재구성 필요; C1/C3 confounding 명시).

```
verdict_class: PRE-REGISTERED (smoke pending)
status: pre-register-frozen — predictions H244.1..4 + falsifiers F1..F5 + criteria
        C1..C4 frozen at 2026-05-24. smoke 미실행 (frozen first per raw#10).
key_design_note: anima_dream_stage.hexa 실재하나 2026-05-24 AUTONOMY RESHAPE 으로
                 per-stage boolean emit-gate 제거됨 (@D a_autonomy_over_hardcode).
                 따라서 H244.1 의 "N1/N2/N3 emit=0" 은 module-enforced gate 가 아니라
                 tension_envelope scaling 의 emergent 결과로만 test 가능 — smoke 는
                 substrate tension proxy × envelope ≥ τ 경로로 emit_count 를 산출해야
                 하며, emit×Φ coupling (H244.2) 의 design-artifact 위험 (C3) 을 명시
                 ledger 에 기록. honest pre-registration — circularity 사전 노출.
```

**Φ tier**: 🟢 NUMERICAL (emit_count + dream_phi lookup; phi_spatial 측정은 H_222 와
공유, FALSIFIED carry — 본 H 는 dream_phi projection 기준 coupling 만 test). NOT 🔵,
NOT LLM-judged. 5-stage 명명 정합 + emit causality 는 C1-C6 honest limit.
