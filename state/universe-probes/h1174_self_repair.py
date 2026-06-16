"""
H_1174 — SELF-REPAIR: does damage->REPAIR maintain function under sustained
perturbation BETTER than HOMEOSTASIS alone? (life-criterion #4: self-repair)

Audit gap (from .discoveries/1174_self_repair.tape): homeostasis (SOC, Psi=1/2,
H_931/H_1126) keeps the REGIME stable but does not REPAIR damaged COMPONENTS.
Life repairs damage (DNA repair, wound healing) — a mechanism DISTINCT from
homeostasis. Does an explicit repair rule beat the self-healing the homeostatic
online-update already provides?

REUSE h1159b cells (prototype/centroid stream-clustering, online LR update = the
HOMEOSTASIS regime). INJECT DAMAGE = each step perturb a fraction f of cell
centroids by a large gaussian kick (knock them off their manifold). REPAIR rule =
nudge the damaged cells back toward their RECENT assignment manifold (a running
mean of the points each cell has recently won), at rate REPAIR_LR.

  HOMEOSTASIS-ONLY arm: damage + the same h1159b online LR update on the WON cell
                        only (the regime's intrinsic self-healing), NO repair rule.
  REPAIR arm:           damage + the SAME online LR update + the repair rule that
                        actively pulls EVERY damaged cell back toward its manifold.

Both arms see the IDENTICAL damage schedule (same RNG draw per seed) so the only
difference is the repair mechanism.

FROZEN FALSIFIER (pre-registered, VERBATIM from the tape, deterministic, >=8 seeds):
  🟢 REPAIR-HELPS iff under SUSTAINED damage the repair arm holds LOWER error
     (Cohen's d >= 0.8, repair vs homeostasis-only) AND RECOVERS toward pre-damage
     error after a damage BURST.
  🔴 if repair ~= homeostasis (the regime self-heals already; repair is redundant).
  (a_paper_negative_ok)

Operationalization of the two clauses:
  CLAUSE-A (sustained, the d>=0.8 gate): over a SUSTAINED-damage window, mean
     assignment error repair vs homeostasis-only, Cohen's d across seeds >= 0.8
     (repair lower).
  CLAUSE-B (recovery, the burst gate): a single concentrated damage BURST is
     applied at t_burst (no sustained damage), then damage stops. RECOVERS =
     after the burst the repair arm's error returns to within RECOVER_TOL of its
     OWN pre-burst baseline within RECOVER_WIN steps, AND does so FASTER (lower
     post-burst error) than homeostasis-only (paired, across seeds).
  SUPPORTED = CLAUSE-A and CLAUSE-B.

toy ($0 numpy CPU, 12 seeds, deterministic). live engine + scale UNVERIFIED
(a_scale_honest_scope). p7 (error = real assignment distance, NOT perplexity).
"""
import json, math
import numpy as np

DIM = 8
T = 4000
WARMUP = 300
N_SEEDS = 12
SEEDS = list(range(800, 800 + N_SEEDS))
K_TRUE = 5
LR = 0.05                 # h1159b homeostatic online-update rate (the regime's self-heal)
MANI_WIN = 60.0           # running-mean window for each cell's recent assignment manifold
REPAIR_LR = 0.30          # rate the repair rule pulls a damaged cell back to its manifold

# --- damage ---
DAMAGE_FRAC = 0.30        # fraction of cells perturbed each step under sustained damage
DAMAGE_MAG = 5.0          # gaussian kick magnitude (knocks a centroid off its manifold)

# CLAUSE-A sustained-damage window (steady-state, after warmup of the damage regime)
SUS_START = 1500
SUS_END = 4000

# CLAUSE-B burst: one concentrated multi-step burst, then damage stops; measure recovery
BURST_T = 1500
BURST_LEN = 40            # burst spans these steps (every cell hit hard, repeatedly)
BURST_MAG = 6.0
RECOVER_WIN = 400         # steps after the burst within which recovery must occur
PRE_WIN = 200             # pre-burst baseline window
RECOVER_TOL = 0.20        # repair err must return within (1+TOL)*pre-burst baseline


def make_stream(seed):
    """Stationary K_TRUE-cluster stream (sustained-perturbation regime needs a fixed world)."""
    rng = np.random.default_rng(seed)
    centers = rng.standard_normal((K_TRUE, DIM)) * 4.0
    X = np.empty((T, DIM))
    lab = np.empty(T, dtype=int)
    for t in range(T):
        c = int(rng.integers(K_TRUE))
        X[t] = centers[c] + rng.standard_normal(DIM) * 0.6
        lab[t] = c
    return X


