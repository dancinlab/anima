#!/usr/bin/env python3
"""morphatom_reinit.py — MORPH-ATOM re-fire ckpt surgery (Fable option 3).

The S1 fire returned INVALID because warm-starting a utf-8-byte-trained 303M on the re-encoded 2-byte
codec alphabet gives an ACTIVELY WRONG input-embedding prior (worse than random init) — gradient must
first destroy utf-8 structure before building codec structure, so 8k CPT bought discrimination (F1 via
memorization) but zero compositional geometry (C3 leak-ceiling dead). Fix: reinit ONLY the alphabet-facing
tensors (embed.weight + readout.weight/bias) to fresh normal init, keep the trunk/MoE warm. This keeps M
and C1 on the same trunk lineage (arm comparability) while giving the embedding a clean slate for the codec
alphabet. Untied embed (nn.Embedding) + readout (nn.Conv1d(d,V,1)) per core/model.py:272,284.

Runs on the pod (torch installed). Usage: morphatom_reinit.py <in.pt> <out.pt> [--reinit-embed-conv]
"""
import sys
import math
import torch

IN = sys.argv[1]
OUT = sys.argv[2]
ALSO_CONV = "--reinit-embed-conv" in sys.argv     # fallback knob if G-a1 stalls

sd = torch.load(IN, map_location="cpu")
# torch ckpt may be {"model": state_dict, ...} or a bare state_dict
state = sd.get("model", sd) if isinstance(sd, dict) and "model" in sd else sd

def norm_(t, std):
    with torch.no_grad():
        t.normal_(0.0, std)

reinit = []
for k in list(state.keys()):
    kk = k.split("model.")[-1]
    if kk == "embed.weight":
        d = state[k].shape[1]
        norm_(state[k], d ** -0.5)             # match nn.Embedding-scale init used elsewhere (d**-0.5)
        reinit.append((k, tuple(state[k].shape)))
    elif kk == "readout.weight":
        norm_(state[k], (state[k].shape[1]) ** -0.5)   # Conv1d(d,V,1): fan_in=d
        reinit.append((k, tuple(state[k].shape)))
    elif kk == "readout.bias":
        with torch.no_grad():
            state[k].zero_()
        reinit.append((k, tuple(state[k].shape)))
    elif ALSO_CONV and kk.startswith("embed_conv."):
        if state[k].dim() >= 2:
            norm_(state[k], (state[k].shape[1]) ** -0.5)
        else:
            with torch.no_grad():
                state[k].zero_()
        reinit.append((k, tuple(state[k].shape)))

torch.save(sd, OUT)
print("reinit tensors:")
for k, s in reinit:
    print(" ", k, s)
assert any("embed.weight" in k for k, _ in reinit), "embed.weight not found — check state_dict keys"
assert any("readout.weight" in k for k, _ in reinit), "readout.weight not found"
print("MORPHATOM_REINIT_DONE -> %s" % OUT)
