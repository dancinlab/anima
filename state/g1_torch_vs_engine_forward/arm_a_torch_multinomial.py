"""arm_a_torch_multinomial.py — ARM A: torch.nn (GroupNorm) + torch.multinomial G1/G6.

VERIFIED (logit_parity_check on summer):
  torch.nn.GroupNorm(1,d=3784) vs engine per-row GN: max|diff|=0.0000, argmax agree 8/8.
  (d=3784 >> T, making per-row ≈ global GN statistics empirically identical.)
  ARM C (torch.nn + xorshift32) == ARM B (engine + xorshift32): forward is identical.
  The SOLE variable: torch.multinomial vs engine xorshift32 sampler.

ARM B (engine numpy + xorshift32) from ablate.py — TERMINAL baseline:
  seed 7:    G1 best_distinct=0 FAIL | G6 dist=6 fals=0 FAIL
  seed 4302: G1 best_distinct=0 FAIL | G6 dist=6 fals=0 FAIL
  seed 4303: G1 best_distinct=0 FAIL | G6 dist=6 fals=0 FAIL

This script determines: does torch.multinomial at seeds {7,4302,4303} flip G1 or G6 fals?
"""
import os, sys, time
import numpy as np

ANIMA_CORE = os.environ.get("ANIMA_CORE", "/home/summer/anima/core")
GTRACE = os.environ.get("GTRACE", "/home/summer/g1_trace")
sys.path.insert(0, ANIMA_CORE)
sys.path.insert(0, GTRACE)
os.environ.setdefault("OMP_NUM_THREADS", "4")

HERE = os.path.dirname(os.path.abspath(__file__))
PT = os.environ.get("CLM303_PT", "/home/summer/anima-weights/clm303_clean/clm303_clean.pt")
LOG = os.path.join(HERE, "arm_a.log")


def log(msg):
    print(msg, flush=True)
    with open(LOG, "a") as f:
        f.write(msg + "\n")


log(f"=== ARM A: torch.multinomial G1/G6 on clm303_clean ===  {time.strftime('%Y-%m-%d %H:%M:%S')}")
log(f"PT = {PT}")

import torch
import torch.nn.functional as F
log(f"torch {torch.__version__}")

from wbuild import build_wfp32
import g_gates as gg

log("Loading W_fp32 ...")
t0 = time.time()
Wf = build_wfp32(PT, E_active=3)
d, L, E, K, V = Wf["d"], Wf["L"], Wf["E"], Wf["K"], Wf["V"]
log(f"  d={d} L={L} E={E} K={K} V={V} in {time.time()-t0:.1f}s")


def make_tc(Wt, Cin, K, Cout):
    """Engine Wt[Cin*K, Cout] → torch [Cout, Cin, K], float32 tensor.
    Wt[ci*K+k, co] = original_w[co, ci, k], so:
    Wt.T[co, ci*K+k] → reshape(Cout, Cin, K)[co, ci, k] = original_w[co, ci, k].
    """
    w = np.array(Wt, dtype=np.float32)  # [Cin*K, Cout]
    w = w.T.reshape(Cout, Cin, K)       # [Cout, Cin, K] — correct permutation
    return torch.tensor(w, dtype=torch.float32)


# ── pre-cache all weight tensors (avoids repeated tensor creation per step) ──
log("Pre-caching torch tensors ...")
tc = {
    "embed": torch.tensor(Wf["embed"], dtype=torch.float32),      # [V, d]
    "ecWt": make_tc(Wf["ecWt"], d, K, d),                         # [d, d, K]
    "ecB":  torch.tensor(Wf["ecB"], dtype=torch.float32),
    "tcWt": [make_tc(Wf["tcWt"][li], d, K, d) for li in range(L)],
    "tcB":  [torch.tensor(Wf["tcB"][li], dtype=torch.float32) for li in range(L)],
    "tgG":  [torch.tensor(Wf["tgG"][li], dtype=torch.float32) for li in range(L)],
    "tgB":  [torch.tensor(Wf["tgB"][li], dtype=torch.float32) for li in range(L)],
    "rWt":  make_tc(Wf["rWt"], d, 1, E),                          # [E, d, 1]
    "rB":   torch.tensor(Wf["rB"], dtype=torch.float32),
    "eWt":  [make_tc(Wf["eWt"][j], d, K, d) for j in range(E)],
    "eB":   [torch.tensor(Wf["eB"][j], dtype=torch.float32) for j in range(E)],
    "noG":  torch.tensor(Wf["noG"], dtype=torch.float32),
    "noB":  torch.tensor(Wf["noB"], dtype=torch.float32),
    "roWt": make_tc(Wf["roWt"], d, 1, V),                         # [V, d, 1]
    "roB":  torch.tensor(Wf["roB"], dtype=torch.float32),
}
log("  done")


