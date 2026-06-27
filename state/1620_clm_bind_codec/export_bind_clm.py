#!/usr/bin/env python3
"""Export a trained EXP-3 ARM-BIND torch ckpt (.pt state_dict) -> bind .clm (H_9023).

The census trainer (state/binding_arch_census/exp3_303m/trainer.py) ALWAYS saves a
torch .pt for the bind/bind_linear arms (--ckpt-out) but USED to skip .clm
serialization ("NOT .clm-serializable ... engine-native BLOCKED-by-construction").
With the CLMB bind-readout codec that block is GONE: this post-hoc exporter loads
the saved BindCLM state_dict and writes a bind .clm that core/clm_decode.hexa
decodes, UNBLOCKING engine-native G1/G6 measurement (anima eval / clm_forward_ce).

Runs on the trainer/pool torch host (torch.load needs torch). After export, gate
the artifact with the held-out mirror-DESCENT check:
    python3 train/clm/model/verify_clm_v2.py descent <out.clm> <heldout_corpus>

Usage:
  export_bind_clm.py --ckpt <arm.pt> --d 3784 --L 4 --E <e_active> --k 512 \
      --readout-type {1,2} --out <arm.clm>
  (readout-type 1 = Hadamard u*v [bind]; 2 = linear u+v [bind_linear])
"""
import argparse
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_REPO = _HERE
while _REPO != "/" and not os.path.exists(os.path.join(_REPO, "core", "clm_decode.py")):
    _REPO = os.path.dirname(_REPO)
sys.path.insert(0, os.path.join(_REPO, "train", "clm", "model"))
import clm_serialize_v2 as S


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ckpt", required=True, help="BindCLM torch .pt state_dict")
    ap.add_argument("--d", type=int, required=True)
    ap.add_argument("--L", type=int, required=True, help="n_trunk_layers")
    ap.add_argument("--E", type=int, required=True, help="active experts (= e_active at save)")
    ap.add_argument("--k", type=int, default=512, help="bind head bottleneck (informational)")
    ap.add_argument("--readout-type", type=int, choices=[1, 2], required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()

    import torch  # lazy — torch host only
    sd = torch.load(a.ckpt, map_location="cpu")
    if isinstance(sd, dict) and "model" in sd and hasattr(sd.get("model"), "items"):
        sd = sd["model"]
    # serialize_v3_bind accepts the BindCLM state_dict (base.<trunk> + Wa/Wb/Wo).
    S.serialize_v3_bind(sd, n_trunk_layers=a.L, n_experts=a.E,
                        readout_type=a.readout_type, out_path=a.out)
    print(f"WROTE bind .clm {os.path.getsize(a.out)} bytes -> {a.out} "
          f"(readout_type={a.readout_type} d={a.d} L={a.L} E={a.E} k={a.k})")
    print("NEXT: held-out descent gate + engine-native eval:")
    print(f"  python3 train/clm/model/verify_clm_v2.py descent {a.out} <heldout_corpus>")
    print(f"  hexa run cli/anima.hexa -- {a.out} eval   # G0-G6 single-entry")


if __name__ == "__main__":
    main()
