"""Probe: does BC.00.000.002 (NSoC_v2 / AKD1000) support on-chip edge learning?

On-chip Akida unsupervised learning requires the trainable layer to receive
BINARY inputs. We feed a 1-bit InputData so the FullyConnected gets binary
spikes, then compile AkidaUnsupervised + fit() ON CHIP.
"""
import hashlib
import json
import os
import sys

import numpy as np
import akida

# ── learning-input entropy source (H_923 M7 → H_924 M5 qentropy SSOT migration) ──
# The few-shot on-chip AkidaUnsupervised input is host-side. H_924 M5 migrates this
# draw onto the unified qentropy SSOT while staying FULLY BACKWARD-COMPATIBLE.
# Precedence for the binary learning input (first match wins):
#
#   1. LEGACY env  ANIMA_QRNG_LEARN_BIN=<path>  (explicit) — if set, unpack that ANU
#      buffer's bits directly, byte-for-byte as before. Preserves existing pi5
#      dispatch / CI pinning a specific buffer; the legacy path is untouched.
#   2. qentropy SSOT — if the legacy env is UNSET and the SSOT is importable, draw
#      via qentropy.qentropy_bits(n, "akida_learn_input").reshape(shape). The active
#      policy is ANIMA_ENTROPY_MODE: quantum (DEFAULT — committed ANU buffer) or
#      deterministic (AUXILIARY — reproducible PRNG). Unified, A/B-benchmarkable.
#   3. numpy PRNG — if neither is available, fall back to a local seeded numpy
#      Generator so this device probe still runs standalone.
#
# Statistical quality is identical (chacha20==ANU, #123-A); the SSOT's value is
# provenance · auditability · one policy across every anima seed point. DECODER
# inference is untouched (deterministic, separate lane).
_QRNG_BIN = os.environ.get("ANIMA_QRNG_LEARN_BIN", "")
_qrng_sha = None

# qentropy SSOT imported ONLY as a soft dependency (try/except), consulted only when
# the legacy env above is UNSET. Insert mirror/qmirror/seed (three levels up from
# SUB_ENGINES/AKIDA/scripts) on sys.path; on ImportError fall through to numpy PRNG.
_qentropy = None
if not _QRNG_BIN:
    _HERE = os.path.dirname(os.path.abspath(__file__))
    _REPO = os.path.abspath(os.path.join(_HERE, os.pardir, os.pardir, os.pardir))
    _QENTROPY_DIR = os.path.join(_REPO, "mirror", "qmirror", "seed")
    if _QENTROPY_DIR not in sys.path:
        sys.path.insert(0, _QENTROPY_DIR)
    try:
        import qentropy as _qentropy  # type: ignore
    except Exception:  # noqa: BLE001  (SSOT absent -> fall through to numpy PRNG)
        _qentropy = None


def _learn_input(shape):
    """Binary {0,1} learning samples under the precedence legacy-env → qentropy → numpy."""
    global _qrng_sha
    n = int(np.prod(shape))
    # (1) legacy explicit buffer — unpack bits, identical to the pre-M5 path.
    if _QRNG_BIN and os.path.exists(_QRNG_BIN):
        raw = open(_QRNG_BIN, "rb").read()
        _qrng_sha = hashlib.sha256(raw).hexdigest()
        bits = np.unpackbits(np.frombuffer(raw, dtype=np.uint8))
        if bits.size < n:
            bits = np.resize(bits, n)          # cycle if buffer short
        return bits[:n].astype(np.uint8).reshape(shape)
    # (2) qentropy SSOT — binary bits under the active ANIMA_ENTROPY_MODE policy.
    if _qentropy is not None:
        return _qentropy.qentropy_bits(n, "akida_learn_input").astype(np.uint8).reshape(shape)
    # (3) numpy PRNG fallback.
    return np.random.default_rng(42).integers(0, 2, size=shape, dtype=np.uint8)


def _learn_input_source_and_provenance():
    """Resolve (source_label, provenance_dict) for the learn-input draw, mirroring the
    _learn_input precedence. Prefers qentropy.last_provenance() (mode·tier·sha256·
    request_id) on the SSOT path. Field NAMES are KEPT (learn_input_source /
    learn_input_provenance) so downstream JSON parsing is unbroken."""
    if _qrng_sha is not None:                         # (1) legacy env (set after a draw)
        return "anu_quantum", {"bin": _QRNG_BIN, "sha256": _qrng_sha,
                               "path": "legacy_env_ANIMA_QRNG_LEARN_BIN"}
    if _qentropy is not None:                          # (2) qentropy SSOT
        _m = _qentropy.mode()
        return ("anu_quantum" if _m == "quantum" else "numpy_prng_deterministic"), {
            "path": "qentropy_ssot", "entropy_mode": _m,
            "provenance": _qentropy.last_provenance()}
    return "numpy_prng", None                          # (3) numpy fallback


out = {}
dev = akida.devices()[0]
out["device_version"] = str(dev.version)
out["ip_version"] = str(dev.ip_version)

model = akida.Model()
# input_bits=1 => binary spikes feeding the trainable layer
model.add(akida.InputData(input_shape=(1, 1, 16), input_bits=1, name="in"))
model.add(akida.FullyConnected(units=10, name="fc", weights_bits=1,
                               activation=True))
model.map(dev)
out["mapped_backend"] = str(model.sequences[0].backend)

learn_ok = fit_ok = False
try:
    model.compile(optimizer=akida.AkidaUnsupervised(num_weights=2,
                                                    learning_competition=0.1))
    learn_ok = True
    out["compile_AkidaUnsupervised"] = "ok"
    out["device_learn_enabled_after_compile"] = bool(dev.learn_enabled)
except Exception as e:  # noqa: BLE001
    out["compile_err"] = repr(e)

if learn_ok:
    x = _learn_input((8, 1, 1, 16))  # legacy-env → qentropy SSOT → numpy PRNG
    # Resolve source + provenance AFTER the draw so the legacy sha256 / qentropy
    # last_provenance() reflect the bytes actually consumed. Field names are KEPT.
    out["learn_input_source"], out["learn_input_provenance"] = \
        _learn_input_source_and_provenance()
    try:
        model.fit(x)  # on-chip Hebbian learning
        fit_ok = True
        out["fit_on_chip"] = "ok"
        out["device_learn_enabled_after_fit"] = bool(dev.learn_enabled)
    except Exception as e:  # noqa: BLE001
        out["fit_err"] = repr(e)

out["edge_learning_supported"] = bool(learn_ok and fit_ok)
print(json.dumps(out, indent=2))
