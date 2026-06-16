"""H_1010 — MODULUS-axis curriculum: ramp the ring SIZE (mod-P state-space), not the length —
does an easy->hard STATE-SPACE curriculum at full len=36 crack the H_1005 T3 horizon cap?

H_1005 capped T3 (modular path-integration) at length while T2 (commutative 1-bit accumulator)
scaled — the interpretation was that the mod-6 RING COUNTER's long-range credit chain is the hard
part. H_1003/H_1005 only ever ramped the LENGTH axis. THIS H ramps a DIFFERENT axis: the RING
SIZE P (the state-space granularity), at the FULL break length 36 throughout. Curriculum mod-2 ->
mod-3 -> mod-4 -> mod-6 (a parity-like 2-state counter is easy; the 6-state ring is hard),
advancing on the same competence threshold, same 40-ep budget. If the integrator can be
bootstrapped by growing the STATE-SPACE at full length (where length-curriculum failed), the cap
is about state-space granularity, not horizon — a different method-shape unlock.

in_dim is FIXED at the max P=6 layout (2 move + 1 query + 6 position channels = 9) across the
whole curriculum (mod-2 episodes only use the first 2 position channels); the GRU/LM never see a
changing input space — only the number of reachable states grows. The final eval is the SAME
full mod-6 / len-36 held-out test as H_1005 (apples-to-apples with the break point).

FROZEN PASS = modulus-curriculum curr-GRU SOLVES T3(mod-6)@len36 (>> chance 1/6, d>0.8 vs LM at
>=2 rungs) AND keeps T2@40; FAIL = still ~chance (the cap is the horizon, not the state-space).
ONLY moved lever vs H_1005 = the curriculum AXIS (modulus instead of length). compute-matched
(40 ep). substrate=CPU-mirror; g5 CODE-measured; toy.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "CWM", "probes"))
import time
import numpy as np
from h1006_method_lib import (SLATE_RUNGS, SLATE_SEEDS, T3_BREAK, T2_SENTINEL,
                              CHANCE_T3, CHANCE_T2, make_full, gru_train_curriculum_len,
                              run_baseline_curr, sep_rungs, solves, cracks_t3, keeps_t2,
                              print_table, header, verdict_line)
from h985_keystone_scaleup import N_TRAIN, N_TEST, T3_P, T2_CTX, T3_CTX
from h1000_gru_wm_t2t3 import GRUWorldModel, run_cell_lm, GRU_BATCH, GRU_LR, gru_hidden_for_rung
from h1003_t2t3_curriculum import (t2_episode_len, t3_episode_len, _ramp,
                                   CURR_THRESH, CURR_MIN_EP, TOTAL_EPOCHS)

P_STAGES = [2, 3, 4, T3_P]    # ring-size curriculum: 2 -> 3 -> 4 -> 6 (full)
P_MAX = T3_P                  # in_dim fixed at the max-P layout (9 channels)


def t3_episode_modP(rng, steps, P, memaug=False):
    """T3 path-integration at ring size P, but in_dim FIXED at the P_MAX layout (2+1+P_MAX) so
    the input space is constant across the modulus curriculum. Position is mod-P (only the first
    P position channels are ever active); the final query target is the mod-P position."""
    in_dim = 2 + 1 + P_MAX
    T = steps + 1
    seq = np.zeros((T, in_dim))
    pos = 0
    for t in range(steps):
        mv = int(rng.integers(2))
        seq[t, mv] = 1.0
        pos = (pos + (1 if mv == 0 else -1)) % P
    seq[steps, 2] = 1.0
    if memaug:
        seq[steps, 3 + pos] = 1.0
    return seq, pos, P_MAX   # n_classes = P_MAX (fixed readout; unused classes stay unselected)


def gru_train_modulus_curriculum(gru, steps, seed):
    """Curriculum over MODULUS P (mod-2->3->4->6), at the FIXED full length `steps`, 40-ep budget."""
    train_rng = np.random.default_rng(seed + 4242)
    data_rng = np.random.default_rng(seed)
    progression = []
    epochs_left = TOTAL_EPOCHS
    n_stages = len(P_STAGES)
    for si, P in enumerate(P_STAGES):
        if epochs_left <= 0:
            break
        train = [t3_episode_modP(data_rng, steps, P) for _ in range(N_TRAIN)]
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
        progression.append((int(P), int(spent), round(acc, 3)))
    return progression


def run_modulus(steps, latent, seed):
    """Modulus-curriculum GRU. EVAL on full mod-P_MAX / full-length test set (== H_1005 break)."""
    test_rng = np.random.default_rng(seed)
    full = lambda rng, memaug=False: t3_episode_modP(rng, steps, P_MAX, memaug=memaug)
    for _ in range(N_TRAIN):
        full(test_rng)
    test = [full(test_rng) for _ in range(N_TEST)]
    tseqs = [s for s, _, _ in test]
    yte = np.array([cc for _, cc, _ in test])
    in_dim = tseqs[0].shape[1]
    hidden = gru_hidden_for_rung(latent)
    gru = GRUWorldModel(in_dim, hidden, P_MAX, seed=seed + 7)
    prog = gru_train_modulus_curriculum(gru, steps, seed)
    pred = gru.predict(tseqs)
    return float(np.mean(pred == yte)), prog


def run_arm_lm(steps, latent, seed):
    """LM/mem arms on the modP full-length task (apples-to-apples with the modulus eval)."""
    full = lambda rng, memaug=False: t3_episode_modP(rng, steps, P_MAX, memaug=memaug)
    l, _ = run_cell_lm(full, T3_CTX, P_MAX, latent, seed, memaug=False)
    m, _ = run_cell_lm(full, T3_CTX, P_MAX, latent, seed, memaug=True)
    return l, m


def main():
    t0 = time.time()
    header("H_1010", "Modulus-axis curriculum (mod-2->6) at len=36 — crack the T3 horizon cap?")
    print(f"T3 at FULL len={T3_BREAK} throughout; curriculum AXIS = ring size P {P_STAGES} "
          f"(not length). in_dim FIXED at P_MAX={P_MAX} layout. T2 sentinel len={T2_SENTINEL}. "
          f"rungs={SLATE_RUNGS} seeds={SLATE_SEEDS}, 40-ep budget (== H_1005). ONLY moved lever "
          f"vs H_1005 = the curriculum axis (modulus instead of length).\n")

    rows, t3_cells, t2_cells = [], {}, {}
    for latent in SLATE_RUNGS:
        curr, lm, mem, p0 = [], [], [], None
        for s in range(SLATE_SEEDS):
            cg, prog = run_modulus(T3_BREAK, latent, s)
            l, m = run_arm_lm(T3_BREAK, latent, s)
            curr.append(cg); lm.append(l); mem.append(m)
            if s == 0:
                p0 = prog
        curr, lm, mem = np.array(curr), np.array(lm), np.array(mem)
        t3_cells[latent] = dict(curr=curr, lm=lm)
        rows.append(("T3_modcurr", T3_BREAK, latent, CHANCE_T3, curr, lm, mem))
        print(f"  done T3 mod-curr rung={latent:<3} curr={curr.mean():.3f} LM={lm.mean():.3f} "
              f"mem={mem.mean():.3f}  prog={p0} [{time.time()-t0:.0f}s]", flush=True)
    # T2 sentinel — standard length curriculum (baseline arm; the method is T3-specific)
    for latent in SLATE_RUNGS:
        curr, lm, mem = [], [], []
        for s in range(SLATE_SEEDS):
            cg, _, _ = run_baseline_curr(t2_episode_len, 2, T2_SENTINEL, latent, s)
            fm = make_full(t2_episode_len, T2_SENTINEL)
            l, _ = run_cell_lm(fm, T2_CTX, 2, latent, s, memaug=False)
            m, _ = run_cell_lm(fm, T2_CTX, 2, latent, s, memaug=True)
            curr.append(cg); lm.append(l); mem.append(m)
        curr, lm, mem = np.array(curr), np.array(lm), np.array(mem)
        t2_cells[latent] = dict(curr=curr, lm=lm)
        rows.append(("T2_basecurr", T2_SENTINEL, latent, CHANCE_T2, curr, lm, mem))
        print(f"  done T2 base rung={latent:<3} curr={curr.mean():.3f} LM={lm.mean():.3f} "
              f"mem={mem.mean():.3f} [{time.time()-t0:.0f}s]", flush=True)

    print_table("MODULUS-CURRICULUM (curr-GRU vs LM vs mem-aug)", rows)

    cracks36 = cracks_t3(t3_cells)
    t2_ok = keeps_t2(t2_cells)
    means = {L: round(t3_cells[L]["curr"].mean(), 3) for L in SLATE_RUNGS}
    print(f"\nT3(mod-6)@{T3_BREAK} modulus-curriculum: curr={means} "
          f"sep@>=2rungs={len(sep_rungs(t3_cells))>=2} sep-rungs={sep_rungs(t3_cells)}")
    print(f"T2@{T2_SENTINEL} sentinel kept: {t2_ok}")
    print(f"modulus-axis curriculum cracks T3@{T3_BREAK}: {cracks36}\n")

    if cracks36 and t2_ok:
        verdict_line("H_1010", "PASS",
                     f"MODULUS-CURRICULUM-CRACKS-T3-CAP — ramping the curriculum on the RING-SIZE "
                     f"axis (mod-2->3->4->{T3_P}) at the FIXED full break length {T3_BREAK} "
                     f"(where the LENGTH curriculum FAILED in H_1005) RESTORES the WM>LM separator "
                     f"on T3 (curr-GRU {means} >> chance {CHANCE_T3:.3f}, d>0.8 vs LM at >=2 rungs) "
                     f"WHILE keeping T2@{T2_SENTINEL}. The H_1005 T3 cap was about STATE-SPACE "
                     f"granularity, not horizon: bootstrapping the integrator through a growing ring "
                     f"size (easy 2-state -> hard {T3_P}-state) at full length cracks it where "
                     f"growing the length did not — a DIFFERENT-AXIS method-shape unlock (compute-"
                     f"matched, no extra labels; toy len {T3_BREAK}, production OPEN, "
                     f"a_scale_honest_scope).")
    else:
        verdict_line("H_1010", "FAIL",
                     f"MODULUS-CURRICULUM-INSUFFICIENT — a ring-size curriculum (mod-2->{T3_P}) at "
                     f"full length {T3_BREAK} does NOT crack the H_1005 T3 cap (curr-GRU {means}, "
                     f"sep@>=2rungs={len(sep_rungs(t3_cells))>=2}, T2-kept={t2_ok}). The cap is "
                     f"about the long-range HORIZON (the {T3_BREAK}-step credit chain), NOT the "
                     f"state-space granularity — growing the modulus at full length does not "
                     f"substitute for the long-range integration the curriculum cannot bootstrap "
                     f"(closed-negative, a_paper_negative_ok; toy, production OPEN, "
                     f"a_scale_honest_scope).")
    print(f"\n[total wall {time.time()-t0:.0f}s]")


if __name__ == "__main__":
    main()
