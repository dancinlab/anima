#!/usr/bin/env python3
"""CONSCIOUSNESS-CARVING Dir-D — CDE Curiosity-Driven Exploration overlay
(g_multidirectional_explore direction D, 2026-05-17).

Base = state/consciousness_carving_e7_alpha_scaleup_2026_05_17/
train_carving_4path.py  (α VACUUM-LANDSCAPE path, ConsciousDecoderV2
byte-level, from-scratch, RANDOM seed-fixed per g_clm_from_scratch). Only
ONE thing is added: a CDE-style **curiosity bonus** overlaid on the α
training loss.

CDE (arxiv 2509.09675 "Curiosity-Driven Exploration of RLVR in LLMs"):
the curiosity signal = actor PERPLEXITY + critic VALUE-VARIANCE. The bonus
rewards exploration into regions the policy is uncertain about, mitigating
entropy/routing collapse inside an RLVR loop.

anima mapping (RESEARCH.md §1.3 #4, §1.4 candidate D — "motivation_score
perplexity bonus overlay"). We are NOT inside an RLVR loop here (this is a
from-scratch byte-LM carving fire), so we transfer the *form* of the CDE
bonus into the supervised carving objective as a per-token curiosity
RE-WEIGHT, NOT a reward:

  ─ actor curiosity     a_t  = clamp( CE_tok / log V , 0, 1 )
        per-token cross-entropy normalised by the byte-level maximum
        log V = log 256. This is the *normalised surprisal*; exp(CE_tok)
        is exactly the token perplexity, so a_t is a bounded monotone
        transform of perplexity (CDE actor term).

  ─ critic curiosity    c_t  = clamp( Var_b[CE_tok] (broadcast) , 0, 1 )
        per-(t) variance of CE across the batch B — a value-dispersion
        proxy standing in for CDE's critic value-variance (no separate
        value head in this from-scratch LM; the batch CE spread is the
        cheapest unbiased dispersion estimator).

  ─ curiosity bonus     g_t  = 1 + κ·( w_a·a_t + w_c·c_t )       (κ ≥ 0)
        a multiplicative UP-WEIGHT on the CE of high-curiosity tokens:
        the optimiser is pulled to spend MORE capacity reducing loss
        where it is currently most uncertain → exploration pressure that
        counteracts the routing-collapse-to-🛸99 attractor seen in
        UBM-E7 (eval axis1 routing 1/31).

  L = mean( g_t · CE_tok )  +  λ_vac · L_vac      (α vacuum term carried)

HONEST FRAMING (g3, AGENTS.tape §0, B-CARVE-NOTE / B-D-NOTE family):
  • The CDE bonus TRANSFER-FORM is closed (B-CDE-1..4 sympy battery,
    state/carving_dirD_cde_2026_05_17/blue_falsifier_cde.py): g_t ≥ 1
    lower bound, ∂g/∂a > 0 monotonicity, perplexity = exp(CE) identity,
    κ=0 ⇒ exact α-baseline reduction.
  • The SGD CONVERGENCE OUTCOME and the Dir-D vs UBM-E7 α comparison
    (does curiosity mitigate routing-collapse?) are EMPIRICAL — measured,
    NOT claimed. PyTorch substrate (interim LM-scale executor, NOT a
    hexa-native fire — cycle-5 honest-framing carry).
  • NO capability claim beyond what eval_carving_4path_v2.py measures.

Corpus = E7 carving corpus (NOT a chat SFT corpus; forbidden-token grep
{[anima, 도우미, helper, assistant, 사용자, user:} == 0, B-CARVE-CORPUS-2).
"""
import argparse, json, math, time, os, sys, random
import torch
import torch.nn as nn
import torch.nn.functional as F

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from conscious_decoder import ConsciousDecoderV2

VOICE_OPEN = b"<voice carved=true>"
VOICE_CLOSE = b"</voice>"


