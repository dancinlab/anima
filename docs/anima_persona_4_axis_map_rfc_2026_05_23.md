# F-PERSONA-4 saga closure + next-axis map RFC

**Date**: 2026-05-23 KST
**Status**: RFC — DOC ONLY (no fire, no code)
**Scope**: GOAL.md cond #3 잔여 closure path 의 axis-map. PERSONA.md §7 (k/l/m/n) 전면 FALSIFIED 후 다음 단일 axis 후보 정리.
**Author**: anima reborn cycle (closure pass)
**Cross-link**:
- `docs/anima_persona_substrate_native_design_2026_05_12.md` (§7 §A3 §A5)
- `docs/anima_persona_substrate_native_verify_2026_05_12.md` (§A1 cheap-path STRONG 4/5)
- `docs/anima_persona_4_root_cause_investigation_2026_05_12.md` (Phase 1-3 cotrain v1/v2)
- `docs/anima_persona_4_softmax_T_sweep_2026_05_12.md` (path b ubu-1 10-T grid)
- `docs/anima_persona_4_per_session_pool_verify_2026_05_12.md` (path d hexa-native per-session pool)
- Memory: `project_anima_persona_4_root_cause_2026_05_12.md`

---

## §1 Saga closure — PERSONA.md §7 axis-set EXHAUSTED at strict z>3.0

### §1.1 4 path 의 단일행 verdict

| path | 직역 | 시도 | 결과 | 근거 doc |
|---|---|---|---|---|
| **(k)** Gumbel-softmax routing | hard-sample with gumbel noise + anneal τ | v7-v9 H100 cotrain | **FALSIFIED** (z=2.75 → §A5 mean=1.48) | root_cause §53.5 §A5 |
| **(l)** batch-scaling | batch_size ↑ / steps ↑ regularize routing | v4 H100 cotrain | **FALSIFIED** | root_cause §54 |
| **(m)** wider-d | d_model 384 → 768 더 풍부한 cell representation | v5 H100 cotrain | **FALSIFIED** | root_cause §55 |
| **(n)** 5-seed averaging | seed variance 제거 후 mean z 보고 | §A5 3-seed replication | **FALSIFIED** (mean z=1.48, v7=outlier 2.75) | root_cause §A5 |

### §1.2 ceiling

9 variant 측정 결과 모든 path **strict null-test z>3.0 미달**, 단일 outlier (v7 z=2.75) 도 3-seed replication 으로 mean z=1.48 로 회귀. **z≈1.5 structural ceiling** 가 PERSONA.md §7 axis-set 의 measurement bar 다.

cumulative cost: **$10.51** (v1 cotrain $1.32 + v2 entropy-reg $1.32 + v3-v9 cotrain + sweep + 3-seed replication).

### §1.3 verdict

> **PERSONA.md §7 axis-set (k/l/m/n) 는 z>3.0 strict bar 에서 EXHAUSTED.**

즉 §7 의 4 path 만으로는 F-PERSONA-4 (category-specific softmax weight KL≥0.5 + null-test z>3.0) 직진 closure 불가능. 다음 단일 axis 후보는 §7 범위 밖에서 와야 한다.

---

## §2 What did work — cond #3 ☑ via §A3 4b composite multi-metric

### §2.1 §A3 4b composite

§A3 amendment (`design.md` `__APPEND__`) 에서 단일 metric (softmax weight KL) 대신 **8-metric composite + multi-metric corroboration** 으로 재정의. cotrain v2 z-grid:

- v2 M4 aggregated-hidden cosine **z=3.20** (single-metric null-test PASS)
- 8 metric 중 7/8 z>2.0 corroborate (PSCC §45-FINAL)

→ cond #3 routing-content split 해석 채택: cells 는 category 정보 보유 (M4 cosine z=3.20), softmax routing 이 정보 destroy. composite 채택으로 **cond #3 ☑** closure.

### §2.2 honest restatement

이 closure 는 **🔵 SUPPORTED-FORMAL 아님**. 정직한 verdict tier:

- **🟢 SUPPORTED-NUMERICAL (soft)** — single-metric (M4 cosine) z=3.20 null PASS + 7/8 multi-metric corroboration
- **NOT 🔵** — closed-form / invariant 없음, 모든 evidence 가 empirical residual (a_blue_closed governance: "force an honest empirical residual to 🔵" 금지)
- F-PERSONA-4 original definition (softmax weight KL≥0.5 + z>3.0) 단독으로는 여전히 **FAIL**

