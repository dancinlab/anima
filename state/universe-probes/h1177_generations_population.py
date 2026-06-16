"""
H_1177 — GENERATIONS / population evolution. Completes the Darwinian set
(selection #1175, competition #1176, generations #1177).

Audit gap: anima mitosis grows ONE organism's cell-count (H_1159/H_1159b); there
is no POPULATION reproducing across GENERATIONS with a fitness-differential. True
Darwinian evolution needs heredity + variation + selection ACROSS generations,
not just one organism developing within its lifetime.

This harness builds a POPULATION of N agents — each an h1159b-style cell-cluster
clusterer (reuse the exact assign/run_arm mechanics of
UNIVERSE/h1159b_mitosis_capacity_self_tuning.py). Per generation:
  - eval fitness  = inverse running quantization error on the (fixed) task stream
  - selection     = keep top-half by fitness (truncation selection)
  - heredity      = survivors copied into the next generation
  - variation     = offspring = mutated copy of a survivor (Gaussian jitter on the
                    HERITABLE trait — the cluster-centroid init seeds)
Repeat for G generations. Compare the evolved population's best/mean fitness to a
SINGLE agent that only GROWS within one lifetime (H_1159b MITOSIS arm, same total
compute budget, NO generations / heredity / selection).

FROZEN FALSIFIER (pre-reg, deterministic, >=8 seeds, p7):
  F1 RISE:  population mean-fitness INCREASES across G generations
            (Spearman(generation_index, mean_fitness) >= +0.5, per-seed median).
  F2 BEAT:  the evolved population (final-gen best agent) BEATS the single-growing
            organism on the SAME task, Cohen's d >= 0.8 (paired across seeds).
  SUPPORTED = F1 AND F2  -> 🟢 POPULATION-EVOLVES (cross-generational Darwinian
            improvement adds adaptive power single-lifetime growth lacks).
  else -> 🔴 CLOSED-NEGATIVE: generations add nothing over single-organism growth
            at toy scale (a_paper_negative_ok).

fitness = substrate quantization error (NOT perplexity/LLM-judge, p7).
toy $0 numpy CPU, >=8 seeds, deterministic. live engine + scale UNVERIFIED
(a_scale_honest_scope). xref h1175_fitness_selection, h1159b, p8.
"""
import json, math
import numpy as np

# --- world / task (h1159b-style multi-cluster drift stream) ---
DIM = 8
T = 1200            # stream length used per fitness evaluation
WARMUP = 150
K_TRUE = 6          # world complexity (#clusters the agents must quantize)

# --- population evolution ---
N_AGENTS = 12       # population size
G_GENS = 10         # number of generations
N_SEEDS = 8
SEEDS = list(range(900, 900 + N_SEEDS))

# --- agent (cell-cluster) mechanics, identical spirit to h1159b ---
LR = 0.05
N_CELLS = K_TRUE    # fixed-capacity clusterer (population evolves the SEEDS, not capacity)
MUT_SCALE = 0.8     # heritable-trait mutation jitter
INIT_SPREAD = 4.0   # offspring/genome centroid-seed spread (matches center scale)


def make_stream(seed, k_true=K_TRUE):
    """h1159b drift stream: k_true Gaussian clusters appearing spread over time."""
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


def lifetime_error(genome, X):
    """Run one agent's LIFETIME on the task: online-adapt its cells from its genome
    (heritable centroid-seeds), return final-window quantization error = -fitness.
    Same online cell-update loop as h1159b's MITOSIS arm (instructive growth)."""
    cells = genome.copy().astype(float)
    for t in range(WARMUP):
        j, _ = assign(cells, X[t]); cells[j] += LR * (X[t] - cells[j])
    errs = np.empty(T - WARMUP)
    for i, t in enumerate(range(WARMUP, T)):
        x = X[t]; j, d = assign(cells, x); errs[i] = d
        cells[j] += LR * (x - cells[j])
    return float(errs[-WARMUP:].mean())


