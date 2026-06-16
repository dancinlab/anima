"""
H_1175 — KEYSTONE Darwinian gap: does fitness-differential SELECTION (fit cells
divide MORE, unfit cells CULLED) produce evolution BEYOND instructive growth?

Audit gap (from .discoveries/1175_fitness_selection.tape):
  anima has VARIATION (daughter noise) + HEREDITY (inherit centroid) +
  REPRODUCTION (mitosis, H_1159/H_1159b) but NO SELECTION — every cell survives
  equally. Without fitness-differential survival there is no Darwinian evolution,
  only instructive / Lamarckian online adaptation (H_1159). This is THE keystone
  evolution gap.

Build on UNIVERSE/h1159b_mitosis_capacity_self_tuning.py:
  - same prototype/cell substrate (centroids, assign-to-nearest, online LR move)
  - FIXED-CAPACITY population of CAP cells (vs h1159b's growth-to-cap)
  - SELECTION arm: fitness = inverse running error; at each generation, fit cells
    REPRODUCE (a high-fitness parent spawns a noisy daughter) and the unfit cell
    is CULLED (apoptosis, ref 1171) so total cell-count stays = CAP. Selection
    operates on a POPULATION of cells competing for the fixed capacity.
  - INSTRUCTIVE arm (H_1159 control): SAME CAP cells, SAME online LR move, but NO
    differential reproduction/cull — every cell adapts equally, none replaced.
    This is instructive/Lamarckian growth-only.

The two arms are matched on capacity (CAP cells), online LR, stream, and seed —
the ONLY difference is the Darwinian selection operator (reproduce-fit / cull-unfit).

FROZEN FALSIFIER (pre-registered, deterministic, >=8 seeds), VERBATIM from tape:
  🟢 SELECTION-EVOLVES iff
     (A) the selection arm's POPULATION mean-fitness INCREASES over generations
         (fitness slope > 0, i.e. mean-fitness late-gens > early-gens), AND
     (B) selection BEATS instructive-growth on a held-out SHIFTED task (Cohen's
         d >= 0.8) — differential reproduction adds adaptive power instruction lacks.
  🔴 CLOSED-NEGATIVE if selection adds nothing over instructive online-adaptation
     at toy scale (a_paper_negative_ok).

p7: fitness = substrate clustering error (inverse), NOT perplexity.
toy ($0 numpy CPU). live engine + scale UNVERIFIED (a_scale_honest_scope).
"""
import json, math
import numpy as np

DIM = 8
N_SEEDS = 8
SEEDS = list(range(900, 900 + N_SEEDS))
CAP = 12                 # fixed population capacity (cells competing)
K_TRUE = 5               # true #clusters in the TRAIN world
LR = 0.05                # online centroid move rate (== h1159b)
GEN_LEN = 300            # stream steps per generation
N_GEN = 14               # generations of selection
FIT_WIN = 120            # running-error window for fitness
DAUGHTER_NOISE = 0.30    # variation injected on reproduction (== h1159b 0.3)
EARLY_GENS = 3           # "early" window for fitness-increase test
LATE_GENS = 3            # "late" window for fitness-increase test
HELDOUT_LEN = 600        # held-out shifted-task eval length


def make_centers(rng, k):
    return rng.standard_normal((k, DIM)) * 4.0


def stream_from_centers(rng, centers, n):
    """Sample n points from the given cluster centers (+ isotropic noise)."""
    k = centers.shape[0]
    X = np.empty((n, DIM))
    for t in range(n):
        c = rng.integers(k)
        X[t] = centers[c] + rng.standard_normal(DIM) * 0.6
    return X


def assign(cells, x):
    d = np.linalg.norm(cells - x[None], axis=1)
    j = int(np.argmin(d))
    return j, float(d[j])


def online_pass(cells, X, lr, per_cell_err=None, counts=None):
    """One streaming pass: assign->move; returns mean assignment error.
    If per_cell_err/counts given, accumulate per-cell running error (for fitness)."""
    errs = np.empty(len(X))
    for t in range(len(X)):
        x = X[t]
        j, d = assign(cells, x)
        errs[t] = d
        if per_cell_err is not None:
            per_cell_err[j] += d
            counts[j] += 1
        cells[j] += lr * (x - cells[j])
    return float(errs.mean())


def init_cells(rng, X0):
    """Seed CAP cells from the first points of the stream (matched both arms)."""
    cells = np.empty((CAP, DIM))
    for i in range(CAP):
        cells[i] = X0[i % len(X0)] + rng.standard_normal(DIM) * 0.1
    return cells


