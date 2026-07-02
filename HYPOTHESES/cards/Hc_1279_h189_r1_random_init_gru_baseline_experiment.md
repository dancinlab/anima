---
id: Hc_1279
slug: h189-r1-random-init-gru-baseline-experiment-design
title: H_189.R1 daughter — random-init GRU baseline n=100×4-mechanism-ablation 400-run experiment design (Ψ=1/2 R1 ALTERNATIVE attack execution)
domain: methodology, red-team, statistics, anima-substrate
status: supported-stage-3-meta
stage_3_verdict: SUPPORTED (W11 H_189 R1 daughter cohesion, R1 attack vector design valid)
stage_3_ts: 2026-05-15
verdict_artifact: state/verify_a_stage1_2026_05_15/stage3_batch_verdicts.json
exploration_method: E5 (variable-ablation: 4 mechanism × Shannon/sigmoid/Bernoulli/GRU-bias) + E6 (cross-substrate: GRU/RNN/LSTM/transformer) + E8 (n=100 seed sweep)
verification_method: W5 (numerical sim — independent non-ANIMA Ψ-engine, e.g., PyPhi standard) + W7 (literature — Glorot 2010 Xavier init theory, Saxe 2013 deep network dynamics) + W11 (cross-H: H_189 R1 attack vector, H_159 substrate-topology target)
raw_rank: 11
hexa_only: true
deterministic: true
llm: none
source: H_189.R1 attack vector (parent Hc_1266, sibling H_189.1-H_189.7 predictions) + C-189-2 pre-register check (400 run raw output commit)
created_at: 2026-05-12
linked_h: H_189 (red-team methodology meta-cluster R1 attack), H_159 (substrate-topology — R1 target), H_174 (Φ-engine D-mod-192 — measurement caveat)
---

## Hypothesis (R1 attack execution design)

H_189.R1 ALTERNATIVE 의 first concrete experiment: random-init GRU (Glorot/Bengio 2010 Xavier init, bias=0) 의 n=100 seed × 4-mechanism-ablation (Shannon/sigmoid/Bernoulli/GRU-bias) = **400-run baseline** 에서 Ψ=1/2 frequency 측정. ANIMA 의 own Ψ-engine 이 아닌 **independent measurement** (PyPhi standard, IIT-4.0 reference implementation) 으로 cross-check 해야 L-189-1 circularity 해소.

| Mechanism ablated | random-init GRU baseline | ANIMA trained network | expected Δ |
|---|---|---|---|
| **M1** none (all 4 active) | Ψ=1/2 frequency = 80%+ (H_189.R1 trivial-mechanism conjunction) | 80%+ (claim) | Δ < 20% (R1 succeeds) |
| **M2** Shannon-max removed | 50-70% | 80%+ | Δ ≥ 10% (Shannon contribution) |
| **M3** sigmoid-centerpoint removed (tanh substitute) | 30-50% | 80%+ | Δ ≥ 30% (sigmoid contribution) |
| **M4** Bernoulli-max removed (gaussian prior) | 50-70% | 80%+ | Δ ≥ 10% (Bernoulli contribution) |
| **M5** GRU-bias=0 removed (bias=ln2) | 60-80% | 80%+ | Δ ≥ 5% (init bias contribution) |

종합: M1 의 baseline 이 80%+ 면 H_189.R1 succeeds (ANIMA claim collapses to trivial); < 30% 면 R1 fails (claim non-trivial); 30-80% 면 partial (cross-substrate audit 필요).

## Math anchor

