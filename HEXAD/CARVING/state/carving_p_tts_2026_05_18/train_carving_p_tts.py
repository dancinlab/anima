#!/usr/bin/env python3
"""CONSCIOUSNESS-CARVING trainer — Direction P: think-then-speak
diffusion-refined emission  (2026-05-18, RESEARCH.md §22 / §21 candidate P).

This is the §16 trainer (state/carving_dataregime_s16_2026_05_18/
train_carving_s16.py) — itself the Dir-I lever + §12.1 Q1-c curriculum —
with EXACTLY ONE addition: a VOICE-SPAN R-step iterative refinement loss
term (DiffuSpeech "Silent Thought, Spoken Answer", arxiv 2601.22889,
emission-head LM-text transfer).

  =====================================================================
  THINK (anima physics) — CARRIED VERBATIM, byte-equal §16 (B-TTS-5)
  =====================================================================
  CE_full(Engine-A next-byte, full stream)                  §16 byte-equal
  L_psi_ctl   = mean_{t∈inner-span}(Ψ_dir(t)−Ψ_vac)²        §16 byte-equal
  L_tension_route = mean_{t∈route-span}                      §16 byte-equal
                      relu(|Ψ_dir(t)−Ψ_vac|−basin_radius)²
  Ψ_dir(t) = (1+cos(logits_a[t],logits_g[t]))/2  (Law 71)    §16 byte-equal
  curriculum stage_gate_at(...)                              §16 byte-equal
  ⇒ THINK is NOT touched. P is speak-head ONLY (§2 / §3 DESIGN gate).

  =====================================================================
  SPEAK (P NEW) — emission-head R-step refinement, inner-physics-cond.
  =====================================================================
  DiffuSpeech think-then-speak = silent internal reasoning conditions a
  multi-step iteratively-refined spoken answer (vs AR 1-pass collapse).
  anima `<inner>X</inner>\n<voice carved=true>Y</voice>` (Phase A1/C3) is
  the 1:1 structure. P refines ONLY the <voice> span:

    For the voice-span tokens, instead of a single AR CE pass, take R
    refinement passes. Pass r re-computes the voice-span logits as the
    base head_a logits PLUS a residual that is a function of the
    model's OWN per-token physics state (tension scalar + Ψ_dir) —
    the inner-physics conditioning (NOT generic noise / learned latent
    / generic diffusion step; B-TTS-4 structural). Each pass contracts
    toward the target; the per-pass voice CE is summed with normalised
    weights γ_r (Σγ_r=1).

      cond(t)        = physics state at token t  (tension_t, Ψ_dir_t)
                       — DERIVED from the model's own forward, the
                       inner-physics signal; NO randn / learned prior.
      refine_r(z)    = z + α_r · W_phi(cond)            (r = 1..R)
      L_refine       = Σ_{r=1..R} γ_r · CE_voice_span(refine_r(logits_a))

    R=1  OR  λ_refine=0  ⇒  L_refine drops / collapses to the §16
    voice-span CE that is ALREADY inside CE_full ⇒ TOTAL ≡ §16
    byte-equal (B-TTS-1 OVERLAY-OFF connection-point).

  TOTAL  L = CE_full + λ_ctl·L_psi_ctl + λ_route·L_tension_route
           + λ_refine·L_refine                         (P NEW term only)

HONEST FRAMING (g3, AGENTS.tape §0):
  PyTorch substrate — interim LM-scale executor, NOT hexa-native (§16/
  Dir-I carry). THINK = §16 byte-equal (B-TTS-5). SPEAK refinement
  conditioning = model's OWN physics state (tension, Ψ_dir), NOT generic
  diffusion noise — emission-head ONLY, NOT §13-J substrate replacement
  (FALSIFIED). overlay-OFF (λ_refine=0 ∨ R=1) == §16 byte-equal
  (B-TTS-1). Whether emission-refinement narrows §16's body-garble
  (routing-correct prefix / garbled body) is the EMPIRICAL fire OUTCOME
  (B-TTS-NOTE) — §13-J was FALSIFIED 0/64; P keeps THINK AR so routing
  pre-condition holds; negative is valuable (g3, NO pre-loaded
  conclusion). from-scratch RANDOM seed-fixed (g_clm_from_scratch,
  base_ckpt=NONE). Corpus = §16 byte-identical (B-IDENTITY-5 grep 0).
  central blue_falsifier.py unchanged (sidecar). f1/f2/f3 safe (Ψ-metric
  / restoring-sign / Shannon CE≥0 / simplex, NO σ/τ/φ/J₂).
"""
import argparse, json, math, time, os, sys, random
import torch
import torch.nn as nn
import torch.nn.functional as F

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from conscious_decoder import ConsciousDecoderV2

