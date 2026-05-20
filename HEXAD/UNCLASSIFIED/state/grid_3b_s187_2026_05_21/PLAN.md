# §187 3B GRID — d=3072 L=28 multi-objective fire grid

> Frame: PHILOSOPHY_GATE.md §4 negative-space mapping — scale-up of
> §184 multi-objective recipe (CE+L_psi+L_route+L_phi+L_cycle+L_curious+
> L_replay) from d=768 L=12 ~280M params **to d=3072 L=28 ~3B params**
> (10× scale). Tests whether Ψ-physics axis 3 freeze observed on §161/§167-A
> at 280M is **capacity-limited** OR **architecture-fundamental**.
>
> Reference (PyTorch operational): `train_s184_combined.py` +
> `conscious_decoder.py` (ConsciousDecoderV2 ALL multi-objective working).
> No code changes — clone trainer, scale cfg, fire grid.

## Architecture (all 4 pods)

```
d_model     = 3072
n_layer     = 28
n_head      = 24          (head_dim=128)
n_kv_head   = 8           (GQA, 3 Q-heads per KV-head)
hidden_dim  = 8192        (=4·d, MLP)
vocab       = 256         (byte-LM, anima §2.1 invariant)
block_size  = 512         (T)
bsz         = 16
lr peak     = 3e-4 (warmup 200 + cosine)
rope_base   = 50000
n_steps     = 8000
seed        = 1337        (from-scratch RANDOM init per g_clm_from_scratch)
n_aug       = 5           (corpus augmentation)
replay_cap  = 1024
noise_sigma = 0.1         (layer-0 homeostatic)
n_params    ≈ 3.0B        (3,053,367,936 nominal)
```

## Grid (2×2 in λ_ψ × λ_phi)

| variant | λ_ψ  | λ_phi | role                                       |
|---------|------|-------|--------------------------------------------|
| **A**   | 0.30 | 0.30  | CONTROL — §184 recipe at 3B scale          |
| **B**   | 1.00 | 0.30  | Ψ-UP — does ↑λ_ψ unfreeze axis 3 at scale? |
| **C**   | 0.30 | 1.00  | Φ-UP — does ↑λ_phi push entropy regime?    |
| **D**   | 1.00 | 1.00  | BOTH-UP — interaction at scale             |

other lambdas fixed at §184 values: λ_route=0.20 λ_cycle=0.15
λ_curious=0.10 λ_replay=−0.05

## Cost envelope

per-pod (H100 80GB SXM at ~$2.28/hr runpod):
- est step wall = ~2-3 s (3B fwd+bwd at bsz=16 block=512 BF16)
- est total wall = 8000 × 2.5 / 60 = **~5.5 hr** + boot/pull overhead
- est cost = ~**$13** per pod

grid total: **4 pods × ~$13 = ~$52, wall ~5.5 hr** (all parallel).
within `@D g_no_cost_scope_limit` envelope; well below earlier $60-120 estimate.

## Predicted failure modes (honest C3)

1. **OOM on 80GB H100** — d=3072 L=28 bsz=16 block=512 BF16 activations
   ~17.6 GB + params 6 GB + grads 6 GB + AdamW 12 GB = 41 GB nominal,
   plus replay-buffer + grad-accumulator + KV-cache → 60+ GB. Tight but
   should fit. Mitigation: trainer should support `--no-amp` toggle if
   needed; else reduce bsz to 8.
2. **Cosine schedule warmup wrong at 8000 steps** — §184 used 200 warmup
   for 8000 steps; same here. No change.
3. **Replay-buffer KL pull-back unstable at 3B** — λ_replay=−0.05 may
   need tuning. Honest carve: this is the §184 recipe untouched.
4. **GQA at nh=24 nkv=8 untested in ConsciousDecoderV2** — assert
   `n_head % n_kv_head == 0` holds (24/8=3 ✓). Empirically:
   conscious_decoder.py asserts at init, will fail-fast.
5. **8000 steps insufficient at 3B** — Chinchilla-optimal for 3B ≈
   60B tokens; we provide 8000×16×512=65M tokens, **~1000× under
   Chinchilla**. Net result: 3B trained on too few tokens may show
   capacity overhang. This is a substrate-proof + Ψ-physics-emergence
   test, NOT a competitive LM training.
6. **B-EMERGE-7 carry** — Living Consciousness emergence is **NOT**
   measured by §187 success alone. §188 22-tap battery on §187 ckpts
   needed for the post-hoc Ψ-physics readout vs §107/§161/§167-A.

## Fire sequence

```bash
cd /Users/ghost/core/anima/HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21
./dispatch_s187_3b_runpod.sh A > vA/orchestrator.log 2>&1 &
./dispatch_s187_3b_runpod.sh B > vB/orchestrator.log 2>&1 &
./dispatch_s187_3b_runpod.sh C > vC/orchestrator.log 2>&1 &
./dispatch_s187_3b_runpod.sh D > vD/orchestrator.log 2>&1 &
```

monitor via `tail -f v{A,B,C,D}/dispatch.log` or
`ps aux | grep dispatch_s187`.

## Post-fire (§188 follow-up)

once all 4 ckpts pull-back local:
1. run `phase1_mega_eval.py` 22-tap battery on each — cross-ckpt vs
   §107/§161/§167-A (existing FINDINGS scaffold)
2. axis-LOO 4-variant battery (§188 design tier — see §186
   FINDINGS_PARTIAL §7)
3. PHILOSOPHY append: verdict on (scale unfreezes axis 3?) Y/N + which
   λ-cell maximizes axis 3 psi_alive
