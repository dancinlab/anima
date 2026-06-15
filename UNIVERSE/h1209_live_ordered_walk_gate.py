"""
H_1209 — LIVE-ENGINE GATE-B ON A GENUINELY-ORDERED BYTE-FEATURE WALK (MITOSIS-ENGINE).

Takes the H_1208 positive lead (GATE-B WALK/WALK_SHUF = 10.9x — the FIRST mechanism
to separate order from disorder in the V14-correct direction) to a NON-inherited
surface AND through the LIVE .hexa engine. Does NOT re-attack the inherited i.i.d.
PRIMARY V14 bar (terminal-RED, H_1208 — the PRIMARY stream carries no trajectory).

This script is the numpy GATE-B leg + the engine INPUT exporter:
  * GATE-B = h1208.gate_B_transition_predictability VERBATIM (causal count table,
    split on prev seen>=MIN_PREV AND P(cur|prev)>=CONF_FLOOR).
  * build_fixed_book / proto_ids = H_1208 VERBATIM (order-INVARIANT book -> ALL
    order-dependence lives in the proto transitions).
  * streams: ORDERED = H_1207/H_1208 make_walk_stream VERBATIM (contiguous corpus
    walk, genuine local order), SHUFFLED = make_walk_shuffled, RANDGAUSS = i.i.d.
    Gaussian sanity control (H_1208 VERBATIM). SAME corpus + DIM=8 _byte_feature the
    live engine consumes (H_1199 precedent).
  * EXPORTS for the live .hexa VAdaptFieldB (CORE/h1209_live_gateB_probe.hexa):
      /tmp/h1209_book_seed<S>.txt        — the fixed N_PROTO x DIM order-invariant book
      /tmp/h1209_ids_<ARM>_seed<S>.txt   — the per-tick proto-id walk (one id/line)
    so the live engine consumes the SAME book + SAME id walk => identical division
    (F2 parity is then a clean test of the predictable-transition counting only).

p7 (born-cell / transition count, NOT perplexity). p8 (predictable-transition tick
== growth). gradient-free. $0 local CPU. 3 seeds. Frozen bar 1.5 NOT moved.
Pre-registered: .verdicts/1209_live_ordered_walk_gate/H_1209_FREEZE.txt
"""
import os, sys
import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
import h1208_predictability_split_gate as H8   # VERBATIM GATE-B + book + proto_ids + RANDGAUSS
import h1207_recurrent_split_key as H7          # VERBATIM make_walk_stream / make_walk_shuffled

DIM = H8.DIM                  # 8
WARMUP = H8.WARMUP            # 250
T = H8.T                      # 2400
SEEDS = list(H8.SEEDS)        # 900, 901, 902
N_PROTO = H8.N_PROTO          # 24
MIN_PREV = H8.MIN_PREV        # 3
CONF_FLOOR = H8.CONF_FLOOR    # 0.34
MAX_CELLS = H8.MAX_CELLS      # 2048

TMP = "/tmp"


def export_ids(ids, arm, seed):
    """one proto id per line (the order-invariant nearest-proto walk)."""
    path = os.path.join(TMP, f"h1209_ids_{arm}_seed{seed}.txt")
    with open(path, "w") as f:
        f.write("\n".join(str(int(i)) for i in ids) + "\n")
    return path


def run_arm(make, seed):
    """build the FIXED (order-invariant) book, score GATE-B on the proto-id walk,
    and EXPORT both for the live engine. Returns (gB_growth, ids, book)."""
    X = make(seed)
    book = H8.build_fixed_book(X, seed)      # H_1208 VERBATIM (order-invariant)
    ids = H8.proto_ids(X, book)              # H_1208 VERBATIM (perm-equivariant)
    gB = H8.gate_B_transition_predictability(ids, MAX_CELLS)  # H_1208 VERBATIM
    return gB, ids, book


