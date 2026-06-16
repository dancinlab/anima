"""H_1008 — ORTHOGONAL recurrent init (gradient-flow trick): does an orthogonal initialization of
the GRU's recurrent matrices crack the H_1005 T3 horizon cap at len>=36?

H_1005 root-caused the T3 cap to long-range CREDIT ASSIGNMENT through a deep BPTT chain. The
classic, single-lever fix for long-range gradient flow in RNNs is ORTHOGONAL recurrent
initialization (Saxe et al. 2014; Le et al. IRNN/np-RNN): an orthogonal recurrent matrix has
unit singular values, so gradients neither vanish nor explode as they propagate back through
many steps. THIS H tests exactly that — initialize the GRU's recurrent gate matrices (Uz, Ur,
Un) as random ORTHOGONAL (QR of a Gaussian) instead of the H_1000 baseline's 1/sqrt(H) Gaussian,
everything else (recurrence form, BPTT, Adam, curriculum, capacity, 40-ep budget, eval) VERBATIM.

This is a compute-matched, free method-shape probe (no extra labels, no extra epochs) — the
purest "does a long-range-gradient trick alone unlock the horizon?" test. If orthogonal init
cracks T3@36 -> the cap was a gradient-conditioning limit (a FREE method-shape unlock). If not ->
the cap is not (just) gradient flow.

FROZEN PASS = orthogonal-init curr-GRU SOLVES T3@36 (>> chance 1/6, d>0.8 vs LM at >=2 rungs) AND
keeps T2@40; FAIL = still ~chance (cap is not gradient conditioning). ONLY moved lever = the
recurrent-matrix init. substrate=CPU-mirror; g5 CODE-measured; toy len 36.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "CWM", "probes"))
import time
import numpy as np
from h1006_method_lib import (SLATE_RUNGS, SLATE_SEEDS, T3_BREAK, T2_SENTINEL,
                              CHANCE_T3, CHANCE_T2, make_full, gru_train_curriculum_len,
                              sep_rungs, solves, cracks_t3, keeps_t2, print_table,
                              header, verdict_line)
from h985_keystone_scaleup import N_TRAIN, N_TEST, T3_P, T2_CTX, T3_CTX
from h1000_gru_wm_t2t3 import GRUWorldModel, run_cell_lm, gru_hidden_for_rung
from h1003_t2t3_curriculum import t2_episode_len, t3_episode_len


class OrthoInitGRU(GRUWorldModel):
    """GRUWorldModel with ORTHOGONAL recurrent-matrix init (Uz, Ur, Un <- QR of Gaussian).
    EVERYTHING else (input weights, recurrence form, BPTT, Adam) is the H_1000 baseline VERBATIM —
    the ONLY change is the recurrent-init (the gradient-flow treatment under test)."""
    def __init__(self, in_dim, hidden, n_classes, seed=0):
        super().__init__(in_dim, hidden, n_classes, seed=seed)
        rng = np.random.default_rng(seed + 31337)
        for name in ("Uz", "Ur", "Un"):
            A = rng.standard_normal((hidden, hidden))
            Q, R = np.linalg.qr(A)
            Q = Q * np.sign(np.diag(R))          # make the QR deterministic (positive diag)
            setattr(self, name, Q)               # orthogonal: unit singular values


def run_ortho(maker, ncl, target, latent, seed):
    full_maker = make_full(maker, target)
    test_rng = np.random.default_rng(seed)
    for _ in range(N_TRAIN):
        full_maker(test_rng, memaug=False)
    test = [full_maker(test_rng, memaug=False) for _ in range(N_TEST)]
    tseqs = [s for s, _, _ in test]
    yte = np.array([cc for _, cc, _ in test])
    in_dim = tseqs[0].shape[1]
    hidden = gru_hidden_for_rung(latent)
    gru = OrthoInitGRU(in_dim, hidden, ncl, seed=seed + 7)
    gru_train_curriculum_len(gru, maker, target, seed)
    pred = gru.predict(tseqs)
    return float(np.mean(pred == yte))


def run_arm(maker, ncl, ctx, target, latent, seed):
    cg = run_ortho(maker, ncl, target, latent, seed)
    fm = make_full(maker, target)
    l, _ = run_cell_lm(fm, ctx, ncl, latent, seed, memaug=False)
    m, _ = run_cell_lm(fm, ctx, ncl, latent, seed, memaug=True)
    return cg, l, m


def main():
    t0 = time.time()
    header("H_1008", "Orthogonal recurrent init — crack the H_1005 T3@36 horizon cap?")
    print(f"T3 break len={T3_BREAK}, T2 sentinel len={T2_SENTINEL}. rungs={SLATE_RUNGS} "
          f"seeds={SLATE_SEEDS}, fixed 40-ep budget (== H_1005, NO extra compute/labels). ONLY "
          f"moved lever vs H_1005 = recurrent-matrix init -> ORTHOGONAL (QR of Gaussian).\n")

    rows, t3_cells, t2_cells = [], {}, {}
    for latent in SLATE_RUNGS:
        curr, lm, mem = [], [], []
        for s in range(SLATE_SEEDS):
            cg, l, m = run_arm(t3_episode_len, T3_P, T3_CTX, T3_BREAK, latent, s)
            curr.append(cg); lm.append(l); mem.append(m)
        curr, lm, mem = np.array(curr), np.array(lm), np.array(mem)
        t3_cells[latent] = dict(curr=curr, lm=lm)
        rows.append(("T3_ortho", T3_BREAK, latent, CHANCE_T3, curr, lm, mem))
        print(f"  done T3 len={T3_BREAK} rung={latent:<3} curr={curr.mean():.3f} "
              f"LM={lm.mean():.3f} mem={mem.mean():.3f} [{time.time()-t0:.0f}s]", flush=True)
    for latent in SLATE_RUNGS:
        curr, lm, mem = [], [], []
        for s in range(SLATE_SEEDS):
            cg, l, m = run_arm(t2_episode_len, 2, T2_CTX, T2_SENTINEL, latent, s)
            curr.append(cg); lm.append(l); mem.append(m)
        curr, lm, mem = np.array(curr), np.array(lm), np.array(mem)
        t2_cells[latent] = dict(curr=curr, lm=lm)
        rows.append(("T2_ortho", T2_SENTINEL, latent, CHANCE_T2, curr, lm, mem))
        print(f"  done T2 len={T2_SENTINEL} rung={latent:<3} curr={curr.mean():.3f} "
              f"LM={lm.mean():.3f} mem={mem.mean():.3f} [{time.time()-t0:.0f}s]", flush=True)

    print_table("ORTHOGONAL-INIT (curr-GRU vs LM vs mem-aug)", rows)

    cracks36 = cracks_t3(t3_cells)
    t2_ok = keeps_t2(t2_cells)
    means = {L: round(t3_cells[L]["curr"].mean(), 3) for L in SLATE_RUNGS}
    print(f"\nT3@{T3_BREAK} ortho-init: curr={means} sep@>=2rungs={len(sep_rungs(t3_cells))>=2} "
          f"sep-rungs={sep_rungs(t3_cells)}")
    print(f"T2@{T2_SENTINEL} sentinel kept: {t2_ok}")
    print(f"orthogonal init cracks T3@{T3_BREAK}: {cracks36}\n")

    if cracks36 and t2_ok:
        verdict_line("H_1008", "PASS",
                     f"ORTHOGONAL-INIT-CRACKS-T3-CAP — initializing the GRU's recurrent matrices as "
                     f"ORTHOGONAL (vs the H_1000 1/sqrt(H) Gaussian baseline), at the SAME 40-ep "
                     f"budget / capacity / curriculum (NO extra compute or labels), RESTORES the "
                     f"WM>LM separator on T3 at the H_1005 break length {T3_BREAK} (curr-GRU {means} "
                     f">> chance {CHANCE_T3:.3f}, d>0.8 vs LM at >=2 rungs) WHILE keeping T2@"
                     f"{T2_SENTINEL}. The H_1005 T3 cap was a long-range GRADIENT-CONDITIONING limit: "
                     f"orthogonal recurrence (unit singular values) lets gradient propagate through "
                     f"the {T3_BREAK}-step BPTT chain without vanishing, bootstrapping the integrator "
                     f"past the cap — a FREE method-shape unlock (no extra compute, no extra labels; "
                     f"toy len {T3_BREAK}, production OPEN, a_scale_honest_scope).")
    else:
        verdict_line("H_1008", "FAIL",
                     f"ORTHOGONAL-INIT-INSUFFICIENT — orthogonal recurrent init does NOT crack the "
                     f"H_1005 T3 cap at len {T3_BREAK} (curr-GRU {means}, sep@>=2rungs="
                     f"{len(sep_rungs(t3_cells))>=2}, T2-kept={t2_ok}). The cap is NOT (just) a "
                     f"gradient-conditioning limit — a better-conditioned recurrence alone does not "
                     f"teach the mod-{T3_P} ring counter at {T3_BREAK} steps from a final-step label "
                     f"(closed-negative, a_paper_negative_ok; toy, production OPEN, "
                     f"a_scale_honest_scope).")
    print(f"\n[total wall {time.time()-t0:.0f}s]")


if __name__ == "__main__":
    main()
