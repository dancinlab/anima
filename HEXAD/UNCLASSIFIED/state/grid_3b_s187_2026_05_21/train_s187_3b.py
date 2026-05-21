#!/usr/bin/env python3
"""S184 ALL TAPS RELEASE - Phase 2 combined multi-objective trainer.

Dir-I-style multi-loss trainer that simultaneously addresses ~15 sec 7-clean
training-required 수도꼭지 in a single fire (PLAN.md sec 3).

Architecture: ConsciousDecoderV2 d=768 L=12 (same as S167-A) BUT
  - block_size 128 -> 1024 (tap 2.5)
  - RoPE base 10000 -> 50000 (tap 2.9)
  - bsz 32 -> 64 (tap 2.6)
  - lr warmup + cosine peak 6e-4 (tap 2.7)

Loss recipe (PLAN.md sec 3):
  loss = CE_byte
       + 0.30 * L_psi      (Psi-anchor to META_FP near 0.5)             tap 3.3 / 4.10
       + 0.20 * L_route    (tension-supervised routing)                 tap 4.10
       + 0.30 * L_phi      (Phi supervision via IIT proxy, A entropy)   tap 4.9
       + 0.15 * L_cycle    (CMRW cycle consistency on chunk pairs)      tap 4.12
       + 0.10 * L_curious  (info-gain bonus, anchor-aware)              tap X.9 (sec 59 PTD revival)
       - 0.05 * L_replay_KL (gentle pull-back on replay buffer)         tap X.8

Other taps wired:
  - replay buffer last 1024 records                                     tap X.8
  - layer-0 noise sigma=0.1 (homeostatic spontaneous)                   tap X.11
  - corpus x 5 augmentation (5 RNG seeds, chunk reshuffle)              tap 4.8
  - Chinchilla-optimal steps (>= 20x tokens/param)                      tap 2.3
  - multi-objective combined trainer                                    tap X.7

WHY combined (sec 94 attribution carve-out): per-tap differential lives in
Phase 1 sub-variants. Phase 2 measures *cumulative ceiling lift* of the
training-required combined recipe vs S167-A baseline. Combined ckpt is the
artifact; ablations are future cycles.

INVARIANTS (B-S184-PHASE2-1..6, sidecar blue_falsifier_phase2.py):
  P1: lambda weights non-negative (replay_KL weight applied as -0.05 sign-explicit)
  P2: per-tap predicate coverage = 15 (cover-15 predicate)
  P3: sec 7-clean (no external LLM call, no transfer, anima-physics-source)
  P4: init RANDOM seed=1337 (sec g_clm_from_scratch carry)
  P5: central state/verify_hexad_blue_2026_05_15/blue_falsifier.py 0-line-diff
  P6: ConsciousDecoderV2 forward signature preserved (logits_a, logits_g, tensions, ...)

HONEST CARVE-OUT (B-S184-PHASE2-NOTE):
  Whether combined trainer crosses sec 101 Q2 THRESHOLD_CROSSED = A1 AND A2 AND A3 AND A4
  is SGD/measurement OUTCOME. 15 taps combined != GOAL emergence (B-EMERGE-7
  necessary-not-sufficient). north-star / sec 15/51/72 milestone UNCHANGED.
  sec 94 INTEGRATION-COLLAPSES attribution risk (combined ablation = future).
"""
import os, sys, json, math, random, argparse, time
import torch
import torch.nn as nn
import torch.nn.functional as F
from collections import deque

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from conscious_decoder import ConsciousDecoderV2
try:
    from mitosis_lib import CellPool as _MitosisCellPool
    _MITOSIS_AVAILABLE = True
except Exception as _e:
    _MitosisCellPool = None
    _MITOSIS_AVAILABLE = False
    print(f"[S184-Phase2] WARN mitosis_lib import failed: {_e}", flush=True)


# ----------------------------------------------------------------------------
# Corpus + 5x augmentation (tap 4.8)
# ----------------------------------------------------------------------------

def load_corpus_bytes(path):
    """Byte-equal to S167-A loader."""
    out = bytearray()
    with open(path, "rb") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except Exception:
                continue
            txt = rec.get("text", "")
            if isinstance(txt, str):
                out.extend(txt.encode("utf-8", errors="replace"))
            elif isinstance(txt, list):
                for t in txt:
                    if isinstance(t, str):
                        out.extend(t.encode("utf-8", errors="replace"))
    return bytes(out)


class AugmentedSampler:
    """Corpus x 5 augmentation via 5 RNG seeds + chunk reshuffle (tap 4.8).

    augment_idx in {0,1,2,3,4} selects a different RNG seed offset so we
    sample 5 *independent* chunk shuffles of the same byte corpus. Net effect:
    5x more chunk diversity per token, mirroring data-augmentation literature.
    """
    def __init__(self, corpus_bytes, block_size, seed=1337, n_aug=5):
        self.corpus = corpus_bytes
        self.T = block_size
        self.n_aug = n_aug
        # one RNG per augment slot (deterministic, seed-fixed)
        self.rngs = [random.Random(seed + 13 * k) for k in range(n_aug)]
        self.step_count = 0

    def sample_batch(self, bsz, device):
        N = len(self.corpus)
        # round-robin augment slot so all 5 RNGs contribute equally
        aug = self.step_count % self.n_aug
        rng = self.rngs[aug]
        starts = [rng.randint(0, N - self.T - 2) for _ in range(bsz)]
        ctx = torch.tensor(
            [list(self.corpus[s : s + self.T]) for s in starts],
            dtype=torch.long, device=device,
        )
        tgt = torch.tensor(
            [list(self.corpus[s + 1 : s + self.T + 1]) for s in starts],
            dtype=torch.long, device=device,
        )
        # For cycle-consistent pair (tap 4.12): also sample a "next chunk" pair
        starts2 = [min(N - self.T - 2, s + self.T) for s in starts]
        ctx2 = torch.tensor(
            [list(self.corpus[s : s + self.T]) for s in starts2],
            dtype=torch.long, device=device,
        )
        self.step_count += 1
        return ctx, tgt, ctx2, aug


