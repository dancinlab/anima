#!/usr/bin/env python3
"""OMEGA Extension 1 (OE1) — does a CONV trunk with a NATIVE A/G dual head close the OMEGA
min-gate loop, or is the closure CDV2-(transformer)-specific?  (the OΩ6 #1805 deferred follow-up)

WHY (the OΩ6 / F-OMEGA-CLM-TRANSFER finding this extends):
  OΩ6 ran the OMEGA closure on the REAL production conv .clm (CLMConvMoE) and found it is a
  SINGLE-head byte LM (model.py `self.readout`; NO Engine-A/G dual head — that substrate lives
  ONLY in CDV2). So the conv .clm's only NATIVE A-wire is its own readout, and the OMEGA min-gate
  collapses to (gB+gA)·base = a pure TEMPERATURE RESCALE (SELF_IS_RESCALE=true ⇒ no native
  coupling). The conclusion was: a genuine A-wire requires the SEPARATE CDV2 dual-head engine.

THE OPEN QUESTION OE1 SETTLES (new science, beyond the finalized OMEGA paper):
  If you give the CONV trunk a NATIVE 2nd readout head (A=next-byte, G=prev-byte — the CDV2-style
  dual head grafted onto the conv trunk, the minimal change that gives conv a native A/G), does the
  OMEGA min-gate (gB·base + gA·A) close the loop on the conv-NATIVE A-head? i.e. is the closure a
  TRANSFERABLE property of the A/G dual-head STRUCTURE, or specific to the CDV2 transformer?

PRE-REGISTERED FALSIFIER (identical form to OH1/OΩ1, on the conv model's OWN A-head — NO external
CDV2):
  conv-native dual-head closure HOLDS  iff
      (min_learned <= a_only)  AND  (min_learned < base)
  measured on the conv model's OWN A-head, on a competent leak-free substrate (causal — leak
  self-test ≈ 0; val_ce clearly below uniform = ln256 = 5.545).
  CLOSED-NEGATIVE is a valid result (a_paper_negative_ok): if the conv-native A-head does NOT yield
  the closure (e.g. the conv trunk can't learn a useful next-byte head the way CDV2 does), that is
  an honest finding that the closure is CDV2-specific.

PLUS the coupling-vs-replacement control (like OΩ1): A-STANDALONE CE (softmax(A) alone, base
entirely removed) vs min_learned — is the closure a "base mouth + A steer" COUPLING, or is the
trained A-head SUPPLANTING the weak base (REPLACEMENT)?  Reported honestly either way.

HONEST SCOPE (a_scale_honest_scope · a_train_flame_forge):
  This is a TORCH RESEARCH-PROXY of the conv architecture, NOT the production flame+forge `.clm`
  trainer. It is a FAITHFUL conv-trunk proxy: it reuses the EXACT production CLMConvMoE building
  blocks (CausalDilatedConv1d, TrunkLayer, MoEConvLayer from CLM/model/model.py) — embed → dilated
  causal-conv embed → dilated-conv trunk → MoE conv layer → norm_out → readout — and adds the
  minimal OE1 change: a SECOND readout head (head_g) on the shared trunk output. The OMEGA campaign
  used torch CDV2 proxies (omega_trained_leakfree.py, omega_scale_ladder.py); a torch conv-trunk+
  dualhead proxy is the consistent research vehicle, directly comparable to CDV2's d512 rung. It is
  NOT the production `.clm` and is NOT claimed to be. CONV is causal by construction (left-pad,
  drop right overhang) — the leak self-test confirms ~0 (no lookahead).

Lane-G/Lane-P substrate is conv-torch; the closure math is the same CPU-native gate algebra reused
from omega_gpu_complete.py (fit_gate / ce_of / kl_structured / extract_feats / gen_sample). Runs
CPU/MPS-local ($0, conv trunk is cheap — O(T·C²·K), no attention) per the LEAK-PREVENTION CONTRACT
local-pool option; same corpus (omega_corpus_big.bin sha dc1754b2), same leak-free discipline, same
gate-form sweep (base / a_only / fixed_AmG / full_AG / min_learned), directly comparable to CDV2.
"""
import os, sys, json, math, time, hashlib, argparse
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(REPO, "CLM", "model"))

