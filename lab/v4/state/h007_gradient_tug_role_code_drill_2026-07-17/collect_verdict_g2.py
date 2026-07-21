#!/usr/bin/env python3
"""H_007 mech-5 G-2 verdict collector — reads g2_result_full.json, applies the FROZEN falsifiers
(2026-07-17), emits SUPPORTED / PARTIAL / FALSIFIED / DEAD / INCONCLUSIVE ($0, deterministic).

Gate order (a fail short-circuits):
  precond : drill fit — f1(A-tug) ≥ 0.85 both seeds (F2 liveness), else measurement DEAD.
  harness : f2(C-perm) ∈ [0.45,0.55] both, else HARNESS BROKEN.
  F3      : f2(C-scaf) < 0.60 both, else the two-head scaffold alone leaks ⇒ NO VERDICT.
  P-conflict : differential cos∇ vs C-dup (A-tug cos_mean_early below C-dup by ≥ τ=0.05) both seeds —
               else any green is scoped to auxiliary transfer (mechanism claim NOT written, K4).
  F4      : A-tug role-code eff-rank ≥ 2 both seeds, else 1-bit seam (v1 death) ⇒ DEAD.
  F5      : A-tug Δd_acc(projF4) ≥ 0.05 both AND specificity (Δd_acc(projRand) < 0.05, C-dup projF4 inert)
            — else the code is epiphenomenal ⇒ DEAD.
  F6      : d_acc(A-tug) − d_acc(C-shuf) ≥ 0.05 both, else "any hard second task" ⇒ PARTIAL.
  F1      : Δ = d_acc(A-tug,f2) − d_acc(C-dup,f2). SUPPORTED iff ≥0.15 both; DEAD iff <0.05 both; else PARTIAL.
  seed-spread: a SPLIT across seeds (one ≥0.15, other <0.05) ⇒ INCONCLUSIVE-CONSOLIDATE (no 3rd-seed fishing).
"""
from __future__ import annotations

import json
import os

_HERE = os.path.dirname(os.path.abspath(__file__))
_R = os.path.join(_HERE, "g2_result_full.json")
TAU = 0.05


def _get(res, arm, seed, key="f2_dacc"):
    return res.get(f"{arm}.s{seed}", {}).get(key)


