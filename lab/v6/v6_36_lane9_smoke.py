"""V6_36 lane-9 (SRC) $0 codec+store_apply smoke. Guards the clms-py-1 recurrence 3 ways:
(1) codec roundtrip compares ALL array shapes+values (not just lane_type, which is byte 0 and
    survives a wrong header); (2) store_apply must LEAVE THE MOUTH LOGITS UNCHANGED (structural
    NLL-probe); (3) manipulation-response: value-permute and oracle must MOVE s_A (identical output
    under manipulation = a dead path, not a pass). $0 numpy, no torch, no pool.
"""
import sys, os
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "core"))
import clms

def build_lane9(d=32, d_k=16, d_s=8, n_slot=8, seed=0):
    rng = np.random.default_rng(seed)
    return {"lane_type": 9, "n_slot": n_slot, "d_k": d_k, "d_s": d_s, "key_seed": 123,
            "key_emb": rng.standard_normal((256, d_k)).astype("<f4"),
            "W_q": rng.standard_normal((d, d_k)).astype("<f4"),
            "val": rng.standard_normal((2, d_s)).astype("<f4"),
            "w_A": rng.standard_normal((d_s,)).astype("<f4"),
            "b_A": rng.standard_normal((1,)).astype("<f4"),
            "lam": np.array([1.0], "<f4")}

def main():
    d, V = 32, 256
    w = build_lane9(d=d)
    # (1) codec roundtrip — ALL arrays byte-identical
    buf = clms.pack_clms(w)
    r, off = clms.read_clms(buf, 0, d, V)
    assert r is not None, "read_clms returned None (header branch missing → lane silently dead)"
    assert off == len(buf), f"read did not consume the whole trailer ({off} vs {len(buf)})"
    for k in ("key_emb", "W_q", "val", "w_A", "b_A"):
        a, b = np.asarray(w[k]), np.asarray(r[k])
        assert a.shape == b.shape, f"{k} shape drift {a.shape} != {b.shape}"
        assert np.array_equal(a, b), f"{k} value drift"
    assert r["lane_type"] == 9 and r["n_slot"] == 8 and r["d_g"] == 0
    print("(1) codec roundtrip: all arrays byte-identical, lane_type=9, d_g=0  ✓")

    # store_apply setup
    T = 6
    rng = np.random.default_rng(1)
    yn = rng.standard_normal((T, d)).astype("<f4")
    logits = rng.standard_normal((T, V)).astype("<f4")
    ents = ["crystal", "monarch", "gravel", "festival", "harbor", "lantern", "orchard", "timber"]
    pols = [1, 0, 0, 1, 1, 0, 1, 0]
    store = {"entities": ents, "pols": pols, "target_slot": 3}
    qpos = [T - 1]

    # (2) mouth logits UNCHANGED (structural NLL-probe invariant)
    aud = []
    out = clms.store_apply(logits, yn, r, store, qpos, audit=aud)
    assert np.array_equal(out, logits), "SRC lane WROTE the mouth (out != logits) — NLL-probe not structural!"
    assert aud and "s_A" in aud[-1], "s_A not written to audit (agency read channel dead)"
    print(f"(2) mouth logits unchanged (max|Δ|={np.max(np.abs(out-logits)):.1e}); s_A={aud[-1]['s_A']:+.4f}  ✓")

    # (3a) oracle moves the read (hands target_slot) — must differ from softmax read
    aud_o = []
    clms.store_apply(logits, yn, r, store, qpos, oracle=True, audit=aud_o)
    assert aud_o[-1]["s_A"] != aud[-1]["s_A"], "oracle s_A identical to softmax s_A — addressing dead"
    # oracle s_A should equal the target slot's own value read: v=(onehot(3)-1/n)·val[pols]
    a_or = np.zeros(8); a_or[3] = 1.0; a_or -= 1.0 / 8
    v_or = a_or @ r["val"][np.asarray(pols)]
    s_expect = float(v_or @ r["w_A"] + r["b_A"][0])
    assert abs(aud_o[-1]["s_A"] - s_expect) < 1e-4, f"oracle s_A {aud_o[-1]['s_A']} != recomputed {s_expect}"
    print(f"(3a) oracle read matches hand-recompute (s_A={aud_o[-1]['s_A']:+.4f})  ✓")

    # (3b) value-permute MUST move s_A (values reshuffled, addresses fixed) — dead path would not move
    pols_perm = [pols[i] for i in (2, 3, 4, 5, 6, 7, 0, 1)]
    store_vp = {"entities": ents, "pols": pols_perm, "target_slot": 3}
    aud_vp = []
    clms.store_apply(logits, yn, r, store_vp, qpos, oracle=True, audit=aud_vp)
    assert aud_vp[-1]["s_A"] != aud_o[-1]["s_A"], "value-permute did NOT move s_A — value binding dead"
    print(f"(3b) value-permute moves s_A ({aud_o[-1]['s_A']:+.4f} → {aud_vp[-1]['s_A']:+.4f})  ✓")

    # (4) lam=0 passthrough (byte-identical) + audit empty
    aud0 = []
    out0 = clms.store_apply(logits, yn, r, store, qpos, lam_override=0.0, audit=aud0)
    assert np.array_equal(out0, logits) and not aud0, "lam=0 not a clean passthrough"
    print("(4) lam=0 passthrough byte-identical, no audit  ✓")

    # (5) regression: lanes 1-8 codec still round-trips (no collateral) — spot-check lane 2 & 6
    for lt in (2, 6):
        rng2 = np.random.default_rng(lt)
        d_s, d_g, rr = 8, 4, 12
        w2 = {"lane_type": lt, "n_slot": 8, "d_k": 16, "d_s": d_s, "d_g": d_g, "r": rr, "key_seed": 7,
              "key_emb": rng2.standard_normal((256, 16)).astype("<f4"),
              "W_q": rng2.standard_normal((d, 16)).astype("<f4"),
              "W_g": rng2.standard_normal((d, d_g)).astype("<f4"),
              "val": rng2.standard_normal((2, d_s)).astype("<f4"),
              "W_h": rng2.standard_normal((d_s + d_g, rr)).astype("<f4"),
              "b_h": rng2.standard_normal((rr,)).astype("<f4"),
              "W_out": rng2.standard_normal((rr, V)).astype("<f4"),
              "lam": np.array([0.5], "<f4")}
        b2 = clms.pack_clms(w2); r2, o2 = clms.read_clms(b2, 0, d, V)
        assert r2 is not None and o2 == len(b2) and r2["lane_type"] == lt
        for k in ("key_emb", "W_q", "W_g", "val", "W_h", "b_h", "W_out"):
            assert np.array_equal(np.asarray(w2[k]), np.asarray(r2[k])), f"lane {lt} {k} drift"
    print("(5) lanes 2 & 6 codec regression: still byte-identical  ✓")

    print("\nLANE-9 SMOKE: ALL PASS")
    return 0

if __name__ == "__main__":
    sys.exit(main())
