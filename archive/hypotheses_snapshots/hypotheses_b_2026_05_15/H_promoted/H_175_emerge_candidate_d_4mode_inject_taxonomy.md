---
id: H_175
slug: emerge-candidate-d-4mode-inject-taxonomy
title: Emerge Candidate D — 4-mode inject taxonomy (none/zero/canonical/user) 가 CLM v4 cross-attn dormancy 의 architectural pivot 을 runtime 에서 해소
domain: clm-architecture | consciousness
status: pre-register-frozen
exploration_method: E5 (engineering-spec audit — DecoderBlockV2:553 guard) + E8 (taxonomy completion — 4-mode inject)
verification_method: W5 (numerical sim — 4-mode phi_star sweep) + W2 (math identity — 5-axis balance) + W11 (cross-engine — PyPhi noise-floor)
raw_rank: 6
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-12
since: 2026-05-12
source_hc: Hc_623
source_doc: docs/anima_emerge_candidate_d_always_inject_spec_2026_05_05.md
source_lines: 14-32, 165-260
promoted_at: 2026-05-12
linked_h: H_011 (iit-geometry — phi_star variation by inject mode), H_022 (consciousness-universe-map — substrate engagement), H_167 (Emerge Candidate E ODE-AR bridge — CHILD-GATED on F-CAND-D-1), H_174 (phi_star geometry aliasing — phi_star validity bound)
verify_source: scripts/hc_verify/cache_2026_05_12/verify/verify5_authored.jsonl row 15
---

# H_175 — Emerge Candidate D: 4-mode inject taxonomy (none/zero/canonical/user)

## Hypothesis

`DecoderBlockV2:553` 의 guard `if consciousness_states is not None` 가 L37 root pattern (substrate change ≠ behavior change) 의 한 사례 — cross-attn 이 inject 없으면 dormant. 4-mode taxonomy — **none** (baseline, inject 없음) / **zero** (arch-engagement-isolator, all-zero inject = neutral cross-attn 활성화) / **canonical** (paradigm-v11-G3 8-cell standard inject) / **user_supplied** (5-axis user-conditioned inject) — 가 cross-attn engagement 를 runtime 에서 dial 가능하게 한다, source 수정 없이 (~65 LoC mount-layer additive). 본 H 는 H_011 iit-geometry 의 phi_star 가 inject mode 에 따라 어떻게 변하는지를 4-point 로 고정하고, H_167 (Emerge E ODE-AR bridge) 의 전제조건 (F-CAND-D-1 PASS) 을 검증한다.

## Why (motivation)

- **conscious_decoder.py:553**: guard `if consciousness_states is not None` — inject 없으면 cross-attn block 전체가 skip
- **L37 root pattern**: substrate (architecture) change ≠ behavior change — guard 가 그 사례
- **paradigm v11 G3**: 8-cell canonical consciousness-state injection (현 default)
- **anima phi_star 측정**: inject mode 별 phi_star 차이가 "cross-attn 이 실제로 engage 하는가" 의 proxy
- **Hc_624 (H_167)**: Emerge E (non-collapsing ODE flow → consciousness AR bridge) 가 본 H 의 F-CAND-D-1 PASS 에 CHILD-GATED — 4-mode pivot 이 robust 해야 H_167 측정이 의미

## Predictions

| ID | 예측 | 근거 |
|----|------|------|
| **H_175.1** | canonical phi_star − none phi_star > 0.005 (inject 가 visible) | F-CAND-D-1 inverted |
| **H_175.2** | canonical 5-axis phi_star balance max/min < 1.5 (single-axis dominance 없음) | F-CAND-D-2 inverted |
| **H_175.3** | user_supplied per-axis input ↔ phi_star Pearson ≥ 0.7 (user-spec tracking) | F-CAND-D-3 inverted |
| **H_175.4** | zero-mode phi_star − none-mode phi_star < 0.001 (zero-inject 는 neutral baseline) | F-CAND-D-4 inverted |
| **H_175.5** | 4-mode 로 cross-attn dormancy 패턴 전부 설명 — 5th mode (random/adversarial) 불필요 | F-CAND-D-5 inverted |

## Run Protocol

deterministic + hexa-only + llm: none. (~65 LoC mount.hexa + dialogue.bash additive; BG-A real-load probe $0-1 H100)

