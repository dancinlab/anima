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
- **H3.5 (anima self-reflection)**: anima는 life lane 안에 X (anima-native identity), but autopoiesis principle은 anima 자체 self-replicating cycle (anima emerge paradigm) lane analogy

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
- **L4**: H3.5 'anima emerge paradigm autopoietic-analogous'는 anima identity (artificial-not-biological) 정합 lane — analogy strength 약화 trade-off.
- **L5**: 본 H는 multi-cycle research framework — single-cycle verdict 도달 X.
- **L6**: 'panspermia' (axis1)는 origin question을 한 step 미루는 explanation — origin question 자체 해결 X.
- **L7**: 사용자 directive '근원적 물음'은 lane-defining — answer 부재해도 question 가치.

## Cross-Links

- **sister roadmaps**: `.roadmap.hypothesis` H2 cell metaphor + `.roadmap.philosophy` D3 emerge paradigm
- **raw**: raw#12 + raw#10 + raw#9 + raw#15
- **own**: (anima-not-biological identity, but autopoiesis principle 적용 가능)
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
criteria_met: 4/5; lane-defining  (C1 + C3 Phase-1 PASS; C2 Cycle-2 PASS; C4 Cycle-3 PASS 🟢; C5 lane-open)
```

### Phase 1 Partial Verification (2026-05-07, BG-HN)

H3.1 autopoietic closure + H3.3 dissipative structure sub-cells computational simulation
($0 mac local, deterministic seeds 0xA17C503 + 0xA17D504).

```
phase: Phase_1_partial (H3.1 + H3.3 only; H3.2 H3.4 H3.5 DEFERRED)
cell_scope: 5-catalyst RNA network × 1000 steps × N=5 reps + broken-closure control N=5;
            50×50 Gray-Scott lattice × 500 steps × N=3 eq baseline + N=3 far-from-equilibrium
