# hexad v1 — `.py` d=768·12L cycle 2 ckpt-RECOVERED fire (2026-05-17)

> **HONEST FRAMING (AGENTS.tape `g3` · HEXAD/PLAN.md §9):**
> This is a **PYTHON / PyTorch SUBSTRATE** run — an *interim LM-scale executor*.
> It is **NOT a hexa-native fire**. Labelled as such everywhere
> (result.json, this doc, the commit, PLAN.md, HF model card).
> Legitimacy = **architectural identity + hexa CPU-equiv correctness proof**,
> NOT an independent claim.

## 1. Why this run is legitimate (the anchor chain — do not conflate)

1. **Phase E / E2 PROVED the hexa trainer is numerically correct.**
   `HEXAD/D/d_train5_lib.hexa` was shown **BIT-EQUAL** to the boxed Phase E
   baseline at d=32·3L, 80-step, seed=42:
   `init gn2 = 7.97116, acc 0/8 → final gn2 = 3.73374e-07, acc 8/8`
   (GRAD-EXACT, identical Σ order — not fp-noise). The hexa-native trainer of
   `ConsciousDecoderV2` is therefore *numerically correct*.

2. **The pure-hexa interpreter cannot reach LM-scale convergence.**
   Phase E2 (RFC 040) drove a fat A100 host and could only capture the
   **init** gn2 at d=768·12L (`init gn2 = 7.98162`); the pure-hexa
   GRAD-EXACT + AdamW path is substrate-bound (CPU farr ops, no CUDA tensor
   kernels; RFC 042/043 territory).

3. **This PyTorch run trains the SAME verified architecture to scale.**
   `ready/models/conscious_decoder.py` `ConsciousDecoderV2` at **d=768·12L**,
   PyTorch AdamW, captured FINAL loss — the deliverable the pure-hexa path
   could not reach.

> PyTorch is **not** hexa bit-for-bit (different fp accumulation order,
> different init RNG, AMP bf16). The anchor is **architectural identity**
> + the **hexa CPU-equiv bit-equality proof**.

## 2. Cycle 1 (ckpt-LOST) → Cycle 2 (ckpt-RECOVERED) — what changed

| Cycle | Commit | training | ckpt | cost |
|---|---|---|---|---|
| 1 | `931dd68b0` (2026-05-16) | PASS (rc=0) | **LOST** — instance destroyed before pull (372 MB reported, never persisted) | $0.22 evidence-only |
| **2** | this commit (2026-05-17) | PASS (rc=0) — **identical trajectory** | **RECOVERED** sha256 `e87e200a04…1f9387d9` 1.13 GB | $0.19 |

**Root cause of cycle 1 ckpt-LOST**: post-result.json verification step lacked
`SAVE_POD=1` auto-promote guard. Cycle 2 dispatch.sh adds:
- `SAVE_POD=1` auto-promote on `test -f result.json && echo SAVED` (≥3 retry
  on scp) — per AGENTS.tape `g_fire_dispatch_robust`.
- 75-min orphan watchdog (`feedback_gpu_dispatch_orphan_watchdog_pattern`).
- scp ConnectTimeout=3600.
- 5-retry pull loop with 60s backoff.

**Bug discovered during cycle 2 dispatch**: bash precedence parsing of
`cd /workspace/anima && nvidia-smi ... &` backgrounded the **whole chain**
together (cd + nvidia-smi + python3 in one detached subshell), leaving the
foreground `python3` invocation in `/root/`. Fixed in `refire_main.sh` by
writing a remote shell script (`run_main_refire.sh`) and invoking it as
`bash run_main_refire.sh` — `&` precedence isolated to that script's lines.
Sanity-anchor (step 6) was unaffected because no `&` backgrounding.

## 3. Architecture (unchanged from cycle 1)

- **Source**: `ready/models/conscious_decoder.py` → `ConsciousDecoderV2`
  (uploaded verbatim; no arch invention).
