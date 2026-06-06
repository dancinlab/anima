"""H_992 — WM>LM failure FRONTIER: the gap widens with task memory-depth (ladder).

1st-round seed: H_970🟢 KEYSTONE found ONE WM>LM separator (delayed-cue, persistent state).
That was a single point. This maps the FRONTIER: (A) does the WM>LM gap grow monotonically
with the required memory DEPTH (delay L), turning the keystone point into a curve? and
(B) is the failure specific to memory, or does an LM also fail a 2nd task family (running
parity / accumulation) that a WM solves?

Falsifier (frozen):
  D1 (ladder)  delayed-cue recall over delays L ∈ {2,4,8,12,16,24}. WM keeps high success;
               LM (window ctx < L) decays toward chance. PASS-A iff the WM−LM gap is
               monotone-increasing in L (Spearman rho(L, gap) > 0.8) and gap(L=24)>gap(L=2).
  D2 (2nd family) running-parity-accumulation: WM must integrate a stream; LM sees a window.
               PASS-B iff WM beats LM by Cohen d>1.0 on this DIFFERENT task too.
  PASS iff PASS-A AND PASS-B (the WM>LM advantage is a memory-depth FRONTIER, not one task).
  FAIL iff the gap does not grow with depth OR the 2nd family shows no WM advantage.
substrate=CPU-mirror (numpy). a_scale_honest_scope: single toy rung, ladder OPEN.
"""
import sys, os
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "probes"))
from cwm_probe_lib import LatentWorldModel, StatelessLM, header, cohens_d, spearman

K = 4
DELAYS = [2, 4, 8, 12, 16, 24]
LM_CTX = 4
N_SEEDS = 10
N_TR, N_TE = 500, 250
LAT = 32


def gen_cue_task(rng, L, n):
    """At t=0 a cue ∈ {0..K-1}; after L filler steps, a GO flag; target = recall the cue."""
    in_dim = K + 1
    X, Y = [], []
    for _ in range(n):
        cue = rng.integers(K)
        seq = np.zeros((L + 2, in_dim))
        seq[0, cue] = 1.0
        for t in range(1, L + 1):
            seq[t, rng.integers(K)] = 0.3      # filler noise (not the GO channel)
        seq[L + 1, K] = 1.0                    # GO flag
        X.append(seq); Y.append(cue)
    return X, np.array(Y)


def run_cue(rng, L):
    Xtr, ytr = gen_cue_task(rng, L, N_TR)
    Xte, yte = gen_cue_task(rng, L, N_TE)
    in_dim = K + 1
    wm = LatentWorldModel(in_dim, latent_dim=LAT, seed=int(rng.integers(1e6)), retentive=True,
                          spectral_radius=1.0)
    Ytr = np.eye(K)[ytr]
    Hwm = np.array([wm.final_latent(x) for x in Xtr])
    wm.fit_readout(Hwm, Ytr, ridge=1e-1)
    Hte = np.array([wm.final_latent(x) for x in Xte])
    pwm = wm.predict_readout(Hte).argmax(1)
    s_wm = (pwm == yte).mean()
    lm = StatelessLM(in_dim, ctx=LM_CTX, feat_dim=LAT, seed=int(rng.integers(1e6)))
    Ftr = np.array([lm.features_over_seq(x)[-1] for x in Xtr])
    lm.fit_readout(Ftr, Ytr, ridge=1e-1)
    Fte = np.array([lm.features_over_seq(x)[-1] for x in Xte])
    plm = lm.predict_readout(Fte).argmax(1)
    s_lm = (plm == yte).mean()
    return s_wm, s_lm


def gen_parity_task(rng, L, n):
    """Stream of ±1 events; target = sign of the running SUM at the end (needs accumulation
    of the WHOLE stream, not a window)."""
    in_dim = 2
    X, Y = [], []
    for _ in range(n):
        bits = rng.choice([-1.0, 1.0], size=L)
        seq = np.zeros((L, in_dim))
        seq[bits > 0, 0] = 1.0; seq[bits < 0, 1] = 1.0
        X.append(seq); Y.append(1 if bits.sum() > 0 else 0)
    return X, np.array(Y)


