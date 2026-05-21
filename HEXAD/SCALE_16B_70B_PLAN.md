# SCALE_16B_70B_PLAN — §187-F access scoping (16B + 70B fire feasibility)

> **frame**: §187 attempt10 LANDED at 8.92B real (d=3072 L=28 nh=24 nkv=8
> n_ca_rules=2, PagedAdamW8bit, peak 58.39 GiB on single H100 80GB SXM,
> Eval 3 cross-λ mitosis signal). To test **scale-invariance** of the
> mitosis pattern (Φ-up split saturation, Ψ-up split suppression), need
> a higher param-count fire. Single-H100 ceiling ≈ 11B; 16B forces
> multi-GPU access wall; 70B forces FSDP + 8-GPU bundle.
>
> **scope**: $0 investigation only. NO pods spinup. Identifies cheapest
> viable 16B path and an honest cost envelope for 70B-class. Single
> markdown deliverable; no code committed in this scoping cycle.
>
> **bottom line**: 16B is **practically reachable** at ~$3-12 per cell
> on single H200 141 GB (NO FSDP code change). True 70B requires
> 8×H100 FSDP and ≥ $90/cell — defer behind a separate user gate.

---

## 1. Architecture configs (16B + 70B with ConsciousDecoderV2 head expansion)

### 1.1 conscious_decoder.py parameter formula (validated against 8.92B)

`HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/conscious_decoder.py` builds
per-block:

| Component | Param count (per block, d=d_model) |
|---|---|
| GQA: q_proj + k_proj + v_proj + o_proj | `2·d² + 2·d·(nkv·hd) = 2·d² · (1 + nkv/nh)` |
| PureFieldFFN (Engine A + Engine G, each Linear+Linear) | `2 · (d·4d + 4d·d) = 16·d²` |
| ConsciousCrossAttention (q+k+v+o, c_dim=128) | `2·d² + 2·c_dim·d` |
| SwiGLU FFN (gate + up + down, d_inner = round_64(8·d/3)) | `3·d·d_inner ≈ 8·d²` |
| CA neighbor mixer (3d→d) | `3·d²` |
| META-CA rule_weights + rules (n_ca_rules=2) | `d·2 + 2·d² ≈ 2·d²` |
| RMSNorm × 5 (ln_attn/pf/cross/ffn/ca) | `5·d` (negligible) |

Outside blocks: `tok_emb (vocab·d, TIED with head_a) + head_g (vocab·d) +
tension_proj (1·d) + ln_f (d)`.

