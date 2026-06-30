"""MetaTF mock for Mac-local pre-arrival validation.

Mocks the slice of the ``akida`` API surface used by anima adapters so that
``pack.runtime.metatf_runtime`` can transparently fall back to a numpy-based
implementation when the real BrainChip SDK is unavailable.

API surface mocked — matched against real BrainChip API
-------------------------------------------------------
Per ``doc/metatf_api_model.md`` and ``...layers.md``:

- ``akida.Model(filename=None, layers=None)`` — empty / load-from-file / from-list
- ``akida.InputData(input_shape, input_bits=4, name='')``
- ``akida.InputConvolutional(...)``      — V1 first-layer conv (filtered fields)
- ``akida.Convolutional(kernel_size, filters, ...)``  — V1 inner conv (NOT Conv2D)
- ``akida.SeparableConvolutional(...)``
- ``akida.FullyConnected(units, weights_bits=1, activation=True, act_bits=1)``
- ``akida.Padding`` / ``akida.PoolType`` / ``akida.ActivationType`` enums
- ``akida.LayerType`` enum
- ``akida.HwVersion`` enum (NSoC_v1)
- ``akida.ClockMode`` enum (Performance/Economy/LowPower)
- ``akida.MapMode`` enum (AllNps/HwPr/Minimal)
- ``akida.AkidaUnsupervised(num_weights, num_classes=1, ...)`` — edge-learn optimizer
- ``akida.devices()`` → list[MockHwDevice]
- ``akida.AKD1000()`` → virtual device factory
- ``model.add(layer)``                 — stack a layer
- ``model.compile(optimizer)``         — bind edge-learn optimizer (required for fit)
- ``model.forward(uint8 input)``       — deterministic LCG mock inference (returns int32)
- ``model.predict(input)``             — float32 version of forward
- ``model.fit(inputs, input_labels)``  — Hebbian sw approximation of AkidaUnsupervised
- ``model.map(device, hw_only=False, mode=MapMode.AllNps)`` — bind to device
- ``model.add_classes(n)``             — incremental class expansion
- ``model.save(path)`` / ``Model("foo.fbz")`` — round-trip via pickle
- ``model.summary()`` / ``model.input_shape`` / ``model.layers`` / ``model.statistics``
- ``device.version`` / ``device.mesh`` / ``device.soc`` / ``device.power_meter``
- ``device.program(...)`` (deprecated alias for ``model.map(device)``)

Backwards compat (BEFORE the 2026-05-21 BrainChip survey)
---------------------------------------------------------
- ``akida.layers.FullyConnected(**kw)`` — still works (V2-style namespace alias)
- ``akida.layers.Conv2D(**kw)`` — alias for ``akida.Convolutional`` (V2 forward-compat)
- ``MockModel.fit(input, target)`` — still works if both args are numpy arrays
  (old Hebbian signature) — internally coerced to ``(inputs, input_labels)`` form

Determinism
-----------
``forward`` seeds a ``numpy.random.RandomState`` from a stable hash of the
input bytes, so identical input always yields identical mock spikes — this
lets falsifiers that depend on byte-equality (``F-AKIDA-*-5-PARITY``-style)
run on Mac without a real device.
"""

from __future__ import annotations

import enum
import os
import pickle
from dataclasses import dataclass, field
from typing import Any, Optional, Sequence

import numpy as np


# --------------------------------------------------------------------------- #
# enums — matching real `akida.*` enums
# --------------------------------------------------------------------------- #
class HwVersion(enum.Enum):
    """Mirror of ``akida.HwVersion``."""
    NSoC_v1 = "NSoC_v1"   # AKD1000 — pack target
    NSoC_v2 = "NSoC_v2"   # AKD2000 — future, out-of-scope


class ClockMode(enum.Enum):
    """Mirror of ``akida.ClockMode``."""
    Performance = "Performance"
    Economy = "Economy"
    LowPower = "LowPower"


class MapMode(enum.Enum):
    """Mirror of ``akida.MapMode``."""
    AllNps = "AllNps"
    HwPr = "HwPr"
    Minimal = "Minimal"


class Padding(enum.Enum):
    """Mirror of ``akida.Padding``."""
    Valid = "Valid"
    Same = "Same"
    SameUpper = "SameUpper"


class PoolType(enum.Enum):
    """Mirror of ``akida.PoolType``."""
    NoPooling = "NoPooling"
    Max = "Max"
    Average = "Average"


class ActivationType(enum.Enum):
    """Mirror of ``akida.ActivationType``."""
    NoActivation = "NoActivation"
    ReLU = "ReLU"
    LUT = "LUT"   # V2 only — included for forward-compat


class LayerType(enum.Enum):
    """Mirror of ``akida.LayerType`` (V1 subset for AKD1000)."""
    InputData = "InputData"
    InputConvolutional = "InputConvolutional"
    Convolutional = "Convolutional"
    SeparableConvolutional = "SeparableConvolutional"
    FullyConnected = "FullyConnected"
    # V2 (alias for forward-compat — would never actually map to AKD1000):
    Conv2D = "Conv2D"
    InputConv2D = "InputConv2D"


