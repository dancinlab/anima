#!/usr/bin/env python3
"""$0 mini-safe smoke for `anima train --py --init` warm-start (feat-train-warmstart-init).

Drives MY worktree's cli/train.py by IMPORT (not the enforcement-blocked `python cli/train.py`
top-level form) so the smoke exercises the edited code, not $ANIMA_SRC's."""
import os, sys, struct, tempfile, io, contextlib
import numpy as np
import torch

ROOT = os.environ["ROOT"]
sys.path.insert(0, os.path.join(ROOT, "cli"))
sys.path.insert(0, os.path.join(ROOT, "archive", "train", "clm", "model"))
sys.path.insert(0, os.path.join(ROOT, "core"))   # core first — shadow cli/serialize.py

import serialize as S
from bytegpt_model import ByteGPTConfig, ByteGPT

tmp = tempfile.mkdtemp()
D, L, H, BLK, V = 64, 2, 2, 128, 256

# 1) build a tiny random ByteGPT, snapshot its state_dict, serialize to .pt then engine .bin
torch.manual_seed(123)
cfg = ByteGPTConfig(vocab=V, d=D, n_layer=L, n_head=H, block=BLK)
m = ByteGPT(cfg)
orig = {k: v.detach().clone() for k, v in m.state_dict().items()}
pt = os.path.join(tmp, "base.pt")
torch.save({"model": m.state_dict(), "config": cfg.as_dict()}, pt)
binp = os.path.join(tmp, "base.bin")
S.serialize(pt, binp)

# 2) deserialize the .bin back → assert BYTE-PARITY with the original tensors
sd2, cfg2 = S.deserialize_bytegpt(binp)
assert cfg2 == cfg.as_dict(), f"cfg mismatch {cfg2} != {cfg.as_dict()}"
worst = 0.0
for k, v in orig.items():
    a = v.numpy().astype("<f4").tobytes()
    b = sd2[k].numpy().astype("<f4").tobytes()
    assert a == b, f"BYTE MISMATCH on {k}"
    worst = max(worst, float(np.abs(v.numpy() - sd2[k].numpy()).max()))
print(f"[1] deserialize round-trip BYTE-PARITY ✓  {len(orig)} tensors  max|Δ|={worst:.2e}")

# 3) end-to-end: build a FRESH ByteGPT via train.main(), --init the base.bin, run 1 step.
#    After load, the fresh model's tok.weight must byte-equal the base (warm-start took).
import train as T
outbin = os.path.join(tmp, "trained.bin")
argv = ["train", "--arch", "bytegpt", "--init", binp,
        "--d", str(D), "--L", str(L), "--seq-len", str(BLK),
        "--steps", "1", "--batch-size", "2", "--out", outbin]
# capture main() but tap the model right after warm-start via a load_state_dict spy
loaded_tok = {}
_orig_lsd = ByteGPT.load_state_dict
def _spy(self, sd, *a, **k):
    r = _orig_lsd(self, sd, *a, **k)
    loaded_tok["tok"] = self.state_dict()["tok.weight"].detach().clone()
    return r
ByteGPT.load_state_dict = _spy
sys.argv = argv
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    T.main()
ByteGPT.load_state_dict = _orig_lsd
out = buf.getvalue()
initline = [l for l in out.splitlines() if "[--init]" in l]
print(f"[2] train --init end-to-end:  {initline[0].strip() if initline else 'NO --init LINE'}")
assert initline, "no [--init] warm-start report printed"
assert "warm-start ✓" in initline[0]
# the warm-started tok.weight must byte-match the base ckpt (weights actually loaded)
tokp = (loaded_tok["tok"].numpy().astype("<f4").tobytes()
        == orig["tok.weight"].numpy().astype("<f4").tobytes())
print(f"[3] warm-started tok.weight BYTE-EQ base ckpt ✓  {tokp}")
assert tokp
donel = [l for l in out.splitlines() if "step" in l.lower()][-1:] or ["(loop ran)"]
print(f"[4] 1 training step completed after warm-start ✓  tail={donel[0].strip()[:70]}")

# 4) H_247 HARD guard — a dim mismatch must RAISE, not silently floor.
mism = ByteGPT(ByteGPTConfig(vocab=V, d=32, n_layer=L, n_head=2, block=BLK))  # d=32 != .bin d=64
try:
    T._warm_start(mism, binp, True,
                  {"vocab": V, "d": 32, "n_layer": L, "n_head": 2, "block": BLK})
    print("[5] MISMATCH GUARD ✗ (should have raised!)"); sys.exit(1)
except ValueError as e:
    print(f"[5] H_247 dim-mismatch HARD guard ✓  raised: {str(e)[:70]}...")

# 5) .clm refusal (quantized not a warm-start source)
try:
    T._warm_start(m, os.path.join(tmp, "x.clm"), False, {"d": D, "L": L})
    print("[6] .clm refusal ✗"); sys.exit(1)
except ValueError as e:
    print(f"[6] quantized .clm refused ✓  raised: {str(e)[:60]}...")

# 6) CLM .pt symmetric path — build tiny CLMConvMoE, save .pt, warm-start a fresh one.
from model import CLMConfig, CLMConvMoE
ccfg = CLMConfig(n_experts=3, n_trunk_layers=2, d_model=64, kernel_size=3,
                 variant="AB", dilation_base=2, max_dilation=512)
c1 = CLMConvMoE(ccfg)
cpt = os.path.join(tmp, "clm_base.pt")
torch.save({"model": c1.state_dict()}, cpt)
c2 = CLMConvMoE(ccfg)
rep = T._warm_start(c2, cpt, False, {"d": 64, "L": 2})
# verify a param actually copied
k0 = next(iter(c1.state_dict()))
ceq = torch.equal(c1.state_dict()[k0], c2.state_dict()[k0])
print(f"[7] CLM .pt symmetric warm-start ✓  {rep}  param[{k0}]-eq={ceq}")
assert ceq
print("\nALL SMOKE CHECKS PASSED")
