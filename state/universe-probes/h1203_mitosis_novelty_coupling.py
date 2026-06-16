"""
H_1203 — MITOSIS NOVELTY-COUPLING (MITOSIS-ENGINE).

Does the NOVELTY of a real text/chat trajectory DRIVE cell division in the live
engine substrate (CORE/engine_cli.hexa VAdaptField, H_1199), or is mitosis
substrate-NEUTRAL the way the clm_v2 "V14 mirror VIOLATED" finding showed
(random_init produced the SAME division trajectory => division carries no info)?

We build THREE byte-feature streams over the REAL corpus and run each through a
numpy MIRROR of CORE/engine_cli.hexa vadapt_field_step (mechanism-identical:
nearest-by-L2, recon-err = L2 to nearest, recon-err>SPLIT_THRESH=0.30 spawns a
cell seeded AT the sample under mitosis ON, else LR=0.20 online winner pull —
exactly vadapt_field_step). H_1199 is the precedent that this numpy ref reproduces
the live .hexa engine byte-for-byte on the same input.

  NOVEL    = high topic-turnover: each tick window drawn from a fresh SCATTERED
             corpus offset (frequent regime switches => genuinely novel stream).
  REPEAT   = low novelty: the SAME short corpus block repeated (one regime revisited).
  SHUFFLED = the NOVEL ticks with TIME ORDER permuted (V14 control — same feature
             multiset, order destroyed).

p7 metric = cell_growth (cells born) + L2 recon-err, NOT perplexity. p8: inference
== growth (the split tick is the growth gate). gradient-free. $0 local CPU.
FROZEN falsifiers in .verdicts/1203_mitosis_novelty_coupling/H_1203_FREEZE.txt:
  F1  NOVEL/REPEAT   cell_growth >= 1.5  (novelty drives division)
  F2  NOVEL/SHUFFLED cell_growth >= 1.5  (DEFEAT V14: division needs input order)

HONESTY (a_scale_honest_scope): ONE corpus, toy scale, 3 seeds, scale UNVERIFIED.
"""
import os, sys
import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
import h1163_tick_decode_metric as H   # _byte_feature / DIM / WARMUP / T / WIN_BYTES / STRIDE / SEEDS

DIM = H.DIM                    # 8
WIN_BYTES = H.WIN_BYTES        # 48
STRIDE = H.STRIDE              # 24
WARMUP = H.WARMUP              # 250
T = H.T                        # 2400
SEEDS = list(H.SEEDS[:3])      # 900, 901, 902
SPLIT_THRESH = 0.30            # == CORE/engine_cli.hexa vadapt_field_step
LR = 0.20                      # == the live engine
MAX_CELLS = 2048               # cap = N_MIGRATE (lets us SEE growth approach it)
SAMPLE_EVERY = 200

CORPUS = H.CORPUS


def _load_corpus():
    data = open(CORPUS, "rb").read()
    return data


# ── three byte-feature streams (NOVEL / REPEAT / SHUFFLED) over REAL bytes ──────
def make_novel_stream(seed):
    """High topic-turnover: every tick window drawn from a FRESH scattered corpus
    offset => the byte-feature regime jumps constantly (a genuinely novel stream)."""
    data = _load_corpus()
    rng = np.random.default_rng(seed)
    need = WARMUP + T + 1
    hi = max(1, len(data) - WIN_BYTES - 1)
    offs = rng.integers(0, hi, size=need)        # scattered, independent offsets
    X = np.empty((need, DIM))
    for i in range(need):
        p = int(offs[i])
        X[i] = H._byte_feature(data[p:p + WIN_BYTES])
    return X


def make_repeat_stream(seed):
    """Low novelty: the SAME short corpus block, its windows cycled over and over
    (one regime revisited; almost no new structure after warmup)."""
    data = _load_corpus()
    rng = np.random.default_rng(seed)
    need = WARMUP + T + 1
    # one short block of ~12 consecutive windows, repeated cyclically
    n_block = 12
    block_span = WIN_BYTES + STRIDE * n_block
    start = int(rng.integers(0, max(1, len(data) - block_span - 1)))
    block = []
    for k in range(n_block):
        p = start + k * STRIDE
        block.append(H._byte_feature(data[p:p + WIN_BYTES]))
    block = np.array(block)
    X = np.empty((need, DIM))
    for i in range(need):
        X[i] = block[i % n_block]
    return X


def make_shuffled_stream(seed):
    """V14 control: the NOVEL ticks with their TIME ORDER permuted (same multiset
    of feature vectors, order destroyed)."""
    X = make_novel_stream(seed)
    rng = np.random.default_rng(seed + 10_000)   # disjoint stream from offsets
    perm = rng.permutation(X.shape[0])
    return X[perm]