# --------------------------------------------------------------------------- #
# Layer dataclasses — match real BrainChip layer signatures
# --------------------------------------------------------------------------- #
@dataclass
class MockLayer:
    """Base for all mock layers — opaque, inspectable, picklable."""
    layer_type: LayerType
    name: str = ""
    params: dict = field(default_factory=dict)

    def __repr__(self) -> str:  # pragma: no cover
        return f"<{self.layer_type.value} name={self.name!r} params={self.params}>"


def InputData(input_shape: Sequence[int], input_bits: int = 4, name: str = "") -> MockLayer:  # noqa: N802
    """Mirror ``akida.InputData(input_shape, input_bits=4, name='')``."""
    if input_bits not in (1, 2, 4, 8):
        raise ValueError(f"input_bits must be 1, 2, 4, or 8; got {input_bits}")
    return MockLayer(
        layer_type=LayerType.InputData,
        name=name,
        params={"input_shape": tuple(input_shape), "input_bits": input_bits},
    )


def InputConvolutional(  # noqa: N802
    input_shape: Sequence[int],
    kernel_size: int,
    filters: int,
    name: str = "",
    padding: Padding = Padding.Same,
    kernel_stride: tuple = (1, 1),
    weights_bits: int = 1,
    pool_size: tuple = (-1, -1),
    pool_type: PoolType = PoolType.NoPooling,
    pool_stride: tuple = (-1, -1),
    activation: bool = True,
    act_bits: int = 1,
    padding_value: int = 0,
) -> MockLayer:
    """Mirror ``akida.InputConvolutional`` — AKD1000 first-layer conv."""
    if len(input_shape) != 3 or input_shape[2] not in (1, 3):
        raise ValueError(f"InputConvolutional needs (H,W,C) with C ∈ {{1,3}}; got {input_shape}")
    if kernel_size not in (3, 5, 7):
        raise ValueError(f"InputConvolutional kernel_size must be 3, 5, or 7; got {kernel_size}")
    return MockLayer(
        layer_type=LayerType.InputConvolutional,
        name=name,
        params=dict(
            input_shape=tuple(input_shape), kernel_size=kernel_size, filters=filters,
            padding=padding, kernel_stride=tuple(kernel_stride),
            weights_bits=weights_bits, pool_size=tuple(pool_size), pool_type=pool_type,
            pool_stride=tuple(pool_stride), activation=activation, act_bits=act_bits,
            padding_value=padding_value,
        ),
    )


def Convolutional(  # noqa: N802
    kernel_size: int,
    filters: int,
    name: str = "",
    padding: Padding = Padding.Same,
    kernel_stride: tuple = (1, 1),
    weights_bits: int = 1,
    pool_size: tuple = (-1, -1),
    pool_type: PoolType = PoolType.NoPooling,
    pool_stride: tuple = (-1, -1),
    activation: bool = True,
    act_bits: int = 1,
) -> MockLayer:
    """Mirror ``akida.Convolutional`` — AKD1000 inner conv (NOT named ``Conv2D``)."""
    if kernel_size not in (1, 3, 5, 7):
        raise ValueError(f"Convolutional kernel_size must be 1, 3, 5, or 7; got {kernel_size}")
    if kernel_stride[0] == 2 and kernel_size != 3:
        raise ValueError("Convolutional stride=2 only allowed for 3×3 kernel on AKD1000")
    if weights_bits not in (1, 2, 4):
        raise ValueError(f"Convolutional weights_bits must be 1, 2, or 4; got {weights_bits}")
    return MockLayer(
        layer_type=LayerType.Convolutional,
        name=name,
        params=dict(
            kernel_size=kernel_size, filters=filters, padding=padding,
            kernel_stride=tuple(kernel_stride), weights_bits=weights_bits,
            pool_size=tuple(pool_size), pool_type=pool_type,
            pool_stride=tuple(pool_stride), activation=activation, act_bits=act_bits,
        ),
    )


def SeparableConvolutional(  # noqa: N802
    kernel_size: int,
    filters: int,
    name: str = "",
    padding: Padding = Padding.Same,
    kernel_stride: tuple = (1, 1),
    weights_bits: int = 2,   # default differs from Convolutional per real SDK
    pool_size: tuple = (-1, -1),
    pool_type: PoolType = PoolType.NoPooling,
    pool_stride: tuple = (-1, -1),
    activation: bool = True,
    act_bits: int = 1,
) -> MockLayer:
    """Mirror ``akida.SeparableConvolutional`` — depthwise-separable for AKD1000."""
    return MockLayer(
        layer_type=LayerType.SeparableConvolutional,
        name=name,
        params=dict(
            kernel_size=kernel_size, filters=filters, padding=padding,
            kernel_stride=tuple(kernel_stride), weights_bits=weights_bits,
            pool_size=tuple(pool_size), pool_type=pool_type,
            pool_stride=tuple(pool_stride), activation=activation, act_bits=act_bits,
        ),
    )


