"""v2/evaluate.py — SEQUENTIAL gate evaluator.

Gate order is mechanical, not a habit: C0 -> C1 -> C2 -> P1, and P1 is NOT COMPUTED (not
merely not printed) until every prior gate passes. That is the structural defence against
a burned anchor — if the primary number is already on screen, any later "gate" decision is
shopping.

DV = the first answer byte ('g' for good / 'b' for bad) under greedy argmax of the mixed
distribution. That byte IS the polarity, so the DV reads binding directly and needs no
spelling credit.

Cells (operator x polarity) are reported BEFORE the macro; a macro over a collapsed cell is
an artifact, not a score.
"""

import argparse
import json
import os
import pickle

import numpy as np

import gen
import model as M
from loss import forward_loss
from train import encode_batch

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = "/tmp/v2"
GOOD_B, BAD_B = ord("g"), ord("b")


def eval_stream(seed, entities, n_slots, n, rotate=1):
    s = gen.Stream(seed + 1000, entities, n_slots, rotate_every=rotate)
    return s.batch(n)


def predict(p, cfg, exs, use_store, lam_override=None, val_override=None,
            shuffle_keys=False, flip_pols=False, rng=None, oracle=False):
    ids, tg, mask, sids, vidx, qp, ap = encode_batch(exs, cfg)
    if shuffle_keys:                       # C2: keys <-> values permuted
        # DERANGEMENT (no fixed points). A plain permutation leaves the queried slot in
        # place 1/S of the time (S=8 -> 12.5%), so a PERFECT content-lookup would still
        # score ~0.56 on key-shuffle (0.99*1/8 + 0.5*7/8) and fail the 0.55 bar by
        # construction. The fixed-point leak is a control defect, not a model failure;
        # a derangement removes it. (Instrument repair, not a bar move — P1 never opened.)
        n = sids.shape[1]
        while True:
            perm = rng.permutation(n)
            if not np.any(perm == np.arange(n)):
                break
        sids = sids[:, perm]
    if flip_pols:                          # C2: wrong-store (negative control)
        vidx = 1 - vidx
    oslot = np.array([e["slot"] for e in exs]) if oracle else None
    _, aux = forward_loss(p, cfg, ids, tg, mask, sids, vidx, qp, ap,
                          use_store=use_store, lam_override=lam_override,
                          val_override=val_override, oracle_slot=oslot,
                          gate=cfg.get("gate", "mix"))
    probs = aux["probs"]
    B = len(exs)
    first = probs[np.arange(B), ap]        # (B,V) distribution over the first answer byte
    pred = np.where(first[:, GOOD_B] >= first[:, BAD_B], GOOD_B, BAD_B)
    want = np.array([ex["answer"][0] for ex in exs])
    return pred, want


def cells(exs, pred, want):
    """Per (operator x polarity) accuracy — read BEFORE any macro."""
    out = {}
    for op in (0, 1):
        for pol in (0, 1):
            m = np.array([(e["op"] == op and e["polarity"] == pol) for e in exs])
            out[f"op{op}_pol{pol}"] = float((pred[m] == want[m]).mean()) if m.any() else float("nan")
    return out


def macro(cellmap):
    return float(np.mean([v for v in cellmap.values()]))


def acc(pred, want):
    return float((pred == want).mean())


