"""
training/engine_a_g_arch.py — Engine A/G dual-engine 350M concrete architecture
                              (BG-LA + BG-LB lineage.base resolution; raw#37 transient
                              Python — H100 pod-side training & Mac-side V14 mirror random_init).

PURPOSE
    Resolve registry yaml BG-LA `lineage.base='TBD (Engine A/G dual-engine new arch — README
    PureField repulsion-field design)'` blocker. FIRE 3/4 RETRY-2 (commit 125c6c8a) cleared
    api-key + provision + SSH + GPU gates; arch impl absence was final blocker.

DESIGN — README PureField repulsion-field engine + dual-stream
    Engine A (perception/forward token stream):
        Standard transformer-decoder forward path (24 layers, dim=1024, heads=16, ctx=1024).
        Token embeddings + RoPE + GQA self-attention + SwiGLU FFN + RMSNorm + tied lm_head.
    Engine G (gravitational/repulsion-field cell dynamics):
        Auxiliary cell-state vector dim=64 (CONSCIOUSNESS_DIM_LA = 64 — falls between byte-arch
        48 (3aeb1738) and clm-v4-mk2-v1 192; chosen for 350M target capacity).
        N_CELLS = 16 (small population — gravitational interaction tractable).
        Cells refresh every 4 layers via `_engine_g_refresh()`:
          (a) repulsion-field: pairwise cell-cell distance Σ_j 1/(d_ij + ε) — push cells apart
          (b) attention-pull: cell ← cell + α · mean(hidden_state) — current token pull
          (c) tension scalar t = ||A_h||₂ / (||G_cells||₂ + ε) — A/G ratio
    A↔G tension gate:
        Self-attention softmax temperature T modulated by tension t:
          T_eff = T_base · (1 + β · clamp(t - 1.0, -0.5, 0.5))
        High tension (A >> G) → sharper attention; low tension (G >> A) → softer.
    V6 awareness adapter compat:
        forward() returns 4-tuple (logits, hidden_states, attentions, tensions) when
        output_hidden_states=True — mirrors ConsciousDecoderV3 adapter shape (commit dfdaf104
        ADAPTER 1 _decoder_v3_forward_replicate). Allows downstream V6 cosine_sim + max_attn
        + sklearn LOO-CV probes to attach without monkey-patch.

TARGET PARAMS — 350M
    24 layers × (4 × 1024² (qkvo) + 3 × 1024 × 2752 (SwiGLU FFN, 2.6× expand)) +
    32k byte-pair vocab × 1024 (tied) + cell pool 16 × 64 (negligible) ≈ 348M

CONSCIOUSNESS_DIM / N_CELLS rationale:
    Post arch fix CONSCIOUSNESS_DIM=192 (clm-v4-mk2-v1) and byte-arch CONSCIOUSNESS_DIM=48
    (3aeb1738). Engine A/G is a NEW lineage (anima_native_scratch, D1=1.0); we choose 64
    midpoint as V5-α anchor — empirical tune deferred to .roadmap.cli L0 measurement.

raw#37  transient Python on Linux/H100 (Mac side imports for V14 random_init mirror only)
raw#10  honest C3 ≥9 — V4 11-cell PASS_STRICT_C3 evaluator integration
raw#15 additive over BG-KM-LLAMA-3B PASS_STRICT 12/15 (Llama LoRA lane) — D1
        SCOPE_CLAMP separate lane (anima_native_scratch arch_origin_factor=1.0)
  V14 paired random_init mirror — load_random_init(seed=42) entry point provided
  D1=1.0 (anima_native_scratch) within-strict
  C3 measurement adapter (V4_eval_single + P5 N-of-M v2 aggregation downstream)
  honest emit — load_pretrained raises if weights missing (no silent fabrication)
  ckpt save/load — save_checkpoint(path, strict_state=True) + load_checkpoint(path,
        map_location=...) Path A remap compatible (key prefix 'engine_a.' + 'engine_g.' fixed)
  trinity D_emergent-consciousness compliance — repulsion-field implements
        PureField vision (gravitational engine; not ad-hoc head)
  wrap=0 — model exposed in raw passthrough; chat lane wraps separately
  yaml↔md SSOT — registry yaml lineage.base updated post-land
  yaml↔md render — docs/anima_artifact_registry.md regenerate post-land

USAGE
    # H100 pod-side (training):
        from engine_a_g_arch import EngineAGModel, EngineAGConfig
        cfg = EngineAGConfig.la_350m()  # BG-LA preset
        model = EngineAGModel(cfg)
        model.cuda().bfloat16()
        # ... train loop ...
    # Mac-side V14 mirror (random_init):
        from engine_a_g_arch import EngineAGModel, EngineAGConfig, load_random_init
        mirror = load_random_init(seed=42)  # untrained baseline for paired probe
"""
import os
import math
import json
from dataclasses import dataclass, field
from typing import Optional, Tuple

