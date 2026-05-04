# hexa-lang Upstream Audit — ML Training Capability Gap + Roadmap (2026-05-03)

> **Trigger**: VLM stage1 ABORT (state/markers/vlm_stage1_aborted.marker, 2026-05-04). Root: `audio_token_predictor.hexa` (1576 LoC, Mk.III) cannot execute on PyTorch/RunPod because:
> - hexa runtime not on ubu1 (`ssh ubu1 'which hexa hxcc hx'` = empty)
> - no `.py` port exists (find audio_token_predictor* -not -name *.hexa = empty)
> - hexa C codegen output is Mk.I stub (build/artifacts/audio_token_predictor_nb.c = 57 LoC, returns `tok = step*7 mod 1024`)
> - `feedback_py_to_hexa_only` (raw#9 STRICT) bans `.py` creation on Mac including `_python_bridge/`
>
> **Output**: comprehensive audit + ML gap matrix + 5 ranked tracks + VLM-specific unblock recommendation

---

## 1. Executive Summary

**hexa-lang current state**: mature **language + self-host compiler + native runtime + extensive ML "shell"** (510 .hexa files in `self/ml/`, 9648 LoC of C/CUDA FFI shims). Compiler targets: ARM64, x86_64, VM, ESP32, FPGA Verilog, WGSL. **No PyTorch/Python codegen target exists.**

**ML capability — actual training readiness** (vs marketing surface):

| Layer | Surface (hexa) | Backend (live?) | Verdict |
|---|---|---|---|
| Pure-hexa NN math (relu/softmax/layernorm/gelu) | `stdlib/nn.hexa` 149 LoC | ✓ executes (interpreter, scalar fp64) | **CPU toy only** — list ops, O(n) per element-wise, useless beyond <1k params |
| Pure-hexa optim (Adam + LR sched) | `stdlib/optim.hexa` 21 LoC | ✓ executes | **CPU toy only** |
| GPU training stack (cuBLAS+NVRTC) | `self/ml/gpu_train.hexa` 2357 LoC | depends on hxqwen14b CUDA v5+ | **partial** — kernels exist (RMSNorm/RoPE/GQA/SwiGLU/AdamW/CE in hxqwen14b_cuda.cu 1391 LoC) but `hxqwen14b_generate` and 3 LoRA entry points return `RC_ERR_CUDA_TODO=-5` (per `doc/plans/python_serving_purge_audit_20260419.md` §4 P7) |
| Audio (whisper-style encoder) | `self/ml/audio_encoder.hexa` ~700 LoC | scalar pure-hexa | **spec-only** for serious training |
| Distributed train (multi-GPU/FSDP) | `self/ml/distributed_train.hexa` 518 LoC | depends on hxccl_linux 704 LoC C | **untested at scale** in repo state |

**Critical gap for VLM**: hexa-lang has **no path** to execute `audio_token_predictor.hexa` on a real GPU **today** because:
1. hexa native runtime (hexa.real Mach-O arm64) doesn't exist on ubu1/RunPod (Linux only via build, not deployed).
2. C codegen for ML files emits a degenerate stub (audio_token_predictor → 57-line stub vs 1576 source).
3. CUDA path is Qwen14B-shaped, not audio-token-predictor-shaped (no audio-specific kernels published live).
4. No PyTorch transpiler.

**Resolution shape**: hexa-lang needs **either** (a) a hexa→PyTorch transpiler so `audio_token_predictor.hexa` becomes runnable `.py`, **or** (b) hexa native deployed to ubu1+RunPod with C codegen brought to parity with source. (a) is days; (b) is months.

**Ranked recommendation** (완성도 lens; details §6):

1. **Track A — hexa→py transpiler (VLM-shaped subset first)** ★ recommended
2. **Track D — hexa+Python FFI via embedded interp**
3. **Track E — dual-source maintenance with audit trail** (current de-facto state; formalize)
4. **Track B — hexa stdlib expansion (tensor/PyTorch FFI surface)**
5. **Track C — hexa runtime overhaul (JIT/AOT for ML)**

---

## 2. Repository Inventory

### 2.1 hexa-lang locations on this machine

| Path | Role | Live? |
|---|---|---|
| `/Users/ghost/core/hexa-lang` | **Primary repo** (91 top-level entries, .git active, .roadmap chflags-locked) | ✓ canonical |
| `/Users/ghost/core/legacy/hexa-lang` | Archive (.roadmap snapshot only, 60KB) | frozen |
| `/Users/ghost/core/nexus/hexa-lang` | nexus-side benchmark/manifest (rt-commands, ml-next-level, etc.) | nexus-owned |
| `/Users/ghost/Dev/hexa-lang` | Build skeleton (only `build/`) | scaffold |
| `/Users/ghost/core/anima/anima-tools/hexa-bridge` | anima→hexa intent bridge (1 file: bridge.hexa) | anima-owned |

**Audit subject** = `/Users/ghost/core/hexa-lang`.

### 2.2 stdlib coverage (ML-relevant)

```
stdlib/
├── nn.hexa                  149 LoC  relu/sigmoid/tanh/softmax/gelu/layernorm/linear/mlp2/CE
├── optim.hexa                21 LoC  adam wrapper + scheduled_lr + safe_update
├── proc.hexa                446 LoC  proc_spawn_supervised + proc_run_with_stdin (P0) + proc_run_json_bridge (P0)
├── json.hexa                155 LoC
├── http.hexa                133 LoC
├── bytes.hexa               195 LoC
├── linalg/                  ffi/dispatch/reference/mod  — wraps hxblas
├── matrix/                  construct/stack/mod
├── math/                    eigen, rng, permille, strict_fp
├── optim/                   cpgd (constrained PGD), projector
├── tokenize/                tokenizer_spec
├── consciousness.hexa       — anima-bridge primitive
├── parse.hexa, string.hexa, collections.hexa, yaml.hexa, qrng_anu.hexa
└── portable_fs.hexa
```

**P0 status (per session memory anchor)**: `proc_run_with_stdin` + `proc_run_json_bridge` — **LIVE** (stdlib/proc.hexa L395-L444, both `pub fn`).

**P1 status**: json.hexa / http.hexa / bytes.hexa — **LIVE** (155+133+195 LoC respectively).

### 2.3 ML "shell" (self/ml/, self/native/)

```
self/ml/    510 .hexa files  — every named pattern: lora, adalora, molora, mixture_of_lora,
                              adapter_fusion, attention_fused, attention_sink, gqa, mla, mha,
                              flash_attention, gpu_*, cuda_*, distributed_train, fp8_training,
                              tokenizer_trainer, train_100m_alpha[1..10], audio_encoder,
                              activation_checkpointing, awq, aqlm, bitnet, marlin_kernel,
                              speculative_*, medusa, eagle_*, paged_attention, kv_cache, ...

self/serve/    serve.hexa (1089 LoC) + serve_alm.hexa (1302 LoC) + http_server.hexa (~400 LoC)

self/native/   hxqwen14b.c           5752 LoC  — core CUDA FFI shim (Linux x86_64 + Mac stub)
               hxqwen14b_cuda.cu     1391 LoC  — actual CUDA kernels
               hxblas_linux.c         836 LoC  — cuBLAS sgemm wrappers
               hxccl_linux.c          704 LoC  — NCCL collective
               hxflash_linux.c        579 LoC  — flash-attention kernel host-side
               hxlmhead_linux.c       293 LoC
               hxlayer_linux.c         93 LoC
               hxqwen32b.c            (sibling 32B variant)
               hxqwen14b_cuda_*.cu    (RMSNorm/RoPE/GQA/SwiGLU/AdamW/CE — found in 1391 LoC)
               hxcuda_conv1d.cu, hxcuda_fused.cu, hxcuda_stft.cu  — audio-relevant CUDA
               hxcuda_istft (anima-voice/build_hxcuda_istft.hexa references)
```

### 2.4 Compiler/codegen

```
self/codegen_c.hexa             AST → C source
self/codegen_c2.hexa            C codegen v2 (newer)
self/codegen_c_min.hexa         minimal C
self/codegen_native.hexa        in-mem native (with arm64+x86 IR)
self/codegen_native_elf.hexa    ELF emit
self/codegen_native_fib.hexa    early native target
self/codegen_asm.hexa           assembly
self/codegen_wgsl.hexa          WebGPU shader
self/codegen_verilog.hexa       Verilog (FPGA target)
self/codegen_esp32.hexa         ESP32 microcontroller
self/codegen/                   arm64 + x86 IR backends, neon_fp16_gemm, peephole, regalloc
```

**No `codegen_python.hexa`. No `codegen_pytorch.hexa`.** Transpilation surface ends at C+native+wgsl+verilog+esp32.

### 2.5 Python "shadow" (the unspoken bridge)

| Surface | Count | Purpose |
|---|---|---|
| `_python_bridge/` (anima/state/qmirror_phase1_staging/...) | 1 file (`aer_runner.py`) | currently | one orphan |
| `state/.X_helper.py` (auto-generated transient) | **~25 files** | hexa scripts emit then exec via `project_python()` (RFC-008 P1 done) — **the established escape hatch**, contradicts `feedback_py_to_hexa_only` strict reading |
| `tool/active_redteam_*.py`, `tool/anima_holographic_ib_ksg_validate_prod.py` | 3 files | **explicit `.own 1` opt-out** (raw 9 grandfather list, gitignored, scipy-required) |
| `ready/*.py` | 1431 files | **opt-out** (historical archive, gitignore) |

**Hexa upstream itself**: `gate/wrappers/bin/python3` + `gate/wrappers/src/python3.hexa` exist as PATH guards (block accidental system python3 invocation). Per `doc/plans/python_serving_purge_audit_20260419.md`: serving/inference path has **0 python3 invocations**, **0 torch/transformers/peft imports**.

---

## 3. ML Capability Matrix (vs PyTorch baseline)

| Capability | hexa-lang surface | hexa-lang execution | PyTorch parity | Notes |
|---|---|---|---|---|
| **Tensor allocation (fp32)** | `stdlib/matrix/construct.hexa`, lists | scalar interpreter | ❌ | List-based; no contiguous buffers |
| **Tensor allocation (fp16/bf16)** | `self/ml/cuda_ffi.hexa` device ptrs | CUDA path: ✓ via cuBLAS | ✓ in CUDA path | Only on Linux+NVIDIA |
| **MatMul (CPU)** | `stdlib/linalg/ffi.hexa` → hxblas | C-FFI | ✓ via OpenBLAS | Linux-built |
| **MatMul (GPU)** | `gpu_sgemm` family (cuBLAS) | extern → hxblas_linux.c | ✓ | Linux+CUDA only |
| **Autograd** | none | none | ❌ | Hand-written backward in each `gpu_layer_bwd` |
| **Optimizer state (Adam m/v)** | `stdlib/optim.hexa`, `gpu_train.hexa::alloc_adamw_state` | CPU: pure-hexa; GPU: `hxqwen14b_cu_launch_adamw_step` LIVE per kernel L1248 | partial | AdamW kernel exists, multi-tensor not |
| **LoRA fwd/bwd** | `self/ml/lora.hexa` 158 LoC + `lora_hotswap.hexa` 317 LoC + `mixture_of_lora.hexa` | hxqwen14b LoRA entries return `-5 RC_ERR_CUDA_TODO` (v5 pending per audit doc 2026-04-19) | ❌ today | Spec ready, kernels stubbed |
| **DataLoader** | `distributed_train.hexa::dist_train_with_data` | tokenizer_bpe.hexa exists | partial | No streaming, no num_workers parallelism |
| **Tokenizer (BPE/SP)** | `self/ml/tokenizer_trainer.hexa`, `stdlib/tokenize/tokenizer_spec.hexa` | pure-hexa BPE train/encode/decode | ✓ for training | Slow vs HF tokenizers |
| **Checkpoint (HEXACKPT-v1)** | `gpu_train.hexa::save_checkpoint_gpu` | live (Linux+CUDA) | custom format | NOT compatible with HF safetensors |
| **HF safetensors load** | none | ❌ | ✗ | Critical gap for using pretrained weights |
| **Multi-GPU (NCCL)** | `self/ml/launch_multigpu.hexa`, hxccl_linux.c 704 LoC | Linux only | partial | Untested at >1 H100 in repo state |
| **Mixed precision (fp8/bf16)** | `self/ml/fp8_training.hexa` | scalar surface | ❌ | Spec-only |
| **Flash attention** | `self/ml/flash_attention.hexa`, `mps_flash_attention.hexa`, hxflash_linux.c 579 LoC | Linux+CUDA | partial | Mac MPS variant exists |
| **STFT/iSTFT (audio)** | `anima-voice/hxcuda_istft_bridge.hexa`, `hxcuda_stft.cu` | hexa→CUDA C bridge | partial | Audio kernels exist! |
| **Mel filterbank** | `self/ml/audio_encoder.hexa::ae_mel_filterbank` | pure-hexa scalar | ❌ realtime | Toy-scale only |
| **RVQ codebook** | `anima-voice/rvq_*.hexa` referenced | unverified live | ❌ | spec-shape only |

**Bottom line**: hexa-lang has **wide spec surface**, **narrow live execution** (Linux+NVIDIA Qwen14B-shaped only), and **zero compatibility** with HuggingFace ecosystem (safetensors / tokenizers / datasets / transformers / peft).

---

## 4. Codegen Output Quality — concrete failure mode

`build/artifacts/audio_token_predictor_nb.c` (last codegen output, 57 LoC):

```c
HexaVal predict_frame(HexaVal intent_mem, HexaVal prev_tokens, HexaVal step) {
    HexaVal tok = hexa_mod(hexa_mul(step, hexa_int(7)), hexa_int(1024));
    return hexa_to_string(tok);
}
```

vs `anima-voice/audio_token_predictor.hexa` source (1576 LoC, Mk.III with KV-cache, 8-stage RVQ delayed-pattern, CFG, top-k sampling).

**The C codegen took a Mk.I pre-Mk.III file and emitted a placeholder.** Either (a) the codegen ran against a stale source, or (b) the codegen cannot lower the Mk.III constructs (struct fields, complex array indexing, multi-arg signatures with `array` type). Either way: **C-output path cannot today produce a working `.c` for the live `.hexa` source**.

This means even if hexa native runtime were deployed to ubu1, **`hexa anima-voice/audio_token_predictor.hexa` would not produce a trainable model** without major codegen work.

---

## 5. The `feedback_py_to_hexa_only` ↔ Reality Conflict

**Policy text** (memory file): "STRICT raw#9 — .py BANNED on Mac including `_python_bridge/`. All Python SDK calls must convert to hexa http/proc primitives. .py allowed ONLY on ubu1/RunPod runtime."

**Reality on Mac** (live disk inventory):

```
state/.*helper.py                   ~25 files (auto-generated by hexa scripts; raw#37 sister rule)
tool/active_redteam_*.py             3 files (own 1 grandfather opt-out)
tool/anima_holographic_ib_ksg_*.py   1 file  (own 1 explicit raw 9 relaxation 2026-04-28)
ready/*.py                        1431 files (own 1 opt-out)
.hxc_bench_*.py                      1 file  (bench harness)
```

**Anima `.own 1`** (canonical, chflags-locked per `.own`): explicitly grants `raw 9` opt-outs for `ready/`, redteam, F3 KSG validator, helper-transients-via-raw-37.

**Conclusion**: the `feedback_py_to_hexa_only` policy as a *strict* reading **already conflicts** with `.own 1` and with the live hexa pattern of emitting `state/.X_helper.py` and invoking via `project_python()`. The strict reading is an aspirational tightening; the de-facto policy is "no new Mac-side .py except (a) raw#37 transient helpers regenerated each invocation, (b) .own 1 grandfather list, (c) ready/ archive."

**Implication for VLM unblock**: the existing **raw#37 transient pattern** is the precedent for letting `.py` exist on Mac as long as it's: (i) auto-generated by a `.hexa` orchestrator, (ii) regenerated per invocation (no human edits), (iii) namespaced in `state/.X_helper.py`. This is **already the bridge** between hexa-design-time and python-runtime.

---

## 6. Ranked Roadmap Tracks (완성도 lens)

### Track A — hexa→py transpiler ★ RECOMMENDED for VLM
- **Scope**: write `self/codegen_py.hexa` (or an external hexa script) that takes a `.hexa` AST and emits PyTorch `.py`. Audio-token-predictor-shaped subset first; expand from there.
- **Effort**: VLM-shaped subset 8-24h dev (matches `vlm_cond3_blocker_landed` §10 estimate of 4-16h for hand-port). Generic transpiler 2-6 weeks.
- **Leverage**: hexa-lang already has codegen pattern (codegen_c2.hexa, codegen_native.hexa). Adding a python target follows the same AST→string template approach. No runtime.c change required.
- **Output topology**: `.hexa` (canonical, Mac-side) → `.py` (auto-generated, deployed to ubu1/RunPod, gitignored on Mac). Raw#37 namespace pattern: `state/.atp_pytorch.py` regenerated by `tool/atp_to_pytorch.hexa`.
- **Wins**: respects `feedback_py_to_hexa_only` spirit (Mac humans never touch .py); reuses HF ecosystem (transformers/peft/safetensors/datasets); fastest VLM unblock.
- **Caveats**: transpiler quality limits what's expressible (autograd-backed PyTorch ops vs hand-written hexa). Need to decide: emit `class Module(nn.Module)` skeleton + lift hexa fwd to PyTorch ops? Or emit raw torch.nn calls?
- **Recommendation**: build VLM-specific transpiler first (audio_token_predictor only), prove the contract, then generalize.

### Track D — hexa+Python FFI via embedded interp
- **Scope**: link CPython into hexa runtime; expose `py_call("torch.nn.Linear", args)` from hexa.
- **Effort**: 2-4 weeks (CPython embedding API, GIL handling, hexa↔py value marshalling).
- **Leverage**: hexa already has `cuda_ffi.hexa` pattern for FFI; extending to a python-FFI module follows precedent.
- **Wins**: zero `.py` files anywhere — hexa code calls torch directly via FFI; satisfies strictest reading of `feedback_py_to_hexa_only`.
- **Caveats**: large dependency added to hexa runtime; deployment to RunPod needs Python+torch in the hexa runtime image; Mac runtime needs CPython bundled. Brittle (GIL, refcounts, interpreter init order).
- **Recommendation**: medium-term, after Track A proves the pattern is needed broadly.

### Track E — dual-source maintenance with audit trail
- **Scope**: formalize the *current* de-facto state: `.hexa` source-of-truth on Mac, hand-ported `.py` mirror on ubu1, a `tool/hexa_py_drift_audit.hexa` that parses both sides and reports semantic divergence.
- **Effort**: 1-3 days for the auditor; ongoing manual port labor per ML file.
- **Leverage**: zero new compiler work; uses RFC-008 `project_python()` already done.
- **Wins**: lowest engineering investment; ships immediately; lets VLM proceed today.
- **Caveats**: drift inevitable (human ports → divergence over time); doesn't scale beyond a handful of ML files; violates DRY for every ML file we add.
- **Recommendation**: short-term **bandaid for VLM today**, abandon once Track A lands.

### Track B — hexa stdlib expansion (tensor ops + PyTorch FFI surface)
- **Scope**: native hexa tensor type (contiguous buffer + dtype + shape + device), tensor stdlib (matmul/conv/attention/softmax with backward), bridge to existing CUDA kernels.
- **Effort**: 4-12 weeks (autograd alone is months of work to do well).
- **Leverage**: extends `self/ml/gpu_tensor.hexa` etc.
- **Wins**: hexa becomes a real ML language standalone.
- **Caveats**: enormous. Reimplementing PyTorch's depth (50+ engineers × years) in hexa is unrealistic at solo-dev pace. Only meaningful if combined with Track A (so other people's models reach hexa via py→hexa transpile) AND Track C (perf parity).
- **Recommendation**: long-term ambition; not VLM-relevant.

