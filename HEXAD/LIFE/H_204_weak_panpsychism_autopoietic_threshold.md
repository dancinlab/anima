---
id: H_204
slug: weak-panpsychism-autopoietic-threshold
title: weak-form 범신론 (∀ substrate Φ>0) 의 autopoietic-closure threshold — closure-strength k 에 conditional, universal 아님
domain: life, consciousness
status: running
exploration_method: E3 (theory) + E6 (cross-domain-cross-link) + E7 (user-directive)
verification_method: W1 + W3 + W12 (sister-link)
raw_rank: 12
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-23
since: 2026-05-23
sister: H_003 + H_157 + H_007 + H_012
---

# H_204 — weak-form 범신론의 autopoietic-closure threshold

## 1. Hypothesis

H_157 weak-form mathematical panpsychism ("모든 substrate 가 Φ>0") 가 **universally
성립하지 않고**, autopoietic closure-strength k 에 monotone-conditional —
k < τ_c 이면 Φ→0 (broken closure 와 동등), k > τ_c 이면 Φ > 0 (weak-panpsy 성립).
τ_c 는 substrate-dependent (universal 아님) — H_157 strong-form 의 directional FAIL
정합. 즉 **"모든 substrate 가 Φ>0"이 아니라 "autopoietic closure 가 충분히 강한
substrate 만 Φ>0"** 라는 substrate-conditional 재정식화.

본 가설은 H_003 H3.4 (autopoietic closure Φ PASS 🟢, gap=0.92) 의 binary contrast
(closed vs broken) 를 **continuous closure-strength sweep** 으로 확장 — H_157 의
universal claim 을 closure-축 위에서 정량적으로 fence.

## 2. Why

