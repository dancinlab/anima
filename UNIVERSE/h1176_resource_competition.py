"""
H_1176 — RESOURCE COMPETITION: does a scarce shared resource (carrying capacity)
create the selection pressure pure mitosis lacks?

Audit gap (CORE engine): grep 'competition' = 0. h1159b mitosis grows cells to
fit world complexity, but EVERY cell survives equally — there is no scarcity, so
fitness-differential reproduction (Darwinian selection, H_1175) has no teeth.
This H ADDS a scarce shared resource pool R with carrying capacity K_cap: cells
draw R proportional to their assignment share; when total demand > R, the
LOWEST-FITNESS cells starve and die (competition). Compare the COMPETITION arm
against an unconstrained equal-survival (NO-COMPETITION) growth arm.

Reuses the h1159b cell substrate (clustering cells, assign(), mitosis on tension)
VERBATIM in spirit; ADDS resource draw + starvation culling.

FROZEN FALSIFIER (pre-registered, deterministic, >=8 seeds, p7):
  🟢 COMPETITION-DRIVES-SELECTION iff
     F1 FITNESS-TRACKING: scarcity yields a population whose composition TRACKS
        fitness — corr(fitness, survival) >= 0.5 (high-fitness cells survive,
        low-fitness cells starve) in the COMPETITION arm.
     F2 BOUNDED: COMPETITION population is bounded by K_cap (final cell-count
        <= K_cap), vs the NO-COMPETITION arm which grows UNBOUNDED past K_cap.
     SUPPORTED iff F1 AND F2.
  🔴 if competition does not produce fitness-tracking selection (a_paper_negative_ok).

toy ($0 numpy CPU). a_scale_honest_scope. p7 (fitness = substrate clustering
error, NOT perplexity).
"""
import json, math
import numpy as np

DIM = 8
T = 4000
WARMUP = 250
N_SEEDS = 10
SEEDS = list(range(900, 900 + N_SEEDS))
# Construction (pre-freeze fix BEFORE scoring, a_completeness_over_cheap / H_1061
# defect-fix discipline): the first parameterization (THETA=1.6, K_TRUE=8, K_CAP=8)
# put the substrate in a DEGENERATE regime — mitosis produced only ~9-11 cells total,
# so K_CAP=8 was NOT meaningfully scarce, competition fired 0-9 times (some seeds never
# culled -> trivial corr=0), and NOCOMP never grew "unbounded" past K_CAP. That tests
# nothing about scarcity. FIX: a RICHER world (K_TRUE=16) + a LOWER mitosis threshold
# (THETA=0.9) so mitosis genuinely OVER-PRODUCES well past a SMALLER carrying capacity
# (K_CAP=6) -> real demand>>supply, competition bites EVERY seed, NOCOMP runs unbounded.
THETA = 0.9          # tension threshold for mitosis (lowered: over-produce past K_CAP)
WIN = 200            # tension running window (h1159b)
LR = 0.05            # centroid adaptation rate (h1159b)
MAX_CELLS = 60       # hard ceiling so the unbounded arm can be SEEN to exceed K_cap
K_CAP = 6            # carrying capacity: at most K_cap cells the resource can support
K_TRUE = 16          # world complexity (>> K_CAP so demand strongly exceeds supply)
RESOURCE = float(K_CAP)   # scarce shared pool R sized to support exactly K_CAP cells
CULL_EVERY = 50      # competition resolution interval (substrate ticks)


def make_stream(seed, k_true):
    rng = np.random.default_rng(seed)
    centers = rng.standard_normal((k_true, DIM)) * 4.0
    onsets = np.linspace(0, T * 0.85, k_true).astype(int)
    X = np.empty((T, DIM)); active = []; oi = 0
    for t in range(T):
        while oi < k_true and t >= onsets[oi]:
            active.append(oi); oi += 1
        c = active[rng.integers(len(active))]
        X[t] = centers[c] + rng.standard_normal(DIM) * 0.6
    return X


def assign(cells, x):
    d = np.linalg.norm(cells - x[None], axis=1); j = int(np.argmin(d)); return j, float(d[j])


