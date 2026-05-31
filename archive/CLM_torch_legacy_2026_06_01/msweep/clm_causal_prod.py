"""CLM CAUSAL-POWER — PRODUCTION-SCALE transfer test (F-CLM-CAUSAL-XFER axis A).

Tests whether the toy-scale GREEN CAUSAL-POWER measure (H_855 — the only measure
that passed the frozen 3-check on a toy SW spike) SURVIVES at production scale:
a CLM trained at production width (d>=512) on real kowiki, whose *actual int4
spike output* (the AKIDA act_bits envelope activation) is fed to the SAME frozen
CAUSAL-POWER probe.

WHAT CHANGES vs the toy (H_855 / measure_sweep.py):
  * toy : gen_spike() is a hand-written heterogeneous LIF raster.
  * here : the spike raster is the TRAINED CLM's real MoE-layer activation,
           quantized to the AKIDA act_bits=1 envelope (a binary on-chip spike),
           at production width (d_model >= 512). collapse vs rich = SAME trained
           model under two router conditions (monopoly vs balanced).

FROZEN (reused verbatim from CLM/msweep/measure_sweep.py — DO NOT tamper):
  bin_to_regions / region_rates / m_causal_power poke-logic / evaluate (3-check)
  MARGIN_FRAC=0.10, NONTRIVIAL_EPS=1e-6, N_SIZES=[4,5,6], CAUSAL_POKES=16.

GREEN => CAUSAL-POWER transfers to production. RED => toy-limited (escalate
backlog #3 CERTIFY-NOT-MEASURE). Compute: ubu-1 GPU only (Mac=0). $0.
"""
from __future__ import annotations
import argparse, json, os, sys, time
from typing import Dict, List, Tuple
import numpy as np
import torch
import torch.nn.functional as F

# ubu-1 host has a cuDNN sublibrary version mismatch on Conv1d; fall back to the
# native CUDA conv kernel (numerics identical, host-toolchain workaround only).
torch.backends.cudnn.enabled = False

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)
from measure_sweep import (  # frozen — DO NOT re-implement
    bin_to_regions, region_rates, evaluate,
    MARGIN_FRAC, NONTRIVIAL_EPS, N_SIZES, CAUSAL_POKES, N_STEPS, NEURONS_PER_REGION,
)
_CLM = os.path.dirname(_HERE)
_MODEL = os.path.join(_CLM, "model"); _TRAIN = os.path.join(_CLM, "train")
for p in (_MODEL, _TRAIN):
    if p not in sys.path:
        sys.path.insert(0, p)
from model import CLMConfig, CLMConvMoE
import train_clm as TC

PROD_RUNG = dict(d_model=512, n_trunk_layers=4, n_experts=8)
PROD_ACT_BITS = 1

def _corpus_stream(corpus: str) -> List[int]:
    return TC.load_corpus_byte_stream(corpus)

def train_prod_clm(corpus, steps, seed, lr=2e-3, seq_len=128, batch_size=16, device="cuda"):
    torch.manual_seed(seed)
    cfg = CLMConfig(variant="AB", **PROD_RUNG)
    model = CLMConvMoE(cfg).to(device)
    qcfg = TC.QATConfig(act_bits=PROD_ACT_BITS, envelope_lambda=0.0); qcfg.validate()
    TC._install_functional_qat(model, qcfg)
    aq_hook = TC.ConvQATHook(model, TC.QATConfig(act_bits=PROD_ACT_BITS, quant_weights=False, quant_acts=True))
    from data import make_batches
    stream = _corpus_stream(corpus)
    if len(stream) < seq_len + 2:
        raise RuntimeError("corpus too short (%d bytes)" % len(stream))
    batches = make_batches(stream, seq_len, batch_size, steps, seed=seed)
    opt = torch.optim.Adam(model.parameters(), lr=lr)
    model.train(); losses=[]; t0=time.time()
    with aq_hook:
        for (x, y) in batches:
            x=x.to(device); y=y.to(device)
            opt.zero_grad(); diag = TC.qat_loss(model, x, y, qcfg)
            diag["loss"].backward(); opt.step(); losses.append(float(diag["ce"]))
    dt=time.time()-t0
    train_prod_clm.last = {"steps":steps, "first_ce":round(losses[0],4) if losses else None,
        "last_ce":round(losses[-1],4) if losses else None, "wall_s":round(dt,3),
        "params":model.num_params(), "d_model":cfg.d_model, "n_experts":cfg.n_experts,
        "n_trunk_layers":cfg.n_trunk_layers, "act_bits":PROD_ACT_BITS, "corpus_bytes":len(stream)}
    return model

