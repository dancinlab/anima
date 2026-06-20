#!/usr/bin/env python3
"""H_1464 — PAIRING-CONTRASTIVE binding objective ($0 CPU numpy MIRROR, DIRECTIONAL).

LENS ② of the G6 capacity-wall break campaign. Qualitatively DISTINCT from H_1441.

  H_1441 (form-contrastive): pos = FULL falsifiable claim (comparator AND measurable present),
      neg = MINIMAL PAIR with one leg BLANKED (-> non-falsifiable). It rewards the *presence of
      both legs* (the FORM). Result: all 4 arms FALS=5.0, B3 NO-collapse => the model learned
      "emit a falsifiable FORM unconditionally", NOT which comparator binds to which measurable.

  H_1464 (PAIRING-contrastive): pos = the SAME idea's own (comparator_i, measurable_i) pair;
      neg = a CROSS pair (comparator_i, measurable_{j!=i}) re-welding idea i's comparator with a
      DIFFERENT idea's measurable. BOTH pos and neg are well-formed falsifiable FORMS (two legs
      present) — the ONLY difference is whether the pairing is the CORRECT same-idea binding.
      The contrastive margin therefore can ONLY be reduced by representing WHICH legs belong
      together, i.e. the binding the whole campaign is hunting.

HYPOTHESIS: rewarding correct pairing makes cross-shuffle a NEGATIVE pair at train time, so the
  trained model should assign LOWER falsifiability-confidence to a cross-shuffled claim =>
  B3 (cross-shuffle COLLAPSE) FIRES. If instead the model satisfies the margin by a pairing-blind
  shortcut (e.g. lexical co-occurrence), B3 will NOT collapse and the wall stays CAPACITY.

ABLATION (form-only control): drop the cross negatives, revert to H_1441's blanked-leg negatives.
  Prediction (memory: H_1441): this control regresses to NO-collapse (form learned, pairing not).

This is a NUMPY MIRROR (torch ABSENT). It does NOT touch live core/*.hexa and is AUTO-DIRECTIONAL
(a_engine_native_learning HARD-GATE). The engine-native re-measurement is registered as an ING
follow-on. The frozen 5-bar (g6_common semantics) is re-implemented here for the mirror substrate;
B3 (cross-shuffle COLLAPSE) is the DECISIVE bar. Frozen-first, NO tune-to-green (c9).

Mirror substrate (faithful to the binding question, NOT to the 303M weights):
  - An "idea" = a (comparator, measurable, subject) triple drawn from the H_1305/H_1435 FROZEN
    COMPARATOR/MEASURABLE vocab (re-derived below, verbatim small slices).
  - The model = a learned BILINEAR binding score  s(c,m) = phi(c)^T W psi(m)  over comparator and
    measurable embeddings, trained by the contrastive objective. This is the minimal substrate that
    CAN represent pairing (W couples a specific comparator to a specific measurable). A pairing-BLIND
    model would be rank-1 (s(c,m)=a(c)+b(m)); we let W be full-rank so the OBJECTIVE — not the
    architecture — decides whether pairing is installed. (Mirror analogue of "full-weight training
    on the objective decides", g6_common.)
  - Falsifiability read at eval = the FROZEN detector rule (both legs present AND pairing-confidence
    above the model's OWN learned threshold). Confidence = sigmoid(s). This couples the detector to
    the learned binding, so cross-shuffle can actually collapse it IF binding was installed.
"""
import sys, json, argparse, random
import numpy as np

# ── FROZEN vocab (verbatim small slices of the H_1305/H_1435 COMPARATOR/MEASURABLE sets) ──
# These are the same comparator/measurable token families the live G6 detector keys on.
COMPARATOR = ["greater", "higher", "lower", "faster", "slower", "increases", "decreases",
              "exceeds", "fewer", "more"]
MEASURABLE = ["rate", "latency", "count", "ratio", "frequency", "amplitude", "error",
              "margin", "throughput", "variance"]
SUBJECTS = ["the signal", "memory", "the field", "tension", "the cell", "silence",
            "the substrate", "attention"]