def FullyConnected(  # noqa: N802
    units: int,
    name: str = "",
    weights_bits: int = 1,
    activation: bool = True,
    act_bits: int = 1,
) -> MockLayer:
    """Mirror ``akida.FullyConnected(units, name='', weights_bits=1, activation=True, act_bits=1)``."""
    if units <= 0:
        raise ValueError(f"FullyConnected units must be > 0; got {units}")
    if weights_bits not in (1, 2, 4):
        raise ValueError(f"FullyConnected weights_bits must be 1, 2, or 4; got {weights_bits}")
    if act_bits not in (1, 2, 4):
        raise ValueError(f"FullyConnected act_bits must be 1, 2, or 4; got {act_bits}")
    return MockLayer(
        layer_type=LayerType.FullyConnected,
        name=name,
        params=dict(units=units, weights_bits=weights_bits,
                    activation=activation, act_bits=act_bits),
    )


# --------------------------------------------------------------------------- #
# Backwards-compat: ``akida.layers.FullyConnected(**kw)`` (V2 namespace style)
# --------------------------------------------------------------------------- #
class MockLayers:
    """Mock for the ``akida.layers`` namespace (V2-style, kept for back-compat)."""

    def InputData(self, **kwargs: Any) -> MockLayer:  # noqa: N802
        # accept old style kwargs (e.g. just `shape=(8,)`) → wrap as input_shape
        if "input_shape" not in kwargs and "shape" in kwargs:
            kwargs["input_shape"] = kwargs.pop("shape")
        input_shape = kwargs.pop("input_shape", (1, 1, 1))
        input_bits = kwargs.pop("input_bits", 4)
        name = kwargs.pop("name", "")
        # tolerate extra unknown kwargs (old mock was anything-goes)
        return InputData(input_shape=_coerce_shape_3d(input_shape),
                         input_bits=input_bits, name=name)

    def FullyConnected(self, **kwargs: Any) -> MockLayer:  # noqa: N802
        units = kwargs.pop("units", 1)
        return FullyConnected(
            units=units,
            name=kwargs.pop("name", ""),
            weights_bits=kwargs.pop("weights_bits", 1),
            activation=kwargs.pop("activation", True),
            act_bits=kwargs.pop("act_bits", 1),
        )

    def Conv2D(self, **kwargs: Any) -> MockLayer:  # noqa: N802
        """V2-style name → V1 ``Convolutional`` (alias, AKD1000 actually uses V1)."""
        kernel_size = kwargs.pop("kernel_size", 3)
        if isinstance(kernel_size, (tuple, list)):
            kernel_size = kernel_size[0]
        filters = kwargs.pop("filters", 1)
        return Convolutional(
            kernel_size=kernel_size, filters=filters,
            name=kwargs.pop("name", ""),
            padding=kwargs.pop("padding", Padding.Same),
            kernel_stride=kwargs.pop("kernel_stride", (1, 1)),
            weights_bits=kwargs.pop("weights_bits", 1),
            act_bits=kwargs.pop("act_bits", 1),
        )

    def Convolutional(self, **kwargs: Any) -> MockLayer:  # noqa: N802
        return self.Conv2D(**kwargs)


def _coerce_shape_3d(s: Any) -> tuple[int, int, int]:
    """Tolerate (n,) → (n, 1, 1) etc. so old tests keep working."""
    t = tuple(s) if hasattr(s, "__iter__") else (int(s),)
    if len(t) == 1:
        return (int(t[0]), 1, 1)
    if len(t) == 2:
        return (int(t[0]), int(t[1]), 1)
    return (int(t[0]), int(t[1]), int(t[2]))


# --------------------------------------------------------------------------- #
# AkidaUnsupervised — edge-learning optimizer
# --------------------------------------------------------------------------- #
@dataclass
class MockAkidaUnsupervised:
    """Mirror ``akida.AkidaUnsupervised`` for edge learning on AKD1000.

    Matches real signature: ``AkidaUnsupervised(num_weights, num_classes=1,
    initial_plasticity=1.0, learning_competition=0.0, min_plasticity=0.1,
    plasticity_decay=0.25)``.
    """
    num_weights: int
    num_classes: int = 1
    initial_plasticity: float = 1.0
    learning_competition: float = 0.0
    min_plasticity: float = 0.1
    plasticity_decay: float = 0.25

    def __post_init__(self) -> None:
        if self.num_weights <= 0:
            raise ValueError("num_weights must be > 0")
        for f, v in (
            ("initial_plasticity", self.initial_plasticity),
            ("min_plasticity", self.min_plasticity),
            ("plasticity_decay", self.plasticity_decay),
        ):
            if not (0.0 <= v <= 1.0):
                raise ValueError(f"{f} must be in [0,1]; got {v}")
        if not (0.0 <= self.learning_competition <= 0.5):
            raise ValueError("learning_competition must be in [0, 0.5]")


