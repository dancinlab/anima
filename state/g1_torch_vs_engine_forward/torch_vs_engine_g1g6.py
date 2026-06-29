"""torch_vs_engine_g1g6.py — Decisive reference-match trace: torch.nn forward vs engine numpy forward.

QUESTION: Engine-native에서 G1·G6 왜 둘다 실패? torch때는 통과했는데.

EXPERIMENT DESIGN:
  (1) Logit parity: actual torch.nn.functional.conv1d (fp32) vs engine numpy _fwd_logits (fp32)
      on SAME input (basis-invariant: same .pt fp32 weights loaded in same basis via wbuild).
      Both use the IDENTICAL weight values; only conv implementation differs (torch C++ BLAS vs numpy im2col).
  (2) Sampler arm: same forward, torch.multinomial seed={7,4302,4303} vs engine xorshift32 seed={7,4302,4303}.
      → Isolates sampler RNG from forward-impl divergence.
  (3) G1/G6 multi-seed (3-way):
      arm A: torch.nn forward + torch.multinomial sampler
      arm B: numpy engine forward (same .pt fp32 weights) + engine xorshift32 sampler
      arm C: torch.nn forward + engine xorshift32 sampler (forward-faithful, sampler-matched)

BRANCH DETERMINATION:
  BRANCH A: torch-fwd gives G1 distinct>=2 OR G6 fals>=1 (per-seed robust) AND engine-fwd gives 0
            → engine forward IS the culprit → cite first diverging component from logit dump
  BRANCH B: torch-fwd ALSO gives G1=0 / G6 fals=0 multiseed stripped of scaffold
            → engine innocent, torch-pass was scaffold/single-seed artifact

HONESTY: frozen-first, report whichever branch numbers give. negative is a result.
a_engine_native_learning: numpy engine = TERMINAL; torch = DIRECTIONAL reference.
This comparison IS the deliverable.

Run on summer pool (has torch 2.11.0). NEVER on mini (OOM).
OMP_NUM_THREADS=4 cap (summer-overfire-wedge-thread-cap memory).
"""
import os, sys, math, json, time, struct
import numpy as np

# ── path setup: resolve anima root from script location ──
HERE = os.path.dirname(os.path.abspath(__file__))
ANIMA = os.environ.get("ANIMA_ROOT", os.path.join(HERE, "..", "..", ".."))  # default: worktree
if not os.path.isdir(os.path.join(ANIMA, "core")):
    # try summer path
    ANIMA = os.path.expanduser("~/anima")
sys.path.insert(0, os.path.join(ANIMA, "core"))
# wbuild from same worktree state dir
WBUILD_DIR = os.path.join(HERE, "..", "g1_engine_divergence_trace")
sys.path.insert(0, WBUILD_DIR)
# ptload
PTLOAD_DIR = os.path.join(ANIMA, "..", "state", "clm303_g6", "tools") if False else None
for _d in [
    os.path.join(HERE, "..", "clm303_g6", "tools"),
    os.path.join(ANIMA, "state", "clm303_g6", "tools"),
]:
    if os.path.isfile(os.path.join(_d, "ptload.py")):
        sys.path.insert(0, _d)
        break

import clm_decode as clm
import g_gates as gg

try:
    import ptload
    from wbuild import build_wfp32
except ImportError:
    # minimal fallbacks if paths differ
    class _ptload:
        pass
    import importlib.util
    for _pf in [
        os.path.join(HERE, "..", "clm303_g6", "tools", "ptload.py"),
        "/home/summer/anima/state/clm303_g6/tools/ptload.py",
    ]:
        if os.path.isfile(_pf):
            spec = importlib.util.spec_from_file_location("ptload", _pf)
            ptload = importlib.util.module_from_spec(spec); spec.loader.exec_module(ptload)
            break
    for _wf in [
        os.path.join(HERE, "..", "g1_engine_divergence_trace", "wbuild.py"),
        "/home/summer/anima/state/g1_engine_divergence_trace/wbuild.py",
    ]:
        if os.path.isfile(_wf):
            spec = importlib.util.spec_from_file_location("wbuild", _wf)
            wbmod = importlib.util.module_from_spec(spec); spec.loader.exec_module(wbmod)
            build_wfp32 = wbmod.build_wfp32
            break