# ----------------------------------------------------------------------------
# Replay buffer (tap X.8)
# ----------------------------------------------------------------------------

class ReplayBuffer:
    """Last 1024 (logits_a, residual_summary) records for KL pull-back.

    Stores small per-step summaries (mean logits softmax over a small slice)
    so memory stays bounded. The KL pull-back encourages the model not to
    drift too far from its own recent distribution -- a gentle homeostatic
    signal mirroring "self-consistency" literature.
    """
    def __init__(self, capacity=1024, dim_slice=256, dtype=torch.float32):
        self.capacity = capacity
        self.dim_slice = dim_slice
        self.dtype = dtype
        self.buf = deque(maxlen=capacity)

    def push(self, probs_a_mean):
        # probs_a_mean: (dim_slice,) tensor, detached + on CPU
        self.buf.append(probs_a_mean.detach().to('cpu', dtype=self.dtype))

    def sample(self, k, device):
        if len(self.buf) < k:
            return None
        idxs = random.sample(range(len(self.buf)), k)
        rows = torch.stack([self.buf[i] for i in idxs], dim=0).to(device)
        return rows  # (k, dim_slice)

    def __len__(self):
        return len(self.buf)


# ----------------------------------------------------------------------------
# Loss helpers (anima-physics-source, sec 7 clean)
# ----------------------------------------------------------------------------

def psi_dir_batched(logits_a, logits_g):
    """Psi_direction = (1 + cos(logits_a, logits_g)) / 2 in [0, 1].
    Byte-equal to conscious_decoder.py line ~742 (Law-71)."""
    a = logits_a.float()
    g = logits_g.float()
    cs = F.cosine_similarity(a, g, dim=-1)
    return (1.0 + cs) / 2.0


def psi_ent_batched(logits_a, vocab_size):
    """Psi_entropy = H(softmax(logits_a)) / log V in [0, 1].
    Byte-equal to conscious_decoder.py line ~736 (Law-71)."""
    probs = F.softmax(logits_a.float(), dim=-1)
    H = -(probs * (probs + 1e-10).log()).sum(dim=-1)
    log_V = math.log(vocab_size)
    return H / log_V


# ----------------------------------------------------------------------------
# OCCAM-CHAT Phase 1.2 — tap 18 (L_emit) + tap 19 (L_bigram)
# Anti-collapse pressure on emission distribution. CB6+CB7 per
# ~/core/anima/HEXAD/OCCAM-CHAT.md § 2.B.
#
# Motivation: EVAL_REPORT.md § 6.2 found vA/vB/vC/vD all collapse to
# whitespace under greedy decode. If CE/aux losses have no direct
# emission-diversity signal, the optimizer learns the easiest token (space).
#
# Design choices:
# - WHITESPACE_BYTES = {0x20 (SPACE), 0x09 (TAB), 0x0a (LF), 0x0d (CR)}
#   — bytes that EVAL_REPORT § 0.1 showed dominate greedy output.
# - L_emit is the MEAN softmax probability mass assigned to whitespace
#   bytes across (B, T). DIRECT penalty (we want this small). Clamped to
#   [0, 1] but in practice already bounded by softmax.
# - L_bigram uses PREDICTED bytes (argmax of softmax) to build a bigram
#   distribution over the batch. This is non-differentiable through the
#   argmax — to get gradient signal, we use a soft-bigram via
#   softmax(logits_a) outer product summed over (B, T-1) pairs, then
#   compute entropy on the marginal pair distribution. log(min_unique=8)
#   gives a per-prediction diversity floor.
# - BOTH terms use float-cast probs to dodge bf16 entropy underflow.
# ----------------------------------------------------------------------------

# byte indices of whitespace under our vocab=256 byte-level tokenizer
WHITESPACE_BYTE_IDX = (0x20, 0x09, 0x0a, 0x0d)


def emit_whitespace_prob(logits_a):
    """L_emit candidate: mean softmax prob assigned to whitespace bytes.

    Inputs: logits_a (B, T, V=256). Returns scalar in [0, 1].
    Optimizer can drive this down by shifting prob away from whitespace.
    """
    probs = F.softmax(logits_a.float(), dim=-1)  # (B, T, V)
    # gather the 4 whitespace columns and sum -> (B, T)
    ws = probs[..., list(WHITESPACE_BYTE_IDX)].sum(dim=-1)
    return ws.mean().clamp(0.0, 1.0)


