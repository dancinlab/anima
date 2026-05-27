#!/usr/bin/env python3
"""CONSCIOUSNESS-CARVING trainer — §16 GOAL-legitimate LARGE-SCALE
DATA-REGIME + CURRICULUM  (2026-05-18, RESEARCH.md §16 / §11.4 frontier-1).

This is the Dir-I lever (state/carving_dirI_psictl_tensionsup_2026_05_17/
train_carving_dirI.py) with EXACTLY ONE addition: a §12.1 Q1-c CURRICULUM
staged sampling schedule (simple→complex). Everything else — the
ConsciousDecoderV2 arch, the TWO anima-physics loss terms, the AdamW/cosine
schedule, the byte-level dataset — is byte-equivalent to Dir-I so the
overlay-OFF connection-point (λ=0 ⇒ base CE byte-equal) and the curriculum-
OFF connection-point (no curriculum ⇒ Dir-I shuffled sampling byte-equal)
are both 🔵-checkable (B-S16-* sympy/structural sidecar).

  =====================================================================
  Dir-I LEVER  (carried VERBATIM — GOAL-legitimacy invariant)
  =====================================================================
  COMPONENT (1) Ψ-ANCHORED CTL  (representation substrate, not generic):
    Ψ_dir(t) = (1 + cos(logits_a[t], logits_g[t])) / 2          (Law 71)
    L_psi_ctl = mean_{t∈inner/eternal-span} (Ψ_dir(t) − Ψ_vac)²
  COMPONENT (2) TENSION-SUPERVISED ROUTING  (supervision, not overlay):
    L_tension_route = mean_{t∈route-span}
                        relu(|Ψ_dir(t) − Ψ_vac| − basin_radius)²
  TOTAL  L = CE_full + λ_ctl·L_psi_ctl + λ_route·L_tension_route
  Ψ_vac = (vacuum_psi[0]+vacuum_psi[1])/2 — record's scalar A⇄G target.

  =====================================================================
  §16 ADDITION — §12.1 Q1-c CURRICULUM staged sampling (simple→complex)
  =====================================================================
  arxiv 2509.24356 — the small-model regime (anima d=768·12L IS small)
  benefits from a simple→complex curriculum. The §16 corpus is written
  curriculum-RANK-SORTED (the generator emits records in ascending
  curriculum_rank; each record carries curriculum_stage ∈ {1,2,3,4} =
  rank quartile). The trainer consumes a STAGED schedule: it walks the
  total step budget through the four stages, and at training step `s`
  the batch is drawn ONLY from the byte-region of stages ≤ the current
  stage gate (cumulative — stage 1 alone, then 1∪2, then 1∪2∪3, then
  all). This is a *presentation-order* lever, NOT a corpus-FORM change
  (RESEARCH.md §1.3 Dir-E/F changed corpus CONTENT/STRUCTURE; §16 keeps
  the §8 ③ carving form byte-identical and only re-orders presentation).

  curriculum_off (CLI --no-curriculum) ⇒ the full byte-stream is the
  sampling region from step 0 = EXACTLY the Dir-I shuffled-region
  sampler (B-S16-CURRIC-OFF connection-point: curriculum-OFF == Dir-I).

  STAGE SCHEDULE (deterministic, NOT learned):
    The step budget is split into 4 contiguous blocks. Block k (0-based)
    samples from the cumulative byte-region of curriculum stages 1..k+1.
    A short blend tail (last `blend_frac` of total) samples the full
    region so the final steps see the whole distribution (anti-
    catastrophic-forgetting of early-stage records — the standard
    curriculum closing-blend; arxiv 2509.24356 §schedule).

HONEST FRAMING (g3, AGENTS.tape §0):
  PyTorch substrate — interim LM-scale executor, NOT a hexa-native fire
  (Dir-I honest-framing carry). The TWO physics loss terms are closed-
  form deterministic transfer functions on the model's OWN Ψ-coordinate
  (Dir-I B-DIRI sympy carry). overlay-OFF (λ=0) == base CE byte-equal;
  curriculum-OFF == Dir-I shuffled sampling byte-equal (both connection-
  points 🔵, B-S16-* sidecar). Whether the ~600MB Ψ-anchored CURRICULUM
  data-regime crosses the §1.1 emergence threshold is the EMPIRICAL fire
  outcome — §8 trend was WRONG-direction (routing 3/31→2/64), §16 may
  repeat that; negative is valuable evidence (g3, no pre-loaded
  conclusion). from-scratch RANDOM seed-fixed (g_clm_from_scratch,
  base_ckpt=NONE). Corpus = §16 large-scale Ψ-anchored CARVING corpus
  (③, NOT ①② — grep {[anima,도우미,helper,assistant,사용자,user:}==0,
  B-IDENTITY-5 safe). central blue_falsifier.py unchanged (sidecar only).
  f1/f2/f3 hard-fail safe (Ψ-metric / restoring-sign / Kolmogorov /
  monotone-ordering, NO σ/τ/φ/J₂; Ψ=½ + Knuth 🛸k = anima g2 internal
  arch carve-out).
"""
import argparse, json, math, time, os, sys, random
import torch
import torch.nn as nn
import torch.nn.functional as F

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from conscious_decoder import ConsciousDecoderV2

