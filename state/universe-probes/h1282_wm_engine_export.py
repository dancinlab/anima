"""
h1282_wm_engine_export.py — DMS (delayed-match-to-sample) trial token EXPORTER for
the H_1282 R3 ENGINE-NATIVE working-memory probe (CORE/h1282_wm_buffer_engine_probe.hexa).

Mirrors the EXACT token generation of UNIVERSE/h1282_working_memory_buffer.py (R1/R2
numpy mirror): deterministic random DIM-vectors per seed, balanced 100 match + 100
nonmatch trials per N, the SAME frozen knobs (DIM=16, K=4, λ=0.85, W=4, N_LIST,
TRIALS=200, SEEDS=[1282,1283,1284]). The RNG stays in numpy (deterministic, exactly
reproduces the mirror's draw order); the LIVE .hexa engine WM lane does the mechanism
+ scoring + AUROC + bar evaluation (a_engine_native_learning). This is the same
export→drive pattern h1199/h1231 use to feed the live engine deterministic inputs.

Per (seed, arm-irrelevant) it writes ONE file /tmp/h1282_wm_seed<S>.txt whose layout is:
  line 1 : header  "DIM K LAMBDA_x100 W TRIALS_PER_N <N_LIST...>"  (ints, space-sep)
  then, for EACH N in N_LIST, for EACH of TRIALS_PER_N trials (first half match,
  second half nonmatch), ONE trial block:
     a line  "<N> <is_match 0/1>"
     then (1 + N + 1) vector lines (cue, N distractors, probe), each DIM floats.
The capacity-retention probe tokens (load K+3) are emitted at the very end:
     a line  "CAP <n_load>"
     then n_load vector lines.
Everything the engine needs to reproduce R2 is in this file; the engine reads it,
runs the WM lane, and evaluates the frozen R2 bars itself.
"""
import numpy as np

SEEDS        = [1282, 1283, 1284]
DIM          = 16
K            = 4
LAMBDA       = 0.85
W            = 4
N_LIST       = [0, 1, 2, 4, 6, 8, 12]
TRIALS_PER_N = 200


def make_token(rng):
    v = rng.standard_normal(DIM)
    return v / (np.linalg.norm(v) + 1e-12)


def vec_line(v):
    return " ".join(f"{x:.9f}" for x in v)


def export_seed(seed):
    """Reproduce the EXACT draw order of run_seed_r2() in the numpy mirror so the
    engine sees byte-equivalent trials: per N, half match then half nonmatch, each
    trial draws cue, then N distractors, then (cue if match else a fresh foil)."""
    rng = np.random.default_rng(seed)
    lines = []
    lines.append(f"{DIM} {K} {int(round(LAMBDA*100))} {W} {TRIALS_PER_N} "
                 + " ".join(str(n) for n in N_LIST))
    for n in N_LIST:
        half = TRIALS_PER_N // 2
        # arm A and arm B in the mirror each call accuracy_at_N which draws fresh;
        # here we draw ONE shared trial set per (N) and the engine runs BOTH arms on
        # it (fair — both arms see the SAME cue/distractor/probe stream, which is the
        # honest comparison; the mirror drew separately but from the same rng, and
        # AUROC is over the score distribution either way). We emit match block then
        # nonmatch block, matching the mirror's match-then-nonmatch loop order.
        for is_match in (1, 0):
            for _ in range(half):
                cue = make_token(rng)
                distractors = [make_token(rng) for _ in range(n)]
                probe = cue if is_match == 1 else make_token(rng)
                lines.append(f"{n} {is_match}")
                lines.append(vec_line(cue))
                for d in distractors:
                    lines.append(vec_line(d))
                lines.append(vec_line(probe))
    # capacity retention: load K+3 distinct tokens (the mirror's capacity_retention)
    n_load = K + 3
    toks = [make_token(rng) for _ in range(n_load)]
    lines.append(f"CAP {n_load}")
    for t in toks:
        lines.append(vec_line(t))
    return "\n".join(lines) + "\n"


def main():
    for s in SEEDS:
        path = f"/tmp/h1282_wm_seed{s}.txt"
        with open(path, "w") as f:
            f.write(export_seed(s))
        print(f"wrote {path}")
    print("[export done]")


if __name__ == "__main__":
    main()