### Track C — hexa runtime overhaul (JIT/AOT for ML)
- **Scope**: replace interpreter with JIT/AOT for ML hot paths; emit native code with vectorization, fused kernels, tensor lifetimes.
- **Effort**: 6+ months minimum (LLVM or custom backend).
- **Leverage**: existing `self/codegen_native.hexa` + `self/native/codegen_c2_v2.c` partial baseline.
- **Wins**: required for hexa to compete on raw perf vs PyTorch+torch.compile.
- **Caveats**: massive engineering surface; doesn't unblock VLM in any reasonable horizon.
- **Recommendation**: defer indefinitely.

---

## 7. VLM-Specific Unblock Path

### 7.1 What VLM needs (per `vlm_cond3_blocker_landed_2026_05_03.ai.md` §4 + abort marker)

```
1. audio_token_predictor.hexa → executable on RunPod H100 / Colab T4
2. LibriSpeech-clean-100 corpus prep
3. SP 32k tokenizer (CLM v4 reuse)
4. LoRA r=8 on atp decoder block attn (q/k/v/o) + intent_proj
5. text_head (NEW): Linear(384, 32000) parallel to rvq_heads
6. loss = 0.5 audio_CE + 0.5 text_CE
7. 10k steps, eval every 1k, sentinel on text_CE
```

