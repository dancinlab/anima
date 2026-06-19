#!/usr/bin/env python3
"""substrate_akida.py — SubstrateAKIDA(Substrate): BrainChip AKD1000 substrate
with graceful numpy-LIF SW fallback + provenance.

Substrate ABC impl (substrate_base.py) for the neuromorphic-silicon path:

  - HW path  : `import akida` succeeds AND akida.devices() is non-empty.
               Wraps the on-chip threshold-and-fire forward of
               SUB_ENGINES/AKIDA/scripts/spontaneous_emission.py
               (FullyConnected(units=N, weights_bits=4, act_bits=1),
               integer threshold comparator on BackendType.Hardware).
               self.provenance == "akida-hw".
  - SW path  : akida absent OR no device -> akida_sw_lif numpy simulator
               (deterministic seed=187, same FullyConnected.forward interface).
               self.provenance == "akida-sw-fallback".

This is a SUBSTRATE SURFACE only — no system-prompt / persona / assistant
framing, no consciousness-engine framing of the bridge (AGENT bridge policy,
p1-p8). It exposes the chip's spontaneous spike raster to anima's
substrate-agnostic dynamics; emission/silence stays substrate-decided upstream.

Selected by anima_participant.build_substrate('akida') when AKIDA_BACKEND env is
set or --substrate akida is passed.
"""
from __future__ import annotations

import logging

import numpy as np
import torch

from substrate_base import Substrate
import akida_sw_lif

log = logging.getLogger("substrate_akida")


def _try_akida():
    """Return (akida_module_or_None, device_or_None). No raise."""
    try:
        import importlib
        ak = importlib.import_module("akida")
    except Exception:  # ImportError or partial-install error
        return (None, None)
    try:
        devs = ak.devices()
        if devs:
            return (ak, devs[0])
        return (ak, None)
    except Exception:
        return (ak, None)


class SubstrateAKIDA(Substrate):
    """BrainChip AKD1000 substrate with numpy-LIF SW fallback.

    The substrate's 'generation' is a spontaneous spike raster (anima's
    hardware-native p5 answer): a regime is run on the chip (HW) or the
    deterministic SW LIF (fallback) and the resulting spike train is
    surfaced as the substrate output. There is no token vocabulary here —
    vocab_size is the spike-event alphabet {0,1} (=2).
    """

    name = "akida"

    def __init__(self, device: str | None = None, regime: str = "R3_tonic_zero_input"):
        self.regime = regime
        self.vocab_size = 2                       # spike alphabet {0, 1}
        self._ak, self._dev = _try_akida()
        if self._ak is not None and self._dev is not None:
            self.provenance = "akida-hw"
            self.device = device or "akd1000"
            self._build_hw_model()
            log.info("SubstrateAKIDA HW path: device=%s version=%s",
                     self.device, getattr(self._dev, "version", "?"))
        else:
            self.provenance = "akida-sw-fallback"
            self.device = device or "cpu"
            self._N = akida_sw_lif.N
            self._IN = akida_sw_lif.IN
            log.info("SubstrateAKIDA SW fallback (akida %s, device %s) — numpy LIF seed=%d",
                     "absent" if self._ak is None else "present-no-device",
                     "none" if self._dev is None else "present", akida_sw_lif.SEED)

    # ── HW path setup (wraps spontaneous_emission.py model build) ───────────
    def _build_hw_model(self) -> None:
        ak = self._ak
        self._N = N = akida_sw_lif.N
        self._IN = IN = akida_sw_lif.IN
        m = ak.Model()
        m.add(ak.InputData(input_shape=(1, 1, IN), input_bits=4, name="in"))
        m.add(ak.FullyConnected(units=N, weights_bits=4, activation=True,
                                act_bits=1, name="lif"))
        m.map(self._dev)
        lif = m.get_layer("lif")
        W = lif.get_variable("weights")
        lif.set_variable("weights", np.ones_like(W))   # all-ones excitatory
        self._model = m
        self._lif = lif

    def _hw_forward(self, input_vec: np.ndarray, threshold_vec: np.ndarray) -> np.ndarray:
        """One on-chip forward — mirrors spontaneous_emission._spike_decision_on_chip."""
        self._lif.set_variable("threshold", threshold_vec.astype(np.int32))
        x = np.clip(input_vec, 0, 15).astype(np.uint8).reshape(1, 1, 1, self._IN)
        y = self._model.forward(x)
        return (y.reshape(-1) > 0).astype(np.int8)[:self._N]

    def _run_regime(self) -> dict:
        """Run the configured regime; route HW vs SW by provenance.
        Returns the regime record dict ({total_spikes, mean_spike_rate..., ...})."""
        if self.provenance == "akida-hw":
            thr_het = np.where(np.arange(self._N) % 2 == 0, -1, 8).astype(np.int32)
            spike_counts = []
            for _ in range(akida_sw_lif.T):
                sp = self._hw_forward(np.zeros(self._IN), thr_het)
                spike_counts.append(int(sp.sum()))
            total = int(sum(spike_counts))
            return {"total_spikes": total,
                    "mean_spike_rate_per_neuron_step":
                        round(total / float(self._N * akida_sw_lif.T), 5),
                    "spike_count_max": int(max(spike_counts)),
                    "step_varies": bool(np.std(spike_counts) > 1e-9)}
        sim = akida_sw_lif.simulate_regimes()
        return sim["regimes"].get(self.regime, sim["regimes"]["R3_tonic_zero_input"])

    # ── Substrate ABC ───────────────────────────────────────────────────────
    def generate(self, seed_text: str, max_new: int = 80,
                 lang_hint: str | None = None, **kw) -> str:
        """Surface the spontaneous spike raster as the substrate output.

        Returns a compact textual rendering of the spike train (per-step counts)
        — there is no token vocab; the chip's emission IS the output.
        """
        rec = self._run_regime()
        rate = rec.get("mean_spike_rate_per_neuron_step", 0.0)
        total = rec.get("total_spikes", 0)
        return (f"[akida:{self.provenance}] regime={self.regime} "
                f"spikes={total} rate={rate}")

    @torch.no_grad()
    def entropy_of_next(self, seed_text: str) -> tuple[float, torch.Tensor]:
        """Normalized entropy of the spike-rate (Bernoulli) + a small embed.

        For a spike train with mean rate p, H = -p log p - (1-p) log(1-p),
        normalized by log(2) -> [0, 1]. The embed is a fixed-width vector of
        the regime rates (substrate fingerprint).
        """
        rec = self._run_regime()
        p = float(rec.get("mean_spike_rate_per_neuron_step", 0.0))
        p = min(max(p, 1e-9), 1.0 - 1e-9)
        h = -(p * np.log(p) + (1.0 - p) * np.log(1.0 - p)) / np.log(2.0)
        emb = torch.tensor([p, 1.0 - p, h], dtype=torch.float32)
        return float(min(max(h, 0.0), 1.0)), emb

    def param_count(self) -> int:
        """Spike-pool size (N neurons x IN inputs) — there are no learned params
        on the AKD1000 LIF pool here (all-ones weights, per-unit threshold)."""
        return int(self._N * self._IN)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    s = SubstrateAKIDA()
    print("provenance:", s.provenance)
    print("generate:", s.generate(""))
    print("entropy:", s.entropy_of_next("")[0])
    print("param_count:", s.param_count())