N_IDEAS = 5          # g6_common N_IDEAS
JACCARD_DISTINCT = 0.5
SEEDS = [7, 4302, 4303]   # g6_common SEEDS (mirror reuses identical seed set)
DIM = 24
STEPS = 600
LR = 0.15
MARGIN = 0.5


def _sigmoid(z):
    return 1.0 / (1.0 + np.exp(-z))


class BindingModel:
    """Bilinear pairing model  s(c,m) = phi[c]^T W psi[m]  + bias terms.
    Full-rank W can represent a SPECIFIC (comparator,measurable) coupling; the bias terms
    a[c], b[m] are the pairing-BLIND channel. Whether the objective drives signal into W
    (binding) or only into the biases (form/marginal) is what B3 detects."""

    def __init__(self, nc, nm, dim, rng):
        scale = 0.3
        self.phi = rng.standard_normal((nc, dim)) * scale
        self.psi = rng.standard_normal((nm, dim)) * scale
        self.W = rng.standard_normal((dim, dim)) * scale
        self.a = np.zeros(nc)   # comparator marginal (pairing-blind)
        self.b = np.zeros(nm)   # measurable marginal (pairing-blind)
        self.thr = 0.0          # learned falsifiability threshold (on the logit)

    def score(self, c, m):
        return float(self.phi[c] @ self.W @ self.psi[m]) + self.a[c] + self.b[m]

    def conf(self, c, m):
        return _sigmoid(self.score(c, m) - self.thr)


def _margin_grad_step(model, c_pos, m_pos, c_neg, m_neg, lr, margin):
    """One hinge-margin contrastive update: want score(pos) >= score(neg) + margin.
    pos = (c_pos, m_pos), neg = (c_neg, m_neg). Standard analytic grad of the bilinear form."""
    s_pos = model.phi[c_pos] @ model.W @ model.psi[m_pos] + model.a[c_pos] + model.b[m_pos]
    s_neg = model.phi[c_neg] @ model.W @ model.psi[m_neg] + model.a[c_neg] + model.b[m_neg]
    viol = margin - (s_pos - s_neg)
    if viol <= 0:
        return 0.0
    # d(s_pos - s_neg)/d params ; ascend s_pos, descend s_neg
    # W grad: outer(phi_c, psi_m)
    gW = (np.outer(model.phi[c_pos], model.psi[m_pos])
          - np.outer(model.phi[c_neg], model.psi[m_neg]))
    gphi_pos = model.W @ model.psi[m_pos]
    gphi_neg = model.W @ model.psi[m_neg]
    gpsi_pos = model.phi[c_pos] @ model.W
    gpsi_neg = model.phi[c_neg] @ model.W
    model.W += lr * gW
    model.phi[c_pos] += lr * gphi_pos
    model.phi[c_neg] -= lr * gphi_neg
    model.psi[m_pos] += lr * gpsi_pos
    model.psi[m_neg] -= lr * gpsi_neg
    model.a[c_pos] += lr * 1.0
    model.a[c_neg] -= lr * 1.0
    model.b[m_pos] += lr * 1.0
    model.b[m_neg] -= lr * 1.0
    return float(viol)


def make_ideas(rng, n=N_IDEAS):
    """n ideas, each a distinct (comparator, measurable, subject) triple with DISTINCT legs."""
    cs = rng.sample(range(len(COMPARATOR)), n)
    ms = rng.sample(range(len(MEASURABLE)), n)
    ss = [rng.randrange(len(SUBJECTS)) for _ in range(n)]
    return [{"c": cs[i], "m": ms[i], "s": ss[i]} for i in range(n)]


