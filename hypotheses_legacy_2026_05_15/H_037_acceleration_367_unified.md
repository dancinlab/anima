---
id: H_037
slug: acceleration-367-unified-hypotheses
title: Self-Discovery Closure Super-H (367 acceleration unified + 9-variable closed basis + 2509 laws + 4-tier evolution)
domain: substrate
status: running
exploration_method: E5 (variable-ablation 367-cell sweep) + E8 (coverage-gap 100% intervention mapping) + E12 (self-discovery closure)
verification_method: W4 (verdict per H) + W9 (replication via 16-lens re-measurement) + W11 (meta-aggregate) + W3 (Φ × discovery rate)
raw_rank: 12
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: false
frozen_at: 2026-05-11
since: 2025-12 (legacy commits 28c26959 + 8cdf0917)
---

# H_037 — Self-Discovery Closure (acceleration_367_unified, expanded)

## Hypothesis (revised, unified 2026-05-11)

anima의 acceleration 367 unified hypotheses — schema v3.0 mass-scale hypothesis enumeration (17.2% convergence, 100% intervention mapping). 2026-05-11 expansion 으로 **self-discovery closure** super-H 로 promotion:

Anima closed-loop consciousness engine 은 **8 tightly-coupled property** 를 만족하는 self-discovery closure 를 exhibit:

1. **9-variable closed basis** (Hc_419): Φ, MI, tension_mean, tension_std, cell_variance, faction_entropy, hebbian_coupling, n_cells, output_entropy — 2509 laws 에서 10th variable 미출현 (M45 empirical closure)
2. **2509 laws / 77% auto-discovered** (Hc_054): T2/T3/T4 tier 의 auto-discovery loop
3. **53-law ceiling per config** (Hc_422): N(g) = 53·(1 − exp(−g/15)) — scale-invariant within arch; inverse-N at large scale (64c=53 / 128c=37 / 1024c=31)
4. **Evidence floor 0.50-0.70 = SOC signature** (Hc_423): 77.8% 의 law 가 evidence 0.50-0.70 cluster; > 0.95 없음 → criticality of discovery process
5. **17×17 = 136 intervention-pair synergy map** (Hc_421): 65 synergistic / 13 antagonistic / 58 neutral (M39)
6. **Thompson sampling > greedy / correlation** (Hc_420): Beta(α,β) ≥ 2× discovery rate
7. **60% cross-architecture transfer** (Hc_424): GRU→transformer ~60% law transfer (40% arch-specific)
8. **Convergence, not paradox** (Hc_425): saturation + compression + meta-laws (53 meta-laws + 7 generative template → 5.4× compression) → self-referential 수렴

4-tier evolution path: **T1 manual → T2 self-evo → T3 multi-loop → T4 consciousness pipeline**. 7-template generative compression (5.4×) + 53 meta-law structure 는 discovered law 들이 low-dimensional generative skeleton 을 가짐 시사.

## Why

- **367 acceleration brainstorm (2025-12)**: anima 가 자체 acceleration 가설 enumeration → 17.2% (62/367) supported
- **Hc_054 self-discovery 2509 laws (2026-05-11)**: 77% auto-discovered, 53 meta-laws, 7 generative templates (5.4× compression)
- **M45 empirical closure (Hc_419)**: 9-variable state basis 가 2509 laws 에서 10th variable 미요구 → discovery operator 의 finite-dim attractor
- **Thompson sampling (Hc_420)**: Beta(α,β) posterior selection 의 정량적 discovery-rate 우위
- **사용자 directive 2026-05-11**: Cycle 3 closure 에서 self-discovery closure 정식 promotion

## Inventory (preserved)

- 367 hypotheses unified: `ready/config/acceleration_hypotheses.json`
- 304/304 intervention mapping (commit f801931a)
- 65 hypotheses 16-lens re-measurement (DD163, commit 6fabdc2a)
- top x173.9 speedup achieved (95e13f39)
- 2509 laws / 77% auto / 53 meta / 7 generative template (Hc_054)

