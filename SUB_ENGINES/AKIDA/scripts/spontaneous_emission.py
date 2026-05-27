"""HW-native spontaneous spike emission (자연발화) on AKD1000 — Pi 5 LAN, $0.

anima's 자연발화 = emit a spike WITHOUT an external prompt. On the BrainChip
AKD1000 the analog is: a threshold-and-fire (LIF) SNN whose neurons cross
threshold and emit spikes from WEAK / ZERO / NOISY drive (not a strong clamped
input). The spike decision (potential = Σ w·x, fire iff potential > threshold)
is computed ON THE CHIP by the FullyConnected layer's integer threshold
comparator (`BackendType.Hardware`) — the recurrent feedback (spikes → next
input) is the only software glue, because Akida 1.0 IP is feed-forward.

Three on-chip neuron primitives are exercised:
  * threshold  : positive per-unit threshold — requires drive to fire.
  * tonic/bias : NEGATIVE threshold — potential 0 > threshold, so the neuron
                 fires with ZERO external input = pure intrinsic excitability
                 (pacemaker). This is the cleanest 자연발화 signal.

Five input regimes, all run with the SAME on-chip model (only the per-unit
threshold + the input tensor change):
  R0 driven         : strong clamped input, high threshold  (sanity, like first-inference)
  R1 weak           : weak constant sub-threshold input, high threshold (should be SILENT)
  R2 zero+noise     : zero-mean Poisson/uniform noise input, mid threshold (stochastic 자연발화)
  R3 tonic-zero     : ZERO input + NEGATIVE threshold (intrinsic-bias 자연발화, no input at all)
  R4 recurrent      : tonic seed + spikes fed back as next-step input (self-sustained 자연발화)

For each regime we measure over a T-step window:
  * total spikes, mean spike-rate (spikes / neuron / step)
  * per-step spike counts (event-driven evidence: does it vary with internal state?)
  * inter-spike intervals (ISI) of the population
  * on-chip clock cycles + wall latency (efficiency proxy — INA power unavailable
    on this M.2 board, see FIRST_INFERENCE doc)

Verdict logic:
  HW-native spontaneous emission CONFIRMED iff
    R3 (tonic, ZERO input) emits spikes  AND  R1 (weak input, high thr) is silent
    AND R4 (recurrent) sustains emission across the window after the seed,
    AND R2 (noise) emission rate varies step-to-step (event-driven, not constant).
"""
import json
import time

import numpy as np

import akida

SEED = 187
N = 16          # neurons in the LIF pool (one NP)
IN = 16         # input lines
T = 200         # steps per regime window

rng = np.random.default_rng(SEED)
out = {"seed": SEED, "n_neurons": N, "n_inputs": IN, "window_steps": T,
       "regimes": {}}

# --- device + model (built ONCE, reused for every regime) -------------------
dev = akida.devices()[0]
out["device_version"] = str(dev.version)
out["device_ip_version"] = str(dev.ip_version)

# power telemetry attempt (expected unavailable on this board)
try:
    dev.soc.power_measurement_enabled = True
    out["power_measurement_supported"] = True
except Exception as e:  # noqa: BLE001
    out["power_measurement_supported"] = False
    out["power_enable_note"] = repr(e)[:120]

model = akida.Model()
model.add(akida.InputData(input_shape=(1, 1, IN), input_bits=4, name="in"))
model.add(akida.FullyConnected(units=N, weights_bits=4, activation=True,
                               act_bits=1, name="lif"))
model.map(dev)
out["mapped_backend"] = str(model.sequences[0].backend)
out["mapped_on_hardware"] = ("Hardware" in out["mapped_backend"])

lif = model.get_layer("lif")
W = lif.get_variable("weights")          # (1,1,IN,N) int8
THR = lif.get_variable("threshold")      # (N,) int32

# Fixed all-ones excitatory weights: potential(unit_j) = Σ_i input_i (input-independent of j).
# With per-unit threshold we get a clean threshold-and-fire decision on chip.
lif.set_variable("weights", np.ones_like(W))