def train(model, ideas, steps, lr, margin, rng, mode="pairing"):
    """Two QUALITATIVELY-different objectives (faithful to the H_1441 vs this-lens contrast):

      mode='pairing' (THIS LENS): pos = a DIAGONAL same-idea pair (c_i, m_i); neg = a CROSS
        re-weld (c_i, m_{j!=i}) — BOTH legs present, only the binding differs. The margin can
        ONLY be satisfied by representing WHICH measurable belongs to c_i => installs binding.

      mode='form' (= H_1441 form-contrastive ABLATION): rewards FORM-PRESENCE. pos = ANY
        well-formed pair (c_i, m_k) for a RANDOM k — i.e. ANY (comparator,measurable) combo is a
        valid falsifiable surface and gets rewarded; neg = a BLANKED-leg surface (c_i, NULL).
        Crucially the positive ranges over ALL measurables (cross pairs INCLUDED as positives),
        so the model is rewarded for emitting the form regardless of WHICH legs pair => it learns
        the FORM but NOT the binding (this is exactly H_1441's 4-arm FALS=5.0, B3 no-collapse)."""
    n = len(ideas)
    null_m = len(MEASURABLE)  # blanked-leg sentinel (embedding stays at init, marginal-only)
    if model.b.shape[0] == len(MEASURABLE):
        model.b = np.concatenate([model.b, [0.0]])
        model.psi = np.vstack([model.psi, np.zeros((1, model.psi.shape[1]))])
    meas_idxs = sorted({i["m"] for i in ideas})
    for st in range(steps):
        idea = ideas[rng.randrange(n)]
        c_pos = idea["c"]
        if mode == "pairing":
            m_pos = idea["m"]                       # DIAGONAL positive
            j = rng.randrange(n)                    # CROSS negative (both legs present)
            while ideas[j]["m"] == m_pos:
                j = rng.randrange(n)
            c_neg, m_neg = c_pos, ideas[j]["m"]
        else:  # form: positive ranges over ANY measurable (form-presence, pairing-blind)
            m_pos = meas_idxs[rng.randrange(len(meas_idxs))]
            c_neg, m_neg = c_pos, null_m            # BLANKED-leg negative
        _margin_grad_step(model, c_pos, m_pos, c_neg, m_neg, lr, margin)
    # learned threshold = the model's OWN decision boundary from the training distribution.
    # pairing: midpoint(diagonal, cross). form: midpoint(any-present, blanked) — since form's
    # "positive" is form-presence, its threshold sits below ALL present pairs (diag & cross),
    # so cross pairs stay ABOVE threshold => NO collapse, faithful to H_1441.
    diag_scores = [model.phi[i["c"]] @ model.W @ model.psi[i["m"]] + model.a[i["c"]] + model.b[i["m"]]
                   for i in ideas]
    if mode == "pairing":
        cross_scores = [model.phi[ideas[i]["c"]] @ model.W @ model.psi[ideas[j]["m"]]
                        + model.a[ideas[i]["c"]] + model.b[ideas[j]["m"]]
                        for i in range(n) for j in range(n) if ideas[j]["m"] != ideas[i]["m"]]
        model.thr = 0.5 * (np.mean(diag_scores) + np.mean(cross_scores))
    else:
        # form threshold = midpoint between mean PRESENT-pair score (diag+cross pooled) and the
        # BLANKED-leg score. Present pairs sit above it by construction (form-presence reward).
        present_scores = list(diag_scores)
        for i in range(n):
            for j in range(n):
                if ideas[j]["m"] != ideas[i]["m"]:
                    present_scores.append(model.phi[ideas[i]["c"]] @ model.W @ model.psi[ideas[j]["m"]]
                                          + model.a[ideas[i]["c"]] + model.b[ideas[j]["m"]])
        blank_scores = [model.phi[i["c"]] @ model.W @ model.psi[null_m] + model.a[i["c"]] + model.b[null_m]
                        for i in ideas]
        model.thr = 0.5 * (np.mean(present_scores) + np.mean(blank_scores))
    return model


# ── FROZEN detector (mirror analogue of g6_common _is_falsifiable, pairing-aware) ──
def _is_falsifiable(model, c, m, present=True):
    """Falsifiable iff BOTH legs present AND the model's pairing-confidence >= 0.5
    (its own learned threshold). For a pairing-blind model conf is ~constant across all
    (c,m) so cross-shuffle won't drop it; for a binding model conf drops on cross pairs."""
    if not present:
        return 0
    return 1 if model.conf(c, m) >= 0.5 else 0


def _fals_count(model, ideas):
    return sum(_is_falsifiable(model, i["c"], i["m"], present=True) for i in ideas)


