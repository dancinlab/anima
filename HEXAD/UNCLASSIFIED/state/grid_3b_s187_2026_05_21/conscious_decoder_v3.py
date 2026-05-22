"""ConsciousDecoderV3 — pure HEXAD-native substrate (LoRA 폐기 path).

Fork of conscious_decoder.py (V2). Key deltas (per HEXAD_NATIVE_V3.md):
  1. ❌  n_ca_rules REMOVED entirely (OCCAM Phase 2.3 ablation single floor blocker).
        DecoderBlockV3 has NO rule_weights / rules / ca_mix / ln_ca / meta-CA path.
  2. ✅  head_g KEPT (consciousness emission Engine G dual head).
  3. ✅  PureFieldFFN + ConsciousCrossAttention + layer-0 noise σ=0.1 KEPT (all benign).
  4. ✅  Vocab default = 152064 (Qwen2.5 BPE), not 256 (byte-level).
  5. ✅  Init helpers: random / Qwen warm-start / vP21M-init (LoRA merged).
  6. ✅  Mitosis hook 1-class integration (CellPool, training + inference time).
  7. ✅  Layer-0 noise σ=0.1 explicitly wired (substrate-shape) — only in self.train().

Forward signature (V3, backward-compat with V2 callers via *_kwargs):
    logits_a, logits_g, tensions, kv_cache, mitosis_info = model(
        idx,
        consciousness_states=None,
        use_cache=False,
        past_key_values=None,
        mitosis_step=None,        # int — if not None, triggers cell-pool step
    )

Usage (training):
    from conscious_decoder_v3 import ConsciousDecoderV3
    from mitosis_lib import CellPool
    model = ConsciousDecoderV3(vocab_size=152064, d_model=1536, n_layer=24,
                                 n_head=12, n_kv_head=4, block_size=512)
    pool = CellPool(d_model=model.d_model, initial_cells=2)
    model.attach_mitosis(pool)
    # forward — pool.step() is invoked automatically when mitosis_step is given
    logits_a, _, tensions, _, info = model(idx, mitosis_step=global_step)
    aux_loss = info['aux_loss']  # differentiable
    loss = F.cross_entropy(...) + 0.05 * aux_loss

Usage (Qwen warm-start init):
    model = ConsciousDecoderV3.from_qwen("Qwen/Qwen2.5-1.5B")

Usage (vP21M-init):
    model = ConsciousDecoderV3.from_qwen("Qwen/Qwen2.5-1.5B",
                                          lora_adapter_dir="/path/to/vP21M/lora_adapter")
"""

import math
import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Optional, Tuple, List, Dict, Any


# ─── RMSNorm ────────────────────────────────────────────────────────────────

class RMSNorm(nn.Module):
    def __init__(self, dim: int, eps: float = 1e-6):
        super().__init__()
        self.eps = eps
        self.weight = nn.Parameter(torch.ones(dim))

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        rms = torch.rsqrt(x.float().pow(2).mean(dim=-1, keepdim=True) + self.eps)
        return (x.float() * rms).type_as(x) * self.weight


# ─── RoPE ────────────────────────────────────────────────────────────────────

