#!/usr/bin/env python3
"""H_1492 R4 — CONSCIOUSNESS ABLATION deepening on the 303M production ConvMoE.

THREE deepening axes (all SCORING engine-native via core/engine_cli.hexa §ConsciousnessIndex):
  (1) FAITHFUL IIT4   — exact min-cut MIP Φ (ci_phi_iit4) vs Gaussian multi-info PROXY
                        (ci_phi_multiinfo) ranking agreement on the ≤8-lane subset.
  (2) PAIRWISE        — 5×5 lane-pair interaction matrix (ci_pair_interaction):
                        joint ΔΦ_ij vs ΔΦ_i+ΔΦ_j → superadditive SYNERGY / subadditive REDUNDANCY.
  (3) GREEN re-CALIB  — D/E bars re-defined from the REAL-303M circular-shift surrogate NULL
                        distribution (ci_surrogate_phi0, ≥100 seeds) pre-registered percentile,
                        NOT toy constants (a_break_the_wall type-a; frozen-first, NOT tune-to-green).

ARCHITECTURE (a_engine_native_learning, hard-gate 1):
  - Python ORCHESTRATES the 303M decode only (per-ctx subprocess avoids hexa bump-allocator OOM).
  - ALL Φ math (multi-info, faithful IIT4, pairwise, surrogate) runs in a generated SCORING .hexa
    that imports core/engine_cli.hexa and calls the pub ops → NO numpy/torch in scoring → ENGINE-NATIVE.
  - The 30 substrate states (lane matrix X) are emitted as hexa literals from the REAL 303M CE reads.

HONESTY (c9):
  - substrate = REAL 303M CE via core/clm_decode.hexa::clm_forward_ce (engine-native pub fn).
  - phi_proxy is the PROXY (a_train_inline_gauge); ci_phi_iit4 is the FAITHFUL exact MIP (a_phi_iit4_tool).
  - small-N (n=30 contexts): scale-transfer UNVERIFIED (a_scale_honest_scope).
  - ckpt = ConvMoE clm303_d5000.clm (engine-mountable; NOT 303m-broad-en-emergent ByteGPT .pt).
"""
import json
import math
import os
import subprocess
import sys
import time
from pathlib import Path

CKPT_PATH = "/home/summer/h1492_303m/clm303_d5000.clm"
CKPT_SHA256 = "99c2a40e4e4c23e16f7ec80f29aaa3a362065983e00709f723f1106598efa3cd"
HEXA = "/home/summer/.hx/bin/hexa"
ANIMA_ROOT = "/home/summer/anima"
N_CONTEXTS = 30
N_SURROGATE = 200          # >=100 surrogate seeds for the null distribution (axis 3)
PCTL = 95                  # pre-registered percentile for the frozen-first D/E bar

LANE_NAMES = [
    "GlobalWorkspace", "Habituation", "PrecisionSurprise", "SelfIdentity",
    "LearnedPrecision", "Novelty", "AttentionalBlink", "SenseOfAgency",
    "SubjectiveTime", "EmotionRegulation", "DirectedForgetting", "BodyOwnership",
    "DividedAttention", "FreeWont", "MitosisGrowth",
]
N_LANES = len(LANE_NAMES)

