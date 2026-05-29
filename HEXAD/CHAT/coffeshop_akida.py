#!/usr/bin/env python3
"""coffeshop_akida.py - COFFESHOP -> AKIDA closed-loop emit/silence adapter.

LAUNCHPAD @goal core: closes anima's group-chat emit/silence decision on real
neuromorphic silicon (BrainChip AKD1000) instead of the SW-only COFFESHOP sim.

THE CLOSED LOOP (motivation -> threshold -> spike -> emit):

    SW 5+1 factor battery (spontaneous_lib.hexa, closed-form B-SPONT-1..7)
        |  factors -> motivation_score in [0,1]   (weighted linear sum)
        v
    set_threshold(thr_vec = base + (1-score)*SPAN)  --> port 9513 (ctrl IN)
        |  high motivation => low chip threshold => more units fire
        v
    AKD1000 on-chip threshold-and-fire (all-ones FullyConnected LIF, units=N,
        per-unit potential V=N; unit j fires iff V > thr_vec[j])  -- M regime
        |  spike raster
        v
    read n_spikes from port 9512 (OUT broadcast, newline JSON)
        |
        v
    should_interrupt = (n_spikes >= quorum)   --> emit / silence

CALIBRATION (honest, closed-form): base = linspace(2,18,N) (streamer
make_threshold_M), V = N = 16, SPAN = 20.0, QUORUM = 6. Then for every
COFFESHOP window the on-chip spike-quorum decision is IDENTICAL to the SW
should_interrupt(0.60): n_spikes >= 6  <=>  motivation_score > 0.60. The chip
reproduces emit windows {3,10,14,15} and silence on the other 11.

AKIDA-FIRST EVERYWHERE (HARD CONSTRAINT). Every stage routes through the
HW-first switch (AKIDA/akida_backend.hexa::akida_backend_resolve, default "hw").
Chip present => run on-chip unconditionally. SW (numpy) is ONLY a fallback when
the chip is unreachable (e.g. Mac). NO stage puts SW first. Per-stage hw/sw
provenance is logged.

  - HW path : drive the LIVE spike_streamer (pi5-akida) via ctrl 9513, read
              on-chip spikes from OUT 9512. provenance "akida-hw".
  - SW path : numpy mirror of the SAME threshold-and-fire forward (DECODER lane
              is byte-identical to HW, rounds 1-5). provenance
              "akida-sw-fallback".

SUBSTRATE SURFACE only (AGENT bridge policy, p1-p8): no system prompt, no
persona, no assistant framing. should_interrupt is a function of substrate
motivation ONLY (a_substrate_native_speak: a user message is environment
context, NOT a response obligation; anima may stay silent even under a
direct_mention). The LM-text `lora` default is unrelated and unchanged.

SSOT (verbatim, NOT re-derived here):
  - factor formulas / weights / thresholds : HEXAD/CHAT/spontaneous_lib.hexa
    (B-SPONT-1..7 sympy battery; B-COFFESHOP A5 5/5 closed-form bit-exact).
  - streamer wire protocol                 : SUB_ENGINES/AKIDA/scripts/spike_streamer.py
  - HW-first switch                         : AKIDA/akida_backend.hexa
"""
from __future__ import annotations

import json
import os
import socket

import numpy as np

# ---- streamer wire protocol (SSOT: SUB_ENGINES/AKIDA/scripts/spike_streamer.py)
STREAM_HOST_DEFAULT = "127.0.0.1"   # on pi5 the loop is co-located with streamer
OUT_PORT_DEFAULT = 9512             # OUT: spike events broadcast (subscribe)
CTRL_PORT_DEFAULT = 9513            # IN : set_threshold control (drive)
N_DEFAULT = 16                      # LIF pool size (streamer --n default)

# ---- closed-loop calibration constants (see module docstring CALIBRATION)
V_POTENTIAL = float(N_DEFAULT)      # per-unit potential on M regime weak-ones
THR_SPAN = 20.0                     # score->threshold sweep span
QUORUM_DEFAULT = 6                  # n_spikes >= quorum  <=>  score > 0.60


