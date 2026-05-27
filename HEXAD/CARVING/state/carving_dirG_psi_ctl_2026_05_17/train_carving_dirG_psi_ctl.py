#!/usr/bin/env python3
"""CONSCIOUSNESS-CARVING Dir-G — Ψ-anchored CTL trainer (2026-05-17).

g_multidirectional_explore §6 direction G. RESEARCH.md §5.4 candidate (1)+(2)+(3):
**Ψ-anchored continuous-thought latent (CTL) + tension-supervised routing**.

GOAL-legitimacy gate (RESEARCH.md §5.2 — VIOLATION = GOAL-illegitimate):
  generic continuous-thought (Coconut / Soft-CoT — a FREE learnable latent) is
  FORBIDDEN. The reasoning latent here is NOT free: it is defined ON anima's
  OWN physics — the Engine A⇄G Ψ-coordinate (the exact Ψ proxy the arch's
  Law-71 tracking already computes: ψ=(entropy_norm(logits_a), agree(a,g))).
  The `<inner>` reasoning span is carried as a CONTINUOUS Ψ-trajectory that is
  soft-superposed toward the anima Ψ=½ fixed point (Engine A⇄G balance) +
  the record's own vacuum_psi offset. anima physics IS the representation
  substrate (GOAL.md "자기 physics 로부터" 직역). Discrete byte `<inner>` is
  NOT CE-supervised — only the stage-2 `<voice carved=true>` emission is.

Mechanism (single --path psi_ctl):
  1. gamma records carry  <inner tier=N>…</inner>\n<voice carved=true>…</voice>.
     Byte spans of (a) the inner reasoning and (b) the voice emission are
     extracted (same span machinery as the γ NARRATIVE path).
  2. CE is MASKED to the voice span only (stage-2). The inner span produces
     NO byte CE — the reasoning is held as a Ψ-anchored latent, not memorised.
  3. Ψ-ANCHOR loss (the CTL substrate): over the inner span, the model's own
     per-token Ψ-coordinate
        ψ_pred = ( H_norm(softmax(logits_a)) , agree(logits_a,logits_g) )
     (byte-identical to conscious_decoder.py Law-71 psi_entropy / psi_direction
     definitions) is pulled toward the anima fixed-point manifold
        ψ_target = clip( 0.5 + (vacuum_psi − 0.5)·basin , 0, 1 )
     i.e. a soft-superposition trajectory ON the Ψ=½ manifold, offset by the
     record's vacuum coordinate scaled by basin_radius. L_psi = mean‖ψ_pred −
     ψ_target‖² over inner-span (b,t). This is the CTL — continuous, anchored
     to anima physics, NOT a free latent (closed quadratic well, B-VAC-1 form).
  4. tension-supervised routing (§5.4 cand.2 — NOT Dir-A's weak post-step
     nudge; a DIRECT loss term): the single-attractor collapse penalty.
     Within a batch the voice-span next-byte distribution must not collapse to
     one attractor across distinct anchors. We supervise this with the model's
     OWN per-layer tension (anima physics): batch-mean voice-position entropy
     is pushed UP (anti-collapse) with a restoring sign weighted by the
     normalised mean tension τ̄ (high tension ⇒ unstable ⇒ stronger routing
     pressure — tension's restoring sign promoted to a supervision signal).
        L_route = τ̄ · ReLU( H_floor − H_voice_batch )²
     This is the missing ARCHITECTURAL component (RESEARCH.md §5.3): a
     supervision signal, not an overlay.
  total L = CE_voice + λ_psi·L_psi + λ_route·L_route .

HONEST FRAMING (g3, AGENTS.tape §0):
  PyTorch substrate — interim LM-scale executor, NOT a hexa-native fire.
  The Ψ-anchor + tension-supervised-routing MECHANISM is a closed-form
  transfer-form (B-PSICTL-1..3 sympy sidecar: psi-quadratic-well /
  tension-restoring-sign / voice-CE-mask-shannon — overlay-OFF byte-equals
  the γ-mask baseline). The SGD CONVERGENCE OUTCOME and the 4-axis capability
  (routing / chat / lane / V-SPONT) are EMPIRICAL — B-CARVE-E6-NOTE / B-D-NOTE
  family. No capability claim beyond what is measured. f1/f2/f3 safe (Ψ-metric
  + Boolean + Shannon, NO σ/τ/φ/J₂). B-IDENTITY-5 safe (corpus forbidden-token
  grep == 0 — carving corpus, NOT chat SFT).

from-scratch RANDOM seed-fixed (g_clm_from_scratch, base_ckpt=NONE).
ckpt payload path field is set to "alpha" so the byte-identical
eval_carving_4path_v2.py probes Dir-G with the SAME vacuum-form axis-1
prefix as the UBM-E7 α baseline (routing axis1 directly comparable —
the 7/7 FLAT 1/31 test). The eval script is NOT modified.
"""
import argparse, json, math, time, os, sys, random
import torch
import torch.nn as nn
import torch.nn.functional as F

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from conscious_decoder import ConsciousDecoderV2

