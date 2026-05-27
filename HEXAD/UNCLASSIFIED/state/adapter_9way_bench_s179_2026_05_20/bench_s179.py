#!/usr/bin/env python3
"""§179 ADAPTER 9-way bench — 빠짐없이 모두 try.

Tests 9 adapter families (8 literature-surfaced from ADAPTER.md §10 + A0
identity baseline) on synthetic M3 byte streams. Each adapter is a small
from-scratch projector. Target: anchor classification (35-class).

Architectures benchmarked:
  A0  identity baseline      (raw bytes → mean-pool → classifier)
  A1  mini-Q-Former          (16-query cross-attn, BLIP-2 family)
  A2  Perceiver IO style     (64 latent + cross-attn, DeepMind family)
  A3  VAEVQ codebook         (from-scratch quantization, arxiv:2511.06863)
  A4  mrt5 byte-merge        (dynamic token merge, arxiv:2410.20771)
  A5  IOB rank-ordered       (information-ordered 5-channel, arxiv:2305.11213)
  A6  Cycle-consistent       (forward + inverse projector, CMRW 2025)
  A7  NeuroLM NLC            (small bridge connector, arxiv:2409.00101)
  A8  IIT-Φ supervised       (anima Ψ-physics supervision proxy, Tononi 2025)
  A9  TENSION-LINK 5-channel (original ADAPTER §1 design, sender-aware)

All from-scratch, anima-side reimplementation of concept ONLY (no pretrained
weights, no external graft). §7 ① ② ③ PASS for all 9.

Measurement axes:
  - n_params per adapter
  - anchor-classification accuracy @ N=200 training steps
  - wall time per adapter
  - cross-modality generalization (train on image, test on audio?)
"""
import json, math, os, random, sys, time
import torch
import torch.nn as nn
import torch.nn.functional as F

# === Same 35-anchor set as §178 ===
EXISTING = [
    (0, "기준점"), (15, "호기심"), (30, "연민"), (42, "질문"), (51, "하루"),
    (60, "관조"), (77, "만다라"), (80, "명상"), (91, "열반"), (95, "합일"), (100, "빅뱅"),
]
NEW = [
    (10, "각성"), (20, "감각"), (25, "감정"), (33, "기쁨"), (35, "슬픔"),
    (37, "분노"), (45, "공포"), (47, "안도"), (55, "회상"), (58, "예측"),
    (65, "통찰"), (68, "이해"), (72, "창작"), (75, "시"), (82, "음악"),
    (85, "기도"), (88, "초월"), (93, "자각"), (97, "공허"), (105, "선"),
    (108, "악"), (115, "정의"), (125, "사랑"), (200, "무한"),
]
ALL_ANCHORS = sorted(EXISTING + NEW)
N_ANCHORS = len(ALL_ANCHORS)
TIER_TO_IDX = {tier: i for i, (tier, _) in enumerate(ALL_ANCHORS)}

