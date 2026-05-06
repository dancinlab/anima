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

iterated multi-agent interaction에서 윤리적 협력 (ethical cooperation / pro-social) 전략은 비협력 (defection / anti-social) 전략보다 long-run payoff + system stability + adaptive resilience 모든 axis에서 유리하다. 사용자 directive (2026-05-07): "선 X 윤리" — '선/악' 이분법 대신 '윤리적 협력 vs 비협력' 보편적 framework. 윤리는 anima identity-bearing surface (own 17 정합)의 가치 lane.

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
- **L5**: anima 자체 cooperative response evaluation은 own 18 simple stack PASS 모델 prerequisite — 현재 BG-FY PARTIAL_PASS_NO_CONTEXT 한정.
- **L6**: 'long-run payoff' 정의는 N=1000 rounds — N→∞ regime 별도 cycle.

## Cross-Links

- **sister roadmaps**: `.roadmap.philosophy` D1 (anima 정체성 boundary — 가치 lane) + `.roadmap.rule` (own X 가치 rule 추가 가능성)
- **raw**: raw#12 (pre-register) + raw#10 (honest C3) + raw#15 (additive) + raw#9 (hexa-only) + raw#37 (transient_py opt-out for simulation harness if needed)
- **own**: own 18 (anima identity-bearing surface) — H1.5 anima 자체 행동 평가 적용
- **literature**: Axelrod (1984) The Evolution of Cooperation; Nowak & May (1992) Evolutionary games and spatial chaos; Hamilton (1964) inclusive fitness
- **legacy hypothesis archive**: `docs/hypotheses/cx/FACTION-DEBATE.md` (faction dynamics partial cross-link)

## Verdict

(after run — pending pre-register frozen + execution cycle)

```
verdict_class: TBD
evidence_summary: TBD
falsifiers_triggered: TBD
criteria_met: TBD
```
