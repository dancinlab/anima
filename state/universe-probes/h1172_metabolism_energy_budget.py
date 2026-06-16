"""
H_1172 — METABOLISM / binding energy budget. Does a REAL energy-in/out budget
(starve -> die) self-regulate cell-count the way H_1159b's EXTERNAL hard MAX_CELLS
cap does — but ORGANICALLY, with no external cap at all?

Audit gap (life-criterion MISSING #2: metabolism): the E ratchet in
a_substrate_native_speak is a MOTIVATION scalar, not a binding metabolism. Real
life consumes energy and dies when starved. H_1159b regulates capacity with an
EXTERNAL hard MAX_CELLS cap; a metabolic budget should replace it organically.

DESIGN (REUSE h1159b mitosis prototype-split; ADD per-cell energy E; REMOVE cap):
  each step:  E -= UPKEEP                          (metabolic upkeep)
              winner cell GAINS  REWARD * (1 - d/D_REF)   (clamped >=0): a cell that
                wins LOW-error assignments is 'useful' and earns energy; a cell that
                only wins high-error (far) points earns ~nothing and starves.
              division (mitosis on tension) COSTS  DIV_COST  and the daughter
                inherits half the parent's energy (the parent pays to reproduce).
              E <= 0  ->  the cell DIES (removed). NO external MAX_CELLS cap.

FROZEN FALSIFIER (from the tape, pre-registered, deterministic, >=10 seeds):
  🟢 ENERGY-GATES iff the energy budget ALONE (no MAX_CELLS) regulates cell-count
     to track world complexity:
       F1  Spearman(K_true, final live cell-count) >= 0.8
     AND surviving cells are the low-error / useful ones:
       F2  survival-usefulness corr >= 0.5
          (across all cells ever born: usefulness = mean reward earned while alive;
           survived = alive at end; point-biserial / Spearman(usefulness, survived) >= 0.5)
  🔴 CLOSED-NEG if energy can't self-regulate count OR the population
     collapses (dies out) / explodes (runaway) (a_paper_negative_ok).
  Guard CONTROL: count must neither collapse (>=1 live cell each K) nor explode
     (bounded, no runaway) — reported, and a collapse/explosion forces 🔴.
  SUPPORTED iff F1 & F2 & no-collapse & no-explosion.

toy ($0 numpy CPU, p7). a_scale_honest_scope.
"""
import json, math
import numpy as np

DIM = 8; T = 4000; WARMUP = 250; N_SEEDS = 10
SEEDS = list(range(800, 800 + N_SEEDS))   # same seed family as h1159b
THETA = 1.6; WIN = 200; LR = 0.05
K_TRUES = [3, 5, 8]

# --- metabolism parameters (the new, binding energy budget) ---
E_INIT   = 1.0     # starting energy of a (newly born) cell
UPKEEP   = 0.010   # energy consumed every step a cell is alive (metabolic cost)
REWARD   = 0.040   # max energy a winning cell can earn on a perfect (d=0) assignment
# D_REF = error scale of the reward kernel reward = REWARD*(1 - d/D_REF) clamped to [0,REWARD].
# CONSTRUCTION NOTE (set BEFORE scoring, diagnosed via /tmp/diag*): the 8-D gaussian
# clusters (centers*4.0, noise sigma=0.6) give an ON-cluster oracle assignment error of
# ~1.65 (=sigma*sqrt(DIM)) while a between-cluster / wrong-cluster point sits at ~4.5-7.
# D_REF MUST sit ABOVE the on-cluster floor (else even a perfectly-useful cell earns less
# than upkeep and the whole population starves trivially -> not a test of the hypothesis,
# the H_1145-style defect) and BELOW the between-cluster scale (so a redundant/mismatched
# cell that only wins far points earns ~0 and starves). D_REF=6.0 -> on-cluster d~1.65 nets
# +0.019/step (survives), far d~5 nets -0.003/step (starves): survival becomes CONTINGENT
# on usefulness, which is exactly the axis F1/F2 probe. This scales the reward kernel to the
# world; it does NOT pre-decide the count or the F1/F2 verdict.
D_REF    = 6.0
DIV_COST = 0.50    # energy a parent pays to divide (daughter inherits half of remainder)
# EXPLOSION guard: a hard sanity ceiling FAR above any expected count (NOT the regulator).
# The metabolism must self-limit well below this; hitting it == runaway == 🔴.
EXPLODE_LIMIT = 200


def make_stream(seed, k_true):
    """Identical world model to h1159b: k_true gaussian clusters appearing spread over time."""
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