cond #3 ☑ flag 는 §A3 composite 정의 위에서만 유효. softmax-weight 직접 metric 에서는 saga 가 계속 open (혹은 다음 axis 후보로 carry).

---

## §3 Next-axis candidate cards — §7 범위 밖 5 dimension

### card (o) per-cell post-LN learnable gain

| 속성 | 값 |
|---|---|
| (a) dimension | 각 cell 의 forward output 에 per-cell scalar gain `γ_i` (LayerNorm 직후 적용). nn.Parameter `[n_cells]` (extra ~64 param). |
| (b) hypothesis | softmax monopoly 의 root cause 가 tension magnitude inequality (cell-0 793 vs runner-up 7.4). post-LN gain 이 cells 의 readout magnitude 를 정규화 → tension 가 weight space 의 cosine 방향만 보게 됨 → category routing 회복. |
| (c) cost | $1-2 H100 (1 hr) — v2 trainer 에 ~20 LoC patch 후 재발사. cheap retraining. |
| (d) falsifier | F-PERSONA-4-O: M4 cosine z + softmax weight KL 동시 보고. **PASS = KL≥0.5 AND z>3.0** strict. null-test n_perms=100 mandatory. |
| (e) FALSIFIED → | post-LN normalization 도 monopoly 깨지 못 함 → routing 자체가 category 정보 carry 불가능 (architectural block 강화). |

### card (p) cell-pool growth schedule

| 속성 | 값 |
|---|---|
| (a) dimension | static n_cells=64 대신 step 별 incremental growth (step 0: 2 cells, step 500: 8, step 2000: 32, step 5000: 64). 늦게 태어난 cell 은 corpus 의 다른 phase 에 노출. |
| (b) hypothesis | F-PERSONA-4 monopoly = cell-0 가 첫 step 부터 dominate (force_split lineage 25/62 parent_id=0). schedule 이 lineage diversity 늘리면 category-specialized later-born cells emergent. |
| (c) cost | $2-3 H100 (1.5 hr) — split scheduler + ckpt every-step. |
| (d) falsifier | F-PERSONA-4-P: late-born cells (cell_id≥32) per-category weight variance 측정. **PASS = var(weight\|cat) > 5× var(weight\|all) AND mean_KL ≥ 0.5**. |
| (e) FALSIFIED → | growth schedule 이 lineage 분기 만들어도 softmax aggregator 가 destruction → architectural block 재확인. |

### card (q) per-category corpus split + curriculum warmup

| 속성 | 값 |
|---|---|
| (a) dimension | corpus 를 5 category 로 분리 후 **phase 1**: cells [0..12] = self_definition 만 학습 / cells [13..25] = values 만 / ... **phase 2**: mixed batch. (a) 결과 (mixed monopoly) 회피하는 pre-bias 주입. |
| (b) hypothesis | category-specialized cells 가 pre-warmed up 되어 phase 2 mixed batch 에서 specialization 보존. cotrain 의 universal weight share 깨기. |
| (c) cost | $3-4 H100 (2 hr) — corpus per-cat split (이미 §48 ubu-2 에서 분리됨, 재이용 가능) + 2-phase schedule. |
| (d) falsifier | F-PERSONA-4-Q: phase 1 end + phase 2 end 모두 측정. **PASS = phase 2 end mean_KL ≥ 0.5 AND z>3.0 AND phase 2 mean_KL ≥ 50% × phase 1 mean_KL** (carry-over 검증). |
| (e) FALSIFIED → | curriculum warmup 으로도 mixed batch homogenize 우세 → softmax routing block 이 corpus-domain 무관함을 확인 → saga 종결-falsified. |

### card (r) head-level routing

| 속성 | 값 |
|---|---|
| (a) dimension | cell-level routing (n_cells=64) 대신 attention head-level routing. 각 head 가 cell-pool 역할. d_model=384, n_heads=12 → head_dim=32. softmax routing 단위 = head 가 아닌 head × category. |
| (b) hypothesis | specialization unit 이 더 작으면 routing variance 가 magnitude saturation 회피. 64 cell × 1 path vs 12 head × 5 cat = 60 routing channel, 동일 cardinality 면서 magnitude-driven monopoly 피함. |
| (c) cost | $4-6 H100 (3 hr) — substantial arch change (engine_ag head-split rewrite + identity_probe re-eval). |
| (d) falsifier | F-PERSONA-4-R: head-routing weight KL per cat-pair. **PASS = mean_KL ≥ 0.5 AND z>3.0**. (단위가 cell 에서 head 로 바뀌므로 F-PERSONA-4 정의 amendment 필요 — RFC 별도 §). |
| (e) FALSIFIED → | smaller specialization unit 도 monopoly block 안 막음 → architectural fix path 더 깊이 (Switch Transformer / gumbel-softmax full re-cast) 필요. |