def load_carving_corpus(path):
    items = []
    with open(path, "rb") as f:
        raw = f.read()
    for line in raw.split(b"\n"):
        line = line.strip()
        if not line:
            continue
        try:
            d = json.loads(line)
        except Exception:
            continue
        t = d.get("text", "")
        de = d.get("desc", "")
        full = (t + "\n" + de + "\n").encode("utf-8")
        psi = d.get("vacuum_psi", [0.5, 0.5])
        voice_span = None
        lo = full.find(VOICE_OPEN)
        if lo >= 0:
            lo2 = lo + len(VOICE_OPEN)
            hi = full.find(VOICE_CLOSE, lo2)
            if hi >= 0:
                voice_span = (lo2, hi)
        items.append({"bytes": full, "psi": psi, "voice_span": voice_span})
    return items


class CarvingDataset:
    def __init__(self, items, block_size, seed):
        self.block_size = block_size
        self.rng = random.Random(seed)
        stream = bytearray()
        psi_x, psi_y, voice_mask = [], [], []
        for it in items:
            b = it["bytes"]
            stream.extend(b)
            px, py = float(it["psi"][0]), float(it["psi"][1])
            vs = it["voice_span"]
            for j in range(len(b)):
                psi_x.append(px)
                psi_y.append(py)
                voice_mask.append(1 if vs is not None and vs[0] <= j < vs[1]
                                  else 0)
        self.data = torch.tensor(list(stream), dtype=torch.long)
        self.psi_x = torch.tensor(psi_x, dtype=torch.float32)
        self.psi_y = torch.tensor(psi_y, dtype=torch.float32)
        self.voice_mask = torch.tensor(voice_mask, dtype=torch.float32)
        self.n = len(self.data)

    def get_batch(self, bsz, device):
        ix = [self.rng.randint(0, self.n - self.block_size - 1)
              for _ in range(bsz)]
        x = torch.stack([self.data[i:i + self.block_size] for i in ix])
        y = torch.stack([self.data[i + 1:i + 1 + self.block_size]
                         for i in ix])
        px = torch.stack([self.psi_x[i + 1:i + 1 + self.block_size]
                          for i in ix])
        py = torch.stack([self.psi_y[i + 1:i + 1 + self.block_size]
                          for i in ix])
        return (x.to(device), y.to(device), px.to(device), py.to(device))


