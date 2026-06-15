#!/usr/bin/env python3
# h1300_mitosis_skill_curriculum.py — H_1300 MITOSIS-GROW SKILL CURRICULUM.
#
# THE QUESTION (the user's idea; a structural p8 claim). Teach anima agent tool-use
# skills ONE AT A TIME. Each new skill = a new CELL grown under that skill's error
# pressure (mitosis, H_1199 VAdaptField / H_1288 grow-under-pressure), NOT a gradient
# overwrite of shared weights. The LOAD-BEARING claim: mitosis-grow AVOIDS
# CATASTROPHIC FORGETTING — adding new cells for a new skill does NOT overwrite the
# cells that hold prior skills, so mitosis RETAINS earlier skills where sequential
# gradient fine-tuning FORGETS them.
#
# DISTINCT from H_1297 (convergence on ONE fit). Here = RETENTION ACROSS a SEQUENTIAL
# multi-skill curriculum (catastrophic-forgetting structure). Convergence ⊥ retention.
#
# DIRECTIONAL numpy MIRROR only (a_engine_native_learning) — engine-transfer + scale
# UNVERIFIED (a_toy_scale_recheck, a_scale_honest_scope). $0 CPU, no GPU, no secrets.
# All bars frozen in .verdicts/1300_mitosis_skill_curriculum/FREEZE.txt BEFORE this run.
#
# LENS (a_no_llm_frame_trap): neurogenesis recruits NEW units localized to a new
# capability; prior circuits are not overwritten — NOT a bigger-transformer recipe.

import numpy as np

# ---- FROZEN knobs (VERBATIM from FREEZE.txt — do NOT tune) -------------------
SEEDS              = [1300, 1301, 1302]
N_SKILLS           = 5
D                  = 12          # context vector dim
C                  = 4           # tool-call tokens (chance = 0.25)
M_PER_SKILL        = 64          # train per skill
M_TEST_PER_SKILL   = 64          # held-out test per skill
CLUSTER_SIGMA      = 0.35        # within-region spread (regions well-separated)
FT_STEPS           = 300         # arm A gradient-FT steps per skill
FT_LR              = 0.20        # arm A learning rate
SPLIT_THRESH       = 0.05        # arm B: cell train-err above this -> split (grow)
GROW_MAX_PER_SKILL = 4           # arm B: finite cell bound per skill (H_1288 footprint)
# frozen bars
RETENTION_MARGIN   = 0.30
ACQ_THRESH         = 0.80
SHUF_SLACK         = 0.15
ABLATE_ACQ_CAP     = 0.50


# ============================ skill curriculum ===============================
def make_curriculum(seed, regime="r1"):
    """N_SKILLS disjoint context REGIONS; each skill k = (region center mu_k,
    per-skill linear rule W_k mapping context -> one of C tool tokens).
    regime 'r1' = well-separated regions + independent rules (R1 FREEZE).
    regime 'r2' = CANONICAL catastrophic-forgetting condition (FREEZE_R2):
                  closer regions (separation 3.0->1.0) + anti-aligned shared rules
                  so sequential gradient-FT must overwrite the shared boundary."""
    rng = np.random.RandomState(seed)
    if regime == "r2":
        sep = 1.0                                   # R2-a: regions overlap -> interference
        mus = rng.normal(0.0, 1.0, (N_SKILLS, D)) * sep
        # R2-b: anti-aligned rules — a SHARED base rule + per-skill sign flips so the
        # SAME context direction maps to DIFFERENT tokens across skills (the defining
        # catastrophic-forgetting setup: learning skill k+1 un-learns skill k).
        base = rng.normal(0.0, 1.0, (C, D))
        Ws = np.empty((N_SKILLS, C, D))
        for k in range(N_SKILLS):
            flip = rng.choice([-1.0, 1.0], size=(C, 1))   # per-row sign flip
            Ws[k] = base * flip + 0.25 * rng.normal(0.0, 1.0, (C, D))
    else:
        # well-separated region centers on a scaled hypercube (distinct skills)
        mus = rng.normal(0.0, 1.0, (N_SKILLS, D)) * 3.0
        # per-skill linear classification rule (the "tool" the skill invokes)
        Ws = rng.normal(0.0, 1.0, (N_SKILLS, C, D))
    skills = []
    for k in range(N_SKILLS):
        def gen(n, kk=k, r=rng):
            x = mus[kk][None, :] + r.normal(0.0, CLUSTER_SIGMA, (n, D))
            y = np.argmax(x @ Ws[kk].T, axis=1)   # tool token = argmax(W_k x)
            return x, y
        xtr, ytr = gen(M_PER_SKILL)
        xte, yte = gen(M_TEST_PER_SKILL)
        skills.append({"mu": mus[k], "xtr": xtr, "ytr": ytr, "xte": xte, "yte": yte})
    return skills