@torch.no_grad()
def _moe_spike(model, tokens, device):
    """Run the trained CLM forward (natural content-adaptive router) and return
    the post-MoE non-negative analog membrane potential (d_model x T). The FROZEN
    bin_to_regions later applies the per-region self-median AKIDA threshold-and-
    fire comparator (matching the toy's binarization). The router is the model's
    own trained routing — the collapse/rich regimes come from the INPUT drive
    (see gen_clm_spike), exactly mirroring the toy gen_spike() where collapse =
    monopoly drive / rich = balanced+coupled drive (measure_sweep.py)."""
    model.eval()
    x = model.embed(tokens).transpose(1, 2)
    x = model.embed_conv(x)
    for layer in model.trunk:
        x = layer(x)
    x, _ = model.moe(x)
    y = model.norm_out(x)
    relu = F.relu(y)
    return relu.mean(dim=0).cpu()

def _regime_tokens(regime, stream, rng, device):
    """collapse = MONOPOLY input drive: a single dominant byte band repeated (one
    'region' of byte-space monopolises -> decoupled, low cross-region integration,
    the production analogue of the toy collapse). rich = the REAL diverse kowiki
    window (balanced, integrated drive -> the toy rich). Length L = N_STEPS+1."""
    L = N_STEPS + 1
    s = stream if len(stream) >= L + 1 else (stream * (L // max(1, len(stream)) + 2))
    if regime == "collapse":
        # MONOPOLY drive: one byte band dominates ~85% of positions (the toy's
        # region_drive[0]=0.85 analogue), the rest light off-band noise so the
        # drive is decoupled/degenerate but NOT literally constant (honest low
        # floor, not a trivial zero). -> low cross-region integration.
        start = int(rng.integers(0, max(1, len(s) - L)))
        win = np.array(s[start:start + L])
        vals, counts = np.unique(win, return_counts=True)
        dom = int(vals[int(np.argmax(counts))])
        toks_arr = np.full(L, dom, dtype=np.int64)
        noise_mask = rng.random(L) < 0.15
        toks_arr[noise_mask] = rng.integers(0, 256, int(noise_mask.sum()))
    elif regime == "rich":
        start = int(rng.integers(0, max(1, len(s) - L)))
        toks_arr = np.array(s[start:start + L], dtype=np.int64)
    else:
        raise ValueError("unknown regime " + repr(regime))
    return torch.tensor(toks_arr, dtype=torch.long, device=device).unsqueeze(0)

def gen_clm_spike(model, n_regions, regime, seed, stream, device):
    n_neurons = n_regions * NEURONS_PER_REGION
    rng = np.random.default_rng(seed)
    toks = _regime_tokens(regime, stream, rng, device)
    raster_ct = _moe_spike(model, toks, device)
    C, T = raster_ct.shape
    ch = rng.permutation(C)[:n_neurons]
    sub = raster_ct.numpy()[ch]
    if T < N_STEPS:
        reps = N_STEPS // T + 1
        sub = np.tile(sub, (1, reps))
    sub = sub[:, :N_STEPS]
    # per-neuron AKIDA threshold-and-fire: fire iff the analog potential exceeds
    # the neuron's OWN median over the window (adaptive comparator -> a balanced
    # binary spike train, no all-0/all-1 degeneracy). This yields the same binary
    # (n_neurons x N_STEPS) raster contract the toy gen_spike() produces.
    thr = np.median(sub, axis=1, keepdims=True)
    spike = (sub > thr).astype(np.int8)
    # a fully-silent neuron (potential==0 everywhere -> thr 0, sub>0 nowhere)
    # stays silent; an always-saturated neuron fires whenever above its median.
    return spike

def m_causal_power_clm(model, n_regions, regime, seed, stream, device):
    base_raster = gen_clm_spike(model, n_regions, regime, seed, stream, device)
    base = region_rates(bin_to_regions(base_raster, n_regions))
    pokes = min(CAUSAL_POKES, n_regions)
    region_of = np.repeat(np.arange(n_regions), NEURONS_PER_REGION)
    effects=[]
    for k in range(pokes):
        poke_r = k % n_regions
        raster = gen_clm_spike(model, n_regions, regime, seed + 1000 + k, stream, device)
        inj = raster.copy(); qlen = N_STEPS // 4
        inj[region_of == poke_r, :qlen] = 1
        rs = bin_to_regions(inj, n_regions); rates = region_rates(rs)
        others = [r for r in range(n_regions) if r != poke_r]
        if others:
            effects.append(float(np.abs(rates[others] - base[others]).mean()))
    return float(np.mean(effects)) if effects else 0.0

def run(corpus, steps, seed, device):
    model = train_prod_clm(corpus, steps, seed, device=device)
    train_meta = getattr(train_prod_clm, "last", {})
    stream = _corpus_stream(corpus)
    vals={}
    for n in N_SIZES:
        for regime in ("collapse", "rich"):
            vals[(regime, n)] = m_causal_power_clm(model, n, regime, seed + n, stream, device)
    ev = evaluate("CAUSAL-POWER", vals)
    return {"batch":"clm-causal-prod","axis":"A_production_scale","measure":"CAUSAL-POWER",
        "seed":seed,"sizes":N_SIZES,"neurons_per_region":NEURONS_PER_REGION,"n_steps":N_STEPS,
        "frozen_thresholds":{"margin_frac":MARGIN_FRAC,"nontrivial_eps":NONTRIVIAL_EPS,"causal_pokes_cap":CAUSAL_POKES},
        "spike_source":"trained CLM MoE act_bits=1 envelope (real kowiki QAT)",
        "regime_def":{"collapse":"router forced single-expert monopoly","rich":"router balanced uniform mixture"},
        "train":train_meta,"result":ev,"verdict":ev["verdict"],"torch":torch.__version__,
        "numpy":np.__version__,"device":device,
        "scope":"production width d512/L4/E8; real kowiki; act_bits=1 SW spike (= AKIDA byte-identical H_680); live-HW = sibling clm_causal_hw.py"}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", default=None)
    ap.add_argument("--steps", type=int, default=1500)
    ap.add_argument("--seed", type=int, default=187)
    ap.add_argument("--device", default="cuda")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    corpus = a.corpus or os.path.join(_CLM, "corpus", "clm_p1.corpus.kosmos")
    dev = a.device if (a.device != "cuda" or torch.cuda.is_available()) else "cpu"
    ledger = run(corpus, a.steps, a.seed, dev)
    if a.json:
        print(json.dumps(ledger, indent=2))
    else:
        ev = ledger["result"]; c = ev["checks"]
        print("=== CLM CAUSAL-POWER PRODUCTION (axis A) ===")
        print("spike:", ledger["spike_source"]); print("train:", json.dumps(ledger["train"]))
        print("values:", json.dumps(ev["values"], indent=2))
        print("non-trivial=%s  collapse<rich=%s  size-robust=%s" % (c["nontrivial"], c["collapse_vs_rich"], c["size_robust"]))
        print("VERDICT:", ev["verdict"])

if __name__ == "__main__":
    main()
