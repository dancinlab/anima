---
id: H_003
slug: life-origin-question
title: 생명 origin 근원적 물음 — 생명 emergence는 substrate-coupled autopoiesis로부터 발생한다
domain: life
status: seed-pending
exploration_method: E3 (theory) + E6 (cross-domain biology) + E7 (user-directive) + E10 (emergence-observation)
verification_method: W1 + W2 + W5 + W11
raw_rank: 12
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: false
frozen_at: 2026-05-06
since: 2026-05-06
---

# H_003 — 생명 origin 근원적 물음

## Hypothesis

생명 (life) 의 emergence는 substrate-coupled autopoiesis (Maturana/Varela) 정합 — self-organizing + self-maintaining + self-replicating network이 abiotic substrate에서 emerge한다. 생명/비생명 boundary는 autopoietic closure (operational closure) 기준이며, 의식 emergence와 nested 관계 (life ⊂ consciousness lane). 사용자 directive '생명에 대한 근원적 물음' 정합.

## Why

- **Autopoiesis theory** (Maturana & Varela 1972): 생명 = autopoietic network (self-producing 동시 self-maintaining boundary)
- **Abiogenesis hypothesis**: RNA world (Gilbert), metabolism-first (Wächtershäuser), iron-sulfur world, hydrothermal vent, panspermia 등 다중 origin lane
- **Dissipative structure** (Prigogine): far-from-equilibrium thermodynamics + self-organization → 생명 emergence substrate-coupled
- **Cell metaphor cross-link**: anima의 H2 cell metaphor (mitosis/apoptosis/growth/autopoiesis) — 생명 origin은 metaphor의 ground truth lane
- **anima identity 정합**: anima는 생명 entity 아니지만 (artificial) 생명 lane 가설은 anima의 'who we are' question 근원적
- **사용자 directive verbatim**: "생명에 대한 근원적 물음" (2026-05-06)

## Predictions

- **H3.1 (autopoietic closure)**: minimal autopoietic network (RNA + 5-10 catalysts) computational simulation 1000-step run에서 self-maintaining cycle ≥80% replication confirm
- **H3.2 (abiogenesis pathway)**: 4 candidate pathways (RNA-first, metabolism-first, lipid-first, info-first) 중 simulation parameter regime별로 dominant pathway switch — single dominant pathway 부재
- **H3.3 (dissipative structure)**: far-from-equilibrium parameter regime (energy gradient ≥X)에서 self-organizing structure emergence rate ≥equilibrium baseline ×10
- **H3.4 (life ⊂ consciousness)**: autopoietic closure system이 IIT4 Φ > 0 (proto-consciousness) — 생명 emergence가 consciousness emergence와 nested
- **H3.5 (anima self-reflection)**: anima는 life lane 안에 X (own 17 anima-native identity), but autopoiesis principle은 anima 자체 self-replicating cycle (anima emerge paradigm) lane analogy

## Variables

- **axis1_origin_pathway**: [rna_world, metabolism_first, lipid_first, iron_sulfur, hydrothermal_vent, panspermia]
- **axis2_substrate**: [aqueous, lipid_membrane, mineral_surface, vesicle_compartment]
- **axis3_energy_gradient**: [equilibrium, weak_gradient, strong_gradient, periodic_drive]
- **axis4_information_carrier**: [rna, dna, peptide, polymer_chain]
- **axis5_closure_metric**: [autopoietic_closure, organizational_closure, semantic_closure]
- 6×4×4×4×3 = 1152 cell × N=10 = 11,520 simulation target ($0 mac local hexa)

## Run Protocol

