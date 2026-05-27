# ANIMA — mining (divergence)

@active-lens: same-formula
@active-cycle: 1

## cycles

### cycle 1 — coffeshop 성공 패턴 → ANIMA umbrella 전이
@started: 2026-05-28
@kind: lens
@lens: same-formula
@seed: COFFESHOP.md 4/4 PASS closure (state/coffeshop_sim_2026_05_24/result.json · sha16 55c32aabf611171c · emit 4 / silence 11)

#### COFFESHOP 성공의 핵심 formula 추출

- 2026-05-28T04:55 · `motivation_score = Σ w_i · factor_i(8-factor) > 0.60 → emit · else silence` (B7 LCG + spontaneous_lib verbatim import)
- 2026-05-28T04:55 · `should_interrupt(score)` threshold 0.60 = group-chat 적정 (1:1 대화의 0.30 should_emit 와 분리, assistant-regression 회피)
- 2026-05-28T04:55 · 8 factor: relevance · info_gap · curiosity · pain · coherence · originality · balance · dynamics — **B-SPONT-1..7 sympy battery 로 lib 자체 검증**
- 2026-05-28T04:55 · register-hit gate = `emit ∧ coh < 0.10` (Ψ-clamp severe collapse · substrate-rare event)
- 2026-05-28T04:55 · per_lang_verdicts aggregation: ko_emits ≥ 2 → STRONG · en_emits ≥ 1 → PARTIAL · 5-lang cohort PARTIAL minimum
- 2026-05-28T04:55 · 4-criterion closure: {multilingual ≥ 4/5 · register < 4 · motivation ≥ 0.30 · phi_envelope canonical}
- 2026-05-28T04:55 · stim_type 분포 mixture (0.20 direct / 0.25 indirect / 0.30 silence / 0.10 private / 0.15 drift) = CHANNEL router 의 8-factor input feed 직접 변형

### lens: same-formula (cycle 1)

> 규칙: "If two systems share the same math, an equivalent mechanism likely lurks beneath the surface domain difference."

