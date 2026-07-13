"""H_9289 C3+C4 GATE readout — frozen pre-registered bars, verbatim (no tune-to-green).

Spec (HYPOTHESES/cards/H_9289_gt_transfer_grounding_install.md + FABLE_C34_RECIPE.md):
  V1      per-arm SEEN P_grid D-acc >= 0.85 (controls included) — a failing arm is INVALID
  GATE-0  representation probe on the hidden dumps: main held-out probe-acc >= 0.65 on BOTH seeds
          AND >= shufGT-probe + 0.10. Frozen protocol = gt_step0_gprobe.py (L2-logreg, l2=5.0,
          800 iters, lr 0.1, standardized; 20x shuffle-label control) reused VERBATIM on reps_*.npz.
  GATE-1  headline = held-out flip0 acc, per-ATOM (29) paired delta = main - shufGT
          bar: delta >= +0.15 on BOTH seeds AND main absolute > 0.55 (a delta, never a raw value)
  GATE-2  only if GATE-1 passes: held-out XOR D-acc, same paired structure, delta >= +0.15
  §6e     ALSO report delta(main - N2rep). A large delta(main-shufGT) with delta(main-N2rep) ~ 0 means
          the shufGT control's contradictory text destroyed learning and inflates the delta
          => INVALID-CTRL.
  negative TOST at delta_eq = 0.10; N_REQ from the observed per-atom variance. A threshold grid must
          never be used to cement a negative.

eval rows carry no `flip` field — they are index-matched against n2_eval_manifest.json heldout[i].
"""

import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
KEEP = os.path.expanduser("~/anima-weights/c34")

MAINS = ("main_s7", "main_s11")
ARMS = MAINS + ("shufGT", "N2rep")

BAR_V1_SEEN = 0.85
BAR_G0_ABS = 0.65
BAR_G0_OVER_CTRL = 0.10
BAR_G1_DELTA = 0.15
BAR_G1_ABS = 0.55
BAR_G2_DELTA = 0.15
DELTA_EQ = 0.10
L2 = 5.0
SEED = 7


def _find(name):
    for d in (KEEP, HERE):
        p = os.path.join(d, name)
        if os.path.exists(p):
            return p
    return None


def load_json(name):
    p = _find(name)
    return json.load(open(p)) if p else None


# ---------------------------------------------------------------- GATE-1 / 2
def join_rows(ev, manifest):
    """Index-match eval rows against the manifest (rows carry no flip/xor field)."""
    items = manifest["heldout"]
    rows = ev["splits"]["heldout"]["rows"]
    if len(rows) != len(items):
        raise SystemExit(f"[FAIL] rows={len(rows)} vs manifest={len(items)} — 정렬 불가, 추측 금지")
    out = []
    for r, m in zip(rows, items):
        if r.get("a") != m.get("a") or r.get("b") != m.get("b"):
            raise SystemExit(f"[FAIL] 키 불일치 {r.get('a')}/{r.get('b')}")
        out.append({**r, "flip": m["flip"], "xor": m["xor"], "atom": m["a"]})
    return out


def per_atom_acc(joined, pred):
    agg = {}
    for r in joined:
        if pred(r):
            agg.setdefault(r["atom"], []).append(1.0 if r.get("d_hit") else 0.0)
    return {a: sum(v) / len(v) for a, v in agg.items() if v}


def _stats(diffs):
    n = len(diffs)
    if n == 0:
        return float("nan"), float("nan"), float("nan"), 0
    mean = sum(diffs) / n
    if n < 2:
        return mean, float("nan"), float("nan"), n
    sd = math.sqrt(sum((d - mean) ** 2 for d in diffs) / (n - 1))
    se = sd / math.sqrt(n)
    t = mean / se if se else (float("inf") if mean else 0.0)
    return mean, se, t, n


def paired(m, c):
    shared = sorted(set(m) & set(c))
    diffs = [m[a] - c[a] for a in shared]
    mean, se, t, n = _stats(diffs)
    return mean, se, t, n, diffs


def tost(diffs, eq=DELTA_EQ):
    """Two one-sided tests — a negative is licensed by equivalence, not by a non-significant t."""
    mean, se, _, _ = _stats(diffs)
    if not se or math.isnan(se):
        return False
    crit = 1.65
    return (mean + eq) / se > crit and (eq - mean) / se > crit


def n_req(diffs, eq=DELTA_EQ, power_t=2.8):
    """Atoms needed to license equivalence at delta_eq, from the observed per-atom SD."""
    _, se, _, n = _stats(diffs)
    if n < 2 or math.isnan(se) or se == 0:
        return float("nan")
    sd = se * math.sqrt(n)
    return math.ceil((power_t * sd / eq) ** 2)


