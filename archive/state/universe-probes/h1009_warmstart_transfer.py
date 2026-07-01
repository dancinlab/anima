"""H_1009 — WARM-START TRANSFER: does initializing the len-36 GRU from the len-18-SOLVED model
(instead of from scratch) crack the H_1005 T3 horizon cap?

H_1003/H_1005 showed the GRU SOLVES T3 at the base length 18 (the integrator IS learnable at
short horizon) but a from-scratch curriculum BREAKS at 36. A natural method: TRANSFER — first
train the GRU on the len-18 curriculum (where it solves), then WARM-START a len-36 run from those
weights and continue the curriculum out to 36. If the short-horizon ring-counter solution is a
good initialization for the long-horizon one, transfer should bootstrap past the cap. This is the
"warm-start from the shorter-length solved model" lever.

Compute note (REPORTED honestly): warm-start spends the len-18 budget FIRST (40 ep) and THEN the
len-36 budget (40 ep) = ~2x total epochs vs H_1005's single 40-ep run. So a PASS here is partly a
compute story (like H_1007) AND a transfer story; a FAIL means even a solved-short init + 2x
compute does not transfer to the long horizon (the short solution is not on the path to the long
one). Both readings are reported.

FROZEN PASS = warm-started curr-GRU SOLVES T3@36 (>> chance 1/6, d>0.8 vs LM at >=2 rungs) AND
keeps T2@40; FAIL = still ~chance (no transfer). ONLY moved lever vs H_1005 = warm-start init
from the len-18-solved weights. substrate=CPU-mirror; g5 CODE-measured; toy len 36.
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
from h985_keystone_scaleup import N_TRAIN, N_TEST, T3_STEPS, T3_P, T2_LEN, T2_CTX, T3_CTX
from h1000_gru_wm_t2t3 import GRUWorldModel, run_cell_lm, gru_hidden_for_rung
from h1003_t2t3_curriculum import t2_episode_len, t3_episode_len


def run_warmstart(maker, ncl, base_len, target, latent, seed):
    """Phase 1: train a GRU on the base-len curriculum (where it solves). Phase 2: CONTINUE the
    SAME GRU (warm-start — weights + Adam state carried) on the target-len curriculum. EVAL on
    full-target test set. The ONLY change vs H_1005 is that phase-2 starts from a solved init."""
    full_maker = make_full(maker, target)
    test_rng = np.random.default_rng(seed)
    for _ in range(N_TRAIN):
        full_maker(test_rng, memaug=False)
    test = [full_maker(test_rng, memaug=False) for _ in range(N_TEST)]
    tseqs = [s for s, _, _ in test]
    yte = np.array([cc for _, cc, _ in test])
    in_dim = tseqs[0].shape[1]
    hidden = gru_hidden_for_rung(latent)
    gru = GRUWorldModel(in_dim, hidden, ncl, seed=seed + 7)
    # Phase 1: base length (in_dim is FIXED across lengths so weights are directly transferable)
    prog1 = gru_train_curriculum_len(gru, maker, base_len, seed)
    # Phase 2: warm-start at the target length (SAME gru object — weights+Adam carried)
    prog2 = gru_train_curriculum_len(gru, maker, target, seed + 1)
    pred = gru.predict(tseqs)
    return float(np.mean(pred == yte)), (prog1, prog2)


def run_arm(maker, ncl, ctx, base_len, target, latent, seed):
    cg, prog = run_warmstart(maker, ncl, base_len, target, latent, seed)
    fm = make_full(maker, target)
    l, _ = run_cell_lm(fm, ctx, ncl, latent, seed, memaug=False)
    m, _ = run_cell_lm(fm, ctx, ncl, latent, seed, memaug=True)
    return cg, l, m, prog


def main():
    t0 = time.time()
    header("H_1009", "Warm-start transfer from the len-18-solved model — crack the T3@36 cap?")
    print(f"T3: phase1 base len={T3_STEPS} (solved) -> phase2 warm-start to len={T3_BREAK} "
          f"(H_1005 break). T2 sentinel: base {T2_LEN} -> {T2_SENTINEL}. rungs={SLATE_RUNGS} "
          f"seeds={SLATE_SEEDS}. ONLY moved lever vs H_1005 = warm-start init from solved-short "
          f"weights. COMPUTE NOTE: 2x budget (40ep base + 40ep target) — REPORTED.\n")

    rows, t3_cells, t2_cells = [], {}, {}
    for latent in SLATE_RUNGS:
        curr, lm, mem, p0 = [], [], [], None
        for s in range(SLATE_SEEDS):
            cg, l, m, prog = run_arm(t3_episode_len, T3_P, T3_CTX, T3_STEPS, T3_BREAK, latent, s)
            curr.append(cg); lm.append(l); mem.append(m)
            if s == 0:
                p0 = prog
        curr, lm, mem = np.array(curr), np.array(lm), np.array(mem)
        t3_cells[latent] = dict(curr=curr, lm=lm)
        rows.append(("T3_warm", T3_BREAK, latent, CHANCE_T3, curr, lm, mem))
        print(f"  done T3 warm rung={latent:<3} curr={curr.mean():.3f} LM={lm.mean():.3f} "
              f"mem={mem.mean():.3f}  phase1-end={p0[0][-1] if p0 else '-'} "
              f"phase2-end={p0[1][-1] if p0 else '-'} [{time.time()-t0:.0f}s]", flush=True)
    for latent in SLATE_RUNGS:
        curr, lm, mem = [], [], []
        for s in range(SLATE_SEEDS):
            cg, l, m, _ = run_arm(t2_episode_len, 2, T2_CTX, T2_LEN, T2_SENTINEL, latent, s)
            curr.append(cg); lm.append(l); mem.append(m)
        curr, lm, mem = np.array(curr), np.array(lm), np.array(mem)
        t2_cells[latent] = dict(curr=curr, lm=lm)
        rows.append(("T2_warm", T2_SENTINEL, latent, CHANCE_T2, curr, lm, mem))
        print(f"  done T2 warm rung={latent:<3} curr={curr.mean():.3f} LM={lm.mean():.3f} "
              f"mem={mem.mean():.3f} [{time.time()-t0:.0f}s]", flush=True)

    print_table("WARM-START-TRANSFER (curr-GRU vs LM vs mem-aug)", rows)

    cracks36 = cracks_t3(t3_cells)
    t2_ok = keeps_t2(t2_cells)
    means = {L: round(t3_cells[L]["curr"].mean(), 3) for L in SLATE_RUNGS}
    print(f"\nT3@{T3_BREAK} warm-start: curr={means} sep@>=2rungs={len(sep_rungs(t3_cells))>=2} "
          f"sep-rungs={sep_rungs(t3_cells)}")
    print(f"T2@{T2_SENTINEL} sentinel kept: {t2_ok}")
    print(f"warm-start transfer cracks T3@{T3_BREAK}: {cracks36}\n")

    if cracks36 and t2_ok:
        verdict_line("H_1009", "PASS",
                     f"WARM-START-TRANSFER-CRACKS-T3-CAP — initializing the len-{T3_BREAK} GRU from "
                     f"the len-{T3_STEPS}-SOLVED model (then continuing the curriculum to {T3_BREAK}) "
                     f"RESTORES the WM>LM separator on T3 at the H_1005 break (curr-GRU {means} >> "
                     f"chance {CHANCE_T3:.3f}, d>0.8 vs LM at >=2 rungs) WHILE keeping T2@"
                     f"{T2_SENTINEL}. The short-horizon ring-counter solution IS on the path to the "
                     f"long-horizon one: a solved-short init bootstraps the integrator past the cap. "
                     f"COMPUTE CAVEAT (REPORTED): this spends ~2x the epochs (base + target phases) "
                     f"vs H_1005's single budget — so the unlock is partly transfer, partly more "
                     f"compute (cf H_1007); both reported (toy len {T3_BREAK}, production OPEN, "
                     f"a_scale_honest_scope).")
    else:
        verdict_line("H_1009", "FAIL",
                     f"WARM-START-NO-TRANSFER — initializing from the len-{T3_STEPS}-solved model "
                     f"(plus ~2x compute) does NOT crack the H_1005 T3 cap at len {T3_BREAK} "
                     f"(curr-GRU {means}, sep@>=2rungs={len(sep_rungs(t3_cells))>=2}, "
                     f"T2-kept={t2_ok}). The short-horizon ring-counter solution does NOT transfer "
                     f"to the long horizon — it is not a good initialization for the {T3_BREAK}-step "
                     f"integrator (the long-horizon solution is in a different basin). The cap "
                     f"survives warm-start + extra compute (closed-negative, a_paper_negative_ok; "
                     f"toy, production OPEN, a_scale_honest_scope).")
    print(f"\n[total wall {time.time()-t0:.0f}s]")


if __name__ == "__main__":
    main()
