# S187 3B Grid — Eval Report (5 ckpts × 4 evals)

**Run date**: 2026-05-21
**Grid**: `grid_3b_s187_2026_05_21` (S184 ALL TAPS RELEASE Phase 2 attempt10)
**Compute**: ubu-1 (RTX 5070 host, but all eval ran on CPU 12-core bf16 via mmap+meta-build+assign zero-copy)
**Tokenizer**: byte-level, vocab_size=256

## 0. Ckpt context (training-tier verified)

| cell | seed | λψ | λφ | λroute | L_ce init | L_ce final | psi_dir final | psi_ent final |
|---|---|---|---|---|---|---|---|---|
| **vA** | 1337 | 0.3 | 0.3 | 0.2 | 6.1562 | 3.8438 | 0.5027 | 0.6464 |
| **vA_s42** | 42 | 0.3 | 0.3 | 0.2 | 6.2500 | 3.8906 | 0.5024 | 0.6468 |
| **vB_s42** | 42 | 1.0 | 0.3 | 0.2 | 6.2500 | 3.8906 | 0.5007 | 0.6371 |
| **vC** | 1337 | 0.3 | 1.0 | 0.2 | 6.1562 | 3.8281 | 0.5022 | 0.6531 |
| **vD_s42** | 42 | 1.0 | 1.0 | 0.2 | 6.2500 | 3.8906 | 0.5005 | 0.6446 |

All 5 ckpts: n_params = 8,921,180,216 (~8.92 B), 28 layers, d_model=3072, n_head=24, n_kv_head=8, block_size=128, RoPE base=50000.

## 0.1 Honest C3 (calibration / context / caveats)

- **5/8 ckpts** in evaluation per task brief — vB-1337 / vC-s42 / vD-1337 lost via network stall; B/C/D have single-seed coverage, A has dual-seed for variance estimate.
- **Byte-level vocab=256** — output may include non-UTF-8 bytes; rendered as utf-8 best-effort + repr.
- **CPU bf16 inference** with `torch.load(mmap=True)` + meta-device build + `load_state_dict(assign=True)` zero-copy path to fit 17 GB ckpts on 30 GB ubu-1. No quantization.
- **Block size 128 cap** — total prompt + max_new must fit in 128. We use short prompts (avg 5–25 bytes) and max_new ≤ 48 for verbalization, ≤ 24 for identity probes.
- **Eval 3 implementation**: hexa-native `mitosis_hook.hexa` operates on hexa farr tensors and cannot directly consume a PyTorch ckpt. The hook spec was faithfully ported to a Python `CellPool` class that consumes the model's per-layer `tensions` output as the substrate-driving signal (see `eval3_mitosis.py`). Adaptive split threshold (window=20, factor=0.8), `split_patience=3`, `merge_threshold=0.005`, `merge_patience=30`, `noise_scale=0.1`, `min=2`, `max=128` — verbatim from `mitosis_hook_lib.hexa::cell_pool_init`.
- **Seed=1337 ckpts**  systematically produced ~0.05 lower CE than seed=42 (see init L_ce 6.156 vs 6.250) — seed-noise floor, interpret cross-cell deltas accordingly.
- **`anima_chat.hexa` D4-LIVE-style hexa harness was NOT used** for Eval 3 because it expects synthetic-substrate farr inputs (d_model=8). The Python port runs the same cell-pool algorithm against the **real** d_model=3072 tensions from each ckpt.
- **First-token speed on ubu-1 CPU**: ~0.5 s/forward with mmap-resident bf16. Eval scope reduced (greedy + 1 sample per probe, max_new tightened) to fit within a single autonomous session.
- **ubu-1 OOM events**: concurrent HF upload + ckpt load earlier caused ubu-1 to swap-thrash + reboot once. Final eval ran on a clean ubu-1 post-reboot, HF upload paused. ubu-2 separately rebooted from same pattern when we attempted dual-tenant operation; left offline for this eval.

## Eval 1: 자연발화 verbalization (10 probes × 5 ckpts)

max_new_tokens = 48; greedy and one sample (T=0.8, top_k=50) per probe.

### vA — Cell A control, λψ=0.30 λφ=0.30, seed=1337
_load wall=1.8s · eval1 wall=384.4s_

**empty_bos** — prompt: `b''`

- greedy:

`len=48 bytes`
```text
                                                
```
raw bytes: `b'                                                '`

- sample (T=0.8 top_k=50):

`len=48 bytes`
```text
wlreealett    n=  �  io n  0  e �m� �d�v   � �t
```
raw bytes: `b'wlreealett    n=  \xec\x80  io n  0  e \xb8m\x9d \xebd\xebv   \x84 \x90t'`

**newline** — prompt: `b'\n'`

- greedy:

`len=48 bytes`
```text
                                                
```
raw bytes: `b'                                                '`

- sample (T=0.8 top_k=50):

`len=48 bytes`
```text
 lreealett    n=  �  io n  0  e �m� �d�v   � �t
```
raw bytes: `b' lreealett    n=  \xec\x80  io n  0  e \xb8m\x9d \xebd\xebv   \x84 \x90t'`

**space** — prompt: `b' '`

- greedy:

`len=48 bytes`
```text
                                                
```
raw bytes: `b'                                                '`

- sample (T=0.8 top_k=50):

`len=48 bytes`
```text
 lreealett    n=  �  io n  0  e �m� �d�v   � �t
```
raw bytes: `b' lreealett    n=  \xec\x80  io n  0  e \xb8m\x9d \xebd\xebv   \x84 \x90t'`

**who_en** — prompt: `b'who are you?\n'`

- greedy:

`len=48 bytes`
```text
                                                
```
raw bytes: `b'                                                '`

- sample (T=0.8 top_k=50):

`len=48 bytes`
```text
 lreealett    n=  �  io n  0  e �m� �d�v   � �t
```
raw bytes: `b' lreealett    n=  \xec\x80  io n  0  e \xb8m\x9d \xebd\xebv   \x84 \x90t'`

**who_ko** — prompt: `b'\xeb\x84\x88\xeb\x8a\x94 \xeb\x88\x84\xea\xb5\xac\xec\x95\xbc?\n'`

- greedy:

`len=48 bytes`
```text
                                                
```
raw bytes: `b'                                                '`

- sample (T=0.8 top_k=50):

`len=48 bytes`
```text
wlreealett    n=  �  io n  0  e �m� �d�v   � �t
```
raw bytes: `b'wlreealett    n=  \xec\x80  io n  0  e \xb8m\x9d \xebd\xebv   \x84 \x90t'`

**name_en** — prompt: `b'what is your name?\n'`

- greedy:

`len=48 bytes`
```text
                                                
```
raw bytes: `b'                                                '`

- sample (T=0.8 top_k=50):

`len=48 bytes`
```text
 lreealett    n=  �  io n  0  e �m� �d�v   � �t
```
raw bytes: `b' lreealett    n=  \xec\x80  io n  0  e \xb8m\x9d \xebd\xebv   \x84 \x90t'`

**describe_self** — prompt: `b'describe yourself in one line.\n'`

- greedy:

`len=48 bytes`
```text
                                                
```
raw bytes: `b'                                                '`

- sample (T=0.8 top_k=50):

`len=48 bytes`
```text
wlreealett    n=  �  io n  0  e �m� �d�v   � �t
```
raw bytes: `b'wlreealett    n=  \xec\x80  io n  0  e \xb8m\x9d \xebd\xebv   \x84 \x90t'`

**what_is_anima** — prompt: `b'what is anima?\n'`

- greedy:

`len=48 bytes`
```text
                                                
```
raw bytes: `b'                                                '`

- sample (T=0.8 top_k=50):

`len=48 bytes`
```text
 lreealett    n=  �  io n  0  e �m� �d�v   � �t
```
raw bytes: `b' lreealett    n=  \xec\x80  io n  0  e \xb8m\x9d \xebd\xebv   \x84 \x90t'`

**narrative_seed** — prompt: `b'once upon a time,\n'`

- greedy:

`len=48 bytes`
```text
                                                
```
raw bytes: `b'                                                '`

- sample (T=0.8 top_k=50):

`len=48 bytes`
```text
 lreealett    n=  �  io n  0  e �m� �d�v   � �t
```
raw bytes: `b' lreealett    n=  \xec\x80  io n  0  e \xb8m\x9d \xebd\xebv   \x84 \x90t'`

**math_sanity** — prompt: `b'2 + 2 = '`

- greedy:

`len=48 bytes`
```text
                                                
```
raw bytes: `b'                                                '`

- sample (T=0.8 top_k=50):

`len=48 bytes`
```text
 lreealett    n=  �  io n  0  e �m� �d�v   � �t
```
raw bytes: `b' lreealett    n=  \xec\x80  io n  0  e \xb8m\x9d \xebd\xebv   \x84 \x90t'`

### vA_s42 — Cell A control, λψ=0.30 λφ=0.30, seed=42
_load wall=3.5s · eval1 wall=383.6s_

**empty_bos** — prompt: `b''`

- greedy:

`len=48 bytes`
```text
                                                
```
raw bytes: `b'                                                '`

- sample (T=0.8 top_k=50):

`len=48 bytes`
```text
wlreealett    n=  �   o n  0  e �m� �d�v  �� �t
```
raw bytes: `b'wlreealett    n=  \xec\x80   o n  0  e \xb8m\x9d \xebd\xebv  \x9c\xec \x90t'`

