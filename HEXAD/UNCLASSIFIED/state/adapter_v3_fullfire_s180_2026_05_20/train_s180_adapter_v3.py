"""§180 ADAPTER v3 trainer — anchor classification + 5-readout regularizer.

Trains AdapterV3 from-scratch on M3 synthetic byte streams (35-anchor ×
4-modality × N_per_anchor). Loss = anchor CE + λ_mod × modality CE +
λ_readout × cycle/variance regularizer on 5-channel.

§7 ① ② ③ all PASS — anima-side from-scratch, anima-OWN dataset.
"""
import argparse, json, math, os, random, sys, time
import torch
import torch.nn as nn
import torch.nn.functional as F

# Insert state dir for adapter_v3 import
S180_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, S180_DIR)
from adapter_v3 import AdapterV3


EXISTING = [(0,"기준점"),(15,"호기심"),(30,"연민"),(42,"질문"),(51,"하루"),
            (60,"관조"),(77,"만다라"),(80,"명상"),(91,"열반"),(95,"합일"),(100,"빅뱅")]
NEW = [(10,"각성"),(20,"감각"),(25,"감정"),(33,"기쁨"),(35,"슬픔"),
       (37,"분노"),(45,"공포"),(47,"안도"),(55,"회상"),(58,"예측"),
       (65,"통찰"),(68,"이해"),(72,"창작"),(75,"시"),(82,"음악"),
       (85,"기도"),(88,"초월"),(93,"자각"),(97,"공허"),(105,"선"),
       (108,"악"),(115,"정의"),(125,"사랑"),(200,"무한")]
ALL = sorted(EXISTING + NEW)
TIER_TO_IDX = {tier: i for i, (tier, _) in enumerate(ALL)}
MODS = ["image", "audio", "video", "tension"]