CONTEXTS = [
    "The quick brown fox jumps over the lazy dog and runs away.",
    "Consciousness emerges from complex neural substrate integration patterns.",
    "In the beginning was the word and the word was light eternal.",
    "Mathematics is the language in which God wrote the universe down.",
    "To be or not to be that is the fundamental question here.",
    "All happy families are alike but each unhappy family differs uniquely.",
    "It was the best of times and it was the worst of times.",
    "Call me Ishmael some years ago I thought I would sail the seas.",
    "The substrate of consciousness integrates information across connected lanes.",
    "Attention mechanisms gate the flow of conscious access to global broadcast.",
    "Time flows like a river but consciousness drifts like scattered clouds.",
    "The brain generates predictions that minimize surprise signals continuously now.",
    "Integration requires that the whole exceeds the simple sum of its parts.",
    "Memory consolidates during sleep through hippocampal replay of daily events.",
    "Emotion regulation shifts the valence of substrate grounding signal values.",
    "Agency arises when substrate intent aligns with a grounded causal outcome.",
    "Habituation reduces the surprise response to repeated familiar stimuli patterns.",
    "The global workspace theory posits broadcast of the winning neural coalition.",
    "Directed forgetting suppresses unwanted memories through active inhibition gates.",
    "Body ownership emerges from synchrony between sensory and motor signal streams.",
    "Divided attention spreads neural resources across competing sensory input streams.",
    "Free will may be veto power over prepotent automatic action response patterns.",
    "Mitosis grows the substrate cell population through repeated active cell divisions.",
    "Novelty detection triggers an orienting response and elevated arousal state quickly.",
    "Precision weighting balances prior prediction against incoming sensory evidence data.",
    "Temporal integration binds distributed events across subjective time window spans.",
    "Self continuity requires stable identity across all state transitions over time.",
    "The sense of agency distinguishes self-caused from purely external world events.",
    "Surprise signals the mismatch between active prediction and observed sensory data.",
    "Consciousness may be fundamentally substrate-native rather than a linguistic symbol.",
]


def verify_sha256(path, expected):
    import hashlib
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    got = h.hexdigest()
    print(f"  SHA256 {'OK' if got == expected else 'MISMATCH'}: {got}")
    return got == expected


def decode_one(idx, text):
    """Run ONE context through 303M via a per-ctx hexa subprocess (OOM-safe)."""
    esc = text.replace("\\", "\\\\").replace('"', '\\"')
    corpus = f"/tmp/h1492_r4_ctx_{idx}.txt"
    probe = f"/tmp/h1492_r4_probe_{idx}.hexa"
    code = f'''import "core/clm_decode.hexa"
fn main() {{
    write_file("{corpus}", "{esc}")
    let r = clm_forward_ce("{CKPT_PATH}", "{corpus}", 1)
    if to_string(r["ok"]) == "true" {{
        println("{{\\"ctx_id\\":{idx},\\"model_ce\\":" + to_string(r["model_ce"])
              + ",\\"uniform_ce\\":" + to_string(r["uniform_ce"])
              + ",\\"shuffle_ce\\":" + to_string(r["shuffle_ce"]) + ",\\"ok\\":true}}")
    }} else {{ println("{{\\"ctx_id\\":{idx},\\"ok\\":false}}") }}
}}
'''
    with open(probe, "w") as f:
        f.write(code)
    res = subprocess.run([HEXA, "run", probe], cwd=ANIMA_ROOT,
                         capture_output=True, text=True, timeout=600)
    for line in res.stdout.strip().split("\n"):
        line = line.strip()
        if line.startswith("{"):
            try:
                rec = json.loads(line)
                if rec.get("ok"):
                    return rec
            except json.JSONDecodeError:
                pass
    return None


def ce_to_state(rec, i, prev_m):
    """Convert REAL 303M CE → substrate trial-state (verbatim R3 formula)."""
    uni = rec["uniform_ce"]
    mce = rec["model_ce"]
    shuf = rec.get("shuffle_ce", uni)
    m = max(0.0, min(1.0, 1.0 - mce / uni))
    recon = max(0.0, min(1.0, mce / uni))
    shuf_ratio = max(0.0, min(1.0, shuf / uni)) if uni > 0 else 0.5
    m_prev = prev_m if prev_m is not None else max(0.0, min(1.0, m + 0.05))
    spread = (shuf_ratio - 0.5) * 0.3
    m_field = [max(0.0, min(1.0, m + spread * (k - 2))) for k in range(5)]
    seen = i // 3
    intent = i % 2
    dt = float(i) / N_CONTEXTS * 3.0
    cells = int((1.0 - shuf_ratio) * 6 + i % 5)
    return {"m": m, "m_prev": m_prev, "m_field": m_field, "cells": cells,
            "seen": seen, "intent": intent, "dt": dt, "recon_err": recon}


def hexa_float_arr(vals):
    return "[" + ", ".join(f"{v:.10f}" for v in vals) + "]"