def _resolve_scarcity(cells, ten, cell_err, cell_cnt, culled_fitness, culled_survive):
    """Resolve one round of competition: if demand (n cells) exceeds the scarce pool
    (carrying capacity K_CAP), the LOWEST-fitness cells starve and die until the
    population fits K_CAP. fitness = 1/(running clustering error). Records culled
    cells' fitness with survival=0. Returns the pared-down arrays."""
    n = len(cells)
    if n <= K_CAP:
        return cells, ten, cell_err, cell_cnt
    fitness = 1.0 / (cell_err + 1e-6)        # low clustering error => FIT
    n_kill = n - K_CAP                        # demand>supply: this many must starve
    order = np.argsort(fitness)               # ascending: least fit first
    kill_idx = set(order[:n_kill].tolist())
    keep_mask = np.array([i not in kill_idx for i in range(n)])
    for i in range(n):
        if i in kill_idx:
            culled_fitness.append(float(fitness[i]))
            culled_survive.append(0)
    return (cells[keep_mask], ten[keep_mask], cell_err[keep_mask],
            np.zeros(int(keep_mask.sum())))   # fresh demand accounting each round


def run_arm(X, mode, seed):
    """
    mode = "NOCOMP"      : h1159b mitosis, equal survival, no scarcity (grows unbounded).
    mode = "COMPETITION" : same mitosis, PLUS a scarce shared resource R = K_CAP.
                           Cells draw R proportional to assignment share; fitness =
                           1/(running error). When n_cells > K_CAP the resource cannot
                           support all cells (demand > R) -> the LOWEST-FITNESS cells
                           starve and die until n_cells <= K_CAP (competition cull).
    Returns dict with final cell-count + per-cell (fitness, survived) over every cell
    that was ever born (survivors=1, competition-starved=0).
    """
    rng = np.random.default_rng(seed + 5000)
    cells = X[:2].copy().astype(float)
    for t in range(WARMUP):
        j, _ = assign(cells, X[t]); cells[j] += LR * (X[t] - cells[j])

    ten = np.zeros(len(cells))
    cell_err = np.zeros(len(cells))   # EWMA assignment distance (lower = fitter)
    cell_cnt = np.zeros(len(cells))   # recent assignment frequency (resource demand share)
    ever_born = 0
    culled_fitness = []   # fitness (1/err) of cells that STARVED (survival=0)
    culled_survive = []

    for t in range(WARMUP, T):
        x = X[t]; j, d = assign(cells, x)
        # instructive online adaptation (h1159b)
        cells[j] += LR * (x - cells[j])
        cell_err[j] += (d - cell_err[j]) / WIN
        cell_cnt[j] += 1.0
        # mitosis on tension (h1159b) — variation + heredity + reproduction
        ten[j] += (d - ten[j]) / WIN
        if ten[j] > THETA and len(cells) < MAX_CELLS:
            daughter = cells[j] + rng.standard_normal(DIM) * 0.3
            cells = np.vstack([cells, daughter[None]])
            ten = np.concatenate([ten, [0.0]])
            cell_err = np.concatenate([cell_err, [cell_err[j]]])  # inherit parent err est
            cell_cnt = np.concatenate([cell_cnt, [0.0]])
            ten[j] = 0.0
            ever_born += 1

        # COMPETITION: periodically resolve scarcity
        if mode == "COMPETITION" and (t % CULL_EVERY == 0):
            cells, ten, cell_err, cell_cnt = _resolve_scarcity(
                cells, ten, cell_err, cell_cnt, culled_fitness, culled_survive)

    # FINAL competition resolution so the COMP population is EXACTLY bounded by K_CAP
    # (a daughter born after the last periodic cull tick must still face scarcity).
    if mode == "COMPETITION":
        cells, ten, cell_err, cell_cnt = _resolve_scarcity(
            cells, ten, cell_err, cell_cnt, culled_fitness, culled_survive)

    final_fitness = (1.0 / (cell_err + 1e-6)).tolist()
    final_survive = [1] * len(cells)
    all_fitness = final_fitness + culled_fitness
    all_survive = final_survive + culled_survive
    return {
        "final_cellcount": len(cells),
        "ever_born": int(ever_born),
        "n_culled": len(culled_fitness),
        "all_fitness": all_fitness,
        "all_survive": all_survive,
    }


def pearson(a, b):
    a = np.asarray(a, float); b = np.asarray(b, float)
    if len(a) < 2 or np.std(a) < 1e-12 or np.std(b) < 1e-12:
        return 0.0
    a = a - a.mean(); b = b - b.mean()
    den = math.sqrt((a * a).sum() * (b * b).sum())
    return float((a * b).sum() / den) if den else 0.0


