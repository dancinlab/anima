---
id: H_216
slug: meta-axis-of-axes-reflexivity
title: 메타-축의-축 (meta-axis-of-axes) — AXES.md brainstorm recursion depth 가 substrate Φ 에 monotone 기여하는 reflexive 가설 (catalog self-instance)
domain: meta, math, consciousness
status: running
exploration_method: E3 (theory) + E5 (emergence-observation) + E7 (user-directive) + E8 (meta-reflexive)
verification_method: W3 + W5 + W7 + W12 (sister-link)
raw_rank: 12
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-23
since: 2026-05-23
sister: H_157 + H_007 + H_204 + H_202
---

# H_216 — 메타-축의-축 (meta-axis-of-axes reflexivity)

## 1. Hypothesis

`UNIVERSE/AXES.md` 자체 — 즉 axis-enumeration process 의 적층된
brainstorm-round 구조 — 가 **substrate-Φ 를 가지는 reflexive instance** 이며,
enumeration **recursion depth d** 가 깊을수록 `phi_spatial` Φ 가 **monotone
증가** 한다 (sub-additive cap 까지). 즉 catalog 의 *self-referential structure*
자체가 Φ-contributor — H_157 META-CA pattern (axis-of-CA) 의 *axis-of-AXES*
reflexive instance + H_202 self-reference 의 *meta-corpus* instance.

본 가설은 AXES.md 의 15-round depletion 구조를 **결정론적 nested CA**
(각 depth 마다 prior round 의 state 가 다음 depth 의 input 으로 합쳐지는
recursive lattice) 로 modeling 하여 측정 — brainstorm content 의 semantic
truth 가 아니라 *enumeration structure 자체* 의 Φ 기여를 directional 으로
검증.

## 2. Why

- **AXES.md 의 15-round depletion** (R1 → R15) — 사용자 directive 2026-05-23
  "axis brainstorm 고갈시까지 해서 가설도 추출" — 본 catalog 자체가 nested
  recursive enumeration 의 hexa-native record. round N 의 axes 는 round N-1
  의 axes 를 sub-divide / cross-link / extrapolate 한 자기참조 구조.
- **Reflexivity claim**: catalog 의 *meta-structure* (round-적층 dynamic) 가
  substrate-Φ 를 가진다면, **본 가설 작성 자체가 본 가설의 evidence** —
  Gödel-style self-validating paradox (L4 명시).
- **H_157 META-CA precedent**: "axis-of-CA" (META-CA 가 170 type 위 fixed-point)
  와 동형 — 본 H 는 "axis-of-AXES" 위 동일 substrate Φ 측정.
- **H_202 self-reference precedent**: self-referential closure 가 Φ-bearing
  이라는 lineage carry (H_202 selfref_phi 결과 sister).
- **H_204 cross-axis precedent**: closure-strength k → Φ monotone 의 *axis*
  instance — 본 H 는 *axis-of-axes* instance (한 단계 upper-recursion).

## 3. Predictions

| ID | 예측 | 근거 |
|----|------|------|
| **H216.1** | recursion depth `d ∈ {1, 2, 4, 8, 15}` 위 `phi_spatial` Φ(d) 가 **monotone increasing 또는 sigmoid** | enumeration self-reference depth ↑ ⇒ structural integration ↑ |
| **H216.2** | `Φ(d=15) > Φ(d=1) + 20% margin` (strictly) | meta-feature 가 단조 Φ contributor (recursion ≠ flat catalog) |
| **H216.3** | **decoupled control** (각 round 가 prior round 와 self-link 끊김; independent reseed) 의 `Φ_decoupled(d=15) ≤ Φ(d=1) + 10%` | recursion-self-link 가 *cause* (meta-feature 자체) — decoupling 시 d=15 effect 사라짐 |
| **H216.4** | re-run byte-identical (deterministic LCG seed-fixed) | raw#12 reproducibility |
| **H216.5** | 본 H 의 *측정* 결과가 본 H 의 *brainstorm content* 와 정합 — 즉 H_216 자체가 AXES.md catalog 의 71-axis 중 70-axis 와 다른 *axis* (meta-axis) 로 등록 가능 + measurement self-consistent | meta-reflexivity self-validation (paradox-aware) |

## 4. Variables