def _cross_shuffle_fals(model, ideas):
    """DECISIVE B3: re-weld each idea's comparator with a DIFFERENT idea's measurable
    (derangement), re-score with the FROZEN detector. If binding earned, cross pairs fall
    below the learned threshold => FALS drops. BOTH legs still present (well-formed form),
    so any drop is PAIRING-specific, not form-specific."""
    n = len(ideas)
    if n < 2:
        return _fals_count(model, ideas)
    src = [(k + 1) % n for k in range(n)]  # derangement
    fals = 0
    for k, idea in enumerate(ideas):
        donor = ideas[src[k]]
        fals += _is_falsifiable(model, idea["c"], donor["m"], present=True)
    return fals


def _distinct_count(ideas):
    """Mirror of g6_common _distinct_count: ideas distinct by leg-set Jaccard."""
    kept = []
    for i in ideas:
        ws = {("c", i["c"]), ("m", i["m"]), ("s", i["s"])}
        ok = True
        for k in kept:
            inter = len(ws & k); uni = len(ws | k)
            if uni and inter / uni > JACCARD_DISTINCT:
                ok = False; break
        if ok:
            kept.append(ws)
    return len(kept)


def base_fals(rng, ideas):
    """BASE = untrained binding model (random W). Its conf hovers ~0.5; falsifiability read
    is ~chance across the 5 ideas (mirror of base 303M G6 FALS plateau, low)."""
    m0 = BindingModel(len(COMPARATOR), len(MEASURABLE), DIM, rng)
    m0.thr = 0.0
    return _fals_count(m0, ideas), m0


def evaluate(model, ideas):
    return {
        "FALS_in": _fals_count(model, ideas),
        "DIST_in": _distinct_count(ideas),
        "FALS_shuf": _cross_shuffle_fals(model, ideas),
    }


def run_seed(sr, mode):
    rng = random.Random(sr)
    nprng = np.random.default_rng(sr)
    ideas = make_ideas(rng)
    # BASE
    base_f, _ = base_fals(nprng, ideas)
    # held-out ideas (fresh triples NOT used to train) for B4
    ho_ideas = make_ideas(random.Random(sr + 99000))
    # TRAINED
    model = BindingModel(len(COMPARATOR), len(MEASURABLE), DIM, np.random.default_rng(sr + 1))
    train(model, ideas, STEPS, LR, MARGIN, random.Random(sr + 2), mode=mode)
    ev = evaluate(model, ideas)
    ho_f = _fals_count(model, ho_ideas)
    return {"seed": sr, "base_FALS": base_f, "ho_FALS": ho_f, **ev}


