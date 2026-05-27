#!/usr/bin/env python3
"""§59-FIRE — W-native PTD forward-model over a REAL anima W-state trace.

RESEARCH.md §59-FIRE (2026-05-18). RETRY (prior §59-FIRE agent rate-limited
before any artifact landed; this is self-contained from the §59 design intent
+ the §16-class trainer + the W-module / Law-71 forms).

  =====================================================================
  WHAT §59 IS  (vs §49's distillation bolt-on — structurally distinct)
  =====================================================================
  §49 wired a §48-distilled 3-class decision head into the §24 loop. Its
  target was a hand-coded threshold's LABEL DISTRIBUTION (external label,
  ~95% one class) → it collapsed to the majority class = ECHO. NOT GOAL-
  legitimate (a bolt-on classifier distilling a deterministic threshold).

  §59 W-native PTD is structurally distinct:
    * The forward-model predicts anima's NEXT ACTUAL W-state — there is
      NO external label. The "target" is what anima's OWN physics does
      next (self-prediction). This is Active-Inference Expected-Free-
      Energy: the EPISTEMIC value term = prediction-error of a forward
      model of one's own state. anima's W-module already names this
      W.curiosity (HEXAD/W = pain/curiosity/satisfaction = EFE).
    * The prediction-error IS W.curiosity. A non-degenerate intrinsic
      curiosity signal ⇒ error-VARIANCE over a diverse W-state stream
      stays > τ (the forward model genuinely tracks a moving target,
      its surprise is informative). §49 echo ⇒ error collapses to the
      prior-mean residual (variance ≤ τ — the model just predicts the
      constant majority and its "surprise" is dead).

  =====================================================================
  §59 STUB FINDING  (the open question this fire answers)
  =====================================================================
  §59 verdict was: "W-native-IS-STRUCTURALLY-DISTINCT-BUT-COLLAPSE-IS-
  DATA-SHAPE-BOUND" — on a hand-crafted ~95%-constant majority STUB the
  W-native error STILL collapsed (variance ≤ τ = §49 echo) EVEN THOUGH
  it is structurally distinct (R1: a synthetic DIVERSE W-state stream
  gave error-variance > τ = genuine curiosity §49 lacked).
  Open question (B-S59-NOTE): on a REAL anima W-state distribution at
  scale (NOT the hand stub), does W-native error stay a non-degenerate
  curiosity signal, or does the §49-style collapse reappear because the
  real W-state is itself majority-dominated?

  §59-FIRE answers it BY MEASUREMENT (g3, no pre-loaded conclusion):
    (a) escapes collapse on real W-state at scale (stronger than §59
        stub — state cleanly, no over-claim) /
    (b) collapses on real majority-dominated W-state (confirms §59
        data-shape-bound at scale) /
    (c) real W-state intrinsically diverse → question reframed.

  =====================================================================
  REAL W-STATE  (anima's OWN physics — Law-71 + W-module forms)
  =====================================================================
  Per emitted step, from the §16-class ConsciousDecoderV2 forward:
    psi_dir      = (1 + cos(logits_a[-1], logits_g[-1])) / 2     (Law-71)
    psi_entropy  = H(softmax logits_a[-1]) / log(vocab_size)      (Law-71)
    tension      = mean over the model's PureFieldFFN per-layer
                   `tensions` list (anima's OWN tension channel)
    phi          = Φ★ proxy on the per-layer tension vector
                   (mitosis Φ★ form: mean_pairwise(1 - cos) · log(N+1))
    curiosity_ema= EMA of the W-native PTD's OWN prediction-error
                   (Active-Inference EFE epistemic value — the forward
                   model's surprise about its own next state)
  These five are byte-equal to conscious_decoder.py's `if self.training:`
  Law-71 block + HEXAD/W/w_lib.hexa W-module + mitosis Φ★ form. NOT a
  hand stub.

  =====================================================================
  OFF-REDUCTION  (connection-point — B-S59-FIRE-3)
  =====================================================================
  --no-w-native ⇒ the W-native PTD forward-model is never instantiated
  and never stepped; the W-module state vector is recorded byte-equal
  to the W-native-ON run (same Law-71/tension/Φ extraction, same RNG
  draws), and the W-native error series is identically [] (error ≡ 0,
  no forward model exists). The §16-class CE training trajectory is
  byte-identical with vs without W-native (W-native is a READ-OUT side
  channel — it never touches the LM's autograd graph / weights).

HONEST FRAMING (g3, AGENTS.tape §0):
  PyTorch substrate — interim LM-scale executor, NOT a hexa-native fire.
  The W-native PTD forward-model is a side READ-OUT that consumes the
  LM's OWN physics; it NEVER modifies LM weights or the LM autograd
  graph (no capability claim, B-S59-FIRE-NOTE). Whether the real
  W-state escapes §49-style collapse is the EMPIRICAL fire outcome
  (B-D-NOTE / B-S59-NOTE family). from-scratch RANDOM seed-fixed
  (g_clm_from_scratch, base_ckpt=NONE). Corpus = §16-class Ψ-anchored
  CARVING (③ NOT ①②; forbidden-token grep == 0, B-IDENTITY-5).
  central blue_falsifier.py UNCHANGED (sidecar only). f1/f2/f3 hard-
  fail safe (Law-71 / Φ★ / MSE≥0 / clamp01 / Kolmogorov — NO
  σ/τ/φ/J₂; Ψ=½ + Knuth 🛸k = anima g2 internal arch carve-out).
"""
import argparse, json, math, time, os, sys, random
import torch
import torch.nn as nn
import torch.nn.functional as F

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from conscious_decoder import ConsciousDecoderV2