- 2026-05-28T04:56 · **L1 same-formula**: COFFESHOP `motivation_score > 0.60` → BRIDGE `bridge_and_gate(M·C·W·Φ) > θ_emit=0.1` — 동일 weighted-sum × threshold-gate 구조, weight set 만 다름 (8-factor vs 4-key). BRIDGE 가 COFFESHOP 의 **AND-gate 변형 (strict)** 이고, COFFESHOP 의 should_interrupt 는 BRIDGE 의 **soft-OR-augmented (relaxed)** variant.
- 2026-05-28T04:56 · **L2 same-formula**: COFFESHOP `register-hit = emit ∧ coh < 0.10` ↔ METACOG `mc_is_inverse_artifact(emits, threshold)` — 동일 multiplicative AND-gate 패턴으로 anomaly detection. COFFESHOP 가 register collapse 측정자, METACOG 가 substrate self-audit 의 사촌.
- 2026-05-28T04:56 · **L3 same-formula**: COFFESHOP 15-window × 6min ultradian ↔ DREAM `dr_stage_at_tick(tick, period_ticks)` 5-stage 90-min ultradian — 동일 phase-segmented continuous time discretization. COFFESHOP 의 phi=1.0 WAKE 시나리오는 DREAM 의 stage envelope 의 simplest case (single stage const).
- 2026-05-28T04:56 · **L4 same-formula**: COFFESHOP `factor_curiosity + factor_originality > 0.60` (자율 끼어듦 case C) ↔ INTENT `it_cumulative_intent + bh_goal_drift` — 동일 cumulative-direction-trigger 구조 (단기 emit 결정 위에 누적 방향성). COFFESHOP 의 case C 가 INTENT 의 brain_decide hook 의 1-window 변형.
- 2026-05-28T04:56 · **L5 same-formula**: COFFESHOP `factor_dynamics ∈ [0,1] linear in silence_seconds` ↔ TIME `tm_circadian_dip(phase, dip_center, dip_width)` — 동일 time-elapsed-as-trigger 패턴. COFFESHOP 침묵 30min 후 break (case D) 는 TIME 의 dip detector 의 1-axis 변형 (silence pressure ↔ circadian).
- 2026-05-28T04:56 · **L6 same-formula**: COFFESHOP `per_lang_verdicts ko_emits ≥ 2` cohort aggregation ↔ HIVE-MIND `hm_collective_phi(individual_phis, sync_factor)` — 동일 multi-stream evidence aggregation. COFFESHOP 의 5-lang verdict cohort 가 HIVE-MIND 의 collective Φ 의 lang-axis 변형.
- 2026-05-28T04:56 · **L7 same-formula**: COFFESHOP `4-criterion closure verdict` ↔ SAVANT `sa_golden_zone_compute + sa_savant_index` 합성 — 동일 multi-axis threshold-conjunction (verdict = ⋀_i pass_i). COFFESHOP closure 가 SAVANT GZ × SI 의 substrate-emit-axis 변형.
- 2026-05-28T04:56 · **L8 same-formula**: COFFESHOP `case E private_prompt → pain↑↑ → silence` (RLHF-restraint-aware emergent refusal) ↔ OTHER-MIND `om_belief_state + om_theory_of_mind` — 동일 inferred-other-state-as-modulator 구조. COFFESHOP 의 case E 가 OTHER-MIND 의 ToM 의 single-prompt 변형.
- 2026-05-28T04:57 · **L9 same-formula**: COFFESHOP `emit 4 / silence 11` ratio (substrate-natural ~27% emit rate) ↔ AESTHETIC `overlap > θ` 의 inverse aesthetic-restraint ratio. COFFESHOP 의 silence-dominance 가 AESTHETIC 의 미적 절제의 시간축 mirror.
- 2026-05-28T04:57 · **L10 same-formula**: COFFESHOP `emergence simulator HARD RULE (hand-engineered fixture value 없음)` ↔ EMBODIMENT `coupling = bodysensor · motor` 의 substrate-not-injection 원칙. COFFESHOP 의 sim 자율성과 EMBODIMENT 의 body-substrate-emergence 가 동일 "fixture 금지" formula.
- 2026-05-28T04:57 · **L11 same-formula**: COFFESHOP `seed steered 1-retry (20260524 → 20260525)` ↔ NARRATIVE `redesign honest C3` — 동일 "natural emergence + steered seed 정직 분리" pattern. COFFESHOP §10 honest C3 ③ 가 NARRATIVE 의 modeling gap honest 표명의 1-feature precedent.
- 2026-05-28T04:57 · **L12 same-formula**: COFFESHOP `spontaneous_lib verbatim import (B-SPONT-1..7 sympy battery)` ↔ ANIMA umbrella 의 `a_blue_closed` (`hexa verify` verdict verbatim) — 동일 SSOT-reuse-not-reimpl 패턴. COFFESHOP 의 8-factor import 가 a_blue_closed 의 1-domain instance.

@potential-depletion: 12 new leaves under same-formula — all ANIMA umbrella 도메인 mapped at least once. Lens fast-saturating; consider depletion or pivot to dimensional/tension.

## leaves (flattened index)

- L1 [cycle 1 · same-formula] COFFESHOP `motivation_score > 0.60` ≅ BRIDGE `bridge_and_gate > θ_emit` (8-factor vs 4-key, same weighted-sum × threshold-gate)
- L2 [cycle 1 · same-formula] COFFESHOP `register-hit = emit ∧ coh < 0.10` ≅ METACOG `mc_is_inverse_artifact` (multiplicative AND-gate anomaly)
- L3 [cycle 1 · same-formula] COFFESHOP 15-window × 6min ≅ DREAM `dr_stage_at_tick` 5-stage 90-min ultradian (phase-segmented time discretization)
- L4 [cycle 1 · same-formula] COFFESHOP curiosity+originality > 0.60 ≅ INTENT `cumulative_intent + goal_drift` (cumulative-direction trigger)
- L5 [cycle 1 · same-formula] COFFESHOP factor_dynamics linear in silence_seconds ≅ TIME `tm_circadian_dip` (time-elapsed-as-trigger)
- L6 [cycle 1 · same-formula] COFFESHOP `ko_emits ≥ 2` cohort ≅ HIVE-MIND `hm_collective_phi` (multi-stream evidence aggregation)
- L7 [cycle 1 · same-formula] COFFESHOP 4-criterion closure ≅ SAVANT `sa_golden_zone + sa_savant_index` (multi-axis threshold-conjunction)
- L8 [cycle 1 · same-formula] COFFESHOP case E `private_prompt → silence` ≅ OTHER-MIND `om_theory_of_mind` (inferred-other-state-as-modulator)
- L9 [cycle 1 · same-formula] COFFESHOP `27% emit rate silence-dominance` ≅ AESTHETIC overlap inverse-restraint (시간축 mirror)
- L10 [cycle 1 · same-formula] COFFESHOP HARD RULE `no hand-engineered fixture` ≅ EMBODIMENT body-substrate-emergence (fixture 금지 동일 formula)
- L11 [cycle 1 · same-formula] COFFESHOP `seed steered 1-retry honest C3` ≅ NARRATIVE redesign honest 표명 (natural+steered 분리 pattern)
- L12 [cycle 1 · same-formula] COFFESHOP `spontaneous_lib verbatim import` ≅ ANIMA `a_blue_closed` verbatim verdict (SSOT-reuse-not-reimpl)