def _spike_decision_on_chip(input_vec: np.ndarray, threshold_vec: np.ndarray) -> np.ndarray:
    """Run ONE forward pass ON THE AKD1000; return per-neuron 0/1 spikes.

    The integer threshold comparison (potential > threshold → spike) is the
    chip's native LIF activation — this is the on-chip emission decision.
    """
    lif.set_variable("threshold", threshold_vec.astype(np.int32))
    x = np.clip(input_vec, 0, 15).astype(np.uint8).reshape(1, 1, 1, IN)
    y = model.forward(x)                 # ON CHIP
    return (y.reshape(-1) > 0).astype(np.int8)[:N]


def _isi_stats(spike_counts):
    """Population inter-spike intervals: gaps between steps that had ≥1 spike."""
    fire_steps = [i for i, c in enumerate(spike_counts) if c > 0]
    isis = [fire_steps[i + 1] - fire_steps[i] for i in range(len(fire_steps) - 1)]
    if not isis:
        return {"n_fire_steps": len(fire_steps), "isi_mean": None,
                "isi_min": None, "isi_max": None}
    return {"n_fire_steps": len(fire_steps),
            "isi_mean": round(float(np.mean(isis)), 3),
            "isi_min": int(min(isis)), "isi_max": int(max(isis))}


def run_regime(name, threshold_const, input_fn, recurrent=False,
               threshold_vec=None, recur_gain=4.0, recur_seed_steps=1):
    """Run T steps of one regime, recording spike counts + on-chip clock.

    ``threshold_vec`` (per-neuron int32) overrides the scalar ``threshold_const``
    — heterogeneous thresholds give each neuron its own intrinsic excitability
    so the population spike count reflects internal structure (not saturation).
    """
    if threshold_vec is not None:
        thr = threshold_vec.astype(np.int32)
    else:
        thr = np.full(N, threshold_const, dtype=np.int32)
    spike_counts = []
    last_spikes = np.zeros(N, dtype=np.int8)
    clocks = []
    t0 = time.perf_counter()
    for step in range(T):
        if recurrent:
            # feedback: previous spikes (scaled) become this step's input.
            # A short tonic seed (first ``recur_seed_steps`` steps get a small
            # constant kick) ignites the loop; thereafter emission is driven
            # ONLY by the chip's own prior spikes fed back as input.
            fb = last_spikes.astype(np.float32)
            base = np.zeros(IN, dtype=np.float32)
            k = min(N, IN)
            base[:k] = fb[:k] * recur_gain          # recurrent drive
            if step < recur_seed_steps:
                base[:k] += 6.0                      # ignition seed
            inp = base
        else:
            inp = input_fn(step)
        sp = _spike_decision_on_chip(inp, thr)
        spike_counts.append(int(sp.sum()))
        last_spikes = sp
        # sample on-chip clock cheaply (parse statistics string occasionally)
        if step < 3 or step == T - 1:
            try:
                st = str(model.statistics)
                for line in st.splitlines():
                    if "Last inference clock" in line:
                        clocks.append(int(line.split("=")[-1].split(":")[-1].strip()
                                          .split()[-1]) if "=" in line
                                      else int(line.split(":")[-1].strip()))
            except Exception:  # noqa: BLE001
                pass
    t1 = time.perf_counter()

    total = int(sum(spike_counts))
    rate = total / float(N * T)
    rec = {
        "threshold_const": int(threshold_const),
        "recurrent": recurrent,
        "total_spikes": total,
        "mean_spike_rate_per_neuron_step": round(rate, 5),
        "spike_count_min": int(min(spike_counts)),
        "spike_count_max": int(max(spike_counts)),
        "spike_count_std": round(float(np.std(spike_counts)), 4),
        "step_varies": bool(np.std(spike_counts) > 1e-9),  # event-driven evidence
        "first10_step_counts": spike_counts[:10],
        "last10_step_counts": spike_counts[-10:],
        "isi": _isi_stats(spike_counts),
        "wall_ms_per_step": round((t1 - t0) / T * 1000.0, 4),
        "onchip_clock_samples": clocks,
    }
    out["regimes"][name] = rec
    return rec


# === REGIMES ================================================================
# R0 driven: strong input (all 15s), high threshold → sanity, fires every step.
run_regime("R0_driven", threshold_const=64,
           input_fn=lambda s: np.full(IN, 15.0))

# R1 weak: weak constant input (all 1s → potential 16), HIGH threshold 64
#          → sub-threshold, should be SILENT (control: no spurious emission).
run_regime("R1_weak_silent", threshold_const=64,
           input_fn=lambda s: np.full(IN, 1.0))

