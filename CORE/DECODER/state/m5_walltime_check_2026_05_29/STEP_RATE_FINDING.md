# M5 wall-time check — FINDING (2026-05-29)

Falsifier: **F-BC-ANIMA-M4-CEILING** (re-attempt after #1324).

## Verdict: ⚪ UNVERIFIABLE-AT-SCALE (infrastructure) — but BUILD now GREEN

The 500-step wall-rate was NOT measured: the H100 pod's container was reset
mid-session (3rd consecutive pod, same churn that wiped the worktree) immediately
AFTER a clean `clang_rc=0` build but BEFORE the fire log could be captured. The
falsifier remains pre-registered + unmeasured (0 trainer steps logged).

HOWEVER this attempt made decisive forward progress past #1324, on TWO fronts:

### Finding 1 — the #1324 "ssh transport outage" was an SSH-KEY MISMATCH (RESOLVED)

`hexa cloud exec` / the `runpodctl … .ssh.ssh_command` point at
`~/.runpod/ssh/RunPod-Key-Go` (RSA, SHA256:2bo…). But RunPod seeds the pod's
`authorized_keys` from `env.PUBLIC_KEY`, which is the LOCAL `~/.ssh/id_ed25519`
(`…KOEWe0SBseZceuCgcVnlNDhEwbU/TIqGeK9FdrpIy9V ghost@ghostui-MacBookAir.local`).

- `ssh -i ~/.ssh/id_ed25519 …` → AUTHENTICATES, runs commands (verified:
  `nvidia-smi -L` → NVIDIA H100 80GB HBM3, nproc=224, scp + build all ran).
- `ssh -i ~/.runpod/ssh/RunPod-Key-Go …` → `Permission denied (publickey,password)`
  → reported by `hexa cloud exec` as the generic "ssh transport failure (exit 255)
  … vast.ai/RunPod transport outage" guard text.

⇒ #1324's "outage" was NOT a runpod/vast outage — it was the wrong SSH key.
   FIX for hexa-lang inbox (a_runpod_inbox): make `hexa cloud {exec,run,copy-to}`
   offer `~/.ssh/id_ed25519` (the key whose pubkey runpod injects), not just
   RunPod-Key-Go. Workaround in hand: bare `ssh/scp -i ~/.ssh/id_ed25519`.

### Finding 2 — the M4-wired trainer BUILDS + LINKS with cuBLAS (clang_rc=0)

The post-M4 trainer (`train_v3_moe_longtrain.hexa`, PRs #1319/#1320/#1322/#1323)
compiled clean to a 1,012,200-byte H100 binary under `-DHEXA_CUDA -arch=sm_90`,
cuBLAS + CUDA-driver linked. Two toolchain blockers had to be cleared first:

1. **M2/M3 builtins absent from the installed hexa-lang.** The trainer calls the
   in-place 4-arg `farr_softmax_rows(x, out, R, C)` and the slim 5-arg
   `farr_ce_seed(softmax, target, dlogits, R, C)`. The HEAD-installed hexa-lang
   `self/runtime.c` only has the `_gpu`-suffixed return-a-new-id variants →
   `error: use of undeclared identifier 'farr_softmax_rows'`. RESOLVED by using
   the `~/core/hexa-lang/.worktrees/cloud-m3` `self/runtime.c` (which has the
   in-place wrappers) overlaid with HEAD's `self/runtime_core.c` + `self/cuda/`.
   (lesson: `flame_bpe_corpus_lib stale install` — the M2/M3 host wrappers are
   only in the cloud-m3 worktree, NOT in the `~/.hx` install.)

2. **`_hx_cuda_farr_ce_seed` kernel was authored AHEAD of its definition.** The
   cloud-m3 host wrapper `hexa_farr_ce_seed()` hard-calls a slim block-per-row
   CUDA symbol `_hx_cuda_farr_ce_seed(softmax,target,dlogits,R,C)` that exists in
   NO checked-out `runtime_cuda.c` (only the 6-arg fused `_hx_cuda_farr_ce_seed_gpu`
   does) → `undefined reference`. RESOLVED by writing the missing kernel
   (`ce_seed_slim_shim.c.txt` here, ~60 LoC): `dlogits[r*C+c] = softmax[r*C+c]
   - onehot(c==target[r])`, mirroring `_hx_k_ce_seed`'s device-array seam
   (`_h2d`/`_ensure_dev_alloc_out`/`g_slots`/`_d2h_out`, HX_RR_BLOCK grid). This
   is the genuine missing M3-slim kernel and should be upstreamed to hexa-lang.

3. **glue.c now double-defines `hexa_cuda_available`.** The cloud-m3 runtime has
   a REAL `hexa_cuda_available → _hx_cuda_runtime_available` (line 14291), so the
   old glue.c strong-override shim (a weak-stub-era workaround) now conflicts
   (`multiple definition`). RESOLVED by linking WITHOUT glue.c.

Build line that succeeded (no glue.c):
```
nvcc -O2 -std=c++14 -DHEXA_CUDA -arch=sm_90 -x cu -c self/cuda/runtime_cuda.c -o runtime_cuda.o   # rc=0
clang -O2 -D_GNU_SOURCE -D_XOPEN_SOURCE=600 -DHEXA_CUDA -I self -I /usr/local/cuda/include \
  -Wno-trigraphs -fbracket-depth=8192 -Wno-incompatible-pointer-types-discards-qualifiers \
  -Wno-macro-redefined trainer.c self/runtime.c runtime_cuda.o \
  -L/usr/local/cuda/lib64 -L/usr/lib/x86_64-linux-gnu \
  -lcublas -lcudart -lcudart_static -lcuda -ldl -lrt -lm -lpthread -lstdc++ -o trainer  # clang_rc=0
```

## What was NOT measured

- step_rate (step/s) — pod died after build, before the 500-step fire logged.
- nvidia-smi utilization.gpu avg — telemetry never started (DONE-gated loop).
- cuBLAS gemv illegal-mem (Blocker 2) — UNTESTED (run never started). NOT
  confirmed active, NOT confirmed clear — simply unreached this attempt.
- ratio vs pre-M4 ~1 step/s baseline — N/A (no measurement).

## Pod lifecycle (all torn down, $0 net billing)

| pod | name | port | fate |
|-----|------|------|------|
| cpnocpur5jjf5e | m5-walltime    | 13798 | uptime never >0; restart→404 |
| nyvghgacgb1cp3 | m5-walltime-r2 | 16917→reset | reachable (id_ed25519), /work wiped on reset, →404 |
| 2a468nyn6947gc | m5-walltime-r3 | 12673→reset | **clean build clang_rc=0**, container reset before fire, →404 |

`runpodctl pod list` → `[]` (0 pods) at teardown. All forgotten from registry.
Container-reset pattern (3/3) correlates with the concurrent workspace-sync churn
that also deleted the `/tmp/wt-m5probe` worktree mid-session.

## Next action (M5 re-fire, when a STABLE pod is available)

The build is now reproducible (combo2 self/ + ce_seed shim + no glue.c, ssh via
id_ed25519). A single uninterrupted pod will measure the 500-step rate in <8 min.
The toolchain blockers are CLOSED; only pod-stability remains. The wedge ladder
(M1 already wired; mm_extract per-step V×d copy still CPU) is the next profiling
target IF the measured rate lands 5–20 step/s (🟡).
