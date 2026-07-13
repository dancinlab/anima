"""H_9289 C3+C4 GATE readout — frozen pre-registered bars, verbatim (no tune-to-green).

Pre-registration (HYPOTHESES/cards/H_9289_gt_transfer_grounding_install.md):
  V1 install     SEEN P_grid D-acc >= 0.85 (per main arm) -> else INVALID (bar never lowered)
  GATE-1 headline held-out flip0 acc, per-ATOM paired delta = main-GT - ctrl-shufGT
                 bar: delta >= +0.15 on BOTH seeds AND main absolute > 0.55
  GATE-2         only if GATE-1 passes: held-out XOR D-acc, same delta structure, bar >= +0.15
  falsifier      V1 passes (install confirmed) but flip0 delta <= +0.05 on both seeds (TOST-equivalent)
                 => "readout skill does not transfer across atoms"
  negative       TOST with delta_eq = 0.10 (N_REQ fixed pre-fire from N2 variance)

Signal is the DELTA against the shufGT control, never a raw value (measurement meta-law:
FORM tunable / BIND earned). Reads only harvested artifacts; computes nothing on the pods.
"""

import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

ARMS = {
    "main_s7": {"role": "main", "seed": 7},
    "main_s11": {"role": "main", "seed": 11},
    "shufGT": {"role": "control", "seed": 7},
    "N2rep": {"role": "n2_baseline", "seed": 7},
}

BAR_V1_SEEN = 0.85
BAR_G1_DELTA = 0.15
BAR_G1_ABS = 0.55
BAR_G2_DELTA = 0.15
DELTA_EQ = 0.10  # TOST equivalence margin (pre-registered)


def load(tag, seen=False):
    name = f"eval_seen_c34_{tag}.json" if seen else f"eval_c34_{tag}.json"
    path = os.path.join(HERE, name)
    if not os.path.exists(path):
        return None
    with open(path) as f:
        return json.load(f)


def load_manifest(seen=False):
    name = "n2_seen_manifest.json" if seen else "n2_eval_manifest.json"
    path = os.path.join(HERE, name)
    with open(path) as f:
        return json.load(f)


def rows_of(ev, split="heldout"):
    return ev.get("splits", {}).get(split, {}).get("rows", []) if ev else []


def join_rows(ev, manifest, split="heldout"):
    """Align eval rows with manifest items positionally (the evaluator preserves order)
    and attach the item's flip / xor / atom labels."""
    items = manifest.get(split if split in manifest else "heldout", [])
    rows = rows_of(ev, split)
    if len(rows) != len(items):
        raise SystemExit(
            f"[FAIL] row/manifest length mismatch: rows={len(rows)} manifest={len(items)} "
            f"(split={split}) — cannot align, refusing to guess"
        )
    out = []
    for r, m in zip(rows, items):
        if r.get("a") != m.get("a") or r.get("b") != m.get("b"):
            raise SystemExit(f"[FAIL] row/manifest key mismatch at {r.get('a')}/{r.get('b')}")
        out.append({**r, "flip": m.get("flip"), "xor": m.get("xor"), "atom": m.get("a")})
    return out


def per_atom_acc(joined, predicate):
    """Accuracy per atom over items matching the predicate → {atom: acc}."""
    agg = {}
    for r in joined:
        if not predicate(r):
            continue
        agg.setdefault(r["atom"], []).append(1.0 if r.get("d_hit") else 0.0)
    return {a: sum(v) / len(v) for a, v in agg.items() if v}


def paired_t(diffs):
    n = len(diffs)
    if n < 2:
        return float("nan"), float("nan"), float("nan")
    mean = sum(diffs) / n
    var = sum((d - mean) ** 2 for d in diffs) / (n - 1)
    sd = math.sqrt(var)
    se = sd / math.sqrt(n) if sd > 0 else 0.0
    t = mean / se if se > 0 else float("inf") if mean != 0 else 0.0
    return mean, se, t