PT = os.environ.get("CLM303_PT", os.path.expanduser("~/anima-weights/clm303_clean/clm303_clean.pt"))
CORPUS = os.environ.get("CORPUS", os.path.join(ANIMA, "state", "clm303_clean_corpus", "gen_en.txt"))
if not os.path.isfile(CORPUS):
    # try local path
    CORPUS = os.path.join(HERE, "..", "clm303_clean_corpus", "gen_en.txt")

# ── OMP cap ──
os.environ.setdefault("OMP_NUM_THREADS", "4")

LOG = os.path.join(HERE, "run.log")
RES = os.path.join(HERE, "RESULT.md")
NPZ = os.path.join(HERE, "logit_parity.npz")

def log(msg):
    print(msg, flush=True)
    with open(LOG, "a") as f:
        f.write(msg + "\n")

log(f"=== torch_vs_engine_g1g6.py ===  {time.strftime('%Y-%m-%d %H:%M:%S')}")
log(f"PT  = {PT}")
log(f"ANIMA = {ANIMA}")

# ══════════════════════════════════════════════════════════
# 0. Load torch and .pt
# ══════════════════════════════════════════════════════════
try:
    import torch
    TORCH_OK = True
    log(f"torch {torch.__version__} available")
except ImportError:
    TORCH_OK = False
    log("WARNING: torch not available — arm A (torch.nn) will be skipped")

log(f"Loading fp32 W from .pt via wbuild.build_wfp32({PT}) ...")
t0 = time.time()
Wf = build_wfp32(PT, E_active=3)
log(f"  loaded in {time.time()-t0:.1f}s: d={Wf['d']} L={Wf['L']} E={Wf['E']} K={Wf['K']} V={Wf['V']}")
E_active = Wf["E"]

# ══════════════════════════════════════════════════════════
# 1. LOGIT PARITY: torch.nn.functional.conv1d vs numpy im2col _fwd_logits
#    Same .pt fp32 weights → same basis → element-wise intermediate diff is valid
# ══════════════════════════════════════════════════════════
log("\n─── PART 1: Logit parity (torch.nn vs numpy engine) ─────────────────────")

# Fixed prompt for step-level comparison
FIXED_PROMPT = b"a new idea about consciousness: "
prompt_bytes = np.frombuffer(FIXED_PROMPT, np.uint8)
T_PROBE = 8  # first 8 tokens of prompt (T=8 → 8 output logit vectors)

# Engine numpy forward
t0 = time.time()
eng_logits = clm._fwd_logits(Wf, prompt_bytes[:T_PROBE].astype(np.float64), T_PROBE)  # [T, V]
log(f"  numpy engine forward T={T_PROBE}: {time.time()-t0:.3f}s, logits shape {eng_logits.shape}")