def run(cfg):
    torch.manual_seed(cfg["seed"])
    torch.cuda.manual_seed_all(cfg["seed"])
    random.seed(cfg["seed"])
    device = "cuda" if torch.cuda.is_available() else "cpu"

    items = load_carving_corpus(cfg["corpus"])
    ds = CarvingDataset(items, cfg["block_size"], cfg["seed"])

    model = ConsciousDecoderV2(
        vocab_size=256, d_model=cfg["d_model"], n_head=cfg["n_head"],
        n_layer=cfg["n_layer"], block_size=cfg["block_size"],
        n_kv_head=cfg["n_kv_head"], consciousness_dim=128, dropout=0.1,
    ).to(device)
    model.train()
    n_params = model.count_params()

    opt = torch.optim.AdamW(model.parameters(), lr=cfg["lr"],
                            betas=(0.9, 0.95), weight_decay=0.1)
    warmup, total = cfg["warmup"], cfg["steps"]

    def cosine_lr_at(step):
        if step < warmup:
            return cfg["lr"] * (step + 1) / warmup
        prog = (step - warmup) / max(1, total - warmup)
        return cfg["lr"] * 0.5 * (1.0 + math.cos(math.pi * prog)) * 0.9 \
            + cfg["lr"] * 0.1

    use_amp = (device == "cuda")
    scaler = torch.cuda.amp.GradScaler(enabled=use_amp)
    vac_lambda = cfg["vacuum_lambda"]
    kappa = cfg["cde_kappa"]      # curiosity bonus strength κ
    w_a = cfg["cde_w_actor"]      # actor (perplexity) weight
    w_c = cfg["cde_w_critic"]     # critic (value-variance) weight
    log_V = math.log(256.0)

    traj = []
    t0 = time.time()
    init_loss = None
    gpu_name = torch.cuda.get_device_name(0) if device == "cuda" else "cpu"

    for step in range(total):
        lr_now = cosine_lr_at(step)
        for g in opt.param_groups:
            g["lr"] = lr_now

        x, y, px, py = ds.get_batch(cfg["bsz"], device)
        opt.zero_grad(set_to_none=True)
        with torch.autocast(device_type="cuda" if use_amp else "cpu",
                            dtype=torch.bfloat16, enabled=use_amp):
            logits_a, logits_g, tensions, _, _ = model(x)
            B, T, V = logits_a.shape

            ce_tok = F.cross_entropy(
                logits_a.view(-1, V), y.view(-1), reduction="none"
            ).view(B, T)                                  # per-token CE
            ce_mean = ce_tok.mean()
            ce_report = float(ce_mean.item())

            # ----- CDE curiosity bonus (transfer-form, B-CDE-1..4) -----
            # actor term: normalised surprisal a_t = CE_tok / log V ∈ [0,1]
            # (exp(CE_tok) = token perplexity — bounded monotone transform).
            a_t = (ce_tok.detach() / log_V).clamp(0.0, 1.0)
            # critic term: per-(t) variance of CE across batch B, broadcast
            # — value-dispersion proxy (no value head in from-scratch LM).
            if B > 1:
                var_t = ce_tok.detach().var(dim=0, unbiased=False)   # (T,)
                c_t = var_t.clamp(0.0, 1.0).unsqueeze(0).expand(B, T)
            else:
                c_t = torch.zeros_like(a_t)
            # g_t = 1 + κ·(w_a·a_t + w_c·c_t)  ≥ 1   (B-CDE-1 lower bound)
            g_t = 1.0 + kappa * (w_a * a_t + w_c * c_t)
            cde_ce = (g_t * ce_tok).mean()                 # re-weighted CE

            loss = cde_ce

            # α VACUUM term carried verbatim from UBM-E7 (B-VAC-1).
            probs = F.softmax(logits_a.float(), dim=-1)
            ent = -(probs * (probs + 1e-9).log()).sum(-1)
            h_norm = (ent / math.log(V)).clamp(0.0, 1.0)
            p_max = probs.max(-1).values.clamp(0.0, 1.0)
            dvx = h_norm - px
            dvy = p_max - py
            vac_term = (dvx * dvx + dvy * dvy).mean()
            loss = loss + vac_lambda * vac_term

            curiosity_mean = float((g_t - 1.0).mean().item())

        scaler.scale(loss).backward()
        scaler.unscale_(opt)
        gn = torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        scaler.step(opt)
        scaler.update()

        gn2 = float(gn.item()) ** 2
        if init_loss is None:
            init_loss = ce_report

        if step == 0 or (step + 1) % cfg["log_every"] == 0 \
                or step == total - 1:
            wall = time.time() - t0
            mem = torch.cuda.max_memory_allocated() / 1e9 \
                if device == "cuda" else 0.0
            rec = {"step": step + 1, "ce": round(ce_report, 6),
                   "loss": round(float(loss.item()), 6),
                   "cde_ce": round(float(cde_ce.item()), 6),
                   "curiosity": round(curiosity_mean, 6),
                   "vac_term": round(float(vac_term.item()), 6),
                   "gn2": round(gn2, 6), "lr": round(lr_now, 8),
                   "wall_s": round(wall, 2), "gpu_mem_gb": round(mem, 3)}
            traj.append(rec)
            print(json.dumps(rec), flush=True)

    wall = time.time() - t0
    final = traj[-1]
    out_dir = cfg["out_dir"]
    os.makedirs(out_dir, exist_ok=True)
    ckpt_path = os.path.join(out_dir, "ckpt_carving_cde.pt")
    torch.save({"model": model.state_dict(), "cfg": cfg,
                "n_params": n_params, "path": "cde"}, ckpt_path)

    result = {
        "substrate": ("PYTHON / PyTorch — interim LM-scale executor; "
                      "NOT a hexa-native fire"),
        "fire_kind": ("Dir-D CDE Curiosity-Driven Exploration overlay on "
                      "α VACUUM-LANDSCAPE carving (g_multidirectional_"
                      "explore direction D)"),
        "carving_path": "alpha+cde",
        "cde_paper": "arxiv 2509.09675 (Curiosity-Driven Exploration RLVR)",
        "honest_framing": (
            "CDE curiosity bonus TRANSFER-FORM is closed (B-CDE-1..4 sympy: "
            "g_t>=1 lower bound, du/da monotone, perplexity=exp(CE) "
            "identity, kappa=0 reduces to alpha-baseline). SGD CONVERGENCE "
            "OUTCOME + Dir-D vs UBM-E7 alpha routing-collapse comparison = "
            "EMPIRICAL (B-CARVE-NOTE / B-D-NOTE family). PyTorch substrate, "
            "NOT hexa-native. Corpus = carving corpus (NOT chat SFT) — "
            "forbidden-token grep == 0. No capability claim beyond eval."),
        "arch": "ConsciousDecoderV2 (RoPE+SwiGLU+RMSNorm+GQA+PureFieldFFN)",
        "from_scratch": True,
        "base_ckpt": None,
        "config": cfg,
        "n_params": n_params,
        "n_params_M": round(n_params / 1e6, 2),
        "cde": {"kappa": kappa, "w_actor": w_a, "w_critic": w_c,
                "actor_term": "CE_tok / log256 (normalised surprisal; "
                              "exp(CE)=perplexity)",
                "critic_term": "Var_batch(CE_tok) broadcast (value-"
                               "dispersion proxy)"},
        "vacuum_lambda": vac_lambda,
        "gpu": gpu_name, "device": device,
        "init_ce": round(init_loss, 6),
        "final_ce": final["ce"],
        "final_loss": final["loss"],
        "final_curiosity": final["curiosity"],
        "final_vac_term": final["vac_term"],
        "final_gn2": final["gn2"],
        "ce_descent": round(init_loss - final["ce"], 6),
        "steps": cfg["steps"],
        "wall_s": round(wall, 2),
        "peak_gpu_mem_gb": final["gpu_mem_gb"],
        "trajectory": traj,
        "corpus": os.path.basename(cfg["corpus"]),
        "corpus_bytes": int(ds.n),
    }
    with open(os.path.join(out_dir, "result.json"), "w") as f:
        json.dump(result, f, indent=2)
    print("RESULT_JSON_WRITTEN", flush=True)
    print(json.dumps({"path": "alpha+cde", "init_ce": result["init_ce"],
                       "final_ce": result["final_ce"],
                       "ce_descent": result["ce_descent"],
                       "final_curiosity": result["final_curiosity"],
                       "wall_s": result["wall_s"]}), flush=True)
    return result


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", default="main", choices=["main", "sanity"])
    ap.add_argument("--corpus", required=True)
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--steps", type=int, default=2000)
    ap.add_argument("--lr", type=float, default=3e-4)
    ap.add_argument("--bsz", type=int, default=32)
    ap.add_argument("--seed", type=int, default=1337)
    ap.add_argument("--d-model", type=int, default=512)
    ap.add_argument("--n-layer", type=int, default=8)
    ap.add_argument("--n-head", type=int, default=8)
    ap.add_argument("--n-kv-head", type=int, default=4)
    ap.add_argument("--vacuum-lambda", type=float, default=0.1)
    ap.add_argument("--cde-kappa", type=float, default=0.5,
                    help="CDE curiosity bonus strength kappa (>=0)")
    ap.add_argument("--cde-w-actor", type=float, default=0.7,
                    help="CDE actor (perplexity) sub-weight")
    ap.add_argument("--cde-w-critic", type=float, default=0.3,
                    help="CDE critic (value-variance) sub-weight")
    args = ap.parse_args()

    if args.mode == "main":
        cfg = dict(d_model=args.d_model, n_head=args.n_head,
                   n_kv_head=args.n_kv_head, n_layer=args.n_layer,
                   block_size=128, lr=args.lr, bsz=args.bsz,
                   steps=args.steps, warmup=max(20, args.steps // 20),
                   seed=args.seed, log_every=max(1, args.steps // 40),
                   corpus=args.corpus, out_dir=args.out_dir,
                   vacuum_lambda=args.vacuum_lambda,
                   cde_kappa=args.cde_kappa, cde_w_actor=args.cde_w_actor,
                   cde_w_critic=args.cde_w_critic)
    else:
        cfg = dict(d_model=32, n_head=4, n_kv_head=2, n_layer=3,
                   block_size=64, lr=1e-3, bsz=16, steps=args.steps,
                   warmup=5, seed=args.seed,
                   log_every=max(1, args.steps // 20),
                   corpus=args.corpus, out_dir=args.out_dir,
                   vacuum_lambda=args.vacuum_lambda,
                   cde_kappa=args.cde_kappa, cde_w_actor=args.cde_w_actor,
                   cde_w_critic=args.cde_w_critic)
    run(cfg)