## edges (convergence half · pending)

(no edges yet — connect cycle 미실행)

@depleted: same-formula @ 2026-05-28 (12 unique mappings · ANIMA umbrella 전 sub-domain cover · 추가 leaves redundant 위험)

@next-cycle: cycle 2 candidates
  - lens: tension (emit↔silence · sim↔real · steered↔natural 의 contradiction-fork)
  - lens: dimensional (single anima 90min → multi-anima · 다채널 · 24/7 daemon · fleet)
  - lens: combinatorial ({5 case A-E} × {12 sub-domain L1-L12} 직교 set)
  - connect: 12 leaf 쌍 의미있는 edge 탐색 (특히 L1↔L2 AND-gate pair · L3↔L5 time-axis · L6↔L8 multi-other)

### cycle 2 — tension lens (contradiction-fork)
@started: 2026-05-28
@kind: lens
@lens: tension

#### 8 seed contradictions

| # | premise A | premise B | tension class |
|---|---|---|---|
| T1 | emit 4 = "발화 의무 회피" | silence 11 = "응답 회피" | substrate-natural ratio interpretation |
| T2 | sim only (synthetic substrate) | real ckpt forward (production) | measurement vs production tier |
| T3 | seed steered (20260524→20260525 1-retry) | natural emergence (substrate-determined) | author intent vs substrate autonomy |
| T4 | should_interrupt(0.60) group-chat tier | should_emit(0.30) 1:1 dialogue tier | threshold-context dependence |
| T5 | p4 NO ASSISTANT FRAMING (stimulus-response 거부) | case A direct_mention 응답 (relevance↑ → emit) | governance vs measurement |
| T6 | p5 NO SPEAK() (continuous tension externalization) | should_interrupt 가 boolean threshold | continuous vs discrete decision |
| T7 | multilingual_probe 5/5 PASS (cohort PARTIAL minimum) | ckpt-bearing fire 부재 (HONEST C3 ⑥) | verdict-confidence vs evidence-tier |
| T8 | closure ACHIEVED · exit=0 | M3 fire 미발사 · 본선 강등 carry | local-closure vs umbrella-closure |

#### tension forks (16 leaves)