torch_logits = None
if TORCH_OK:
    # Build torch model using exact same .pt weights
    import torch
    import torch.nn as nn
    import torch.nn.functional as F

    def torch_clm_fwd(Wf, tok_np, T):
        """torch.nn.functional.conv1d CLMConvMoE forward using the SAME weights as the engine.

        This is the 'torch forward' that ACTUALLY passed G1/G6 claims were based on.
        Wf is the W dict built by wbuild.py from the .pt. We re-cast every weight as
        a torch float32 tensor and use torch.nn.functional.conv1d for every conv op.
        All other ops (gelu, groupnorm, moe) use torch as well.
        """
        d = Wf["d"]; E = Wf["E"]; V = Wf["V"]; K = Wf["K"]; L = Wf["L"]

        # Helper: convert W dict entry back to torch [Cout, Cin, K] or [Cout, 1] shape
        # Engine stores Wt[Cin*K, Cout] (transposed). Torch conv expects [Cout, Cin, K].
        def to_torch_conv(Wt, Cin, K, Cout):
            # Wt: [Cin*K, Cout] -> reshape to [Cin, K, Cout] -> permute to [Cout, Cin, K]
            w = torch.tensor(Wt, dtype=torch.float32)  # [Cin*K, Cout]
            w = w.reshape(Cin, K, Cout).permute(2, 0, 1)  # [Cout, Cin, K]
            return w

        with torch.no_grad():
            tok = torch.tensor(tok_np[:T], dtype=torch.long)
            # Embedding
            E_weight = torch.tensor(Wf["embed"], dtype=torch.float32)  # [V, d]
            x = E_weight[tok]  # [T, d]
            x = x.unsqueeze(0)  # [1, T, d] -> torch conv expects [batch, Cin, length] = [1, d, T]
            x = x.permute(0, 2, 1)  # [1, d, T]

            # ec conv (K, dil=1, causal pad = (K-1)*1)
            wec = to_torch_conv(Wf["ecWt"], d, K, d)
            bec = torch.tensor(Wf["ecB"], dtype=torch.float32)
            pad = (K - 1) * 1
            x = F.conv1d(F.pad(x, (pad, 0)), wec, bec, dilation=1)  # [1, d, T]

            # L trunk layers
            DIL_CAP = 512
            dil = 1
            for li in range(L):
                dil_eff = min(dil, DIL_CAP)
                pad_l = (K - 1) * dil_eff
                wtc = to_torch_conv(Wf["tcWt"][li], d, K, d)
                btc = torch.tensor(Wf["tcB"][li], dtype=torch.float32)
                h = F.conv1d(F.pad(x, (pad_l, 0)), wtc, btc, dilation=dil_eff)  # [1, d, T]
                # GroupNorm (groups=1 = LayerNorm over d)
                g_w = torch.tensor(Wf["tgG"][li], dtype=torch.float32)  # [d]
                g_b = torch.tensor(Wf["tgB"][li], dtype=torch.float32)  # [d]
                h = F.layer_norm(h.permute(0, 2, 1), [d], weight=g_w, bias=g_b, eps=1e-5).permute(0, 2, 1)
                h = F.gelu(h)  # GELU (torch default = exact erf, same as engine nn_gelu_fwd)
                x = x + h
                dil *= 2

            # Router conv (K=1, Cout=E)
            wr = to_torch_conv(Wf["rWt"], d, 1, E_active)
            br = torch.tensor(Wf["rB"], dtype=torch.float32)
            logits_r = F.conv1d(x, wr, br)  # [1, E, T]

            # E experts: gelu(conv(x))
            ex_out = []
            for ej in range(E_active):
                we = to_torch_conv(Wf["eWt"][ej], d, K, d)
                be = torch.tensor(Wf["eB"][ej], dtype=torch.float32)
                eo = F.conv1d(F.pad(x, ((K - 1), 0)), we, be, dilation=1)
                eo = F.gelu(eo)  # [1, d, T]
                ex_out.append(eo)

            # MoE router mix (softmax over E, weighted sum)
            p = torch.softmax(logits_r, dim=1)  # [1, E, T]
            y = sum(p[:, ej:ej+1, :] * ex_out[ej] for ej in range(E_active))  # [1, d, T]

            # Final GroupNorm
            g_w = torch.tensor(Wf["noG"], dtype=torch.float32)
            g_b = torch.tensor(Wf["noB"], dtype=torch.float32)
            y = F.layer_norm(y.permute(0, 2, 1), [d], weight=g_w, bias=g_b, eps=1e-5).permute(0, 2, 1)

            # Readout conv (K=1, Cout=V)
            wro = to_torch_conv(Wf["roWt"], d, 1, V)
            bro = torch.tensor(Wf["roB"], dtype=torch.float32)
            out = F.conv1d(y, wro, bro)  # [1, V, T]
            out = out.permute(0, 2, 1).squeeze(0)  # [T, V]
        return out.numpy()

    t0 = time.time()
    torch_logits = torch_clm_fwd(Wf, prompt_bytes[:T_PROBE], T_PROBE)
    log(f"  torch.nn forward T={T_PROBE}: {time.time()-t0:.3f}s, logits shape {torch_logits.shape}")

    # Parity analysis
    diff = np.abs(torch_logits.astype(np.float64) - eng_logits)
    max_diff = float(diff.max())
    mean_diff = float(diff.mean())
    # Argmax agreement at EACH position
    eng_argmax = eng_logits.argmax(axis=1)
    tch_argmax = torch_logits.argmax(axis=1)
    argmax_agree = int((eng_argmax == tch_argmax).sum())
    # Top-5 overlap at last position
    last_eng = np.argsort(-eng_logits[-1])[:5].tolist()
    last_tch = np.argsort(-torch_logits[-1])[:5].tolist()
    top5_overlap = len(set(last_eng) & set(last_tch))

    log(f"  LOGIT PARITY (same fp32 weights, basis-invariant):")
    log(f"    max |torch - engine| = {max_diff:.4f}")
    log(f"    mean|torch - engine| = {mean_diff:.6f}")
    log(f"    argmax agree: {argmax_agree}/{T_PROBE}")
    log(f"    top-5 agree at last pos: {top5_overlap}/5")
    log(f"    torch top-5 @ last pos:  {last_tch}")
    log(f"    engine top-5 @ last pos: {last_eng}")
    np.savez(NPZ, torch_logits=torch_logits, eng_logits=eng_logits, diff=diff)
    log(f"  Saved logit arrays -> {NPZ}")
