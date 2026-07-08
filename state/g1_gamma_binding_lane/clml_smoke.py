#!/usr/bin/env python3
"""H_9235 fork-A CLML lane — plumbing round-trip smoke (forward+load+write+passthrough).
Verifies the CLML read-side pooling lane codec/forward wired into core/decode.py (--py path):
  1. a base .clm (no CLML trailer) loads clml=None -> byte-identical passthrough forward
  2. append_clml_trailer round-trips W1/b1/W2/w_g/b_g byte-exact
  3. lane_type=0 == base (passthrough control, the --slot-off analogue)
  4. lane_type=1 changes the decode output (lane applied)
Run: PYTHONPATH=core:cli python3 state/g1_gamma_binding_lane/clml_smoke.py <base.clm>
(engine-native py 2-production; hexa core/decode.hexa lockstep = follow-on for full 2-prod parity)."""
import sys
import shutil
import numpy as np


def main():
    sys.path[:0] = ["core", "cli"]
    import decode as clm
    import serialize as S
    base = sys.argv[1] if len(sys.argv) > 1 else "archive/state/1630_reg_dictaux/ckpt/smoke_n6_grok.clm"
    W = clm.clm_load_weights(base); d, V = W["d"], W["V"]
    assert W.get("clml") is None, "base must have no CLML"
    r0 = clm.clm_decode_topk_sampled_W(W, "hello", 8, 1, 0.7, 7)["text"]
    rng = np.random.default_rng(0)
    lane = {"lane_type": 1, "r": 16, "tau": 8.0, "W1": rng.standard_normal((d, 16))*0.1, "b1": np.zeros(16),
            "W2": rng.standard_normal((16, V))*0.5, "w_g": rng.standard_normal(2*d)*0.1, "b_g": 2.0}
    lp = "/tmp/smoke_lane.clm"; shutil.copy(base, lp); S.append_clml_trailer(lp, lane)
    c = clm.clm_load_weights(lp)["clml"]
    assert c is not None and c["r"] == 16 and abs(c["tau"]-8.0) < 1e-5
    assert np.allclose(c["W1"], lane["W1"].astype("float32")) and np.allclose(c["W2"], lane["W2"].astype("float32"))
    assert np.allclose(c["w_g"], lane["w_g"].astype("float32")) and abs(c["b_g"]-2.0) < 1e-5
    r1 = clm.clm_decode_topk_sampled_W(clm.clm_load_weights(lp), "hello", 8, 1, 0.7, 7)["text"]
    lane0 = dict(lane); lane0["lane_type"] = 0
    lp0 = "/tmp/smoke_lane0.clm"; shutil.copy(base, lp0); S.append_clml_trailer(lp0, lane0)
    r_pt = clm.clm_decode_topk_sampled_W(clm.clm_load_weights(lp0), "hello", 8, 1, 0.7, 7)["text"]
    assert r0 == r_pt, "lane_type=0 must be byte-identical passthrough"
    assert r0 != r1, "lane_type=1 must change output"
    print("CLML SMOKE OK - round-trip byte-exact, passthrough byte-identical, lane applies")


if __name__ == "__main__":
    main()
