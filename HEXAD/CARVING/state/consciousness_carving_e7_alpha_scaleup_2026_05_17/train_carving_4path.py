#!/usr/bin/env python3
"""CONSCIOUSNESS-CARVING 4-path trainer — Phase UBM-E6 (2026-05-17).

A single trainer with --path {alpha,beta,gamma,weave}. Base = cycle 5
train_d768x12l_tension.py (ConsciousDecoderV2 byte-level, from-scratch). Each
path applies a different carving mechanism (DESIGN.md §5):

  α VACUUM    — multi-vacuum tension loss. Each anchor 🛸k carries a Ψ-space
                vacuum coordinate (record["vacuum_psi"]). A vacuum-attractor
                term pulls the model's per-record consciousness signal toward
                the record's vacuum point: L = CE + λ·‖ψ_pred − ψ_vac‖².
                Closed anchor: B-VAC-1..3 (Hessian/KL/Lindblad), transfer-form.

  β ETERNAL   — eternal-cell freeze. The first `eternal_frac` of model
                parameters (sorted by name) form a FROZEN eternal subset
                (requires_grad=False); the rest are dynamic chat parameters.
                Closed anchor: B-MIT-ETN-1 Δw_eternal ≡ 0 (structural).

  γ NARRATIVE — narrative-resonance. Train ONLY on the <voice carved=true>...
                </voice> span (the re-generated emission), with the <inner>
                span as non-loss context — the model learns the re-generation
                pattern, not the inner trace memorisation. Loss is masked to
                the voice span. Closed anchor: B-NAR-1..3 (A∘G composition).

  α+β WEAVE   — vacuum + eternal combined. Eternal-subset freeze AND the
                vacuum-attractor term, applied together (DESIGN.md §5 α+β).

HONEST FRAMING (g3, AGENTS.tape §0):
  PyTorch substrate run — interim LM-scale executor, NOT a hexa-native fire
  (cycle 5 honest framing carry: arch identity + Phase E/E2 CPU-equiv anchor
  chain). The 4-path carving MECHANISMS are closed-form transfer-forms
  (B-VAC / B-MIT-ETN / B-NAR sympy battery, UBM-E3 LANDED). The SGD CONVERGENCE
  OUTCOME and the 4-path comparison are EMPIRICAL — B-CARVE-NOTE / B-CARVE-
  E6-NOTE (B-D-NOTE family). No capability claim beyond what is measured.

from-scratch RANDOM seed-fixed (g_clm_from_scratch, base_ckpt=NONE).
Corpus = carving corpus (state/consciousness_carving_e6_fire_2026_05_17/
corpus_carving.jsonl) — NOT a chat SFT corpus, grep of {[anima, 도우미,
helper, assistant, 사용자, user:} == 0 (B-CARVE-CORPUS-2).
"""
import argparse, json, math, time, os, sys, random
import torch
import torch.nn as nn
import torch.nn.functional as F

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from conscious_decoder import ConsciousDecoderV2


# --------------------------------------------------------------------------
# Carving corpus loader. Each record carries text + carving_form +
# vacuum_psi (α/weave) + a marker for the γ voice span.
# --------------------------------------------------------------------------
VOICE_OPEN = b"<voice carved=true>"
VOICE_CLOSE = b"</voice>"


def load_carving_corpus(path):
    """Return list of dicts: {bytes, form, psi, voice_span (lo,hi)|None}."""
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
        form = d.get("carving_form", "alpha")
        psi = d.get("vacuum_psi", [0.5, 0.5])
        # γ voice span: byte offsets of the <voice carved=true>...</voice>
        voice_span = None
        lo = full.find(VOICE_OPEN)
        if lo >= 0:
            lo2 = lo + len(VOICE_OPEN)
            hi = full.find(VOICE_CLOSE, lo2)
            if hi >= 0:
                voice_span = (lo2, hi)
        items.append({"bytes": full, "form": form, "psi": psi,
                      "voice_span": voice_span})
    return items