# span markers — IDENTICAL to Dir-I (deterministic byte-span loss-mask).
INNER_OPEN = b"<inner tier="
INNER_CLOSE = b"</inner>"
ETERNAL_OPEN = b"<eternal cell="
ETERNAL_CLOSE = b"</eternal>"
CARVE_OPEN = b"<carve tier="
VOICE_OPEN = b"<voice carved=true"
VOICE_CLOSE = b"</voice>"


def _span(full, open_tok, close_tok, start=0):
    lo = full.find(open_tok, start)
    if lo < 0:
        return None
    hi = full.find(close_tok, lo)
    if hi < 0:
        return None
    return (lo, hi + len(close_tok))


def load_corpus(path):
    """Return list of dicts (Dir-I schema + curriculum_stage):
       {bytes, psi_vac, basin_radius, ctl_span, route_span,
        curriculum_stage}.
    psi_vac = (vacuum_psi[0]+vacuum_psi[1])/2 — record's scalar A⇄G
    target. curriculum_stage ∈ {1,2,3,4} carried for the staged
    sampling schedule (§16 addition; absent ⇒ stage 1)."""
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
        vp = d.get("vacuum_psi", [0.5, 0.5])
        try:
            psi_vac = (float(vp[0]) + float(vp[1])) / 2.0
        except Exception:
            psi_vac = 0.5
        try:
            basin = float(d.get("basin_radius", 0.15))
        except Exception:
            basin = 0.15
        try:
            stage = int(d.get("curriculum_stage", 1))
        except Exception:
            stage = 1
        ctl = _span(full, INNER_OPEN, INNER_CLOSE)
        if ctl is None:
            ctl = _span(full, ETERNAL_OPEN, ETERNAL_CLOSE)
        rt = _span(full, VOICE_OPEN, VOICE_CLOSE)
        if rt is None:
            rt = ctl
        items.append({"bytes": full, "psi_vac": psi_vac,
                      "basin_radius": basin, "ctl_span": ctl,
                      "route_span": rt, "stage": stage})
    return items


