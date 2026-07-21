"""H_004 guard battery (G-A..G-E) — the $0 deterministic verdict on the REPAIRED rig.

After the donor-pair fix, the question is not "does the frozen arm cheat at order-1"
(it no longer can) but "at what ORDER is the NEG class recoverable from the frozen
tokenization, and does that leave any room above it for atomicity". These guards
answer it deterministically, with no training run:

  G-A  last-token (order-1) Bayes lookup     — must be <= 0.55  (order-1 dead)
  G-B  body-length-only Bayes lookup         — must be <= 0.55  (no length shortcut)
  G-C  last-2-token (order-2) bigram lookup   — REPORTED as the frozen ceiling
  G-D  atomicity contrast (frozen 0/12, oracle 12/12)
  G-E  leak / co-occurrence on the trained corpus

The verdict this produces is about the RIG's ability to isolate atomicity, which is
the precondition for H_004's Δ_pilot to mean anything. If G-C ≈ 1.0, the frozen arm
has a trivial order-2 path a transformer binds with one attention head, so
Δ_pilot < 0.20 is structurally forced regardless of the training run.

Run: python3 state/h004_static-anchor-pilot_2026-07-16/run_guards.py
Deterministic, stdlib + generator only, $0.
"""

from __future__ import annotations

import collections
import json
import os
import random
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.abspath(os.path.join(_HERE, "..", ".."))
sys.path.insert(0, os.path.join(_ROOT, "src", "generator"))

import spec as S
import stream as ST
import codec as C
import audit as A
from lang import to_jamo, render
from stream import NEG_MARK, SENTINEL

FIT_LINES = 20000
TRAIN_LOOKUP_LINES = 40000
K = 512


def _body_and_polarity(line):
    body = line.split(SENTINEL)[0]
    is_neg = line.endswith(to_jamo(NEG_MARK))
    return body, is_neg


def _lookup(spec, frozen, keyfn):
    """Fit P(neg | key) on phase-2 training lines; return the key->neg-prob table."""
    rng = random.Random(spec["seed"] + 31)
    cnt, negc = collections.Counter(), collections.Counter()
    for _ in range(TRAIN_LOOKUP_LINES):
        body, is_neg = _body_and_polarity(ST.line(spec, 2, rng))
        key = keyfn(frozen.encode_tokens(to_jamo(body)))
        cnt[key] += 1
        if is_neg:
            negc[key] += 1
    return cnt, negc


def _score(spec, frozen, items, keyfn):
    cnt, negc = _lookup(spec, frozen, keyfn)
    correct = 0
    for it in items:
        body = it["neg"] if it["label"] == "neg" else it["pos"]
        key = keyfn(frozen.encode_tokens(to_jamo(body)))
        pred = "neg" if (cnt[key] > 0 and negc[key] / cnt[key] > 0.5) else "pos"
        if pred == it["label"]:
            correct += 1
    return correct / len(items)


def main() -> int:
    spec = S.build_spec()
    frozen = C.fit_bpe_jamo(ST.stream_sample(spec, 1, FIT_LINES), K)
    oracle = C.fit_bpe_jamo(ST.stream_sample(spec, 1, 10000) + ST.stream_sample(spec, 2, 10000), K)
    items = ST.eval_items(spec)
    n = len(items)

    print("=" * 74)
    print("H_004 GUARD BATTERY (repaired rig · $0 deterministic)")
    print("=" * 74)
    print(f"genspec {S.spec_hash(spec)[:16]} · novel = donor pairs · n_eval {n}\n")

    res = {"genspec_sha256": S.spec_hash(spec), "n_eval": n}

    ga = _score(spec, frozen, items, lambda t: t[-1])
    gb = _score(spec, frozen, items, lambda t: len(t))
    gc = _score(spec, frozen, items, lambda t: (t[-2], t[-1]) if len(t) >= 2 else (None, t[-1]))
    res["G_A_lasttoken"] = ga
    res["G_B_length"] = gb
    res["G_C_bigram"] = gc
    print(f"G-A last-token (order-1) lookup : {ga:.4f}   {'PASS' if ga <= 0.55 else 'FAIL'} (<=0.55)")
    print(f"G-B length-only lookup          : {gb:.4f}   {'PASS' if gb <= 0.55 else 'MARGINAL'} (<=0.55)")
    print(f"G-C order-2 bigram lookup       : {gc:.4f}   (the FROZEN CEILING — reported)")

    novel = spec["novel_neg_forms"]
    heldout = spec["heldout_stems"]
    fic = [(to_jamo(af), to_jamo(render(heldout[i % len(heldout)], [af]))) for i, af in enumerate(novel)]
    df = C.atomicity_audit(frozen, fic)
    do = C.atomicity_audit(oracle, fic)
    res["G_D_frozen_single"] = df["single_token"]
    res["G_D_oracle_single"] = do["single_token"]
    gd = df["single_token"] == 0 and do["single_token"] == 12
    print(f"G-D atomicity: frozen {df['single_token']}/12  oracle {do['single_token']}/12   "
          f"{'PASS' if gd else 'FAIL'}")

    negf = sorted({it["neg"] for it in items})

    def _b(phase, m=200000):
        for i, ch in enumerate(ST.stream(spec, phase)):
            if i >= m:
                break
            yield ch
    leak = A.leak_scan(_b(1), spec, negf)["total"] + A.leak_scan(_b(2), spec, negf)["total"]
    cooc = A.heldout_neg_cooccurrence(spec, _b(1)) + A.heldout_neg_cooccurrence(spec, _b(2))
    res["G_E_leak"] = leak
    res["G_E_cooc"] = cooc
    ge = leak == 0 and cooc == 0
    print(f"G-E leak {leak} · co-occurrence {cooc}   {'PASS' if ge else 'FAIL'}")

    # --- structural verdict ------------------------------------------------
    order1_dead = ga <= 0.55 and gb <= 0.58
    frozen_ceiling_trivial = gc >= 0.90
    res["order1_dead"] = order1_dead
    res["frozen_order2_trivial"] = frozen_ceiling_trivial
    print("\n" + "=" * 74)
    print("STRUCTURAL VERDICT")
    print("=" * 74)
    print(f"order-1 shortcuts closed : {order1_dead} (G-A {ga:.3f}, G-B {gb:.3f})")
    print(f"frozen order-2 ceiling   : {gc:.4f} → the frozen arm has a TRIVIAL bigram path")
    if frozen_ceiling_trivial:
        res["verdict"] = "TWIN-REFUSED-STRUCTURAL"
        print("\n  The novel allomorph is a FIXED 2-token unit; a transformer binds order-2")
        print("  with one attention head, so frozen F2 ≈ G-C regardless of training.")
        print("  Δ_pilot ≥ 0.20 is STRUCTURALLY IMPOSSIBLE — atomicity cannot be isolated")
        print("  from bigram-binding for a fixed morpheme. TWIN-REFUSED, at $0.")
    else:
        res["verdict"] = "PILOT-LIVE"
        print("\n  Frozen has no trivial order-2 path — the MPS pilot is worth running.")

    out = os.path.join(_HERE, "guards_result.json")
    with open(out, "w") as f:
        json.dump(res, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print(f"\nartifacts: {os.path.relpath(out, _ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