def run_selection_arm(seed):
    """SELECTION: per generation, measure per-cell fitness (inverse running err),
    reproduce the FITTEST cell (noisy daughter) into the slot of the UNFITTEST
    cell (cull). Population stays = CAP. Darwinian differential reproduction."""
    rng = np.random.default_rng(seed + 11000)
    centers = make_centers(rng, K_TRUE)
    X0 = stream_from_centers(rng, centers, CAP)
    cells = init_cells(rng, X0)
    gen_mean_fit = []
    for g in range(N_GEN):
        Xg = stream_from_centers(rng, centers, GEN_LEN)
        per_cell_err = np.zeros(CAP)
        counts = np.zeros(CAP)
        online_pass(cells, Xg, LR, per_cell_err, counts)
        # fitness = inverse running error (cells never assigned a point => neutral)
        mean_err = np.where(counts > 0, per_cell_err / np.maximum(counts, 1), np.nan)
        # population mean-fitness = 1/(1+err) over cells that did work
        active = ~np.isnan(mean_err)
        fitness = 1.0 / (1.0 + np.where(active, mean_err, 0.0))
        pop_fit = float(np.mean(fitness[active])) if active.any() else 0.0
        gen_mean_fit.append(pop_fit)
        # SELECTION operator: reproduce fittest, cull unfittest (differential reprod.)
        # idle cells (counts==0) are prime cull targets; among active, highest err.
        cull_score = np.where(counts > 0, mean_err, np.inf)  # idle => inf => culled
        worst = int(np.argmax(cull_score))
        best = int(np.argmin(np.where(counts > 0, mean_err, np.inf)))
        if active.any() and worst != best:
            daughter = cells[best] + rng.standard_normal(DIM) * DAUGHTER_NOISE
            cells[worst] = daughter  # cull worst, fill with fit parent's daughter
    return cells, gen_mean_fit, centers, rng


def run_instructive_arm(seed):
    """INSTRUCTIVE (H_1159 control): SAME CAP cells, SAME online LR move, SAME
    generations, but NO differential reproduction / cull. Every cell adapts
    equally (Lamarckian / instructive growth-only). Matched on everything but
    the selection operator."""
    rng = np.random.default_rng(seed + 11000)  # SAME seed-stream as selection arm
    centers = make_centers(rng, K_TRUE)
    X0 = stream_from_centers(rng, centers, CAP)
    cells = init_cells(rng, X0)
    gen_mean_fit = []
    for g in range(N_GEN):
        Xg = stream_from_centers(rng, centers, GEN_LEN)
        per_cell_err = np.zeros(CAP)
        counts = np.zeros(CAP)
        online_pass(cells, Xg, LR, per_cell_err, counts)
        mean_err = np.where(counts > 0, per_cell_err / np.maximum(counts, 1), np.nan)
        active = ~np.isnan(mean_err)
        fitness = 1.0 / (1.0 + np.where(active, mean_err, 0.0))
        pop_fit = float(np.mean(fitness[active])) if active.any() else 0.0
        gen_mean_fit.append(pop_fit)
        # NO selection: cells just keep adapting (instructive). nothing replaced.
    return cells, gen_mean_fit, centers, rng


def heldout_shifted_eval(cells, centers, rng):
    """Held-out SHIFTED task: the world's clusters SHIFT (novel center offsets +
    a new cluster). Freeze the evolved/adapted cells; measure mean assignment
    error on the shifted stream WITHOUT further adaptation. Lower err = better
    generalization of the population to a novel-but-related world."""
    shift = rng.standard_normal((centers.shape[0], DIM)) * 2.0
    shifted = centers + shift
    extra = rng.standard_normal((2, DIM)) * 4.0           # 2 genuinely-new clusters
    shifted = np.vstack([shifted, extra])
    Xh = stream_from_centers(rng, shifted, HELDOUT_LEN)
    frozen = cells.copy()
    errs = np.empty(HELDOUT_LEN)
    for t in range(HELDOUT_LEN):
        _, d = assign(frozen, Xh[t])
        errs[t] = d
    return float(errs.mean())


def cohen_d(x, y):
    x = np.asarray(x, float); y = np.asarray(y, float)
    sp = math.sqrt((np.std(x) ** 2 + np.std(y) ** 2) / 2.0) or 1e-9
    return float((np.mean(x) - np.mean(y)) / sp)


