"""MetaTF mock for Mac-local pre-arrival validation.

Mocks the small slice of the ``akida`` API surface used by anima adapters
so that ``pack.runtime.metatf_runtime`` can transparently fall back to a
numpy-based implementation when the real BrainChip SDK is unavailable.

API surface mocked
------------------
- ``akida.Model()``                    — empty model container
- ``akida.layers.InputData(**kw)``     — input layer factory
- ``akida.layers.FullyConnected(**kw)`` — dense layer factory
- ``akida.layers.Conv2D(**kw)``        — conv layer factory
- ``model.add(layer)``                 — stack a layer
- ``model.forward(input)``             — deterministic LCG mock inference
- ``model.fit(input, target)``         — mock Hebbian 1-shot update
- ``akida.devices()``                  — returns ``[MockDevice()]``
- ``device.program(model)``            — mock no-op

Determinism
-----------
``forward`` seeds a ``numpy.random.RandomState`` from a stable hash of the
input bytes, so identical input always yields identical mock spikes — this
lets falsifiers that depend on byte-equality (``F-AKIDA-*``-style) run on
Mac without a real device.
"""

from __future__ import annotations

from typing import Any

import numpy as np


# --------------------------------------------------------------------------- #
# layer-factory return type — opaque tuple keeps the mock cheap & inspectable
# --------------------------------------------------------------------------- #
LayerSpec = tuple  # ("FullyConnected", {"units": 128, ...})


class MockLayers:
    """Mock for the ``akida.layers`` namespace."""

    def InputData(self, **kwargs: Any) -> LayerSpec:  # noqa: N802 — mirror SDK
        return ("InputData", dict(kwargs))

    def FullyConnected(self, **kwargs: Any) -> LayerSpec:  # noqa: N802
        return ("FullyConnected", dict(kwargs))

    def Conv2D(self, **kwargs: Any) -> LayerSpec:  # noqa: N802
        return ("Conv2D", dict(kwargs))


class MockDevice:
    """Mock for the ``akida.Device`` returned by ``akida.devices()``."""

    def __init__(self, name: str = "AKD1000_MOCK") -> None:
        self._name = name

    @property
    def name(self) -> str:
        return self._name

    def program(self, model: "MockModel") -> bool:  # noqa: ARG002
        return True  # no-op on mock


class MockModel:
    """Mock for ``akida.Model`` — supports stacked layers + forward + fit."""

    def __init__(self) -> None:
        self.layers: list[LayerSpec] = []
        self.weights: dict[str, np.ndarray] = {}

    # ---- layer assembly -------------------------------------------------- #
    def add(self, layer: LayerSpec) -> None:
        self.layers.append(layer)

    # ---- inference -------------------------------------------------------- #
    def forward(self, input_data: np.ndarray) -> np.ndarray:
        """Deterministic mock inference — LCG seeded from input bytes.

        Returns a binary spike mask with the same shape as ``input_data``.
        """
        arr = np.asarray(input_data)
        try:
            raw = arr.tobytes()
        except AttributeError:
            raw = str(arr).encode("utf-8")
        seed = abs(hash(raw)) & 0xFFFFFFFF
        rng = np.random.RandomState(seed)
        return (rng.random(arr.shape) > 0.5).astype(np.int32)

    # ---- on-chip learning ------------------------------------------------ #
    def fit(self, input_data: np.ndarray, target: np.ndarray) -> None:
        """Mock 1-shot Hebbian update — ``W += lr * outer(input, target)``."""
        lr = 0.01
        in_vec = np.asarray(input_data).reshape(-1)
        tgt_vec = np.asarray(target).reshape(-1)
        key = "W"
        if key not in self.weights:
            self.weights[key] = np.zeros((in_vec.shape[0], tgt_vec.shape[0]), dtype=np.float64)
        # Hebbian outer-product update
        self.weights[key] += lr * np.outer(in_vec, tgt_vec)


class MetaTFMock:
    """Drop-in replacement for the ``akida`` top-level module on Mac."""

    def __init__(self) -> None:
        self.is_mock: bool = True
        self.version: str = "0.0.0-mock"
        self.__version__: str = self.version  # mirror SDK attribute
        self._layers = MockLayers()
        self._devices = [MockDevice()]

    # ---- factory --------------------------------------------------------- #
    def Model(self) -> MockModel:  # noqa: N802 — mirror SDK casing
        return MockModel()

    # ---- device list ----------------------------------------------------- #
    def devices(self) -> list[MockDevice]:
        return list(self._devices)

    # ---- namespace ------------------------------------------------------- #
    @property
    def layers(self) -> MockLayers:
        return self._layers

    # ---- debug ----------------------------------------------------------- #
    def __repr__(self) -> str:  # pragma: no cover — trivial
        return f"<MetaTFMock version={self.version} devices={len(self._devices)}>"


# pre-instantiated singleton — `from pack.mocks.metatf_mock import metatf_mock`
metatf_mock = MetaTFMock()


# --------------------------------------------------------------------------- #
# tiny self-test (no pytest needed — `python -m pack.mocks.metatf_mock`)
# --------------------------------------------------------------------------- #
def _selftest() -> dict:
    """Minimal sanity selftest — used by INSTALL.sh fallback path."""
    mock = MetaTFMock()
    m = mock.Model()
    m.add(mock.layers.InputData(shape=(8,)))
    m.add(mock.layers.FullyConnected(units=4))
    x = np.arange(8, dtype=np.float32)
    y1 = m.forward(x)
    y2 = m.forward(x)
    deterministic = bool(np.array_equal(y1, y2))
    m.fit(x, np.ones(4, dtype=np.float32))
    has_weights = "W" in m.weights and m.weights["W"].shape == (8, 4)
    devs = mock.devices()
    device_ok = len(devs) == 1 and devs[0].program(m) is True
    return {
        "version": mock.version,
        "is_mock": mock.is_mock,
        "forward_deterministic": deterministic,
        "fit_weights_ok": has_weights,
        "device_program_ok": device_ok,
    }


if __name__ == "__main__":  # pragma: no cover
    import json

    print(json.dumps(_selftest(), indent=2))
