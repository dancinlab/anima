#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""H_6196 — extract h1129 (G0 303M byte-LM) hidden-channel time-series for faithful IIT4 Φ.

Produces a multichannel time-series (n_ch top-variance hidden channels over a corpus byte
stream) in the SAME flat layout `s[ch*n_samp + t]` that BRAIN/eeg/eeg_to_tpm.hexa's
`eeg_big_phi(samples, n_ch, n_samp, state)` consumes — so the anima faithful IIT4 big-Φ
engine measures the G0 TRUNK's integration exactly as it measures EEG (a_phi_iit4_tool).

HEAVY: 303M forward per position → pool (summer/aiden), never mini (OOM rc=137).
Emits samples_*.txt (n_ch, n_samp, then flat floats) + shuffle-control + meta. Faithful Φ is
then computed by the hexa probe (reference BRAIN/eeg/eeg_iit4_demo.hexa). $0 (no train).
"""
import os
import sys
import json
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
# core/decode.py provides bg_load / bg_forward_last_hidden (final-LN last-pos hidden)
for _c in ("core", os.path.expanduser("~/anima/core")):
    if os.path.isdir(_c) and _c not in sys.path:
        sys.path.insert(0, _c)
import decode as D

CKPT = os.path.expanduser("~/anima-weights/bytegpt303_h1129/h1129.bin")
N_CH = 6            # faithful IIT4 exact limit is n_ch <= 8; 6 -> 2^6=64 states
N_SAMP = 3000       # enough transitions to estimate the 64-state TPM
CTX = 64            # fixed context window per position (sliding)
SEED = 20260705


def load_corpus_bytes(paths, need):
    buf = bytearray()
    for p in paths:
        if os.path.isfile(p):
            with open(p, "rb") as f:
                buf += f.read()
        if len(buf) >= need + CTX + 1:
            break
    if len(buf) < need + CTX + 1:
        raise SystemExit(f"corpus too small: have {len(buf)}, need {need + CTX + 1} (pass more --corpus)")
    return bytes(buf)


def main():
    corpus_paths = sys.argv[1:] or [os.path.join(HERE, "corpus_sample.txt")]
    raw = load_corpus_bytes(corpus_paths, N_SAMP)
    print(f"[1/4] load 303M {CKPT} ...", flush=True)
    W = D.bg_load(CKPT)

    print(f"[2/4] {N_SAMP} per-position hiddens (ctx={CTX}) ...", flush=True)
    H = np.empty((N_SAMP, 768), dtype=np.float64)
    for t in range(N_SAMP):
        window = list(raw[t:t + CTX + 1])          # sliding fixed-CTX window ending at t+CTX
        h = D.bg_forward_last_hidden(W, window, len(window))
        H[t] = np.asarray(h, dtype=np.float64)
        if t % 500 == 0:
            print(f"    t={t}/{N_SAMP}", flush=True)

    print("[3/4] pick top-variance n_ch channels (honest slice) + random-ch control ...", flush=True)
    var = H.var(axis=0)
    top = np.argsort(var)[::-1][:N_CH]                       # top-variance channels
    rng = np.random.RandomState(SEED)
    rnd = rng.choice(768, size=N_CH, replace=False)          # random-channel control

    def to_flat(chans):
        # flat s[ch*n_samp + t] as eeg_to_tpm expects (raw floats; hexa binarizes at per-ch mean)
        return [float(H[t, ch]) for ch in chans for t in range(N_SAMP)]

    def to_flat_shuffle(chans):
        # time-shuffle EACH channel independently -> destroys temporal integration (control)
        out = []
        for ch in chans:
            col = H[:, ch].copy()
            rng.shuffle(col)
            out += [float(x) for x in col]
        return out

    print("[4/4] write samples_*.txt + controls + meta ...", flush=True)

    def dump(name, flat):
        with open(os.path.join(HERE, name), "w") as f:
            f.write(f"{N_CH} {N_SAMP}\n")
            f.write(" ".join(f"{x:.6f}" for x in flat))

    dump("samples_topvar.txt", to_flat(top))
    dump("samples_shuffle.txt", to_flat_shuffle(top))
    dump("samples_random.txt", to_flat(rnd))
    json.dump({"n_ch": N_CH, "n_samp": N_SAMP, "ctx": CTX, "ckpt": CKPT,
               "top_channels": [int(x) for x in top], "rand_channels": [int(x) for x in rnd],
               "note": "feed each samples_*.txt to eeg_big_phi(n_ch,n_samp); verdict = Phi_topvar - Phi_shuffle"},
              open(os.path.join(HERE, "meta.json"), "w"), ensure_ascii=False, indent=1)
    print("    done. next: hexa probe -> eeg_big_phi on samples_topvar/shuffle/random.", flush=True)


if __name__ == "__main__":
    main()
