# M4b longtrain — production-scale blockers (2026-05-28, fire agent)

The decisive dec_undertrain epoch-budget sweep at production V=151643 hit THREE
hard toolchain blockers that make MID/HI (the ≫V-presentation pods) intractable.
LO (1 epoch, the under-trained baseline) is the only tractable production datapoint.

## Measured facts (on H100 80GB SECURE pods, real Qwen2.5-1.5B BPE)
- BPE merge-table LOAD is O(1): 151387 merges / 151643 vocab loaded in 358 ms
  (hexa-lang #1869 fix confirmed for the LOAD path).
- BPE corpus ENCODE is NOT O(1): `get_merge_rank` (self/ml/tokenizer_bpe.hexa
  ~L200) is a LINEAR SCAN over 151387 merges per adjacent-pair lookup → encode is
  ~O(text_bytes × n_merges). Measured: full 2000-line corpus (1.27 MB) did NOT
  finish encoding in 15.5 min @ 100% CPU; 100-line/63 KB slice did NOT finish in
  180 s; only the 24-line/6.6 KB trim corpus encodes tractably (n_toks=6034).
- cuBLAS GPU path is BROKEN for the expert gemv shape [V=151643 × d=64] @ [d×1]:
  cuda_available()==1 (glue.c strong override WORKS), but
  `_hx_cuda_farr_matmul_gpu` → `cudaMemcpy C D2H failed: an illegal memory access
  was encountered`, returns -1. So mm() returns handle -1 (broken) on GPU; GPU
  util/mem stays 0 even mid-train. The CPU oracle path works but is slow.
- CPU step rate ≈ 0.26 s/step (1 epoch = 1507 steps did not finish in 401 s),
  dominated by the O(V) per-step scalar work: `mm_extract` copies the [V×d]=9.7M
  -element expert weights into a fresh buffer PER TOKEN + O(V) softmax/argmax/loss
  loops over V=151643. cuBLAS (if it worked) only accelerates the one gemv, not
  the O(V) extracts/loops, so it could not rescue the step rate to feasibility.

## Wall-time consequence (V=151643, 24-line corpus, 1507 steps/epoch, ~0.26 s/step)
| pod | epochs | steps    | ~wall @ 0.26s/step | feasible? |
|-----|--------|----------|--------------------|-----------|
| LO  | 1      | 1,507    | ~7 min             | YES |
| MID | ~1500 (40×V pres) | ~2.3M | ~7 days  | NO |
| HI  | ~7500 (200×V pres)| ~11M  | ~33 days | NO |

## Ruling
The toy (V=64) predicted ~50 epochs escapes. VERIFYING that at production
V=151643 is BLOCKED by hexa-lang toolchain limits (BPE encode complexity +
broken cuBLAS gemv + O(V) per-step CPU cost) — NOT by the anima trainer. This is
a toy→production transfer that could not be executed at scale, consistent with
the cross-cutting principle (transfer is not guaranteed AND may be unverifiable
with the current toolchain).

## a_runpod_inbox candidates (hexa-lang)
1. `self/ml/tokenizer_bpe.hexa get_merge_rank` linear scan → hashmap (O(1) rank
   lookup) so corpus encode is O(text) not O(text × n_merges).
2. `self/cuda/runtime_cuda.c _hx_cuda_farr_matmul_gpu` illegal D2H for [M=151643,
   N=1] gemv shape — out-buffer/grid sizing bug for the tall N=1 gemv.