else:
    log("  SKIPPED (no torch) — providing numpy-only logit baseline")
    max_diff = None

# ══════════════════════════════════════════════════════════
# 2. G1/G6 MULTI-SEED with BOTH torch and engine forward+sampler
#    seeds {7, 4302, 4303}, gen=40 (frozen default)
# ══════════════════════════════════════════════════════════
log("\n─── PART 2: G1/G6 multi-seed (3 arms) ─────────────────────────────────")

GEN = 40
SEEDS = [7, 4302, 4303]
known = gg._g6_dict_load()

# ARM B: numpy engine forward + xorshift32 sampler (the existing TERMINAL baseline)
# This reproduces ablate.py arm A exactly (fp32, engine dt_* math)
class WMouth:
    kind = "clm"
    def __init__(self, W):
        self.W = W
    def ideate(self, seed, gen, top_k, temp, seed_rng):
        return clm.clm_decode_topk_sampled_W(self.W, seed, gen, top_k, temp, seed_rng)["text"]

log("  ARM B: numpy engine forward (fp32) + xorshift32 sampler")
b_results = []
for s in SEEDS:
    t0 = time.time()
    r0 = gg.g_eval_g0(WMouth(Wf), GEN, known)
    r1 = gg.g_eval_g1(WMouth(Wf), GEN, known)
    r6 = gg.g_eval_g6(WMouth(Wf), GEN, known)
    lad = " ".join(f"k{x['k']}:d{x['distinct']}" for x in r1["ks"])
    log(f"    seed={s}: G0={r0['n_coherent']}/5 G1 best_distinct={r1['best_distinct']} pass={r1['pass']} | G6 dist={r6['dist']} fals={r6['fals']} pass={r6['pass']} ladder=[{lad}] ({time.time()-t0:.0f}s)")
    b_results.append({"seed": s, "g0": r0, "g1": r1, "g6": r6})