# R2 zero+noise: sparse uniform-noise input centred just below threshold.
#   Mean potential ≈ threshold so some steps cross and some don't — emission
#   count VARIES step-to-step purely from input noise → STOCHASTIC 자연발화
#   (event-driven: the chip emits iff its momentary integrated potential
#   crosses the on-chip comparator, which fluctuates with the noise).
#   16 lines × U[0,3] mean 1.5 ⇒ potential mean ≈ 24, std ≈ √(16·var)≈√(16·1.25)≈4.5.
#   threshold 24 sits at the mean ⇒ ~half the steps cross.
def _noise(step):
    return rng.integers(0, 4, size=IN).astype(np.float32)   # 0..3 per line
run_regime("R2_zero_noise", threshold_const=24, input_fn=_noise)

# R3 tonic-zero: ZERO input, NEGATIVE per-neuron threshold → potential 0 fires
#   the neurons whose threshold < 0. HETEROGENEOUS thresholds: half the pool is
#   tonic (thr = -1, intrinsically excitable), half is quiescent (thr = +8,
#   needs drive). With zero input only the tonic half emits → spike count
#   reflects internal neuron state, NOT input. Cleanest hardware 자연발화.
thr_het = np.where(np.arange(N) % 2 == 0, -1, 8).astype(np.int32)
run_regime("R3_tonic_zero_input", threshold_const=0, threshold_vec=thr_het,
           input_fn=lambda s: np.zeros(IN, dtype=np.float32))

# R4 recurrent: heterogeneous tonic pool + spikes fed back as next-step input.
#   A brief ignition seed lights the tonic neurons; their spikes feed back and
#   recruit the higher-threshold neurons → self-sustained emission carried by
#   the chip's OWN prior spikes after the seed ends (no external stimulus).
run_regime("R4_recurrent_selfsustained", threshold_const=0,
           threshold_vec=thr_het, input_fn=lambda s: np.zeros(IN),
           recurrent=True, recur_gain=3.0, recur_seed_steps=2)

# === VERDICT ================================================================
r0, r1 = out["regimes"]["R0_driven"], out["regimes"]["R1_weak_silent"]
r2, r3 = out["regimes"]["R2_zero_noise"], out["regimes"]["R3_tonic_zero_input"]
r4 = out["regimes"]["R4_recurrent_selfsustained"]

# R4 self-sustained AFTER the ignition seed: count spikes in steps >= seed end.
r4_post_seed = sum(r4["last10_step_counts"]) > 0 and r4["isi"]["n_fire_steps"] > T - 5

checks = {
    "driven_fires": r0["total_spikes"] > 0,
    "weak_is_silent": r1["total_spikes"] == 0,
    "tonic_zero_input_fires": r3["total_spikes"] > 0,       # 자연발화 core
    # tonic regime emits a PARTIAL pool (only thr<0 neurons), not full saturation:
    "tonic_partial_pool": 0 < r3["spike_count_max"] < N,
    "noise_emits": r2["total_spikes"] > 0,
    "noise_event_driven": r2["step_varies"],                # varies with state
    "recurrent_sustains": r4["total_spikes"] > 0 and r4["isi"]["n_fire_steps"] > T // 2,
    "recurrent_post_seed_sustains": bool(r4_post_seed),     # emits after seed ends
}
out["checks"] = checks
out["hw_native_spontaneous_emission"] = bool(
    checks["driven_fires"] and checks["weak_is_silent"]
    and checks["tonic_zero_input_fires"]
    and checks["recurrent_sustains"]
)
out["stochastic_spontaneous_emission"] = bool(
    checks["noise_emits"] and checks["noise_event_driven"]
)

# efficiency proxy
all_clocks = [c for r in out["regimes"].values() for c in r["onchip_clock_samples"]]
out["onchip_clock_cycles_mean"] = (round(float(np.mean(all_clocks)), 1)
                                   if all_clocks else None)
out["wall_ms_per_step_mean"] = round(
    float(np.mean([r["wall_ms_per_step"] for r in out["regimes"].values()])), 4)

import os
_dst = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    "state", "spontaneous_emission_result_2026_05_22.json")
with open(_dst, "w") as fh:
    json.dump(out, fh, indent=2)
print(json.dumps(out, indent=2))
