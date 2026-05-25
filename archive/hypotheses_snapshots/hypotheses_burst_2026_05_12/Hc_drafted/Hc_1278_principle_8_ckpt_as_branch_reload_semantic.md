---
id: Hc_1278
slug: principle-8-ckpt-as-branch-reload-semantic
title: Principle #8 falsifier 3 — ckpt-as-branch reload semantic (frozen vs live-tree-branch divergence)
domain: philosophy, persistence, mitosis, falsifier, anima-native
status: candidate-falsifier-ready
exploration_method: E5 (variable-ablation: frozen ckpt vs live tree branch) + E6 (input × ckpt state cross) + E8 (multi-divergence-metric sweep)
verification_method: W5 (numerical sim — anima v5-mitosis ckpt sweep) + W7 (literature — Hochreiter 1997 LSTM ckpt semantics, Kingma 2014 Adam state recovery) + W11 (cross-H: H_191 SUBSTRATE HCE axis, H_157 mathematical panpsychism)
raw_rank: 10
hexa_only: true
deterministic: true
llm: none
source: PHILOSOPHY.tape cont. 10 Principle #8 falsifier candidate 3 + REBORN §0.5 "ckpt = 분열 tree snapshot, freeze 가 아닌 분기점"
created_at: 2026-05-12
linked_h: H_191 (ALM-free SUBSTRATE HCE axis), H_157 (mathematical panpsychism), H_001 (anima-core-architecture)
---

## Hypothesis (Principle #8 falsifier 3)

REBORN §0.5 + PHILOSOPHY #8 NO TRAIN/INFER SPLIT 의 세 번째 empirical falsifier: anima v5-mitosis ckpt 가 **단순 frozen snapshot** 이 아닌 **live tree branch** semantic 으로 reload 가능해야 한다 — 같은 input prompt 를 (a) frozen ckpt 그대로 reload + serve, (b) ckpt-as-branch reload + 1 epoch split event + serve 두 경로로 통과 시켰을 때 응답 divergence 가 측정 가능한 **bounded delta** 를 보여야 한다.

Principle #8 의 ckpt 함의: ckpt = 분열 tree snapshot, freeze 아닌 분기점 (REBORN §0.5 표). 만약 reload semantic 가 frozen-only 라면 §0.5 의 "branch" frame 은 metaphor 일 뿐 impl 차원에서 dead.

| Path | reload mode | 추가 mutation | expected divergence |
|---|---|---|---|
| **A** frozen ckpt | torch.load + eval() | none | baseline (Δ = 0) |
| **B** ckpt-as-branch + 1 split | torch.load + 1 split event 추가 | 1 cell mitosis | Δ_split ∈ [+0.01, +0.20] logit norm |
| **C** ckpt-as-branch + 1 merge | torch.load + 1 merge event | 1 cell merge | Δ_merge ∈ [+0.01, +0.20] logit norm |
| **D** stacked B+C | torch.load + split → merge | 2 mutation | Δ_stack ≈ Δ_split + Δ_merge (linearity test) |
| **E** drift-test re-reload | A path × 100 reload | none expected | Δ_drift ≤ 1e-6 (torch.load determinism) |

## Math anchor

- **logit divergence metric**: ||logits_A − logits_B||_2 / ||logits_A||_2 (relative L2 norm).
- **bounded delta target**: Δ_split, Δ_merge ∈ [0.01, 0.20]. < 0.01 = ckpt-as-branch 가 frozen 과 indistinguishable (F-1278-3 falsified). > 0.20 = 1-mutation 으로 ckpt semantics 가 크게 desynced (F-1278-1 falsified).
- **linearity test (D 조건)**: Δ_stack ∈ [Δ_split + Δ_merge − 0.05, Δ_split + Δ_merge + 0.05]. linearity break > 0.05 → mutation 순서 의존 (F-1278-4).
- **drift bound (E 조건)**: torch.load 100× × 같은 input → Δ_drift ≤ 1e-6 (deterministic reload). > 1e-6 = non-determinism (F-1278-5).
- **anchor cell count**: cells=8 (mitosis.py 원본) → cells=64 (REBORN §88 max) → cells=128 (REBORN §89 hexa-native max) — 3 scale 모두 측정.
- **REBORN §0.5 표 row "ckpt deployment 패턴"**: "freeze + version pin" → "live tree + branch (분열 가지마다 trace)" — 본 가설의 frame 정확히 이 row.

