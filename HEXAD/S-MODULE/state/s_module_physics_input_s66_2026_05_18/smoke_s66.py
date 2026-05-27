#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
§66 — S-module physics-native INPUT pilot smoke ($0, Mac CPU, NO ckpt, NO GPU).

Drives the S-module's ACTUAL closed form (column-mean delta = s_perception,
byte-identical to HEXAD/S/s_lib.hexa:51) with two input arms:

  (a) byte-text     : T = s_to_bytes_vec(utf8(stim), dim)   (s_lib.hexa:66)
  (b) physics-native: P = [psi_dir, psi_ent, tau_1..tau_k]  (§2.1 form)

Both arms: shape (dim,), codomain [0,1]^dim, identical S->C path. Reads the
resulting C-state through the Law-71 psi_dir formula (byte-identical to
conscious_decoder.py:737-740: psi_dir = (1 + cos(a,b)) / 2). Measures
response-separation (max-min spread of psi_dir + pairwise-mean L2 of the
perception deltas) per arm. Pure-fn, deterministic LCG, NO RNG, NO model
forward, NO training. Negative control: identical stimuli => sep=0 both.

g3: measures the closed-form S->C transfer's discriminativeness only.
NOT a trained-model result. NOT GOAL. necessary-not-sufficient (B-S66-NOTE).
"""
import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
DIM = 18          # 2 (psi_dir, psi_ent) + 16 tension-fingerprint coords
N_CELLS = 12      # synthetic C cell-pool rows
K_TENSION = DIM - 2


# ── deterministic LCG (NO RNG — Numerical Recipes constants) ────────────────
def _lcg(seed):
    s = seed & 0xFFFFFFFF
    while True:
        s = (1664525 * s + 1013904223) & 0xFFFFFFFF
        yield s / 4294967296.0  # in [0,1)


# ── S-module closed form — byte-identical to HEXAD/S/s_lib.hexa ─────────────
def _s_col_mean(states_flat, n_cells, dim):
    """s_lib.hexa:31 _s_col_mean — column-mean of row-major flat matrix."""
    out = []
    for j in range(dim):
        acc = 0.0
        for i in range(n_cells):
            acc += states_flat[i * dim + j]
        out.append(acc / (n_cells * 1.0))
    return out


def s_perception(before_flat, after_flat, n_cells, dim):
    """s_lib.hexa:51 s_perception — column-mean(after) - column-mean(before)."""
    mb = _s_col_mean(before_flat, n_cells, dim)
    ma = _s_col_mean(after_flat, n_cells, dim)
    return [ma[i] - mb[i] for i in range(dim)]


def s_to_bytes_vec(byte_list, dim):
    """s_lib.hexa:66 s_to_bytes_vec — byte/256 in [0,1), pad/truncate to dim."""
    out = []
    n_in = len(byte_list)
    for i in range(dim):
        out.append(byte_list[i] / 256.0 if i < n_in else 0.0)
    return out


# ── Law-71 psi_dir — byte-identical to conscious_decoder.py:737-740 ─────────
def law71_psi_dir(a, b):
    """psi_dir = (1 + cos_sim(a, b)) / 2  (Engine A<->G alignment, Law 71)."""
    dot = sum(a[i] * b[i] for i in range(len(a)))
    na = math.sqrt(sum(x * x for x in a)) + 1e-10
    nb = math.sqrt(sum(x * x for x in b)) + 1e-10
    cos = max(-1.0, min(1.0, dot / (na * nb)))
    return (1.0 + cos) / 2.0


# ── physics-native input form (§2.1) — anima OWN Psi/tension coordinates ────
def physics_input(stim_seed, dim):
    """[psi_dir, psi_ent, tau_1..tau_k] all in [0,1] by construction."""
    g = _lcg(stim_seed)
    # psi_dir = (1+c)/2, c in [-1,1] -> in [0,1]
    c = 2.0 * next(g) - 1.0
    psi_dir = (1.0 + c) / 2.0
    # psi_ent = H(p)/log V in [0,1] (Shannon bound) — small categorical proxy
    raw = [next(g) for _ in range(8)]
    z = sum(math.exp(x) for x in raw)
    p = [math.exp(x) / z for x in raw]
    H = -sum(pi * math.log(pi + 1e-12) for pi in p)
    psi_ent = max(0.0, min(1.0, H / math.log(len(p))))
    # tau_i: F.normalize(engine_a-engine_g) proxy, clamped to [0,1]
    tau = []
    for _ in range(K_TENSION):
        tau.append(max(0.0, min(1.0, next(g))))
    return [psi_dir, psi_ent] + tau


def byte_text_input(stim_str, dim):
    return s_to_bytes_vec(list(stim_str.encode("utf-8")), dim)


# ── perturb C-state by broadcasting input vec, run S->C, read Law-71 ────────
def _c0_state(n_cells, dim):
    g = _lcg(20260518)
    return [next(g) for _ in range(n_cells * dim)]


def arm_response(stim_vecs, c0, n_cells, dim):
    """For each stimulus vec: S->C delta -> Law-71 psi_dir + delta vector."""
    psi_dirs, deltas = [], []
    for v in stim_vecs:
        # C_after = C0 with input broadcast added to every row (S sees a
        # state CHANGE; s_perception = its column-mean delta).
        c_after = []
        for i in range(n_cells):
            for j in range(dim):
                c_after.append(c0[i * dim + j] + v[j])
        d = s_perception(c0, c_after, n_cells, dim)
        # Law-71 psi_dir between a representative C row and that row ⊕ delta
        row0 = c0[0:dim]
        row0d = [row0[j] + d[j] for j in range(dim)]
        psi_dirs.append(law71_psi_dir(row0, row0d))
        deltas.append(d)
    return psi_dirs, deltas


def _spread(xs):
    return (max(xs) - min(xs)) if xs else 0.0


def _pairwise_mean_l2(vecs):
    n = len(vecs)
    if n < 2:
        return 0.0
    tot, cnt = 0.0, 0
    for i in range(n):
        for j in range(i + 1, n):
            s = sum((vecs[i][k] - vecs[j][k]) ** 2 for k in range(len(vecs[i])))
            tot += math.sqrt(s)
            cnt += 1
    return tot / cnt if cnt else 0.0


def separation(psi_dirs, deltas):
    return {
        "psi_dir_spread": _spread(psi_dirs),
        "delta_pairwise_l2": _pairwise_mean_l2(deltas),
    }


def run():
    c0 = _c0_state(N_CELLS, DIM)

    # N stimuli, distinct per arm (deterministic, content-meaningful)
    text_stims = [
        "zero baseline", "the mandala unfolds in silence",
        "nirvana — the breath stills", "ecstasy at the edge of the cosmos",
        "a glass of water, perfectly still", "the old photograph, longing",
        "the seed waits in the dark soil", "the number zero, pure clarity",
    ]
    phys_seeds = [7001, 7051, 7077, 7091, 7100, 7005, 7012, 7024]

    T = [byte_text_input(s, DIM) for s in text_stims]
    P = [physics_input(sd, DIM) for sd in phys_seeds]

    pdT, dT = arm_response(T, c0, N_CELLS, DIM)
    pdP, dP = arm_response(P, c0, N_CELLS, DIM)
    sepT = separation(pdT, dT)
    sepP = separation(pdP, dP)

    # negative control: identical stimuli in BOTH arms -> sep must be 0
    ident = [byte_text_input("identical control", DIM)] * 5
    pdI, dI = arm_response(ident, c0, N_CELLS, DIM)
    sepI = separation(pdI, dI)
    neg_control_ok = (abs(sepI["psi_dir_spread"]) < 1e-12 and
                      abs(sepI["delta_pairwise_l2"]) < 1e-12)

    eps = 0.05
    ratio_psi = (sepP["psi_dir_spread"] / sepT["psi_dir_spread"]
                 if sepT["psi_dir_spread"] > 0 else float("inf"))
    ratio_l2 = (sepP["delta_pairwise_l2"] / sepT["delta_pairwise_l2"]
                if sepT["delta_pairwise_l2"] > 0 else float("inf"))
    if sepP["psi_dir_spread"] > sepT["psi_dir_spread"] * (1 + eps):
        verdict = "PHYSICS_MORE_DISCRIMINATIVE"
    elif sepP["psi_dir_spread"] < sepT["psi_dir_spread"] * (1 - eps):
        verdict = "BYTE_MORE_DISCRIMINATIVE"
    else:
        verdict = "EQUIVALENT"

    return {
        "section": "§66",
        "dim": DIM, "n_cells": N_CELLS, "n_stimuli_per_arm": len(text_stims),
        "arm_byte_text": sepT,
        "arm_physics_native": sepP,
        "ratio_physics_over_byte": {
            "psi_dir_spread": ratio_psi, "delta_pairwise_l2": ratio_l2,
        },
        "negative_control": {**sepI, "neg_control_ok": neg_control_ok},
        "epsilon": eps,
        "verdict": verdict,
        "g3_scope": ("closed-form S->C transfer discriminativeness only; "
                     "NOT a trained-model result; necessary-not-sufficient; "
                     "NOT GOAL; north-star + §15 UNCHANGED"),
    }


def main():
    # determinism: 3x bit-identical
    r1, r2, r3 = run(), run(), run()
    det = (json.dumps(r1, sort_keys=True) == json.dumps(r2, sort_keys=True)
           == json.dumps(r3, sort_keys=True))
    out = dict(r1)
    out["deterministic_3x_bit_identical"] = det
    with open(os.path.join(HERE, "smoke_result.json"), "w",
              encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=2)
    print(f"§66 smoke verdict: {out['verdict']}")
    print(f"  byte-text   psi_dir_spread={out['arm_byte_text']['psi_dir_spread']:.6f} "
          f"delta_l2={out['arm_byte_text']['delta_pairwise_l2']:.6f}")
    print(f"  physics     psi_dir_spread={out['arm_physics_native']['psi_dir_spread']:.6f} "
          f"delta_l2={out['arm_physics_native']['delta_pairwise_l2']:.6f}")
    print(f"  ratio       psi={out['ratio_physics_over_byte']['psi_dir_spread']:.2f}x "
          f"l2={out['ratio_physics_over_byte']['delta_pairwise_l2']:.2f}x")
    print(f"  neg_control_ok={out['negative_control']['neg_control_ok']} "
          f"deterministic_3x={det}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