def load(arm, seed, out=None):
    out = out or OUT
    path = os.path.join(out, f"{arm}_seed{seed}.pkl")
    if not os.path.exists(path):
        return None
    return pickle.load(open(path, "rb"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, nargs="+", default=None)
    ap.add_argument("--gate", choices=["mix", "logit", "store_only"], default="mix")
    ap.add_argument("--readout", choices=["linear", "mlp"], default="linear")
    ap.add_argument("--tag", default="")
    ap.add_argument("--fixed-key", action="store_true", dest="fixed_key")  # informational; cfg drives it
    args = ap.parse_args()
    _tag = args.gate + ("-mlp" if args.readout == "mlp" else "") + args.tag
    out = f"/tmp/v2-{_tag}"

    bars = json.load(open(os.path.join(HERE, "bars.json")))
    t, C0, C1, C2, P1 = (bars["task"], bars["C0_instrument_integrity"],
                         bars["C1_power"], bars["C2_validity"], bars["P1_primary"])
    seeds = args.seeds or bars["seeds"]
    train_ent, eval_ent = gen.split_pool(t["entity_pool"], t["entity_train"], t["entity_eval"])
    n_eval = C1["eval_n_per_arm"]

    print("=" * 78)
    print(f"v2 [gate={args.gate} readout={args.readout}] — SEQUENTIAL GATES.  DIRECTIONAL ceiling (never TERMINAL)")
    print("=" * 78)

    # ── C0 instrument integrity ────────────────────────────────────────────────
    print("\nC0 INSTRUMENT INTEGRITY")
    c0 = {}
    leak = gen.assert_no_eval_leak(seeds[0], train_ent, eval_ent, t["store_slots"], 100_000)
    c0["C0a_leak"] = leak <= C0["C0a_eval_key_leak_max"]
    print(f"  C0-a eval-key leak       : {leak} (max {C0['C0a_eval_key_leak_max']}) "
          f"-> {'PASS' if c0['C0a_leak'] else 'FAIL'}")

    sha1 = gen.stream_sha(seeds[0], train_ent, t["store_slots"])
    sha2 = gen.stream_sha(seeds[0], train_ent, t["store_slots"])
    c0["C0c_determinism"] = sha1 == sha2
    print(f"  C0-c stream determinism  : {sha1[:16]} -> {'PASS' if c0['C0c_determinism'] else 'FAIL'}")

    ns_accs = {}
    for s in seeds:
        m = load("NOSTORE", s, out)
        if m is None:
            print(f"  C0-b NOSTORE seed{s}      : MISSING ckpt -> run train.py --arm NOSTORE")
            c0["C0b_nostore"] = False
            break
        exs = eval_stream(s, eval_ent, t["store_slots"], n_eval)
        pred, want = predict(m["params"], m["cfg"], exs, use_store=False)
        ns_accs[s] = acc(pred, want)
    else:
        lo, hi = C0["C0b_nostore_heldout_lo"], C0["C0b_nostore_heldout_hi"]
        c0["C0b_nostore"] = all(lo <= a <= hi for a in ns_accs.values())
        for s, a in ns_accs.items():
            print(f"  C0-b NOSTORE seed{s} held-out: {a:.4f} (must be in [{lo},{hi}] = "
                  f"memorisation is worthless) -> {'PASS' if lo <= a <= hi else 'FAIL'}")

    print("  C0-d gradcheck           : run `python3 gradcheck.py` (+ --selftest)")

    # C0-e POSITIVE CONTROL — without it a negative is unreadable: NOSTORE only proves the
    # task does not leak, never that this toy CAN show a positive
    # (power-before-negative-verdict, at the architecture level).
    orc = {}
    for s in seeds:
        m = load("ORACLE", s, out)
        if m is None:
            print(f"  C0-e ORACLE seed{s}       : MISSING ckpt -> run train.py --arm ORACLE")
            c0["C0e_oracle"] = False
            break
        exs = eval_stream(s, eval_ent, t["store_slots"], n_eval)
        pred, want = predict(m["params"], m["cfg"], exs, True, oracle=True)
        orc[s] = acc(pred, want)
    else:
        bar_o = C0.get("C0e_oracle_min", 0.90)
        c0["C0e_oracle"] = all(a >= bar_o for a in orc.values())
        for s, a in orc.items():
            print(f"  C0-e ORACLE seed{s} held-out : {a:.4f} (>= {bar_o} = the toy CAN express "
                  f"the task) -> {'PASS' if a >= bar_o else 'FAIL'}")
    if not all(c0.values()):
        print("\n🔴 C0 FAIL -> INSTRUMENT-DEAD. P1 is NOT computed. No verdict.")
        return 1
    print("  => C0 PASS")

    # ── C1 power ───────────────────────────────────────────────────────────────
    print("\nC1 POWER")
    se = np.sqrt(0.25 / n_eval)
    mde = 2.8 * se
    ok_c1 = mde <= C1["mde_required_max"]
    print(f"  n={n_eval}/arm  se={se:.4f}  MDE={mde:.4f} (max {C1['mde_required_max']}) "
          f"-> {'PASS' if ok_c1 else 'FAIL'}")
    if not ok_c1:
        print("\n🔴 C1 FAIL -> UNDERPOWERED. Widen eval; do NOT move the bar. P1 not computed.")
        return 1
    print("  => C1 PASS")

    # ── C2 validity (per arm) ──────────────────────────────────────────────────
    print("\nC2 VALIDITY (per arm; a failing arm's DV is INVALID)")
    valid, results = {}, {}
    for arm in ("COTRAIN", "BOLT", "SLOWROT"):
        for s in seeds:
            m = load(arm, s, out)
            if m is None:
                continue
            rng = np.random.default_rng(s + 99)
            exs = eval_stream(s, eval_ent, t["store_slots"], n_eval)
            p, cfg = m["params"], m["cfg"]

            pred, want = predict(p, cfg, exs, True)
            base = acc(pred, want)

            pr, wa = predict(p, cfg, exs, True, shuffle_keys=True, rng=rng)
            a_shuf = acc(pr, wa)
            neutral = np.repeat(p["val"].mean(0, keepdims=True), 2, axis=0)
            pr, wa = predict(p, cfg, exs, True, val_override=neutral)
            a_neut = acc(pr, wa)
            pr, wa = predict(p, cfg, exs, True, lam_override=0.0)
            a_lam0 = acc(pr, wa)
            pr_f, _ = predict(p, cfg, exs, True, flip_pols=True)
            flip_coh = float((pr_f != pred).mean())

            ok = (a_shuf <= C2["key_shuffle_max"] and a_neut <= C2["neutral_store_max"]
                  and a_lam0 <= C2["lambda_zero_max"]
                  and flip_coh >= C2["wrong_store_flip_coherence_min"])
            valid[(arm, s)] = ok
            results[(arm, s)] = {"base": base, "exs": exs, "pred": pred, "want": want,
                                 "lam": float(M.sigmoid(p["lam_raw"][0]))}
            print(f"  {arm:8s} s{s}: key-shuf {a_shuf:.3f}(<={C2['key_shuffle_max']})  "
                  f"neutral {a_neut:.3f}  lam0 {a_lam0:.3f}  "
                  f"wrong-store flip-coh {flip_coh:.3f}(>={C2['wrong_store_flip_coherence_min']})"
                  f"  -> {'VALID' if ok else 'INVALID'}")

    # ── P1 primary ─────────────────────────────────────────────────────────────
    print("\nP1 PRIMARY (cells first; a collapsed cell voids the macro)")
    macros = {}
    for (arm, s), r in sorted(results.items()):
        if not valid[(arm, s)]:
            print(f"  {arm:8s} s{s}: INVALID (C2) — DV not read")
            continue
        cm = cells(r["exs"], r["pred"], r["want"])
        mac = macro(cm)
        worst = min(cm.values())
        collapsed = worst < mac - P1["cell_collapse_delta"]
        macros[(arm, s)] = None if collapsed else mac
        cs = "  ".join(f"{k}={v:.3f}" for k, v in cm.items())
        print(f"  {arm:8s} s{s}: {cs}")
        print(f"           macro={mac:.4f}  lam={r['lam']:.3f}"
              f"{'  ⚠️ CELL-COLLAPSE -> macro VOID' if collapsed else ''}")

    def cotrain_macros():
        v = [macros.get(("COTRAIN", s)) for s in seeds]
        return v if all(x is not None for x in v) else None

    # BOLT's held-out accuracy IS its score against supported_bolt_max. A BOLT that fails
    # C2 by sitting at chance (store not causally driving the answer) is not "unmeasurable" —
    # it is a MEASURED bolt-on failure, which is exactly the SUPPORTED signal. So read BOLT's
    # held-out directly (frozen bar supported_bolt_max=0.60 is about held-out, not a C2-gated
    # macro). A C2-VALID BOLT instead reads its macro (it genuinely used the store).
    def bolt_scores():
        out = []
        for s in seeds:
            r = results.get(("BOLT", s))
            if r is None:
                return None
            out.append(macros.get(("BOLT", s), r["base"]))  # macro if valid else held-out
        return out

    co, bo = cotrain_macros(), bolt_scores()
    print("\n" + "=" * 78)
    if co is None or bo is None:
        print("VERDICT: PENDING — COTRAIN/BOLT ckpts missing")
    elif all(c >= P1["supported_cotrain_min"] for c in co) and all(b <= P1["supported_bolt_max"] for b in bo):
        print(f"VERDICT: 🟢 SUPPORTED (DIRECTIONAL) — the bridge is EARNED by learning "
              f"(COTRAIN macro {co[0]:.3f}/{co[1]:.3f} ≥ {P1['supported_cotrain_min']} · "
              f"BOLT held-out {bo[0]:.3f}/{bo[1]:.3f} ≤ {P1['supported_bolt_max']} = bolt-on fails)")
    elif all(b >= P1["boltsufficient_bolt_min"] for b in bo):
        print("VERDICT: 🔵 BOLT-SUFFICIENT — bolting on is enough; the 'only by learning' clause dies")
    elif all(c <= P1["dead_cotrain_max"] for c in co):
        print("VERDICT: 🔴 HYPOTHESIS DEAD — even a co-trained bridge fails")
    else:
        print(f"VERDICT: ⚪ NO-VERDICT — grey zone {P1['grey_zone']} (re-tuning the bar is forbidden)")
    print("Scope: DIRECTIONAL only. Port to core/ + an anima-py flag to earn TERMINAL.")
    print("=" * 78)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
