#!/usr/bin/env python3
"""Build a small synthetic BIND .clm (no torch) for the hexa<=>py byte-parity +
backward-compat QA of the CLMB bind-readout codec (H_9023).

Uses train/clm/model/clm_serialize_v2.serialize_v3_bind with logical-key numpy
weights (the EXP-3 BindCLM readout: Wa/Wb (k,d), Wo (V,k)). Deterministic seed so
the hexa and py engines decode the SAME bytes. Also builds the additive twin via
serialize_v3 (same trunk weights) so backward-compat is exercised on a matched pair.
"""
import os
import sys
import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
_REPO = _HERE
while _REPO != "/" and not os.path.exists(os.path.join(_REPO, "core", "clm_decode.py")):
    _REPO = os.path.dirname(_REPO)
sys.path.insert(0, os.path.join(_REPO, "train", "clm", "model"))
import clm_serialize_v2 as S


def build(d=32, L=2, E=2, k=48, V=256, K=3, seed=20260627):
    rng = np.random.default_rng(seed)
    def r(*s):
        return (rng.standard_normal(s) * 0.1).astype(np.float32)
    # shared trunk (identical for the additive twin)
    trunk = {"embed": r(V, d), "ecW": r(d, d, K), "ecB": r(d),
             "rW": r(E, d, 1), "rB": r(E), "noG": r(d), "noB": r(d)}
    for i in range(L):
        trunk[f"tc{i}W"] = r(d, d, K); trunk[f"tc{i}B"] = r(d)
        trunk[f"tg{i}G"] = r(d); trunk[f"tg{i}B"] = r(d)
    for j in range(E):
        trunk[f"e{j}W"] = r(d, d, K); trunk[f"e{j}B"] = r(d)

    # bind readout
    bind = dict(trunk)
    bind["Wa"] = r(k, d, 1); bind["WaB"] = r(k)
    bind["Wb"] = r(k, d, 1); bind["WbB"] = r(k)
    bind["Wo"] = r(V, k, 1); bind["WoB"] = r(V)

    # additive twin (same trunk + a real d->V readout)
    add = dict(trunk)
    add["roW"] = r(V, d, 1); add["roB"] = r(V)

    bind_h = os.path.join(_HERE, "synth_bind_hadamard.clm")
    bind_l = os.path.join(_HERE, "synth_bind_linear.clm")
    add_p = os.path.join(_HERE, "synth_additive.clm")
    S.serialize_v3_bind(bind, n_trunk_layers=L, n_experts=E, readout_type=1, out_path=bind_h)
    S.serialize_v3_bind(bind, n_trunk_layers=L, n_experts=E, readout_type=2, out_path=bind_l)
    S.serialize_v3(add, n_trunk_layers=L, n_experts=E, out_path=add_p)
    for p in (bind_h, bind_l, add_p):
        print(f"WROTE {p} ({os.path.getsize(p)} bytes)")


if __name__ == "__main__":
    build()