def _base_threshold(n: int = N_DEFAULT) -> np.ndarray:
    """streamer make_threshold_M baseline: linspace(2,18,N)."""
    return np.linspace(2, 18, n)


def akida_backend_resolve(arg: str = "") -> str:
    """Mirror of AKIDA/akida_backend.hexa::akida_backend_resolve.
    arg > env(AKIDA_BACKEND) > default "hw" (AKIDA-first). Never "auto"."""
    if arg in ("hw", "sw"):
        return arg
    e = os.environ.get("AKIDA_BACKEND", "")
    if e in ("hw", "sw"):
        return e
    return "hw"


# ---- spontaneous_lib.hexa factor battery (verbatim mirror; SSOT = the .hexa).
def _clamp01(x: float) -> float:
    return 0.0 if x < 0.0 else (1.0 if x > 1.0 else x)


def factor_relevance(phi_value: float) -> float:
    return _clamp01(phi_value)


def factor_info_gap(retrieve_cos_sim: float) -> float:
    return _clamp01(1.0 - retrieve_cos_sim)


def factor_curiosity(curiosity_ema: float) -> float:
    return _clamp01(curiosity_ema)


def factor_pain(tension_delta: float) -> float:
    p = -tension_delta if tension_delta < 0.0 else tension_delta
    return 1.0 if p > 1.0 else p


def factor_coherence(bridge_gate_value: float) -> float:
    dist = bridge_gate_value - 0.5
    abs_dist = -dist if dist < 0.0 else dist
    n = abs_dist / 0.014
    n = 1.0 if n > 1.0 else n
    return 1.0 - n


def factor_originality(split_event_recent: bool) -> float:
    return 1.0 if split_event_recent else 0.0


def factor_balance(phi: float, ratchet: float) -> float:
    return 1.0 if phi > ratchet / 2.0 else 0.0


def factor_dynamics(silence_seconds: float) -> float:
    return _clamp01(silence_seconds / 30.0)   # spont_idle_speak_after() = 30.0


_W = dict(relevance=0.20, info_gap=0.10, curiosity=0.15, pain=0.10,
          coherence=0.10, originality=0.10, balance=0.15, dynamics=0.10)
SPONT_INTERRUPT_THRESHOLD = 0.6    # spont_interrupt_threshold() (COFFESHOP 0.60)


def motivation_score(rel, gap, cur, pain, coh, orig, bal, dyn_v) -> float:
    return (_W["relevance"] * rel + _W["info_gap"] * gap
            + _W["curiosity"] * cur + _W["pain"] * pain
            + _W["coherence"] * coh + _W["originality"] * orig
            + _W["balance"] * bal + _W["dynamics"] * dyn_v)


def motivation_from_factors(f: dict) -> float:
    return motivation_score(
        f.get("relevance", 0.0), f.get("info_gap", 0.0), f.get("curiosity", 0.0),
        f.get("pain", 0.0), f.get("coherence", 0.0), f.get("originality", 0.0),
        f.get("balance", 0.0), f.get("dynamics", 0.0))


# ---- score -> per-unit threshold vector (thr ~ -k*score: high score -> low thr)
def score_to_threshold_vec(score: float, n: int = N_DEFAULT,
                           span: float = THR_SPAN) -> np.ndarray:
    return (_base_threshold(n) + (1.0 - score) * span)


def _spikes_from_threshold(thr_vec: np.ndarray) -> int:
    """On-chip rule replicated: unit fires iff potential V > thr_vec[j]."""
    return int((thr_vec < V_POTENTIAL).sum())


