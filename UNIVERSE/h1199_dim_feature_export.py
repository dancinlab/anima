"""
H_1199 — DIM>1 live AdaptField (MITOSIS-ENGINE · Lane-1), FEATURE-EXPORT leg.

Closes the H_1198 honest gap: H_1198 ran the DIM=8 real byte-feature growth as a
LABELLED NUMPY MIRROR because the live .hexa AdaptField was 1-D scalar. H_1199
extended the live engine with a VECTOR AdaptField (CORE/engine_cli.hexa
VAdaptField / vadapt_field_step / vadapt_field_recon_err / vadapt_field_cells),
so the DIM=8 stream now drives the ACTUAL .hexa engine.

This script ONLY produces the engine INPUT (and a numpy reference of the SAME
mechanism for cross-check). It does NOT decide the verdict — the live .hexa
VAdaptField run does (CORE/h1199_dim_adaptfield_probe.hexa).

  * feat8[t] = the DIM=8 real-corpus byte feature (H_1163 `_byte_feature` window
               statistic) for every tick of the scored span — VERBATIM via import
               of h1163_tick_decode_metric (make_text_stream).

The DIM=8 features are written to /tmp/h1199_feat8_seed<S>.txt — one tick per line,
DIM space-separated full-repr floats — for the .hexa engine to read (lossless,
parsed with hexa string split + to_float; IEEE-754 byte decode is unneeded). The
live engine
gates the split on its OWN recon-err > SPLIT_THRESH (the native VAdaptField
mechanism — the SAME recon-err gate the scalar AdaptField uses), NOT a separate
surprise track: this is the engine's intrinsic novelty signal in DIM space, so
the leg that was a numpy mirror is now the actual engine.

The numpy REFERENCE below mirrors vadapt_field_step EXACTLY (nearest by L2,
recon-err = L2 to nearest, recon-err>0.30 split + capped, LR=0.20 winner pull) so
we can assert the .hexa engine reproduces the mechanism byte-for-byte on the same
input — a guard that the live engine and the reference agree, NOT the verdict.

HONESTY (a_scale_honest_scope): ONE corpus, gradient-free, toy-ish scale.
p7 metric = real L2 reconstruction distance, NOT perplexity. $0 local CPU.
"""
import os, sys
import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
import h1163_tick_decode_metric as H   # make_text_stream / _byte_feature / DIM / WARMUP / T / SEEDS

DIM = H.DIM                # 8
SEEDS = list(H.SEEDS[:3])  # 900, 901, 902 (>=3 deterministic seeds)
SPLIT_THRESH = 0.30        # matches CORE/engine_cli.hexa vadapt_field_step
LR = 0.20                  # matches the live engine
MAX_CELLS = 2048           # cap = N_MIGRATE (lets us SEE if real-corpus growth approaches it)
SAMPLE_EVERY = 200


def ref_growth(X, mitosis_on, max_cells):
    """numpy REFERENCE of vadapt_field_step (recon-err-gated, DIM=8). NOT the
    verdict — a cross-check that the live .hexa engine reproduces the mechanism on
    the same input. Mirrors vadapt_field_step EXACTLY: nearest by L2, recon-err =
    L2 to nearest, split when recon-err>SPLIT_THRESH & n_cells<cap, LR winner pull."""
    Xs = X[H.WARMUP:H.WARMUP + H.T]
    protos = [Xs[0].astype(float).copy()]   # one seed prototype (matches vadapt_field_new)
    rows = []
    win_err, win_cnt = 0.0, 0
    for i in range(len(Xs)):
        x = Xs[i].astype(float)
        d = np.array([np.linalg.norm(p - x) for p in protos])
        j = int(d.argmin())
        err = float(d[j])
        win_err += err; win_cnt += 1
        if mitosis_on and err > SPLIT_THRESH and len(protos) < max_cells:
            protos.append(x.copy())          # new cell AT the novel DIM-sample
        else:
            protos[j] += LR * (x - protos[j])  # online winner pull
        if (i + 1) % SAMPLE_EVERY == 0:
            rows.append((i + 1, len(protos), win_err / max(win_cnt, 1)))
            win_err, win_cnt = 0.0, 0
    return rows, len(protos)


def main():
    print(f"=== H_1199 DIM=8 feature export (local CPU, $0) — DIM={DIM} SEEDS={SEEDS} ===", flush=True)
    for s in SEEDS:
        X, stages = H.make_text_stream(s)              # VERBATIM h1163 real-corpus feature
        Xs = X[H.WARMUP:H.WARMUP + H.T]
        # write the DIM=8 scored span as text: one tick per line, DIM space-sep
        # full-repr floats (lossless; the .hexa engine parses with split+to_float).
        path = f"/tmp/h1199_feat8_seed{s}.txt"
        with open(path, "w") as f:
            for t in range(Xs.shape[0]):
                f.write(" ".join(repr(float(v)) for v in Xs[t]) + "\n")
        # numpy reference (cross-check the live engine)
        on_rows, on_final = ref_growth(X, True, MAX_CELLS)
        off_rows, off_final = ref_growth(X, False, MAX_CELLS)
        q = max(1, len(on_rows) // 4)
        late_on = float(np.mean([r[2] for r in on_rows[-q:]]))
        late_off = float(np.mean([r[2] for r in off_rows[-q:]]))
        print(f"  seed {s}: wrote {Xs.shape[0]} ticks x DIM={DIM} -> {path}", flush=True)
        print(f"    [numpy ref] cells ON 1->{on_final}  OFF ->{off_final}  "
              f"late recon-err ON={late_on:.4f} OFF={late_off:.4f} ratio={late_off/max(late_on,1e-9):.2f}x", flush=True)
    print("[done]", flush=True)


if __name__ == "__main__":
    main()