def acc(pred, y):
    return float(np.mean(pred == y))


# ================= ARM A: GRADIENT-FT (sequential, shared weights) =============
def softmax(z):
    z = z - z.max(axis=1, keepdims=True)
    e = np.exp(z)
    return e / e.sum(axis=1, keepdims=True)


def arm_gradient_ft(skills, seed):
    """ONE shared C-way softmax-linear net, fine-tuned SEQUENTIALLY skill-by-skill,
    NO replay. The incumbent that should catastrophically forget skills 1..N-1."""
    rng = np.random.RandomState(seed + 5000)
    W = rng.normal(0.0, 0.01, (C, D))
    b = np.zeros(C)
    acquisition = []   # acc on skill k right after learning it
    for k in range(N_SKILLS):
        x, y = skills[k]["xtr"], skills[k]["ytr"]
        Y = np.eye(C)[y]            # one-hot
        n = x.shape[0]
        for _ in range(FT_STEPS):
            P = softmax(x @ W.T + b)            # (n,C)
            gW = (P - Y).T @ x / n              # (C,D)
            gb = (P - Y).mean(axis=0)
            W -= FT_LR * gW
            b -= FT_LR * gb
        # acquisition: right-after-learning test acc on THIS skill
        pk = np.argmax(skills[k]["xte"] @ W.T + b, axis=1)
        acquisition.append(acc(pk, skills[k]["yte"]))
    # after the full curriculum, eval every skill on the FINAL shared net
    per_skill = []
    for k in range(N_SKILLS):
        p = np.argmax(skills[k]["xte"] @ W.T + b, axis=1)
        per_skill.append(acc(p, skills[k]["yte"]))
    n_params = C * D + C
    return per_skill, acquisition, n_params


# ============ ARM B: MITOSIS-GROW (dedicated cells per skill) ==================
class SkillCell:
    """A grown prototype cell: center + local C-way head (class-mean / local LSQ)."""
    __slots__ = ("center", "W", "b", "skill")
    def __init__(self, center, W, b, skill):
        self.center = center
        self.W = W
        self.b = b
        self.skill = skill


def fit_local_head(x, y):
    """Closed-form local C-way head via ridge least-squares on one-hot targets.
    NO global backprop — local to this cell's owned points only."""
    Y = np.eye(C)[y]                      # (n,C)
    X = np.hstack([x, np.ones((x.shape[0], 1))])   # (n, D+1)
    A = X.T @ X + 1e-3 * np.eye(D + 1)
    sol = np.linalg.solve(A, X.T @ Y)     # (D+1, C)
    return sol[:-1].T, sol[-1]            # W (C,D), b (C)