def tost(diffs, eq=DELTA_EQ):
    """Two one-sided tests: is the paired delta statistically WITHIN +-eq (equivalent to zero)?
    Returns (equivalent: bool, mean, se, t_lower, t_upper). Licensing a negative needs this,
    not a non-significant t (negative-claims-need-tost-not-ns)."""
    mean, se, _ = paired_t(diffs)
    if not se or math.isnan(se):
        return False, mean, se, float("nan"), float("nan")
    t_lo = (mean - (-eq)) / se   # H0: delta <= -eq
    t_hi = (eq - mean) / se      # H0: delta >= +eq
    crit = 1.65  # one-sided ~alpha .05, large-n normal approx
    return (t_lo > crit and t_hi > crit), mean, se, t_lo, t_hi


def main():
    missing = [t for t in ARMS if load(t) is None]
    if missing:
        print(f"[PENDING] 미회수 arm: {', '.join(missing)} — 4/4 회수 후 재실행")
        sys.exit(3)

    man = load_manifest()
    man_seen = load_manifest(seen=True)

    print("=" * 74)
    print("H_9289 C3+C4 — GATE readout (frozen pre-registered bars)")
    print("=" * 74)

    # ---- V1: install validity (SEEN grid) -------------------------------------
    print("\n[V1 설치검증] SEEN P_grid D-acc >= %.2f" % BAR_V1_SEEN)
    v1 = {}
    for tag in ARMS:
        ev = load(tag, seen=True)
        acc = ev["splits"]["heldout"]["summary"]["d_acc"] if ev else float("nan")
        n = ev["splits"]["heldout"]["summary"]["n"] if ev else 0
        v1[tag] = acc
        mark = "PASS" if acc >= BAR_V1_SEEN else "FAIL"
        print(f"  {tag:10s} seen D-acc={acc:.4f} (n={n})  {mark}")
    mains_installed = all(v1[t] >= BAR_V1_SEEN for t in ("main_s7", "main_s11"))
    if not mains_installed:
        print("  ⟹ 양 main 중 설치 미달 → 그리드 INVALID (bar 하향 금지 · N2 전례)")

    # ---- GATE-1: headline held-out flip0, per-atom paired delta vs shufGT ------
    print("\n[GATE-1 헤드라인] held-out flip0 · 원자별 paired Δ(main − shufGT)")
    print(f"  bar: Δ >= +{BAR_G1_DELTA:.2f} 양 seed  ∧  main 절대치 > {BAR_G1_ABS:.2f}")
    ctrl = per_atom_acc(join_rows(load("shufGT"), man), lambda r: r["flip"] == 0)
    g1 = {}
    for tag in ("main_s7", "main_s11"):
        m = per_atom_acc(join_rows(load(tag), man), lambda r: r["flip"] == 0)
        shared = sorted(set(m) & set(ctrl))
        diffs = [m[a] - ctrl[a] for a in shared]
        abs_acc = sum(m[a] for a in shared) / len(shared) if shared else float("nan")
        ctrl_acc = sum(ctrl[a] for a in shared) / len(shared) if shared else float("nan")
        mean, se, t = paired_t(diffs)
        eq, _, _, t_lo, t_hi = tost(diffs)
        g1[tag] = {
            "delta": mean, "se": se, "t": t, "abs": abs_acc, "ctrl": ctrl_acc,
            "n_atoms": len(shared), "tost_equivalent": eq, "diffs": diffs,
        }
        ok = (mean >= BAR_G1_DELTA) and (abs_acc > BAR_G1_ABS)
        print(f"  {tag:10s} main={abs_acc:.4f} shufGT={ctrl_acc:.4f} "
              f"Δ={mean:+.4f} (se={se:.4f} t={t:+.2f} n_atom={len(shared)})  "
              f"{'PASS' if ok else 'FAIL'}"
              f"{'  · TOST≡0(Δ_eq=%.2f)' % DELTA_EQ if eq else ''}")
    gate1_pass = all(
        g1[t]["delta"] >= BAR_G1_DELTA and g1[t]["abs"] > BAR_G1_ABS
        for t in ("main_s7", "main_s11")
    )

    # ---- GATE-2: held-out XOR (only if GATE-1 passed) -------------------------
    print("\n[GATE-2 XOR] (GATE-1 통과 시에만 판정)")
    g2 = {}
    if gate1_pass:
        ctrl_x = per_atom_acc(join_rows(load("shufGT"), man), lambda r: True)
        for tag in ("main_s7", "main_s11"):
            m = per_atom_acc(join_rows(load(tag), man), lambda r: True)
            shared = sorted(set(m) & set(ctrl_x))
            diffs = [m[a] - ctrl_x[a] for a in shared]
            mean, se, t = paired_t(diffs)
            g2[tag] = {"delta": mean, "se": se, "t": t}
            print(f"  {tag:10s} XOR Δ={mean:+.4f} (se={se:.4f})  "
                  f"{'PASS' if mean >= BAR_G2_DELTA else 'FAIL'}")
    else:
        print("  SKIP — GATE-1 미통과 (사전등록: GATE-1 통과 시에만 GATE-2)")

    # ---- N2 replication sanity ------------------------------------------------
    n2 = load("N2rep")
    n2_acc = n2["splits"]["heldout"]["summary"]["d_acc"]
    print(f"\n[N2rep 재현대조] held-out D-acc={n2_acc:.4f} (N2 원값 0.4770 = 연산자 이득 0 재현 확인용)")

    # ---- verdict --------------------------------------------------------------
    print("\n" + "=" * 74)
    if not mains_installed:
        verdict = "INVALID — 설치(V1) 미달, 그리드가 서지 않음 (bar 하향/재해석 금지)"
    elif gate1_pass:
        g2_pass = g2 and all(v["delta"] >= BAR_G2_DELTA for v in g2.values())
        verdict = ("🟢 GATE-1 PASS + GATE-2 PASS — C3+C4 접지 install + XOR 합성 성립"
                   if g2_pass else
                   "🟡 GATE-1 PASS · GATE-2 FLOOR — 벽이 grounding → composition-consumption 으로 재국소화")
    else:
        both_eq = all(g1[t]["tost_equivalent"] for t in ("main_s7", "main_s11"))
        small = all(g1[t]["delta"] <= 0.05 for t in ("main_s7", "main_s11"))
        if both_eq and small:
            verdict = ("🧱 FALSIFIER 발동 — V1 설치 확인에도 flip0 Δ≈0 (TOST 등가 · Δ_eq=%.2f 양 seed): "
                       "'판독 스킬이 원자간 전이되지 않음'" % DELTA_EQ)
        else:
            verdict = ("🔴 GATE-1 FAIL (TOST 등가 미licensing — 검정력 부족 · N_REQ 미달 가능): "
                       "음성 cement 금지, 사전등록 N_REQ 재확인 필요")
    print("VERDICT:", verdict)
    print("=" * 74)

    out = {
        "hypothesis": "H_9289",
        "bars": {"v1_seen": BAR_V1_SEEN, "gate1_delta": BAR_G1_DELTA,
                 "gate1_abs": BAR_G1_ABS, "gate2_delta": BAR_G2_DELTA, "delta_eq": DELTA_EQ},
        "v1_seen_dacc": v1,
        "gate1": {k: {kk: vv for kk, vv in v.items() if kk != "diffs"} for k, v in g1.items()},
        "gate2": g2,
        "n2rep_heldout_dacc": n2_acc,
        "install_ok": mains_installed,
        "gate1_pass": gate1_pass,
        "verdict": verdict,
    }
    with open(os.path.join(HERE, "GATE_RESULT.json"), "w") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("→ GATE_RESULT.json 기록")


if __name__ == "__main__":
    main()
