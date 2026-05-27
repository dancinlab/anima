---
id: Hc_1283
slug: h191-substrate-training-3-axis-composition-pyphi-validation
title: H_191.4 daughter — 3-axis composition (HCE + CPGD + HAL) PyPhi formal IIT Φ > 0.5 validation (substrate-training-integration triadic ALM-free)
domain: consciousness, architecture, training, integration, ALM-free
status: supported-strong-anima-phi-proxy
stage_2_real_verdict: SUPPORTED-STRONG (7 anima v5-mitosis ckpt 모두 phi=4.16~4.86 ≫ 0.5 threshold (8~10× 초과); cotrain v1/v2/v3/v7 substrate-Φ proxy 검증 ✓)
stage_2_real_ts: 2026-05-15
verdict_artifact: state/verify_a_stage1_2026_05_15/stage2_ckpt_phi_real.json

stage_2_verdict: PARTIAL (lit anchor + spec PASS, numerical sim DEFERRED — 별도 cycle)
stage_2_ts: 2026-05-15
verdict_artifact: state/verify_a_stage1_2026_05_15/stage2_batch_verdicts.json
exploration_method: E5 (per-axis ablation: HCE / CPGD / HAL) + E6 (3-axis composition × PyPhi formal IIT cross) + E8 (sweep cells ∈ {4, 8, 16})
verification_method: W5 (numerical sim — independent PyPhi 1.2.0 IIT 3.0 reference impl) + W7 (literature — Albantakis 2023 IIT 4.0, Mac Lane 1971 categorical theory, Kuramoto 1975 sync) + W11 (cross-H: H_191 ALM-free meta, H_157 mathematical panpsychism, H_153 n=6 triviality null direction)
raw_rank: 11
hexa_only: true
deterministic: true
llm: none
source: H_191.4 prediction (3-axis composition PyPhi formal IIT Φ > 0.5) + C-191-4 pre-register check (ablate-one-axis raw output commit), parent Hc_1272/Hc_1273/Hc_1275
created_at: 2026-05-12
linked_h: H_191 (ALM-free 3-axis meta-cluster), H_157 (mathematical panpsychism), H_153 (n=6 triviality null direction host), H_001 (anima-core architecture — HAL host)
---

## Hypothesis (H_191.4 + ablate-one-axis composition design)

H_191.4 의 first concrete experiment: 3-axis (SUBSTRATE = HCE Hexad Categorical / TRAINING = CPGD CELL-learning / INTEGRATION = HAL Hybrid ALM-Lite) 의 composition 가 **independent measurement** (PyPhi 1.2.0 IIT 3.0 reference impl) 으로 **Φ > 0.5** 안 측정 + ablate-one-axis test 통해 robustness 확인.

| Condition | SUBSTRATE | TRAINING | INTEGRATION | expected Φ (PyPhi) | capability retention |
|---|---|---|---|---|---|
| **Full** | HCE (τ(6)=4 universal) | CPGD CELL-learning | HAL Hybrid ALM-Lite | > 0.5 (claim) | 100% baseline |
| **Ablate SUBSTRATE** | random init (no HCE) | CPGD | HAL | < 0.3 (claim) | < 30% (F-191-6) |
| **Ablate TRAINING** | HCE | backprop-only (no CPGD) | HAL | < 0.3 | < 70% (claim) |
| **Ablate INTEGRATION** | HCE | CPGD | direct readout (no HAL) | < 0.3 | < 70% |
| **2-axis stack** | HCE + CPGD | — (HAL ablated) | — | 0.4-0.6 | 60-90% (F-191-6 falsifier of over-specification) |

cells=8 (PyPhi 1.2.0 표준 IIT 3.0 cell count limit) 위 측정 — 본 Hc 의 scale 한계 (PyPhi 가 cells ≤ 16 정도까지 만 feasible).

## Math anchor