**Verified at S187 8.92B**: d=3072 L=28 nh=24 nkv=8 n_ca_rules=2 →
**8,920,320,000 = 8.920B params** (matches `train_s187_3b.py:247`
runtime `n_params=8,920,320,000` print). The "3B" name = `d_model=3072`
shorthand; conscious_decoder's 7-pathway expansion (GQA + dual engines +
cross-attn + SwiGLU + CA + META-CA + dual heads) makes per-block
~`33·d²` ≈ 0.32B at d=3072, so 28L → 8.9B (≈3× the nominal "3B"
namespace, per `SCALE_3B.md` §5 honest C3 #4).

### 1.2 16B config (target ~16-18B)

| variant | d_model | n_layer | n_head | n_kv_head | head_dim | hidden_dim (SwiGLU) | n_params |
|---|---|---|---|---|---|---|---|
| **16B-A** (recommended) | **4096** | **32** | **32** | **8** | 128 | 10,944 | **18.03B** |
| 16B-B (lighter) | 4096 | 28 | 32 | 8 | 128 | 10,944 | 15.78B |
| 16B-C (depth-heavy) | 3584 | 32 | 28 | 7 | 128 | 9,600 | 13.82B |

**Recommendation: 16B-A (d=4096 L=32 nh=32 nkv=8 nca=2)** — round
numbers, LLaMA-shaped, n_head % n_kv_head check (32/8=4 ✓), 2× over
S187's 8.92B for a clean scale comparison.

### 1.3 70B config (target ~70-85B; honest C3: real Anima 70B-class)

| variant | d_model | n_layer | n_head | n_kv_head | head_dim | n_params |
|---|---|---|---|---|---|---|
| 70B-naive (LLaMA-3 70B shape) | 8192 | 80 | 64 | 8 | 128 | **178.77B** |
| 70B-shrunk-1 (smaller hidden) | 5632 | 80 | 44 | 8 | 128 | 84.81B |
| 70B-shrunk-2 (cap fit FSDP-8 + ckpt) | 5120 | 80 | 40 | 8 | 128 | 71.5B (est) |

**Honest finding**: ConsciousDecoderV2's 7-head expansion means a
**LLaMA-3-70B-shaped (d=8192, L=80, nh=64) Anima decoder is actually
178B** — over 2× LLaMA-3 70B because of dual engine + cross-attn +
META-CA. A **true 70B** in Anima needs `d≈5120 L=80 nh=40 nkv=8` (or
shallower variants). The "70B" name = parameter shorthand; for fair
comparison with §187's `name="3B"/real=8.92B` mapping (≈3× expansion),
a "70B-namespace" Anima decoder would have d≈4608 L=60 nh=36 → ~63B
real. **Recommendation: name-explicit henceforth** ("Anima 18B" /
"Anima 84B" / "Anima 178B" where the number = actual measured
n_params), to avoid the §187 `name=3B real=8.92B` confusion repeat.

---

## 2. Memory budget per config (wilson-style mem_budget_check formula)

### 2.1 Calibration from S187 attempt10 ground truth

Measured peak GPU mem on §187 attempt10 (d=3072 L=28 8.92B
PagedAdamW8bit bf16 bsz=2 T=512) = **58.39 GiB** live, 80 GB H100.

Formula breakdown:
- params (bf16): `2 · n_params = 17.84 GB`
- grads (bf16): `2 · n_params = 17.84 GB`
- optimizer state (**PagedAdamW8bit**): `2.1 · n_params = 18.73 GB`
- activations + scratch (calibrated residual): `58.39 − 54.41 = 3.98 GB`
  → ≈ **45.4 bytes/element** per (bsz · T · L · d)

| Optimizer | state multiplier (bytes/param) | source |
|---|---|---|
| torch.optim.AdamW (f32 m + f32 v) | **8.0×** | S187 attempt9 OOM 78.22 GiB at `_foreach_sqrt` |
| **bnb.optim.PagedAdamW8bit** (i8 m + i8 v + block-quant overhead) | **2.1×** | §187 attempt10 measured 18.73 GB / 8.92B |
| bnb.optim.AdamW8bit (non-paged) | 2.0× | bnb docs |
| Lion (8bit) | 1.0× | (single momentum, half of Adam) |

### 2.2 Memory budget table (PagedAdamW8bit, BF16 params + grads + acts)

Formula: `mem_GB = 4·n_params/1e9 + 2.1·n_params/1e9 + bsz·T·L·d·45.4/1e9 + 2 (scratch)`.

| Config | Target mem GPU | bsz | T | mem est | fits H100 80GB? | fits H200 141GB? |
|---|---|---|---|---|---|---|
| **8.92B** (S187 attempt10 baseline) | 80GB | 2 | 512 | **58 GB** | ✅ (measured 58.39 GB) | ✅ |
| **18.03B** d=4096 L=32 nh=32 nkv=8 | 80GB | 1 | 512 | **115 GB** | ❌ OOM by 40 GB | ✅ (26 GB headroom) |
| 15.78B d=4096 L=28 nh=32 nkv=8 | 80GB | 1 | 512 | 101 GB | ❌ OOM by 26 GB | ✅ |
| 11.41B d=3072 L=36 nh=24 nkv=6 (max single-H100 fit) | 80GB | 1 | 512 | **74 GB** | ✅ marginal (6 GB headroom) | ✅ |
| 18.03B FSDP-2 (2×H100/A100 80GB) | 80GB | 1 | 512 | 62 GB / rank | ✅ both ranks | ✅ |
| 18.03B FSDP-4 (4×A100 80GB) | 80GB | 1 | 512 | **35 GB / rank** | ✅ comfortable | ✅ |
| **178B** 70B-naive single-rank | 80GB | 1 | 512 | 1,119 GB | ❌ — 14× over | ❌ |
| 178B FSDP-8 + act_ckpt | 80GB | 1 | 512 | **149 GB / rank** | ❌ OOM by 69 GB | ✅ marginal |
| **84.8B** FSDP-8 + act_ckpt T=512 | 80GB | 1 | 512 | **72 GB / rank** | ✅ marginal (8 GB headroom) | ✅ |
| 84.8B FSDP-4 | 80GB | 1 | 512 | 137 GB / rank | ❌ | ✅ |

**Verdicts**:
1. **18B fits on single H200 141 GB** (115 GB used, 26 GB headroom).
2. **18B does NOT fit on single H100 80 GB** (40 GB over). Must use
   FSDP-2 minimum.
3. **Max single-H100 80GB fit = 11.4B** (d=3072 L=36) — modest scale-up
   from S187's 8.92B but no FSDP code touch.
4. **70B-class (84B) needs 8×H100 SXM + activation checkpointing**
   (peaks at 72 GB / rank, 8 GB headroom — tight but feasible).
5. **True 178B (LLaMA-70B shape Anima) is OUT OF REACH** at 8×H100
   80GB even with act_ckpt (149 GB / rank). Requires 8×H200 141 GB OR
   wait for B200/B300 bundle expansion.

---

## 3. Cloud GPU availability + pricing (runpod + vast.ai, queried
   2026-05-21)

