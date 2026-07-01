#!/usr/bin/env python3
"""h1464_torch_golden.py — torch GOLDEN for the engine-native argmax==torch parity check.
Loads a ByteGPT-303M .pt (g6_common loader), forwards a fixed 15-byte prompt, prints the
last-position next-byte ARGMAX + first-16 logits. Diffed byte-exact vs core/bytegpt_decode
forward (verify303m-style). a_engine_native_learning: engine argmax MUST == torch argmax."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import g6_common as C
import torch
PT = sys.argv[1]  # e.g. ckpt/h1464_pairing.pt
m, cfg = C.load_model(PT, "cpu")
m.eval()
prompt = b"The quick brown"   # same 15 bytes as core/verify303m_mount_parity.hexa
ids = torch.tensor([[b for b in prompt]], dtype=torch.long)
with torch.no_grad():
    out = m(ids)
    logits = out[0] if isinstance(out, (tuple, list)) else out
    last = logits[0, -1, :].float()
am = int(last.argmax().item())
print("TORCH_ARGMAX", am)
print("TORCH_MAXVAL", float(last[am].item()))
top5 = torch.topk(last, 5).indices.tolist()
print("TORCH_TOP5", top5)
print("TORCH_FIRST16", " ".join(f"{float(last[j].item()):.4f}" for j in range(16)))
