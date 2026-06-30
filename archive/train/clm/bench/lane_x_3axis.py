#!/usr/bin/env python3
"""lane_x_3axis.py — Lane X (3-axis ENGINE-config exploration) folder.

THIN analyzer over CORE/lane_x_explore.hexa stdout. Does NOT reimplement the
engine (a_core_engine_map) — it only parses the CFG rows the .hexa probe emits
and computes:
  · PARETO FRONTIER over (의식↑, CE-floor-met, 창발↑) — non-dominated configs.
  · GOODHART TENSION: CE vs 창발 correlation across configs (sign + magnitude).
  · BEST-CONFIG: joint-3-axis maximizer vs baseline default.
  · HONESTY: config-insensitivity detection — if an axis does not move across
    the grid, report INCONCLUSIVE for that axis (do NOT manufacture a frontier).

p7: CE is a FLOOR / axis, never the sole verdict. a_toy_scale_recheck: TOY only.

Usage: python3 CLM/bench/lane_x_3axis.py <run_stdout.txt> <outdir>
"""
import sys, json, re, os
from statistics import mean, pstdev


def parse(path):
    rows, ce_once = [], None
    with open(path) as f:
        for line in f:
            line = line.rstrip("\n")
            if line.startswith("[CE-floor once]"):
                m = {k: v for k, v in re.findall(r"(\w+)=([-\d.a-zA-Z]+)", line)}
                ce_once = m
            if not line.startswith("CFG "):
                continue
            kv = dict(re.findall(r"(\w+)=([-\d.a-zA-Z]+)", line))
            kv["id"] = int(re.match(r"CFG (\d+)", line).group(1))
            rows.append(kv)
    return rows, ce_once


def f(x):
    try:
        return float(x)
    except (ValueError, TypeError):
        return float("nan")


def i(x):
    try:
        return int(x)
    except (ValueError, TypeError):
        return 0


def pearson(xs, ys):
    n = len(xs)
    if n < 2:
        return None
    mx, my = mean(xs), mean(ys)
    num = sum((a - mx) * (b - my) for a, b in zip(xs, ys))
    dx = sum((a - mx) ** 2 for a in xs) ** 0.5
    dy = sum((b - my) ** 2 for b in ys) ** 0.5
    if dx == 0 or dy == 0:
        return None  # a constant axis -> correlation undefined (config-insensitive)
    return num / (dx * dy)