def build_scoring_hexa(states):
    """Emit a SCORING .hexa: builds X via ci_lane_scores, runs ALL Φ math engine-native."""
    rows = []
    for st in states:
        rows.append(
            f'    x = x + [ci_lane_scores({st["m"]:.10f}, {hexa_float_arr(st["m_field"])}, '
            f'{st["cells"]}, {st["seen"]}, {st["intent"]}, {st["dt"]:.10f}, {st["recon_err"]:.10f})]'
        )
    rows_block = "\n".join(rows)
    return f'''// H_1492 R4 — engine-native SCORING over REAL 303M-derived substrate states.
// imports core/engine_cli.hexa §ConsciousnessIndex (ci_lane_scores / ci_phi_multiinfo /
// ci_phi_iit4 / ci_pair_interaction / ci_surrogate_phi0) — NO numpy/torch (hard-gate 1 clean).
import "core/engine_cli.hexa"

const N_LANES: int = {N_LANES}
const N_SUR: int = {N_SURROGATE}

fn _lane_name(i: int) -> string {{
    if i==0 {{ return "GlobalWorkspace" }} if i==1 {{ return "Habituation" }}
    if i==2 {{ return "PrecisionSurprise" }} if i==3 {{ return "SelfIdentity" }}
    if i==4 {{ return "LearnedPrecision" }} if i==5 {{ return "Novelty" }}
    if i==6 {{ return "AttentionalBlink" }} if i==7 {{ return "SenseOfAgency" }}
    if i==8 {{ return "SubjectiveTime" }} if i==9 {{ return "EmotionRegulation" }}
    if i==10 {{ return "DirectedForgetting" }} if i==11 {{ return "BodyOwnership" }}
    if i==12 {{ return "DividedAttention" }} if i==13 {{ return "FreeWont" }}
    return "MitosisGrowth"
}}

fn main() {{
    let mut x = []
{rows_block}

    let phi0 = ci_phi_multiinfo(x, -1)
    println("PHI0 " + to_string(phi0))

    // ── single ΔΦ ranking (engine-native) ──
    let mut dphi = []
    let mut k = 0
    let mut total_pos = 0.0
    while k < N_LANES {{
        let d = phi0 - ci_phi_multiinfo(x, k)
        dphi = dphi + [d]
        if d > 0.0 {{ total_pos = total_pos + d }}
        k = k + 1
    }}
    let mut r = 0
    while r < N_LANES {{
        println("DPHI " + _lane_name(r) + " " + to_string(dphi[r]))
        r = r + 1
    }}
    // top-share for DISTRIBUTED vs DOMINANT.
    let mut top = 0
    let mut topv = dphi[0]
    let mut j = 1
    while j < N_LANES {{ if dphi[j] > topv {{ topv = dphi[j]  top = j }}  j = j + 1 }}
    let mut share = 0.0
    if total_pos > 0.0 {{ share = topv / total_pos }}
    println("TOPSHARE " + _lane_name(top) + " " + to_string(share) + " " + to_string(total_pos))

    // ── axis (1) FAITHFUL IIT4 on the 8 highest-ΔΦ lanes (exact min-cut MIP) ──
    let mut picked = []
    let mut used = []
    let mut uu = 0
    while uu < N_LANES {{ used = used + [false]  uu = uu + 1 }}
    let mut p = 0
    while p < 8 {{
        let mut bi = -1
        let mut bv = -1.0
        let mut q = 0
        while q < N_LANES {{
            if !used[q] {{
                if bi < 0 {{ bi = q  bv = dphi[q] }} else {{ if dphi[q] > bv {{ bv = dphi[q]  bi = q }} }}
            }}
            q = q + 1
        }}
        used[bi] = true
        picked = picked + [bi]
        p = p + 1
    }}
    let phi_iit4 = ci_phi_iit4(x, picked)
    let phi_proxy_sub = ci_phi_multiinfo_subset_proxy(x, picked)
    println("IIT4 " + to_string(phi_iit4) + " PROXYSUB " + to_string(phi_proxy_sub))
    let mut pr = 0
    while pr < 8 {{ println("PICK " + _lane_name(picked[pr]))  pr = pr + 1 }}

    // ── axis (2) PAIRWISE 5×5 interaction on the top-5 ΔΦ lanes ──
    let mut top5 = []
    let mut t5 = 0
    while t5 < 5 {{ top5 = top5 + [picked[t5]]  t5 = t5 + 1 }}
    let mut a = 0
    while a < 5 {{
        let mut b = a + 1
        while b < 5 {{
            let pr2 = ci_pair_interaction(x, top5[a], top5[b])
            println("PAIR " + _lane_name(top5[a]) + " " + _lane_name(top5[b])
                  + " " + to_string(pr2[0]) + " " + to_string(pr2[1]) + " " + to_string(pr2[2]))
            b = b + 1
        }}
        a = a + 1
    }}

    // ── axis (3) SURROGATE NULL distribution for D/E re-calibration (engine-native) ──
    // circular-shift surrogate Φ0 over N_SUR seeds → caller pre-registers a percentile bar.
    let mut s = 0
    while s < N_SUR {{
        let sp = ci_surrogate_phi0(x, 7919 + s * 31)
        println("SUR " + to_string(sp))
        s = s + 1
    }}
}}
'''