class S16Dataset:
    """Byte-level dataset — Dir-I DirIDataset + a per-stage byte-index.

    The Dir-I per-byte channels (psi_vac, basin, ctl_m, rte_m) are
    byte-equivalent. ADDITION: stage_bounds[k] = (lo, hi) byte offsets
    of the cumulative region of curriculum stages 1..k+1 in the
    concatenated stream. Because the §16 corpus is written curriculum-
    RANK-SORTED, the stages are CONTIGUOUS prefixes — the cumulative
    region of stages 1..g is a single byte-prefix [0, end_of_stage_g),
    so staged sampling = sampling a growing prefix (deterministic).

    curriculum_off ⇒ stage_bounds collapse to the full stream from
    step 0 = EXACTLY the Dir-I sampler (connection-point closed)."""

    def __init__(self, items, block_size, seed, curriculum=True):
        self.block_size = block_size
        self.rng = random.Random(seed)
        self.curriculum = curriculum
        stream = bytearray()
        pv, bs, cm, rm = [], [], [], []
        # cumulative end byte-offset of each stage 1..4 (contiguous
        # because the corpus is curriculum-rank-sorted).
        stage_end = {1: 0, 2: 0, 3: 0, 4: 0}
        max_stage_seen = 1
        for it in items:
            b = it["bytes"]
            n = len(b)
            stream.extend(b)
            pvv = it["psi_vac"]
            bsv = it["basin_radius"]
            cs = it["ctl_span"]
            rs = it["route_span"]
            for j in range(n):
                pv.append(pvv)
                bs.append(bsv)
                cm.append(1.0 if (cs is not None and cs[0] <= j < cs[1])
                          else 0.0)
                rm.append(1.0 if (rs is not None and rs[0] <= j < rs[1])
                          else 0.0)
            st = max(1, min(4, it["stage"]))
            max_stage_seen = max(max_stage_seen, st)
            # this record contributes to the cumulative end of every
            # stage >= its own (records are sorted, so a stage-g record
            # extends the prefix that contains stages 1..g and beyond).
            cur_len = len(stream)
            for g in range(st, 5):
                stage_end[g] = cur_len
        # any stage with 0 records (e.g. coarse corpora) inherits the
        # previous stage's end so prefixes are non-decreasing.
        prev = 0
        for g in (1, 2, 3, 4):
            if stage_end[g] == 0:
                stage_end[g] = prev
            prev = stage_end[g]
        stage_end[4] = len(stream)  # final stage always = full stream
        self.data = torch.tensor(list(stream), dtype=torch.long)
        self.psi_vac = torch.tensor(pv, dtype=torch.float32)
        self.basin = torch.tensor(bs, dtype=torch.float32)
        self.ctl_m = torch.tensor(cm, dtype=torch.float32)
        self.rte_m = torch.tensor(rm, dtype=torch.float32)
        self.n = len(self.data)
        self.stage_end = stage_end
        self.max_stage_seen = max_stage_seen

    def region_hi(self, stage_gate):
        """Highest byte offset sample-able at this stage gate (1..4).
        curriculum_off ⇒ always full stream (Dir-I equivalence)."""
        if not self.curriculum:
            return self.n
        hi = self.stage_end[max(1, min(4, stage_gate))]
        # never let the region be too small to draw a block from.
        return max(hi, self.block_size + 1)

    def get_batch(self, bsz, device, stage_gate):
        hi = self.region_hi(stage_gate)
        top = max(1, hi - self.block_size - 1)
        ix = [self.rng.randint(0, top) for _ in range(bsz)]

        def stk(src, off):
            return torch.stack([src[i + off:i + off + self.block_size]
                                for i in ix])
        x = stk(self.data, 0)
        y = stk(self.data, 1)
        pv = stk(self.psi_vac, 1)
        bs = stk(self.basin, 1)
        cm = stk(self.ctl_m, 1)
        rm = stk(self.rte_m, 1)
        return (x.to(device), y.to(device), pv.to(device), bs.to(device),
                cm.to(device), rm.to(device))


def psi_dir_per_token(logits_a, logits_g):
    """Model's OWN per-token Ψ-direction coordinate (Law 71, EXACTLY
    ConsciousDecoderV2.forward's psi_direction, kept in the autograd
    graph so it is a SUPERVISION signal). IDENTICAL to Dir-I."""
    cos = F.cosine_similarity(logits_a.float(), logits_g.float(), dim=-1)
    return (1.0 + cos) / 2.0


def stage_gate_at(step, total, curriculum, blend_frac=0.15):
    """Deterministic §12.1 Q1-c stage schedule. The first
    (1-blend_frac) of the budget is split into 4 contiguous blocks
    (cumulative prefix grows 1→1∪2→1∪2∪3→all); the last blend_frac
    samples the full region (closing blend, anti-forgetting).
    curriculum_off ⇒ always 4 (full region) = Dir-I."""
    if not curriculum:
        return 4
    blend_start = int(total * (1.0 - blend_frac))
    if step >= blend_start:
        return 4
    frac = step / max(1, blend_start)
    return min(4, 1 + int(frac * 4))