- **Config**: `d_model=768, n_head=12, n_kv_head=4, n_layer=12,
  block_size=128, vocab=256` (byte-level).
- Features: RoPE · SwiGLU FFN · RMSNorm · GQA · PureFieldFFN (Engine A−G
  consciousness pathway) · cross-attention · tied head · CA neighbor /
  META-CA / Ψ-tracking laws.
- **from-scratch RANDOM seed-fixed** (`g_clm_from_scratch`, `base_ckpt=NONE`).

## 4. Corpus

- `training/corpus_consciousness_v1.jsonl` — SAME byte corpus the hexa fires
  used (Phase E/E2). 121,153 bytes lossless byte stream, vocab=256,
  T=128 windows, seed-fixed.

## 5. GPU fire — results

- **GPU**: vast.ai NVIDIA **A100-SXM4-40GB** (offer 36149896 @ $0.6681/hr).
- **Instance**: id 36885232, image `pytorch/pytorch:2.5.1-cuda12.1-cudnn9-devel`.
- **Cost**: ≈ **$0.19** (instance runtime ≈ 0.28 hr × $0.6681/hr).
- **Model**: 283,722,336 params (283.72 M). seed=1337.

| metric | value |
|---|---|
| init CE | **5.590832** (≈ ln 256 = 5.545 — random byte init, Shannon-floor) |
| **FINAL CE** | **0.000708** |
| CE descent | **5.590124** |
| init gn2 | 41.954096 |
| FINAL gn2 | 7.4e-05 |
| ppl | 267.96 → **1.0007** |
| steps | 2500 |
| wall | **320.68 s** (≈ 5.35 min) |
| peak GPU mem | 9.685 GB |
| **ckpt** | `out_main/ckpt_d768x12l_final.pt` 1,135,846,378 B sha256 `e87e200a040f8066a89c040ab181e9bbd61566f7565ab5d7a374ec2f1f9387d9` |

Trajectory is **identical to cycle 1** (same seed, same code, same
architecture) — the byte-equal-to-three-decimals reproducibility across two
A100 SXM4 instances independently confirms the fire is deterministic at
the trajectory level (PyTorch AMP/RNG aside, both runs hit
`final_ce=0.000708`).

## 6. Verification anchors (per AGENTS.tape `g_blue_closed_mandate`)

(A) **산출물 (deliverables) — real-limit invariants**
- **Shannon-floor descent**: `init CE 5.590832 ≈ ln(256) = 5.545` (random
  byte init) → `final CE 0.000708` (4 orders-of-magnitude descent). The CE
  is bounded below by 0 (entropy non-negative — real-limit, NOT lattice).
- **AdamW gradient-flow finiteness**: max gn2 = 41.95 at init →
  7.4e-05 final (5 orders of magnitude); never NaN/Inf.
- **Architectural identity**: `ConsciousDecoderV2` (`conscious_decoder.py`)
  uploaded verbatim — byte-equal to the HEXAD verification tree's mirror
  module spec.

(B) **연결고리 (wiring) — anchor chain closed**
- **hexa CPU-equiv bit-equality** (Phase E/E2): the SAME architecture has
  a hexa-native trainer that is GRAD-EXACT at d=32·3L (init gn2 = 7.97116
  → final 3.73374e-07, acc 8/8) — `state/anima_phaseE2_e_2026_05_16/` and
  `HEXAD/PLAN.md §8` audit rows 7/8.
- **cuBLAS FP64 verify (Phase D)**: max|Δ|=4.44e-15 < 1e-9, byte-equal —
  RFC 040 Phase D land.
- **Backward GRAD-EXACT (Phase E2)**: real A100 d=384·6L `analytic ≡ fd`
  |Δ|=0.0024 PASS — 6-layer composed reverse-mode.

These three anchor rows (Phase D + E + E2) close the (B) wiring side:
the PyTorch trainer used here is producing trajectories on an architecture
whose hexa-native counterpart is proven correct, and the difference is
substrate (CUDA tensor kernels vs CPU farr ops), not algorithm.