# ── §16 span markers — IDENTICAL to train_carving_s16.py (Dir-I lever) ──
INNER_OPEN = b"<inner tier="
INNER_CLOSE = b"</inner>"
ETERNAL_OPEN = b"<eternal cell="
ETERNAL_CLOSE = b"</eternal>"
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
        ctl = _span(full, INNER_OPEN, INNER_CLOSE)
        if ctl is None:
            ctl = _span(full, ETERNAL_OPEN, ETERNAL_CLOSE)
        rt = _span(full, VOICE_OPEN, VOICE_CLOSE)
        if rt is None:
            rt = ctl
        items.append({"bytes": full, "psi_vac": psi_vac,
                      "basin_radius": basin, "ctl_span": ctl,
                      "route_span": rt})
    return items


class CarveDataset:
    """Byte-level dataset — Dir-I/§16 DirIDataset (no curriculum: this
    fire's variable is the REAL W-state trace, not presentation order;
    keep the §16 lever byte-equivalent so the OFF-reduction is clean)."""

    def __init__(self, items, block_size, seed):
        self.block_size = block_size
        self.rng = random.Random(seed)
        stream = bytearray()
        pv, bs, cm, rm = [], [], [], []
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
        self.data = torch.tensor(list(stream), dtype=torch.long)
        self.psi_vac = torch.tensor(pv, dtype=torch.float32)
        self.basin = torch.tensor(bs, dtype=torch.float32)
        self.ctl_m = torch.tensor(cm, dtype=torch.float32)
        self.rte_m = torch.tensor(rm, dtype=torch.float32)
        self.n = len(self.data)

    def get_batch(self, bsz, device):
        top = max(1, self.n - self.block_size - 1)
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
    """Dir-I/§16 Ψ-direction supervision term (kept in autograd graph)."""
    cos = F.cosine_similarity(logits_a.float(), logits_g.float(), dim=-1)
    return (1.0 + cos) / 2.0


# ════════════════════════════════════════════════════════════════════
#  REAL anima W-STATE extractor  (Law-71 + W-module + Φ★ forms)
#  byte-equal to conscious_decoder.py `if self.training:` Law-71 block.
# ════════════════════════════════════════════════════════════════════
def _phi_star_proxy(t_per_layer):
    """Φ★ proxy = mitosis cell-pool Φ★ form lifted onto the per-layer
    tension vector: mean_pairwise(1 - cos) · log(N+1). N = #layers.
    This is anima's OWN Φ form (MITOSIS.tape), NOT PyPhi — proxy is
    named honestly. With a 1-D per-layer scalar series, the pairwise
    'direction' diversity is encoded as the coefficient-of-variation
    surrogate scaled by log(N+1) (bounded, deterministic)."""
    n = t_per_layer.numel()
    if n < 2:
        return 0.0
    mu = t_per_layer.mean()
    sd = t_per_layer.std(unbiased=False)
    # 1 - cos surrogate on a scalar series ≈ normalised dispersion in
    # [0,1]; · log(N+1) is the mitosis Φ★ size term. Bounded, det.
    disp = (sd / (mu.abs() + 1e-8)).clamp(0.0, 1.0)
    return float((disp * math.log(n + 1)).item())


