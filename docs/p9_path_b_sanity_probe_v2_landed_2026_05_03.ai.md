# P9 Path B Sanity Probe V2 — Landed 2026-05-03

**Goal**: Re-run the Path B HellaSwag sanity probe with the **restored 64K BPE tokenizer** instead of the byte-fallback workaround used in V1. Verify whether the V1 floor verdict (`CLM_V4_AT_FLOOR`, acc_norm=0.242) was robust to tokenization choice or hiding capability behind degraded inputs.

**Substrate**: ssh ubu1 (RTX 5070 12GB, sm_120, torch 2.11.0+cu128, lm-eval 0.4.11, sentencepiece 0.2.1), venv `/home/aiden/venv_orchestrator/bin/python`. $0.

**Constraints honored**: raw#9 (.py + tokenizer .model/.vocab kept only on ubu1; not mirrored to Mac), raw#15 (`~/anima/...` paths on ubu1), raw#10 (honest C3 below).

---

## Result

| Field | V1 (byte-fallback) | V2 (proper 64K BPE) |
|------|---|---|
| Task | hellaswag (5-shot, limit=500) | hellaswag (5-shot, limit=500, seed=42) |
| acc_norm (primary) | **0.242 ± 0.019** | **0.252 ± 0.019** |
| acc (unnormalized) | 0.254 ± 0.019 | 0.258 ± 0.020 |
| Wall time | 143s | 192s (GPU contention) |
| GPU alloc | 1.93 GB | 1.93 GB |
| Tokenizer | byte-fallback (`[i+4 for i in bytes]`) | sentencepiece-bpe-64k |

| Comparison | V1 | V2 |
|---|---|---|
| Random baseline (4-choice) | 0.250 | 0.250 |
| Llama-3.2-3B-Instruct 4bit | 0.644 | 0.644 |
| Llama − CLM v4 | +0.402 | +0.392 |

**Delta V2 − V1 = +0.010** — within 1σ of either probe. Tokenization-robustness verdict: `ROBUST_TO_TOKENIZATION`.

**Verdict: `CLM_V4_AT_FLOOR` (CONFIRMED via two independent tokenization paths).**

acc_norm 0.252 ∈ [0.20, 0.30]; statistically indistinguishable from random (0.252 vs 0.250 baseline; ±0.019 stderr).

---

## What V2 changed vs V1

V1 had **two** unresolved blockers when it ran:
1. `consciousness_laws.py _DATA[k]` hard-fail — fixed via `.get(k, {})` band-aid (later superseded by schema-aware loader, see `docs/consciousness_laws_root_cause_fix_landed_2026_05_03.ai.md`).
2. **64K BPE tokenizer artifact missing** — worked around with byte-fallback encoding (`text.encode('utf-8','replace')` → `[i+4 for i in bytes]`).

V2 swapped only blocker #2's workaround for the proper artifact. Everything else identical:
- Same `best.pt` checkpoint (step 20000, training CE 0.046, training Φ 27.91)
- Same `ConsciousDecoderV2` 350M scale config (768d/16L/12H/4kv, vocab=64000, block_size=512)
- Same head selection (`head_a` for next-token loglik per spec §1.2(iii))
- Same task config (hellaswag, 5-shot, limit=500, seed=42)
- Same lm-eval-harness wrapper structure (only `tok_encode`/`tok_decode` swapped)

### Tokenizer restoration → ubu1 deployment

The restored 64K BPE artifact (Mac: `state/clm_v4_tokenizer_restoration_2026_05_03/tokenizer_64k_multilingual.{model,vocab}`, SHA256 `bb851d39...`) was scp'd to ubu1's v2 outdir. Falsifiers re-verified on ubu1 prior to eval:

| Check | Spec | Result |
|---|---|---|
| SHA256 match | `bb851d39fbe3286dda11fc43da78d9bbf29ac6400d61b75616c8c750b710b8ab` | PASS |
| Vocab size | 64000 | PASS (`get_piece_size() = 64000`) |
| Special tokens | pad=0, bos=1, eos=2, unk=3 | PASS |
| Byte-fallback range | id 4 = `<0x00>`, id 259 = `<0xFF>` | PASS |
| English BPE merges | "hello" → ≤2 tokens (vs 5 for byte) | PASS (`[450, 11596]`) |
| Korean BPE merges | "안녕하세요" → ≤4 tokens (vs 15 for byte) | PASS (`[3346, 62255, 9216]`) |

The dead-symlink existing on ubu1 at `~/anima/data/tokenizer_64k_multilingual.model -> ../../ready/anima/config/...` was bypassed entirely; v2 used the freshly scp'd copy at `~/anima/state/p9_path_b_sanity_probe_v2_2026_05_03/tokenizer_64k_multilingual.model`.

---

## Interpretation

**The floor result is robust.** The +0.010 acc_norm delta is well within the ±0.019 stderr of either measurement. Three readings of this finding:

1. **Tokenization wasn't hiding capability.** If byte-fallback had been suppressing real English LM signal, V2 with proper BPE would have produced a markedly higher score. It didn't. CLM v4 base genuinely scores at random on HellaSwag English commonsense regardless of how text reaches the embedding rows.