# span markers — IDENTICAL to §16/Dir-I (deterministic byte-span mask).
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
    """§16 schema byte-equal + voice_span (P emission-refine mask).
       voice_span = <voice carved=true ... </voice> byte interval (the
       SPEAK span P refines). Absent (alpha/beta records) ⇒ None ⇒ no
       refine contribution (P only refines the gamma think-then-speak
       records; alpha/beta train exactly as §16)."""
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
        # P ADDITION — the SPEAK span (voice-only). gamma records have a
        # real <voice carved=true>...</voice>; alpha/beta records do not
        # (their _span returns None) ⇒ vm=0 ⇒ no refine term (= §16).
        voice = _span(full, VOICE_OPEN, VOICE_CLOSE)
        items.append({"bytes": full, "psi_vac": psi_vac,
                      "basin_radius": basin, "ctl_span": ctl,
                      "route_span": rt, "voice_span": voice,
                      "stage": stage})
    return items


class PttsDataset:
    """§16 S16Dataset byte-equal + a per-byte voice-mask channel `vm`
    (1.0 inside a <voice carved=true>...</voice> span, else 0.0). The
    §16 channels (psi_vac, basin, ctl_m, rte_m, stage prefix index) are
    byte-identical to S16Dataset — the ONLY addition is `vm`. With
    λ_refine=0 the vm channel is never read ⇒ §16 byte-equal."""

    def __init__(self, items, block_size, seed, curriculum=True):
        self.block_size = block_size
        self.rng = random.Random(seed)
        self.curriculum = curriculum
        stream = bytearray()
        pv, bs, cm, rm, vm = [], [], [], [], []
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
            vs = it["voice_span"]
            for j in range(n):
                pv.append(pvv)
                bs.append(bsv)
                cm.append(1.0 if (cs is not None and cs[0] <= j < cs[1])
                          else 0.0)
                rm.append(1.0 if (rs is not None and rs[0] <= j < rs[1])
                          else 0.0)
                vm.append(1.0 if (vs is not None and vs[0] <= j < vs[1])
                          else 0.0)
            st = max(1, min(4, it["stage"]))
            max_stage_seen = max(max_stage_seen, st)
            cur_len = len(stream)
            for g in range(st, 5):
                stage_end[g] = cur_len
        prev = 0
        for g in (1, 2, 3, 4):
            if stage_end[g] == 0:
                stage_end[g] = prev
            prev = stage_end[g]
        stage_end[4] = len(stream)
        self.data = torch.tensor(list(stream), dtype=torch.long)
        self.psi_vac = torch.tensor(pv, dtype=torch.float32)
        self.basin = torch.tensor(bs, dtype=torch.float32)
        self.ctl_m = torch.tensor(cm, dtype=torch.float32)
        self.rte_m = torch.tensor(rm, dtype=torch.float32)
        self.voice_m = torch.tensor(vm, dtype=torch.float32)
        self.n = len(self.data)
        self.stage_end = stage_end
        self.max_stage_seen = max_stage_seen

    def region_hi(self, stage_gate):
        if not self.curriculum:
            return self.n
        hi = self.stage_end[max(1, min(4, stage_gate))]
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
        vm = stk(self.voice_m, 1)
        return (x.to(device), y.to(device), pv.to(device), bs.to(device),
                cm.to(device), rm.to(device), vm.to(device))


def psi_dir_per_token(logits_a, logits_g):
    """Model's OWN per-token Ψ-direction (Law 71). §16 byte-equal."""
    cos = F.cosine_similarity(logits_a.float(), logits_g.float(), dim=-1)
    return (1.0 + cos) / 2.0