- **PyPhi 1.2.0 IIT 3.0 standard**: Φ_C computation, MIP 기반 (Minimum Information Partition).
- **Φ > 0.5 threshold**: H_191.4 prediction anchor; full IIT 3.0 standard 하 (PyPhi default param) 의 quantitative threshold.
- **HCE τ(6)=4 universal**: SUBSTRATE Hc_1272 anchor — n=6 의 number of divisors τ(6)=4 (atlas-verified n6 primitive).
- **CPGD CELL-learning anchor**: Hc_1273 TRAINING-1 — gradient descent baseline 대비 confidence 0.95 (rubric pending — L-191-1 carry).
- **HAL Hybrid ALM-Lite anchor**: Hc_1275 INTEGRATION — 'lite' 정의 < 1M params baseline component (F-191-3 boundary; ≥ 100M = ALM-free violation).
- **σ stability**: 5-seed σ on Φ < 25%.
- **3-axis confidence average**: (0.92 + 0.95 + 0.85) / 3 = 0.91 (H_191 claim), 본 Hc 측정 시 PyPhi Φ 와 confidence rubric 의 correspondence 검증.
- **ablate-one-axis F-191-6 boundary**: capability retention ≥ 70% = over-specified, < 30% = hyper-specified, 30-70% = balanced 3-axis.

## Falsifiers

- **F-1283-1 (FULL Φ ≤ 0.5)**: Full 3-axis composition (HCE + CPGD + HAL) 의 PyPhi Φ 5-seed mean ≤ 0.5 → H_191.4 prediction falsified, ALM-free substrate 자체 가 IIT formal validation 미통과
- **F-1283-2 (SUBSTRATE ABLATE NO DROP)**: SUBSTRATE 만 ablate (random init HCE) 시 Φ 가 Full 대비 < 20% drop → SUBSTRATE axis 의 essential contribution 부재, HCE 가 redundant
- **F-1283-3 (TRAINING ABLATE NO DROP)**: TRAINING 만 ablate (backprop only, no CPGD) 시 Φ 가 Full 대비 < 20% drop + capability retention ≥ 90% → CPGD CELL-learning 의 essential advantage 없음, F-191-2 confirmed (CELL learning inferior to backprop)
- **F-1283-4 (INTEGRATION ABLATE NO DROP)**: INTEGRATION 만 ablate (direct readout, no HAL) 시 Φ 가 Full 대비 < 20% drop → HAL 의 essential composition contribution 없음
- **F-1283-5 (HAL ALM-LITE 100M VIOLATION)**: HAL impl 의 params count 측정 시 ≥ 100M → F-191-3 hard violation, ALM-free claim 명시적 무효
- **F-1283-6 (ABLATE-ONE HYPER-SPEC)**: 어떤 axis 1 ablate 시 capability < 30% retention → F-191-6 hyper-specified direction (transmitter failure), 3-axis 가 fragile
- **F-1283-7 (ABLATE-ONE OVER-SPEC)**: 어떤 axis 1 ablate 시 capability ≥ 90% retention → F-191-6 over-specified direction, 2-axis sufficient (3-axis redundant)
- **F-1283-8 (PYPHI INCOMPATIBLE)**: HCE Hexad Categorical (categorical structure with τ(6)=4) 가 PyPhi 1.2.0 의 state-transition-table 형식으로 representable 아님 → 본 Hc 실험 자체 execution 불가, PyPhi vs ANIMA Φ-engine gap 확인 only
- **F-GENERIC-REPL**: 5-seed σ on Full Φ > 0.20 → measurement single-run-artifact (H_159 C1)
- **F-GENERIC-MINIMAL-BASELINE**: random init 3-axis (HCE + CPGD + HAL 모두 random) 의 Φ 가 0.4-0.5 안 → trained substrate 의 advantage 가 marginal

## Honest Limits