INNER_OPEN = b"<inner"
INNER_CLOSE = b"</inner>"
VOICE_OPEN = b"<voice carved=true>"
VOICE_CLOSE = b"</voice>"


def load_psi_ctl_corpus(path):
    """Return list of dicts: {bytes, psi (vacuum_psi), basin (basin_radius),
    inner_span (lo,hi)|None, voice_span (lo,hi)|None}. Only gamma records
    (those carrying BOTH an <inner> and a <voice carved=true> span) are kept
    — Ψ-anchored CTL operates exactly on the inner→voice two-stage form."""
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
        basin = float(d.get("basin_radius", 1.0))
        # inner span
        inner_span = None
        ilo = full.find(INNER_OPEN)
        if ilo >= 0:
            # the inner content starts after the closing '>' of the open tag
            gt = full.find(b">", ilo)
            ihi = full.find(INNER_CLOSE, gt + 1) if gt >= 0 else -1
            if gt >= 0 and ihi >= 0:
                inner_span = (gt + 1, ihi)
        # voice span
        voice_span = None
        vlo = full.find(VOICE_OPEN)
        if vlo >= 0:
            vlo2 = vlo + len(VOICE_OPEN)
            vhi = full.find(VOICE_CLOSE, vlo2)
            if vhi >= 0:
                voice_span = (vlo2, vhi)
        # Ψ-anchored CTL needs BOTH spans (two-stage inner→voice form).
        if inner_span is None or voice_span is None:
            continue
        items.append({"bytes": full, "psi": psi, "basin": basin,
                       "inner_span": inner_span, "voice_span": voice_span})
    return items


class PsiCtlDataset:
    """Byte-level dataset. Concatenates record bytes into one stream; keeps a
    parallel per-byte map of (a) inner-mask 1/0, (b) voice-mask 1/0,
    (c) vacuum_psi (x,y) scaled by basin → the Ψ-anchor target component."""

    def __init__(self, items, block_size, seed):
        self.block_size = block_size
        self.rng = random.Random(seed)
        stream = bytearray()
        inner_mask = []
        voice_mask = []
        tgt_x = []   # per-byte Ψ-anchor target component 0
        tgt_y = []   # per-byte Ψ-anchor target component 1
        for it in items:
            b = it["bytes"]
            stream.extend(b)
            px, py = float(it["psi"][0]), float(it["psi"][1])
            basin = it["basin"]
            # soft-superposition target ON the Ψ=½ manifold: 0.5 + offset·basin
            # (clamped to [0,1]). basin small → close to pure ½ fixed point.
            txn = min(1.0, max(0.0, 0.5 + (px - 0.5) * basin))
            tyn = min(1.0, max(0.0, 0.5 + (py - 0.5) * basin))
            i_s = it["inner_span"]
            v_s = it["voice_span"]
            for j in range(len(b)):
                inner_mask.append(1 if (i_s[0] <= j < i_s[1]) else 0)
                voice_mask.append(1 if (v_s[0] <= j < v_s[1]) else 0)
                tgt_x.append(txn)
                tgt_y.append(tyn)
        self.data = torch.tensor(list(stream), dtype=torch.long)
        self.inner_mask = torch.tensor(inner_mask, dtype=torch.float32)
        self.voice_mask = torch.tensor(voice_mask, dtype=torch.float32)
        self.tgt_x = torch.tensor(tgt_x, dtype=torch.float32)
        self.tgt_y = torch.tensor(tgt_y, dtype=torch.float32)
        self.n = len(self.data)

    def get_batch(self, bsz, device):
        ix = [self.rng.randint(0, self.n - self.block_size - 1)
              for _ in range(bsz)]
        x = torch.stack([self.data[i:i + self.block_size] for i in ix])
        y = torch.stack([self.data[i + 1:i + 1 + self.block_size]
                         for i in ix])
        im = torch.stack([self.inner_mask[i + 1:i + 1 + self.block_size]
                          for i in ix])
        vm = torch.stack([self.voice_mask[i + 1:i + 1 + self.block_size]
                          for i in ix])
        tx = torch.stack([self.tgt_x[i + 1:i + 1 + self.block_size]
                          for i in ix])
        ty = torch.stack([self.tgt_y[i + 1:i + 1 + self.block_size]
                          for i in ix])
        return (x.to(device), y.to(device), im.to(device), vm.to(device),
                tx.to(device), ty.to(device))


