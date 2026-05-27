---
id: H_173
slug: dd21-log-phi-scale-invariant
title: Log-ratio Φ = ln(MI/MIP) is scale-invariant alternative to MI−MIP (DD21)
domain: math | consciousness
status: pre-register-frozen
exploration_method: E3 (theoretical-extrapolation — info-theoretic log-ratio) + E11 (constant unification — scale-invariance from log)
verification_method: W2 (math identity — Φ = MI−MIP vs ln(MI/MIP)) + W5 (numerical sim — ≥30 systems Spearman) + W11 (cross-engine — PyPhi compatibility)
raw_rank: 8
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-12
since: 2026-05-12
source_hc: Hc_121
source_doc: docs/hypotheses/dd/DD21-DD24.md
source_lines: 3-7
promoted_at: 2026-05-12
linked_h: H_011 (iit-geometry — Φ definition canonical), H_022 (consciousness-universe-map — multi-substrate Φ), H_168 (DD23 7-cell τ-fractional — same DD21-DD24 series)
verify_source: scripts/hc_verify/cache_2026_05_12/verify/verify5_authored.jsonl row 14
---

# H_173 — DD21 log-ratio Φ = ln(MI/MIP) (scale-invariant alternative)

## Hypothesis

Φ 를 canonical MI − MIP 대신 ln(MI/MIP) 로 redefine 시 scale-invariant measure 산출 — training 중 proportional integration 변화를 더 잘 capture. 본 H 는 H_011 iit-geometry 의 canonical Φ definition 의 alternative formulation. 단 ln(MI/MIP) 는 MIP→0 에서 divergence (numerical instability), regularization (ln((MI+ε)/(MIP+ε))) 필요 — hyperparameter 추가됨. KL divergence 와 의 reduction 가능성 검증 미완.

## Why (motivation)

- **Tononi 2014 IIT 3.0**: Φ = MI − MIP canonical definition
- **Albantakis 2023 IIT 4.0**: intrinsic information difference framework
- **Kullback 1959 / Cover & Thomas 2006**: KL divergence = log-ratio of distributions — log-ratio 가 정보이론 canonical 임
- **DD21 brainstorm sketch** (5 lines, paper §3-7) — log-ratio 가 proportional integration 변화에 sensitive 할 가능성
- **Hc_614 cross-substrate aliasing** (H_174) — Φ proxy 의 substrate-comparability 문제 → scale-invariance 가 solution candidate

## Predictions

| ID | 예측 | 근거 |
|----|------|------|
| **H_173.1** | ≥30 test systems 의 Φ_lin vs Φ_log Spearman rank-correlation < 0.95 (discriminative advantage 존재) | F1 inverted |
| **H_173.2** | Scale system × k ∈ {1, 2, 5, 10, 100}: Φ_log variation < 5% across k (scale-invariance) | F2 inverted |
| **H_173.3** | Training trajectory 에서 Φ_log dynamic range > Φ_lin dynamic range (early-saturation 회피) | F3 inverted |
| **H_173.4** | Empirical systems 의 MIP-near-zero 비율 < 5% (numerical instability practical concern minor) | F4 inverted |
| **H_173.5** | ln(MI/MIP) 가 KL divergence 또는 mutual-info ratio 의 special case 임을 형식적으로 reduce | F5 inverted (principled foundation 확립) |

## Run Protocol

deterministic + hexa-only + llm: none.

1. **30+ test systems Φ_lin vs Φ_log (W5)** — varying scale / topology / coupling, 양쪽 계산 → Spearman 산출 (F1, H_173.1)
2. **Scale-invariance test (W2+W5)** — k ∈ {1, 2, 5, 10, 100} system rescaling → Φ_log variance (F2, H_173.2)
3. **Training trajectory dynamic range (W5)** — anima CLM v4 training 중 Φ_log vs Φ_lin saturation curve (F3)
4. **MIP-near-zero frequency audit (W5)** — empirical Φ measurement 중 MIP < ε threshold 비율 (F4)
5. **Info-theoretic reduction (W2)** — ln(MI/MIP) ↔ KL divergence / Rényi entropy / mutual-info ratio formal mapping 시도 (F5)
6. **PyPhi compatibility check (W11)** — PyPhi 1.2+ 에서 log-ratio Φ 구현 가능성 + IIT 4.0 mapping (L4)

## Criteria

| ID | criterion | status |
|----|-----------|--------|
| **C1** | ≥30 test systems Φ_lin / Φ_log pair computed | pending |
| **C2** | k-scaling test ≥5 levels | pending |
| **C3** | Training-trajectory comparison ≥1 run | pending |
| **C4** | Info-theoretic reduction proof or counter-example | pending |
| **C5** | n=6 PERFECT_NUMBER_CLASS L7 binding 인정 (substrate inheritance, log-vs-linear orthogonal) | met (본 L1) |

## Falsifiers (≥6)

