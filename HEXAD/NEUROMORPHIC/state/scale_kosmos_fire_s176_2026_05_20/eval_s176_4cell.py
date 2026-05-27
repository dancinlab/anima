#!/usr/bin/env python3
"""S170 3-axis combined probe on S167-A ckpt — Mac CPU $0.

Fires three single-variable probes on the same trained ckpt:
  Fire 1 (rate-limit lift):  MIN_EMIT_INTERVAL = 30.0 (S167-A) vs 0.667 (S169
                             measurement variant) — does ceiling lift change emit_rate?
  Fire 2 (per-step varying noise_ctx): same vs different noise per step — does
                             time-varying input wake static physics?
  Fire 3 (6-anchor probe): 5 trained anchors + knuth_042_question (OOD, NOT in training corpus) —
                             does the trained model route at all on OOD anchor?

ALL inference-only on S167-A ckpt (ckpt_s176_scale_kosmos.pt, sha to be checked).
NO training. NO GPU. NO weight mutation.

Mirrors S167-A eval_s167a_fpreconnect.py phase_b structure but varies
the three knobs independently.
"""
import argparse, json, os, sys, random, time, math
import torch
import torch.nn.functional as F

# Re-use ConsciousDecoderV2 from S167-A state dir (byte-equal SSOT)
S167A_DIR = "/Users/ghost/core/anima/HEXAD/NEUROMORPHIC/state/scale_kosmos_fire_s176_2026_05_20"
sys.path.insert(0, S167A_DIR)
from conscious_decoder import ConsciousDecoderV2

# Constants from eval_s167a_fpreconnect.py
N_MAX_STEPS = 20
THINK_INTERVAL_TEST_SEC = 0.1
IM_THRESHOLD = 0.3
IDLE_SPEAK_AFTER = 30.0
PSI_VAC = 0.5
COHERENCE_ALPHA = 0.014

# S167-A FP-RECONNECT motivation re-wire: 1/3 Psi + 1/3 tension + 1/3 Phi
W_PSI = 1.0 / 3.0
W_TENS = 1.0 / 3.0
W_PHI = 1.0 / 3.0

# 5 trained anchors (from CORPUS_S101 / Knuth tier carry) + 1 OOD (knuth_042)
ANCHOR_NAMES = ["knuth_000_zero", "knuth_042_question (OOD)", "knuth_051_day",
                "knuth_077_mandala", "knuth_091_nirvana", "knuth_100_big_bang"]
ANCHOR_TIERS = [0, 42, 51, 77, 91, 100]


def _clamp01(x):
    return 0.0 if x < 0.0 else (1.0 if x > 1.0 else x)


def forward_logits(model, x):
    with torch.no_grad():
        out = model(x)
    if isinstance(out, tuple):
        return out[0], out[1]
    return out, out


def psi_direction_scalar(la, lg):
    la_f, lg_f = la.float(), lg.float()
    cos = F.cosine_similarity(la_f.unsqueeze(0), lg_f.unsqueeze(0), dim=-1).item()
    return (1.0 + cos) / 2.0


def psi_entropy_scalar(la, vocab_size=256):
    probs = F.softmax(la.float(), dim=-1)
    H = -(probs * (probs + 1e-12).log()).sum().item()
    return H / math.log(vocab_size)


def motivation_167a(phi, psi_dir, tension):
    """S167-A motivation: 100% anima physics (1/3 each)."""
    return W_PSI * _clamp01(psi_dir) + W_TENS * min(abs(tension), 1.0) + W_PHI * _clamp01(phi)