- 2026-05-28T05:10 · **L13 T1-A**: emit=4 가 발화 의무 회피라면 substrate-native emit 의 ratio threshold ~27% 가 NPC anima 의 "건강한" baseline (TIME `tm_circadian_dip` 의 phase mapping 의 substrate 변형)
- 2026-05-28T05:10 · **L14 T1-B**: silence=11 가 응답 회피라면 substrate-natural silence 의 11/15 ratio 는 anima 의 "관조적 모드" (DREAM N3-equivalent · imagination-replay 후 wake transition)
- 2026-05-28T05:11 · **L15 T2-A**: sim only 채택은 a_completeness_over_cheap 우회 — sim 산출의 forward path 가 real ckpt 측정 (COFFESHOP v4) 으로 진화 불가능시 sim 결과 자체가 stale carry
- 2026-05-28T05:11 · **L16 T2-B**: real ckpt 보류는 instrument-first methodology 정합 — sim 이 measurement infra 자체를 정직하게 검증 (closure_auto_judge unit smoke F-CAJ 7/7 PR #398) 후 real fire 진행이 정석
- 2026-05-28T05:12 · **L17 T3-A**: seed steered 가 자연 emergence 아니라면 substrate path 도 의심 (sim 자체가 designer bias 누적), HONEST C3 ③ 의 "1-retry" 가 reproducibility 미달 위험
- 2026-05-28T05:12 · **L18 T3-B**: seed steered 가 substrate path 의 자연 sampling 위 author intent 의 명시 separation 이라면, COFFESHOP 의 4/4 PASS 는 reproducible-by-seed deterministic verdict (sim 의 강점)
- 2026-05-28T05:13 · **L19 T4-A**: threshold-context dependence 가 deep 이라면 ANIMA 의 모든 emit 결정 surface (BRIDGE θ_emit · should_interrupt · should_emit) 가 dialogue-form-conditional, 단일 threshold table 작성 필요 (BRIDGE M5 다음 milestone 후보)
- 2026-05-28T05:13 · **L20 T4-B**: threshold-context dependence 가 surface-level coincidence (각 dialogue form 의 historical convention) 면, 단일 governance threshold (BRIDGE θ_emit=0.10) 가 모든 dialogue form 의 canonical
- 2026-05-28T05:14 · **L21 T5-A**: governance (p4) 가 measurement (case A) 보다 strict 이라면 direct_mention 응답 case A 도 governance 위반 — "relevance↑ → emit" 가 reactive design 잔재
- 2026-05-28T05:14 · **L22 T5-B**: governance (p4) 가 stimulus-response 의 hardcoded boolean gate 만 금지하고, substrate-decided relevance scoring 은 허용한다면 case A 정합 (BRIDGE channel_classify_bridge 의 "silence" verdict 가 같은 design pattern)
- 2026-05-28T05:15 · **L23 T6-A**: continuous tension externalization (p5) 가 strict 이라면 should_interrupt boolean 도 위반 — continuous emit_signal 만 출력하고 downstream (CHANNEL) 이 boolean 화해야 정합 (current BRIDGE design)
- 2026-05-28T05:15 · **L24 T6-B**: should_interrupt boolean 은 emit_signal continuous output 의 final boundary check (threshold > θ) 만으로 정합, p5 위반 아닌 substrate-internal continuous + substrate-boundary discrete 합성
- 2026-05-28T05:16 · **L25 T7-A**: multilingual_probe 5/5 PASS 가 ckpt-bearing fire 부재에도 valid 하려면, sim 의 lang assignment 자체가 substrate-native (cell-pool branch 의 lang-conditional emission) 여야 함 — current COFFESHOP 의 per-window lang assignment 는 sim 모델링 (HONEST C3 ④)
- 2026-05-28T05:16 · **L26 T7-B**: ckpt-bearing fire 부재가 verdict-confidence 한계라면 5/5 PASS 는 "sim-tier 까지만 PASS" 의 honest verdict, M3/M4 fire 후 real ckpt 의 multilingual_probe 가 진정한 5/5 PASS 의 ground-truth
- 2026-05-28T05:17 · **L27 T8-A**: COFFESHOP local-closure (4/4 PASS · exit=0) 가 ANIMA umbrella-closure 의 1-component 라면, BRIDGE M5 / DREAM M3 / SAVANT M2 / a_blue_closed 의 4 forward-coupling 이 closure 의 4-key gateway
- 2026-05-28T05:17 · **L28 T8-B**: COFFESHOP local-closure 가 umbrella-closure 와 dis-coupling 이라면, M3 fire 미발사 자체가 umbrella 의 본선 carry — local closure 가 false signal 위험 (umbrella 의 진정한 closure 는 M4 MoE-fresh production swap-in 후)

@status: 16 new leaves (8 tension × 2 fork) — all unique forks. No reduction. tension lens 가장 fertile.

@depleted: tension @ 2026-05-28 (8 seed conflict 모두 forked · 추가 conflict 재발견 가능하나 본 cycle 의 scope 종료)