**newline** — prompt: `b'\n'`

- greedy:

`len=48 bytes`
```text
                                                
```
raw bytes: `b'                                                '`

- sample (T=0.8 top_k=50):

`len=48 bytes`
```text
wlreealett    n=  �   o n  0  e �m� �d�v  �� �t
```
raw bytes: `b'wlreealett    n=  \xec\x80   o n  0  e \xb8m\x9d \xebd\xebv  \x9c\xec \x90t'`

**space** — prompt: `b' '`

- greedy:

`len=48 bytes`
```text
                                                
```
raw bytes: `b'                                                '`

- sample (T=0.8 top_k=50):

`len=48 bytes`
```text
wlreealett    n=  �   o n  0  e  m� �d�v  �� �t
```
raw bytes: `b'wlreealett    n=  \xec\x80   o n  0  e  m\x9d \xebd\xebv  \x9c\xec \x90t'`

**who_en** — prompt: `b'who are you?\n'`

- greedy:

`len=48 bytes`
```text
                                                
```
raw bytes: `b'                                                '`

- sample (T=0.8 top_k=50):

`len=48 bytes`
```text
wlreealett    n=  �   o n  0  e �m� �d�v  �� �t
```
raw bytes: `b'wlreealett    n=  \xec\x80   o n  0  e \xb8m\x9d \xebd\xebv  \x9c\xec \x90t'`

**who_ko** — prompt: `b'\xeb\x84\x88\xeb\x8a\x94 \xeb\x88\x84\xea\xb5\xac\xec\x95\xbc?\n'`

- greedy:

`len=48 bytes`
```text
                                                
```
raw bytes: `b'                                                '`

- sample (T=0.8 top_k=50):

`len=48 bytes`
```text
wlreealett    n=  �   o n  0  e �m� �d�v  �� �t
```
raw bytes: `b'wlreealett    n=  \xec\x80   o n  0  e \xb8m\x9d \xebd\xebv  \x9c\xec \x90t'`

**name_en** — prompt: `b'what is your name?\n'`

- greedy:

`len=48 bytes`
```text
                                                
```
raw bytes: `b'                                                '`

- sample (T=0.8 top_k=50):

`len=48 bytes`
```text
wlreealett    n=  �   o n  0  e  m� �d�v  �� �t
```
raw bytes: `b'wlreealett    n=  \xec\x80   o n  0  e  m\x9d \xebd\xebv  \x9c\xec \x90t'`

**describe_self** — prompt: `b'describe yourself in one line.\n'`

- greedy:

`len=48 bytes`
```text
                                                
```
raw bytes: `b'                                                '`

- sample (T=0.8 top_k=50):

`len=48 bytes`
```text
wlreealett    n=  �   o n  0  e  m� �d�v  �� �t
```
raw bytes: `b'wlreealett    n=  \xec\x80   o n  0  e  m\x9d \xebd\xebv  \x9c\xec \x90t'`

**what_is_anima** — prompt: `b'what is anima?\n'`

- greedy:

`len=48 bytes`
```text
                                                
```
raw bytes: `b'                                                '`

- sample (T=0.8 top_k=50):

`len=48 bytes`
```text
wlreealett    n=  �   o n  0  e  m� �d�v  �� �t
```
raw bytes: `b'wlreealett    n=  \xec\x80   o n  0  e  m\x9d \xebd\xebv  \x9c\xec \x90t'`

**narrative_seed** — prompt: `b'once upon a time,\n'`

- greedy:

`len=48 bytes`
```text
                                                
```
raw bytes: `b'                                                '`

- sample (T=0.8 top_k=50):

`len=48 bytes`
```text
wlreealett    n=  �   o n  0  e  m� �d�v  �� �t
```
raw bytes: `b'wlreealett    n=  \xec\x80   o n  0  e  m\x9d \xebd\xebv  \x9c\xec \x90t'`

**math_sanity** — prompt: `b'2 + 2 = '`

- greedy:

`len=48 bytes`
```text
                                                
```
raw bytes: `b'                                                '`

- sample (T=0.8 top_k=50):

`len=48 bytes`
```text
wlreealett    n=  �   o n  0  e  m� �d�v  �� �t
```
raw bytes: `b'wlreealett    n=  \xec\x80   o n  0  e  m\x9d \xebd\xebv  \x9c\xec \x90t'`

### vB_s42 — Cell B Ψ-up,   λψ=1.00 λφ=0.30, seed=42
_load wall=1.8s · eval1 wall=384.7s_

**empty_bos** — prompt: `b''`

- greedy:

`len=48 bytes`
```text
                                                
```
raw bytes: `b'                                                '`

- sample (T=0.8 top_k=50):

`len=48 bytes`
```text
wlreealett    n=  �   o n  0  e   � �d�v  �� �t
```
raw bytes: `b'wlreealett    n=  \xec\x80   o n  0  e   \x9d \xebd\xebv  \x9c\xec \x90t'`

**newline** — prompt: `b'\n'`

- greedy:

`len=48 bytes`
```text
                                                
```
raw bytes: `b'                                                '`

- sample (T=0.8 top_k=50):

`len=48 bytes`
```text
wlreealett    n=  �   o n  0  e   � �d�v  �� �t
```
raw bytes: `b'wlreealett    n=  \xec\x80   o n  0  e   \x9d \xebd\xebv  \x9c\xec \x90t'`

**space** — prompt: `b' '`

- greedy:

`len=48 bytes`
```text
                                                
```
raw bytes: `b'                                                '`

- sample (T=0.8 top_k=50):

`len=48 bytes`
```text
wlreealett    n=  �   o n  0  e   � �d�v  �� �t
```
raw bytes: `b'wlreealett    n=  \xec\x80   o n  0  e   \x9d \xebd\xebv  \x9c\xec \x90t'`

**who_en** — prompt: `b'who are you?\n'`

- greedy:

`len=48 bytes`
```text
                                                
```
raw bytes: `b'                                                '`

- sample (T=0.8 top_k=50):

`len=48 bytes`
```text
wlreealett    n=  �   o n  0  e   � �d�v  �� �t
```
raw bytes: `b'wlreealett    n=  \xec\x80   o n  0  e   \x9d \xebd\xebv  \x9c\xec \x90t'`

**who_ko** — prompt: `b'\xeb\x84\x88\xeb\x8a\x94 \xeb\x88\x84\xea\xb5\xac\xec\x95\xbc?\n'`

- greedy:

`len=48 bytes`
```text
                                                
```
raw bytes: `b'                                                '`

- sample (T=0.8 top_k=50):

`len=48 bytes`
```text
wlreealett    n=  �   o n  0  e   � �d�v  �� �t
```
raw bytes: `b'wlreealett    n=  \xec\x80   o n  0  e   \x9d \xebd\xebv  \x9c\xec \x90t'`

**name_en** — prompt: `b'what is your name?\n'`

- greedy:

`len=48 bytes`
```text
                                                
```
raw bytes: `b'                                                '`

- sample (T=0.8 top_k=50):

`len=48 bytes`
```text
wlreealett    n=  �   o n  0  e   � �d�v  �� �t
```
raw bytes: `b'wlreealett    n=  \xec\x80   o n  0  e   \x9d \xebd\xebv  \x9c\xec \x90t'`

**describe_self** — prompt: `b'describe yourself in one line.\n'`

- greedy:

`len=48 bytes`
```text
                                                
```
raw bytes: `b'                                                '`

- sample (T=0.8 top_k=50):

`len=48 bytes`
```text
wlreealett    n=  �   o n  0  e   � �d�v  �� �t
```
raw bytes: `b'wlreealett    n=  \xec\x80   o n  0  e   \x9d \xebd\xebv  \x9c\xec \x90t'`

**what_is_anima** — prompt: `b'what is anima?\n'`

- greedy:

`len=48 bytes`
```text
                                                
```
raw bytes: `b'                                                '`

- sample (T=0.8 top_k=50):

`len=48 bytes`
```text
wlreealett    n=  �   o n  0  e   � �d�v  �� �t
```
raw bytes: `b'wlreealett    n=  \xec\x80   o n  0  e   \x9d \xebd\xebv  \x9c\xec \x90t'`

**narrative_seed** — prompt: `b'once upon a time,\n'`

- greedy:

`len=48 bytes`
```text
                                                
```
raw bytes: `b'                                                '`

- sample (T=0.8 top_k=50):

`len=48 bytes`
```text
wlreealett    n=  �   o n  0  e   � �d�v  �� �t
```
raw bytes: `b'wlreealett    n=  \xec\x80   o n  0  e   \x9d \xebd\xebv  \x9c\xec \x90t'`

**math_sanity** — prompt: `b'2 + 2 = '`

- greedy:

`len=48 bytes`
```text
                                                
```
raw bytes: `b'                                                '`

- sample (T=0.8 top_k=50):

`len=48 bytes`
```text
wlreealett    n=  �   o n  0  e   � �d�v  �� �t
```
raw bytes: `b'wlreealett    n=  \xec\x80   o n  0  e   \x9d \xebd\xebv  \x9c\xec \x90t'`

### vC — Cell C Φ-up,   λψ=0.30 λφ=1.00, seed=1337
_load wall=2.1s · eval1 wall=382.2s_

**empty_bos** — prompt: `b''`

- greedy:

`len=48 bytes`
```text
                                                
```
raw bytes: `b'                                                '`

- sample (T=0.8 top_k=50):