# ── numpy MIRROR of vadapt_field_step (CORE/engine_cli.hexa), mechanism-identical ─
def run_vadapt(X, mitosis_on, max_cells):
    """EXACTLY vadapt_field_step: nearest by L2, recon-err = L2 to nearest, split
    when recon-err>SPLIT_THRESH & n_cells<cap (cell seeded AT the sample), else
    LR winner pull. Returns (sampled rows, final n_cells, late recon-err mean)."""
    Xs = X[WARMUP:WARMUP + T]
    protos = [Xs[0].astype(float).copy()]        # vadapt_field_new: one seed cell
    rows = []
    win_err, win_cnt = 0.0, 0
    for i in range(len(Xs)):
        x = Xs[i].astype(float)
        d = np.array([np.linalg.norm(p - x) for p in protos])
        j = int(d.argmin())
        err = float(d[j])
        win_err += err; win_cnt += 1
        if mitosis_on and err > SPLIT_THRESH and len(protos) < max_cells:
            protos.append(x.copy())              # new cell AT the novel sample
        else:
            protos[j] += LR * (x - protos[j])    # homeostatic winner pull
        if (i + 1) % SAMPLE_EVERY == 0:
            rows.append((i + 1, len(protos), win_err / max(win_cnt, 1)))
            win_err, win_cnt = 0.0, 0
    q = max(1, len(rows) // 4)
    late_err = float(np.mean([r[2] for r in rows[-q:]])) if rows else 0.0
    return rows, len(protos), late_err


def main():
    print(f"=== H_1203 mitosis novelty-coupling (local CPU, $0) — DIM={DIM} "
          f"WARMUP={WARMUP} T={T} SEEDS={SEEDS} SPLIT_THRESH={SPLIT_THRESH} LR={LR} ===", flush=True)
    print(f"corpus = {os.path.relpath(CORPUS)}  (numpy mirror == engine_cli.hexa vadapt_field_step)\n", flush=True)

    arms = {"NOVEL": make_novel_stream, "REPEAT": make_repeat_stream, "SHUFFLED": make_shuffled_stream}

    # export the scored span of each arm so the LIVE .hexa VAdaptField can be run
    # as a cross-check guard (c2) — one tick/line, DIM space-sep full-repr floats.
    if os.environ.get("H1203_EXPORT", "1") == "1":
        for s in SEEDS:
            for a, mk in arms.items():
                Xs = mk(s)[WARMUP:WARMUP + T]
                with open(f"/tmp/h1203_{a.lower()}_seed{s}.txt", "w") as f:
                    for t in range(Xs.shape[0]):
                        f.write(" ".join(repr(float(v)) for v in Xs[t]) + "\n")

    # growth_on[arm] = list of per-seed cell_growth (final-1); also OFF control + recon-err
    growth_on = {a: [] for a in arms}
    growth_off = {a: [] for a in arms}
    err_on = {a: [] for a in arms}

    for s in SEEDS:
        print(f"--- seed {s} ---", flush=True)
        for a, mk in arms.items():
            X = mk(s)
            on_rows, on_final, on_late = run_vadapt(X, True, MAX_CELLS)
            off_rows, off_final, off_late = run_vadapt(X, False, MAX_CELLS)
            g_on = on_final - 1
            g_off = off_final - 1
            growth_on[a].append(g_on)
            growth_off[a].append(g_off)
            err_on[a].append(on_late)
            print(f"  {a:8s}: cell_growth ON={g_on:4d} (OFF={g_off})  "
                  f"final_cells={on_final}  late recon-err ON={on_late:.4f} OFF={off_late:.4f}", flush=True)
        print(flush=True)

    # 3-seed means
    m = {a: float(np.mean(growth_on[a])) for a in arms}
    me = {a: float(np.mean(err_on[a])) for a in arms}
    print("=== 3-seed MEAN cell_growth (mitosis ON) ===", flush=True)
    for a in arms:
        print(f"  {a:8s}: cell_growth = {m[a]:.2f}   (per-seed {growth_on[a]})   "
              f"late recon-err = {me[a]:.4f}", flush=True)

    f1 = m["NOVEL"] / max(m["REPEAT"], 1e-9)     # novelty drives division
    f2 = m["NOVEL"] / max(m["SHUFFLED"], 1e-9)   # DEFEAT V14: needs input order
    print(f"\n=== FROZEN FALSIFIERS ===", flush=True)
    print(f"  F1  NOVEL/REPEAT   = {f1:.3f}   (bar >= 1.5)   -> {'PASS' if f1 >= 1.5 else 'FAIL'}", flush=True)
    print(f"  F2  NOVEL/SHUFFLED = {f2:.3f}   (bar >= 1.5)   -> {'PASS' if f2 >= 1.5 else 'FAIL'}", flush=True)

    f1p = f1 >= 1.5
    f2p = f2 >= 1.5
    if f1p and f2p:
        tier = "GREEN  — mitosis couples to trajectory novelty; V14 DEFEATED."
    elif f1p and not f2p:
        tier = ("PARTIAL — grows on novelty (F1) but order-invariant (F2 FAIL): growth "
                "tracks the feature MARGINAL not the trajectory; V14 not fully defeated.")
    else:
        tier = ("RED — novelty does not drive division (F1 FAIL); substrate-neutral, "
                "V14 reconfirmed (closed-negative, a_paper_negative_ok).")
    print(f"\nTIER: {tier}", flush=True)
    print("\nHONESTY: ONE corpus (clm_mid_5lang_c4), toy scale, 3 seeds, gradient-free, "
          "numpy mirror mechanism-identical to engine_cli.hexa vadapt_field_step (H_1199 "
          "precedent). Scale transfer UNVERIFIED.", flush=True)
    print("[done]", flush=True)


if __name__ == "__main__":
    main()
