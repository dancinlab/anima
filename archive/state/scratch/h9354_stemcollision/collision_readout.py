#!/usr/bin/env python3
"""H_9354 V3 STEM-COLLISION readout — reads the `anima-py evaluate --xbind` row dump ONLY.

This is post-hoc statistics on engine output. It does NOT re-implement a forward pass and it does
NOT produce a number the engine did not produce (a_experiment_engine_native): every `margin` and
`first_word` it reads was written by cli/evaluate.py's engine-native decode.

Pre-registered in HYPOTHESES/cards/H_9354_stem_collision_byte_vs_repr.md BEFORE any number was read.

  DV        per-item margin m = NLL(counterfactual) - NLL(gold), gold = DONOR-implied flip1 word.
  S_k       0.5*[mean(m|donor pol=1) + mean(m|donor pol=0)]   <- polarity-balanced: a constant
            response bias enters the two cells with opposite sign and cancels.
  A         S_3 (the exact address) — every bound is a FRACTION of A (scale-free).
  PRIMARY   Jonckheere-Terpstra trend across k in {0,1,2} ONLY (k3 = exact address, excluded).

Clustering: items within a donor share a stem representation, so the independent unit is the
DONOR, not the item. Permutation shuffles the k label WITHIN donor (preserves donor effects) and
the CI is a cluster bootstrap over donors. Treating 108 items as 108 independent draws would
manufacture significance out of 12 donors.
"""
import json, sys, random

OPER = ("negL", "negZ")       # operator-live surfaces
CTRL_SURF = "negJ"            # the NO-operator control surface
BOUND = 0.20                  # pre-registered equivalence bound, as a fraction of A
NPERM = 10000
NBOOT = 10000


def load(path):
    d = json.load(open(path))
    out = []
    for r in d["splits"]["heldout"]["rows"]:
        k, tag, donor, pol, f = r["b"].split("|")
        out.append({"k": k, "tag": tag, "donor": donor, "pol": int(pol), "f": f,
                    "m": float(r["margin"]), "hit": int(r["d_hit"]),
                    "nonce": r["a"], "fw": r["first_word"], "gold": r["gold_word"]})
    return out


def S(rows):
    """polarity-balanced cell-mean average (bias-free even under unequal cell counts)."""
    a = [r["m"] for r in rows if r["pol"] == 1]
    b = [r["m"] for r in rows if r["pol"] == 0]
    if not a or not b:
        return float("nan")
    return 0.5 * (sum(a) / len(a) + sum(b) / len(b))


def dacc(rows):
    return sum(r["hit"] for r in rows) / len(rows) if rows else float("nan")


def jt_stat(by_k):
    """Jonckheere-Terpstra: sum over ordered strata pairs of #(m_j > m_i) + 0.5*ties."""
    ks = sorted(by_k)
    U = 0.0
    for i in range(len(ks)):
        for j in range(i + 1, len(ks)):
            for x in by_k[ks[i]]:
                for y in by_k[ks[j]]:
                    U += 1.0 if y > x else (0.5 if y == x else 0.0)
    return U


def jt_test(rows, rng):
    """One-sided (increasing) JT over k in {0,1,2}; k label permuted WITHIN donor."""
    rows = [r for r in rows if r["k"] in ("k0", "k1", "k2")]

    def group(rs):
        g = {}
        for r in rs:
            g.setdefault(r["k"], []).append(r["m"])
        return g

    obs = jt_stat(group(rows))
    by_d = {}
    for r in rows:
        by_d.setdefault(r["donor"], []).append(r)
    ge = 0
    for _ in range(NPERM):
        perm = []
        for d, rs in by_d.items():
            ks = [r["k"] for r in rs]
            rng.shuffle(ks)
            perm += [{"k": kk, "m": r["m"]} for kk, r in zip(ks, rs)]
        if jt_stat(group(perm)) >= obs:
            ge += 1
    return obs, (ge + 1) / (NPERM + 1)


def boot_ci(rows, donors, rng, lo=0.05, hi=0.95):
    """cluster bootstrap over DONORS (the independent unit)."""
    by_d = {}
    for r in rows:
        by_d.setdefault(r["donor"], []).append(r)
    vals = []
    for _ in range(NBOOT):
        samp = []
        for _ in range(len(donors)):
            samp += by_d.get(rng.choice(donors), [])
        v = S(samp)
        if v == v:
            vals.append(v)
    vals.sort()
    return vals[int(lo * len(vals))], vals[int(hi * len(vals))]