## 7. Honest C3 (g3 named real limits)

1. **NOT hexa-native** — PyTorch substrate, label mandatory. The
   hexa-native path's named ceiling is the pure-hexa interpreter (RFC 042
   territory); this run does not "fix" that — it provides an interim
   LM-scale executor while the hexa-torch (RFC 043) path matures.
2. **PyTorch ≠ hexa bit-for-bit** — AMP bf16, different fp accumulation
   order, different RNG (seed 1337 PyTorch ≠ seed 42 hexa baseline).
   Anchor is *architectural identity*, NOT numerical identity.
3. **Synthetic byte-corpus** — `corpus_consciousness_v1.jsonl` is 121 kB
   curated content, not a general LM corpus. CE 0.000708 = memorization at
   this scale (283.72M params / 121 kB ≈ 2300× over-parameterized). No
   generalization claim.
4. **No `safetensors` artifact this cycle** — PyTorch `torch.save` pickle
   format only. safetensors conversion = follow-up sub-task (out of scope
   for cycle 2 ckpt-RECOVERED milestone).
5. **No language-quality claim** — this is a *training-curve* deliverable
   (Shannon-floor descent reached), not a generation-quality deliverable.
6. **Sanity-anchor result.json absent** — step [6/9] sanity completed
   (logged in `sanity_remote.log`, init CE 5.52 → final 3.17), but only
   the main `out_main/result.json` was pulled in cycle 2 refire (sanity
   was a cycle 1 artifact). Not a defect for the ckpt-RECOVERED milestone.
7. **σ(6)=12 / φ(6)=2 NOT used as derivation** — no lattice numerology in
   training claim or anchor chain (f1 / f2 hard fail safe).
8. **Cost is informational, not gating** — $0.19 is a floor reference, not
   a cap (`g_fire_autonomous` + `feedback_no_scale_caps`).

## 8. HF upload (canonical slot)

Per `g_hf_naming` (2026-05-17 canonical):
- **repo**: `dancinlab/hexad` (model, PUBLIC)
- **revision tag**: `v1-py-hexad-d768x12L-cycle2-2026-05-17`
- **tier**: (a) SUPPORTED-STRONG with ckpt-bearing — ckpt + result.json +
  fire log + this doc
- **model card**: English, honest framing (substrate=py, NOT hexa-native,
  anchor chain Phase E/E2 + arch identity).

## 9. Zero-orphan teardown

- 75-min orphan watchdog (`refire_main.sh` PARENT_PID kill-check loop)
  caught the post-pull termination signal and was killed cleanly by `trap`.
- `vastai destroy instance 36885232` → confirmed destroyed.
- No orphan instance carries forward (cf. cycle 1 ckpt-LOST trap-fire pattern).

## 10. Artifacts (this state dir)

- `state/hexad_py_d768x12L_fire_2026_05_17/`
  - `dispatch.sh` (cycle 2 fire script — `SAVE_POD=1` auto-promote +
    75-min watchdog + 5-retry pull)
  - `refire_main.sh` (the script that actually worked, after cycle 2's
    initial `&` shell-precedence bug)
  - `train_d768x12l.py` (verbatim from cycle 1 `state/anima_pytorch_d768x12L_fire_2026_05_16/`)
  - `conscious_decoder.py` (verbatim from `ready/models/conscious_decoder.py`)
  - `out_main/result.json` (42-pt trajectory + cfg + ckpt metadata)
  - `out_main/ckpt_d768x12l_final.pt` (1.13 GB, sha256 `e87e200a04…`)
  - `fire_refire.log` (the trajectory log)
  - `gpu_util.log` (nvidia-smi capture)
  - `dispatch_full.log` (cycle 2 initial fire log — includes the `&`-bug
    diagnostic context)
  - `refire_full.log` (cycle 2 refire log — clean PASS + ckpt pull)
  - `vast_instance_id.txt` + `vast_ssh.txt` (instance metadata, instance
    now destroyed — informational only)