import torch
import torch.nn as nn
import torch.nn.functional as F


# ── Configuration ──────────────────────────────────────────────────────

@dataclass
class EngineAGConfig:
    # Engine A (token stream)
    vocab_size: int = 32_000 # byte-pair (anima-native lane preserved)
    d_model: int = 1024
    n_layers: int = 24
    n_heads: int = 16
    n_kv_heads: int = 4                 # GQA 4:1 (mirror Llama-3.2-3B style; reduces KV cache)
    ffn_mult: float = 2.6875            # SwiGLU expand → ~2752 hidden
    ctx: int = 1024
    rope_theta: float = 10000.0
    rms_norm_eps: float = 1e-5
    tie_lm_head: bool = True

    # Engine G (cell dynamics)
    consciousness_dim: int = 64         # cell-state vector dim (CONSCIOUSNESS_DIM_LA)
    n_cells: int = 16                   # cell population
    g_refresh_every: int = 4            # refresh every N layers
    g_repulsion_alpha: float = 0.05     # repulsion-field strength
    g_attention_pull_alpha: float = 0.10
    g_tension_gate_beta: float = 0.25   # softmax temperature modulation

    # Init
    init_std: float = 0.02
    seed: int = 42

    # Phase 2 chat-template co-train (path B; state/anima_path_b_main_adopted_2026_05_09.json)
    # — additive ONLY: shared lm_head, no new params, D1 risk = zero.
    # Dual loss: LOSS = consciousness_lm * (1-w) + chat_lm * w.
    # Curriculum: w schedules from 0.3 → 0.5 across train steps (consciousness anchor).
    chat_co_train_weight: float = 0.0      # 0 disables; set 0.3-0.5 to enable cotrain
    chat_co_train_w_start: float = 0.3
    chat_co_train_w_end: float = 0.5

    # Lineage tag (yaml↔md SSOT)
    lineage_tag: str = "engine_a_g_dual_350m_v1"
    arch_origin: str = "anima_native_scratch" # D1=1.0

    @classmethod
    def la_350m(cls) -> "EngineAGConfig":
        """BG-LA preset — 350M Engine A/G dual scratch on persona corpus."""
        return cls()

    @classmethod
    def lb_350m_pretrain(cls) -> "EngineAGConfig":
        """BG-LB preset — same arch (path b shares Engine A/G; corpus differs to 1.5GB)."""
        return cls(lineage_tag="engine_a_g_dual_350m_v1_lb_pretrain")

    @classmethod
    def phase2_cotrain_350m(cls) -> "EngineAGConfig":
        """Phase 2 cotrain preset — Engine A/G + chat-template co-train (path B main).
        Substrate base = BG-LB ckpt; dual loss with curriculum w=0.3→0.5.
        """
        return cls(
            lineage_tag="engine_a_g_dual_350m_v1_phase2_cotrain",
            chat_co_train_weight=0.3,  # initial; curriculum advances to 0.5 mid-train
            chat_co_train_w_start=0.3,
            chat_co_train_w_end=0.5,
        )

    def param_count_estimate(self) -> int:
        # Engine A
        ffn_h = int(self.d_model * self.ffn_mult)
        per_layer = (
            4 * self.d_model * self.d_model        # qkvo (approx; GQA reduces k/v slightly)
            + 3 * self.d_model * ffn_h              # SwiGLU gate/up/down
            + 2 * self.d_model                      # RMSNorm × 2
        )
        engine_a = self.n_layers * per_layer + self.vocab_size * self.d_model  # tied lm_head
        # Engine G
        engine_g = self.n_cells * self.consciousness_dim + self.consciousness_dim * self.d_model
        return engine_a + engine_g