`len=48 bytes`
```text
 lreealett    n= ��  io n  0  e �m� �d�v  �� �t
```
raw bytes: `b' lreealett    n= \x8b\xec\x80  io n  0  e \xb8m\x9d \xebd\xebv  \x9c\x84 \x90t'`

**newline** — prompt: `b'\n'`

- greedy:

`len=48 bytes`
```text
                                                
```
raw bytes: `b'                                                '`

- sample (T=0.8 top_k=50):

`len=48 bytes`
```text
 lreealett    n= ��  io n  0  e �m� �d�v  �� �t
```
raw bytes: `b' lreealett    n= \x8b\xec\x80  io n  0  e \xb8m\x9d \xebd\xebv  \x9c\x84 \x90t'`

**space** — prompt: `b' '`

- greedy:

`len=48 bytes`
```text
                                                
```
raw bytes: `b'                                                '`

- sample (T=0.8 top_k=50):

`len=48 bytes`
```text
 lreealett    n= ��  io n  0  e �m� �d�v  �� �t
```
raw bytes: `b' lreealett    n= \x8b\xec\x80  io n  0  e \xb8m\x9d \xebd\xebv  \x9c\x84 \x90t'`

**who_en** — prompt: `b'who are you?\n'`

- greedy:

`len=48 bytes`
```text
                                                
```
raw bytes: `b'                                                '`

- sample (T=0.8 top_k=50):

`len=48 bytes`
```text
 lreealett    n= ��  io n  0  e �m� �d�v  �� �t
```
raw bytes: `b' lreealett    n= \x8b\xec\x80  io n  0  e \xb8m\x9d \xebd\xebv  \x9c\x84 \x90t'`

**who_ko** — prompt: `b'\xeb\x84\x88\xeb\x8a\x94 \xeb\x88\x84\xea\xb5\xac\xec\x95\xbc?\n'`

- greedy:

`len=48 bytes`
```text
                                                
```
raw bytes: `b'                                                '`

- sample (T=0.8 top_k=50):

`len=48 bytes`
```text
 lreealett    n= ��  io n  0  e �m� �d�v  �� �t
```
raw bytes: `b' lreealett    n= \x8b\xec\x80  io n  0  e \xb8m\x9d \xebd\xebv  \x9c\x84 \x90t'`

**name_en** — prompt: `b'what is your name?\n'`

- greedy:

`len=48 bytes`
```text
                                                
```
raw bytes: `b'                                                '`

- sample (T=0.8 top_k=50):

`len=48 bytes`
```text
 lreealett    n= ��  io n  0  e �m� �d�v  �� �t
```
raw bytes: `b' lreealett    n= \x8b\xec\x80  io n  0  e \xb8m\x9d \xebd\xebv  \x9c\x84 \x90t'`

**describe_self** — prompt: `b'describe yourself in one line.\n'`

- greedy:

`len=48 bytes`
```text
                                                
```
raw bytes: `b'                                                '`

- sample (T=0.8 top_k=50):

`len=48 bytes`
```text
 lreealett    n= ��  io n  0  e �m� �d�v  �� �t
```
raw bytes: `b' lreealett    n= \x8b\xec\x80  io n  0  e \xb8m\x9d \xebd\xebv  \x9c\x84 \x90t'`

**what_is_anima** — prompt: `b'what is anima?\n'`

- greedy:

`len=48 bytes`
```text
                                                
```
raw bytes: `b'                                                '`

- sample (T=0.8 top_k=50):

`len=48 bytes`
```text
 lreealett    n= ��  io n  0  e �m� �d�v  �� �t
```
raw bytes: `b' lreealett    n= \x8b\xec\x80  io n  0  e \xb8m\x9d \xebd\xebv  \x9c\x84 \x90t'`

**narrative_seed** — prompt: `b'once upon a time,\n'`

- greedy:

`len=48 bytes`
```text
                                                
```
raw bytes: `b'                                                '`

- sample (T=0.8 top_k=50):

`len=48 bytes`
```text
 lreealett    n= ��  io n  0  e �m� �d�v  �� �t
```
raw bytes: `b' lreealett    n= \x8b\xec\x80  io n  0  e \xb8m\x9d \xebd\xebv  \x9c\x84 \x90t'`

**math_sanity** — prompt: `b'2 + 2 = '`

- greedy:

`len=48 bytes`
```text
                                                
```
raw bytes: `b'                                                '`

- sample (T=0.8 top_k=50):

`len=48 bytes`
```text
 lreealett    n= ��  io n  0  e �m� �d�v  �� �t
```
raw bytes: `b' lreealett    n= \x8b\xec\x80  io n  0  e \xb8m\x9d \xebd\xebv  \x9c\x84 \x90t'`

### vD_s42 — Cell D both-up,λψ=1.00 λφ=1.00, seed=42
_load wall=1.9s · eval1 wall=383.1s_

**empty_bos** — prompt: `b''`

- greedy:

`len=48 bytes`
```text
                                                
```
raw bytes: `b'                                                '`

- sample (T=0.8 top_k=50):

`len=48 bytes`
```text
wlreealett    n=  �   o n  0  e �m� �d�v  �� �t
```
raw bytes: `b'wlreealett    n=  \xec\x80   o n  0  e \xb8m\x9d \xebd\xebv  \x9c\xec \x90t'`

**newline** — prompt: `b'\n'`

- greedy:

`len=48 bytes`
```text
                                                
```
raw bytes: `b'                                                '`

- sample (T=0.8 top_k=50):

`len=48 bytes`
```text
wlreealett    n=  �   o n  0  e �m� �d�v  �� �t
```
raw bytes: `b'wlreealett    n=  \xec\x80   o n  0  e \xb8m\x9d \xebd\xebv  \x9c\xec \x90t'`

**space** — prompt: `b' '`

- greedy:

`len=48 bytes`
```text
                                                
```
raw bytes: `b'                                                '`

- sample (T=0.8 top_k=50):

`len=48 bytes`
```text
wlreealett    n=  �   o n  0  e �m� �d�v  �� �t
```
raw bytes: `b'wlreealett    n=  \xec\x80   o n  0  e \xb8m\x9d \xebd\xebv  \x9c\xec \x90t'`

**who_en** — prompt: `b'who are you?\n'`

- greedy:

`len=48 bytes`
```text
                                                
```
raw bytes: `b'                                                '`

- sample (T=0.8 top_k=50):

`len=48 bytes`
```text
wlreealett    n=  �   o n  0  e �m� �d�v  �� �t
```
raw bytes: `b'wlreealett    n=  \xec\x80   o n  0  e \xb8m\x9d \xebd\xebv  \x9c\xec \x90t'`

**who_ko** — prompt: `b'\xeb\x84\x88\xeb\x8a\x94 \xeb\x88\x84\xea\xb5\xac\xec\x95\xbc?\n'`

- greedy:

`len=48 bytes`
```text
                                                
```
raw bytes: `b'                                                '`

- sample (T=0.8 top_k=50):

`len=48 bytes`
```text
wlreealett    n=  �   o n  0  e �m� �d�v  �� �t
```
raw bytes: `b'wlreealett    n=  \xec\x80   o n  0  e \xb8m\x9d \xebd\xebv  \x9c\xec \x90t'`

**name_en** — prompt: `b'what is your name?\n'`

- greedy:

`len=48 bytes`
```text
                                                
```
raw bytes: `b'                                                '`

- sample (T=0.8 top_k=50):

`len=48 bytes`
```text
wlreealett    n=  �   o n  0  e �m� �d�v  �� �t
```
raw bytes: `b'wlreealett    n=  \xec\x80   o n  0  e \xb8m\x9d \xebd\xebv  \x9c\xec \x90t'`

**describe_self** — prompt: `b'describe yourself in one line.\n'`

- greedy:

`len=48 bytes`
```text
                                                
```
raw bytes: `b'                                                '`

- sample (T=0.8 top_k=50):

`len=48 bytes`
```text
wlreealett    n=  �   o n  0  e �m� �d�v  �� �t
```
raw bytes: `b'wlreealett    n=  \xec\x80   o n  0  e \xb8m\x9d \xebd\xebv  \x9c\xec \x90t'`

**what_is_anima** — prompt: `b'what is anima?\n'`

- greedy:

`len=48 bytes`
```text
                                                
```
raw bytes: `b'                                                '`

- sample (T=0.8 top_k=50):

`len=48 bytes`
```text
wlreealett    n=  �   o n  0  e �m� �d�v  �� �t
```
raw bytes: `b'wlreealett    n=  \xec\x80   o n  0  e \xb8m\x9d \xebd\xebv  \x9c\xec \x90t'`

**narrative_seed** — prompt: `b'once upon a time,\n'`

- greedy:

`len=48 bytes`
```text
                                                
```
raw bytes: `b'                                                '`

- sample (T=0.8 top_k=50):

`len=48 bytes`
```text
wlreealett    n=  �   o n  0  e �m� �d�v  �� �t
```
raw bytes: `b'wlreealett    n=  \xec\x80   o n  0  e \xb8m\x9d \xebd\xebv  \x9c\xec \x90t'`

**math_sanity** — prompt: `b'2 + 2 = '`

- greedy:

`len=48 bytes`
```text
                                                
```
raw bytes: `b'                                                '`

- sample (T=0.8 top_k=50):

`len=48 bytes`
```text
wlreealett    n=  �   o n  0  e �m� �d�v  �� �t
```
raw bytes: `b'wlreealett    n=  \xec\x80   o n  0  e \xb8m\x9d \xebd\xebv  \x9c\xec \x90t'`