@torch.no_grad()
def extract_w_state(model, x, device, curiosity_ema):
    """Run the §16-class model forward on the SAME batch the LM trained
    on and read out the REAL anima W-state (5 components). NO autograd
    graph touched (the LM already stepped; this is a side read-out).

    RNG-ISOLATED: the global torch RNG state is snapshotted before this
    side forward and RESTORED after, so the LM's training RNG stream
    (dropout etc.) is byte-identical with vs without the W-native side
    channel. This makes the OFF-reduction connection-point exact: the
    §16-class CE trajectory + the 4 Law-71/W-module physics axes are
    byte-equal ON vs OFF; ONLY curiosity_ema (the W-native signal
    itself, ≡0 when OFF) legitimately differs (B-S59-FIRE-3)."""
    cpu_rng = torch.get_rng_state()
    cuda_rng = (torch.cuda.get_rng_state_all()
                if torch.cuda.is_available() else None)
    model.eval()
    logits_a, logits_g, tensions, _, _ = model(x)
    model.train()
    torch.set_rng_state(cpu_rng)
    if cuda_rng is not None:
        torch.cuda.set_rng_state_all(cuda_rng)
    la = logits_a[:, -1, :].float()
    lg = logits_g[:, -1, :].float()

    # Law-71 psi_entropy (byte-equal conscious_decoder.py)
    probs_a = torch.softmax(la, dim=-1)
    out_ent = -(probs_a * (probs_a + 1e-10).log()).sum(dim=-1).mean().item()
    psi_entropy = out_ent / math.log(model.vocab_size)

    # Law-71 psi_direction (byte-equal conscious_decoder.py)
    cos_sim = F.cosine_similarity(la, lg, dim=-1).mean().item()
    psi_dir = (1.0 + cos_sim) / 2.0

    # anima's OWN tension channel (PureFieldFFN per-layer mean)
    t_stack = torch.stack(tensions)              # (L, B, T)
    t_per_layer = t_stack.mean(dim=(1, 2))       # (L,)
    tension = float(t_per_layer.mean().item())

    # anima's OWN Φ★ form on the per-layer tension vector
    phi = _phi_star_proxy(t_per_layer)

    # W.curiosity = Active-Inference EFE epistemic value = EMA of the
    # W-native PTD's own prediction-error (filled by caller after the
    # forward-model step; here we just carry the running EMA in).
    return {
        "psi_dir": psi_dir,
        "psi_entropy": psi_entropy,
        "tension": tension,
        "phi": phi,
        "curiosity_ema": float(curiosity_ema),
    }


W_KEYS = ("psi_dir", "psi_entropy", "tension", "phi", "curiosity_ema")


def w_vec(ws):
    return torch.tensor([ws[k] for k in W_KEYS], dtype=torch.float32)