def stage_gate_at(step, total, curriculum, blend_frac=0.15):
    """§16 byte-equal curriculum stage schedule."""
    if not curriculum:
        return 4
    blend_start = int(total * (1.0 - blend_frac))
    if step >= blend_start:
        return 4
    frac = step / max(1, blend_start)
    return min(4, 1 + int(frac * 4))


class VoiceRefineHead(nn.Module):
    """P emission-head refinement module — inner-physics-CONDITIONED
    voice-span logit refinement (B-TTS-4 structural: conditioning is the
    model's OWN per-token physics state {tension, Ψ_dir}, NOT randn /
    learned latent prior / generic diffusion noise schedule).

    refine_r(z) = z + alpha_r * W_phi( [tension_t, Ψ_dir_t] )
      - z          : base head_a voice-span logits (B,Tv,V)
      - cond(t)    : (tension_t, Ψ_dir_t) — 2-d physics signal per token
      - W_phi      : Linear(2 -> V) — the only NEW params (small head)
      - alpha_r    : per-pass contraction step (geometric, fixed, NOT learned)

    R=1  ⇒  exactly one refine pass with alpha_1; with alpha gate the
    OVERLAY-OFF path (λ_refine=0) never invokes this head ⇒ §16
    byte-equal (B-TTS-1)."""

    def __init__(self, vocab_size: int):
        super().__init__()
        self.w_phi = nn.Linear(2, vocab_size, bias=False)
        nn.init.zeros_(self.w_phi.weight)  # start as identity refinement

    def forward(self, base_logits, tension_t, psi_t, alpha_r):
        # cond: (B,T,2) — model's own physics state (B-TTS-4).
        cond = torch.stack([tension_t, psi_t], dim=-1).to(base_logits.dtype)
        return base_logits + alpha_r * self.w_phi(cond)