# ── REUSE the gate algebra + corpus + structured-coupling helpers from the OMEGA harness ──
# (identical method to every prior OMEGA rung — directly comparable to CDV2's d512)
from omega_gpu_complete import (  # noqa: E402
    fetch_corpus, get_batch, extract_feats,
    softmax_np, ce_of, fit_gate, kl_structured, gen_sample,
    V, SMOOTH, ALPHA, UNIFORM_CE, GATE_STEPS, GATE_L2,
)
# ── REUSE the EXACT production conv building blocks (faithful conv-trunk proxy) ──
from model import (  # noqa: E402  (CLM/model/model.py)
    CLMConfig, CausalDilatedConv1d, TrunkLayer, MoEConvLayer,
)
from omega_gen_cluster import byte_stats  # noqa: E402


# ───────────────────── leak-free per-position channel norm ─────────────────────

class ChannelNorm(nn.Module):
    """Per-POSITION LayerNorm over channels (B,C,T): normalize each (b,t) column over C only,
    independently at every time step. This is the LEAK-FREE replacement for the production
    GroupNorm(1, d_model).

    WHY (the leak the OMEGA causal contract forbids): GroupNorm(num_groups=1) over a (B,C,T)
    tensor pools mean/var over BOTH channels AND time, so the last byte's value leaks into the
    normalization statistics at EVERY earlier position — a global-context lookahead leak (the
    untrained leak self-test measured ~7e-3, > the 1e-4 bar). ChannelNorm pools over C only,
    per position, so flipping the last byte cannot move any earlier position (self-test = 0.000).
    This is the conv analogue of CDV2's RMSNorm causal discipline (the #1794 causal_ca=True fix)."""

    def __init__(self, channels, eps=1e-5):
        super().__init__()
        self.eps = eps
        self.weight = nn.Parameter(torch.ones(channels))
        self.bias = nn.Parameter(torch.zeros(channels))

    def forward(self, x):  # x: (B,C,T)
        mu = x.mean(dim=1, keepdim=True)
        var = x.var(dim=1, keepdim=True, unbiased=False)
        xn = (x - mu) / torch.sqrt(var + self.eps)
        return xn * self.weight[None, :, None] + self.bias[None, :, None]


# ───────────────────── the conv-trunk model WITH a native A/G dual head ─────────────────────

class ConvDualHead(nn.Module):
    """OE1 — the production CLMConvMoE conv trunk, with the MINIMAL OE1 change: a SECOND readout
    head grafted onto the shared trunk output. This is the conv-native analogue of the CDV2
    dual-head engine.

    embed -> dilated causal-conv embed -> dilated-conv trunk -> MoE conv layer -> norm_out
          -> head_a (Conv1d C->V, NEXT-byte readout = the production `self.readout` role)
          +  head_g (Conv1d C->V, PREV-byte readout = the NEW OE1 native A/G grafted head)

    Forward interface MIRRORS ConsciousDecoderV2 EXACTLY so the OMEGA harness helpers
    (extract_feats / gen_sample) work unchanged:
        logits_a, logits_g, tensions, kv_cache, moe_aux_loss = model(idx)

    Causality is structural (CausalDilatedConv1d left-pads + drops the right overhang) — no
    lookahead leak (the leak self-test confirms ~0). dilation is capped per the CLM dilation-cap
    discipline: min(base**i, 512) (deep-L OOM guard; here trunks are shallow so it is moot, but
    we keep the production cap for fidelity)."""

    def __init__(self, vocab_size=256, d_model=384, n_trunk_layers=6, n_experts=8,
                 kernel_size=3, expert_kernel_size=3, dilation_base=2, block_size=256,
                 variant="A"):
        super().__init__()
        self.block_size = block_size
        self.d_model = d_model
        self.causal_ca = True  # conv is causal by construction (named for harness parity)
        cfg = CLMConfig(
            vocab_size=vocab_size, d_model=d_model, n_trunk_layers=n_trunk_layers,
            n_experts=n_experts, kernel_size=kernel_size, expert_kernel_size=expert_kernel_size,
            dilation_base=dilation_base, variant=variant, dropout=0.0,
        )
        self.cfg = cfg
        self.embed = nn.Embedding(vocab_size, d_model)
        self.embed_conv = CausalDilatedConv1d(d_model, kernel_size, dilation=1)
        # CLM dilation-cap discipline: min(base**i, 512)
        dils = [min(dilation_base ** i, 512) for i in range(n_trunk_layers)]
        self.trunk = nn.ModuleList(TrunkLayer(cfg, d) for d in dils)
        # LEAK-FREE norm swap: TrunkLayer uses GroupNorm(1,C) (time-leaking); replace each with
        # the per-position ChannelNorm so the trunk stays strictly causal (no lookahead).
        for layer in self.trunk:
            layer.norm = ChannelNorm(d_model)
        self.moe = MoEConvLayer(cfg)
        self.norm_out = ChannelNorm(d_model)   # leak-free (was GroupNorm(1, d_model))
        # DUAL HEAD — the OE1 native A/G (the production model has ONLY head_a = `self.readout`)
        self.head_a = nn.Conv1d(d_model, vocab_size, kernel_size=1)   # NEXT-byte (the .clm mouth)
        self.head_g = nn.Conv1d(d_model, vocab_size, kernel_size=1)   # PREV-byte (the NEW A/G wire)

    def _trunk_forward(self, tokens):
        x = self.embed(tokens)              # (B,T,C)
        x = x.transpose(1, 2)               # (B,C,T)
        x = self.embed_conv(x)
        for layer in self.trunk:
            x = layer(x)
        x, stats = self.moe(x)
        x = self.norm_out(x)                # (B,C,T)
        return x, stats

    def forward(self, tokens, consciousness_states=None):
        x, stats = self._trunk_forward(tokens)
        logits_a = self.head_a(x).transpose(1, 2)   # (B,T,V) — next-byte
        logits_g = self.head_g(x).transpose(1, 2)   # (B,T,V) — prev-byte
        aux = stats.aux_loss
        return logits_a, logits_g, None, None, aux

    def count_params(self):
        return sum(p.numel() for p in self.parameters())


