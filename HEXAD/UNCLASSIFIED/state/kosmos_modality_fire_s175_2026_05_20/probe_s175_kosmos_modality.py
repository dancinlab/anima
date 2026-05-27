#!/usr/bin/env python3
"""§175 KOSMOS 5-modality 전수 fire — 11 anchors × 4 measurable modalities.

modality coverage (honest):
  ✅ text       (top-1 byte argmax on anchor prefix forward)
  ✅ tension    (12-layer per-token activation energy CV per anchor)
  ✅ psi_dir    (Law-71 (1+cos(logits_a, logits_g))/2 per anchor)
  ✅ phi_proxy  (mitosis-form residual partition cosine spread, n_cells=12)
  ❌ image/audio/video — §109 DESIGN-CLOSE-WITH-NARROW-OPEN, §7-clean encoder 부재

per-anchor signature = 4-tuple (text_top1, tension, psi_dir, phi).
cross-anchor distinguishing check:
  - if all 11 anchors → identical signature → modality NOT distinguishing
  - if pairwise distinct → modality distinguishes anchors

$0 Mac CPU, no GPU, no training, single ckpt forward.
"""
import json, math, os, sys, time
import torch, torch.nn.functional as F

S167A_DIR = "/Users/ghost/core/anima/HEXAD/NEUROMORPHIC/state/fp_reconnect_fire_s167a_2026_05_20"
ANCHORS_DIR = "/Users/ghost/core/anima/HEXAD/UNIVERSE-BRAIN-MAP/anchors"
sys.path.insert(0, S167A_DIR)
from conscious_decoder import ConsciousDecoderV2

N_CELLS = 12  # 768 / 12 = 64 dims per cell for phi_proxy


def parse_kosmos(path):
    out = {"file": os.path.basename(path)}
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            for k in ("knuth_tier", "category", "top_emotion", "lane"):
                if line.startswith(k):
                    eq = line.split("=", 1)
                    if len(eq) == 2:
                        v = eq[1].strip().strip('"').split("#")[0].strip()
                        if k == "knuth_tier":
                            try: v = int(v)
                            except: pass
                        out[k] = v
    return out


def list_anchors():
    out = []
    for fn in sorted(os.listdir(ANCHORS_DIR)):
        if fn.endswith(".kosmos"):
            out.append(parse_kosmos(os.path.join(ANCHORS_DIR, fn)))
    return out


def anchor_prefix_bytes(tier, block_size=128):
    """Build prefix '[anima 우주뇌지도] 🛸<tier>' encoded UTF-8, padded."""
    prefix = "[anima 우주뇌지도] 🛸{}".format(tier)
    b = list(prefix.encode("utf-8"))[:block_size]
    while len(b) < block_size:
        b = [32] + b
    return b


def forward_with_residual(model, ctx, residual_cache):
    residual_cache[0] = None
    with torch.no_grad():
        out = model(ctx)
    if isinstance(out, tuple):
        la, lg = out[0], out[1]
    else:
        la, lg = out, out
    return la, lg


def psi_direction(la_last, lg_last):
    cos = F.cosine_similarity(
        la_last.float().unsqueeze(0), lg_last.float().unsqueeze(0), dim=-1
    ).item()
    return (1.0 + cos) / 2.0


