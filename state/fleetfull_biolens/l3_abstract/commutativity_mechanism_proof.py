#!/usr/bin/env python3
"""
H_9129 L3 ABSTRACT phase — meta-law mechanism proof (SYNTHETIC, $0, mini-safe).

CLAIM UNDER TEST (structural, NOT engine-native — DIRECTIONAL on the escape's LOGIC only):
  The rung-2 WALL (FM_additive <= FM_full on all 5 seeds, binding INERT) is a
  necessary consequence of the CONSEQUENCE TARGET being COMMUTATIVE (a bag /
  histogram of attributes), NOT a property of the substrate or the operator.

  Prediction:
    (A) commutative bag target   -> additive MATCHES full (binding INERT)  [reproduces WALL]
    (B) non-commutative target    -> full BEATS additive (binding EARNED)   [escape diagnostic]

  If (A) and (B) both hold, then the WALL is TARGET-CHOICE-bound: the escape is to
  ground G6 falsifiability in a non-commutative consequence, which FORM (additive,
  position-weighted linear) provably cannot forge.

  This is a PURE-NUMPY proof of the mechanism's LOGIC. It does NOT touch the 303M —
  it only establishes that additive-composability <=> commutativity of the target,
  so the WALL cannot be universal unless the 303M's OWN sequential composition is
  also commutative. That last empirical question is the FALSIFY-round observation
  (over real h1129 reps), pre-registered in ABSTRACT.md.
"""
import json
import numpy as np

D_REP = 32          # part-representation dim (stand-in for 303M penultimate)
D_CONS = 8          # consequence dim
N_CONC = 40
HID = 64
STEPS = 4000
LR = 3e-3
SEEDS = [1305, 2026, 7, 42, 909]


def make_concepts(rng):
    return rng.standard_normal((N_CONC, D_REP)) / np.sqrt(D_REP)


def target_commutative(vx, vy, Wc):
    # consequence = additive bag: symmetric in (x,y), no interaction term.
    # (this is the immune_embed_key trigram-histogram analogue: hist(x U y) = hist(x)+hist(y))
    return (vx + vy) @ Wc


def target_noncommutative(vx, vy, Wc, Wr):
    # consequence carries an ORDER-SENSITIVE bilinear interaction term:
    #   c(x,y) != c(y,x), and NOT recoverable from any position-weighted linear map.
    # A sum is commutative, so this is provably OUTSIDE the additive+position span.
    inter = ((vx @ Wr) * vy) @ Wc[:D_REP]          # bilinear (x rotated) (.) y  -> non-commutative
    lin = (vx - vy) @ Wc                            # antisymmetric linear (still additive-representable w/ position)
    return lin + inter


def fit_forward(vx, vy, cons, rng):
    """Isolate REPRESENTATIONAL CAPACITY, not optimizer skill: both models are solved to
    OPTIMALITY by lstsq. FM_additive = optimal linear map on [vx,vy] (position-weighted, NO
    interaction). FM_full = FM_additive PLUS explicit bilinear (outer-product) interaction feats.
    Held-out MSE. If full < additive strictly -> the interaction term carries irreducible info
    -> binding EARNED. If full ~= additive -> interaction adds nothing -> binding INERT (the WALL)."""
    n = cons.shape[0]
    idx = rng.permutation(n)
    tr, te = idx[: int(0.8 * n)], idx[int(0.8 * n):]

    feat_add = np.concatenate([vx, vy, np.ones((n, 1))], axis=1)          # linear + bias
    outer = (vx[:, :, None] * vy[:, None, :]).reshape(n, -1)              # bilinear vx (X) vy
    feat_full = np.concatenate([feat_add, outer], axis=1)                 # linear + interaction

    Wa = np.linalg.lstsq(feat_add[tr], cons[tr], rcond=None)[0]
    add_err = float(np.mean((feat_add[te] @ Wa - cons[te]) ** 2))
    Wf = np.linalg.lstsq(feat_full[tr], cons[tr], rcond=None)[0]
    full_err = float(np.mean((feat_full[te] @ Wf - cons[te]) ** 2))
    return full_err, add_err


def run_regime(kind, seed):
    rng = np.random.default_rng(seed)
    V = make_concepts(rng)
    Wc = rng.standard_normal((D_REP, D_CONS)) / np.sqrt(D_REP)
    Wr = rng.standard_normal((D_REP, D_REP)) / np.sqrt(D_REP)
    # all ordered pairs (x,y), x!=y  (recombination: held-out unseen combos)
    pairs = np.array([(i, j) for i in range(N_CONC) for j in range(N_CONC) if i != j])
    vx, vy = V[pairs[:, 0]], V[pairs[:, 1]]
    if kind == "commutative":
        cons = target_commutative(vx, vy, Wc)
    else:
        cons = target_noncommutative(vx, vy, Wc, Wr)
    return fit_forward(vx, vy, cons, rng)


def main():
    out = {"D_REP": D_REP, "D_CONS": D_CONS, "N_CONC": N_CONC, "STEPS": STEPS,
           "seeds": SEEDS, "regimes": {}}
    for kind in ["commutative", "noncommutative"]:
        rows = []
        for s in SEEDS:
            fe, ae = run_regime(kind, s)
            rows.append({"seed": s, "FM_full": fe, "FM_additive": ae,
                         "bind_margin": ae - fe,
                         "binding_earned": bool(ae - fe > 0.02 * ae)})
        earned = sum(r["binding_earned"] for r in rows)
        out["regimes"][kind] = {
            "per_seed": rows,
            "mean_full": float(np.mean([r["FM_full"] for r in rows])),
            "mean_additive": float(np.mean([r["FM_additive"] for r in rows])),
            "seeds_binding_earned": f"{earned}/{len(rows)}"}
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