# Allow positional + keyword (mirror real SDK)
def AkidaUnsupervised(*args: Any, **kwargs: Any) -> MockAkidaUnsupervised:  # noqa: N802
    return MockAkidaUnsupervised(*args, **kwargs)


# --------------------------------------------------------------------------- #
# Device hierarchy — Device / HwDevice / SocDriver / PowerMeter / NP
# --------------------------------------------------------------------------- #
@dataclass
class MockPowerEvent:
    """Mirror ``akida.PowerEvent`` — fields inferred (see brainchip_reference)."""
    inference_index: int = 0
    power_mw: float = 5.0          # sub-mW typical; mock returns 5 mW per event
    duration_us: float = 1000.0    # 1 ms per inference on mock
    energy_uj: float = 5.0         # power_mw × duration_us / 1000


class MockPowerMeter:
    """Mirror ``akida.PowerMeter``."""
    def __init__(self) -> None:
        self.events: list[MockPowerEvent] = []
        self.total_energy: float = 0.0  # Joules

    def _record(self) -> None:
        ev = MockPowerEvent(inference_index=len(self.events))
        self.events.append(ev)
        self.total_energy += ev.energy_uj * 1e-6


@dataclass
class MockNpInfo:
    """Mirror ``akida.NP.Info`` — one entry per NPU."""
    ident: int
    type: str = "akida_v1"
    sram_size: int = 409 * 1024   # 8 MB / 20 NPUs ≈ 409 KB per NP
    used: int = 0


class MockMesh:
    """Mirror ``akida.NP.Mesh`` for AKD1000 — 20 NPU mesh."""
    def __init__(self, n_nps: int = 20) -> None:
        self.nps: list[MockNpInfo] = [MockNpInfo(ident=i) for i in range(n_nps)]


class MockSocDriver:
    """Mirror ``akida.SocDriver``."""
    def __init__(self) -> None:
        self.power_measurement_enabled: bool = False
        self.clock_mode: ClockMode = ClockMode.Economy


class MockHwDevice:
    """Mirror ``akida.HwDevice`` — what ``akida.devices()`` returns."""
    def __init__(self, version: HwVersion = HwVersion.NSoC_v1,
                 desc: str = "AKD1000_MOCK (anima Pack pre-arrival)") -> None:
        self.version: HwVersion = version
        self.desc: str = desc
        self.mesh: MockMesh = MockMesh(n_nps=20)
        self.soc: MockSocDriver = MockSocDriver()
        self.power_meter: MockPowerMeter = MockPowerMeter()
        self.ip_version: str = "v1.0.mock"

    @property
    def name(self) -> str:
        """Backwards-compat — old mock exposed `.name`."""
        return self.desc

    def program(self, model: "MockModel") -> bool:  # noqa: ARG002
        """Deprecated alias — use ``model.map(device)`` instead. Returns True."""
        return True


def _AKD1000() -> MockHwDevice:  # noqa: N802 — mirror SDK
    """Mirror ``akida.AKD1000()`` — virtual device for offline mapping."""
    return MockHwDevice(version=HwVersion.NSoC_v1, desc="AKD1000_VIRTUAL")