def assign(cells, x):
    d = np.linalg.norm(cells - x[None], axis=1)
    j = int(np.argmin(d))
    return j, float(d[j])


def run_arm(X, repair, damage_seed, schedule):
    """
    repair: bool — apply the active repair rule (pull damaged cells back to manifold).
    schedule: callable(t)->bool — True when damage is injected at step t.
    Damage draws (which cells, the kick vectors) are governed by damage_seed so the
    REPAIR and HOMEOSTASIS arms see the IDENTICAL damage. Returns per-step error trace.
    """
    rng_init = np.random.default_rng(damage_seed + 5000)
    cells = X[:K_TRUE].copy().astype(float)
    # warm the homeostatic regime to a clean baseline before any damage
    for t in range(WARMUP):
        j, _ = assign(cells, X[t])
        cells[j] += LR * (X[t] - cells[j])

    n = len(cells)
    mani = cells.copy()                 # running mean of each cell's recent assignments (the manifold)
    dmg_rng = np.random.default_rng(damage_seed)   # SHARED across arms -> identical damage
    errs = np.full(T, np.nan)
    damaged_recent = np.zeros(n, dtype=bool)

    for t in range(WARMUP, T):
        x = X[t]

        # 1) DAMAGE injection (identical draws for both arms)
        damaged_recent[:] = False
        if schedule(t):
            k = max(1, int(round(DAMAGE_FRAC * n)))
            idx = dmg_rng.choice(n, size=k, replace=False)
            mag = DAMAGE_MAG if SUS_START <= t else DAMAGE_MAG  # sustained uses DAMAGE_MAG
            kick = dmg_rng.standard_normal((k, DIM)) * mag
            cells[idx] += kick
            damaged_recent[idx] = True

        # 2) measure error AFTER damage (function = assignment quality of the damaged net)
        j, d = assign(cells, x)
        errs[t] = d

        # 3) HOMEOSTASIS: online LR update on the won cell + manifold running-mean (both arms)
        cells[j] += LR * (x - cells[j])
        mani[j] += (x - mani[j]) / MANI_WIN

        # 4) REPAIR rule: pull every recently-damaged cell back toward its recent manifold
        if repair and damaged_recent.any():
            di = np.where(damaged_recent)[0]
            cells[di] += REPAIR_LR * (mani[di] - cells[di])

    return errs


def burst_schedule(t):
    return BURST_T <= t < BURST_T + BURST_LEN


def sustained_schedule(t):
    # sustained damage every step from the start of streaming (post-warmup)
    return True


def cohen_d(x, y):
    x = np.asarray(x, float); y = np.asarray(y, float)
    sp = math.sqrt((np.std(x) ** 2 + np.std(y) ** 2) / 2.0) or 1e-9
    return (np.mean(x) - np.mean(y)) / sp