def report(path, label):
    rows = load(path)
    op = [r for r in rows if r["tag"] in OPER and r["k"] != "nat"]
    nat = [r for r in rows if r["tag"] in OPER and r["k"] == "nat"]
    cj = [r for r in rows if r["tag"] == CTRL_SURF and r["k"] != "nat"]
    donors = sorted({r["donor"] for r in op})

    print("\n" + "=" * 78)
    print("H_9354 V3 STEM-COLLISION  —  %s   (%s)" % (label, path))
    print("=" * 78)

    per = {}
    print("\n  operator-live surfaces (negL, negZ)   [S_k = polarity-balanced margin, nats]")
    print("  %-5s %-6s %8s %8s %8s %8s" % ("k", "shared", "n", "S_k", "D-acc", "S_k/A"))
    A = S([r for r in op if r["k"] == "k3"])
    for k, sb in (("k0", "0B"), ("k1", "3B"), ("k2", "6B"), ("k3", "9B")):
        rs = [r for r in op if r["k"] == k]
        per[k] = {"n": len(rs), "S": S(rs), "dacc": dacc(rs)}
        print("  %-5s %-6s %8d %8.4f %8.4f %8s" %
              (k, sb, len(rs), per[k]["S"], per[k]["dacc"],
               "%.3f" % (per[k]["S"] / A) if A else "-"))
    per["nat"] = {"n": len(nat), "S": S(nat), "dacc": dacc(nat)}
    print("  %-5s %-6s %8d %8.4f %8.4f      (H_9327 anchor)" %
          ("nat", "-", len(nat), per["nat"]["S"], per["nat"]["dacc"]))
    print("\n  A = S_3 = %.4f nats   equivalence band = +-%.4f  (%.0f%% of A)"
          % (A, BOUND * abs(A), BOUND * 100))

    # ---- gates -------------------------------------------------------------------------------
    print("\n  --- GATES (fail => INVALID instrument, NOT a wall) ---")
    g_pos = per["k3"]["dacc"] >= 0.75 and A > 0
    g_anc = 0.35 <= per["nat"]["dacc"] <= 0.65
    g_c0 = abs(per["k0"]["S"]) <= BOUND * abs(A)
    print("  G-POS    k3 D-acc=%.4f >= 0.75 and S_3=%.4f > 0        %s"
          % (per["k3"]["dacc"], A, "PASS" if g_pos else "FAIL"))
    print("  G-ANCHOR nat D-acc=%.4f in [0.35,0.65]                 %s"
          % (per["nat"]["dacc"], "PASS" if g_anc else "FAIL"))
    print("  G-CTRL0  |S_0|=%.4f <= %.4f                            %s"
          % (abs(per["k0"]["S"]), BOUND * abs(A), "PASS" if g_c0 else "FAIL"))

    # ---- polarity split (polarity-split-before-headline) --------------------------------------
    print("\n  --- polarity split (never read a binary DV before splitting it) ---")
    for k in ("k0", "k1", "k2", "k3"):
        rs = [r for r in op if r["k"] == k]
        p1 = [r["m"] for r in rs if r["pol"] == 1]
        p0 = [r["m"] for r in rs if r["pol"] == 0]
        a1 = dacc([r for r in rs if r["pol"] == 1])
        a0 = dacc([r for r in rs if r["pol"] == 0])
        print("  %-4s donor+ : m=%+7.4f (n=%2d, D-acc=%.3f)   donor- : m=%+7.4f (n=%2d, D-acc=%.3f)"
              % (k, sum(p1) / len(p1), len(p1), a1, sum(p0) / len(p0), len(p0), a0))

    # ---- PRIMARY: Jonckheere trend ------------------------------------------------------------
    obs, p = jt_test(op, random.Random(7))
    print("\n  --- PRIMARY: Jonckheere-Terpstra trend, k in {0,1,2}, one-sided increasing ---")
    print("  JT = %.1f   p(perm, within-donor, %d) = %.4f   %s"
          % (obs, NPERM, p, "TREND" if p < 0.05 else "no trend"))

    # ---- CIs (cluster bootstrap over donors) --------------------------------------------------
    print("\n  --- 90%% CI of S_k (cluster bootstrap over %d donors) vs the +-%.4f band ---"
          % (len(donors), BOUND * abs(A)))
    ci = {}
    for k in ("k0", "k1", "k2"):
        rs = [r for r in op if r["k"] == k]
        dk = sorted({r["donor"] for r in rs})
        lo, hi = boot_ci(rs, dk, random.Random(11))
        ci[k] = (lo, hi)
        inside = abs(lo) <= BOUND * abs(A) and abs(hi) <= BOUND * abs(A)
        width = hi - lo
        wider = width > 2 * BOUND * abs(A)
        print("  %-4s S=%+7.4f  90%% CI [%+7.4f, %+7.4f]  width=%.4f  %s"
              % (k, S(rs), lo, hi, width,
                 "WITHIN band (equivalent to 0)" if inside
                 else ("CI WIDER than band -> UNDERPOWERED" if wider else "OUTSIDE band")))

    # ---- pedestal: donor-polarity label shuffle (true value = 0) -------------------------------
    rngp = random.Random(99)
    ped = []
    for _ in range(200):
        pol = {d: rngp.randint(0, 1) for d in donors}
        sh = [{"m": r["m"] if pol[r["donor"]] == r["pol"] else -r["m"],
               "pol": pol[r["donor"]], "k": r["k"], "donor": r["donor"]} for r in op]
        ped.append(S([r for r in sh if r["k"] == "k2"]))
    ped.sort()
    print("\n  --- PEDESTAL (donor-polarity label shuffle, true value = 0) ---")
    print("  S_2 under shuffled labels: median=%+.4f  90%% range [%+.4f, %+.4f]"
          % (ped[len(ped) // 2], ped[int(.05 * len(ped))], ped[int(.95 * len(ped))]))

    # ---- surface control: negJ (no operator) --------------------------------------------------
    objj, pj = jt_test(cj, random.Random(7))
    print("\n  --- SURFACE CONTROL: negJ (the NO-operator surface) ---")
    for k in ("k0", "k1", "k2", "k3"):
        rs = [r for r in cj if r["k"] == k]
        print("  %-4s S=%+7.4f  D-acc=%.4f  (n=%d)" % (k, S(rs), dacc(rs), len(rs)))
    print("  negJ JT p = %.4f  %s"
          % (pj, "TREND (=> NOT the operator lane)" if pj < .05 else "no trend"))

    return {"A": A, "per": per, "jt_p": p, "ci": ci,
            "gates": {"G-POS": g_pos, "G-ANCHOR": g_anc, "G-CTRL0": g_c0},
            "negJ_p": pj, "pedestal_med": ped[len(ped) // 2]}


if __name__ == "__main__":
    out = {}
    for a in sys.argv[1:]:
        path, lab = a.split("=")
        out[lab] = report(path, lab)

    print("\n" + "=" * 78)
    print("VERDICT (pre-registered)")
    print("=" * 78)
    seeds = list(out)
    bleed = all(out[s]["jt_p"] < .05 and
                out[s]["per"]["k2"]["S"] > BOUND * abs(out[s]["A"]) for s in seeds)
    equiv = all(all(abs(lo) <= BOUND * abs(out[s]["A"]) and abs(hi) <= BOUND * abs(out[s]["A"])
                    for lo, hi in (out[s]["ci"]["k1"], out[s]["ci"]["k2"])) for s in seeds)
    under = any((out[s]["ci"]["k2"][1] - out[s]["ci"]["k2"][0]) > 2 * BOUND * abs(out[s]["A"])
                for s in seeds)
    gates = all(all(out[s]["gates"].values()) for s in seeds)
    if not gates:
        print("  ⛔ INVALID — a pre-registered gate failed. INSTRUMENT failure, not a wall.")
    elif bleed:
        print("  🟢 BLEED / BYTE-FUZZY — the stem key is a byte form.")
    elif equiv:
        print("  🔴 NO BLEED / DISCRETE — the stem address is representational, made by LEARNING.")
    elif under:
        print("  ⏳ UNDERPOWERED — CI wider than the band. NO negative claim is made.")
    else:
        print("  ⚠️  INDETERMINATE — neither the bleed bar nor the equivalence bound was met.")
    json.dump(out, open("h9353_summary.json", "w"), indent=1)
