# M4b-fire-rev2 — fire blocked (sign-gate) · honest surface (2026-05-28)

## summary

The autonomous fire path for **train_v3_moe_pilot_rev2** is **BLOCKED** by a
Mac-local sign-gate on the canonical `hexa build --c-only` transpile step. Pod
was created and validated (H100 PCIe 80GB available), then torn down to contain
cost when the gate surfaced.

- **artifacts ready**: trainer (rev2) + diverse corpus builder + dispatcher,
  all `hexa parse` clean, branch `feat/m4b-fire-rev2-diverse-corpus`.
- **pod created + verified**: `ydaz9wvlqlv7d9` (H100 PCIe @ $2.89/hr · 81GB free
  · SSH 3-consec stable · cuda 12 visible).
- **pod torn down**: ~14min @ $2.89/hr = **~$0.67 actual cost** (vs $3-5 budgeted).
- **blocker**: `sidecar sign local` token absent → all `hexa build`, `clang`,
  `gcc`, `python` heavy invocations refuse on Mac absolute paths.

## what was done (autonomous)

1. **Scope-check** — train_v3_moe_pilot.hexa (Phase 5b, 812 LoC) + Phase 5b
   verdict 2/5 PASS + D3 #1269 finding (corpus-skew root cause, NOT router).
2. **Diverse corpus build** — `training/build_corpus_diverse_v2.hexa` (hexa-native)
   extracted 2K Korean QA lines from `corpus_alm_70b.jsonl` (90K source lines)
   into `training/corpus_consciousness_v2_diverse.jsonl` (~1.2MB, derived not
   committed). Ran clean on Mac local (no GPU/build).
3. **Trainer fork rev2** — `CORE/DECODER/train_v3_moe_pilot_rev2.hexa` (812 LoC):
   - corpus path → diverse v2
   - n_steps 20 → 200 (10× signal budget)
   - n_decode 20 → 100 (stable TTR/LZ76 sample)
   - LZ76 verdict inlined (g61 reuse from d1_lz76_collapse_proxy)
   - F-M4B-FIRE-1' (TTR≥0.30) + F-M4B-FIRE-LZ (LZ_norm≥0.50) + F-M4B-FIRE-3
     (distinct_experts) + F-M4B-FIRE-4 (CE monotone) + F-M4B-FIRE-router (HARD)
   - result.json + verdict matrix written to `/opt/anima/state/m4b_pilot_rev2/`
   - HARD top-1 router preserved (M4b toy 🟢 + Phase 5b 2/2 distinct PASS)
   - `hexa parse` OK
4. **Dispatcher rev2** — `CORE/DECODER/dispatch_m4b_pilot_rev2.hexa` (artifact-of-
   record · pod create + RUNNING poll + provisioning runbook printer).
5. **Pod fire** — RunPod H100 PCIe 80GB created (`ydaz9wvlqlv7d9`):
   - $2.89/hr · CA secure cloud · 60GB disk · 22/tcp
   - SSH ready in ~30s (`root@62.169.159.96:45135`)
   - 3-consec SSH stability PASS (Vast.ai flakiness pattern not present)
   - clang + gcc + git installed (apt update + install build-essential)
   - hexa-lang origin/main cloned to `/opt/hexa-lang` (10629 files)
   - flame_bpe_corpus_lib present in pod's `stdlib/flame/` ✓
   - pre-built `build/hexa_linux` + `build/hexat_linux` exist but require
     **GLIBC 2.38** (pod has 2.35 on Ubuntu 22.04) → cannot run on pod.

## the GLIBC blocker (hexa-lang side)

`/opt/hexa-lang/build/hexa.real` (canonical `hexa run` interpreter binary)
requires GLIBC ≥ 2.38, but the runpod/pytorch image is Ubuntu 22.04 (GLIBC 2.35).
The `install.sh` script's `module_loader` build step also fails (no git in PATH
during install).