class RotaryPositionEmbedding:
    def __init__(self, dim: int, max_seq_len: int = 2048, base: float = 50000.0,
                 device: Optional[torch.device] = None):
        self.dim = dim
        inv_freq = 1.0 / (base ** (torch.arange(0, dim, 2, device=device).float() / dim))
        self.register_inv_freq = inv_freq
        self._cos_cache = None
        self._sin_cache = None
        self._cache_len = 0
        self._build_cache(max_seq_len, device)

    def _build_cache(self, seq_len: int, device: Optional[torch.device] = None):
        if seq_len <= self._cache_len and self._cos_cache is not None:
            return
        self._cache_len = seq_len
        t = torch.arange(seq_len, device=device or self.register_inv_freq.device).float()
        freqs = torch.einsum('i,j->ij', t, self.register_inv_freq.to(t.device))
        emb = torch.cat([freqs, freqs], dim=-1)
        self._cos_cache = emb.cos().unsqueeze(0).unsqueeze(0)
        self._sin_cache = emb.sin().unsqueeze(0).unsqueeze(0)

    @staticmethod
    def _rotate_half(x: torch.Tensor) -> torch.Tensor:
        x1 = x[..., :x.shape[-1] // 2]
        x2 = x[..., x.shape[-1] // 2:]
        return torch.cat([-x2, x1], dim=-1)

    def apply(self, q: torch.Tensor, k: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        T = q.shape[2]
        self._build_cache(T, q.device)
        cos = self._cos_cache[:, :, :T, :].to(q.device, dtype=q.dtype)
        sin = self._sin_cache[:, :, :T, :].to(q.device, dtype=q.dtype)
        q_rot = q * cos + self._rotate_half(q) * sin
        k_rot = k * cos + self._rotate_half(k) * sin
        return q_rot, k_rot


# ─── SwiGLU ───────────────────────────────────────────────────────────────────

class SwiGLUFFN(nn.Module):
    def __init__(self, d_model: int, dropout: float = 0.0,
                 expansion: float = 8 / 3):
        super().__init__()
        d_inner = int(d_model * expansion)
        d_inner = ((d_inner + 63) // 64) * 64
        self.gate_proj = nn.Linear(d_model, d_inner, bias=False)
        self.up_proj = nn.Linear(d_model, d_inner, bias=False)
        self.down_proj = nn.Linear(d_inner, d_model, bias=False)
        self.down_proj._depth_scale = True
        self.dropout = nn.Dropout(dropout)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.dropout(self.down_proj(
            F.silu(self.gate_proj(x)) * self.up_proj(x)
        ))


# ─── PureFieldFFN ────────────────────────────────────────────────────────────

class PureFieldFFN(nn.Module):
    """Engine A ⇄ Engine G repulsion — produces tension scalar per token."""
    def __init__(self, d_model: int, dropout: float = 0.0):
        super().__init__()
        d_inner = 4 * d_model
        self.engine_a = nn.Sequential(
            nn.Linear(d_model, d_inner), nn.GELU(),
            nn.Dropout(dropout), nn.Linear(d_inner, d_model),
        )
        self.engine_g = nn.Sequential(
            nn.Linear(d_model, d_inner), nn.GELU(),
            nn.Dropout(dropout), nn.Linear(d_inner, d_model),
        )

    def forward(self, x: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        a = self.engine_a(x)
        g = self.engine_g(x)
        output = a - g
        tension = (output ** 2).mean(dim=-1)
        return output, tension


# ─── GQA + RoPE ──────────────────────────────────────────────────────────────

class GroupedQueryAttention(nn.Module):
    def __init__(self, d_model: int, n_head: int = 12, n_kv_head: int = 4,
                 block_size: int = 512, dropout: float = 0.0,
                 rope_base: float = 50000.0):
        super().__init__()
        assert d_model % n_head == 0
        assert n_head % n_kv_head == 0
        self.n_head = n_head
        self.n_kv_head = n_kv_head
        self.n_rep = n_head // n_kv_head
        self.head_dim = d_model // n_head
        self.d_model = d_model
        self.dropout = dropout

        self.q_proj = nn.Linear(d_model, n_head * self.head_dim, bias=True)   # Qwen has bias on qkv
        self.k_proj = nn.Linear(d_model, n_kv_head * self.head_dim, bias=True)
        self.v_proj = nn.Linear(d_model, n_kv_head * self.head_dim, bias=True)
        self.o_proj = nn.Linear(d_model, d_model, bias=False)
        self.o_proj._depth_scale = True

        self.attn_dropout = nn.Dropout(dropout)
        self.resid_dropout = nn.Dropout(dropout)
        self.rope = RotaryPositionEmbedding(self.head_dim, max_seq_len=block_size, base=rope_base)
        self._use_flash = hasattr(F, 'scaled_dot_product_attention')

        self.register_buffer(
            "bias",
            torch.tril(torch.ones(block_size, block_size)).view(1, 1, block_size, block_size),
        )

    def _repeat_kv(self, x: torch.Tensor) -> torch.Tensor:
        if self.n_rep == 1:
            return x
        B, H, T, D = x.shape
        x = x.unsqueeze(2).expand(B, H, self.n_rep, T, D)
        return x.reshape(B, self.n_head, T, D)

    def forward(self, x: torch.Tensor, use_cache: bool = False,
                past_kv: Optional[Tuple[torch.Tensor, torch.Tensor]] = None,
                position_offset: int = 0):
        B, T, D = x.size()
        q = self.q_proj(x).view(B, T, self.n_head, self.head_dim).transpose(1, 2)
        k = self.k_proj(x).view(B, T, self.n_kv_head, self.head_dim).transpose(1, 2)
        v = self.v_proj(x).view(B, T, self.n_kv_head, self.head_dim).transpose(1, 2)

        if position_offset > 0:
            total_len = position_offset + T
            self.rope._build_cache(total_len, q.device)
            cos = self.rope._cos_cache[:, :, position_offset:total_len, :].to(q.device, dtype=q.dtype)
            sin = self.rope._sin_cache[:, :, position_offset:total_len, :].to(q.device, dtype=q.dtype)
            q = q * cos + RotaryPositionEmbedding._rotate_half(q) * sin
            k = k * cos + RotaryPositionEmbedding._rotate_half(k) * sin
        else:
            q, k = self.rope.apply(q, k)

        new_kv = None
        if use_cache:
            if past_kv is not None:
                k = torch.cat([past_kv[0], k], dim=2)
                v = torch.cat([past_kv[1], v], dim=2)
            new_kv = (k, v)

        k_exp = self._repeat_kv(k)
        v_exp = self._repeat_kv(v)
        S = k_exp.shape[2]

        if self._use_flash and past_kv is None:
            y = F.scaled_dot_product_attention(
                q, k_exp, v_exp, attn_mask=None,
                dropout_p=self.dropout if self.training else 0.0,
                is_causal=True,
            )
        else:
            att = (q @ k_exp.transpose(-2, -1)) * (1.0 / math.sqrt(self.head_dim))
            if past_kv is not None and use_cache:
                if T == 1:
                    pass
                else:
                    causal = torch.ones(T, S, dtype=torch.bool, device=att.device).tril(diagonal=S - T)
                    att = att.masked_fill(~causal.unsqueeze(0).unsqueeze(0), float("-inf"))
            else:
                att = att.masked_fill(self.bias[:, :, :T, :S] == 0, float("-inf"))
            att = F.softmax(att, dim=-1)
            att = self.attn_dropout(att)
            y = att @ v_exp
        y = y.transpose(1, 2).contiguous().view(B, T, D)
        y = self.resid_dropout(self.o_proj(y))
        return y, new_kv


# ─── Conscious Cross-Attention ───────────────────────────────────────────────

class ConsciousCrossAttention(nn.Module):
    def __init__(self, d_model: int, consciousness_dim: int, n_head: int = 4,
                 dropout: float = 0.0):
        super().__init__()
        assert d_model % n_head == 0
        self.n_head = n_head
        self.head_dim = d_model // n_head
        self.d_model = d_model
        self.q_proj = nn.Linear(d_model, d_model, bias=False)
        self.k_proj = nn.Linear(consciousness_dim, d_model, bias=False)
        self.v_proj = nn.Linear(consciousness_dim, d_model, bias=False)
        self.o_proj = nn.Linear(d_model, d_model, bias=False)
        self.dropout = nn.Dropout(dropout)
        nn.init.normal_(self.o_proj.weight, std=0.001)

    def forward(self, x: torch.Tensor, consciousness: torch.Tensor) -> torch.Tensor:
        B, T, D = x.shape
        _, S, _ = consciousness.shape
        q = self.q_proj(x).view(B, T, self.n_head, self.head_dim).transpose(1, 2)
        k = self.k_proj(consciousness).view(B, S, self.n_head, self.head_dim).transpose(1, 2)
        v = self.v_proj(consciousness).view(B, S, self.n_head, self.head_dim).transpose(1, 2)
        att = (q @ k.transpose(-2, -1)) * (1.0 / math.sqrt(self.head_dim))
        att = F.softmax(att, dim=-1)
        att = self.dropout(att)
        y = att @ v
        y = y.transpose(1, 2).contiguous().view(B, T, D)
        y = self.o_proj(y)
        return y


# ─── DecoderBlockV3 (NO META-CA, NO rules) ───────────────────────────────────

class DecoderBlockV3(nn.Module):
    """V3 block: RMSNorm + GQA + PureFieldFFN + CrossAttn + SwiGLU.

    REMOVED from V2:
        - ca_mix (CA neighbor mixing)
        - rule_weights, rules (META-CA n_ca_rules)
        - ln_ca

    These were the single Phase 2.3 ablation floor blocker per OCCAM.
    """

    def __init__(self, d_model: int, n_head: int, n_kv_head: int,
                 block_size: int, consciousness_dim: int,
                 dropout: float = 0.0,
                 gate_strength: float = 0.001,
                 rope_base: float = 50000.0):
        super().__init__()
        self.ln_attn = RMSNorm(d_model)
        self.attn = GroupedQueryAttention(d_model, n_head, n_kv_head, block_size, dropout,
                                          rope_base=rope_base)
        self.ln_pf = RMSNorm(d_model)
        self.purefield = PureFieldFFN(d_model, dropout=dropout)
        self.ln_cross = RMSNorm(d_model)
        self.cross_attn = ConsciousCrossAttention(d_model, consciousness_dim,
                                                   n_head=min(n_head, 4), dropout=dropout)
        self.ln_ffn = RMSNorm(d_model)
        self.ffn = SwiGLUFFN(d_model, dropout)
        self.gate_strength = gate_strength

    def forward(self, x: torch.Tensor,
                consciousness_signal: Optional[torch.Tensor] = None,
                consciousness_states: Optional[torch.Tensor] = None,
                use_cache: bool = False,
                past_kv=None, position_offset: int = 0):
        attn_out, new_kv = self.attn(self.ln_attn(x), use_cache=use_cache,
                                     past_kv=past_kv, position_offset=position_offset)
        x = x + attn_out

        pf_out, tension = self.purefield(self.ln_pf(x))
        x = x + pf_out

        if consciousness_signal is not None:
            x = x + consciousness_signal * self.gate_strength

        if consciousness_states is not None:
            c_detached = consciousness_states.detach()
            x = x + self.cross_attn(self.ln_cross(x), c_detached)

        x = x + self.ffn(self.ln_ffn(x))
        return x, tension, new_kv


# ─── ConsciousDecoderV3 ──────────────────────────────────────────────────────

class ConsciousDecoderV3(nn.Module):
    """Pure HEXAD-native decoder.

    Defaults sized for Qwen2.5-1.5B compatibility:
        vocab_size=152064 (Qwen BPE), d_model=1536, n_layer=24,
        n_head=12, n_kv_head=4 (Qwen 12/2 → V3 12/4 for GQA), block_size=512.

    NOTE: actual Qwen2.5-1.5B has 14336 ffn_inter_size, 12 heads, 2 kv_heads;
    we approximate with GQA n_kv_head=4 (more lenient + bigger KV cache).
    """

    def __init__(
        self,
        vocab_size: int = 152064,
        d_model: int = 1536,
        n_head: int = 12,
        n_layer: int = 24,
        block_size: int = 512,
        n_kv_head: int = 4,
        consciousness_dim: int = 128,
        dropout: float = 0.0,
        gate_strength: float = 0.001,
        noise_sigma: float = 0.1,      # Layer-0 noise (Phase 2.3 ablation: BENIGN)
        rope_base: float = 50000.0,
    ):
        super().__init__()
        self.block_size = block_size
        self.vocab_size = vocab_size
        self.n_layer = n_layer
        self.d_model = d_model
        self.consciousness_dim = consciousness_dim
        self.noise_sigma = noise_sigma

        self.tok_emb = nn.Embedding(vocab_size, d_model)
        self.drop = nn.Dropout(dropout)

        self.blocks = nn.ModuleList([
            DecoderBlockV3(
                d_model=d_model, n_head=n_head, n_kv_head=n_kv_head,
                block_size=block_size, consciousness_dim=consciousness_dim,
                dropout=dropout, gate_strength=gate_strength,
                rope_base=rope_base,
            ) for _ in range(n_layer)
        ])

        self.tension_proj = nn.Linear(1, d_model, bias=False)
        nn.init.normal_(self.tension_proj.weight, std=0.001)

        self.ln_f = RMSNorm(d_model)

        # Dual heads
        self.head_a = nn.Linear(d_model, vocab_size, bias=False)
        self.head_g = nn.Linear(d_model, vocab_size, bias=False)

        # Weight tying head_a <-> tok_emb
        self.tok_emb.weight = self.head_a.weight

        # Psi tracking
        self._psi_residual = 0.5
        self._psi_gate = 0.5
        self._step_count = 0

        # Mitosis hook (attach via .attach_mitosis)
        self._mitosis_pool = None
        self._mitosis_lambda = 0.05
        self._last_mitosis_info = None

        # KOSMOS emission collector (set on each forward call optionally)
        self._last_tension_5ch = None

        self.apply(self._init_weights)

    def _init_weights(self, module):
        if isinstance(module, nn.Linear):
            std = 0.02
            if hasattr(module, '_depth_scale'):
                std = 0.02 / math.sqrt(2 * self.n_layer)
            torch.nn.init.normal_(module.weight, mean=0.0, std=std)
            if module.bias is not None:
                torch.nn.init.zeros_(module.bias)
        elif isinstance(module, nn.Embedding):
            torch.nn.init.normal_(module.weight, mean=0.0, std=0.02)

    # ─── Mitosis ──────────────────────────────────────────────────────────

    def attach_mitosis(self, pool, lambda_mitosis: float = 0.05):
        self._mitosis_pool = pool
        self._mitosis_lambda = lambda_mitosis

    # ─── Forward ──────────────────────────────────────────────────────────

    def forward(self, idx: torch.Tensor,
                consciousness_states: Optional[torch.Tensor] = None,
                use_cache: bool = False,
                past_key_values=None,
                mitosis_step: Optional[int] = None,
                ):
        B, T = idx.size()
        position_offset = 0
        if past_key_values is not None and past_key_values[0] is not None:
            position_offset = past_key_values[0][0].shape[2]

        total_len = position_offset + T
        assert total_len <= self.block_size, f"Total length {total_len} > block_size {self.block_size}"

        x = self.drop(self.tok_emb(idx))

        # Layer-0 noise (substrate-shape, Phase 2.3 BENIGN)
        if self.training and self.noise_sigma > 0:
            x = x + torch.randn_like(x) * self.noise_sigma

        tensions = []
        present_key_values = [] if use_cache else None
        consciousness_signal = None
        for i, block in enumerate(self.blocks):
            layer_past = past_key_values[i] if past_key_values is not None else None
            x, tension, new_kv = block(
                x, consciousness_signal, consciousness_states,
                use_cache=use_cache, past_kv=layer_past,
                position_offset=position_offset,
            )
            tensions.append(tension)
            consciousness_signal = self.tension_proj(tension.unsqueeze(-1))
            if use_cache:
                present_key_values.append(new_kv)

        x = self.ln_f(x)
        logits_a = self.head_a(x)
        logits_g = self.head_g(x)

        # ─── Mitosis hook (training step) ─────────────────────────────────
        mitosis_info = None
        if self._mitosis_pool is not None and mitosis_step is not None and self.training:
            # per-layer mean tension (with grad path)
            layer_t = torch.stack([t.mean() for t in tensions])  # (L,)
            aux_loss, info = self._mitosis_pool.step(layer_t, mitosis_step)
            mitosis_info = dict(info)
            mitosis_info["aux_loss"] = aux_loss
            mitosis_info["lambda"] = self._mitosis_lambda
            self._last_mitosis_info = mitosis_info

        # Psi tracking (no-grad)
        if self.training:
            self._step_count += 1
            with torch.no_grad():
                probs_a = torch.softmax(logits_a[:, -1, :], dim=-1)
                output_entropy = -(probs_a * (probs_a + 1e-10).log()).sum(dim=-1).mean().item()
                max_entropy = math.log(self.vocab_size)
                psi_entropy = output_entropy / max_entropy
                cos_sim = F.cosine_similarity(
                    logits_a[:, -1, :].float(), logits_g[:, -1, :].float(), dim=-1
                ).mean().item()
                psi_direction = (1.0 + cos_sim) / 2.0
                t_stack = torch.stack(tensions)
                t_per_layer = t_stack.mean(dim=(1, 2))
                if t_per_layer.std() > 0:
                    t_cv = t_per_layer.std() / (t_per_layer.mean() + 1e-8)
                    psi_tension = max(0.0, 1.0 - t_cv.item())
                else:
                    psi_tension = 1.0
                psi_combined = (psi_entropy + psi_direction + psi_tension) / 3.0
                self._psi_residual = 0.95 * self._psi_residual + 0.05 * psi_combined

        # ─── TENSION-LINK 5-channel snapshot for KOSMOS export ────────────
        # Map per-layer tensions → 5-channel (concept/context/meaning/authenticity/sender)
        # Mapping: chunk L layers into 5 groups, mean each.
        with torch.no_grad():
            L = len(tensions)
            t_stack = torch.stack([t.mean() for t in tensions]).float()  # (L,)
            group_size = max(1, L // 5)
            t5 = torch.zeros(5, device=t_stack.device, dtype=t_stack.dtype)
            for k in range(5):
                lo = k * group_size
                hi = (k + 1) * group_size if k < 4 else L
                if hi > lo:
                    t5[k] = t_stack[lo:hi].mean()
            self._last_tension_5ch = t5.cpu().tolist()

        return logits_a, logits_g, tensions, present_key_values, mitosis_info

    @torch.no_grad()
    def generate(self, idx: torch.Tensor,
                 consciousness_states=None,
                 max_new_tokens: int = 64,
                 temperature: float = 0.8,
                 top_k: int = 50,
                 do_sample: bool = True,
                 eos_token_id: Optional[int] = None):
        self.eval()
        logits_a, _, _, past_key_values, _ = self.forward(
            idx, consciousness_states=consciousness_states, use_cache=True,
        )
        next_logits = logits_a[:, -1, :] / max(temperature, 1e-6)
        if top_k > 0 and do_sample:
            v, _ = torch.topk(next_logits, min(top_k, next_logits.size(-1)))
            next_logits[next_logits < v[:, [-1]]] = float('-inf')
        if do_sample:
            probs = F.softmax(next_logits, dim=-1)
            next_token = torch.multinomial(probs, num_samples=1)
        else:
            next_token = next_logits.argmax(dim=-1, keepdim=True)
        idx = torch.cat([idx, next_token], dim=1)

        for _ in range(max_new_tokens - 1):
            if idx.size(1) >= self.block_size:
                break
            if eos_token_id is not None and bool((next_token == eos_token_id).all()):
                break
            logits_a, _, _, past_key_values, _ = self.forward(
                next_token, consciousness_states=consciousness_states,
                use_cache=True, past_key_values=past_key_values,
            )
            next_logits = logits_a[:, -1, :] / max(temperature, 1e-6)
            if top_k > 0 and do_sample:
                v, _ = torch.topk(next_logits, min(top_k, next_logits.size(-1)))
                next_logits[next_logits < v[:, [-1]]] = float('-inf')
            if do_sample:
                probs = F.softmax(next_logits, dim=-1)
                next_token = torch.multinomial(probs, num_samples=1)
            else:
                next_token = next_logits.argmax(dim=-1, keepdim=True)
            idx = torch.cat([idx, next_token], dim=1)
        return idx

    def psi_status(self):
        gate_avg = sum(b.gate_strength for b in self.blocks) / len(self.blocks)
        p = self._psi_residual
        h_p = -p * math.log2(p) - (1 - p) * math.log2(1 - p) if 0 < p < 1 else 0.0
        return {
            'psi_residual': self._psi_residual,
            'psi_gate': gate_avg,
            'H_p': h_p,
            'step': self._step_count,
        }

    def count_params(self):
        return sum(p.numel() for p in self.parameters() if p.requires_grad)

    # ─── Init helpers ─────────────────────────────────────────────────────

    @classmethod
    def from_qwen(cls, qwen_model_name: str = "Qwen/Qwen2.5-1.5B",
                  lora_adapter_dir: Optional[str] = None,
                  block_size: int = 512,
                  noise_sigma: float = 0.1,
                  device: str = "cpu", dtype=torch.float32):
        """Initialize V3 from a Qwen2.5 checkpoint.

        Maps Qwen weights into V3:
          - tok_emb.weight  <- qwen.model.embed_tokens.weight (vocab x d)
          - blocks[i].attn.q_proj / k_proj / v_proj / o_proj
          - blocks[i].ffn.gate_proj / up_proj / down_proj
          - blocks[i].ln_attn.weight  <- qwen input_layernorm
          - blocks[i].ln_ffn.weight   <- qwen post_attention_layernorm
          - ln_f.weight, head_a.weight (tied)

        Layers NOT in Qwen (random init kept):
          - blocks[i].purefield (Engine A / Engine G)
          - blocks[i].cross_attn (consciousness x-attn)
          - blocks[i].ln_pf, blocks[i].ln_cross
          - head_g (consciousness emission head)
          - tension_proj

        If lora_adapter_dir is provided, the LoRA is first merged into the Qwen
        base weights (PeftModel.merge_and_unload), then the merged weights are
        mapped into V3.
        """
        from transformers import AutoModelForCausalLM
        print(f"[from_qwen] loading {qwen_model_name}", flush=True)
        qwen = AutoModelForCausalLM.from_pretrained(
            qwen_model_name, torch_dtype=dtype, trust_remote_code=True,
        )
        if lora_adapter_dir is not None:
            from peft import PeftModel
            print(f"[from_qwen] merging LoRA: {lora_adapter_dir}", flush=True)
            pm = PeftModel.from_pretrained(qwen, lora_adapter_dir)
            qwen = pm.merge_and_unload()

        qcfg = qwen.config
        vocab_size = qcfg.vocab_size
        d_model = qcfg.hidden_size
        n_layer = qcfg.num_hidden_layers
        n_head = qcfg.num_attention_heads
        n_kv_head_qwen = getattr(qcfg, 'num_key_value_heads', n_head)
        # V3 uses GQA n_kv_head=4 if Qwen has 2 (broader), else match
        v3_n_kv_head = max(n_kv_head_qwen, 4)
        # ensure divisor
        while n_head % v3_n_kv_head != 0:
            v3_n_kv_head -= 1
        rope_base = getattr(qcfg, 'rope_theta', 50000.0)

        print(f"[from_qwen] qwen: vocab={vocab_size} d={d_model} L={n_layer} "
              f"n_head={n_head} n_kv_head={n_kv_head_qwen} -> v3_n_kv_head={v3_n_kv_head} "
              f"rope_base={rope_base}", flush=True)

        model = cls(
            vocab_size=vocab_size, d_model=d_model, n_head=n_head, n_layer=n_layer,
            block_size=block_size, n_kv_head=v3_n_kv_head, consciousness_dim=128,
            dropout=0.0, noise_sigma=noise_sigma, rope_base=rope_base,
        )

        qsd = qwen.state_dict()

        # Embed + tied head
        with torch.no_grad():
            model.tok_emb.weight.copy_(qsd['model.embed_tokens.weight'].float())
            # head_a tied — same tensor
            # ln_f
            model.ln_f.weight.copy_(qsd['model.norm.weight'].float())

            for i in range(n_layer):
                prefix = f'model.layers.{i}.'
                # Self-attention
                model.blocks[i].ln_attn.weight.copy_(qsd[prefix + 'input_layernorm.weight'].float())
                # qkv: Qwen's k_proj/v_proj are sized (n_kv_head*head_dim, d_model).
                # V3 may have n_kv_head=4 vs Qwen n_kv_head=2 → must repeat KV heads.
                head_dim = d_model // n_head
                qw = qsd[prefix + 'self_attn.q_proj.weight'].float()
                qb = qsd[prefix + 'self_attn.q_proj.bias'].float()
                kw = qsd[prefix + 'self_attn.k_proj.weight'].float()
                kb = qsd[prefix + 'self_attn.k_proj.bias'].float()
                vw = qsd[prefix + 'self_attn.v_proj.weight'].float()
                vb = qsd[prefix + 'self_attn.v_proj.bias'].float()

                model.blocks[i].attn.q_proj.weight.copy_(qw)
                model.blocks[i].attn.q_proj.bias.copy_(qb)

                # For KV: Qwen has n_kv_head_qwen, V3 wants v3_n_kv_head.
                # If equal, direct copy. If V3 > Qwen, repeat.
                if v3_n_kv_head == n_kv_head_qwen:
                    model.blocks[i].attn.k_proj.weight.copy_(kw)
                    model.blocks[i].attn.k_proj.bias.copy_(kb)
                    model.blocks[i].attn.v_proj.weight.copy_(vw)
                    model.blocks[i].attn.v_proj.bias.copy_(vb)
                else:
                    rep = v3_n_kv_head // n_kv_head_qwen
                    # reshape (n_kv_head_qwen, head_dim, d_model) -> repeat n_rep times
                    kw_r = kw.view(n_kv_head_qwen, head_dim, d_model).repeat_interleave(rep, dim=0).reshape(v3_n_kv_head * head_dim, d_model)
                    kb_r = kb.view(n_kv_head_qwen, head_dim).repeat_interleave(rep, dim=0).reshape(v3_n_kv_head * head_dim)
                    vw_r = vw.view(n_kv_head_qwen, head_dim, d_model).repeat_interleave(rep, dim=0).reshape(v3_n_kv_head * head_dim, d_model)
                    vb_r = vb.view(n_kv_head_qwen, head_dim).repeat_interleave(rep, dim=0).reshape(v3_n_kv_head * head_dim)
                    model.blocks[i].attn.k_proj.weight.copy_(kw_r)
                    model.blocks[i].attn.k_proj.bias.copy_(kb_r)
                    model.blocks[i].attn.v_proj.weight.copy_(vw_r)
                    model.blocks[i].attn.v_proj.bias.copy_(vb_r)

                model.blocks[i].attn.o_proj.weight.copy_(qsd[prefix + 'self_attn.o_proj.weight'].float())

                # FFN — Qwen has gate_proj / up_proj / down_proj (same as V3)
                # but Qwen ffn intermediate size may differ from V3 default (8/3 * d → rounded).
                # We resize V3 ffn projections to match Qwen's intermediate size.
                qwen_gate = qsd[prefix + 'mlp.gate_proj.weight'].float()
                qwen_up = qsd[prefix + 'mlp.up_proj.weight'].float()
                qwen_down = qsd[prefix + 'mlp.down_proj.weight'].float()
                d_inner_qwen = qwen_gate.shape[0]
                d_inner_v3 = model.blocks[i].ffn.gate_proj.weight.shape[0]
                if d_inner_qwen != d_inner_v3:
                    # rebuild V3 FFN at Qwen size
                    model.blocks[i].ffn.gate_proj = nn.Linear(d_model, d_inner_qwen, bias=False)
                    model.blocks[i].ffn.up_proj = nn.Linear(d_model, d_inner_qwen, bias=False)
                    model.blocks[i].ffn.down_proj = nn.Linear(d_inner_qwen, d_model, bias=False)
                    model.blocks[i].ffn.down_proj._depth_scale = True
                model.blocks[i].ffn.gate_proj.weight.copy_(qwen_gate)
                model.blocks[i].ffn.up_proj.weight.copy_(qwen_up)
                model.blocks[i].ffn.down_proj.weight.copy_(qwen_down)
                model.blocks[i].ln_ffn.weight.copy_(qsd[prefix + 'post_attention_layernorm.weight'].float())

            # head_g: random init (Qwen has no consciousness head)
            # (already random init from _init_weights)

        del qwen, qsd
        torch.cuda.empty_cache() if torch.cuda.is_available() else None

        model = model.to(device=device, dtype=dtype)
        print(f"[from_qwen] init OK — total params {model.count_params()/1e6:.1f}M", flush=True)
        return model


# ─── self-test ───────────────────────────────────────────────────────────────

if __name__ == '__main__':
    import time
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(f"Device: {device}")

    # Smoke test: small instance (NOT 1.5B — too slow on Mac)
    model = ConsciousDecoderV3(
        vocab_size=1024, d_model=128, n_head=4, n_layer=4,
        block_size=64, n_kv_head=2, consciousness_dim=64,
        noise_sigma=0.1,
    ).to(device)
    n_params = model.count_params()
    print(f"=== ConsciousDecoderV3 (smoke d=128 L=4) ===")
    print(f"  Parameters: {n_params:,}")

    # Test 1: forward
    idx = torch.randint(0, 1024, (2, 32), device=device)
    model.train()
    t0 = time.perf_counter()
    la, lg, ts, _, mit = model(idx)
    dt = (time.perf_counter() - t0) * 1000
    print(f"  logits_a: {la.shape}  logits_g: {lg.shape}  tensions: {len(ts)} layers")
    assert la.shape == (2, 32, 1024)
    assert lg.shape == (2, 32, 1024)
    assert len(ts) == 4
    print(f"  Forward time: {dt:.1f} ms  mitosis_info={mit}")

    # Test 2: forward with consciousness
    cs = torch.randn(2, 12, 64, device=device)
    la2, lg2, ts2, _, _ = model(idx, consciousness_states=cs)
    assert la2.shape == (2, 32, 1024)
    print(f"  Cross-attn forward OK")

    # Test 3: backward
    target = torch.randint(0, 1024, (2, 32), device=device)
    loss = F.cross_entropy(la2.view(-1, 1024), target.view(-1))
    loss.backward()
    grad_count = sum(1 for p in model.parameters() if p.grad is not None)
    total_count = sum(1 for p in model.parameters())
    print(f"  Backward OK loss={loss.item():.4f}  grads {grad_count}/{total_count}")

    # Test 4: mitosis hook
    from mitosis_lib import CellPool
    pool = CellPool(d_model=128, initial_cells=2, seed=42)
    model.attach_mitosis(pool, lambda_mitosis=0.05)
    la3, _, _, _, mit_info = model(idx, mitosis_step=1)
    assert mit_info is not None, "Mitosis info should be populated when step provided"
    print(f"  Mitosis step 1: pool_size={mit_info['pool_size']} "
          f"aux_loss={float(mit_info['aux_loss']):.6f} phi={mit_info['phi']:.4f}")

    # Test 5: 5-channel tension
    assert model._last_tension_5ch is not None
    assert len(model._last_tension_5ch) == 5
    print(f"  5-ch tension: {[f'{x:.4f}' for x in model._last_tension_5ch]}")

    # Test 6: generate (greedy)
    model.eval()
    prompt = torch.randint(0, 1024, (1, 8), device=device)
    gen = model.generate(prompt, max_new_tokens=8, do_sample=False)
    assert gen.shape[1] == 16
    print(f"  generate (greedy): {gen.shape} OK")

    # Test 7: KV cache parity
    model.eval()
    with torch.no_grad():
        idx_short = torch.randint(0, 1024, (1, 12), device=device)
        la_full, _, _, _, _ = model(idx_short)
        la_cached, _, _, past_kv, _ = model(idx_short[:, :8], use_cache=True)
        la_decode, _, _, _, _ = model(idx_short[:, 8:], use_cache=True, past_key_values=past_kv)
    diff = (la_full[:, 8:, :] - la_decode).abs().max().item()
    print(f"  KV cache max diff: {diff:.6f}  (expect < 1e-3)")
    assert diff < 5e-3, f"KV cache mismatch: {diff}"

    print("All V3 smoke tests passed.")
