#!/usr/bin/env python3
# H_904 - on-chip plasticity measured on AKD1000 silicon.
# Measures the LEARNING half: Akida native on-chip edge-learning (AkidaUnsupervised),
# HW (AKD1000 BC.00.000.002, BackendType.Hardware) vs a deterministic SW-sim of the
# SAME update with an IDENTICAL fixed init weight + IDENTICAL deterministic inputs.
# Closes H_877 (inference byte-identical) by measuring the learning half: H_679 claims
# learning is HW != SW. g5 = CODE-measured. a_paper_negative_ok.
import os, json, hashlib, time
import numpy as np
import akida
from akida import Model, InputData, FullyConnected, AkidaUnsupervised

OUT = os.path.expanduser("~/h904_out")
os.makedirs(OUT, exist_ok=True)

SEED = 904
INC = 64
UNITS = 16
NSAMP = 20
NWEIGHTS_PER_NEURON = 12

# Deterministic binary spike samples (fixed seed) - identical for HW and SW.
np.random.seed(SEED)
samples = (np.random.rand(NSAMP, 1, 1, INC) > 0.6).astype(np.uint8)


def build_model():
    m = Model()
    m.add(InputData(name="input", input_shape=(1, 1, INC), input_bits=1))
    m.add(FullyConnected(name="fc", units=UNITS, weights_bits=1, activation=False))
    m.compile(AkidaUnsupervised(num_weights=NWEIGHTS_PER_NEURON))
    return m


def get_w(m):
    return np.array(m.get_layer("fc").variables["weights"])


def set_w(m, w):
    m.get_layer("fc").variables["weights"] = w.copy()


def h(a):
    return hashlib.sha256(np.ascontiguousarray(a).tobytes()).hexdigest()[:16]


def run_path(map_to_hw, init_w):
    m = build_model()
    set_w(m, init_w)                     # identical fixed init for both paths
    pre = get_w(m)
    if map_to_hw:
        devs = akida.devices()
        if not devs:
            raise RuntimeError("no akida device visible (device lock held by another proc?)")
        m.map(devs[0])
        set_w(m, init_w)                 # re-assert init after map (map may re-init on device)
        backend = "hardware:" + str(devs[0].version)
    else:
        backend = "software"
    outs = []
    for i in range(NSAMP):
        o = m.fit(samples[i:i + 1])      # unsupervised on-chip / on-sim update
        outs.append(np.array(o).astype(np.int64).ravel())
    post = get_w(m)
    return dict(backend=backend, pre=pre, post=post, outs=np.stack(outs))


result = {"hypothesis": "H_904", "seed": SEED, "akida_version": akida.__version__,
          "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
          "inc": INC, "units": UNITS, "nsamp": NSAMP, "num_weights": NWEIGHTS_PER_NEURON}

dev_list = [str(d.version) for d in akida.devices()]
print("[h904] akida", akida.__version__, "devices:", dev_list)

# Fixed init weight (one valid binary edge-learning init), injected into BOTH paths.
init_w = get_w(build_model())
result["init_weight_hash"] = h(init_w)

# --- HW path (on-chip learn on AKD1000 silicon) ---
hw = run_path(map_to_hw=True, init_w=init_w)
print("[h904] HW", hw["backend"], "post-w", h(hw["post"]), "out", h(hw["outs"]))

# --- SW path (deterministic sim of the same update) ---
sw = run_path(map_to_hw=False, init_w=init_w)
print("[h904] SW", sw["backend"], "post-w", h(sw["post"]), "out", h(sw["outs"]))

w_delta = np.abs(hw["post"].astype(np.int64) - sw["post"].astype(np.int64))
o_delta = np.abs(hw["outs"] - sw["outs"])
learn_hw = bool(np.any(hw["post"] != hw["pre"]))
learn_sw = bool(np.any(sw["post"] != sw["pre"]))

result.update(dict(
    devices=dev_list,
    hw_backend=hw["backend"], sw_backend=sw["backend"],
    hw_weight_hash=h(hw["post"]), sw_weight_hash=h(sw["post"]),
    hw_out_hash=h(hw["outs"]), sw_out_hash=h(sw["outs"]),
    learn_happened_hw=learn_hw, learn_happened_sw=learn_sw,
    weight_delta_max=int(w_delta.max()), weight_delta_sum=int(w_delta.sum()),
    weight_delta_nnz=int((w_delta != 0).sum()), weight_total=int(w_delta.size),
    out_delta_max=int(o_delta.max()), out_delta_sum=int(o_delta.sum()),
    out_delta_nnz=int((o_delta != 0).sum()), out_total=int(o_delta.size),
    hw_eq_sw_weights=bool(np.array_equal(hw["post"], sw["post"])),
    hw_eq_sw_outs=bool(np.array_equal(hw["outs"], sw["outs"])),
))

on_chip_learned = learn_hw
hw_neq_sw = (not result["hw_eq_sw_weights"]) or (not result["hw_eq_sw_outs"])
result["F_CLM_ONCHIP_on_chip_learned"] = on_chip_learned
result["F_CLM_ONCHIP_hw_neq_sw"] = hw_neq_sw
result["verdict"] = "GREEN" if (on_chip_learned and hw_neq_sw) else "RED"
result["verdict_reason"] = (
    "on-chip learn ran on AKD1000 AND HW!=SW quantified" if (on_chip_learned and hw_neq_sw)
    else ("HW==SW byte-exact (REFUTES H_679 learning-differs claim - major finding)"
          if (on_chip_learned and not hw_neq_sw)
          else "on-chip learning did not change weights (could not measure)"))

with open(os.path.join(OUT, "result.json"), "w") as f:
    json.dump(result, f, indent=2)
np.savez(os.path.join(OUT, "raw.npz"), hw_post=hw["post"], sw_post=sw["post"],
         hw_outs=hw["outs"], sw_outs=sw["outs"], samples=samples, init_w=init_w)

print("[h904] VERDICT", result["verdict"], "-", result["verdict_reason"])
print("[h904] weight_delta max", result["weight_delta_max"], "nnz",
      result["weight_delta_nnz"], "/", result["weight_total"])
print("[h904] out_delta max", result["out_delta_max"], "nnz",
      result["out_delta_nnz"], "/", result["out_total"])
print("[h904] wrote", os.path.join(OUT, "result.json"))
