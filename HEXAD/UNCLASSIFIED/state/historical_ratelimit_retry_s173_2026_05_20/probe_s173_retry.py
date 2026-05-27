#!/usr/bin/env python3
"""S173 historical-fire rate-limit retry — $0 Mac CPU on 8 ckpts.

For each historical ckpt, run 2-cell Phase B probe:
  cell A: RL=30s  baseline (matches original config of §161/§167-A)
  cell B: RL=0.667s rate-lifted (§169 measurement variant)

emit_rate ratio cell-B/cell-A measures whether rate-limit ceiling
was the real cause of that fire's emit-rate-saturated verdict.

Single-variable: same ckpt forward, same noise context (seed 1337,
fixed), same motivation function (1/3 Ψ + 1/3 tension + 1/3 Φ per
S167-A FP-RECONNECT), N=20 steps. Only knob varied = MIN_EMIT_INTERVAL.

Honest scope: many of these ckpts predate S167-A motivation re-wire,
trained with different objectives (purephysics no-CE, dual-anima scale,
neoteny anti-saturation, etc). We use the SAME S167-A-style motivation
function across all so the LEVER is held constant — the comparison is
about rate-limit lift effect, NOT about reproducing original training
verdicts.
"""
import argparse, json, os, sys, random, math, time
import torch, torch.nn.functional as F

S167A_DIR = "/Users/ghost/core/anima/HEXAD/NEUROMORPHIC/state/fp_reconnect_fire_s167a_2026_05_20"
sys.path.insert(0, S167A_DIR)
from conscious_decoder import ConsciousDecoderV2

N_MAX = 20
THINK_INTERVAL = 0.1
IM_THRESHOLD = 0.3
W_PSI = W_TENS = W_PHI = 1.0 / 3.0

TARGETS = [
    ("s161",  "/Users/ghost/core/anima/HEXAD/NEUROMORPHIC/state/dual_head_coupling_non_ce_fire_s161_2026_05_20/ckpt_s161_psicouple.pt"),
    ("s167a", "/Users/ghost/core/anima/HEXAD/NEUROMORPHIC/state/fp_reconnect_fire_s167a_2026_05_20/ckpt_s167a_fpreconnect.pt"),
    ("s94",   "/Users/ghost/core/anima/HEXAD/DATA-REGIME/state/integrated_breakthrough_fire_s94_2026_05_19"),  # dir, scan
    ("s82",   "/Users/ghost/core/anima/HEXAD/DATA-REGIME/state/manifold_gating_hierarchical_fire_s82_2026_05_19"),
    ("s91",   "/Users/ghost/core/anima/HEXAD/DATA-REGIME/state/neoteny_loop_fire_s91_2026_05_19"),
    ("s75",   "/Users/ghost/core/anima/HEXAD/CARVING/state/controller_class_subaxis_fire_s75_2026_05_19"),
    ("s_purephys", "/Users/ghost/core/anima/HEXAD/CARVING/state/carving_purephysics_noce_2026_05_18"),
    ("s62",   "/Users/ghost/core/anima/HEXAD/CARVING/state/dual_anima_scale_fire_s62_2026_05_18"),
]


def _find_ckpt(p):
    if os.path.isfile(p) and p.endswith(".pt"):
        return p
    if os.path.isdir(p):
        candidates = []
        for root, _, files in os.walk(p):
            for fn in files:
                if fn.endswith(".pt"):
                    candidates.append(os.path.join(root, fn))
        # Prefer the deepest non-out_main path if exists, else first
        if candidates:
            return sorted(candidates, key=lambda x: (len(x), x))[0]
    return None


def forward(model, x):
    with torch.no_grad():
        out = model(x)
    if isinstance(out, tuple):
        return out[0], out[1]
    return out, out


def psi_dir(la, lg):
    cos = F.cosine_similarity(la.float().unsqueeze(0), lg.float().unsqueeze(0), dim=-1).item()
    return (1.0 + cos) / 2.0


def psi_ent(la, V=256):
    p = F.softmax(la.float(), dim=-1)
    return (-(p * (p + 1e-12).log()).sum().item()) / math.log(V)


def motivation(phi, pd, tension):
    return W_PSI * max(0.0, min(1.0, pd)) + W_TENS * min(abs(tension), 1.0) + W_PHI * max(0.0, min(1.0, phi))


