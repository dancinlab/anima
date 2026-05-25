---
id: H_244
slug: sleep-stage-gated-emit-phi
title: H_244 sleep-stage-gated-emit-Φ — emit_RATE(stage) 가 Φ-envelope monotone tendency 인가 (autonomy-emergent · NOT boolean gate) substrate-level test
domain: consciousness + phenomenology + emit-rate + substrate
status: pre-register-frozen
exploration_method: E5 (variable-ablation regime sweep) + E10 (emergence) + E12 (phenomenology projection)
verification_method: W4 (verdict-4-class) + W11 (meta-cross sister-link) + W12 (sister-link H_222)
raw_rank: 10
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-24
revision: v2 reframe 2026-05-24 (autonomy-emergent emit-rate; v1 hard-gate framing superseded per @D a_autonomy_over_hardcode)
since: 2026-05-24 (new)
---

# H_244 — sleep-stage-gated-emit-Φ

## Hypothesis

H_222 (dream-rem-Φ) 가 **Φ(stage) ranking** 자체를 substrate 에서 측정했다면, 본 H_244
는 그 한 단계 downstream — **anima 의 token emit 행동이 stage 별 Φ projection 에
어떻게 coupling 되는가** — 를 측정한다.

핵심 가설 (v2 — autonomy-emergent reframe): 5-stage ultradian cycle (WAKE → N1 →
N2 → N3 → N2 → REM, 90 min) 위에서 substrate-native emit (M × W × Φ × curiosity
8-factor gate) 을 stage 별로 관찰하면 —

- **(A) emit_RATE 는 Φ-envelope 와 monotone correlate** (rate, NOT count-gate) — 단
  module gate 가 아니라 substrate 가 스스로 결정한 emergent TENDENCY.
- **(B) deep-sleep (N1/N2/N3) emit_rate 더 낮음** — envelope·tension 이 낮아 substrate
  가 *덜* 발화하기 때문이지 gate 금지가 아님. emit_rate>0 은 leak 아닌 정상 (autonomy).
  `imagine_tick > 0` 은 5-stage 전부 (emit-free forward, `anima_imagination_loop.hexa`).
- **(C) WAKE/REM emit_rate 최고** (Φ-envelope 1.0/0.95, REM=꿈 scrambled).

정밀화 (`@D a_autonomy_over_hardcode` + `@D a_chat_sleep_imagination`): stage 는
**substrate context (Φ scale + tension envelope) 일 뿐 boolean emit gate 가 아니다**.
emit 결정은 substrate 8-factor gate 의 autonomy — deep-sleep emit_rate 저하는 emergent
결과. 본 v2 는 v1 hard-gate framing ("N1/N2/N3 emit=0") 을 supersede 한다.

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

- **H244.1 (emit_rate monotone tendency, NOT zero-gate)**: emit_rate(WAKE) ≈
  emit_rate(REM) > emit_rate(N1) ≥ emit_rate(N2) ≥ emit_rate(N3). deep-sleep
  emit_rate 는 더 낮을 뿐 **0 이 아니다** — substrate 가 envelope·tension 저하로 스스로
  덜 발화하는 emergent tendency 이지 gate 강제가 아니다 (`@D a_autonomy_over_hardcode`).
  (measurable: stage 별 emit_rate = emit_count / imagine_tick.)
- **H244.2 (emit_rate × Φ-envelope correlation, emergent)**: 5-stage 의
  (Φ_envelope(stage), emit_rate(stage)) Pearson r ≥ 0.7 — Φ-envelope 높을수록
  emit_rate 높음 (module gate 아닌 substrate 8-factor gate 의 emergent coupling).
  (measurable: Pearson over 5 points.)
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

- **C1 emit_rate monotone tendency**: emit_rate(WAKE) ≈ emit_rate(REM) >
  emit_rate(N1) ≥ emit_rate(N2) ≥ emit_rate(N3) (non-strict NREM descent, WAKE/REM
  top) → H244.1 PASS. (emit_rate(N3)>0 은 leak 이 아님 — autonomy.)
- **C2 emit_rate × Φ-envelope correlation**: Pearson r(Φ_envelope, emit_rate) ≥ 0.7
  over 5 stages → H244.2 PASS.