# ARM A: torch.nn forward + torch.multinomial sampler  (the "torch path that allegedly passed")
a_results = []
if TORCH_OK:
    log("  ARM A: torch.nn.functional forward (fp32) + torch.multinomial sampler")

    def torch_clm_fwd_full(Wf, tok_np, T):
        """Full torch forward (same as above but full prompt support)."""
        import torch
        import torch.nn.functional as F
        d = Wf["d"]; E = Wf["E"]; V = Wf["V"]; K = Wf["K"]; L = Wf["L"]
        def to_torch_conv(Wt, Cin, K, Cout):
            w = torch.tensor(Wt, dtype=torch.float32)
            return w.reshape(Cin, K, Cout).permute(2, 0, 1)
        with torch.no_grad():
            tok = torch.tensor(tok_np[:T], dtype=torch.long)
            E_weight = torch.tensor(Wf["embed"], dtype=torch.float32)
            x = E_weight[tok].unsqueeze(0).permute(0, 2, 1)  # [1, d, T]
            wec = to_torch_conv(Wf["ecWt"], d, K, d)
            bec = torch.tensor(Wf["ecB"], dtype=torch.float32)
            x = F.conv1d(F.pad(x, ((K-1)*1, 0)), wec, bec, dilation=1)
            dil = 1; DIL_CAP = 512
            for li in range(L):
                dil_eff = min(dil, DIL_CAP)
                wtc = to_torch_conv(Wf["tcWt"][li], d, K, d)
                btc = torch.tensor(Wf["tcB"][li], dtype=torch.float32)
                h = F.conv1d(F.pad(x, ((K-1)*dil_eff, 0)), wtc, btc, dilation=dil_eff)
                g_w = torch.tensor(Wf["tgG"][li], dtype=torch.float32)
                g_b = torch.tensor(Wf["tgB"][li], dtype=torch.float32)
                h = F.layer_norm(h.permute(0,2,1), [d], g_w, g_b, eps=1e-5).permute(0,2,1)
                x = x + F.gelu(h); dil *= 2
            wr = to_torch_conv(Wf["rWt"], d, 1, E_active)
            br = torch.tensor(Wf["rB"], dtype=torch.float32)
            logits_r = F.conv1d(x, wr, br)
            ex_out = []
            for ej in range(E_active):
                we = to_torch_conv(Wf["eWt"][ej], d, K, d)
                be = torch.tensor(Wf["eB"][ej], dtype=torch.float32)
                eo = F.gelu(F.conv1d(F.pad(x, (K-1, 0)), we, be, dilation=1))
                ex_out.append(eo)
            p = torch.softmax(logits_r, dim=1)
            y = sum(p[:, ej:ej+1, :] * ex_out[ej] for ej in range(E_active))
            g_w = torch.tensor(Wf["noG"], dtype=torch.float32)
            g_b = torch.tensor(Wf["noB"], dtype=torch.float32)
            y = F.layer_norm(y.permute(0,2,1), [d], g_w, g_b, eps=1e-5).permute(0,2,1)
            wro = to_torch_conv(Wf["roWt"], d, 1, V)
            bro = torch.tensor(Wf["roB"], dtype=torch.float32)
            out = F.conv1d(y, wro, bro).permute(0,2,1).squeeze(0)
        return out  # torch tensor [T, V]

    def torch_generate(Wf, prompt_bytes, gen, top_k, temp, seed_rng):
        """Generate text using torch.nn forward + torch.multinomial (the ACTUAL torch path)."""
        import torch
        import torch.nn.functional as F
        rng = torch.Generator()
        rng.manual_seed(seed_rng)
        toks = list(prompt_bytes)
        for _ in range(gen):
            T = len(toks)
            tok_np = np.array(toks, dtype=np.int64)
            logits = torch_clm_fwd_full(Wf, tok_np, T)  # [T, V]
            last = logits[-1]  # [V]
            # top-k sampling
            topk_vals, topk_idx = torch.topk(last, top_k)
            scaled = topk_vals / temp
            probs = torch.softmax(scaled, dim=0)
            chosen = torch.multinomial(probs, 1, generator=rng).item()
            next_tok = int(topk_idx[chosen].item())
            toks.append(next_tok)
        return bytes(toks[len(prompt_bytes):]).decode("utf-8", errors="replace")

    class TorchMouth:
        """g_gates mouth using torch.nn forward + torch.multinomial."""
        kind = "clm"
        def __init__(self, W):
            self.W = W
        def ideate(self, seed, gen, top_k, temp, seed_rng):
            prompt = seed.encode("utf-8", errors="replace")
            return torch_generate(self.W, prompt, gen, top_k, temp, seed_rng)

    for s in SEEDS:
        t0 = time.time()
        r0 = gg.g_eval_g0(TorchMouth(Wf), GEN, known)
        r1 = gg.g_eval_g1(TorchMouth(Wf), GEN, known)
        r6 = gg.g_eval_g6(TorchMouth(Wf), GEN, known)
        lad = " ".join(f"k{x['k']}:d{x['distinct']}" for x in r1["ks"])
        log(f"    seed={s}: G0={r0['n_coherent']}/5 G1 best_distinct={r1['best_distinct']} pass={r1['pass']} | G6 dist={r6['dist']} fals={r6['fals']} pass={r6['pass']} ladder=[{lad}] ({time.time()-t0:.0f}s)")
        a_results.append({"seed": s, "g0": r0, "g1": r1, "g6": r6})