def phi_proxy(h_last, n_cells=N_CELLS):
    """mitosis-form Φ★ = mean_{i<j}(1-cos(cell_i,cell_j)) × log(n+1).
    Same form as §168 phi_threshold_posthoc_probe."""
    d = h_last.shape[-1]
    if d % n_cells != 0:
        return None
    cells = h_last.view(n_cells, d // n_cells)
    norms = cells.norm(dim=-1, keepdim=True).clamp_min(1e-10)
    cells_n = cells / norms
    cos_mat = cells_n @ cells_n.T
    one_minus_cos = 1.0 - cos_mat
    mask = torch.triu(torch.ones_like(cos_mat), diagonal=1).bool()
    spread = float(one_minus_cos[mask].mean().item())
    return spread * math.log(n_cells + 1.0)


def measure_anchor(model, anchor, residual_cache):
    """Measure 4-modality signature for one anchor."""
    tier = anchor.get("knuth_tier", 0)
    ctx = torch.tensor([anchor_prefix_bytes(tier)], dtype=torch.long)
    la, lg = forward_with_residual(model, ctx, residual_cache)
    la_l = la[0, -1] if la.dim() == 3 else la[-1]
    lg_l = lg[0, -1] if lg.dim() == 3 else lg[-1]
    h_last = residual_cache[0][0, -1] if residual_cache[0].dim() == 3 else residual_cache[0][-1]

    # text modality
    top1 = int(la_l.argmax().item())
    top1_char = chr(top1) if 32 <= top1 < 127 else "?"

    # psi_direction modality
    psi_d = psi_direction(la_l, lg_l)

    # tension modality — std of la_last (proxy for per-token activation energy variance)
    tension = float(la_l.float().std().item())

    # phi_proxy modality — residual cell-partition spread
    phi = phi_proxy(h_last, N_CELLS)

    return {
        "anchor": anchor["file"],
        "tier": tier,
        "category": anchor.get("category", "?"),
        "top_emotion": anchor.get("top_emotion", "?"),
        "lane": anchor.get("lane", "?"),
        "text_top1": top1,
        "text_top1_char": top1_char,
        "psi_dir": psi_d,
        "tension": tension,
        "phi_proxy": phi,
    }


def measure_distinguishing(results):
    """For each modality, count distinct values across 11 anchors.

    distinguishing_ratio = (# distinct values) / (# anchors).
    1.0 = each anchor produces different value (perfectly distinguishing).
    1/N = all anchors collapse to same value (zero distinguishing).
    """
    n = len(results)
    out = {}
    for key in ("text_top1", "psi_dir", "tension", "phi_proxy"):
        vals = [r[key] for r in results]
        # round floats for clean distinct-count
        if isinstance(vals[0], float):
            vals_rounded = [round(v, 6) for v in vals]
        else:
            vals_rounded = vals
        n_distinct = len(set(vals_rounded))
        out[key] = {
            "n_distinct": n_distinct,
            "n_anchors": n,
            "distinguishing_ratio": n_distinct / n,
            "min": min(vals) if isinstance(vals[0], (int, float)) else None,
            "max": max(vals) if isinstance(vals[0], (int, float)) else None,
            "mean": sum(vals) / n if isinstance(vals[0], (int, float)) else None,
            "values_sample": vals[:5],
        }
    return out


def main():
    t0 = time.time()
    print("[s175] loading ckpt + 11 anchors ...")
    ckpt = os.path.join(S167A_DIR, "ckpt_s167a_fpreconnect.pt")
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
    print("[s175] load missing={} unexpected={}".format(len(msg.missing_keys), len(msg.unexpected_keys)))
    model.eval()

    # hook head_a for residual capture
    residual_cache = [None]
    def _hook(_m, inputs):
        residual_cache[0] = inputs[0].detach()
    h = model.head_a.register_forward_pre_hook(_hook)

    anchors = list_anchors()
    print("[s175] {} anchors found".format(len(anchors)))
    print()
    print("=== 4-modality signature per anchor ===")
    print("{:<35} {:<5} {:<14} {:<8} {:<10} {:<10} {:<12}".format(
        "anchor", "tier", "category", "top1", "psi_dir", "tension", "phi_proxy"))
    print("-" * 110)

    results = []
    for anchor in anchors:
        r = measure_anchor(model, anchor, residual_cache)
        results.append(r)
        print("{:<35} {:<5} {:<14} {:<8} {:<10.6f} {:<10.6f} {:<12.6f}".format(
            r["anchor"][:34], r["tier"], r["category"][:13],
            "{}({})".format(r["text_top1"], r["text_top1_char"]),
            r["psi_dir"], r["tension"], r["phi_proxy"]))

    h.remove()

    dist = measure_distinguishing(results)
    print()
    print("=== distinguishing ratio per modality (anchor-discrimination capability) ===")
    print("{:<12} {:<10} {:<8} {:<12} {}".format("modality", "n_distinct", "n", "ratio", "range"))
    print("-" * 80)
    for k in ("text_top1", "psi_dir", "tension", "phi_proxy"):
        d = dist[k]
        rng = "{} → {}".format(d["min"], d["max"]) if d["min"] is not None else "-"
        print("{:<12} {:<10} {:<8} {:<12.4f} {}".format(
            k, d["n_distinct"], d["n_anchors"], d["distinguishing_ratio"], rng))

    print()
    print("=== honestly EXCLUDED modalities ===")
    print("  image  — §7-clean encoder 부재 (S-module image encoder 미-wired)")
    print("  audio  — §7-clean encoder 부재 (S-module audio encoder 미-wired)")
    print("  video  — §7-clean encoder 부재")
    print("  per §109 C06 DESIGN-CLOSE-WITH-NARROW-OPEN")

    out = {
        "probe": "S175 KOSMOS 5-modality fire on S167-A ckpt × 11 anchors",
        "ckpt": "ckpt_s167a_fpreconnect.pt",
        "n_anchors": len(anchors),
        "measurable_modalities": ["text", "psi_dir", "tension", "phi_proxy"],
        "excluded_modalities": {
            "image": "§7-clean encoder absent (S-module unwired)",
            "audio": "§7-clean encoder absent (S-module unwired)",
            "video": "§7-clean encoder absent",
            "reference": "§109 C06 DESIGN-CLOSE-WITH-NARROW-OPEN",
        },
        "per_anchor_signature": results,
        "modality_distinguishing": dist,
        "wall_s": round(time.time() - t0, 2),
        "honest_carve_out": (
            "Modality distinguishing capability measured = anchor-discrimination "
            "ON A TRAINED CKPT. ratio = 1.0 means each anchor → different value. "
            "ratio = 1/N means all anchors collapse. NOT GOAL emergence (B-EMERGE-7); "
            "distinguishing capability ≠ V-SPONT honest coherent emission. image/audio/"
            "video modalities EXCLUDED per §109 DESIGN-CLOSE; payload pending status preserved."
        ),
    }
    out_p = "/Users/ghost/core/anima/HEXAD/UNCLASSIFIED/state/kosmos_modality_fire_s175_2026_05_20/result.json"
    with open(out_p, "w") as f:
        json.dump(out, f, indent=2, default=str)
    print()
    print("[s175] DONE wall={}s result→{}".format(out["wall_s"], out_p))


if __name__ == "__main__":
    main()