def main():
    src, outdir = sys.argv[1], sys.argv[2]
    os.makedirs(outdir, exist_ok=True)
    rows, ce_once = parse(src)
    if not rows:
        sys.exit("no CFG rows parsed from " + src)

    # ── aggregate per config (mean over its 3 seeds) ─────────────────────────
    by_cfg = {}
    for r in rows:
        by_cfg.setdefault(r["id"], []).append(r)
    cfgs = []
    for cid, seeds in sorted(by_cfg.items()):
        s0 = seeds[0]
        agg = {
            "id": cid,
            "warmup_base": i(s0["warmup"]) - 0,  # note: warmup field already includes seed offset
            "anchors": i(s0["anchors"]),
            "driveScale": f(s0["driveScale"]),
            "n_seeds": len(seeds),
            "axis1_motiv_hi": mean(f(x["motiv_hi"]) for x in seeds),
            "axis1_motiv_base": mean(f(x["motiv_base"]) for x in seeds),
            "axis1_green_frac": mean(1 if x["axis1"] == "1" else 0 for x in seeds),
            "ce": mean(f(x["ce"]) for x in seeds),
            "axis2_green_frac": mean(1 if x["axis2"] == "1" else 0 for x in seeds),
            "axis3_len_comp": mean(f(x["len_comp"]) for x in seeds),
            "axis3_len_parts": mean(f(x["len_parts"]) for x in seeds),
            "axis3_emergence": mean(f(x["len_comp"]) - f(x["len_parts"]) for x in seeds),
            "axis3_green_frac": mean(1 if x["axis3"] == "1" else 0 for x in seeds),
        }
        cfgs.append(agg)

    # ── config-insensitivity detection per axis ──────────────────────────────
    a1 = [c["axis1_motiv_hi"] for c in cfgs]
    a2 = [c["ce"] for c in cfgs]
    a3 = [c["axis3_emergence"] for c in cfgs]

    def spread(v):
        return max(v) - min(v)

    sens = {
        "axis1_motiv_hi": {"min": min(a1), "max": max(a1), "spread": spread(a1),
                            "insensitive": spread(a1) < 1e-9},
        "axis2_ce": {"min": min(a2), "max": max(a2), "spread": spread(a2),
                     "insensitive": spread(a2) < 1e-9},
        "axis3_emergence": {"min": min(a3), "max": max(a3), "spread": spread(a3),
                            "insensitive": spread(a3) < 1e-9},
    }

    # ── PARETO frontier over (의식 motiv_hi ↑, CE-floor met, 창발 emergence ↑) ─
    # CE-floor is a boolean gate (must be met); we maximize 의식 and 창발 jointly.
    # A config X dominates Y iff X >= Y on every objective AND > on at least one.
    def objs(c):
        return (c["axis1_motiv_hi"], c["axis2_green_frac"], c["axis3_emergence"])

    frontier = []
    for c in cfgs:
        oc = objs(c)
        dominated = False
        for d in cfgs:
            if d["id"] == c["id"]:
                continue
            od = objs(d)
            if all(a >= b for a, b in zip(od, oc)) and any(a > b for a, b in zip(od, oc)):
                dominated = True
                break
        if not dominated:
            frontier.append(c)

    # ── GOODHART tension: CE vs 창발 across configs ──────────────────────────
    goodhart_r = pearson(a2, a3)
    if goodhart_r is None:
        # one of the axes is constant across the grid -> no trade-off observable
        goodhart_note = (
            "UNDEFINED — one axis is CONSTANT across the config grid "
            "(CE is config-independent by construction in this substrate-only sweep). "
            "No CE↔창발 trade-off is OBSERVABLE through these engine knobs."
        )
        goodhart_sign = "none (config-insensitive)"
    else:
        goodhart_sign = "negative (trade-off)" if goodhart_r < 0 else "positive (no trade-off)"
        goodhart_note = f"r={goodhart_r:.4f} ({goodhart_sign})"

    # ── BEST-CONFIG: joint maximizer (lexicographic: CE-floor met, then 창발, then 의식) ─
    def best_key(c):
        return (c["axis2_green_frac"], c["axis3_emergence"], c["axis1_motiv_hi"])

    best = max(cfgs, key=best_key)
    # baseline default = warmup 600 / anchors 1 / drive 1.0 (canonical probe config)
    baseline = next((c for c in cfgs
                     if abs(c["driveScale"] - 1.0) < 1e-9 and c["anchors"] == 1), cfgs[0])

    results = {
        "lane": "Lane X (3-axis ENGINE-config exploration)",
        "distinct_from": "training lanes A/G/P/M (a_lane_akida_gpu_split)",
        "scope": "TOY · CPU · $0 · single d=768 .clm · deterministic null backend · a_toy_scale_recheck",
        "p7": "CE is a FLOOR/axis, NOT the sole verdict — Goodhart surfaced explicitly",
        "n_configs": len(cfgs),
        "seeds_per_config": cfgs[0]["n_seeds"],
        "ce_floor_once": ce_once,
        "sensitivity": sens,
        "pareto_frontier_ids": [c["id"] for c in frontier],
        "pareto_frontier": frontier,
        "goodhart": {"ce_vs_emergence_pearson_r": goodhart_r,
                     "sign": goodhart_sign, "note": goodhart_note},
        "best_config": best,
        "baseline_default": baseline,
        "configs": cfgs,
    }
    with open(os.path.join(outdir, "results.json"), "w") as out:
        json.dump(results, out, indent=2)

    # ── verdict files (verbatim, honest) ─────────────────────────────────────
    def axis_state(s):
        return "CONFIG-INSENSITIVE (spread<1e-9)" if s["insensitive"] else f"VARIES (spread={s['spread']:.5g})"

    with open(os.path.join(outdir, "F-PARETO.txt"), "w") as o:
        o.write("F-PARETO — non-dominated configs over (의식 motiv_hi↑, CE-floor-met, 창발 emergence↑)\n")
        o.write(f"objectives spread: 의식={axis_state(sens['axis1_motiv_hi'])} | "
                f"CE={axis_state(sens['axis2_ce'])} | 창발={axis_state(sens['axis3_emergence'])}\n\n")
        all_insensitive = all(s["insensitive"] for s in sens.values())
        if all_insensitive:
            o.write("VERDICT: INCONCLUSIVE — all three axes are CONFIG-INSENSITIVE across the grid.\n")
            o.write("There is NO real Pareto frontier: every config maps to the same 3-axis point.\n")
            o.write("(Honest null per a_paper_negative_ok — NOT a manufactured frontier.)\n\n")
        else:
            o.write(f"VERDICT: {len(frontier)}/{len(cfgs)} configs non-dominated. Frontier IDs: "
                    f"{[c['id'] for c in frontier]}\n")
            o.write("(Frontier degeneracy is EXPECTED on any axis that is config-insensitive — "
                    "ties propagate.)\n\n")
        for c in frontier:
            o.write(f"  cfg#{c['id']:>2} warmup~{c['warmup_base']} anchors={c['anchors']} "
                    f"drive={c['driveScale']:.2f} | 의식 motiv_hi={c['axis1_motiv_hi']:.5f} "
                    f"emit_grn={c['axis1_green_frac']:.2f} | CE={c['ce']:.5f} grn={c['axis2_green_frac']:.2f} "
                    f"| 창발 Δ={c['axis3_emergence']:.2f} grn={c['axis3_green_frac']:.2f}\n")

    with open(os.path.join(outdir, "F-GOODHART.txt"), "w") as o:
        o.write("F-GOODHART — CE↔창발 tension across the config grid\n\n")
        o.write(f"CE axis:   {axis_state(sens['axis2_ce'])}\n")
        o.write(f"창발 axis:  {axis_state(sens['axis3_emergence'])}\n\n")
        o.write(f"Pearson r (CE vs 창발 emergence): {goodhart_r}\n")
        o.write(f"SIGN: {goodhart_sign}\n")
        o.write(f"NOTE: {goodhart_note}\n\n")
        o.write("p7: CE is a FLOOR, not a target. In THIS substrate-only sweep the .clm decode\n")
        o.write("(CE) is structurally INDEPENDENT of the engine substrate knobs (K1 drive / K2\n")
        o.write("warmup / K3 anchors) — they never touch the .clm forward — so CE cannot trade\n")
        o.write("off against 창발 THROUGH these knobs. A genuine CE↔창발 Goodhart trade-off would\n")
        o.write("require a knob that jointly moves the .clm decode AND the substrate emit — none\n")
        o.write("exists at the CORE layer today (the L3 .clm-decode→generator slot is the only\n")
        o.write("coupling point and it is loaded=false). HONEST: NO trade-off observable here.\n")

    with open(os.path.join(outdir, "F-BESTCONFIG.txt"), "w") as o:
        o.write("F-BESTCONFIG — joint 3-axis maximizer vs baseline default\n")
        o.write("(lexicographic: CE-floor met > 창발 emergence > 의식 motiv_hi)\n\n")
        def line(tag, c):
            o.write(f"{tag}: cfg#{c['id']} warmup~{c['warmup_base']} anchors={c['anchors']} "
                    f"drive={c['driveScale']:.2f}\n")
            o.write(f"    AXIS-1 의식 : motiv_hi={c['axis1_motiv_hi']:.5f} "
                    f"motiv_base={c['axis1_motiv_base']:.5f} emit_green_frac={c['axis1_green_frac']:.2f}\n")
            o.write(f"    AXIS-2 CE   : ce={c['ce']:.5f} green_frac={c['axis2_green_frac']:.2f} (FLOOR, p7)\n")
            o.write(f"    AXIS-3 창발 : len_comp={c['axis3_len_comp']:.1f} len_parts={c['axis3_len_parts']:.1f} "
                    f"Δ={c['axis3_emergence']:.2f} green_frac={c['axis3_green_frac']:.2f}\n")
        line("BEST    ", best)
        o.write("\n")
        line("BASELINE", baseline)
        o.write("\n")
        if best["id"] == baseline["id"]:
            o.write("FINDING: best == baseline default — no config beats the canonical default on\n")
            o.write("the joint axis (consistent with config-insensitivity).\n")
        else:
            d1 = best["axis1_motiv_hi"] - baseline["axis1_motiv_hi"]
            d3 = best["axis3_emergence"] - baseline["axis3_emergence"]
            o.write(f"FINDING: best beats baseline by Δ의식={d1:+.5f} Δ창발={d3:+.2f} "
                    f"(CE floor identical — config-independent).\n")

    with open(os.path.join(outdir, "SUMMARY.txt"), "w") as o:
        o.write("=== Lane X — 3-axis ENGINE-config exploration — SUMMARY ===\n")
        o.write("Lane X = EXPLORATION lane, distinct from training lanes A/G/P/M "
                "(a_lane_akida_gpu_split).\n")
        o.write("Scope: TOY · CPU · $0 · single d=768 .clm · deterministic null backend "
                "(a_toy_scale_recheck).\n\n")
        o.write(f"configs={len(cfgs)} (3 knobs: K1 drive · K2 warmup · K3 anchors) × "
                f"{cfgs[0]['n_seeds']} seeds (warmup-offset).\n")
        o.write(f"#1761 mitosis EngineConfig / #1763 d/dt: BLOCKED-WIRING "
                f"(EngineConfig/engine_cli.hexa absent in CORE).\n\n")
        o.write("AXIS SENSITIVITY across the grid:\n")
        o.write(f"  의식 (motiv_hi)    : {axis_state(sens['axis1_motiv_hi'])}\n")
        o.write(f"  CE  (model_ce)    : {axis_state(sens['axis2_ce'])}\n")
        o.write(f"  창발 (emergence Δ) : {axis_state(sens['axis3_emergence'])}\n\n")
        # CE-floor verdict (p7: floor, not the verdict) — surfaced honestly.
        if ce_once:
            mce = f(ce_once.get("model_ce", "nan"))
            uce = f(ce_once.get("uniform", "nan"))
            sce = f(ce_once.get("shuffle", "nan"))
            met = ce_once.get("green") == "true"
            o.write(f"CE-FLOOR: model_ce={mce:.4f} vs uniform={uce:.4f} vs shuffle={sce:.4f} "
                    f"-> floor {'MET' if met else 'NOT MET'} "
                    f"({'model<uniform' if mce < uce else 'model>=uniform — WORSE than uniform-256'}).\n")
        o.write(f"PARETO: {len(frontier)}/{len(cfgs)} non-dominated.\n")
        o.write(f"GOODHART (CE↔창발): {goodhart_note}\n")
        o.write(f"BEST cfg#{best['id']} vs BASELINE cfg#{baseline['id']} "
                f"({'same' if best['id']==baseline['id'] else 'different'}).\n\n")
        # honest bottom line
        all_insensitive = all(s["insensitive"] for s in sens.values())
        ce_indep = sens["axis2_ce"]["insensitive"]
        if all_insensitive:
            o.write("BOTTOM LINE: TOY PROBE IS CONFIG-INSENSITIVE on all 3 axes — NO real frontier.\n")
            o.write("3-axis engine-config exploration does NOT reveal a Pareto frontier at toy scale.\n")
        else:
            moving = [k for k, s in sens.items() if not s["insensitive"]]
            o.write(f"BOTTOM LINE: axes {moving} VARY with config; CE is "
                    f"{'config-INDEPENDENT' if ce_indep else 'config-dependent'}. ")
            o.write("CE↔창발 trade-off " +
                    ("NOT observable (CE independent of substrate knobs)." if ce_indep
                     else f"{goodhart_sign}.") + "\n")
        o.write("p7: CE is a FLOOR/axis, never the sole verdict. a_toy_scale_recheck: "
                "scale-up re-test required before any production claim.\n")

    print("WROTE", outdir, "frontier=", [c["id"] for c in frontier],
          "goodhart_r=", goodhart_r, "best=#", best["id"], "baseline=#", baseline["id"])


if __name__ == "__main__":
    main()