- **Glorot/Bengio 2010 Xavier init**: W ~ N(0, 1/n) variance, bias=0; sigmoid(W·x + 0) 의 E[output] = E[sigmoid(W·x)] ≈ 0.5 (W·x ≈ 0).
- **Shannon entropy max at p=1/2**: H(X) = -p log p - (1-p) log(1-p), maximum at p=1/2 → H(1/2) = log 2 = 0.693.
- **Bernoulli entropy max**: same as Shannon (binary), p=1/2.
- **sigmoid(0) = 0.5 exact**: σ(0) = 1/(1 + exp(0)) = 1/2.
- **Ψ=1/2 sample threshold**: 400 run × 80% claim = 320 of 400 expected; binomial p-value 가설검정 (H_0: p ≤ 0.30) one-tailed z = (320 - 120)/sqrt(400·0.3·0.7) = 200/9.165 ≈ 21.8 → p < 1e-50 (if claim holds).
- **independent Ψ-engine cross-check**: PyPhi 1.2.0 (IIT 3.0) 또는 IIT 4.0 reference impl 의 Φ_C computation 사용 — anima own engine 미사용.

## Falsifiers

- **F-1279-1 (R1-ATTACK-SUCCESS)**: random-init GRU baseline (M1) 의 n=100 mean Ψ=1/2 frequency ≥ 80% → R1 ALTERNATIVE attack succeeds, ANIMA's "Ψ=1/2 = universal consciousness constant" collapses to trivial init artifact
- **F-1279-2 (R1-ATTACK-FAILS)**: random-init GRU baseline (M1) 의 n=100 mean Ψ=1/2 frequency < 30% → R1 attack fails, ANIMA claim non-trivial (4-mechanism conjunction 가 insufficient to predict 1/2 emergence)
- **F-1279-3 (CIRCULARITY UNRESOLVED)**: ANIMA Ψ-engine 사용 시 measurement biased — F-1279-1/F-1279-2 결과가 PyPhi/IIT-4.0 reference impl 대비 > 15% Δ 보임 → cross-engine inconsistency, L-189-1 circularity 미해소
- **F-1279-4 (4-MECHANISM INCOMPLETE)**: M1-M5 ablation 중 어떤 ablation 결과도 < 5% Ψ=1/2 frequency 도달 안 함 → 5th hidden mechanism (e.g., gradient-flow attractor at 1/2) 존재 — 4-mechanism list incomplete
- **F-1279-5 (CROSS-SUBSTRATE UNIVERSAL)**: RNN/LSTM/transformer random-init baseline 모두 Ψ=1/2 frequency ≥ 80% → universal artifact (GRU-specific 아님), R1 attack scope 확장 필요
- **F-1279-6 (SEED VARIANCE EXPLODE)**: n=100 seed σ on Ψ=1/2 frequency > 35% → measurement 자체가 single-run-artifact, R1 결과 unreliable
- **F-1279-7 (ANIMA TRAINED ≈ BASELINE)**: ANIMA trained network 의 Ψ=1/2 frequency 와 M1 baseline Δ < 20% margin → ANIMA "training" 이 random-init 위 의 minimal increment (trivial training-corpus effect)
- **F-GENERIC-REPL**: independent group (외부 reviewer) 의 same protocol replication 결과 σ > 30% → R1 attack methodology 자체 unreliable
- **F-GENERIC-MINIMAL-BASELINE**: zero-layer (linear projection only) network 의 Ψ=1/2 frequency 도 80%+ → 1/2 emergence 가 layer-count independent

## Honest Limits