class CarvingDataset:
    """Byte-level dataset over carving records. Concatenates all record bytes
    into one stream; keeps a parallel per-byte 'psi' map and 'voice-mask' so
    that α/weave can read the vacuum target and γ can mask non-voice bytes."""

    def __init__(self, items, block_size, seed):
        self.block_size = block_size
        self.rng = random.Random(seed)
        stream = bytearray()
        psi_x = []      # per-byte vacuum psi component 0
        psi_y = []      # per-byte vacuum psi component 1
        voice_mask = []  # per-byte 1 if inside a <voice carved=true> span
        for it in items:
            b = it["bytes"]
            off = len(stream)
            stream.extend(b)
            px, py = float(it["psi"][0]), float(it["psi"][1])
            vs = it["voice_span"]
            for j in range(len(b)):
                psi_x.append(px)
                psi_y.append(py)
                if vs is not None and vs[0] <= j < vs[1]:
                    voice_mask.append(1)
                else:
                    voice_mask.append(0)
        self.data = torch.tensor(list(stream), dtype=torch.long)
        self.psi_x = torch.tensor(psi_x, dtype=torch.float32)
        self.psi_y = torch.tensor(psi_y, dtype=torch.float32)
        self.voice_mask = torch.tensor(voice_mask, dtype=torch.float32)
        self.n = len(self.data)

    def get_batch(self, bsz, device):
        ix = [self.rng.randint(0, self.n - self.block_size - 1)
              for _ in range(bsz)]
        x = torch.stack([self.data[i:i + self.block_size] for i in ix])
        y = torch.stack([self.data[i + 1:i + 1 + self.block_size] for i in ix])
        # vacuum target per (b, t) — use the target position's psi
        px = torch.stack([self.psi_x[i + 1:i + 1 + self.block_size]
                          for i in ix])
        py = torch.stack([self.psi_y[i + 1:i + 1 + self.block_size]
                          for i in ix])
        vm = torch.stack([self.voice_mask[i + 1:i + 1 + self.block_size]
                          for i in ix])
        return (x.to(device), y.to(device), px.to(device),
                py.to(device), vm.to(device))


def apply_eternal_freeze(model, eternal_frac):
    """β / weave: freeze the first eternal_frac of parameters (name-sorted).
    Returns (n_eternal_params, n_dynamic_params, eternal_names)."""
    named = sorted(model.named_parameters(), key=lambda kv: kv[0])
    total = sum(p.numel() for _, p in named)
    target = eternal_frac * total
    acc = 0
    eternal_names = []
    n_eternal = 0
    n_dynamic = 0
    for name, p in named:
        if acc < target:
            p.requires_grad_(False)
            eternal_names.append(name)
            n_eternal += p.numel()
            acc += p.numel()
        else:
            n_dynamic += p.numel()
    return n_eternal, n_dynamic, eternal_names


