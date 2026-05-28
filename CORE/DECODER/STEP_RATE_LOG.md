# BC-ANIMA decoder trainer — step-rate measurements

Per `GPU.anima.md` "## 🩺 진단" + "## 📋 진행 마일스톤 (BC-ANIMA)" — running tally
of decoder trainer wall-time per step on the M4b production trainer
(`CORE/DECODER/train_v3_moe_longtrain.hexa`, d=64 · V=151643 · E=2 · h=256 ·
n_layer=1 · T=4 · HARD top-1 · m_size≈29M FP64 params).

Each row: code revision · pod · GPU · measurement window · steps/s.

## Log

### Pre-M4 baseline — anima PR #1318 STEP_RATE_FINDING (2026-05-28)

- Code: pre-`farr_softmax_rows`/`farr_ce_seed` wiring. Per-step hot-path =
  V-wide CPU softmax (~3V `farr_get` + 1 `exp` + 1 `log`) + 29M-param CPU
  AdamW + structurally-truncated CE seed (`farr_set(d_logits, target, 1.0)`,
  no `softmax - onehot`).
- Pod: RunPod H100 SXM `4q2rab8ds2zhsr` (torn down post-fire; no longer
  available in the runpod registry).
- Measured: ~1 step/s (per PR #1318 + `M4B_LONGTRAIN_RESULT.md` block ③ —
  "CPU step rate ≈ 0.26s/step (1 epoch=1507 step in 401s not completed)";
  GPU util/mem stayed at 0% during training; one cuBLAS gemv path errored
  out and reverted to CPU).
- Verdict: production sweep declared UNVERIFIABLE-AT-SCALE — `dec_undertrain`
  could not be tested because wall budget made MID/HI infeasible.

### Post-M4 wiring — anima PR #1320 (2026-05-28, merged d3107f266)

- Code: M2 `farr_softmax_rows` + M3 `farr_ce_seed` wired into the same
  trainer (commit `a16815267`, 25+/15- net). Per-step softmax now runs on
  the H100 under `HEXA_CUDA` build (kernel `_hx_cuda_farr_softmax_rows_gpu`);
  CE seed now runs on the H100 (kernel `_hx_cuda_farr_ce_seed`); CE
  monitoring scalar now reuses the precomputed softmax (`-log(sm[target])`
  with a 1e-300 floor) instead of a fresh V-wide loop.
- Pod: target was the same H100 SXM `4q2rab8ds2zhsr`, but the pod is no
  longer in the runpod registry (`hexa cloud list --provider runpod` →
  0 pods) and the two cached vast pods (`37868501`, `38095989`) are SSH-
  unreachable (`ssh transport failure (exit 255)`).
- Measured: ⚪ **deferred** — no live GPU pod available, and the M4 task
  is constrained "Don't spin up new pods — pod `4q2rab8ds2zhsr` is the
  existing one" (rate-limited retry guardrails).
- Trainer `hexa parse` is clean. CPU helper byte-eq for both builtins is
  already proven (M2 PR #1920 + M3 PR #1924 each landed with a byte-eq
  oracle PASS). The wiring change itself is therefore green at the
  symbolic + CPU-numerical layer; only the wall-time speedup is unmeasured.

### Expected gain (calculation, not measurement)

Pre-M4 per-step hot loops were:
  1. CE seed truncated (no V-wide work, but gradient was structurally wrong).
  2. CE-monitoring softmax: 3V `farr_get` + V `exp` + 1 `log`. At V=151643
     and a measured ~0.26 s/step, this loop alone is ~hundreds of ms.

Post-M4 the same softmax runs as one CUDA kernel launch (`_hx_k_softmax_rows`
two-pass max+sumexp, V threads). On H100 the V=151643 reduction is
bandwidth-bound and well under 1 ms — the CPU/GPU ratio for this single op
is expected to be 100×+, but the trainer's residual CPU cost (29M-param
AdamW + `mm_extract` of [V×d] expert weights per step) is unchanged and
will set a new ceiling. Whether the combined wiring crosses the ≥10 step/s
green-tier gate is **not predictable from this change alone** — the AdamW
CPU loop (M1) and the expert weight copy are likely the next dominant
costs once softmax/CE move to GPU. A follow-up wedge (M1 wiring +
`mm_extract` GPU port) is likely required to reach 10 step/s.

### Verdict (g5 rubric)

🟠 **PARTIAL** — wiring landed and symbolically green (parse clean, byte-eq
already proven for both builtins). Wall-time measurement deferred to the
next live H100 fire (a new pod-rent + sweep cycle, gated by user/budget
approval). The follow-up wedge to file (post-measurement, if step-rate
< 10 step/s):

  - **F-BC-ANIMA-M4-CEILING** — measure step-rate with M4 wiring. If
    < 10 step/s, profile residual: (a) 29M-param CPU AdamW loop (M1
    `farr_adamw_step_gpu` is already a registered builtin in
    `stdlib/flame/train_lib.hexa:59` — wire it next), (b) per-step
    `mm_extract` of [V×d] expert weights, (c) the small d=64 matmul
    under-utilizing the GPU. The diagnosis already noted (c) as a known
    decoder-shape problem (d=64 too small for matmul TC utility).

See `GPU.anima.md` "## 📋 진행 마일스톤 (BC-ANIMA)" + the
`.discoveries/decoder_collapse_undertrain.tape` SSOT for the broader
saga (M4 unblocks M5 = `dec_undertrain` decisive re-fire, gated on
step-rate ≥ 10 step/s).
