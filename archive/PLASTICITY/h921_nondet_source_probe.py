#!/usr/bin/env python3
"""h921_hw_probe_v2.py — H_921 M2-v2: locate the SOURCE of AKD1000 non-determinism.

M2-v1 found raw_weight_diversity == 1 under a PINNED *degenerate* init (all units
identical). That init guarantees deterministic winner-collapse (always unit 0), so
it MASKS any chip non-determinism by construction (same class of flaw as M1's float
ties). It also did not confirm fit() actually changed the weights.

v2 disambiguates with THREE on-chip conditions, each N episodes, SAME deterministic
input, recording init/post-fit weight hashes + full output hash + whether fit moved
the weights:

  A_pinned_nondegen : init pinned to a FIXED *non-degenerate* (distinct-per-unit)
                      weight set every episode -> competition actually fires. If
                      weight_div==1 here, on-chip learning is DETERMINISTIC given a
                      truly fixed init.
  B_nopin_default   : NO set_variable; AkidaUnsupervised's own init each compile.
                      If weight_div>1 here while A==1, the previously-reported
                      run-to-run non-determinism (H_860 hamming {28,38,34,38}) was
                      INIT-SEEDED, not a property of the learning dynamics.

Interpretation map:
  A>1                      -> chip learning intrinsically non-det even when pinned.
  A==1 & B>1               -> "AKIDA non-determinism" = random INIT, not learning.
  A==1 & B==1              -> learning fully deterministic; H_860 non-det not repro'd.
  fit_changed==False       -> fit no-op; probe invalid, ignore the row.
"""
import hashlib
import json

import numpy as np
import akida

IN_DIM = 16
N_UNITS = 10
N_PATTERNS = 12
N_EPISODES = 16
INIT_SEED = 187


def make_trap_patterns(seed: int = 7) -> np.ndarray:
    rng = np.random.default_rng(seed)
    core = np.zeros(IN_DIM, dtype=np.uint8)
    core[:8] = 1
    pats = np.tile(core, (N_PATTERNS, 1))
    for i in range(N_PATTERNS):
        pats[i, 8 + (i % 8)] = 1
    return pats.astype(np.uint8).reshape(N_PATTERNS, 1, 1, IN_DIM)


def nondegen_init(seed: int = INIT_SEED):
    """FIXED but NON-degenerate: each unit a distinct binary column -> real
    winner competition (no artificial collapse to unit 0)."""
    rng = np.random.default_rng(seed)
    return (rng.random((IN_DIM, N_UNITS)) < 0.5).astype(np.int8)


def whash(a) -> str:
    return hashlib.sha256(np.ascontiguousarray(a).tobytes()).hexdigest()[:12]


def build_model(dev):
    m = akida.Model()
    m.add(akida.InputData(input_shape=(1, 1, IN_DIM), input_bits=1, name="in"))
    m.add(akida.FullyConnected(units=N_UNITS, name="fc", weights_bits=1, activation=True))
    m.map(dev)
    return m


def set_init(model, w):
    fc = model.get_layer("fc")
    cur = fc.get_variable("weights")
    fc.set_variable("weights", w.reshape(cur.shape).astype(cur.dtype))
    return whash(fc.get_variable("weights"))


def run_condition(dev, x, *, pin):
    w_init = nondegen_init() if pin else None
    inits, posts, outs, changed, err = [], [], [], [], []
    for ep in range(N_EPISODES):
        try:
            m = build_model(dev)
            m.compile(optimizer=akida.AkidaUnsupervised(num_weights=2,
                                                        learning_competition=0.1))
            fc = m.get_layer("fc")
            ih = set_init(m, w_init) if pin else whash(fc.get_variable("weights"))
            inits.append(ih)
            m.fit(x)
            ph = whash(fc.get_variable("weights"))
            posts.append(ph)
            changed.append(ph != ih)
            outs.append(whash(np.asarray(m.forward(x))))
        except Exception as e:  # noqa: BLE001
            err.append(f"ep{ep}:{e!r}")
    return {
        "pin": pin,
        "n_ok": len(posts),
        "n_err": len(err),
        "errors": err[:3],
        "init_diversity": len(set(inits)),
        "weight_diversity_postfit": len(set(posts)),
        "output_diversity": len(set(outs)),
        "fit_changed_weights": (sum(changed), len(changed)),  # (n_changed, n_total)
    }


def main():
    dev = akida.devices()[0]
    x = make_trap_patterns()
    res = {
        "probe": "h921_hw_probe_v2_source_of_nondeterminism",
        "device": str(dev.version),
        "n_episodes": N_EPISODES,
        "A_pinned_nondegen": run_condition(dev, x, pin=True),
        "B_nopin_default": run_condition(dev, x, pin=False),
    }
    A, B = res["A_pinned_nondegen"], res["B_nopin_default"]
    res["reading"] = {
        "A_weight_div": A["weight_diversity_postfit"],
        "B_weight_div": B["weight_diversity_postfit"],
        "interpretation": (
            "A>1: chip learning intrinsically non-det (pinned) | "
            "A==1 & B>1: non-determinism is INIT-seeded, not learning | "
            "A==1 & B==1: learning fully deterministic, H_860 not repro'd"),
    }
    blob = json.dumps(res)
    with open("/tmp/h921_v2_result.json", "w") as fh:
        fh.write(blob + "\n")
    print(blob)


if __name__ == "__main__":
    main()