def main() -> int:
    if not os.path.exists(_R):
        print(f"NO RESULT YET — {_R} missing. Run train_g2.py first.")
        return 2
    data = json.load(open(_R, encoding="utf-8"))
    res = data["results"]
    seeds = sorted({int(k.split(".s")[1]) for k in res})

    per = {}
    for s in seeds:
        atug = _get(res, "A-tug", s); cdup = _get(res, "C-dup", s)
        cshuf = _get(res, "C-shuf", s); cscaf = _get(res, "C-scaf", s); cperm = _get(res, "C-perm", s)
        live = _get(res, "A-tug", s, "f1_dacc")
        at_cos = _get(res, "A-tug", s, "cos_mean_early"); cd_cos = _get(res, "C-dup", s, "cos_mean_early")
        f4 = res.get(f"A-tug.s{s}", {}).get("F4", {})
        f5 = res.get(f"A-tug.s{s}", {}).get("F5", {})
        cdup_f5 = res.get(f"C-dup.s{s}", {}).get("F5", {})
        per[s] = {
            "F1_delta": None if (atug is None or cdup is None) else round(atug - cdup, 4),
            "A_tug": atug, "C_dup": cdup, "C_shuf": cshuf, "C_scaf": cscaf, "C_perm": cperm,
            "liveness_f1": live,
            "Pconflict_diff": None if (at_cos is None or cd_cos is None) else round(cd_cos - at_cos, 4),
            "F4_effrank_ge2": f4.get("effrank_ge2"), "F4_probe_subj": f4.get("probe_subj"),
            "F4_probe_obj": f4.get("probe_obj"), "F4_cos_dirs": f4.get("cos_dirs"),
            "F5_delta_projF4": f5.get("delta_projF4"), "F5_delta_projRand": f5.get("delta_projRand"),
            "F5_cdup_delta_projF4": cdup_f5.get("delta_projF4"),
            "F6_delta": None if (atug is None or cshuf is None) else round(atug - cshuf, 4),
        }

    def alls(p):
        return all(p(per[s]) for s in seeds)

    precond_ok = alls(lambda r: r["liveness_f1"] is not None and r["liveness_f1"] >= 0.85)
    harness_bad = any(per[s]["C_perm"] is not None and not (0.45 <= per[s]["C_perm"] <= 0.55) for s in seeds)
    f3_leak = any(per[s]["C_scaf"] is not None and per[s]["C_scaf"] >= 0.60 for s in seeds)
    pconf_ok = alls(lambda r: r["Pconflict_diff"] is not None and r["Pconflict_diff"] >= TAU)
    f4_ok = alls(lambda r: r["F4_effrank_ge2"] is True)
    f5_ok = alls(lambda r: r["F5_delta_projF4"] is not None and r["F5_delta_projF4"] >= 0.05
                 and (r["F5_delta_projRand"] is None or r["F5_delta_projRand"] < 0.05)
                 and (r["F5_cdup_delta_projF4"] is None or r["F5_cdup_delta_projF4"] < 0.05))
    f6_ok = alls(lambda r: r["F6_delta"] is not None and r["F6_delta"] >= 0.05)
    deltas = [per[s]["F1_delta"] for s in seeds if per[s]["F1_delta"] is not None]
    f1_supported = bool(deltas) and all(d >= 0.15 for d in deltas)
    f1_dead = bool(deltas) and all(d < 0.05 for d in deltas)
    f1_split = bool(deltas) and any(d >= 0.15 for d in deltas) and any(d < 0.05 for d in deltas)

    if not precond_ok:
        verdict = "DEAD (F2 liveness) — f1(A-tug) < 0.85; the drill did not fit, measurement invalid"
    elif harness_bad:
        verdict = "HARNESS BROKEN — f2(C-perm) outside [0.45,0.55]; permuted-gold arm did not collapse to chance"
    elif f3_leak:
        verdict = "NO VERDICT (F3) — f2(C-scaf) ≥ 0.60; the two-head scaffold alone answers, field not isolable"
    elif not pconf_ok:
        verdict = ("K4 (P-conflict absent) — no differential gradient conflict vs C-dup (< τ=0.05); any A-tug "
                   "gain is auxiliary transfer, NOT tension — the mechanism/thinking claim is NOT written")
    elif f1_dead:
        verdict = "FALSIFIED (F1 DEAD) — Δd_acc(A-tug−C-dup) < 0.05 both seeds; the conflict buys nothing (K2, OMEGA-consistent red)"
    elif f1_split:
        verdict = "INCONCLUSIVE-CONSOLIDATE — F1 SPLIT across seeds (H_003 seed-spread trap); NO third-seed fishing"
    elif not f4_ok:
        verdict = "DEAD (F4 eff-rank) — A-tug role-code eff-rank < 2 (one merged scalar = v1's 1-bit seam)"
    elif not f5_ok:
        verdict = "DEAD (F5 project-out) — stripping the role-code subspace does not move d_acc (or fails specificity); code epiphenomenal"
    elif f1_supported and not f6_ok:
        verdict = "PARTIAL (F6) — F1 ≥ 0.15 both but A-tug − C-shuf < 0.05: 'any hard second task', not role-specific"
    elif f1_supported and f6_ok:
        verdict = ("SUPPORTED — Δd_acc(A-tug−C-dup) ≥ 0.15 both seeds, P-conflict present & role-specific, "
                   "F4 eff-rank ≥ 2, F5 project-out ≥ 0.05 (specific), F6 vs C-shuf ≥ 0.05, F2/F3/harness "
                   "clean. Two irreconcilable objectives on ONE trunk FORCE a recombinable role-code the "
                   "forward objective alone does not build.")
    else:
        verdict = "PARTIAL — F1 Δ between 0.05 and 0.15 (or seed-inconsistent short of the split rule)"

    print("=" * 80 + "\nH_007 mech-5 G-2 verdict — frozen falsifiers on the measured 5-arm run\n" + "=" * 80)
    print(f"seeds: {seeds}  ·  config: {data.get('config')}")
    for s in seeds:
        r = per[s]
        print(f"\n[seed {s}]")
        print(f"  F1 Δ(A-tug−C-dup)={r['F1_delta']}  (A-tug {r['A_tug']} · C-dup {r['C_dup']} · "
              f"C-shuf {r['C_shuf']} · C-scaf {r['C_scaf']} · C-perm {r['C_perm']})")
        print(f"  liveness f1(A-tug)={r['liveness_f1']} · P-conflict diff={r['Pconflict_diff']} (≥{TAU}) · "
              f"F6 Δ={r['F6_delta']} (≥0.05)")
        print(f"  F4 effrank≥2={r['F4_effrank_ge2']} (subj {r['F4_probe_subj']} obj {r['F4_probe_obj']} "
              f"cosdirs {r['F4_cos_dirs']}) · F5 ΔprojF4={r['F5_delta_projF4']} (≥0.05) "
              f"ΔprojRand={r['F5_delta_projRand']} (<0.05) C-dup ΔprojF4={r['F5_cdup_delta_projF4']}")
    print(f"\nprecond={precond_ok} harness_ok={not harness_bad} F3_ok={not f3_leak} Pconf={pconf_ok} "
          f"F4={f4_ok} F5={f5_ok} F6={f6_ok} · F1 deltas={deltas}")
    print("\nVERDICT:", verdict)

    json.dump({"verdict": verdict, "per_seed": per, "precond_ok": precond_ok, "harness_bad": harness_bad,
               "f3_leak": f3_leak, "pconf_ok": pconf_ok, "f4_ok": f4_ok, "f5_ok": f5_ok, "f6_ok": f6_ok,
               "f1_deltas": deltas}, open(os.path.join(_HERE, "verdict_g2.json"), "w"),
              indent=2, ensure_ascii=False)
    print("\nwrote verdict_g2.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