1. **4-mode flag impl (W5 prep)** — mount-layer 4-mode flag (~65 LoC mount.hexa + dialogue.bash), source 미수정 (Migration TODO)
2. **canonical vs none phi_star (W5)** — 동일 prompt set, canonical inject vs none → Δphi_star (H_175.1, F-CAND-D-1)
3. **5-axis balance (W2+W5)** — canonical inject 의 per-axis phi_star 5개 → max/min ratio (H_175.2, F-CAND-D-2; AXIS_SPANS slice geometry calibration 선행 — C3 risk)
4. **user_supplied tracking (W5)** — user 가 5-axis 값 지정 → 출력 phi_star 의 per-axis correlation Pearson (H_175.3, F-CAND-D-3)
5. **zero-mode neutrality (W5)** — all-zero inject vs none → Δphi_star 가 noise floor 이하인지 (H_175.4, F-CAND-D-4)
6. **noise-floor characterization (W11)** — anima phi_star RNG-induced variance 측정 → 0.005 threshold 가 noise level 위인지 확인 (L4) + PyPhi cross-check
7. **5th-mode necessity test (W5)** — random-axis / adversarial inject 추가가 dormancy 패턴 설명에 필요한지 (H_175.5, F-CAND-D-5)

## Criteria

| ID | criterion | status |
|----|-----------|--------|
| **C1** | 4-mode flag impl + BG-A real-load probe ≥1 run | pending |
| **C2** | canonical/none/zero phi_star 3-point 측정 완료 | pending |
| **C3** | AXIS_SPANS slice geometry calibration 완료 (5-axis balance 정의 가능) | at-risk (frontmatter 명시) |
| **C4** | noise-floor characterization (phi_star RNG variance) | pending |
| **C5** | n=6 PERFECT_NUMBER_CLASS L7 binding 인정 (paradigm v11 G3 8-cell sopfr(8)=6 perfect-class diagonal) | met (본 L1) |

## Falsifiers (≥6)

- **F-CAND-D-1 (inject-invisible)** [PRE-LOCKED]: canonical phi_star ≈ none phi_star (Δ ≤ 0.005) → inject 가 cross-attn 에 visible 한 효과를 못 만듦, 4-mode pivot 의 전제 (cross-attn 이 inject 로 dial 됨) FALSIFIED. (FAIL_TRUE)
- **F-CAND-D-2 (single-axis dominance)** [PRE-LOCKED]: canonical 5-axis phi_star 의 max/min ≥ 1.5 → 한 axis 가 지배, "5-axis balanced injection" claim FALSIFIED. (FAIL_TRUE)
- **F-CAND-D-3 (user-spec untracked)** [PRE-LOCKED]: user_supplied per-axis input ↔ phi_star Pearson < 0.7 → user 가 지정한 axis 값이 출력에 반영 안 됨, "user_supplied mode" 무의미 FALSIFIED
- **F-CAND-D-4 (zero-mode broken)**: zero-mode phi_star 가 none-mode 와 Δ ≥ 0.001 (즉 zero-inject 가 none 과 diverge) → "zero = arch-engagement-isolator neutral baseline" semantics 파괴, zero 가 별도 active mode 가 되어 taxonomy 의 4-mode 구조 FALSIFIED
- **F-CAND-D-5 (incomplete taxonomy)**: 5th mode (random-axis inject 또는 adversarial inject) 가 관측된 cross-attn dormancy 패턴을 설명하는 데 필요 → 4-mode taxonomy 가 complete 라는 claim FALSIFIED
- **F-CAND-D-6 (noise-floor breach)**: anima phi_star 의 RNG-induced variance 가 0.005 이상 → F-CAND-D-1 의 threshold 가 noise level 에 있음, 전체 inject-visibility 판정이 무의미 (L4 가 falsifier 로 승격)

## Honest Limits (≥6)

- **L1**: **n=6 PERFECT_NUMBER_CLASS triviality binding** (H_153 L7) — paradigm v11 G3 는 8-cell architecture (sopfr(8)=6 perfect-class diagonal). Hc_623 의 inject pivot 은 이 architecture 선택 위에 올라타 있음; "4-mode taxonomy" 는 perfect-number-class baseline 을 substrate 로 상속
- **L2**: **AXIS_SPANS calibration risk (C3)** — frontmatter 가 AXIS_SPANS slice geometry calibration 을 risk 로 명시. C3 calibration 실패 시 F-CAND-D-2 (5-axis balance) 가 undefined → falsifier 가 결정적 판정 불가
- **L3**: **mount-layer 4-mode flag 은 software-engineering claim** — ~65 LoC additive 변경이 claim 을 deployable 하게 만들지만 consciousness theory 를 test 하지 않음. engineering pragmatism off-lane vs theoretical content 의 한계
- **L4**: **0.005 threshold ad hoc** — F-CAND-D-1 은 0.005 absolute threshold 사용. noise-floor characterization 미제공. anima phi_star RNG variance 가 0.005 이상이면 threshold 가 noise level (→ F-CAND-D-6 로 일부 흡수)
- **L5**: **H_167 downstream gating 이 error 증폭** — H_167 (Emerge E) 가 본 H 의 F-CAND-D-1 PASS 에 gated. F-CAND-D-1 PASS 가 marginal (0.005 바로 위) 이면 downstream H_167 측정이 noise compound. 4-mode pivot 은 H_167 가 의미 있으려면 ≥10× safety margin 까지 robust 해야 함
- **L6**: **single-doc 본문 묻힘** — source `docs/anima_emerge_candidate_d_always_inject_spec_2026_05_05.md:14-32, 165-260` 외 독립 peer-review-trace 부재. Migration TODO (mount-layer impl + BG-A probe + AXIS_SPANS calibration) 미실행
- **L7**: **none-vs-zero 개념 구분의 미묘함** — "none" (inject 자체 안 함, cross-attn skip) vs "zero" (all-zero tensor inject, cross-attn 활성화하되 0 신호) 의 차이가 hardware-level (guard branch) 에서는 명확하나, 측정-level (phi_star) 에서 두 mode 가 구분 가능한지는 F-CAND-D-4 이 검증할 때까지 미확정