def run_metabolism(X, seed):
    """Mitosis with a binding energy budget and NO external MAX_CELLS cap.

    Returns:
      final_live_count : # cells alive at end
      max_count        : peak live count over the run (explosion probe)
      collapsed        : True if population hit 0 live cells at any point
      born_records     : list of per-cell dicts {reward_sum, alive_steps, survived}
                         over EVERY cell ever born — feeds the F2 survival-usefulness corr.
    """
    rng = np.random.default_rng(seed + 5000)
    cells = X[:2].copy().astype(float)
    # warmup: pure prototype adaptation (no energy/mitosis yet), as in h1159b
    for t in range(WARMUP):
        j, _ = assign(cells, X[t]); cells[j] += LR * (X[t] - cells[j])

    n0 = len(cells)
    E = np.full(n0, E_INIT)                 # per-cell energy
    ten = np.zeros(n0)                       # per-cell tension (mean assignment error, EMA)
    # per-cell ledgers indexed by a stable cell-id (rows of `cells` can be deleted)
    reward_sum = [0.0] * n0
    alive_steps = [0] * n0
    cid = list(range(n0))                    # cell-id for each current row
    next_id = n0
    rec = {i: {"reward_sum": 0.0, "alive_steps": 0, "survived": False} for i in range(n0)}

    max_count = len(cells); collapsed = False

    for t in range(WARMUP, T):
        x = X[t]
        if len(cells) == 0:
            collapsed = True
            break
        j, d = assign(cells, x)
        # learn (prototype moves toward the point it won)
        cells[j] += LR * (x - cells[j])
        # --- metabolism: upkeep on all, reward to the winner ---
        E -= UPKEEP
        r = REWARD * (1.0 - d / D_REF)
        if r < 0.0:
            r = 0.0
        E[j] += r
        reward_sum[j] += r
        # tension-driven mitosis (same trigger as h1159b) — but cap is GONE; cost is energy
        ten[j] += (d - ten[j]) / WIN
        if ten[j] > THETA and E[j] > DIV_COST and len(cells) < EXPLODE_LIMIT:
            E[j] -= DIV_COST
            child_E = E[j] * 0.5            # daughter inherits half the parent's remainder
            E[j] -= child_E
            daughter = cells[j] + rng.standard_normal(DIM) * 0.3
            cells = np.vstack([cells, daughter[None]])
            E = np.concatenate([E, [child_E]])
            ten = np.concatenate([ten, [0.0]]); ten[j] = 0.0
            reward_sum.append(0.0); alive_steps.append(0)
            cid.append(next_id)
            rec[next_id] = {"reward_sum": 0.0, "alive_steps": 0, "survived": False}
            next_id += 1
        # age all live cells one step
        for k in range(len(cells)):
            alive_steps[k] += 1
        # --- starvation death: E <= 0 -> remove ---
        alive_mask = E > 0.0
        if not alive_mask.all():
            for k in range(len(cells)):
                if not alive_mask[k]:
                    cell_id = cid[k]
                    rec[cell_id]["reward_sum"] = reward_sum[k]
                    rec[cell_id]["alive_steps"] = alive_steps[k]
                    rec[cell_id]["survived"] = False
            keep = np.where(alive_mask)[0]
            cells = cells[keep]; E = E[keep]; ten = ten[keep]
            reward_sum = [reward_sum[k] for k in keep]
            alive_steps = [alive_steps[k] for k in keep]
            cid = [cid[k] for k in keep]
        if len(cells) == 0:
            collapsed = True
            break
        if len(cells) > max_count:
            max_count = len(cells)

    # finalize survivors
    for k in range(len(cells)):
        cell_id = cid[k]
        rec[cell_id]["reward_sum"] = reward_sum[k]
        rec[cell_id]["alive_steps"] = alive_steps[k]
        rec[cell_id]["survived"] = True

    born_records = []
    for cell_id, d in rec.items():
        steps = d["alive_steps"] if d["alive_steps"] > 0 else 1
        born_records.append({
            "usefulness": d["reward_sum"] / steps,   # mean reward per step alive
            "survived": bool(d["survived"]),
        })
    return len(cells), max_count, collapsed, born_records


def spearman(a, b):
    a = np.asarray(a, float); b = np.asarray(b, float)
    if len(a) < 2:
        return 0.0
    ra = np.argsort(np.argsort(a)).astype(float); rb = np.argsort(np.argsort(b)).astype(float)
    ra -= ra.mean(); rb -= rb.mean(); den = math.sqrt((ra*ra).sum()*(rb*rb).sum())
    return float((ra*rb).sum()/den) if den else 0.0