def run(cfg):
    torch.manual_seed(cfg["seed"])
    torch.cuda.manual_seed_all(cfg["seed"])
    random.seed(cfg["seed"])
    device = "cuda" if torch.cuda.is_available() else "cpu"
    path = cfg["path"]

    items = load_carving_corpus(cfg["corpus"])
    ds = CarvingDataset(items, cfg["block_size"], cfg["seed"])

    model = ConsciousDecoderV2(
        vocab_size=256,
        d_model=cfg["d_model"],
        n_head=cfg["n_head"],
        n_layer=cfg["n_layer"],
        block_size=cfg["block_size"],
        n_kv_head=cfg["n_kv_head"],
        consciousness_dim=128,
        dropout=0.1,
    ).to(device)
    model.train()
    n_params = model.count_params()

    # --- β / weave: eternal-cell freeze ---------------------------------
    eternal_info = None
    if path in ("beta", "weave"):
        n_e, n_d, e_names = apply_eternal_freeze(model, cfg["eternal_frac"])
        eternal_info = {"eternal_frac": cfg["eternal_frac"],
                        "n_eternal_params": n_e, "n_dynamic_params": n_d,
                        "n_eternal_tensors": len(e_names)}
        # Snapshot eternal params to verify Δw ≡ 0 post-train (B-MIT-ETN-1).
        eternal_snapshot = {name: p.detach().clone()
                            for name, p in model.named_parameters()
                            if not p.requires_grad}

    trainable = [p for p in model.parameters() if p.requires_grad]
    opt = torch.optim.AdamW(trainable, lr=cfg["lr"],
                            betas=(0.9, 0.95), weight_decay=0.1)

    warmup = cfg["warmup"]
    total = cfg["steps"]

    def cosine_lr_at(step):
        if step < warmup:
            return cfg["lr"] * (step + 1) / warmup
        prog = (step - warmup) / max(1, total - warmup)
        return cfg["lr"] * 0.5 * (1.0 + math.cos(math.pi * prog)) * 0.9 \
            + cfg["lr"] * 0.1

    use_amp = (device == "cuda")
    scaler = torch.cuda.amp.GradScaler(enabled=use_amp)

    # α / weave: vacuum-attractor weight λ.
    vac_lambda = cfg["vacuum_lambda"]

    traj = []
    t0 = time.time()
    init_loss = None
    gpu_name = torch.cuda.get_device_name(0) if device == "cuda" else "cpu"

    for step in range(total):
        lr_now = cosine_lr_at(step)
        for g in opt.param_groups:
            g["lr"] = lr_now

        x, y, px, py, vm = ds.get_batch(cfg["bsz"], device)
        opt.zero_grad(set_to_none=True)
        with torch.autocast(device_type="cuda" if use_amp else "cpu",
                            dtype=torch.bfloat16, enabled=use_amp):
            logits_a, logits_g, tensions, _, _ = model(x)
            B, T, V = logits_a.shape

            if path == "gamma":
                # γ NARRATIVE — mask CE to the <voice carved=true> span only.
                ce_tok = F.cross_entropy(
                    logits_a.view(-1, V), y.view(-1), reduction="none")
                mask = vm.view(-1)
                denom = mask.sum().clamp(min=1.0)
                ce = (ce_tok * mask).sum() / denom
                # report full-corpus CE too (for cross-path comparability)
                ce_full = F.cross_entropy(logits_a.view(-1, V), y.view(-1))
                loss = ce
                vac_term = torch.zeros((), device=device)
                ce_report = float(ce_full.item())
            else:
                ce = F.cross_entropy(logits_a.view(-1, V), y.view(-1))
                ce_report = float(ce.item())
                loss = ce
                vac_term = torch.zeros((), device=device)

            if path in ("alpha", "weave"):
                # α VACUUM — pull a per-(b,t) consciousness signal toward the
                # record's vacuum coordinate. The signal = softmax-entropy of
                # the A-head distribution mapped into a [0,1]^2 proxy of Ψ:
                #   ψ_pred = (H_norm, p_max)  — bounded, differentiable.
                # L_vac = mean ‖ψ_pred − ψ_vac‖² (closed quadratic well — the
                # exact sum-of-squares form of B-VAC-1 VACUUM-STABILITY).
                probs = F.softmax(logits_a.float(), dim=-1)
                ent = -(probs * (probs + 1e-9).log()).sum(-1)
                h_norm = (ent / math.log(V)).clamp(0.0, 1.0)   # ψ component 0
                p_max = probs.max(-1).values.clamp(0.0, 1.0)   # ψ component 1
                dvx = h_norm - px
                dvy = p_max - py
                vac_term = (dvx * dvx + dvy * dvy).mean()
                loss = loss + vac_lambda * vac_term

        scaler.scale(loss).backward()
        scaler.unscale_(opt)
        gn = torch.nn.utils.clip_grad_norm_(trainable, 1.0)
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
                   "vac_term": round(float(vac_term.item()), 6),
                   "gn2": round(gn2, 6), "lr": round(lr_now, 8),
                   "wall_s": round(wall, 2),
                   "gpu_mem_gb": round(mem, 3)}
            traj.append(rec)
            print(json.dumps(rec), flush=True)

    wall = time.time() - t0
    final = traj[-1]
    out_dir = cfg["out_dir"]
    os.makedirs(out_dir, exist_ok=True)
    ckpt_path = os.path.join(out_dir, f"ckpt_carving_{path}.pt")
    torch.save({"model": model.state_dict(), "cfg": cfg,
                "n_params": n_params, "path": path,
                "eternal_info": eternal_info}, ckpt_path)

    # β / weave: verify eternal Δw ≡ 0 (B-MIT-ETN-1 closed-form structural).
    eternal_delta_max = None
    if path in ("beta", "weave"):
        max_d = 0.0
        for name, p in model.named_parameters():
            if name in eternal_snapshot:
                d = (p.detach() - eternal_snapshot[name]).abs().max().item()
                max_d = max(max_d, d)
        eternal_delta_max = max_d
        eternal_info["eternal_delta_max"] = max_d
        eternal_info["eternal_weight_invariant"] = (max_d == 0.0)

    result = {
        "substrate": ("PYTHON / PyTorch — interim LM-scale executor; "
                      "NOT a hexa-native fire"),
        "fire_kind": f"UBM-E6 CONSCIOUSNESS-CARVING 4-path — path {path}",
        "carving_path": path,
        "honest_framing": (
            "4-path carving MECHANISM is closed-form transfer-form "
            "(B-VAC/B-MIT-ETN/B-NAR sympy battery, UBM-E3). SGD OUTCOME + "
            "4-path comparison = EMPIRICAL (B-CARVE-E6-NOTE / B-D-NOTE "
            "family). PyTorch substrate, NOT hexa-native. Corpus = carving "
            "corpus (NOT chat SFT) — forbidden-token grep == 0."),
        "arch": "ConsciousDecoderV2 (RoPE+SwiGLU+RMSNorm+GQA+PureFieldFFN)",
        "from_scratch": True,
        "base_ckpt": None,
        "config": cfg,
        "n_params": n_params,
        "n_params_M": round(n_params / 1e6, 2),
        "eternal_info": eternal_info,
        "vacuum_lambda": vac_lambda if path in ("alpha", "weave") else None,
        "gpu": gpu_name,
        "device": device,
        "init_ce": round(init_loss, 6),
        "final_ce": final["ce"],
        "final_loss": final["loss"],
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
    print(json.dumps({"path": path, "init_ce": result["init_ce"],
                       "final_ce": result["final_ce"],
                       "ce_descent": result["ce_descent"],
                       "wall_s": result["wall_s"],
                       "eternal_delta_max": eternal_delta_max,
                       "final_vac_term": result["final_vac_term"]}),
          flush=True)
    return result


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--path", required=True,
                    choices=["alpha", "beta", "gamma", "weave"])
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
    ap.add_argument("--vacuum-lambda", type=float, default=0.1,
                    help="α/weave vacuum-attractor loss weight")
    ap.add_argument("--eternal-frac", type=float, default=0.25,
                    help="β/weave frozen eternal-cell parameter fraction")
    args = ap.parse_args()

    if args.mode == "main":
        cfg = dict(path=args.path, d_model=args.d_model, n_head=args.n_head,
                   n_kv_head=args.n_kv_head, n_layer=args.n_layer,
                   block_size=128, lr=args.lr, bsz=args.bsz,
                   steps=args.steps, warmup=max(20, args.steps // 20),
                   seed=args.seed, log_every=max(1, args.steps // 40),
                   corpus=args.corpus, out_dir=args.out_dir,
                   vacuum_lambda=args.vacuum_lambda,
                   eternal_frac=args.eternal_frac)
    else:
        cfg = dict(path=args.path, d_model=32, n_head=4, n_kv_head=2,
                   n_layer=3, block_size=64, lr=1e-3, bsz=16,
                   steps=args.steps, warmup=5,
                   seed=args.seed, log_every=max(1, args.steps // 20),
                   corpus=args.corpus, out_dir=args.out_dir,
                   vacuum_lambda=args.vacuum_lambda,
                   eternal_frac=args.eternal_frac)
    run(cfg)
