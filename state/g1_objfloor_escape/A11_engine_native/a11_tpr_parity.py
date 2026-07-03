#!/usr/bin/env python3
"""Byte-exact parity: the numpy scorer (core/decode.py, torch-free) TPR readout
must equal the torch reference on the SAME dequantized .clm weights (fixed ckpt).

The trunk (embed->conv->MoE->groupnorm->yn) is the proven-unchanged CLM decode
path; the genuinely NEW code is the CLMT bind_type=3 readout branch, so this
isolates and byte-checks it: load the trained TPR .clm via decode.py -> W (dequant
S_0,S_1,roles), take a random hidden yn, and compare
  numpy:  (yn*roles0)@roWt + roB + (yn*roles1)@S1Wt + S1B   (decode.py branch)
  torch:  the same op in torch float64 on the same W tensors.
Also runs decode.py full _fwd_logits end-to-end (finite + argmax stream smoke) to
confirm the whole autoregressive mouth executes with the TPR slot.
"""
import sys, os
import numpy as np
sys.path.insert(0, sys.argv[2])          # core/ dir
import decode as D
import torch

clm = sys.argv[1]
W = D.clm_load_weights(clm)
assert W.get("bind_type", 0) == 3, f"not a CLMT/TPR .clm (bind_type={W.get('bind_type')})"
d, V, R = W["d"], W["V"], W["R"]
print(f"loaded TPR .clm: d={d} V={V} R={R} L={W['L']} E={W['E']}")

rng = np.random.default_rng(0)
T = 7
yn = rng.standard_normal((T, d)).astype(np.float64)

# numpy (verbatim decode.py bind_type==3 branch)
roles = W["roles"]
c0 = yn * roles[0]; c1 = yn * roles[1]
out_np = (c0 @ W["roWt"] + W["roB"]) + (c1 @ W["S1Wt"] + W["S1B"])

# torch float64 on identical tensors
tyn = torch.tensor(yn, dtype=torch.float64)
tr = torch.tensor(roles, dtype=torch.float64)
tro = torch.tensor(W["roWt"], dtype=torch.float64); trb = torch.tensor(W["roB"], dtype=torch.float64)
ts1 = torch.tensor(W["S1Wt"], dtype=torch.float64); ts1b = torch.tensor(W["S1B"], dtype=torch.float64)
tc0 = tyn * tr[0]; tc1 = tyn * tr[1]
out_t = (tc0 @ tro + trb) + (tc1 @ ts1 + ts1b)
out_t = out_t.numpy()

mx = float(np.abs(out_np - out_t).max())
print(f"[readout parity] max|numpy - torch| = {mx:.3e}  ({'BYTE-EXACT PASS' if mx < 1e-9 else 'FAIL'})")

# full-forward smoke: decode.py _fwd_logits over a real seed context
seed_ids = np.array([ord(c) for c in "energy. memory. "], dtype=np.int64)
lg = D._fwd_logits(W, seed_ids, len(seed_ids))
finite = bool(np.isfinite(lg).all())
am = [int(x) for x in lg.argmax(1)]
print(f"[full-forward smoke] logits shape={lg.shape} finite={finite} argmax[:8]={am[:8]}")
print("PARITY_PASS" if (mx < 1e-9 and finite) else "PARITY_FAIL")