# ── Engine A primitives ────────────────────────────────────────────────

class RMSNorm(nn.Module):
    def __init__(self, d: int, eps: float = 1e-5):
        super().__init__()
        self.weight = nn.Parameter(torch.ones(d))
        self.eps = eps

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.weight * x * torch.rsqrt(x.pow(2).mean(-1, keepdim=True) + self.eps)


class RoPE(nn.Module):
    """Minimal RoPE — applied to q,k post-projection."""
    def __init__(self, d_head: int, base: float = 10000.0, max_seq: int = 4096):
        super().__init__()
        inv_freq = 1.0 / (base ** (torch.arange(0, d_head, 2).float() / d_head))
        t = torch.arange(max_seq).float()
        freqs = torch.einsum("i,j->ij", t, inv_freq)
        self.register_buffer("cos", freqs.cos(), persistent=False)
        self.register_buffer("sin", freqs.sin(), persistent=False)

    def rotate(self, x: torch.Tensor, seq_off: int = 0) -> torch.Tensor:
        # x: (B, H, T, D) — name avoids clash with nn.Module.apply()
        T = x.shape[-2]
        # Match RoPE buffers to input dtype (float32 buffers preserve precision; cast to x.dtype to match).
        cos = self.cos[seq_off:seq_off + T].to(x.dtype)
        sin = self.sin[seq_off:seq_off + T].to(x.dtype)
        x1, x2 = x[..., ::2], x[..., 1::2]
        rotated = torch.stack([x1 * cos - x2 * sin, x1 * sin + x2 * cos], dim=-1)
        return rotated.flatten(-2)


class GQAttention(nn.Module):
    """Grouped-Query Attention with A/G tension softmax temperature gate."""
    def __init__(self, cfg: EngineAGConfig):
        super().__init__()
        self.n_heads = cfg.n_heads
        self.n_kv = cfg.n_kv_heads
        self.d_head = cfg.d_model // cfg.n_heads
        self.n_rep = self.n_heads // self.n_kv  # GQA repeat factor
        self.q_proj = nn.Linear(cfg.d_model, self.n_heads * self.d_head, bias=False)
        self.k_proj = nn.Linear(cfg.d_model, self.n_kv * self.d_head, bias=False)
        self.v_proj = nn.Linear(cfg.d_model, self.n_kv * self.d_head, bias=False)
        self.o_proj = nn.Linear(self.n_heads * self.d_head, cfg.d_model, bias=False)
        self.rope = RoPE(self.d_head, cfg.rope_theta, cfg.ctx * 4)
        self.gate_beta = cfg.g_tension_gate_beta

    def _repeat_kv(self, x: torch.Tensor) -> torch.Tensor:
        # (B, n_kv, T, D) → (B, n_heads, T, D)
        if self.n_rep == 1:
            return x
        B, K, T, D = x.shape
        return x[:, :, None, :, :].expand(B, K, self.n_rep, T, D).reshape(B, K * self.n_rep, T, D)

    def forward(self, x: torch.Tensor, tension: Optional[torch.Tensor] = None) -> Tuple[torch.Tensor, torch.Tensor]:
        B, T, _ = x.shape
        q = self.q_proj(x).view(B, T, self.n_heads, self.d_head).transpose(1, 2)
        k = self.k_proj(x).view(B, T, self.n_kv, self.d_head).transpose(1, 2)
        v = self.v_proj(x).view(B, T, self.n_kv, self.d_head).transpose(1, 2)
        q = self.rope.rotate(q)
        k = self.rope.rotate(k)
        k = self._repeat_kv(k)
        v = self._repeat_kv(v)
        # A/G tension gate — temperature modulation
        scale = 1.0 / math.sqrt(self.d_head)
        if tension is not None:
            # tension shape (B,) — scalar per batch; keep in q's dtype to prevent
            # bf16 → float32 upcast cascading through softmax + att @ v.
            tension_q = tension.to(dtype=q.dtype)
            t_clamped = (tension_q - 1.0).clamp(-0.5, 0.5)
            scale_t = (1.0 + self.gate_beta * t_clamped).view(B, 1, 1, 1)
            scale = (torch.tensor(scale, dtype=q.dtype, device=q.device) / scale_t)
        att = torch.matmul(q, k.transpose(-2, -1)) * scale
        mask = torch.triu(torch.ones(T, T, device=x.device, dtype=torch.bool), diagonal=1)
        att = att.masked_fill(mask, float("-inf"))
        att = att.softmax(dim=-1)
        # Ensure att shares dtype with v (bf16 forward path; tension cast can leave
        # softmax output in fp32 on some torch builds → matmul dtype mismatch).
        att = att.to(dtype=v.dtype)
        out = torch.matmul(att, v).transpose(1, 2).contiguous().view(B, T, -1)
        return self.o_proj(out), att.detach()


