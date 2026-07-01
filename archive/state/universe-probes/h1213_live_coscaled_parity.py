"""
H_1213 — LIVE-ENGINE CO-SCALED N_PROTO PARITY (MITOSIS-ENGINE).

H_1212 (numpy mirror, GREEN) found the co-scaling rule N_PROTO=round(T/100) — holding
obs_per_row = T/N_PROTO at the clean-toy ~100 — RESTORES GATE-B trajectory separation
(WALK/WALK_SHUF >= 1.5) across the SAME AXIS-T ladder where fixed-24 COLLAPSED. That was
the NUMPY MIRROR ONLY; live-engine parity at a CO-SCALED N_PROTO was the untested follow-on.

H_1209 proved numpy<->hexa VAdaptFieldB byte-exact at FIXED N_PROTO=24 (toy T). This script
is the NUMPY LEG + the engine INPUT exporter for the CO-SCALED extension:
  * GATE-B = h1208.gate_B_transition_predictability VERBATIM.
  * build_fixed_book / proto_ids = H_1208 VERBATIM (order-INVARIANT book).
  * WALK / WALK_SHUF = h1207 make_walk_stream / make_walk_shuffled VERBATIM.
  * RANDGAUSS / RANDGAUSS_SHUF = h1208 VERBATIM (sanity).
  * scale knobs (T, WARMUP, MAX_CELLS) monkeypatched on (H,H3,H7,H8) per H_1212
    _set_scale VERBATIM; N_PROTO set via the co-scaling rule round(T/100).
  * EXPORTS the per-tick proto-id walk for the live .hexa VAdaptFieldB:
      /tmp/h1213_ids_<RULE>_<ARM>_T<T>_N<N>_seed<S>.txt   (one id/line)
    so the live engine consumes the SAME id walk => identical division (parity = a
    clean test of the predictable-transition counting at the co-scaled alphabet).

FEASIBLE LIVE LADDER (interpreted .hexa ctab alloc wall measured in FREEZE):
  RUNG-1: T=2400,  N_PROTO=24  (toy baseline, obs/row=100)
  RUNG-2: T=24000, N_PROTO=240 (first 10x co-scaled rung, obs/row=100)
plus a fixed-24 @ T=24000 CONTRAST leg (also feasible) to show on the LIVE engine that
holding obs/row=100 via co-scaling keeps the separation cleaner than fixed-24. The
T=240000/N=2400 rung exceeds the interpreted-engine alloc budget (numpy-mirror-only,
H_1212 GREEN) -- stated honestly, NOT faked.

p7 (born-cell / transition count, NOT perplexity). p8 (predictable-transition tick ==
growth). gradient-free. $0 local CPU. 3 seeds. Frozen bar 1.5 NOT moved.
Pre-registered: .verdicts/1213_live_coscaled_parity/H_1213_FREEZE.txt
"""
import os, sys, math
import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
import h1163_tick_decode_metric as H          # _byte_feature / DIM / WIN_BYTES / STRIDE / WARMUP / T / CORPUS
import h1203_mitosis_novelty_coupling as H3   # constants + _load_corpus
import h1207_recurrent_split_key as H7        # make_walk_stream / make_walk_shuffled VERBATIM
import h1208_predictability_split_gate as H8  # GATE-B + build_fixed_book + proto_ids + randgauss VERBATIM

BAR = 1.5
SEEDS = [900, 901, 902]
TOY_CORPUS = H.CORPUS
TMP = "/tmp"
BIG_CAP = 10**9

# arms (order fixed for deterministic export naming)
ARMS = [("WALK", H7.make_walk_stream), ("WALK_SHUF", H7.make_walk_shuffled),
        ("RANDGAUSS", H8.make_randgauss_stream), ("RANDGAUSS_SHUF", H8.make_randgauss_shuffled)]


def n_proto_linear(T):  return max(2, int(round(T / 100.0)))   # H_1212 PRIMARY rule (obs/row~100)


def _set_scale(T, warmup):
    """H_1212 _set_scale VERBATIM — monkeypatch the pre-declared scale knobs on every
    module that captured a copy at import. Builder/gate CODE byte-unchanged."""
    for m in (H, H3, H7, H8):
        if hasattr(m, "T"):       m.T = T
        if hasattr(m, "WARMUP"):  m.WARMUP = warmup
    for m in (H3, H7, H8):
        if hasattr(m, "MAX_CELLS"): m.MAX_CELLS = BIG_CAP
    H.CORPUS = TOY_CORPUS
    H3.CORPUS = TOY_CORPUS
    if hasattr(H7, "CORPUS"): H7.CORPUS = TOY_CORPUS


def export_ids(ids, rule, arm, T, n, seed):
    path = os.path.join(TMP, f"h1213_ids_{rule}_{arm}_T{T}_N{n}_seed{seed}.txt")
    with open(path, "w") as f:
        f.write("\n".join(str(int(i)) for i in ids) + "\n")
    return path