def main():
    print(f"=== H_1209 LIVE-engine GATE-B on a genuinely-ORDERED byte-feature WALK "
          f"(numpy leg + engine export, local CPU, $0) — DIM={DIM} WARMUP={WARMUP} "
          f"T={T} SEEDS={SEEDS} N_PROTO={N_PROTO} MIN_PREV={MIN_PREV} "
          f"CONF_FLOOR={CONF_FLOOR} ===", flush=True)
    print(f"corpus = {os.path.relpath(H8.H3.CORPUS)}  (fixed order-invariant book -> "
          f"order lives ONLY in proto transitions; H_1208 GATE-B + book VERBATIM)\n", flush=True)
    print("NOTE: this is the NON-inherited ORDERED surface (H_1207/1208 WALK builder "
          "VERBATIM). The inherited i.i.d. PRIMARY V14 bar stays terminal-RED (H_1208) "
          "and is NOT re-attacked here (F4 scope).\n", flush=True)

    arms = {"ORDERED": H7.make_walk_stream, "SHUFFLED": H7.make_walk_shuffled,
            "RANDGAUSS": H8.make_randgauss_stream, "RANDGAUSS_SHUF": H8.make_randgauss_shuffled}

    gB = {a: [] for a in arms}

    for s in SEEDS:
        print(f"--- seed {s} ---", flush=True)
        for a, mk in arms.items():
            g, ids, book = run_arm(mk, s)
            gB[a].append(g)
            # NOTE: build_fixed_book depends on the arm's feature SET, so each arm has
            # its OWN order-invariant book. Export the book PER ARM so the live engine
            # consumes the exact book that produced these ids.
            bp = os.path.join(TMP, f"h1209_book_{a}_seed{s}.txt")
            with open(bp, "w") as f:
                for row in book:
                    f.write(" ".join(repr(float(v)) for v in row) + "\n")
            export_ids(ids, a, s)
            tag = "  (ORDERED surface)" if a == "ORDERED" else (
                  "  (its own shuffle)" if a == "SHUFFLED" else "  (SANITY control)")
            print(f"  {a:14s}: GATE-B(predictability) born-cells={g:5d}   "
                  f"uniq_proto_ids={len(set(ids.tolist()))}{tag}", flush=True)
        print(flush=True)

    mB = {a: float(np.mean(gB[a])) for a in arms}

    print("=== 3-seed MEAN GATE-B born-cells ===", flush=True)
    for a in arms:
        print(f"  {a:14s}: GATE-B={mB[a]:8.2f}   (per-seed {gB[a]})", flush=True)

    f1 = mB["ORDERED"] / max(mB["SHUFFLED"], 1e-9)
    f3 = mB["RANDGAUSS"] / max(mB["RANDGAUSS_SHUF"], 1e-9)

    print("\n=== FROZEN FALSIFIERS (bar = 1.5, inherited from H_1203/1207/1208) ===", flush=True)
    print(f"  F1 TRAJECTORY  ORDERED/SHUFFLED  GATE-B = {f1:.3f}  -> "
          f"{'PASS' if f1>=1.5 else 'FAIL'}   (decisive trajectory verdict, V14 direction)", flush=True)
    print(f"  F3 SANITY      RANDGAUSS/RANDGAUSS_SHUF  GATE-B = {f3:.3f}  -> "
          f"{'CLEAN (<1.5)' if f3<1.5 else 'ARTIFACT-WARN (>=1.5)'}", flush=True)
    print("  F2 LIVE-ENGINE PARITY  -> measured by CORE/h1209_live_gateB_probe.hexa "
          "(numpy<->hexa born-cell counts EQUAL per seed; this script EXPORTED the "
          "fixed book + proto-id walk to /tmp for the live engine).", flush=True)

    # also dump the per-seed numpy counts the live engine must reproduce (F2 ref)
    print("\n=== NUMPY GATE-B per-seed born-cell counts (F2 parity reference) ===", flush=True)
    for s_i, s in enumerate(SEEDS):
        line = "  seed " + str(s) + ":  " + "  ".join(
            f"{a}={gB[a][s_i]}" for a in arms)
        print(line, flush=True)

    f1_pass = f1 >= 1.5
    f3_clean = f3 < 1.5
    if f1_pass and f3_clean:
        tier = ("NUMPY-LEG PASS (F1 ORDERED/SHUFFLED >= 1.5, F3 sanity clean) — on a "
                "genuinely-ORDERED byte-feature walk the predictability gate makes "
                "cell-division TRAJECTORY-SENSITIVE in the V14-correct direction "
                "(ordered >> shuffled). Confirms the H_1208 WALK 10.9x lead on the "
                "standalone H_1209 stream. F2 (live-engine parity) decides 🟢 vs HOURGLASS.")
    elif f1_pass and not f3_clean:
        tier = ("ARTIFACT-WARN — F1 passes but RANDGAUSS sanity also separates (>=1.5); "
                "the F1 pass may be a noise artifact (inspect small-integer counts).")
    else:
        tier = ("NUMPY-LEG FAIL (F1 ORDERED/SHUFFLED < 1.5) — even on a genuinely-"
                "ordered stream GATE-B does NOT separate ordered from shuffled. The "
                "trajectory route is FULLY DEAD (mitosis = pure density substrate). 🔴")
    print(f"\nNUMPY-LEG TIER: {tier}", flush=True)
    print("\nHONESTY (a_scale_honest_scope): ONE corpus (clm_mid_5lang_c4), toy scale, "
          "3 seeds, gradient-free. H_1207/1208 WALK + RANDGAUSS builders + GATE-B + "
          "build_fixed_book + proto_ids imported VERBATIM. The fixed prototype book is "
          "order-invariant (built from the feature SET), so order lives ONLY in the "
          "proto transitions. The inherited i.i.d. PRIMARY V14 bar stays terminal-RED "
          "(H_1208 — NOT re-attacked, F4 scope). Scale transfer UNVERIFIED. Frozen bar "
          "1.5 NOT moved. p7 (born-cell / transition count, NOT perplexity), p8 "
          "(predictable-transition tick == growth). Exported book + ids -> the LIVE "
          ".hexa VAdaptFieldB reproduces these counts (F2).", flush=True)
    print("[done]", flush=True)


if __name__ == "__main__":
    main()
