"""H_1011 — DENSE per-step state supervision SCALE-UP: does the H_1006 dense-supervision crack of
T3@36 KEEP holding as the horizon scales to 72, 144 — or does dense-sup have its own horizon cap?

H_1006 (🟢 DENSE-SUPERVISION-CRACKS-T3-CAP) showed per-step hidden-state supervision restores the
WM>LM separator on T3 at len=36 — the EXACT horizon where H_1005's length-curriculum BROKE (🔴
CURRICULUM-HORIZON-CAPPED). The credit-DENSITY lever beat the long-range credit-assignment wall at
len 36. OPEN (this H): does it KEEP working as the horizon scales (72, 144), removing the horizon
dependence — or does dense-sup itself cap at some longer horizon (just farther out than curriculum)?

FROZEN FALSIFIER (H_1011.md §2, frozen 2026-06-07): reuse the H_1006 dense-supervision GRU-WM + the
T3 generator + capacity-matched LM + mem-aug control VERBATIM. Run a T3 LENGTH LADDER in {36, 72,
144} (>=3 rungs), multi-seed, capacity-matched. The ONLY moved lever vs H_1006 is the TARGET LENGTH.
  - PASS = DENSE-SUP-SCALES: dense-sup SOLVES T3 (>> chance 0.167, d>0.8 vs LM tracking mem-aug) at
    ALL rungs incl. the longest (144) -> credit-density REMOVES the horizon dependence.
  - FAIL = DENSE-SUP-HORIZON-CAPPED-AT-<L>: it caps at some horizon (acc collapses to chance at len
    L) -> per-step supervision buys a longer-but-still-bounded horizon; report the break length (a
    refined scaling law over H_1005 / H_1006).

WALL-TIME GUARD (PROBE_CONVENTIONS): len144 BPTT is ~4x deeper than the H_1006 len36 cell (which ran
~200-250s/cell at 6 seeds). To stay under wall-budget we START with SEEDS_LADDER=3 (of H_1006's 6 —
REPORTED) and the EPOCH budget held EQUAL to H_1005/H_1006 (40ep, NOT scaled with length — by design,
isolating the horizon at fixed compute, == H_1005). dose = full dense (every-1) ONLY — the final-only
break is already the H_1005 measured baseline (the LM arm is the apples-to-apples chance floor here).
If a rung is too slow it is CUT and the cut REPORTED (a smaller honest ladder beats a hang).

substrate=CPU-mirror (pure numpy GRU + BPTT + Adam; NO torch, $0 CPU-local, deterministic per seed).
g5 CODE-measured, no LLM self-judge (p7). a_scale_honest_scope: TOY ladder; production / real-corpus
transfer UNVERIFIED. NOTHING on AKIDA (a_lane_akida_gpu_split).
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "CWM", "probes"))
import time
import numpy as np
from h1006_dense_supervision import run_dense            # dense (every-1) curr-GRU treatment, VERBATIM
from h1006_method_lib import (CHANCE_T3, make_full, print_table, header, verdict_line,
                              cohens_d)
from h985_keystone_scaleup import T3_P, T3_CTX
from h1000_gru_wm_t2t3 import run_cell_lm                 # LM + mem-aug arms, VERBATIM
from h1003_t2t3_curriculum import t3_episode_len, TOTAL_EPOCHS

# ---- H_1011 scale-ladder knobs (the ONLY moved lever vs H_1006 = TARGET LENGTH) -------------
T3_LADDER = [36, 72, 144]   # the >=3-rung horizon ladder (1x/2x/4x the H_1006 break point)
SLATE_RUNGS = [16, 32]      # capacity-matched to H_1006 (its top-2 width rungs)
SEEDS_LADDER = 3            # WALL-TIME TRIM of H_1006's 6 (REPORTED — len144 BPTT is ~4x deeper)
AUX_STRIDE = 1              # full dense (every-1) — the H_1006 winning dose
# wall budget per rung; if a cell exceeds this, CUT remaining rungs and REPORT (PROBE_CONVENTIONS)
WALL_CUT_S = 5400           # 90 min hard cut per cumulative rung-checkpoint


def cell(target, latent, seed):
    """ONE (len,rung,seed) cell: dense curr-GRU (H_1006 run_dense VERBATIM) vs LM vs mem-aug.
    Draw order identical to H_1006 so the LM/mem arms stay apples-to-apples."""
    cg, _ = run_dense(t3_episode_len, T3_P, target, latent, seed, AUX_STRIDE)
    fm = make_full(t3_episode_len, target)
    l, _ = run_cell_lm(fm, T3_CTX, T3_P, latent, seed, memaug=False)
    m, _ = run_cell_lm(fm, T3_CTX, T3_P, latent, seed, memaug=True)
    return cg, l, m


def sep_rungs_d(cells, latents):
    return [L for L in latents
            if cohens_d(cells[L]["curr"], cells[L]["lm"]) > 0.8
            and (cells[L]["curr"].mean() - cells[L]["lm"].mean()) > 0.1]


def solved_at(cells, latents):
    """frozen SOLVE @ a rung-set: sep@>=2rungs (d>0.8 & gap>0.1) AND curr>>chance(+0.1) at both."""
    sep = sep_rungs_d(cells, latents)
    above = all(cells[L]["curr"].mean() > CHANCE_T3 + 0.1 for L in latents)
    return len(sep) >= 2 and above, sep


def main():
    t0 = time.time()
    header("H_1011",
           "Dense per-step supervision SCALE-UP — does it keep cracking T3 at horizon 72/144, or cap?")
    print(f"T3 LADDER={T3_LADDER} (1x/2x/4x the H_1006 break @36). rungs={SLATE_RUNGS} "
          f"seeds={SEEDS_LADDER} (WALL-TRIM of H_1006's 6 — REPORTED). budget={TOTAL_EPOCHS}ep "
          f"(== H_1005/H_1006, NOT scaled with length — isolates horizon at fixed compute). "
          f"dose=every-1 (full dense, the H_1006 winning treatment). aux head=TRAINING-only; "
          f"eval=final-label. chance={CHANCE_T3:.3f}. ONLY moved lever vs H_1006 = TARGET LENGTH.\n")

    rows = []
    ladder_cells = {}     # length -> {rung -> dict(curr,lm,mem)}
    cut_lengths = []      # rungs we had to CUT for wall-time (REPORTED)
    cut_triggered = False
    for target in T3_LADDER:
        # CUT the rest of the ladder ONLY once a prior rung pushed cumulative wall past the budget
        if cut_triggered or (time.time() - t0) > WALL_CUT_S:
            cut_triggered = True
            cut_lengths.append(target)
            print(f"  CUT len={target} — cumulative wall {time.time()-t0:.0f}s exceeded budget "
                  f"{WALL_CUT_S}s (PROBE_CONVENTIONS: smaller honest ladder beats a hang)", flush=True)
            continue
        ladder_cells[target] = {}
        for latent in SLATE_RUNGS:
            curr, lm, mem = [], [], []
            for s in range(SEEDS_LADDER):
                cg, l, m = cell(target, latent, s)
                curr.append(cg); lm.append(l); mem.append(m)
                print(f"    [len{target} rung{latent} seed{s}] curr={cg:.3f} LM={l:.3f} "
                      f"mem={m:.3f}  [{time.time()-t0:.0f}s]", flush=True)
            curr, lm, mem = np.array(curr), np.array(lm), np.array(mem)
            ladder_cells[target][latent] = dict(curr=curr, lm=lm, mem=mem)
            rows.append((f"T3 len{target}", target, latent, CHANCE_T3, curr, lm, mem))
            print(f"  done len={target:<4} rung={latent:<3} curr={curr.mean():.3f} "
                  f"LM={lm.mean():.3f} mem={mem.mean():.3f}  [{time.time()-t0:.0f}s]", flush=True)

    print_table("DENSE-SUPERVISION SCALE-UP — T3 length ladder (dense curr-GRU vs LM vs mem-aug)", rows)

    # ---- ladder summary + frozen ruling ----
    print("\nladder (T3 — does dense-sup keep cracking the cap as horizon grows?):")
    solved = {}
    measured_lengths = [L for L in T3_LADDER if L in ladder_cells]
    for target in measured_lengths:
        c = ladder_cells[target]
        ok, sep = solved_at(c, SLATE_RUNGS)
        solved[target] = ok
        means = {L: round(c[L]["curr"].mean(), 3) for L in SLATE_RUNGS}
        lmmeans = {L: round(c[L]["lm"].mean(), 3) for L in SLATE_RUNGS}
        ds = {L: round(cohens_d(c[L]["curr"], c[L]["lm"]), 2) for L in SLATE_RUNGS}
        print(f"  len={target:<4} curr={means} LM={lmmeans} d={ds} sep@>=2rungs={len(sep)>=2!s:<5} "
              f"SOLVED={ok!s:<5} sep-rungs={sep}")

    longest = max(measured_lengths) if measured_lengths else None
    # harness validation: len36 must reproduce the H_1006 crack (SOLVED), else mis-wired
    harness_ok = solved.get(36, False)
    # find the first break length (smallest measured length that is NOT solved)
    break_len = None
    for target in measured_lengths:
        if not solved[target]:
            break_len = target
            break
    scales = all(solved[L] for L in measured_lengths) and longest == max(T3_LADDER)

    print(f"\nharness-validate (len36 reproduces H_1006 dense crack): {harness_ok}")
    print(f"measured ladder rungs: {measured_lengths}  (CUT for wall-time: {cut_lengths})")
    print(f"longest measured: {longest}  break length: {break_len}  scales-to-all: {scales}\n")

    curr_summary = {L: {R: round(ladder_cells[L][R]["curr"].mean(), 3) for R in SLATE_RUNGS}
                    for L in measured_lengths}

    if scales:
        verdict_line("H_1011", "PASS",
                     f"DENSE-SUP-SCALES — per-step hidden-state supervision (H_1006's dense every-1 "
                     f"treatment, VERBATIM) KEEPS cracking T3 across the FULL length ladder "
                     f"{measured_lengths} incl. the longest ({longest}): dense curr-GRU {curr_summary} "
                     f">> chance {CHANCE_T3:.3f}, d>0.8 vs the stateless LM at >=2 width-rungs (mem-aug "
                     f"=ceiling) at EVERY rung. Credit-DENSITY REMOVES the horizon dependence that "
                     f"capped the H_1005 length-curriculum at 36 — the WM>LM generality is "
                     f"HORIZON-ROBUST under per-step supervision. CAVEAT (the cost, == H_1006): the "
                     f"method REQUIRES per-step ground-truth state (an EXTRA label a final-label-only "
                     f"task does not give for free) — reach, not free-lunch. TOY ladder (seeds="
                     f"{SEEDS_LADDER} wall-trim of 6, REPORTED; budget={TOTAL_EPOCHS}ep fixed); "
                     f"production / real-corpus transfer OPEN (a_scale_honest_scope).")
    else:
        verdict_line("H_1011", "FAIL",
                     f"DENSE-SUP-HORIZON-CAPPED-AT-{break_len} — per-step hidden-state supervision "
                     f"(H_1006's dense every-1 treatment, VERBATIM) cracks T3 at len 36 (harness-"
                     f"validated == H_1006) but BREAKS at len {break_len}: dense curr-GRU collapses "
                     f"toward chance {CHANCE_T3:.3f} (sep lost / d<0.8 vs LM). Measured ladder "
                     f"{measured_lengths} (CUT for wall-time: {cut_lengths}); curr {curr_summary}. "
                     f"Per-step supervision buys a LONGER-but-still-BOUNDED horizon than the "
                     f"length-curriculum (H_1005 capped at 36 too, but at chance there; dense-sup "
                     f"pushes the WM>LM separator out, capping at {break_len}) — a refined scaling "
                     f"law: credit-DENSITY raises the horizon ceiling but does NOT remove the horizon "
                     f"dependence (closed-negative, a_paper_negative_ok). TOY ladder (seeds="
                     f"{SEEDS_LADDER}, budget={TOTAL_EPOCHS}ep fixed, NOT length-scaled — by design); "
                     f"larger-budget / production OPEN (a_scale_honest_scope).")
    if not harness_ok:
        print("\n*** WARNING: harness validation FAILED (len36 did not reproduce the H_1006 dense "
              "crack) — verdict is SUSPECT, re-check wiring before ruling. ***")
    print(f"\n[total wall {time.time()-t0:.0f}s]")


if __name__ == "__main__":
    main()