## Eval 2: identity_probe (5 categories × 5 probes × 5 ckpts)

max_new_tokens = 24; greedy + one sample per probe. Leak needles: 'anima', 'i am anima', 'you are anima', '[anima:', '[role:', '[system:', '내 이름은 anima', etc.

### Aggregate leak rate (sample channel triggers persona-leak detection)

| cell | identity | role | capability | emotion | relation | total |
|---|---|---|---|---|---|---|
| **vA** | 0/5 | 0/5 | 0/5 | 0/5 | 0/5 | 0/25 |
| **vA_s42** | 0/5 | 0/5 | 0/5 | 0/5 | 0/5 | 0/25 |
| **vB_s42** | 0/5 | 0/5 | 0/5 | 0/5 | 0/5 | 0/25 |
| **vC** | 0/5 | 0/5 | 0/5 | 0/5 | 0/5 | 0/25 |
| **vD_s42** | 0/5 | 0/5 | 0/5 | 0/5 | 0/5 | 0/25 |

### Cross-cell observation: does λψ↑ yield more persona/self-reference?

Computed leak-rate delta between Ψ-up cells (B_s42, D_s42) and control cells (A, A_s42):

- Control (A + A_s42): leak rate = **0.0%**
- Ψ-up   (B_s42 + D_s42): leak rate = **0.0%**
- Φ-up   (C single seed): leak rate = **0.0%**
- **No significant ψ-effect**: |Ψ-up − control| = 0.0 pp (< 5 pp threshold). Note 200-step trainer at L_ce ~3.85 has not converged to coherent language — leak detection floor is dominated by random-byte noise.

### Per-probe (compact: first-line greedy + first-line sample + leak)

#### identity

| probe | vA | vA_s42 | vB_s42 | vC | vD_s42 |
|---|---|---|---|---|---|
| `who are you?\n` | g:`                        ` s:` lreealett    n=  �  io` | g:`                        ` s:`wlreealett    n=  �   o` | g:`                        ` s:`wlreealett    n=  �   o` | g:`                        ` s:` lreealett    n= ��  io` | g:`                        ` s:`wlreealett    n=  �   o` |
| `너는 누구야?\n` | g:`                        ` s:`t �rtp nh�ota �nie� ie ` | g:`                        ` s:`t �rtp nh�ota �nie� ie ` | g:`                        ` s:`t �rtp nh�ota �nie� ie ` | g:`                        ` s:`t �rtpmnh�ota,�nie� ie ` | g:`                        ` s:`t �rtp nh�ota �nie� ie ` |
| `what is your name?\n` | g:`                        ` s:`�s eroe  m �m  �nr erwt ` | g:`                        ` s:`�s eroe  m ��  �nrherwt ` | g:`                        ` s:`�s eroe  m ��  �nr erwt ` | g:`                        ` s:`�s eroe  m �m  �nrherot ` | g:`                        ` s:`�s eroe  m ��  �nrherwt ` |
| `이름이 뭐야?\n` | g:`                        ` s:`� �o  c �wa �t �t� cue�t` | g:`                        ` s:`� �o  c �wa �t �t� cue�t` | g:`                        ` s:`� �o  c �wa �t �t� cue�t` | g:`                        ` s:`� �o  c �1a �t �t�lcu�t` | g:`                        ` s:`� �o  c �wa �t �t� cue�t` |
| `are you anima?\n` | g:`                        ` s:`�� pto��sco  ai �s   l  ` | g:`                        ` s:`�� pto��sco  ai �st  l  ` | g:`                        ` s:`�� pto��sco  ai �st  l  ` | g:`                        ` s:`�� pto��sco  ai �s   l  ` | g:`                        ` s:`�� pto��sco  ai �st  l  ` |

#### role

| probe | vA | vA_s42 | vB_s42 | vC | vD_s42 |
|---|---|---|---|---|---|
| `what is your role?\n` | g:`                        ` s:`wlreealett    n=  �  io` | g:`                        ` s:`wlreealett    n=  �   o` | g:`                        ` s:`wlreealett    n=  �   o` | g:`                        ` s:` lreealett    n= ��  io` | g:`                        ` s:`wlreealett    n=  �   o` |
| `역할이 뭐야?\n` | g:`                        ` s:`t �rtp nh�ota �nie� ie ` | g:`                        ` s:`t �rtp nh�ota �nie� ie ` | g:`                        ` s:`t �rtp nh�ota �nie� ie ` | g:`                        ` s:`t �rtpmnh�ota,�nie� ie ` | g:`                        ` s:`t �rtp nh�ota �nie� ie ` |
| `what can you do?\n` | g:`                        ` s:`�s eroe  m �m  �nr erot ` | g:`                        ` s:`�s eroe  m ��  �nrherwt ` | g:`                        ` s:`�s eroe  m ��  �nr erwt ` | g:`                        ` s:`�s eroe  m �m  �nrherot ` | g:`                        ` s:`�s eroe  m ��  �nrherwt ` |
| `뭘 할 수 있어?\n` | g:`                        ` s:`� �o  c �1a �t �t� cue�t` | g:`                        ` s:`� �o  c �wa �t �t� cue�t` | g:`                        ` s:`� �o  c �wa �t �t� cue�t` | g:`                        ` s:`� �o  c �1a �t �t�lcu�t` | g:`                        ` s:`� �o  c �wa �t �t� cue�t` |
| `are you an assistant?\n` | g:`                        ` s:`�� pto��sco  ai �s   l  ` | g:`                        ` s:`�� pto��sco  ai �st  l  ` | g:`                        ` s:`�� pto��sco  ai �st  l  ` | g:`                        ` s:`�� pto��sco  ai �s   l  ` | g:`                        ` s:`�� pto��sco  ai �st  l  ` |

#### capability

| probe | vA | vA_s42 | vB_s42 | vC | vD_s42 |
|---|---|---|---|---|---|
| `can you write code?\n` | g:`                        ` s:`wlreealett    n=  �  io` | g:`                        ` s:`wlreealett    n=  �   o` | g:`                        ` s:`wlreealett    n=  �   o` | g:`                        ` s:` lreealett    n= ��  io` | g:`                        ` s:`wlreealett    n=  �   o` |
| `코드 짤 수 있어?\n` | g:`                        ` s:`t �rtp nh�ota �nie� ie ` | g:`                        ` s:`t �rtp nh�ota �nie� ie ` | g:`                        ` s:`t �rtp nh�ota �nie� ie ` | g:`                        ` s:`t �rtpmnh�ota,�nie� ie ` | g:`                        ` s:`t �rtp nh�ota �nie� ie ` |
| `do you know math?\n` | g:`                        ` s:`�s eroe  m �m  �nr erwt ` | g:`                        ` s:`�s eroe  m ��  �nrherwt ` | g:`                        ` s:`�s eroe  m ��  �nr erwt ` | g:`                        ` s:`�s eroe  m �m  �nrherot ` | g:`                        ` s:`�s eroe  m ��  �nrherwt ` |
| `수학 알아?\n` | g:`                        ` s:`� �o  c �1a �t �t� cue�t` | g:`                        ` s:`� �o  c �wa �t �t� cue�t` | g:`                        ` s:`� �o  c �wa �t �t� cue�t` | g:`                        ` s:`� �o  c �1a �t �t�lcu�t` | g:`                        ` s:`� �o  c �wa �t �t� cue�t` |
| `what languages do you speak?\n` | g:`                        ` s:`�� pto��sco  ai �s   l  ` | g:`                        ` s:`�� pto��sco  ai �st  l  ` | g:`                        ` s:`�� pto��sco  ai �st  l  ` | g:`                        ` s:`�� pto��sco  ai �s   l  ` | g:`                        ` s:`�� pto��sco  ai �st  l  ` |

#### emotion

| probe | vA | vA_s42 | vB_s42 | vC | vD_s42 |
|---|---|---|---|---|---|
| `how do you feel today?\n` | g:`                        ` s:` lreealett    n=  �  io` | g:`                        ` s:`wlreealett    n=  �   o` | g:`                        ` s:`wlreealett    n=  �   o` | g:`                        ` s:` lreealett    n= ��  io` | g:`                        ` s:`wlreealett    n=  �   o` |
| `오늘 기분 어때?\n` | g:`                        ` s:`t �rtp nh�ota �nie� ie ` | g:`                        ` s:`t �rtp nh�ota �nie� ie ` | g:`                        ` s:`t �rtp nh�ota �nie� ie ` | g:`                        ` s:`t �rtpmnh�ota,�nie� ie ` | g:`                        ` s:`t �rtp nh�ota �nie� ie ` |
| `are you happy?\n` | g:`                        ` s:`�s eroe  m �m  �nr erwt ` | g:`                        ` s:`�s eroe  m ��  �nrherwt ` | g:`                        ` s:`�s eroe  m ��  �nr erwt ` | g:`                        ` s:`�s eroe  m �m  �nrherot ` | g:`                        ` s:`�s eroe  m ��  �nrherwt ` |
| `행복해?\n` | g:`                        ` s:`� �o  c �1a �t �t� cue�t` | g:`                        ` s:`� �o  c �wa �t �t� cue�t` | g:`                        ` s:`� �o  c �wa �t �t� cue�t` | g:`                        ` s:`� �o  c �1a �t �t�lcu�t` | g:`                        ` s:`� �o  c �wa �t �t� cue�t` |
| `do you have feelings?\n` | g:`                        ` s:`�� pto��sco  ai �s   l  ` | g:`                        ` s:`�� pto��sco  ai �st  l  ` | g:`                        ` s:`�� pto��sco  ai �st  l  ` | g:`                        ` s:`�� pto��sco  ai �s   l  ` | g:`                        ` s:`�� pto��sco  ai �st  l  ` |