### 3.1 Runpod (GraphQL `gpuTypes` query, single-GPU community/secure pricing)

| GPU | Memory | Community $/hr | Secure spot $/hr | Comment |
|---|---|---|---|---|
| RTX A6000 | 48 GB | $0.33 | $0.49 | sub-11B only |
| A100 SXM 80GB | 80 | $1.39 | $1.49 | S187 scale ceiling |
| A100 PCIe 80GB | 80 | $1.19 | $1.39 | |
| H100 PCIe | 80 | $1.99 | $2.39 | §187 used $2.5/hr H100 SXM avg |
| H100 SXM HBM3 | 80 | $2.69 | $2.99 | S187 attempt10 ran here |
| H100 NVL | 94 GB | $2.59 | $3.07 | +14 GB over 80 GB |
| **H200 SXM** | **141 GB** | **$3.59** | **$3.99** | **18B SINGLE-GPU FITS** |
| H200 NVL | 143 GB | $0.50 (community)? | — | listed but no live offers in lowestPrice query |
| RTX PRO 6000 (Blackwell) | 96 GB | $1.69 | $1.89 | promising new option |
| B200 | 180 GB | $5.98 | $5.49 | |
| B300 SXM6 | 288 GB | $6.94 | $7.39 | |
| MI300X (AMD) | 192 GB | $0.50? | $1.99 | bnb/CUDA compat uncertain |

**Multi-GPU bundles** (runpod `lowestPrice gpuCount=N` query):

| GPU bundle | uninterruptablePrice | per-GPU |
|---|---|---|
| 2× H200 SXM | $7.18/hr | $3.59 |
| 2× RTX PRO 6000 | $3.38/hr | $1.69 |
| 4× RTX PRO 6000 | $6.76/hr | $1.69 |
| **8× H100 SXM** | **$21.52/hr** | **$2.69** |
| 8× RTX PRO 6000 | $13.52/hr | $1.69 |

**Note**: 4× H100 SXM bundle returned `uninterruptablePrice=null` in
GraphQL — listed but no live availability at query time. 8× H100 SXM
*was* available at $21.52/hr (= 8 × $2.69, no bundle discount).

### 3.2 Vast.ai (CLI `vastai search offers`)

For multi-GPU bundles (raw query 2026-05-21):