# --------------------------------------------------------------------------- #
# Model — the central class
# --------------------------------------------------------------------------- #
class MockModel:
    """Mirror ``akida.Model`` — supports add / compile / forward / fit / map.

    Construction:
        Model()                          → empty
        Model(filename="foo.fbz")        → load from disk (pickle for mock)
        Model(layers=[...])              → from list
    """

    def __init__(self, filename: Optional[str] = None,
                 layers: Optional[list[MockLayer]] = None) -> None:
        self.layers: list[MockLayer] = []
        self._weights: dict[str, np.ndarray] = {}  # per-layer Hebbian weights
        self._optimizer: Optional[MockAkidaUnsupervised] = None
        self._device: Optional[MockHwDevice] = None
        self._n_classes: int = 0   # increments via add_classes()
        self._inference_count: int = 0

        if filename is not None:
            self._load(filename)
        elif layers is not None:
            for layer in layers:
                self.add(layer)

    # ---- layer assembly -------------------------------------------------- #
    def add(self, layer: MockLayer, inbound_layers: Optional[list] = None) -> None:  # noqa: ARG002
        self.layers.append(layer)

    def pop_layer(self) -> Optional[MockLayer]:
        return self.layers.pop() if self.layers else None

    def get_layer(self, name_or_index: Any) -> Optional[MockLayer]:
        if isinstance(name_or_index, int):
            return self.layers[name_or_index] if 0 <= name_or_index < len(self.layers) else None
        for layer in self.layers:
            if layer.name == name_or_index:
                return layer
        return None

    # ---- introspection --------------------------------------------------- #
    @property
    def input_shape(self) -> tuple:
        if not self.layers:
            return (1, 1, 1)
        first = self.layers[0]
        if first.layer_type == LayerType.InputData:
            return tuple(first.params.get("input_shape", (1, 1, 1)))
        return tuple(first.params.get("input_shape", (1, 1, 1)))

    @property
    def output_shape(self) -> tuple:
        if not self.layers:
            return (1, 1, 1)
        last = self.layers[-1]
        if last.layer_type == LayerType.FullyConnected:
            return (1, 1, last.params.get("units", 1))
        return self.input_shape

    @property
    def layer_count(self) -> int:
        return len(self.layers)

    @property
    def device(self) -> Optional[MockHwDevice]:
        return self._device

    @property
    def macs(self) -> int:
        """Multiply-accumulate count (mock approximation)."""
        total = 0
        for layer in self.layers:
            if layer.layer_type == LayerType.FullyConnected:
                u = layer.params.get("units", 1)
                in_size = int(np.prod(self.input_shape))
                total += in_size * u
        return total

    @property
    def statistics(self) -> dict:
        return {
            "inference_count": self._inference_count,
            "backend": "akida_mock",
            "device_bound": self._device is not None,
            "n_classes": self._n_classes,
        }

    @property
    def sequences(self) -> list:
        """HW sequences after map() — mock: one sequence per device-bound model."""
        return [{"program": b"\x00" * 64, "components": []}] if self._device else []

    def summary(self) -> str:
        lines = ["Model summary (mock)"]
        for i, layer in enumerate(self.layers):
            lines.append(f"  [{i}] {layer.layer_type.value:<24s} name={layer.name!r}")
        lines.append(f"  device: {self._device.desc if self._device else 'unmapped'}")
        lines.append(f"  optimizer: {type(self._optimizer).__name__ if self._optimizer else 'none'}")
        s = "\n".join(lines)
        print(s)
        return s

    # ---- inference ------------------------------------------------------- #
    def forward(self, inputs: np.ndarray, batch_size: int = 0) -> np.ndarray:  # noqa: ARG002
        """Deterministic mock inference — LCG seeded from input bytes.

        Real ``akida.Model.forward(uint8 nparray)`` returns integer potentials.
        Mock returns ``np.int32`` of the same trailing shape (output_shape).
        """
        arr = np.asarray(inputs)
        try:
            raw = arr.tobytes()
        except (AttributeError, TypeError):
            raw = str(arr).encode("utf-8")
        seed = abs(hash(raw)) & 0xFFFFFFFF
        rng = np.random.RandomState(seed)

        # output shape: (batch, *output_shape)
        batch = arr.shape[0] if arr.ndim > 0 else 1
        out_shape = (batch,) + tuple(self.output_shape)
        out = (rng.random(out_shape) * 16).astype(np.int32)  # 4-bit potential ladder

        self._inference_count += 1
        if self._device is not None and self._device.soc.power_measurement_enabled:
            self._device.power_meter._record()
        return out

    def predict(self, inputs: np.ndarray, batch_size: int = 0) -> np.ndarray:
        """Float32 replica of forward() (mirrors real Akida ``.predict()``)."""
        return self.forward(inputs, batch_size=batch_size).astype(np.float32)

    # ---- on-chip learning ------------------------------------------------ #
    def compile(self, optimizer: MockAkidaUnsupervised) -> None:
        """Bind edge-learning optimizer (required before .fit())."""
        if not isinstance(optimizer, MockAkidaUnsupervised):
            raise TypeError(
                "compile() requires AkidaUnsupervised optimizer instance; "
                f"got {type(optimizer).__name__}"
            )
        self._optimizer = optimizer

    def fit(self, inputs: np.ndarray,
            input_labels: Any = None,
            batch_size: int = 0) -> None:  # noqa: ARG002
        """Mock AkidaUnsupervised update (Hebbian sw approximation).

        Real signature: ``model.fit(uint8 inputs, int32 input_labels, batch_size=0)``.
        Tolerates old signature ``model.fit(input_data, target_array)`` for
        backwards-compat: if input_labels is an ndarray of float (not int32),
        treats it as the legacy Hebbian target.
        """
        if self._optimizer is None and not _is_legacy_target(input_labels):
            raise RuntimeError(
                "fit() requires prior compile(AkidaUnsupervised(...)) — "
                "edge learning only works after the optimizer is bound."
            )

        in_arr = np.asarray(inputs)
        in_vec = in_arr.reshape(-1).astype(np.float64)

        if _is_legacy_target(input_labels):
            # Old-style: (input, target) Hebbian outer-product
            tgt_vec = np.asarray(input_labels).reshape(-1).astype(np.float64)
            lr = 0.01
        else:
            # New-style: int32 labels → one-hot internally
            labels = np.asarray(input_labels).reshape(-1).astype(np.int32)
            n_classes = max(int(labels.max()) + 1, self._n_classes, 1)
            tgt_vec = np.zeros(n_classes, dtype=np.float64)
            for lab in labels:
                if 0 <= lab < n_classes:
                    tgt_vec[lab] += 1.0
            lr = (self._optimizer.initial_plasticity if self._optimizer else 1.0) * 0.01

        key = "W"
        if key not in self._weights:
            self._weights[key] = np.zeros((in_vec.shape[0], tgt_vec.shape[0]), dtype=np.float64)
        # resize if labels grew (add_classes())
        if self._weights[key].shape[1] < tgt_vec.shape[0]:
            old = self._weights[key]
            new = np.zeros((in_vec.shape[0], tgt_vec.shape[0]), dtype=np.float64)
            new[:, : old.shape[1]] = old
            self._weights[key] = new
        # Hebbian outer-product
        self._weights[key] += lr * np.outer(in_vec, tgt_vec)

    def add_classes(self, n: int) -> None:
        """Mirror ``model.add_classes(n)`` — incremental class expansion."""
        if n < 0:
            raise ValueError("add_classes requires n >= 0")
        self._n_classes += int(n)

    # ---- HW deployment --------------------------------------------------- #
    def map(self, device: MockHwDevice,
            hw_only: bool = False,           # noqa: ARG002
            mode: MapMode = MapMode.AllNps,  # noqa: ARG002
            constraints: Any = None) -> None:  # noqa: ARG002
        """Mirror ``model.map(device, hw_only=False, mode=MapMode.AllNps)``."""
        if not isinstance(device, MockHwDevice):
            raise TypeError(f"map() requires HwDevice (or virtual AKD1000()); got {type(device).__name__}")
        if device.version != HwVersion.NSoC_v1:
            raise ValueError(
                f"anima Pack targets AKD1000 (NSoC_v1); got {device.version.value} "
                f"— pack adapters require Akida 1.0 silicon for edge learning"
            )
        self._device = device

    # ---- persistence ----------------------------------------------------- #
    def save(self, model_file: str) -> None:
        with open(model_file, "wb") as f:
            pickle.dump({"layers": self.layers, "weights": self._weights,
                         "n_classes": self._n_classes}, f)

    def _load(self, filename: str) -> None:
        if not os.path.exists(filename):
            raise FileNotFoundError(filename)
        with open(filename, "rb") as f:
            d = pickle.load(f)
        self.layers = d["layers"]
        self._weights = d.get("weights", {})
        self._n_classes = d.get("n_classes", 0)

    def to_buffer(self) -> bytes:
        return pickle.dumps({"layers": self.layers, "weights": self._weights,
                             "n_classes": self._n_classes})