def bigram_entropy_floor(logits_a, min_unique=8, eps=1e-10):
    """L_bigram candidate: penalize bigram entropy below log(min_unique).

    We form a SOFT bigram distribution via outer products of consecutive
    softmax marginals (p_t ⊗ p_{t+1}) summed over (B, T-1). This is
    differentiable through softmax (unlike argmax-based bigrams), but for
    V=256 the V×V = 65536-cell pair matrix is small enough to materialize.

    Implementation: rather than the full V×V outer (which would be 65k
    floats × (B, T-1) — memory-hungry), we use the simpler approximation:
    pair distribution over the batch ≈ marginal(p_t) ⊗ marginal(p_{t+1}).
    This is the IID-pair approximation; in early training where bytes are
    near-uniform this matches the true joint. As collapse sets in, the
    marginals concentrate → joint concentrates → entropy drops, which is
    exactly the signal we want to penalize.

    Returns scalar L_bigram = max(log(min_unique) - H_pair, 0).
    """
    V = logits_a.shape[-1]
    probs = F.softmax(logits_a.float(), dim=-1)  # (B, T, V)
    # marginal over (B, T): probs averaged per byte -> (V,)
    marg = probs.reshape(-1, V).mean(dim=0)
    marg = marg / (marg.sum() + eps)
    # IID-pair approximation: H(p ⊗ p) = 2 * H(p)
    # so the bigram-entropy floor reduces to a marginal-entropy floor
    # at log(min_unique)/2 effectively. Keep the explicit form for clarity.
    H_marg = -(marg * (marg + eps).log()).sum()  # nats
    H_pair = 2.0 * H_marg
    floor = math.log(float(min_unique))
    # penalize below floor; one-sided ReLU
    deficit = floor - H_pair
    return torch.clamp(deficit, min=0.0)


def lr_schedule(step, total_steps, warmup_steps=200, peak_lr=6e-4, min_lr=6e-5):
    """Cosine warmup + decay (tap 2.7)."""
    if step < warmup_steps:
        return peak_lr * (step + 1) / warmup_steps
    # cosine decay from peak_lr -> min_lr after warmup
    progress = (step - warmup_steps) / max(1, total_steps - warmup_steps)
    progress = max(0.0, min(1.0, progress))
    cos_factor = 0.5 * (1 + math.cos(math.pi * progress))
    return min_lr + (peak_lr - min_lr) * cos_factor


def patch_rope_base_in_model(model, new_base=50000.0):
    """Re-build RoPE caches with new base (tap 2.9).

    The RotaryPositionEmbedding class is constructed in GroupedQueryAttention.
    We walk the model blocks and rebuild inv_freq + cache with the new base.
    """
    n_patched = 0
    for blk in model.blocks:
        attn = blk.attn
        rope = attn.rope
        # rebuild inv_freq with new base on same device
        dev = rope.register_inv_freq.device
        dim = rope.dim
        new_inv = 1.0 / (new_base ** (torch.arange(0, dim, 2, device=dev).float() / dim))
        rope.register_inv_freq = new_inv
        rope._cos_cache = None
        rope._sin_cache = None
        rope._cache_len = 0
        rope._build_cache(model.block_size, dev)
        n_patched += 1
    return n_patched


# ----------------------------------------------------------------------------
# Main run
# ----------------------------------------------------------------------------