def fitness(genome, X):
    return 1.0 / (lifetime_error(genome, X) + 1e-9)


def run_population(X, seed):
    """Evolve a population of N_AGENTS genomes over G_GENS generations:
    heredity (copy survivors) + variation (mutate offspring) + selection (truncation).
    Returns (mean_fitness_per_gen, best_final_error)."""
    rng = np.random.default_rng(seed + 7000)
    # initial population: random centroid-seed genomes (the heritable trait)
    pop = [rng.standard_normal((N_CELLS, DIM)) * INIT_SPREAD for _ in range(N_AGENTS)]
    mean_fit_per_gen = []
    best_genome = None
    for g in range(G_GENS):
        fits = np.array([fitness(gm, X) for gm in pop])
        mean_fit_per_gen.append(float(fits.mean()))
        order = np.argsort(-fits)                      # best first
        n_keep = N_AGENTS // 2
        survivors = [pop[i].copy() for i in order[:n_keep]]
        best_genome = pop[int(order[0])].copy()
        # next generation: survivors (heredity) + mutated offspring (variation)
        nxt = [s.copy() for s in survivors]
        while len(nxt) < N_AGENTS:
            parent = survivors[rng.integers(n_keep)]
            child = parent + rng.standard_normal((N_CELLS, DIM)) * MUT_SCALE
            nxt.append(child)
        pop = nxt
    # evolved performance = best agent of the final generation, evaluated on the task
    final_fits = np.array([fitness(gm, X) for gm in pop])
    best_final = pop[int(np.argmax(final_fits))]
    evolved_err = lifetime_error(best_final, X)
    return mean_fit_per_gen, evolved_err


def run_single_growing_organism(X, seed):
    """Baseline: ONE agent, same total compute budget as the population evolution
    (N_AGENTS*G_GENS lifetimes), that only GROWS within a single lifetime — repeated
    online passes, NO heredity / variation / selection across generations.
    This is the h1159b single-organism-growth control (instructive adaptation only)."""
    rng = np.random.default_rng(seed + 9000)
    budget = N_AGENTS * G_GENS          # equal #lifetimes of compute
    cells = rng.standard_normal((N_CELLS, DIM)) * INIT_SPREAD
    # the organism keeps growing/refining across repeated passes of its single life
    for _ in range(budget):
        for t in range(min(WARMUP, T)):
            j, _ = assign(cells, X[t]); cells[j] += LR * (X[t] - cells[j])
        for t in range(WARMUP, T):
            j, d = assign(cells, X[t]); cells[j] += LR * (X[t] - cells[j])
    # final error of the single grown organism
    errs = np.empty(T - WARMUP)
    for i, t in enumerate(range(WARMUP, T)):
        _, d = assign(cells, X[t]); errs[i] = d
    return float(errs[-WARMUP:].mean())


def cohen_d(x, y):
    sp = math.sqrt((np.std(x) ** 2 + np.std(y) ** 2) / 2.0) or 1e-9
    return (np.mean(x) - np.mean(y)) / sp


def spearman(a, b):
    a = np.asarray(a, float); b = np.asarray(b, float)
    ra = np.argsort(np.argsort(a)).astype(float); rb = np.argsort(np.argsort(b)).astype(float)
    ra -= ra.mean(); rb -= rb.mean(); den = math.sqrt((ra * ra).sum() * (rb * rb).sum())
    return float((ra * rb).sum() / den) if den else 0.0