def main():
    np.seterr(all="ignore")
    print("=== H_1175 — fitness-differential SELECTION vs instructive growth (Darwinian gap, p8) ===", flush=True)

    sel_fit_traj = []          # per-seed selection-arm gen mean-fitness trajectory
    sel_heldout = []           # per-seed selection held-out shifted err (lower=better)
    ins_heldout = []           # per-seed instructive held-out shifted err
    sel_fit_increase = []      # per-seed (late-mean - early-mean) fitness

    for s in SEEDS:
        sel_cells, sel_traj, sel_centers, sel_rng = run_selection_arm(s)
        ins_cells, ins_traj, ins_centers, ins_rng = run_instructive_arm(s)
        # held-out shifted eval: use a FRESH deterministic rng per seed, SAME shift
        # for both arms (so the comparison is apples-to-apples).
        h_rng_sel = np.random.default_rng(s + 77000)
        h_rng_ins = np.random.default_rng(s + 77000)
        e_sel = heldout_shifted_eval(sel_cells, sel_centers, h_rng_sel)
        e_ins = heldout_shifted_eval(ins_cells, ins_centers, h_rng_ins)
        sel_heldout.append(e_sel); ins_heldout.append(e_ins)
        sel_fit_traj.append(sel_traj)
        early = float(np.mean(sel_traj[:EARLY_GENS]))
        late = float(np.mean(sel_traj[-LATE_GENS:]))
        sel_fit_increase.append(late - early)
        print(f"  seed={s}: sel_fit early={early:.4f} late={late:.4f} dFit={late-early:+.4f} | "
              f"heldout_err sel={e_sel:.3f} ins={e_ins:.3f}", flush=True)

    sel_heldout = np.array(sel_heldout); ins_heldout = np.array(ins_heldout)
    sel_fit_increase = np.array(sel_fit_increase)

    # (A) population mean-fitness INCREASES over generations:
    #     across seeds, late-window fitness > early-window fitness (mean dFit > 0
    #     AND a majority of seeds increase). Effect size of the increase reported.
    mean_dfit = float(np.mean(sel_fit_increase))
    frac_increase = float(np.mean(sel_fit_increase > 0))
    fitness_increases = bool(mean_dfit > 0 and frac_increase >= 0.5)

    # (B) selection BEATS instructive on held-out shifted task, d >= 0.8.
    #     lower err = better; advantage of selection = ins_err - sel_err (positive
    #     => selection generalizes better). Cohen's d on the paired arms.
    d_heldout = cohen_d(ins_heldout, sel_heldout)   # >0 => selection lower err = better
    beats_instructive = bool(d_heldout >= 0.8)

    supported = bool(fitness_increases and beats_instructive)

    verdict = {
        "H": "H_1175",
        "title": "fitness-differential SELECTION vs instructive growth — the keystone Darwinian gap (p8)",
        "config": {
            "DIM": DIM, "N_SEEDS": N_SEEDS, "CAP": CAP, "K_TRUE": K_TRUE, "LR": LR,
            "GEN_LEN": GEN_LEN, "N_GEN": N_GEN, "FIT_WIN": FIT_WIN,
            "DAUGHTER_NOISE": DAUGHTER_NOISE, "HELDOUT_LEN": HELDOUT_LEN,
            "EARLY_GENS": EARLY_GENS, "LATE_GENS": LATE_GENS,
        },
        "A_fitness_increases": {
            "mean_dFit_late_minus_early": mean_dfit,
            "frac_seeds_increasing": frac_increase,
            "bar": "mean_dFit>0 AND frac>=0.5",
            "pass": fitness_increases,
        },
        "B_beats_instructive_heldout_shifted": {
            "sel_heldout_err_mean": float(np.mean(sel_heldout)),
            "ins_heldout_err_mean": float(np.mean(ins_heldout)),
            "cohen_d_ins_minus_sel": d_heldout,
            "bar": 0.8,
            "pass": beats_instructive,
            "note": "lower held-out err = better; d>0 => selection generalizes better than instructive",
        },
        "supported": supported,
        "ruling": (
            "🟢 SELECTION-EVOLVES: fitness-differential reproduction (fit cells "
            "divide more, unfit culled) produces evolution BEYOND instructive "
            "growth — population mean-fitness increases over generations AND the "
            "selected population beats instructive online-adaptation on a held-out "
            "shifted task (d>=0.8). Darwinian selection adds adaptive power "
            "instruction alone lacks (the keystone evolution gap is REAL)."
            if supported else
            "🔴 CLOSED-NEGATIVE: fitness-differential selection adds NOTHING over "
            "instructive online-adaptation at toy scale — selection either does "
            "not raise population mean-fitness over generations OR fails to beat "
            "instructive growth on the held-out shifted task (d<0.8). At this "
            "scale instructive/Lamarckian adaptation (H_1159) captures the "
            "available adaptive gains; the Darwinian selection operator is not a "
            "distinct lever (a_paper_negative_ok)."
        ),
        "scope": "toy numpy $0 CPU 8 seeds, prototype-cell PROXY for CORE cell-division; "
                 "live engine + scale UNVERIFIED (a_scale_honest_scope). p7: fitness = "
                 "clustering error not perplexity.",
        "xref": "h1159_inference_time_mitosis_learning · h1159b_mitosis_capacity_self_tuning · "
                "1171_apoptosis_death · p8 · a_paper_negative_ok",
    }
    print("\n=== VERDICT ===\n" + json.dumps(verdict, ensure_ascii=False, indent=2), flush=True)
    json.dump(verdict, open("/tmp/h1175_result.json", "w"), ensure_ascii=False, indent=2)
    print("[done]", flush=True)


if __name__ == "__main__":
    main()