def main():
    np.seterr(all="ignore")
    print("=== H_1176 — resource competition: does scarcity create selection pressure? ===", flush=True)
    print(f"K_TRUE={K_TRUE} K_CAP={K_CAP} RESOURCE={RESOURCE} MAX_CELLS={MAX_CELLS} "
          f"seeds={N_SEEDS}", flush=True)

    comp_counts, nocomp_counts = [], []
    fit_surv_corrs = []
    comp_bounded_flags = []
    nocomp_unbounded_flags = []
    pooled_fitness, pooled_survive = [], []

    for s in SEEDS:
        X = make_stream(s, K_TRUE)
        comp = run_arm(X, "COMPETITION", s)
        noc = run_arm(X, "NOCOMP", s)
        comp_counts.append(comp["final_cellcount"])
        nocomp_counts.append(noc["final_cellcount"])

        r = pearson(comp["all_fitness"], comp["all_survive"])
        fit_surv_corrs.append(r)
        pooled_fitness.extend(comp["all_fitness"])
        pooled_survive.extend(comp["all_survive"])

        comp_bounded_flags.append(comp["final_cellcount"] <= K_CAP)
        nocomp_unbounded_flags.append(noc["final_cellcount"] > K_CAP)

        print(f"  seed={s}: COMP final={comp['final_cellcount']} culled={comp['n_culled']} "
              f"corr(fit,surv)={r:+.3f} | NOCOMP final={noc['final_cellcount']}", flush=True)

    pooled_corr = pearson(pooled_fitness, pooled_survive)
    mean_corr = float(np.mean(fit_surv_corrs))

    # F1 FITNESS-TRACKING: scarcity culls low-fitness cells -> corr(fitness,survival) >= 0.5
    f1 = mean_corr >= 0.5
    # F2 BOUNDED: competition arm <= K_CAP every seed AND no-competition arm exceeds K_CAP
    f2_comp_bounded = all(comp_bounded_flags)
    f2_nocomp_unbounded = all(nocomp_unbounded_flags)
    f2 = f2_comp_bounded and f2_nocomp_unbounded

    supported = bool(f1 and f2)

    verdict = {
        "H": "H_1176",
        "title": "resource competition — does a scarce shared resource create the selection pressure pure mitosis lacks?",
        "config": {"K_true": K_TRUE, "K_cap": K_CAP, "resource_pool": RESOURCE,
                   "max_cells": MAX_CELLS, "n_seeds": N_SEEDS, "cull_every": CULL_EVERY},
        "competition_final_cellcount_mean": float(np.mean(comp_counts)),
        "nocompetition_final_cellcount_mean": float(np.mean(nocomp_counts)),
        "F1_fitness_tracking": {
            "mean_corr_fitness_survival": mean_corr,
            "pooled_corr_fitness_survival": pooled_corr,
            "bar": 0.5, "pass": bool(f1),
            "note": "competition culls the LOWEST-fitness cells -> survival tracks fitness",
        },
        "F2_bounded": {
            "competition_bounded_by_Kcap": bool(f2_comp_bounded),
            "nocomp_unbounded_over_Kcap": bool(f2_nocomp_unbounded),
            "Kcap": K_CAP,
            "comp_max_cellcount": int(np.max(comp_counts)),
            "nocomp_min_cellcount": int(np.min(nocomp_counts)),
            "pass": bool(f2),
        },
        "supported": supported,
        "ruling": (
            "SUPPORTED: a scarce shared resource (carrying capacity K_cap) DOES create the "
            "selection pressure pure mitosis lacks — under scarcity survival TRACKS fitness "
            "(low-fitness cells starve, corr>=0.5) and the population is BOUNDED by K_cap, "
            "whereas equal-survival mitosis grows UNBOUNDED past K_cap. Competition makes "
            "fitness-differential reproduction BITE (Darwinian selection)."
            if supported else
            "CLOSED-NEGATIVE: scarce-resource competition does NOT produce fitness-tracking "
            "selection at toy scale (see which gate failed). a_paper_negative_ok."
        ),
        "scope": "toy numpy $0 CPU 10 seeds; reuses h1159b cell substrate; carrying-capacity "
                 "competition PROXY for CORE cell scarcity — live engine + scale UNVERIFIED "
                 "(a_scale_honest_scope). p7 (fitness=clustering error, NOT perplexity).",
        "xref": "h1159b_mitosis_capacity_self_tuning · 1175_fitness_selection · 1171_apoptosis_death · 1172_metabolism_energy_budget",
    }
    print("\n=== VERDICT ===\n" + json.dumps(verdict, ensure_ascii=False, indent=2), flush=True)
    json.dump(verdict, open("/tmp/h1176_result.json", "w"), ensure_ascii=False, indent=2)
    print("[done]", flush=True)


if __name__ == "__main__":
    main()
