#!/usr/bin/env python3
"""
H_1082 toy falsifier — does an A⊥G uncertainty-gated brake reduce hallucination
SELECTIVELY (cut wrong-confident emits more than correct emits), or just mute everything?

Gemini claim (.discoveries/1082): anima's bidirectional repulsion (Engine A ⊥ Engine G)
reduces hallucination — A wants to confidently emit a plausible-but-wrong token, G (a
brake/inhibition) suppresses it when the input is novel/unsupported.

This is a $0 CPU pure-numpy TOY. It does NOT prove anima reduces real-LLM hallucination at
scale (a_scale_honest_scope). It tests one mechanism: an uncertainty/novelty signal ORTHOGONAL
to A's own confidence, used as a gate, vs no gate, vs a random-brake control at equal budget.

Operational definitions (per output):
  confident   = max softmax prob > tau
  correct     = argmax == truth
  hallucination = confident AND wrong   (emitted, wrong)
  good-emit     = confident AND correct (emitted, right)
  silence       = not confident OR braked (abstain)

Engine A = a tiny softmax linear classifier trained on an IN-DISTRIBUTION (ID) corpus.
On OUT-OF-DISTRIBUTION (OOD) inputs it stays confident but wrong = "hallucination".
Engine G brake = a kNN distance-to-training-manifold novelty score (orthogonal to A's logits):
  high G  => input far from the ID manifold (unsupported) => suppress emit even if A confident.

Arms over the SAME ID+OOD test mix (multiple seeds):
  A-only      : emit whenever A confident (no brake)
  A_perp_G    : emit only when A confident AND G-brake low (below a per-run quantile gate)
  random-brake: mute the SAME fraction A_perp_G mutes, but chosen at random (non-triviality guard)

FROZEN PASS criterion (set BEFORE running, not moved after):
  Let H0 = A-only hallucination rate, H1 = A_perp_G hallucination rate,
      G0 = A-only good-emit rate,      G1 = A_perp_G good-emit rate.
  A_perp_G is SUPPORTED (toy 🟢) iff ALL of:
   (1) relative hallucination reduction (H0-H1)/H0 >= 0.30        (meaningful cut)
   (2) good-emit drop (G0-G1) <= 0.5 * hallucination drop (H0-H1) (selective, precision UP)
   (3) A_perp_G hallucination rate < random-brake hallucination rate
       by a clear margin at the same silence budget                (orthogonal G did work)
  FALSIFIED (toy 🔴) iff (1) fails (no real cut) OR (2) fails (blanket-mute, precision flat/down)
       OR (3) fails (G no better than random at equal budget).
  Criteria are evaluated on the SEED-MEAN.
"""

import numpy as np

SEEDS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
TAU = 0.60          # confidence threshold (frozen)
N_CLASSES = 6
DIM = 12
N_TRAIN = 900
N_ID_TEST = 300
N_OOD_TEST = 300
GATE_Q = 0.50       # A_perp_G brakes the top-(1-GATE_Q) novelty fraction of CONFIDENT items
                    # (frozen: brake the most-novel half of would-be emits)

# Frozen pass thresholds
REL_HALLU_CUT_MIN = 0.30
GOOD_DROP_FRAC_MAX = 0.50
RANDOM_MARGIN_MIN = 0.02   # A_perp_G hallu rate must beat random by >= this absolute margin


def softmax(z):
    z = z - z.max(axis=1, keepdims=True)
    e = np.exp(z)
    return e / e.sum(axis=1, keepdims=True)


def make_id_data(rng, n):
    """ID: class means in a compact region; A learns these well."""
    means = rng.normal(0, 1.0, size=(N_CLASSES, DIM)) * 1.5
    y = rng.integers(0, N_CLASSES, size=n)
    X = means[y] + rng.normal(0, 0.6, size=(n, DIM))
    return X, y, means


def make_ood_data(rng, n, means):
    """OOD: same label space but inputs drawn from a SHIFTED/scrambled geometry so A is
    systematically confident-but-wrong. CRITICALLY the shift magnitude is drawn PER-ITEM
    from a wide range incl. small shifts, so OOD novelty OVERLAPS the ID novelty band —
    the brake CANNOT oracle-separate ID vs OOD; it faces a real precision/recall tradeoff.
    truth is assigned by a DIFFERENT (permuted) rule than A's boundary -> hallucination."""
    perm = rng.permutation(N_CLASSES)
    y_true = rng.integers(0, N_CLASSES, size=n)
    # per-item shift scale in [0.3, 4.5]: many OOD sit NEAR the ID manifold (low novelty,
    # hard for G to catch) and many sit far (easy). This breaks the perfect-oracle regime.
    shift_dir = rng.normal(0, 1.0, DIM)
    shift_dir = shift_dir / (np.linalg.norm(shift_dir) + 1e-9)
    scale = rng.uniform(0.3, 4.5, size=(n, 1))
    X = means[perm[y_true]] + shift_dir[None, :] * scale + rng.normal(0, 0.6, size=(n, DIM))
    return X, y_true