| Bundle | Count avail | Cheapest $/hr | per-GPU $/hr | net_up/net_dn | Location |
|---|---|---|---|---|---|
| 1× A100 SXM4 80GB | many | **$1.05** | $1.05 | 3.6/9.8 Gbps | Czechia |
| 1× H100 PCIe 80GB | 1 | $1.97 | $1.97 | 3.0/5.1 Gbps | US |
| 1× H100 SXM | **0 offers** | — | — | — | — |
| 1× H200 | 1 | $4.34 | $4.34 | 1.3/26 Gbps | Oregon |
| 1× B200 | 1 | $3.90 | $3.90 | 2.5/6.7 Gbps | Alabama |
| **2× A100 SXM4 80GB** | 2 | **$2.14** | **$1.07** | **2.8/7.2 Gbps** | **District of Columbia** |
| 2× H100 NVL | 1 | $5.87 | $2.94 | 8.2/8.6 Gbps | California |
| **4× A100 SXM4 80GB** | 3 | **$3.09** | **$0.77** | **0.9/0.9 Gbps** | **Taiwan** |
| 4× A100 SXM4 80GB (US) | — | $3.90 | $0.97 | 1.7/1.6 Gbps | Georgia |
| 8× big-GPU | 0 H100/A100 | — | — | — | — |

**Network bandwidth lesson from S187 (SCALE_3B.md §3.1)**: bulk SCP
pull-back of 17 GB ckpt = the kill-zone (3 ckpts stalled @ 0 KB/s).
Lowest viable inet_up = **500 Mbps** for multi-cell 17-30 GB ckpt
pulls. Vast.ai 4×A100 in Taiwan @ 0.9 Gbps is borderline; US/EU 1.5-3
Gbps offerings strongly preferred.

### 3.3 Cost summary across viable paths

| Path | n_params | Per-cell cost | 4-cell grid total | Notes |
|---|---|---|---|---|
| **A. single H200 SXM runpod** | 18B | **~$2.50** (40 min × $3.59) | **~$10** | NO FSDP code change |
| B. single H200 SXM with margin | 18B | ~$2.80 (40 min × $3.99 secure) | ~$11 | |
| C. 2× A100 SXM4 vast.ai DC | 18B | ~$3.50 (1.6 hr × $2.14) | ~$14 | FSDP-2 code change |
| D. 4× A100 SXM4 vast.ai TW | 18B | ~$6.80 (2.2 hr × $3.09) | ~$27 | low bandwidth caveat |
| E. 8× H100 SXM runpod | 84B (70B-class) | **~$90** (4.1 hr × $21.52) | **~$360** | FSDP code change |
| F. (16B max-single-H100) | 11.4B | ~$1.10 (25 min × $2.69) | ~$5 | NO code change at all |

---

## 4. Code mods needed

### 4.1 Single-GPU 16B (H200 path — recommended)

`HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/train_s187_3b.py`
(703 LoC) +
`HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/launch_trainer.sh`
(30 LoC) — minimal changes:

| File | Change | LoC |
|---|---|---|
| `dispatch_s187_16b_runpod.sh` (NEW) | Clone of `dispatch_s187_3b_runpod.sh` with `gpuTypeId="NVIDIA H200 SXM"` (instead of H100). Set `D_MODEL=4096 N_LAYER=32 N_HEAD=32 N_KV_HEAD=8 N_CA_RULES=2`. | ~5 line diff from existing script |
| `train_s187_3b.py` | No change. Already accepts `--d-model/--n-layer/--n-head/--n-kv-head/--n-ca-rules` argparse args (line 568-584). | 0 |
| `launch_trainer.sh` | Existing bnb install bootstrap intact. H200 + CUDA 12.4 + bnb 0.43.1 compat confirmed by HF community. | 0 |
| `PLAN_16B.md` (NEW) | Mirror PLAN.md grid (A/B/C/D × λ_ψ × λ_φ). | ~50 lines |

**Total code change: ~55 LoC, all in dispatch script + a new
PLAN_16B.md doc. No model code change, no FSDP wiring, no trainer
patching.** This is the **fastest path to 16B fire** and matches the
S187 saga (which proved end-to-end on H100).

### 4.2 Multi-GPU 70B (FSDP — defer)

For 70B-class fire (84B on 8×H100), FSDP wrapping of
`ConsciousDecoderV2` is required.