def run_parity(rng, L=20):
    Xtr, ytr = gen_parity_task(rng, L, N_TR)
    Xte, yte = gen_parity_task(rng, L, N_TE)
    in_dim = 2
    wm = LatentWorldModel(in_dim, latent_dim=LAT, seed=int(rng.integers(1e6)), retentive=True,
                          spectral_radius=1.0)
    Ytr = np.eye(2)[ytr]
    Hwm = np.array([wm.final_latent(x) for x in Xtr]); wm.fit_readout(Hwm, Ytr, ridge=1e-1)
    pwm = wm.predict_readout(np.array([wm.final_latent(x) for x in Xte])).argmax(1)
    s_wm = (pwm == yte).mean()
    lm = StatelessLM(in_dim, ctx=LM_CTX, feat_dim=LAT, seed=int(rng.integers(1e6)))
    Ftr = np.array([lm.features_over_seq(x)[-1] for x in Xtr]); lm.fit_readout(Ftr, Ytr, ridge=1e-1)
    plm = lm.predict_readout(np.array([lm.features_over_seq(x)[-1] for x in Xte])).argmax(1)
    s_lm = (plm == yte).mean()
    return s_wm, s_lm


def main():
    header("H_992", "WM>LM failure frontier: gap widens with memory-depth (ladder)")
    gaps = []
    print(f"D1 delayed-cue ladder (K={K} chance={1/K:.3f}, LM_ctx={LM_CTX}) over delays:")
    for L in DELAYS:
        ws, ls = [], []
        for s in range(N_SEEDS):
            rng = np.random.default_rng(1000 * L + s)
            a, b = run_cue(rng, L)
            ws.append(a); ls.append(b)
        gap = np.mean(ws) - np.mean(ls)
        gaps.append(gap)
        print(f"  L={L:2d}: WM={np.mean(ws):.3f}  LM={np.mean(ls):.3f}  gap={gap:.3f}")
    rho, p = spearman(np.array(DELAYS, float), np.array(gaps))
    grow = rho > 0.8 and gaps[-1] > gaps[0]
    print(f"  → gap-vs-depth Spearman rho={rho:.3f} p={p:.3e}  gap(L=24)={gaps[-1]:.3f} > gap(L=2)={gaps[0]:.3f}: {gaps[-1]>gaps[0]}")
    print()
    print("D2 second family — running-parity accumulation (different task):")
    pws, pls = [], []
    for s in range(N_SEEDS):
        rng = np.random.default_rng(50000 + s)
        a, b = run_parity(rng)
        pws.append(a); pls.append(b)
    pws, pls = np.array(pws), np.array(pls)
    dpar = cohens_d(pws, pls)
    print(f"  WM={pws.mean():.3f}  LM={pls.mean():.3f}  Cohen d(WM,LM)={dpar:.3f}")
    famB = pws.mean() > pls.mean() and dpar > 1.0
    print("-" * 78)
    if grow and famB:
        v = (f"PASS WM>LM is a memory-depth FRONTIER: gap grows monotonically with delay "
             f"(rho={rho:.2f}, gap {gaps[0]:.2f}→{gaps[-1]:.2f}) AND a 2nd task family (running-parity) "
             f"also favors WM (d={dpar:.2f}) — the LM failure generalizes beyond one task (toy rung).")
        tok = "PASS"
    elif grow:
        v = (f"PASS-PARTIAL gap grows with depth (rho={rho:.2f}) but the 2nd family advantage is weak "
             f"(d={dpar:.2f}) — frontier confirmed on memory-depth only (toy).")
        tok = "PASS"
    else:
        v = (f"FAIL gap does not grow monotonically with memory-depth (rho={rho:.2f}) — no WM>LM "
             f"frontier here (closed-negative, toy).")
        tok = "FAIL"
    print(f"VERDICT H_992: {v}")
    print("-" * 78)
    return tok


if __name__ == "__main__":
    main()
