"""H_985 (KEYSTONE SCALE-UP) — scale-up + task-diversity re-test of H_970.

H_970 found a WM>LM separator on ONE toy (delayed-cue recall) at ONE capacity: WM 0.995 vs
matched-capacity LM 0.258~chance (gap 0.737, d 36.8); a mem-aug LM control recovered to 1.0,
localizing the gap to the persistent-state requirement. a_toy_scale_recheck: a single toy
point is INCOMPLETE for a general claim. This H runs the ladder H_970 lacked.

FROZEN FALSIFIER (verbatim honored; pre-registered in the .md BEFORE this measurement):
  Build >=3 DISTINCT partially-observable task families, each requiring a persistent/partially-
  observed world-state (not just the one delayed-cue toy) x a small ladder of capacities
  (latent/feature dim). For each cell measure:
    arm-WM   = recurrent latent-state world model (persistent state)
    arm-LM   = capacity-matched feedforward windowed predictor (NO persistent state)
    arm-memLM= memory-augmented LM control (cue/needed-state re-exposed at decision step)
  D1 = task success WM vs LM vs memLM, per (task, rung).  D2 = gap (WM-LM) + Cohen d, per cell.
  D3 = does the WM>LM gap PERSIST as capacity grows (LM does NOT catch up) AND across ALL tasks,
       and does the mem-aug control CLOSE it (gap -> persistent-state requirement)?
  PASS (frozen): WM>LM gap PERSISTS (large effect d>0.8) across ALL >=3 task families AND
       >=2 capacity rungs, AND mem-aug control closes it -> SCALE+DIVERSITY-ROBUST (H_970
       generalizes; CWM premise robust beyond the single toy).
  FAIL (frozen): the gap COLLAPSES at larger capacity (LM catches up, d<0.8 at the top rung)
       OR is task-specific (holds only on delayed-cue) -> H_970 was a toy/task artifact
       (closed-negative, a_paper_negative_ok).
  INCOMPLETE: ladder too short / a task not actually WM-requiring (mem-aug doesn't close it).

THREE DISTINCT PARTIALLY-OBSERVABLE TASK FAMILIES (each needs a persistent latent world-state,
mechanistically different from the others — this is the diversity H_970 lacked):

  T1  delayed-cue recall (H_970's family, the anchor): a CUE at t=0, then L distractors,
      then GO -> recall the cue. The cue scrolls out of any fixed window. memLM = cue re-shown
      at GO. (memory of a single past symbol across a delay.)

  T2  hidden-state / POMDP parity tracking: a stream of +/-1 toggle events; the hidden world-
      state is the running PARITY (XOR) of all toggles so far, NEVER directly observed. At a
      query step, output the current parity. A fixed window sees only the last CTX toggles, not
      the accumulated hidden state -> chance for any window shorter than the stream. WM must
      integrate observations into a latent register. memLM = the true running parity exposed
      at the query. (integration of unobserved accumulated state, NOT a single stored symbol.)

  T3  multi-step counterfactual / hidden-position gridworld: an agent on a 1-D ring of size P
      takes a sequence of move actions (+1/-1) from an unobserved start; only the MOVES are
      observed, never the position. At GO, output the final position. The position is a hidden
      variable that must be integrated from the whole move history (a window of the last CTX
      moves under-determines absolute position). memLM = the true final position exposed at GO.
      (path-integration of a continuous-ish latent over many steps where PAST unobserved state
      matters — a counterfactual "where would I be" world-state.)

All three: a stateless windowed predictor is information-theoretically unable to recover the
target from its window; a persistent latent state can. The three differ in WHAT must be carried
(a symbol / an accumulated parity bit / an integrated position), so a PASS across all three is
diversity-robust, not a single-mechanism fluke.

CAPACITY LADDER (>=2 rungs, here 4): latent/feature dim in {16, 32, 64, 128}. WM and LM are
capacity-matched per rung (equal learned-readout params; both use a fixed random projection of
the same width + a ridge readout, so the LM is NOT handicapped by size).

substrate=CPU-mirror (numpy). $0 CPU-local. g5 CODE-measured, no LLM self-judge (p7).
a_scale_honest_scope: STILL a toy ladder (bounded dim/N), production-scale OPEN — but >=3 tasks
x >=4 rungs is the ladder H_970's single point lacked.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "CWM", "probes"))
import numpy as np
from cwm_probe_lib import (LatentWorldModel, StatelessLM, cohens_d, welch_t, header,
                           verdict_line)

# ---- ladder / task config (frozen) ------------------------------------------------------
RUNGS = [16, 32, 64, 128]      # capacity (latent/feature dim) ladder, >=2 rungs
N_SEEDS = 10
N_TRAIN = 600
N_TEST = 300

# T1 delayed-cue
T1_K = 4          # cue alphabet (chance 1/K = 0.25)
T1_L = 16         # delay
T1_CTX = 4        # LM window (< L)
# T2 parity tracking
T2_LEN = 20       # toggle-stream length (chance = 0.5, binary parity)
T2_CTX = 4        # LM window (< LEN)
# T3 hidden-position gridworld
T3_P = 6          # ring size (chance = 1/P)
T3_STEPS = 18     # number of moves
T3_CTX = 4        # LM window (< STEPS)


def onehot(i, n):
    v = np.zeros(n); v[i] = 1.0; return v


# ---- T1 delayed-cue recall (H_970's anchor family) -------------------------------------
def t1_episode(rng, memaug=False):
    in_dim = T1_K + 2                     # symbol(K) + is_cue + is_go
    c = int(rng.integers(T1_K))
    T = 1 + T1_L + 1
    seq = np.zeros((T, in_dim))
    seq[0, :T1_K] = onehot(c, T1_K); seq[0, T1_K] = 1.0
    for t in range(1, 1 + T1_L):
        seq[t, :T1_K] = onehot(int(rng.integers(T1_K)), T1_K)
    seq[1 + T1_L, T1_K + 1] = 1.0
    if memaug:
        seq[1 + T1_L, :T1_K] = onehot(c, T1_K)   # cue re-exposed at GO (external memory)
    return seq, c, T1_K


# ---- T2 hidden-state parity tracking ---------------------------------------------------
def t2_episode(rng, memaug=False):
    # observation = a toggle event one-hot {no-op, toggle} + is_query flag; hidden world-state
    # = running parity of toggles. target class in {0,1} = parity at the query (final) step.
    in_dim = 2 + 1 + 2                    # [is_noop, is_toggle, is_query, memaug_parity(2)]
    T = T2_LEN + 1
    seq = np.zeros((T, in_dim))
    parity = 0
    for t in range(T2_LEN):
        tog = int(rng.integers(2))       # 0 no-op, 1 toggle
        seq[t, tog] = 1.0
        parity ^= tog
    seq[T2_LEN, 2] = 1.0                  # query step
    if memaug:
        seq[T2_LEN, 3 + parity] = 1.0     # true running parity exposed at query
    return seq, parity, 2


# ---- T3 hidden-position gridworld (path integration) -----------------------------------
def t3_episode(rng, memaug=False):
    # observation = move one-hot {+1, -1} + is_go flag; hidden world-state = position on a ring
    # of size P from an unobserved start (fixed at 0). target = final position class in {0..P-1}.
    in_dim = 2 + 1 + T3_P                 # [move+, move-, is_go, memaug_pos(P)]
    T = T3_STEPS + 1
    seq = np.zeros((T, in_dim))
    pos = 0
    for t in range(T3_STEPS):
        mv = int(rng.integers(2))        # 0 -> +1, 1 -> -1
        seq[t, mv] = 1.0
        pos = (pos + (1 if mv == 0 else -1)) % T3_P
    seq[T3_STEPS, 2] = 1.0               # GO step
    if memaug:
        seq[T3_STEPS, 3 + pos] = 1.0      # true final position exposed at GO
    return seq, pos, T3_P


TASKS = {
    "T1_delayed_cue":   (t1_episode, T1_CTX, T1_K),
    "T2_parity_track":  (t2_episode, T2_CTX, 2),
    "T3_hidden_pos":    (t3_episode, T3_P and T3_CTX, T3_P),
}


def run_cell(make, ctx, n_classes, latent, seed, mode):
    """One (task, rung, seed) cell. mode in {'wm','lm','memlm'}; returns success rate."""
    rng = np.random.default_rng(seed)
    memaug = (mode == "memlm")
    train = [make(rng, memaug=memaug) for _ in range(N_TRAIN)]
    test = [make(rng, memaug=memaug) for _ in range(N_TEST)]
    in_dim = train[0][0].shape[1]
    Ytr = np.array([onehot(c, n_classes) for _, c, _ in train])
    yte = np.array([c for _, c, _ in test])

    if mode == "wm":
        wm = LatentWorldModel(in_dim, latent_dim=latent, seed=seed,
                              retentive=True, spectral_radius=1.0, in_scale=1.0)
        Htr = np.array([wm.final_latent(s) for s, _, _ in train])
        wm.fit_readout(Htr, Ytr)
        Hte = np.array([wm.final_latent(s) for s, _, _ in test])
        pred = wm.predict_readout(Hte).argmax(1)
    else:
        # lm and memlm both use the stateless windowed predictor; memlm differs only in that
        # the episode re-exposes the needed state at the decision step (external memory).
        lm = StatelessLM(in_dim, ctx=ctx, feat_dim=latent, seed=seed + 100)
        Ftr = np.array([lm.features_over_seq(s)[-1] for s, _, _ in train])
        lm.fit_readout(Ftr, Ytr)
        Fte = np.array([lm.features_over_seq(s)[-1] for s, _, _ in test])
        pred = lm.predict_readout(Fte).argmax(1)
    return float(np.mean(pred == yte))


def main():
    header("H_985", "Keystone WM>LM scale-up + task-diversity re-test (of H_970)")
    print(f"ladder (latent/feat dim) = {RUNGS}   N_SEEDS={N_SEEDS}  "
          f"N_train={N_TRAIN} N_test={N_TEST}")
    print(f"tasks: T1 delayed-cue (K={T1_K},L={T1_L},ctx={T1_CTX})  "
          f"T2 parity-track (len={T2_LEN},ctx={T2_CTX})  "
          f"T3 hidden-pos (P={T3_P},steps={T3_STEPS},ctx={T3_CTX})")
    print(f"capacity-matched per rung: WM readout (latent+1)*C == LM readout (feat+1)*C "
          f"(feat==latent)\n")

    chance = {"T1_delayed_cue": 1 / T1_K, "T2_parity_track": 0.5, "T3_hidden_pos": 1 / T3_P}

    # results[task][rung] = dict(wm=[...seeds], lm=[...], memlm=[...])
    results = {}
    for tname, (make, ctx, ncl) in TASKS.items():
        results[tname] = {}
        for latent in RUNGS:
            wm_s, lm_s, mem_s = [], [], []
            for s in range(N_SEEDS):
                wm_s.append(run_cell(make, ctx, ncl, latent, s, "wm"))
                lm_s.append(run_cell(make, ctx, ncl, latent, s, "lm"))
                mem_s.append(run_cell(make, ctx, ncl, latent, s, "memlm"))
            results[tname][latent] = dict(wm=np.array(wm_s), lm=np.array(lm_s),
                                          memlm=np.array(mem_s))

    # ---- per-cell table -----------------------------------------------------------------
    print("=" * 78)
    print(f"{'task':<16}{'rung':>5}{'chance':>8}{'WM':>9}{'LM':>9}{'memLM':>9}"
          f"{'gap':>8}{'d':>9}{'p':>10}")
    print("-" * 78)
    all_cells = []     # (task, rung, gap, d, p, wm, lm, memlm, chance)
    for tname in TASKS:
        ch = chance[tname]
        for latent in RUNGS:
            r = results[tname][latent]
            wm, lm, mem = r["wm"], r["lm"], r["memlm"]
            gap = wm.mean() - lm.mean()
            d = cohens_d(wm, lm)
            try:
                _, p = welch_t(wm, lm)
            except Exception:
                p = float("nan")
            print(f"{tname:<16}{latent:>5}{ch:>8.3f}{wm.mean():>9.3f}{lm.mean():>9.3f}"
                  f"{mem.mean():>9.3f}{gap:>8.3f}{d:>9.2f}{p:>10.1e}")
            all_cells.append((tname, latent, gap, d, p, wm.mean(), lm.mean(),
                              mem.mean(), ch))
    print("=" * 78)

    # ---- frozen PASS/FAIL evaluation ----------------------------------------------------
    # PASS needs: for EVERY task, gap large (d>0.8) at >=2 rungs AND specifically NOT
    # collapsing at the TOP rung (LM does not catch up), AND mem-aug closes the gap
    # (memLM near WM / well above LM) on every task.
    top_rung = RUNGS[-1]
    per_task_ok = {}
    memaug_closes = {}
    lm_catches_up_top = {}
    for tname in TASKS:
        ch = chance[tname]
        rungs_big = [latent for latent in RUNGS
                     if cohens_d(results[tname][latent]["wm"],
                                 results[tname][latent]["lm"]) > 0.8
                     and (results[tname][latent]["wm"].mean()
                          - results[tname][latent]["lm"].mean()) > 0.1]
        per_task_ok[tname] = len(rungs_big) >= 2
        top = results[tname][top_rung]
        d_top = cohens_d(top["wm"], top["lm"])
        # LM "catches up" at top rung if the gap there is no longer large.
        lm_catches_up_top[tname] = not (d_top > 0.8 and (top["wm"].mean() - top["lm"].mean()) > 0.1)
        # mem-aug closes the gap: memLM lands much closer to WM than plain LM does.
        mem_gain = top["memlm"].mean() - top["lm"].mean()
        wm_lm_gap_top = top["wm"].mean() - top["lm"].mean()
        memaug_closes[tname] = (mem_gain > 0.5 * wm_lm_gap_top) and (top["memlm"].mean() > top["lm"].mean() + 0.1)

    print("per-task summary:")
    for tname in TASKS:
        print(f"  {tname:<16} gap-large@>=2rungs={per_task_ok[tname]!s:<5}  "
              f"LM-catches-up@top({top_rung})={lm_catches_up_top[tname]!s:<5}  "
              f"mem-aug-closes={memaug_closes[tname]}")
    print()

    all_tasks_pass = all(per_task_ok.values())
    any_collapse = any(lm_catches_up_top.values())
    all_memaug = all(memaug_closes.values())

    if all_tasks_pass and not any_collapse and all_memaug:
        verdict_line("H_985", "PASS",
                     f"WM>LM separator is SCALE+DIVERSITY-ROBUST: gap large (d>0.8) at >=2 rungs "
                     f"on ALL {len(TASKS)} task families, LM does NOT catch up at the top rung "
                     f"(dim={top_rung}), and the mem-aug control closes it on every task -> "
                     f"H_970 GENERALIZES beyond the single delayed-cue toy (toy ladder; "
                     f"production OPEN, a_scale_honest_scope).")
    elif any_collapse:
        collapsed = [t for t in TASKS if lm_catches_up_top[t]]
        verdict_line("H_985", "FAIL",
                     f"gap COLLAPSES at the top rung (dim={top_rung}) on {collapsed} — the "
                     f"matched LM catches up at larger capacity -> H_970 was capacity-limited "
                     f"(closed-negative, a_paper_negative_ok).")
    elif not all_tasks_pass:
        failed = [t for t in TASKS if not per_task_ok[t]]
        verdict_line("H_985", "FAIL",
                     f"separator is TASK-SPECIFIC — no large WM>LM gap on {failed}; holds only on "
                     f"a subset -> H_970 was a task artifact, not a general WM>LM property "
                     f"(closed-negative, a_paper_negative_ok).")
    else:
        verdict_line("H_985", "INCOMPLETE",
                     "mem-aug control did not close the gap on some task (task may not be "
                     "purely persistent-state-bound); toy-only C3.")


if __name__ == "__main__":
    main()