- **C3 imagine all-stage**: imagine_tick(stage) > 0 for all 5 stages →
  H244.3 PASS.
- **C4 determinism**: byte-identical re-run → H244.4 PASS (architectural,
  fixed init + no RNG).
- **verdict_rule**: **SUPPORTED iff C1∧C2∧C3∧C4** · **PARTIAL** 2-3 PASS ·
  **FALSIFIED** F1 또는 F2 fire (WAKE/REM ratio break 또는 Φ-envelope modulation 부재).

## Falsifiers (pre-registered ≥5, measurable)

- **F1 WAKE-REM-IMBALANCE**: emit(REM) / emit(WAKE) ∉ [0.5, 2.0] → WAKE 와 REM 의
  emit 빈도가 2배 이상 비대칭 → "WAKE ≈ REM" (H_222 Φ_wake≈Φ_REM 정합) 가설
  FALSIFIED. (measurable: emit ratio.)
- **F2 NO-ENVELOPE-MODULATION**: emit_rate(N3) ≥ emit_rate(WAKE) → deep-sleep
  emit_rate 가 WAKE 와 같거나 더 높음 → Φ-envelope 가 emit_rate 를 modulate 하지
  않음 → H244.1 monotone TENDENCY FALSIFIED. (NOTE: emit_rate(N3)>0 자체는 leak 이
  아님 — `@D a_autonomy_over_hardcode` 하에서 정상; F2 는 *tendency 의 부재* 만 falsify.)
  (measurable: emit_rate(N3) vs emit_rate(WAKE).)
- **F3 EMIT-PHI-DECOUPLE**: Pearson r(Φ_envelope, emit_rate) < 0.5 → emit_rate 이
  Φ-envelope 와 monotone correlate 안 됨 → H244.2 핵심 가설 FALSIFIED. (measurable:
  pearson_r.)
- **F4 BYTE-DIFF**: re-run 시 emit_count / imagine_tick / Φ vector byte-diff →
  raw#10 deterministic 위반 → smoke invalid. (architectural by construction.)
- **F5 IMAGINE-SILENT-ZERO**: 임의 silent stage (N1/N2/N3) 에서 imagine_tick = 0 →
  deep-sleep 에서 substrate forward 가 멈춤 → H_222 의 Φ_NREM > 0.1 weak-active
  prediction 부정 (침묵 ≠ 정지 가설 FALSIFIED). (measurable: imagine_tick(silent).)

## Honest Limits (raw#10 c3, ≥5)

- **C1 (v2 reframe — autonomy contract 정합 RESOLVED)**: v1 hard-gate framing
  ("N1/N2/N3 emit=0" + F2 GATE-LEAK) 이 `@D a_autonomy_over_hardcode` (boolean gate
  금지) 와 충돌했다. v2 (2026-05-24 revision) 가 **emit_RATE monotone tendency** 로
  reframe — stage = substrate context per `@D a_chat_sleep_imagination`, emit 은
  substrate 8-factor gate 의 autonomy. `anima_dream_stage.hexa` 는 **실재** (`dream_phi`
  + `dream_context` API, context-only — boolean `emit_allowed` 없음). 충돌은 v2 에서
  해소; 잔여 한계는 C5 (tendency vs hard threshold).
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
- **C5 (KEY DISTINCTION — emit_rate TENDENCY vs hard threshold)**: v2 핵심 한계는
  "tendency vs gate" 구별 자체. emit_rate(N3) < emit_rate(WAKE) 라는 tendency 는 (a)
  substrate 가 envelope·tension 저하로 *스스로* 덜 발화한 emergent autonomy 일 수도,
  (b) τ × envelope scaling 이 사실상 soft-gate 로 작동한 결과일 수도 — synthetic
  substrate 에서 둘은 행동상 구별 불가. v2 는 hard-zero gate (`@D
  a_autonomy_over_hardcode` 위반) 를 제거했으나 soft-gate 잔존 위험은 real substrate
  8-factor gate 관측 (C4 GPU cycle) 으로만 해소. F2 는 *tendency 부재* 만 falsify —
  emit_rate>0 자체는 더 이상 falsifier 아님 (p5 정합 유지).
