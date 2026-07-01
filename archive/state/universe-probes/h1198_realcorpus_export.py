"""
H_1198 — REAL-CORPUS mitosis growth (MITOSIS-ENGINE · Lane-1), GPU-READER leg.

This script is the GPU half of H_1198. It trains the H_1193 byte-level Transformer
reader (VERBATIM, summer RTX 5070, VRAM-capped) on the held-out first half of the
REAL corpus, then EXPORTS, for several seeds, the position-aligned per-tick streams
that drive the live mitosis growth:

  * surprise[t]  = −log2 P_transformer(byte_t | preceding ctx)   (the novelty driver,
                   a real-corpus scalar — H_1192/H_1193's saccadic-reading signal)
  * feat8[t]     = the DIM=8 byte-statistics feature of the window at the SAME tick
                   (H_1163 make_text_stream's real-corpus feature)
  * stage[t]     = the per-tick stage label (H_1163 quantized byte-feature regime)

These three tracks are the REAL corpus byte stream. They feed two growth legs:
  (A) the LIVE .hexa engine (CORE/h1198_realcorpus_mitosis_growth.hexa) over the
      1-D surprise scalar — the actual adapt_field_step / engine_mitosis_tick on
      real-corpus data (the live AdaptField is 1-D scalar; surprise is the real
      1-D corpus signal), and
  (B) the DIM=8 SURPRISE-GATED numpy mirror (this file's growth section) — the
      full multi-dim byte-feature AdaptField with "high surprise → spawn a cell"
      (the H_1192/H_1193 mechanism), CLEARLY LABELLED as the numpy mirror because
      the live .hexa AdaptField cannot take a DIM>1 sample without an engine change.

GPU reader = H_1193's ByteTransformer VERBATIM (imported). The reader's training is a
SEPARATE Lane-G GPU predictor; the mitosis GROWTH is gradient-free Lane-1
(a_lane_akida_gpu_split). The model's loss is NOT the verdict (p7) — the growth
curve (cell_count + recon-error on real data) is.

HONESTY (a_scale_honest_scope): small reader, ONE corpus, gradient-free toy-ish
growth; the live-.hexa (1-D surprise) vs numpy-mirror (DIM=8 surprise-gated)
distinction is stated explicitly. VRAM capped to 25% of the 12GB card; co-tenant
rbfe-prod NEVER disturbed (OOM → shrink+retry, never grab more).
"""
import json, math, os, sys, time
import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
import h1163_tick_decode_metric as H            # make_text_stream / DIM / WARMUP / T / STRIDE / WIN_BYTES / SEEDS / N_STAGES_TEXT / assign / LR / WIN
import h1187_learned_surprise_reader as R       # corpus_bytes / HELDOUT_FRAC / SURPRISE_SIGMA / SURPRISE_REFRAC

# ── reuse H_1193's reader VERBATIM (it trains on import) ───────────────────────
# h1193 imports torch + caps VRAM at 0.28 on import; we re-cap to 0.25 first to be
# extra-safe with the co-tenant, then import (which trains the reader once).
import torch
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
if DEVICE == "cuda":
    torch.cuda.set_per_process_memory_fraction(0.25, 0)   # ≤3.05GB of 12GB; co-tenant safe
import h1193_summer_gpu_transformer_reader as TR          # trains the ByteTransformer on import

np.seterr(all="ignore")

OUT = "/tmp/h1198_streams.json"
N_EXPORT_SEEDS = 5
EXPORT_SEEDS = list(H.SEEDS[:N_EXPORT_SEEDS])


def feat8_track(seed):
    """The DIM=8 real-corpus byte feature for every tick of this seed's test span,
    position-aligned to make_text_stream (same `start` draw)."""
    X, stages = H.make_text_stream(seed)
    return X, stages


