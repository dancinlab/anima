"""H_1007 — LENGTH-PROPORTIONAL epoch budget: is the H_1005 T3 cap just a compute-vs-horizon
tradeoff (fixed budget at a longer horizon), or a method-shape limit that more compute can't buy?

H_1005 held the TOTAL epoch budget FIXED at 40 across all lengths (by design — to isolate the
horizon at fixed compute). Its mechanism finding: the curriculum spends its 40 epochs clearing
short stages and arrives at the len-32 stage too LATE to bootstrap (train-acc already at chance).
The obvious confound H_1005 itself names as OPEN: maybe T3@36 just needs MORE epochs at the long
stage. THIS H removes that confound — scale the total budget PROPORTIONALLY to the target length
(budget = 40 * len/18, so len=36 gets ~80 epochs, 2x) so the long stage gets a fair share.

This is the explicit "is the unlock just more compute?" control demanded by the mission. If a
length-proportional budget cracks T3@36 -> the cap was a BUDGET tradeoff (more compute at horizon
suffices); REPORTED as the finding (NOT a free method-shape unlock). If it STILL fails even with
~2-4x the compute -> the cap is a genuine method-shape / credit-assignment limit that compute
alone does not buy.

FROZEN PASS = length-proportional-budget curr-GRU SOLVES T3@36 (>> chance 1/6, d>0.8 vs LM at
>=2 rungs) AND keeps T2@40; FAIL = still ~chance even with the scaled budget (cap is not compute).
The ONLY moved lever vs H_1005 = the total epoch budget (scaled with length); the EXTRA compute
is REPORTED (epochs per rung printed). substrate=CPU-mirror; g5 CODE-measured; toy len 36/72.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "CWM", "probes"))
import time
import numpy as np
from h1006_method_lib import (SLATE_RUNGS, SLATE_SEEDS, T3_BREAK, T2_SENTINEL,
                              CHANCE_T3, CHANCE_T2, make_full, run_baseline_curr,
                              sep_rungs, solves, cracks_t3, keeps_t2, print_table,
                              header, verdict_line)
from h985_keystone_scaleup import T3_STEPS, T3_P, T2_CTX, T3_CTX
from h1000_gru_wm_t2t3 import run_cell_lm
from h1003_t2t3_curriculum import t2_episode_len, t3_episode_len, TOTAL_EPOCHS

# T3 ladder: the break (36) AND 2x-break (72) — at length-PROPORTIONAL budget each.
T3_LENS = [T3_BREAK, T3_STEPS * 4]   # 36, 72


def budget_for(target, base_len=T3_STEPS, base_ep=TOTAL_EPOCHS):
    """budget proportional to length: base_ep * target/base_len, rounded. len=18->40, 36->80, 72->160."""
    return int(round(base_ep * target / base_len))


def run_arm(maker, ncl, ctx, target, latent, seed, budget):
    cg, _, _ = run_baseline_curr(maker, ncl, target, latent, seed, total_epochs=budget)
    fm = make_full(maker, target)
    l, _ = run_cell_lm(fm, ctx, ncl, latent, seed, memaug=False)
    m, _ = run_cell_lm(fm, ctx, ncl, latent, seed, memaug=True)
    return cg, l, m


def main():
    t0 = time.time()
    header("H_1007",
           "Length-proportional epoch budget — is the T3@36 cap just a compute tradeoff?")
    base_b = TOTAL_EPOCHS
    print(f"T3 lens={T3_LENS} (H_1005 break + 2x), T2 sentinel len={T2_SENTINEL}. rungs="
          f"{SLATE_RUNGS} seeds={SLATE_SEEDS}. ONLY moved lever vs H_1005 = TOTAL budget scaled "
          f"PROPORTIONALLY to length (base {base_b}ep @ len{T3_STEPS} -> "
          f"{ {L: budget_for(L) for L in T3_LENS} } @ T3 lens). EXTRA compute REPORTED.\n")

    rows = []
    t3_cells = {}        # t3_cells[len][rung]
    for target in T3_LENS:
        budget = budget_for(target)
        t3_cells[target] = {}
        for latent in SLATE_RUNGS:
            curr, lm, mem = [], [], []
            for s in range(SLATE_SEEDS):
                cg, l, m = run_arm(t3_episode_len, T3_P, T3_CTX, target, latent, s, budget)
                curr.append(cg); lm.append(l); mem.append(m)
            curr, lm, mem = np.array(curr), np.array(lm), np.array(mem)
            t3_cells[target][latent] = dict(curr=curr, lm=lm)
            rows.append((f"T3 b={budget}", target, latent, CHANCE_T3, curr, lm, mem))
            print(f"  done T3 len={target:<3} budget={budget:<4} rung={latent:<3} "
                  f"curr={curr.mean():.3f} LM={lm.mean():.3f} mem={mem.mean():.3f} "
                  f"[{time.time()-t0:.0f}s]", flush=True)
    # T2@40 sentinel at proportional budget
    t2_cells = {}
    t2_budget = budget_for(T2_SENTINEL, base_len=20)  # T2 base len 20
    for latent in SLATE_RUNGS:
        curr, lm, mem = [], [], []
        for s in range(SLATE_SEEDS):
            cg, l, m = run_arm(t2_episode_len, 2, T2_CTX, T2_SENTINEL, latent, s, t2_budget)
            curr.append(cg); lm.append(l); mem.append(m)
        curr, lm, mem = np.array(curr), np.array(lm), np.array(mem)
        t2_cells[latent] = dict(curr=curr, lm=lm)
        rows.append((f"T2 b={t2_budget}", T2_SENTINEL, latent, CHANCE_T2, curr, lm, mem))
        print(f"  done T2 len={T2_SENTINEL} budget={t2_budget} rung={latent:<3} "
              f"curr={curr.mean():.3f} LM={lm.mean():.3f} mem={mem.mean():.3f} "
              f"[{time.time()-t0:.0f}s]", flush=True)

    print_table("LENGTH-PROPORTIONAL-BUDGET (curr-GRU vs LM vs mem-aug)", rows)

    print("\nT3 @ length-proportional budget (does MORE compute at horizon crack the cap?):")
    for target in T3_LENS:
        c = t3_cells[target]
        means = {L: round(c[L]["curr"].mean(), 3) for L in SLATE_RUNGS}
        print(f"  len={target:<3} budget={budget_for(target):<4} curr={means} "
              f"sep@>=2rungs={len(sep_rungs(c))>=2!s:<5} solves={solves(c, CHANCE_T3)!s:<5} "
              f"sep-rungs={sep_rungs(c)}")
    cracks36 = cracks_t3(t3_cells[T3_BREAK])
    t2_ok = keeps_t2(t2_cells)
    print(f"\nT2@{T2_SENTINEL} sentinel kept: {t2_ok}")
    print(f"length-proportional budget cracks T3@{T3_BREAK} (budget {budget_for(T3_BREAK)}ep "
          f"= {budget_for(T3_BREAK)/base_b:.1f}x H_1005): {cracks36}\n")

    if cracks36 and t2_ok:
        verdict_line("H_1007", "PASS",
                     f"T3-CAP-IS-A-BUDGET-TRADEOFF — scaling the TOTAL epoch budget PROPORTIONALLY "
                     f"to length ({budget_for(T3_BREAK)}ep at len {T3_BREAK} = "
                     f"{budget_for(T3_BREAK)/base_b:.1f}x H_1005's fixed {base_b}ep) RESTORES the "
                     f"WM>LM separator on T3 at the H_1005 break length {T3_BREAK} (curr-GRU "
                     f"{ {L: round(t3_cells[T3_BREAK][L]['curr'].mean(),3) for L in SLATE_RUNGS} } "
                     f">> chance {CHANCE_T3:.3f}, d>0.8 vs LM at >=2 rungs) WHILE keeping T2@"
                     f"{T2_SENTINEL}. The H_1005 T3 cap was NOT a method-shape limit but a "
                     f"COMPUTE-vs-HORIZON tradeoff: at H_1005's FIXED 40-ep budget the curriculum "
                     f"arrived at the long stage too late to bootstrap, but with budget scaled to "
                     f"the horizon the integrator gets enough epochs at the long stage to crack it. "
                     f"This is the HONEST finding: the cap is bought back by MORE compute, NOT a "
                     f"free unlock (REPORTED — the budget grew with length; toy len {T3_BREAK}, "
                     f"production OPEN, a_scale_honest_scope).")
    else:
        verdict_line("H_1007", "FAIL",
                     f"T3-CAP-IS-NOT-JUST-COMPUTE — even a LENGTH-PROPORTIONAL budget "
                     f"({budget_for(T3_BREAK)}ep = {budget_for(T3_BREAK)/base_b:.1f}x H_1005 at len "
                     f"{T3_BREAK}, {budget_for(T3_LENS[-1])}ep = {budget_for(T3_LENS[-1])/base_b:.1f}x "
                     f"at len {T3_LENS[-1]}) does NOT crack the T3 cap (curr-GRU "
                     f"{ {L: round(t3_cells[T3_BREAK][L]['curr'].mean(),3) for L in SLATE_RUNGS} } at "
                     f"len {T3_BREAK}, sep@>=2rungs={len(sep_rungs(t3_cells[T3_BREAK]))>=2}). The "
                     f"H_1005 T3 horizon cap is a genuine METHOD-SHAPE / long-range credit-assignment "
                     f"limit that MORE compute at fixed method does NOT buy — the integrator fails "
                     f"to fit the mod-{T3_P} ring counter at {T3_BREAK} steps even with "
                     f"{budget_for(T3_BREAK)/base_b:.1f}x the epochs (closed-negative, "
                     f"a_paper_negative_ok; toy, production OPEN, a_scale_honest_scope).")
    print(f"\n[total wall {time.time()-t0:.0f}s]")


if __name__ == "__main__":
    main()