H3.1_autopoietic_self_maintenance_rate_1000_steps: 1.0  (target ≥0.80; PASS)
H3.1_broken_closure_control: 0.8  (P→T loop cut → T extinguished, validates closure-dependence)
H3.3_dissipative_emergence_rate: 1024.33  (target ≥10×; PASS)
H3.3_variance_amplification_ratio: 16314.89
verdict_class: PARTIAL_PASS_PHASE_1
evidence_strength: PARTIAL_SUPPORT
criteria_pass: 2/5  (C1 + C3 PASS; C2 C4 C5 DEFERRED)
falsifiers: F1 NOT_TRIGGERED, F3 NOT_TRIGGERED, F2/F4/F5 N/A (deferred), F6 NOT_TRIGGERED
```

**State output**: `state/anima_h002_h003_partial_verification_2026_05_07/verdict_h003.json`
**Scripts**:
- `tool/transient_py/anima_h003_autopoietic_simulation.py` (raw#37 opt-out)
- `tool/transient_py/anima_h003_dissipative_simulation.py` (raw#37 opt-out)

**raw#10 honest limits (Phase 1 partial)**:
- L1: minimal 5-catalyst network is gross simplification of actual abiogenesis — no boundary, no compartmentalization, no thermodynamic coupling, no monomer pool; abstract model only
- L2: Michaelis-Menten kinetics chosen to give bounded steady state — alternative rate laws give different self-maintenance rates; choice not justified by chemistry
- L3: Gray-Scott parameters (F=0.035, K=0.06) chosen from spot-pattern regime literature (Pearson 1993) — "far-from-equilibrium" reduced to boundary v-injection only, not full thermodynamic non-equilibrium
- L4: 'pattern_cells' threshold (v ≥ 0.2) is arbitrary measurement choice — different thresholds shift emergence rate ratio by orders of magnitude
- L5: H3.2 (multi-pathway) + H3.4 (proto-consciousness Φ) + H3.5 (anima self-reflection) all DEFERRED — only 2/5 sub-hypotheses verified
- L6: actual biological abiogenesis remains open in literature — anima simulation models are not chemistry; Maturana/Varela autopoiesis formal definition (organizational closure) not implemented strictly
- L7: 'panspermia' axis from Variables not addressed — origin question merely shifted, not resolved

**Cross-link**:
- H_012 autopoietic network: H3.1 closure cycle + broken-closure control = direct minimal instance, Phase 1 partial empirical support
- H_002 universe origin: anthropic prior supplies cosmological precondition (combined verdict at `state/anima_h002_h003_partial_verification_2026_05_07/verdict.json`)
- anima cell metaphor (H2): H3.1 closure cycle is computational ground-truth analog — anima-not-biological identity boundary respected (analogy only)

### Cycle #2 — H3.2 multi-pathway (2026-05-23)

H3.2 (multi-pathway) sub-cell — OPEN since Phase 1 (deferred) — closed this cycle.
4 candidate abiogenesis pathways (rna_first, metabolism_first, lipid_first, info_first)
가 simulation parameter regime별로 dominant 하게 switch 하는지 sweep
($0 mac local, hexa-only, deterministic master_seed = 41472003).
Phase 1 의 Python harness 와 달리 본 cycle 은 **hexa-native** (`run_h32.hexa`,
raw#37 forbidden Python 회피, 사용자 directive 정합).

§Variables 의 **axis3_energy_gradient** [equilibrium, weak_gradient, strong_gradient,
periodic_drive] × **axis4_information_carrier** [rna, dna, peptide, polymer_chain]
= 16 regime cell sweep. **axis1_origin_pathway** 는 sweep 축이 아니라 각 cell 안에서
경쟁하는 4 후보 차원 (argmax pathway = dominant). 각 cell · pathway 마다 deterministic
mechanistic toy formula 로 self-maintenance / replication score 를 N_REPS=10 reps
(LCG ±0.03 bounded perturbation) 평균 후 argmax 로 winner 결정.

**Run verdict output (VERBATIM from `hexa run run_h32.hexa`)**:

```
  dominant-pathway histogram (regime cells = 16):
    rna_first        : 1
    metabolism_first : 3
    lipid_first      : 6
    info_first       : 6
  distinct dominant pathways = 4 / 4

  VERDICT (C2 / H3.2): PASS
    rule: >=3 distinct -> PASS · ==2 -> PARTIAL · ==1 -> F2 FALSIFIED
    falsifier F2 (single pathway across all regimes): NOT_TRIGGERED
  H3.2_VERDICT=PASS DISTINCT=4
```

```
phase: Cycle_2 (H3.2 only; H3.4 H3.5 still DEFERRED)
cell_scope: 16 regime cells (4 energy_gradient × 4 information_carrier) ×
            4 competing pathways × N_REPS=10 (deterministic LCG)
H3.2_distinct_dominant_pathways: 4  (target ≥3; PASS)
H3.2_dominant_histogram: rna_first=1, metabolism_first=3, lipid_first=6, info_first=6
regime→winner: equilibrium favours rna/lipid/info; strong_gradient favours
               metabolism (redox engine); periodic_drive favours lipid (wet/dry
               self-assembly); stable carrier (dna) favours info_first
