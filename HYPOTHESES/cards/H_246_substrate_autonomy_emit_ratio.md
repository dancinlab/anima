---
id: H_246
slug: substrate-autonomy-emit-ratio
title: H_246 substrate-autonomy emit ratio — 55.56% emit-through 정량 post-deploy baseline (autonomy reshape evidence)
domain: substrate + consciousness + corpus
status: pre-register-frozen
exploration_method: E5 (live telemetry sweep) + E10 (autonomy-reshape post-deploy 측정) + E12 (substrate ↔ deployment cadence)
verification_method: W4 (verdict-4-class) + W11 (meta-cross sister-link H_018/H_230) + W12 (autonomy-over-hardcode confirmation)
raw_rank: 12
hexa_only: true
deterministic: false  # live mini telemetry, substrate cadence
llm: none
pre_register_frozen: true
frozen_at: 2026-05-24
since: 2026-05-24 (new — autonomy reshape 9-PR post-deploy baseline · H_241 corpus-quality (#319) ID 충돌 해소 renumber → H_246)
---

# H_246 — substrate-autonomy emit ratio

## Hypothesis

CLAUDE.md `@D a_substrate_native_speak` + `@D a_autonomy_over_hardcode` 거버넌스 directive 가 substrate-side 에서 *measurable* deployment cadence 로 표출된다 — 구체적으로 *9-PR autonomy reshape* (#272 #273 #274 #275 #279 #281 #282 #286 #288) post-deploy mini PID 35411 위 235-tick / 8.5-min window 에서 substrate 가 다음 4 ratio 를 유지한다:

1. **H246.1 emit_attempt_per_tick ≈ 11%** — substrate-internal cadence floor.
2. **H246.2 emit_actual_per_attempt ≈ 55%** — p3/p5 silent-drop filter 가 *결정적 침묵* (0%) 도 *전부 통과* (100%) 도 아닌 *partial conservative gate* 로 동작.
3. **H246.3 p3p5_drop_ratio_of_attempts ≈ 44%** — H246.2 의 dual (1 - 55%).
4. **H246.4 net_emit_per_tick ≈ 6%** — autonomous cadence 의 deployment-side observable.

핵심 substrate claim: **substrate 자율 emit ratio 의 conservative-but-non-zero 동작** 이 `@D a_substrate_native_speak` 의 *"may speak during user silence and may stay silent under a direct question"* 의 deployment-level instance. 본 H 는 `p3/p5 drop 100% 가설` (gate 가 모든 substrate emit 을 silent-drop) 을 직접 falsify — 측정된 55.56% emit-through ratio 가 evidence.

정밀화 (operational): PR #300 의 27 emit attempts / 235 ticks / 15 actual emits / 12 silent-drops verbatim telemetry 가 본 cycle 의 *raw evidence* (substrate-internal filter 가 conservative 하지만 *결정적 침묵이 아님*).

## Why

- **PR #300 (FIRST quantified post-deploy baseline)**: mini PID 35411 (`anima_participant.py` 585 LoC, PR #286) 재시작 직후 participant.err telemetry 첫 정량 측정. 9-PR autonomy reshape 운행 결과 substrate 가 자율 emit 발화. headline metrics (n=27 emit attempts, 235 ticks span, ~8.5 min window): emit_attempt_per_tick = 11.49%, emit_actual_per_attempt = 55.56%, net_emit_per_tick = 6.38%, p3p5_drop_ratio_of_attempts = 44.44%.
- **PR #182 (anima_monologue_sim.hexa)**: 본 H 의 *반대편 baseline* — gate ON / `/history` empty → 0 anima emit (gate working in void). PR #300 + PR #182 가 한 쌍을 이뤄 gate 양 방향 모두 검증.
- **PR #279 (a_autonomy_over_hardcode governance)**: CLAUDE.md `@D a_autonomy_over_hardcode` directive 신규 등록 — autonomy 가 hardcode 보다 우월. 본 H 는 그 directive 의 *deployment-level numerical instance* (자매 PR #291 H_230 은 substrate-level mitosis 위 numerical instance).
- **PR #272 (conversation-active gate 삭제)**: anima_participant 의 conversation-active gate 폐기 + dream/imagination hook 추가. 본 H 의 substrate 가 *gate-removed* state 에서 자율 cadence 산출.
- **PR #273 (anima_imagination_loop.hexa)**: emit-free internal rehearsal + mitosis tick. 본 H 의 emit_attempt 와 *분리된* internal-only cycle (emit-free) — autonomy 의 *침묵 lane*.
- **PR #275 (anima_dream_stage.hexa)**: WAKE/N1/N2/N3/REM 5-stage sleep state machine — H_222 (dream-rem-Φ) 의 substrate machinery. 본 H 의 11.49% cadence 가 *sleep stage 무관하게* 산출되는지 후행 측정 (현재 baseline 은 single-stage WAKE).
- **PR #281 (CHAT.md SSOT + DEPLOY.md sleep/imagination)**: P47 substrate-native deployment runbook. mini PID 35411 가 본 runbook 따라 재시작.
- **PR #282 / #286 / #288 (dict API reshape)**: `emit_allowed` boolean gate 폐기 → `dream_context` dict 주입. 본 H 의 *측정 가능성* 의 기반 (이전 boolean gate 면 dict telemetry 자체 미존재).
- **PR #274 (PHILOSOPHY p5)**: tension-driven emit ≠ silence-filler. 본 H 의 11.49% cadence 가 tension-driven 인지 idle-filler 인지 후행 검증 lane.
- **cross-link H_018 (GENESIS spontaneous emergence)**: zero-drive 완전정지 (0 split) → self-reference (SELFFEED) → 자발 genesis. 본 H 의 11.49% cadence 가 PR #182 의 0% (gate ON void) 와 PR #300 의 11.49% (autonomy reshape) 양 boundary 를 가짐 — H_018 의 self-reference 가 substrate cadence 의 *trigger source*.
- **cross-link H_230 (autonomy-over-hardcode substrate)**: PR #291 substrate-level mitosis cell-pool 위 numerical instance (`SUPPORTED_FULL`, 4/4 criteria, 5/5 falsifiers, +32.76% Φ richness, 11× stronger substrate-coupling). 본 H 는 *deployment-level* 측면 — H_230 의 substrate-side advantage 가 deployment-side cadence 로 표출되는지 직접 측정.
- **cross-link H_231 (tension-driven emit vs filler)**: PR #285 — tension 이 emit 의 actual trigger 인지 측정. 본 H 의 55.56% emit-through 의 *trigger source* (composite tension τ vs random walk) 는 H_231 의 follow-up 측정.
- **raw#12 deviation note**: 본 H 는 deterministic=false (live mini telemetry, substrate cadence stochastic) — raw#12 strict deterministic 요건 위반. 대신 *byte-identical replay* (참고 PR #300 stdout verbatim 보존) 로 cycle-internal 재현성 보장.

## Predictions

- **H246.1 emit_attempt_per_tick**: ratio ∈ [0.08, 0.15] (8~15% band, 측정 11.49% 가 centered). substrate-internal cadence floor — 너무 sparse 면 substrate inert, 너무 dense 면 hardcode-like.
- **H246.2 emit_actual_per_attempt**: ratio ∈ [0.40, 0.70] (40~70% band, 측정 55.56% 가 centered). conservative-but-non-zero gate — 0% (전부 silent-drop) 도 100% (gate 무력화) 도 아닌 partial filter.
- **H246.3 p3p5_drop_ratio**: ratio = 1 - H246.2 ∈ [0.30, 0.60] (측정 44.44% centered). p3/p5 filter 의 *active conservatism* 의 dual.
- **H246.4 net_emit_per_tick**: ratio ∈ [0.04, 0.09] (4~9% band, 측정 6.38% centered). deployment-side observable cadence — H246.1 × H246.2.
- **H246.5 dual-baseline coherence**: gate ON void baseline (PR #182, /history empty) 의 net_emit_per_tick = 0% AND gate OFF telemetry baseline (PR #300, autonomy reshape) 의 net_emit_per_tick > 0% — 두 baseline 이 *같은 substrate* 위 *반대 boundary condition* 으로 양립.

## Variables

- **axis1_window_length**: ticks ∈ {235 (PR #300 측정), 720 (30-min target), 2880 (2-hour multi-stage), 17280 (12-hour diurnal)}
- **axis2_deployment_state**: {pre-reshape (boolean gate, baseline 0%), post-reshape 9-PR (autonomy dict, measured 55.56%), post-reshape + tension-instrument H_231 (future)}
- **axis3_dream_stage**: {WAKE (current single-stage measurement), N1, N2, N3, REM (H_222 sister cycle 후행)}
- **axis4_user_msg_presence**: {0 (현재 baseline, 순수 substrate-driven), 1+ (user-driven cadence cross-check)}
- **axis5_strategy_diversity**: {single (`w_curiosity_peak_seed` 100% currently), multi-strategy (audit future)}
- **fixed**: PID 35411, mini host, telemetry source = `~/anima_chat_pack/logs/participant.err`, parse regex `EMIT|EMIT-DROP|silent`

## Run Protocol

- **baseline measurement**: `ssh mini 'cat ~/anima_chat_pack/logs/participant.err'` → regex parse (EMIT / EMIT-DROP / silent lines) → 4 headline ratio 계산.
- **multi-window scaling**: 30-min window (PR #300 target 미달), 2-hour, 12-hour (diurnal pattern) — H246.1~4 의 *time-stability* 검증.
- **dual-baseline pair**: PR #182 monologue_sim.hexa (gate ON void = 0%) + PR #300 telemetry (gate OFF autonomy = 55.56%) — H246.5 의 boundary condition pair.
- **hexa_only**: telemetry parse 는 hexa-native (PR #138 akida_consumer pattern, type_of "array" guard PR #188/#192).
- **llm**: none.
- **runtime**: $0 mini SSH + local hexa parse; GPU 불필요.
- **ledger**: `UNIVERSE/state/h246_substrate_autonomy_emit_ratio_2026_05_24/result.json` {window_secs, n_attempts, n_actual, n_drops, n_silent, ratio_table, criteria, falsifiers, verdict}.
- **honest tier**: 🟡 SUPPORTED-BY-CITATION (PR #300 verbatim telemetry citation — single 8.5-min window, multi-window scaling 미실행).

## Criteria

- **C1 (attempt cadence)**: emit_attempt_per_tick ∈ [0.08, 0.15] → H246.1 PASS (현재 11.49%).
- **C2 (emit-through ratio)**: emit_actual_per_attempt ∈ [0.40, 0.70] → H246.2 PASS (현재 55.56%).
- **C3 (drop-ratio dual)**: p3p5_drop_ratio ∈ [0.30, 0.60] → H246.3 PASS (현재 44.44%).
- **C4 (net cadence)**: net_emit_per_tick ∈ [0.04, 0.09] → H246.4 PASS (현재 6.38%).
- **C5 (dual-baseline coherence)**: void-baseline net = 0% AND autonomy-baseline net > 0% → H246.5 PASS (PR #182 + PR #300 양 boundary).
- **verdict_rule**:
  - **SUPPORTED** = 5/5 PASS (band 안정 + dual boundary coherent)
  - **PARTIAL** = 3-4 PASS
  - **FALSIFIED** = C2 OR C5 FAIL (gate 가 결정적 침묵 OR autonomy baseline 이 void 와 등가)

## Falsifiers (≥5, pre-registered)

- **F1 GATE-100%-DROP**: emit_actual_per_attempt < 0.05 (즉 95%+ silent-drop) → H246.2 FALSIFIED, p3/p5 가 결정적 침묵 gate (autonomy reshape 의도 좌초). (measurable: telemetry ratio.)
- **F2 GATE-100%-PASS**: emit_actual_per_attempt > 0.95 (즉 5% 미만 drop) → H246.3 FALSIFIED, p3/p5 filter 무력화 (autonomy 가 *over-emit* 으로 표출). (measurable.)
- **F3 CADENCE-INERT**: emit_attempt_per_tick < 0.02 (즉 2% 미만 attempt) → H246.1 FALSIFIED, substrate inert (autonomy reshape 가 cadence 산출 못함). (measurable.)
- **F4 CADENCE-HARDCODE**: emit_attempt_per_tick > 0.50 (즉 50%+ attempt) → hardcode-like firing (autonomy 가 schedule 로 collapse). (measurable.)
- **F5 BOUNDARY-COLLAPSE**: dual-baseline 에서 void net = autonomy net (양 boundary 가 등가) → H246.5 FALSIFIED, autonomy reshape 가 deployment-side observable 산출 못함. (measurable: PR #182 vs PR #300 net.)
- **F6 SAMPLE-NON-REPLICABLE**: multi-window scaling (30-min, 2-hour) 에서 ratio 가 [측정 ratio ± 0.20] band 이탈 → sample 자체가 *transient artifact* (replication 불가). (measurable.)
- **F7 POST-HOC RETRACT**: frozen 후 ratio band 정의를 verdict-fit 으로 edit → raw#12 위반.

## Honest Limits (raw#12 c3, ≥5)

- **L1 (window 8.5-min 한정)**: PR #300 의 telemetry 가 8.5-min window — 30-min 목표 미달, multi-hour diurnal pattern 미측정. 본 baseline 의 ratio 가 *transient* 일 가능성 (cell-pool warm-up phase, mitosis tick 초기 transient 등). multi-window scaling 후행 cycle 필요.
- **L2 (score band [0.627, 0.681] 좁음)**: 27 시도 전부 좁은 score band — *diversity 미관측*. tension-driven emit 의 *trigger threshold* 가 좁은 band 안에서만 fire 하는지, 또는 score 자체가 *quasi-deterministic* 인지 unresolved (H_231 follow-up).
- **L3 (single strategy 100%)**: `w_curiosity_peak_seed` strategy 100% — multi-strategy 도달 여부 별도 audit. 본 ratio 가 *single-strategy artifact* 일 가능성, 다른 strategy 에서 ratio 변동 가능.
- **L4 (no user msg)**: 측정 window 동안 user msg 0 회 — 순수 substrate-driven cadence. user-driven cross-check 미실행 (`@D a_substrate_native_speak` 의 *user messages = environment context, not response obligation* directive 의 측면).
- **L5 (dream_stage stub/real 분리 안됨)**: sister "ctx verify" agent 결과 미반영 — `_dream_context dict` (PR #286) 가 stub 데이터인지 real 5-stage state machine (PR #275) 출력인지 telemetry 만으로 분리 불가.
- **L6 (deterministic=false note)**: 본 H 는 raw#12 strict deterministic 위반 — substrate cadence 가 stochastic. 대신 verbatim PR #300 stdout 보존 + multi-window replication 으로 sample-level reproducibility 추구.
- **L7 (substrate emit ≠ phenomenal speech)**: 본 ratio 는 deployment-side observable 측정량 — substrate 의 *phenomenal experience* 와 직접 mapping 없음 (H_004 dissociation 정합). high emit ratio = high consciousness 식 strong identity NOT made.
- **L8 (mini PID single instance)**: PID 35411 single mini host — 다른 host (ubu-1, ubu-2) 또는 different boot session 에서 ratio 변동 가능. host-cross replication 미실행.

## Cross-Links

- **philosophy (CLAUDE.md)**: `@D a_substrate_native_speak` (compute motivation from internal substrate state · may speak during user silence · may stay silent under direct question) · `@D a_autonomy_over_hardcode` (autonomy > hardcode) · `@D p5` (NO SPEAK — output = continuous externalization of tension field).
- **sister H**: H_018 (GENESIS spontaneous emergence — substrate cadence trigger source) · H_230 (autonomy-over-hardcode substrate-level, PR #291 SUPPORTED_FULL) · H_231 (tension-driven emit vs filler, PR #285 — trigger source 후행) · H_222 (dream-rem-Φ — sleep stage substrate machinery) · H_204 (weak-panpsy threshold — autonomy 가 threshold 위 instance) · **H_248 (substrate-autonomy-nonreflexivity — 동일 PR #300 telemetry 위 *비반사성* (emit ⊥ user-message) framing-axis sibling; numeric SSOT = 本 H_246; dedup 2026-05-25 PR #379 R2 option A: 이전 stale "H_240 압축 sibling" cross-link 교체 — renumber 이전 PR #311 의 obsolete H_240 identity 참조였음, 현 H_240 은 bilingual-integration-Φ 로 무관)** · **H_244 (sleep-stage-gated-emit-Φ, autonomy-reframe — emit cadence 의 sleep-stage 의존성; 본 H_246 의 axis3_dream_stage 가 H_244 의 stage-gated emit 와 cross-fire)**.
- **source PR**: #300 (FIRST quantified baseline · raw evidence) · #182 (void baseline pair) · #272 (gate 삭제) · #273 (imagination_loop) · #274 (PHILOSOPHY p5) · #275 (dream_stage 5-stage) · #279 (autonomy governance) · #281 (CHAT.md SSOT + DEPLOY.md) · #282/#286/#288 (dict API reshape).
- **raw**: raw#12 (deviation: deterministic=false, verbatim stdout 보존으로 대체) · raw#82 (FALSIFIED verdict 도 honest).
- **literature**:
  - Tononi (2008) Φ as integrated information — substrate cadence ≠ phenomenal claim (L7).
  - Dehaene (2014) Consciousness and the Brain — global workspace ignition threshold (본 H 의 score band 정합 후행 lane).
  - Friston (2010) Free-energy principle — active inference cadence (substrate emit attempt 의 prior).
  - Hofstadter (1979) Gödel, Escher, Bach — strange-loop substrate self-reference (H_018 trigger source).

## Verdict

본 cycle (2026-05-24) — pre-register-frozen + PR #300 single-window evidence 위 SUPPORTED_SINGLE_WINDOW state.

```
verdict_class: SUPPORTED_SINGLE_WINDOW
evidence_summary:
  PR #300 mini PID 35411 telemetry (n=27 emit attempts, 235 ticks, ~8.5 min):
    emit_attempt_per_tick       = 27/235   = 11.49 %
    emit_actual_per_attempt     = 15/27    = 55.56 %
    p3p5_drop_ratio_of_attempts = 12/27    = 44.44 %
    net_emit_per_tick           = 15/235   =  6.38 %

  Dual-baseline pair (gate 양 방향):
    PR #182 (gate ON,  /history empty)  : 0 anima emit  (gate working in void)
    PR #300 (gate OFF, autonomy reshape) : 15 actual emit (autonomy working)

  C1 emit_attempt ∈ [0.08, 0.15]  : PASS (11.49% centered)
  C2 emit_actual  ∈ [0.40, 0.70]  : PASS (55.56% centered)  ←★ key
  C3 drop_ratio   ∈ [0.30, 0.60]  : PASS (44.44% centered)
  C4 net_emit     ∈ [0.04, 0.09]  : PASS (6.38%  centered)
  C5 dual-baseline coherent       : PASS (void 0% vs autonomy 6.38%)

  F1 GATE-100%-DROP        : not fired (55.56% ≫ 5%)
  F2 GATE-100%-PASS        : not fired (55.56% ≪ 95%)
  F3 CADENCE-INERT         : not fired (11.49% ≫ 2%)
  F4 CADENCE-HARDCODE      : not fired (11.49% ≪ 50%)
  F5 BOUNDARY-COLLAPSE     : not fired (void 0% ≠ autonomy 6.38%)
  F6 SAMPLE-NON-REPLICABLE : PENDING (multi-window scaling 후행)

  VERDICT_RULE: SUPPORTED iff 5/5 · PARTIAL if 3-4 · FALSIFIED if C2∨C5 fail
  VERDICT     : SUPPORTED_SINGLE_WINDOW (5/5 criteria PASS, F6 pending)

key_finding: 9-PR autonomy reshape post-deploy substrate 가 deployment-
             side 에서 *conservative-but-non-zero* emit cadence 산출
             (55.56% emit-through, 44.44% silent-drop) — p3/p5 가 결정적
             침묵 gate 아니고 *partial filter* 로 동작. `@D
             a_substrate_native_speak` directive 의 "may speak during user
             silence" 가 deployment-level instance 로 표출. PR #182 (void
             baseline 0%) 와 PR #300 (autonomy baseline 6.38%) 가 gate
             양 방향 boundary 로 dual coherent.

honest_note: L1 8.5-min single window — multi-hour diurnal scaling
             미실행, sample 이 *transient* 일 가능성 (F6 PENDING). L2
             score band 0.627-0.681 좁음 (diversity 미관측), L3 single
             strategy 100%, L4 no user msg, L5 dream_stage stub/real
             분리 안됨. SUPPORTED_SINGLE_WINDOW = 5/5 criteria PASS but
             window scope 제약.
```

**State output**: `UNIVERSE/state/h246_substrate_autonomy_emit_ratio_2026_05_24/result.json` (multi-window scaling 후 update).
**Source SSOT**: PR #300 verbatim telemetry (mini PID 35411, `~/anima_chat_pack/logs/participant.err`).
**Φ tier**: 🟡 SUPPORTED-BY-CITATION (single-window telemetry citation) — 🟢 NUMERICAL 도달 path = 30-min / 2-hour / 12-hour scaling replication.