def _is_legacy_target(input_labels: Any) -> bool:
    """True if input_labels looks like the old Hebbian target array (float, not int32)."""
    if input_labels is None:
        return False
    if not hasattr(input_labels, "dtype"):
        return False
    return not np.issubdtype(input_labels.dtype, np.integer)


# --------------------------------------------------------------------------- #
# MetaTFMock — drop-in for ``akida`` top-level module
# --------------------------------------------------------------------------- #
class MetaTFMock:
    """Drop-in replacement for the ``akida`` top-level module on Mac."""

    def __init__(self) -> None:
        self.is_mock: bool = True
        self.version: str = "2.19.1-anima-mock"
        self.__version__: str = self.version  # mirror SDK attribute
        self._layers = MockLayers()
        self._devices = [MockHwDevice()]

        # enums (mirror akida.* enums at package level)
        self.HwVersion = HwVersion
        self.ClockMode = ClockMode
        self.MapMode = MapMode
        self.Padding = Padding
        self.PoolType = PoolType
        self.ActivationType = ActivationType
        self.LayerType = LayerType

    # ---- model factories ------------------------------------------------- #
    def Model(self, filename: Optional[str] = None,  # noqa: N802
              layers: Optional[list[MockLayer]] = None) -> MockModel:
        return MockModel(filename=filename, layers=layers)

    # ---- top-level layer factories (V1 style) ---------------------------- #
    InputData = staticmethod(InputData)
    InputConvolutional = staticmethod(InputConvolutional)
    Convolutional = staticmethod(Convolutional)
    SeparableConvolutional = staticmethod(SeparableConvolutional)
    FullyConnected = staticmethod(FullyConnected)

    # ---- optimizer ------------------------------------------------------- #
    AkidaUnsupervised = staticmethod(AkidaUnsupervised)

    # ---- device factories ------------------------------------------------ #
    def devices(self) -> list[MockHwDevice]:
        return list(self._devices)

    def AKD1000(self) -> MockHwDevice:  # noqa: N802
        return _AKD1000()

    # ---- V2-style namespace alias (back-compat) -------------------------- #
    @property
    def layers(self) -> MockLayers:
        return self._layers

    # ---- debug ----------------------------------------------------------- #
    def __repr__(self) -> str:  # pragma: no cover — trivial
        return f"<MetaTFMock version={self.version} devices={len(self._devices)}>"


