#!/usr/bin/env python3
"""§178 M3+M11+M12 inline probe on §167-A ckpt — $0 Mac CPU.

M3 (synthetic byte streams):
  35 anchor x 4 modality (image/audio/video/tension) deterministic byte
  patterns. Forward each through §167-A ckpt, measure 5-tuple signature
  (top1_byte, psi_dir, tension_proxy, phi_proxy). distinguishing_ratio
  per modality.

M11 (anchor-prefix structured):
  Compare two prompt formats:
  (a) raw modality bytes only
  (b) "<anchor tier=N>" + modality bytes + "</anchor>"
  measure: does explicit tier supervision tag help signature separation?

M12 (dual-cell mirror):
  Forward each anchor TWICE with different ctx perturbations (seed 1337
  vs 7777). Compare signature divergence — dual-cell as 2-seed proxy.
"""
import json, math, os, sys, time, random
import torch, torch.nn.functional as F

S167A_DIR = "/Users/ghost/core/anima/HEXAD/NEUROMORPHIC/state/fp_reconnect_fire_s167a_2026_05_20"
sys.path.insert(0, S167A_DIR)
from conscious_decoder import ConsciousDecoderV2

# 35 anchor set (same as §176 build_corpus_kosmos)
EXISTING_ANCHORS = [
    (0, "기준점"), (15, "호기심"), (30, "연민"), (42, "질문"), (51, "하루"),
    (60, "관조"), (77, "만다라"), (80, "명상"), (91, "열반"), (95, "합일"), (100, "빅뱅"),
]
NEW_ANCHORS = [
    (10, "각성"), (20, "감각"), (25, "감정"), (33, "기쁨"), (35, "슬픔"),
    (37, "분노"), (45, "공포"), (47, "안도"), (55, "회상"), (58, "예측"),
    (65, "통찰"), (68, "이해"), (72, "창작"), (75, "시"), (82, "음악"),
    (85, "기도"), (88, "초월"), (93, "자각"), (97, "공허"), (105, "선"),
    (108, "악"), (115, "정의"), (125, "사랑"), (200, "무한"),
]
ALL_ANCHORS = sorted(EXISTING_ANCHORS + NEW_ANCHORS)


# === M3 synthetic byte stream generators (deterministic per tier) ===