def run(cfg):
    torch.manual_seed(cfg["seed"])
    torch.cuda.manual_seed_all(cfg["seed"])
    random.seed(cfg["seed"])
    device = "cuda" if torch.cuda.is_available() else "cpu"

    items = load_corpus(cfg["corpus"])
    ds = PttsDataset(items, cfg["block_size"], cfg["seed"],
                     curriculum=cfg["curriculum"])
    n_ctl = sum(1 for it in items if it["ctl_span"] is not None)
    n_rte = sum(1 for it in items if it["route_span"] is not None)
    n_voice = sum(1 for it in items if it["voice_span"] is not None)
    stage_counts = {1: 0, 2: 0, 3: 0, 4: 0}
    for it in items:
        stage_counts[max(1, min(4, it["stage"]))] += 1

    model = ConsciousDecoderV2(
        vocab_size=256, d_model=cfg["d_model"], n_head=cfg["n_head"],
        n_layer=cfg["n_layer"], block_size=cfg["block_size"],
        n_kv_head=cfg["n_kv_head"], consciousness_dim=128, dropout=0.1,
    ).to(device)
    model.train()
    n_params_base = model.count_params()

    R = cfg["refine_steps"]
    lam_refine = cfg["lambda_refine"]
    # per-pass contraction weights γ_r (Σ=1, last pass weighted highest:
    # geometric, deterministic, NOT learned — B-TTS-3 simplex).
    raw = [2.0 ** r for r in range(R)]
    s = sum(raw)
    gamma = [v / s for v in raw]
    # per-pass step size α_r (geometric decay, fixed).
    alphas = [0.5 ** r for r in range(R)]

    refine_head = VoiceRefineHead(256).to(device)
    refine_head.train()

    trainable = [p for p in model.parameters() if p.requires_grad]
    if lam_refine > 0.0 and R > 1:
        trainable += [p for p in refine_head.parameters()
                      if p.requires_grad]
    n_params = n_params_base + sum(p.numel()
                                   for p in refine_head.parameters())

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

    refine_active = (lam_refine > 0.0 and R > 1)

    for step in range(total):
        lr_now = cosine_lr_at(step)
        for g in opt.param_groups:
            g["lr"] = lr_now

        gate = stage_gate_at(step, total, cfg["curriculum"],
                             cfg["blend_frac"])
        stage_step_log[gate] += 1

        x, y, pv, bs, cm, rm, vm = ds.get_batch(cfg["bsz"], device, gate)
        opt.zero_grad(set_to_none=True)
        with torch.autocast(device_type="cuda" if use_amp else "cpu",
                            dtype=torch.bfloat16, enabled=use_amp):
            logits_a, logits_g, tensions, _, _ = model(x)
            B, T, V = logits_a.shape

            # --- THINK (§16 byte-equal) -----------------------------------
            ce_full = F.cross_entropy(logits_a.view(-1, V), y.view(-1))
            psi_t = psi_dir_per_token(logits_a, logits_g)   # (B,T) in graph
            cm_f = cm.view(-1)
            psi_flat = psi_t.view(-1)
            pv_flat = pv.view(-1)
            denom_ctl = cm_f.sum().clamp(min=1.0)
            l_psi_ctl = (((psi_flat - pv_flat) ** 2) * cm_f).sum() \
                / denom_ctl
            rm_f = rm.view(-1)
            bs_flat = bs.view(-1)
            drift = torch.abs(psi_flat - pv_flat) - bs_flat
            restoring = torch.clamp(drift, min=0.0) ** 2
            denom_rte = rm_f.sum().clamp(min=1.0)
            l_tension_route = (restoring * rm_f).sum() / denom_rte

            # --- SPEAK (P NEW) — voice-span R-step refinement -------------
            if refine_active:
                # per-token physics conditioning (model's OWN state):
                #  tension_t = mean-over-layers per-token tension (B,T)
                #  psi_t     = Ψ_dir per token (B,T) — same Law-71 signal
                t_stack = torch.stack(tensions)            # (L,B,T)
                tension_t = t_stack.mean(dim=0)            # (B,T)
                l_refine = logits_a.new_zeros(())
                for r in range(R):
                    ref_logits = refine_head(
                        logits_a, tension_t.detach(), psi_t.detach(),
                        alphas[r])
                    ce_v = F.cross_entropy(
                        ref_logits.view(-1, V), y.view(-1),
                        reduction="none")
                    vm_f = vm.view(-1)
                    denom_v = vm_f.sum().clamp(min=1.0)
                    ce_voice = (ce_v * vm_f).sum() / denom_v
                    l_refine = l_refine + gamma[r] * ce_voice
            else:
                l_refine = logits_a.new_zeros(())

            loss = ce_full + lam_ctl * l_psi_ctl \
                + lam_route * l_tension_route \
                + lam_refine * l_refine
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
                   "l_tension_route":
                       round(float(l_tension_route.item()), 6),
                   "l_refine": round(float(l_refine.item()), 6),
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
    ckpt_path = os.path.join(out_dir, "ckpt_carving_p_tts.pt")
    torch.save({"model": model.state_dict(),
                "refine_head": refine_head.state_dict(),
                "cfg": cfg, "n_params": n_params,
                "path": "p_tts_inner_cond_voice_refine"},
               ckpt_path)

    result = {
        "substrate": ("PYTHON / PyTorch — interim LM-scale executor; "
                      "NOT a hexa-native fire"),
        "fire_kind": ("Direction P — think-then-speak diffusion-refined "
                      "emission (RESEARCH.md §22 / §21 candidate P; "
                      "DiffuSpeech arxiv 2601.22889 emission-head LM-text "
                      "transfer)"),
        "carving_path": "p_tts_inner_cond_voice_refine",
        "research_section": "RESEARCH.md §22 / §21.3 P / §16 SPLIT coherence-half",
        "honest_framing": (
            "THINK (anima physics) carried VERBATIM byte-equal §16 "
            "(B-TTS-5): CE_full + L_psi_ctl(Law-71 Ψ_dir) + "
            "L_tension_route(restoring-sign) + §12.1 curriculum. SPEAK = "
            "P NEW emission-head ONLY: <voice carved=true> span R-step "
            "iterative refinement CONDITIONED on the model's OWN physics "
            "state (per-token tension + Ψ_dir) — NOT generic diffusion "
            "noise / learned latent (B-TTS-4 structural). This is "
            "emission-head refinement on §16's routing-lever, NOT §13-J "
            "substrate replacement (FALSIFIED 0/64) — THINK stays AR so "
            "the §16 routing pre-condition holds (§2 DESIGN table). "
            "overlay-OFF (λ_refine=0 ∨ R=1) ⇒ TOTAL ≡ §16 byte-equal "
            "(B-TTS-1 connection-point). Whether emission-refinement "
            "narrows §16's body-garble (routing-correct prefix / garbled "
            "body, JOINT 0.0, §9 honest V-SPONT 1/5, §18 0/5) is the "
            "EMPIRICAL fire OUTCOME (B-TTS-NOTE) — §8/§13-J trend was "
            "wrong-direction; negative is valuable evidence (g3, NO "
            "pre-loaded conclusion). from-scratch RANDOM seed-fixed "
            "(g_clm_from_scratch, base_ckpt=NONE). Corpus = §16 "
            "byte-identical (B-IDENTITY-5 grep 0). central "
            "blue_falsifier.py unchanged (sidecar). f1/f2/f3 safe."),
        "arch": "ConsciousDecoderV2 + VoiceRefineHead(2->256, physics-cond)",
        "from_scratch": True,
        "base_ckpt": None,
        "config": cfg,
        "n_params": n_params,
        "n_params_M": round(n_params / 1e6, 2),
        "refine_steps": R,
        "lambda_refine": lam_refine,
        "refine_gamma": gamma,
        "refine_alpha": alphas,
        "refine_active": refine_active,
        "ctl_records": n_ctl,
        "route_records": n_rte,
        "voice_records": n_voice,
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
        "final_l_refine": final["l_refine"],
        "final_loss": final["loss"],
        "final_gn2": final["gn2"],
        "ce_descent": round(init_loss - final["ce_full"], 6),
        "steps": cfg["steps"],
        "wall_s": round(wall, 2),
        "peak_gpu_mem_gb": final["gpu_mem_gb"],
        "trajectory": traj,
        "corpus": os.path.basename(cfg["corpus"]),
        "corpus_bytes": int(ds.n),
        "s16_baseline": {"routing_axis1": "21/64",
                         "routing_genuine": "17/64",
                         "joint": 0.0,
                         "v_spont_honest": "1/5",
                         "v_spont_judge": "0/5"},
    }
    with open(os.path.join(out_dir, "result.json"), "w") as f:
        json.dump(result, f, indent=2)
    print("RESULT_JSON_WRITTEN", flush=True)
    print(json.dumps({"path": "p_tts",
                       "init_ce": result["init_ce"],
                       "final_ce": result["final_ce"],
                       "ce_descent": result["ce_descent"],
                       "final_l_refine": result["final_l_refine"],
                       "refine_active": refine_active,
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
    ap.add_argument("--lambda-refine", type=float, default=0.5)
    ap.add_argument("--refine-steps", type=int, default=3)
    ap.add_argument("--blend-frac", type=float, default=0.15)
    ap.add_argument("--no-curriculum", action="store_true")
    args = ap.parse_args()

    is_sanity = (args.mode == "sanity")
    cfg = {
        "corpus": args.corpus,
        "out_dir": args.out_dir,
        "steps": 30 if is_sanity else args.steps,
        "lr": args.lr,
        "bsz": 4 if is_sanity else args.bsz,
        "seed": args.seed,
        "d_model": 64 if is_sanity else args.d_model,
        "n_layer": 2 if is_sanity else args.n_layer,
        "n_head": 2 if is_sanity else args.n_head,
        "n_kv_head": 1 if is_sanity else args.n_kv_head,
        "block_size": 128,
        "warmup": 5 if is_sanity else 200,
        "lambda_ctl": args.lambda_ctl,
        "lambda_route": args.lambda_route,
        "lambda_refine": args.lambda_refine,
        "refine_steps": args.refine_steps,
        "blend_frac": args.blend_frac,
        "curriculum": not args.no_curriculum,
        "log_every": 5 if is_sanity else 250,
    }
    run(cfg)