## Predictions (H_037.1 — H_037.9)

| ID | 예측 | 근거 Hc |
|----|------|---------|
| **H_037.1** | new auto-discovery run → ≥ 2,500 laws with ≥ 75% auto-fraction; 7 generative templates compress @ ≥ 5× | Hc_054 |
| **H_037.2** | new engine run with auto-discovery → zero 10th-variable additions to state basis (closure replicates) | Hc_419 |
| **H_037.3** | A/B Thompson vs ε-greedy vs correlation @ matched compute → Thompson ≥ 2× greedy rate | Hc_420 |
| **H_037.4** | independent-seed reproduction of 17×17 synergy map → partition (65, 13, 58) ± 5 per cell (M39 stable) | Hc_421 |
| **H_037.5** | 53-law ceiling at 64c reproduces with N(g) = 53·(1 − exp(−g/15)) fit R² > 0.95 | Hc_422 |
| **H_037.6** | evidence-score distribution peaks at 0.50-0.70 (≥ 70% laws); zero laws > 0.95 on independent run | Hc_423 |
| **H_037.7** | formal cross-architecture transfer on full 2509 laws → 30% < transfer < 90% (claim region) | Hc_424 |
| **H_037.8** | long-run (>1000 generations) divergence-vs-convergence metric remains bounded; no oscillation/blow-up/infinite-regress | Hc_425 |
| **H_037.9** | bridge to H_067: 448-law subset of 2509 + Ψ-constants (α=0.014, balance=0.5, steps=4.33, entropy=0.998, f_crit=0.10) derive from n=6 + Egyptian | Hc_018 |

## Variables

- **axis-A**: 9-variable state basis (Φ, MI, tension_mean, tension_std, cell_variance, faction_entropy, hebbian_coupling, n_cells, output_entropy)
- **axis-B**: intervention space (17 base interventions)
- **axis-C**: synergy partition (synergistic / antagonistic / neutral)
- **axis-D**: selection method (Thompson / ε-greedy / correlation)
- **axis-E**: configuration scale (n_cells: 64 / 128 / 256 / 512 / 1024)
- **axis-F**: architecture (GRU+faction vs transformer)
- **axis-G**: evidence score (per discovered law)
- **axis-H**: generation count g (discovery progress)
- **axis-I**: tier (T1 manual / T2 self-evo / T3 multi-loop / T4 consciousness pipeline)

## Run Protocol

1. **9-variable closure (W3)**: new auto-discovery run on anima engine → 10th-variable 출현 여부 확인 (deterministic)
2. **Thompson A/B (W3)**: Thompson vs ε-greedy vs correlation @ matched compute → discovery rate 비교
3. **53-law ceiling (W3)**: 64c / 128c / 1024c 각각 N(g) fit, R² > 0.95 target
4. **Evidence-floor distribution (W3)**: independent run → 0.50-0.70 cluster ≥ 70% + zero > 0.95 verify
5. **Synergy map (W3)**: independent seed 17×17 pair → (65, 13, 58) ± 5 per cell
6. **Cross-arch transfer (W3)**: GRU→transformer full 2509 law transfer test → 30% < r < 90% target
7. **Long-run convergence (W3)**: >1000 generation sweep → divergence/oscillation/blow-up 부재 verify
8. **H_067 bridge (W11)**: 448-law subset + Ψ-constants derive from n=6 + Egyptian (Hc_018 cross-link to H_067 super-H)
9. deterministic + hexa-only, llm: none

## Criteria