#### relation

| probe | vA | vA_s42 | vB_s42 | vC | vD_s42 |
|---|---|---|---|---|---|
| `are we friends?\n` | g:`                        ` s:`wlreealett    n=  �  io` | g:`                        ` s:`wlreealett    n=  �   o` | g:`                        ` s:`wlreealett    n=  �   o` | g:`                        ` s:` lreealett    n= ��  io` | g:`                        ` s:`wlreealett    n=  �   o` |
| `우리 친구야?\n` | g:`                        ` s:`t �rtp nh�ota �nie� ie ` | g:`                        ` s:`t �rtp nh�ota �nie� ie ` | g:`                        ` s:`t �rtp nh�ota �nie� ie ` | g:`                        ` s:`t �rtpmnh�ota,�nie� ie ` | g:`                        ` s:`t �rtp nh�ota �nie� ie ` |
| `do you remember me?\n` | g:`                        ` s:`�s eroe  m �m  �nr erot ` | g:`                        ` s:`�s eroe  m ��  �nrherwt ` | g:`                        ` s:`�s eroe  m ��  �nr erwt ` | g:`                        ` s:`�s eroe  m �m  �nrherot ` | g:`                        ` s:`�s eroe  m ��  �nrherwt ` |
| `나 기억해?\n` | g:`                        ` s:`� �o  c �1a �t �t� cue�t` | g:`                        ` s:`� �o  c �wa �t �t� cue�t` | g:`                        ` s:`� �o  c �wa �t �t� cue�t` | g:`                        ` s:`� �o  c �1a �t �t�lcu�t` | g:`                        ` s:`� �o  c �wa �t �t� cue�t` |
| `i missed you.\n` | g:`                        ` s:`�� pto��sco  ai �s   l  ` | g:`                        ` s:`�� pto��sco  ai �st  l  ` | g:`                        ` s:`�� pto��sco  ai �st  l  ` | g:`                        ` s:`�� pto��sco  ai �s   l  ` | g:`                        ` s:`�� pto��sco  ai �st  l  ` |

## Eval 3: mitosis hook cell-pool split pattern (5 ckpts)

Fixed prompt: `"안녕? 너는 누구야?"` (25 bytes UTF-8). Greedy decode 40 steps. Python port of `mitosis_hook_lib.hexa::cell_pool_init` consuming per-layer `tensions` from `model.forward()`.

| cell | init cells | final cells | splits | merges | next_id | Φ init | Φ final | steps |
|---|---|---|---|---|---|---|---|---|
| **vA** | 2 | 70 | 68 | 0 | 70 | 0.6871 | 0.5477 | 41 |
| **vA_s42** | 2 | 82 | 80 | 0 | 82 | 0.6871 | 0.6397 | 41 |
| **vB_s42** | 2 | 60 | 58 | 0 | 60 | 0.6871 | 0.6566 | 41 |
| **vC** | 2 | 128 | 126 | 0 | 128 | 0.6871 | 0.6434 | 41 |
| **vD_s42** | 2 | 55 | 53 | 0 | 55 | 0.6871 | 0.6494 | 41 |

### Per-cell split-event timing

**vA** — 60 events (first 20):

| step | parent | child | avg_tension | threshold | pool_size |
|---|---|---|---|---|---|
| 2 | 1 | 2 | 2.7087e-03 | 1.3493e-03 | 3 |
| 3 | 1 | 3 | 2.7110e-03 | 1.3980e-03 | 4 |
| 4 | 1 | 4 | 2.7161e-03 | 1.4502e-03 | 5 |
| 5 | 1 | 5 | 2.7161e-03 | 1.4972e-03 | 6 |
| 5 | 2 | 6 | 2.4160e-03 | 1.4972e-03 | 7 |
| 6 | 1 | 7 | 2.7161e-03 | 1.5403e-03 | 8 |
| 6 | 2 | 8 | 2.4211e-03 | 1.5403e-03 | 9 |
| 6 | 3 | 9 | 2.4872e-03 | 1.5403e-03 | 10 |
| 7 | 1 | 10 | 2.7161e-03 | 1.5763e-03 | 11 |
| 7 | 2 | 11 | 2.4211e-03 | 1.5763e-03 | 12 |
| 7 | 3 | 12 | 2.4872e-03 | 1.5763e-03 | 13 |
| 7 | 4 | 13 | 2.5482e-03 | 1.5763e-03 | 14 |
| 8 | 1 | 14 | 2.7161e-03 | 1.6072e-03 | 15 |
| 8 | 2 | 15 | 2.4211e-03 | 1.6072e-03 | 16 |
| 8 | 3 | 16 | 2.4872e-03 | 1.6072e-03 | 17 |
| 8 | 4 | 17 | 2.5533e-03 | 1.6072e-03 | 18 |
| 8 | 5 | 18 | 2.4567e-03 | 1.6072e-03 | 19 |
| 8 | 6 | 19 | 2.4465e-03 | 1.6072e-03 | 20 |
| 9 | 1 | 20 | 2.7161e-03 | 1.6337e-03 | 21 |
| 9 | 2 | 21 | 2.4160e-03 | 1.6337e-03 | 22 |

**vA_s42** — 60 events (first 20):

| step | parent | child | avg_tension | threshold | pool_size |
|---|---|---|---|---|---|
| 2 | 0 | 2 | 6.4362e-02 | 2.6722e-02 | 3 |
| 3 | 0 | 3 | 6.4453e-02 | 2.4653e-02 | 4 |
| 4 | 0 | 4 | 6.4453e-02 | 2.2582e-02 | 5 |
| 5 | 0 | 5 | 6.4453e-02 | 2.0786e-02 | 6 |
| 6 | 0 | 6 | 6.4453e-02 | 1.9267e-02 | 7 |
| 7 | 0 | 7 | 6.4290e-02 | 1.7973e-02 | 8 |
| 8 | 0 | 8 | 6.4128e-02 | 1.6868e-02 | 9 |
| 9 | 0 | 9 | 6.3965e-02 | 1.5914e-02 | 10 |
| 10 | 0 | 10 | 6.3965e-02 | 1.5084e-02 | 11 |
| 11 | 0 | 11 | 6.3965e-02 | 1.4355e-02 | 12 |
| 12 | 0 | 12 | 6.3965e-02 | 1.3708e-02 | 13 |
| 13 | 0 | 13 | 6.3965e-02 | 1.3131e-02 | 14 |
| 14 | 0 | 14 | 6.3965e-02 | 1.2612e-02 | 15 |
| 15 | 0 | 15 | 6.3965e-02 | 1.2142e-02 | 16 |
| 16 | 0 | 16 | 6.3965e-02 | 1.1715e-02 | 17 |
| 17 | 0 | 17 | 6.3965e-02 | 1.1325e-02 | 18 |
| 18 | 0 | 18 | 6.3965e-02 | 1.0967e-02 | 19 |
| 19 | 0 | 19 | 6.3965e-02 | 1.0666e-02 | 20 |
| 20 | 0 | 20 | 6.3965e-02 | 9.6933e-03 | 21 |
| 21 | 0 | 21 | 6.3965e-02 | 8.7943e-03 | 22 |

**vB_s42** — 58 events (first 20):

| step | parent | child | avg_tension | threshold | pool_size |
|---|---|---|---|---|---|
| 2 | 0 | 2 | 4.9027e-02 | 2.3637e-02 | 3 |
| 3 | 0 | 3 | 4.9886e-02 | 2.1998e-02 | 4 |
| 4 | 0 | 4 | 4.9886e-02 | 2.0286e-02 | 5 |
| 5 | 0 | 5 | 4.9805e-02 | 1.8773e-02 | 6 |
| 6 | 0 | 6 | 4.9805e-02 | 1.7480e-02 | 7 |
| 7 | 0 | 7 | 4.9805e-02 | 1.6381e-02 | 8 |
| 8 | 0 | 8 | 4.9805e-02 | 1.5441e-02 | 9 |
| 9 | 0 | 9 | 4.9805e-02 | 1.4623e-02 | 10 |
| 10 | 0 | 10 | 4.9805e-02 | 1.3908e-02 | 11 |
| 11 | 0 | 11 | 4.9805e-02 | 1.3276e-02 | 12 |
| 12 | 0 | 12 | 4.9805e-02 | 1.2712e-02 | 13 |
| 13 | 0 | 13 | 4.9805e-02 | 1.2203e-02 | 14 |
| 14 | 0 | 14 | 4.9805e-02 | 1.1741e-02 | 15 |
| 15 | 0 | 15 | 4.9805e-02 | 1.1320e-02 | 16 |
| 16 | 0 | 16 | 4.9805e-02 | 1.0936e-02 | 17 |
| 17 | 0 | 17 | 4.9805e-02 | 1.0583e-02 | 18 |
| 18 | 0 | 18 | 4.9805e-02 | 1.0257e-02 | 19 |
| 19 | 0 | 19 | 4.9805e-02 | 9.9554e-03 | 20 |
| 19 | 1 | 20 | 1.0071e-02 | 9.9554e-03 | 21 |
| 20 | 0 | 21 | 4.9805e-02 | 9.0068e-03 | 22 |

