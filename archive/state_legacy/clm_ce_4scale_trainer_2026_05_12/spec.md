---
id: clm_ce_4scale_trainer_2026_05_12
parent_spec: state/phi_ce_orthogonality_decisive_2026_05_11/spec.md (§2.1 P-axis, §5 protocol, §5.7 P=100M ceiling)
parent_audit: state/phi_ce_orthogonality_decisive_2026_05_11/spec_audit_2026_05_11.md (§5.2 B5 finding, §1.2 CE capability zero)
parent_blocker: state/phi_ce_orthogonality_decisive_2026_05_11/noise_calibration_dryrun_blocker_2026_05_12.md (§B5)
naming_manifest: state/phi_star_naming_refactor_2026_05_12.md (3-engine split — this trainer = CE-track)
parent_h: H_080 (topo_24variants unified) — Conflict Resolution Pending
status: SPEC + PHASE-0 SCAFFOLDING (no actual training executed — cycle 7+ scope)
date: 2026-05-12
deterministic_seed: 0xC0EC0AC (inherited)
cycle_provenance: cycle 6 #P
lock_policy: NO chflags/chattr — repository directive 2026-05-11
commit_policy: NO separate commit — main process batches
---

# CE-Track CLM 3-Scale Trainer Spec — B5 Resolution

본 spec 은 `phi_ce_orthogonality_decisive_2026_05_11` 의 **B5 critical blocker**
(noise_calibration_dryrun_blocker_2026_05_12.md §B5 — CE-track CLM training pipeline
미land) 을 spec + Phase 0 scaffolding 으로 해소한다. spec.md §5.8 의 3-engine split
중 **CE-track engine** 에 해당.

actual training 은 본 spec 범위 밖 — cycle 7+ scope (cost $210-600, 3-scale dual-seed).

## 0. Context

- **Φ×CE measurement** (parent spec §2.1) 은 (N, P) cell key 로 join 되는 *2-track* —
  Φ-track (phi_star_cell_engine, TBD per naming_manifest) + CE-track (본 spec).
- **B5 finding** (spec_audit §5.2 / dryrun-blocker §B5): `anima_clm_invoke.hexa` 는
  *inference wrapper* (mock/local/hf), training loop / optimizer / dataset / checkpoint
  script 미land. {1M, 10M, 100M} 3 scale 모두 *새로 train* 필요.