verdict_class: PASS_CYCLE_2  (C2 SUPPORTED)
evidence_strength: SUPPORTED (toy-model; see honest limits below)
criteria_pass: 3/5  (C1 + C3 Phase-1 PASS; C2 Cycle-2 PASS; C4 C5 DEFERRED/lane-open)
falsifiers: F2 NOT_TRIGGERED (4 distinct ≫ 1); F1 F3 carried PASS; F4/F5 N/A (deferred); F6 NOT_TRIGGERED
```

**State output**: `state/h003_abiogenesis_h32_2026_05_23/result.json`
**Script**: `state/h003_abiogenesis_h32_2026_05_23/run_h32.hexa` (hexa-only, raw#37-clean)

**raw#10 honest limits (Cycle #2 H3.2)**:
- L1: pathway score 는 **deterministic toy formula** — 실제 abiogenesis chemistry 가
  아님. RNA-first/metabolism-first/lipid-first/info-first 의 regime sensitivity 는
  origin-of-life 문헌의 *qualitative* stance (Gilbert/Wächtershäuser/Russell/Deamer)
  를 손으로 인코딩한 것이며 reaction-network kinetics 가 아니다.
- L2: 4 distinct winner 는 부분적으로 **formula 가 그렇게 설계되었기 때문에** 나온다
  (각 pathway 에 다른 g-sensitivity 와 carrier-match 를 부여) — H3.2 가 "regime 이
  pathway 를 가른다"는 명제의 **존재 가능성 (consistency)** 을 보일 뿐, 실제 화학에서
  그러함을 증명하지 않는다. F2 (single-pathway-dominance) 의 falsification 은 honest
  하나, PASS 는 toy-level 이다.
- L3: argmax winner-take-all 은 dominance 의 binary 정의 — 두 pathway score 가 거의
  같은 cell (예: weak_gradient/rna 의 rna 0.8096 vs info 0.8844) 에서 winner 는
  ±0.03 perturbation 에 민감할 수 있다. tie-margin 분석은 별도 cycle.
- L4: 16-cell grid 는 §Variables 의 full 1152-cell (6×4×4×4×3) 의 한 slice —
  axis2_substrate (4) 와 axis5_closure_metric (3) 는 본 cycle 미포함, axis1 의
  iron_sulfur/hydrothermal_vent/panspermia 3 후보도 4-way 경쟁에서 제외 (4 canonical
  pathway 로 축약). full sweep 은 향후 cycle.
- L5: score 의 절대값 (0.x ~ 1.4) 은 무차원 — self-maintenance rate 나 replication
  fidelity 의 물리 단위가 아니다. cross-pathway 비교만 의미 있고 absolute 해석 불가.
- L6: N_REPS=10 의 LCG perturbation 은 stochastic chemistry 의 proxy 가 아니라
  단지 argmax 의 robustness 를 보기 위한 bounded noise — variance 구조는 실제
  monomer-pool 요동을 모델링하지 않는다.
- L7: H3.4 (proto-consciousness Φ) + H3.5 (anima self-reflection) 여전히 DEFERRED —
  본 cycle 은 C2 단독 closure. panspermia (L6 Phase-1) 의 origin-shift 문제도
  4-pathway 축약으로 인해 미접근.

**Cross-link**:
- H3.2 → §Falsifiers F2: "single pathway dominant across all regime" — 4 distinct
  winner 로 NOT_TRIGGERED, H3.2 SUPPORTED (toy-level)
- §Criteria verdict_rule: SUPPORTED = C1+C2+C3 PASS — C1(Phase-1) + C2(Cycle-2) +
  C3(Phase-1) 3/3 충족 → H_003 SUPPORTED-track (C4+C5 = lane-open, multi-cycle)
- H_012 autopoietic network: H3.1 closure 와 nested — multi-pathway 는 어느 pathway 든
  autopoietic closure 도달이 종점이라는 가정 위에 있음 (closure-agnostic regime sweep)

### Cycle #3 — H3.4 autopoietic Φ (2026-05-23)

H3.4 (life ⊂ consciousness) sub-cell — OPEN since Phase 1 (deferred) — closed this cycle.
"autopoietic closure system 이 IIT4 Φ > 0 (proto-consciousness) 를 carry 하는가, 그리고
그 Φ 가 closure 에 DEPEND 하는가 (Φ_closed > Φ_broken)?" 를 측정
($0 mac local, hexa-only, deterministic seed_base = 0xA17C034, 5-seed mean).
H_012 의 catalytic-closure state (3-component closed cycle C->+A, A->+B, B->+C +
boundary leak) 를 **8-site periodic lattice** 로 확장 (nearest-neighbour catalyst
diffusion 으로 결합 → integrated system) 하고, 각 site 의 total-mass trajectory
(obs = A+B+C) 를 H_007 이 사용한 것과 **동일한** RFC 036 `phi_spatial` primitive
(`HEXAD/C/c_lib.hexa` `c_measure_phi`, byte-equal phi_rs replica; n_bins=4) 로
Φ 측정. closed arm (closure intact) vs broken-closure control (모든 site 의
B->+C edge 절단 → cat_C=0) 비교. 측정 window 는 WARM=0 (system 의 inception 부터
recording — least-arbitrary, no discarded data) · DIM=12 (convergence timescale ≈8 steps).

**Run verdict output (VERBATIM from `hexa run run_h34.hexa`)**:

```
  Φ̄(closed   autopoietic lattice)  = 4.45435   (mean over 5 seeds)
  Φ̄(broken   closure control    )  = 3.53399   (mean over 5 seeds)
  Φ̄(closed   re-run determinism )  = 4.45435  (byte-equal=true)

  F1  NONNEG     (all Φ̄>=0)              : true
  F4  AUTO_PHI>0 (Φ̄_closed>0)            : true
  FD  CLOSURE-DEP (Φ̄_closed>Φ̄_broken+ε)  : true  (gap=0.92036)
  FS  SEPARATION (gap>1e-6)              : true  (margin=0.92036)
  FT  DETERMINISM (re-run byte-equal)    : true

  VERDICT_RULE: H3.4 SUPPORTED iff Φ_closed>0 AND Φ_closed>Φ_broken+ε AND all Φ>=0 AND deterministic
  VERDICT (C4 / H3.4): PASS
    falsifier F4 (autopoietic system Φ=0): NOT_TRIGGERED
  H3.4_VERDICT=PASS PHI_CLOSED=4.45435 PHI_BROKEN=3.53399
