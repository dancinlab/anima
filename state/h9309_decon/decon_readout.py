"""H_9309 DECON — frozen readout. Bars come from PREREG.md; this file only ENFORCES them.

PC-NONCE launch gate (both seeds must pass, else held-out is not fired):
  NOSTORE flip0 in [0.35, 0.65]  — the nonce carries no prior (absence, measured on the model)
  STORE   flip0 >= 0.80          — the store fact is CONSUMED
  STORE   flip1 cluster >= 20/29 — the fact is COMPOSED with the negation morpheme (anti-parrot)

TEST (held-out, only after the gate):
  PRIMARY = flip1, aggregated to 29 atom clusters by 3-form majority, bar C >= 20/29, both seeds.
  flip1 is primary because there the injected fact points at the WRONG answer: a parrot loses.

Any DROPPED trial (window truncation) => INVALID-INSTRUMENT, not a negative result.
"""

import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

BAR_NOSTORE = (0.35, 0.65)     # chance band
BAR_CONSUME = 0.80             # STORE flip0
BAR_COMPOSE = 20               # clusters out of 29
N_CLUSTER = 29


def rows(path):
    if not os.path.exists(path):
        return None
    d = json.load(open(path))
    return d["splits"]["heldout"]["rows"], d["splits"]["heldout"]["summary"]


def frac_pos(rs):
    return sum(1 for r in rs if r["margin"] > 0) / max(1, len(rs))


def z(f, n):
    return (f - 0.5) / math.sqrt(0.25 / n) if n else float("nan")


def clusters(rs, man_rows):
    """3-form majority per atom on flip1 trials — the pre-registered unit (29 atoms, not 87
    trials): the three negation forms of one stem are not independent draws."""
    by = {}
    for r, m in zip(rs, man_rows):
        if m["flip"] != 1:
            continue
        by.setdefault(m["p"], []).append(1 if r["margin"] > 0 else 0)
    return sum(1 for v in by.values() if sum(v) * 2 > len(v)), len(by)


def audit(summ, tag):
    dr = summ.get("consult_dropped", 0)
    if dr:
        print("  ⛔ %s: DROPPED=%d — INVALID-INSTRUMENT (window truncation, not a negative)"
              % (tag, dr))
        return False
    return True


def report(name, path, man_rows):
    got = rows(path)
    if not got:
        print("  %-22s (pending)" % name)
        return None
    rs, summ = got
    f0 = [r for r, m in zip(rs, man_rows) if m["flip"] == 0]
    f1 = [r for r, m in zip(rs, man_rows) if m["flip"] == 1]
    c, nc = clusters(rs, man_rows)
    ok = audit(summ, name)
    a0, a1 = frac_pos(f0), frac_pos(f1)
    print("  %-22s flip0=%.4f (z=%+.2f, n=%d) · flip1=%.4f (z=%+.2f, n=%d) · clusters=%d/%d"
          % (name, a0, z(a0, len(f0)), len(f0), a1, z(a1, len(f1)), len(f1), c, nc))
    return {"flip0": a0, "flip1": a1, "clusters": c, "n_cluster": nc, "audit_ok": ok,
            "d_acc": summ["d_acc"]}