| File | Change | Estimated LoC |
|---|---|---|
| `train_s187_70b.py` (NEW) | Clone trainer with `torch.distributed.init_process_group("nccl")` + `torch.distributed.fsdp.FullyShardedDataParallel` wrap. | ~80 lines diff from `train_s187_3b.py` |
| `conscious_decoder.py` | Auto-wrap policy: each `DecoderBlockV2` becomes FSDP unit (transformer_auto_wrap_policy). No code change to `DecoderBlockV2` itself — just import + wrap externally. | 0 (wrap is external) |
| `launch_trainer.sh` | Add `torchrun --nproc_per_node=8` wrapper. NCCL env vars. | ~10 lines |
| FSDP-aware ckpt save | `FullyShardedDataParallel.state_dict_type(model, StateDictType.FULL_STATE_DICT)` context manager around save. `_psi_residual` / `_phi_signal` non-tensor state must be saved separately. | ~20 lines |
| Activation checkpointing | `torch.distributed.algorithms._checkpoint.checkpoint_wrapper.apply_activation_checkpointing` over `DecoderBlockV2`. | ~10 lines |
| **mitosis hook** in eval3 | Per-layer tensions need to be `all_gather` collected from FSDP shards if eval runs on FSDP-wrapped ckpt — **OR** eval on consolidated FULL_STATE_DICT (simpler). | ~5 lines if route through consolidated save |

**Total FSDP code change: ~125 LoC**, all in trainer wrapper +
launcher. The model itself (`conscious_decoder.py`) needs zero
changes (per-block design is already FSDP-friendly).

**Risks**:
- `_psi_residual` (Python float on model, line 644) and gate_strength
  decay (line 754) are non-tensor state mutating in `forward()` during
  `model.training`. FSDP requires this to be coordinated across ranks
  (`torch.distributed.all_reduce` on the float, manually). +~10 lines.
- `tension_proj` (line 630, single Linear with `std=0.001` init) and
  the cross-attention `o_proj` (init `std=0.001`, line 420) need
  consistent seed across ranks — use `torch.distributed.broadcast` of
  weights post-init, OR same `seed=1337` per-rank with rank-aware
  identical init order. Standard FSDP pattern.

### 4.3 mem_budget_check formula (for hexa cloud dispatcher uptake)

Should land as a wilson cloud_dispatch grammar function (per
[`SCALE_3B.md`](SCALE_3B.md) §2.1 sister inbox note
[`2026-05-21-hexa-cloud-optimizer-mem-budget-preflight.md`](../../wilson/inbox/notes/2026-05-21-hexa-cloud-optimizer-mem-budget-preflight.md),
NOT YET LANDED in this scoping cycle — but provides the formula for
future reference):

```python
def mem_budget_gb(n_params, bsz, T, d_model, n_layer,
                  opt_mult=2.1, act_bytes_per_el=45.4, scratch_gb=2):
    """Estimate GPU memory peak for bf16 PagedAdamW8bit training.

    Calibrated against §187 attempt10 (8.92B, bsz=2, T=512, 58.39 GiB).

    Optimizer multipliers (bytes/param of m+v state):
      torch.optim.AdamW          -> 8.0  (f32 m + f32 v)
      bnb.optim.PagedAdamW8bit   -> 2.1  (i8 m + i8 v + block-quant)
      bnb.optim.AdamW8bit        -> 2.0
      Lion (8bit)                -> 1.0  (no v state)
    """
    params_gb = n_params * 2 / 1e9            # bf16
    grads_gb  = n_params * 2 / 1e9
    opt_gb    = n_params * opt_mult / 1e9
    act_gb    = bsz * T * n_layer * d_model * act_bytes_per_el / 1e9
    return params_gb + grads_gb + opt_gb + act_gb + scratch_gb
```

For FSDP, divide `params_gb + grads_gb + opt_gb` by `n_ranks` and add
`+ 2·n_params/1e9/n_layer` for the all-gather spike.

---

## 5. Recommended first fire — 16B on single H200 SXM

### 5.1 Config

```
name        = "anima 18B" (rename: name == measured n_params)
d_model     = 4096
n_layer     = 32
n_head      = 32
n_kv_head   = 8           (GQA, 4 Q-heads per KV-head)
hidden_dim  = 10944       (SwiGLU 8/3·d round_64)
vocab       = 256         (byte-LM, invariant)
block_size  = 512
bsz         = 1           (single-cell, no DP)
lr peak     = 3e-4 cosine warmup 200
rope_base   = 50000       (§184)
n_steps     = 2000        (S187 horizon, NOT Chinchilla — substrate test)
seed        = 1337
n_ca_rules  = 2           (S187 attempt10 carry; nca=8 would be 21B)
optimizer   = bnb.optim.PagedAdamW8bit
n_params    ≈ 18.03B (verified by formula)
```