def main():
    np.seterr(all="ignore")
    print("=== H_1177 — generations/population evolution vs single growing organism ===", flush=True)
    print(f"N_AGENTS={N_AGENTS} G_GENS={G_GENS} N_CELLS={N_CELLS} K_TRUE={K_TRUE} seeds={N_SEEDS}", flush=True)
    gen_idx = list(range(G_GENS))
    rho_per_seed = []
    evolved_fit, single_fit = [], []   # fitness = 1/err (higher = better)
    rows = []
    for s in SEEDS:
        X = make_stream(s)
        mean_fit_per_gen, evolved_err = run_population(X, s)
        rho = spearman(gen_idx, mean_fit_per_gen)
        rho_per_seed.append(rho)
        single_err = run_single_growing_organism(X, s)
        ev_f = 1.0 / (evolved_err + 1e-9)
        sg_f = 1.0 / (single_err + 1e-9)
        evolved_fit.append(ev_f); single_fit.append(sg_f)
        rows.append({"seed": s, "rho_gen_vs_meanfit": rho,
                     "gen0_meanfit": mean_fit_per_gen[0], "genLast_meanfit": mean_fit_per_gen[-1],
                     "evolved_err": evolved_err, "single_err": single_err,
                     "evolved_fit": ev_f, "single_fit": sg_f})
        print(f"  seed={s}: rho(gen,meanfit)={rho:+.3f} meanfit {mean_fit_per_gen[0]:.4f}->{mean_fit_per_gen[-1]:.4f} "
              f"| evolved_err={evolved_err:.4f} single_err={single_err:.4f}", flush=True)

    median_rho = float(np.median(rho_per_seed))
    f1 = median_rho >= 0.5
    d_beat = cohen_d(np.array(evolved_fit), np.array(single_fit))   # >0 => evolved fitter
    f2 = d_beat >= 0.8
    supported = bool(f1 and f2)

    verdict = {
        "H": "H_1177",
        "title": "generations/population evolution (heredity+variation+selection) vs single growing organism",
        "config": {"N_AGENTS": N_AGENTS, "G_GENS": G_GENS, "N_CELLS": N_CELLS,
                   "K_TRUE": K_TRUE, "DIM": DIM, "T": T, "WARMUP": WARMUP,
                   "MUT_SCALE": MUT_SCALE, "N_SEEDS": N_SEEDS, "SEEDS": SEEDS,
                   "single_budget_lifetimes": N_AGENTS * G_GENS},
        "per_seed": rows,
        "F1_rise_across_generations": {
            "spearman_gen_vs_meanfit_median": median_rho,
            "per_seed_rho": rho_per_seed, "bar": 0.5, "pass": bool(f1)},
        "F2_beats_single_growing_organism": {
            "cohen_d_evolved_minus_single_fitness": float(d_beat),
            "mean_evolved_fit": float(np.mean(evolved_fit)),
            "mean_single_fit": float(np.mean(single_fit)),
            "bar": 0.8, "pass": bool(f2)},
        "supported": supported,
        "ruling": (
            "SUPPORTED 🟢 POPULATION-EVOLVES: a multi-generation population with heredity+variation+selection "
            "raises mean fitness across generations AND the evolved population beats a single-growing organism "
            "given equal compute (d>=0.8) — cross-generational Darwinian improvement adds adaptive power that "
            "single-lifetime growth (H_1159 instructive mitosis) lacks. Completes the Darwinian set with #1175/#1176."
            if supported else
            "CLOSED-NEGATIVE 🔴: generations add nothing over single-organism growth at toy scale "
            "(see F1/F2 for which gate failed) — at this scale instructive single-lifetime adaptation matches "
            "or exceeds cross-generational selection (a_paper_negative_ok)."),
        "scope": "toy numpy $0 CPU; fitness=quantization error not perplexity (p7); population layer on h1159b "
                 "cell-cluster; live CORE engine + scale UNVERIFIED (a_scale_honest_scope).",
        "xref": "1175_fitness_selection · 1176_resource_competition · 1159b_mitosis_capacity_self_tuning · p8",
    }
    print("\n=== VERDICT ===\n" + json.dumps(verdict, ensure_ascii=False, indent=2), flush=True)
    json.dump(verdict, open("/tmp/h1177_result.json", "w"), ensure_ascii=False, indent=2)
    print("[done]", flush=True)


if __name__ == "__main__":
    main()