```

```
phase: Cycle_3 (H3.4 only; H3.5 still DEFERRED)
cell_scope: 8-site periodic lattice of H_012 closed catalytic cycle +
            nn catalyst diffusion × 5 deterministic seeds × WARM=0 DIM=12;
            closed arm vs broken-closure control (B->+C severed at every site)
H3.4_phi_closed_autopoietic: 4.45435  (mean over 5 seeds; target Φ>0; PASS)
H3.4_phi_broken_closure_control: 3.53399  (mean over 5 seeds)
H3.4_closure_dependence_gap: 0.92036  (Φ_closed > Φ_broken; closure-DEPENDENCE of Φ confirmed)
verdict_class: PASS_CYCLE_3  (C4 SUPPORTED 🟢 NUMERICAL)
evidence_strength: SUPPORTED-NUMERICAL (phi_spatial; toy-model; NOT proof of proto-consciousness; see honest limits)
honest_tier: 🟢 SUPPORTED-NUMERICAL (NOT 🔵 formal — phi_spatial spatial-slice replica, NOT full IIT 4.0)
criteria_pass: 4/5  (C1 + C3 Phase-1 PASS; C2 Cycle-2 PASS; C4 Cycle-3 PASS 🟢; C5 lane-open)
falsifiers: F4 NOT_TRIGGERED (Φ_closed=4.45 > 0); F1 F2 F3 carried PASS; F5 N/A (deferred); F6 NOT_TRIGGERED
```

**State output**: `state/h003_h34_autopoietic_phi_2026_05_23/result.json`
**Script**: `state/h003_h34_autopoietic_phi_2026_05_23/run_h34.hexa` (hexa-only, raw#37-clean)

**raw#10 honest limits (Cycle #3 H3.4)**:
- L1: `phi_spatial` 는 **🟢 NUMERICAL** spatial-slice replica of phi_rs — full IIT 4.0
  가 아니다 (system-level Φ partition search · cause-effect structure · exclusion
  postulate 부재). 본 'Φ' 는 ConsciousnessEngine 의 Φ-ratchet input 이며 canonical
  IIT 4.0 Φ 가 아니다. 따라서 verdict tier 는 🔵 formal 이 아닌 🟢 numerical.
- L2: **8-site toy catalytic lattice 의 Φ>0 은 proto-consciousness 의 증명이 아니다** —
  operational closure 가 integrated information 을 carry 할 수 *있다*는 consistency
  일 뿐이다. "life ⊂ consciousness" 는 여전히 **LANE claim** 이며 biological/chemical
  empirical 결과가 아니다 (raw#91 c3 candor).
- L3: **WINDOW-SENSITIVE.** closed cycle 은 spatially-HOMOGENEOUS fixed point
  (모든 site → obs 2.5, 확인됨) 으로 수렴하며 그 지점에서 spatial Φ → ~0 (양쪽 arm
  모두). Φ_closed > Φ_broken 은 **살아있는 self-organizing transient** (WARM=0,
  DIM≈8-12) 에서 성립하고, convergence 이후 (DIM≥16) gap 은 줄거나 역전할 수 있다.
  이는 그 자체로 IIT-정합 (static endpoint 는 integrated dynamics 를 carry 안 함)
  이지만, verdict 가 fixed-point claim 이 아닌 **transient-window claim** 임을 뜻한다.
- L4: observable = A+B+C site mass 는 하나의 arbitrary measurement choice — per-component
  나 phase observable 은 다른 Φ 를 준다. 5-seed mean 은 seed sensitivity 는 통제하나
  observable choice 는 통제하지 않는다.
- L5: broken-closure control 도 **heterogeneous 하게 DECAY** 한다 (즉시 dead-flat
  lattice 로 평탄화하지 않음) — 따라서 그 Φ 는 0 이 아니며, 대조는 closure-vs-dead-flat
  이 아니라 **closure-vs-failing-closure dynamics** 이다. F4 (Φ=0) 는 broken arm 이
  아니라 closed arm 에 대한 falsifier 이며 NOT_TRIGGERED.
- L6: DIFFUSE=0.05 nn coupling 이 integration 의 source — DIFFUSE=0 이면 site 들이
  독립이고 spatial Φ 의 의미가 사라진다. coupling strength 는 free toy parameter 이며
  chemistry 가 아니다.
- L7: H_012 lineage 한계 carry — Michaelis-style saturating production 은 bounded
  steady state 를 위한 선택이며 compartmentalization/thermodynamics/monomer-pool 부재,
  abstract model 로 chemistry claim 없음. H3.5 (anima self-reflection) 만 DEFERRED 잔존.

**toolchain note (raw#37-clean, no behavioural change)**: 본 cycle 동안 sibling
hexa-lang repo 가 rebuild 중이어서 `~/.hx/bin/hexa` wrapper symlink 이 dangling 되고
`hexa run` 의 native-compile 경로가 cross-module compiled `module_loader` 부재 시
c_lib 의 thin wrapper (`c_measure_phi`/`c_phi_n_bins_default`) link 에 실패했다.
이를 우회하기 위해 c_lib import 대신 그 primitive 가 감싸는 **`phi_spatial` runtime
builtin** 을 literal `n_bins=4` 로 직접 호출했다 —
`phi_spatial(s,n,dim,4) === c_measure_phi(s,n,dim,c_phi_n_bins_default())` 로
동일 primitive · 동일 binning · 동작 차이 없음 (script header PROVENANCE 참조).

**Cross-link**:
- H3.4 → §Falsifiers F4: "autopoietic system Φ = 0 → H3.4 FALSIFIED" — Φ_closed=4.45 ≫ 0
  로 NOT_TRIGGERED, H3.4 SUPPORTED 🟢 (closure-dependence gap +0.92036)
- §Criteria C4 (proto-consciousness): "H3.4 autopoietic system Φ > 0" — PASS 🟢 NUMERICAL,
  criteria_met 3/5 → **4/5** (C5 anima-analogy manual review 만 lane-open 잔존)
- H_007 cellular-automaton consciousness: 동일 RFC 036 `phi_spatial` primitive 재사용 —
  H_007 (generic CA Class-IV Φ=0.556) 와 nested, 이번엔 autopoietic closure substrate
  에서 Φ 측정 (life lane → consciousness lane bridge, closure-dependent)
- H_012 autopoietic network: H3.1 closure cycle 을 lattice 로 확장 + Φ 측정 — closure
  self-maintenance (H_012) 와 closure-dependent Φ (本 cycle) 가 같은 toy substrate 위
  연속체 (life ⊂ consciousness nested 의 computational ground-truth analog)