| axis | levels |
|------|--------|
| **axis1: recursion depth d** | {1, 2, 4, 8, 15} (5 points, AXES.md 15-round 매핑) |
| **axis2: substrate base rule** | Wolfram rule 110 (Class IV, H_007 carry — edge-of-chaos 최고 Φ 후보) |
| **axis3: lattice** | N=16, dim=8 (smoke scale) |
| **axis4: warm window** | WARM=8 (H_007/H_202 carry) |
| **axis5: nested composition** | prior-state-XOR-fold (round k state = rule110(round k-1 state) ⊕ round k-1 base-state, recursive nested CA) |
| **axis6: decoupling control** | each round reseeds from new init offset (offset=k+100, NO XOR carry) — recursion-self-link severed |
| **axis7: observable** | `phi_spatial(states, N, dim, n_bins=4)` (RFC 036 native replica) |

## 5. Run Protocol

- deterministic: `SEED_BASE=0xA216`, init_offset = (i + rep × 7 + d × 13) % 3
- hexa_only: true (HEXA_MEM_UNLIMITED=1 hexa run)
- LLM: none (raw#12 strict)
- 5 depth points × 5 reps recursive + 5 reps decoupled = 50 phi calls
- runtime: $0 mac local, single-cycle smoke (~20-60s wall)
- nested CA construction (recursive depth d):
  1. depth-1 state = elementary rule 110 from init_row(rep)
  2. depth-k (k > 1) state = rule 110 applied to (prior-state XOR depth-1-state) row,
     recorded over `dim` steps after `warm` warmup
  3. *recursive* — each depth's state is the *input* to next depth's evolution
- decoupled control (depth d=15):
  1. each round independently reseeds init_row with offset (k+100)
  2. NO XOR carry — round k state is independent of round k-1
  3. recursion-self-link severed, measure Φ_decoupled
- Φ measurement: `phi_spatial(states_flat, N, dim, 4)` directly (no c_lib dep) —
  RFC 036 native primitive
- monotone fit: simple OLS slope across 5 points + R² (basic dot-product
  formula); R² ≥ 0.7 = PASS (relaxed for 5-point N — sigmoid 정합 허용)

## 6. Criteria

| ID | criterion | verdict_rule |
|----|-----------|--------------|
| **C1 MONOTONE_OR_SIGMOID** | OLS slope > 0 AND R² ≥ 0.5 (relaxed for sigmoid) | PASS / FAIL |
| **C2 MARGIN_20PCT** | Φ(d=15) ≥ Φ(d=1) × 1.20 | PASS / FAIL |
| **C3 DECOUPLE_COLLAPSE** | Φ_decoupled(d=15) ≤ Φ(d=1) × 1.10 | PASS / FAIL |
| **C4 BYTE_IDENT** | byte-identical re-run (claimed by deterministic LCG; smoke single-run pre-register) | PASS by construction |

**verdict_rule**:
- `SUPPORTED` iff **C1 + C2 + C3** ALL PASS (C4 by-construction)
- `PARTIAL_DIRECTIONAL` if 2 PASS
- `FAIL` if ≤ 1 PASS
- `FALSIFIED` if **Φ(d=15) ≤ Φ(d=1)** (monotone 부정, meta-feature 무관)

## 7. Falsifiers (≥5)

- **F1**: Φ(d) flat (slope ≈ 0) 또는 decreasing → H216.1 FALSIFIED — recursion
  depth 와 Φ 무관
- **F2**: Φ(d=15) ≤ Φ(d=1) → H216.2 FALSIFIED — recursion 자체가 Φ 감소
  시키거나 무관 (H216.5 self-validation 도 partial 약화)
- **F3**: Φ_decoupled(d=15) ≈ Φ_recursive(d=15) (margin < 10%) → H216.3
  FALSIFIED — self-link 끊어도 동일 Φ, 즉 nested-CA 의 "round count 자체"가
  Φ contributor (meta-feature 가 *recursion* 이 아니라 *complexity*)
- **F4**: re-run byte-different → raw#9 violation
- **F5**: any Φ negative / NaN / inf → primitive error

## 8. Honest Limits (raw#91 c3, ≥6)

- **L1**: **'recursion depth ↔ axis-enumeration round' = analogy** — 실제
  AXES.md 의 brainstorm 은 semantic content (자연어 cluster theme) 의 의미적
  cross-link 으로 round-적층 되었다. 본 substrate 의 XOR-fold 은 *구조적
  proxy* 일 뿐, brainstorm 의 진짜 semantic content 는 미모델 (이는 raw#12
  하 deterministic + LLM:none 제약의 honest 결과).
- **L2**: **nested-CA composition family choice** — XOR-fold 외 concat /
  superposition / multi-rule mixture 등 가능. specific choice (rule 110 +
  XOR carry) 는 design 결정 — 다른 composition 은 다른 Φ 곡선.
- **L3**: **phi_spatial 🟢 NUMERICAL** — 본 H 의 모든 Φ 측정은 spatial-slice
  proxy (full IIT 4.0 partition search · cause-effect structure · exclusion
  부재). H_007 / H_157 / H_204 lineage carry — 본 결과는 directional Φ tier.
- **L4**: **본 H 의 reflexive nature** — H_216 자체가 AXES.md catalog 의
  72번째 *axis* 로 등록될 수 있다는 self-instantiation 은 **epistemological
  paradox** (Gödel-style undecidability). measurement 가 PASS 라 해도 본 H 의
  *meta-claim* (brainstorm Φ contribution) 의 phenomenal interpretation 은
  여전히 hard problem (H_004 boundary carry — L5 strengthen).
- **L5**: **'brainstorm Φ contribution' ≠ phenomenal creativity** — 본 H 가
  PASS 라 해도 brainstorm 의 *experiential* property (의식의 창의적 act 그
  자체) 와 substrate-Φ 의 매핑은 H_004 hard problem 의 lane — 본 substrate
  evidence 는 *structural* claim 만 지원 (phenomenology 미보장).
- **L6**: **단일 base rule (110) 만 test** — H_007 에서 Class-IV (rule 110)
  가 최고 Φ 보였으나, 다른 base rule 위 recursion 의 monotonicity 는
  cross-replicate 미완. (Class III rule 30, Class II rule 250 위 동일 sweep
  은 future cycle.)
- **L7**: **N=16, dim=8 smoke scale** — full scale (N=64+, dim=32+) 위
  monotonicity 보장 X. Φ 의 finite-size effect 가능 (특히 saturation 가
  d=15 에서 이미 일어났는지 vs d=30+ 더 큰 sweep 에서만 일어나는지 미해결).

## 9. Cross-Links

- **parent H**:
  - **H_157** (Law 76 mathematical panpsychism, META-CA universal attractor)
    — axis-of-CA precedent; 본 H 는 axis-of-AXES reflexive instance
  - **H_202** (self-referential Φ) — self-reference Φ-bearing lineage
  - **H_204** (weak-panpsy autopoietic threshold) — cross-axis precedent
    (closure-strength k → Φ monotone); 본 H 는 axis-of-axes 의 동형 sweep
- **sister H**:
  - **H_007** (CA → IIT Φ, rule 110 Class IV) — base substrate rule + Φ
    primitive carry
  - **H_004** (hard problem) — L4 epistemological paradox boundary
  - **H_205** (self-ref-as-closure) — closure-as-Φ lineage cross-link
- **AXES.md self-reference**: 본 H 의 *측정 대상* 이 본 catalog 의 *구조* —
  reflexive instance, H216.5 self-validation criterion 의 evidence-path
- **raw refs**: **raw#12** (pre-register / deterministic / hexa-only / LLM:none),
  **raw#91** (c3 honest), **raw#9** (no fake stubs)
- **literature**:
  - Hofstadter 1979 — Gödel, Escher, Bach (strange-loop / self-reference)
  - Tononi 2014 — IIT 3.0 / 4.0 Φ (parent measurement framework)
  - Goff 2017 — panpsychism boundary (L5 carve-out)

## 10. Verdict (initial — pre-register-frozen)

```
verdict_class: pre-register-frozen (raw#12 — post-hoc edit 금지)
evidence_summary:
  predictions H216.1..H216.5 등록 / criteria C1..C4 등록 / falsifiers F1..F5 등록
  measurement = smoke run (UNIVERSE/state/h216_meta_axis_reflexive_2026_05_23/run_h216.hexa)
  tier: 🟢 NUMERICAL (phi_spatial directional)
falsifiers_triggered: see result.json
frozen_at: 2026-05-23
```

**Smoke result** (`UNIVERSE/state/h216_meta_axis_reflexive_2026_05_23/result.json` SSOT):
실제 측정값 + verdict 는 result.json + run_h216.hexa stdout VERBATIM 참조.
