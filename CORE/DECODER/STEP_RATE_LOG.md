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

### M5 fire attempt — F-BC-ANIMA-M4-CEILING (2026-05-28, $5/30min budget)

User-approved live H100 fire attempt — pre-registered falsifier
`F-BC-ANIMA-M4-CEILING` (measure step-rate with M4 wiring on H100; <10
step/s triggers M1 + `mm_extract` follow-up wedges).

- Cached vast pods (`37868501` ssh6.vast.ai:28500 · `38095989`
  ssh9.vast.ai:15988): ssh-port resolve OK but `hexa cloud exec` both
  returned **`ssh transport failure (exit 255)`** verbatim — guard text:
  "host unreachable (connection refused / timeout / auth / changed host
  key). The pod may be alive and billing but not accepting SSH — a
  vast.ai/RunPod transport outage. Stop retrying; verify reachability
  or tear the pod down." Matches the deferred-state note above (vast
  pods SSH-unreachable).
- Fresh RunPod H100 SXM rented — `hexa cloud rent runpod
  --gpu "NVIDIA H100 80GB HBM3" --disk 50 --owner bc-anima-m5` →
  `[cloud] rent runpod: created pod 3e541pil5jazhk` →
  `[cloud] rent runpod: READY 64.247.201.49:11038`. Registry confirmed
  pod live in `hexa cloud list --provider runpod`.
- SSH polling against 64.247.201.49:11038 — first probe at +0s, retry
  loop every 8-15s for ~7 minutes. Every single `hexa cloud exec`
  returned the same `ssh transport failure (exit 255)` verbatim guard
  text. `hexa cloud resolve` continued to print `64.247.201.49:11038`
  unchanged (no port flap). Pod was billing but SSH transport refused
  for the full polling window — same outage class as the cached vast
  pods.
- Per the policy guardrail ("If pod spin-up itself fails — region
  exhaust, quota — report and abort"), and per the guard text's own
  "Stop retrying; verify reachability or tear the pod down" directive,
  the pod was torn down: `hexa cloud down 3e541pil5jazhk
  --provider runpod` → `[cloud] down runpod: terminated 3e541pil5jazhk
  / [cloud] forgot 3e541pil5jazhk (registry status=closed)`.
  Post-teardown `hexa cloud list --provider runpod` →
  `[cloud] runpod: list (new) — 0 pods`. `hexa cloud pods` →
  `pods=0   jobs=0`.
- Wall budget consumed: ~501s (~8.4min of the 30min cap). Spend
  estimate: ~$0.56 (~11% of the $5 cap, assuming $4/hr H100 SXM).
  Stage 1 was NOT entered — pod never accepted SSH so trainer was
  never copied, built, or executed. Stage 2 likewise NOT entered.

#### Verdict (g5 rubric, this attempt)

⚪ **UNVERIFIABLE-AT-SCALE (infrastructure)** — F-BC-ANIMA-M4-CEILING
remains pre-registered but unmeasured. The falsifier was NOT reached
(0 trainer steps run). The result is NOT a measurement of M4 wiring;
it is a measurement of pod SSH-transport availability on the day of
the fire — three pods in a row (2 vast + 1 freshly-rented runpod)
declined SSH. This is the same RunPod/vast transport-outage class
already noted in the post-M4 entry above; today's attempt confirms
the outage extends to fresh pod rentals as well.

The 🟠 PARTIAL verdict on M4 wiring itself (parse clean, byte-eq
proven, wall-time deferred) is UNCHANGED. M5 remains the next live
fire when SSH transport is reliably available; the M1 follow-up wedge
is still the next-action if step-rate measures <10 step/s.

No false claim filed in CLAIMS.tape / atlas — per g5 (no LLM
self-judge of correctness; only run/no-run reported here).