### 7.2 Per-track time-to-VLM-unblock

| Track | Time to first training step | Risk |
|---|---|---|
| **A** (transpiler, VLM-subset) | **8-24h dev + 1-2h verify** | medium — transpiler subset needs autograd-backed PyTorch fwd only (no hexa kernel reimpl); LoRA via `peft.LoraConfig` |
| **A2** hand-port (degenerate Track A — write the .py once by hand) | **4-16h** (per blocker doc §6 estimate) | low — proven pattern, but brittle to source drift |
| **D** (embedded CPython) | **2-4 weeks** | high — runtime change blocks everything else |
| **E** (formalize dual-source) | **same as A2 plus auditor** | low | ongoing drift cost |
| **B+C** (full native hexa training) | **months** | high — out of scope for VLM |

### 7.3 RECOMMENDED: Track A2 → A escalation

**Phase 1 (now, 4-16h)**: hand-port `audio_token_predictor.hexa` → `audio_token_predictor.py` once. Place at `state/.atp_pytorch.py` (raw#37 transient namespace) OR (cleaner) at `tool/transient_py/atp_pytorch.py` with a generator marker. Deploy to ubu1 alongside corpus. Train.

**Phase 2 (after VLM stage1 lands, 1-2 weeks)**: write `tool/atp_to_pytorch.hexa` — a Track A transpiler narrowly scoped to audio_token_predictor's AST shape. Generator emits the `.py` from the `.hexa` source on Mac, before each ubu1 deploy. This eliminates drift and proves the pattern.

**Phase 3 (after pattern proven, weeks-months)**: generalize transpiler to handle other ML `.hexa` files. Eventually deprecate hand-port.

### 7.4 Mac-side policy reconciliation

Recommend formalizing in anima `.own`:

```
own N proposed "transient .py for ubu/RunPod ML training"
  base raw 9 hexa-only + raw 37 transient helper precedent
  scope tool/transient_py/*.py — auto-generated from .hexa source by tool/X_to_pytorch.hexa
  enforcement (1) .gitignore tool/transient_py/  (2) regeneration marker in each .py header
                (3) drift auditor tool/hexa_py_drift_audit.hexa runs pre-commit
                (4) human edit of any tool/transient_py/*.py = raw violation
  why ML training requires PyTorch (HF ecosystem); hexa source remains canonical;
      no human .py touched on Mac; bridges raw#9 STRICT spirit (Mac = hexa) with
      ML reality (training = .py)
```

This keeps `feedback_py_to_hexa_only` honest — Mac humans still **never write .py** — while granting auto-generated .py the same status as `state/.X_helper.py` (raw#37 transient).

---

## 8. Bridge Options Matrix (audit summary)

| Option | Where .py lives | Generator | Drift risk | Effort | VLM ETA |
|---|---|---|---|---|---|
| **(a) hexa→py transpiler** | tool/transient_py/ (auto-gen, gitignored) | tool/atp_to_pytorch.hexa | low (regen each commit) | 8-24h subset | 1-2 days |
| **(b) tensor/PyTorch FFI from hexa** | nowhere (.hexa calls libtorch directly) | n/a | n/a | 4-12 weeks | months |
| **(c) embedded CPython in hexa runtime** | nowhere (.hexa calls torch via py_call FFI) | n/a | n/a | 2-4 weeks runtime | weeks |
| **(d) hand-ported .py with audit trail** (Track E) | state/.atp_pytorch.py or tool/transient_py/ | human | high (manual sync) | 4-16h once | hours |
| **(e) status quo** | doesn't exist → VLM stays blocked | n/a | n/a | 0h | infinite |

**Selected**: **(d) → (a) escalation** per §7.3.

---

## 9. Honest C3 Caveats (raw#10)

1. **Audit may miss internal hexa-lang work** — this audit examined `/Users/ghost/core/hexa-lang` snapshot at 2026-05-03. Active branches, unmerged commits, work-in-progress on `hxqwen14b_cuda v5+` kernels are not visible here. CUDA `RC_ERR_CUDA_TODO` count may already be lower than the 2026-04-19 audit doc reports.

2. **Gap analysis is opinion, not measurement** — no benchmarks were run. "Useless beyond <1k params" for pure-hexa nn.hexa is inferred from list-based scalar fp64 element-wise ops (149 LoC, no SIMD/BLAS); no measurement was performed. CUDA path liveness is read from comments + symbol presence, not from end-to-end training run.

3. **PyTorch parity column is a sketch** — actual parity requires running each named capability and measuring throughput/correctness. None of that was done. Treat the matrix as a structural inventory, not a competitive benchmark.

4. **Track effort estimates are point estimates** — "8-24h dev" for VLM transpiler subset has ±2× uncertainty; full Track A (general transpiler) "2-6 weeks" has ±3× uncertainty. Real estimates need design-doc + spike.

5. **`feedback_py_to_hexa_only` reading may be wrong** — the policy memory was authored 2026-05-03 (today) without elaboration. If user intent is truly STRICT no-py-anywhere-on-Mac including raw#37 transient and `.own 1` grandfathers, then current Mac state is already in violation and the entire ~25 helper.py corpus needs deletion as well. This audit assumes the policy targets **new humanly-authored .py creation** (consistent with the original "py -> hexa only" trigger that landed `_python_bridge/hf_upload_runner.py` at 500 LoC).

---

## 10. Recommended Next Cycles (priority order)

1. **VLM unblock immediate** — hand-port `audio_token_predictor.hexa` → `tool/transient_py/atp_pytorch.py` (4-16h, $0 if done locally). Deploy to ubu1, run LibriSpeech-clean-100 stage1 LoRA training.
2. **Policy reconciliation cycle** — propose `own N` (per §7.4) to formalize tool/transient_py/ as auto-gen .py namespace; resolves `feedback_py_to_hexa_only` strict-reading conflict.
3. **Track A spike** — write minimal `tool/atp_to_pytorch.hexa` (audio_token_predictor.hexa AST → PyTorch .py); proves transpiler pattern, kills drift risk.
4. **hexa-lang C codegen audit** — investigate why `build/artifacts/audio_token_predictor_nb.c` is Mk.I stub vs Mk.III source (1576 LoC). File a roadmap entry on hexa-lang side. Likely orthogonal to VLM (Track A/D bypass C codegen entirely).
5. **CUDA v5 kernel land tracking** — open issue in hexa-lang to track hxqwen14b LoRA fwd/bwd kernels (currently `RC_ERR_CUDA_TODO=-5`); when these land, Track E (dual-source) becomes optional rather than required.

---

## 11. Artifacts & References

```
docs/hexa_lang_upstream_audit_2026_05_03.md          (this doc)
docs/hexa_lang_upstream_audit_landed_2026_05_03.ai.md (handoff TL;DR)
state/markers/hexa_lang_upstream_audit_landed.marker  (machine-readable verdict)

source repos audited:
  /Users/ghost/core/hexa-lang/                       primary (~50k+ files in .hexa-cache, hundreds source)
  /Users/ghost/core/hexa-lang/stdlib/                ML-relevant stdlib
  /Users/ghost/core/hexa-lang/self/ml/               510 .hexa files
  /Users/ghost/core/hexa-lang/self/native/           CUDA/cuBLAS/NCCL FFI shims
  /Users/ghost/core/hexa-lang/self/serve/            HTTP serving (alm, generic)
  /Users/ghost/core/hexa-lang/self/codegen*.hexa     C/native/wgsl/verilog/esp32 backends
  /Users/ghost/core/hexa-lang/proposals/rfc_008_*.md project_python() primitive (P1 done)
  /Users/ghost/core/hexa-lang/doc/plans/python_serving_purge_audit_20260419.md

upstream blockers:
  /Users/ghost/core/anima/state/markers/vlm_stage1_aborted.marker
  /Users/ghost/core/anima/docs/vlm_cond3_blocker_landed_2026_05_03.ai.md
  /Users/ghost/core/anima/anima-voice/audio_token_predictor.hexa  (Mk.III, 1576 LoC source)
  /Users/ghost/core/hexa-lang/build/artifacts/audio_token_predictor_nb.c  (Mk.I stub, 57 LoC)

policy refs:
  /Users/ghost/.hive/claude-config/.../memory/feedback_py_to_hexa_only.md
  /Users/ghost/core/anima/.own (raw 9 + own 1 grandfather list)
  /Users/ghost/core/hexa-lang/.roadmap (RFC-001, RFC-008 done)

cost
  $0 (read-only audit; no in-place changes; no destructive ops)
  wallclock ~45 min
  destructive 0
  in-place changes 0 (audit + handoff docs only, in /Users/ghost/core/anima/docs/)
```