# ====================================================================================
# DIM=8 SURPRISE-GATED numpy MIRROR of the AdaptField growth (leg B).
# This is the H_1197 AdaptField mirror extended to the FULL DIM=8 real byte features
# with the split GATED BY SURPRISE (high surprise -> spawn a cell), the H_1192/H_1193
# saccadic mechanism. It is the numpy MIRROR (clearly labelled): the live .hexa
# AdaptField is 1-D scalar and cannot take a DIM>1 sample without an engine change.
# Mechanism is faithful to CORE/engine_cli.hexa adapt_field_step: nearest-prototype
# assign, recon-err = distance to nearest, online winner pull (LR), split when the
# gate fires AND n_cells < cap. The ONLY change vs the live engine: (1) DIM=8 not 1,
# (2) the split gate is SURPRISE>thr (not recon-err>thr) — the learned novelty driver.
# ====================================================================================
SPLIT_LR = 0.20          # matches the live engine's adapt_field_step LR
MIRROR_MAX_CELLS = 2048  # cap = N_MIGRATE (the migration trigger) so we can SEE if it is approached


def mirror_growth(X, stages, surprise, mitosis_on, max_cells, seed):
    """Drive the DIM=8 AdaptField mirror over the real-corpus stream with a
    surprise-gated split. Returns (cell_count_track, recon_err_track) sampled per
    window of SAMPLE_EVERY, plus final cell count. ON => split on high surprise;
    OFF => frozen at the seed cells (the H_1159 ON-vs-OFF control)."""
    SAMPLE_EVERY = 200
    cells = X[:1].copy().astype(float)          # one seed prototype (matches adapt_field_new)
    # surprise threshold from the WARMUP baseline (VERBATIM grow_arm_surprise)
    warm = surprise[:H.WARMUP]
    s_thr = float(np.mean(warm)) + R.SURPRISE_SIGMA * (float(np.std(warm)) + 1e-9)
    last_fire = -10 ** 9
    cell_track, err_track = [], []
    win_err, win_cnt = 0.0, 0
    for i, t in enumerate(range(H.WARMUP, H.WARMUP + H.T)):
        x = X[t]
        j, d = H.assign(cells, x)               # recon-err = distance to nearest prototype
        win_err += d; win_cnt += 1
        # surprise-gated split (high surprise -> spawn a cell), refractory + cap
        surprising = surprise[t] > s_thr
        fire = mitosis_on and surprising and (i - last_fire) >= R.SURPRISE_REFRAC
        if fire and len(cells) < max_cells:
            cells = np.vstack([cells, x[None].copy()])   # new cell AT the novel sample
            last_fire = i
        else:
            cells[j] += SPLIT_LR * (x - cells[j])        # online winner pull (homeostatic)
        if (i + 1) % SAMPLE_EVERY == 0:
            cell_track.append((t + 1, len(cells), win_err / max(win_cnt, 1)))
            win_err, win_cnt = 0.0, 0
    return cell_track, len(cells)


