"""MetaTF wrapper with mock fallback.

Two paths
---------
- **HW path**  : ``import akida`` (BrainChip MetaTF SDK installed via
  ``pip install akida`` on the Pi 5 host — aarch64 wheel auto-selected from
  PyPI; see ``doc/metatf_install_linux_arm.md``).
- **Mock path**: ``from pack.mocks.metatf_mock import MetaTFMock`` (Mac-local
  pre-arrival validation; rewritten 2026-05-21 to mirror real BrainChip API
  per cached reference docs).

Auto-detect at first :func:`get_runtime` call.  The choice is sticky for the
lifetime of the process — repeated calls return the same backend.  Use
:func:`reset_runtime` from tests when you need to swap backends mid-process.

The module deliberately tolerates **both** an importable ``akida`` SDK *and*
the absence of any mock — in that case :func:`init_runtime` raises a clear
``RuntimeError`` rather than silently substituting a no-op.

When HW backend is selected, :func:`assert_akd1000` validates that at least one
attached device reports ``HwVersion.NSoC_v1`` (the AKD1000 family). Pack
adapters require Akida 1.0 silicon for on-chip Hebbian / 1-shot learning
(Akida 2.0 dropped edge learning).
"""

from __future__ import annotations

import importlib
import importlib.util
import os
import sys
from typing import Any, Optional

_RUNTIME: Optional[Any] = None
_BACKEND: Optional[str] = None
_ERROR_LOG: list[str] = []


def _try_import_akida_hw() -> Optional[Any]:
    """Attempt to import the real BrainChip ``akida`` SDK."""
    try:
        spec = importlib.util.find_spec("akida")
    except (ImportError, ValueError):
        return None
    if spec is None:
        _ERROR_LOG.append("akida SDK not importable (find_spec → None)")
        return None
    try:
        return importlib.import_module("akida")
    except Exception as exc:  # noqa: BLE001  (defensive — any import failure)
        _ERROR_LOG.append(f"akida import raised: {exc!r}")
        return None


def _try_import_mock() -> Optional[Any]:
    """Attempt to import the Mac-local mock MetaTF runtime."""
    # First try the canonical package path.
    try:
        mod = importlib.import_module("pack.mocks.metatf_mock")
        return mod.MetaTFMock()
    except (ImportError, AttributeError) as exc:
        _ERROR_LOG.append(f"pack.mocks.metatf_mock import failed: {exc!r}")

    # Fallback: load by relative file path (handles editable installs
    # that haven't been pip-registered yet).
    here = os.path.dirname(os.path.abspath(__file__))
    mocks_dir = os.path.normpath(os.path.join(here, "..", "mocks"))
    if mocks_dir not in sys.path:
        sys.path.insert(0, mocks_dir)
    try:
        mod = importlib.import_module("metatf_mock")
        return mod.MetaTFMock()
    except (ImportError, AttributeError) as exc:
        _ERROR_LOG.append(f"metatf_mock direct import failed: {exc!r}")
        return None


def init_runtime(prefer: str = "auto") -> str:
    """Initialise the global MetaTF runtime.

    Parameters
    ----------
    prefer : {"auto", "hw", "mock"}
        ``"auto"`` (default) → HW first, mock fallback.
        ``"hw"``  → only HW; raise if absent.
        ``"mock"``→ only mock; raise if absent.

    Returns
    -------
    str
        The selected backend name (``"akida_hw"`` or ``"akida_mock"``).
    """
    global _RUNTIME, _BACKEND

    if prefer not in {"auto", "hw", "mock"}:
        raise ValueError(f"prefer must be auto|hw|mock, got {prefer!r}")

    rt: Optional[Any] = None
    backend: Optional[str] = None

    if prefer in {"auto", "hw"}:
        rt = _try_import_akida_hw()
        if rt is not None:
            backend = "akida_hw"

    if rt is None and prefer in {"auto", "mock"}:
        rt = _try_import_mock()
        if rt is not None:
            backend = "akida_mock"

    if rt is None:
        msg = (
            "Neither akida HW nor mocks/metatf_mock available. "
            f"errors={_ERROR_LOG!r}"
        )
        raise RuntimeError(msg)

    _RUNTIME = rt
    _BACKEND = backend
    return backend  # type: ignore[return-value]


def get_runtime() -> Any:
    """Return the live runtime, lazy-initialising on first call."""
    if _RUNTIME is None:
        init_runtime()
    return _RUNTIME


def get_runtime_info() -> dict:
    """Return ``{"backend", "runtime_class", "error_log"}`` snapshot."""
    if _RUNTIME is None:
        try:
            init_runtime()
        except RuntimeError:
            # In info mode we never raise — surface the failure for record.
            return {
                "backend": "unavailable",
                "runtime_class": "None",
                "error_log": list(_ERROR_LOG),
            }
    return {
        "backend": _BACKEND,
        "runtime_class": _RUNTIME.__class__.__name__,
        "error_log": list(_ERROR_LOG),
    }


def reset_runtime() -> None:
    """Reset the cached runtime (test-only helper)."""
    global _RUNTIME, _BACKEND
    _RUNTIME = None
    _BACKEND = None
    _ERROR_LOG.clear()


def assert_akd1000() -> dict:
    """Verify the bound runtime exposes at least one AKD1000 (NSoC_v1) device.

    Works for both backends:
    - HW backend: checks ``akida.devices()[0].version == akida.HwVersion.NSoC_v1``
    - Mock backend: checks ``MockHwDevice.version == HwVersion.NSoC_v1`` (mock enum)

    Returns
    -------
    dict
        ``{"backend": str, "device_count": int, "device_versions": list[str],
           "akd1000_present": bool, "first_device_desc": str}``

    Raises
    ------
    RuntimeError
        If no AKD1000 (NSoC_v1) device present in either backend.
    """
    rt = get_runtime()
    try:
        devs = rt.devices()
    except Exception as exc:  # noqa: BLE001
        raise RuntimeError(f"runtime devices() failed: {exc!r}") from exc

    versions: list[str] = []
    akd1000_present = False
    first_desc = ""
    for i, dev in enumerate(devs):
        # both real + mock expose `.version` (HwVersion enum or HwVersion-like)
        v = getattr(dev, "version", None)
        v_str = getattr(v, "name", None) or getattr(v, "value", None) or str(v)
        versions.append(v_str)
        if v_str == "NSoC_v1":
            akd1000_present = True
        if i == 0:
            first_desc = getattr(dev, "desc", "") or getattr(dev, "name", "") or repr(dev)

    if not akd1000_present:
        raise RuntimeError(
            "No AKD1000 (NSoC_v1) device detected. Pack adapters require "
            "Akida 1.0 silicon for edge learning. "
            f"backend={_BACKEND} devices={versions}"
        )

    return {
        "backend": _BACKEND or "unknown",
        "device_count": len(devs),
        "device_versions": versions,
        "akd1000_present": akd1000_present,
        "first_device_desc": first_desc,
    }


__all__ = [
    "init_runtime",
    "get_runtime",
    "get_runtime_info",
    "reset_runtime",
    "assert_akd1000",
]