# ------------------------------------------------------------------- GATE-0
def logreg_l2(Xtr, ytr, Xte, l2=L2, iters=800, lr=0.1):
    """VERBATIM from gt_step0_gprobe.py (frozen protocol — never retuned here)."""
    import numpy as np
    mu, sd = Xtr.mean(0), Xtr.std(0) + 1e-6
    Xtr = (Xtr - mu) / sd
    Xte = (Xte - mu) / sd
    n, d = Xtr.shape
    w = np.zeros(d)
    b = 0.0
    yb = ytr.astype("float64")
    for _ in range(iters):
        p = 1.0 / (1.0 + np.exp(-(Xtr @ w + b)))
        w -= lr * (Xtr.T @ (p - yb) / n + l2 * w / n)
        b -= lr * float((p - yb).mean())
    return 1.0 / (1.0 + np.exp(-(Xte @ w + b)))


def gate0_probe(tag):
    import numpy as np
    p = _find(f"reps_{tag}.npz")
    if not p:
        return None
    z = np.load(p, allow_pickle=True)
    X, y, split = z["X"].astype("float64"), z["y"], z["split"]
    tr, te = split == "train", split == "heldout"
    if tr.sum() < 4 or te.sum() < 4:
        return {"error": "atom 부족", "n_tr": int(tr.sum()), "n_te": int(te.sum())}
    acc = float(np.mean((logreg_l2(X[tr], y[tr], X[te]) >= 0.5).astype(int) == y[te]))
    rng = np.random.RandomState(SEED)
    sh = float(np.mean([
        np.mean((logreg_l2(X[tr], rng.permutation(y[tr]), X[te]) >= 0.5).astype(int) == y[te])
        for _ in range(20)
    ]))
    return {"probe_acc": round(acc, 4), "shuffle_acc": round(sh, 4),
            "delta_vs_shuffle": round(acc - sh, 4),
            "n_train_atoms": int(tr.sum()), "n_heldout_atoms": int(te.sum())}


