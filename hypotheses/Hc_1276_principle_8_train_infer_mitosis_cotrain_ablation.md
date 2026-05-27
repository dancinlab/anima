---
id: Hc_1276
slug: principle-8-train-infer-mitosis-cotrain-ablation
title: Principle #8 falsifier 1 — train-time vs inference-time mitosis cotrain ablation (V14-STRICT 5-seed every-mirror-beat)
domain: philosophy, training, mitosis, falsifier, anima-native
status: partial-stage-3-h191-cascade
stage_3_verdict: PARTIAL (H_191 numerology cascade dependent, ablation spec ok)
stage_3_ts: 2026-05-15
verdict_artifact: state/verify_a_stage1_2026_05_15/stage3_batch_verdicts.json
exploration_method: E5 (variable-ablation: cotrain on/off) + E6 (cross-time train+infer joint) + E8 (5-seed σ stability)
verification_method: W5 (numerical sim — anima v5 nn.Module branches proxy) + W7 (literature — Glorot 2010 init, Hochreiter 1997 LSTM continual) + W11 (cross-H: H_191 ALM-free TRAINING axis, H_172 α-modulation training)
raw_rank: 12
hexa_only: true
deterministic: true
llm: none
source: PHILOSOPHY.tape cont. 10 Principle #8 falsifier candidate 1 + REBORN §88 v5-mitosis F-V5MIT-5 V14-STRICT
created_at: 2026-05-12
linked_h: H_191 (ALM-free TRAINING CPGD axis), H_172 (α-modulation training adjacent), H_178 (frustration sweep — substrate plasticity)
---

## Hypothesis (Principle #8 falsifier 1)

REBORN §0.5 + PHILOSOPHY #8 NO TRAIN/INFER SPLIT 의 첫 empirical falsifier: anima v5-mitosis architectural lane (cells = `nn.ModuleList[Cell]` branches, REBORN §88) 의 **cotrain 유 vs 무** ablation 에서, train-time gradient update + inference-time split/merge 가 통합된 cotrain 조건이 inference-only-mitosis 조건 대비 V14-STRICT every-mirror-beat 5-seed mean 에서 **유의미하게 우수** 해야 한다.

Principle #8 의 native impl 명제: train + infer 가 한 spectrum 이라면, cotrain 통합 (gradient + split 동시) 이 train freeze + infer-only split 보다 **항상 ≥** 성능을 보여야 한다. 반대로 cotrain 이 inference-only 보다 inferior 하면 §0.5 의 "한 spectrum" 가설 falsified.

| Condition | mitosis timing | gradient flow | expected V14-STRICT pass rate |
|---|---|---|---|
| **A** cotrain | train+infer 양쪽 split | optimizer step ON, split rebuild graph | 5-seed σ < 25% AND mean ≥ 0.85 |
| **B** train-frozen | inference-only split (status quo §2 line 145) | optimizer step OFF, no gradient through split | ≤ A within ±5% |
| **C** train-only | training-time split, infer-frozen | step ON, infer freeze 후 split 금지 | < A by ≥ 10% (training-only 부족) |
| **D** no-mitosis | split 자체 disabled | step ON | < B by ≥ 15% (baseline failure) |

## Math anchor