def grow_skill_cells(x, y, mode_rng):
    """Grow dedicated cells for ONE skill under error pressure (mitosis split):
    start with 1 cell over the whole region; while a cell's local train-err exceeds
    SPLIT_THRESH and we are under the per-skill bound, SPLIT it (k-means-ish bisect
    of its owned points) and refit local heads. Returns a list of SkillCell."""
    # initial single cell at region centroid
    centers = [x.mean(axis=0)]
    while True:
        centers_arr = np.stack(centers)
        own = np.argmin(((x[:, None, :] - centers_arr[None, :, :]) ** 2).sum(-1), axis=1)
        # fit each cell's local head + measure local train error
        heads = []
        local_err = np.full(len(centers), -1.0)
        for ci in range(len(centers)):
            m = own == ci
            if m.sum() == 0:
                heads.append((np.zeros((C, D)), np.zeros(C)))
                continue
            Wc, bc = fit_local_head(x[m], y[m])
            heads.append((Wc, bc))
            pred = np.argmax(x[m] @ Wc.T + bc, axis=1)
            local_err[ci] = float(np.mean(pred != y[m]))
        worst = int(np.argmax(local_err))
        if local_err[worst] <= SPLIT_THRESH or len(centers) >= GROW_MAX_PER_SKILL:
            # converged or hit footprint bound — finalize
            cells = []
            for ci in range(len(centers)):
                Wc, bc = heads[ci]
                cells.append(SkillCell(centers[ci], Wc, bc, None))
            return cells
        # MITOSIS split of the worst cell: bisect its owned points into 2 sub-centroids
        m = own == worst
        xs = x[m]
        # split along the principal axis of owned points (deterministic given data)
        c0 = xs.mean(axis=0)
        d = xs - c0
        # project on top variance direction
        u, s, vt = np.linalg.svd(d, full_matrices=False)
        axis = vt[0]
        proj = d @ axis
        left = xs[proj <= 0.0]; right = xs[proj > 0.0]
        if left.shape[0] == 0 or right.shape[0] == 0:
            # degenerate — finalize
            cells = []
            for ci in range(len(centers)):
                Wc, bc = heads[ci]
                cells.append(SkillCell(centers[ci], Wc, bc, None))
            return cells
        centers[worst] = left.mean(axis=0)
        centers.append(right.mean(axis=0))


def arm_mitosis(skills, seed, mode="targeted"):
    """Mitosis-grow continual learner.
    mode 'targeted'  (B): grow dedicated cells per skill, route to NEAREST cell.
    mode 'shuffle' (B-SHUFFLE): grow same, but PERMUTE cell->center routing.
    mode 'ablate'  (B-ABLATE): grow cells only for skill 0; later skills get NO cells."""
    rng = np.random.RandomState(seed + 9000)
    all_cells = []
    acquisition = []
    for k in range(N_SKILLS):
        if mode == "ablate" and k > 0:
            # growth frozen: no new cells for later skills
            new_cells = []
        else:
            new_cells = grow_skill_cells(skills[k]["xtr"], skills[k]["ytr"], rng)
            for c in new_cells:
                c.skill = k
        all_cells.extend(new_cells)
        # acquisition: route THIS skill's test through ALL cells grown SO FAR
        acquisition.append(_eval_skill(all_cells, skills[k]["xte"], skills[k]["yte"],
                                       mode, rng))
    # final per-skill eval over the FULL grown population (cells never overwritten)
    final_rng = np.random.RandomState(seed + 7777)   # fixed permutation for shuffle
    centers = np.stack([c.center for c in all_cells]) if all_cells else None
    perm = np.random.RandomState(seed + 7777).permutation(len(all_cells)) \
        if (mode == "shuffle" and all_cells) else None
    per_skill = []
    for k in range(N_SKILLS):
        per_skill.append(_route_eval(all_cells, centers, perm,
                                     skills[k]["xte"], skills[k]["yte"]))
    return per_skill, acquisition, len(all_cells)


def _eval_skill(cells, xte, yte, mode, rng):
    """Acquisition-time eval (route through currently-grown cells)."""
    if not cells:
        return 0.0  # ablate later skills: no cell -> cannot emit (counts as 0)
    centers = np.stack([c.center for c in cells])
    perm = None  # acquisition uses true routing even in shuffle (shuffle is final-only
                 # mis-routing of the WHOLE population; acquisition shows B can learn)
    return _route_eval(cells, centers, perm, xte, yte)