@torch.no_grad()
def fwd(tok_list):
    """torch.nn.functional forward on tok_list (Python list of ints).
    Returns logits[-1] as a float32 tensor [V].
    VERIFIED: GroupNorm(1,d=3784) ≡ engine per-row GN (max diff=0.000).
    """
    T = len(tok_list)
    tok = torch.tensor(tok_list, dtype=torch.long)
    x = tc["embed"][tok].unsqueeze(0).permute(0, 2, 1)           # [1, d, T]
    x = F.conv1d(F.pad(x, ((K-1), 0)), tc["ecWt"], tc["ecB"])
    dil = 1
    for li in range(L):
        dil_e = min(dil, 512)
        h = F.conv1d(F.pad(x, ((K-1)*dil_e, 0)), tc["tcWt"][li], tc["tcB"][li], dilation=dil_e)
        h = F.group_norm(h, 1, weight=tc["tgG"][li], bias=tc["tgB"][li], eps=1e-5)
        x = x + F.gelu(h)
        dil *= 2
    lr = F.conv1d(x, tc["rWt"], tc["rB"])                        # [1, E, T]
    ex = [F.gelu(F.conv1d(F.pad(x, (K-1, 0)), tc["eWt"][j], tc["eB"][j]))
          for j in range(E)]
    p = torch.softmax(lr, dim=1)                                   # [1, E, T]
    y = sum(p[:, j:j+1, :] * ex[j] for j in range(E))            # [1, d, T]
    y = F.group_norm(y, 1, weight=tc["noG"], bias=tc["noB"], eps=1e-5)
    out = F.conv1d(y, tc["roWt"], tc["roB"])                      # [1, V, T]
    return out[0, :, -1]                                           # [V] last position


def generate_multinomial(prompt_bytes, gen, top_k, temp, seed_rng):
    """torch.multinomial autoregressive generation."""
    rng = torch.Generator()
    rng.manual_seed(seed_rng)
    toks = list(prompt_bytes)
    for _ in range(gen):
        last = fwd(toks)                                            # [V]
        topk_vals, topk_idx = torch.topk(last, top_k)
        probs = torch.softmax(topk_vals / temp, dim=0)
        chosen = torch.multinomial(probs, 1, generator=rng).item()
        toks.append(int(topk_idx[chosen].item()))
    return bytes(toks[len(prompt_bytes):]).decode("utf-8", errors="replace")


class TorchMultinomialMouth:
    """g_gates mouth: torch.nn.functional (GroupNorm) + torch.multinomial."""
    kind = "clm"

    def ideate(self, seed, gen, top_k, temp, seed_rng):
        return generate_multinomial(seed.encode("utf-8", errors="replace"),
                                    gen, top_k, temp, seed_rng)


GEN = 40
SEEDS = [7, 4302, 4303]
known = gg._g6_dict_load()
mouth = TorchMultinomialMouth()

log("\n─── ARM A (torch.nn GroupNorm + torch.multinomial), gen=40, seeds {7,4302,4303} ───")
results = []
for s in SEEDS:
    t0 = time.time()
    r0 = gg.g_eval_g0(mouth, GEN, known)
    r1 = gg.g_eval_g1(mouth, GEN, known)
    r6 = gg.g_eval_g6(mouth, GEN, known)
    dt = time.time() - t0
    lad = " ".join(f"k{x['k']}:d{x['distinct']}/kwr{x['kwr']:.2f}/{x['clears']}" for x in r1["ks"])
    log(f"  seed={s}: G0={r0['n_coherent']}/5  G1 max_single={r1['max_single']} best_distinct={r1['best_distinct']} pass={r1['pass']}  "
        f"G6 dist={r6['dist']} fals={r6['fals']} pass={r6['pass']}  ({dt:.0f}s)")
    log(f"    G1 ladder: {lad}")
    results.append({"seed": s, "g0": r0, "g1": r1, "g6": r6})

log("\n=== SUMMARY ===")
log(f"ARM B (baseline, engine numpy+xorshift32): G1=0 all 3 seeds, G6 fals=0 all 3 seeds")
g1_any = any(r["g1"]["pass"] for r in results)
g6_any = any(r["g6"]["fals"] > 0 for r in results)
g1_distinct = [r["g1"]["best_distinct"] for r in results]
g6_fals = [r["g6"]["fals"] for r in results]
log(f"ARM A (this, torch.nn+multinomial): G1 best_distinct={g1_distinct} pass={[r['g1']['pass'] for r in results]}")
log(f"ARM A (this, torch.nn+multinomial): G6 fals={g6_fals} pass={[r['g6']['pass'] for r in results]}")

if not g1_any and not g6_any:
    log("\n*** BRANCH B CONFIRMED ***")
    log("torch.multinomial ALSO gives G1=0 / G6 fals=0 on clm303_clean.")
    log("The 'torch passed G1/G6' claim for conv was NOT from a bare torch.nn forward pass.")
    log("Engine is innocent. Signal absent from weights = training/objective floor.")
elif g1_any:
    log(f"\n*** BRANCH A: SAMPLER IS THE CULPRIT ***")
    log("torch.multinomial flips G1 GREEN on at least one seed!")
    log("The engine xorshift32 sampler misses the RNG walk that finds concept compositions.")
    log("Root-cause fix: replace xorshift32 with torch.multinomial-equivalent in engine sampler.")
elif g6_any:
    log(f"\n*** BRANCH A-G6: sampler affects G6 fals ***")
    log("torch.multinomial finds falsifiable ideas; engine xorshift32 doesn't.")
    log("Same root-cause: sampler RNG walk difference.")

log(f"\nDone at {time.strftime('%Y-%m-%d %H:%M:%S')}")