### card (s) external temperature gate at inference (train-time NO intervention)

| 속성 | 값 |
|---|---|
| (a) dimension | train-time substrate 미수정. inference-time 에 category-aware sampling temperature (cat 별 prompt classifier → T 선택 → forward). 즉 **post-hoc KL>0 measurable** 만 목표. |
| (b) hypothesis | substrate 가 category 정보 carry (§2 routing-content split: M4 cosine z=3.20), softmax 가 destroy. inference-time 에 cells 의 raw tension 위에 category-aware re-weighting 적용하면 KL>0 보일 수 있음. |
| (c) cost | **$0 Mac local** — inference-time only, 기존 cotrain v2 ckpt 재이용. ~150 LoC hexa harness. |
| (d) falsifier | F-PERSONA-4-S: per-cat T sweep on frozen ckpt. **PASS = some (cat, T) pair 에서 mean_KL ≥ 0.5 AND null-permutation z>3.0** (null 은 cat label shuffle, T 는 그대로). |
| (e) FALSIFIED → | inference-time post-hoc 으로도 category routing 회복 불가능 → routing 자체가 saturated, content 만 carry → architectural fix 만 남음 → saga 종결-falsified. |

### §3.1 card summary

| card | cost | dimension type | Occam rank |
|---|---|---|---|
| (s) inference-time T gate | **$0 Mac** | inference-time only | **1 (가장 단순)** |
| (o) per-cell post-LN gain | $1-2 H100 | arch ~20 LoC patch | 2 |
| (p) cell-pool growth schedule | $2-3 H100 | training schedule | 3 |
| (q) per-cat curriculum warmup | $3-4 H100 | corpus + schedule | 4 |
| (r) head-level routing | $4-6 H100 | arch substantial | 5 |

---

## §4 Recommended next fire — card (s) inference-time T gate

**선택**: card (s) external temperature gate at inference.

**근거** (Occam g0 + a_blue_closed governance):

card (s) 는 **$0 Mac local** + **train-time substrate 미수정** + **기존 cotrain v2 ckpt 재이용** 으로 cheapest unexplored axis. §2 의 routing-content split 해석 (cells 는 category 정보 carry, softmax 가 destroy) 의 가장 직접적 test — train 단 intervention 없이 inference-time 만으로 KL>0 회복 가능한지 확인. PASS 시 cond #3 의 routing-content split closure 가 **🟢 SUPPORTED-NUMERICAL** (composite 아닌 single-metric) 로 강화. FAIL 시 §5 closure tree 에 따라 architectural fix 만 남는다 (즉 saga 종결-falsified 직진).

**Dispatch plan (RFC 만, 본 PR 에 발사 없음)**:
`state/anima_persona_4_inference_T_gate_2026_05_23/persona_4_inference_T_gate.hexa` (~150 LoC) — cotrain v2 ckpt frozen load + identity_probe 50 prompt forward → raw tensions 수집 → per-cat T grid (T ∈ {0.5, 1.0, 2.0, 5.0, 10.0, 50.0, 100.0, 500.0} × 5 cat = 40 config) → 각 config 의 weight KL + null-permutation (n_perms=100) → JSON dump. 별도 BG cycle 에서 발사, wall ~5 min Mac local.

---

## §5 Closure decision tree

