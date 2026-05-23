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