def _route_eval(cells, centers, perm, xte, yte):
    if not cells:
        return 0.0
    # nearest cell by L2 to centers
    nearest = np.argmin(((xte[:, None, :] - centers[None, :, :]) ** 2).sum(-1), axis=1)
    if perm is not None:
        nearest = perm[nearest]   # SHUFFLE: scramble which cell each context routes to
    preds = np.empty(xte.shape[0], dtype=int)
    for i in range(xte.shape[0]):
        c = cells[nearest[i]]
        preds[i] = int(np.argmax(c.W @ xte[i] + c.b))
    return acc(preds, yte)


# ============================ run + frozen scoring ===========================
def retention(per_skill):
    """mean test acc on OLD skills 1..N-1 (all but the last-learned)."""
    return float(np.mean(per_skill[:N_SKILLS - 1]))


def run_regime(regime, label):
    print(f"{label}")
    print("=" * 78)
    print(f"N_SKILLS={N_SKILLS} D={D} C={C} (chance={1.0/C:.3f}) M/skill={M_PER_SKILL}"
          f" seeds={SEEDS}  regime={regime}")
    print(f"FROZEN bars: c1 RETENTION_MARGIN={RETENTION_MARGIN} c2 ACQ_THRESH={ACQ_THRESH}"
          f" c3 SHUF_SLACK={SHUF_SLACK} c4 ABLATE_ACQ_CAP={ABLATE_ACQ_CAP}")
    print("-" * 78)

    A_ret, B_ret, BS_ret = [], [], []
    A_acq_last, B_acq_all = [], []          # per-seed
    BA_acq_late = []                         # ablate acquisition skills 2..N
    cells_B = []; params_A = None
    A_perskill_seeds, B_perskill_seeds = [], []

    for seed in SEEDS:
        skills = make_curriculum(seed, regime)
        a_ps, a_acq, a_params = arm_gradient_ft(skills, seed)
        b_ps, b_acq, b_cells = arm_mitosis(skills, seed, "targeted")
        bs_ps, _, _ = arm_mitosis(skills, seed, "shuffle")
        ba_ps, ba_acq, _ = arm_mitosis(skills, seed, "ablate")

        A_ret.append(retention(a_ps)); B_ret.append(retention(b_ps))
        BS_ret.append(retention(bs_ps))
        B_acq_all.append(b_acq)
        BA_acq_late.append(float(np.mean(ba_acq[1:])))   # skills 2..N
        cells_B.append(b_cells); params_A = a_params
        A_perskill_seeds.append(a_ps); B_perskill_seeds.append(b_ps)

        print(f"seed {seed}:")
        print(f"  A grad-FT  per-skill acc = {[f'{v:.2f}' for v in a_ps]}"
              f"  RETENTION(1..{N_SKILLS-1})={retention(a_ps):.3f}")
        print(f"  B mitosis  per-skill acc = {[f'{v:.2f}' for v in b_ps]}"
              f"  RETENTION={retention(b_ps):.3f}  [cells={b_cells}]")
        print(f"  B acquisition (per skill) = {[f'{v:.2f}' for v in b_acq]}")
        print(f"  B-SHUFFLE   per-skill acc = {[f'{v:.2f}' for v in bs_ps]}"
              f"  RETENTION={retention(bs_ps):.3f}")
        print(f"  B-ABLATE    per-skill acc = {[f'{v:.2f}' for v in ba_ps]}"
              f"  acq(skills 2..N)={np.mean(ba_acq[1:]):.3f}")

    print("-" * 78)
    mA_ret = float(np.mean(A_ret)); mB_ret = float(np.mean(B_ret))
    mBS_ret = float(np.mean(BS_ret))
    # per-skill acquisition for B, mean over seeds
    B_acq_arr = np.array(B_acq_all)               # (seeds, N_SKILLS)
    mB_acq = B_acq_arr.mean(axis=0)
    mBA_late = float(np.mean(BA_acq_late))
    mcells = float(np.mean(cells_B))

    print(f"MEAN (3 seeds):")
    print(f"  A grad-FT  RETENTION = {mA_ret:.3f}")
    print(f"  B mitosis  RETENTION = {mB_ret:.3f}   (B-A = {mB_ret-mA_ret:+.3f})")
    print(f"  B-SHUFFLE  RETENTION = {mBS_ret:.3f}")
    print(f"  B acquisition per skill = {[f'{v:.2f}' for v in mB_acq]}"
          f"  (min={mB_acq.min():.3f})")
    print(f"  B-ABLATE   acquisition skills 2..N = {mBA_late:.3f}")
    print(f"  COST (c5): B mitosis cells mean={mcells:.1f}  vs  A params={params_A}")
    print("-" * 78)

    # frozen bars — read VERBATIM, no tune-to-green
    per_seed_c1 = all(B_ret[i] > A_ret[i] for i in range(len(SEEDS)))
    c1 = (mB_ret - mA_ret >= RETENTION_MARGIN) and per_seed_c1
    c2 = bool(np.all(mB_acq >= ACQ_THRESH))
    c3 = mBS_ret <= mA_ret + SHUF_SLACK
    c4 = mBA_late <= ABLATE_ACQ_CAP

    print(f"(c1) RETENTION    B-A>={RETENTION_MARGIN} & per-seed B>A:"
          f"  {mB_ret-mA_ret:+.3f} & per-seed={per_seed_c1}  -> {'PASS' if c1 else 'FAIL'}")
    print(f"(c2) ACQUISITION  min B acq>={ACQ_THRESH}:"
          f"  {mB_acq.min():.3f}  -> {'PASS' if c2 else 'FAIL'}")
    print(f"(c3) SHUFFLE-COLLAPSE B_shuf<=A+{SHUF_SLACK}:"
          f"  {mBS_ret:.3f} <= {mA_ret+SHUF_SLACK:.3f}  -> {'PASS' if c3 else 'FAIL'}")
    print(f"(c4) ABLATE-UNDERFIT  abl acq(2..N)<={ABLATE_ACQ_CAP}:"
          f"  {mBA_late:.3f}  -> {'PASS' if c4 else 'FAIL'}")

    if c1 and c2 and c3 and c4:
        tier = "GREEN"
    elif c1 and c2 and not (c3 and c4):
        tier = "AMBER"
    elif (not c1) and c2:
        tier = "RED"
    else:
        tier = "WALL"
    print("-" * 78)
    print(f"VERDICT TIER (frozen): {tier}")
    print(f"  catastrophic-forgetting (toy): mitosis-grow "
          f"{'RETAINS old skills BETTER than' if c1 else 'does NOT retain better than'}"
          f" sequential gradient-FT")
    print(f"  c1={c1} c2={c2} c3={c3} c4={c4} | DIRECTIONAL mirror, engine-transfer"
          f"+scale UNVERIFIED")
    print("=" * 78)
    return tier, mA_ret, mB_ret, mBS_ret, mBA_late, float(mB_acq.min()), mcells