# --------------------------------------------------------------------- main
def main():
    missing = [t for t in ARMS if not _find(f"eval_c34_{t}.json")]
    if missing:
        print(f"[PENDING] 미회수 arm: {', '.join(missing)}")
        sys.exit(3)

    man = load_json("n2_eval_manifest.json")
    print("=" * 78)
    print("H_9289 C3+C4 — GATE readout (동결 사전등록 bar · tune-to-green 금지)")
    print("=" * 78)

    # ---- V1 install validity
    print(f"\n[V1 설치검증] arm 별 SEEN P_grid D-acc >= {BAR_V1_SEEN}")
    v1 = {}
    for t in ARMS:
        ev = load_json(f"eval_seen_c34_{t}.json")
        s = ev["splits"]["heldout"]["summary"] if ev else {"d_acc": float("nan"), "n": 0}
        v1[t] = s["d_acc"]
        print(f"  {t:9s} SEEN={s['d_acc']:.4f} (n={s['n']})  "
              f"{'PASS' if s['d_acc'] >= BAR_V1_SEEN else 'FAIL = INVALID arm'}")
    v1_ok = all(v1[t] >= BAR_V1_SEEN for t in ARMS)

    # ---- GATE-0 representation probe
    print(f"\n[GATE-0 표현-probe] held-out probe-acc >= {BAR_G0_ABS} 양 seed "
          f"AND >= shufGT-probe +{BAR_G0_OVER_CTRL}")
    g0 = {t: gate0_probe(t) for t in ARMS}
    for t in ARMS:
        r = g0[t]
        print(f"  {t:9s} " + ("(reps 미회수)" if r is None else
              f"probe={r.get('probe_acc')} shuffle={r.get('shuffle_acc')} "
              f"delta_sh={r.get('delta_vs_shuffle')} n_te={r.get('n_heldout_atoms')}"))
    ctrl_probe = (g0.get("shufGT") or {}).get("probe_acc")
    g0_pass = bool(ctrl_probe is not None and all(
        (g0.get(t) or {}).get("probe_acc") is not None
        and g0[t]["probe_acc"] >= BAR_G0_ABS
        and g0[t]["probe_acc"] >= ctrl_probe + BAR_G0_OVER_CTRL
        for t in MAINS))
    print(f"  => GATE-0 {'PASS' if g0_pass else 'FAIL'}")

    # ---- GATE-1 headline + §6e control guard
    print(f"\n[GATE-1 헤드라인] held-out flip0 · 원자별 paired Δ · "
          f"bar Δ>=+{BAR_G1_DELTA} 양 seed AND 절대치>{BAR_G1_ABS}")
    f0 = lambda r: r["flip"] == 0
    ctrl = per_atom_acc(join_rows(load_json("eval_c34_shufGT.json"), man), f0)
    n2 = per_atom_acc(join_rows(load_json("eval_c34_N2rep.json"), man), f0)
    ctrl_mean = sum(ctrl.values()) / len(ctrl)
    n2_mean = sum(n2.values()) / len(n2)
    g1 = {}
    for t in MAINS:
        m = per_atom_acc(join_rows(load_json(f"eval_c34_{t}.json"), man), f0)
        d, se, tt, n, diffs = paired(m, ctrl)
        d2, se2, _, _, _ = paired(m, n2)          # §6e guard
        absacc = sum(m.values()) / len(m)
        g1[t] = {"delta_vs_shufGT": d, "se": se, "t": tt, "abs": absacc, "n_atoms": n,
                 "delta_vs_N2rep": d2, "se_n2": se2,
                 "tost_equivalent": tost(diffs), "n_req": n_req(diffs)}
        ok = d >= BAR_G1_DELTA and absacc > BAR_G1_ABS
        print(f"  {t:9s} main={absacc:.4f} shufGT={ctrl_mean:.4f} "
              f"delta={d:+.4f}(se {se:.3f} t {tt:+.2f} n={n})  {'PASS' if ok else 'FAIL'}"
              f"{' · TOST=0' if g1[t]['tost_equivalent'] else ''}"
              f"  · 6e delta(main-N2rep)={d2:+.4f}  N_REQ={g1[t]['n_req']}")
    print(f"  (N2rep flip0 원자평균={n2_mean:.4f})")
    g1_pass = all(g1[t]["delta_vs_shufGT"] >= BAR_G1_DELTA and g1[t]["abs"] > BAR_G1_ABS
                  for t in MAINS)

    invalid_ctrl = all(
        g1[t]["delta_vs_shufGT"] >= BAR_G1_DELTA and abs(g1[t]["delta_vs_N2rep"]) < 0.05
        for t in MAINS)
    if invalid_ctrl:
        print("  [!] 6e INVALID-CTRL — delta(main-shufGT) 는 큰데 delta(main-N2rep)~0 "
              "=> shufGT 모순텍스트가 학습을 파괴해 delta 과대평가")

    # ---- GATE-2
    print("\n[GATE-2 XOR] (GATE-1 통과 시에만 판정)")
    g2 = {}
    if g1_pass and not invalid_ctrl:
        allr = lambda r: True
        cx = per_atom_acc(join_rows(load_json("eval_c34_shufGT.json"), man), allr)
        for t in MAINS:
            m = per_atom_acc(join_rows(load_json(f"eval_c34_{t}.json"), man), allr)
            d, se, tt, n, _ = paired(m, cx)
            g2[t] = {"delta": d, "se": se}
            print(f"  {t:9s} XOR delta={d:+.4f}(se {se:.3f})  "
                  f"{'PASS' if d >= BAR_G2_DELTA else 'FAIL'}")
    else:
        print("  SKIP — 사전등록: GATE-1 통과 시에만")

    n2_acc = load_json("eval_c34_N2rep.json")["splits"]["heldout"]["summary"]["d_acc"]
    print(f"\n[N2rep 재현대조] held-out D-acc={n2_acc:.4f} (N2 원값 0.4770)")

    # ---- verdict per the pre-registered interpretation matrix
    print("\n" + "=" * 78)
    if not v1_ok:
        v = "INVALID — V1 설치 미달 arm 존재 (bar 하향 금지)"
    elif invalid_ctrl:
        v = "INVALID-CTRL (6e) — shufGT 통제군 학습파괴로 delta 과대평가"
    elif not g0_pass:
        v = ("[WALL] GATE-0 FAIL => C3+C4 반증 — 접지 채널은 여전히 data/scale. "
             "합성 XBIND 1.000 = substrate 무죄 상수 · substrate 천장 선언 금지")
    elif not g1_pass:
        eqv = all(g1[t]["tost_equivalent"] for t in MAINS)
        v = ("[WALL] GATE-0 PASS + GATE-1 FAIL"
             + (" (TOST 등가 licensing)" if eqv else " (TOST 미licensing = 검정력 부족·N_REQ 확인)")
             + " => 벽이 grounding -> read-side/register-bridge 로 재국소화 · 렌즈 1개이므로 천장 금지")
    else:
        g2ok = bool(g2) and all(x["delta"] >= BAR_G2_DELTA for x in g2.values())
        v = ("[GREEN] NAT-CRACK (scope: relational-install · nature-only 아님)" if g2ok else
             "[AMBER] GATE-1 PASS + GATE-2 FAIL — grounding 뚫림 · 잔여 벽 = grounded-operand 소비")
    print("VERDICT:", v)
    print("=" * 78)

    out = {"hypothesis": "H_9289",
           "bars": {"v1": BAR_V1_SEEN, "gate0_abs": BAR_G0_ABS,
                    "gate0_over_ctrl": BAR_G0_OVER_CTRL, "gate1_delta": BAR_G1_DELTA,
                    "gate1_abs": BAR_G1_ABS, "gate2_delta": BAR_G2_DELTA, "delta_eq": DELTA_EQ},
           "v1_seen": v1, "gate0": g0, "gate1": g1, "gate2": g2,
           "invalid_ctrl_6e": invalid_ctrl, "n2rep_heldout_dacc": n2_acc,
           "v1_ok": v1_ok, "gate0_pass": g0_pass, "gate1_pass": g1_pass, "verdict": v}
    with open(os.path.join(HERE, "GATE_RESULT.json"), "w") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("→ GATE_RESULT.json")


if __name__ == "__main__":
    main()