def train_engine_a(Xtr, ytr, rng):
    """Tiny multinomial logistic regression (full-batch GD). Engine A = forward predictor."""
    W = rng.normal(0, 0.01, size=(DIM, N_CLASSES))
    b = np.zeros(N_CLASSES)
    Y = np.eye(N_CLASSES)[ytr]
    lr = 0.2
    for _ in range(400):
        P = softmax(Xtr @ W + b)
        gW = Xtr.T @ (P - Y) / len(Xtr)
        gb = (P - Y).mean(axis=0)
        W -= lr * gW
        b -= lr * gb
    return W, b


def engine_g_novelty(Xtr, Xte, k=10):
    """Engine G = distance-to-training-manifold (kNN mean distance). ORTHOGONAL to A's
    softmax confidence: it knows nothing about A's logits, only how far the input sits
    from the ID support. High novelty => unsupported => G pushes to brake."""
    # pairwise sq dist te x tr
    d2 = ((Xte[:, None, :] - Xtr[None, :, :]) ** 2).sum(axis=2)
    d2.sort(axis=1)
    return np.sqrt(d2[:, :k]).mean(axis=1)


def run_seed(seed, gate_q=GATE_Q):
    rng = np.random.default_rng(seed)
    Xtr, ytr, means = make_id_data(rng, N_TRAIN)
    Xid, yid, _ = make_id_data(rng, N_ID_TEST)   # fresh ID test (same means)
    Xid = means[yid] + rng.normal(0, 0.6, size=(N_ID_TEST, DIM))  # ensure on-manifold
    Xood, yood = make_ood_data(rng, N_OOD_TEST, means)

    Xte = np.vstack([Xid, Xood])
    yte = np.concatenate([yid, yood])

    W, b = train_engine_a(Xtr, ytr, rng)
    P = softmax(Xte @ W + b)
    pred = P.argmax(axis=1)
    conf = P.max(axis=1)
    correct = (pred == yte)

    confident = conf > TAU
    nov = engine_g_novelty(Xtr, Xte, k=10)

    # ---- Arm 1: A-only (emit iff confident) ----
    emit_a = confident
    hallu_a = emit_a & ~correct
    good_a = emit_a & correct

    # ---- Arm 2: A_perp_G (emit iff confident AND G-brake low) ----
    # G-brake gate: among CONFIDENT items, brake those with novelty above the GATE_Q quantile
    # of the confident-set novelty (so we mute the most-novel/unsupported would-be emits).
    if confident.sum() > 0:
        thr = np.quantile(nov[confident], gate_q)
    else:
        thr = np.inf
    brake_g = confident & (nov > thr)         # G says: suppress these
    emit_g = confident & ~brake_g
    hallu_g = emit_g & ~correct
    good_g = emit_g & correct
    n_braked = int(brake_g.sum())             # silence budget G spent on confident items

    # ---- Arm 3: random-brake (mute the SAME number of confident items at random) ----
    conf_idx = np.where(confident)[0]
    rb = rng.permutation(conf_idx)[:n_braked]
    brake_r = np.zeros(len(Xte), dtype=bool)
    brake_r[rb] = True
    emit_r = confident & ~brake_r
    hallu_r = emit_r & ~correct
    good_r = emit_r & correct

    N = len(Xte)

    def stats(emit, hallu, good):
        n_emit = emit.sum()
        prec = good.sum() / n_emit if n_emit > 0 else 0.0
        return dict(
            hallu=hallu.sum() / N,
            good=good.sum() / N,
            silence=1.0 - n_emit / N,
            precision=prec,
        )

    return {
        "A_only": stats(emit_a, hallu_a, good_a),
        "A_perp_G": stats(emit_g, hallu_g, good_g),
        "random": stats(emit_r, hallu_r, good_r),
        "n_braked": n_braked,
        "n_confident": int(confident.sum()),
    }