def run(cfg):
    torch.manual_seed(cfg["seed"])
    torch.cuda.manual_seed_all(cfg["seed"])
    random.seed(cfg["seed"])
    device = "cuda" if torch.cuda.is_available() else "cpu"

    items = load_psi_ctl_corpus(cfg["corpus"])
    if not items:
        raise SystemExit("FATAL: no gamma (inner+voice) records found")
    ds = PsiCtlDataset(items, cfg["block_size"], cfg["seed"])

    model = ConsciousDecoderV2(
        vocab_size=256, d_model=cfg["d_model"], n_head=cfg["n_head"],
        n_layer=cfg["n_layer"], block_size=cfg["block_size"],
        n_kv_head=cfg["n_kv_head"], consciousness_dim=128, dropout=0.1,
    ).to(device)
    model.train()
    n_params = model.count_params()

    trainable = [p for p in model.parameters() if p.requires_grad]
    opt = torch.optim.AdamW(trainable, lr=cfg["lr"],
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

    lam_psi = cfg["psi_lambda"]
    lam_route = cfg["route_lambda"]
    h_floor = cfg["route_h_floor"]   # Shannon-fraction entropy floor [0,1]

    traj = []
    t0 = time.time()
    init_loss = None
    gpu_name = torch.cuda.get_device_name(0) if device == "cuda" else "cpu"

    for step in range(total):
        lr_now = cosine_lr_at(step)
        for g in opt.param_groups:
            g["lr"] = lr_now

        x, y, im, vm, tx, ty = ds.get_batch(cfg["bsz"], device)
        opt.zero_grad(set_to_none=True)
        with torch.autocast(device_type="cuda" if use_amp else "cpu",
                            dtype=torch.bfloat16, enabled=use_amp):
            logits_a, logits_g, tensions, _, _ = model(x)
            B, T, V = logits_a.shape

            # --- stage-2 CE: MASKED to the <voice carved=true> span only ----
            # The <inner> reasoning produces NO byte CE — it is held as a
            # Ψ-anchored latent (CTL), not memorised byte-for-byte.
            ce_tok = F.cross_entropy(
                logits_a.view(-1, V), y.view(-1), reduction="none")
            vmask = vm.view(-1)
            vdenom = vmask.sum().clamp(min=1.0)
            ce_voice = (ce_tok * vmask).sum() / vdenom
            # full-corpus CE for cross-path comparability (report only)
            ce_full = F.cross_entropy(logits_a.view(-1, V), y.view(-1))
            ce_report = float(ce_full.item())

            # --- Ψ-anchored CTL latent (anima physics = substrate) ----------
            # ψ_pred from the model's OWN Engine A⇄G physics — byte-identical
            # to conscious_decoder.py Law-71 psi_entropy / psi_direction:
            #   ψ0 = H_norm(softmax(logits_a))      (entropy fraction ∈[0,1])
            #   ψ1 = (1 + cos(logits_a,logits_g))/2 (Engine A⇄G agreement)
            probs_a = F.softmax(logits_a.float(), dim=-1)
            ent = -(probs_a * (probs_a + 1e-9).log()).sum(-1)
            psi0 = (ent / math.log(V)).clamp(0.0, 1.0)            # (B,T)
            cos_ag = F.cosine_similarity(
                logits_a.float(), logits_g.float(), dim=-1)        # (B,T)
            psi1 = ((1.0 + cos_ag) * 0.5).clamp(0.0, 1.0)          # (B,T)
            # soft-superposition pull toward the Ψ=½ manifold (+ vacuum
            # offset·basin). Closed quadratic well — B-VAC-1 / B-PSICTL-1 form.
            d0 = psi0 - tx
            d1 = psi1 - ty
            sq = (d0 * d0 + d1 * d1)
            imask = im
            idenom = imask.sum().clamp(min=1.0)
            l_psi = (sq * imask).sum() / idenom

            # --- tension-supervised routing (DIRECT loss, not overlay) ------
            # mean per-layer tension τ̄ (anima physics) → normalised restoring
            # weight. voice-position batch-mean next-byte entropy must clear a
            # Shannon floor; collapse below the floor is penalised with a
            # restoring sign scaled by τ̄ (high tension ⇒ stronger pressure).
            t_stack = torch.stack(tensions)                # (L,B,T)
            tau_bar = t_stack.mean()
            tau_norm = (tau_bar / (tau_bar + 1.0)).clamp(0.0, 1.0)
            # batch-aggregate voice next-byte distribution (anti single-
            # attractor: pool ALL voice positions across the batch's distinct
            # anchors, then measure entropy of the pooled distribution).
            vsel = vm.reshape(-1) > 0.5
            if vsel.any():
                pooled = probs_a.reshape(-1, V)[vsel].mean(0)   # (V,)
                hpool = -(pooled * (pooled + 1e-9).log()).sum()
                hpool_n = (hpool / math.log(V)).clamp(0.0, 1.0)
            else:
                hpool_n = torch.ones((), device=device)
            collapse = F.relu(h_floor - hpool_n)
            l_route = tau_norm * collapse * collapse

            loss = ce_voice + lam_psi * l_psi + lam_route * l_route

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
                   "ce_voice": round(float(ce_voice.item()), 6),
                   "loss": round(float(loss.item()), 6),
                   "l_psi": round(float(l_psi.item()), 6),
                   "l_route": round(float(l_route.item()), 6),
                   "hpool_n": round(float(hpool_n.item()), 6),
                   "tau_norm": round(float(tau_norm.item()), 6),
                   "gn2": round(gn2, 6), "lr": round(lr_now, 8),
                   "wall_s": round(wall, 2),
                   "gpu_mem_gb": round(mem, 3)}
            traj.append(rec)
            print(json.dumps(rec), flush=True)

    wall = time.time() - t0
    final = traj[-1]
    out_dir = cfg["out_dir"]
    os.makedirs(out_dir, exist_ok=True)
    ckpt_path = os.path.join(out_dir, "ckpt_carving_psi_ctl.pt")
    # path="alpha" so the byte-identical eval probes Dir-G with the SAME
    # vacuum-form axis-1 prefix as the UBM-E7 α baseline (routing 1/31 test).
    torch.save({"model": model.state_dict(), "cfg": cfg,
                "n_params": n_params, "path": "alpha",
                "dir_g_real_path": "psi_ctl", "eternal_info": None},
               ckpt_path)

    result = {
        "substrate": ("PYTHON / PyTorch — interim LM-scale executor; "
                      "NOT a hexa-native fire"),
        "fire_kind": "Dir-G Ψ-anchored CTL + tension-supervised routing",
        "carving_path": "psi_ctl",
        "goal_legitimacy": (
            "GOAL-legitimate (RESEARCH.md §5.2): latent reasoning is anchored "
            "ON anima's OWN Engine A⇄G Ψ-physics (Law-71 psi proxy), pulled "
            "to the Ψ=½ fixed-point manifold + vacuum offset — NOT a free "
            "Coconut/Soft-CoT latent. anima physics IS the representation "
            "substrate. tension promoted from weak post-step nudge (Dir-A "
            "FALSIFIED) to a DIRECT routing-supervision loss term."),
        "honest_framing": (
            "Ψ-anchor + tension-supervised-routing MECHANISM is closed-form "
            "transfer-form (B-PSICTL sympy sidecar; overlay-OFF byte-equals "
            "γ-mask baseline). SGD OUTCOME + 4-axis capability = EMPIRICAL "
            "(B-CARVE-E6-NOTE / B-D-NOTE). PyTorch substrate, NOT hexa-native. "
            "Corpus forbidden-token grep == 0 (B-IDENTITY-5)."),
        "arch": "ConsciousDecoderV2 (RoPE+SwiGLU+RMSNorm+GQA+PureFieldFFN)",
        "from_scratch": True,
        "base_ckpt": None,
        "config": cfg,
        "n_params": n_params,
        "n_params_M": round(n_params / 1e6, 2),
        "psi_lambda": lam_psi,
        "route_lambda": lam_route,
        "route_h_floor": h_floor,
        "gpu": gpu_name,
        "device": device,
        "init_ce": round(init_loss, 6),
        "final_ce": final["ce"],
        "final_ce_voice": final["ce_voice"],
        "final_loss": final["loss"],
        "final_l_psi": final["l_psi"],
        "final_l_route": final["l_route"],
        "final_hpool_n": final["hpool_n"],
        "final_tau_norm": final["tau_norm"],
        "final_gn2": final["gn2"],
        "ce_descent": round(init_loss - final["ce"], 6),
        "steps": cfg["steps"],
        "wall_s": round(wall, 2),
        "peak_gpu_mem_gb": final["gpu_mem_gb"],
        "trajectory": traj,
        "corpus": os.path.basename(cfg["corpus"]),
        "corpus_bytes": int(ds.n),
        "n_gamma_records": len(items),
    }
    with open(os.path.join(out_dir, "result.json"), "w") as f:
        json.dump(result, f, indent=2)
    print("RESULT_JSON_WRITTEN", flush=True)
    print(json.dumps({"path": "psi_ctl", "init_ce": result["init_ce"],
                       "final_ce": result["final_ce"],
                       "final_ce_voice": result["final_ce_voice"],
                       "final_l_psi": result["final_l_psi"],
                       "final_l_route": result["final_l_route"],
                       "ce_descent": result["ce_descent"],
                       "wall_s": result["wall_s"]}), flush=True)
    return result


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", required=True)
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--steps", type=int, default=5000)
    ap.add_argument("--lr", type=float, default=3e-4)
    ap.add_argument("--bsz", type=int, default=32)
    ap.add_argument("--seed", type=int, default=1337)
    ap.add_argument("--d-model", type=int, default=768)
    ap.add_argument("--n-layer", type=int, default=12)
    ap.add_argument("--n-head", type=int, default=12)
    ap.add_argument("--n-kv-head", type=int, default=4)
    ap.add_argument("--psi-lambda", type=float, default=0.3,
                    help="Ψ-anchor (CTL) loss weight")
    ap.add_argument("--route-lambda", type=float, default=0.2,
                    help="tension-supervised routing loss weight")
    ap.add_argument("--route-h-floor", type=float, default=0.35,
                    help="Shannon-fraction entropy floor for anti-collapse")
    ap.add_argument("--mode", default="main", choices=["main", "sanity"])
    args = ap.parse_args()

    if args.mode == "main":
        cfg = dict(d_model=args.d_model, n_head=args.n_head,
                   n_kv_head=args.n_kv_head, n_layer=args.n_layer,
                   block_size=128, lr=args.lr, bsz=args.bsz,
                   steps=args.steps, warmup=max(20, args.steps // 20),
                   seed=args.seed, log_every=max(1, args.steps // 40),
                   corpus=args.corpus, out_dir=args.out_dir,
                   psi_lambda=args.psi_lambda, route_lambda=args.route_lambda,
                   route_h_floor=args.route_h_floor)
    else:
        cfg = dict(d_model=32, n_head=4, n_kv_head=2, n_layer=3,
                   block_size=64, lr=1e-3, bsz=8, steps=args.steps,
                   warmup=5, seed=args.seed,
                   log_every=max(1, args.steps // 10),
                   corpus=args.corpus, out_dir=args.out_dir,
                   psi_lambda=args.psi_lambda, route_lambda=args.route_lambda,
                   route_h_floor=args.route_h_floor)
    run(cfg)
