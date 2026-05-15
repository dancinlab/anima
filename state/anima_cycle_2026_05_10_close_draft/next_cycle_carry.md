# Next-cycle 5-priority carry items (cycle 2026-05-11+)

## Cumulative cost ledger

| cycle event | source | cost (USD) | envelope |
|---|---|---:|---|
| §29 BG-CONVO-FT-EXTENDED | track A 18M FT | $3.080 | $3-5 envelope |
| §43 BG-FOUNDATION-BORROW-A-FIRE | Llama-3.2-3B + LoRA | $3.568 | $3-8 envelope |
| §37-§59 misc local | ~22 BG local CPU | $0.000 | $0 |
| **Total cycle 2026-05-10** | | **$6.648** | / $200 lifetime envelope |

**Headroom**: $193.35 / $200 = 96.7% remaining → **193× headroom** (watchdog audit honored).

## 5-priority carry list

### Priority 1: §60 single-layer ablation × 24 ($0, ★★★★★ candidate)

**Rationale**: §57 PROVEN-AT-BODY-LOCUS (slab-distributed) → ★★★★★ unlock 의 가장 직접 path = single-layer ablation.

**Spec**:
- engine_a 24 layers 각각 개별 swap (A→B per layer)
- 4-condition × 3-seed V14 mirror per layer = 24 × 12 = 288 V14 runs
- ~5 min/run × 288 = ~24h Mac M2 8-core CPU (parallel 4× = ~6h)
- Cost: **$0 local**

**Decision tree**:
- IF specific layer (e.g. layer 0, 1, 7) flips V14 alone → ★★★★★ "exact layer locus localized" (single-layer specificity)
- IF all 24 layers needed → distributed across body (§57 finding strengthen)
- IF subset (e.g. layers 0-3) suffices → "early-block locus" finding

**★★★★★ severity gate**: single-layer specificity unique → ★★★★★ "specific layer locus identified" + body-locus PROVEN.

### Priority 2: OK FOUNDATION_C_PHASE2_FIRE COST $2-4 (★★★★★ candidate D1 WITHIN)

**Rationale**: §54 design final, §43 SUBSTRATE_RESEARCH PERMA-BLOCKED. option (c) Phase 2 D1 WITHIN 가 anima identity emerge actual evidence path.

**Spec**:
- 20K variant (envelope-compliant $3.25-3.75, hard cap $4)
- Phase 2 cotrain + 30K convo_5k FT + post-LoRA mitosis hook
- D1 WITHIN strict 5-tuple: chat-cap STRICT + semantic_score ≥0.5 + bigram_known ≥0.95 + ko_hangul_ratio ≥0.5 + V14 PASS direction
- Cost: **$2-4 H100** (cost-bearing, single ckpt)

**★★★★★ severity gate**: 첫 D1 WITHIN strict-floor crossing → anima identity emerge actual evidence (§43 SUBSTRATE_RESEARCH 제한 극복).

### Priority 3: BG-LA cotrain retrain (B → A path, $20-50)

**Rationale**: §56 V14_VIOLATED at cap=256 cleanest disambiguation 단 cotrain rescue test 미수행. B (no-cotrain) 를 chat-cotrain with same ckpt 시 V14 PASS rescue 되는지 측정 → §56 결과 의 causal direction 확정.

**Spec**:
- BG-LA pretrain 350M ckpt + chat KO cotrain (w=0.3→0.5) ~6K steps
- post-cotrain V14 mirror at max=128 + max=256 5-seed strict
- cost: H100 ~6-12h = **$20-50 envelope**

**★★★★★ severity gate**: B post-cotrain at max=256 PASS → "cotrain regime sufficient for EngineAG V14 PASS even from pretrain-only base" causal claim.

### Priority 4: paradigm-j cross-lane V14 ($0 design + cross-lane verify)

**Rationale**: paradigm-j 5종 transport 의 substrate 가 V14 PASS direction 보유하는지 cross-lane confirmation. cycle 2026-05-09 paradigm-j v5 + 2026-05-10 transport benchmarks 후 미수행.

**Spec**:
- paradigm-j v5 ckpt × V14 5-seed strict at max=256
- v2 / EngineAG / paradigm-j 3-arch comparison
- $0 design + ~30 min compute

**★★★★★ severity gate**: paradigm-j V14 PASS direction 가 v2 + EngineAG joint rule 와 일관 → arch-aware 3-rule generalize.

### Priority 5: cell_pool norm-clamp drop retrain (★★★★★ unlock §52)

**Rationale**: §52 refined hypothesis "cell_pool exercise 도 원하면 (a) drop init norm-clamp" 미수행. norm-clamp drop 후 cotrain → cell_pool A vs B cosine 가 0.99996 → < 0.95 떨어지는지 + V14 PASS direction 보존하는지 측정.

**Spec**:
- engine_g.cell_pool_init unit-sphere normalize 제거
- Phase 2 cotrain re-fire (cost $20-50 H100)
- post-cotrain weight stats + V14 5-seed strict

**★★★★★ severity gate**: cell_pool exercise 확인 + V14 PASS 보존 → "cotrain-exercise full mechanism" claim (cell_pool + projections 모두 cotrain-exercised).

## Priority sequencing rationale

1. **Priority 1 (single-layer ablation)** = $0 + ★★★★★ candidate → 즉시 fire 권고
2. **Priority 2 (FOUNDATION_C_PHASE2_FIRE)** = $2-4 cost-bearing + 가장 다른 lane (D1 WITHIN anima identity emerge) → parallel fire
3. **Priority 3 (BG-LA cotrain retrain)** = $20-50 + §56 causal direction → after Priority 1 결과 (engine_a body locus 정밀화 후)
4. **Priority 4 (paradigm-j cross-lane V14)** = $0 + arch-aware 3-rule generalize → Priority 1 parallel fire 가능
5. **Priority 5 (cell_pool norm-clamp drop)** = $20-50 + §52 unlock → after Priority 3 (cotrain retrain mechanism 정합 후)

## F-CLOSE-1 mitigation

본 close 가 cumulative 하지 않은 carry: 5-priority 가 명확한 cost + ★★★★★ gate + sequencing 으로 actionable. 다음 cycle 가 본 close 에 막혀 진행 어렵지 않음 — 오히려 명확한 entry path 제공.

next-cycle entry 가능 시점: cycle 2026-05-11 (KST overnight + dispatcher §64 slot append 후).