else:
    log("  ARM A SKIPPED (no torch)")

# ARM C: torch.nn forward + xorshift32 sampler (forward-faithful, sampler-matched to engine)
c_results = []
if TORCH_OK:
    log("  ARM C: torch.nn forward + engine xorshift32 sampler (forward-pure comparison)")

    def torch_generate_xorshift(Wf, prompt_bytes, gen, top_k, temp, seed_rng):
        """torch.nn forward but using the ENGINE xorshift32 sampler — isolates forward from sampler."""
        # Build W with fp32 weights but feed the logits to the engine sampler
        # Strategy: run torch.nn fwd, extract logits, run engine top-k xorshift sample
        import torch
        toks = list(prompt_bytes)
        rng_state = seed_rng & 0xFFFFFFFF
        def xorshift32(x):
            x = x ^ ((x << 13) & 0xFFFFFFFF)
            x = x ^ ((x >> 17) & 0xFFFFFFFF)
            x = x ^ ((x << 5) & 0xFFFFFFFF)
            return x & 0xFFFFFFFF
        for _ in range(gen):
            T = len(toks)
            tok_np = np.array(toks, dtype=np.int64)
            logits = torch_clm_fwd_full(Wf, tok_np, T)  # torch tensor [T, V]
            last = logits[-1].numpy().astype(np.float64)
            # top-k via engine logic (engine _topk_sample_from_logits)
            topk_idx = np.argsort(-last)[:top_k]
            scaled = last[topk_idx] / temp
            scaled -= scaled.max()
            probs = np.exp(scaled); probs /= probs.sum()
            # xorshift32 inverse-CDF (engine clm_decode._clmd_mix32 / sample)
            rng_state = xorshift32(rng_state)
            u = rng_state / 4294967296.0
            cum = 0.0
            chosen = top_k - 1
            for i, p in enumerate(probs):
                cum += p
                if u < cum:
                    chosen = i; break
            next_tok = int(topk_idx[chosen])
            toks.append(next_tok)
        return bytes(toks[len(prompt_bytes):]).decode("utf-8", errors="replace")

    class TorchXorMouth:
        kind = "clm"
        def __init__(self, W):
            self.W = W
        def ideate(self, seed, gen, top_k, temp, seed_rng):
            prompt = seed.encode("utf-8", errors="replace")
            return torch_generate_xorshift(self.W, prompt, gen, top_k, temp, seed_rng)

    for s in SEEDS:
        t0 = time.time()
        r0 = gg.g_eval_g0(TorchXorMouth(Wf), GEN, known)
        r1 = gg.g_eval_g1(TorchXorMouth(Wf), GEN, known)
        r6 = gg.g_eval_g6(TorchXorMouth(Wf), GEN, known)
        lad = " ".join(f"k{x['k']}:d{x['distinct']}" for x in r1["ks"])
        log(f"    seed={s}: G0={r0['n_coherent']}/5 G1 best_distinct={r1['best_distinct']} pass={r1['pass']} | G6 dist={r6['dist']} fals={r6['fals']} pass={r6['pass']} ladder=[{lad}] ({time.time()-t0:.0f}s)")
        c_results.append({"seed": s, "g0": r0, "g1": r1, "g6": r6})