# --------------------------------------------------------------------------- #
# CNN2SNN converter — host-side path (sparse_attention adapter uses this)
# --------------------------------------------------------------------------- #
class MockAkidaVersion(enum.Enum):
    """Mirror of ``cnn2snn.AkidaVersion``."""
    v1 = "v1"   # AKD1000 — pack target
    v2 = "v2"   # AKD2000 — out-of-scope


class MockCNN2SNN:
    """Mock CNN2SNN converter — accepts Keras-style dict, returns a MockModel.

    Mirrors the host-side flow described in ``doc/akd1000_quantization.md``:

        cnn2snn.set_akida_version(AkidaVersion.v1)
        akida_model = cnn2snn.convert(quantized_keras_model)
        akida_model.save("foo.fbz")

    Real CNN2SNN walks a Keras model, fuses quantize ops, and emits an
    `akida.Model` with V1 layers.  The mock skips actual conversion and just
    materialises an equivalent ``MockModel`` from a layer-config dict —
    enough for the sparse-attention adapter to assert "I went through the
    converter path" without needing the full Keras/TF stack on Mac.

    The accepted ``keras_model_dict`` shape:

        {
          "name": "...",
          "layers": [
            {"type": "InputData", "input_shape": (8, 1, 1), "input_bits": 1},
            {"type": "FullyConnected", "units": 8,
             "weights_bits": 1, "act_bits": 1, "name": "attn_head"},
            ...
          ]
        }

    Unknown layer types raise ``ValueError`` (no silent passthrough — the
    real converter is strict).
    """

    AkidaVersion = MockAkidaVersion
    _target_version: MockAkidaVersion = MockAkidaVersion.v1

    @staticmethod
    def set_akida_version(version: MockAkidaVersion) -> None:
        """Mirror ``cnn2snn.set_akida_version(v)``."""
        if not isinstance(version, MockAkidaVersion):
            raise TypeError(
                f"set_akida_version requires MockAkidaVersion enum; got {type(version).__name__}"
            )
        MockCNN2SNN._target_version = version

    @staticmethod
    def get_akida_version() -> MockAkidaVersion:
        return MockCNN2SNN._target_version

    @staticmethod
    def convert(keras_model_dict: dict,
                file_path: Optional[str] = None,
                input_scaling: Optional[tuple] = None) -> "MockModel":  # noqa: ARG004
        """Mock CNN2SNN converter — accepts Keras-style dict, returns ``MockModel``."""
        if not isinstance(keras_model_dict, dict):
            raise TypeError(
                f"convert() requires a dict (Keras-style model spec); got {type(keras_model_dict).__name__}"
            )
        if MockCNN2SNN._target_version != MockAkidaVersion.v1:
            raise ValueError(
                "anima Pack targets AKD1000 (NSoC_v1); "
                f"got target_version={MockCNN2SNN._target_version.value} "
                "— call cnn2snn.set_akida_version(AkidaVersion.v1) first"
            )

        m = MockModel()
        for layer_cfg in keras_model_dict.get("layers", []):
            ltype = layer_cfg.get("type")
            if ltype == "InputData":
                m.add(InputData(
                    input_shape=tuple(layer_cfg.get("input_shape", (1, 1, 1))),
                    input_bits=int(layer_cfg.get("input_bits", 4)),
                    name=layer_cfg.get("name", ""),
                ))
            elif ltype == "InputConvolutional":
                m.add(InputConvolutional(
                    input_shape=tuple(layer_cfg.get("input_shape", (8, 8, 1))),
                    kernel_size=int(layer_cfg.get("kernel_size", 3)),
                    filters=int(layer_cfg.get("filters", 8)),
                    name=layer_cfg.get("name", ""),
                    weights_bits=int(layer_cfg.get("weights_bits", 1)),
                    act_bits=int(layer_cfg.get("act_bits", 1)),
                ))
            elif ltype == "Convolutional":
                m.add(Convolutional(
                    kernel_size=int(layer_cfg.get("kernel_size", 3)),
                    filters=int(layer_cfg.get("filters", 8)),
                    name=layer_cfg.get("name", ""),
                    weights_bits=int(layer_cfg.get("weights_bits", 1)),
                    act_bits=int(layer_cfg.get("act_bits", 1)),
                ))
            elif ltype == "SeparableConvolutional":
                m.add(SeparableConvolutional(
                    kernel_size=int(layer_cfg.get("kernel_size", 3)),
                    filters=int(layer_cfg.get("filters", 8)),
                    name=layer_cfg.get("name", ""),
                    weights_bits=int(layer_cfg.get("weights_bits", 2)),
                    act_bits=int(layer_cfg.get("act_bits", 1)),
                ))
            elif ltype == "FullyConnected":
                m.add(FullyConnected(
                    units=int(layer_cfg.get("units", 1)),
                    name=layer_cfg.get("name", ""),
                    weights_bits=int(layer_cfg.get("weights_bits", 1)),
                    activation=bool(layer_cfg.get("activation", True)),
                    act_bits=int(layer_cfg.get("act_bits", 1)),
                ))
            else:
                raise ValueError(
                    f"MockCNN2SNN: unknown layer type {ltype!r}; "
                    f"V1 supports InputData / InputConvolutional / Convolutional / "
                    f"SeparableConvolutional / FullyConnected"
                )

        if file_path is not None:
            m.save(file_path)
        return m

    @staticmethod
    def check_model_compatibility(keras_model_dict: dict,
                                  device: Optional[MockHwDevice] = None,  # noqa: ARG004
                                  input_dtype: str = "uint8") -> None:
        """Mirror ``cnn2snn.check_model_compatibility`` — raises on first issue."""
        if input_dtype != "uint8":
            raise ValueError(
                f"AKD1000 InputConvolutional requires uint8 input; got {input_dtype}"
            )
        # If layers list has any V2-only types, fail loud
        v2_only = {"Conv2D", "InputConv2D", "DepthwiseConv2D", "Add", "Concatenate",
                   "Dense1D", "BufferTempConv", "Dequantizer"}
        for layer_cfg in keras_model_dict.get("layers", []):
            ltype = layer_cfg.get("type", "")
            if ltype in v2_only:
                raise ValueError(
                    f"layer type {ltype!r} is Akida 2.0 only — not compatible with AKD1000"
                )