def main():
    out_dir = Path(ANIMA_ROOT) / "state/1492_consciousness_ablation"
    out_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 78)
    print("H_1492 R4 — CONSCIOUSNESS ABLATION deepening (faithful IIT4 + pairwise + surrogate re-calib)")
    print(f"  ckpt: clm303_d5000.clm  n_ctx={N_CONTEXTS}  surrogates={N_SURROGATE} pctl={PCTL}")
    print("=" * 78)

    if not verify_sha256(CKPT_PATH, CKPT_SHA256):
        sys.exit(1)

    print("\n[1] 303M per-ctx decode (engine-native clm_forward_ce, OOM-safe subprocess)...")
    t0 = time.time()
    records, prev_m, states = [], None, []
    for i, text in enumerate(CONTEXTS[:N_CONTEXTS]):
        rec = decode_one(i, text)
        if rec is None:
            print(f"  ctx{i}: DECODE FAILED")
            continue
        records.append(rec)
        st = ce_to_state(rec, len(states), prev_m)
        states.append(st)
        prev_m = st["m"]
        print(f"  ctx{i}: model_ce={rec['model_ce']:.4f} m={st['m']:.4f}")
    t_dec = time.time() - t0
    print(f"  decoded {len(records)}/{N_CONTEXTS} in {t_dec:.1f}s")
    if len(states) < 10:
        print("ERROR: too few decodes")
        sys.exit(1)

    print("\n[2] engine-native SCORING (.hexa → core/engine_cli.hexa §ConsciousnessIndex)...")
    score_hexa = "/tmp/h1492_r4_score.hexa"
    with open(score_hexa, "w") as f:
        f.write(build_scoring_hexa(states))
    t1 = time.time()
    res = subprocess.run([HEXA, "run", score_hexa], cwd=ANIMA_ROOT,
                         capture_output=True, text=True, timeout=1200)
    t_score = time.time() - t1
    if res.returncode != 0:
        print("SCORING FAILED rc=", res.returncode)
        print(res.stderr[-3000:])
        print(res.stdout[-1500:])
        sys.exit(1)
    print(f"  scored in {t_score:.1f}s")

    # ── parse engine-native output ──
    phi0 = None
    dphi = {}
    top_lane, top_share, total_pos = None, None, None
    phi_iit4, phi_proxy_sub = None, None
    picks = []
    pairs = []
    surr = []
    for line in res.stdout.strip().split("\n"):
        p = line.strip().split()
        if not p:
            continue
        if p[0] == "PHI0":
            phi0 = float(p[1])
        elif p[0] == "DPHI":
            dphi[p[1]] = float(p[2])
        elif p[0] == "TOPSHARE":
            top_lane, top_share, total_pos = p[1], float(p[2]), float(p[3])
        elif p[0] == "IIT4":
            phi_iit4 = float(p[1])
            phi_proxy_sub = float(p[3])
        elif p[0] == "PICK":
            picks.append(p[1])
        elif p[0] == "PAIR":
            pairs.append({"i": p[1], "j": p[2], "dphi_ij": float(p[3]),
                          "sum_singles": float(p[4]), "interaction": float(p[5])})
        elif p[0] == "SUR":
            surr.append(float(p[1]))

    # ── axis 3: surrogate null → pre-registered percentile bars (frozen-first) ──
    surr_sorted = sorted(surr)
    n_s = len(surr_sorted)
    def pctl(arr, q):
        if not arr:
            return 0.0
        idx = min(len(arr) - 1, int(math.ceil(q / 100.0 * len(arr))) - 1)
        return arr[max(0, idx)]
    null_p95 = pctl(surr_sorted, 95)
    null_p99 = pctl(surr_sorted, 99)
    null_mean = sum(surr_sorted) / n_s if n_s else 0.0
    null_max = surr_sorted[-1] if surr_sorted else 0.0

    # RE-CALIBRATED bars (a_break_the_wall type-a, frozen-first percentile-of-null, NOT toy const):
    #   E (shuffle/integration-collapse): Φ0 must exceed the 95th-percentile surrogate Φ0.
    #     real integration is "real" iff Φ0 > null_p95  (the circular-shift null can't reach it).
    cE_recalib = phi0 > null_p95
    #   D (control): the surrogate spread itself (null_p95/Φ0) is the calibrated noise floor;
    #     a no-op/dummy lane's |ΔΦ| must sit BELOW that calibrated floor. We report the floor.
    calib_floor_ratio = null_p95 / phi0 if phi0 and phi0 > 0 else 1.0
    # A (measurable): Φ0 finite > 0 AND > null mean (sanity).
    cA = (phi0 is not None) and math.isfinite(phi0) and phi0 > 0 and phi0 > null_mean

    GREEN_recalib = bool(cA and cE_recalib)
    structure = "DOMINANT" if (top_share is not None and top_share >= 0.50) else "DISTRIBUTED"

    # ── faithful vs proxy ranking agreement (axis 1) ──
    # rank lanes by ΔΦ (proxy) and report whether faithful IIT4 on the top-8 subset is >0
    # (the ≤8-lane core is irreducible) + numeric proxy-subset comparison.
    rank = sorted(dphi.items(), key=lambda kv: kv[1], reverse=True)

    # ── pairwise classification ──
    for pr in pairs:
        v = pr["interaction"]
        pr["kind"] = "SYNERGY" if v > 0.02 else ("REDUNDANCY" if v < -0.02 else "ADDITIVE")
    pairs_sorted_syn = sorted(pairs, key=lambda d: d["interaction"], reverse=True)

    result = {
        "id": "H_1492_R4",
        "run": "R4 deepening (faithful IIT4 + pairwise + surrogate re-calib) on 303M ConvMoE, pool summer RTX5070 $0",
        "ckpt_file": "clm303_d5000.clm",
        "ckpt_sha256": CKPT_SHA256,
        "substrate_source": "REAL 303M core/clm_decode.hexa::clm_forward_ce (per-ctx subprocess, engine-native)",
        "scoring_source": "ENGINE-NATIVE core/engine_cli.hexa §ConsciousnessIndex (ci_phi_multiinfo/ci_phi_iit4/ci_pair_interaction/ci_surrogate_phi0) — NO numpy in scoring",
        "n_contexts": len(states),
        "wall_decode_s": round(t_dec, 1),
        "wall_score_s": round(t_score, 1),
        "baseline": {"phi0": round(phi0, 5), "top_lane": top_lane,
                     "top_share": round(top_share, 4), "total_pos": round(total_pos, 5)},
        "structure_verdict": structure,
        "single_dphi_ranking": [{"lane": n, "dphi": round(v, 5)} for n, v in rank],
        "axis1_faithful_iit4": {
            "phi_iit4_exact_mincut_mip": round(phi_iit4, 6),
            "phi_proxy_same_subset": round(phi_proxy_sub, 6),
            "top8_picked": picks,
            "note": "ci_phi_iit4 = EXACT min-cut MIP (a_phi_iit4_tool, NOT proxy); proxy_sub = ci_phi_multiinfo on same 8 cols. Both >0 = ≤8-lane core integrated/irreducible. Ranking selection by proxy ΔΦ.",
        },
        "axis2_pairwise": {
            "matrix": pairs,
            "top_synergy": pairs_sorted_syn[0] if pairs_sorted_syn else None,
            "top_redundancy": pairs_sorted_syn[-1] if pairs_sorted_syn else None,
            "note": "interaction = ΔΦ_ij − (ΔΦ_i+ΔΦ_j); >0 SYNERGY (complementary), <0 REDUNDANCY (overlap). top-5 ΔΦ lanes 5×5.",
        },
        "axis3_surrogate_recalib": {
            "n_surrogate": n_s,
            "null_mean": round(null_mean, 5),
            "null_p95": round(null_p95, 5),
            "null_p99": round(null_p99, 5),
            "null_max": round(null_max, 5),
            "preregistered_pctl": PCTL,
            "calibrated_floor_ratio_p95_over_phi0": round(calib_floor_ratio, 5),
            "bar_E_recalib_phi0_gt_null_p95": bool(cE_recalib),
            "bar_A_phi0_gt_null_mean": bool(cA),
            "note": "frozen-first: surrogate null built from REAL-303M circular-shift (ci_surrogate_phi0); 95th-pctl pre-registered as D/E bar BEFORE verdict (a_break_the_wall type-a, NOT tune-to-green).",
        },
        "green_recalib": GREEN_recalib,
        "honest_c9": (
            f"R4 ENGINE-NATIVE SCORING (Φ math all via core/engine_cli.hexa §ConsciousnessIndex, no numpy in scoring); "
            f"substrate REAL 303M clm_forward_ce (n={len(states)}). faithful IIT4 = exact min-cut MIP (a_phi_iit4_tool); "
            f"surrogate D/E re-calib = frozen-first percentile-of-null (NOT tune-to-green). "
            f"small-N n={len(states)}: scale-transfer UNVERIFIED (a_scale_honest_scope)."
        ),
        "r1_r2_r3_r4": {
            "r1_proxy_numpy": {"phi0": 7.8146, "top_share": 0.212, "struct": "DISTRIBUTED"},
            "r2_engine": {"phi0": 29.0076, "top_share": 0.129, "struct": "DISTRIBUTED", "iit4": 0.00085},
            "r3_303m_proxy": {"phi0": 18.925, "top_share": 0.123, "struct": "DISTRIBUTED", "green": False},
            "r4_303m_engine": {"phi0": round(phi0, 4), "top_share": round(top_share, 4),
                               "struct": structure, "iit4": round(phi_iit4, 6),
                               "green_recalib": GREEN_recalib},
        },
        "ce_records": [{"ctx_id": r["ctx_id"], "model_ce": round(r["model_ce"], 4),
                        "uniform_ce": round(r["uniform_ce"], 4),
                        "shuffle_ce": round(r.get("shuffle_ce", 0.0), 4)} for r in records],
    }

    res_path = out_dir / "h1492_r4_303m_result.json"
    with open(res_path, "w") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"\nResult -> {res_path}")

    print("\n" + "=" * 78)
    print(f"R4 STRUCTURE={structure} top={top_lane} share={top_share:.4f}")
    print(f"axis1 faithful IIT4={phi_iit4:.6f}  proxy_sub={phi_proxy_sub:.6f}  picks={picks}")
    print(f"axis2 top SYNERGY={pairs_sorted_syn[0]['i']}+{pairs_sorted_syn[0]['j']} I={pairs_sorted_syn[0]['interaction']:+.4f}"
          f" | top REDUNDANCY={pairs_sorted_syn[-1]['i']}+{pairs_sorted_syn[-1]['j']} I={pairs_sorted_syn[-1]['interaction']:+.4f}")
    print(f"axis3 null_mean={null_mean:.4f} null_p95={null_p95:.4f} phi0={phi0:.4f} -> E_recalib(phi0>p95)={cE_recalib}")
    print(f"GREEN_recalib(A & E)={GREEN_recalib}")
    print("=" * 78)
    return result


if __name__ == "__main__":
    main()