def main():
    nonce = json.load(open(os.path.join(HERE, "pc_nonce_manifest.json")))["heldout"]
    real = json.load(open(os.path.expanduser(
        "~/anima-weights/c34/n2_eval_manifest.json")))["heldout"]
    seeds = ("main_s7", "main_s11")
    out = {"hypothesis": "H_9309", "bars": {"nostore": BAR_NOSTORE, "consume": BAR_CONSUME,
                                            "compose": BAR_COMPOSE}, "pc": {}, "test": {}}

    print("=" * 90)
    print("H_9309 DECON — A-channel (declarative store -> already-learned negation operator)")
    print("  margin 2AFC · win=64B · consult=F2 · primary DV = held-out flip1 (anti-parrot)")
    print("=" * 90)

    print("\n[PC-NONCE launch gate] nonce stems, truth declared by us")
    for s in seeds:
        out["pc"]["nostore_" + s] = report("NOSTORE " + s,
                                           os.path.join(HERE, "nonce_nostore_%s.json" % s), nonce)
        out["pc"]["store_" + s] = report("STORE   " + s,
                                         os.path.join(HERE, "nonce_store_%s.json" % s), nonce)

    pc = out["pc"]
    have = all(pc.get(k) for k in ("nostore_main_s7", "store_main_s7",
                                   "nostore_main_s11", "store_main_s11"))
    if not have:
        print("\n[PENDING] PC-NONCE incomplete — held-out must NOT be fired yet.")
        json.dump(out, open(os.path.join(HERE, "DECON.json"), "w"), ensure_ascii=False, indent=1)
        return

    absent = all(BAR_NOSTORE[0] <= pc["nostore_" + s]["flip0"] <= BAR_NOSTORE[1] for s in seeds)
    consume = all(pc["store_" + s]["flip0"] >= BAR_CONSUME for s in seeds)
    compose = all(pc["store_" + s]["clusters"] >= BAR_COMPOSE for s in seeds)
    clean = all(pc[k]["audit_ok"] for k in pc)
    gate = absent and consume and compose and clean

    print("\n  absence(NOSTORE flip0 in %s) = %s" % (str(BAR_NOSTORE), absent))
    print("  consumption(STORE flip0 >= %.2f) = %s" % (BAR_CONSUME, consume))
    print("  composition(STORE clusters >= %d/%d) = %s" % (BAR_COMPOSE, N_CLUSTER, compose))
    print("  byte-audit clean = %s" % clean)
    print("  => LAUNCH GATE: %s" % ("PASS — held-out may be fired" if gate else "FAIL"))

    if not gate:
        if not absent:
            v = ("⛔ INVALID — a nonce carries a prior polarity (NOSTORE is not at chance). "
                 "Swap the offending stems and re-run. held-out NOT fired.")
        elif not consume:
            v = ("⛔ INVALID-MECHANISM — the store is NOT consumed at all (STORE flip0 < 0.80) "
                 "even when the model can know nothing else. The context-injection channel does "
                 "not deliver the fact. held-out NOT fired (its one-shot contact budget is "
                 "preserved). The lever must be RE-DESIGNED, not re-tuned.")
        else:
            v = ("🔴 PARROT-ONLY (mechanism scope) — the fact IS consumed (flip0 high) but is NOT "
                 "composed with the negation morpheme (flip1 clusters < %d/%d) even on nonces, "
                 "where nothing else could supply the answer. The store can only be echoed, not "
                 "operated on. held-out NOT fired — a held-out negative would be uninterpretable."
                 % (BAR_COMPOSE, N_CLUSTER))
        print("\nVERDICT:", v)
        out["verdict"] = v
        out["gate"] = False
        json.dump(out, open(os.path.join(HERE, "DECON.json"), "w"), ensure_ascii=False, indent=1)
        return

    print("\n[TEST] held-out 29 atoms — PRIMARY = flip1 clusters (bar %d/%d, BOTH seeds)"
          % (BAR_COMPOSE, N_CLUSTER))
    for s in seeds:
        out["test"][s] = report("HELDOUT " + s,
                                os.path.join(HERE, "heldout_store_%s.json" % s), real)
    if not all(out["test"].get(s) for s in seeds):
        print("\n[PENDING] held-out arms not back yet.")
        json.dump(out, open(os.path.join(HERE, "DECON.json"), "w"), ensure_ascii=False, indent=1)
        return

    cs = [out["test"][s]["clusters"] for s in seeds]
    passes = [c >= BAR_COMPOSE for c in cs]
    print("\n  clusters: main_s7=%d/%d · main_s11=%d/%d  (bar %d)"
          % (cs[0], N_CLUSTER, cs[1], N_CLUSTER, BAR_COMPOSE))

    if all(passes):
        v = ("🟢-dir A-CHANNEL — the declarative store STANDS UP held-out recombination. The "
             "already-learned negation operator consumes an externally-supplied polarity and "
             "composes with it (flip1, where a parrot LOSES). ⟹ the G1 wall at this locus was "
             "GROUNDING (a missing input the trunk declined to write), NOT a combination-capacity "
             "ceiling. NEXT = wire the store into the generation path (a_verified_must_wire); "
             "scope: store-supplied grounding, NOT spontaneous natural emergence.")
    elif any(passes):
        v = ("⚠️ SEED-SPLIT — the seeds disagree (%d vs %d of %d). install-fragile, the same "
             "signature H_9289 showed (sign flip across seeds). NOT cementable on one seed."
             % (cs[0], cs[1], N_CLUSTER))
    else:
        v = ("🧱 CONSUME-BUT-NOT-COMPOSE — the mechanism is PROVEN live on nonces (launch gate "
             "PASS: the store is consumed AND composed there), yet held-out recombination still "
             "fails. So this is not an instrument failure: handed the exact missing fact, the "
             "model still cannot recombine on the real atoms. Isomorphic to the read-side "
             "closure's 'restorable but causally unconsumable' — a DEEPER wall than grounding. "
             "⚠️ SUPPORTING, not cemented: n=29 clusters cannot license TOST at Δ_eq=0.10 "
             "(N_REQ≈190) — negatives are earned with power, not with 'ns'.")
    print("\nVERDICT:", v)
    out["verdict"] = v
    out["gate"] = True
    json.dump(out, open(os.path.join(HERE, "DECON.json"), "w"), ensure_ascii=False, indent=1)
    print("→ DECON.json")


if __name__ == "__main__":
    sys.exit(main())