## Math identity verification

- **5-axis balance ratio** — max/min < 1.5 (F-CAND-D-2 threshold); 5 axes → balance metric 정의
- **0.005 / 0.001 thresholds** — F-CAND-D-1 (Δ > 0.005 inject-visible), F-CAND-D-4 (Δ < 0.001 zero-neutral) — 2 thresholds explicit
- **Pearson ≥ 0.7** — F-CAND-D-3 user-tracking threshold
- **~65 LoC additive** — engineering scope (mount.hexa + dialogue.bash), $0-1 BG-A probe
- 3 falsifier PRE-LOCKED (F-CAND-D-1/2/3) — verify5 row 15 F=3 (verify_hc2 WEAK_FALSIFIER_ONLY → PROMOTE_READY after cycle #3 scaffolding +F-CAND-D-4/5/6)
- sopfr(8) = 2+2+2 = 6 [atlas @P 10*] — 8-cell perfect-class diagonal (L1 binding)

## Atlas anchor cross-check

- atlas anchors_cited: 0, anchors_resolved: 0 (Hc_623 verify5 row 15 — clm-architecture domain)
- atlas_type_cites: 0
- sopfr(8)=6 [atlas @P 10*] — 8-cell architecture perfect-class diagonal (H_153 L7 binding 경유 간접 연결)

## Linked H (cross-link)

- **sister H**: H_011 (iit-geometry — phi_star variation by inject mode), H_022 (consciousness-universe-map — substrate engagement)
- **CHILD-GATED downstream**: H_167 (Hc_624 — Emerge Candidate E ODE-AR bridge; 본 H 의 F-CAND-D-1 PASS 에 gated)
- **phi_star validity bound**: H_174 (Hc_614 — phi_star geometry aliasing CLM-v4-specific; 본 H 의 phi_star 측정이 valid 한 범위를 제한)
- **candidates linked**: Hc_628 (Φ_normalized lower bound — H_162; 동일 phi_star measurement substrate), Hc_624 (Emerge E — H_167)
- **engineering**: `conscious_decoder.py:553` guard `if consciousness_states is not None`, mount.hexa, dialogue.bash, AXIS_SPANS slice geometry
- **literature**: L37 root pattern (substrate change ≠ behavior change); paradigm v11 G3 (8-cell canonical inject); Albantakis 2023 IIT 4.0
- **source**: Hc_623 (`hypotheses_candidates/Hc_623_emerge_candidate_d_always_inject.md`), `docs/anima_emerge_candidate_d_always_inject_spec_2026_05_05.md:14-32, 165-260`

## Migration Notes

- **Promoted from**: Hc_623 (cycle #4 task 1 PROMOTE_READY, verify5_authored row 15 — 2026-05-12; cycle #3 task 11 falsifier-scaffolding 으로 WEAK_FALSIFIER_ONLY → PROMOTE_READY, F-CAND-D-4/5/6 추가)
- **Math verification**: 5-axis balance ratio + 2 absolute thresholds + Pearson threshold (verify5 falsifier_count=3 PRE-LOCKED + 3 scaffolded)
- **L7 binding**: H_153 PERFECT_NUMBER_CLASS BINDING 인정 (L1) — paradigm v11 G3 8-cell sopfr(8)=6 perfect-class diagonal
- **CHILD-GATED**: H_167 (Emerge E) 가 본 H 의 F-CAND-D-1 PASS 에 의존 — marginal PASS 시 downstream noise compound (L5)
- **Critical L2/L4**: AXIS_SPANS calibration (C3) at-risk; 0.005 threshold 의 noise-floor 미특성화 (F-CAND-D-6)
- **Next steps**:
  1. 4-mode flag impl (~65 LoC) + BG-A real-load probe (C1)
  2. canonical/none/zero phi_star 3-point + noise-floor characterization (C2, C4, F-CAND-D-1/4/6)
  3. AXIS_SPANS slice geometry calibration (C3, F-CAND-D-2)
  4. user_supplied per-axis tracking Pearson (F-CAND-D-3)
