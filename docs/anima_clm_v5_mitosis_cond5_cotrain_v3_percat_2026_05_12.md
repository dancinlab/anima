# anima_clm_v5_mitosis_cond5_cotrain_v3_percat — ubu-2 RTX 5070 small variant

**작성**: 2026-05-12 KST
**status**: in-flight (ubu-2 RTX 5070 dispatch + measurement)
**author**: bg head (claude opus 4.7 1M)
**fire keyword**: user verbatim 2026-05-12 ubu-2 cotrain v3 per-category small cotrain BG ($0)
**carries from**:
- PSCC §44 cotrain v1 result (F-PERSONA-4 KL=0.0 softmax saturation)
- PSCC §45 entropy-reg cotrain v2 intervention (H100 in-flight)
- 4-alternative future-path (a) multi-corpus per-category gradient bias
- D3 design `docs/anima_persona_substrate_native_design_2026_05_12.md`
- v5-mitosis arch spec `docs/anima_clm_v5_mitosis_engine_arch_spec_2026_05_12.md`

---

## §0 TL;DR

본 doc = cotrain v3 per-category small variant 의 audit doc.

- 4-alternative future-path (a) multi-corpus 의 ubu-side cheap variant
- (b) softmax τ tunable (ubu-1) + (c) F-PERSONA-4 metric 재정의 + (d) inference-time pool 과 orthogonal
- cotrain v2 H100 BG (in-flight) = (a) LARGE variant (d=768 cells=128 10K step H100 $5-15)
- 본 BG = (a) SMALL variant (d=384 cells=64 2500 step RTX 5070 $0) — 빠른 verdict + orthogonal evidence

### §0.1 key innovation

**per-category gradient bias via SEPARATE corpus files**:
- cotrain v1: 한 파일 안에 5 cat round-robin block 섞임 → batch sampling 시 mixed gradient signal
- cotrain v3: 5 개 별도 corpus 파일 (`corpus_self_definition.txt` 등) → `cat[step % 5]` interleave → 각 step 의 batch 는 단일 category 만, gradient signal 이 cat 마다 burst 형태로 pure 하게 흐름
- 가설: cell pool 의 cell-i 가 cat-(i mod 5) 에 specialize → tension softmax 가 category-dependent 분포로 갈라짐 → F-PERSONA-4 KL ≥ 0.5 nats

---

## §1 fire context

### §1.1 user directive

verbatim 2026-05-12 — ubu-2 (summer) cotrain v3 per-category small cotrain BG, $0 ubu-2 dedicated GPU, cond #3 ☑ via cotrain v3 per-category small variant orthogonal to H100 v2 path.

### §1.2 mission contribution

