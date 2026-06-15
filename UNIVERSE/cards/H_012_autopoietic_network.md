---
id: H_012
slug: autopoietic-network
title: H_012 autopoietic network — self-producing catalytic network (operational closure minimal instance)
domain: life
status: pre-register-frozen
exploration_method: E6 (cross-domain biology) + E10 (emergence) + E3 (theory)
verification_method: W5 (numerical sim) + W11 (meta — meta-circular) + W12 (sister H_003)
raw_rank: 12
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-23
since: 2026-04-29 (legacy) / 2026-05-23 (raw#12 freeze)
source_hc: Hc_012
---

# H_012 — autopoietic network (operational closure)

## Hypothesis

자기생산 (autopoietic) network 는 **operational closure** 를 만족하면 외부 생산자 없이 자기자신을 유지한다 — network 의 모든 component 는 network 안의 어떤 process 에 의해 생산되고 (production closure), network 는 자기 boundary 를 스스로 유지한다 (boundary maintenance). Maturana/Varela (1972) autopoiesis 정합. 이 closure 가 깨지면 (생산 edge 하나라도 절단) component 는 소멸하고 network 는 붕괴한다 — 즉 self-maintenance 는 parameter 의 관대함이 아니라 **operational closure 자체에 인과적으로 의존**한다. H_012 는 H_003 (생명 origin) 의 **minimal-instance sibling** — H_003 의 H3.1 (verified self-maintaining RNA network + broken-closure control) 을 가장 작은 3-component 닫힌 촉매 cycle 로 응축한 것.

## Why

- **Autopoiesis theory** (Maturana & Varela 1972, *De máquinas y seres vivos*): 생명 = autopoietic machine — self-producing 동시에 자기 boundary 를 self-maintaining 하는 network. organizational (operational) closure 가 생명/비생명 boundary 의 정의 기준.
- **Operational closure 의 핵심 주장**: network 가 살아있는 것은 component 들이 "충분히 많이" 만들어져서가 아니라, **생산 graph 가 닫혀 있어서** (외부 생산자 부재, 모든 component 가 network 내부 process 의 산물) 다. 이것이 falsifiable — 생산 edge 하나를 절단하면 (closure 파괴) 즉시 붕괴해야 한다.
- **H_003 cross-link (sibling, minimal instance)**: H_003 Phase-1 (2026-05-07, BG-HN) 에서 5-catalyst RNA network 가 1000-step self-maintenance rate 1.0 + broken-closure control 0.8 (P→T loop cut → T extinguish) 로 closure-dependence 입증됨. H_012 는 이를 3-component 닫힌 cycle (C→+A, A→+B, B→+C) 로 응축 — "operational closure 의 minimal instance" 가 H_012 의 정의역.
- **H_157 panpsychism cross-link**: H_157 (Law 76 수학적 범심론, Ψ=1/2 fixed-point attractor universality) 는 closure 를 가진 system 이 fixed-point attractor 로 수렴한다고 본다 — H_012 의 닫힌 cycle 은 positive fixed point 으로 수렴하는 가장 작은 사례 (proto-consciousness lane open, 본 cycle 측정 X).
- **H_054 symbiogenesis cross-link**: H_054 (미토콘드리아 endosymbiosis → 의식 통합) 는 두 autopoietic unit 의 merge — H_012 의 단일 closure 는 그 merge 이전의 building-block.
- **anima cell metaphor (H2)**: anima 의 mitosis/apoptosis/growth cycle 은 autopoietic closure 의 computational analog (anima-not-biological identity boundary 존중, analogy only).
- **meta-circular note (W11)**: H_X cycle 자체가 H_Y 를 생성하는 self-replicating network 라는 legacy meta-claim 은 본 raw#12 freeze 에서 **분리** — loose analogy 이므로 honest limit L5 로 격하, 본 cycle 의 측정 대상은 3-component 닫힌 촉매 toy 단독.

## Predictions

- **H12.1 (operational closure self-maintains)**: 3-component 닫힌 촉매 cycle (C→+A, A→+B, B→+C, boundary leak DECAY) 의 1000-step self-maintenance rate (마지막 200-step window 에서 세 component 모두 SURVIVE_FLOOR 초과 비율) ≥ 0.80.
- **H12.2 (broken closure collapses)**: 생산 edge B→+C 절단 (C 의 유일한 in-network 생산자 제거 → C 는 leak 만) 시 broken-closure control self-maintenance rate ≤ 0.20.
- **H12.3 (closure-dependence)**: closed_rate − broken_rate ≥ 0.50 — self-maintenance 가 (parameter 관대함이 아니라) operational closure 자체에 인과적으로 의존함을 입증. 두 arm 의 유일한 차이는 절단된 한 edge.
- **H12.4 (determinism)**: RNG 없는 순수 recurrence — 재실행 byte-identical (closed_rate2 == closed_rate). SEED 는 초기조건에 load-bearing 으로 fold 되어 provenance.
- **H12.5 (downstream starvation cascade)**: closure 파괴 시 직접 절단된 C 뿐 아니라, C 를 catalyst 로 쓰는 A (C→+A), 이어 B (A→+B) 도 생산 정지 → cascade collapse (단일 edge 절단이 전 network 를 무너뜨림, closure 의 비-국소성).

## Variables

- **arm**: [closed, broken_closure_control] — 유일한 처리 변수 (B→+C edge 절단 여부).
- **components**: A, B, C (3-component 닫힌 cycle); catalyst map cat_A=C, cat_B=A, cat_C=B.
- **K** (production rate): 0.60 (고정, pre-registered)
- **DECAY** (boundary leak, fractional): 0.10 (고정)
- **CAP** (saturation): 1.0
- **SURVIVE_FLOOR**: 0.05 (component alive iff > floor)
- **STEPS**: 1000; **MEASURE_WINDOW**: last 200 steps (steady state)
- **SEED**: 0xA17C012 (= 169328658) — 초기조건 fold, provenance + load-bearing
- scope: 2 arm × 1 deterministic run (no RNG, no replication needed — byte-reproducible)

## Run Protocol

- **hexa_only**: true — `UNIVERSE/state/h012_autopoietic_2026_05_23/run_closure.hexa` (NO .py/.sh)
- **deterministic**: 순수 recurrence (X' = X + K·cat·(1 − X/CAP) − DECAY·X), seed-folded 초기조건, RNG 부재
- **LLM**: none (raw#12 strict; literature 사용자 manual annotation only)
- **runtime**: $0 mac local, wall < 1s
- **commands**: `hexa parse run_closure.hexa` → `hexa run run_closure.hexa`
- **ledger**: `result.json` — {arm rates, gap, params, criteria, verdict, seed}
- **verify**: 본 doc 의 verdict 는 hexa run stdout VERBATIM (LLM self-judge 금지, sympy 1차 증거 금지 — g5)

## Criteria

- **C1 (self-maintenance)**: H12.1 closed_rate ≥ 0.80 → PASS
- **C2 (broken collapse)**: H12.2 broken_rate ≤ 0.20 → PASS
- **C3 (closure-dependence)**: H12.3 (closed_rate − broken_rate) ≥ 0.50 → PASS (load-bearing — 인과 분리)
- **C4 (determinism)**: H12.4 재실행 byte-equal → PASS
- **verdict_rule**: **PASS** = C1 ∧ C2 ∧ C3 ∧ C4 모두 충족; 아니면 **FAIL**. C3 가 핵심 — C1 단독으로는 "관대한 parameter" 와 구분 불가, C3 (broken control 와의 gap) 이 closure-causation 을 입증.

## Falsifiers (≥5)

- **F1 (self-maintenance)**: closed_rate < 0.80 → H12.1 FALSIFIED (닫힌 cycle 이 steady state 에서 자기유지 실패).
- **F2 (broken collapse)**: broken_rate > 0.20 → H12.2 FALSIFIED (edge 절단해도 network 생존 → closure 가 self-maintenance 의 원인이 아님).
- **F3 (closure-dependence)**: (closed_rate − broken_rate) < 0.50 → H12.3 FALSIFIED (두 arm 차이 미미 → self-maintenance 는 parameter 관대함이지 operational closure 아님 — 가장 치명적 falsifier).
- **F4 (determinism)**: 재실행 시 closed_rate2 ≠ closed_rate → H12.4 FALSIFIED (비결정성 → raw#12 deterministic 위반).
- **F5 (cascade)**: broken arm 에서 절단된 C 만 죽고 A·B 는 floor 위 유지 (broken_rate 가 0 으로 안 떨어짐) → H12.5 FALSIFIED (closure 의 비-국소 cascade 부재).
- **F6 (post-hoc edit)**: pre-register-frozen 후 thresholds/model 수정 → raw#12 violation, raw#82 retraction.

## Honest Limits (raw#91 c3, ≥5)

- **L1**: 3-component 닫힌 촉매 cycle 은 실제 abiogenesis 의 극단적 단순화 — monomer pool 없음, 실제 막/구획 없음, thermodynamic coupling 없음, stochastic 화학 없음. **abstract model only, NOT chemistry.**
- **L2 (가장 중요)**: 본 toy 의 "operational closure" 는 Maturana/Varela 의 **formal organizational closure 가 아니다.** 그들의 closure 는 component 들이 자신을 생산하는 process network 의 위상학적 자기지시 (self-reference) 전체를 가리키며, "boundary 가 그 network 의 산물" 이라는 강한 조건을 포함한다. 본 모델의 "boundary" 는 단순 fractional decay term 으로 환원되어 있고, network 가 boundary 를 *생산* 하지는 않는다 — boundary 는 모델에 박혀있는 상수일 뿐. 따라서 본 PASS 는 "닫힌 생산 graph 의 단일 edge 절단이 cascade collapse 를 유발한다" 는 **약한 명제만** 지지하며, autopoiesis 의 형식적 충족을 주장하지 X.
- **L3**: production kinetics (saturating logistic K·cat·(1−X/CAP)) 는 bounded steady state 를 주도록 *선택* 된 것 — 다른 rate law (mass-action, Hill, Michaelis-Menten) 는 다른 self-maintenance rate 를 줄 수 있고, 이 선택은 화학으로 정당화되지 X.
- **L4**: SURVIVE_FLOOR=0.05 + MEASURE_WINDOW=200 은 arbitrary 측정 선택 — floor/window 변경 시 rate 가 이동할 수 있음 (단, broken arm 의 0.0 collapse 는 floor 에 robust — C 가 0 으로 수렴하므로).
- **L5**: legacy meta-circular claim ("H_X cycle 자체가 autopoietic hypothesis network") 은 본 cycle 의 측정 대상이 **아니다** — loose analogy 이며 사용자 directive 의존 lane (anima autonomous self-replication 은 별도 lane). 본 verdict 는 3-component toy 단독.
- **L6**: H_157 proto-consciousness (Φ>0) cross-link 는 lane-open — 본 cycle 에서 닫힌 cycle 의 Φ 측정 미수행 (anima Φ★ engine 통합 별도 cycle, H_003 H3.4 와 동일 deferred).
- **L7**: 단일 seed (0xA17C012) 단일 trajectory — 초기조건 sweep / multi-seed robustness 미수행. 결정론적이므로 재현성은 보장되나 초기조건 일반성은 미입증 (단, 닫힌 cycle 의 positive fixed point 는 광범위 basin 으로 수렴할 것으로 예상 — 미검증).

## Cross-Links

- **sister H**: H_003 (생명 origin — 본 H 의 parent, H3.1 5-catalyst RNA network = 본 3-component cycle 의 확장형), H_054 (symbiogenesis — autopoietic unit merge, 본 closure 의 building-block 이후), H_157 (Law 76 panpsychism — closure → Ψ=1/2 fixed-point attractor universality), H_002 (universe origin — cosmological precondition), H_018 (genesis spontaneous emergence)
- **raw**: raw#12 (deterministic ≥5 falsifier) + raw#10 (honest limits) + raw#91 (c3 candor) + raw#82 (retraction on post-hoc edit)
- **literature** (사용자 manual annotation, LLM none):
  - Maturana, Varela (1972) *De máquinas y seres vivos* — autopoiesis, organizational closure (핵심 reference)
  - Varela, Maturana, Uribe (1974) Autopoiesis: the organization of living systems
  - Gilbert (1986) Origin of life: The RNA world (H_003 lane)
  - Prigogine (1977) Self-organization in non-equilibrium systems (dissipative — H_003 H3.3 lane)
  - Kauffman (1986) Autocatalytic sets of proteins (닫힌 촉매 set 의 자기생산 — 본 toy 의 직접 선행)
- **anima legacy archive**: `docs/hypotheses/H-CX-533-autopoietic-network.md` (legacy pointer 원본), `docs/modules/mitosis.md` + `docs/modules/growth_engine.md` (cell metaphor)
- **roadmap**: `.roadmap.hypothesis` H2 cell metaphor + `.roadmap.philosophy` D3 emerge paradigm
- **own**: (anima-not-biological identity; autopoiesis principle 은 cell metaphor analogy lane 으로만 적용)
- **state**: `UNIVERSE/state/h012_autopoietic_2026_05_23/{run_closure.hexa, result.json}`

## Verdict

raw#12 pre-register-frozen smoke — operational-closure minimal instance, $0 mac local hexa-only deterministic. `hexa run UNIVERSE/state/h012_autopoietic_2026_05_23/run_closure.hexa` stdout VERBATIM:

```
H_012 autopoietic network — operational-closure minimal-instance smoke
  model: 3-component closed catalytic cycle (C->+A, A->+B, B->+C) + boundary leak
  STEPS=1000 WINDOW=200 K=0.6 DECAY=0.1 FLOOR=0.05 SEED=169328658

  [closed]  self-maintenance rate (last 200 steps) = 1.0
  [broken]  self-maintenance rate (last 200 steps) = 0.0

  C1 closed_rate >= 0.8          : true
  C2 broken_rate <= 0.2          : true
  C3 closure-dependence gap >= 0.5 : true  (gap=1.0)
  C4 determinism (re-run byte-equal)        : true

=== H_012 VERDICT: PASS ===
  ledger -> UNIVERSE/state/h012_autopoietic_2026_05_23/result.json
```

```
verdict_class: PASS
evidence_summary: closed catalytic cycle self-maintains @ 1.0 (≥0.80);
                  broken-closure control (cut B->+C) collapses @ 0.0 (≤0.20);
                  closure-dependence gap = 1.0 (≥0.50, load-bearing — self-maintenance
                  CAUSED BY operational closure, not parameter generosity);
                  determinism byte-equal on re-run.
criteria_met: 4/4 (C1 + C2 + C3 + C4 PASS)
falsifiers_triggered: none (F1 NOT_TRIGGERED, F2 NOT_TRIGGERED, F3 NOT_TRIGGERED,
                      F4 NOT_TRIGGERED, F5 NOT_TRIGGERED via broken_rate=0.0 full
                      cascade collapse, F6 NOT_TRIGGERED)
honest_carve_out: PASS supports the WEAK claim (single cut edge → cascade collapse of
                  a closed production graph) ONLY; NOT Maturana/Varela formal
                  organizational closure (boundary is a constant decay term, not a
                  network product — see L2). abstract toy model, not chemistry.
sibling: H_003 H3.1 (5-catalyst RNA network, rate 1.0 + broken control) — same
         closure-dependence result at a larger scale; H_012 is the minimal instance.
```

### Phase 1 Verification (2026-05-23, raw#12 freeze)

```
phase: raw#12_pre_register_frozen (operational-closure minimal instance)
cell_scope: 3-component closed catalytic cycle × 1000 steps × 2 arms (closed + broken-closure control)
H12.1_closed_self_maintenance_rate: 1.0   (target ≥0.80; PASS)
H12.2_broken_closure_control_rate:  0.0   (target ≤0.20; PASS — full cascade collapse)
H12.3_closure_dependence_gap:       1.0   (target ≥0.50; PASS — load-bearing causation)
H12.4_determinism:                  byte-equal re-run (PASS)
verdict_class: PASS
evidence_strength: SUPPORTS_WEAK_CLAIM (cascade collapse on single-edge cut; NOT formal autopoiesis — L2)
criteria_pass: 4/4 (C1 + C2 + C3 + C4)
falsifiers: F1..F6 NOT_TRIGGERED
seed: 0xA17C012 (169328658)
```

**State output**: `UNIVERSE/state/h012_autopoietic_2026_05_23/result.json`
**Smoke**: `UNIVERSE/state/h012_autopoietic_2026_05_23/run_closure.hexa` (hexa-only, $0 mac local)