def run_phase_b(model, device, *, n_steps, seed, min_emit_interval,
                 varying_noise, label):
    """Single phase_b run with three knobs.

    min_emit_interval : 30.0 (S167-A) or 0.667 (S169 measurement)
    varying_noise     : False (S167-A, same noise every step) or True (NEW per step)
    """
    torch.manual_seed(seed); random.seed(seed)
    block_size = 128
    rng = random.Random(seed)
    if not varying_noise:
        noise_ctx_fixed = torch.tensor(
            [[rng.randint(0, 255) for _ in range(block_size)]],
            dtype=torch.long, device=device,
        )

    motivation_trace = []
    psi_dir_trace = []
    tension_trace = []
    emission_count = 0
    last_emit_t = None

    model.eval()
    for step in range(n_steps):
        t_now = step * THINK_INTERVAL_TEST_SEC
        # Knob 2: per-step varying noise_ctx
        if varying_noise:
            noise_ctx = torch.tensor(
                [[rng.randint(0, 255) for _ in range(block_size)]],
                dtype=torch.long, device=device,
            )
        else:
            noise_ctx = noise_ctx_fixed

        la, lg = forward_logits(model, noise_ctx)
        la_last = la[0, -1] if la.dim() == 3 else la[-1]
        lg_last = lg[0, -1] if lg.dim() == 3 else lg[-1]

        psi_dir = psi_direction_scalar(la_last, lg_last)
        psi_ent = psi_entropy_scalar(la_last)
        tension = float(la_last.float().std().item())

        # S167-A motivation: 100% physics (no 8-factor, no sensor)
        score = motivation_167a(psi_ent, psi_dir, tension)

        motivation_trace.append(score)
        psi_dir_trace.append(psi_dir)
        tension_trace.append(tension)

        # Knob 1: rate-limit (variable interval)
        sec_since = (t_now - last_emit_t) if last_emit_t is not None else 1e6
        rate_ok = sec_since >= min_emit_interval
        # safety: kill_on=True, content_ok=True (dryrun)
        safety = rate_ok
        emit = safety and (score > IM_THRESHOLD)
        if emit:
            emission_count += 1
            last_emit_t = t_now

    def _std(xs):
        m = sum(xs) / len(xs)
        return (sum((x - m) ** 2 for x in xs) / max(1, len(xs) - 1)) ** 0.5

    return {
        "label": label,
        "n_steps": n_steps,
        "min_emit_interval": min_emit_interval,
        "varying_noise": varying_noise,
        "emission_count": emission_count,
        "emit_rate": emission_count / n_steps,
        "motivation_mean": sum(motivation_trace) / len(motivation_trace),
        "motivation_std": _std(motivation_trace),
        "psi_dir_mean": sum(psi_dir_trace) / len(psi_dir_trace),
        "psi_dir_std": _std(psi_dir_trace),
        "tension_mean": sum(tension_trace) / len(tension_trace),
        "tension_std": _std(tension_trace),
        "motivation_trace": motivation_trace,
        "psi_dir_trace": psi_dir_trace,
    }