2. **The architectural-blocker reframe is fully validated.** `docs/p9_benchmark_base_validation_landed_2026_05_03.ai.md` argued CLM v4 base ≠ a useful comparison point for English benchmarks because of (a) tokenizer mismatch with Llama, (b) no instruction tuning, (c) extreme overfit to narrow Korean-heavy corpus (training CE 0.046, perplexity ≈ 1.05). V1 confirmed this empirically with byte-fallback; V2 confirms it again with the model's actual training tokenizer. Two independent paths, same floor.

3. **A' main eval recommendation stands.** Skip CLM v4 base from cross-model benchmark scoring. Compare Llama base vs Llama+LoRA(clm-v4-sft-stage1 adapter) — the LoRA delta IS the actual question; CLM v4 base is a random-baseline anchor by both empirical paths now.

### Why isn't the score slightly LOWER with proper BPE?

A reasonable prior was that BPE might score even closer to random (0.25) than byte-fallback by averaging out token-level noise more cleanly. We observe +0.010 (BPE slightly higher). This is within noise but consistent with: BPE tokens compress the prompt, making more of the few-shot context fit before truncation (truncation rate at block_size=512 was 84.2% under BPE — see C3 below; byte-fallback truncation was certainly higher but wasn't logged in V1). More few-shot context → marginally more signal — which still lands inside the floor band.

---

## Honest C3 (raw#10)

- **(a) limit=500 wide CI**: same as V1 — ±0.019 stderr at score≈0.25; AT_FLOOR band [0.20, 0.30] accommodates both 0.242 and 0.252.
- **(b) Tokenization parity now real, not approximated**: V2 used the actual training-time `.model` (SHA-verified). Byte-fallback IDs 4-259 in V1 were faithful to the training-time embedding layout (the training tokenizer had `byte_fallback=True`), but BPE merges were lost. V2 restores those merges. The floor verdict survives both paths.
- **(c) Truncation rate 84.2% (1684/2000 loglik calls)**: even with BPE compression, 5-shot HellaSwag prompts overflow block_size=512 in the vast majority of cases. Truncation is **left-side** (drops oldest few-shot, preserves continuation intact). This applies symmetrically across all 4 HellaSwag candidates per query (each has the same truncation point), so it cannot bias the loglik *ranking* — it only erodes how much demonstration context the model sees. Net effect: V2 effectively measures "few-shot up to 512 tokens" which for most items collapses toward 1-2-shot or even zero-shot in practice. The floor verdict therefore reflects the model's behavior under truncated conditioning, not its hypothetical full-5-shot behavior. **For a true 5-shot eval, block_size would need to be larger than the model was trained at — which is out of scope (would require ALiBi/RoPE extension or retraining).** This caveat applies equally to V1.
- **(d) head_a only**: same as V1 — dual-head model; head_a (next-token) for loglik per spec §1.2(iii). Pre-registered.
- **(e) GPU contention**: V2 ran while two other ubu1 BG processes (`p9_paradigm_j_50k_v2.py` and `qmirror_alpha_burst_run_chsh.py`) were active. Did not preempt either (per spec). Wall increased 143s → 192s but throughput steady at ~10.7 it/s, no OOM.
- **(f) random_seed=42 explicit**: V1 may have used the lm-eval default; V2 explicitly passed `random_seed=42, numpy_random_seed=42, torch_random_seed=42, fewshot_random_seed=42` to ensure deterministic few-shot selection across re-runs. Same hellaswag dataset hash as V1 (`Rowan/hellaswag` revision `218ec52e09a7e7462a5400043bb9a69a41d06b76`).

---

## Files

```
state/p9_path_b_sanity_probe_v2_2026_05_03/
├── result.json          # primary verdict + V1/V2 comparison block
├── hellaswag_raw.json   # lm-eval-harness raw output (with truncation stats)
└── run.log              # full eval stdout/stderr (75KB)
state/markers/p9_path_b_sanity_probe_v2_landed.marker
docs/p9_path_b_sanity_probe_v2_landed_2026_05_03.ai.md  (this file)
```

ubu1 only (raw#9):
```
~/anima/state/p9_path_b_sanity_probe_v2_2026_05_03/eval_clm_v4_hellaswag_v2.py
~/anima/state/p9_path_b_sanity_probe_v2_2026_05_03/tokenizer_64k_multilingual.model
~/anima/state/p9_path_b_sanity_probe_v2_2026_05_03/tokenizer_64k_multilingual.vocab
```

---

## Cost / Time

- Cost: $0 (ubu1 local).
- Wall time: scp tokenizer + script ~30s; eval load ~5s; eval 192s; mirror artifacts ~10s; marker/doc ~5min.
- **Total: ~10min** (clean — no blocker investigation needed; V1 had already paved the path).

---

## Verdict

**`CLM_V4_AT_FLOOR` (CONFIRMED — robust to tokenization choice).**

V1 (byte-fallback) and V2 (proper 64K BPE) agree within 1σ. CLM v4 base scores at the random-chance floor on HellaSwag English commonsense via both tokenization paths. The reframe in `docs/p9_benchmark_base_validation_landed_2026_05_03.ai.md` is fully validated empirically; the byte-fallback workaround was not introducing a hidden bias. Treat CLM v4 base as a random anchor in A' main eval; compare LoRA deltas instead of base scores.

The restored 64K BPE tokenizer (`docs/clm_v4_tokenizer_restored_2026_05_03.ai.md`) is now also operationally validated on ubu1 — round-trip + falsifier checks all PASS, eval ran clean to completion. Future LoRA inference + BLM Phase 5 stimulus pipeline can use the restored tokenizer with confidence.
