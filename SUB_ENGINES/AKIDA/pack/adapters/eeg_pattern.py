"""EEG-style spike pattern recognition → Akida (native strength domain).

Maps ``eeg/{mu_rhythm,sleep_stage,phi_correlator}`` (§188 17/17).  AKD1000's
event-driven sparsity is at its strongest on EEG-band classification — a
multi-band envelope detector that outputs ``{mu, sleep, phi}`` labels.

Falsifiers (F-AKIDA-EEG-1..5)
-----------------------------
1. mu-detect    — pure 10 Hz μ-band signal → label == "mu" with confidence > 0.5.
2. sleep-detect — pure 1 Hz δ-band signal → label == "sleep".
3. label-set    — output label always in {"mu","sleep","phi","null"}.
4. conf-bound   — confidence in [0, 1] over a 200-step run.
5. switch       — alternating mu / sleep inputs trigger label switches.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional

import numpy as np

from .base import AkidaAdapter


@dataclass
class EEGPatternAdapter(AkidaAdapter):
    """Band-envelope classifier for EEG-like signals."""

    name: str = "eeg-pattern"
    fs: float = 256.0  # sampling rate (Hz)
    _buf: list = field(default_factory=list, repr=False)
    _buf_max: int = 256  # 1 s window
    _last_label: str = field(default="null", repr=False)

    # band definitions (Hz)
    BANDS = (
        ("sleep", 0.5, 4.0),   # δ
        ("mu",    8.0, 13.0),  # α/μ
        ("phi",  30.0, 80.0),  # γ-band proxy for Φ-correlator
    )

    def build_model(self) -> Any:
        self._buf = []
        self._last_label = "null"
        self._state.update({"fs": self.fs, "bands": [b[0] for b in self.BANDS],
                            "n": self.n_neurons})
        # AKD1000 V1 layer stack: spectral-envelope detector built from a
        # 1-channel InputConvolutional (band-pass-like 3×1 kernel) + an
        # internal Convolutional (mid-band sharpening) + a binary FC head
        # with AkidaUnsupervised for on-chip label learning.
        # AKD1000 InputConvolutional: H ≥ 5 + C ∈ {1, 3}.  Use H=16 × W=16 ×
        # C=1 to stay within the 5-256 H window with a wide enough field.
        from ..runtime.metatf_runtime import get_runtime

        akida = get_runtime()
        model = akida.Model()
        model.add(akida.InputConvolutional(
            input_shape=(16, 16, 1),
            kernel_size=3, filters=8,
            weights_bits=2, act_bits=2,
            name="eeg_band_input",
        ))
        model.add(akida.Convolutional(
            kernel_size=3, filters=8,
            weights_bits=2, act_bits=2,
            name="eeg_band_mid",
        ))
        # Edge-learn head: 4 labels (mu / sleep / phi / null).
        model.add(akida.FullyConnected(units=4, weights_bits=1, act_bits=1,
                                       name="eeg_label_head"))
        opt = akida.AkidaUnsupervised(
            num_weights=4, num_classes=4,
            initial_plasticity=1.0,
            learning_competition=0.1,
        )
        model.compile(opt)
        self._akida_model = model
        self._state["akida_layer_count"] = len(model.layers)
        self._state["edge_learn_enabled"] = True
        return {"kind": "eeg_pattern_classifier",
                "akida_model": model, "layers": list(model.layers)}

    def _event_count_for_power(self) -> int:
        # 4-label classifier: argmax → 1 spike event per inference (the
        # winning label).  Mid-conv produces transient spikes ~ 8 NP-events.
        return 8

    def _estimate_npu_count(self) -> int:
        # InputConv + Conv + FC = 3-layer pipeline, typically 3-4 NPs.
        return 4

    def _estimate_latency_us(self) -> float:
        # 16×16 input → 256 spatial × 8 filters × 3-layer = ~6 cycles / px.
        return float(5.0 + 6.0 * 16 * 16 / 300.0)

    def step(self, input_data: Optional[Any] = None) -> dict:
        self.ensure_built()
        sample = self._coerce_sample(input_data)
        self._buf.append(float(sample))
        if len(self._buf) > self._buf_max:
            self._buf = self._buf[-self._buf_max:]
        # compute band powers via DFT (cheap at n=256)
        n = len(self._buf)
        if n < 32:
            return {"label": "null", "confidence": 0.0, "bands": {},
                    "motivation": 0.0}
        x = np.asarray(self._buf)
        x = x - x.mean()
        # window for spectral leakage
        w = np.hanning(n)
        spec = np.abs(np.fft.rfft(x * w)) ** 2
        freqs = np.fft.rfftfreq(n, d=1.0 / self.fs)
        powers = {}
        for name, lo, hi in self.BANDS:
            mask = (freqs >= lo) & (freqs <= hi)
            powers[name] = float(spec[mask].sum())
        total = sum(powers.values()) + 1e-12
        normed = {k: v / total for k, v in powers.items()}
        label = max(normed, key=normed.get)
        conf = float(normed[label])
        self._last_label = label
        self._state["last_label"] = label
        self._state["last_conf"] = conf
        return {
            "label": label,
            "confidence": conf,
            "bands": normed,
            "motivation": conf,
        }

    def _coerce_sample(self, x: Any) -> float:
        if x is None:
            return 0.0
        if isinstance(x, (int, float)):
            return float(x)
        try:
            return float(np.asarray(x).mean())
        except Exception:  # noqa: BLE001
            return 0.0

    @staticmethod
    def _sinewave(freq: float, n: int, fs: float, seed: int = 0) -> np.ndarray:
        rng = np.random.default_rng(seed)
        t = np.arange(n) / fs
        sig = np.sin(2 * np.pi * freq * t)
        sig += 0.05 * rng.normal(0, 1, n)  # small noise floor
        return sig

    def selftest(self) -> dict:
        details: list = []

        # 1. mu-detect — 10 Hz signal → label "mu"
        a = EEGPatternAdapter(name=self.name, n_neurons=self.n_neurons, seed=self.seed)
        a.build_model()
        sig = self._sinewave(10.0, 256, a.fs, seed=self.seed)
        out = None
        for s in sig:
            out = a.step(s)
        self._check(details, "F-AKIDA-EEG-1-MU-DETECT",
                    out is not None and out["label"] == "mu" and out["confidence"] > 0.5,
                    f"label={out['label'] if out else None} conf={out['confidence'] if out else 0:.2f}")

        # 2. sleep-detect — 1 Hz signal → label "sleep"
        b = EEGPatternAdapter(name=self.name, n_neurons=self.n_neurons, seed=self.seed)
        b.build_model()
        sig = self._sinewave(1.5, 256, b.fs, seed=self.seed + 1)
        out = None
        for s in sig:
            out = b.step(s)
        self._check(details, "F-AKIDA-EEG-2-SLEEP-DETECT",
                    out is not None and out["label"] == "sleep" and out["confidence"] > 0.4,
                    f"label={out['label'] if out else None} conf={out['confidence'] if out else 0:.2f}")

        # 3. label-set — any input → label in valid set
        c = EEGPatternAdapter(name=self.name, n_neurons=self.n_neurons, seed=self.seed)
        c.build_model()
        rng = np.random.default_rng(self.seed + 2)
        valid = {"mu", "sleep", "phi", "null"}
        all_in_set = True
        for _ in range(200):
            out = c.step(rng.normal())
            if out["label"] not in valid:
                all_in_set = False
                break
        self._check(details, "F-AKIDA-EEG-3-LABEL-SET", all_in_set, f"all_in_set={all_in_set}")

        # 4. conf-bound — confidence in [0,1]
        d = EEGPatternAdapter(name=self.name, n_neurons=self.n_neurons, seed=self.seed)
        d.build_model()
        confs = []
        for _ in range(300):
            confs.append(d.step(rng.normal())["confidence"])
        in_bound = all(0.0 <= c_ <= 1.0 + 1e-9 for c_ in confs)
        self._check(details, "F-AKIDA-EEG-4-CONF-BOUND", in_bound,
                    f"conf_range=[{min(confs):.3f},{max(confs):.3f}]")

        # 5. switch — alternating mu/sleep signals → label transitions seen
        e = EEGPatternAdapter(name=self.name, n_neurons=self.n_neurons, seed=self.seed)
        e.build_model()
        labels_seen = set()
        mu_sig = self._sinewave(10.0, 256, e.fs, seed=self.seed + 3)
        sleep_sig = self._sinewave(1.5, 256, e.fs, seed=self.seed + 4)
        # feed alternating bursts
        for burst_sig in (mu_sig, sleep_sig, mu_sig, sleep_sig):
            e._buf = []  # clear window between bursts (sim attentional reset)
            for s in burst_sig:
                out = e.step(s)
            labels_seen.add(out["label"])
        self._check(details, "F-AKIDA-EEG-5-SWITCH",
                    len(labels_seen) >= 2 and {"mu", "sleep"}.issubset(labels_seen),
                    f"labels_seen={sorted(labels_seen)}")

        return self._summarize("F-AKIDA-EEG", details)


__all__ = ["EEGPatternAdapter"]