- **P=100M ceiling** (parent spec §5.7 / NEXT.md cycle 5 #1): P=1B 제거, 15-cell grid
  (5 N × 3 P) 가 baseline. 본 spec 도 3-scale {1M, 10M, 100M} base + 1B deferred lane (§7).
- **$0 dev** (본 spec) — training cost 는 별도 cycle. spec + Phase 0 scaffolding 만 land.

## 1. Architecture — 3-Scale Parameter Sweep

3-scale base — `state/phi_ce_orthogonality_decisive_2026_05_11/spec.md` §2.1 의
P ∈ {10^6, 10^7, 10^8} 와 정합.

| scale id | P (target) | layers | hidden | heads | ffn_mult | seq_len | tied_emb |
|----------|-----------|--------|--------|-------|----------|---------|----------|
| tiny (1M)    | 1.0 × 10^6  | 4  | 256 | 4  | 4 | 512  | yes |
| small (10M)  | 1.0 × 10^7  | 6  | 512 | 8  | 4 | 1024 | yes |
| medium (100M)| 1.0 × 10^8  | 12 | 768 | 12 | 4 | 1024 | yes |
| (deferred) large (1B) | 1.0 × 10^9 | 24 | 1536 | 24 | 4 | 2048 | yes |

- transformer decoder-only (causal LM), GPT-2 style block (pre-LN, GELU, learned positional).
- exact P count 은 vocab size + tied_emb 에 의존 — config 작성 시 ±10 % tolerance.
- `tied_emb=yes` 로 input/output embedding 공유 → small scale 의 param efficiency.

## 2. Training Corpus

3 scale 모두 동일 corpus + 동일 split 사용 — CE 비교의 distributional 일관성 확보.

| field | value |
|-------|-------|
| primary | `state/anima_clm_3_*_corpus/` 의 anima hxc-corpus (tool/hxc_corpus_manifest.hexa 가 enumerate) |
| fallback | OpenWebText subset (~10 GB plaintext) — anima corpus 부족 scale 시 |
| held-out validation | 5 % stratified split, deterministic seed 0xC0EC0AC inherited |
| token budget per scale | Chinchilla 20× param: tiny 20M / small 200M / medium 2B tokens |
| dedup | minhash @ 0.8 jaccard threshold (existing pipeline 재사용) |

**caveat**: corpus 다양성 미명시 — held-out validation 의 distribution 모순 가능 (§8-L2).

## 3. Tokenizer

| option | path | rationale |
|--------|------|-----------|
| A (default) | `skt/kogpt2-base-v2` (BPE, vocab=51200) | 기존 anima HF cache 존재 (dryrun-blocker §1.3), back-compat |
| B (alternative) | 새 BPE train on training corpus, vocab=16384 | 더 작은 vocab → tiny scale 의 P budget 효율 |

**default = A** (kogpt2-base-v2). multi-tokenizer 비교는 별 cycle (§8-L3).
3-scale 모두 동일 tokenizer 사용 — CE 의 단위 (bits/token, nat) 일관성 확보.

## 4. Training Protocol

### 4.1 Optimizer / schedule

| field | value |
|-------|-------|
| optimizer | AdamW (β1=0.9, β2=0.95, ε=1e-8) |
| weight decay | 0.1 (transformer block params), 0 (embedding/LN) |
| LR peak | tiny 6e-4 / small 4e-4 / medium 3e-4 (Chinchilla-style scale) |
| LR schedule | linear warmup (1 % of steps) → cosine decay to 10 % peak |
| grad clip | 1.0 (global L2 norm) |
| precision | bf16 mixed (A100/A10 capable) |

### 4.2 Batch / step

| scale | global batch (tokens) | grad accum | step count | wall (A100) |
|-------|----------------------|------------|------------|-------------|
| tiny    | 32k  | 1  | ~610 steps  | ~1-2 h  |
| small   | 128k | 2  | ~1560 steps | ~2-4 h  |
| medium  | 512k | 8  | ~3900 steps | ~4-8 h  |

### 4.3 Dual-seed protocol (Hc_604)

- per scale, 2 init-seed variants (deterministic seed_a = 0xC0EC0AC, seed_b = 0xC0EC0AC ^ 0x42)
- final CE 의 *across-init-seed* variance → σ_CE_rel 추정 (parent prereq §5 Step 2 정합)
- dataset shuffle seed 는 init seed 와 동일 — *paired difference* (Hc_604 twin form)
- spec_audit §3.3 권고 (training 의 init-seed variance 가 small → dual-seed 면 충분, 64-twin 비현실)

## 5. CE Measurement Output

### 5.1 Output schema

```
{
  "schema": "anima/clm_ce_trainer/1",
  "scale_id": "tiny|small|medium|large",
  "param_count_actual": <int>,
  "seed_id": "a|b",
  "tokens_seen": <int>,
  "final_ce_nat": <float>,           // negative log-likelihood, nat/token
  "final_ce_bits": <float>,          // = final_ce_nat / ln(2)
  "perplexity": <float>,             // = exp(final_ce_nat)
  "held_out_split": "validation",
  "held_out_tokens": <int>,
  "tokenizer": "kogpt2-base-v2|custom_bpe_16k",
  "config_path": "trainer_{scale}.config.yaml",
  "checkpoint_path": "<runpod path>",
  "wall_seconds": <int>,
  "gpu_hours_a100": <float>,
  "deterministic_seed": "0xC0EC0AC",
  "phi_ce_join_key": {"N": null, "P": <param_count_actual>}
}
```

- `N=null` — CE-track 단독 측정 시 N 미정. (N, P) join 은 harness.py 가 cell key 로 수행.
- emit 위치: `state/clm_ce_4scale_trainer_2026_05_12/results/<scale>_<seed>.json`

### 5.2 Harness integration

- `state/phi_ce_orthogonality_decisive_2026_05_11/harness.py` 가 본 trainer 의 emit JSON 을
  *직접 ingest* — `final_ce_nat` field 를 parent spec §2.1 의 CE_i 값으로 사용.
- ingest contract: `phi_ce_join_key.P` 가 cell key 의 P-axis 와 match → mean(CE) over seed_a/b
  으로 cell value 산출.

## 6. Cost Estimate Per Scale

RunPod A100 spot 기준 (`secret get runpod.api_key` 경유, MEMORY.md reference_runpod_pipeline).

| scale | wall (single seed) | $ (single seed) | $ (dual seed) | parent spec §5.7.1 정합 |
|-------|--------------------|------------------|----------------|---------------------------|
| tiny (1M)    | 1-2 h | $5-15   | $10-30  | ✅ ($1-5 row 의 wall 늘림 변형) |
| small (10M)  | 2-4 h | $15-30  | $30-60  | ✅ ($5-20 row 정합)          |
| medium (100M)| 4-8 h | $50-150 | $100-300| ✅ ($50-150 row 정합)        |
| **3-scale dual-seed total** | — | **$70-200 single seed** | **$140-400 dual seed** | parent §5.7.1 P=100M-row 합 정합 |

**actual total prereq**: dual-seed × 3 scale = **$140-400** per Φ×CE measurement cycle.
noise calibration ($15-45, parent §5.7.4) + Φ-track 64-seed × 15 cell ($50-200, parent §5.7.1)
= overall **$205-645** for full decisive run.

본 spec 의 conservative range = **$210-600** (dual-seed 3-scale + small contingency,
parent spec.md §5.7.1 의 P=100M-row 합과 정합).

## 7. Deferred 1B Scale Lane

P=1B 은 parent spec §5.7.3 의 extension trigger (15-cell verdict = mixed) 충족 시만 활성화.

| field | value |
|-------|-------|
| scale_id | large |
| param_count | 1.0 × 10^9 |
| token budget | 20B (Chinchilla 20×) |
| wall | 12-24 h on A100 (single seed) |
| cost | $300-1500 (single seed); dual-seed $600-3000 |
| config | `trainer_1b.config.yaml` (Phase 0 placeholder, `status: deferred`) |
| trigger | parent spec §5.7.3 mixed verdict OR cycle 6+ budget 가용 |

→ 본 spec 의 baseline 3-scale 가 cycle 7+ 실행 후 verdict 보고 활성화.

## 8. Honest Limits (≥ 4)

- **L1**: parent spec §2.1 의 P ∈ {10^6, 10^7, 10^8} 3 P-point 와 본 spec 의 3-scale base
  *정합* — P=1B 은 parent §5.7.3 와 동일하게 deferred. spec 간 P-axis 통일성 OK.
- **L2**: training corpus 다양성 미명시 — anima hxc-corpus 가 *anima-axis-biased* 일 가능성,
  held-out validation 의 distribution 이 같은 axis 라면 CE 가 *general LM* 의 CE 와 다를
  수 있음. parent spec §3 의 "CE ∝ P^-0.85 scaling" fit 의 absolute slope 가 corpus 의존.
- **L3**: tokenizer 통일 (3-scale 모두 kogpt2-base-v2 또는 동일 custom BPE) 가정 — vocab size
  / merge rule 차이는 CE 의 bits/token 단위 비교를 깨뜨림. multi-tokenizer 비교는 별 cycle.
- **L4**: tiny scale (P=1M) 의 statistical power 부족 — 1M param 모델은 token budget 20M 이라도
  loss curve 가 saturate 안 함, init-seed variance > 5-10 % 가능. dual-seed 만으로는
  confidence interval narrow 어려움. actual run 시 4-seed 확장 옵션 고려 (cost +50 %).
- **L5**: 3-scale linear regression (CE vs log P) 의 slope SE 는 ~20-30 % 예상 (parent
  spec §5.7.2 정합). P=1B 추가 시 slope SE 절반으로 감소.
- **L6**: actual training pipeline 의 *implementation* (Python script, RunPod orchestrator,
  checkpoint save/load) 은 본 spec 범위 밖 — cycle 7+ scope. 기존 `tool/transient_py/anima_h153_capacity_100m_train.py`
  / `tool/clm_v4_lora_train_orchestrator.hexa` pattern 재사용 권장.
- **L7**: deterministic seed 0xC0EC0AC inherited — dataset shuffle / init / dropout 모두
  같은 seed family 사용 시 *seed correlation* 가능. dual-seed b = `seed ^ 0x42` 의 mix
  가 충분히 decorrelate 하는지 별도 audit 필요.

## 9. Cross-Links

- **parent spec**: `state/phi_ce_orthogonality_decisive_2026_05_11/spec.md` §2.1 / §5 / §5.7 / §5.8
- **parent audit**: `state/phi_ce_orthogonality_decisive_2026_05_11/spec_audit_2026_05_11.md` §1.2 / §5.2 (B5 source)
- **dryrun blocker**: `state/phi_ce_orthogonality_decisive_2026_05_11/noise_calibration_dryrun_blocker_2026_05_12.md` §B5
- **naming manifest**: `state/phi_star_naming_refactor_2026_05_12.md` (CE-track engine role)
- **harness**: `state/phi_ce_orthogonality_decisive_2026_05_11/harness.py` (ingest target)
- **pattern references** (Phase 0 scaffolding 재사용 후보):
  - `tool/clm_v4_lora_train_orchestrator.hexa` (RunPod lifecycle pattern)
  - `tool/transient_py/anima_h153_capacity_100m_train.py` (100M trainer pattern)
  - `tool/transient_py/anima_ib_capacity_50m_train.py` (50M trainer pattern)
  - `tool/transient_py/anima_h154_bpe_18m_train.py` (small scale trainer pattern)
  - `tool/anima_clm_invoke.hexa` (inference wrapper — training-side extension target)
- **orchestrator**: `tool/anima_runpod_orchestrator.hexa` (RunPod dispatch path)
- **parent H**: `hypotheses/H_080_topo_24variants.md` §Conflict Resolution Pending
- **cycle provenance**: NEXT.md cycle 6 #P (본 spec land trigger)

---

**Phase 0 Scaffolding** (placeholder files, NOT yet wired):

- `trainer_1m.config.yaml` — tiny scale config placeholder
- `trainer_10m.config.yaml` — small scale config placeholder
- `trainer_100m.config.yaml` — medium scale config placeholder
- `trainer_1b.config.yaml` — DEFERRED lane (status: deferred)
- `ce_measurement_hook.hexa.template` — emit hook template (~30 LOC, NOT executable)
- `README.md` — Phase 0 intro + spec.md cross-link + cycle 6 #P provenance

actual implementation = cycle 7+ scope. prereqs: training corpus stage / GPU allocation
(RunPod A100 or local A10 fallback) / B4 (runpod.api_key access via main process).

**B5 status transition**: BLOCKED → **RESOLVED-SPEC** (actual run = 별 cycle).

---

**lock policy reminder**: chflags +uchg/+schg/chattr +i 적용 *금지*. unlock 된 파일 *재잠금 금지*.
**commit policy**: 본 spec 은 *separate commit 금지* — 메인 process 가 일괄 commit.