def run_rung(rule, T, warmup, n_proto):
    """Compute numpy GATE-B per (arm,seed) at the given N_PROTO, export each id walk for
    the live engine. Returns {arm: [per-seed born-cells]} + 3-seed means."""
    _set_scale(T, warmup)
    H8.N_PROTO = n_proto                       # the SAME knob H_1211/1212 set
    gB = {a: [] for a, _ in ARMS}
    for s in SEEDS:
        for arm, mk in ARMS:
            X = mk(s)
            book = H8.build_fixed_book(X, s)   # VERBATIM (clamps to span internally)
            ids = H8.proto_ids(X, book)        # VERBATIM
            g = H8.gate_B_transition_predictability(ids, BIG_CAP)  # VERBATIM
            gB[arm].append(int(g))
            export_ids(ids, rule, arm, T, n_proto, s)
    m = {a: float(np.mean(gB[a])) for a, _ in ARMS}
    return gB, m


def main():
    print("================================================================================", flush=True)
    print("H_1213 LIVE-ENGINE CO-SCALED N_PROTO PARITY — numpy leg + engine export, $0 CPU, p7/p8, 3 seeds", flush=True)
    print(f"SEEDS={SEEDS}  BAR={BAR}  DIM={H.DIM} (structural, NOT scaled)", flush=True)
    print(f"corpus = {os.path.relpath(H.CORPUS)}", flush=True)
    print("GATE-B + build_fixed_book + proto_ids (H_1208) + WALK/RANDGAUSS (H_1207/1208) VERBATIM;", flush=True)
    print("H_1212 _set_scale VERBATIM sets ONLY (T,WARMUP,MAX_CELLS); N_PROTO via co-scaling round(T/100).", flush=True)
    print("Exports per-tick proto-id walks to /tmp for the LIVE .hexa VAdaptFieldB (parity reference below).", flush=True)
    print("================================================================================", flush=True)

    # FEASIBLE LIVE LADDER (co-scaled, obs/row=100) + a fixed-24 contrast at T=24000.
    # rule label, T, warmup, n_proto
    rungs = [
        ("linear", 2400,  250,  n_proto_linear(2400)),    # N=24  (toy baseline)
        ("linear", 24000, 2500, n_proto_linear(24000)),   # N=240 (co-scaled 10x rung)
        ("fixed24", 24000, 2500, 24),                      # fixed-24 contrast at T=24000
    ]

    results = {}
    for rule, T, wu, npp in rungs:
        obs = T / max(npp, 1)
        print(f"\n=== RUNG  rule={rule}  T={T}  N_PROTO={npp}  obs/row={obs:.1f} ===", flush=True)
        gB, m = run_rung(rule, T, wu, npp)
        results[(rule, T, npp)] = (gB, m)
        for arm, _ in ARMS:
            print(f"  {arm:14s}: GATE-B born-cells per-seed {gB[arm]}  mean {m[arm]:.2f}", flush=True)
        f2 = m["WALK"] / max(m["WALK_SHUF"], 1e-9)
        print(f"  WALK/WALK_SHUF = {f2:.3f}  (bar>={BAR}) -> {'PASS' if f2>=BAR else 'FAIL'}", flush=True)

    # ── per-seed parity reference the live engine must reproduce ──────────────────
    print("\n================================================================================", flush=True)
    print("NUMPY GATE-B per-seed born-cell counts (PARITY REFERENCE for the live engine)", flush=True)
    print("================================================================================", flush=True)
    for (rule, T, npp), (gB, m) in results.items():
        print(f"  [rule={rule} T={T} N={npp}]", flush=True)
        for s_i, s in enumerate(SEEDS):
            line = "    seed " + str(s) + ":  " + "  ".join(f"{a}={gB[a][s_i]}" for a, _ in ARMS)
            print(line, flush=True)

    print("\nHONESTY (a_scale_honest_scope): numpy mirror leg + engine export (H_1199/1209 precedent), "
          "gradient-free, $0 CPU, 3 seeds. GATE-B + build_fixed_book + proto_ids (H_1208) + WALK/"
          "RANDGAUSS (H_1207/1208) VERBATIM; H_1212 _set_scale VERBATIM sets ONLY (T,WARMUP,MAX_CELLS), "
          "N_PROTO via the co-scaling rule round(T/100). DIM=8 structural, NOT scaled. p7 (born-cell/"
          "transition count, NOT perplexity), p8 (split == growth). Frozen bar 1.5 NOT moved. Feasible "
          "live ladder = T=2400/N=24 + T=24000/N=240 (obs/row=100) + fixed-24 contrast @T=24000; the "
          "T=240000/N=2400 rung exceeds the interpreted-engine ctab alloc budget (numpy-mirror-only, "
          "H_1212 GREEN). The LIVE .hexa VAdaptFieldB reproduces these counts (F1 parity).", flush=True)
    print("[done]", flush=True)


if __name__ == "__main__":
    main()