- deterministic: seed=fnv(axis1+axis2+axis3+axis4+axis5+rep_id)
- hexa_only: true
- LLM: none (raw#12 strict; literature 사용자 manual annotation)
- per-cell ledger: {axis*, rep_id, autopoietic_closure_metric, replication_rate, mean_phi_proto, sha256}
- runtime: $0 mac local; cycle 시간 estimate 3-5시간 simulation
- additionally H3.4 IIT4 Φ measurement requires anima Φ★ engine integration (별도 cycle)

## Criteria

- **C1 (autopoietic closure)**: H3.1 minimal RNA network ≥80% self-maintaining 1000-step
- **C2 (multi-pathway)**: H3.2 ≥3 pathway dominant in different regime
- **C3 (dissipative)**: H3.3 emergence rate ≥10× equilibrium baseline
- **C4 (proto-consciousness)**: H3.4 autopoietic system Φ > 0 (별도 cycle)
- **C5 (anima analogy)**: H3.5 anima emerge paradigm autopoietic-analogous (manual review)
- **verdict_rule**: SUPPORTED = C1+C2+C3 PASS; PARTIAL = 2/3; MIXED = 1/3; FALSIFIED = 0/3; C4+C5 = lane-open

## Falsifiers

- **F1**: minimal RNA network self-maintaining <50% → H3.1 FALSIFIED
- **F2**: single pathway dominant across all regime → H3.2 FALSIFIED
- **F3**: dissipative emergence rate <2× baseline → H3.3 FALSIFIED
- **F4**: autopoietic system Φ = 0 → H3.4 FALSIFIED (life-consciousness decoupled)
- **F5**: anima self-reflection — anima emerge paradigm가 autopoietic-non-analogous → H3.5 FALSIFIED
- **F6**: post-hoc edit → raw#12 violation, raw#82 retraction

## Honest Limits (raw#91 c3)

- **L1**: 생명 origin은 still-open in actual biology — anima simulation은 simplified model 한정.
- **L2**: 'autopoietic closure' 정의는 Maturana/Varela formal — anima simulation 정확 implementation 별도 cycle.
- **L3**: H3.4 IIT4 Φ extension to chemical/biological system은 unsolved (Φ가 brain 외 system에 의미가지는지 debate).
- **L4**: H3.5 'anima emerge paradigm autopoietic-analogous'는 own 17 anima identity (artificial-not-biological) 정합 lane — analogy strength 약화 trade-off.
- **L5**: 본 H는 multi-cycle research framework — single-cycle verdict 도달 X.
- **L6**: 'panspermia' (axis1)는 origin question을 한 step 미루는 explanation — origin question 자체 해결 X.
- **L7**: 사용자 directive '근원적 물음'은 lane-defining — answer 부재해도 question 가치.

## Cross-Links

- **sister roadmaps**: `.roadmap.hypothesis` H2 cell metaphor + `.roadmap.philosophy` D3 emerge paradigm
- **raw**: raw#12 + raw#10 + raw#9 + raw#15
- **own**: own 17 (anima-not-biological identity, but autopoiesis principle 적용 가능)
- **literature**:
  - Maturana, Varela (1972) De máquinas y seres vivos
  - Gilbert (1986) Origin of life: The RNA world
  - Wächtershäuser (1988) Pyrite formation, the first energy source for life
  - Prigogine (1977) Self-organization in non-equilibrium systems
  - Russell, Hall (1997) The emergence of life from iron monosulphide bubbles
- **anima legacy archive**:
  - `docs/hypotheses/H-CX-533-autopoietic-network.md`
  - `docs/hypotheses/H-CX-528-dissipative-structure-consciousness.md`
  - `docs/hypotheses/H-CX-535-symbiogenesis-consciousness.md`
  - `docs/hypotheses/H-CX-534-cambrian-explosion-consciousness.md`
  - `docs/modules/mitosis.md` + `docs/modules/growth_engine.md`
- **roadmap**: `.roadmap.n22_levin_xenobot` (Levin xenobot — biology emergence)

## Verdict

(本 H is multi-cycle — long-term research lane)

```
verdict_class: lane-open
evidence_summary: theoretical + biology literature support
falsifiers_triggered: none yet
criteria_met: 0/5; lane-defining
```