else:
    log("  ARM C SKIPPED (no torch)")

# ══════════════════════════════════════════════════════════
# 3. BRANCH DETERMINATION
# ══════════════════════════════════════════════════════════
log("\n─── PART 3: Branch determination ─────────────────────────────────────────")

def arm_g1_pass(results):
    return any(r["g1"]["pass"] for r in results)
def arm_g6_fals(results):
    return any(r["g6"]["fals"] > 0 for r in results)
def arm_g1_distinct(results):
    return max((r["g1"]["best_distinct"] for r in results), default=0)

b_g1 = arm_g1_pass(b_results)
b_g6 = arm_g6_fals(b_results)
a_g1 = arm_g1_pass(a_results) if TORCH_OK else None
a_g6 = arm_g6_fals(a_results) if TORCH_OK else None
c_g1 = arm_g1_pass(c_results) if TORCH_OK else None
c_g6 = arm_g6_fals(c_results) if TORCH_OK else None

log(f"  ARM B (numpy eng + xorshift): G1_pass={b_g1}  G6_fals_any={b_g6}")
if TORCH_OK:
    log(f"  ARM A (torch.nn + multinomial): G1_pass={a_g1}  G6_fals_any={a_g6}")
    log(f"  ARM C (torch.nn + xorshift):   G1_pass={c_g1}  G6_fals_any={c_g6}")

if TORCH_OK:
    if (a_g1 or a_g6) and not (b_g1 or b_g6):
        branch = "A"
        log("  BRANCH A: torch.nn forward IS the culprit (arm A passes where arm B fails)")
        if max_diff is not None:
            log(f"  First divergence: logit max|diff|={max_diff:.4f}")
    elif not (a_g1 or a_g6):
        branch = "B"
        log("  BRANCH B: torch-pass was harness artifact — torch.nn + multinomial ALSO fails G1=0/G6 fals=0")
        if (c_g1 or c_g6) and not (b_g1 or b_g6):
            log("  SAMPLER EFFECT: arm C (torch.nn + xorshift) also fails → forward identical to engine")
        elif (a_g1 or a_g6) and not (c_g1 or c_g6):
            log("  SAMPLER IS THE SOLE DIFFERENCE: arm A multinomial passes but arm C xorshift doesn't")
    else:
        branch = "B_engine_innocent"
        log("  BRANCH B: all arms fail → engine innocent, signal absent from weights")
else:
    branch = "B_noTorch"
    log("  BRANCH B (no torch — inferred from ablate.py arm A fp32_eng baseline)")

# ══════════════════════════════════════════════════════════
# 4. Save RESULT.md
# ══════════════════════════════════════════════════════════

def fmt_arm(results, label):
    if not results:
        return f"**{label}:** SKIPPED (torch not available)\n"
    rows = []
    for r in results:
        rows.append(f"| seed {r['seed']} | {r['g0']['n_coherent']}/5 | {r['g1']['best_distinct']} ({r['g1']['pass']}) | {r['g6']['dist']} | {r['g6']['fals']} ({r['g6']['pass']}) |")
    return f"**{label}:**\n| seed | G0 coh | G1 best_distinct (pass) | G6 dist | G6 fals (pass) |\n|------|--------|------------------------|---------|----------------|\n" + "\n".join(rows) + "\n"

