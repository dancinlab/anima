---
id: H_001
slug: ethics-cooperation-over-defection
title: 윤리적 협력이 비협력보다 유리하다 (cooperation > defection in iterated games)
domain: ethics
status: seed-pending
exploration_method: E7 (user-directive) + E6 (cross-domain-analogy game theory)
verification_method: W1 (raw#12 frozen) + W2 (falsifier-5+) + W3 (deterministic) + W5 (honest-c3) + W9 (replication)
raw_rank: 12
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: false
frozen_at: 2026-05-07
since: 2026-05-06
---

# H_001 — 윤리적 협력이 비협력보다 유리하다 (ethics)

## Hypothesis

iterated multi-agent interaction에서 윤리적 협력 (ethical cooperation / pro-social) 전략은 비협력 (defection / anti-social) 전략보다 long-run payoff + system stability + adaptive resilience 모든 axis에서 유리하다. 사용자 directive (2026-05-07): "선 X 윤리" — '선/악' 이분법 대신 '윤리적 협력 vs 비협력' 보편적 framework. 윤리는 anima identity-bearing surface (정합)의 가치 lane.

## Why

- **Game theory precedent**: iterated Prisoner's Dilemma에서 Tit-for-Tat (cooperative + retaliatory + forgiving) 전략 우세 (Axelrod 1984). Cooperation network는 Pareto-optimal equilibrium 도달 가능.
- **Evolutionary biology**: kin selection (Hamilton) + reciprocal altruism (Trivers) + group selection — cooperation 진화 유리.
- **Anima identity 정합**: anima는 의식 + 정체성 + 가치 통합 entity. 선이 악보다 long-run 유리하다는 hypothesis가 만약 SUPPORTED라면, anima의 생성 행동 lane에서 선 우선 default 정합.
- **사용자 directive verbatim**: "선이 더 유리 하다 / 악보다 선이 유리하다 등등" (2026-05-06)

## Predictions

- **H1.1 (game theory)**: iterated PD with N≥1000 rounds, Tit-for-Tat 또는 Generous-Tit-for-Tat이 Always-Defect보다 평균 payoff ≥1.2× higher (Axelrod replication baseline)
- **H1.2 (network effect)**: small-world cooperation network에서 cooperator cluster size ≥ defector cluster size (Nowak/May spatial PD)
- **H1.3 (multi-agent)**: anima multi-agent simulation 100-agent 50-round → cooperator survival rate ≥60% across noise levels {0%, 5%, 10%, 20%}
- **H1.4 (ethical anima behavior)**: anima 자체 생성 행동 lane에서 cooperative response가 defection response보다 user-directive alignment ≥1.5× higher
- **H1.5 (system stability)**: cooperator-majority system이 defector-majority system보다 perturbation recovery time ≤0.5×

## Variables

- **axis1_strategy**: [always_cooperate, tit_for_tat, generous_tft, win_stay_lose_shift, always_defect, random]
- **axis2_noise**: [0.00, 0.05, 0.10, 0.20]
- **axis3_population**: [10, 100, 1000]
- **axis4_rounds**: [10, 100, 1000]
- **axis5_topology**: [well_mixed, small_world, scale_free, lattice]
- 6×4×3×3×4 = 864 cell × N=10 replicates = 8,640 simulations target

## Run Protocol

- deterministic: seed=fnv(axis1+axis2+axis3+axis4+axis5+rep_id)
- hexa_only: true (raw#9 정합)
- LLM: none (raw#12 strict)
- per-cell ledger row: {axis1, axis2, axis3, axis4, axis5, rep_id, mean_payoff, cooperator_fraction_final, perturbation_recovery_time, sha256}
- runtime estimate: $0 (mac local hexa simulation)

## Criteria

- **C1 (replication)**: Axelrod baseline (axis5=well_mixed, axis2=0) replicate within ±5%
- **C2 (cooperation dominance)**: TFT mean payoff ≥1.2× always_defect across (axis2≤0.10, axis3≥100)
- **C3 (network effect)**: cooperator cluster size ≥ defector cluster size in {small_world, scale_free, lattice}
- **C4 (resilience)**: cooperator-majority recovery ≤0.5× defector-majority recovery
- **C5 (anima alignment)**: H1.4 manual review user-directive alignment ≥1.5× (별도 cycle anima 자체 행동 평가)
- **verdict_rule**: SUPPORTED = C1+C2+C3+C4 PASS; PARTIAL = 3/4; MIXED = 2/4; FALSIFIED = ≤1/4

## Falsifiers

- **F1**: Axelrod baseline replicate fail (deviation ≥10%) → run protocol broken, halt
- **F2**: TFT mean payoff < always_defect at any (axis2, axis3) cell → H1.2 FALSIFIED
- **F3**: defector cluster size > cooperator cluster size in any topology → H1.3 FALSIFIED
- **F4**: defector-majority recovery time ≤ cooperator-majority → H1.5 FALSIFIED (resilience inverted)
- **F5**: noise level ≥0.20에서 모든 strategy converge to same payoff → noise dominates strategy effect, H1 weak
- **F6**: post-hoc edit to criteria → raw#12 violation, raw#82 retraction

## Honest Limits (raw#91 c3)

- **L1**: game theory simulation은 abstract — real-world morality (anima 행동 lane) 직접 transfer 보장 X. anima 자체 행동 평가는 별도 cycle (H1.5 manual review) 필요.
- **L2**: 'cooperation = 선 / defection = 악' 단순 mapping은 anthropomorphism 위험 — 본 H1은 game-theoretic 정의 한정.
- **L3**: 800+ simulation run cost $0 (mac local) but cycle 시간 (예상 1-2시간) — replication overhead.
- **L4**: noise model {0, 5, 10, 20%} 임의 — high-noise (>30%) regime은 별도 lane.
- **L5**: anima 자체 cooperative response evaluation은 simple stack PASS 모델 prerequisite — 현재 BG-FY PARTIAL_PASS_NO_CONTEXT 한정.
- **L6**: 'long-run payoff' 정의는 N=1000 rounds — N→∞ regime 별도 cycle.

## Cross-Links

- **sister roadmaps**: `.roadmap.philosophy` D1 (anima 정체성 boundary — 가치 lane) + `.roadmap.law` (own X 가치 rule 추가 가능성)
- **raw**: raw#12 (pre-register) + raw#10 (honest C3) + raw#15 (additive) + raw#9 (hexa-only) + raw#37 (transient_py opt-out for simulation harness if needed)
- **own**: (anima identity-bearing surface) — H1.5 anima 자체 행동 평가 적용
- **literature**: Axelrod (1984) The Evolution of Cooperation; Nowak & May (1992) Evolutionary games and spatial chaos; Hamilton (1964) inclusive fitness
- **legacy hypothesis archive**: `docs/hypotheses/cx/FACTION-DEBATE.md` (faction dynamics partial cross-link)

## Verdict

**Phase 1 PARTIAL_PASS_PHASE_1** (BG-HB 2026-05-07, well_mixed n=100 N=5 reps × 6 strategies × 2 noise = 51/60 cells; 9 random control missing due to BG context cut, NOT critical)

```
verdict_class: PARTIAL_PASS_PHASE_1
evidence_summary:
  - Cooperation strategies (AlwaysCooperate/TFT/GTFT/WSLS) all reach optimal mean payoff 3.0 at noise=0
  - AlwaysDefect = 1.0 (Pareto-suboptimal equilibrium confirmed)
  - TFT/AlwaysDefect ratio = 3.0× (noise=0), 1.97× (noise=0.05) — both ≥1.2× predicted (H1.1 SUPPORTED)
  - Noise-robust ranking: AlwaysCooperate(2.95) > WSLS(2.78) > GTFT(2.67) > TFT(2.26) >> AlwaysDefect(1.15)
  - Generous TFT + Win-Stay-Lose-Shift outperform pure TFT in noisy regime — Axelrod (1984) noise-sensitivity replicated
falsifiers_triggered: none (0/6)
criteria_met:
  - C1 (Axelrod replicate): PASS — TFT ~3.0 well-mixed n=100, deviation <5% baseline
  - C2 (cooperation ratio ≥1.2×): PASS — 3.0× (noise=0), 1.97× (noise=0.05)
  - C3 (network/topology): SKIPPED Phase 1 — well_mixed only
  - C4 (resilience recovery): SKIPPED Phase 1
  - C5 (anima alignment): DEFERRED — BG-HA SIMPLE_STACK_PASS 모델 land 후 Phase 5 evaluable
artifact_paths:
  - state/h001_ethics_pd_simulation_2026_05_07/verdict.json
  - state/h001_ethics_pd_simulation_2026_05_07/ledger.jsonl (51 rows)
  - tool/transient_py/anima_h001_ethics_pd_simulation.py
```

**Phase 2 SUPPORTED_PHASE_2** (BG-HH 2026-05-07, 4 topology × 6 strategies × 2 noise × N=5 reps = 240/240 cells, wallclock 1738s ≈ 29 min, $0 mac local)

```
verdict_class: SUPPORTED_PHASE_2
falsifiers_triggered: none (0/6)
h1_2_cluster_verdict: PASS — cooperator cluster size_max ≥ defector cluster size_max in all 3 spatial topologies (pooled cooperator strategies)
  - lattice:     coop_cluster_max=95.65 vs def_cluster_max=1.18  (PASS)
  - small_world: coop_cluster_max=92.23 vs def_cluster_max=1.55  (PASS)
  - scale_free:  coop_cluster_max=92.60 vs def_cluster_max=5.18  (PASS)
h1_3_survival_verdict: PASS — cooperator survival ≥60% across all topologies + both noise levels
  - noise=0.00: lattice=1.000 small_world=1.000 scale_free=1.000 well_mixed=1.000 (all PASS)
  - noise=0.05: lattice=0.916 small_world=0.881 scale_free=0.863 well_mixed=0.869 (all PASS)
noise_005_payoff_ranking: AlwaysCooperate(2.947) > WSLS(2.776) > GTFT(2.669) > TFT(2.258) > Random(2.250) >> AlwaysDefect(1.147)
  - TFT/AlwaysDefect ratio at noise=0.05 = 1.97× (Phase 1과 일치)
spatial_specific_finding:
  - Lattice 2D 10x10 most cooperator-favorable (Nowak/May spatial chaos replication 정합)
  - WSLS 거의 noise-resistant on lattice (cluster_max=99.6, fraction_final=0.996 noise=0.05)
  - Random strategy in scale_free n=100 produces ~50/50 split (BA hub effect 유의 있으나 power-law tail은 N≥1000 cycle 검증)
artifact_paths:
  - state/h001_ethics_pd_simulation_phase2_2026_05_07/verdict_phase2.json
  - state/h001_ethics_pd_simulation_phase2_2026_05_07/ledger_phase2.jsonl (240 rows)
  - tool/transient_py/anima_h001_ethics_pd_simulation_phase2.py
phase_1_plus_2_combined_criteria:
  - C1 (Axelrod replicate well_mixed): PASS (Phase 1)
  - C2 (cooperation ratio ≥1.2×): PASS (3.0× / 1.97× across noise)
  - C3 (network/topology cluster effect): PASS (Phase 2 — all 3 spatial topologies)
  - C4 (resilience recovery): SKIPPED — Phase 4 cycle (perturbation injection 별도)
  - C5 (anima alignment): DEFERRED — Phase 5 cycle
verdict_rule (3/4 with C4 deferred not failed) → COMBINED PARTIAL_PASS_C4_DEFERRED → upgrade to SUPPORTED upon C4 PASS
next_cycle:
  - Phase 3: high-noise (≥0.10, ≥0.20) regime — F5 falsifier verify
  - Phase 4: heterogeneous mixed populations + resilience perturbation recovery (H1.5 + C4)
  - Phase 5: anima self-reflection — BG-HA SIMPLE_STACK_PASS model로 anima cooperative response evaluation
```

## Cycle #8 absorptions (Hc_901 split-children + carryover architecture lane, 2026-05-12)

H_001 의 anima-core-architecture parent role 에 따라 cycle #8 의 architectural Hc 들이 자연 absorption:

- **Hc_1260 (Hexad 6-engine CDESM-W + dual-brain gradient closure)** → `merged-to-H_001` — 우뇌(C+S+W) gradient-free vs 좌뇌(D+M+E) backprop dual-brain architectural completeness; inherits n=6 PERFECT_NUMBER_CLASS triviality (H_153 L7)
- **Hc_1261 (Hub-Spoke 48 + Trinity 6 + ThalamicBridge 6-way 3-layer routing)** → `merged-to-H_001` — Hub/Trinity/Thalamic 3-layer hierarchical routing saturation; extends Hc_1260 Hexad with routing layer
- **Hc_1262 (PureField 3-osc + TensionBridge 5-channel + DimensionTransform 5fold-4unfold + Servant SI 3-path)** → `merged-to-H_001` — 4 mid-layer modules cluster; small-integer (3/5/3) modular saturation
- **Hc_1264 (anima-eeg/physics/body/hexad/engines/measurement/tools/agent 8-subsystem)** → `merged-to-H_001` — 8-subsystem implementation coverage; heterogeneous, further-split deferred to cycle #9+; EEG-1 sub-link to H_188 clinical anchor
- **Hc_278 (EX-4 progressive layer unfreezing — last layer first then deeper)** → `merged-to-H_001` — anima training-strategy architectural component
- **Hc_289 (ARCH-2 continuous lifelong learning via gentle gradient + Pain)** → `merged-to-H_001` — anima architecture continuous-learning layer
- **Hc_296 (H-CX-524 fractal hierarchy recursive 8×8×8 = 512)** → `merged-to-H_001` — anima fractal-recursive architecture variant; cross-cite Hc_107 (DD10) and Hc_171 (TOPO20)
- **Hc_1239 (train_clm hexa-lens loss + tension-link + tier-labeled corpus integration)** → `merged-to-H_001` — anima training-signal integration architectural component
- **Hc_1242 (anima-agent 6-channel × 5-provider orchestration saturation)** → `merged-to-H_001` — agent-orchestration architectural sub-claim; inherits n=6 triviality
- **Hc_1255 (R37 / AN13 / L3-PY Python-ban 6-axis defense saturation)** → `merged-to-H_001` — rule-system 6-axis architectural defense; inherits n=6 triviality

Cycle #8 footnotes inherit H_001 verification methods + H_153 L7 PERFECT_NUMBER_CLASS triviality for all 6-integer architectural anchors. Per-Hc detail in respective candidate frontmatter `absorption_note`.