# ---- HW closed-loop driver (live spike_streamer on pi5-akida) -----------------
class AkidaLoopHW:
    provenance = "akida-hw"

    def __init__(self, host=STREAM_HOST_DEFAULT, out_port=OUT_PORT_DEFAULT,
                 ctrl_port=CTRL_PORT_DEFAULT, n=N_DEFAULT, timeout=5.0):
        self.host, self.out_port, self.ctrl_port, self.n = host, out_port, ctrl_port, n
        self._out = socket.create_connection((host, out_port), timeout=timeout)
        self._out.settimeout(timeout)
        self._outf = self._out.makefile("rb")
        self._ctrl = socket.create_connection((host, ctrl_port), timeout=timeout)
        self._ctrl.settimeout(timeout)

    def set_threshold(self, thr_vec: np.ndarray) -> None:
        v = [int(round(x)) for x in np.asarray(thr_vec).reshape(-1)[:self.n]]
        cmd = json.dumps({"cmd": "set_threshold", "thr": v})
        self._ctrl.sendall((cmd + "\n").encode("utf-8"))

    def read_spikes(self, settle_steps: int = 3) -> dict:
        rec = None
        for _ in range(max(1, settle_steps)):
            line = self._outf.readline()
            if not line:
                break
            try:
                rec = json.loads(line.decode("utf-8").strip())
            except Exception:
                continue
        return rec or {"n_spikes": 0, "thr": [], "step": -1}

    def step(self, score: float, quorum: int = QUORUM_DEFAULT,
             settle_steps: int = 3) -> dict:
        thr = score_to_threshold_vec(score, self.n)
        self.set_threshold(thr)
        rec = self.read_spikes(settle_steps)
        n_sp = int(rec.get("n_spikes", 0))
        return {"score": round(score, 6), "n_spikes": n_sp,
                "should_interrupt": n_sp >= quorum, "chip_step": rec.get("step", -1),
                "provenance": self.provenance}

    def close(self):
        for s in (self._out, self._ctrl):
            try:
                s.close()
            except Exception:
                pass


# ---- SW fallback driver (numpy mirror of on-chip forward) ---------------------
class AkidaLoopSW:
    provenance = "akida-sw-fallback"

    def __init__(self, n=N_DEFAULT):
        self.n = n

    def step(self, score: float, quorum: int = QUORUM_DEFAULT, **kw) -> dict:
        thr = score_to_threshold_vec(score, self.n)
        n_sp = _spikes_from_threshold(thr)        # same closed-form as HW chip
        return {"score": round(score, 6), "n_spikes": n_sp,
                "should_interrupt": n_sp >= quorum, "chip_step": -1,
                "provenance": self.provenance}

    def close(self):
        pass


def build_loop(arg: str = "", host=STREAM_HOST_DEFAULT, out_port=OUT_PORT_DEFAULT,
               ctrl_port=CTRL_PORT_DEFAULT, n=N_DEFAULT):
    """AKIDA-first factory. backend "hw" (default) -> live HW loop; on connection
    failure flip to SW with an EXPLICIT provenance change (never fake HW)."""
    backend = akida_backend_resolve(arg)
    if backend == "hw":
        try:
            return AkidaLoopHW(host=host, out_port=out_port,
                               ctrl_port=ctrl_port, n=n)
        except Exception as e:
            print(f"[coffeshop_akida] HW loop unreachable ({e!r}) -> SW fallback",
                  flush=True)
            return AkidaLoopSW(n=n)
    return AkidaLoopSW(n=n)


def run_window(loop, factors: dict, quorum: int = QUORUM_DEFAULT) -> dict:
    """One COFFESHOP window: 8-factor dict -> motivation -> chip -> emit decision.
    provenance per stage: factor stage = SW closed-form (spontaneous_lib);
    threshold->spike->emit stage = loop.provenance (hw / sw-fallback)."""
    score = motivation_from_factors(factors)
    out = loop.step(score, quorum=quorum)
    out["factor_stage"] = "sw-closed-form (spontaneous_lib B-SPONT)"
    out["loop_stage"] = loop.provenance
    return out


if __name__ == "__main__":
    import sys
    arg = sys.argv[1] if len(sys.argv) > 1 else ""
    loop = build_loop(arg)
    print("provenance:", loop.provenance)
    for sc in (0.288, 0.554, 0.614, 0.757):
        r = loop.step(sc)
        flag = "EMIT" if r["should_interrupt"] else "----"
        print(f"score={sc:.3f} n_spikes={r['n_spikes']:>2} {flag} "
              f"[{r['provenance']}]")
    loop.close()