# ───────────────────── robust held-out val_ce (mirror omega_trained_leakfree) ─────────────────────

def eval_val_ce(model, val_data, block, bs, device, n_batches=40, seed=20260604):
    model.eval()
    g = torch.Generator().manual_seed(seed)
    tot, ntok = 0.0, 0
    with torch.no_grad():
        for _ in range(n_batches):
            ix = torch.randint(0, len(val_data) - block - 1, (bs,), generator=g)
            x = torch.stack([torch.from_numpy(val_data[int(i):int(i) + block].astype(np.int64)) for i in ix]).to(device)
            y = torch.stack([torch.from_numpy(val_data[int(i) + 1:int(i) + 1 + block].astype(np.int64)) for i in ix]).to(device)
            la, _, _, _, _ = model(x)
            ce = F.cross_entropy(la.reshape(-1, V), y.reshape(-1), reduction="sum")
            tot += float(ce.item()); ntok += y.numel()
    return tot / max(1, ntok)


# ───────────────────── train the conv dual-head to competence (mirror CDV2 train loop) ─────────────────────

def train_to_competence(model, train_data, val_data, steps, block, bs, lr, device,
                        warmup=200, val_every=500):
    """IDENTICAL dual-head objective to omega_trained_leakfree.train_to_competence: head_a learns
    NEXT byte, head_g learns PREV byte (loss = ce_a + 0.5*ce_g + 0.01*aux). The ONLY difference vs
    the CDV2 ladder is the TRUNK is conv (CLMConvMoE blocks) not a GQA transformer — exactly the
    OE1 axis."""
    opt = torch.optim.AdamW(model.parameters(), lr=lr, betas=(0.9, 0.95), weight_decay=0.1)

    def lr_at(step):
        if step < warmup:
            return lr * (step + 1) / warmup
        prog = (step - warmup) / max(1, steps - warmup)
        return lr * (0.1 + 0.9 * 0.5 * (1.0 + math.cos(math.pi * prog)))

    train_curve, val_curve = [], []
    model.train()
    t0 = time.time()
    for step in range(steps):
        for pg in opt.param_groups:
            pg["lr"] = lr_at(step)
        x, y_next = get_batch(train_data, block, bs, device)
        y_prev = torch.roll(x, shifts=1, dims=1)
        logits_a, logits_g, _, _, aux = model(x)
        loss_a = F.cross_entropy(logits_a.reshape(-1, V), y_next.reshape(-1))
        loss_g = F.cross_entropy(logits_g.reshape(-1, V), y_prev.reshape(-1))
        loss = loss_a + 0.5 * loss_g
        if aux is not None:
            loss = loss + 0.01 * aux
        opt.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        opt.step()
        if step % max(1, steps // 40) == 0 or step == steps - 1:
            train_curve.append({"step": step, "ce_a": float(loss_a.item()), "ce_g": float(loss_g.item())})
            print(f"  step {step:6d}/{steps}  ce_a(next)={loss_a.item():.4f}  ce_g(prev)={loss_g.item():.4f}"
                  f"  lr={lr_at(step):.2e}  {(time.time()-t0):.1f}s", flush=True)
        if step % val_every == 0 or step == steps - 1:
            vce = eval_val_ce(model, val_data, block, bs, device)
            val_curve.append({"step": step, "val_ce": vce})
            print(f"    [val] step {step:6d}  val_ce(head_a, multi-batch)={vce:.4f}  "
                  f"(uniform={UNIFORM_CE:.4f}, below_uniform={vce < UNIFORM_CE})", flush=True)
            model.train()
    final_val = eval_val_ce(model, val_data, block, bs, device, n_batches=80)
    return train_curve, val_curve, final_val, time.time() - t0


# ───────────────────── the conv-native closure eval (mirror OH1/OΩ1 exactly) ─────────────────────

def closure_eval(model, held, block, device, label, do_gen=True, max_pos=12000):
    """Identical to omega_trained_leakfree.closure_eval, on the CONV model's OWN A/G heads.
    Reports the FULL gate-form sweep + the OΩ1 coupling-vs-replacement control.

    PRE-REGISTERED falsifier: conv-native closure HOLDS iff min_learned <= a_only AND < base."""
    gate_seq = held[:len(held) // 2]
    test_seq = held[len(held) // 2:]
    gate_feats, gate_tgt = extract_feats(model, gate_seq, block, device, max_pos=max_pos)
    test_feats, test_tgt = extract_feats(model, test_seq, block, device, max_pos=max_pos)
    test_feats_shuf, _ = extract_feats(model, test_seq, block, device, max_pos=max_pos, shuffle_ctx=True)

    # ── FULL-AG joint gate (over A AND G) — the multi-wire form, fit on the gate split ──
    g_full = fit_gate(gate_feats, gate_tgt, steps=GATE_STEPS, l2=GATE_L2)
    # ── MIN-gate (gB·base + gA·A, drop G) — the OH1 honest closure form ──
    base_g, A_g, G_g = gate_feats
    g_min = fit_gate((base_g, A_g, np.zeros_like(G_g)), gate_tgt, steps=GATE_STEPS, l2=GATE_L2)
    g_min[2] = 0.0
    print(f"full_AG gate  g* = [gB={g_full[0]:.4f}, gA={g_full[1]:.4f}, gG={g_full[2]:.4f}]", flush=True)
    print(f"min_learned   g* = [gB={g_min[0]:.4f}, gA={g_min[1]:.4f}, gG={g_min[2]:.4f}]", flush=True)

    # ── held-out TEST CE for every gate form ──
    ce_base = ce_of(np.array([1.0, 0.0, 0.0]), test_feats, test_tgt)
    ce_fixed = ce_of(np.array([1.0, ALPHA, -ALPHA]), test_feats, test_tgt)
    ce_aonly = ce_of(np.array([1.0, ALPHA, 0.0]), test_feats, test_tgt)
    ce_full = ce_of(g_full, test_feats, test_tgt)
    ce_min = ce_of(g_min, test_feats, test_tgt)
    print(f"--- held-out TEST CE (CONV-native dual head, leak-free, nats/byte) ---", flush=True)
    print(f"  base {ce_base:.6f} | fixed_AmG {ce_fixed:.6f} | a_only {ce_aonly:.6f} | "
          f"full_AG {ce_full:.6f} | min_learned {ce_min:.6f} | uniform {UNIFORM_CE:.6f}", flush=True)

    # ── OΩ1 coupling-vs-replacement control: A-STANDALONE vs min_learned ──
    # A-standalone = softmax(A) alone (base entirely removed): gB=0, gA=1, gG=0
    ce_a_standalone = ce_of(np.array([0.0, 1.0, 0.0]), test_feats, test_tgt)
    # base-ABLATED min (gB->0, keep gA·A from the min fit)
    ce_min_baseablate = ce_of(np.array([0.0, g_min[1], 0.0]), test_feats, test_tgt)
    repl_gap = abs(ce_a_standalone - ce_min)
    replacement = bool(repl_gap < 0.05 and ce_min < ce_base)
    print(f"  [coupling-vs-replacement] A_standalone(softmax(A) alone) {ce_a_standalone:.6f} "
          f"vs min_learned {ce_min:.6f} (|Δ|={repl_gap:.4f}); base-ablated min {ce_min_baseablate:.6f}", flush=True)
    print(f"  RULING_REPLACEMENT={replacement} (A alone reproduces min_learned ⇒ A-head SUPPLANTS "
          f"the weak base, not a base+steer coupling)", flush=True)

    # ── leak-invariant structured-coupling (real A vs context-shuffled A) ──
    st = kl_structured(test_feats, test_feats_shuf, test_tgt)
    print(f"structured: A-wire gain real {st['gain_real']:.4f} vs shuf {st['gain_shuf']:.4f} "
          f"-> structured(>1.5x)={st['structured_ce']}", flush=True)

    # ── PRE-REGISTERED falsifier (on min_learned, the OH1 honest form) ──
    min_le_aonly = ce_min <= ce_aonly
    min_lt_base = ce_min < ce_base
    closure_holds = bool(min_le_aonly and min_lt_base)
    print(f"\n  >>> CONV-NATIVE CLOSURE FALSIFIER: min_learned<=a_only={min_le_aonly}  AND  "
          f"min_learned<base={min_lt_base}  -> closure_HOLDS={closure_holds}", flush=True)

    gen = None
    if do_gen:
        counts = np.full(V, SMOOTH)
        for b in test_seq:
            counts[int(b)] += 1.0
        log_base_vec = np.log(counts / counts.sum())
        prompt = bytes(test_seq[:48].tobytes())
        base_txt, gated_txt = gen_sample(model, prompt, 300, device, g_min, log_base_vec)
        # gen_sample returns decoded strings; re-encode the gated tail for byte_stats
        gated_tail = gated_txt[len(prompt.decode('utf-8', errors='replace')):]
        gstats = byte_stats(gated_tail.encode('utf-8', errors='ignore'))
        coherent = (gstats["entropy"] > 1.5 and gstats["distinct_frac"] > 0.10 and gstats["ws_frac"] < 0.80)
        print(f"\n  gen(min-gate): entropy={gstats['entropy']:.3f} distinct={gstats['distinct_frac']:.3f}"
              f" ws={gstats['ws_frac']:.3f} coherent={coherent}", flush=True)
        print(f"  [MIN-GATE] {gated_tail[:160]!r}", flush=True)
        gen = {"coherent": bool(coherent), "gated_stats": gstats,
               "gated_sample": gated_tail[:300], "base_sample": base_txt[len(prompt.decode('utf-8', errors='replace')):][:300]}

    return {
        "gate_full": {"gB": float(g_full[0]), "gA": float(g_full[1]), "gG": float(g_full[2])},
        "gate_min": {"gB": float(g_min[0]), "gA": float(g_min[1]), "gG": float(g_min[2])},
        "ce": {"base": ce_base, "fixed_AmG": ce_fixed, "a_only": ce_aonly,
               "full_AG": ce_full, "min_learned": ce_min, "uniform_floor": UNIFORM_CE},
        "coupling_vs_replacement": {"a_standalone": ce_a_standalone, "min_learned": ce_min,
                                    "base_ablated_min": ce_min_baseablate, "abs_gap": repl_gap,
                                    "RULING_REPLACEMENT": replacement},
        "structured": st,
        "closure": {"min_le_aonly": min_le_aonly, "min_lt_base": min_lt_base, "HOLDS": closure_holds},
        "gen": gen,
    }


def run_rung(d_model, n_trunk_layers, n_experts, block, bs, lr, steps, device,
             train_data, val_data, held, label, ckpt_path=None):
    print(f"\n{'='*22} OE1 CONV-NATIVE DUAL-HEAD RUNG {label} (d_model={d_model}, L={n_trunk_layers}, E={n_experts}) {'='*22}", flush=True)
    model = ConvDualHead(vocab_size=V, d_model=d_model, n_trunk_layers=n_trunk_layers,
                         n_experts=n_experts, block_size=block, variant="A").to(device)
    nparam = model.count_params()
    print(f"ConvDualHead params: {nparam:,} ({nparam/1e6:.2f}M)  [conv trunk + native A/G dual head]", flush=True)

    # leak self-test (untrained): flip ONLY last byte -> head_a at earlier positions must NOT move
    model.eval()
    with torch.no_grad():
        xt = torch.randint(0, V, (1, min(32, block)), device=device)
        la1, _, _, _, _ = model(xt)
        xt2 = xt.clone(); xt2[0, -1] = (int(xt[0, -1]) + 7) % V
        la2, _, _, _, _ = model(xt2)
        leak = float((la1[0, :-1] - la2[0, :-1]).abs().max().item())
    print(f"leak self-test (flip last byte -> max change in head_a earlier pos): {leak:.3e}  (want ~0)", flush=True)
    leak_free = leak < 1e-4

    train_curve, val_curve, final_val, train_wall = train_to_competence(
        model, train_data, val_data, steps, block, bs, lr, device)
    first_ce = train_curve[0]["ce_a"]; final_ce = train_curve[-1]["ce_a"]
    below_uniform = final_val < UNIFORM_CE
    competent = final_val <= 4.0
    print(f"\n(b) trained leak-free conv: ce_a {first_ce:.4f} -> {final_ce:.4f}  FINAL val_ce={final_val:.4f}  "
          f"below_uniform={below_uniform}  competent(<=4.0)={competent}  wall={train_wall:.1f}s", flush=True)

    ckpt_sha = None
    if ckpt_path:
        cfg = {"vocab_size": V, "d_model": d_model, "n_trunk_layers": n_trunk_layers,
               "n_experts": n_experts, "block_size": block, "variant": "A", "arch": "ConvDualHead"}
        torch.save({"model": model.state_dict(), "config": cfg}, ckpt_path)
        ckpt_sha = hashlib.sha256(open(ckpt_path, "rb").read()).hexdigest()
        print(f"ckpt saved: {ckpt_path}  sha256={ckpt_sha[:16]}", flush=True)

    cl = closure_eval(model, held, block, device, label)

    return {
        "label": label, "arch": "ConvDualHead (CLMConvMoE conv trunk + native A/G dual head)",
        "leak_self_test": leak, "leak_free": bool(leak_free),
        "params": int(nparam), "d_model": d_model, "n_trunk_layers": n_trunk_layers, "n_experts": n_experts,
        "steps": steps,
        "train": {"first_ce_a": first_ce, "final_ce_a": final_ce, "final_val_ce": final_val,
                  "below_uniform": bool(below_uniform), "competent": bool(competent),
                  "wall_s": train_wall, "train_curve": train_curve, "val_curve": val_curve},
        "ckpt_sha256": ckpt_sha,
        **cl,
        "config": {"vocab_size": V, "d_model": d_model, "n_trunk_layers": n_trunk_layers,
                   "n_experts": n_experts, "block_size": block, "variant": "A"},
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--steps", type=int, default=12000)
    ap.add_argument("--block", type=int, default=256)
    ap.add_argument("--bs", type=int, default=32)
    ap.add_argument("--lr", type=float, default=6e-4)
    ap.add_argument("--corpus_mb", type=int, default=400)
    ap.add_argument("--d_model", type=int, default=384)
    ap.add_argument("--n_trunk_layers", type=int, default=6)
    ap.add_argument("--n_experts", type=int, default=8)
    ap.add_argument("--device", default="auto", help="auto|cpu|mps|cuda")
    ap.add_argument("--out", default="omega_conv_native_results.json")
    ap.add_argument("--ckpt", default="omega_conv_native.pt")
    ap.add_argument("--corpus_path", default=None)
    args = ap.parse_args()

    if args.device == "auto":
        if torch.cuda.is_available():
            device = "cuda"
        elif torch.backends.mps.is_available():
            device = "mps"
        else:
            device = "cpu"
    else:
        device = args.device
    print(f"=== OMEGA OE1 — CONV-NATIVE dual-head closure (torch research-proxy of CLMConvMoE) ===", flush=True)
    print(f"device={device}  torch={torch.__version__}", flush=True)
    if device == "cuda":
        torch.backends.cuda.matmul.allow_tf32 = True
        torch.backends.cudnn.allow_tf32 = True
        print(f"gpu={torch.cuda.get_device_name(0)}", flush=True)

    corpus_path = args.corpus_path or os.path.join(HERE, "omega_corpus_big.bin")
    target = args.corpus_mb * 1_000_000
    corpus, prov = fetch_corpus(target, corpus_path)
    sha = hashlib.sha256(corpus.tobytes()).hexdigest()
    n = len(corpus)
    print(f"corpus: {n}B ({n/1e6:.1f}MB)  prov={prov}  sha256={sha[:16]}", flush=True)

    cut = int(n * 0.9)
    train_data = corpus[:cut]
    held = corpus[cut:]
    val_data = held[:len(held) // 2]

    t_start = time.time()
    r = run_rung(args.d_model, args.n_trunk_layers, args.n_experts, args.block,
                 args.bs, args.lr, args.steps, device, train_data, val_data, held,
                 f"conv-d{args.d_model}-L{args.n_trunk_layers}-E{args.n_experts}", ckpt_path=args.ckpt)

    results = {
        "lane": "Lane-G/Lane-P", "substrate": "conv-torch (research-proxy of CLMConvMoE)",
        "device": device, "torch": torch.__version__,
        "honest_scope": "TORCH RESEARCH-PROXY of the conv architecture (faithful CLMConvMoE blocks "
                        "+ native A/G dual head), NOT the production flame+forge .clm trainer "
                        "(a_scale_honest_scope · a_train_flame_forge)",
        "corpus_bytes": int(n), "corpus_mb": n / 1e6, "corpus_prov": prov, "corpus_sha256": sha,
        "question": "does a CONV trunk with a NATIVE A/G dual head close the OMEGA min-gate, or is "
                    "the closure CDV2-(transformer)-specific?  (OΩ6 #1805 deferred)",
        "falsifier": "conv-native closure HOLDS iff min_learned <= a_only AND min_learned < base, "
                     "on the conv model's OWN A-head, competent leak-free substrate",
        "ckpt": {"path": args.ckpt, "sha256": r.get("ckpt_sha256")},
        "rung": r,
        "total_wall_s": time.time() - t_start,
    }
    json.dump(results, open(args.out, "w"), indent=2, ensure_ascii=False)

    print("\n=== OE1 CONV-NATIVE SUMMARY ===", flush=True)
    print(f"  leak self-test: {r['leak_self_test']:.3e} (leak_free={r['leak_free']})", flush=True)
    print(f"  final val_ce: {r['train']['final_val_ce']:.4f}  below_uniform={r['train']['below_uniform']}"
          f"  competent(<=4.0)={r['train']['competent']}", flush=True)
    ce = r["ce"]
    print(f"  CE: base {ce['base']:.4f} | a_only {ce['a_only']:.4f} | fixed_AmG {ce['fixed_AmG']:.4f}"
          f" | full_AG {ce['full_AG']:.4f} | min_learned {ce['min_learned']:.4f} | uniform {ce['uniform_floor']:.4f}", flush=True)
    cr = r["coupling_vs_replacement"]
    print(f"  coupling-vs-replacement: A_standalone {cr['a_standalone']:.4f} vs min {cr['min_learned']:.4f}"
          f" (|Δ|{cr['abs_gap']:.4f}) -> RULING_REPLACEMENT={cr['RULING_REPLACEMENT']}", flush=True)
    print(f"  structured: real {r['structured']['gain_real']:.4f} vs shuf {r['structured']['gain_shuf']:.4f}"
          f" -> {r['structured']['structured_ce']}", flush=True)
    print(f"  >>> CONV-NATIVE CLOSURE HOLDS = {r['closure']['HOLDS']}"
          f"  (min<=a_only={r['closure']['min_le_aonly']}, min<base={r['closure']['min_lt_base']})", flush=True)
    print(f"results -> {args.out}", flush=True)


if __name__ == "__main__":
    main()