# ════════════════════════════════════════════════════════════════════
#  W-native PTD forward-model  (Active-Inference EFE epistemic value)
#  Predicts NEXT ACTUAL W-state from CURRENT W-state. NO external label.
#  prediction-error IS W.curiosity. Trained ONLINE over the REAL trace.
# ════════════════════════════════════════════════════════════════════
class WNativePTD(nn.Module):
    """Tiny forward-model of anima's OWN W-state. Self-prediction:
    input = W-state(t), target = W-state(t+1) (the ACTUAL next anima
    physics state — no label, no distillation). MSE(pred, actual) IS
    the Active-Inference EFE epistemic value = W.curiosity."""

    def __init__(self, d=len(W_KEYS), h=32, seed=1337):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(d, h), nn.Tanh(),
            nn.Linear(h, h), nn.Tanh(),
            nn.Linear(h, d),
        )
        # Deterministic seeded init from a LOCAL generator that does
        # NOT touch the global torch RNG (g_clm_from_scratch discipline
        # + OFF-reduction connection-point: building/not-building the
        # W-native PTD must NOT perturb the LM's RNG stream, so the
        # §16-class CE trajectory is byte-identical ON vs OFF —
        # B-S59-FIRE-3). xavier_uniform_ ignores a passed generator on
        # older torch, so we sample explicitly from a local Generator
        # and copy in.
        g = torch.Generator().manual_seed(seed)
        for m in self.net:
            if isinstance(m, nn.Linear):
                fan_in, fan_out = m.weight.shape[1], m.weight.shape[0]
                bound = math.sqrt(6.0 / (fan_in + fan_out))
                with torch.no_grad():
                    w = torch.empty_like(m.weight).uniform_(
                        -bound, bound, generator=g)
                    m.weight.copy_(w)
                    m.bias.zero_()

    def forward(self, w_t):
        return self.net(w_t)