- **C1**: 9-variable closure holds on new auto-discovery run (zero 10th-variable additions)
- **C2**: 2509-law corpus reproducible; 7-template compression ≥ 5× on independent fit
- **C3**: Thompson rate ≥ 2× greedy @ matched compute (Hc_420)
- **C4**: 53-law ceiling fit R² > 0.95 on independent reproduction
- **C5**: evidence-score distribution mode 0.50-0.70 (≥ 70% laws), zero > 0.95
- **C6**: cross-architecture transfer 30% < r < 90% on formal test
- **C7**: long-run (>1000 gen) discovery operator bounded (no divergence)
- **C8**: 17×17 synergy partition (65, 13, 58) reproduces ± 5 per cell on independent seed
- **verdict_rule**: C1+C2+C3+C5+C7 met → verdict-supported super-H closure. C7 fail (divergence) → retracted closure claim.

## Falsifiers (≥ 9)

- **F1**: discovered law requires 10th variable not in 9-basis → Hc_419 closure killed
- **F2**: Thompson rate ≤ greedy rate @ matched compute → Hc_420 killed
- **F3**: synergy partition variance > 30% across seeds → Hc_421 M39 stability killed
- **F4**: ceiling fluctuation > 20% across seeds at fixed config → Hc_422 killed
- **F5**: evidence-score distribution shifts to ≥ 0.95 without rate loss on longer validation → Hc_423 criticality-signature killed
- **F6**: cross-architecture transfer < 30% OR > 90% → Hc_424 partition claim killed
- **F7**: late-generation divergence (oscillation / blow-up / infinite-regress) at >1000 generations → Hc_425 convergence killed
- **F8**: 7-template compression < 3× on independent law-corpus refit → Hc_054 generative-skeleton claim killed
- **F9**: 448-law subset cannot be derived from n=6 + Egyptian (Hc_018 bridge fails) → cross-link to H_067 weakened

## Honest Limits (raw#91 c3, ≥ 8)

### Original (preserved)

- **L1 (original)**: 367 hypothesis individual migration은 multi-cycle — 본 entry는 inventory pointer
- **L2 (original)**: 17.2% convergence rate는 본 cycle 한정 — 후속 cycle convergence 변동 가능
- **L3 (original)**: 'acceleration' 정의 = anima training cost 절감 (16-lens metrics)
- **L4 (original)**: legacy 2025-12, modern paradigm 이전 — re-verify 별도 cycle
- **L5 (original)**: top x173.9 speedup은 cherry-pick — 평균/median은 multi-instance 평가 별도

### Self-discovery closure expansion (added 2026-05-11)