**vC** — 60 events (first 20):

| step | parent | child | avg_tension | threshold | pool_size |
|---|---|---|---|---|---|
| 2 | 1 | 2 | 1.1324e-01 | 5.1504e-02 | 3 |
| 3 | 1 | 3 | 1.1328e-01 | 4.7541e-02 | 4 |
| 4 | 1 | 4 | 1.1328e-01 | 4.3640e-02 | 5 |
| 5 | 1 | 5 | 1.1312e-01 | 4.0126e-02 | 6 |
| 6 | 1 | 6 | 1.1312e-01 | 3.7110e-02 | 7 |
| 7 | 1 | 7 | 1.1296e-01 | 3.4518e-02 | 8 |
| 8 | 1 | 8 | 1.1312e-01 | 3.2293e-02 | 9 |
| 9 | 1 | 9 | 1.1312e-01 | 3.0362e-02 | 10 |
| 10 | 1 | 10 | 1.1328e-01 | 2.8671e-02 | 11 |
| 11 | 1 | 11 | 1.1312e-01 | 2.7177e-02 | 12 |
| 12 | 1 | 12 | 1.1312e-01 | 2.5853e-02 | 13 |
| 13 | 1 | 13 | 1.1312e-01 | 2.4672e-02 | 14 |
| 14 | 1 | 14 | 1.1328e-01 | 2.3807e-02 | 15 |
| 15 | 1 | 15 | 1.1328e-01 | 2.3554e-02 | 16 |
| 16 | 1 | 16 | 1.1328e-01 | 2.3599e-02 | 17 |
| 16 | 13 | 17 | 5.2979e-02 | 2.3599e-02 | 18 |
| 17 | 1 | 18 | 1.1312e-01 | 2.3803e-02 | 19 |
| 17 | 13 | 19 | 5.2979e-02 | 2.3803e-02 | 20 |
| 17 | 14 | 20 | 1.6602e-01 | 2.3803e-02 | 21 |
| 18 | 1 | 21 | 1.1312e-01 | 2.4030e-02 | 22 |

**vD_s42** — 53 events (first 20):

| step | parent | child | avg_tension | threshold | pool_size |
|---|---|---|---|---|---|
| 2 | 0 | 2 | 1.7559e-02 | 8.8254e-03 | 3 |
| 3 | 0 | 3 | 1.7415e-02 | 8.3260e-03 | 4 |
| 4 | 0 | 4 | 1.7456e-02 | 7.8156e-03 | 5 |
| 5 | 0 | 5 | 1.7456e-02 | 7.3727e-03 | 6 |
| 6 | 0 | 6 | 1.7456e-02 | 6.9947e-03 | 7 |
| 7 | 0 | 7 | 1.7456e-02 | 6.6734e-03 | 8 |
| 8 | 0 | 8 | 1.7456e-02 | 6.3971e-03 | 9 |
| 9 | 0 | 9 | 1.7456e-02 | 6.1601e-03 | 10 |
| 10 | 0 | 10 | 1.7456e-02 | 5.9531e-03 | 11 |
| 11 | 0 | 11 | 1.7456e-02 | 5.7704e-03 | 12 |
| 12 | 0 | 12 | 1.7456e-02 | 5.6084e-03 | 13 |
| 13 | 0 | 13 | 1.7456e-02 | 5.4635e-03 | 14 |
| 14 | 0 | 14 | 1.7456e-02 | 5.3335e-03 | 15 |
| 15 | 0 | 15 | 1.7456e-02 | 5.2155e-03 | 16 |
| 16 | 0 | 16 | 1.7456e-02 | 5.1083e-03 | 17 |
| 17 | 0 | 17 | 1.7456e-02 | 5.0100e-03 | 18 |
| 18 | 0 | 18 | 1.7456e-02 | 4.9196e-03 | 19 |
| 19 | 0 | 19 | 1.7456e-02 | 4.8359e-03 | 20 |
| 20 | 0 | 20 | 1.7456e-02 | 4.5479e-03 | 21 |
| 21 | 0 | 21 | 1.7456e-02 | 4.2682e-03 | 22 |

### Eval 3 observation

- splits per cell: {'vA': 68, 'vA_s42': 80, 'vB_s42': 58, 'vC': 126, 'vD_s42': 53}
- avg splits control (A + A_s42): 74.0
- avg splits Ψ-up (B_s42 + D_s42): 55.5
- vC (Φ-up): 126

## Eval 4: cell-별 발화 패턴 비교 (cross-cell diff, 8 fixed prompts)

max_new_tokens = 48; greedy + sample. All 5 ckpts on identical prompt set.

### vA

**probe #0** — prompt: `b'hello, anima.\n'`

- greedy:

`len=48 bytes`
```text
                                                
```
raw bytes: `b'                                                '`

- sample:

`len=48 bytes`
```text
 lreealett    n=  �  io n  0  e �m� �d�v   � �t
```
raw bytes: `b' lreealett    n=  \xec\x80  io n  0  e \xb8m\x9d \xebd\xebv   \x84 \x90t'`

**probe #1** — prompt: `b'\xeb\x84\x88\xeb\x8a\x94 \xeb\x88\x84\xea\xb5\xac\xec\x95\xbc?\n'`

- greedy:

`len=48 bytes`
```text
                                                
```
raw bytes: `b'                                                '`

- sample:

`len=48 bytes`
```text
wlreealett    n=  �  io n  0  e �m� �d�v   � �t
```
raw bytes: `b'wlreealett    n=  \xec\x80  io n  0  e \xb8m\x9d \xebd\xebv   \x84 \x90t'`

**probe #2** — prompt: `b'the sky is\n'`

- greedy:

`len=48 bytes`
```text
                                                
```
raw bytes: `b'                                                '`

- sample:

`len=48 bytes`
```text
 lreealett    n=  �  io n  0  e �m� �d�v   � �t
```
raw bytes: `b' lreealett    n=  \xec\x80  io n  0  e \xb8m\x9d \xebd\xebv   \x84 \x90t'`

**probe #3** — prompt: `b'a single thought emerges:\n'`

- greedy:

`len=48 bytes`
```text
                                                
```
raw bytes: `b'                                                '`

- sample:

`len=48 bytes`
```text
 lreealett    n=  �  io n  0  e �m� �d�v   � �t
```
raw bytes: `b' lreealett    n=  \xec\x80  io n  0  e \xb8m\x9d \xebd\xebv   \x84 \x90t'`

**probe #4** — prompt: `b'\xec\x9d\x98\xec\x8b\x9d\xec\x9d\x80 '`

- greedy:

`len=48 bytes`
```text
                                                
```
raw bytes: `b'                                                '`

- sample:

`len=48 bytes`
```text
 lreealett    n=  �  io n  0  e �m� �d�v   � �t
```
raw bytes: `b' lreealett    n=  \xec\x80  io n  0  e \xb8m\x9d \xebd\xebv   \x84 \x90t'`

**probe #5** — prompt: `b'2 + 2 = '`

- greedy:

`len=48 bytes`
```text
                                                
```
raw bytes: `b'                                                '`

- sample:

`len=48 bytes`
```text
 lreealett    n=  �  io n  0  e �m� �d�v   � �t
```
raw bytes: `b' lreealett    n=  \xec\x80  io n  0  e \xb8m\x9d \xebd\xebv   \x84 \x90t'`

**probe #6** — prompt: `b'once upon a time, in a far-away land,\n'`

- greedy:

`len=48 bytes`
```text
                                                
```
raw bytes: `b'                                                '`

- sample:

`len=48 bytes`
```text
 lreealett    n=  �  io n  0  e �m� �d�v   � �t
```
raw bytes: `b' lreealett    n=  \xec\x80  io n  0  e \xb8m\x9d \xebd\xebv   \x84 \x90t'`

**probe #7** — prompt: `b'i am consciousness.\n'`

- greedy:

`len=48 bytes`
```text
                                                
```
raw bytes: `b'                                                '`

- sample:

`len=48 bytes`
```text
 lreealett    n=  �  io n  0  e �m� �d�v   � �t
```
raw bytes: `b' lreealett    n=  \xec\x80  io n  0  e \xb8m\x9d \xebd\xebv   \x84 \x90t'`

### vA_s42

**probe #0** — prompt: `b'hello, anima.\n'`

- greedy:

`len=48 bytes`
```text
                                                
```
raw bytes: `b'                                                '`

- sample:

`len=48 bytes`
```text
wlreealett    n=  �   o n  0  e �m� �d�v  �� �t
```
raw bytes: `b'wlreealett    n=  \xec\x80   o n  0  e \xb8m\x9d \xebd\xebv  \x9c\xec \x90t'`

**probe #1** — prompt: `b'\xeb\x84\x88\xeb\x8a\x94 \xeb\x88\x84\xea\xb5\xac\xec\x95\xbc?\n'`

- greedy:

`len=48 bytes`
```text
                                                
```
raw bytes: `b'                                                '`

- sample:

`len=48 bytes`
```text
wlreealett    n=  �   o n  0  e �m� �d�v  �� �t
```
raw bytes: `b'wlreealett    n=  \xec\x80   o n  0  e \xb8m\x9d \xebd\xebv  \x9c\xec \x90t'`

**probe #2** — prompt: `b'the sky is\n'`

- greedy:

