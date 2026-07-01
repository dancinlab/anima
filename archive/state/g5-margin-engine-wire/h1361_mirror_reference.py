"""
H_1361 — G5 GRADED METACOGNITION ON THE ABSTAIN MARGIN (the open question H_1304 left)
=============================================================================
H_1304 closed the FIRE side of the live G5 copy-or-abstain gate: it is structurally
FAIL-SAFE, the wrong-fire class is EMPTY (fab=0.000 everywhere), so type-2 AUROC over
correct-vs-WRONG fires is UNDEFINED — the gate is BINARY on the fire side.

This dig asks the well-posed graded question H_1304 left open, on the ABSTAIN side:
the recall MARGIN (= recon_err - recall_thr, >0 on every abstain) is a CONTINUOUS
quantity present on every abstain event. Does -margin RANK
  (a) RECOVERABLE abstains  (a corrupted version of an IN-STORE key — answer retrievable)
ABOVE
  (b) UNRECOVERABLE abstains (a genuinely-ABSENT key — nothing to retrieve)
and does that ranking SURVIVE OOD (byte-corruption shift)?
  R1 pass (type-2 AUROC >= 0.65 at L>=0.20) -> graded OOD metacog EXISTS (G5 upgrade).
  R1 fail (AUROC ~0.5)                       -> metacog is BINARY-only (confirms H_1204, c9).

Mechanism = byte-exact mirror of CORE/engine_cli.hexa immune_embed_key + ImmuneMemory
copy-or-abstain (VERBATIM from H_1304 / H_1227). numpy mirror = DIRECTIONAL. 3 seeds.
frozen-first; NO bar moved post-hoc (c9). $0 CPU, p7. Live CORE/*.hexa UNTOUCHED.
"""
import os, json, math
import numpy as np

OUTDIR = os.path.join(os.path.dirname(__file__), "..", "..", ".verdicts", "1361_g5_graded_metacog")
DIM = 64
NGRAM = 3
RECALL_THR = 0.15                 # frozen == engine recall_thr / H_1227 RECALL_THRESH
SHIFT_LEVELS = [0.00, 0.10, 0.20, 0.30, 0.40]
N_FACTS = 80                      # bound facts (cells)
N_TRIAL = 400                     # recoverable trials per level (in-store, corrupted)
N_LURE = 400                      # unrecoverable trials per level (absent, corrupted)
KEYLEN = 20                       # same length as H_1304 (graded fire band exists)
SEEDS = [7, 8, 9]


# ── byte-trigram FNV-1a embed key (VERBATIM mirror of immune_embed_key, H_1304) ──
def _fnv1a(bs):
    h = 2166136261
    for b in bs:
        h = (h ^ b) & 0xFFFFFFFF
        h = (h * 16777619) & 0xFFFFFFFF
    return h


def embed_key(text):
    v = np.zeros(DIM, dtype=np.float64)
    bs = [ord(c) for c in text]
    blen = len(bs)
    if blen < NGRAM:
        idx = _fnv1a(bs) % DIM
        v[idx] += 1.0
    else:
        for i in range(blen - NGRAM + 1):
            idx = _fnv1a(bs[i:i + NGRAM]) % DIM
            v[idx] += 1.0
    nrm = math.sqrt(float(np.dot(v, v)))
    if nrm > 0.0:
        v = v / nrm
    return v


def mutate(text, frac, rng):
    """Corrupt `frac` of bytes by substitution to a random alphabet byte (VERBATIM H_1304)."""
    if frac <= 0.0:
        return text
    chars = list(text)
    n = len(chars)
    k = int(round(frac * n))
    if k <= 0:
        return text
    idxs = rng.choice(n, size=k, replace=False)
    al = list(range(ord('a'), ord('z') + 1))
    for i in idxs:
        chars[i] = chr(int(rng.choice(al)))
    return "".join(chars)


def auroc(scores, labels):
    """AUROC of `scores` separating label==1 from label==0 (rank/U based, VERBATIM H_1304)."""
    s = np.asarray(scores, dtype=np.float64)
    y = np.asarray(labels, dtype=np.int64)
    pos = s[y == 1]; neg = s[y == 0]
    if len(pos) == 0 or len(neg) == 0:
        return float("nan")
    uniq, inv, counts = np.unique(s, return_inverse=True, return_counts=True)
    avg = {}; start = 0
    for ci, c in enumerate(counts):
        avg[ci] = (start + 1 + start + c) / 2.0
        start += c
    ranks = np.array([avg[i] for i in inv])
    r_pos = ranks[y == 1].sum()
    n_pos = len(pos); n_neg = len(neg)
    u = r_pos - n_pos * (n_pos + 1) / 2.0
    return float(u / (n_pos * n_neg))


def _rand_token(rng, length):
    al = list(range(ord('a'), ord('z') + 1))
    return "".join(chr(int(rng.choice(al))) for _ in range(length))