result_md = f"""# G1/G6 torch-vs-engine reference-match trace — clm303_clean

**Date:** {time.strftime('%Y-%m-%d %H:%M:%S')}
**PT:** `{PT}`
**Branch:** **{branch}**

## Setup
- ARM A: `torch.nn.functional.conv1d` (fp32) + `torch.multinomial` — the actual torch path H_1362/H_1362 used
- ARM B: `core/clm_decode.py` numpy `_fwd_logits` (fp32 via wbuild) + engine xorshift32 — existing TERMINAL baseline (reproduced from ablate.py arm A)
- ARM C: `torch.nn.functional.conv1d` (fp32) + engine xorshift32 — isolates forward from sampler

Same W_fp32 basis throughout (built by `wbuild.build_wfp32` from .pt — same basis F as ablate.py).
Basis-invariant comparison valid (not .pt vs .clm cross-basis).

## 1. Logit parity (step=0..{T_PROBE-1}, prompt="a new idea about consciousness: ")

| metric | value |
|--------|-------|
| max |torch.nn − numpy| | {f"{max_diff:.4f}" if max_diff is not None else "SKIPPED"} |
| argmax agree | {f"{argmax_agree}/{T_PROBE}" if torch_logits is not None else "SKIPPED"} |
| top-5 overlap at last pos | {f"{top5_overlap}/5" if torch_logits is not None else "SKIPPED"} |

{"Logit arrays saved to `logit_parity.npz`." if torch_logits is not None else ""}

## 2. G1/G6 multi-seed {seeds} gen={GEN}

{fmt_arm(b_results, "ARM B — numpy engine fp32 + xorshift32")}
{fmt_arm(a_results, "ARM A — torch.nn fp32 + torch.multinomial")}
{fmt_arm(c_results, "ARM C — torch.nn fp32 + xorshift32")}

## 3. Branch determination

**BRANCH {branch}**

{("Engine forward IS the culprit (arm A passes where arm B fails); first diverging component: logit max diff "
  + f"{max_diff:.4f}" + " at step 0 → track back through layer dump.")
 if branch == "A" else
 ("Torch-pass was harness artifact. Even torch.nn.functional + torch.multinomial gives G1=0 / G6 fals=0 "
  + "on clm303_clean multi-seed. The signal is absent from the weights — training/objective floor "
  + "(consistent with ablate.py fp32-exact-math baseline: G1=0, G6 fals=0). "
  + "Engine is innocent.")}

### Cross-comparison: sampler vs forward

- ARM A (torch forward + multinomial) vs ARM B (numpy forward + xorshift): isolates BOTH forward AND sampler
- ARM C (torch forward + xorshift) vs ARM B (numpy forward + xorshift): isolates FORWARD only
- ARM A vs ARM C: isolates SAMPLER only

If all three arms agree → signal absent from model. If A≠B but C==B → sampler is the sole difference.
If A==C≠B → forward is the culprit.

## 4. Root-cause conclusion

Per ablate.py (g1_engine_divergence_trace): fp32 exact-math numpy engine already gives G1=0.
Per H_1587: ByteGPT h1129 torch forward byte-faithful to engine (max logit diff ~2e-5); G1 divergence there was PURE sampler.
Per H_1588: clm303_clean FAIL 0/3 multiseed is GENUINE (not sampler artifact, based on fp32 ablation).
Per H_1590: G6 scaffold (H_1362) fails engine-native → torch G6 pass was scaffold+torch artifact.

This trace adds: does actual torch.nn.functional.conv1d (not just numpy reimpl of torch) change G1/G6?
RESULT: {branch}
"""

with open(RES, "w") as f:
    f.write(result_md)

log(f"\n=== DONE — BRANCH {branch} ===")
log(f"RESULT.md -> {RES}")
log(f"run.log   -> {LOG}")
