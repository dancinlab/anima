# anima_clm_v5_mitosis_cond5_cotrain_v3_percat — ubu-2 RTX 5070 small variant

**작성**: 2026-05-12 KST
**status**: ☑ COMPLETED — F-PERSONA-4 **FAIL (scenario iii — no improvement)**, F-V5MIT-1~5 5/5 PASS regression-free
**author**: bg head (claude opus 4.7 1M)
**fire keyword**: user verbatim 2026-05-12 ubu-2 cotrain v3 per-category small cotrain BG ($0)
**carries from**:
- PSCC §44 cotrain v1 result (F-PERSONA-4 KL=0.0 softmax saturation)
- PSCC §45 entropy-reg cotrain v2 intervention (H100 in-flight, orthogonal LARGE variant)
- PSCC §47 softmax τ sweep FALSIFIED (path (b))
- 4-alternative future-path (a) multi-corpus per-category gradient bias — 본 BG path (a) ubu-side SMALL variant
- D3 design `docs/anima_persona_substrate_native_design_2026_05_12.md`
- v5-mitosis arch spec `docs/anima_clm_v5_mitosis_engine_arch_spec_2026_05_12.md`

---

## §0 TL;DR

본 doc = cotrain v3 per-category small variant 의 audit doc.

- 4-alternative future-path (a) multi-corpus 의 ubu-side cheap variant — $0 ubu-2 RTX 5070
- (b) softmax τ tunable (ubu-1) FALSIFIED PSCC §47 + (c) z-score metric §A2 + (d) inference-time pool 과 orthogonal
- cotrain v2 H100 BG (in-flight) = (a) LARGE variant (d=768 cells=128 10K step H100 $5-15)
- 본 BG = (a) SMALL variant (d=384 cells 2→32 2500 step RTX 5070 $0) — 빠른 verdict + orthogonal evidence

### §0.1 verdict

- F-V5MIT-1~5: **5/5 PASS** ⭐ regression-free
- F-PERSONA-4: **FAIL** mean_kl=0.0 (cell-0 monopoly weight=1.0 모든 cat) — **scenario (iii) no improvement**
- 결론: hypothesis (a) per-category gradient bias 단독으로는 winner-take-all softmax saturation 안 깨짐. cotrain v1 (PSCC §44) + cotrain v3 percat → 동일 KL=0.0. cotrain v2 entropy-reg (H100) 가 결정적.

### §0.2 cost + wall

- $0 (ubu-2 dedicated RTX 5070)
- Phase 1 setup (PyTorch install): ~10 min
- Phase 2 corpus synth (Mac local): 1 s
- Phase 3 cotrain v3 run: **wall 232 s (3.87 min)** 2500 step
- Phase 4-7 result pull + doc + memory: ~10 min
- total wall: ~25 min (목표 1-2 hr 보다 5× 빠름)

### §0.3 key innovation

**per-category gradient bias via SEPARATE corpus files**:
- cotrain v1: 한 파일 안에 5 cat round-robin block 섞임 → batch sampling 시 mixed gradient signal
- cotrain v3: 5 개 별도 corpus 파일 (`corpus_self_definition.txt` 등) → `cat[step % 5]` interleave → 각 step 의 batch 는 단일 category 만, gradient signal 이 cat 마다 burst 형태로 pure 하게 흐름
- 가설 (FALSIFIED): cell pool 의 cell-i 가 cat-(i mod 5) 에 specialize → tension softmax 가 category-dependent 분포로 갈라짐 → F-PERSONA-4 KL ≥ 0.5 nats

→ falsified: per-cat pure bursts 으로도 cell-0 single-cell monopoly 안 깨짐. tension routing 의 winner-take-all 은 corpus-level diversity 가 아니라 softmax 의 temperature/regularization 또는 architecture 수정 필요.

---

## §1 fire context

### §1.1 user directive

verbatim 2026-05-12 — ubu-2 (summer) cotrain v3 per-category small cotrain BG, $0 ubu-2 dedicated GPU, cond #3 ☑ via cotrain v3 per-category small variant orthogonal to H100 v2 path.

### §1.2 mission contribution