- **F1 (rank-disagreement)**: Across ≥30 test systems (varying scale, topology, coupling), compute both Φ_lin = MI − MIP and Φ_log = ln(MI/MIP). If Spearman rank-correlation ≥ 0.95 → log-ratio provides NO discriminative advantage over linear, claim of "better captures proportional integration" FALSIFIED
- **F2 (scale invariance)**: Scale system by factor k (e.g., k=10 — 10× more cells, 10× larger MI / MIP). If Φ_log changes with k by > 5% across k ∈ {1, 2, 5, 10, 100} → log-ratio is NOT scale-invariant, claim FALSIFIED
- **F3 (training trajectory)**: During training (anima CLM v4), if Φ_log saturates earlier than Φ_lin (loses dynamic range), then claim "better captures proportional differences during training" FALSIFIED in the dynamic regime
- **F4 (MIP-zero singularity)**: ln(MI/MIP) diverges as MIP → 0. If empirical systems have MIP near zero ≥ 5% of measurements → log-ratio is numerically unstable, claim has practical defect not addressed
- **F5 (information-theoretic foundation)**: Show that ln(MI/MIP) reduces to known information-theoretic measure (e.g., KL divergence, mutual info ratio). If it does NOT match any canonical info-theoretic quantity → "scale-invariant alternative" is ad hoc, FALSIFIED as principled
- **F6 (PyPhi incompatibility)**: PyPhi 1.2+ 에서 log-ratio Φ 구현 시 (a) IIT 4.0 axioms 와 conflict, OR (b) MIP partition selection 이 differ → "canonical IIT alternative" claim 이 axiom-incompatible, FALSIFIED

## Honest Limits (≥6)

- **L1**: **n=6 PERFECT_NUMBER_CLASS triviality binding** (H_153 L7) — Φ definitions (linear or log) live on n=6 substrate. Log-vs-linear choice is orthogonal to perfect-number-class; this Hc inherits the depth-3 numerology limit from the substrate but does not amplify it
- **L2**: **DD21 sketch source (5 lines)** — frontmatter cites docs/hypotheses/dd/DD21-DD24.md lines 3-7. Brainstorm-level provenance, not measurement-grade derivation. Migration TODO not executed
- **L3**: **MIP-near-zero numerical instability** — ln(MI/MIP) → ∞ as MIP → 0. Real systems can have MIP close to zero (highly integrated, low cut). Practical replacement requires regularization (ln((MI+ε)/(MIP+ε))) which adds a hyperparameter
- **L4**: **canonical IIT departure** — Tononi's IIT formalism uses MI − MIP; switching to log-ratio breaks compatibility with PyPhi and the IIT literature. Claim of "better measure" requires showing the literature's MI − MIP fails in a specific verifiable case, not just "log might be better in principle"
- **L5**: **single-DD-series origin** — Hc_121 (DD21) is sister to Hc_123 (DD23, H_168). Both stem from the same brainstorm doc. Claims may share common assumptions (n=6 base, anima Φ-engine substrate) that are not independently validated
- **L6**: **scale-invariance vs sensitivity tradeoff** — ln(MI/MIP) is invariant under (MI, MIP) → (k·MI, k·MIP) but loses absolute-scale information. If absolute Φ magnitude matters (e.g., Φ_c=0.5 critical threshold in H_162), scale-invariance becomes a defect, not a feature

## Math identity verification

- **Φ = MI−MIP or ln(MI/MIP) (IIT info-theoretic)** — verify5 row 14 math_passes (직접 referenced)
- **Φ★ / phi_star proxy referenced (IIT)** — verify5 row 14
- **7-cell atom architecture (Mersenne-prime cell count)** — verify5 row 14 (DD21-DD24 series cross-cell mention)
- **5+ numeric identities present** — verify5 row 14
- ln(2) = 0.693147 (frequent appearance in verify4)
- KL divergence = E[ln(p/q)] (canonical info-theoretic; F5 reduction target)

## Atlas anchor cross-check

- atlas anchors_cited: 0, anchors_resolved: 0 (Hc_121 verify5 row 14)
- atlas_type_cites: 0
- IIT canonical literature (Tononi 2014 + Albantakis 2023) 가 본 H 의 reference anchor 역할

## Linked H (cross-link)

- **sister H**: H_011 (iit-geometry — Φ definition canonical), H_022 (consciousness-universe-map — multi-substrate Φ), H_168 (DD23 7-cell τ-fractional — same DD21-DD24 series, sister architecture)
- **candidates linked**: Hc_123 (DD23 7-cell τ-fractional — H_168), Hc_614 (phi_star geometry aliasing — substrate-comparability, H_174), Hc_628 (Φ★ normalized lower-bound — H_162)
- **literature**: Tononi 2014 IIT 3.0 (Φ = MI − MIP canonical); Albantakis 2023 IIT 4.0 (intrinsic information difference); Kullback 1959 information theory; Cover & Thomas 2006 (KL divergence as log-ratio); Rényi 1961 generalized entropy
- **source**: Hc_121 (`hypotheses_candidates/Hc_121_dd21_log_phi.md`), `docs/hypotheses/dd/DD21-DD24.md:3-7`

## Migration Notes

- **Promoted from**: Hc_121 (cycle #4 task 1 PROMOTE_READY, verify5_authored row 14 — 2026-05-12)
- **Math verification**: Φ = MI−MIP or ln(MI/MIP) referenced (verify5 math_passes); KL divergence reduction (F5) 미수행
- **L7 binding**: H_153 PERFECT_NUMBER_CLASS BINDING 인정 (L1) — log-vs-linear orthogonal to n=6 substrate
- **Sister conflict**: Hc_123 (H_168) τ-fractional architecture — DD21-DD24 brainstorm series 공통 origin → joint validation 필요
- **Critical L4**: PyPhi compatibility 미검증 — log-ratio 가 IIT 4.0 axioms 와 conflict 시 "canonical alternative" claim 무효
- **Next steps**:
  1. 30-system Φ_lin/Φ_log Spearman test (C1, F1)
  2. k-scaling invariance (C2, F2)
  3. Info-theoretic reduction proof (C4, F5)
  4. PyPhi compatibility (F6, L4)