def main():
    np.seterr(all="ignore")
    print("=== H_1174 — self-repair vs homeostasis-only under perturbation (life #4) ===", flush=True)

    # ---------- CLAUSE-A: SUSTAINED damage, repair-err vs homeostasis-err, d>=0.8 ----------
    sus_repair, sus_homeo = [], []
    for s in SEEDS:
        X = make_stream(s)
        er = run_arm(X, repair=True,  damage_seed=s, schedule=sustained_schedule)
        eh = run_arm(X, repair=False, damage_seed=s, schedule=sustained_schedule)
        sus_repair.append(float(np.nanmean(er[SUS_START:SUS_END])))
        sus_homeo.append(float(np.nanmean(eh[SUS_START:SUS_END])))
    sus_repair = np.array(sus_repair); sus_homeo = np.array(sus_homeo)
    d_sustained = cohen_d(sus_homeo, sus_repair)   # positive => repair LOWER error
    clause_a = bool(d_sustained >= 0.8 and sus_repair.mean() < sus_homeo.mean())
    print(f"  CLAUSE-A sustained: repair_err={sus_repair.mean():.3f} homeo_err={sus_homeo.mean():.3f} "
          f"d(homeo-repair)={d_sustained:.2f} (bar 0.8) -> {clause_a}", flush=True)

    # ---------- CLAUSE-B: BURST then recovery toward pre-burst baseline ----------
    recovered_flags = []
    post_repair, post_homeo = [], []
    rec_steps_repair = []
    for s in SEEDS:
        X = make_stream(s)
        er = run_arm(X, repair=True,  damage_seed=s, schedule=burst_schedule)
        eh = run_arm(X, repair=False, damage_seed=s, schedule=burst_schedule)
        pre = float(np.nanmean(er[BURST_T - PRE_WIN:BURST_T]))
        post_start = BURST_T + BURST_LEN
        post_r = er[post_start:post_start + RECOVER_WIN]
        post_h = eh[post_start:post_start + RECOVER_WIN]
        # recovery: first step the repair-arm err falls within (1+TOL)*pre baseline
        thresh = pre * (1.0 + RECOVER_TOL)
        below = np.where(post_r <= thresh)[0]
        rec_step = int(below[0]) if below.size else RECOVER_WIN  # RECOVER_WIN = "did not recover in window"
        recovered = bool(below.size > 0)
        recovered_flags.append(recovered)
        rec_steps_repair.append(rec_step)
        post_repair.append(float(np.nanmean(post_r)))
        post_homeo.append(float(np.nanmean(post_h)))
    post_repair = np.array(post_repair); post_homeo = np.array(post_homeo)
    frac_recovered = float(np.mean(recovered_flags))
    d_post = cohen_d(post_homeo, post_repair)      # positive => repair recovers to LOWER err faster
    # CLAUSE-B: repair returns toward baseline in (almost) every seed AND beats homeostasis post-burst
    clause_b = bool(frac_recovered >= 0.8 and d_post >= 0.8 and post_repair.mean() < post_homeo.mean())
    print(f"  CLAUSE-B burst: frac_recovered={frac_recovered:.2f} (bar 0.80) "
          f"mean_rec_step_repair={np.mean(rec_steps_repair):.1f}/{RECOVER_WIN} "
          f"post_repair_err={post_repair.mean():.3f} post_homeo_err={post_homeo.mean():.3f} "
          f"d_post(homeo-repair)={d_post:.2f} (bar 0.8) -> {clause_b}", flush=True)

    supported = bool(clause_a and clause_b)
    verdict = {
        "H": "H_1174",
        "title": "self-repair maintains function under perturbation better than homeostasis alone (life-criterion #4)",
        "n_seeds": N_SEEDS,
        "config": {
            "DIM": DIM, "K_TRUE": K_TRUE, "T": T, "LR": LR,
            "DAMAGE_FRAC": DAMAGE_FRAC, "DAMAGE_MAG": DAMAGE_MAG, "BURST_MAG": BURST_MAG,
            "REPAIR_LR": REPAIR_LR, "MANI_WIN": MANI_WIN,
            "BURST_T": BURST_T, "BURST_LEN": BURST_LEN, "RECOVER_WIN": RECOVER_WIN,
            "RECOVER_TOL": RECOVER_TOL,
        },
        "CLAUSE_A_sustained": {
            "repair_err": float(sus_repair.mean()), "homeo_err": float(sus_homeo.mean()),
            "cohen_d_homeo_minus_repair": float(d_sustained), "bar": 0.8, "pass": clause_a,
        },
        "CLAUSE_B_recovery": {
            "frac_recovered": frac_recovered, "frac_bar": 0.8,
            "mean_recovery_step_repair": float(np.mean(rec_steps_repair)), "recover_win": RECOVER_WIN,
            "post_burst_repair_err": float(post_repair.mean()),
            "post_burst_homeo_err": float(post_homeo.mean()),
            "cohen_d_post_homeo_minus_repair": float(d_post), "d_bar": 0.8, "pass": clause_b,
        },
        "supported": supported,
        "repair_vs_homeostasis_d_sustained": float(d_sustained),
        "ruling": (
            "SUPPORTED (REPAIR-HELPS): under sustained damage the active repair rule holds LOWER "
            "assignment error than homeostasis-only (Cohen's d>=0.8) AND recovers toward the pre-damage "
            "baseline after a damage burst faster than homeostasis alone — self-repair is a function-"
            "maintaining mechanism DISTINCT from the homeostatic regime (life-criterion #4 present)."
            if supported else
            "CLOSED-NEGATIVE: explicit repair ~= homeostasis-only (the SOC/online-update regime already "
            "self-heals damage; the added repair rule is redundant) — see which clause failed (a_paper_negative_ok)."
        ),
        "scope": "toy numpy $0 CPU 12 seeds; prototype-cell PROXY for the CORE cell substrate; "
                 "live engine + scale UNVERIFIED (a_scale_honest_scope). p7 (real assignment error, not perplexity).",
        "xref": ["h931_self_organized_criticality", "h1126_psi_stability", "h1159b_mitosis_capacity_self_tuning",
                 "h1153_criticality_branching"],
    }
    print("\n=== VERDICT ===\n" + json.dumps(verdict, ensure_ascii=False, indent=2), flush=True)
    json.dump(verdict, open("/tmp/h1174_result.json", "w"), ensure_ascii=False, indent=2)
    print("[done]", flush=True)


if __name__ == "__main__":
    main()