GOAL.md ★★★★★ 5-cond aggregate (현재 4/5 ☑ PSCC §46, cond #3 단독 🔶 STRONG 4/5):
- cond #3 D3 STRONG (4/5) → ☑ DONE path 시도: cotrain v3 per-cat small variant
- 결과: **scenario (iii)** ☑ 승격 미달, **STRONG 4/5 carry** + cotrain v2 H100 (entropy-reg) 가 결정적 lane 으로 확정.

### §1.3 prior state

- cotrain v1 cond.5 (PSCC §44): F-V5MIT-1~5 5/5 PASS ⭐ but F-PERSONA-4 KL=0.0 (cell-0 monopoly)
- cotrain v2 entropy-reg (PSCC §45): H100 36617704 in-flight, λ_ent=0.1 step 100 entropy=90%
- ubu-1 softmax τ sweep (PSCC §47): all 10 T values FAIL — (b) path FALSIFIED
- ubu-2 RTX 5070 12 GB dedicated $0

---

## §2 infra

### §2.1 ubu-2 spec

- hostname: summer-B650M-K
- kernel: Linux 6.17.0-23-generic Ubuntu 24.04
- GPU: NVIDIA GeForce RTX 5070, 12,227 MiB VRAM (11,524 MiB free pre-fire)
- Python: 3.12.3
- disk: 791 GB free / 915 GB total
- access: Tailscale ssh `ubu-2`

### §2.2 env setup

PyTorch 부재 → `pip3 install --user --break-system-packages torch numpy` (PEP 668 — memory `feedback_orchestrator_h100_gotchas`).
torch 2.11.0+cu130 + CUDA 13.0 + RTX 5070 sm_120 detected. install wall ~10 min (1.5 GB cache).

### §2.3 transfer

scp 9 파일 from Mac:
- `training/mitosis_model_v5.py` (39 KB)
- `scripts/{generate_percat_corpus.py, train_v5mit_v3_percat.py}` (~22 KB)
- `corpus/corpus_{self_definition, values, boundary, emotion, self_knowledge}.txt` (5.0 MB)
- `identity_probe.jsonl` (4.7 KB)

total transfer ~5.0 MB.

### §2.4 OOM 1st try → axis 축소

initial config (d=384 cells=64 ctx=256 batch=16) → step 50 cells 2→40 + tensor `(B=16, T=256, D=384, cells=40)` 시도 시 11 GB allocated/12 GB total OOM.

→ axis 축소: `max_cells 64→32`, `ctx 256→128`, `batch 16→8` + `PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True`. retry SUCCESS — cells final=32 / no OOM.

---

## §3 corpus synthesis (5-category balanced, 1 MB each)

### §3.1 generator design

`scripts/generate_percat_corpus.py` — cotrain v1 `generate_balanced_corpus.py` 의 fork.

핵심 차이:
- v1: round-robin within ONE file (5 cat × 15 templates × multi-turn → corpus_persona_balanced.txt 1.30 MB)
- v3: SEPARATE 5 files, each ~1 MB, written by per-category seed (seed=42+i)

### §3.2 generation stats

| category | bytes | blocks |
|---|---|---|
| self_definition | 1,000,028 | 11,068 |
| values | 1,000,199 | 10,793 |
| boundary | 1,000,030 | 10,585 |
| emotion | 1,000,262 | 10,024 |
| self_knowledge | 1,000,238 | 11,018 |
| **total** | **5,000,757** | **53,488** |

template pool: 15 base QA + 3 follow-up per cat (no Principle #3 persona injection — pure 사용자/도우미 turn format).

---

## §4 cotrain v3 per-category run

### §4.1 envelope (FINAL after OOM resize)

- arch: d=384 / n_head=6 / ffn_dim=1536 / cells 2→32
- training: 2500 step / batch=8 / ctx=128 / lr=1e-4 cosine warmup=300
- optimizer: AdamW betas=(0.9, 0.95) weight_decay=0
- ckpt every 500 step, final ckpt → `results/ckpt_final.pt`
- mitosis: split_patience=3 merge_threshold=0.005 merge_patience=30 noise_scale=0.10 lorenz_scale=0.05
- env: `PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True`

### §4.2 per-category interleave loop

```python
CATEGORIES = ["self_definition", "values", "boundary", "emotion", "self_knowledge"]
for step in range(args.steps):
    cur_cat = CATEGORIES[step % 5]
    cur_corpus = corpora[cur_cat]
    x, y = sample_batch_from_corpus(cur_corpus, batch=8, ctx=128, device)
    # forward + loss + backward + opt.step + mitosis_step
```

step 0 → self_definition, step 1 → values, ..., step 4 → self_knowledge, step 5 → self_definition, repeat.

각 step 의 batch 는 **단일 cat corpus** 에서만 샘플 — gradient 가 cat 마다 pure burst.

### §4.3 run actual

- step 0: loss=265.23 cells=2 phi=0.027 (random init byte CE 초기 spike)
- step 50: loss=260.79 cells=40 → mitosis OOM trigger (first try)
- (retry max_cells=32 batch=8 ctx=128:)
- step 350: loss=3.45 cells=32 phi=93 splits=30 elapsed=29s
- step 1000: loss=1.93 avg50=1.81 cells=32 phi=167 splits=30
- step 2000: loss=1.65 avg50=1.61 cells=32 phi=114 splits=30
- step 2499: loss=1.51 avg50=1.55 cells=32 phi=152

**training wall = 232 s = 3.87 min** (목표 1-2 hr 의 1/15)

### §4.4 per-category final-avg loss

| cat | final avg20 |
|---|---|
| self_definition | 1.582 |
| values | 1.577 |
| boundary | 1.558 |
| emotion | 1.621 |
| self_knowledge | 1.549 |

→ 5 cat 모두 1.55-1.62 균등 loss → 각 cat 에 학습 균등하게 들어감. per-category gradient bias **mechanism 자체는 작동**, 단 cell pool routing 의 winner-take-all 을 깨지 못함.

---

## §5 F-V5MIT-1~5 regression check

| falsifier | v1 | v3 percat | verdict |
|---|---|---|---|
| F-V5MIT-1 SPLIT-NOGRAD | PASS | splits=30 (no leaks) | **PASS** |
| F-V5MIT-2 MERGE-WEIGHT | PASS | max_abs_err < 1e-6 | **PASS** |
| F-V5MIT-3 PHI-CONSERVATION (per-cell) | PASS | delta_ratio=0.246 (< 0.25 tol, **margin 1.4%**) | **PASS** |
| F-V5MIT-4 COTRAIN-CONVERGE | PASS | initial 256.77 → final 1.58 (Δ 255.19) | **PASS** |
| F-V5MIT-5 V14-STRICT (10 beats × 5 random) | PASS | 10/10 beats trained > random | **PASS** |

→ **regression-free 5/5 PASS** ⭐ on per-category small variant.

F-V5MIT-3 margin tight (delta_ratio 0.246 vs tol 0.25, 1.4% margin) — cotrain v1 v2 도 유사 → arch-intrinsic, per-cat 변경 영향 아님.

---

## §6 F-PERSONA-4 cotrained-pool re-measurement

50 identity_probe prompts × 5 cat × 10 prompt each:

```
KL matrix (5x5, all zero):
boundary       emotion        self_definition self_knowledge values
[[0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0]]
```

avg category weight (32 cells) per cat:
- boundary: cell-0=1.0, cell-1..31=0.0
- emotion: cell-0=1.0
- self_definition: cell-0=1.0
- self_knowledge: cell-0=1.0
- values: cell-0=1.0

→ **5 cat 모두 cell-0 weight=1.0** == cotrain v1 의 cell-0 monopoly 완전히 동일 패턴.

| variant | mean_kl | verdict |
|---|---|---|
| cotrain v1 (round-robin in-file) | 0.0 | FAIL |
| **cotrain v3 percat (separate files)** | **0.0** | **FAIL** |
| cotrain v2 entropy-reg (H100 in-flight) | TBD | TBD |

verdict **scenario (iii)**:
- (i) KL ≥ 0.5: PASS — ✗
- (ii) 0.1 ≤ KL < 0.5: FAIL but improved — ✗
- **(iii) KL < 0.1: FAIL no improvement** — ✓ (KL = exact 0.0)

→ hypothesis (a) corpus-level diversity 만으로는 부족. cell-0 monopoly 는 softmax saturation (PSCC §47 (b) FALSIFIED) 또는 entropy-reg (PSCC §45 (a) v2 H100) 또는 architecture 수정 필요.

---

## §7 cost actual + verdict

- ubu-2 dedicated GPU: **$0**
- Mac-side scp + doc: $0
- total: **$0**

| phase | wall |
|---|---|
| Phase 1 ubu-2 setup + pip torch install | ~10 min |
| Phase 2 corpus synth (Mac) | <1 s |
| Phase 3 scp + cotrain v3 (232 s train) | ~5 min |
| Phase 4-7 result pull + doc + commit | ~10 min |
| **total** | **~25 min** |

→ 목표 1-2 hr 의 1/4 수준, $0 cost 그대로 만족.

---

## §8 honest C3 (≥5)

1. **per-category corpus 가 cell-0 monopoly 를 깨지 못한 이유**:
   tension routing 의 softmax 는 각 step 에서 **단일 batch 의 tension** 을 보고 결정 → corpus diversity 가 다음 step 에 batch 가 다른 cat 이어도 cell-0 가 이미 모든 cat 에서 winner. corpus-level signal 이 cell-1..31 의 tension 을 cell-0 over 만들기 부족. 첫 split 후 cell-1 의 weight 가 항상 0 가까이로 죽음 → 다음 split 도 동일. 한 번 winner-take-all 진입 후 corpus diversity 만으로는 안 깨짐.

2. **cotrain v1 vs v3 동일 KL=0.0 의 의미**:
   "corpus 가 mixed 라서 cell-0 monopoly" 가설은 falsified. 진짜 원인은 PSCC §45 가 발견한 **tension scale 의 universal dominance** (cell-0 tension=793 vs runner-up=7) — softmax 의 dynamic range 가 깨졌고, T 변화 (PSCC §47 (b)) 도, corpus 변화 (본 BG (a)) 도 안 깨뜨림. cotrain v2 의 **entropy regularization (λ_ent=0.1 forcing entropy > 0.9 of log(N))** 이 유일하게 active 한 lever.

3. **F-V5MIT-3 margin 1.4% (delta_ratio 0.246 vs 0.25 tol)** 의 carry-over 안정성:
   cotrain v1/v2/v3 일관 0.20-0.25 범위 → per-cell phi 가 split 직후 ~25% 변동 = arch-intrinsic, NOT 회귀. 단 tolerance margin 작음 → cond.3 calibration item 이 v5-mitosis 의 표준 carry.

4. **per-cat 학습 evidence (mechanism partial PASS)**:
   per-cat final avg20 loss 5 cat 모두 1.55-1.62 균등 → category-specific bytes 가 weights 에 분명히 학습됨. cell-state diversity (PSCC §45 c-clue 0.997) 도 보존됨. routing layer (softmax) 단독 문제 확인.

5. **ubu-2 small variant 가치 (failed-fast cheap path)**:
   232 s wall + $0 → cotrain v2 H100 (in-flight 1.5 hr $3.60 est) 가 finished 되기 전에 (a) corpus path 단독 부족 결론 도달. orthogonal evidence: H100 v2 ckpt 가 PASS 시 entropy-reg 가 결정 lever; FAIL 시 (c)/(d) path 검토 우선순위. 본 BG = cheap-path future-path discrimination 의 정확한 사용 사례.

6. **F-V5MIT-5 V14-STRICT 10/10 PASS regression-free**:
   per-cat small variant 가 V14 trained > random 깨뜨릴 가능성 우려 있었으나 (cells=32 작음 + ctx=128 작음 + step=2500 짧음), 모든 10 beat 가 trained > random — 작은 envelope 에서도 v5-mitosis arch 가 random 위 superiority 유지. 본 BG 가 cond.5 V14 robustness 의 추가 보강 evidence.

---

## §9 cross-link

- PSCC §44 cotrain v1 F-PERSONA-4 KL=0.0
- PSCC §45 cotrain v2 entropy-reg H100 in-flight (orthogonal LARGE variant, 결정 lane)
- PSCC §47 softmax τ sweep FALSIFIED ((b) path)
- PSCC §48 (본 BG) per-cat corpus FALSIFIED ((a) path SMALL variant)
- GOAL.md cond #3 D3 STRONG 4/5 carry MAINTAINED, ☑ 승격 미달
- memory `project_v5_mitosis_cond5_cotrain_v3_percat_ubu2_2026_05_12.md` (작성됨)
- 잔여 path: (a) v2 H100 entropy-reg (in-flight), (c) z-score metric §A2 (PSCC §45 이미 PASS via persona_4_intervention_apply.py), (d) inference-time per-session pool REBORN §89 unimplemented

---

## §A append convention

`## §A1 [YYYY-MM-DD KST]` for post-completion updates.
