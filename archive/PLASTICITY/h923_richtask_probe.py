#!/usr/bin/env python3
"""h923_richtask_probe.py — H_923 M5: lift the D1 ceiling with a richer task.

M2/M4 found D1=2 functional-output-diversity under the TOY trap task (10-unit FC,
near-degenerate patterns). The pre-registered honest C3 says that ceiling is the
TASK output-space, NOT the ANU entropy source. M5 tests that directly: same ANU
quantum init-injection, but a RICHER task (64-unit FC + varied non-degenerate
patterns -> huge winner-assignment space). If D1 climbs from 2 toward N=16, the
ceiling was task-limited and the coupling delivers real entropy-sourced diversity.

init per episode = distinct 128-byte ANU window (16*64=1024 weight bits). Needs a
>=2048-byte ANU buffer (anu_pull.py chunks >1024 automatically). argv[1]=ANU path.
"""
import hashlib
import json
import sys

import numpy as np
import akida

IN_DIM = 16
N_UNITS = 64               # richer output space (was 10)
N_PATTERNS = 24            # more, varied patterns (was 12 near-degenerate)
N_EPISODES = 16
WINDOW = 128               # bytes/episode = IN_DIM*N_UNITS bits = 1024 bits


def make_rich_patterns(seed: int = 11) -> np.ndarray:
    """Varied (NON-degenerate) binary patterns -> real winner competition across 64 units."""
    rng = np.random.default_rng(seed)
    pats = (rng.random((N_PATTERNS, IN_DIM)) < 0.5).astype(np.uint8)
    return pats.reshape(N_PATTERNS, 1, 1, IN_DIM)


def init_from_anu(window: bytes):
    bits = np.unpackbits(np.frombuffer(window, dtype=np.uint8))
    return bits[:IN_DIM * N_UNITS].astype(np.int8).reshape(IN_DIM, N_UNITS)


def whash(a) -> str:
    return hashlib.sha256(np.ascontiguousarray(a).tobytes()).hexdigest()[:12]


def build_model(dev):
    m = akida.Model()
    m.add(akida.InputData(input_shape=(1, 1, IN_DIM), input_bits=1, name="in"))
    m.add(akida.FullyConnected(units=N_UNITS, name="fc", weights_bits=1, activation=True))
    m.map(dev)
    return m


def run_one(dev, x, w):
    m = build_model(dev)
    m.compile(optimizer=akida.AkidaUnsupervised(num_weights=2, learning_competition=0.1))
    fc = m.get_layer("fc")
    cur = fc.get_variable("weights")
    fc.set_variable("weights", w.reshape(cur.shape).astype(cur.dtype))
    m.fit(x)
    return whash(np.asarray(m.forward(x)))


def main():
    raw = open(sys.argv[1], "rb").read()
    need = N_EPISODES * WINDOW
    if len(raw) < need:
        print(json.dumps({"ok": 0, "error": f"need {need} ANU bytes, got {len(raw)}"}))
        return
    dev = akida.devices()[0]
    x = make_rich_patterns()
    out_hashes = []
    for ep in range(N_EPISODES):
        w = init_from_anu(raw[ep * WINDOW:(ep + 1) * WINDOW])
        out_hashes.append(run_one(dev, x, w))
    # D3 determinism re-check on episode 0
    d3 = run_one(dev, x, init_from_anu(raw[0:WINDOW])) == out_hashes[0]
    out = {
        "probe": "h923_richtask_ceiling",
        "device": str(dev.version),
        "task": {"units": N_UNITS, "n_patterns": N_PATTERNS, "degenerate": False},
        "n_episodes": N_EPISODES,
        "anu_sha256": hashlib.sha256(raw).hexdigest(),
        "D1_functional_output_diversity": len(set(out_hashes)),
        "D3_determinism_preserved": bool(d3),
        "compare": "toy task gave D1=2 (10-unit degenerate); this is richer -> D1 should climb",
    }
    open("/tmp/h923_rich_result.json", "w").write(json.dumps(out) + "\n")
    print(json.dumps(out))


if __name__ == "__main__":
    main()