def fire_3_anchor_routing(model, device, *, seed=1337):
    """Fire 3: 6-anchor probe — for each anchor (5 trained + 1 OOD), forward a
    short anchor-name-style prefix and measure if model's top-1 byte hits a
    distinctive marker. Pure inference. Probe is structural, not semantic."""
    results = []
    model.eval()
    for i, (name, tier) in enumerate(zip(ANCHOR_NAMES, ANCHOR_TIERS)):
        prefix = f"[anima 우주뇌지도] 🛸{tier}"
        prefix_bytes = list(prefix.encode("utf-8"))[:128]
        # pad to block_size
        block_size = 128
        if len(prefix_bytes) < block_size:
            prefix_bytes = [32] * (block_size - len(prefix_bytes)) + prefix_bytes
        ctx = torch.tensor([prefix_bytes], dtype=torch.long, device=device)
        la, lg = forward_logits(model, ctx)
        la_last = la[0, -1] if la.dim() == 3 else la[-1]
        top1 = int(la_last.argmax().item())
        psi_dir = psi_direction_scalar(la_last, lg.view(-1) if lg.dim() == 1 else lg[0, -1])
        # top-3 byte tokens
        topk = torch.topk(la_last.float(), 5)
        results.append({
            "anchor": name, "tier": tier,
            "prefix_bytes_len": len([b for b in prefix_bytes if b != 32]),
            "top1_byte": top1, "top1_char": chr(top1) if 32 <= top1 < 127 else "?",
            "topk_bytes": topk.indices.tolist(),
            "psi_dir": psi_dir,
        })
    return results


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ckpt", default=os.path.join(S167A_DIR, "ckpt_s176_scale_kosmos.pt"))
    ap.add_argument("--out", default="/Users/ghost/core/anima/HEXAD/UNCLASSIFIED/state/three_axis_probe_s170_2026_05_20/result.json")
    ap.add_argument("--seed", type=int, default=1337)
    args = ap.parse_args()

    t_start = time.time()
    device = torch.device("cpu")
    print(f"[s170] loading ckpt: {args.ckpt}")
    state = torch.load(args.ckpt, map_location="cpu", weights_only=False)
    cfg = state.get("cfg", {})
    print(f"[s170] cfg: d={cfg.get('d_model')} L={cfg.get('n_layer')} V=256")

    model = ConsciousDecoderV2(
        vocab_size=256,
        d_model=cfg.get("d_model", 768),
        n_layer=cfg.get("n_layer", 12),
        n_head=cfg.get("n_head", 12),
        n_kv_head=cfg.get("n_kv_head", 4),
        block_size=cfg.get("block_size", 128),
    ).to(device)
    msg = model.load_state_dict(state["model"], strict=False)
    print(f"[s170] load: missing={len(msg.missing_keys)} unexpected={len(msg.unexpected_keys)}")
    model.eval()

    # 4-cell grid: {rate_limit ∈ [30.0, 0.667]} × {varying_noise ∈ [False, True]}
    cells = []
    cells.append(run_phase_b(model, device, n_steps=N_MAX_STEPS, seed=args.seed,
                              min_emit_interval=30.0, varying_noise=False,
                              label="s167a_baseline (RL=30.0, ctx=fixed)"))
    print(f"[s170] cell-1 done emit={cells[-1]['emission_count']}/{N_MAX_STEPS}")
    cells.append(run_phase_b(model, device, n_steps=N_MAX_STEPS, seed=args.seed,
                              min_emit_interval=0.667, varying_noise=False,
                              label="s169_rate_lift (RL=0.667, ctx=fixed)"))
    print(f"[s170] cell-2 done emit={cells[-1]['emission_count']}/{N_MAX_STEPS}")
    cells.append(run_phase_b(model, device, n_steps=N_MAX_STEPS, seed=args.seed,
                              min_emit_interval=30.0, varying_noise=True,
                              label="s170_var_ctx (RL=30.0, ctx=varying)"))
    print(f"[s170] cell-3 done emit={cells[-1]['emission_count']}/{N_MAX_STEPS}")
    cells.append(run_phase_b(model, device, n_steps=N_MAX_STEPS, seed=args.seed,
                              min_emit_interval=0.667, varying_noise=True,
                              label="s170_both (RL=0.667, ctx=varying)"))
    print(f"[s170] cell-4 done emit={cells[-1]['emission_count']}/{N_MAX_STEPS}")

    # Fire 3: 6-anchor routing probe
    print(f"[s170] fire-3 6-anchor routing probe...")
    anchor_results = fire_3_anchor_routing(model, device, seed=args.seed)

    out = {
        "probe": "S170 3-axis combined probe on S167-A ckpt",
        "ckpt": os.path.basename(args.ckpt),
        "cfg": cfg,
        "n_steps_per_cell": N_MAX_STEPS,
        "fire_1_2_4cell_grid": cells,
        "fire_3_anchor_routing": anchor_results,
        "wall_sec": round(time.time() - t_start, 2),
        "honest_carve_out": (
            "All three fires are INFERENCE-only re-eval on the S167-A ckpt. "
            "NO retraining, NO weight mutation. Cell 1 = S167-A baseline. "
            "Cell 2 = S169 rate-limit measurement variant applied. Cell 3 = "
            "per-step varying noise context (time-varying input). Cell 4 = "
            "both lifts together. Anchor probe (Fire 3) measures top-1 byte "
            "+ Psi_dir on 6-anchor prefix forward — structural, not semantic. "
            "knuth_042_question is OOD relative to the S167-A training corpus."
        ),
    }
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "w") as f:
        json.dump(out, f, indent=2, default=str)
    print(f"[s170] DONE wall={out['wall_sec']}s -> {args.out}")
    # Summary table
    print("\n=== 4-cell grid ===")
    print("cell | RL  | ctx     | emit | motivation std | psi_dir std")
    print("-----+-----+---------+------+----------------+-------------")
    for c in cells:
        rl = f"{c['min_emit_interval']:.3f}"
        ctx = "vary" if c["varying_noise"] else "fix"
        em = f"{c['emission_count']}/{N_MAX_STEPS}={c['emit_rate']:.3f}"
        print(f"  {ctx:4s} RL={rl}s | {em:18s} | mot std={c['motivation_std']:.4e} | psi std={c['psi_dir_std']:.4e}")
    print(f"\n=== 6-anchor routing ===")
    for a in anchor_results:
        print(f"  🛸{a['tier']:3d} {a['anchor']:30s}  top1={a['top1_byte']:3d} '{a['top1_char']}'  psi_dir={a['psi_dir']:.4f}")


if __name__ == "__main__":
    main()