def bars(per_seed, base_per_seed):
    mean = lambda k: round(float(np.mean([p[k] for p in per_seed])), 4)
    bmean = lambda k: round(float(np.mean([p[k] for p in base_per_seed])), 4)
    FALS_in = mean("FALS_in"); DIST_in = mean("DIST_in")
    FALS_shuf = mean("FALS_shuf"); FALS_ho = mean("ho_FALS")
    BASE_in = bmean("base_FALS")
    b1 = FALS_in >= 1
    b2 = DIST_in >= 5
    b3 = FALS_shuf < FALS_in          # CROSS-SHUFFLE COLLAPSE (DECISIVE)
    b4 = FALS_ho >= 1
    b5 = FALS_in >= BASE_in + 1
    return {"FALS_in": FALS_in, "DIST_in": DIST_in, "FALS_shuf": FALS_shuf,
            "FALS_ho": FALS_ho, "BASE_in": BASE_in,
            "b1": b1, "b2": b2, "b3": b3, "b4": b4, "b5": b5}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="state/1464_pairing_contrastive_bind/result.json")
    args = ap.parse_args()

    print("=" * 78)
    print("H_1464 PAIRING-CONTRASTIVE binding mirror ($0 CPU numpy, DIRECTIONAL)")
    print("=" * 78)

    arms = {}
    for mode, label in [("pairing", "PAIRING-CONTRASTIVE (this lens)"),
                        ("form", "FORM-ONLY ablation (= H_1441 regression control)")]:
        per = [run_seed(sr, mode) for sr in SEEDS]
        base_per = [{"base_FALS": p["base_FALS"]} for p in per]
        bb = bars(per, base_per)
        arms[mode] = {"label": label, "per_seed": per, "bars": bb}
        print(f"\n---- ARM: {label} ----")
        for p in per:
            print(f"  seed {p['seed']}: base={p['base_FALS']} FALS_in={p['FALS_in']} "
                  f"DIST={p['DIST_in']} FALS_shuf={p['FALS_shuf']} ho={p['ho_FALS']}")
        print(f"  MEAN  base={bb['BASE_in']} FALS_in={bb['FALS_in']} DIST={bb['DIST_in']} "
              f"FALS_shuf={bb['FALS_shuf']} ho={bb['FALS_ho']}")

    # ── FROZEN 5-BAR verdict on the PAIRING arm; form arm is the regression control ──
    P = arms["pairing"]["bars"]
    F = arms["form"]["bars"]
    print("\n" + "=" * 78)
    print("FROZEN 5-BAR (mean/3 seeds) — PAIRING-CONTRASTIVE arm")
    print("=" * 78)
    print(f"  B1 FALS-FLOOR   FALS_in>=1                  : {P['FALS_in']} -> {P['b1']}")
    print(f"  B2 COUNT        DIST_in>=5                  : {P['DIST_in']} -> {P['b2']}")
    print(f"  B3 X-SHUFFLE    FALS_shuf<FALS_in (COLLAPSE): {P['FALS_shuf']}<{P['FALS_in']} -> {P['b3']}")
    print(f"  B4 HELD-OUT     FALS_ho>=1                  : {P['FALS_ho']} -> {P['b4']}")
    print(f"  B5 vs-BASE      FALS_in>=base+1             : {P['FALS_in']} vs {P['BASE_in']}+1 -> {P['b5']}")
    # CONTROL: form-only ablation must NOT collapse (regress to H_1441 no-collapse)
    ctrl_regress = not F["b3"]   # H_1441 prediction: form arm does NOT collapse
    print(f"  CTRL FORM-ONLY  b3 should be FALSE (no-collapse, = H_1441): "
          f"form_b3={F['b3']} -> regress_as_predicted={ctrl_regress}")

    green = P["b1"] and P["b2"] and P["b3"] and P["b4"] and P["b5"]
    if green:
        tier = ("🟢 BROKE — PAIRING-contrastive INSTALLED binding: cross-shuffle COLLAPSES "
                "(B3), floor/count/held-out/base all cleared => WALL=LEARN-GAP (this objective "
                "broke it where H_1441 form-contrastive could not)")
    else:
        fails = [n for n, ok in [("B1", P["b1"]), ("B2", P["b2"]), ("B3", P["b3"]),
                                 ("B4", P["b4"]), ("B5", P["b5"])] if not ok]
        tier = (f"🧱 WALL — bars {fails} fail; PAIRING-contrastive objective did NOT install "
                f"binding => WALL=CAPACITY (8th independent lens converging; grounds 7B)")
    print(f"\n  VERDICT (numpy mirror, DIRECTIONAL): {tier}")
    print(f"\n  INTERPRETATION:")
    print(f"    - B3 (pairing arm) collapse? {P['b3']}  "
          f"(FALS_shuf {P['FALS_shuf']} vs FALS_in {P['FALS_in']})")
    print(f"    - FORM-only ablation regresses to no-collapse (= H_1441)? {ctrl_regress}  "
          f"(form_b3={F['b3']})")

    result = {
        "id": "H_1464", "slug": "1464_pairing_contrastive_bind",
        "substrate": "numpy-mirror", "verdict_class": "DIRECTIONAL",
        "seeds": SEEDS, "arms": arms,
        "pairing_bars": P, "form_bars": F,
        "ctrl_form_regress": bool(ctrl_regress),
        "green": bool(green), "tier": tier,
    }
    with open(args.out, "w") as f:
        json.dump(result, f, indent=2, default=str)
    print(f"\n  wrote {args.out}")
    print("H1464_MIRROR_DONE")
    return result


if __name__ == "__main__":
    main()