GOAL.md ★★★★★ 5-cond aggregate (현재 4/5 ☑ PSCC §46, cond #3 단독 🔶 STRONG 4/5):
- cond #3 D3 STRONG (4/5) → ☑ DONE path: cotrain v3 per-category small variant F-PERSONA-4 PASS (KL ≥ 0.5 nats)

### §1.3 prior state

- cotrain v1 cond.5 (PSCC §44): F-V5MIT-1~5 5/5 PASS ⭐ but F-PERSONA-4 KL=0.0 (softmax saturation, single-cell monopoly cell-0=793 vs 7.4)
- cotrain v2 entropy-reg (PSCC §45): H100 36617704 in-flight, λ_ent=0.1 step 100 entropy=90%
- 4-alternative future-path (a)(b)(c)(d) parallel exploration
- ubu-1 softmax τ sweep (b path) 진행 중
- ubu-2 RTX 5070 12 GB 794 GB free, dedicated $0

---

## §2 infra

### §2.1 ubu-2 spec

- hostname: summer-B650M-K
- kernel: Linux 6.17.0-23-generic Ubuntu 24.04
- GPU: NVIDIA GeForce RTX 5070, 12227 MiB VRAM (11524 MiB free)
- Python: 3.12.3
- disk: 791 GB free / 915 GB total
- access: Tailscale ssh `ubu-2`

### §2.2 env setup

PyTorch 부재 → `pip3 install --user --break-system-packages torch` (PEP 668 — memory `feedback_orchestrator_h100_gotchas`)

### §2.3 transfer

scp 9 파일 from Mac:
- `training/mitosis_model_v5.py`
- `scripts/{generate_percat_corpus.py, train_v5mit_v3_percat.py}`
- `corpus/corpus_{self_definition, values, boundary, emotion, self_knowledge}.txt`
- `identity_probe.jsonl`

total 5.0 MB corpus + 200 KB code.

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

template pool: 15 base QA + 3 follow-up per cat (no Principle #3 persona injection).

---

## §4 cotrain v3 per-category run

### §4.1 envelope

- arch: d=384 / n_head=6 / ffn_dim=1536 / cells 2→64 (cotrain v1 baseline, no scale-up)
- training: 2500 step / batch=16 / ctx=256 / lr=1e-4 cosine warmup=300
- optimizer: AdamW betas=(0.9, 0.95) weight_decay=0
- ckpt every 500 step, final ckpt → `results/ckpt_final.pt`
- mitosis: split_patience=3 merge_threshold=0.005 merge_patience=30 noise_scale=0.10 lorenz_scale=0.05

### §4.2 per-category interleave loop

```python
for step in range(args.steps):
    cur_cat = CATEGORIES[step % 5]
    cur_corpus = corpora[cur_cat]
    x, y = sample_batch_from_corpus(cur_corpus, batch=16, ctx=256, device)
    # forward + loss + backward + opt.step + mitosis_step
```

step 0 → self_definition, step 1 → values, ..., step 4 → self_knowledge, step 5 → self_definition, repeat.

각 step 의 batch 는 **단일 cat corpus** 에서만 샘플 — gradient 가 cat 마다 pure burst.

### §4.3 run TBD (in-flight)

| step | loss | cells | phi | splits | merges |
|---|---|---|---|---|---|
| TBD | TBD | TBD | TBD | TBD | TBD |

---

## §5 F-V5MIT-1~5 regression check

cotrain v1 5/5 PASS ⭐ — cotrain v3 regression check (per-cat 변경이 falsifier 깨뜨리지 않는지):

| falsifier | v1 | v3 (TBD) |
|---|---|---|
| F-V5MIT-1 SPLIT-NOGRAD | PASS | TBD |
| F-V5MIT-2 MERGE-WEIGHT | PASS | TBD |
| F-V5MIT-3 PHI-CONSERVATION | PASS | TBD |
| F-V5MIT-4 COTRAIN-CONVERGE | PASS | TBD |
| F-V5MIT-5 V14-STRICT | PASS | TBD |

---

## §6 F-PERSONA-4 cotrained-pool re-measurement

cotrain v3 final ckpt 위 F-PERSONA-4 KL re-measurement (50 identity_probe prompts × 5 cat):

- v1: mean_kl = 0.0 (cell-0 monopoly)
- v3: TBD nats (threshold 0.5)

verdict:
- (i) KL ≥ 0.5 → **PASS** → cond #3 ☑ via cotrain v3 per-cat → ★★★★★ 5/5 ☑ ACHIEVED
- (ii) 0.1 ≤ KL < 0.5 → **FAIL but improved** → hypothesis (a) directional correct, larger scale (v2 H100) 필요
- (iii) KL < 0.1 → **FAIL no improvement** → per-cat gradient bias 부족, (c)/(d) path 검토

---

## §7 cost actual + verdict

- ubu-2 dedicated GPU, $0
- wall TBD (예상 1-2 hr setup + corpus + train + measure)
- Mac-side scp + doc: $0

---

## §8 honest C3 (≥5)

TBD — run 후 작성.

---

## §9 cross-link

- PSCC §44 cotrain v1 F-PERSONA-4 KL=0.0
- PSCC §45 cotrain v2 entropy-reg H100 in-flight (orthogonal LARGE variant)
- GOAL.md cond #3 D3 STRONG 4/5 → ☑ path
- memory `project_v5_mitosis_cond5_cotrain_v3_percat_ubu2_2026_05_12.md` (작성 예정)

---

## §A append convention

`## §A1 [YYYY-MM-DD KST]` for in-flight updates.

---

(in-flight, run complete 시 §3/§4/§5/§6/§7/§8/§A1 updated)