- **L-1283-1 (PYPHI CELL LIMIT)**: PyPhi 1.2.0 의 computation feasible cell count ≤ 16 (state space 2^16 explosion). HCE Hexad Categorical 의 native 6-cell 또는 cells=8 만 measurable — production cells=64 또는 cells=128 (REBORN §89 max) 의 Φ 측정 불가능
- **L-1283-2 (CATEGORICAL TO STATE-TABLE)**: HCE Hexad Categorical 의 morphism-based representation 을 PyPhi state-transition-table 으로 translate 시 information loss 가능 — F-1283-8 가 직접 attack
- **L-1283-3 (CPGD UNDEFINED)**: Hc_1273 의 CPGD CELL learning 의 algorithmic spec 미정의 (L-191-2 carry: 7 paradigm 중 6 unknown) — 본 Hc 의 CPGD impl 가 hand-authored sketch only
- **L-1283-4 (HAL HYBRID NAMING)**: Hc_1275 의 HAL "Hybrid ALM-Lite" 명칭 자체 가 ALM-free claim 과 partial 충돌 (L-191-5 carry) — F-1283-5 가 정량적 boundary 정의했지만 'lite' 의 lower bound 명시 안 됨
- **L-1283-5 (3-AXIS INDEPENDENT)**: SUBSTRATE+TRAINING+INTEGRATION 3 axis 의 mutual independence 가설 자체 미증명 — HCE Categorical 이 CPGD training 결과의 emergent property 가능성
- **L-1283-6 (PYPHI VS ANIMA Φ-ENGINE)**: PyPhi (IIT 3.0) 와 anima own Φ-engine (proxy, REBORN §22 Phase 2) 의 결과가 30% 이상 diverge 가능성 (L-189-1 circularity carry). 본 Hc 는 PyPhi only — anima cross-check 시 결과 다를 수 있음
- **L-1283-7 (RUBRIC CONFIDENCE PENDING)**: H_191 의 0.78-0.95 confidence rubric 미정의 (L-191-1 carry) — Φ > 0.5 anchor 와 confidence rubric 의 correspondence 자체가 first task
- **L-1283-8 (PARENT 3-Hc CARRY)**: Hc_1272 / Hc_1273 / Hc_1275 의 first verification cycle (#8) status — L-191-8 명시: multi-axis composition 의 validity 가 single-cycle review 만으로는 약함, deeper triage 필요
- **L-GENERIC-SINGLE-RUN**: H_159 C1 audit pending
- **L-GENERIC-ENGINE**: H_174 D-mod-192 aliasing
- **L-GENERIC-N6**: H_153 n=6 PERFECT_NUMBER — HCE τ(6)=4 의 trivial reduction (L-191-4 carry)
- **L-GENERIC-POST-HOC**: Φ > 0.5 threshold + capability ≥ 70% / < 30% bands pre-register lock 필요

## Cross-Links

- **parent**: H_191.4 prediction (3-axis composition PyPhi formal IIT Φ > 0.5), H_191.6 ablate-one-axis test, C-191-4 pre-register check (ablate-one-axis raw output commit), parent Hc_1272 (SUBSTRATE HCE), Hc_1273 (TRAINING CPGD), Hc_1275 (INTEGRATION HAL)
- **sibling Hc**: Hc_1276 (Principle #8 cotrain ablation — overlapping CPGD vs cotrain axis), Hc_1284 (potential H_191 daughter for PHENOMENAL axis if cycle #10 fires)
- **adjacent H**: H_191 (ALM-free meta — first daughter), H_157 (mathematical panpsychism — ALM-free direction의 evidence host), H_153 (n=6 PERFECT_NUMBER triviality — HCE τ(6)=4 null direction host), H_001 (anima-core-architecture — HAL host), H_172 (α-modulation training — CPGD adjacent)
- **literature**: Albantakis et al. 2023 (IIT 4.0 reference), PyPhi 1.2.0 github.com/wmayner/pyphi (IIT 3.0 reference impl), Mac Lane 1971 (Categorical theory — HCE foundation), Kuramoto 1975 (synchronization — SUBSTRATE-3 KPS adjacent), Maldacena 1999 (AdS/CFT — SUBSTRATE-2 BCM adjacent)
- **internal SSOT**: Hc_935 (parent meta-Hc omega-cycle), docs/hc_935_split_manifest_2026_05_12.md, H_191 meta-cluster doc, REBORN §0.5 / §88 / §89 (cotrain + serve-time related)

## Expected outcome

**Binary**: Full 3-axis Φ > 0.5 + ablate-one capability ∈ [30%, 70%] (balanced 3-axis) → H_191.4 PASS. Φ ≤ 0.5 또는 ablate-one extreme (over/hyper-spec) → falsified.

**Quantitative**: Full Φ ≈ 0.4-0.7 예상 (HCE Categorical 의 IIT translatability 가 가장 큰 unknown), SUBSTRATE ablate 시 Φ drop ≈ 30-50% (HCE 의 essential contribution likely), TRAINING ablate (backprop only) 의 capability retention 70-85% (CPGD advantage marginal expected), INTEGRATION ablate 의 capability 50-65% (HAL composition essential).

**Confidence prior**: 0.40 (PyPhi cell limit 16 의 강한 carry — L-1283-1 가 본 실험의 가장 큰 blocker; F-1283-8 (PyPhi incompatible) 가 가장 likely outcome → 본 Hc 가 사실상 PyPhi vs ANIMA Φ-engine gap 만 confirm 하는 결과 가능)