def main():
    t0 = time.time()
    print("=== H_1198 GPU-READER export (summer GPU, $0, VRAM-capped 25%) ===", flush=True)
    print(f"  device={DEVICE}  reader=H_1193 ByteTransformer params={TR._READER.n_params:,}  "
          f"val_ce={TR._READER.final_val_ce:.4f} bits/byte  unigram={TR._READER.unigram_val_ce:.4f}  "
          f"peakVRAM={TR._READER.peak_vram_mb:.0f}MB", flush=True)

    streams = {}
    mirror = {"on": {}, "off": {}}
    for s in EXPORT_SEEDS:
        X, stages = feat8_track(s)
        surprise = TR.surprise_track_for_seed(s)             # H_1193 reader surprise (real corpus)
        assert len(surprise) == len(X), (len(surprise), len(X))
        # 1-D scalar stream for the LIVE .hexa engine = the surprise track over the
        # scored region (WARMUP..WARMUP+T), the real-corpus per-tick novelty signal.
        surp_scored = [float(surprise[t]) for t in range(H.WARMUP, H.WARMUP + H.T)]
        streams[str(s)] = {
            "surprise_scored": surp_scored,          # live .hexa engine 1-D drive
            "surprise_mean": float(np.mean(surprise)),
            "surprise_std": float(np.std(surprise)),
        }
        # write the 1-D surprise stream as a flat uint8 binary the LIVE .hexa engine
        # reads (2 bytes/tick: hi,lo; surprise = (hi*256+lo)/256.0 bits, clamped).
        buf = bytearray()
        for v in surp_scored:
            q = int(round(max(0.0, min(255.99, v)) * 256.0))
            buf.append((q >> 8) & 0xFF)
            buf.append(q & 0xFF)
        with open(f"/tmp/h1198_surprise_seed{s}.bin", "wb") as f:
            f.write(bytes(buf))
        # DIM=8 surprise-gated MIRROR: ON (mitosis) vs OFF (frozen-cap) on real data
        on_track, on_final = mirror_growth(X, stages, surprise, True, MIRROR_MAX_CELLS, s)
        off_track, off_final = mirror_growth(X, stages, surprise, False, MIRROR_MAX_CELLS, s)
        mirror["on"][str(s)] = {"track": on_track, "final_cells": on_final}
        mirror["off"][str(s)] = {"track": off_track, "final_cells": off_final}
        print(f"  seed {s}: surprise mean={np.mean(surprise):.3f} std={np.std(surprise):.3f} bits  "
              f"mirror ON cells->{on_final}  OFF cells->{off_final}", flush=True)

    # mirror ON-vs-OFF late-window recon-error (last quarter), pooled over seeds
    def late_err(legtracks):
        vals = []
        for s in EXPORT_SEEDS:
            tr = legtracks[str(s)]["track"]
            q = max(1, len(tr) // 4)
            vals += [row[2] for row in tr[-q:]]
        return float(np.mean(vals)) if vals else 0.0
    late_on = late_err(mirror["on"])
    late_off = late_err(mirror["off"])
    on_cells = [mirror["on"][str(s)]["final_cells"] for s in EXPORT_SEEDS]
    off_cells = [mirror["off"][str(s)]["final_cells"] for s in EXPORT_SEEDS]

    out = {
        "H": "H_1198",
        "compute_host": "summer",
        "compute": "summer-GPU-shared (RTX 5070 12GB, torch %s, VRAM capped 25%%; co-tenant rbfe-prod live)" % torch.__version__,
        "device": DEVICE,
        "gpu_reader": {
            "kind": "H_1193 byte-level Transformer LM (VERBATIM)",
            "n_params": int(TR._READER.n_params),
            "final_val_ce_bits": round(TR._READER.final_val_ce, 4),
            "unigram_val_ce_bits": round(TR._READER.unigram_val_ce, 4),
            "uniform_baseline_bits": 8.0,
            "peak_vram_mb": round(TR._READER.peak_vram_mb, 1),
            "vram_fraction_cap": 0.25,
            "train_wall_s": round(TR._TRAIN_WALL, 2),
        },
        "corpus": os.path.relpath(H.CORPUS, os.path.dirname(__file__)),
        "export_seeds": EXPORT_SEEDS,
        "stream_len_per_seed": H.T,
        "streams": streams,                          # live .hexa engine drive (1-D surprise)
        "mirror_dim8_surprise_gated": {
            "note": ("DIM=8 real byte-feature AdaptField with SURPRISE-GATED split "
                     "(high surprise -> spawn a cell). NUMPY MIRROR of the live engine — "
                     "the live .hexa AdaptField is 1-D scalar and cannot take a DIM>1 "
                     "sample without an engine change. Mechanism faithful to "
                     "adapt_field_step (nearest assign, recon-err, online pull, capped split)."),
            "max_cells": MIRROR_MAX_CELLS,
            "on_final_cells": on_cells,
            "off_final_cells": off_cells,
            "late_recon_err_ON": late_on,
            "late_recon_err_OFF": late_off,
            "ratio_OFF_over_ON": (late_off / late_on) if late_on > 0 else 0.0,
            "tracks": mirror,
        },
        "wall_s": round(time.time() - t0, 2),
    }
    json.dump(out, open(OUT, "w"))
    print(f"\n  MIRROR (DIM=8 surprise-gated) ON-vs-OFF on REAL corpus:", flush=True)
    print(f"    cells ON {on_cells} (mean {np.mean(on_cells):.1f})  vs  OFF {off_cells} (frozen-cap=1)", flush=True)
    print(f"    late recon-err ON={late_on:.4f}  OFF={late_off:.4f}  ratio OFF/ON={out['mirror_dim8_surprise_gated']['ratio_OFF_over_ON']:.3f}", flush=True)
    print(f"  wrote {OUT}  ({out['wall_s']}s)\n[done]", flush=True)


if __name__ == "__main__":
    main()