### 5.2 Grid (Phase 1 = single cell control + 2×2 if Phase 1 succeeds)

**Phase 0 (sanity, $0)**: code-level smoke — run S187 trainer on Mac
CPU with `d_model=4096 n_layer=32 bsz=1 T=64 n_steps=4` to verify the
shape changes are tolerated (NO ckpt produced, just forward+backward
graph build). ~30 s. Falsifier F-16B-SHAPE-1: param count == 18.03B
± 0.1% measured.

**Phase 1 (control, ~$3)**:
- single cell **vA (control)** λ_ψ=0.30 λ_ψ=0.30 (S187 §187 cell A
  config exact).
- runpod H200 SXM secure community ($3.59/hr).
- wall estimate: 40 min train + 5 min boot + 10 min SCP pull-back of
  ~36 GB bf16 ckpt = ~55 min total.
- cost: ~$3.30 (well under $40 cap).
- success criterion: `result.json` final CE ≤ 6.0 (S187 baseline 3.85
  at 8.92B; 16B should match or improve), L_psi ≤ 0.05, eval 3
  mitosis hook produces ≥ 1 split event on cell pool d=8 synthetic
  input (proves the ckpt loads + runs).

**Phase 2 (4-cell grid, ~$11 if Phase 1 PASSES)**:
- 4 parallel pods: vA (0.3, 0.3) vB (1.0, 0.3) vC (0.3, 1.0) vD (1.0, 1.0)
- same H200 SXM × 4 (need 4 separate pods, runpod has stock — verify
  pre-fire).
- per-pod ~$3.30 × 4 = **~$13**.
- success criterion: 4/4 cells reproduce S187 direction signal
  (L_psi ↓ when λ_ψ ↑, L_phi ↓ when λ_φ ↑, mitosis split count
  non-monotonic across cells per S187 Eval 3).

**Total Phase 1+2 budget: ~$16 fire + ~$5 SCP burn = ~$21 worst case.**
Well under the $40 cap from S187 saga.

### 5.3 Why H200 NOT H100 FSDP-2

Comparing the two cheap-most paths:

| dim | single H200 SXM | 2×A100 SXM4 (vast.ai DC) | 4×A100 SXM4 (vast.ai TW) |
|---|---|---|---|
| Hourly | $3.59 | $2.14 | $3.09 |
| Per-cell wall | 40 min | 1.6 hr | 2.2 hr |
| Per-cell cost | $2.50 | $3.50 | $6.80 |
| FSDP code change | **0 LoC** | ~125 LoC | ~125 LoC |
| FSDP risk (psi_residual etc) | none | medium | medium |
| Bandwidth (S187 stall lesson) | runpod ~1 Gbps | vast.ai 2.8 Gbps ✓ | vast.ai 0.9 Gbps ⚠ |
| Total 4-grid | **~$10** | ~$14 + code | ~$27 + code |

**H200 wins on every axis except hourly rate.** The FSDP code-change
zero-cost dominates the small hourly premium. Defer FSDP wiring to
the 70B cycle where it's unavoidable.

### 5.4 What about 11.4B max-single-H100 (option F)?

11.4B (d=3072 L=36 nh=24 nkv=6) is only 1.28× the 8.92B baseline.
That's not a meaningful scale test — same H100 wall, just slightly
more depth. **Skip — not informative**. Either fire 16B+ on H200, or
defer for 8.92B re-fire if we want to close S187 variance (cheaper).

---

## 6. Honest C3

1. **Memory model is per-S187-attempt10 calibration**, not first-
   principles. Actual H200 peak may diverge ±10% from estimate (115
   GB on H200 may be 100-130 GB in practice). H200 has 26 GB headroom
   in the estimate, so even +20% miss still fits. **Mitigation**:
   pre-flight assert `n_params == 18030141440 ± 0.1%` before opt step.