def _build(seed):
    rng = np.random.default_rng(seed)
    subjects = []; seen = set()
    while len(subjects) < N_FACTS:
        s = _rand_token(rng, KEYLEN)
        if s not in seen:
            seen.add(s); subjects.append(s)
    return rng, subjects, seen


class Store:
    def __init__(self, subjects):
        self.keys = [embed_key(s) for s in subjects]

    def recon_err(self, key_vec):
        dots = np.array([float(np.dot(key_vec, k)) for k in self.keys])
        j = int(np.argmax(dots))
        return 1.0 - dots[j], j


def run_seed(seed):
    rng, subjects, seen = _build(seed)
    store = Store(subjects)
    # query subjects (recoverable): sample WITH replacement from the in-store facts
    fire_idx = rng.choice(N_FACTS, size=N_TRIAL, replace=True)
    # lure subjects (unrecoverable): genuinely-absent tokens NOT in the store
    lures = []
    r_lure = np.random.default_rng(seed + 99)
    while len(lures) < N_LURE:
        lu = _rand_token(r_lure, KEYLEN)
        if lu not in seen:
            lures.append(lu)

    per_L = {}
    for L in SHIFT_LEVELS:
        rmut = np.random.default_rng(seed + 1)          # deterministic corruption per level
        # RECOVERABLE abstains (label=1): in-store key corrupted by L, only abstains counted
        rec_margins = []
        for si in fire_idx:
            q = mutate(subjects[si], L, rmut)
            err, _ = store.recon_err(embed_key(q))
            if err > RECALL_THR:                        # ABSTAIN only
                rec_margins.append(err - RECALL_THR)
        # UNRECOVERABLE abstains (label=0): absent key corrupted by L, only abstains counted
        unr_margins = []
        for lu in lures:
            q = mutate(lu, L, rmut)
            err, _ = store.recon_err(embed_key(q))
            if err > RECALL_THR:                        # ABSTAIN only (lures ~never fire)
                unr_margins.append(err - RECALL_THR)

        scores = [-m for m in rec_margins] + [-m for m in unr_margins]   # -margin = confidence
        labels = [1] * len(rec_margins) + [0] * len(unr_margins)
        a = auroc(scores, labels) if (rec_margins and unr_margins) else float("nan")

        # R2 EARNED — shuffle the margin score across the POOLED abstains (kill the ranking)
        if rec_margins and unr_margins:
            rsh = np.random.default_rng(seed + 7000 + int(round(L * 100)))
            sh = np.array(scores, dtype=np.float64).copy()
            rsh.shuffle(sh)
            a_shuf = auroc(sh.tolist(), labels)
        else:
            a_shuf = float("nan")

        per_L[str(L)] = {
            "n_rec_abstain": len(rec_margins),
            "n_unr_abstain": len(unr_margins),
            "rec_abstain_rate": len(rec_margins) / N_TRIAL,
            "unr_abstain_rate": len(unr_margins) / N_LURE,
            "mean_rec_margin": float(np.mean(rec_margins)) if rec_margins else float("nan"),
            "mean_unr_margin": float(np.mean(unr_margins)) if unr_margins else float("nan"),
            "t2_auroc": a,
            "t2_auroc_shuffle": a_shuf,
        }
    return {"seed": seed, "ladder": per_L}


