"""pytest — mock-run every adapter in pack.adapters, expect F-AKIDA 5/5 each.

Designed to be resilient against the adapter-pack agent's churn:
- Discovers adapter modules by walking ``pack.adapters`` (no hard-coded
  list of 10/11 names).
- Picks the first ``*Adapter`` class (excluding the abstract base) in each
  module.
- Tolerates both ``{"pass_count", "fail_count"}`` and ``{"passed", "failed"}``
  selftest result shapes.
"""

from __future__ import annotations

import importlib
import inspect
import pkgutil

import pytest


# --------------------------------------------------------------------------- #
# discovery (module-import-time)
# --------------------------------------------------------------------------- #
def _discover_adapter_modules() -> list:
    try:
        import pack.adapters as adapters_pkg
    except ImportError:
        return []  # adapter agent not landed yet — tests skip cleanly
    mods = []
    for mod_info in pkgutil.iter_modules(adapters_pkg.__path__):
        if mod_info.name.startswith("_") or mod_info.name == "base":
            continue
        try:
            mods.append(importlib.import_module(f"pack.adapters.{mod_info.name}"))
        except Exception as exc:  # noqa: BLE001
            pytest.skip(f"cannot import pack.adapters.{mod_info.name}: {exc}")
    return mods


ADAPTER_MODULES = _discover_adapter_modules()


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #
def _adapter_class(mod):
    """Return the first concrete ``*Adapter`` class in ``mod``."""
    base_cls = None
    try:
        from pack.adapters.base import AkidaAdapter as _Base
        base_cls = _Base
    except ImportError:
        pass

    for _, obj in inspect.getmembers(mod, inspect.isclass):
        if not obj.__name__.endswith("Adapter"):
            continue
        if obj.__name__ == "AkidaAdapter":
            continue
        if base_cls is not None and not issubclass(obj, base_cls):
            continue
        return obj
    return None


def _pass_fail_counts(res: dict) -> tuple[int, int]:
    if "pass_count" in res or "fail_count" in res:
        return int(res.get("pass_count", 0)), int(res.get("fail_count", 0))
    if "passed" in res or "failed" in res:
        passed = res.get("passed", [])
        failed = res.get("failed", [])
        p = len(passed) if hasattr(passed, "__len__") else int(passed)
        f = len(failed) if hasattr(failed, "__len__") else int(failed)
        return p, f
    return 0, 0


# --------------------------------------------------------------------------- #
# tests
# --------------------------------------------------------------------------- #
@pytest.mark.skipif(not ADAPTER_MODULES,
                    reason="pack.adapters not installed yet (adapter pack agent)")
@pytest.mark.parametrize("adapter_module", ADAPTER_MODULES,
                         ids=lambda m: m.__name__.rsplit(".", 1)[-1])
def test_adapter_mock_run(adapter_module):
    """Every adapter's ``selftest()`` should yield F-AKIDA-* 5/5 PASS on mock."""
    cls = _adapter_class(adapter_module)
    assert cls is not None, (
        f"no concrete *Adapter class in {adapter_module.__name__}")

    adapter = cls()
    assert hasattr(adapter, "selftest"), f"{cls.__name__} missing selftest()"
    assert hasattr(adapter, "name"), f"{cls.__name__} missing name"

    res = adapter.selftest()
    assert isinstance(res, dict), f"{cls.__name__}.selftest() must return dict"

    passed, failed = _pass_fail_counts(res)
    assert passed == 5, (
        f"{cls.__name__} F-AKIDA-* 5/5 expected, got pass={passed} fail={failed} "
        f"raw={res}")
    assert failed == 0, (
        f"{cls.__name__} expected 0 failures, got {failed} "
        f"raw={res}")


def test_mock_runtime_self_consistency():
    """Sanity-check the metatf mock itself — independent of adapter pack."""
    from pack.mocks.metatf_mock import _selftest
    res = _selftest()
    assert res["forward_deterministic"], "MetaTFMock.forward must be deterministic"
    assert res["fit_weights_ok"], "MetaTFMock.fit must populate weights"
    assert res["device_program_ok"], "MockDevice.program must succeed"
    assert res["is_mock"], "MetaTFMock.is_mock flag must be True"


def test_falsifier_aggregate_smoke():
    """The aggregate runner must be importable and return a dict."""
    from pack.falsifiers.run_all import run_all_adapters
    agg = run_all_adapters(verbose=False)
    assert isinstance(agg, dict)
    assert "pass_total" in agg
    assert "fail_total" in agg
    assert "adapters_discovered" in agg
    assert "per_adapter" in agg