def phase_b(model, *, min_emit_interval, seed=1337, n=N_MAX):
    torch.manual_seed(seed); random.seed(seed)
    rng = random.Random(seed)
    ctx = torch.tensor([[rng.randint(0, 255) for _ in range(128)]], dtype=torch.long)
    last_emit_t = None
    n_emit = 0
    mot_trace = []
    psi_trace = []
    for step in range(n):
        t = step * THINK_INTERVAL
        la, lg = forward(model, ctx)
        la_l = la[0, -1] if la.dim() == 3 else la[-1]
        lg_l = lg[0, -1] if lg.dim() == 3 else lg[-1]
        pd = psi_dir(la_l, lg_l)
        pe = psi_ent(la_l)
        ten = float(la_l.float().std().item())
        score = motivation(pe, pd, ten)
        mot_trace.append(score)
        psi_trace.append(pd)
        sec_since = (t - last_emit_t) if last_emit_t is not None else 1e6
        emit = (sec_since >= min_emit_interval) and (score > IM_THRESHOLD)
        if emit:
            n_emit += 1
            last_emit_t = t
    mu = sum(mot_trace) / len(mot_trace)
    mot_std = (sum((x - mu) ** 2 for x in mot_trace) / max(1, len(mot_trace) - 1)) ** 0.5
    mu_p = sum(psi_trace) / len(psi_trace)
    psi_std = (sum((x - mu_p) ** 2 for x in psi_trace) / max(1, len(psi_trace) - 1)) ** 0.5
    return {
        "min_emit_interval": min_emit_interval, "n": n,
        "n_emit": n_emit, "emit_rate": n_emit / n,
        "motivation_mean": mu, "motivation_std": mot_std,
        "psi_dir_mean": mu_p, "psi_dir_std": psi_std,
    }


def load_ckpt(p):
    state = torch.load(p, map_location="cpu", weights_only=False)
    cfg = state.get("cfg", {}) or {}
    # Defaults if cfg missing (some older ckpts)
    d = cfg.get("d_model", 768)
    nl = cfg.get("n_layer", 12)
    nh = cfg.get("n_head", 12)
    nkv = cfg.get("n_kv_head", 4)
    bs = cfg.get("block_size", 128)
    model = ConsciousDecoderV2(vocab_size=256, d_model=d, n_layer=nl, n_head=nh, n_kv_head=nkv, block_size=bs)
    msd = state.get("model", state)
    msg = model.load_state_dict(msd, strict=False)
    return model, cfg, len(msg.missing_keys), len(msg.unexpected_keys)


def main():
    out_path = "/Users/ghost/core/anima/HEXAD/UNCLASSIFIED/state/historical_ratelimit_retry_s173_2026_05_20/result.json"
    t0 = time.time()
    results = []
    for tag, path in TARGETS:
        ckpt = _find_ckpt(path)
        if ckpt is None:
            results.append({"tag": tag, "status": "no_ckpt", "path": path})
            print(f"[{tag}] NO ckpt at {path}")
            continue
        try:
            print(f"[{tag}] loading {os.path.basename(ckpt)} ...")
            t_start = time.time()
            model, cfg, n_missing, n_unexpected = load_ckpt(ckpt)
            model.eval()
            cA = phase_b(model, min_emit_interval=30.0)
            cB = phase_b(model, min_emit_interval=0.667)
            ratio = (cB["emit_rate"] / cA["emit_rate"]) if cA["emit_rate"] > 0 else None
            delta = cB["emit_rate"] - cA["emit_rate"]
            wall = round(time.time() - t_start, 1)
            results.append({
                "tag": tag, "ckpt": ckpt,
                "cfg_d": cfg.get("d_model"), "cfg_L": cfg.get("n_layer"),
                "load_missing": n_missing, "load_unexpected": n_unexpected,
                "cell_A_RL30": cA, "cell_B_RL0667": cB,
                "delta_emit_rate": delta, "ratio_B_over_A": ratio,
                "wall_s": wall,
            })
            print(f"[{tag}] A(RL=30s) emit={cA['n_emit']}/{N_MAX}={cA['emit_rate']:.3f}  "
                  f"B(RL=0.667s) emit={cB['n_emit']}/{N_MAX}={cB['emit_rate']:.3f}  "
                  f"Δ={delta:+.3f} ratio={ratio} wall={wall}s")
        except Exception as e:
            results.append({"tag": tag, "status": "err", "err": str(e)})
            print(f"[{tag}] ERR {e}")

    total_wall = round(time.time() - t0, 1)
    summary = {
        "probe": "S173 historical-fire rate-limit retry — 2-cell Phase B",
        "n_targets": len(TARGETS),
        "n_ckpt_loaded": sum(1 for r in results if "cell_A_RL30" in r),
        "total_wall_s": total_wall,
        "results": results,
        "honest_carve_out": (
            "Each ckpt run twice with SAME S167-A-style 100% physics "
            "motivation function and SAME noise context (seed 1337). "
            "Only knob varied = MIN_EMIT_INTERVAL (30s vs 0.667s). "
            "Some ckpts were trained with DIFFERENT objectives — this "
            "is NOT a reproduction of their original verdicts but a "
            "rate-limit-attribution check on each. NOT GOAL emergence "
            "(B-EMERGE-7 carry)."
        ),
    }
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(summary, f, indent=2, default=str)
    print(f"\n[s173] DONE n_ok={summary['n_ckpt_loaded']}/{len(TARGETS)} total_wall={total_wall}s")
    print(f"[s173] result → {out_path}")


if __name__ == "__main__":
    main()