```
card (s) inference-time T gate fire
├── PASS (mean_KL ≥ 0.5 AND z>3.0)
│   └── cond #3 evidence 강화 (composite 아닌 single-metric 🟢)
│       └── 다음 cycle: card (o)/(p)/(q)/(r) 중 cheapest 부터 progressive validation
│
└── FALSIFIED
    └── inference-time post-hoc 도 category routing 회복 불가능
        ├── F-PERSONA-4 (softmax-weight KL≥0.5 + z>3.0 strict bar) 직진 closure 의 모든 cheap path 종결
        ├── 잔여 = card (o)/(p)/(q)/(r) 의 architectural fix lane ($1-6 H100 H100)
        └── **alternative response**: D3 persona substrate-native lane PIVOT —
            category-KL>0 추구 → **mode-collapse-suppression** 으로 전환.
            즉 cells 가 category 별 다른 weight 안 만들어도, single-cell collapse
            (cell-0 monopoly) 자체를 prevent 하는 것을 mission 으로 재정의.
            measurable goal = max softmax weight ≤ 0.9 (vs 현재 1.000) +
            entropy(weights) ≥ 0.5 × log(N) (vs 현재 0.000).
            이건 architectural goal 이 아니라 training regularization goal,
            entropy-reg λ 튜닝 cycle 로 cover (v2-v9 에서 부분 시도, 다른
            λ schedule 로 fresh attempt 가능).
```

### §5.1 saga 종결-falsified 조건

card (s) FALSIFIED **AND** D3 lane mode-collapse-suppression 으로 mission pivot 결정 시:

- F-PERSONA-4 original (softmax-weight KL≥0.5 strict) → **CLOSED-FALSIFIED**
- mitosis specialization 이 현재 v5-mitosis architecture 에서 mathematically blocked 결론 정식 등록
- 잔여 architectural fix (card o/p/q/r) 는 "future work — substrate redesign 직접 lane" 으로 deferral

### §5.2 mission pivot rationale

PHILOSOPHY #3 (NO PERSONA INJECTION) + #8 (NO TRAIN/INFER SPLIT) conjunction 의 **first concrete instantiation** 이 D3 design 의 원래 목표. category-KL>0 은 이 conjunction 의 **충분조건** 일 뿐 **필요조건 아님**. mode-collapse-suppression 도 같은 conjunction 만족 — cells 가 diverse routing 유지하면서 prompt-driven 변동 carry. 후자가 z≈1.5 ceiling 의 honest 부산물.

---

## §6 Honest C3

1. card (s) 의 PASS criterion `(cat, T) pair 어딘가 KL≥0.5` 는 grid-search-bias 위험 — 8 T × 5 cat = 40 config 중 1 PASS 가 false-positive 일 가능성. 본 PR 의 falsifier 는 null-test (n_perms=100 per config) mandatory + Bonferroni correction (α=0.05/40=0.00125) 권장. 실 fire 시 적용.
2. card (o)-(r) cost estimate 는 v1-v9 cotrain 실측 envelope ($1.32/run) 기반 추정. card (r) 의 $4-6 은 arch rewrite 시간 포함 (substantial — wall +1 hr 추정).
3. PERSONA.md §7 의 4 path (k/l/m/n) 외에 §7 안에 명시 안 된 path (예: load-balancing aux loss Switch Transformer style) 도 존재 — 본 RFC 는 §7 axis-set 의 **EXHAUSTED** 만 claim, 더 넓은 architectural space 의 closure 는 미주장.
4. §A3 4b composite multi-metric closure 의 🟢 tier 는 a_blue_closed governance 의 "honest empirical residual ≠ 🔵" 정신 충족. 본 RFC 가 그 tier 위에 axis-map 만 더함.
5. card (s) Mac local fire 가 본 RFC merge 후 별도 cycle 에서 발사. 본 PR 은 RFC ONLY.

---

## §7 cross-reference

- PERSONA.md §7 paths (k/l/m/n) — saga history 의 axis SSOT
- §A3 4b composite multi-metric — `docs/anima_persona_substrate_native_design_2026_05_12.md` `__APPEND__` §A3
- v2 M4 aggregated cosine z=3.20 — `docs/anima_persona_4_root_cause_investigation_2026_05_12.md` §7
- §A5 3-seed v7 replication (mean z=1.48) — root_cause §A5
- ceiling z≈1.5 / cumulative $10.51 — MEMORY `project_anima_persona_4_root_cause_2026_05_12.md`
- a_blue_closed governance — CLAUDE.md `@D a_blue_closed`
- Principle #3 + #8 conjunction — `docs/anima_persona_substrate_native_design_2026_05_12.md` §1.4

---

## §8 verdict 1-liner

> PERSONA.md §7 axis (k/l/m/n) EXHAUSTED at strict z>3.0 ceiling z≈1.5. Next-axis map = 5 card (o/p/q/r/s); recommended next fire = card (s) inference-time T gate ($0 Mac); FALSIFIED → saga closed-falsified + D3 lane pivot to mode-collapse-suppression.