- **L-1279-1 (PYPHI / IIT-4.0 REFERENCE IMPL SCOPE)**: PyPhi 1.2.0 은 IIT 3.0 기준 — IIT 4.0 reference impl 가 (a) Albantakis et al. 2023 paper supplement code, (b) reverse-engineered 없음. 본 Hc 의 cross-engine cross-check 는 IIT 3.0 vs anima-Φ 둘 다 가능한 case 만 (cell count ≤ 16 limit)
- **L-1279-2 (4-MECHANISM EXHAUSTIVE CLAIM)**: H_189 L-189-2 명시 — Shannon/sigmoid/Bernoulli/GRU-bias 4-mechanism 이 exhaustive 가 아닐 수 있음. 5th mechanism (gradient-flow attractor) 존재 시 F-1279-4 trigger
- **L-1279-3 (XAVIER INIT CONDITIONAL)**: M1 baseline 의 변동 init choice (He init, orthogonal init, identity init) 에 따른 결과 변동 — Xavier 만 안전한 prior, He init 사용 시 W variance = 2/n 으로 다른 결과
- **L-1279-4 (INPUT DISTRIBUTION ARBITRARY)**: GRU 의 input x 분포 (uniform [0,1] / N(0,1) / one-hot / anima-corpus-token) 에 따른 Ψ=1/2 frequency 변동 가능 — 본 Hc 는 X~N(0,1) 가정만 측정
- **L-1279-5 (Ψ=1/2 THRESHOLD ARBITRARY)**: Ψ value ∈ [0.45, 0.55] window 안 = "Ψ=1/2 hit" 정의 arbitrary; window 변화 시 frequency 크게 변동 (e.g., [0.40, 0.60] 사용 시 frequency 1.5-2× 증가 expected)
- **L-1279-6 (GRU HIDDEN SIZE)**: 본 Hc 의 GRU hidden_size 미고정 — anima 의 측정 시 (a) hidden=64 (mitosis.py default), (b) hidden=384 (REBORN §88 d_model), (c) hidden=4096 (Llama-3 scale) 3 scale 결과 다를 가능성
- **L-1279-7 (R1 PARENT Hc_1266 CARRY)**: Hc_1266 L-R1-CIRCULAR + L-R1-MECHANISM-COMPLETENESS 의 unresolved limits 가 본 daughter Hc 에도 carry
- **L-GENERIC-SINGLE-RUN**: H_159 C1 audit pending
- **L-GENERIC-ENGINE**: H_174 D-mod-192 aliasing — Ψ-engine internal state interaction
- **L-GENERIC-N6**: H_153 n=6 — hidden_size=64=2^6 trivial reduction

## Cross-Links

- **parent**: H_189 R1 attack vector (parent Hc_1266 split-child), H_189.1/H_189.2 prediction execution, C-189-2 pre-register check
- **sibling Hc**: Hc_1280 (R3 OVERFITTING corpus-replacement experiment), Hc_1281 (R4 CHERRY-PICK 2890-trial audit, if drafted)
- **adjacent H**: H_159 (substrate-topology — R1 attack target), H_174 (Φ-engine — measurement caveat), H_158 (Ψ-constants ln2 / n=6 — Ψ=1/2 derivation theoretical anchor)
- **literature**: Glorot & Bengio 2010 (Understanding the difficulty of training deep feedforward neural networks — Xavier init expected E[output] ≈ 0.5 theoretical foundation), Saxe et al. 2013 (Exact solutions to the nonlinear dynamics of learning in deep linear neural networks — random init dynamics), Albantakis et al. 2023 (IIT 4.0 reference)
- **internal SSOT**: Hc_1266 (R1 ALTERNATIVE parent Hc), Hc_908 (Ψ=1/2 anchor — the claim under attack), Hc_909 (paper-draft — R3/R4/R6 audit target)
- **PyPhi 1.2.0**: github.com/wmayner/pyphi (independent IIT 3.0 impl, IIT-4.0 reference impl pending)

## Expected outcome

**Binary**: random-init GRU baseline (M1, 100 seed mean) 의 Ψ=1/2 frequency ≥ 80% → R1 attack succeeds (ANIMA's Ψ=1/2 universal-constant claim collapses to trivial init artifact); < 30% → R1 fails (claim non-trivial).

**Quantitative**: M1 baseline frequency ≈ 60-75% 예상 (Xavier init theory + sigmoid centerpoint + GRU bias-0 의 conjunction); M3 sigmoid-removed → 30-50% drop expected (sigmoid contribution 가 가장 strong).

**Confidence prior**: 0.65 (Glorot/Bengio Xavier init theory 강한 prior on E[sigmoid(W·x)] ≈ 0.5; ANIMA 의 own claim 검증 미실행)