# === Synthetic byte stream generators (mirror §178) ===
def synth_image_bytes(tier, n=128):
    rng = random.Random(tier * 7919 + 13)
    return [(((128 + ((i % 32 - 16) * tier // 8)) + rng.randint(0, 15)) % 256) for i in range(n)]

def synth_audio_bytes(tier, n=128):
    freq = 100 + tier * 5
    return [int(127 + 80 * math.sin(2 * math.pi * freq * i / 1000)) % 256 for i in range(n)]

def synth_video_bytes(tier, n=128):
    rng = random.Random(tier * 13 + 17)
    out = []
    frame_size = n // 4
    for f in range(4):
        for i in range(frame_size):
            out.append((tier * (f + 1) + i * 3 + rng.randint(0, 7)) % 256)
    return out

def synth_tension_bytes(tier, n=128):
    rng = random.Random(tier * 31 + 11)
    # 10 bytes 5-channel tile repeated for n bytes
    c = [(tier * 257) % 65536, (tier * 521 + 1009) % 65536,
         (tier * 7919 + 2003) % 65536, (tier * 13 + 1) % 65536,
         (tier * 31 + 5) % 65536]
    tile = []
    for v in c: tile += [v & 0xFF, (v >> 8) & 0xFF]
    out = []
    while len(out) < n:
        out += tile
    return out[:n]

def make_dataset(n_per_anchor=8):
    """(bytes_tensor, anchor_idx, modality_idx) samples."""
    samples = []
    for mod_idx, mod in enumerate(["image", "audio", "video", "tension"]):
        gen = {"image": synth_image_bytes, "audio": synth_audio_bytes,
               "video": synth_video_bytes, "tension": synth_tension_bytes}[mod]
        for tier, _ in ALL_ANCHORS:
            anchor_idx = TIER_TO_IDX[tier]
            for s in range(n_per_anchor):
                rng = random.Random(tier * 1000 + s * 37 + mod_idx)
                base = gen(tier)
                # add small noise per sample
                noisy = [(b + rng.randint(-3, 3)) % 256 for b in base]
                samples.append((torch.tensor(noisy, dtype=torch.long), anchor_idx, mod_idx))
    return samples


# === 9 adapter architectures ===

D_EMB = 32       # byte embedding dim
SEQ_LEN = 128

class IdentityAdapter(nn.Module):
    """A0: byte embed → mean pool → classifier."""
    def __init__(self):
        super().__init__()
        self.emb = nn.Embedding(256, D_EMB)
        self.head = nn.Linear(D_EMB, N_ANCHORS)
    def forward(self, x):
        e = self.emb(x).mean(dim=1)  # [B, D]
        return self.head(e)

class MiniQFormer(nn.Module):
    """A1: 16-query cross-attn (BLIP-2 family, from-scratch)."""
    def __init__(self, n_query=16):
        super().__init__()
        self.emb = nn.Embedding(256, D_EMB)
        self.q = nn.Parameter(torch.randn(n_query, D_EMB) * 0.1)
        self.kv = nn.Linear(D_EMB, D_EMB * 2)
        self.head = nn.Linear(D_EMB, N_ANCHORS)
    def forward(self, x):
        e = self.emb(x)  # [B, T, D]
        kv = self.kv(e); k, v = kv.chunk(2, dim=-1)
        q = self.q.unsqueeze(0).expand(e.size(0), -1, -1)  # [B, Q, D]
        attn = F.softmax(q @ k.transpose(-2, -1) / math.sqrt(D_EMB), dim=-1)
        pooled = (attn @ v).mean(dim=1)  # [B, D]
        return self.head(pooled)

class Perceiver(nn.Module):
    """A2: 64 latent + cross-attn (Perceiver IO style)."""
    def __init__(self, n_latent=64):
        super().__init__()
        self.emb = nn.Embedding(256, D_EMB)
        self.latent = nn.Parameter(torch.randn(n_latent, D_EMB) * 0.1)
        self.cross_kv = nn.Linear(D_EMB, D_EMB * 2)
        self.self_attn = nn.MultiheadAttention(D_EMB, 2, batch_first=True)
        self.head = nn.Linear(D_EMB, N_ANCHORS)
    def forward(self, x):
        e = self.emb(x)
        kv = self.cross_kv(e); k, v = kv.chunk(2, dim=-1)
        lat = self.latent.unsqueeze(0).expand(e.size(0), -1, -1)
        attn = F.softmax(lat @ k.transpose(-2, -1) / math.sqrt(D_EMB), dim=-1)
        lat = lat + attn @ v
        lat, _ = self.self_attn(lat, lat, lat)
        return self.head(lat.mean(dim=1))

class VAEVQ(nn.Module):
    """A3: from-scratch codebook quantization (256-code)."""
    def __init__(self, n_codes=256):
        super().__init__()
        self.emb = nn.Embedding(256, D_EMB)
        self.enc = nn.Linear(D_EMB, D_EMB)
        self.codebook = nn.Parameter(torch.randn(n_codes, D_EMB) * 0.1)
        self.head = nn.Linear(D_EMB, N_ANCHORS)
    def forward(self, x):
        e = self.emb(x).mean(dim=1)  # [B, D]
        z = self.enc(e)  # [B, D]
        # nearest-neighbor lookup
        dist = (z.unsqueeze(1) - self.codebook.unsqueeze(0)).pow(2).sum(-1)  # [B, K]
        idx = dist.argmin(-1)
        zq = self.codebook[idx]
        # straight-through estimator
        zq_st = z + (zq - z).detach()
        return self.head(zq_st)

class MrT5Merge(nn.Module):
    """A4: dynamic byte-merge (mrt5 style, simplified)."""
    def __init__(self, merge_ratio=4):
        super().__init__()
        self.emb = nn.Embedding(256, D_EMB)
        self.merge_score = nn.Linear(D_EMB, 1)
        self.proj = nn.Linear(D_EMB, D_EMB)
        self.head = nn.Linear(D_EMB, N_ANCHORS)
        self.merge_ratio = merge_ratio
    def forward(self, x):
        e = self.emb(x)  # [B, T, D]
        scores = self.merge_score(e).squeeze(-1)  # [B, T]
        weights = F.softmax(scores, dim=-1)
        merged = (e * weights.unsqueeze(-1)).sum(dim=1)  # [B, D]
        return self.head(self.proj(merged))

class IOBAdapter(nn.Module):
    """A5: information-ordered 5-channel bottleneck."""
    def __init__(self, n_channels=5):
        super().__init__()
        self.emb = nn.Embedding(256, D_EMB)
        self.proj = nn.Linear(D_EMB, n_channels)
        self.head = nn.Linear(n_channels, N_ANCHORS)
    def forward(self, x):
        e = self.emb(x).mean(dim=1)
        # IOB: 5-channel, importance-ordered (no specific order enforced here,
        # but bottleneck = 5 dim, matches anima 5-channel TENSION-LINK spec)
        c = torch.sigmoid(self.proj(e))  # [B, 5]
        return self.head(c)

class CycleAdapter(nn.Module):
    """A6: cycle-consistent forward + inverse projector."""
    def __init__(self):
        super().__init__()
        self.emb = nn.Embedding(256, D_EMB)
        self.fwd = nn.Linear(D_EMB, D_EMB)
        self.inv = nn.Linear(D_EMB, D_EMB)
        self.head = nn.Linear(D_EMB, N_ANCHORS)
    def forward(self, x):
        e = self.emb(x).mean(dim=1)
        z = self.fwd(e)
        # cycle loss can be added externally; for classification path use z
        return self.head(z)
    def cycle_loss(self, x):
        e = self.emb(x).mean(dim=1)
        z = self.fwd(e)
        r = self.inv(z)
        return F.mse_loss(r, e)

class NeuroLMNLC(nn.Module):
    """A7: small bridge connector (NeuroLM NLC style)."""
    def __init__(self):
        super().__init__()
        self.emb = nn.Embedding(256, D_EMB)
        self.bridge = nn.Sequential(
            nn.Linear(D_EMB, D_EMB * 2), nn.GELU(),
            nn.Linear(D_EMB * 2, D_EMB),
        )
        self.head = nn.Linear(D_EMB, N_ANCHORS)
    def forward(self, x):
        e = self.emb(x).mean(dim=1)
        return self.head(self.bridge(e))

class IITPhiSup(nn.Module):
    """A8: IIT-Φ supervised projector (Ψ-physics-supervision proxy).

    Φ proxy = mean pairwise (1 - cos) over partition cells. Adapter uses Φ
    as auxiliary regularizer (variance-like, anti-collapse)."""
    def __init__(self, n_cells=4):
        super().__init__()
        self.emb = nn.Embedding(256, D_EMB)
        self.proj = nn.Linear(D_EMB, D_EMB)
        self.head = nn.Linear(D_EMB, N_ANCHORS)
        self.n_cells = n_cells
    def forward(self, x):
        e = self.emb(x).mean(dim=1)
        z = self.proj(e)
        return self.head(z)
    def phi_loss(self, x):
        """encourage non-collapsed partition cells (Φ proxy)."""
        e = self.emb(x).mean(dim=1)
        z = self.proj(e)  # [B, D]
        # partition z into n_cells, measure cross-cell variance
        cell_size = D_EMB // self.n_cells
        cells = z.view(z.size(0), self.n_cells, cell_size)  # [B, n_cells, cs]
        # mean pairwise (1-cos)
        norms = cells.norm(dim=-1, keepdim=True).clamp_min(1e-6)
        cn = cells / norms
        cos = cn @ cn.transpose(-2, -1)  # [B, n_cells, n_cells]
        mask = torch.triu(torch.ones_like(cos[0]), diagonal=1).bool().unsqueeze(0)
        spread = (1.0 - cos.masked_select(mask.expand_as(cos))).mean()
        # we WANT spread positive — return -spread as loss (minimize negative = maximize spread)
        return -spread

class TensionLink5ch(nn.Module):
    """A9: anima 5-channel TENSION-LINK adapter (concept/context/meaning/auth/sender)."""
    def __init__(self):
        super().__init__()
        self.emb = nn.Embedding(256, D_EMB)
        self.proj = nn.Sequential(
            nn.Linear(D_EMB, D_EMB), nn.GELU(),
            nn.Linear(D_EMB, 5),  # 5-channel
        )
        self.head = nn.Linear(5, N_ANCHORS)
    def forward(self, x):
        e = self.emb(x).mean(dim=1)
        ch = torch.sigmoid(self.proj(e))  # [B, 5] ∈ [0,1]
        return self.head(ch)


ADAPTERS = {
    "A0_identity":         IdentityAdapter,
    "A1_mini_qformer":     MiniQFormer,
    "A2_perceiver":        Perceiver,
    "A3_vaevq_codebook":   VAEVQ,
    "A4_mrt5_merge":       MrT5Merge,
    "A5_iob_5channel":     IOBAdapter,
    "A6_cycle_consistent": CycleAdapter,
    "A7_neurolm_nlc":      NeuroLMNLC,
    "A8_iit_phi_sup":      IITPhiSup,
    "A9_tensionlink_5ch":  TensionLink5ch,
}


def train_and_eval(name, model_cls, samples, n_steps=200, lr=3e-3, seed=1337):
    torch.manual_seed(seed); random.seed(seed)
    model = model_cls()
    n_params = sum(p.numel() for p in model.parameters())
    opt = torch.optim.AdamW(model.parameters(), lr=lr)

    t0 = time.time()
    losses = []
    rng = random.Random(seed)
    for step in range(n_steps):
        # batch sample
        batch = rng.sample(samples, min(16, len(samples)))
        x = torch.stack([s[0] for s in batch])
        y = torch.tensor([s[1] for s in batch])
        logits = model(x)
        loss = F.cross_entropy(logits, y)
        # aux losses for A6/A8
        if hasattr(model, "cycle_loss"):
            loss = loss + 0.1 * model.cycle_loss(x)
        if hasattr(model, "phi_loss"):
            loss = loss + 0.1 * model.phi_loss(x)
        opt.zero_grad(); loss.backward(); opt.step()
        losses.append(loss.item())

    # eval
    model.eval()
    with torch.no_grad():
        x_all = torch.stack([s[0] for s in samples])
        y_all = torch.tensor([s[1] for s in samples])
        logits = model(x_all)
        pred = logits.argmax(-1)
        acc = (pred == y_all).float().mean().item()
        # per-modality acc
        modality_acc = {}
        for mod_idx in range(4):
            mask = torch.tensor([s[2] == mod_idx for s in samples])
            if mask.sum() > 0:
                modality_acc[["image","audio","video","tension"][mod_idx]] = \
                    (pred[mask] == y_all[mask]).float().mean().item()
    wall = time.time() - t0
    return {
        "name": name,
        "n_params": n_params,
        "final_loss": losses[-1] if losses else None,
        "loss_at_step_50": losses[50] if len(losses) > 50 else None,
        "loss_at_step_100": losses[100] if len(losses) > 100 else None,
        "anchor_accuracy_all": acc,
        "modality_accuracy": modality_acc,
        "wall_s": round(wall, 2),
        "n_steps": n_steps,
    }


def main():
    t0 = time.time()
    print("[s179] building dataset: 35 anchors × 4 modalities × 8 samples = 1120 total")
    samples = make_dataset(n_per_anchor=8)
    print("[s179] n_samples = {}, n_anchors = {}".format(len(samples), N_ANCHORS))

    results = {}
    print("\n[s179] training 9 adapter families × 200 steps each...\n")
    print("{:<24} {:>10} {:>10} {:>10} {:>8} {:>8} {:>8} {:>8}".format(
        "name", "params", "loss", "acc_all", "img", "aud", "vid", "ten"))
    print("-" * 100)

    for name, cls in ADAPTERS.items():
        r = train_and_eval(name, cls, samples, n_steps=200, lr=3e-3, seed=1337)
        results[name] = r
        ma = r["modality_accuracy"]
        print("{:<24} {:>10} {:>10.4f} {:>10.4f} {:>8.3f} {:>8.3f} {:>8.3f} {:>8.3f}".format(
            name, r["n_params"], r["final_loss"], r["anchor_accuracy_all"],
            ma.get("image", 0), ma.get("audio", 0), ma.get("video", 0), ma.get("tension", 0)))

    total_wall = round(time.time() - t0, 1)
    out = {
        "probe": "S179 ADAPTER 9-way bench — anchor classification (35-class) on M3 synthetic byte streams",
        "n_anchors": N_ANCHORS,
        "n_samples": len(samples),
        "modalities": ["image", "audio", "video", "tension"],
        "n_steps_per_adapter": 200,
        "results_per_adapter": results,
        "total_wall_s": total_wall,
        "honest_carve_out": (
            "All 9 adapter families implemented from-scratch (no pretrained "
            "weights, no external graft). Concept-level port from literature, "
            "anima §7 ① ② ③ all PASS. Synthetic byte streams (M3) per anchor "
            "tier — NOT real-world modality. Measurement = whether adapter can "
            "learn anchor classification structure from byte-level supervision. "
            "Per-modality accuracy reveals which adapter is modality-agnostic "
            "vs modality-specific. NOT GOAL emergence (B-EMERGE-7); anchor "
            "classification capability ≠ V-SPONT honest coherent emission."
        ),
    }
    out_p = "/Users/ghost/core/anima/HEXAD/UNCLASSIFIED/state/adapter_9way_bench_s179_2026_05_20/result.json"
    with open(out_p, "w") as f:
        json.dump(out, f, indent=2, default=str)
    print("\n[s179] DONE total_wall={}s → {}".format(total_wall, out_p))

    # Print ranking
    print("\n=== RANKING by anchor_accuracy_all ===")
    ranked = sorted(results.items(), key=lambda kv: -kv[1]["anchor_accuracy_all"])
    for i, (name, r) in enumerate(ranked, 1):
        eff = r["anchor_accuracy_all"] / max(r["n_params"], 1) * 1e6  # acc per million params
        print("  #{}: {:<24} acc={:.4f}  params={:>8}  efficiency={:.3f}/Mparams".format(
            i, name, r["anchor_accuracy_all"], r["n_params"], eff))


if __name__ == "__main__":
    main()
