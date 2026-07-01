#!/usr/bin/env python3
"""H_1640 aux-gradient smoke: prove each NEW objective's aux term flows gradient to the
TRUNK. Trick: objfn returns total = ce + λ·aux (tensors). `aux_only = total - ce` is a
differentiable tensor whose gradient is exactly λ·d(aux)/dθ (the ce parts cancel). We
backward ONLY aux_only and confirm the trunk param grad-norm is > 0 = the aux really
sculpts the trunk (not a dead/stubbed aux). Runs on CPU, tiny model."""
import os, sys
os.environ["CUDA_VISIBLE_DEVICES"] = ""
import torch, torch.nn as nn, torch.nn.functional as F
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)
import trainer as TR                     # sets up sys.path for model/, cli/, tool/
from model import CLMConfig, CLMConvMoE

def pen_of(model, x):
    h = model.embed(x).transpose(1, 2); h = model.embed_conv(h)
    for layer in model.trunk:
        h = layer(h)
    hm, _ = model.moe(h); hm = model.norm_out(hm)
    return hm

def check(objname):
    torch.manual_seed(0)
    d, L, V, T, B = 48, 2, 256, 64, 4
    cfg = CLMConfig(n_experts=3, n_trunk_layers=L, d_model=d, kernel_size=3,
                    variant="AB", dilation_base=2, max_dilation=512)
    model = CLMConvMoE(cfg)
    objfn = TR.OBJECTIVE_BUILDERS[objname](d, V, "cpu")
    needs_pen = objname in TR.OBJ_NEEDS_PENULTIMATE
    x = torch.randint(0, V, (B, T)); y = torch.randint(0, V, (B, T))
    gen = torch.Generator().manual_seed(1)
    out = model(x, y)
    pen = pen_of(model, x) if needs_pen else None
    total, auxd = objfn(out["logits"], y, V, gen, penultimate=pen)
    ce = F.cross_entropy(out["logits"].transpose(1, 2).reshape(-1, V), y.reshape(-1))
    aux_only = total - ce                            # == λ·aux (differentiable)
    model.zero_grad()
    if isinstance(objfn, nn.Module):
        objfn.zero_grad()
    aux_only.backward()
    tg = sum((p.grad.norm().item() ** 2)
             for p in model.trunk.parameters() if p.grad is not None) ** 0.5
    finite = bool(torch.isfinite(total).item() and torch.isfinite(aux_only).item())
    aux_nonzero = abs(float(aux_only)) > 1e-9
    print(f"[{objname:17s}] total={float(total):.5f} aux_only(λ·aux)={float(aux_only):.6f} "
          f"aux={auxd} trunk_grad_norm={tg:.6e} finite={finite} "
          f"aux_nonzero={aux_nonzero} FLOWS_TO_TRUNK={tg > 0}")
    assert finite, "non-finite loss"
    assert aux_nonzero, "aux term is exactly zero (dead aux)"
    assert tg > 0, "aux gradient does NOT reach trunk (dead aux)"
    return True

if __name__ == "__main__":
    for name in ("predictive_info", "constructive_bind", "composed_nce"):
        check(name)
    print("ALL AUX-GRADIENT SMOKES PASSED")