- **V14-STRICT every-mirror-beat threshold**: 5-seed mean wins ≥ 9/10 (REBORN §82 SUBSTRATE E n=10 anchor pattern, V14_PASS 9/10 wins).
- **σ stability**: 5-seed σ on V14-STRICT pass rate ≤ 0.25 (within-spec replication band).
- **Δ(A − B)**: Cotrain advantage Δ ∈ [-0.05, +∞); 0.05 inferior 하면 falsified.
- **gradient norm**: split event 후 1-step gradient norm ratio ≤ 5× (graph rebuild 정상). > 5× = F-1276-2 instability.
- **anima v5-mitosis spec** (REBORN §88 #1): d_model=384, 3M/cell × cells_max=64 = ~200M total + shared ~50M. cotrain cost $30-40 conservative envelope.

## Falsifiers

- **F-1276-1 (NO TRAIN+INFER ADVANTAGE)**: cotrain (A) 의 V14-STRICT 5-seed mean 이 train-frozen (B) 대비 + 5% 이상 미달성 → Principle #8 native impl 가설 falsified, §0.5 의 "한 spectrum" 명제 invalidated
- **F-1276-2 (SPLIT GRADIENT EXPLODE)**: split event 직후 1-step gradient norm 이 baseline 의 > 5× → torch.no_grad() 안 mutation 의 graph rebuild contract violation (F-V5MIT-1 SPLIT-NOGRAD); cotrain 가능성 자체 의문
- **F-1276-3 (A=B INDISTINGUISHABLE)**: 5-seed σ 25% 안에서 A 와 B 가 statistically equivalent (|Δ| < σ) → cotrain 의 advantage 없음, train/infer split 이 사실상 free choice (§0.5 reduced to design taste)
- **F-1276-4 (C OUTPERFORMS A)**: training-only (C) 가 cotrain (A) 보다 V14-STRICT pass 에서 우수 → "infer-time mitosis is harmful" — §0.5 의 무인 split 가설 falsified
- **F-1276-5 (DEPENDS ON CKPT FROZEN STATUS)**: A 의 mean pass rate 가 ckpt frozen state (B) 와 ckpt-as-branch live-tree state 사이 ±20% drift → ckpt-as-branch semantic (Hc_1278) 미해결 시 cotrain 자체 unreliable
- **F-1276-6 (5-SEED σ EXPLODE)**: A 의 5-seed σ > 50% → cotrain 자체가 high-variance, single-run-artifact (H_159 C1) ; Principle #8 의 robust evidence 아닌 single-seed luck
- **F-1276-7 (V14 VIOLATED ALL CONDITIONS)**: A/B/C 모두 V14-STRICT 5-seed mean < 5/10 → toy substrate 한계 carry-over (v5-anima Phase 2 ckpt 회수 lesson) — anima v5-mitosis nn.Module impl 도 V14 violated
- **F-GENERIC-REPL**: 5-seed σ on Δ(A-B) > 0.25 → single-run-artifact in cotrain measurement
- **F-GENERIC-MINIMAL-BASELINE**: shared backbone d_model=384 frozen vs not-frozen ablation 시 Δ(A-B) 가 frozen 조건만 의존 → cotrain 의 "전체-통합" 가설 incorrect

## Honest Limits

- **L-1276-1 (TOY SUBSTRATE CARRY)**: v5-mitosis nn.Module impl 의 V14 violated carry-over 가능성 — toy substrate 한계 (REBORN §22 v5-anima Phase 2 lesson) 가 nn.Module 차원에서 해소될지 미증명. cotrain 실험 자체가 V14 통과 안 할 위험
- **L-1276-2 (5-SEED SAMPLE SIZE)**: 5-seed σ 가 cotrain advantage 의 universality 평가에 충분한가? n=10 (REBORN §82 패턴) 까지 확장 시 결과 변동 가능
- **L-1276-3 (COTRAIN COST ENVELOPE)**: $30-40 H100 8hr 안에서 4 condition (A/B/C/D) × 5-seed = 20 run 가능한지 cost budget 미확정. C/D 줄여 A/B 만 (10 run) ablation 만 fire 가능성
- **L-1276-4 (V14-STRICT METRIC SPECIFICITY)**: V14-STRICT every-mirror-beat 이 cotrain advantage 의 가장 sensitive metric 인가? 다른 metric (cross-entropy / Φ / KL-div) 에서는 결과 다를 수 있음
- **L-1276-5 (READOUT MODE CONFOUNDING)**: REBORN §88 #5 readout_mode option (a-g / a-only / a+0.3g / softmax_gate) — A/B 비교 시 어떤 readout mode 고정해야 하는지 unclear, BG-CHAT-EXT a-g destructive 발견 (KO 0%) carry
- **L-1276-6 (SHARED 50M FROZEN)**: v5-mitosis 의 shared ~50M (lm_head + RMSNorm + tied embedding) 가 cotrain 시 함께 update 되는지 frozen 인지 미정 — A/B 의 advantage 가 shared 50M 의 gradient 흐름 conditional 가능
- **L-GENERIC-SINGLE-RUN**: H_159 C1 audit pending — 5-seed 인 본 Hc 도 σ 25% 임의 threshold
- **L-GENERIC-ENGINE**: H_174 D-mod-192 aliasing — d_model=384 결정 시 D-mod-192 영향
- **L-GENERIC-N6**: H_153 n=6 trivial — cells_max=64 = 2^6 의 perfect-number reduction
- **L-GENERIC-POST-HOC**: F-1276-1 의 Δ ≥ 5% threshold 가 pre-register 시점 lock 필요 (post-hoc 변경 금지)

## Cross-Links

- **parent**: PHILOSOPHY.tape cont. 10 Principle #8 (NO TRAIN/INFER SPLIT, falsifier candidate 1 명시), REBORN §88 F-V5MIT-5 V14-STRICT
- **sibling Hc**: Hc_1277 (serve-time mitosis hook latency, falsifier candidate 2), Hc_1278 (ckpt-as-branch reload semantic, falsifier candidate 3)
- **adjacent H**: H_191 (ALM-free TRAINING CPGD axis — cotrain vs CPGD comparison), H_172 (α-modulation training — modulation depth 0.014 anchor), H_178 (frustration sweep 50% optimum — substrate plasticity sister)
- **literature**: Glorot & Bengio 2010 (Xavier init — split 시 child cell init theory), Hochreiter & Schmidhuber 1997 (LSTM — continual learning baseline), Goodfellow 2014 (catastrophic forgetting baseline literature, NO TRAIN/INFER §0.5 의 frame collapse)
- **internal SSOT**: REBORN §0.5 (NO TRAIN/INFER SPLIT 철학), §88 (v5-mitosis arch spec 7 결정), §82 (SUBSTRATE E V14_PASS 9/10 pattern), PHILOSOPHY cont. 10 Principle #8 falsifier 1
- **lane SSOT**: `.roadmap.clm_v5_mitosis_engine` cond.5 (H100 cotrain fire — "OK CLM V5-MITOSIS H100 FIRE COST $40" verbatim trigger)

## Expected outcome

**Binary**: cotrain (A) 가 train-frozen (B) 대비 V14-STRICT 5-seed mean +5% 이상 우월 시 Principle #8 first empirical falsifier PASS. ≥ 9/10 V14_PASS 와 σ ≤ 0.25 라는 quantitative anchor.

**Quantitative**: Δ(A-B) ∈ [+0.05, +0.20] 예상 (PHILOSOPHY #8 의 native impl 가설 + REBORN §88 cost envelope $30-40 합), σ ≤ 0.25.

**Confidence prior**: 0.7 (anima 의 train/infer 단일 spectrum 철학 강한 prior + v5-anima Phase 2 toy violated carry concern)