This means **the canonical "hexa run trainer.hexa on the pod" path is dead** on
Ubuntu 22.04 pods. Phase 5b's actual fire path (per `CORE/DECODER/DECODER.md`)
worked around this by:

1. **Mac-local transpile**: `hexa build --c-only` produces `trainer.c`.
2. **scp trainer.c + runtime fragments + glue.c** to the pod.
3. **Pod compile**: `clang -DHEXA_CUDA trainer.c glue.c self/runtime.c
   runtime_cuda.o -lcublas -lcudart -lcuda -o trainer`.
4. **Pod fire**: `./trainer`.

The 5-workaround chain documented in DECODER.md:
- (a) `HEXA_STDLIB_ROOT` env respected by `hexa build --c-only` (real-BPE unblock)
- (b) `flame_bpe_corpus_lib` import resolves via HEXA_STDLIB_ROOT
- (c) `trim` undeclared cross-backend gap → inline sed patch on trainer.c
- (d) `runtime_core.c`+`runtime_hi_gen.c` are `#include`d by runtime.c (NOT
       separate compilation)
- (e) corpus paths Mac-hardcoded → pod sed-replace `'…→/root/'`

## the Mac sign-gate blocker (sidecar side)

Step (1) Mac-local transpile is gated by **sidecar `sign local`**:

> local-bound heavy invocation (hexa · python · gcc/g++/clang/cc · sh <script>)
> on an absolute host path needs a fresh sign-off — the canonical mac
> fork-storm trigger. USER: run `! sidecar sign local` in the TUI prompt
> (30min token — covers a full build), then retry.

`hexa build` is one of the gated invocations. The agent cannot self-bypass.

**This is the surface honest of the directive**: a_completeness_over_cheap
forbids me from inventing a workaround (e.g. `--c-only` substitute, hexa-lang
fork to pure-C generator) that would compromise the production path. The fix
is one user command (`! sidecar sign local`), then the fire continues.

## what continues after sign-off (30 minutes of work)

1. **Transpile** (Mac, ~30s):
   ```
   HEXA_MAC_BUILD_OK=1 HEXA_STDLIB_ROOT=/Users/ghost/core/hexa-lang \
     hexa build CORE/DECODER/train_v3_moe_pilot_rev2.hexa --c-only \
     -o build/trainer_rev2.c
   ```
2. **trim sed patch** (Mac, 3 occurrences):
   ```
   sed -i '' 's/hexa_call1(trim,/rt_str_trim(/g' build/trainer_rev2.c
   ```
3. **Recreate pod** (RunPod or Vast.ai H100 80GB).
4. **scp bundle**: trainer.c + runtime fragments (self/runtime.c +
   runtime_core.c + runtime_hi_gen.c + runtime.h + cuda/runtime_cuda.c +
   runtime_bf16.c + forge/* + native/*) + glue.c + Qwen tokenizer +
   diverse corpus.
5. **Pod build**:
   ```
   nvcc -DHEXA_CUDA -arch=sm_90 -c runtime_cuda.c -o runtime_cuda.o
   clang -DHEXA_CUDA trainer_rev2.c glue.c self/runtime.c runtime_cuda.o \
     -lcublas -lcudart -lcuda -o trainer
   ```
6. **Pod fire**: `./trainer 2>&1 | tee train.log` (~1-2hr · ~$3-5).
7. **Harvest + LZ76 verdict + HF upload** (a_hf_autonomous).

## audit trail

- Pod ID: `ydaz9wvlqlv7d9` (DELETED 2026-05-28 00:34 UTC)
- Pod cost: **~$0.67** (14min × $2.89/hr · leaked artifacts: none)
- Budget remaining for rev2: **~$2-4** when fire continues post-sign-off
- Branch: `feat/m4b-fire-rev2-diverse-corpus` (3 commits)
- Files ready: 4 new (builder + trainer + dispatcher + this doc) + 1 derived
  corpus (1.2MB, not committed)
- Honest scope: a_completeness_over_cheap maintained — no shortcut taken;
  blocker surfaced not silently bypassed.