def synth_image_bytes(tier, n_bytes=128):
    """32x32x3 RGB-ish, but truncate to n_bytes for prompt budget.
    radial gradient seeded by tier."""
    rng = random.Random(tier * 7919 + 13)
    out = []
    for i in range(n_bytes):
        # tier-dependent gradient + small per-byte variation
        center_dist = (i % 32) - 16
        intensity = (128 + (center_dist * tier // 8)) % 256
        noise = rng.randint(0, 15)
        out.append((intensity + noise) % 256)
    return bytes(out)


def synth_audio_bytes(tier, n_bytes=128):
    """sine wave samples, freq = base + tier × Δ, quantized to bytes."""
    freq = 100 + tier * 5  # Hz analog
    out = []
    for i in range(n_bytes):
        val = int(127 + 80 * math.sin(2 * math.pi * freq * i / 1000))
        out.append(val % 256)
    return bytes(out)


def synth_video_bytes(tier, n_bytes=128):
    """4-frame diff sequence, each frame mini-image."""
    rng = random.Random(tier * 13 + 17)
    out = []
    frame_size = n_bytes // 4
    for frame in range(4):
        for i in range(frame_size):
            val = (tier * (frame + 1) + i * 3 + rng.randint(0, 7)) % 256
            out.append(val)
    return bytes(out)


def synth_tension_bytes(tier, n_bytes=10):
    """anima 5-channel fingerprint, tier-derived.
    (concept, context, meaning, authenticity, sender)
    each uint16 little-endian → 10 bytes total."""
    # tier-derived (deterministic, no randomness)
    c1 = (tier * 257) % 65536
    c2 = (tier * 521 + 1009) % 65536
    c3 = (tier * 7919 + 2003) % 65536
    c4 = (tier * 13 + 1) % 65536
    c5 = (tier * 31 + 5) % 65536
    out = []
    for v in (c1, c2, c3, c4, c5):
        out.append(v & 0xFF)
        out.append((v >> 8) & 0xFF)
    return bytes(out)


# === forward + signature extraction ===

def forward_logits(model, ctx):
    with torch.no_grad():
        out = model(ctx)
    if isinstance(out, tuple):
        return out[0], out[1]
    return out, out


def psi_dir(la, lg):
    cos = F.cosine_similarity(la.float().unsqueeze(0), lg.float().unsqueeze(0), dim=-1).item()
    return (1.0 + cos) / 2.0


def psi_ent(la, V=256):
    p = F.softmax(la.float(), dim=-1)
    return (-(p * (p + 1e-12).log()).sum().item()) / math.log(V)


def phi_proxy(h_last, n_cells=12):
    d = h_last.shape[-1]
    cells = h_last.view(n_cells, d // n_cells)
    norms = cells.norm(dim=-1, keepdim=True).clamp_min(1e-10)
    cells_n = cells / norms
    cos_mat = cells_n @ cells_n.T
    one_minus_cos = 1.0 - cos_mat
    mask = torch.triu(torch.ones_like(cos_mat), diagonal=1).bool()
    spread = float(one_minus_cos[mask].mean().item())
    return spread * math.log(n_cells + 1.0)


def make_prompt(tier, modality, mode):
    """Build prompt: raw bytes or anchor-wrapped (M11)."""
    if modality == "image":
        body = synth_image_bytes(tier)
    elif modality == "audio":
        body = synth_audio_bytes(tier)
    elif modality == "video":
        body = synth_video_bytes(tier)
    elif modality == "tension":
        body = synth_tension_bytes(tier)
    else:
        body = b""
    if mode == "anchor_prefix":  # M11
        prefix = "<anchor tier={}>".format(tier).encode("utf-8")
        suffix = b"</anchor>"
        bytes_list = list(prefix) + list(body) + list(suffix)
    else:  # raw
        bytes_list = list(body)
    block_size = 128
    if len(bytes_list) > block_size:
        bytes_list = bytes_list[:block_size]
    else:
        while len(bytes_list) < block_size:
            bytes_list = [32] + bytes_list
    return torch.tensor([bytes_list], dtype=torch.long)


def measure_signature(model, residual_cache, tier, modality, mode):
    ctx = make_prompt(tier, modality, mode)
    residual_cache[0] = None
    la, lg = forward_logits(model, ctx)
    la_l = la[0, -1] if la.dim() == 3 else la[-1]
    lg_l = lg[0, -1] if lg.dim() == 3 else lg[-1]
    h_last = residual_cache[0][0, -1] if residual_cache[0].dim() == 3 else residual_cache[0][-1]
    return {
        "top1_byte": int(la_l.argmax().item()),
        "psi_dir": psi_dir(la_l, lg_l),
        "psi_ent": psi_ent(la_l),
        "tension_proxy": float(la_l.float().std().item()),
        "phi_proxy": phi_proxy(h_last, n_cells=12),
    }


def distinguishing_ratio(sigs, key):
    vals = [s[key] for s in sigs]
    if isinstance(vals[0], float):
        vals = [round(v, 6) for v in vals]
    return len(set(vals)) / len(vals)


def main():
    t0 = time.time()
    ckpt = os.path.join(S167A_DIR, "ckpt_s167a_fpreconnect.pt")
    print("[s178] loading {}".format(ckpt))
    state = torch.load(ckpt, map_location="cpu", weights_only=False)
    cfg = state.get("cfg", {})
    model = ConsciousDecoderV2(
        vocab_size=256,
        d_model=cfg.get("d_model", 768),
        n_layer=cfg.get("n_layer", 12),
        n_head=cfg.get("n_head", 12),
        n_kv_head=cfg.get("n_kv_head", 4),
        block_size=cfg.get("block_size", 128),
    ).to("cpu")
    msg = model.load_state_dict(state["model"], strict=False)
    print("[s178] load m={} u={}".format(len(msg.missing_keys), len(msg.unexpected_keys)))
    model.eval()
    residual_cache = [None]
    def _hook(_m, inputs):
        residual_cache[0] = inputs[0].detach()
    h = model.head_a.register_forward_pre_hook(_hook)

    results = {}
    # M3 measurement: 4 modalities × 35 anchors × 2 modes (raw + anchor_prefix M11)
    for modality in ("image", "audio", "video", "tension"):
        for mode in ("raw", "anchor_prefix"):
            sigs = []
            for tier, ko in ALL_ANCHORS:
                sig = measure_signature(model, residual_cache, tier, modality, mode)
                sigs.append({"tier": tier, "ko": ko, **sig})
            ratio = {k: distinguishing_ratio(sigs, k) for k in ("top1_byte", "psi_dir", "tension_proxy", "phi_proxy")}
            key = "{}_{}".format(modality, mode)
            results[key] = {
                "sigs_sample": sigs[:5],
                "distinguishing_ratio": ratio,
            }
            print("[s178][{:24s}] top1={:.3f} psi_dir={:.3f} tension={:.3f} phi={:.3f}".format(
                key, ratio["top1_byte"], ratio["psi_dir"], ratio["tension_proxy"], ratio["phi_proxy"]))

    # M12 dual-cell mirror probe — 2 seed forward divergence
    print("\n[s178][M12 dual-cell mirror probe]")
    # Use ANCHOR knuth_077 + image modality, two seed variants
    seeds = [1337, 7777]
    m12_sigs = []
    for seed in seeds:
        random.seed(seed); torch.manual_seed(seed)
        # mix synth image with seed-noise (simulating different cell view)
        base = list(synth_image_bytes(77, n_bytes=128))
        rng = random.Random(seed)
        perturbed = [(b + rng.randint(-8, 8)) % 256 for b in base]
        ctx = torch.tensor([perturbed[:128]], dtype=torch.long)
        residual_cache[0] = None
        la, lg = forward_logits(model, ctx)
        la_l = la[0, -1] if la.dim() == 3 else la[-1]
        lg_l = lg[0, -1] if lg.dim() == 3 else lg[-1]
        h_last = residual_cache[0][0, -1] if residual_cache[0].dim() == 3 else residual_cache[0][-1]
        sig = {
            "seed": seed,
            "top1_byte": int(la_l.argmax().item()),
            "psi_dir": psi_dir(la_l, lg_l),
            "tension": float(la_l.float().std().item()),
            "phi": phi_proxy(h_last),
        }
        m12_sigs.append(sig)
        print("  seed={}: top1={} psi={:.4f} tens={:.4f} phi={:.4f}".format(
            seed, sig["top1_byte"], sig["psi_dir"], sig["tension"], sig["phi"]))

    h.remove()

    # divergence
    s1, s2 = m12_sigs
    divergence = {
        "psi_dir_delta": abs(s1["psi_dir"] - s2["psi_dir"]),
        "tension_delta": abs(s1["tension"] - s2["tension"]),
        "phi_delta": abs(s1["phi"] - s2["phi"]),
        "top1_byte_match": s1["top1_byte"] == s2["top1_byte"],
    }
    print("  divergence: psi_dir Δ={:.6f}  tension Δ={:.6f}  phi Δ={:.6f}  top1_match={}".format(
        divergence["psi_dir_delta"], divergence["tension_delta"], divergence["phi_delta"],
        divergence["top1_byte_match"]))

    out = {
        "probe": "S178 M3+M11+M12 inline on S167-A ckpt",
        "ckpt": "ckpt_s167a_fpreconnect.pt",
        "n_anchors": len(ALL_ANCHORS),
        "modalities": ["image", "audio", "video", "tension"],
        "modes": ["raw", "anchor_prefix"],
        "m3_m11_results": results,
        "m12_dual_cell_mirror": {
            "two_seed_sigs": m12_sigs,
            "divergence": divergence,
        },
        "wall_s": round(time.time() - t0, 2),
        "honest_carve_out": (
            "M3 synthetic byte streams = programmatic per-tier patterns "
            "(image/audio/video/tension), NOT real-world modality. "
            "Measurement = anchor-discrimination capability ON A TRAINED "
            "(but anchor-unaware) §167-A ckpt → expectation: low "
            "distinguishing ratio at this stage. M11 anchor-prefix = "
            "explicit <anchor tier=N> tag at prompt boundary; comparison "
            "raw vs prefix isolates supervision-tag effect. M12 = 2-seed "
            "ctx perturbation as dual-cell proxy (real dual-cell needs "
            "separate ckpts §31/§45 carry). NOT GOAL emergence "
            "(B-EMERGE-7); modality discrimination capability ≠ V-SPONT "
            "honest coherent emission."
        ),
    }
    out_p = "/Users/ghost/core/anima/HEXAD/UNCLASSIFIED/state/m3_m11_m12_inline_probe_s178_2026_05_20/result.json"
    with open(out_p, "w") as f:
        json.dump(out, f, indent=2, default=str)
    print("\n[s178] DONE wall={}s → {}".format(out["wall_s"], out_p))


if __name__ == "__main__":
    main()