def run(cfg):
    torch.manual_seed(cfg["seed"])
    torch.cuda.manual_seed_all(cfg["seed"])
    random.seed(cfg["seed"])
    device = "cuda" if torch.cuda.is_available() else "cpu"

    items = load_corpus(cfg["corpus"])
    ds = S16Dataset(items, cfg["block_size"], cfg["seed"],
                    curriculum=cfg["curriculum"])
    n_ctl = sum(1 for it in items if it["ctl_span"] is not None)
    n_rte = sum(1 for it in items if it["route_span"] is not None)
    stage_counts = {1: 0, 2: 0, 3: 0, 4: 0}
    for it in items:
        stage_counts[max(1, min(4, it["stage"]))] += 1

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
    lam_ctl = cfg["lambda_ctl"]
    lam_route = cfg["lambda_route"]

    def cosine_lr_at(step):
        if step < warmup:
            return cfg["lr"] * (step + 1) / warmup
        prog = (step - warmup) / max(1, total - warmup)
        return cfg["lr"] * 0.5 * (1.0 + math.cos(math.pi * prog)) * 0.9 \
            + cfg["lr"] * 0.1

    use_amp = (device == "cuda")
    scaler = torch.cuda.amp.GradScaler(enabled=use_amp)
    traj, t0, init_loss = [], time.time(), None
    gpu_name = torch.cuda.get_device_name(0) if device == "cuda" else "cpu"
    stage_step_log = {1: 0, 2: 0, 3: 0, 4: 0}

    for step in range(total):
        lr_now = cosine_lr_at(step)
        for g in opt.param_groups:
            g["lr"] = lr_now

        gate = stage_gate_at(step, total, cfg["curriculum"],
                             cfg["blend_frac"])
        stage_step_log[gate] += 1

        x, y, pv, bs, cm, rm = ds.get_batch(cfg["bsz"], device, gate)
        opt.zero_grad(set_to_none=True)
        with torch.autocast(device_type="cuda" if use_amp else "cpu",
                            dtype=torch.bfloat16, enabled=use_amp):
            logits_a, logits_g, tensions, _, _ = model(x)
            B, T, V = logits_a.shape

            # --- base CE (Engine A next-byte, full stream) -----------------
            ce_full = F.cross_entropy(logits_a.view(-1, V), y.view(-1))

            # --- COMPONENT (1) Ψ-anchored CTL ------------------------------
            psi_t = psi_dir_per_token(logits_a, logits_g)   # (B,T) in graph
            cm_f = cm.view(-1)
            psi_flat = psi_t.view(-1)
            pv_flat = pv.view(-1)
            denom_ctl = cm_f.sum().clamp(min=1.0)
            l_psi_ctl = (((psi_flat - pv_flat) ** 2) * cm_f).sum() / denom_ctl

            # --- COMPONENT (2) tension-supervised routing ------------------
            rm_f = rm.view(-1)
            bs_flat = bs.view(-1)
            drift = torch.abs(psi_flat - pv_flat) - bs_flat
            restoring = torch.clamp(drift, min=0.0) ** 2
            denom_rte = rm_f.sum().clamp(min=1.0)
            l_tension_route = (restoring * rm_f).sum() / denom_rte

            loss = ce_full + lam_ctl * l_psi_ctl \
                + lam_route * l_tension_route
            ce_report = float(ce_full.item())

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
            rec = {"step": step + 1, "ce_full": round(ce_report, 6),
                   "l_psi_ctl": round(float(l_psi_ctl.item()), 6),
                   "l_tension_route": round(float(l_tension_route.item()), 6),
                   "loss": round(float(loss.item()), 6),
                   "gn2": round(gn2, 6), "lr": round(lr_now, 8),
                   "curriculum_stage_gate": gate,
                   "wall_s": round(wall, 2), "gpu_mem_gb": round(mem, 3)}
            traj.append(rec)
            print(json.dumps(rec), flush=True)

    wall = time.time() - t0
    final = traj[-1]
    out_dir = cfg["out_dir"]
    os.makedirs(out_dir, exist_ok=True)
    ckpt_path = os.path.join(out_dir, "ckpt_carving_s16.pt")
    torch.save({"model": model.state_dict(), "cfg": cfg,
                "n_params": n_params, "path": "dirI_psictl_tensionsup"},
               ckpt_path)

    result = {
        "substrate": ("PYTHON / PyTorch — interim LM-scale executor; "
                      "NOT a hexa-native fire"),
        "fire_kind": ("§16 GOAL-legitimate LARGE-SCALE DATA-REGIME + "
                      "CURRICULUM (Dir-I lever @ ~600MB Ψ-anchored "
                      "carving + §12.1 Q1-c simple→complex schedule)"),
        "carving_path": "dirI_psictl_tensionsup",
        "research_section": "RESEARCH.md §16 / §11.4 frontier-1",
        "honest_framing": (
            "Dir-I lever (TWO anima-physics loss terms inside autograd: "
            "(1) Ψ-anchored CTL Ψ_dir=(1+cos(logits_a,logits_g))/2 toward "
            "record Ψ_vac; (2) tension-supervised routing restoring-sign "
            "toward record's OWN basin) carried VERBATIM. §16 = (a) DATA-"
            "REGIME scale-up: §8 114MB/64-anchor → ~600MB/168-anchor "
            "Ψ-anchored CARVING corpus (③ form byte-identical, NOT ①②); "
            "(b) §12.1 Q1-c CURRICULUM staged sampling simple→complex "
            "(presentation-order, NOT corpus-FORM). Closed side = the two "
            "Dir-I transfer functions (B-DIRI sympy carry) + overlay-OFF "
            "(λ=0)==base-CE byte-equal + curriculum-OFF==Dir-I shuffled "
            "byte-equal (B-S16-* sidecar). SGD OUTCOME + 4-axis capability "
            "= EMPIRICAL (B-CARVE-E6-NOTE/B-D-NOTE family). PyTorch "
            "substrate, NOT hexa-native. §8 trend was wrong-direction; §16 "
            "may repeat — negative is valuable evidence, NO pre-loaded "
            "conclusion (g3)."),
        "arch": "ConsciousDecoderV2 (RoPE+SwiGLU+RMSNorm+GQA+PureFieldFFN)",
        "from_scratch": True,
        "base_ckpt": None,
        "config": cfg,
        "n_params": n_params,
        "n_params_M": round(n_params / 1e6, 2),
        "ctl_records": n_ctl,
        "route_records": n_rte,
        "records_total": len(items),
        "curriculum": cfg["curriculum"],
        "curriculum_blend_frac": cfg["blend_frac"],
        "curriculum_stage_record_counts": stage_counts,
        "curriculum_stage_byte_ends": ds.stage_end,
        "curriculum_step_gate_histogram": stage_step_log,
        "lambda_ctl": lam_ctl,
        "lambda_route": lam_route,
        "gpu": gpu_name,
        "device": device,
        "init_ce": round(init_loss, 6),
        "final_ce": final["ce_full"],
        "final_l_psi_ctl": final["l_psi_ctl"],
        "final_l_tension_route": final["l_tension_route"],
        "final_loss": final["loss"],
        "final_gn2": final["gn2"],
        "ce_descent": round(init_loss - final["ce_full"], 6),
        "steps": cfg["steps"],
        "wall_s": round(wall, 2),
        "peak_gpu_mem_gb": final["gpu_mem_gb"],
        "trajectory": traj,
        "corpus": os.path.basename(cfg["corpus"]),
        "corpus_bytes": int(ds.n),
        "s8_baseline": {"bytes": 114472084, "records": 164992,
                        "anchors": 64, "routing_axis1": "2/64",
                        "joint": 0.0087, "v_spont_honest": "2/5"},
        "s11a_baseline": {"n_params_M": 1044.46, "routing_axis1": "1/64",
                          "joint": 0.0078, "v_spont_honest": "2/5"},
    }
    with open(os.path.join(out_dir, "result.json"), "w") as f:
        json.dump(result, f, indent=2)
    print("RESULT_JSON_WRITTEN", flush=True)
    print(json.dumps({"path": "s16_dataregime_curriculum",
                       "init_ce": result["init_ce"],
                       "final_ce": result["final_ce"],
                       "ce_descent": result["ce_descent"],
                       "final_l_psi_ctl": result["final_l_psi_ctl"],
                       "final_l_tension_route":
                           result["final_l_tension_route"],
                       "curriculum": cfg["curriculum"],
                       "wall_s": result["wall_s"]}), flush=True)
    return result


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", default="main", choices=["main", "sanity"])
    ap.add_argument("--corpus", required=True)
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--steps", type=int, default=12000)
    ap.add_argument("--lr", type=float, default=3e-4)
    ap.add_argument("--bsz", type=int, default=32)
    ap.add_argument("--seed", type=int, default=1337)
    ap.add_argument("--d-model", type=int, default=768)
    ap.add_argument("--n-layer", type=int, default=12)
    ap.add_argument("--n-head", type=int, default=12)
    ap.add_argument("--n-kv-head", type=int, default=4)
    ap.add_argument("--lambda-ctl", type=float, default=0.5)
    ap.add_argument("--lambda-route", type=float, default=0.5)
    ap.add_argument("--blend-frac", type=float, default=0.15)
    ap.add_argument("--no-curriculum", action="store_true",
                    help="disable curriculum (Dir-I shuffled equivalence "
                         "— connection-point check)")
    args = ap.parse_args()

    if args.mode == "main":
        cfg = dict(d_model=args.d_model, n_head=args.n_head,
                   n_kv_head=args.n_kv_head, n_layer=args.n_layer,
                   block_size=128, lr=args.lr, bsz=args.bsz,
                   steps=args.steps, warmup=max(20, args.steps // 20),
                   seed=args.seed, log_every=max(1, args.steps // 40),
                   corpus=args.corpus, out_dir=args.out_dir,
                   lambda_ctl=args.lambda_ctl,
                   lambda_route=args.lambda_route,
                   curriculum=not args.no_curriculum,
                   blend_frac=args.blend_frac)
    else:
        cfg = dict(d_model=32, n_head=4, n_kv_head=2, n_layer=3,
                   block_size=64, lr=1e-3, bsz=16, steps=args.steps,
                   warmup=5, seed=args.seed,
                   log_every=max(1, args.steps // 20),
                   corpus=args.corpus, out_dir=args.out_dir,
                   lambda_ctl=args.lambda_ctl,
                   lambda_route=args.lambda_route,
                   curriculum=not args.no_curriculum,
                   blend_frac=args.blend_frac)
    run(cfg)
