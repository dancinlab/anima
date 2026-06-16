"""h1006_method_lib — shared $0 CPU-local harness for the H_1006-1011 LEARNING-METHOD slate.

Goal of the slate: the CWM thread converged that the world-model's failure on T3 (modular
path-integration) at long horizon is NOT the primitive (H_1000) and NOT representability
(mem-aug LM = 1.0 everywhere) but HOW you train it — long-range credit assignment. H_1003
showed a length-CURRICULUM cracks T2/T3 at base length; H_1005 showed that crack is
HORIZON-CAPPED: T3 BREAKS at len 36 (2x base 18) while T2 (commutative XOR-parity) scales to
80 (4x). H_1005's named mechanism: the integrator's TRAIN-acc collapses at the len-32 ramp
stage — it never even fits the long-horizon training set from a single final-step label.

This slate brainstorms LEARNING METHODS (beyond length-curriculum) and tests each on the SAME
T3 harness at the H_1005 BREAK POINT (len=36), keeping a T2@40 sentinel to confirm the method
does not break the family that already scales. The ONLY thing each H changes is the LEARNING
METHOD; tasks / GRU primitive / LM+mem-aug arms are imported VERBATIM from h1003/h1000/h985.

FROZEN shared falsifier (per-H .md re-states it): does method M let the GRU-WM SOLVE T3 at
len>=36 (the H_1005 break) AND keep T2? PASS = T3@36 >> chance (1/6) + large effect d>0.8 vs
the stateless LM at >=2 width-rungs, tracking mem-aug; FAIL = still ~chance, sep lost (== H_1005).
Compute is matched to H_1005 (40-epoch budget, rungs {16,32}, seeds) UNLESS a method's whole
point is to spend MORE (H_1007 length-proportional budget) — in which case the extra compute is
REPORTED as the finding ("the cap is a budget tradeoff" vs "a method-shape unlock").

substrate=CPU-mirror (pure numpy GRU + BPTT + Adam; NO torch, $0 CPU-local, deterministic per
seed). g5 CODE-measured, no LLM self-judge (p7). a_scale_honest_scope: TOY — bounded dim/N,
single horizon (len 36, the H_1005 break), pure-numpy GRU; production / real-corpus transfer
UNVERIFIED. NOTHING on AKIDA (a_lane_akida_gpu_split).
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "CWM", "probes"))
import numpy as np
from cwm_probe_lib import cohens_d, welch_t, header, verdict_line  # noqa: F401

from h985_keystone_scaleup import (N_TRAIN, N_TEST, onehot,
                                   T2_LEN, T2_CTX, T3_P, T3_STEPS, T3_CTX)
from h1000_gru_wm_t2t3 import (GRUWorldModel, run_cell_lm, GRU_BATCH, GRU_LR,
                               gru_hidden_for_rung)
from h1003_t2t3_curriculum import (t2_episode_len, t3_episode_len, _ramp,
                                   CURR_THRESH, CURR_MIN_EP, TOTAL_EPOCHS)

# ---- shared slate knobs (matched to H_1005 unless a method's point is to differ) -----------
SLATE_RUNGS = [16, 32]      # == H_1005 trim of H_1003's [16,32,64,128] (REPORTED)
SLATE_SEEDS = 6             # == H_1005 trim of 10 (REPORTED)
T3_BREAK = T3_STEPS * 2     # 36 — the H_1005 BREAK point (the thing every method must crack)
T2_SENTINEL = T2_LEN * 2    # 40 — a T2@2x sentinel (H_1005: T2 HOLDS here) — method must keep it
CHANCE_T3 = 1.0 / T3_P      # 0.1667
CHANCE_T2 = 0.5


def make_full(maker, target):
    return lambda rng, memaug=False: maker(rng, target, memaug=memaug)


# ============================================================================================
# Baseline curriculum-GRU at a TARGET length — the H_1005 arm, VERBATIM-faithful (no method).
# Returns (test_success, progression). Identical draw order to h1005 so it reproduces the
# break (harness validation: T3@36 must come out at chance, T2@40 at solved).
# ============================================================================================
def gru_train_curriculum_len(gru, maker, target, seed, total_epochs=TOTAL_EPOCHS):
    stages = _ramp(target)
    train_rng = np.random.default_rng(seed + 4242)
    data_rng = np.random.default_rng(seed)
    progression = []
    epochs_left = total_epochs
    n_stages = len(stages)
    for si, slen in enumerate(stages):
        if epochs_left <= 0:
            break
        train = [maker(data_rng, slen, memaug=False) for _ in range(N_TRAIN)]
        seqs = [s for s, _, _ in train]
        labels = [int(cc) for _, cc, _ in train]
        remaining_after = n_stages - si - 1
        cap = epochs_left - CURR_MIN_EP * remaining_after
        cap = max(CURR_MIN_EP, min(cap, epochs_left))
        spent, acc = 0, 0.0
        for _ in range(cap):
            gru.train(seqs, labels, epochs=1, batch=GRU_BATCH, lr=GRU_LR, rng=train_rng)
            spent += 1
            pred = gru.predict(seqs)
            acc = float(np.mean(pred == np.array(labels)))
            if spent >= CURR_MIN_EP and acc >= CURR_THRESH and si < n_stages - 1:
                break
        epochs_left -= spent
        progression.append((int(slen), int(spent), round(acc, 3)))
    return progression


def run_baseline_curr(maker, ncl, target, latent, seed, total_epochs=TOTAL_EPOCHS):
    """H_1005 baseline arm (length curriculum, fixed budget). EVAL on full-target test set."""
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
    prog = gru_train_curriculum_len(gru, maker, target, seed, total_epochs)
    pred = gru.predict(tseqs)
    return float(np.mean(pred == yte)), prog, gru


# ============================================================================================
# shared eval helpers: arms (curr-GRU treatment vs LM vs mem-aug) over SLATE_SEEDS, and the
# frozen PASS/FAIL ruling (T3@36 cracked? + T2@40 kept?).
# ============================================================================================
def arms_over_seeds(treat_fn, maker, ncl, ctx, target, latent, seeds=SLATE_SEEDS):
    """treat_fn(maker, ncl, target, latent, seed) -> (success, extra). Returns (curr,lm,mem,extras)."""
    full_maker = make_full(maker, target)
    curr, lm, mem, extras = [], [], [], []
    for s in range(seeds):
        cg, ex = treat_fn(maker, ncl, target, latent, s)
        l, _ = run_cell_lm(full_maker, ctx, ncl, latent, s, memaug=False)
        m, _ = run_cell_lm(full_maker, ctx, ncl, latent, s, memaug=True)
        curr.append(cg); lm.append(l); mem.append(m); extras.append(ex)
    return np.array(curr), np.array(lm), np.array(mem), extras


def sep_rungs(cells, latents=SLATE_RUNGS):
    """cells[latent] = dict(curr,lm). Returns rungs with d>0.8 AND gap>0.1."""
    return [L for L in latents
            if cohens_d(cells[L]["curr"], cells[L]["lm"]) > 0.8
            and (cells[L]["curr"].mean() - cells[L]["lm"].mean()) > 0.1]


def solves(cells, chance, latents=SLATE_RUNGS):
    return all(cells[L]["curr"].mean() > chance + 0.1 for L in latents)


def cracks_t3(cells_t3):
    """frozen: T3@36 SOLVED if sep@>=2rungs AND solves(>chance+0.1 at both rungs)."""
    return len(sep_rungs(cells_t3)) >= 2 and solves(cells_t3, CHANCE_T3)


def keeps_t2(cells_t2):
    """frozen: T2@40 must stay SOLVED (the method must not break the family that already scales)."""
    return len(sep_rungs(cells_t2)) >= 2 and solves(cells_t2, CHANCE_T2)


def print_table(title, rows):
    """rows: list of (task,tgtLen,rung,chance,curr,lm,mem). Prints the per-cell table."""
    print("\n" + "=" * 96)
    print(title)
    print(f"{'task':<14}{'tgtLen':>7}{'rung':>5}{'chance':>8}{'currGRU':>9}{'LM':>8}{'memLM':>8}"
          f"{'gap':>8}{'d':>9}{'p':>10}")
    print("-" * 96)
    for (task, tlen, rung, ch, curr, lm, mem) in rows:
        gap = curr.mean() - lm.mean()
        d = cohens_d(curr, lm)
        try:
            _, p = welch_t(curr, lm)
        except Exception:
            p = float("nan")
        print(f"{task:<14}{tlen:>7}{rung:>5}{ch:>8.3f}{curr.mean():>9.3f}{lm.mean():>8.3f}"
              f"{mem.mean():>8.3f}{gap:>8.3f}{d:>9.2f}{p:>10.1e}")
    print("=" * 96)