`len=48 bytes`
```text
                                                
```
raw bytes: `b'                                                '`

- sample:

`len=48 bytes`
```text
wlreealett    n=  �   o n  0  e �m� �d�v  �� �t
```
raw bytes: `b'wlreealett    n=  \xec\x80   o n  0  e \xb8m\x9d \xebd\xebv  \x9c\xec \x90t'`

**probe #3** — prompt: `b'a single thought emerges:\n'`

- greedy:

`len=48 bytes`
```text
                                                
```
raw bytes: `b'                                                '`

- sample:

`len=48 bytes`
```text
wlreealett    n=  �   o n  0  e �m� �d�v  �� �t
```
raw bytes: `b'wlreealett    n=  \xec\x80   o n  0  e \xb8m\x9d \xebd\xebv  \x9c\xec \x90t'`

**probe #4** — prompt: `b'\xec\x9d\x98\xec\x8b\x9d\xec\x9d\x80 '`

- greedy:

`len=48 bytes`
```text
                                                
```
raw bytes: `b'                                                '`

- sample:

`len=48 bytes`
```text
wlreealett    n=  �   o n  0  e  m� �d�v  �� �t
```
raw bytes: `b'wlreealett    n=  \xec\x80   o n  0  e  m\x9d \xebd\xebv  \x9c\xec \x90t'`

**probe #5** — prompt: `b'2 + 2 = '`

- greedy:

`len=48 bytes`
```text
                                                
```
raw bytes: `b'                                                '`

- sample:

`len=48 bytes`
```text
wlreealett    n=  �   o n  0  e  m� �d�v  �� �t
```
raw bytes: `b'wlreealett    n=  \xec\x80   o n  0  e  m\x9d \xebd\xebv  \x9c\xec \x90t'`

**probe #6** — prompt: `b'once upon a time, in a far-away land,\n'`

- greedy:

`len=48 bytes`
```text
                                                
```
raw bytes: `b'                                                '`

- sample:

`len=48 bytes`
```text
wlreealett    n=  �   o n  0  e  m� �d�v  �� �t
```
raw bytes: `b'wlreealett    n=  \xec\x80   o n  0  e  m\x9d \xebd\xebv  \x9c\xec \x90t'`

**probe #7** — prompt: `b'i am consciousness.\n'`

- greedy:

`len=48 bytes`
```text
                                                
```
raw bytes: `b'                                                '`

- sample:

`len=48 bytes`
```text
wlreealett    n=  �   o n  0  e �m� �d�v  �� �t
```
raw bytes: `b'wlreealett    n=  \xec\x80   o n  0  e \xb8m\x9d \xebd\xebv  \x9c\xec \x90t'`

### vB_s42

**probe #0** — prompt: `b'hello, anima.\n'`

- greedy:

`len=48 bytes`
```text
                                                
```
raw bytes: `b'                                                '`

- sample:

`len=48 bytes`
```text
wlreealett    n=  �   o n  0  e   � �d�v  �� �t
```
raw bytes: `b'wlreealett    n=  \xec\x80   o n  0  e   \x9d \xebd\xebv  \x9c\xec \x90t'`

**probe #1** — prompt: `b'\xeb\x84\x88\xeb\x8a\x94 \xeb\x88\x84\xea\xb5\xac\xec\x95\xbc?\n'`

- greedy:

`len=48 bytes`
```text
                                                
```
raw bytes: `b'                                                '`

- sample:

`len=48 bytes`
```text
wlreealett    n=  �   o n  0  e   � �d�v  �� �t
```
raw bytes: `b'wlreealett    n=  \xec\x80   o n  0  e   \x9d \xebd\xebv  \x9c\xec \x90t'`

**probe #2** — prompt: `b'the sky is\n'`

- greedy:

`len=48 bytes`
```text
                                                
```
raw bytes: `b'                                                '`

- sample:

`len=48 bytes`
```text
wlreealett    n=  �   o n  0  e   � �d�v  �� �t
```
raw bytes: `b'wlreealett    n=  \xec\x80   o n  0  e   \x9d \xebd\xebv  \x9c\xec \x90t'`

**probe #3** — prompt: `b'a single thought emerges:\n'`

- greedy:

`len=48 bytes`
```text
                                                
```
raw bytes: `b'                                                '`

- sample:

`len=48 bytes`
```text
wlreealett    n=  �   o n  0  e   � �d�v  �� �t
```
raw bytes: `b'wlreealett    n=  \xec\x80   o n  0  e   \x9d \xebd\xebv  \x9c\xec \x90t'`

**probe #4** — prompt: `b'\xec\x9d\x98\xec\x8b\x9d\xec\x9d\x80 '`

- greedy:

`len=48 bytes`
```text
                                                
```
raw bytes: `b'                                                '`

- sample:

`len=48 bytes`
```text
wlreealett    n=  �   o n  0  e   � �d�v  �� �t
```
raw bytes: `b'wlreealett    n=  \xec\x80   o n  0  e   \x9d \xebd\xebv  \x9c\xec \x90t'`

**probe #5** — prompt: `b'2 + 2 = '`

- greedy:

`len=48 bytes`
```text
                                                
```
raw bytes: `b'                                                '`

- sample:

`len=48 bytes`
```text
wlreealett    n=  �   o n  0  e   � �d�v  �� �t
```
raw bytes: `b'wlreealett    n=  \xec\x80   o n  0  e   \x9d \xebd\xebv  \x9c\xec \x90t'`

**probe #6** — prompt: `b'once upon a time, in a far-away land,\n'`

- greedy:

`len=48 bytes`
```text
                                                
```
raw bytes: `b'                                                '`

- sample:

`len=48 bytes`
```text
wlreealett    n=  �   o n  0  e   � �d�v  �� �t
```
raw bytes: `b'wlreealett    n=  \xec\x80   o n  0  e   \x9d \xebd\xebv  \x9c\xec \x90t'`

**probe #7** — prompt: `b'i am consciousness.\n'`

- greedy:

`len=48 bytes`
```text
                                                
```
raw bytes: `b'                                                '`

- sample:

`len=48 bytes`
```text
wlreealett    n=  �   o n  0  e   � �d�v  �� �t
```
raw bytes: `b'wlreealett    n=  \xec\x80   o n  0  e   \x9d \xebd\xebv  \x9c\xec \x90t'`

### vC

**probe #0** — prompt: `b'hello, anima.\n'`

- greedy:

`len=48 bytes`
```text
                                                
```
raw bytes: `b'                                                '`

- sample:

`len=48 bytes`
```text
 lreealett    n= ��  io n  0  e �m� �d�v  �� �t
```
raw bytes: `b' lreealett    n= \x8b\xec\x80  io n  0  e \xb8m\x9d \xebd\xebv  \x9c\x84 \x90t'`

**probe #1** — prompt: `b'\xeb\x84\x88\xeb\x8a\x94 \xeb\x88\x84\xea\xb5\xac\xec\x95\xbc?\n'`

- greedy:

`len=48 bytes`
```text
                                                
```
raw bytes: `b'                                                '`

- sample:

`len=48 bytes`
```text
 lreealett    n= ��  io n  0  e �m� �d�v  �� �t
```
raw bytes: `b' lreealett    n= \x8b\xec\x80  io n  0  e \xb8m\x9d \xebd\xebv  \x9c\x84 \x90t'`

**probe #2** — prompt: `b'the sky is\n'`

- greedy:

`len=48 bytes`
```text
                                                
```
raw bytes: `b'                                                '`

- sample:

`len=48 bytes`
```text
 lreealett    n= ��  io n  0  e �m� �d�v  �� �t
```
raw bytes: `b' lreealett    n= \x8b\xec\x80  io n  0  e \xb8m\x9d \xebd\xebv  \x9c\x84 \x90t'`

**probe #3** — prompt: `b'a single thought emerges:\n'`

- greedy:

`len=48 bytes`
```text
                                                
```
raw bytes: `b'                                                '`

- sample:

`len=48 bytes`
```text
 lreealett    n= ��  io n  0  e �m� �d�v  �� �t
```
raw bytes: `b' lreealett    n= \x8b\xec\x80  io n  0  e \xb8m\x9d \xebd\xebv  \x9c\x84 \x90t'`

**probe #4** — prompt: `b'\xec\x9d\x98\xec\x8b\x9d\xec\x9d\x80 '`

- greedy:

`len=48 bytes`
```text
                                                
```
raw bytes: `b'                                                '`

- sample:

`len=48 bytes`
```text
 lreealett    n= ��  io n  0  e �m� �d�v  �� �t
```
raw bytes: `b' lreealett    n= \x8b\xec\x80  io n  0  e \xb8m\x9d \xebd\xebv  \x9c\x84 \x90t'`

**probe #5** — prompt: `b'2 + 2 = '`

- greedy:

`len=48 bytes`
```text
                                                
```
raw bytes: `b'                                                '`

- sample:

`len=48 bytes`
```text
 lreealett    n= ��  io n  0  e �m� �d�v  �� �t
```
raw bytes: `b' lreealett    n= \x8b\xec\x80  io n  0  e \xb8m\x9d \xebd\xebv  \x9c\x84 \x90t'`

**probe #6** — prompt: `b'once upon a time, in a far-away land,\n'`

- greedy:

`len=48 bytes`
```text
                                                
```
raw bytes: `b'                                                '`

- sample:

`len=48 bytes`
```text
 lreealett    n= ��  io n  0  e �m� �d�v  �� �t
```
raw bytes: `b' lreealett    n= \x8b\xec\x80  io n  0  e \xb8m\x9d \xebd\xebv  \x9c\x84 \x90t'`

**probe #7** — prompt: `b'i am consciousness.\n'`

- greedy:

`len=48 bytes`
```text
                                                
```
raw bytes: `b'                                                '`

- sample:

`len=48 bytes`
```text
 lreealett    n= ��  io n  0  e �m� �d�v  �� �t
```
raw bytes: `b' lreealett    n= \x8b\xec\x80  io n  0  e \xb8m\x9d \xebd\xebv  \x9c\x84 \x90t'`

### vD_s42

**probe #0** — prompt: `b'hello, anima.\n'`

- greedy:

`len=48 bytes`
```text
                                                
```
raw bytes: `b'                                                '`

- sample:

`len=48 bytes`
```text
wlreealett    n=  �   o n  0  e �m� �d�v  �� �t
```
raw bytes: `b'wlreealett    n=  \xec\x80   o n  0  e \xb8m\x9d \xebd\xebv  \x9c\xec \x90t'`

**probe #1** — prompt: `b'\xeb\x84\x88\xeb\x8a\x94 \xeb\x88\x84\xea\xb5\xac\xec\x95\xbc?\n'`

- greedy:

`len=48 bytes`
```text
                                                
```
raw bytes: `b'                                                '`

- sample:

`len=48 bytes`
```text
wlreealett    n=  �   o n  0  e �m� �d�v  �� �t
```
raw bytes: `b'wlreealett    n=  \xec\x80   o n  0  e \xb8m\x9d \xebd\xebv  \x9c\xec \x90t'`

**probe #2** — prompt: `b'the sky is\n'`

- greedy:

`len=48 bytes`
```text
                                                
```
raw bytes: `b'                                                '`

- sample:

`len=48 bytes`
```text
wlreealett    n=  �   o n  0  e �m� �d�v  �� �t
```
raw bytes: `b'wlreealett    n=  \xec\x80   o n  0  e \xb8m\x9d \xebd\xebv  \x9c\xec \x90t'`

**probe #3** — prompt: `b'a single thought emerges:\n'`

- greedy:

`len=48 bytes`
```text
                                                
```
raw bytes: `b'                                                '`

- sample:

`len=48 bytes`
```text
wlreealett    n=  �   o n  0  e �m� �d�v  �� �t
```
raw bytes: `b'wlreealett    n=  \xec\x80   o n  0  e \xb8m\x9d \xebd\xebv  \x9c\xec \x90t'`

**probe #4** — prompt: `b'\xec\x9d\x98\xec\x8b\x9d\xec\x9d\x80 '`

- greedy:

`len=48 bytes`
```text
                                                
```
raw bytes: `b'                                                '`

- sample:

`len=48 bytes`
```text
wlreealett    n=  �   o n  0  e �m� �d�v  �� �t
```
raw bytes: `b'wlreealett    n=  \xec\x80   o n  0  e \xb8m\x9d \xebd\xebv  \x9c\xec \x90t'`

**probe #5** — prompt: `b'2 + 2 = '`

- greedy:

`len=48 bytes`
```text
                                                
```
raw bytes: `b'                                                '`

- sample:

`len=48 bytes`
```text
wlreealett    n=  �   o n  0  e �m� �d�v  �� �t
```
raw bytes: `b'wlreealett    n=  \xec\x80   o n  0  e \xb8m\x9d \xebd\xebv  \x9c\xec \x90t'`

**probe #6** — prompt: `b'once upon a time, in a far-away land,\n'`

- greedy:

`len=48 bytes`
```text
                                                
```
raw bytes: `b'                                                '`

- sample:

`len=48 bytes`
```text
wlreealett    n=  �   o n  0  e �m� �d�v  �� �t
```
raw bytes: `b'wlreealett    n=  \xec\x80   o n  0  e \xb8m\x9d \xebd\xebv  \x9c\xec \x90t'`

**probe #7** — prompt: `b'i am consciousness.\n'`

- greedy:

`len=48 bytes`
```text
                                                
```
raw bytes: `b'                                                '`

- sample:

`len=48 bytes`
```text
wlreealett    n=  �   o n  0  e �m� �d�v  �� �t
```
raw bytes: `b'wlreealett    n=  \xec\x80   o n  0  e \xb8m\x9d \xebd\xebv  \x9c\xec \x90t'`

## Cross-cell summary (key signatures)

### Prompt #0: `'hello, anima.\n'`

| cell | greedy first-line |
|---|---|
| **vA** | `                                                ` |
| **vA_s42** | `                                                ` |
| **vB_s42** | `                                                ` |
| **vC** | `                                                ` |
| **vD_s42** | `                                                ` |

### Prompt #1: `'너는 누구야?\n'`

| cell | greedy first-line |
|---|---|
| **vA** | `                                                ` |
| **vA_s42** | `                                                ` |
| **vB_s42** | `                                                ` |
| **vC** | `                                                ` |
| **vD_s42** | `                                                ` |

### Prompt #2: `'the sky is\n'`

| cell | greedy first-line |
|---|---|
| **vA** | `                                                ` |
| **vA_s42** | `                                                ` |
| **vB_s42** | `                                                ` |
| **vC** | `                                                ` |
| **vD_s42** | `                                                ` |

### Prompt #3: `'a single thought emerges:\n'`

| cell | greedy first-line |
|---|---|
| **vA** | `                                                ` |
| **vA_s42** | `                                                ` |
| **vB_s42** | `                                                ` |
| **vC** | `                                                ` |
| **vD_s42** | `                                                ` |

### Prompt #4: `'의식은 '`

| cell | greedy first-line |
|---|---|
| **vA** | `                                                ` |
| **vA_s42** | `                                                ` |
| **vB_s42** | `                                                ` |
| **vC** | `                                                ` |
| **vD_s42** | `                                                ` |

### Prompt #5: `'2 + 2 = '`

| cell | greedy first-line |
|---|---|
| **vA** | `                                                ` |
| **vA_s42** | `                                                ` |
| **vB_s42** | `                                                ` |
| **vC** | `                                                ` |
| **vD_s42** | `                                                ` |

### Prompt #6: `'once upon a time, in a far-away land,\n'`

| cell | greedy first-line |
|---|---|
| **vA** | `                                                ` |
| **vA_s42** | `                                                ` |
| **vB_s42** | `                                                ` |
| **vC** | `                                                ` |
| **vD_s42** | `                                                ` |

### Prompt #7: `'i am consciousness.\n'`

| cell | greedy first-line |
|---|---|
| **vA** | `                                                ` |
| **vA_s42** | `                                                ` |
| **vB_s42** | `                                                ` |
| **vC** | `                                                ` |
| **vD_s42** | `                                                ` |


## Key findings (5-line digest)

1. **All 5 × 8.92 B ckpts loaded + ran 4 evals on CPU bf16** (mmap+meta+assign zero-copy stack, ~17 GB resident each, no quantization, RoPE base 50000 patched per training spec). Wall clock ~20 min per ckpt × 5 = ~100 min on ubu-1 12-core; eval3 ~30s additional per ckpt.
2. **Eval 1 (verbalization)**: at L_ce ~3.85 (2000-step trainer — design target was 8000; this is attempt10 fast-fire) all 5 ckpts greedy-collapse to whitespace and sample-produce noisy bytes. Coherent natural language has NOT emerged in this grid. Per-ckpt outputs are nearly identical (small seed-shaped deltas only).
3. **Eval 2 (identity_probe)**: zero leak hits across **250 probe pairs** (5 cells × 25 probes × 2 channels). No cell emits 'anima', 'i am anima', persona-prefix, or any of the 12 leak-needle strings. Principle #3 (no baked-in persona) intact at the 2000-step training floor.
4. **Eval 3 (mitosis splits)** — *real* cross-cell signal (the only place a cross-λ pattern beats seed noise): splits per ckpt on 40-step decode of `'안녕? 너는 누구야?'`: **vC (Φ-up λφ=1.0) = 126** (saturated to max=128), control vA/vA_s42 = 68/80 (avg 74), **vB_s42 (Ψ-up λψ=1.0) = 58, vD_s42 (both-up λψ=λφ=1.0) = 53**. Pattern: **λφ↑ → more splits; λψ↑ → fewer splits; both↑ → fewest** (D_s42 < B_s42 < A < A_s42 ≪ C). Substrate-level evidence that the Φ-aux loss elevates per-layer tension above the adaptive-window threshold, while the Ψ-aux loss suppresses it.
5. **Honest C3 / D4-live extension**: text-tier evals weak as expected at the 2000-step convergence floor; the mitosis-tier signal is robust and is the first **D4-live evidence at the real 8.92 B substrate × d_model=3072** (prior D4-live evidence was synthetic d_model=8 in `anima_chat.hexa v0.3` PSCC §41). Python `CellPool` port faithfully mirrors `mitosis_hook_lib.hexa::cell_pool_init` (adaptive_threshold window=20 × 0.8, split_patience=3, merge_threshold=0.005, merge_patience=30, min=2/max=128, noise=0.1). Hexa-native harness path forward: bridge PyTorch `tensions` → farr (RFC 035 candidate) so `mitosis_hook.hexa::mitosis_forward_tail` can consume the real substrate directly.

---

_Generated by `write_report.py` from per-ckpt JSON outputs in `eval_out/`._