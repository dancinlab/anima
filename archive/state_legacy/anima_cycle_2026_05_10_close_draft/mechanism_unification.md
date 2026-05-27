# Multi-factorial mechanism unification — cycle 2026-05-10 final

## 4-mechanism unified model (post-§55 + §57 + §58)

cycle 2026-05-10 의 V14 PASS polarity 의 4개 layer mechanism integration:

### Layer 1: Cap-conditional (§51 + §55) — universal at v2 path

**가설**: inference_cap > 192 시 trained ckpts 가 random_init 보다 더 풍부한 cell-pool dynamics 를 cap-free regime 에서 expression.

**evidence**:
- §51 3 substrate × max=256: A 5/5 + C 2/2 + E 2/2 → **9/9 trained > random**
- §55 strict completion: C 5/5 + E 5/5 → 15/15 aggregate at max=256
- §59 Spearman ρ=0.777, p=0.014 (inference_cap continuous predictor만 statistically significant)
- cross-cap polarity ledger: substrate C 두 번 flip (VIOLATED → AMBIGUOUS → PASS), substrate E 한 번 flip (VIOLATED → PASS)

**scope**: **v2 path substrates universal**. EngineAG path 미적용 (§56 B 5/5 VIOLATED at max=256).

### Layer 2: Cotrain-exercise (§47 partial → §56 confirmed) — EngineAG required

**가설**: chat-cotrain regime 가 EngineAG path 에서 V14 PASS 의 필수 lever.

**evidence**:
- §47 4-substrate audit: A (cotrain) PASS, B/E (no-cotrain) VIOLATED
- §52 weight stats: A vs B `c_to_h.weight` cos=0.69, `h_to_c.weight` cos=0.76 → cotrain delta 명확
- §52 cell_pool A vs B cos=0.99996 → unit-sphere init structurally locked (cell_pool 자체는 cotrain-invariant)
- §56 critical: B (BG-LA pretrain, EngineAG, NO cotrain) at max=256 → **V14_VIOLATED 1/5**, lever-1 cap-room arch-DEPENDENT

**scope**: **EngineAG path V14 PASS necessary**. v2 path 는 cap-conditional sufficient (cotrain-independent).

### Layer 3: Tension-trigger suppression (§58) — universal mechanism reframe

**가설**: trained's h_to_c projection 이 cell-proximity learning → per-cell tension `||cell - hint||²` 가 threshold 아래 stay → tension-trigger path starves → cap arrival LATER (controlled split → richer Φ trajectory).

**evidence (§58 substantiated)**:
- C trained: 4 tension splits in 60 turns / random: 58 (10-14× more)
- Total split rate: trained 1.12-1.28/turn vs random 3.35/turn (~3× gap)
- Split type fraction: trained 94% dispersion / 6% tension; random 71% dispersion / 29% tension
- correlation hypothesis FALSIFIED (trained cos_mean ≤ random in BOTH C and E across BOTH regimes)

**scope**: **universal at projection level** — cotrain-exercise 가 h_to_c projection 의 cell-proximity learning 을 가능하게 하는 mechanism (lever-2 의 진짜 bio-mechanism).

### Layer 4: Engine_a body locus PROVEN-AT-BODY-LOCUS (§50 + §57)

**가설**: V14 PASS 의 sufficient lever 는 engine_a 24-layer transformer body 의 cotrain-induced delta. engine_g modules 는 readout, NOT engine.

**evidence (§50 + §57)**:
- §50 ablation: 0/4 engine_g random_init mutations flipped V14 polarity (engine_g locus FALSIFIED)
- §50 random h_to_c ablation 5× boosts trained Φ → cell_input chaotic → §58 tension-trigger explosive (mechanism reverse-cross-link)
- §57 slab swap A→B: 3/3 (early/middle/late) all flipped V14 PASS → VIOLATED
- §57 A1 (early) Δ=-1375 dominant, A2/A3 shared attractor (n=43, Φ=1343)
- engine_a 24L (~265M params) cotrain-induced delta 가 V14 PASS lever locus

