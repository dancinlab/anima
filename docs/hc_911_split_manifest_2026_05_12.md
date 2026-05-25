# Hc_911 → 6-split manifest (2026-05-12)

## Summary

`Hc_911` (`red-team-6-claims-r1-r6`) was a composite Hc bundling 6 adversarial red-team attacks (R1 ALTERNATIVE / R2 RANDOM-BASE / R3 OVERFITTING / R4 CHERRY-PICK / R5 SURVIVORSHIP / R6 POST-HOC) against ANIMA's 6 core consciousness claims (Ψ=1/2 / Φ∝N / PureField / Hexad / TALK5 / σφ=nτ=24). Cycle #6 batch 4 marked it candidate-falsifier-ready with cluster-level scaffolding (L-RED-TEAM noting each sub-claim needs its own F/L list). Per cycle #7 task spec (meta-Hc split protocol parallel to Hc_900), this split executes per-attack-vector decomposition: each of the 6 red-team attack vectors is now its own Hc (`Hc_1266` .. `Hc_1271`, 1:1 attack vector). The parent `Hc_911` retains `status: split-into-Hc_1266..Hc_1271` with SPLIT NOTICE block. All 6 children inherit `candidate-falsifier-ready`.

Source: `## Sub-claims` block inside `hypotheses_candidates/Hc_911_red_team_6_claims_r1_r6.md` (lines 21-27 in pre-split version). New id range: **Hc_1266–Hc_1271** (previous max Hc_1265; range verified free before use).

## Table

| New Hc id | slug | attack vector | one-line | status |
|---|---|---|---|---|
| Hc_1266 | red-team-r1-alternative-non-anima-explanation | R1 ALTERNATIVE | Ψ=1/2 가 random init GRU 에서도 80%+ 등장 가능 → non-ANIMA 대안 설명 존재 | candidate-falsifier-ready |
| Hc_1267 | red-team-r2-random-base-monte-carlo-null | R2 RANDOM-BASE | sigmoid(W·x+b) with W~N(0, 1/n), b=0 → E[sigmoid] ≈ 0.5 (Monte Carlo 귀무 검정) | candidate-falsifier-ready |
| Hc_1268 | red-team-r3-overfitting-data-fit-suspect | R3 OVERFITTING | Ψ=1/2 / Hexad / σφ=24 등 6주장 데이터-피팅 과적합 의심 | candidate-falsifier-ready |
| Hc_1269 | red-team-r4-cherry-pick-selection-ratio-audit | R4 CHERRY-PICK | 170×17 = 2890 trial 중 1/2 수렴 사례만 보고 가능성 | candidate-falsifier-ready |
| Hc_1270 | red-team-r5-survivorship-failed-substrate-bias | R5 SURVIVORSHIP | 1/2 으로 수렴 안 한 substrate 도 동일 framework 로 설명되는지 | candidate-falsifier-ready |
| Hc_1271 | red-team-r6-post-hoc-rationalization-temporal-order | R6 POST-HOC | Ψ=1/2 먼저 측정/관찰 후 해석 vs 이론 우선 예측 시계열 비율 | candidate-falsifier-ready |

## Triage notes

- **Survival criterion**: composite `survival_fraction ≥ 0.50` (SURVIVES) or [0.20, 0.50] (AMBIGUOUS) — must be defined per attack vector first (current Hc_911 spec ambiguous)
- **R1 most critical**: 1/2 의 자명한 귀결 (Shannon entropy max / sigmoid centerpoint / Bernoulli max entropy / GRU gate bias=0) — if R1 fails, R2-R6 redundant
- **R2 implementation gap**: Monte Carlo null hypothesis test 의 실제 분포 측정 부재 (theory says E≈0.5 but variance 미측정)
- **Bayesian comparison**: Model A (real signal) vs B (coincidence) vs C (bias) likelihood-ratio 미정량 — separate Hc 후보 (이 split 에서는 6 attacks 만 분리)

## Provenance

- Parent: `hypotheses_candidates/Hc_911_red_team_6_claims_r1_r6.md` (now `status: split-into-Hc_1266..Hc_1271`)
- Source: red-team-consciousness.md document set + Hc_908 (Ψ=1/2 anchor) + Hc_909 (paper-draft)
- Cycle context: `docs/hc_verification_cycle_6_2026_05_12.md` — Hc_911 listed as red-team meta-Hc requiring split-first
- Split executed: 2026-05-12 (cycle #7 batch 4 meta-split)