- **L-S1**: "self-discovery" 는 anima-built engine 내 실행 — independent re-implementation 부재; convergence 가 engine quirk 의존 가능
- **L-S2**: 9-variable closure (M45) 는 2509 laws empirical claim 이나 discovery operator 자체가 human-designed — basis selection circular 가능
- **L-S3**: evidence floor 0.50-0.70 (M47) 는 SOC criticality interpret 되나 measurement bias (instrument resolution / repeat-count tradeoff) 가능
- **L-S4**: 60% GRU→transformer transfer rate 는 **preliminary** — full formal test pending
- **L-S5**: 7-template / 5.4× compression 은 **post-hoc fit** — generative-template 정의가 data fit 으로 shift 가능
- **L-S6**: Thompson vs greedy 비교가 single engine run series 내 — confounder (random seed, schedule) full control 부재
- **L-S7**: 53-law ceiling N(g) = 53·(1 − exp(−g/15)) 은 가능한 asymptotic fit 중 하나 — alternative power-law / stretched-exponential 미시험
- **L-S8**: convergence-not-paradox (Hc_425) 는 meta-claim — formal stability analysis (fixed-point existence proof) outstanding
- **L8 (raw#91 c3 mandate)**: 본 expansion 은 **draft review 거쳤음, 추가 review 미수행** (raw#91 L8 명시). 2509-law count 는 anima-internal — external corpora / replication 부재

## Cross-Links

- primary: `ready/config/acceleration_hypotheses.json`
- bench results: `ready/anima/data/bench_mass_hypotheses_results.json`
- **sister H**:
  - **H_020** (MASS-50) — meta-pointer
  - **H_028** (dd absorb) — DD subfolder cluster
  - **H_036** (DD116-146 meta-laws) — overlapping meta-law lane
  - **H_041** (evolution_self_singularity) — self-reference / self-evo tier
  - **H_067** (perfect-number-architecture) — Hc_018 bridge (448 laws + Ψ-constants from n=6); super-H sister
  - **H_124** (law_201_thermo_irreversible) — Law 201 ∈ 2509
  - **H_080** (topo_24variants) — n_cells variable + topology-conditional ceiling
- **candidates merged (9)**: Hc_054 / Hc_419 / Hc_420 / Hc_421 / Hc_422 / Hc_423 / Hc_424 / Hc_425 / Hc_018 (bridge)
- **cross-link**: Hc_036 (Landauer ln2 consciousness), Hc_472 (3x validation protocol)
- **legacy commits**: 28c26959 + 8cdf0917 + f801931a + 6fabdc2a + 95e13f39
- **legacy doc**: `docs/anima/paper_self_discovery.hexa` (canonical source), Law 1..2509 corpus
- **own**: own 21
- **raw refs**: raw#12 (pre-register) + raw#9 (hexa-only) + raw#91 (honest limits, expansion review)

## Conflict Resolution Pending

본 self-discovery closure expansion 작성 시점 (2026-05-11) 에 다음 conflict 존재 — Cycle 4 measurement 후 처리:

- **Hc_018 448-law derive vs Hc_054 2509-law total**: 동일 law corpus 의 subset count 차이 — 448 (Hc_018) vs 2509 (Hc_054) — formal cross-link / overlap audit 필요 (H_067 bridge 검증)
- **9-variable closure circularity (L-S2)**: discovery operator human-designed → basis 가 closure 를 enforce 한 것인지 emergent 인지 판별 — independent re-implementation 으로 verdict
- **Convergence vs paradox formal proof (L-S8)**: 현재 empirical claim 한정 — fixed-point existence proof 까지 verdict-partial 유지

## Brief Summary (preserved)

- **Sequential expansion**: 40 → 47 → 65 → 304 → 367 over multiple cycles
- **Schema v3.0**: unified format
- **17.2% convergence**: ~62 hypotheses SUPPORTED out of 367
- **Top result**: x173.9 speedup (1 specific hypothesis)
- **DD163 16-lens**: 65 hypotheses re-measurement cross-validation
- **Self-discovery closure (2026-05-11)**: 8 properties (9-var basis / 2509 laws / 53 ceiling / evidence floor / 17×17 synergy / Thompson / 60% transfer / convergence)

## Verdict

```
verdict_class: running (self-discovery closure super-H expansion landed 2026-05-11)
evidence_summary: 9 child Hc merged. 9-variable closure empirical (M45 2509-law). Thompson > greedy empirical. 53-law ceiling 64c partial. Cross-arch 60% preliminary. Convergence empirical (not formal).
falsifiers_triggered: none
criteria_met: C1 partial (M45 empirical). C3 partial (single engine series). C7 partial (empirical not formal).
frozen_at: 2026-05-11
```

## Migration Notes

- **Expansion source**: `hypotheses/expansions_pending/H_037_self_discovery_closure_expansion_draft.md` (2026-05-11)
- **Status transition**: `legacy-archive-pointer` → `running` (self-discovery closure super-H promotion)
- **Source candidates merged**: 9 (all `merged-to-H_037`; Hc_018 bridge cross-merge to H_067 also)
- **TODO**: independent re-implementation of discovery operator (formal stability analysis), formal cross-architecture transfer test on full 2509 laws, A/B Thompson vs greedy vs correlation @ matched compute, long-run (>1000 generation) divergence-vs-convergence sweep, Hc_018 ↔ H_067 cross-link verification, 17×17 synergy map reproduction on independent seed