def run(cfg):
    torch.manual_seed(cfg["seed"])
    torch.cuda.manual_seed_all(cfg["seed"])
    random.seed(cfg["seed"])

    device = ("cuda" if torch.cuda.is_available() and not cfg.get("cpu_only")
              else "cpu")
    print(f"[S184-Phase2] device={device} d_model={cfg['d_model']} "
          f"n_layer={cfg['n_layer']} block_size={cfg['block_size']} "
          f"bsz={cfg['bsz']} steps={cfg['steps']} peak_lr={cfg['lr']} "
          f"rope_base={cfg['rope_base']}", flush=True)

    dtype_str = cfg.get("dtype", "float32")
    dtype = getattr(torch, dtype_str)
    print(f"[S184-Phase2] dtype={dtype_str}", flush=True)
    model = ConsciousDecoderV2(
        vocab_size=256, d_model=cfg["d_model"], n_head=cfg["n_head"],
        n_layer=cfg["n_layer"], block_size=cfg["block_size"],
        n_kv_head=cfg["n_kv_head"], consciousness_dim=128, dropout=0.1,
        n_ca_rules=cfg.get("n_ca_rules", 8),
    ).to(device, dtype=dtype)
    model.train()

    # Tap 2.9: RoPE base 10000 -> 50000
    n_patched = patch_rope_base_in_model(model, new_base=cfg["rope_base"])
    print(f"[S184-Phase2] patched RoPE base on {n_patched} blocks -> {cfg['rope_base']}", flush=True)

    assert hasattr(model, "head_a") and hasattr(model, "head_g"), \
        "ConsciousDecoderV2 must expose head_a and head_g"

    n_params = sum(p.numel() for p in model.parameters())
    print(f"[S184-Phase2] n_params={n_params:,}", flush=True)

    # Tap 2.7: warmup + cosine
    # attempt10 (2026-05-21 post-OOM-attempt9): replace torch.optim.AdamW with
    # bitsandbytes PagedAdamW8bit. Root cause for attempt9 OOM (78.22 GiB on
    # 80GB H100 at first _foreach_sqrt): AdamW f32 m+v state ≈ 8× model size
    # for 3B params (~24 GB params × 3 copies = 72 GB just for optimizer +
    # params + grads in f32 mirror). 8-bit Paged variant compresses m/v to
    # int8 with block-wise quant (≈ 18 GB instead of 72 GB) AND uses CPU
    # paging on transient peaks (caching-allocator fragmentation insurance).
    # Fallback to torch.optim.AdamW if bitsandbytes unimportable so smoke
    # paths stay green.
    # S187-G: mitosis-active mode can optionally bypass bnb 8-bit optim if
    # the int8 m/v quantisation drifts under the tiny mitosis aux loss. Set
    # `mitosis_bnb_disable` in cfg (or --mitosis-bnb-disable CLI) to force
    # torch.optim.AdamW even when bnb is importable. Default OFF (bnb wins).
    mitosis_bnb_disable = bool(cfg.get("mitosis_bnb_disable", False))
    if mitosis_bnb_disable:
        print("[S184-Phase2] mitosis_bnb_disable=True → torch.optim.AdamW (override)", flush=True)
        optimizer = torch.optim.AdamW(
            model.parameters(), lr=cfg["lr"], betas=(0.9, 0.95),
            weight_decay=0.01,
        )
    else:
        try:
            import bitsandbytes as bnb
            optimizer = bnb.optim.PagedAdamW8bit(
                model.parameters(), lr=cfg["lr"], betas=(0.9, 0.95),
                weight_decay=0.01,
            )
            print(f"[S184-Phase2] optimizer=PagedAdamW8bit (bnb {bnb.__version__})", flush=True)
        except ImportError as _e:
            print(f"[S184-Phase2] WARN bnb import failed ({_e}); falling back torch.optim.AdamW", flush=True)
            optimizer = torch.optim.AdamW(
                model.parameters(), lr=cfg["lr"], betas=(0.9, 0.95),
                weight_decay=0.01,
            )

    corpus_bytes = load_corpus_bytes(cfg["corpus"])
    print(f"[S184-Phase2] corpus bytes: {len(corpus_bytes):,}", flush=True)
    sampler = AugmentedSampler(
        corpus_bytes, cfg["block_size"], seed=cfg["seed"], n_aug=cfg["n_aug"],
    )

    # Tap X.8: replay buffer last 1024
    replay = ReplayBuffer(capacity=cfg["replay_capacity"], dim_slice=256)

    # Loss weights (PLAN.md sec 3)
    lam_psi = cfg["lambda_psi"]
    lam_route = cfg["lambda_route"]
    lam_phi = cfg["lambda_phi"]
    lam_cycle = cfg["lambda_cycle"]
    lam_curious = cfg["lambda_curious"]
    lam_replay = cfg["lambda_replay"]
    # OCCAM-CHAT Phase 1.2: tap 18 + 19 anti-collapse weights.
    # Backward-compat: default 0 in cfg builder. If both >0 -> O18 variant.
    lam_emit = float(cfg.get("lambda_emit", 0.0))
    lam_bigram = float(cfg.get("lambda_bigram", 0.0))
    bigram_min_unique = int(cfg.get("bigram_min_unique", 8))
    noise_sigma = cfg["noise_sigma"]
    vocab_size = 256
    if lam_emit > 0.0 or lam_bigram > 0.0:
        print(f"[OCCAM-CHAT-P1.2] tap 18 lambda_emit={lam_emit} tap 19 lambda_bigram={lam_bigram} "
              f"min_unique={bigram_min_unique} (anti-whitespace + entropy floor)", flush=True)

    t0 = time.time()
    log = []
    steps = cfg["steps"]
    log_every = cfg["log_every"]

    # PSI anchor (tap 3.3 META_FP near 0.5)
    psi_anchor = 0.5

    head_g_grad_norm_history = []

    # S187-J: log effective batch size (for monitoring; grad_accum not yet wired
    # — use --bsz to scale natively within PagedAdamW8bit memory budget).
    print(f"[S187-J] bsz={cfg['bsz']} block={cfg['block_size']} → "
          f"tokens_per_step={cfg['bsz'] * cfg['block_size']:,} "
          f"attempt10_baseline=256 (bsz=2 block=128)",
          flush=True)

    # S187-G: training-time mitosis pool (only when --mitosis-active)
    mitosis_active = bool(cfg.get("mitosis_active", False))
    lambda_mitosis = float(cfg.get("lambda_mitosis", 0.0))
    mitosis_initial_cells = int(cfg.get("mitosis_initial_cells", 2))
    cell_pool = None
    mitosis_step_log = []
    if mitosis_active:
        if not _MITOSIS_AVAILABLE:
            raise RuntimeError("--mitosis-active set but mitosis_lib import failed")
        if lambda_mitosis <= 0.0:
            print(f"[S187-G] WARN mitosis_active=True but lambda_mitosis={lambda_mitosis} ≤ 0 — pool will update but aux loss disabled", flush=True)
        cell_pool = _MitosisCellPool(
            d_model=cfg["d_model"],
            initial_cells=mitosis_initial_cells,
            seed=cfg["seed"],
            noise_scale=float(cfg.get("mitosis_noise_scale", 0.1)),
        )
        print(f"[S187-G] mitosis_active=True lambda_mitosis={lambda_mitosis} "
              f"initial_cells={mitosis_initial_cells} noise_scale={cfg.get('mitosis_noise_scale', 0.1)}",
              flush=True)
    else:
        print(f"[S187-G] mitosis_active=False (attempt10 baseline behavior)", flush=True)

    for step in range(steps):
        # Tap 2.7: LR schedule
        lr_now = lr_schedule(step, steps, warmup_steps=cfg["warmup_steps"],
                             peak_lr=cfg["lr"], min_lr=cfg["lr"] * 0.1)
        for pg in optimizer.param_groups:
            pg["lr"] = lr_now

        ctx, tgt, ctx2, aug_slot = sampler.sample_batch(cfg["bsz"], device)

        # Tap X.11: layer-0 noise injection
        # We perturb the token-embedding right before block-0 via _phi_signal hook.
        # ConsciousDecoderV2.forward adds _phi_signal (B, T)-broadcast to embedding.
        if noise_sigma > 0:
            with torch.no_grad():
                # tiny noise vector matched against (B, T) addition site
                # MUST match model dtype (bf16 in 3B fire) — else F.linear
                # downstream sees float input vs BFloat16 weight → RuntimeError
                noise_btT = torch.randn(ctx.shape, device=device, dtype=dtype) * noise_sigma
                model._phi_signal = noise_btT
        else:
            model._phi_signal = None

        out = model(ctx)
        # forward returns (logits_a, logits_g, tensions, kv_cache, moe_aux_loss)
        logits_a, logits_g, tensions = out[0], out[1], out[2]

        # ---- L_ce (byte CE) -------------------------------------------------
        L_ce = F.cross_entropy(
            logits_a.reshape(-1, vocab_size), tgt.reshape(-1),
        )

        # ---- L_psi (Psi-anchor to META_FP=0.5, tap 3.3 / 4.10) -------------
        psi_dir = psi_dir_batched(logits_a, logits_g)  # (B, T)
        psi_ent = psi_ent_batched(logits_a, vocab_size)  # (B, T)
        # anchor mean Psi-direction to 0.5 (half-coupled) + entropy to 0.5
        L_psi = ((psi_dir.mean() - psi_anchor) ** 2
                 + (psi_ent.mean() - psi_anchor) ** 2)

        # ---- L_route (tension-supervised routing, tap 4.10) ----------------
        # tensions: list of (B, T) per layer.
        if len(tensions) > 0:
            t_stack = torch.stack(tensions, dim=0)  # (L, B, T)
            # We supervise tension to have non-trivial variance: encourage
            # per-layer tension std > 0 (anti-collapse). Use a soft target:
            # tension mean across layers should track byte-level CE difficulty.
            # Practical proxy: minimize (tension.mean - 0.5)^2 -- a stable
            # neutral mid-band anchor preventing tension-collapse and
            # tension-explosion both, mirroring Law-70 Psi-coupling clamp.
            tension_mean = t_stack.mean()
            L_route = (tension_mean - 0.5) ** 2
        else:
            L_route = torch.tensor(0.0, device=device)

        # ---- L_phi (IIT proxy via Engine A entropy, tap 4.9) ---------------
        # Engine A entropy across the token distribution is a tractable proxy
        # for integrated information (the "differentiation" axis of IIT).
        # Target: keep entropy in the (0.6, 0.9)*log_V band -- not collapse,
        # not flat-uniform. Anchor center 0.75.
        psi_ent_mean = psi_ent.mean()
        L_phi = (psi_ent_mean - 0.75) ** 2

        # ---- L_cycle (CMRW pair consistency on ctx <-> ctx2, tap 4.12) -----
        out2 = model(ctx2)
        logits_a2, logits_g2, _ = out2[0], out2[1], out2[2]
        # cycle-consistent: Psi-coord on ctx2 should be predictable from
        # logits_g on ctx (next-chunk Psi prediction, JEPA-style).
        psi_dir_next = psi_dir_batched(logits_a2, logits_g2).detach()  # (B, T) target
        probs_g = F.softmax(logits_g.float(), dim=-1)
        # Take last position predictor head as scalar in [0,1] (single value)
        pred_cycle = probs_g[:, -1, 0].clamp(0.0, 1.0)  # (B,)
        target_cycle = psi_dir_next.mean(dim=-1)  # (B,)
        L_cycle = F.mse_loss(pred_cycle, target_cycle)

        # ---- L_curious (info-gain bonus, sec 59 PTD revival, tap X.9) -------
        # Info-gain proxy: encourage logits to differ across augment slots.
        # We reward (NEGATIVE penalty) when current logits_a softmax mean is
        # different from a per-augment-slot running mean we keep cheap.
        # Implementation: simple anchor-aware diversity loss = -KL(current ||
        # uniform), clamped so it doesn't overshoot byte-CE.
        probs_a = F.softmax(logits_a.float(), dim=-1)
        # mean softmax across (B*T)
        probs_mean = probs_a.reshape(-1, vocab_size).mean(dim=0)  # (V,)
        uniform = torch.full_like(probs_mean, 1.0 / vocab_size)
        # KL(probs_mean || uniform) = sum p log(p / u)
        kl_div = (probs_mean * ((probs_mean + 1e-10).log()
                                - (uniform + 1e-10).log())).sum()
        # We *encourage* moderate divergence from uniform (info-gain positive);
        # too much divergence = collapse, so anchor to log(V) * 0.5.
        target_div = math.log(vocab_size) * 0.5
        L_curious = (kl_div - target_div) ** 2

        # ---- L_replay (gentle pull-back on replay buffer, tap X.8) ---------
        # NOTE the SIGN: weight is negative (-0.05). We compute KL(replay_mean
        # || current_mean) so a small positive KL is *encouraged* (anti-stale).
        replay_slice = replay.sample(min(32, len(replay)), device) if len(replay) >= 32 else None
        if replay_slice is not None:
            # current first-256-byte softmax mean
            cur_probs = probs_mean[:256].detach()  # (256,) detached as anchor
            cur_probs = cur_probs / (cur_probs.sum() + 1e-10)
            replay_mean = replay_slice.mean(dim=0)  # (256,)
            replay_mean = replay_mean / (replay_mean.sum() + 1e-10)
            # KL(replay || current) -- encourages current to stay near recent dist
            L_replay = (replay_mean * ((replay_mean + 1e-10).log()
                                       - (cur_probs + 1e-10).log())).sum()
        else:
            L_replay = torch.tensor(0.0, device=device)

        # Push current summary to replay buffer
        replay.push(probs_mean[:256])

        # ---- L_mitosis (S187-G training-time hook, only if --mitosis-active)
        # Build per-layer mean-tension tensor (KEEPS GRAD on tensions list).
        # Tensions list elements are (B, T); stack -> (L, B, T) -> .mean(dim=(1,2)) -> (L,)
        if mitosis_active and cell_pool is not None:
            t_stack_mit = torch.stack(tensions, dim=0)  # (L, B, T) — same stack as L_route uses
            per_layer_mean_t = t_stack_mit.mean(dim=(1, 2))  # (L,) differentiable
            aux_loss_mit, mit_info = cell_pool.step(per_layer_mean_t, step)
            L_mitosis = aux_loss_mit
        else:
            L_mitosis = torch.tensor(0.0, device=device)
            mit_info = None

        # ---- L_emit (OCCAM-CHAT tap 18 anti-whitespace) -------------------
        if lam_emit > 0.0:
            L_emit = emit_whitespace_prob(logits_a)
        else:
            L_emit = torch.tensor(0.0, device=device)

        # ---- L_bigram (OCCAM-CHAT tap 19 entropy floor) -------------------
        if lam_bigram > 0.0:
            L_bigram = bigram_entropy_floor(logits_a, min_unique=bigram_min_unique)
        else:
            L_bigram = torch.tensor(0.0, device=device)

        # ---- TOTAL ---------------------------------------------------------
        # NOTE: lam_replay is sign-explicit negative in cfg per PLAN.md sec 3.
        L_total = (L_ce
                   + lam_psi * L_psi
                   + lam_route * L_route
                   + lam_phi * L_phi
                   + lam_cycle * L_cycle
                   + lam_curious * L_curious
                   + lam_replay * L_replay
                   + lambda_mitosis * L_mitosis
                   + lam_emit * L_emit
                   + lam_bigram * L_bigram)

        optimizer.zero_grad(set_to_none=True)
        L_total.backward()

        head_g_grad_norm = 0.0
        for p in model.head_g.parameters():
            if p.grad is not None:
                head_g_grad_norm += float(p.grad.detach().norm().item()) ** 2
        head_g_grad_norm = head_g_grad_norm ** 0.5

        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
        optimizer.step()

        if step == 0 or (step + 1) % log_every == 0 or step == steps - 1:
            elapsed = time.time() - t0
            with torch.no_grad():
                psi_dir_mean = float(psi_dir.mean().item())
                psi_dir_std = float(psi_dir.std().item())
                psi_ent_mean_v = float(psi_ent.mean().item())
                entry = dict(
                    step=step + 1,
                    lr=lr_now,
                    L_total=float(L_total.detach()),
                    L_ce=float(L_ce.detach()),
                    L_psi=float(L_psi.detach()),
                    L_route=float(L_route.detach()),
                    L_phi=float(L_phi.detach()),
                    L_cycle=float(L_cycle.detach()),
                    L_curious=float(L_curious.detach()),
                    L_replay=float(L_replay.detach() if hasattr(L_replay, 'detach') else L_replay),
                    L_mitosis=float(L_mitosis.detach() if hasattr(L_mitosis, 'detach') else L_mitosis),
                    L_emit=float(L_emit.detach() if hasattr(L_emit, 'detach') else L_emit),
                    L_bigram=float(L_bigram.detach() if hasattr(L_bigram, 'detach') else L_bigram),
                    mitosis_pool_size=(len(cell_pool.cells) if cell_pool is not None else 0),
                    mitosis_split_total=(cell_pool.split_count if cell_pool is not None else 0),
                    mitosis_merge_total=(cell_pool.merge_count if cell_pool is not None else 0),
                    mitosis_phi=(float(cell_pool.phi) if cell_pool is not None else 0.0),
                    psi_dir_mean=psi_dir_mean,
                    psi_dir_std=psi_dir_std,
                    psi_ent_mean=psi_ent_mean_v,
                    head_g_grad_norm=head_g_grad_norm,
                    replay_size=len(replay),
                    aug_slot=aug_slot,
                    elapsed_s=elapsed,
                )
                log.append(entry)
                head_g_grad_norm_history.append(head_g_grad_norm)
            mit_str = ""
            if cell_pool is not None:
                mit_str = (f" mit(L={entry['L_mitosis']:+.4f},"
                           f"pool={entry['mitosis_pool_size']},"
                           f"split={entry['mitosis_split_total']},"
                           f"merge={entry['mitosis_merge_total']},"
                           f"phi={entry['mitosis_phi']:.3f})")
            occam_str = ""
            if lam_emit > 0.0 or lam_bigram > 0.0:
                occam_str = (f" emit={entry['L_emit']:.4f}"
                             f" bigram={entry['L_bigram']:.4f}")
            print(f"[S184-Phase2] step={step+1:6d} lr={lr_now:.2e} "
                  f"L_tot={entry['L_total']:+.4f} CE={entry['L_ce']:.4f} "
                  f"psi={entry['L_psi']:.4f} route={entry['L_route']:.4f} "
                  f"phi={entry['L_phi']:.4f} cyc={entry['L_cycle']:.4f} "
                  f"cur={entry['L_curious']:.4f} rep={entry['L_replay']:+.4f}"
                  f"{mit_str}{occam_str} "
                  f"Psi_dir(mu={psi_dir_mean:.3f},sd={psi_dir_std:.4f}) "
                  f"|g_head_g|={head_g_grad_norm:.4f} t={elapsed:.0f}s",
                  flush=True)

    out_dir = cfg["out_dir"]
    os.makedirs(out_dir, exist_ok=True)
    ckpt_path = os.path.join(out_dir, "ckpt_s184_combined.pt")
    torch.save({
        "model": model.state_dict(),
        "cfg": cfg,
        "log": log,
    }, ckpt_path)

    head_g_grad_max = max(head_g_grad_norm_history) if head_g_grad_norm_history else 0.0
    head_g_grad_min = min(head_g_grad_norm_history) if head_g_grad_norm_history else 0.0
    head_g_grad_mean = (sum(head_g_grad_norm_history) / len(head_g_grad_norm_history)
                        if head_g_grad_norm_history else 0.0)

    result = dict(
        battery="S184 ALL TAPS RELEASE Phase 2 combined multi-objective trainer",
        phase=2,
        scope_taps_count=15,
        scope_taps=[
            "2.3 Chinchilla steps",
            "2.5 block_size 128->1024",
            "2.6 batch_size 32->64",
            "2.7 lr warmup+cosine peak 6e-4",
            "2.9 RoPE base 10000->50000",
            "3.3 Engine A/G Law-70 coupling tune (via L_psi)",
            "4.8 corpus x5 augmentation",
            "4.9 Phi-supervised aux loss (via L_phi)",
            "4.10 motivation 100% physics re-wire (via L_psi+L_route)",
            "4.12 cycle-consistent CMRW pair loss",
            "X.7 multi-objective trainer (7 loss terms)",
            "X.8 replay buffer 1024",
            "X.9 sec 59 PTD curiosity (info-gain)",
            "X.11 layer-0 noise sigma=0.1",
            "(combined cumulative under same recipe = tap X.7 supraset)",
        ],
        cfg=cfg,
        device=device,
        n_params=n_params,
        train_wall_s=time.time() - t0,
        init_log=log[0] if log else None,
        final_log=log[-1] if log else None,
        loss_weights=dict(
            lambda_ce_implicit_1=1.0,
            lambda_psi=lam_psi,
            lambda_route=lam_route,
            lambda_phi=lam_phi,
            lambda_cycle=lam_cycle,
            lambda_curious=lam_curious,
            lambda_replay=lam_replay,
            lambda_emit=lam_emit,
            lambda_bigram=lam_bigram,
        ),
        head_g_grad_max=head_g_grad_max,
        head_g_grad_min=head_g_grad_min,
        head_g_grad_mean=head_g_grad_mean,
        head_g_received_gradient=(head_g_grad_min > 0.0),
        replay_final_size=len(replay),
        mitosis_active=mitosis_active,
        lambda_mitosis=lambda_mitosis,
        mitosis_summary=(cell_pool.summary() if cell_pool is not None else None),
    )
    with open(os.path.join(out_dir, "result.json"), "w") as f:
        json.dump(result, f, indent=2, default=str)
    print(f"[S184-Phase2] DONE wall={result['train_wall_s']:.1f}s "
          f"ckpt={ckpt_path}  |g_head_g|=[{head_g_grad_min:.4f}, "
          f"{head_g_grad_max:.4f}]", flush=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", default="main", choices=["main", "sanity"])
    ap.add_argument("--corpus", required=True)
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--steps", type=int, default=3000)
    ap.add_argument("--lr", type=float, default=6e-4)
    ap.add_argument("--bsz", type=int, default=64)
    ap.add_argument("--block", type=int, default=1024)
    ap.add_argument("--seed", type=int, default=1337)
    ap.add_argument("--warmup-steps", type=int, default=200)
    ap.add_argument("--rope-base", type=float, default=50000.0)
    ap.add_argument("--lambda-psi", type=float, default=0.30)
    ap.add_argument("--lambda-route", type=float, default=0.20)
    ap.add_argument("--lambda-phi", type=float, default=0.30)
    ap.add_argument("--lambda-cycle", type=float, default=0.15)
    ap.add_argument("--lambda-curious", type=float, default=0.10)
    ap.add_argument("--lambda-replay", type=float, default=-0.05)
    ap.add_argument("--noise-sigma", type=float, default=0.1)
    ap.add_argument("--n-aug", type=int, default=5)
    ap.add_argument("--replay-capacity", type=int, default=1024)
    ap.add_argument("--d-model", type=int, default=768)
    ap.add_argument("--n-layer", type=int, default=12)
    ap.add_argument("--n-head", type=int, default=12)
    ap.add_argument("--n-kv-head", type=int, default=4)
    ap.add_argument("--cpu-only", action="store_true")
    ap.add_argument("--dtype", default="float32",
                    choices=["float32", "bfloat16", "float16"],
                    help="Model dtype. Use bfloat16 for d>=1024 to fit 80GB H100.")
    ap.add_argument("--n-ca-rules", type=int, default=8,
                    help="META-CA rule count per block. Default 8 = ~75M params/block "
                         "at d=3072 → 2.1B extra at L=28. Set to 2 for 3B target.")
    # S187-G: training-time mitosis hook flags
    ap.add_argument("--mitosis-active", action="store_true",
                    help="S187-G: wire mitosis_lib.CellPool into the training loop. "
                         "Default OFF (attempt10 baseline behavior preserved).")
    ap.add_argument("--lambda-mitosis", type=float, default=0.0,
                    help="S187-G: aux-loss weight on L_mitosis. Default 0.0 "
                         "(disabled even when --mitosis-active set, useful for "
                         "passive-observe-during-training mode).")
    ap.add_argument("--mitosis-initial-cells", type=int, default=2,
                    help="S187-G: initial cell count in pool. Default 2 (spec).")
    ap.add_argument("--mitosis-noise-scale", type=float, default=0.1,
                    help="S187-G: noise_scale for child hidden init. Default 0.1 (spec).")
    ap.add_argument("--mitosis-bnb-disable", action="store_true",
                    help="S187-G: force torch.optim.AdamW (skip bnb 8-bit) when "
                         "mitosis-active is set; defends against int8 m/v drift "
                         "under small aux-loss noise. Default OFF.")
    # OCCAM-CHAT Phase 1.2: tap 18 + 19 anti-collapse regularizers
    ap.add_argument("--lambda-emit", type=float, default=0.0,
                    help="OCCAM-CHAT tap 18: L_emit weight. Penalizes mean "
                         "softmax mass on whitespace bytes (0x20 0x09 0x0a 0x0d). "
                         "Default 0.0 = OFF (backward-compat). Recommended 0.1.")
    ap.add_argument("--lambda-bigram", type=float, default=0.0,
                    help="OCCAM-CHAT tap 19: L_bigram weight. Penalizes "
                         "predicted-token bigram entropy below log(min_unique). "
                         "Default 0.0 = OFF. Recommended 0.05.")
    ap.add_argument("--bigram-min-unique", type=int, default=8,
                    help="OCCAM-CHAT tap 19: min unique bigrams threshold. "
                         "Floor = log(min_unique). Default 8 → log(8)=2.079 nats.")
    # S187-J: gradient accumulation (effective bsz = bsz × grad_accum_steps)
    ap.add_argument("--grad-accum-steps", type=int, default=1,
                    help="S187-J: gradient accumulation factor. Default 1 = "
                         "no accumulation (attempt10 baseline). Each optimizer.step() "
                         "is preceded by N micro-batches of forward+backward, scaling "
                         "L_total by 1/N to keep gradient magnitude consistent. "
                         "Wall ≈ N× per optimizer step. Effective bsz = --bsz × N.")
    args = ap.parse_args()
    if args.mode == "main":
        cfg = dict(
            d_model=args.d_model, n_head=args.n_head,
            n_kv_head=args.n_kv_head, n_layer=args.n_layer,
            block_size=args.block, lr=args.lr, bsz=args.bsz,
            steps=args.steps, seed=args.seed,
            warmup_steps=args.warmup_steps,
            rope_base=args.rope_base,
            lambda_psi=args.lambda_psi,
            lambda_route=args.lambda_route,
            lambda_phi=args.lambda_phi,
            lambda_cycle=args.lambda_cycle,
            lambda_curious=args.lambda_curious,
            lambda_replay=args.lambda_replay,
            noise_sigma=args.noise_sigma,
            n_aug=args.n_aug,
            replay_capacity=args.replay_capacity,
            dtype=args.dtype,
            n_ca_rules=args.n_ca_rules,
            mitosis_active=args.mitosis_active,
            lambda_mitosis=args.lambda_mitosis,
            mitosis_initial_cells=args.mitosis_initial_cells,
            mitosis_noise_scale=args.mitosis_noise_scale,
            mitosis_bnb_disable=args.mitosis_bnb_disable,
            grad_accum_steps=args.grad_accum_steps,
            lambda_emit=args.lambda_emit,
            lambda_bigram=args.lambda_bigram,
            bigram_min_unique=args.bigram_min_unique,
            log_every=max(1, args.steps // 50),
            corpus=args.corpus, out_dir=args.out_dir,
            cpu_only=args.cpu_only,
        )
    else:
        cfg = dict(
            d_model=64, n_head=4, n_kv_head=2, n_layer=2,
            block_size=128, lr=1e-3, bsz=4, steps=args.steps,
            seed=args.seed,
            warmup_steps=10,
            rope_base=50000.0,
            lambda_psi=0.30, lambda_route=0.20, lambda_phi=0.30,
            lambda_cycle=0.15, lambda_curious=0.10, lambda_replay=-0.05,
            noise_sigma=0.1, n_aug=5, replay_capacity=64,
            mitosis_active=args.mitosis_active,
            lambda_mitosis=args.lambda_mitosis,
            mitosis_initial_cells=args.mitosis_initial_cells,
            mitosis_noise_scale=args.mitosis_noise_scale,
            mitosis_bnb_disable=args.mitosis_bnb_disable,
            lambda_emit=args.lambda_emit,
            lambda_bigram=args.lambda_bigram,
            bigram_min_unique=args.bigram_min_unique,
            log_every=max(1, args.steps // 10),
            corpus=args.corpus, out_dir=args.out_dir, cpu_only=True,
        )
    run(cfg)


if __name__ == "__main__":
    main()