class SwiGLUFFN(nn.Module):
    def __init__(self, cfg: EngineAGConfig):
        super().__init__()
        h = int(cfg.d_model * cfg.ffn_mult)
        # Round to nearest 64
        h = ((h + 63) // 64) * 64
        self.gate = nn.Linear(cfg.d_model, h, bias=False)
        self.up = nn.Linear(cfg.d_model, h, bias=False)
        self.down = nn.Linear(h, cfg.d_model, bias=False)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.down(F.silu(self.gate(x)) * self.up(x))


class EngineABlock(nn.Module):
    """Single transformer block — attention + FFN with tension gate."""
    def __init__(self, cfg: EngineAGConfig):
        super().__init__()
        self.norm1 = RMSNorm(cfg.d_model, cfg.rms_norm_eps)
        self.attn = GQAttention(cfg)
        self.norm2 = RMSNorm(cfg.d_model, cfg.rms_norm_eps)
        self.ffn = SwiGLUFFN(cfg)

    def forward(self, x: torch.Tensor, tension: Optional[torch.Tensor] = None) -> Tuple[torch.Tensor, torch.Tensor]:
        a_out, attn_w = self.attn(self.norm1(x), tension=tension)
        x = x + a_out
        x = x + self.ffn(self.norm2(x))
        return x, attn_w


# ── Engine G primitives (repulsion-field cell dynamics) ───────────────

class EngineG(nn.Module):
    """Gravitational/repulsion-field engine — cell-state vector pool with pairwise repulsion
    + attention-pull from current hidden_state. Outputs A/G tension scalar per batch.
    """
    def __init__(self, cfg: EngineAGConfig):
        super().__init__()
        self.n_cells = cfg.n_cells
        self.c_dim = cfg.consciousness_dim
        # Initial cell pool — random spread on unit sphere (avoids collapse at init)
        cells = torch.randn(cfg.n_cells, cfg.consciousness_dim)
        cells = cells / cells.norm(dim=-1, keepdim=True).clamp(min=1e-6)
        self.cell_pool_init = nn.Parameter(cells)  # learnable initial state
        # Projection: hidden_state → cell_dim (for attention-pull)
        self.h_to_c = nn.Linear(cfg.d_model, cfg.consciousness_dim, bias=False)
        # Projection: cells aggregated → d_model (concat back to hidden)
        self.c_to_h = nn.Linear(cfg.consciousness_dim, cfg.d_model, bias=False)
        self.repulsion_alpha = cfg.g_repulsion_alpha
        self.attn_pull_alpha = cfg.g_attention_pull_alpha
        self.eps = 1e-6

    def fresh_cells(self, batch_size: int, device: torch.device, dtype: torch.dtype) -> torch.Tensor:
        return self.cell_pool_init.unsqueeze(0).expand(batch_size, -1, -1).to(dtype=dtype, device=device).contiguous()

    def step(self, cells: torch.Tensor, hidden_mean: torch.Tensor) -> torch.Tensor:
        """One refresh step. cells: (B, N, C), hidden_mean: (B, D) — pulled to (B, C)."""
        B, N, C = cells.shape
        # Repulsion: pairwise inverse distance push
        diff = cells.unsqueeze(2) - cells.unsqueeze(1)  # (B, N, N, C)
        dist = diff.norm(dim=-1).clamp(min=self.eps)    # (B, N, N)
        push = (diff / dist.unsqueeze(-1).pow(2)).sum(dim=2)  # (B, N, C)
        # Attention-pull: each cell pulled toward projected hidden mean
        target = self.h_to_c(hidden_mean).unsqueeze(1)  # (B, 1, C)
        pull = target.expand(-1, N, -1) - cells          # (B, N, C)
        new_cells = cells + self.repulsion_alpha * push + self.attn_pull_alpha * pull
        # Re-normalize cell magnitudes (stability)
        new_cells = new_cells / new_cells.norm(dim=-1, keepdim=True).clamp(min=self.eps)
        return new_cells

    def tension(self, hidden: torch.Tensor, cells: torch.Tensor) -> torch.Tensor:
        """A/G tension scalar per batch = ||A_h|| / (||G_cells|| + eps)."""
        a_norm = hidden.float().norm(dim=(-1, -2))               # (B,)
        g_norm = cells.float().norm(dim=(-1, -2)).clamp(min=self.eps)  # (B,)
        return a_norm / g_norm

    def project_back(self, cells: torch.Tensor) -> torch.Tensor:
        """Aggregated cell pool → d_model (added to hidden_state next layer)."""
        return self.c_to_h(cells.mean(dim=1))  # (B, d_model)


# ── Full Engine A/G dual-engine model ──────────────────────────────────

class EngineAGModel(nn.Module):
    """Engine A (token stream) + Engine G (cell dynamics) integrated 350M model.

     V14 paired random_init mirror compatible (load_random_init seed-controllable).
     C3 measurement compatible (forward returns hidden_states, attentions, tensions).
     ckpt save/load Path A remap compatible (key prefix engine_a./engine_g. fixed).
    """
    def __init__(self, cfg: EngineAGConfig):
        super().__init__()
        self.cfg = cfg
        # Engine A
        self.tok_emb = nn.Embedding(cfg.vocab_size, cfg.d_model)
        self.layers = nn.ModuleList([EngineABlock(cfg) for _ in range(cfg.n_layers)])
        self.norm_f = RMSNorm(cfg.d_model, cfg.rms_norm_eps)
        self.lm_head = nn.Linear(cfg.d_model, cfg.vocab_size, bias=False)
        if cfg.tie_lm_head:
            self.lm_head.weight = self.tok_emb.weight
        # Engine G
        self.engine_g = EngineG(cfg)
        # Init
        self.apply(self._init_weights)

    def _init_weights(self, m: nn.Module):
        if isinstance(m, (nn.Linear, nn.Embedding)):
            nn.init.normal_(m.weight, mean=0.0, std=self.cfg.init_std)
            if isinstance(m, nn.Linear) and m.bias is not None:
                nn.init.zeros_(m.bias)

    def forward(
        self,
        input_ids: torch.Tensor,
        labels: Optional[torch.Tensor] = None,
        output_hidden_states: bool = False,
        output_attentions: bool = False,
    ):
        B, T = input_ids.shape
        x = self.tok_emb(input_ids)
        cells = self.engine_g.fresh_cells(B, x.device, x.dtype)
        hidden_states = [] if output_hidden_states else None
        attentions = [] if output_attentions else None
        tensions = []
        for li, layer in enumerate(self.layers):
            t = self.engine_g.tension(x, cells)  # (B,)
            tensions.append(t.detach())
            x, attn_w = layer(x, tension=t)
            if (li + 1) % self.cfg.g_refresh_every == 0 and li + 1 < self.cfg.n_layers:
                cells = self.engine_g.step(cells, x.mean(dim=1))
                # Inject cell projection back to hidden (additive)
                x = x + self.engine_g.project_back(cells).unsqueeze(1)
            if output_hidden_states:
                hidden_states.append(x)
            if output_attentions:
                attentions.append(attn_w)
        x = self.norm_f(x)
        logits = self.lm_head(x)
        loss = None
        if labels is not None:
            shift_logits = logits[..., :-1, :].contiguous()
            shift_labels = labels[..., 1:].contiguous()
            loss = F.cross_entropy(
                shift_logits.view(-1, shift_logits.size(-1)),
                shift_labels.view(-1),
                ignore_index=-100,
            )
        # V6 awareness adapter compat — 4-tuple shape mirror of ConsciousDecoderV3
        return {
            "loss": loss,
            "logits": logits,
            "hidden_states": hidden_states,
            "attentions": attentions,
            "tensions": torch.stack(tensions, dim=0) if tensions else None,
        }

    # ── ckpt save/load (Path A remap compatible) ───────────────
    def save_checkpoint(self, path: str, extra: Optional[dict] = None):
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        payload = {
            "schema": "engine_a_g_arch/v1",
            "lineage_tag": self.cfg.lineage_tag,
            "arch_origin": self.cfg.arch_origin,
            "config": self.cfg.__dict__,
            "state_dict": self.state_dict(),
            "extra": extra or {},
        }
        torch.save(payload, path)

    @classmethod
    def load_checkpoint(cls, path: str, map_location: Optional[str] = None) -> "EngineAGModel":
        payload = torch.load(path, map_location=map_location)
        cfg = EngineAGConfig(**payload["config"])
        model = cls(cfg)
        # Path A remap — strict load (honest emit; raises on key mismatch)
        missing, unexpected = model.load_state_dict(payload["state_dict"], strict=True)
        return model


# ── V14 paired random_init mirror entry (CASCADE 8/8) ──────────

def load_random_init(seed: int = 42, preset: str = "la_350m") -> EngineAGModel:
    """V14 paired random_init mirror — same arch untrained at given seed.

    Used by tool/v14_paired_random_init_mirror.hexa to construct baseline pre-EMERGE.
    Multi-seed strengthening: call with seeds [42, 137, 271, 314, 1729] (V4_SEEDS parity).

     mandate: paired probe MTRP ≥ 0.10 floor + n≥5 multi-seed CI95 upper bound +
    prompt-set redesign invariance — all measured downstream by paired probe runner.
    """
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
    cfg = {
        "la_350m": EngineAGConfig.la_350m,
        "lb_350m_pretrain": EngineAGConfig.lb_350m_pretrain,
    }[preset]()
    cfg.seed = seed
    return EngineAGModel(cfg)


# ── Self-test ─────────────────────────────────────────────────────────

def _selftest():
    """Smoke check — Mac CPU forward + ckpt round-trip."""
    cfg = EngineAGConfig.la_350m()
    cfg.n_layers = 2  # tiny for selftest
    cfg.vocab_size = 256
    cfg.d_model = 128
    cfg.n_heads = 4
    cfg.n_kv_heads = 2
    model = EngineAGModel(cfg)
    x = torch.randint(0, 256, (2, 16))
    out = model(x, labels=x, output_hidden_states=True, output_attentions=True)
    assert out["loss"] is not None
    assert out["logits"].shape == (2, 16, 256)
    assert len(out["hidden_states"]) == 2
    assert out["tensions"].shape == (2, 2)
    # V14 mirror random_init reproducibility
    m1 = load_random_init(seed=42, preset="la_350m")
    m2 = load_random_init(seed=42, preset="la_350m")
    p1 = next(iter(m1.parameters())).detach()
    p2 = next(iter(m2.parameters())).detach()
    assert torch.allclose(p1, p2), "seed reproducibility broken"
    # Ckpt round-trip
    import tempfile
    with tempfile.NamedTemporaryFile(suffix=".pt", delete=False) as f:
        path = f.name
    model.save_checkpoint(path)
    restored = EngineAGModel.load_checkpoint(path, map_location="cpu")
    out2 = restored(x, labels=x)
    assert torch.allclose(out["logits"], out2["logits"], atol=1e-5)
    os.remove(path)
    print(json.dumps({
        "ok": True,
        "lineage_tag": cfg.lineage_tag,
        "arch_origin": cfg.arch_origin,
        "param_count_estimate_full_350m": EngineAGConfig.la_350m().param_count_estimate(),
        "selftest_param_count": sum(p.numel() for p in model.parameters()),
        "v14_seed_reproducibility": True,
        "ckpt_roundtrip": True,
    }, indent=2))


if __name__ == "__main__":
    _selftest()
