#!/usr/bin/env python3
"""h923_qrng_seed_probe.py — H_923 M2: AKIDA init seeded by ANU quantum entropy.

Couples a DETERMINISTIC AKD1000 (H_922) with TRUE quantum entropy (ANU vacuum-
fluctuation bytes, qmirror tier=anu_legacy) at the init-seed lever H_921 located.

Each of N episodes draws a DISTINCT 64-byte window of the ANU buffer as the FC
init. The chip stays deterministic; entropy enters ONLY through the injected seed.

MEASURES (H_923 §2, g5 CODE-measured):
  D1 functional output diversity over N ANU-seeded episodes  -> variation present?
  D2 provenance = sha256 of ANU source + per-window offset    -> audit trail present?
  D3 determinism-preserved = same ANU window re-run -> byte-identical output?
     (confirms the chip is a deterministic function; entropy is single-entry/auditable)

HONEST non-claim (#123-A): statistical quality of ANU == chacha20 PRNG (JSD 23x under
NIST threshold). The value of QRNG here is PROVENANCE / auditability / ontology
(physical quantum origin), NOT better randomness numbers.

ANU bytes: mirror/qmirror/seed/qrng_lora_init_live.bin (1024B, anu_legacy,
request_id anu_legacy_1778042160, 2026-05-06). Path passed as argv[1].
"""
import hashlib
import json
import sys

import numpy as np
import akida

IN_DIM = 16
N_UNITS = 10
N_PATTERNS = 12
N_EPISODES = 16
WINDOW = 64  # bytes per episode (16 * 64 = 1024 = full ANU buffer)


def make_trap_patterns(seed: int = 7) -> np.ndarray:
    rng = np.random.default_rng(seed)
    core = np.zeros(IN_DIM, dtype=np.uint8)
    core[:8] = 1
    pats = np.tile(core, (N_PATTERNS, 1))
    for i in range(N_PATTERNS):
        pats[i, 8 + (i % 8)] = 1
    return pats.astype(np.uint8).reshape(N_PATTERNS, 1, 1, IN_DIM)


def init_from_anu(window: bytes):
    """Derive a binary FC init (IN_DIM x N_UNITS = 160 bits) from ANU bytes.
    Non-degenerate by construction (quantum bytes are unbiased random)."""
    bits = np.unpackbits(np.frombuffer(window, dtype=np.uint8))  # >=512 bits in 64B
    need = IN_DIM * N_UNITS
    w = bits[:need].astype(np.int8).reshape(IN_DIM, N_UNITS)
    return w


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


def run_one(dev, x, w):
    m = build_model(dev)
    m.compile(optimizer=akida.AkidaUnsupervised(num_weights=2, learning_competition=0.1))
    ih = set_init(m, w)
    m.fit(x)
    return ih, whash(np.asarray(m.forward(x)))


def main():
    anu_path = sys.argv[1]
    raw = open(anu_path, "rb").read()
    anu_sha = hashlib.sha256(raw).hexdigest()
    dev = akida.devices()[0]
    x = make_trap_patterns()

    out_hashes, init_hashes, prov = [], [], []
    for ep in range(N_EPISODES):
        win = raw[ep * WINDOW:(ep + 1) * WINDOW]
        w = init_from_anu(win)
        ih, oh = run_one(dev, x, w)
        init_hashes.append(ih)
        out_hashes.append(oh)
        prov.append({"ep": ep, "anu_offset": ep * WINDOW,
                     "win_sha": hashlib.sha256(win).hexdigest()[:12], "init_hash": ih})

    # D3: re-run episode 0's SAME ANU window -> must be byte-identical (chip deterministic)
    w0 = init_from_anu(raw[0:WINDOW])
    _, oh_repeat = run_one(dev, x, w0)
    determinism_preserved = (oh_repeat == out_hashes[0])

    out = {
        "probe": "h923_akida_qrng_coupling",
        "device": str(dev.version),
        "n_episodes": N_EPISODES,
        "entropy_source": {"path": anu_path, "tier": "anu_legacy (ANU vacuum-fluctuation)",
                           "sha256": anu_sha, "n_bytes": len(raw)},
        "D1_functional_output_diversity": len(set(out_hashes)),   # quantum-sourced variation
        "D2_provenance_trace": prov[:4],                          # auditable seed->ANU map (sample)
        "D2_all_distinct_windows": len({p["win_sha"] for p in prov}),
        "D3_determinism_preserved": bool(determinism_preserved),  # same seed -> same output
        "D3_repeat_hash_match": [out_hashes[0], oh_repeat],
        "verdict_rule": ("PASS if D1>1 AND D3 True AND D2 windows distinct ; "
                         "FALSIFIED if D1==1 (ANU did not create variation) "
                         "OR D3 False (chip not deterministic -> H_922 refuted)"),
        "honest_nonclaim": ("statistical quality ANU==PRNG (#123-A JSD 23x under NIST); "
                            "value = provenance/audit/ontology, NOT better randomness"),
    }
    blob = json.dumps(out)
    open("/tmp/h923_result.json", "w").write(blob + "\n")
    print(blob)


if __name__ == "__main__":
    main()
