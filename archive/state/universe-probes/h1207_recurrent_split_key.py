"""
H_1207 — RECURRENT SPLIT KEY (MITOSIS-ENGINE). Defeat V14 at the gate level.

H_1203 found the VAdaptField split gate (per-sample L2 recon-err to nearest
prototype > SPLIT_THRESH=0.30) reacts to novelty-DENSITY (F1 37.5x) but NOT to
TRAJECTORY: shuffling the time order left division UNCHANGED (F2 0.992, ratio
~1.0x) — V14 substrate-neutrality at the trajectory level. The per-sample gate is
PERMUTATION-INVARIANT BY CONSTRUCTION (no recurrence term — sees only x_t).

This probe tests whether a RECURRENT / TEMPORAL term in the split key makes
division trajectory-sensitive. Following the CLM_TIME_ENCODING / "TIME 주입 M3
DERIVATIVE" precedent (the d/dt term on the split TRIGGER was the ONLY temporal
arm to beat shuffle), the split key is the recon-err over a DELTA-AUGMENTED sample:

    Δ_t = x_t − x_{t-1}                 (the d/dt temporal-encoding term)
    z_t = [ x_t ; β·Δ_t ]               (augmented 2*DIM vector, β=1.0 frozen)
    split iff L2(z_t, nearest_proto_z) > SPLIT_THRESH=0.30

Prototypes live in the 2*DIM augmented space; nearest-by-L2, split-at-sample,
LR=0.20 winner-pull OTHERWISE IDENTICAL to vadapt_field_step. Trajectory-sensitive
BY CONSTRUCTION: Δ_t depends on the PAIR (x_{t-1}, x_t) → its value depends on
arrival ORDER.

FROZEN bars in .verdicts/1207_recurrent_split_key/H_1207_FREEZE.txt (1.5 == H_1203):
  F1 (V14 격파)  NOVEL/SHUFFLED cell_growth >= 1.5  [recurrent gate, PRIMARY]
  F2 (no regr.)  NOVEL/REPEAT   cell_growth >= 1.5  [recurrent gate, PRIMARY]
  F3 (mech)      permutation-control Δ% on PRIMARY AND on the WALK diagnostic.

HONEST: the H_1203 NOVEL stream uses i.i.d.-SCATTERED offsets → its Δ distribution
is ITSELF permutation-invariant. WALK (a CONTIGUOUS corpus walk, genuine local
continuity) is reported as a NON-bar diagnostic: a stream that HAS order structure
for the recurrent gate to be sensitive to. p7 (cell-count / recon-err), p8 (split
tick == growth), gradient-free, $0 local CPU, 3 seeds. Scale UNVERIFIED.
"""
import os, sys
import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
import h1203_mitosis_novelty_coupling as H3   # VERBATIM H_1203 stream builders + constants
import h1163_tick_decode_metric as H          # _byte_feature / DIM / WIN_BYTES / STRIDE

DIM = H3.DIM                  # 8
WARMUP = H3.WARMUP            # 250
T = H3.T                      # 2400
SEEDS = list(H3.SEEDS)        # 900, 901, 902
SPLIT_THRESH = H3.SPLIT_THRESH  # 0.30 (frozen, == engine)
LR = H3.LR                    # 0.20 (frozen, == engine)
MAX_CELLS = H3.MAX_CELLS      # 2048
SAMPLE_EVERY = H3.SAMPLE_EVERY  # 200
BETA = 1.0                    # frozen delta weight (equal, no tuning)
CORPUS = H3.CORPUS