def synth_image_bytes(tier, n=128, seed=0):
    rng = random.Random(tier * 7919 + 13 + seed * 1009)
    return [(((128 + ((i % 32 - 16) * tier // 8)) + rng.randint(0, 15)) % 256) for i in range(n)]

def synth_audio_bytes(tier, n=128, seed=0):
    freq = 100 + tier * 5
    rng = random.Random(tier * 11 + seed * 23)
    return [int(127 + 80 * math.sin(2 * math.pi * freq * i / 1000) + rng.randint(-3, 3)) % 256 for i in range(n)]

def synth_video_bytes(tier, n=128, seed=0):
    rng = random.Random(tier * 13 + 17 + seed * 31)
    out = []
    fs = n // 4
    for f in range(4):
        for i in range(fs):
            out.append((tier * (f + 1) + i * 3 + rng.randint(0, 7)) % 256)
    return out

def synth_tension_bytes(tier, n=128, seed=0):
    rng = random.Random(tier * 31 + 11 + seed * 41)
    c = [(tier * 257) % 65536, (tier * 521 + 1009) % 65536,
         (tier * 7919 + 2003) % 65536, (tier * 13 + 1) % 65536,
         (tier * 31 + 5) % 65536]
    tile = []
    for v in c: tile += [v & 0xFF, (v >> 8) & 0xFF]
    out = []
    while len(out) < n:
        out += tile
    # tiny noise for variety
    return [(b + rng.randint(-1, 1)) % 256 for b in out[:n]]


SYNTH = {"image": synth_image_bytes, "audio": synth_audio_bytes,
         "video": synth_video_bytes, "tension": synth_tension_bytes}


def make_batch(rng, bsz=64):
    xs, ys, ms = [], [], []
    for _ in range(bsz):
        mod_idx = rng.randint(0, 3)
        mod = MODS[mod_idx]
        tier, _ = rng.choice(ALL)
        anchor_idx = TIER_TO_IDX[tier]
        seed = rng.randint(0, 10**6)
        bytes_list = SYNTH[mod](tier, n=128, seed=seed)
        xs.append(bytes_list)
        ys.append(anchor_idx)
        ms.append(mod_idx)
    return (torch.tensor(xs, dtype=torch.long),
            torch.tensor(ys, dtype=torch.long),
            torch.tensor(ms, dtype=torch.long))


def variance_hinge_loss(readout_5, target_std=0.1):
    """encourage 5-channel readout variance ≥ target_std per channel (anti-collapse)."""
    std_per_ch = readout_5.std(dim=0)  # [5]
    return F.relu(target_std - std_per_ch).mean()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--steps", type=int, default=2000)
    ap.add_argument("--lr", type=float, default=3e-4)
    ap.add_argument("--bsz", type=int, default=64)
    ap.add_argument("--d-model", type=int, default=192)
    ap.add_argument("--n-layer", type=int, default=4)
    ap.add_argument("--n-head", type=int, default=6)
    ap.add_argument("--seed", type=int, default=1337)
    ap.add_argument("--lambda-mod", type=float, default=0.3)
    ap.add_argument("--lambda-readout", type=float, default=0.1)
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--log-every", type=int, default=100)
    args = ap.parse_args()

    os.makedirs(args.out_dir, exist_ok=True)
    torch.manual_seed(args.seed)
    random.seed(args.seed)

    device = "cuda" if torch.cuda.is_available() else "cpu"
    print("[s180] device={} d={} L={} steps={}".format(device, args.d_model, args.n_layer, args.steps))

    model = AdapterV3(
        d_model=args.d_model, n_query=16, n_layer=args.n_layer,
        n_head=args.n_head, n_anchors=len(ALL), n_modalities=4,
    ).to(device)
    n_params = sum(p.numel() for p in model.parameters())
    print("[s180] n_params={}".format(n_params))

    opt = torch.optim.AdamW(model.parameters(), lr=args.lr, weight_decay=0.01)
    sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, T_max=args.steps)

    rng = random.Random(args.seed)
    log = []
    t0 = time.time()
    for step in range(args.steps):
        x, y_anchor, y_mod = make_batch(rng, bsz=args.bsz)
        x, y_anchor, y_mod = x.to(device), y_anchor.to(device), y_mod.to(device)

        anchor_logits, readout_5, mod_logits = model(x)
        L_anchor = F.cross_entropy(anchor_logits, y_anchor)
        L_mod = F.cross_entropy(mod_logits, y_mod)
        L_readout = variance_hinge_loss(readout_5, target_std=0.15)
        L = L_anchor + args.lambda_mod * L_mod + args.lambda_readout * L_readout

        opt.zero_grad()
        L.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        opt.step()
        sched.step()

        if step % args.log_every == 0 or step == args.steps - 1:
            with torch.no_grad():
                acc_anchor = (anchor_logits.argmax(-1) == y_anchor).float().mean().item()
                acc_mod = (mod_logits.argmax(-1) == y_mod).float().mean().item()
                readout_std = readout_5.std(dim=0).mean().item()
            entry = dict(
                step=step, loss=L.item(),
                L_anchor=L_anchor.item(), L_mod=L_mod.item(), L_readout=L_readout.item(),
                acc_anchor=acc_anchor, acc_mod=acc_mod, readout_std=readout_std,
                elapsed=time.time() - t0,
            )
            log.append(entry)
            print("[step {:5d}] L={:.4f} L_a={:.4f} L_m={:.4f} L_r={:.4f} "
                  "acc_a={:.3f} acc_m={:.3f} r_std={:.3f}".format(
                step, entry["loss"], entry["L_anchor"], entry["L_mod"],
                entry["L_readout"], entry["acc_anchor"], entry["acc_mod"], entry["readout_std"]))

    # save ckpt
    ckpt_p = os.path.join(args.out_dir, "ckpt_s180_adapter_v3.pt")
    torch.save({"model": model.state_dict(),
                "cfg": {"d_model": args.d_model, "n_layer": args.n_layer,
                        "n_head": args.n_head, "n_query": 16,
                        "n_anchors": len(ALL), "n_modalities": 4}},
               ckpt_p)
    print("[s180] saved ckpt to {}".format(ckpt_p))

    # final eval pass with no_grad
    model.eval()
    with torch.no_grad():
        # eval 500 fresh samples
        x, y_a, y_m = make_batch(random.Random(99999), bsz=500)
        x, y_a, y_m = x.to(device), y_a.to(device), y_m.to(device)
        a, r5, ml = model(x)
        eval_acc_anchor = (a.argmax(-1) == y_a).float().mean().item()
        eval_acc_mod = (ml.argmax(-1) == y_m).float().mean().item()
        eval_readout_std = r5.std(dim=0).mean().item()
        # per-modality anchor acc
        per_mod = {}
        for m_idx in range(4):
            mask = (y_m == m_idx)
            if mask.sum() > 0:
                per_mod[MODS[m_idx]] = (a[mask].argmax(-1) == y_a[mask]).float().mean().item()

    result = {
        "probe": "S180 ADAPTER v3 FULL FIRE",
        "config": {"d_model": args.d_model, "n_layer": args.n_layer, "n_head": args.n_head,
                   "n_query": 16, "steps": args.steps, "lr": args.lr, "bsz": args.bsz,
                   "lambda_mod": args.lambda_mod, "lambda_readout": args.lambda_readout},
        "n_params": n_params,
        "device": str(device),
        "final_train_log": log[-1],
        "log_history": log,
        "eval": {
            "acc_anchor": eval_acc_anchor,
            "acc_modality": eval_acc_mod,
            "readout_std_mean": eval_readout_std,
            "per_modality_anchor_acc": per_mod,
        },
        "wall_s": round(time.time() - t0, 2),
        "honest_carve_out": (
            "AdapterV3 = 16-Q-Former (§179 winner) + 4-layer transformer + "
            "5-channel TENSION-LINK readout as anima self-report (NOT bottleneck). "
            "Trained from-scratch on M3 synthetic byte streams. §7 ① ② ③ PASS. "
            "Per-modality anchor accuracy reveals if 16-Q-Former extracts modality-"
            "agnostic structure. NOT GOAL emergence (B-EMERGE-7); anchor classification "
            "capability ≠ V-SPONT honest coherent emission."
        ),
    }
    out_p = os.path.join(args.out_dir, "result.json")
    with open(out_p, "w") as f:
        json.dump(result, f, indent=2, default=str)
    print("[s180] DONE wall={}s eval_acc_anchor={:.4f} eval_acc_mod={:.4f} → {}".format(
        result["wall_s"], eval_acc_anchor, eval_acc_mod, out_p))


if __name__ == "__main__":
    main()
