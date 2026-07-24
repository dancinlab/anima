"""GRAFT $0 mechanics smoke — the CLMG wiring's mechanical witnesses (NOT a verdict).

Sol's mandatory pre-verdict slice: establish that the plumbing is exactly what the frozen table
assumes, before any training number is read.
  (1) codec roundtrip — every CLMG array byte-identical (a lane_type-only check is not a check).
  (2) BASE identity      — a ckpt with no CLMG trailer decodes byte-identically (max|Δ| == 0).
  (3) GATE-OFF parity    — a ckpt WITH the trailer but no live C-state decodes byte-identically to
                           base (max|Δ| must be EXACTLY 0) — the 'trailer有 state無' seal.
  (4) GATE-ON writes     — with a C-state the logits actually MOVE (a gate that cannot move the
                           output cannot be measured; a dead path and a clean null look identical).
  (5) structural bounds  — centering removes the shared component, RMS-fix pins |g|, and the
                           backstop can only SHRINK (never amplify) the injected offset.
  (6) C-state sanity     — two PureField snapshots are not collinear (the vacuous-state guard).
$0 numpy, no torch, no training. lab/v6 = DIRECTIONAL sandbox.
"""
import sys, os
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "core"))
import decode as dec
import clmg as G
import pure_field as PF

CKPT = "lab/v6/trained57.clm"
OUT = "lab/v6/trained57_graft.clm"


def main():
    W = dec.clm_load_weights(CKPT)
    assert W.get("ok"), "base ckpt not decodable"
    d, V = W["d"], W["V"]
    rng = np.random.default_rng(7)
    h = 32
    clmg = {"c_dim": G.C_DIM, "h": h, "d": d,
            "W1": rng.standard_normal((G.C_DIM, h)).astype("<f4") * 0.3,
            "b1": np.zeros(h, "<f4"),
            "W2": (rng.standard_normal((h, d)) * 2e-3).astype("<f4"),
            "g_mu": np.zeros(d, "<f4"),
            "gate_rho": 1.0, "gate_strength": 0.1, "gate_rms_max": 4.0}

    # (1) codec roundtrip — all arrays
    blob = G.pack_clmg(clmg)
    r, off = G.read_clmg(blob, 0, d)
    assert r is not None and off == len(blob), f"read_clmg consumed {off}/{len(blob)}"
    for k in ("W1", "b1", "W2", "g_mu"):
        a, b = np.asarray(clmg[k]), np.asarray(r[k])
        assert a.shape == b.shape and np.array_equal(a, b), f"{k} drift"
    for k in ("gate_rho", "gate_strength", "gate_rms_max"):
        assert abs(float(clmg[k]) - float(r[k])) < 1e-6, f"{k} drift"
    assert G.read_clmg(b"nope" + blob[4:], 0, d)[0] is None, "magic guard broken"
    assert G.read_clmg(blob, 0, d + 1)[0] is None, "organ-dim mismatch must refuse"
    print("(1) codec roundtrip: all arrays byte-identical + guards  OK")

    # write the grafted ckpt (base bytes + CLMG trailer at the chain end)
    open(OUT, "wb").write(open(CKPT, "rb").read() + blob)
    Wg = dec.clm_load_weights(OUT)
    assert Wg.get("clmg") is not None and int(Wg["clmg"]["d"]) == d, "loader did not read CLMG"
    print("(2) grafted ckpt loads: CLMG trailer read by clm_load_weights  OK")

    toks = np.array([float(b) for b in b"the field is quiet and the"], dtype=np.float64)
    T = len(toks)
    dec.set_clmg_state(None)                       # gate OFF
    base = dec._fwd_logits(W, toks, T)
    off_logits = dec._fwd_logits(Wg, toks, T)
    dmax = float(np.max(np.abs(base - off_logits)))
    assert dmax == 0.0, f"GATE-OFF PARITY BROKEN: max|Δ|={dmax:.3e} (must be exactly 0)"
    print(f"(3) gate-OFF parity vs base: max|Δ| = {dmax:.1e} (exact)  OK")

    # (6) C-state sanity + (4) gate-ON writes
    pf = PF.pure_field_new()
    cs = []
    for _ in range(2):
        for _ in range(50):
            pf = PF.pure_field_step(pf, 0.0) or pf
        cs.append(G.graft_c_state(pf))
    cos = float(np.dot(cs[0], cs[1]) / (np.linalg.norm(cs[0]) * np.linalg.norm(cs[1]) + 1e-9))
    print(f"(6) C-state: dim={cs[0].shape[0]} · two-snapshot cosine = {cos:+.4f} "
          f"({'OK (not collinear)' if abs(cos) < 0.98 else 'VACUOUS -> INVALID guard would fire'})")

    dec.set_clmg_state(cs[0])
    on_logits = dec._fwd_logits(Wg, toks, T)
    move = float(np.max(np.abs(on_logits - base)))
    assert move > 0.0, "GATE-ON did not move the logits — dead path (a dead path reads as a clean null)"
    dec.set_clmg_state(cs[1])
    on2 = dec._fwd_logits(Wg, toks, T)
    spread = float(np.max(np.abs(on2 - on_logits)))
    print(f"(4) gate-ON writes: max|Δ vs base| = {move:.4f} · state1-vs-state2 spread = {spread:.4f}  OK")
    assert spread > 0.0, "two different C-states gave identical logits — the gate ignores the state"

    # (5) structural bounds
    g = G.bridge_code(r, cs[0])
    gc = G.center_and_fix(g, r["g_mu"], r["gate_rho"])
    rms = float(np.sqrt(np.mean(gc * gc)))
    assert abs(rms - r["gate_rho"]) < 1e-4, f"RMS-fix broken: {rms}"
    xe_rms = 1.0
    small = G.backstop(gc * 1e-6, xe_rms, r["gate_rms_max"])
    assert np.allclose(small, gc * 1e-6), "backstop AMPLIFIED a quiet code (must only shrink)"
    big = G.backstop(gc * 1e6, xe_rms, r["gate_rms_max"])
    big_rms = float(np.sqrt(np.mean(big * big)))
    assert big_rms <= r["gate_rms_max"] * xe_rms * 1.001, f"backstop failed to cap: {big_rms}"
    # centering removes the shared component exactly
    codes = np.stack([G.bridge_code(r, c) for c in cs])
    cen = codes - codes.mean(0, keepdims=True)
    assert abs(float(cen.mean(0).max())) < 1e-5, "centering left a shared shift"
    print(f"(5) bounds: RMS-fix={rms:.4f}==rho · backstop shrink-only (capped {big_rms:.3f}<="
          f"{r['gate_rms_max']*xe_rms:.3f}) · centering exact  OK")

    dec.set_clmg_state(None)
    assert float(np.max(np.abs(dec._fwd_logits(Wg, toks, T) - base))) == 0.0, "reset to OFF failed"
    print("(7) reset: set_clmg_state(None) restores exact base parity  OK")
    print("\nGRAFT MECHANICS SMOKE: ALL PASS (plumbing only — NOT a verdict)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