# ── WALK diagnostic stream (NON-bar): a CONTIGUOUS corpus walk = genuine local
# temporal continuity (overlapping windows step forward by STRIDE). Unlike the
# H_1203 i.i.d.-scattered NOVEL stream, WALK HAS order structure to destroy. ──────
def make_walk_stream(seed):
    data = H3._load_corpus()
    need = WARMUP + T + 1
    span = H.WIN_BYTES + H.STRIDE * need
    if len(data) <= span + 1:
        data = data * (span // max(len(data), 1) + 2)
    rng = np.random.default_rng(seed)
    start = int(rng.integers(0, max(1, len(data) - span - 1)))
    X = np.empty((need, DIM))
    for i in range(need):
        p = start + i * H.STRIDE
        X[i] = H._byte_feature(data[p:p + H.WIN_BYTES])
    return X


def make_walk_shuffled(seed):
    X = make_walk_stream(seed)
    rng = np.random.default_rng(seed + 20_000)
    perm = rng.permutation(X.shape[0])
    return X[perm]


# ── recurrent (delta-augmented) gate: numpy mirror, mechanism-identical to a
# VAdaptField lifted to z_t = [x_t ; beta*(x_t - x_{t-1})]. Everything else
# (nearest-by-L2, split>thresh seeds at sample, LR winner-pull) is vadapt_field_step.
def run_vadapt_recurrent(X, mitosis_on, max_cells):
    Xs = X[WARMUP:WARMUP + T]
    # z_t = [x_t ; beta*(x_t - x_{t-1})]; t=0 has no predecessor -> zero delta.
    n = len(Xs)
    Z = np.zeros((n, 2 * DIM))
    Z[:, :DIM] = Xs
    Z[1:, DIM:] = BETA * (Xs[1:] - Xs[:-1])
    protos = [Z[0].astype(float).copy()]
    rows = []
    win_err, win_cnt = 0.0, 0
    for i in range(n):
        z = Z[i].astype(float)
        d = np.array([np.linalg.norm(p - z) for p in protos])
        j = int(d.argmin())
        err = float(d[j])
        win_err += err; win_cnt += 1
        if mitosis_on and err > SPLIT_THRESH and len(protos) < max_cells:
            protos.append(z.copy())
        else:
            protos[j] += LR * (z - protos[j])
        if (i + 1) % SAMPLE_EVERY == 0:
            rows.append((i + 1, len(protos), win_err / max(win_cnt, 1)))
            win_err, win_cnt = 0.0, 0
    q = max(1, len(rows) // 4)
    late_err = float(np.mean([r[2] for r in rows[-q:]])) if rows else 0.0
    return rows, len(protos), late_err


# per-sample baseline gate (H_1203 vadapt_field_step VERBATIM) for a side-by-side.
def run_vadapt_persample(X, mitosis_on, max_cells):
    return H3.run_vadapt(X, mitosis_on, max_cells)


def main():
    print(f"=== H_1207 recurrent (delta-augmented) split key (local CPU, $0) — DIM={DIM} "
          f"DIM'={2*DIM} WARMUP={WARMUP} T={T} SEEDS={SEEDS} SPLIT_THRESH={SPLIT_THRESH} "
          f"LR={LR} BETA={BETA} ===", flush=True)
    print(f"corpus = {os.path.relpath(CORPUS)}  (recurrent gate = vadapt_field_step lifted to "
          f"z_t=[x_t; beta*(x_t-x_t-1)])\n", flush=True)

    # PRIMARY arms = H_1203 builders VERBATIM (apples-to-apples).
    primary = {"NOVEL": H3.make_novel_stream, "REPEAT": H3.make_repeat_stream,
               "SHUFFLED": H3.make_shuffled_stream}
    # DIAGNOSTIC (NON-bar): contiguous corpus walk + its shuffle.
    walk = {"WALK": make_walk_stream, "WALK_SHUF": make_walk_shuffled}

    g_rec = {a: [] for a in list(primary) + list(walk)}   # recurrent-gate growth
    g_base = {a: [] for a in primary}                      # per-sample baseline (H_1203)
    e_rec = {a: [] for a in list(primary) + list(walk)}

    for s in SEEDS:
        print(f"--- seed {s} ---", flush=True)
        for a, mk in primary.items():
            X = mk(s)
            r_rows, r_final, r_late = run_vadapt_recurrent(X, True, MAX_CELLS)
            b_rows, b_final, b_late = run_vadapt_persample(X, True, MAX_CELLS)
            g_rec[a].append(r_final - 1); g_base[a].append(b_final - 1); e_rec[a].append(r_late)
            print(f"  {a:9s}: RECURRENT growth={r_final-1:4d} (per-sample baseline={b_final-1:4d})  "
                  f"recurrent late recon-err={r_late:.4f}", flush=True)
        for a, mk in walk.items():
            X = mk(s)
            r_rows, r_final, r_late = run_vadapt_recurrent(X, True, MAX_CELLS)
            g_rec[a].append(r_final - 1); e_rec[a].append(r_late)
            print(f"  {a:9s}: RECURRENT growth={r_final-1:4d}  (DIAGNOSTIC, non-bar)  "
                  f"recurrent late recon-err={r_late:.4f}", flush=True)
        print(flush=True)

    mr = {a: float(np.mean(g_rec[a])) for a in g_rec}
    mb = {a: float(np.mean(g_base[a])) for a in g_base}

    print("=== 3-seed MEAN cell_growth ===", flush=True)
    print("  PRIMARY (H_1203 streams VERBATIM):", flush=True)
    for a in primary:
        print(f"    {a:9s}: RECURRENT={mr[a]:7.2f}  per-sample-baseline={mb[a]:7.2f}   "
              f"(recurrent per-seed {g_rec[a]})", flush=True)
    print("  WALK diagnostic (contiguous corpus walk — HAS order structure):", flush=True)
    for a in walk:
        print(f"    {a:9s}: RECURRENT={mr[a]:7.2f}   (per-seed {g_rec[a]})", flush=True)

    # ── FROZEN falsifiers (PRIMARY, recurrent gate) ──────────────────────────────
    f1 = mr["NOVEL"] / max(mr["SHUFFLED"], 1e-9)   # V14 격파 (was H_1203 F2 = 0.992)
    f2 = mr["NOVEL"] / max(mr["REPEAT"], 1e-9)      # no regression (was H_1203 F1 = 37.5)
    f1_base = mb["NOVEL"] / max(mb["SHUFFLED"], 1e-9)   # the H_1203 per-sample number, reproduced
    # F3 permutation-control magnitude (Δ%): how much shuffle REDUCES division.
    dpct_primary = 100.0 * (mr["NOVEL"] - mr["SHUFFLED"]) / max(mr["NOVEL"], 1e-9)
    dpct_walk = 100.0 * (mr["WALK"] - mr["WALK_SHUF"]) / max(mr["WALK"], 1e-9)

    print("\n=== FROZEN FALSIFIERS (recurrent gate, PRIMARY H_1203 streams) ===", flush=True)
    print(f"  F1  V14 격파   NOVEL/SHUFFLED = {f1:.3f}  (bar >= 1.5)  -> {'PASS' if f1>=1.5 else 'FAIL'}", flush=True)
    print(f"      (H_1203 per-sample baseline reproduced: NOVEL/SHUFFLED = {f1_base:.3f} == ~0.992)", flush=True)
    print(f"  F2  no regr.   NOVEL/REPEAT   = {f2:.3f}  (bar >= 1.5)  -> {'PASS' if f2>=1.5 else 'FAIL'}", flush=True)
    print(f"  F3  permutation-control magnitude (Δ% division lost to shuffle):", flush=True)
    print(f"        PRIMARY  (i.i.d.-scattered NOVEL): Δ% = {dpct_primary:+.2f}%", flush=True)
    print(f"        WALK     (contiguous, HAS order) : Δ% = {dpct_walk:+.2f}%   (diagnostic)", flush=True)

    f1p = f1 >= 1.5
    f2p = f2 >= 1.5
    if f1p and f2p:
        tier = ("GREEN (V14 격파) — the recurrent (delta-augmented) split key makes "
                "VAdaptField division TRAJECTORY-SENSITIVE on the H_1203 streams; "
                "mitosis becomes a trajectory substrate.")
    else:
        tier = ("RED (closed-neg, a_paper_negative_ok) — even the recurrent gate stays "
                "permutation-invariant on the H_1203 PRIMARY streams (F1 FAIL). "
                "Read F3: if WALK Δ% >> PRIMARY Δ%, the gate IS trajectory-sensitive but "
                "the i.i.d.-scattered H_1203 NOVEL stream carries no trajectory to be "
                "sensitive to (a sharper V14 reading); if WALK Δ% ~ 0 too, the gate "
                "itself stays order-invariant for this feature.")
    print(f"\nTIER: {tier}", flush=True)
    print("\nHONESTY: ONE corpus (clm_mid_5lang_c4), toy scale, 3 seeds, gradient-free, "
          "numpy mirror = vadapt_field_step lifted to z_t=[x_t; beta*(x_t-x_t-1)] "
          "(H_1199 mechanism-match precedent). H_1203 stream builders imported VERBATIM. "
          "Scale transfer UNVERIFIED. Frozen bars (1.5 == H_1203) not moved.", flush=True)
    print("[done]", flush=True)


if __name__ == "__main__":
    main()