def main():
    np.seterr(all="ignore")
    print("=== H_1172 — METABOLISM energy budget self-regulates cell-count (NO MAX_CELLS cap) ===", flush=True)
    per_k = {}
    kt_flat, cc_flat = [], []
    all_useful, all_survived = [], []   # pooled over every cell ever born, all K, all seeds
    any_collapse = False; global_max = 0

    for k in K_TRUES:
        counts, maxes, collapses = [], [], []
        for s in SEEDS:
            X = make_stream(s, k)
            cnt, mx, collapsed, born = run_metabolism(X, s)
            counts.append(cnt); maxes.append(mx); collapses.append(collapsed)
            kt_flat.append(k); cc_flat.append(cnt)
            for b in born:
                all_useful.append(b["usefulness"]); all_survived.append(1.0 if b["survived"] else 0.0)
            global_max = max(global_max, mx)
            if collapsed or cnt == 0:
                any_collapse = True
        per_k[k] = {
            "final_count_mean": float(np.mean(counts)),
            "final_count_min": int(np.min(counts)),
            "final_count_max": int(np.max(counts)),
            "peak_count_max": int(np.max(maxes)),
            "n_collapsed": int(np.sum(collapses)),
        }
        print(f"  K_true={k}: final_cells={np.mean(counts):.1f} "
              f"(min {np.min(counts)}/max {np.max(counts)}) peak={np.max(maxes)} "
              f"collapsed={int(np.sum(collapses))}/{N_SEEDS}", flush=True)

    rho_count = spearman(kt_flat, cc_flat)
    rho_surv = spearman(all_useful, all_survived)   # usefulness vs survived (point-biserial-like)
    # survivor-vs-dead usefulness contrast (descriptive support for F2)
    u = np.asarray(all_useful); sv = np.asarray(all_survived)
    surv_u = float(u[sv == 1.0].mean()) if (sv == 1.0).any() else 0.0
    dead_u = float(u[sv == 0.0].mean()) if (sv == 0.0).any() else 0.0

    no_collapse = (not any_collapse) and all(per_k[k]["final_count_min"] >= 1 for k in K_TRUES)
    no_explosion = global_max < EXPLODE_LIMIT
    f1 = rho_count >= 0.8
    f2 = rho_surv >= 0.5
    supported = bool(f1 and f2 and no_collapse and no_explosion)

    verdict = {
        "H": "H_1172",
        "title": "binding metabolism (energy budget, starve->die) self-regulates cell-count WITHOUT the external MAX_CELLS cap",
        "design": "REUSE h1159b mitosis; ADD per-cell energy E (upkeep each step; reward for winning low-error assignments; division costs energy + daughter inherits half; E<=0 -> die); REMOVE the hard MAX_CELLS cap.",
        "params": {"E_INIT": E_INIT, "UPKEEP": UPKEEP, "REWARD": REWARD, "D_REF": D_REF,
                   "DIV_COST": DIV_COST, "THETA": THETA, "WIN": WIN, "LR": LR,
                   "EXPLODE_LIMIT": EXPLODE_LIMIT, "n_seeds": N_SEEDS, "K_trues": K_TRUES},
        "per_K_true": per_k,
        "F1_self_tuning_no_cap": {"spearman_Ktrue_vs_count": rho_count, "bar": 0.8, "pass": bool(f1)},
        "F2_survival_usefulness": {"spearman_usefulness_vs_survived": rho_surv, "bar": 0.5, "pass": bool(f2),
                                   "survivor_mean_usefulness": surv_u, "dead_mean_usefulness": dead_u},
        "guard_no_collapse": {"pass": bool(no_collapse), "note": ">=1 live cell each K, no die-out"},
        "guard_no_explosion": {"pass": bool(no_explosion), "global_peak_count": int(global_max), "explode_limit": EXPLODE_LIMIT},
        "supported": supported,
        "ruling": (
            "SUPPORTED (ENERGY-GATES): a binding metabolic energy budget ALONE — no external MAX_CELLS cap — "
            "self-regulates cell-count to track world complexity (Spearman(K_true,count)>=0.8) AND the survivors "
            "are the useful low-error cells (survival-usefulness>=0.5); starvation IS the organic capacity governor (p8/life)."
            if supported else
            "CLOSED-NEGATIVE: the metabolic energy budget does NOT cleanly self-regulate cell-count without the external cap "
            "(see which gate failed: F1 count-tracking / F2 survival-usefulness / collapse / explosion) — a_paper_negative_ok."
        ),
        "scope": "toy numpy $0 CPU 10 seeds, 3-point K_true ladder {3,5,8}; prototype-split PROXY for CORE cell-division; "
                 "metabolism is a toy energy model, NOT the live E ratchet. live engine + scale UNVERIFIED (a_scale_honest_scope). p7.",
    }
    print("\n=== VERDICT ===\n" + json.dumps(verdict, ensure_ascii=False, indent=2), flush=True)
    json.dump(verdict, open("/tmp/h1172_result.json", "w"), ensure_ascii=False, indent=2)
    print("[done]", flush=True)


if __name__ == "__main__":
    main()