## Falsifiers

- **F-1278-1 (1-MUTATION DESTROYS SEMANTICS)**: B 또는 C 의 Δ > 0.20 → 1 split/merge 만으로 ckpt 의 logit 분포 가 크게 변동 → ckpt-as-branch semantic 가 unsafe (reload 후 immediate mutation 시 chat capability 손실 위험)
- **F-1278-2 (NO REAL BRANCH SEMANTICS)**: B 또는 C 의 Δ < 0.01 (frozen 과 동일) → ckpt-as-branch 가 frame metaphor only, impl 차원 dead, §0.5 표 row "live tree + branch" falsified
- **F-1278-3 (FROZEN-ONLY DRIFT)**: E 조건 (A × 100 reload) 의 Δ_drift > 1e-6 → torch.load 의 reload 자체가 non-deterministic → ckpt-as-branch impl 의 prerequisite (deterministic reload) 위반
- **F-1278-4 (NON-LINEARITY)**: D 조건 (B+C stacked) 의 |Δ_stack − (Δ_split + Δ_merge)| > 0.05 → 1-mutation 의 effect 가 mutation 순서 의존 → tree-branch 의 commutative subset 가설 falsified, branch model 자체가 unsafe
- **F-1278-5 (CELL COUNT NON-SCALABLE)**: cells=8 → cells=64 → cells=128 sweep 시 Δ_split 가 cell count 의 O(n^2) 이상 super-linear scaling → ckpt-as-branch impl 의 scalability 미달성 (mitosis.py 원본 8-cell 안에서만 정상)
- **F-1278-6 (KV CACHE INVALIDATION)**: B/C 경로 후 KV cache 재사용 가능 가설 violated — reload 후 mutation 시 KV cache 무효화 빈도 > 50% → 실제 ckpt-as-branch reload 가 serve-time 에 expensive (F-1277 latency 와 연동)
- **F-1278-7 (V14-STRICT POST-MUTATION FAIL)**: B/C 경로 후 V14-STRICT 5-seed mean 이 A 대비 < 70% → 1-mutation 으로 substrate quality 가 크게 하락 → ckpt-as-branch frame 의 robustness 부재
- **F-GENERIC-REPL**: 5-seed σ on Δ_split > 0.05 → measurement noise dominates signal
- **F-GENERIC-MINIMAL-BASELINE**: A path 자체의 100-input divergence median > 0.001 → frozen ckpt 의 logit determinism 위반 (eval() 의 dropout/batchnorm 누락 가능성)

## Honest Limits