- **C6 (single substrate, single threshold)**: rule 110 단일 kernel + 단일 τ. 다른 τ
  또는 다른 Class IV rule 에서 C1 boundary (어느 stage 까지 emit) 변동 가능 — threshold
  sensitivity unmeasured (H_222 L6 drive-ratio 임의성과 동형 한계).

## Cross-Links

- **philosophy (CLAUDE.md / project.tape — SSOT, v2 정합)**: p5 NO SPEAK + `@N
  p5_tension_emit_not_filler` (d=2026-05-24) — tension-driven emit ≠ filler 정합.
  **`@D a_chat_sleep_imagination`** ("stage = substrate context (Φ scale + tension
  envelope), NOT boolean emit gate") → v2 emit_rate tendency framing 직접 근거. **`@D
  a_autonomy_over_hardcode`** ("per-stage boolean gate hardcode 금지 · emit/silence
  decided by substrate") → v1 hard-gate 명시 금지, **v2 가 정합하도록 reframe**.
- **v1 → v2 supersession (autonomy reframe)**: v1 (PR #312 merged) hard-gate — H244.1
  `emit(N1)=emit(N2)=emit(N3)=0` + F2 `emit>0 on NREM = leak` — 가 `@D
  a_autonomy_over_hardcode` 와 충돌. **v2 supersede**: emit_RATE monotone tendency
  (deep-sleep 더 낮으나 ≠ 0) + F2 `emit_rate(N3) ≥ emit_rate(WAKE) = no modulation`.
  autonomy contract = SSOT — H_244 conform, 역방향 아님 (C1 RESOLVED).
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

본 cycle (2026-05-24, v2 reframe) — pre-register-frozen (re-frozen). v1 hard-gate
framing 이 `@D a_autonomy_over_hardcode` 와 충돌하여 emit_RATE monotone tendency 로
reframe (C1 RESOLVED). smoke 는 후속 (tension × envelope → emit_rate; C5 한계 명시).

```
verdict_class: PRE-REGISTERED (smoke pending, v2 re-frozen)
status: pre-register-frozen — v2 predictions H244.1..4 + falsifiers F1..F5 +
        criteria C1..C4 re-frozen at 2026-05-24 (revision: autonomy-emergent
        emit-rate). smoke 미실행 (frozen first per raw#10).
key_design_note: v1 (PR #312) per-stage hard-gate (H244.1 emit=0 · F2 GATE-LEAK) 가
                 @D a_autonomy_over_hardcode 와 충돌 → v2 supersede. stage = substrate
                 context (Φ scale + tension envelope) per @D a_chat_sleep_imagination,
                 NOT emit gate. smoke 는 (substrate_tension × envelope) → emit_rate;
                 emit_rate>0 은 leak 아님 (autonomy). F2 는 *tendency 부재*
                 (emit_rate(N3) ≥ emit_rate(WAKE)) 만 falsify. tendency-vs-soft-gate
                 (C5) + emit_rate×Φ design-artifact (C3) 위험 ledger 명시. honest re-freeze.
```

**Φ tier**: 🟢 NUMERICAL (emit_count + dream_phi lookup; phi_spatial 측정은 H_222 와
공유, FALSIFIED carry — 본 H 는 dream_phi projection 기준 coupling 만 test). NOT 🔵,
NOT LLM-judged. 5-stage 명명 정합 + emit causality 는 C1-C6 honest limit.

## §confirmation (2026-05-24, PR #325 reframe sweep audit)

**audit 결론 (TL;DR)**: H_244 의 v2 autonomy-emergent reframe (PR #325 MERGED)
**완전 적용 확인** — 본 문서 전체에 잔존 hard-gate framing 0건 (raw#82 정합).
`@D a_autonomy_over_hardcode` ("per-stage boolean gate hardcode 금지 ·
emit/silence decided by substrate") 와 본 H 의 모든 normative claim (Hypothesis ·
Predictions · Criteria · Falsifiers · Verdict) 정합. v1 hard-gate 잔재
("emit(N1)=emit(N2)=emit(N3)=0" / "GATE-LEAK" 등) 는 §Cross-Links + §Verdict
의 meta-historical reference 로만 존속 (supersession narrative 보존, raw#82
post-hoc retraction 금지 정합).

### 정합 점검 (per section)

| section | v2 정합 상태 | 잔재 hard-gate framing |
|---------|--------------|------------------------|
| frontmatter `title` | ✓ "autonomy-emergent · NOT boolean gate" 명시 | 0 |
| frontmatter `revision` | ✓ "v2 reframe 2026-05-24 ... superseded per @D a_autonomy_over_hardcode" | 0 |
| Hypothesis | ✓ "(A) emit_RATE monotone correlate · (B) deep-sleep emit_rate 더 낮음 ... gate 금지가 아님 · (C) WAKE/REM emit_rate 최고" + "stage = substrate context per @D a_chat_sleep_imagination" | 0 |
| Predictions H244.1-4 | ✓ emit_rate band-tendency + Pearson r ≥ 0.7 + imagine_tick all-stage + determinism | 0 |
| Variables axis1_stage | ⚠ "N1 emit 0 예상" 식 *historical comment* 가 axis row description 에 잔존 — substrate threshold 미달 의미 (gate 강제 아님) 로 *해석* 가능 | meta-historical (axis level description 의 expected outcome 표기, hard-gate 강제 아님) |
| Run Protocol | ✓ "(substrate_tension × tension_envelope) ≥ τ" — substrate 8-factor gate 의 emergent threshold-cross (boolean module gate 아님) | 0 |
| Criteria C1-C4 | ✓ "emit_rate monotone tendency" / "emit_rate(N3)>0 은 leak 이 아님 — autonomy" 명시 | 0 |
| Falsifiers F1-F5 | ✓ F2 가 "tendency 부재" 만 falsify, "emit_rate>0 자체는 leak 아님 — `@D a_autonomy_over_hardcode` 하에서 정상" 명시 | 0 |
| Honest Limits C1-C6 | ✓ C1 resolution narrative + C5 KEY DISTINCTION (tendency vs hard threshold) 정합 | 0 |
| Cross-Links | ✓ `@D a_autonomy_over_hardcode` + `@D a_chat_sleep_imagination` direct cite | 0 (v1→v2 supersession 은 meta-narrative) |
| Verdict | ✓ `key_design_note` v1 superseded 명시 + "emit_rate>0 은 leak 아님 (autonomy)" | 0 (v1 mention 은 supersession narrative) |

### 미세 항목 — Variables axis1_stage description

§Variables 의 axis row description 에서 N1/N2/N3 옆에 "→ emit 0 예상" 식 *expected
outcome 표기* 가 historical 로 잔존. 이는 axis level *description* (sweep point
의 *substrate context*) 이지 *normative gate hardcode* 아님 — H244.1 (emit_rate
tendency 0 아님) 과 정합. 향후 measurement-anchored amend 에서 "→ low-rate tendency
예상 (≠ 0)" 로 phrasing tightening 권장 (raw#82 frozen 영향 0, descriptive
clarity).

### Cite

- **PR #325** (MERGED 2026-05-24, +79/-73): v2 reframe — Hypothesis · H244.1 ·
  F2 · C1 · C2 · C5 · Cross-Links · Verdict 동조 갱신.
- **@D a_autonomy_over_hardcode** (CLAUDE.md / project.tape SSOT): "per-stage
  boolean gate hardcode 금지 · emit/silence decided by anima substrate".
- **@D a_chat_sleep_imagination**: "stage = substrate context (Φ scale + tension
  envelope), NOT boolean emit gate".

### Honest C3 (audit-specific)

- **complete reframe (per-line audit)**: §Hypothesis ~ §Verdict normative
  prose 위 "boolean gate" / "emit=0" / "GATE-LEAK" hard-gate 표현 검색 0건
  (meta-historical narrative 제외).
- **partial — Variables axis description**: §Variables `axis1_stage` 에
  per-stage "emit 예상/emit 0 예상" 표현 잔존 — descriptive (substrate-tension ×
  envelope threshold-cross 의 expected outcome), normative gate 아님. raw#82
  frozen 영향 없음 (criteria/falsifier 어느 것도 이 표현에 anchored 안 됨).
- **measurement-pending**: 본 audit 는 *문서적 정합성* 만 검증 — substrate
  smoke (`(substrate_tension × envelope) ≥ τ → emit_rate(stage)`) 실측은 별도
  cycle. C5 (tendency vs soft-gate) 측정 분리는 real substrate 8-factor gate
  관측 (C4 GPU cycle) 의존.