# Module-level alias so ``MetaTFMock.cnn2snn`` resolves like a real package.
MetaTFMock.cnn2snn = MockCNN2SNN  # type: ignore[attr-defined]


# pre-instantiated singleton — `from pack.mocks.metatf_mock import metatf_mock`
metatf_mock = MetaTFMock()


# --------------------------------------------------------------------------- #
# tiny self-test (no pytest needed — `python -m pack.mocks.metatf_mock`)
# --------------------------------------------------------------------------- #
def _selftest() -> dict:
    """Minimal sanity selftest — used by INSTALL.sh fallback path."""
    mock = MetaTFMock()

    # 1. V1-style build (canonical for AKD1000)
    m1 = mock.Model()
    m1.add(mock.InputData(input_shape=(8, 1, 1), input_bits=1))
    m1.add(mock.FullyConnected(units=4, weights_bits=1, act_bits=1))
    x = np.ones((1, 8, 1, 1), dtype=np.uint8)
    y_a = m1.forward(x)
    y_b = m1.forward(x)
    deterministic = bool(np.array_equal(y_a, y_b))
    out_int32 = y_a.dtype == np.int32

    # 2. compile + fit (edge learning)
    m1.compile(mock.AkidaUnsupervised(num_weights=2, num_classes=4))
    labels = np.array([2], dtype=np.int32)
    m1.fit(x, labels)
    has_weights = "W" in m1._weights

    # 3. map to mock AKD1000
    devs = mock.devices()
    device_v1 = devs[0].version == mock.HwVersion.NSoC_v1
    m1.map(devs[0])
    device_bound = m1.device is devs[0]

    # 4. virtual AKD1000 + persistence
    virt = mock.AKD1000()
    m2 = mock.Model()
    m2.add(mock.InputData(input_shape=(4, 1, 1)))
    m2.add(mock.FullyConnected(units=2))
    m2.map(virt)

    # 5. layer validation (real signature)
    try:
        bad = mock.FullyConnected(units=0)  # should raise
        raises_bad_units = False
    except ValueError:
        raises_bad_units = True

    # 6. back-compat: V2-style namespace still works
    m3 = mock.Model()
    m3.add(mock.layers.InputData(shape=(8,)))
    m3.add(mock.layers.FullyConnected(units=4))
    backcompat_ok = len(m3.layers) == 2

    # 7. legacy (input, target) fit signature still works
    m4 = mock.Model()
    m4.add(mock.InputData(input_shape=(8, 1, 1)))
    m4.add(mock.FullyConnected(units=4))
    # without compile — legacy Hebbian path (float target)
    m4.fit(np.ones(8, dtype=np.float32), np.ones(4, dtype=np.float32))
    legacy_fit_ok = "W" in m4._weights

    return {
        "version": mock.version,
        "is_mock": mock.is_mock,
        "forward_deterministic": deterministic,
        "forward_returns_int32": out_int32,
        "fit_weights_ok": has_weights,
        "device_version_v1": device_v1,
        "device_bound": device_bound,
        "virtual_AKD1000_ok": m2.device is virt,
        "validates_bad_units": raises_bad_units,
        "v2_namespace_backcompat": backcompat_ok,
        "legacy_fit_backcompat": legacy_fit_ok,
    }


if __name__ == "__main__":  # pragma: no cover
    import json

    print(json.dumps(_selftest(), indent=2))