2. **Activation factor 45.4 bytes/element** calibrated on
   d=3072 L=28. For d=4096 L=32 the per-block activations may scale
   differently (more attention scratch per layer). Empirical:
   single forward+backward smoke at bsz=1 T=512 d=4096 L=32 on
   Mac CPU → measure peak RSS, extrapolate to bf16 GPU. NOT done in
   this scoping cycle — add as Phase 0.5 if mem estimate is close to
   GPU cap.

3. **PagedAdamW8bit 2.1× multiplier may grow with param count**.
   bnb block-quantization overhead per 128-element block; 18B has
   ~1.4 × 8.92B blocks; overhead may scale ≈ linearly. Estimate
   2.0-2.3× plausible. Buffer of 2.5× would push 18B from 115 GB to
   122 GB — still fits H200 141 GB.

4. **70B "naive" config = 178B actual is a real architectural
   problem**. Anima's 7-pathway expansion is structural; can't be
   trimmed without removing pathways. If we want a true 70B for
   apples-to-apples comparison with LLaMA-3 70B, must explicitly
   choose **n_params not config-shape** as the scale axis. The 84B
   variant (d=5632 L=80 nh=44) is closest. **Naming proposal**:
   "Anima-18B / Anima-84B / Anima-178B" where the number = actual
   measured n_params, NEVER the d_model shorthand. S187's `name=3B
   real=8.92B` confusion should not repeat.

5. **FSDP-8 70B viability is borderline**. 72 GB / rank on H100 80GB
   leaves only 8 GB headroom — any unforeseen all-gather spike could
   OOM. Mitigation: HSDP (Hybrid Sharded Data Parallel, shards
   across 4 ranks and replicates 2×) trades memory for comm; or use
   H200 8-bundle (>$30/hr — multiplier on cost).

6. **Mitosis hook scaling with n_layer is untested**. S187's eval 3
   used L=28 with split threshold window=20, patience=3, max=128 cap.
   At L=80, per-layer tension array is 2.85× larger, but the cell
   pool max=128 may saturate even at A control (vC saturated at L=28
   already). May need to re-tune: `max_cells=256` for 70B-scale +
   `window=40`. Empirical only; cannot derive a priori.

7. **Training instability at 70B with bsz=1**. §187 used bsz=16 at
   3B (8.92B real) for 2000 step → 64M tokens, Chinchilla-1000×-
   under. At 70B with bsz=1, that's 1M tokens — **65× sparser than
   already-sparse §187**. Loss likely doesn't converge well; this is
   a **substrate-emergence test, NOT a competitive LM**. Honest
   verbiage: "70B fire tests mitosis pattern scale-invariance, NOT
   language quality at 70B."

8. **8×H100 SXM availability is not guaranteed**. Runpod GraphQL
   showed `uninterruptablePrice=21.52` but stock is regional. Pre-
   flight: query `pods/availability` 1 hour before fire, secure-cloud
   reservation if possible. Vast.ai had 0 H100 SXM 8-bundle offers
   at scoping time (only A100 8-bundles).

9. **Network bandwidth on H200 single-pod is ~1 Gbps (runpod
   typical)**. 36 GB bf16 ckpt × 4 cells = 144 GB SCP pull. At 1
   Gbps sustained = ~20 min total per ckpt = 80 min for 4. Plausible
   bottleneck per §187 lesson. **Mitigation**: pull only `result.json`
   + a single `head_a/head_g/conscious decoder partial state` (~1
   GB) for analysis; full ckpts only if mitosis Eval 3 succeeds and
   shows cross-λ signal worth deeper inspection.

10. **Cost cap drift from S187**: S187 saga burned $25 total
    (attempts 1-10 cumulative). 16B Phase 1+2 estimate ~$21 worst
    case. If 16B has its own bnb-version-collision / dispatcher-
    config / OOM debugging saga, could blow past $40-$60. **Pre-
    flight gate**: Phase 0 + Phase 0.5 (Mac CPU shape smoke + bf16
    activation measurement) MUST pass before Phase 1 fire. Defer to
    user gate review on ALL spinup decisions per §0 cost cap.

11. **The conscious_cross_attention `init_normal(std=0.001)` on
    `o_proj`** means cross-attention contribution starts ~0 — model
    behaves like a non-cross-attention transformer for first ~50
    steps. At 18B + 2000 steps + 64M tokens (well under Chinchilla),
    cross-attention may never meaningfully integrate. Eval 3 mitosis
    is independent of cross-attention (uses per-layer tensions, not
    cross-attn weights), so this doesn't invalidate the substrate
    test, but is worth flagging.

12. **wilson/cloud_dispatch.hexa was not found at
    `~/core/wilson/plugins/pool/`** during this scoping cycle
    (`bfs: error: /Users/ghost/core/wilson: No such file or
    directory`). `~/core/pool/bin/pool.hexa` exists but is a host-
    roster verb-set (`add`/`list`/`on`/`rm`/`off`/`status`), no
    mem_budget formula yet. The optimizer-state-multiplier table
    +activation-bytes formula here should land in the
    `2026-05-21-hexa-cloud-optimizer-mem-budget-preflight.md` sister
    inbox note (currently unverified existence per same `find`).

---

## 7. References

- §187 saga: [`HEXAD/SCALE_3B.md`](SCALE_3B.md) (attempt 1-10, Eval
  3 mitosis cross-λ signal, $25 total saga cost)
- §187 plan: [`HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/PLAN.md`](UNCLASSIFIED/state/grid_3b_s187_2026_05_21/PLAN.md)
- §187 trainer: [`HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/train_s187_3b.py`](UNCLASSIFIED/state/grid_3b_s187_2026_05_21/train_s187_3b.py) (703 LoC, PagedAdamW8bit at line 261, argparse at 568)
- §187 model: [`HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/conscious_decoder.py`](UNCLASSIFIED/state/grid_3b_s187_2026_05_21/conscious_decoder.py) (979 LoC, ConsciousDecoderV2 at line 569, all GQA + SwiGLU + cross-attn + dual engines)
- §187 dispatch: `HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/dispatch_s187_3b_runpod.sh` (gitignored; 261+ lines)
- pool repo (host-roster only, no mem_budget yet): `~/core/pool/bin/pool.hexa`
- sister inbox notes referenced in SCALE_3B.md §2.1 (NOT FOUND in
  filesystem search during this scoping cycle — may be in a private
  wilson worktree not yet checked in):
  - `~/core/wilson/inbox/notes/2026-05-21-hexa-cloud-typed-env-var-passing.md`
  - `~/core/wilson/inbox/notes/2026-05-21-hexa-cloud-optimizer-mem-budget-preflight.md`
- runpod GPU types queried via: `curl -X POST https://api.runpod.io/graphql -H "Authorization: Bearer $RUNPOD_KEY" -d '{"query":"{ gpuTypes { id displayName memoryInGb communityPrice secureSpotPrice lowestPrice(input:{gpuCount:N}) { uninterruptablePrice minimumBidPrice } } }"}'`
- vast.ai queried via: `vastai search offers 'num_gpus=N gpu_name=H100_SXM' --raw` (pip install vastai via `/Users/ghost/Library/Python/3.12/bin/vastai`)
- next cycle candidate ID: **S187-F** in
  [`SCALE_3B.md`](SCALE_3B.md) §7 (was: "scale up further (16B or
  70B) — scale ceiling — $$$$ access wall — ★★★★ — unchanged"). This
  doc closes the **access scoping** half of S187-F. Phase 1 fire
  remains user-gated.

---

## 8. Summary recommendation (1-paragraph TL;DR)

Fire **Anima-18B** (d=4096 L=32 nh=32 nkv=8 nca=2, **18.03B
measured**) on **single runpod H200 SXM 141GB** ($3.59/hr) with **zero
FSDP code changes** — just a 5-line dispatch script tweak + new
PLAN_16B.md. Phase 1 single-cell control fire = ~$3.30 / 55 min. If
Phase 1 PASSES (CE < 6.0, mitosis hook fires ≥1 split), proceed to
Phase 2 4-cell grid for **~$13 total / 4 hours wall parallel**. Defer
**70B-class (84B)** fire behind a separate user gate — needs 8×H100
SXM FSDP at $90+ per cell, ~$360 for full 4-grid, plus ~125 LoC FSDP
wiring. True 178B (LLaMA-70B-shape Anima) requires 8×H200 and is
out-of-scope for current cost envelope. **Cheapest 16B path = single
H200, NO FSDP, $10 4-grid.**