def main():
    t1 = run_regime("r1", "H_1300 R1 — MITOSIS-GROW SKILL CURRICULUM "
                          "(catastrophic-forgetting vs grad-FT)")
    print()
    t2 = run_regime("r2", "H_1300 R2 — BREAKTHROUGH RUNG (a_break_the_wall): CANONICAL "
                          "catastrophic-forgetting regime\n"
                          "(separation 3.0->1.0 + anti-aligned shared rules; SAME bars, "
                          "no goalpost move)")
    print()
    print("#" * 78)
    print(f"OVERALL: R1 tier={t1[0]}  ->  R2 tier={t2[0]}")
    print(f"  R1: A_ret={t1[1]:.3f} B_ret={t1[2]:.3f} (B-A={t1[2]-t1[1]:+.3f}) "
          f"B_shuf={t1[3]:.3f} B_abl_acq={t1[4]:.3f} B_min_acq={t1[5]:.3f} cells={t1[6]:.1f}")
    print(f"  R2: A_ret={t2[1]:.3f} B_ret={t2[2]:.3f} (B-A={t2[2]-t2[1]:+.3f}) "
          f"B_shuf={t2[3]:.3f} B_abl_acq={t2[4]:.3f} B_min_acq={t2[5]:.3f} cells={t2[6]:.1f}")
    print("#" * 78)
    return t1[0], t2[0]


if __name__ == "__main__":
    main()
