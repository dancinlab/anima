# P9 Paradigm D — KL Pre-Flight Cache Landed (2026-05-03)

**Status**: LANDED (rescue path — prior subagent a150a446 completed work but failed to write local artifacts)
**Substrate**: ubu1 RTX 5070 12GB (nf4 4-bit Mistral-7B-Instruct-v0.3)
**Cost**: $0 (local)
**Cite**: `docs/p9_paradigm_d_distill_spec_2026_05_03.md` (KL axis), `docs/p9_paradigm_d_phi_distillation_2026_05_03.md`

---

## 1. What landed

Top-K=64 logit cache for the 1K subset of `sft_data_full_50k_augmented.jsonl`, built and validated end-to-end on ubu1.

**Cache artifact** (ubu1):
- Path: `/tmp/p9_paradigm_d_kl_cache_v1_1k.jsonl`
- Size: **280.4 MB**
- Records: **1000** (covers 207,188 prompt tokens)
- K = 64, T = 4.0, max_seq_len = 256

**Validation (10 random samples, seed=43)**: VERDICT = **PASS**
- mean Top-K overlap: **64.00 / 64** (perfect)
- min Top-K overlap: 64 / 64
- max top-1 logit diff: **0.0000**
- sanity (vocab range + descending sort over 207,188 tokens): clean

---

## 2. Prior-subagent diagnosis (a150a446)

The previous BG subagent appeared "stuck on validator launched" but in fact had **completed everything successfully** at `2026-05-03 23:58:22 KST`. Diagnostic state:

| signal | observation |
|---|---|
| `/tmp/p9_paradigm_d_kl_cache_v1_1k.jsonl` | exists, 280 MB, 1000 lines |
| `cache_meta.json` | written 23:56 |
| `validation.json` | written 23:58, VERDICT=PASS |
| running mistral processes | none (clean exit) |
| GPU util | 0%, 2.7 GB used (idle baseline, no Mistral resident) |
| `builder.log` / `validator.log` | both end with success line |

**Root cause of "stuck" appearance**: the subagent finished the heavy work but never wrote the local artifacts (`state/p9_paradigm_d_kl_preflight_2026_05_03/`, marker, handoff). It likely silently terminated after the validator log without performing the last propagation step. **Rescue path was correct** — no recompute, just sync ubu1 → local + write closure docs.

---

## 3. Local artifacts (rescue propagation)

`state/p9_paradigm_d_kl_preflight_2026_05_03/`:
- `cache_meta.json` — full meta (teacher, K, T, tokens, ETA extrapolation)
- `validation.json` — 10-sample idempotency report
- `run.log` — orchestration log
- `builder.log` / `validator.log` — full subprocess stdout/stderr

**NOT** propagated locally: the 280 MB `.jsonl` cache itself (kept on ubu1 only — distillation training will run on H100, but pre-flight verifies the **method**, not the artifact transport).

Marker: `state/markers/p9_paradigm_d_kl_preflight_landed.marker`

---

## 4. Full-50K extrapolation

| metric | 1K (measured) | 50K (extrapolated) |
|---|---|---|
| build time | 109.9 s | **1.53 h** |
| cache size | 280.4 MB | **14.0 GB** |
| throughput | 9.10 records/s | (same) |
| total tokens | 207,188 | ~10.36 M |
| mean tokens/record | 207.2 | (same) |

**Verdict on 50K feasibility on ubu1**: tractable on time (1.5 h is fine), **NOT tractable on disk** if kept on `/tmp` (14 GB on a small system partition is risky — must redirect to `/home/aiden/` or external mount). For H100 distill, the cache should be built on the H100 substrate directly to avoid 14 GB SCP transfer cost.

---

## 5. Three caveats

1. **`/tmp` ephemerality** — the 280 MB 1K cache lives in ubu1 `/tmp` and will be wiped on reboot. If needed for replay/audit beyond a reboot, move to `/home/aiden/`. For now the meta+validation are the immutable record.

2. **Top-K overlap = 64/64 is "too perfect" — recheck the entropy floor**. Both build and validate ran with greedy decode + identical nf4 quantization on the same GPU, so byte-exact reproduction is expected. This validates **idempotency** but does NOT certify that the K=64 cutoff captures enough probability mass for KL distillation. **Recommended follow-up before 50K**: compute mean cumulative softmax mass within Top-64 across the 1K cache (target: ≥0.95 mean, ≥0.85 floor). If mass is too low, raise K to 128.

3. **Disk-budget extrapolation linearity assumption** — extrapolation assumes mean tokens/record stays at 207.2 across the full 50K. The augmented 50K may have a different length distribution (especially if any long-tail records exceed the `max_seq_len=256` truncation differently). **Recommended**: sample 5K (not 1K) before committing to 50K — it bounds the variance much tighter at marginal extra cost (~9 min build).

---

## 6. Next-step handoff

Pre-flight gates **CLEARED** for KL axis on Mistral-7B teacher. Ready to:
- (a) decide K=64 vs K=128 based on cumulative-mass check (caveat 2)
- (b) provision H100 substrate for the full-50K cache build (avoid SCP)
- (c) wire the cache into the distill loss path per `p9_paradigm_d_distill_spec_2026_05_03.md`

No blockers. The H100 D 25K run is unaffected (separate substrate, no preemption occurred).
