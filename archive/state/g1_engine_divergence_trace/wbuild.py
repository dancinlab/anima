"""wbuild.py — build an fp32 weight dict in the EXACT clm_decode.py W-format
from a torch .pt (torch-free via ptload), so the SAME core/clm_decode.py forward
runs on full-precision fp32 weights vs the int4 .clm weights. Only the WEIGHT
VALUES differ — every op (conv/GN/MoE/gelu/CE/sampler) is identical.

Mapping proof (clm im2col vs torch causal conv1d, see RESULT.md):
  Wt[ci*K + k, co] = torch_w[co, ci, k]   =>   Wt = w.reshape(Cout, Cin*K).T
Experts/router clipped to E=3 (active; .pt slot-3 expert is the pruned Emax slot).
"""
import sys, os
import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "..", "clm303_g6", "tools"))
import ptload


def build_wfp32(pt_path, E_active=3):
    sd = ptload.load_pt(pt_path)
    V, d = sd["embed.weight"].shape
    K = sd["embed_conv.conv.weight"].shape[2]
    L = sum(1 for k in sd if k.startswith("trunk.") and k.endswith(".conv.conv.weight"))

    def conv_Wt(w):                       # torch [Cout,Cin,K] -> Wt[Cin*K, Cout]
        Cout = w.shape[0]
        return np.ascontiguousarray(w.reshape(Cout, -1).T).astype(np.float64)

    W = {
        "ok": True, "d": d, "E": E_active, "V": V, "K": K, "L": L,
        "embed": sd["embed.weight"].astype(np.float64),               # [V,d]
        "ecWt": conv_Wt(sd["embed_conv.conv.weight"]),
        "ecB":  sd["embed_conv.conv.bias"].astype(np.float64),
        "tcWt": [conv_Wt(sd[f"trunk.{i}.conv.conv.weight"]) for i in range(L)],
        "tcB":  [sd[f"trunk.{i}.conv.conv.bias"].astype(np.float64) for i in range(L)],
        "tgG":  [sd[f"trunk.{i}.norm.weight"].astype(np.float64) for i in range(L)],
        "tgB":  [sd[f"trunk.{i}.norm.bias"].astype(np.float64) for i in range(L)],
        "eWt":  [conv_Wt(sd[f"moe.experts.{e}.conv.conv.weight"]) for e in range(E_active)],
        "eB":   [sd[f"moe.experts.{e}.conv.conv.bias"].astype(np.float64) for e in range(E_active)],
        # router weight torch [E_full, d, 1] -> rows 0:E_active -> Wt[d, E_active]
        "rWt":  conv_Wt(sd["moe.router.weight"][:E_active]),
        "rB":   sd["moe.router.bias"][:E_active].astype(np.float64),
        "roWt": conv_Wt(sd["readout.weight"]),
        "roB":  sd["readout.bias"].astype(np.float64),
        "noG":  sd["norm_out.weight"].astype(np.float64),
        "noB":  sd["norm_out.bias"].astype(np.float64),
    }
    return W