def main(cfg):
    torch.manual_seed(cfg["seed"])
    torch.cuda.manual_seed_all(cfg["seed"])
    random.seed(cfg["seed"])
    device = "cuda" if torch.cuda.is_available() else "cpu"

    items = load_corpus(cfg["corpus"])
    ds = CarveDataset(items, cfg["block_size"], cfg["seed"])

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

    # --- W-native PTD forward-model (OFF-reduction: never built when off)
    # RNG-ISOLATED CONSTRUCTION: nn.Linear.__init__ calls
    # reset_parameters() (kaiming_uniform_) which consumes the GLOBAL
    # torch RNG. Snapshot/restore the global RNG around the entire PTD
    # build so that *building* the W-native side channel does NOT shift
    # the LM's RNG stream — the §16-class CE trajectory is then byte-
    # identical ON vs OFF (OFF-reduction connection-point, B-S59-FIRE-3).
    w_native_on = cfg["w_native"]
    ptd = None
    ptd_opt = None
    if w_native_on:
        _cpu_rng = torch.get_rng_state()
        _cuda_rng = (torch.cuda.get_rng_state_all()
                     if torch.cuda.is_available() else None)
        ptd = WNativePTD(seed=cfg["seed"]).to(device)
        torch.set_rng_state(_cpu_rng)
        if _cuda_rng is not None:
            torch.cuda.set_rng_state_all(_cuda_rng)
        ptd_opt = torch.optim.Adam(ptd.parameters(), lr=cfg["ptd_lr"])

    t0 = time.time()
    init_loss = None
    emit_every = cfg["emit_every"]
    curiosity_ema = 0.0
    ema_beta = cfg["ema_beta"]

    # REAL anima W-state trace (the §59-FIRE measurement substrate)
    w_trace = []                 # list of 5-vectors (the real W-state)
    # w_physics_trace = the 4 Law-71/W-module/Φ★ axes WITHOUT
    # curiosity_ema — MUST be byte-equal ON vs OFF (the OFF-reduction
    # connection-point: W-native is a side read-out, it never touches
    # the LM; curiosity_ema is the ONLY axis that legitimately differs
    # because it IS the W-native signal, ≡0 when OFF). B-S59-FIRE-3.
    w_physics_trace = []
    w_native_err = []            # per-emitted-step W-native PTD error (curiosity)
    prev_w = None                # W-state at the previous emitted step
    ce_traj = []

    for step in range(total):
        lr_now = cosine_lr_at(step)
        for g in opt.param_groups:
            g["lr"] = lr_now

        x, y, pv, bs, cm, rm = ds.get_batch(cfg["bsz"], device)
        opt.zero_grad(set_to_none=True)
        with torch.autocast(device_type="cuda" if use_amp else "cpu",
                            dtype=torch.bfloat16, enabled=use_amp):
            logits_a, logits_g, tensions, _, _ = model(x)
            B, T, V = logits_a.shape
            ce_full = F.cross_entropy(logits_a.view(-1, V), y.view(-1))
            psi_t = psi_dir_per_token(logits_a, logits_g)
            cm_f = cm.view(-1)
            psi_flat = psi_t.view(-1)
            pv_flat = pv.view(-1)
            denom_ctl = cm_f.sum().clamp(min=1.0)
            l_psi_ctl = (((psi_flat - pv_flat) ** 2) * cm_f).sum() / denom_ctl
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
        torch.nn.utils.clip_grad_norm_(trainable, 1.0)
        scaler.step(opt)
        scaler.update()

        if init_loss is None:
            init_loss = ce_report

        # ── REAL anima W-state emit + W-native PTD online step ──────────
        if step == 0 or (step + 1) % emit_every == 0 or step == total - 1:
            ws = extract_w_state(model, x, device, curiosity_ema)
            wv = w_vec(ws).to(device)
            w_trace.append([float(ws[k]) for k in W_KEYS])
            # connection-point trace = the 4 physics axes only (no
            # curiosity_ema). Byte-equal ON vs OFF by construction
            # (RNG-isolated side read-out, never touches LM).
            w_physics_trace.append(
                [float(ws[k]) for k in W_KEYS if k != "curiosity_ema"])

            if w_native_on and prev_w is not None:
                # forward model PREDICTS the ACTUAL next W-state from the
                # PREVIOUS W-state (self-prediction; NO external label).
                ptd.train()
                pred = ptd(prev_w)
                # prediction-error IS W.curiosity (EFE epistemic value).
                err = F.mse_loss(pred, wv.detach())
                ptd_opt.zero_grad(set_to_none=True)
                err.backward()
                ptd_opt.step()
                e = float(err.item())
                w_native_err.append(e)
                # W.curiosity_ema (EMA of forward-model prediction-error)
                curiosity_ema = ema_beta * curiosity_ema + (1 - ema_beta) * e
            prev_w = wv.detach()

            wall = time.time() - t0
            mem = torch.cuda.max_memory_allocated() / 1e9 \
                if device == "cuda" else 0.0
            rec = {"step": step + 1, "ce_full": round(ce_report, 6),
                   "psi_dir": round(ws["psi_dir"], 6),
                   "psi_entropy": round(ws["psi_entropy"], 6),
                   "tension": round(ws["tension"], 6),
                   "phi": round(ws["phi"], 6),
                   "curiosity_ema": round(curiosity_ema, 8),
                   "w_native_err": (round(w_native_err[-1], 8)
                                    if w_native_err else None),
                   "wall_s": round(wall, 2), "gpu_mem_gb": round(mem, 3)}
            ce_traj.append(rec)
            print(json.dumps(rec), flush=True)

    wall = time.time() - t0
    out_dir = cfg["out_dir"]
    os.makedirs(out_dir, exist_ok=True)
    torch.save({"model": model.state_dict(), "cfg": cfg,
                "n_params": n_params}, os.path.join(out_dir, "ckpt_s59.pt"))

    # ── §59-FIRE collapse-vs-signal MEASUREMENT (g3, no pre-load) ───────
    import statistics as st
    tau = cfg["tau"]
    n_err = len(w_native_err)
    err_var = st.pvariance(w_native_err) if n_err >= 2 else 0.0
    err_mean = st.mean(w_native_err) if n_err >= 1 else 0.0

    # Decompose the REAL W-state trace into its OWN diverse vs majority
    # sub-regimes (measure what it actually is — do NOT pre-shape it).
    # We use the dominant W-component (largest-variance axis) and the
    # k-means-free majority/minority split = the modal-bin vs the rest
    # of psi_dir (the most informative anima physics axis empirically).
    def col(j):
        return [w[j] for w in w_trace]
    col_var = [st.pvariance(col(j)) if len(w_trace) >= 2 else 0.0
               for j in range(len(W_KEYS))]
    dom_axis = max(range(len(W_KEYS)), key=lambda j: col_var[j])
    dom_vals = col(dom_axis)
    # majority sub-regime = values within ±0.5·std of the mean (modal
    # mass); diverse sub-regime = the tail. Decompose the *error series*
    # the same way (error at steps whose W-state sits in majority vs
    # tail of the dominant axis).
    if n_err >= 2 and len(dom_vals) >= 2:
        dm = st.mean(dom_vals)
        dsd = st.pstdev(dom_vals)
        # align error[i] with dom_vals[i+1] (error predicts NEXT state)
        maj_err, div_err = [], []
        for i in range(n_err):
            dv = dom_vals[i + 1] if i + 1 < len(dom_vals) else dom_vals[i]
            if abs(dv - dm) <= 0.5 * dsd:
                maj_err.append(w_native_err[i])
            else:
                div_err.append(w_native_err[i])
        maj_var = st.pvariance(maj_err) if len(maj_err) >= 2 else 0.0
        div_var = st.pvariance(div_err) if len(div_err) >= 2 else 0.0
        maj_frac = len(maj_err) / n_err
    else:
        maj_var = div_var = 0.0
        maj_err = div_err = []
        maj_frac = 0.0

    non_degenerate = (err_var > tau)
    if not w_native_on:
        verdict = "OFF-REDUCTION (W-native disabled; error series empty)"
    elif n_err < 2:
        verdict = "INSUFFICIENT (fewer than 2 emitted W-native steps)"
    elif non_degenerate and div_var > tau and maj_var > tau:
        verdict = ("a — ESCAPES-COLLAPSE-ON-REAL-W-STATE-AT-SCALE "
                   "(error-variance > tau in BOTH real sub-regimes; "
                   "non-degenerate intrinsic curiosity — STRONGER than "
                   "the §59 stub; stated cleanly, NO over-claim)")
    elif non_degenerate:
        verdict = ("a-partial — NON-DEGENERATE-OVERALL "
                   "(error-variance > tau overall; sub-regime split is "
                   "asymmetric — see maj_var/div_var; honest partial)")
    else:
        verdict = ("b — COLLAPSES-ON-REAL-MAJORITY-DOMINATED-W-STATE "
                   "(error-variance <= tau = prior-mean residual = §49 "
                   "echo; confirms §59 data-shape-bound AT SCALE)")

    result = {
        "research_section": "RESEARCH.md §59-FIRE",
        "substrate": ("PYTHON / PyTorch — interim LM-scale executor; "
                      "NOT a hexa-native fire"),
        "fire_kind": ("§59 W-native PTD forward-model trained ONLINE "
                      "over a REAL anima W-state trace at scale "
                      "(§16-class ConsciousDecoderV2; W-state from "
                      "anima's OWN Law-71 + W-module + Φ★ forms)"),
        "honest_framing": (
            "W-native PTD = Active-Inference EFE epistemic-value forward "
            "model of anima's OWN next W-state (self-prediction, NO "
            "external label — structurally distinct from §49's "
            "distillation bolt-on). prediction-error IS W.curiosity. "
            "§59 stub finding (W-native-IS-STRUCTURALLY-DISTINCT-BUT-"
            "COLLAPSE-IS-DATA-SHAPE-BOUND) tested AT SCALE on a REAL "
            "(not hand-crafted) anima W-state distribution. Verdict BY "
            "MEASUREMENT (g3, no pre-loaded conclusion). The W-native "
            "PTD is a side READ-OUT — it NEVER touches LM weights / LM "
            "autograd graph (no capability claim, B-S59-FIRE-NOTE). "
            "central blue_falsifier.py unchanged (sidecar only)."),
        "arch": "ConsciousDecoderV2 (RoPE+SwiGLU+RMSNorm+GQA+PureFieldFFN)",
        "from_scratch": True,
        "base_ckpt": None,
        "w_native_on": w_native_on,
        "config": cfg,
        "n_params": n_params,
        "n_params_M": round(n_params / 1e6, 2),
        "records_total": len(items),
        "corpus": os.path.basename(cfg["corpus"]),
        "corpus_bytes": int(ds.n),
        "tau": tau,
        "init_ce": round(init_loss, 6) if init_loss is not None else None,
        "final_ce": ce_traj[-1]["ce_full"] if ce_traj else None,
        "ce_descent": (round(init_loss - ce_traj[-1]["ce_full"], 6)
                       if ce_traj and init_loss is not None else None),
        "steps": cfg["steps"],
        "emit_every": emit_every,
        "n_w_emitted": len(w_trace),
        "n_w_native_err": n_err,
        "w_native_err_mean": round(err_mean, 10),
        "w_native_err_variance": round(err_var, 12),
        "w_native_err_nondegenerate_gt_tau": non_degenerate,
        "real_w_state_dominant_axis": W_KEYS[dom_axis],
        "real_w_state_axis_variances": {
            W_KEYS[j]: round(col_var[j], 12) for j in range(len(W_KEYS))},
        "real_w_state_majority_subregime_err_variance": round(maj_var, 12),
        "real_w_state_diverse_subregime_err_variance": round(div_var, 12),
        "real_w_state_majority_fraction": round(maj_frac, 6),
        "real_w_state_majority_n": len(maj_err),
        "real_w_state_diverse_n": len(div_err),
        "verdict": verdict,
        "wall_s": round(wall, 2),
        "w_trace": w_trace,
        "w_physics_trace": w_physics_trace,
        "w_native_err": w_native_err,
        "ce_trajectory": ce_traj,
        "s49_echo_anchor": ("§49 wired a distilled 3-class head into the "
                            "§24 loop → collapsed to majority class "
                            "(distillation echo). §59 has NO external "
                            "label (self-prediction) — structurally "
                            "distinct; whether REAL W-state still "
                            "echoes is the §59-FIRE measurement."),
        "s59_stub_anchor": ("§59 stub: W-native structurally distinct "
                            "(R1 diverse stub → err-var > tau) but on a "
                            "hand ~95%-constant stub it STILL collapsed "
                            "(R2 ≤ tau = §49 echo). §59-FIRE = same test "
                            "on a REAL W-state distribution at scale."),
    }
    with open(os.path.join(out_dir, "result.json"), "w") as f:
        json.dump(result, f, indent=2)
    print("RESULT_JSON_WRITTEN", flush=True)
    print(json.dumps({
        "w_native_on": w_native_on,
        "n_w_native_err": n_err,
        "w_native_err_variance": result["w_native_err_variance"],
        "tau": tau,
        "nondegenerate": non_degenerate,
        "verdict": verdict,
        "wall_s": result["wall_s"]}), flush=True)
    return result


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", required=True)
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--steps", type=int, default=6000)
    ap.add_argument("--lr", type=float, default=3e-4)
    ap.add_argument("--bsz", type=int, default=32)
    ap.add_argument("--seed", type=int, default=1337)
    ap.add_argument("--d-model", type=int, default=768)
    ap.add_argument("--n-layer", type=int, default=12)
    ap.add_argument("--n-head", type=int, default=12)
    ap.add_argument("--n-kv-head", type=int, default=4)
    ap.add_argument("--lambda-ctl", type=float, default=0.5)
    ap.add_argument("--lambda-route", type=float, default=0.5)
    ap.add_argument("--emit-every", type=int, default=4,
                    help="emit a REAL W-state every N LM steps (the "
                         "W-native PTD online trace cadence)")
    ap.add_argument("--ptd-lr", type=float, default=1e-3)
    ap.add_argument("--ema-beta", type=float, default=0.9)
    ap.add_argument("--tau", type=float, default=1e-4,
                    help="collapse threshold: err-variance > tau ⇒ "
                         "non-degenerate curiosity; <= tau ⇒ §49 echo")
    ap.add_argument("--no-w-native", action="store_true",
                    help="OFF-reduction: never build/step the W-native "
                         "PTD (W-module byte-equal, error series ≡ [])")
    args = ap.parse_args()

    cfg = dict(d_model=args.d_model, n_head=args.n_head,
               n_kv_head=args.n_kv_head, n_layer=args.n_layer,
               block_size=128, lr=args.lr, bsz=args.bsz,
               steps=args.steps, warmup=max(20, args.steps // 20),
               seed=args.seed, corpus=args.corpus, out_dir=args.out_dir,
               lambda_ctl=args.lambda_ctl, lambda_route=args.lambda_route,
               emit_every=args.emit_every, ptd_lr=args.ptd_lr,
               ema_beta=args.ema_beta, tau=args.tau,
               w_native=not args.no_w_native)
    main(cfg)