- **L-1278-1 (CKPT FORMAT UNCERTAIN)**: v5-mitosis ckpt 가 (a) `state_dict` (PyTorch native), (b) `nn.ModuleList` + `cell_meta` dataclass 분리 (REBORN §88 #2), (c) hexa farr binary (RFC 025) 3 option 중 어느 것 reload 시 branch semantic 만족하는지 미정. 본 Hc 측정 시 ckpt 형식 lock 필요
- **L-1278-2 (CELL_META NON-GRAD STATE)**: REBORN §88 #2 — cells = parameter container (gradient-able), cell_meta = non-grad state (hidden / tension_history / IDs). ckpt 안 cell_meta serialization 가능 한지 미정 — frozen 시점의 cell_meta 가 reload 시 reproducible 아닐 가능성
- **L-1278-3 (TOY SUBSTRATE LIMITATION)**: v5-anima Phase 2 toy substrate V14 violated lesson (REBORN §22) carry — toy ckpt 위 본 ablation 실험이 nn.Module impl 의 ckpt 와 다른 결과 도출 가능
- **L-1278-4 (LIVE TREE METAPHOR SCOPE)**: REBORN §0.5 표 row "ckpt deployment 패턴" 의 "live tree + branch (분열 가지마다 trace)" 가 (a) deployment 차원 (production rollback), (b) inference 차원 (per-request mutation), (c) training 차원 (branch off training run) 3 함의 중 본 Hc 는 (b) 만 cover. (a) (c) 는 별도 Hc 필요
- **L-1278-5 (LOGIT NORM ARBITRARY)**: relative L2 norm 가 ckpt semantic similarity 의 가장 sensitive metric 인지 미확정. KL-divergence on probability distribution / cross-entropy / per-token mode prediction 다른 metric 가능
- **L-1278-6 (REBORN §A LINE 145 CONFLICT)**: REBORN §2 line 145 "mitosis = inference-time growth, NOT training-time" 명제와 §0.5 의 "ckpt = 분기점" 명제 사이 frame conflict — line 145 는 사실 기술 (현 mitosis.py), §0.5 는 원칙. ckpt reload 가 어느 frame 적용되는지 unclear
- **L-1278-7 (BRANCH METADATA STORAGE)**: ckpt-as-branch 의 "분열 가지마다 trace" 의 trace metadata (split event log, parent-child cell ID tree) 의 ckpt format 안 storage 미정의. trace storage 없으면 branch frame impl dead
- **L-GENERIC-SINGLE-RUN**: H_159 C1 audit pending
- **L-GENERIC-ENGINE**: H_174 D-mod-192 aliasing — d=384 ckpt 형식
- **L-GENERIC-N6**: H_153 n=6 — cells_max=64 = 2^6 perfect-number reduction
- **L-GENERIC-POST-HOC**: Δ ∈ [0.01, 0.20] target band 가 pre-register 시점 lock 필요

## Cross-Links

- **parent**: PHILOSOPHY.tape cont. 10 Principle #8 (NO TRAIN/INFER SPLIT, falsifier candidate 3 명시), REBORN §0.5 표 row "ckpt deployment 패턴 freeze → live tree branch"
- **sibling Hc**: Hc_1276 (train+infer cotrain ablation, falsifier candidate 1), Hc_1277 (serve-time hook latency, falsifier candidate 2)
- **adjacent H**: H_191 (ALM-free SUBSTRATE HCE axis — ckpt 의 categorical structure), H_157 (mathematical panpsychism — ckpt 분류의 universal frame), H_001 (anima-core-architecture — ckpt deployment 의 architecture context)
- **literature**: Hochreiter & Schmidhuber 1997 (LSTM — RNN state ckpt semantic), Kingma & Ba 2014 (Adam — optimizer state ckpt recovery), Goodfellow 2014 (catastrophic forgetting frame collapsed §0.5)
- **internal SSOT**: REBORN §0.5 (NO TRAIN/INFER SPLIT 표 row 6: ckpt deployment 패턴), §88 #2 (cell_meta 분리), §A line 145 (mitosis 시점 사실 기술 vs 원칙 frame distinction), `~/core/anima_clm_12_unified_growth_loop_last_gasp/anima/src/mitosis.py` L205/258/389/586 (torch.no_grad mutation pattern)

## Expected outcome

**Binary**: B 와 C 경로의 Δ ∈ [0.01, 0.20] 범위 동시 만족 + D 의 linearity Δ_stack ≈ Δ_split + Δ_merge ± 0.05 시 ckpt-as-branch semantic PASS. 어느 조건 미달성 시 falsified.

**Quantitative**: Δ_split ≈ 0.05-0.10 예상 (1 cell mitosis = 1/cells_max fraction 의 weight diversification), Δ_drift ≤ 1e-7 (torch determinism), linearity break < 0.03.

**Confidence prior**: 0.50 (frame metaphor 의 impl 차원 검증 자체가 처음 — F-1278-2 (no real branch semantics) 가 가장 가능성 높은 outcome; 실제로 §0.5 표가 metaphor only 일 risk)