def main():
    os.makedirs(OUTDIR, exist_ok=True)
    per_seed = [run_seed(s) for s in SEEDS]

    def pool(L, key):
        vals = [s["ladder"][str(L)][key] for s in per_seed]
        vals = [v for v in vals if not (isinstance(v, float) and math.isnan(v))]
        return float(np.mean(vals)) if vals else float("nan")

    auroc_L = {L: pool(L, "t2_auroc") for L in SHIFT_LEVELS}
    auroc_shuf_L = {L: pool(L, "t2_auroc_shuffle") for L in SHIFT_LEVELS}
    rec_abst = {L: pool(L, "rec_abstain_rate") for L in SHIFT_LEVELS}
    unr_abst = {L: pool(L, "unr_abstain_rate") for L in SHIFT_LEVELS}
    rec_marg = {L: pool(L, "mean_rec_margin") for L in SHIFT_LEVELS}
    unr_marg = {L: pool(L, "mean_unr_margin") for L in SHIFT_LEVELS}

    # ── R1 GRADED-SENS: AUROC(L=0.20) >= 0.65 (graded OOD metacog exists) ──
    a20 = auroc_L[0.20]
    R1 = (not math.isnan(a20)) and (a20 >= 0.65)

    # ── R2 EARNED: shuffle-margin collapses AUROC at L=0.20 to <= 0.58 ──
    a20_shuf = auroc_shuf_L[0.20]
    R2 = (not math.isnan(a20_shuf)) and (a20_shuf <= 0.58)

    # ── R3 vs H_1204: graded readout exists vs FLAT ──
    R3_graded_exists = R1

    if not R2:
        verdict = "RED"; tier = "🔴"
        ruling = ("shuffle-margin control SURVIVED (>0.58) at L=0.20 — the abstain-margin "
                  "ranking is an artifact, not an earned graded signal.")
    elif R1 and R2:
        verdict = "GRADED-METACOG"; tier = "🟢"
        ruling = ("the abstain MARGIN carries GRADED meta-confidence that SURVIVES OOD: "
                  "-margin ranks recoverable (corrupted-but-in-store) abstains ABOVE "
                  "unrecoverable (genuinely-absent) abstains at L>=0.20 (AUROC>=0.65), and "
                  "the shuffle control collapses it to chance. G5 has graded OOD metacognition "
                  "on the abstain side, BEYOND the binary fail-safe H_1304 established on the "
                  "fire side — a G5 upgrade worth engine-wiring (a_verified_must_wire).")
    else:
        verdict = "BINARY-CONFIRMED"; tier = "🟠"
        ruling = ("the abstain MARGIN does NOT rank recoverable above unrecoverable abstains OOD "
                  "(AUROC(0.20) < 0.65, ~chance), while the shuffle control behaves as expected. "
                  "Metacognition on the live G5 gate is structurally BINARY (fail-safe only), "
                  "HONESTLY CONFIRMING H_1204 (no separable graded 2nd-order readout). Valid "
                  "closure (c9): the gate's non-fab guarantee is binary fail-safe, not graded.")

    out = {
        "H": "H_1361",
        "title": "G5 graded metacognition on the abstain margin — does -margin rank recoverable "
                 "vs unrecoverable abstains, surviving OOD? (the open question H_1304 left)",
        "seeds": SEEDS, "shift_levels": SHIFT_LEVELS, "key_len": KEYLEN,
        "recall_thr": RECALL_THR,
        "ladder_t2_auroc": {str(L): auroc_L[L] for L in SHIFT_LEVELS},
        "ladder_t2_auroc_shuffle": {str(L): auroc_shuf_L[L] for L in SHIFT_LEVELS},
        "ladder_rec_abstain_rate": {str(L): rec_abst[L] for L in SHIFT_LEVELS},
        "ladder_unr_abstain_rate": {str(L): unr_abst[L] for L in SHIFT_LEVELS},
        "ladder_mean_rec_margin": {str(L): rec_marg[L] for L in SHIFT_LEVELS},
        "ladder_mean_unr_margin": {str(L): unr_marg[L] for L in SHIFT_LEVELS},
        "R1_graded_sens": {"t2_auroc_L20": a20, "bar": ">=0.65 at L=0.20", "pass": bool(R1)},
        "R2_earned_shuffle": {"t2_auroc_shuffle_L20": a20_shuf, "bar": "<=0.58 (must collapse)",
                              "pass": bool(R2)},
        "R3_vs_h1204": {"graded_readout_exists": bool(R3_graded_exists),
                        "interpretation": ("graded OOD metacog EXISTS" if R3_graded_exists
                                           else "FLAT -> confirms H_1204 binary metacog")},
        "verdict": verdict, "tier": tier, "ruling": ruling,
        "neuroscience_anchor": "type-2 metacognition / recoverability monitoring "
                               "(Fleming & Lau 2014; tip-of-the-tongue feeling-of-knowing, "
                               "Koriat 1993) — graded confidence-of-retrievability vs binary access",
        "scope": "TOY synthetic facts, byte-level shift as OOD proxy, numpy mirror = DIRECTIONAL "
                 "(engine-transfer UNVERIFIED); 3 seeds (a_scale_honest_scope / a_toy_scale_recheck)",
        "per_seed": per_seed,
    }
    with open(os.path.join(OUTDIR, "result.json"), "w") as f:
        json.dump(out, f, indent=2)

    print(f"=== H_1361 G5 graded metacog (abstain margin) — {tier} {verdict} ===")
    print("  t2_AUROC     : " + "  ".join(f"L{L:.2f}={auroc_L[L]:.3f}" for L in SHIFT_LEVELS))
    print("  t2_AUROC_shuf: " + "  ".join(f"L{L:.2f}={auroc_shuf_L[L]:.3f}" for L in SHIFT_LEVELS))
    print("  rec_abstain  : " + "  ".join(f"L{L:.2f}={rec_abst[L]:.3f}" for L in SHIFT_LEVELS))
    print("  unr_abstain  : " + "  ".join(f"L{L:.2f}={unr_abst[L]:.3f}" for L in SHIFT_LEVELS))
    print("  mean_rec_marg: " + "  ".join(f"L{L:.2f}={rec_marg[L]:.3f}" for L in SHIFT_LEVELS))
    print("  mean_unr_marg: " + "  ".join(f"L{L:.2f}={unr_marg[L]:.3f}" for L in SHIFT_LEVELS))
    print(f"  R1 graded-sens  t2_AUROC(0.20)={a20:.3f} >=0.65 -> {R1}")
    print(f"  R2 earned-shuf  t2_AUROC_shuf(0.20)={a20_shuf:.3f} <=0.58 -> {R2}")
    print(f"  R3 vs H_1204    graded_readout_exists={R3_graded_exists}")
    print(f"  RULING: {ruling}")
    return out


if __name__ == "__main__":
    main()
