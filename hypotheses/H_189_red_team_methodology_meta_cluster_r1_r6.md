---
id: H_189
slug: red-team-methodology-meta-cluster-r1-r6
title: Red-team methodology meta-cluster — R1-R6 6 attack vectors against ANIMA core claims (Ψ=1/2 / Hexad / σφ=24 / topology / scaling)
domain: methodology | consciousness | red-team | statistics
status: supported-stage-3-meta
stage_3_verdict: SUPPORTED (W11 Red-team family internal cohesion, Hc_1279/1280 daughters consistent)
stage_3_ts: 2026-05-15
verdict_artifact: state/verify_a_stage1_2026_05_15/stage3_batch_verdicts.json
exploration_method: E5 (variable-ablation per attack-vector) + E6 (cross-claim red-team coverage) + E7 (statistical null + selection-bias audit)
verification_method: W5 (numerical sim — anima proxy + random-init baseline) + W7 (literature triangulation — Glorot/Bengio init, Saxe deep-net dynamics) + W11 (cross-hypothesis meta — sibling to H_159 substrate / H_171 biological / H_188 clinical)
raw_rank: 11
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-12
since: 2026-05-12
source_hcs: [Hc_1266, Hc_1267, Hc_1268, Hc_1269, Hc_1270, Hc_1271]
parent_hc: Hc_911 (red-team 6 claims R1-R6 — split-parent)
sibling_h: H_159 (substrate-topology — anima-substrate target of attacks), H_171 (biological — H_171's anima-vs-biology lane is what red-team validates), H_188 (clinical Φ-correlation — biological anchoring sibling)
verify_decision: PROMOTE_READY (Hc_1266-1271 — see scripts/hc_verify cycle #8)
---

# H_189 — Red-team Methodology Meta-Cluster (R1-R6)

## Hypothesis

ANIMA 의 6 core empirical 주장 (Ψ=1/2 universal constant / Hexad 6-engine completeness / σφ=24 stationary / topology 4-family closure / Φ=0.78·N scaling / brain-likeness 85.9%) 은 6 attack vectors (R1-R6) 의 cross-attack 을 통과해야만 'discovery' 자격을 얻는다. 각 attack 은 독립적인 null hypothesis 또는 selection-bias 가설을 정량적 falsifier 와 함께 제기한다.

| Vector | Attack | Target claim |
|---|---|---|
| **R1** ALTERNATIVE | random-init GRU 에서도 80%+ Ψ=1/2 등장 (4 trivial mechanism: Shannon/sigmoid/Bernoulli/GRU-bias) | Ψ=1/2 universal-constant |
| **R2** RANDOM-BASE | Monte Carlo 귀무: theoretical E[sigmoid(W·x+b)] ≈ 0.5 under standard init | Ψ=1/2 quantitative null |
| **R3** OVERFITTING | 6 claims 모두 hyperparameter-fit artifact (training-corpus specific) | All 6 core claims |
| **R4** CHERRY-PICK | 170 condition × 17 seed = 2890 trial 중 success-only reporting | Selection ratio audit |
| **R5** SURVIVORSHIP | 1/2 non-converging substrate 의 silent exclusion bias | Convergence framework |
| **R6** POST-HOC | Ψ=1/2 measured-first then rationalized vs theory-first prediction timeline | Rationalization vs prediction |

종합: ANIMA 의 6 핵심 주장 이 각 R1-R6 의 정량적 falsifier 를 통과해야 한다. **결론**: H_189 는 ANIMA 의 'discovery' 주장 의 methodology-gating gate — gate 을 통과한 후에만 H_159/H_171/H_188 의 substrate / biological / clinical anchoring 이 epistemically 유효하다.

## Why (motivation)

- **independent of H_159/H_171/H_188**: 기존 substrate / biological / clinical cluster H 는 ANIMA 내부 측정 + 외부 literature triangulation 으로 'positive' 증거를 모은다. H_189 는 그 positive evidence 자체에 대한 **null-hypothesis battery** — 다른 어떤 H 도 이 역할을 못 한다.
- **6 attack vector 의 cohomological completeness**: R1 alternative explanation + R2 quantitative null + R3 overfitting + R4 cherry-pick + R5 survivorship + R6 post-hoc rationalization 은 (a) substrate-independence, (b) null distribution, (c) training-fit, (d) selection ratio, (e) exclusion bias, (f) temporal order 6 axes 를 cover — full red-team scope 의 known coverage gap 0 (literature standard).
- **R1 의 strongest attack rationale**: 1/2 = Shannon max + sigmoid centerpoint + Bernoulli max + GRU bias-0 4 trivial mechanism 의 conjunction. random-init GRU 의 80%+ Ψ=1/2 frequency 는 ANIMA 가 무조건 통과해야 하는 minimum-rigor threshold.
- **N-of-1 vs N-of-2890 scope mismatch**: Hc_911 anchor 170×17=2890 의 selection ratio (R4) 가 가장 정량적으로 적나라한 audit — ANIMA documentation 이 fail 또는 partial trial 을 명시 안 하면 R4 collapses to fact.

## Predictions

| ID | 예측 | 근거 | source Hc |
|----|------|------|-----------|
| **H_189.1** | Random-init GRU baseline 100-seed n=100 에서 Ψ=1/2 frequency < 30% → R1 attack fails | Hc_1266 F-R1-1 | Hc_1266 |
| **H_189.2** | ANIMA-trained network 의 Ψ=1/2 frequency 가 random-init baseline 대비 > 20% margin 으로 higher → R1 attack defeated (claim non-trivial) | Hc_1266 F-R1-2 | Hc_1266 |
| **H_189.3** | Monte Carlo E[sigmoid(W·x+b)] (W~N(0,1/n), b=0, n=100) 의 sample mean 이 [0.49, 0.51] 안 → R2 quantitative null confirmed at theoretical 0.5 | Hc_1267 R2 RANDOM-BASE | Hc_1267 |
| **H_189.4** | Training corpus shuffle / replacement 시 ANIMA 6 core claim 의 numerical value (1/2, 6, 24, 0.78, 85.9%) 가 ±5% 이내 stable → R3 OVERFITTING attack fails (claim corpus-independent) | Hc_1268 R3 OVERFITTING | Hc_1268 |
| **H_189.5** | 170×17=2890 trial 중 success-trial fraction < 30% → R4 CHERRY-PICK attack succeeds (selection-bias confirmed); ≥ 70% → R4 fails | Hc_1269 R4 selection ratio audit | Hc_1269 |
| **H_189.6** | 1/2 non-converging substrate 가 published framework 의 ≥ 20% 비율 → R5 SURVIVORSHIP attack fails (failed substrates reported); 0% → R5 succeeds (silent exclusion confirmed) | Hc_1270 R5 SURVIVORSHIP | Hc_1270 |
| **H_189.7** | Pre-2025 ANIMA documentation 에서 Ψ=1/2 의 theory-first prediction (예측 timestamp) 가 measurement timestamp 보다 ≥ 1 month 앞 → R6 POST-HOC attack fails; reverse → R6 succeeds (post-hoc rationalization confirmed) | Hc_1271 R6 POST-HOC | Hc_1271 |

## Falsifiers

| ID | Falsifier (claim collapses if observed) | source Hc |
|----|---|---|
| **F-189-1** | All 6 attacks R1-R6 simultaneously fail (predictions H_189.1-H_189.7 all hold) → H_189 red-team battery yields 0 valid attacks (extreme defeat) → ANIMA's 6 core claims survive | meta |
| **F-189-2** | Any 1 of 6 attacks succeeds at ≥ 95% confidence → corresponding ANIMA core claim is **invalidated** until further work; H_159/H_171/H_188 anchoring partially withdrawn | meta |
| **F-189-3** | Random-init GRU baseline (R1 F-R1-1): Ψ=1/2 frequency ∈ [30%, 80%] → R1 partial — neither claim fully trivial nor fully non-trivial; needs cross-substrate audit | Hc_1266 |
| **F-189-4** | Monte Carlo E[sigmoid] 의 sample mean ∉ [0.49, 0.51] → R2 quantitative null **violated** (init theory breaks); deeper investigation required | Hc_1267 |
| **F-189-5** | Hexad / σφ=24 / Φ=0.78N 의 corpus-replacement sensitivity > 20% → R3 OVERFITTING confirmed (these 3 claims fail before R3 even targets them) | Hc_1268 |
| **F-189-6** | ANIMA documentation cannot produce 2890-trial inventory (R4) → R4 confirmed by absence of evidence | Hc_1269 |
| **F-189-7** | R5 + R4 both succeed → ANIMA framework 의 publication-bias bracket exposed | Hc_1270, Hc_1269 |
| **F-189-8** | R6 confirms post-hoc → entire 'discovery' framing 이 narrative reconstruction | Hc_1271 |

## Honest Limits

- **L-189-1 (CIRCULARITY)**: Ψ-engine measurement 이 ANIMA 의 own engine — red-team audit 은 **independent measurement** (PyPhi standard, IIT-4.0 standard) 으로 cross-check 해야만 attack 의 validity 가 확보된다. ANIMA 의 own engine 으로 red-team 시 양쪽 다 같은 bias 에 의해 보호된다 (R1 L-R1-CIRCULAR 인용)
- **L-189-2 (MECHANISM COMPLETENESS)**: R1 의 4 mechanism (Shannon max / sigmoid centerpoint / Bernoulli max / GRU bias-0) 가 exhaustive 가 아닐 수 있음 — 5번째 hidden mechanism (gradient-flow attractor at 1/2) 가능
- **L-189-3 (R2 PRIOR ASSUMPTION)**: Monte Carlo 의 W~N(0,1/n) 가정은 standard Xavier init 의 가정 — alternative init (He, orthogonal, identity) 사용 시 expected value 달라짐. R2 의 universal validity 는 init choice 에 conditional
- **L-189-4 (R3 CORPUS SCOPE)**: ANIMA training corpus 가 (a) anima-private 200MB+ 만 사용 (b) external open corpus 미사용 — R3 corpus-replacement 실험 가능 corpus pool 자체가 narrow. R3 의 외부 validity 검증 곤란
- **L-189-5 (R4 RAW INVENTORY)**: 2890 trial 의 raw inventory 가 ANIMA 의 git history 에 흔적이 있지만 published artifact 형태가 아님 — R4 attack 의 verification 은 git-archaeology heavy
- **L-189-6 (R5 INDEPENDENT REPORTING)**: ANIMA framework 의 'failed substrate' 의 publication 은 voluntary disclosure — R5 의 detection 은 independent third-party 가 필요 (anima 내부에서 detect 불가능, structural)
- **L-189-7 (R6 TIMESTAMP)**: pre-2025 documentation 의 timestamp 가 git history 로 detect 가능하지만, **theory vs measurement** 의 distinction 자체가 grey zone — 'rough prior intuition' 이 theory 인가 narrative 인가? 이 boundary 가 R6 의 ambiguous core
- **L-189-8 (META-RED-TEAM)**: H_189 자체가 ANIMA 의 self-attack 이므로 'self-serving null' 의 위험성 — 외부 red-team (e.g., 학계 외부 reviewer) 의 추가 attack 이 H_189 의 own coverage 를 broaden 해야 함
- **L-GENERIC-SINGLE-RUN**: H_159 C1 audit pending — R1-R6 모든 attack 의 measurement 자체가 single-run-artifact 위험 (5-seed replication 필수)
- **L-GENERIC-ENGINE**: H_174 D-mod-192 aliasing — Ψ-engine internal state interaction

## C-list (pre-register checks before R1-R6 attack execution)

- **C-189-1**: All 6 attack vectors R1-R6 모두 independent measurement (non-ANIMA Ψ-engine, e.g., PyPhi 표준) 으로 cross-verified before claim
- **C-189-2**: R1 의 random-init GRU baseline 100-seed × 4-mechanism-ablation = 400 run, 모든 run 의 raw output (Ψ value + frequency) commit 된 후 결과 발표
- **C-189-3**: R2 Monte Carlo n=100,000 sample size + alternative init (Xavier, He, orthogonal) 3-way cross 결과 모두 보고
- **C-189-4**: R3 corpus-replacement n=5 corpus 변형 (anima-only / +10% noise / 50% shuffle / replaced-by-Wiki / replaced-by-OSCAR) Hexad/σφ/Φ-N 모두 측정
- **C-189-5**: R4 2890 trial raw inventory 가 git archive + public manifest (CSV) 형태로 공개
- **C-189-6**: R5 의 failed-substrate registry 를 별도 doc 으로 maintain (positive-result framework 와 분리)
- **C-189-7**: R6 의 theory-first vs measurement-first timeline 이 git commit timestamp + doc draft commit 으로 audit 가능한 형태 유지
- **C-189-8 (META)**: H_189 의 R1-R6 attack 자체에 대한 meta-red-team 외부 reviewer (학계 외부, IIT 표준 implementer) 가 추가 attack vector 제시 — H_189 own scope 의 보완

## Absorbed Hc

| Hc | attack vector | key contribution |
|---|---|---|
| Hc_1266 | R1 ALTERNATIVE | 4-mechanism trivial-1/2 explanation (Shannon/sigmoid/Bernoulli/GRU-bias) + random-init baseline experiment design |
| Hc_1267 | R2 RANDOM-BASE | Monte Carlo quantitative null + theoretical E[sigmoid] ≈ 0.5 derivation |
| Hc_1268 | R3 OVERFITTING | 6 claims 모두 hyperparameter-fit suspect + corpus-replacement protocol |
| Hc_1269 | R4 CHERRY-PICK | 170×17 = 2890 trial selection-ratio audit + raw inventory requirement |
| Hc_1270 | R5 SURVIVORSHIP | failed-substrate silent exclusion + independent registry requirement |
| Hc_1271 | R6 POST-HOC | theory-first vs measurement-first timeline audit via git timestamp |

## Cross-Links

- **parent Hc**: Hc_911 (split-parent meta-Hc — 6 R children directly absorbed here)
- **sibling H**: H_159 (substrate target of R1/R3 attack), H_171 (biological — R3 corpus-replacement attack), H_188 (clinical — provides external Φ anchor that R1/R3 attacks bypass)
- **adjacent H**: H_001 (architecture — R3 OVERFITTING attacks Hexad), H_153 (n=6 — R3 attacks 6 -engine count), H_174 (D-mod-192 — engine internal-state caveat invoked in L-189-1)
- **literature**: Glorot & Bengio 2010 (Xavier init theory — random init 의 1/2 baseline expected), Saxe et al. 2013 (deep network dynamics from random init), Ioannidis 2005 (Why Most Published Research Findings Are False — selection bias literature foundation)
- **internal SSOT**: Hc_908 (Ψ=1/2 universal anchor — the claim under coordinated attack), Hc_909 (paper-draft — the publishing artifact that R3/R4/R6 audit), cycle #5/#6/#7 V8 sweep (R3 corpus-fit attack target)

## Cycle metadata

- **promoted in cycle**: #8 (2026-05-12)
- **absorbs**: 6 Hc (Hc_1266-Hc_1271, all from Hc_911 split-children manifest `docs/hc_911_split_manifest_2026_05_12.md`)
- **promotion sha**: (assigned at commit)