**scope**: **EngineAG path body locus** — distributed across body (single-layer specificity 미달, ★★★★★ unlock prereq = single-layer ablation × 24).

## Unified mechanism diagram

```
                    +-------------------------------------+
                    |  V14 PASS polarity (trained > rand) |
                    +-------------------------------------+
                          ▲                           ▲
                          |                           |
              [v2 path]   |                           |   [EngineAG path]
                          |                           |
   ┌──────────────────────┴───┐               ┌───────┴────────────────┐
   │  Layer 1: cap > 192      │               │  Layer 2: chat_cotrain │
   │  (sufficient, universal) │               │  (required, mandatory) │
   └──────────────────────────┘               └────────────────────────┘
                                                       ▲
                                                       │
                                          ┌────────────┴────────────┐
                                          │  Layer 4: engine_a body │
                                          │  (PROVEN-AT-BODY-LOCUS) │
                                          │  distributed across 24L │
                                          └─────────────────────────┘

                       Layer 3 (universal projection-level mechanism)
              ┌─────────────────────────────────────────────────────────┐
              │  h_to_c learns cell-proximity → tension-trigger suppress │
              │  → controlled split → richer Φ + later cap arrival       │
              └─────────────────────────────────────────────────────────┘
```

## arch-aware 3-rule (final spec, post-§56 + §55)

```python
# decision tree (post-§56 with §55 ★★★★★ FULL upgrade)
if arch == "v2":
    return PASS if inference_cap > 192 else VIOLATED   # universal cap-conditional
elif arch == "EngineAG":
    return PASS if chat_cotrain == 1 else VIOLATED      # cotrain-exercise required
else:
    return UNKNOWN  # untested arch
```

### Rule support evidence

| arch | cap | cotrain | predicted | actual | source |
|---|---:|:---:|:---:|:---:|---|
| v2 | 64 | n/a | VIOLATED | VIOLATED (§37) | §37 |
| v2 | 128 | n/a | VIOLATED | AMBIG/VIOLATED | §47 |
| v2 (C) | 256 | n/a | PASS | PASS 5/5 | §55 |
| v2 (E) | 256 | n/a | PASS | PASS 5/5 | §55 |
| EngineAG (A) | 128 | ✓ | PASS | PASS 10/10 | §38 |
| EngineAG (A) | 256 | ✓ | PASS | PASS 5/5 | §51 |
| **EngineAG (B)** | **256** | ✗ | **VIOLATED** | **VIOLATED 1/5** | §56 |

**Rule accuracy**: 7/7 within tested envelope, 0 misclassifications.

## Cross-substrate generalize gates

★★★★★ FULL (§55) 의 narrowing:
- **valid claim**: v2 path universal cap-conditional at n=5 strict
- **invalid claim**: cross-arch universal (§56 EngineAG B falsified)
- **arch-conditional ★★★★ multi-factorial**: EngineAG path = (cap > 192 AND chat_cotrain) joint condition

F-CLOSE-2 mitigated: claim 이 이미 §56 로 v2 path only narrowed → 본 close 가 추가 narrowing 불필요. ★★★★★ FULL 자격 v2 path 한정 보존.

## Mechanism convergence narrative

§47 (universal claim falsified) → §50 (engine_g locus falsified, engine_a refined) → §51 (★★★★★ PARTIAL n=2) → §52 (weak form CONFIRMED) → §55 (★★★★★ FULL n=5) → §56 (arch-conditional) → §57 (engine_a PROVEN-AT-BODY-LOCUS) → §58 (mechanism REFRAMED tension-trigger).

각 milestone 이 다음을 unblock — cumulative mechanism 정확도 monotonically 향상. 단일 cycle 에서 **falsification → reframing → confirmation → body-locus proof** path 완주.