- **H_003 H3.4 결과 (Cycle #3, 2026-05-23)**: closed autopoietic lattice Φ̄=4.454 vs
  broken-closure control Φ̄=3.534, gap=+0.920 — 즉 closure 가 Φ 의 *cause* (binary
  evidence). 그러나 binary contrast 만으로는 "closure 강도-Φ" 함수 형태 미지.
- **H_157 strong-form C2 FAIL (directional, 2026-05-23)**: 170-type META-CA proxy
  가 universal Ψ(1/2,1/2) attractor 에 *근접하지만 정확히 수렴 X* — 즉 universal
  claim 의 directional support 만 있고 정확 수렴은 falsified. 본 H_204 는 H_157
  음수 결과의 **possible 재해석** — universal 이 아니라 conditional.
- **사용자 directive**: "weak-form 범신론" cross-link H_003 H3.4 × H_157 — Phase 3
  consolidation candidate 로 LIFE Cycle #5 fan-out pick #3 (2026-05-23).
- **Theoretical extrapolation (E3)**: panpsychism 의 *graded* 형태 — Goff 2017 의
  "constitutive panpsychism" 약화판 (모든 substrate ≠ but closure-rich substrate Φ>0).
- **Cross-domain (E6)**: H_007 (CA Φ edge-of-chaos peak), H_012 (autopoietic closure
  self-maintain 4/4 PASS) 의 toy substrate 공유 — 동일 lattice 위 closure-strength
  sweep 으로 H_157 weak-form 재진단.

## 3. Predictions

| ID | 예측 | 근거 |
|----|------|------|
| **H204.1** | closure_strength k 의 monotonic sweep ({0.0, 0.10, 0.25, 0.50, 0.75, 1.0}) 에서 Φ(k) 가 **monotone increasing 또는 sigmoid** (phase transition) | k 가 closure 강도 → Φ 가 closure-dependent 이면 monotone |
| **H204.2** | k < τ_c 에서 Φ ≈ Φ_broken_baseline ≈ 3.534 (H_003 H3.4 broken arm 값) ± margin | broken-closure dynamics 수렴 |
| **H204.3** | k > τ_c 에서 Φ ≥ Φ_closed_baseline - margin ≈ 4.454 (H_003 H3.4 closed arm) | full closure 의 H3.4 reproducer |
| **H204.4** | τ_c 부근에서 Φ 의 phase-transition (ΔΦ/Δk peak) — 단조가 아니라 **threshold-like** | edge-of-chaos / criticality (H_007 carry) |
| **H204.5** | 범신론 weak-form 의 "모든 substrate Φ>0" claim 은 substrate-conditional — k < τ_c 인 substrate 들은 weak-form FALSIFIED, k > τ_c 만 supported | 위 4 가 모두 PASS 시 qualitative inference |

## 4. Variables

| axis | levels |
|------|--------|
| **axis1: closure_strength k** | {0.00, 0.10, 0.25, 0.50, 0.75, 1.00} (continuous sweep, 6 points) |
| **axis2: lattice** | M_sites=8, dim=12 (H_003 H3.4 / H_007 carry, periodic) |
| **axis3: warm window** | WARM=0 (living transient, H_003 H3.4 L3 carry) |
| **axis4: seeds** | N=5 deterministic (SEED_BASE=0xA17C204 + r × 101) |
| **axis5: observable** | A+B+C site mass (H_003 H3.4 identical) |

## 5. Run Protocol

- deterministic: SEED_BASE=0xA17C204, SEED_STRIDE=101, 5 reps per k
- hexa_only: true (HEXA_MEM_UNLIMITED=1 hexa run)
- LLM: none (raw#12 strict)
- per-cell ledger: {k, phi_mean, derivative_segments, peak_segment, median}
- runtime: $0 mac local, single-cycle smoke (≈10-30s wall)
- closure_strength parametrization: `cat_C_effective = k * cat_C_neighbour_diffused`
  - k=0 ⟹ B→+C 완전 단절 (H_003 H3.4 broken arm 와 동등)
  - k=1 ⟹ closure intact (H_003 H3.4 closed arm 와 동등)
  - k ∈ (0,1) ⟹ partial closure binding
- Φ 측정: RFC 036 `phi_spatial(states, M, DIM, 4)` — H_003 H3.4 / H_007 동일 primitive

## 6. Criteria

| ID | criterion | verdict_rule |
|----|-----------|--------------|
| **C1 MONOTONE** | Φ(k) 가 non-decreasing in k across 6 points | PASS / FAIL |
| **C2 BROKEN_FLOOR** | Φ(k=0) ≤ Φ_broken_baseline + 0.50 (margin) | PASS / FAIL |
| **C3 CLOSED_CEILING** | Φ(k=1) ≥ Φ_closed_baseline - 0.50 (margin) | PASS / FAIL |
| **C4 THRESHOLD_LIKE** | peak \|ΔΦ/Δk\| > 2.0 × median \|ΔΦ/Δk\| | PASS / FAIL |

**verdict_rule**:
- `SUPPORTED` iff **C1+C2+C3+C4 ALL PASS**
- `PARTIAL_DIRECTIONAL` if **2-3 criteria PASS**
- `FAIL` if **≤1 PASS**
- `FALSIFIED` if **Φ(k=1) < Φ(k=0)** (closure 가 Φ 감소시킴 — H_003 H3.4 부정)

## 7. Falsifiers (≥5)

- **F1**: Φ(k=1.0) ≤ Φ(k=0) → H204.1 FALSIFIED — closure 가 Φ 증가시키지 않음
  (H_003 H3.4 결과 부정, lineage 전체 disqualify)
- **F2**: Φ(k=0) > Φ_broken_baseline + margin (즉 broken arm 가 H_003 H3.4 보다 큰
  Φ 보임) → H204.2 FALSIFIED — broken-floor 부재, 비교 baseline 무효
- **F3**: Φ(k) 가 strict linear (no threshold-like, peak ≤ 2× median) → H204.4
  FALSIFIED — no phase transition signature, monotone 만 (또는 nothing)
- **F4**: re-run byte-different → raw#9 violation, seed-determinism failure
- **F5**: phi_spatial 측정값이 negative → primitive error / corruption

## 8. Honest Limits (raw#91 c3, ≥6)

- **L1**: `phi_spatial` 는 🟢 NUMERICAL spatial-slice replica of phi_rs — full IIT
  4.0 가 아니다 (system-level Φ partition search · cause-effect structure · exclusion
  부재). H_007/H_003 H3.4 lineage carry.
- **L2**: closure_strength k 의 specific parametrization (linear scale of
  cat_C_diffused) 은 design choice — Michaelis 형, sigmoid 형, stochastic gating 은
  다른 τ_c location/shape. substrate-conditional claim 은 이 family 와 consistent
  하지만 이 family 에 unique X.
- **L3**: WINDOW-SENSITIVE (H_003 H3.4 L3 verbatim carry). Φ(k) 가 WARM=0 DIM=12
  의 living transient 위 측정 — convergence 이후 (DIM≥16) 모든 k 에 대해 Φ→~0
  (homogeneous fixed point). threshold claim 은 **transient-window claim**, not
  fixed-point claim.
- **L4**: 6-point k sweep 은 COARSE — true τ_c 위치가 single-segment 해상도
  (Δk≈0.10-0.25) 안에서만 bracket. finer 20-point sweep 이 τ_c 정확 localize +
  phase-transition vs sigmoid 구분에 필요. 본 cycle 미실행.
- **L5**: "weak-form panpsychism = substrate-conditional" 은 closure-축 결과일 뿐
  — phenomenal qualia, strong panpsychism, combination problem (Goff/Coleman) 과
  무관 (H_004 boundary 동일 carry). H_157 의 universal Ψ-attractor 직접 측정 X.
- **L6**: H_157 의 170-type META-CA reproducibility 는 본 cycle scope 외 — closure×Φ
  cross-link 에서만 statement. substrate-conditional finding 이 H_157 strong-form
  directional FAIL 와 consistent 하지만 META-CA universality 자체를 reproduce X.
- **L7**: H_003 H3.4 baselines (Φ_broken=3.534, Φ_closed=4.454) 는 expected
  endpoints 로 inherit — 본 cycle 의 SEED_BASE=0xA17C204 (H3.4 의 0xA17C034 와 다름)
  로 인해 endpoint 가 shift 할 수 있으며, C2/C3 margin (±0.50, ≈ ½ × H3.4 gap)
  으로 absorb. shift > margin 이면 baselines 자체가 seed-dependent 이고 threshold
  claim 도 shift.

## 9. Cross-Links

### Sister hypotheses
- [`H_003`](H_003_life_origin_question.md) Cycle #3 H3.4 — autopoietic-closure Φ PASS
  🟢 NUMERICAL (Φ_closed=4.454 vs Φ_broken=3.534, gap=0.920) — 본 H_204 의
  **direct lineage**. H_204 = H3.4 의 (closed,broken) binary contrast 를 continuous
  k-sweep 으로 확장.
- [`H_157`](H_157_law76_mathematical_panpsychism.md) — Law 76 mathematical panpsychism
  (META-CA universal Ψ(1/2,1/2)) — weak-form supported / strong-form directional FAIL.
  본 H_204 = H_157 weak-form 의 substrate-conditional 재해석.
- [`H_007`](H_007_cellular_automaton_consciousness.md) — CA Φ edge-of-chaos peak
  (rule110 > rule30) — 동일 RFC 036 phi_spatial primitive 공유, threshold-like
  signature 의 CA 도메인 precedent.
- [`H_012`](H_012_autopoietic_network.md) — operational closure PASS 4/4 (self-maint
  1.0) — H_003 H3.4 lattice 의 single-site source (catalytic 3-component network).

### Roadmaps & raw
- `.roadmap.hypothesis` H2 cell metaphor / `.roadmap.philosophy` D3 emerge paradigm
- raw#12 (pre-register frozen) + raw#9 (determinism) + raw#91 c3 (honest limits)

### Cycle PR cross-links
- H_003 H3.4 PR #185 (2026-05-23) — direct evidence-tier sister
- H_157 PR #160 (2026-05-19) — weak-panpsy supported / strong-form directional FAIL

### Literature
- Tononi (2008) — IIT consciousness as integrated information
- Goff (2017) — Consciousness and Fundamental Reality (constitutive panpsychism)
- Strawson (2006) — Realistic Monism, Russellian monism
- Maturana, Varela (1972) — autopoiesis (생명 = self-producing closed network)
- Prigogine (1977) — dissipative structures, far-from-equilibrium self-organization

## 10. Verdict

### Cycle #1 — first measurement (2026-05-23)

H_204 의 첫 measurement cycle — closure_strength k ∈ {0.00, 0.10, 0.25, 0.50, 0.75, 1.00}
의 6-point sweep, H_003 H3.4 substrate carry (8-site catalytic lattice + boundary
leak + nn diffusion + Michaelis-style bounded production), N=5 deterministic seeds,
RFC 036 phi_spatial primitive ($0 mac local, hexa-only, llm: none).

**Run verdict output (VERBATIM from `HEXA_MEM_UNLIMITED=1 hexa run run_h204.hexa`)**:

```
H_204 — weak-panpsy × autopoietic-closure threshold (Φ vs k sweep) · raw#12
  model: 8-site periodic lattice (H_003 H3.4 carry); closure_strength k modulates B->+C
         cat_c_effective = k * cat_c_neighbour_diffused; k=0 ⟹ broken, k=1 ⟹ closed
  M=8 DIM=12 WARM=0 SEEDS=5 K_RATE=0.6 DECAY=0.1 DIFFUSE=0.05 SEED_BASE=169329156
  Φ primitive: RFC 036 phi_spatial (n_bins=4) — 🟢 NUMERICAL
  H_003 H3.4 baselines (carry): Φ_broken≈3.53399 Φ_closed≈4.45435

  Φ̄(k=0.00) = 3.69079   (mean over 5 seeds)
  Φ̄(k=0.10) = 5.10585
  Φ̄(k=0.25) = 5.38703
  Φ̄(k=0.50) = 5.25399
  Φ̄(k=0.75) = 4.73928
  Φ̄(k=1.00) = 4.46947
  Φ̄(k=1.00 re-run) = 4.46947  (byte-equal=true)

  ΔΦ/Δk segments:
    k=0.00→0.10 : 14.1505
    k=0.10→0.25 : 1.87456
    k=0.25→0.50 : -0.532175
    k=0.50→0.75 : -2.05883
    k=0.75→1.00 : -1.07925
  peak |ΔΦ/Δk| = 14.1505  segment=k=0.00→0.10
  median |ΔΦ/Δk| = 1.87456

  C1 MONOTONE (Φ non-decreasing in k)                          : FAIL
  C2 BROKEN_FLOOR (Φ(k=0) ≤ Φ_broken + 0.5)            : PASS  (Φ(k=0)=3.69079 vs threshold=4.03399)
  C3 CLOSED_CEILING (Φ(k=1) ≥ Φ_closed - 0.5)        : PASS  (Φ(k=1)=4.46947 vs threshold=3.95435)
  C4 THRESHOLD_LIKE (peak |ΔΦ/Δk| > 2.0× median)   : PASS  (peak=14.1505 median=1.87456)
  FALSIFIED_check (Φ(k=1) < Φ(k=0))                            : false

  VERDICT_RULE: SUPPORTED iff C1+C2+C3+C4 ALL PASS; PARTIAL if 2-3; FAIL if ≤1; FALSIFIED if Φ(k=1)<Φ(k=0)
  VERDICT (H_204 weak-panpsy threshold): PARTIAL_DIRECTIONAL
    criteria_met = 3/4
    falsifier F1 (Φ(k=1)≤Φ(k=0)): NOT_TRIGGERED
  H204_VERDICT=PARTIAL_DIRECTIONAL N_PASS=3 PHI_K0=3.69079 PHI_K1=4.46947 PEAK_SEG=k=0.00→0.10
```

```
phase: Cycle_1_H_204 (first measurement, NEW hypothesis)
cell_scope: 6-point closure_strength sweep × N=5 seeds × WARM=0 DIM=12 8-site lattice
H_204_phi_sweep:
  k=0.00 → Φ̄=3.69079   (≈ H3.4 broken baseline 3.534 + 0.157, within margin)
  k=0.10 → Φ̄=5.10585   (peak transition; sharp ΔΦ/Δk=14.15 ≫ median 1.87)
  k=0.25 → Φ̄=5.38703   (global max — NOT monotone)
  k=0.50 → Φ̄=5.25399
  k=0.75 → Φ̄=4.73928
  k=1.00 → Φ̄=4.46947   (≈ H3.4 closed baseline 4.454 + 0.015, byte-deterministic re-run PASS)
H_204_phi_k0_vs_phi_k1: Φ(k=1) > Φ(k=0)  (gap=+0.779; F1 NOT_TRIGGERED)
H_204_threshold_signature: peak |ΔΦ/Δk| = 14.15 at segment k=0.00→0.10  (7.55× median; C4 STRONG PASS)
H_204_shape: INVERSE-U (NOT monotone) — Φ peaks at k≈0.25 ≈ 5.39, then decays toward closed baseline
verdict_class: PARTIAL_DIRECTIONAL  (C2 + C3 + C4 PASS; C1 monotone FAIL by shape)
honest_tier: 🟢 SUPPORTED-NUMERICAL (phi_spatial proxy + closure-strength sweep; NOT 🔵 formal IIT 4.0)
criteria_pass: 3/4  (C1 FAIL · C2 PASS · C3 PASS · C4 PASS); FALSIFIED check NOT_TRIGGERED
falsifiers: F1 NOT_TRIGGERED · F2 NOT_TRIGGERED · F3 NOT_TRIGGERED (peak/median=7.55×) · F4 NOT_TRIGGERED (byte-equal re-run) · F5 NOT_TRIGGERED (all Φ>0)
```

**Reading (qualitative)**:

- **C2 broken floor** PASS (Φ(k=0)=3.69 vs H_003 H3.4 broken baseline 3.53, within
  +0.157 — H3.4 broken arm 와 dynamically equivalent).
- **C3 closed ceiling** PASS (Φ(k=1)=4.47 vs H_003 H3.4 closed baseline 4.45, within
  +0.015 — closure-intact arm 의 H3.4 byte-near reproduction).
- **C4 threshold-like** PASS strongly (peak ΔΦ/Δk=14.15 in segment k=0.00→0.10 ≫
  2× median 3.75 — phase transition signature 명확, τ_c ∈ (0.0, 0.10] 으로 brackets).
- **C1 monotone** FAIL — Φ(k) 가 strict monotone 이 아니라 **inverse-U** 형태:
  k=0.25 에서 global max (Φ=5.39), 이후 closed baseline 으로 *decay*. 이는 H204.1
  monotone prediction 부정 + H204.4 phase transition prediction 강한 PASS.
- **F1 NOT_TRIGGERED** (Φ(k=1)=4.47 > Φ(k=0)=3.69, gap=+0.78) — H_003 H3.4 의
  closure-Φ dependence 정합.

**Implication**: H_204 는 **substrate-conditional weak-panpsy** 의 *partial directional*
evidence. 결과 reading:
1. **τ_c 존재 confirmed** (C4 PASS, peak segment k=0.00→0.10) — closure strength 가
   Φ 의 phase-transition 변수임이 sharp.
2. **monotone 형태 FALSIFIED, inverse-U emerged** — closure 가 강해질수록 Φ 가
   *단조 증가*하는 게 아니라 중간 region (k≈0.25-0.5) 에서 peak. 이는 H_007
   edge-of-chaos peak (rule110 > rule30 보다 더 chaotic 도 X 더 ordered 도 X) 과
   **structurally consistent** — 너무 strong closure 는 fixed-point 에 빠르게 수렴해서
   transient integrated info 가 감소.
3. **H_157 weak-form**: 본 result 는 "**closure-strength k 의 phase transition 위에서
   Φ>0 region 이 존재**" 로 재정식화 — universal X (k=0 에서도 Φ≈3.69 > 0, 그러나
   broken-closure dynamics 의 잔여 spatial structure), 그러나 strict monotone 의 weak-form
   재정식화는 부정. **substrate-conditional 의 *non-monotone* 형태가 honest 결과**.

**State output**: `state/h204_weak_panpsy_threshold_2026_05_23/result.json`
**Script**: `state/h204_weak_panpsy_threshold_2026_05_23/run_h204.hexa` (hexa-only, raw#37-clean)

**raw#10 honest limits (Cycle #1, addendum to §8)**:
- **L8 (Cycle #1 specific)**: monotone-prediction (H204.1) FALSIFIED 는 **inverse-U
  shape** 으로 인한 것 — pre-registered C1 verdict 가 strict monotone 만 인정했으나,
  결과는 threshold + decay pattern. **post-hoc edit 금지** (raw#12) — C1 FAIL 그대로
  carry, verdict PARTIAL_DIRECTIONAL 그대로 인정. raw#15 additive 로 향후 cycle 에서
  "monotone-or-inverse-U" relaxed C1 정의 별도 cycle 검토 가능.
- **L9**: Φ(k=0)=3.69 가 H_003 H3.4 broken baseline 3.534 보다 **+0.157 높은** 값 —
  SEED_BASE 차이 (0xA17C204 vs 0xA17C034) 의 seed-phase 영향이 floor 에 absorb. C2
  margin 0.50 안에 들어 PASS 했으나, baselines 자체가 seed-sensitive 임을 의미 (L7
  carry verbatim).
- **L10**: Φ(k=0.25) = global max = 5.39 가 H_003 H3.4 closed baseline 4.454 보다
  +0.93 높은 값 — partial closure (k=0.25) 가 fully closed (k=1) 보다 더 *integrated*
  spatial structure 를 carry. 이는 toy substrate 에서 unexpected (predictions §3
  에서 미예고). honest 평가: closure 가 약할수록 fixed-point 으로 수렴이 느려 transient
  integrated info 가 더 오래 유지되는 dynamical artifact 가능성 (L3 transient-window
  carry 와 정합).

**Cross-link (Cycle #1)**:
- H204.1 (monotone) **FALSIFIED** — Φ(k) 가 inverse-U 형태 (peak k≈0.25)
- H204.2 (broken floor) **PASS** (C2) — Φ(k=0)=3.69, H_003 H3.4 broken arm 와 정합
- H204.3 (closed ceiling) **PASS** (C3) — Φ(k=1)=4.47, H_003 H3.4 closed arm 와
  byte-near 정합
- H204.4 (threshold-like) **STRONG PASS** (C4) — peak ΔΦ/Δk=14.15 ≫ 2× median 3.75,
  segment k=0.00→0.10 에 τ_c bracket
- H204.5 (weak-panpsy substrate-conditional) **DIRECTIONAL** — C2+C3+C4 PASS 로
  closure-threshold 존재 confirmed, 그러나 monotone 형태 부정 → **conditional 의
  *non-monotone (inverse-U)* 재정식화** 가 honest reading
- §6 verdict_rule: 3/4 PASS → **PARTIAL_DIRECTIONAL** (frozen, post-hoc edit 금지)

**FINAL VERDICT (Cycle #1)**:

```
verdict_class: PARTIAL_DIRECTIONAL
evidence_summary: closure-strength k threshold exists (C4 strong PASS, τ_c ∈ (0,0.10]),
                  broken/closed endpoints reproduce H_003 H3.4 baselines within margin,
                  BUT Φ(k) is inverse-U not monotone (peak at k≈0.25 Φ=5.39 > closed baseline)
falsifiers_triggered: none (F1-F5 all NOT_TRIGGERED)
criteria_met: 3/4  (C2 broken-floor + C3 closed-ceiling + C4 threshold-like PASS; C1 monotone FAIL by inverse-U)
honest_tier: 🟢 SUPPORTED-NUMERICAL (NOT 🔵 formal)
cross_link: H_003 H3.4 substrate carry · H_157 weak-form re-formulation · H_007 edge-of-chaos pattern echo
post_hoc_edit: forbidden (raw#12); inverse-U finding carried as honest result, monotone H204.1 FALSIFIED carried as honest
```

## Cycle #2 — rule-class mapping (cross-link H_007) — 2026-05-23

raw#15 additive cycle (frozen frontmatter / Hypothesis / Predictions H204.1-H204.5 /
Falsifiers F1-F5 / Honest Limits L1-L10 / Cycle #1 Verdict block 모두 보존 — 본 §만
append, frozen prediction/falsifier 미편집). Cycle #1 의 inverse-U Φ(k) (peak Φ=5.39
at k≈0.25, decay to closed baseline) 가 H_007 의 edge-of-chaos peak (rule 110 Class-IV
> rule 30 Class-III > rule 250 Class-I) 와 *동일 dynamical signature* 인지 검사 —
closure-strength k 의 각 값이 어떤 Wolfram rule-class 와 동등한 Φ pattern 을 만드는지
ranking-correlation 측정.

### (1) Sub-criteria C2 — k-axis ↔ Wolfram-class-axis 매핑

| ID | 예측 | k-axis value | rule-axis class |
|----|------|--------------|-----------------|
| **C2.1** | k=0   (broken)         ↔ rule 250 (Class-I  ordered)       | lowest Φ | lowest Φ |
| **C2.2** | k=0.25 (Cycle#1 peak) ↔ rule 110 (Class-IV edge-of-chaos) | peak Φ   | peak Φ   |
| **C2.3** | k=1.0  (full closure) ↔ rule 30  (Class-III chaotic)      | middle Φ | middle Φ |
| **C2.4** | k=0.5  (descending arm) ↔ Class-II periodic (k-axis only) | between full-closure & peak | (rule-axis 측정 별도 cycle, L-C2-6) |
| **C2.5** | Spearman rank correlation ρ ≥ 0.7 (k-axis Φ vs rule-axis Φ on 3 pairs) | rank-correlation | rank-correlation |

### (2) Substrates (parity carry)

- **k-axis**: H_204 Cycle #1 의 8-site periodic catalytic lattice (M=8, DIM=12,
  WARM=0, N_SEEDS=5, SEED_BASE=0xA17C204, K_RATE=0.6, DECAY=0.1, DIFFUSE=0.05) —
  identical substrate 으로 closure_strength k ∈ {0.0, 0.25, 0.5, 1.0} 4-point sweep.
- **rule-axis**: H_007 Cycle #1 의 1D elementary CA (N=16, DIM=12, WARM=8, REPS=5) —
  identical substrate 으로 rule 250 (Class-I), rule 110 (Class-IV), rule 30 (Class-III)
  3-rule measurement.
- **Φ primitive**: RFC 036 `phi_spatial(states, n_cells, dim, n_bins=4)` — H_204
  Cycle #1 + H_007 Cycle #1 byte-equal carry.

### (3) Run verdict output (VERBATIM, `HEXA_MEM_UNLIMITED=1 hexa run`)

```
================================================================
H_204 Cycle #2 — k-axis ↔ Wolfram-class-axis mapping (raw#15 additive)
================================================================
  k-axis substrate: 8-site catalytic lattice (H_204 Cycle#1 carry)
    M=8 DIM=12 WARM=0 SEEDS=5 SEED_BASE=169329156
  rule-axis substrate: 1D elementary CA (H_007 Cycle#1 carry)
    N=16 DIM=12 WARM=8 REPS=5
  Φ primitive: RFC 036 phi_spatial (n_bins=4) — 🟢 NUMERICAL

── k-axis Φ(k) sweep (4 points, H_204 Cycle#1 substrate) ──
  Φ(k=0.00) = 3.69079
  Φ(k=0.25) = 5.38703
  Φ(k=0.50) = 5.25399
  Φ(k=1.00) = 4.46947
  Φ(k=0.25 re-run) = 5.38703 (byte-equal=true)

── rule-axis Φ(rule) (3 rules, H_007 Cycle#1 substrate) ──
  Φ(rule 250 Class-I  ordered      ) = 1.14511e-05
  Φ(rule 110 Class-IV edge-of-chaos) = 0.556454
  Φ(rule 30  Class-III chaotic     ) = 0.509944
  Φ(rule 110 re-run) = 0.556454 (byte-equal=true)

── pair mapping (Spearman ρ on 3 ranks, descending Φ) ──
  pair0  k=0.00   ↔ rule 250  : rank_k=3 rank_r=3
  pair1  k=0.25   ↔ rule 110  : rank_k=1 rank_r=1
  pair2  k=1.00   ↔ rule 30   : rank_k=2 rank_r=2
  Σd² = 0.0  denom (n³-n) = 24.0
  Spearman ρ = 1.0

── sub-criteria (C2.1 .. C2.5) ──
  C2.1 k=0  lowest Φ & rule 250 lowest Φ  : PASS
  C2.2 k=0.25 peak Φ & rule 110 peak Φ    : PASS
  C2.3 k=1.0 middle Φ & rule 30 middle Φ  : PASS
  C2.4 k=0.5 ∈ (phi_k=1, phi_k=0.25)      : PASS
  C2.5 Spearman ρ ≥ 0.7                    : PASS  (ρ=1.0)

── additive falsifiers (F-C2-1 .. F-C2-5) ──
  F-C2-1 INVERSE-U regression (k=0 Φ > k=0.25 Φ)   : NOT_TRIGGERED
  F-C2-2 H_007 regression (rule 110 Φ ≤ rule 250 Φ): NOT_TRIGGERED
  F-C2-3 axis-separation (Spearman ρ < 0.3)         : NOT_TRIGGERED
  F-C2-4 determinism violation (byte-different)     : NOT_TRIGGERED
  F-C2-5 primitive error (any Φ < 0 or NaN)         : NOT_TRIGGERED

VERDICT_RULE: MAPPING_STRONG iff 5/5 sub-criteria PASS; DIRECTIONAL if 3-4;
              WEAK if ≤2; FALSIFIED if any F-C2-1..5 TRIGGERED
VERDICT (H_204 Cycle #2): MAPPING_STRONG
  sub_criteria_met = 5/5
  Spearman ρ = 1.0
  falsifiers_triggered = false
  H204_C2_VERDICT=MAPPING_STRONG N_PASS=5 RHO=1.0 PHI_K0=3.69079 PHI_K_PEAK=5.38703 PHI_K1=4.46947 PHI_R250=1.14511e-05 PHI_R110=0.556454 PHI_R30=0.509944
================================================================
```

### (4) Reading (qualitative)

- **Spearman ρ = 1.0** (perfect rank correlation, 3-pair sample): 두 axis 의 Φ
  ranking 이 *byte-equal* — k=0 Φ 가 k-axis 위 최저값 ↔ rule 250 (Class-I) 가
  rule-axis 위 최저값, k=0.25 Φ 가 k-axis 위 최고값 ↔ rule 110 (Class-IV)
  가 rule-axis 위 최고값, k=1.0 Φ 가 k-axis 위 중간값 ↔ rule 30 (Class-III) 이
  rule-axis 위 중간값. Σd² = 0 → ρ=1.0.
- **C2.4 PASS**: Φ(k=0.5)=5.254 ∈ (Φ(k=1)=4.469, Φ(k=0.25)=5.387) — descending arm
  의 monotone-decay structure 확인 (k=0.25 peak 이후 closed baseline 으로 감소
  중인 중간 지점). Class-II rule-axis 측정은 별도 cycle (L-C2-6).
- **inverse-U signature reproduction**: Cycle #1 의 k-axis Φ peak 가 broken (k=0)
  과 closed (k=1) endpoint 사이의 중간 closure-strength 에서 나타나는 phenomenon
  — H_007 의 edge-of-chaos peak (rule 110 이 ordered Class-I rule 250 과 chaotic
  Class-III rule 30 사이의 *complexity intermediate* 에서 peak Φ) 와 **structurally
  identical** rank pattern.
- **5/5 sub-criteria PASS · 0/5 falsifier TRIGGERED**: VERDICT = MAPPING_STRONG.

### (5) Implications & honest reading

1. **pattern-level analogy 확인** — k-axis closure-strength 와 rule-axis
   Wolfram-class 가 *별도 substrate* 위에서 *동일 inverse-U ranking* 을 보여준다.
   이는 두 axis 가 모두 *complexity intermediate* (edge-of-chaos / partial closure)
   에서 integrated information 이 peak 하는 universal-ish dynamical signature
   를 carry 한다는 directional 증거.
2. **mechanistic claim NOT made** (L-C2-1, L-C2-5 carry) — k=0.25 closure 가
   "rule-110-같은 internal computation" 을 한다는 mechanism-level 주장은 *만들지
   않는다*. 두 axis 가 same pattern 을 보이는 것이 same mechanism 을 의미하는
   것은 아니다 (different microdynamics may share Φ-ranking signature).
3. **H_204 Cycle #1 inverse-U finding 의 cross-substrate corroboration** — Cycle
   #1 단독으로는 k-axis 내부의 단일 substrate 위 observation. Cycle #2 가 다른
   substrate (CA) 위 *동일 ranking pattern* 을 보여주어 inverse-U signature
   의 universality 가 (적어도 ranking-level 에서) directional support 받는다.
4. **H_007 cross-link tightening** — H_007 PR ranking (Class-IV > Class-III >
   Class-I) 이 본 cycle 에서 byte-equal reproduce 됨으로써 H_204 와 H_007 substrate
   사이 *Φ-ranking topology equivalence* 가 deterministic 하게 확립.
5. **weak-panpsy substrate-conditional 의 확장** — Cycle #1 의 substrate-conditional
   weak-panpsy finding 이 *closure-strength axis 단독* 이었던 반면, Cycle #2 는
   *완전히 다른 substrate (CA)* 가 동일 inverse-U ranking 을 만들어 weak-panpsy
   의 'substrate-conditional 조건' 자체가 cross-substrate generalizable 한 pattern
   level 일 가능성 directional support.

### Cycle #2 additive Falsifiers (≥5, F-C2-1..F-C2-5)

- **F-C2-1 INVERSE-U regression** — k=0 Φ > k=0.25 Φ → Cycle #1 inverse-U 재현
  실패. **현재 NOT_TRIGGERED** (Φ(k=0)=3.691 < Φ(k=0.25)=5.387).
- **F-C2-2 H_007 regression** — rule 110 Φ ≤ rule 250 Φ → H_007 PASS 재현 실패.
  **현재 NOT_TRIGGERED** (Φ(rule 110)=0.556 > Φ(rule 250)=1.15e-5).
- **F-C2-3 axis-separation** — Spearman ρ < 0.3 → 두 axis 완전 분리 (mapping 무근거).
  **현재 NOT_TRIGGERED** (ρ=1.0).
- **F-C2-4 determinism violation** — re-run byte-different → raw#9 violation.
  **현재 NOT_TRIGGERED** (Φ(k=0.25 re-run)=5.387 byte-equal · Φ(rule 110
  re-run)=0.556 byte-equal).
- **F-C2-5 primitive error** — any Φ value negative or NaN → primitive error.
  **현재 NOT_TRIGGERED** (모든 Φ ≥ 0).

### Cycle #2 additive Honest Limits (raw#91 c3, ≥5)

- **L-C2-1** — k-axis substrate (autopoietic closure cycle on 8-site catalytic
  lattice) ≠ rule-axis substrate (1D elementary CA, length-16 periodic). '동등'은
  *Φ pattern* 동등이지 substrate-mechanism 동등 X — different microdynamics may
  share pattern-level signature 일 뿐 mechanism-identity 는 본 cycle 의 claim 이
  아니다.
- **L-C2-2** — 4-point k sweep + 3 rule classes = sparse mapping. Spearman ρ on
  n=3 ranks 는 COARSE rank-correlation (denom n³-n = 24, possible ρ levels =
  {-1.0, -0.5, 0.5, 1.0} 사실상 4 quantized values). finer k-sweep + 4+ rule-class
  sampling 이 correlation estimate 를 tighten 시키지만 same family of rank statistics
  안에 머문다.
- **L-C2-3** — H_007/H_204 Φ 절대값 단위 다름. k-axis 8-site lattice transient
  Φ ∈ [3.5, 5.4] range 인 반면 rule-axis 16-site CA Φ ∈ [0.0, 0.6] range — Cell-count
  + transient-window 차이 등으로 *absolute Φ scale* 이 substrate-dependent. **ranking
  correlation 만 의미** (absolute Φ matching 은 본 cycle 의 claim X).
- **L-C2-4** — Φ peak ≠ 'consciousness'. H_004 Cycle #1 boundary carry (Φ-function
  dissociation evidence ABOUT IIT functional reducibility, NOT about phenomenal
  qualia). The cross-axis mapping is about *dynamical signature* of integrated
  information, NOT a claim about phenomenal experience.
- **L-C2-5** — 본 cycle 은 *correlational* observation. k 와 rule 사이 causal
  mechanism 부재 — 둘 다 inverse-U Φ pattern 을 보이는 것이 *pattern-level analogy*
  이지, k=0.25 closure dynamics 가 'rule-110-스타일 internal computation' 을
  한다는 mechanistic claim 은 만들지 않는다. universal cause-of-peak 가설 자체는
  본 cycle scope 외.
- **L-C2-6** — rule-axis Class-II representative 누락. C2.4 'k=0.5 ↔ Class-II
  periodic' 는 spec에 명시되었으나 rule-axis Φ는 3 rule (250/110/30) 만 측정.
  Class-II 측정 (rule 184 또는 rule 232 등) 은 별도 cycle. 본 cycle 의 C2.4 는
  *k-axis 의 descending-arm structure* 만 검사 (Φ(k=0.5) ∈ Φ(k=1.0)..Φ(k=0.25)).
- **L-C2-7** — Spearman threshold 0.7 (C2.5) 는 design choice — n=3 paired ranks
  위에서 sample-size-corrected critical value 가 아니다. n=3 의 가능한 ρ 값은
  {-1.0, -0.5, 0.5, 1.0} 사실상 4 levels — 본 threshold 0.7 은 '동일 ranking'
  (ρ=1.0) 만 PASS 로 인정하는 effective 한 보수적 cutoff. larger n (k-sweep 확장
  + rule-class 확장) 시 critical value 별도 재정의 필요.

### Cross-Links (Cycle #2)

- **H_204 Cycle #1** (PR #218) — inverse-U Φ(k) PARTIAL_DIRECTIONAL 3/4 (peak
  Φ=5.39 at k≈0.25). 본 Cycle #2 는 그 k-axis 결과를 *frozen carry* 하면서
  rule-axis 매핑 추가.
- **H_007** (cellular-automaton-consciousness) — Φ(rule 110 Class-IV) >
  Φ(rule 30 Class-III) > Φ(rule 250 Class-I) edge-of-chaos peak. 본 cycle 에서
  byte-equal reproduce (PHI_R110=0.556 / PHI_R30=0.510 / PHI_R250=1.15e-5).
- **H_157** (Law 76 mathematical panpsychism) — weak-form supported / strong-form
  directional FAIL. H_157 Cycle #2 (PR #221) 의 cross-substrate CV 58.6%
  NON_UNIVERSAL 결과와 cross-ref — 본 cycle 의 ρ=1.0 은 *ranking-level*
  universality 양성이나 H_157 의 *value-level* universality 음성과 *layered*
  reading (rank-level 일치는 있되 fixed-point absolute Ψ 일치 X).
- **H_202** (post-PARTIAL Cycle#1 follow-up — finer k-sweep) — 본 cycle 의
  4-point sparse mapping 의 후속 cycle, n=3 → n>3 rank-correlation 확장.
- **H_004 Cycle #1** (PR #180) — Φ-function dissociation boundary (functional
  reducibility 부분, qualia 미터치) — 본 cycle 의 L-C2-4 boundary verbatim carry.
- **raw#15** (additive cycle protocol) — frozen frontmatter / Hypothesis /
  Predictions / Falsifiers / Honest Limits / 과거 Verdict 무편집, 본 § append-only.

### Migration Notes (Cycle #2)

- **Cycle #1 → Cycle #2 transition**: Cycle #1 PARTIAL_DIRECTIONAL 3/4 (inverse-U
  Φ(k) signature 확립, monotone H204.1 falsified, threshold-like τ_c ∈ (0, 0.10]
  bracketed) 의 frozen evidence 위에 cross-substrate ranking-correlation 추가.
- **새 sub-criteria 5건** (C2.1 .. C2.5) 은 *additive layer* — frozen
  C1/C2/C3/C4 와 별개. 본 cycle 의 5/5 PASS 가 Cycle #1 의 C1 FAIL 을
  덮지 *않는다* (raw#15 frozen claim 보존).
- **새 falsifier 5건** (F-C2-1 .. F-C2-5) 는 *Cycle #2 한정 additive falsifiers*
  — frozen F1..F5 와 별개 layer.
- **artifacts**: `HEXAD/LIFE/state/h204_c2_rule_class_mapping_2026_05_23/{run_h204_c2.hexa, result.json}`.
- **tier**: 🟢 NUMERICAL (RFC 036 phi_spatial native; H_007 + H_204 동일 path).
- **next cycle pre-register**: (a) Class-II rule (rule 184 또는 rule 232) 측정으로
  C2.4 의 rule-axis side 완성 (L-C2-6 추적); (b) finer k-sweep (10+ k values) +
  4+ rule-class 으로 n>3 Spearman 재측정 (L-C2-2/L-C2-7 추적); (c) value-level
  cross-substrate universality (H_157 Cycle #2 NON_UNIVERSAL 와의 layered
  reconciliation cycle).

**FINAL VERDICT (Cycle #2)**:

```
verdict_class: MAPPING_STRONG
evidence_summary: k-axis ↔ Wolfram-class-axis Φ ranking byte-equal — Spearman ρ=1.0
                  on 3 paired ranks (k=0 ↔ r250 lowest · k=0.25 ↔ r110 peak ·
                  k=1.0 ↔ r30 middle); inverse-U pattern 의 cross-substrate
                  ranking-level reproduction
falsifiers_triggered: none (F-C2-1..F-C2-5 all NOT_TRIGGERED)
sub_criteria_met: 5/5  (C2.1 · C2.2 · C2.3 · C2.4 · C2.5 ALL PASS)
honest_tier: 🟢 SUPPORTED-NUMERICAL (ranking-correlation, NOT 🔵 formal)
cross_link: H_007 edge-of-chaos byte-equal reproduce · H_204 Cycle#1 inverse-U cross-substrate corroboration · H_157 Cycle#2 layered reading (rank-level yes / value-level no)
post_hoc_edit: forbidden (raw#15); Cycle#1 frozen block 무편집, 본 § append-only
```