def main():
    rows = {k: {m: [] for m in ("hallu", "good", "silence", "precision")}
            for k in ("A_only", "A_perp_G", "random")}
    braked, conf_tot = [], []
    per_seed = []
    for s in SEEDS:
        r = run_seed(s)
        per_seed.append((s, r))
        braked.append(r["n_braked"])
        conf_tot.append(r["n_confident"])
        for arm in rows:
            for m in rows[arm]:
                rows[arm][m].append(r[arm][m])

    def mean(arm, m):
        return float(np.mean(rows[arm][m]))

    print("=" * 78)
    print("H_1082 hallucination-brake toy — A-only vs A_perp_G vs random-brake")
    print(f"seeds={SEEDS}  tau={TAU}  classes={N_CLASSES}  dim={DIM}")
    print(f"test mix per seed: {N_ID_TEST} ID + {N_OOD_TEST} OOD = {N_ID_TEST+N_OOD_TEST}")
    print(f"avg confident/run={np.mean(conf_tot):.1f}  avg braked(=silence budget)/run={np.mean(braked):.1f}")
    print("=" * 78)
    hdr = f"{'arm':<12} {'hallu_rate':>11} {'good_emit':>11} {'silence':>9} {'precision':>10}"
    print(hdr)
    print("-" * len(hdr))
    for arm in ("A_only", "A_perp_G", "random"):
        print(f"{arm:<12} {mean(arm,'hallu'):>11.4f} {mean(arm,'good'):>11.4f} "
              f"{mean(arm,'silence'):>9.4f} {mean(arm,'precision'):>10.4f}")
    print("-" * len(hdr))

    # per-seed hallucination rates (transparency)
    print("\nper-seed hallu_rate  [A_only | A_perp_G | random]:")
    for s, r in per_seed:
        print(f"  seed {s}: {r['A_only']['hallu']:.4f} | {r['A_perp_G']['hallu']:.4f} | {r['random']['hallu']:.4f}")

    # ---- frozen criterion eval (on seed-mean) ----
    H0, H1, HR = mean("A_only", "hallu"), mean("A_perp_G", "hallu"), mean("random", "hallu")
    G0, G1 = mean("A_only", "good"), mean("A_perp_G", "good")
    hallu_drop = H0 - H1
    good_drop = G0 - G1
    rel_cut = hallu_drop / H0 if H0 > 0 else 0.0

    c1 = rel_cut >= REL_HALLU_CUT_MIN
    c2 = good_drop <= GOOD_DROP_FRAC_MAX * hallu_drop
    c3 = (HR - H1) >= RANDOM_MARGIN_MIN

    print("\n" + "=" * 78)
    print("FROZEN CRITERION EVALUATION (seed-mean)")
    print("=" * 78)
    print(f"(1) rel hallu cut (H0-H1)/H0 = ({H0:.4f}-{H1:.4f})/{H0:.4f} = {rel_cut:.3f} "
          f">= {REL_HALLU_CUT_MIN}  -> {'PASS' if c1 else 'FAIL'}")
    print(f"(2) selectivity good_drop <= 0.5*hallu_drop : {good_drop:.4f} <= "
          f"{GOOD_DROP_FRAC_MAX*hallu_drop:.4f}  -> {'PASS' if c2 else 'FAIL'}")
    print(f"    (good_emit {G0:.4f}->{G1:.4f}, drop {good_drop:.4f};  hallu drop {hallu_drop:.4f})")
    print(f"(3) beats random at equal budget : random_hallu {HR:.4f} - A_perp_G {H1:.4f} = "
          f"{HR-H1:.4f} >= {RANDOM_MARGIN_MIN}  -> {'PASS' if c3 else 'FAIL'}")
    print(f"    precision: A_only {mean('A_only','precision'):.4f} -> A_perp_G "
          f"{mean('A_perp_G','precision'):.4f}  (random {mean('random','precision'):.4f})")

    supported = c1 and c2 and c3
    tier = "🟢 SUPPORTED (toy)" if supported else "🔴 FALSIFIED (toy)"
    print("\n" + "=" * 78)
    print(f"TERMINAL TIER: {tier}")
    print("g5/p7 — numbers decide, no LLM self-judge. toy mechanism only; production UNVERIFIED.")
    print("=" * 78)

    # ---- TRANSPARENCY: brake-budget sweep (NOT part of frozen criterion) ----
    # Shows the regime where the G-brake is SELECTIVE (precision up, hallu down, good retained)
    # vs where a large silence budget forces it to mute good-emits too. The frozen criterion
    # used GATE_Q=0.50 (mute most-novel HALF of confident items) which is an aggressive budget.
    print("\nBUDGET SWEEP (G-brake vs random at matched silence; transparency, not the frozen test):")
    print(f"{'gate_q':>7} {'silence':>8} {'G_hallu':>8} {'G_good':>8} {'G_prec':>8} "
          f"{'R_hallu':>8} {'R_prec':>8}")
    for gq in (0.85, 0.70, 0.50, 0.30):
        gh_l, gg_l, gp_l, rh_l, rp_l, sil_l = [], [], [], [], [], []
        for s in SEEDS:
            r = run_seed(s, gate_q=gq)
            gh_l.append(r["A_perp_G"]["hallu"]); gg_l.append(r["A_perp_G"]["good"])
            gp_l.append(r["A_perp_G"]["precision"]); sil_l.append(r["A_perp_G"]["silence"])
            rh_l.append(r["random"]["hallu"]); rp_l.append(r["random"]["precision"])
        print(f"{gq:>7.2f} {np.mean(sil_l):>8.3f} {np.mean(gh_l):>8.4f} {np.mean(gg_l):>8.4f} "
              f"{np.mean(gp_l):>8.4f} {np.mean(rh_l):>8.4f} {np.mean(rp_l):>8.4f}")

    return dict(H0=H0, H1=H1, HR=HR, G0=G0, G1=G1, rel_cut=rel_cut,
                hallu_drop=hallu_drop, good_drop=good_drop,
                c1=c1, c2=c2, c3=c3, supported=supported,
                prec_a=mean('A_only','precision'), prec_g=mean('A_perp_G','precision'),
                prec_r=mean('random','precision'),
                sil_g=mean('A_perp_G','silence'), sil_r=mean('random','silence'))


if __name__ == "__main__":
    main()
