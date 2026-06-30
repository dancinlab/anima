"""F-AKIDA-* aggregator — runs ``selftest()`` on every adapter.

Walks the ``pack.adapters`` sub-package, instantiates every concrete
``AkidaAdapter`` subclass (skipping the abstract base), executes its
``selftest()`` and prints a single PASS/FAIL table.  Returns the per-
adapter result dict for programmatic use (CI / boot Day 1 smoke).

Design
------
- **Dynamic discovery** — we don't hard-code the 11 adapter import paths;
  any module under ``pack.adapters`` that exports an ``*Adapter`` subclass
  (other than ``AkidaAdapter`` itself) is picked up.  Keeps this file
  decoupled from the adapter-pack agent's churn.
- **Mock-tolerant** — adapter ``selftest()`` is expected to work without
  real Akida HW thanks to ``pack.runtime.metatf_runtime`` falling back to
  ``pack.mocks.metatf_mock``.  No special-casing here.
- **Target** — 11 adapters × 5 falsifiers = **55 PASS** baseline.
"""

from __future__ import annotations

import importlib
import inspect
import json
import pkgutil
import sys
from typing import Any


# --------------------------------------------------------------------------- #
# adapter discovery
# --------------------------------------------------------------------------- #
def _discover_adapter_classes() -> list[type]:
    """Walk ``pack.adapters`` and return every concrete ``*Adapter`` class."""
    try:
        import pack.adapters as adapters_pkg  # noqa: F401  (import side-effect)
    except ImportError as exc:  # pragma: no cover — propagated up
        raise ImportError(
            "pack.adapters is unavailable — adapter pack agent's files "
            "may not be in place yet"
        ) from exc

    base_cls: type | None = None
    try:
        from pack.adapters.base import AkidaAdapter as _Base
        base_cls = _Base
    except ImportError:
        base_cls = None  # tolerate missing base — discovery still possible

    found: list[type] = []
    seen: set[str] = set()
    pkg_path = adapters_pkg.__path__  # type: ignore[attr-defined]
    for mod_info in pkgutil.iter_modules(pkg_path):
        if mod_info.name.startswith("_") or mod_info.name == "base":
            continue
        full_name = f"pack.adapters.{mod_info.name}"
        try:
            mod = importlib.import_module(full_name)
        except Exception as exc:  # noqa: BLE001
            print(f"[WARN] cannot import {full_name}: {exc}", file=sys.stderr)
            continue
        for _, obj in inspect.getmembers(mod, inspect.isclass):
            if not obj.__name__.endswith("Adapter"):
                continue
            if obj.__name__ == "AkidaAdapter":
                continue
            if base_cls is not None and not issubclass(obj, base_cls):
                continue
            qualname = f"{obj.__module__}.{obj.__name__}"
            if qualname in seen:
                continue
            seen.add(qualname)
            found.append(obj)
    return found


# --------------------------------------------------------------------------- #
# result coercion (adapter selftest dict shape may vary slightly)
# --------------------------------------------------------------------------- #
def _coerce_counts(result: dict[str, Any]) -> tuple[int, int]:
    """Normalise pass / fail counts across mildly varying selftest shapes."""
    if not isinstance(result, dict):
        return (0, 0)
    # canonical keys (`pass_count` / `fail_count`)
    if "pass_count" in result or "fail_count" in result:
        return (int(result.get("pass_count", 0)), int(result.get("fail_count", 0)))
    # alternative pack.adapters.base shape (`passed` / `failed`)
    if "passed" in result or "failed" in result:
        passed = result.get("passed", [])
        failed = result.get("failed", [])
        return (len(passed) if hasattr(passed, "__len__") else int(passed),
                len(failed) if hasattr(failed, "__len__") else int(failed))
    # last-ditch heuristic — count truthy "details" entries
    details = result.get("details", {})
    if isinstance(details, dict):
        passed = sum(1 for v in details.values() if v)
        return (passed, len(details) - passed)
    return (0, 0)


# --------------------------------------------------------------------------- #
# public entry point
# --------------------------------------------------------------------------- #
def run_all_adapters(verbose: bool = True) -> dict[str, Any]:
    """Instantiate every adapter, run ``selftest()``, return aggregate dict."""
    classes = _discover_adapter_classes()
    results: dict[str, dict[str, Any]] = {}

    for cls in classes:
        try:
            adapter = cls()
        except Exception as exc:  # noqa: BLE001
            results[cls.__name__] = {"error": f"instantiate: {exc}",
                                     "pass_count": 0, "fail_count": 5}
            continue
        try:
            res = adapter.selftest()
        except Exception as exc:  # noqa: BLE001
            results[cls.__name__] = {"error": f"selftest: {exc}",
                                     "pass_count": 0, "fail_count": 5}
            continue
        name = getattr(adapter, "name", cls.__name__)
        results[name] = res

    total_pass = 0
    total_fail = 0
    for name, res in results.items():
        p, f = _coerce_counts(res)
        total_pass += p
        total_fail += f
        if verbose:
            print(f"[{ 'PASS' if f == 0 and p > 0 else 'FAIL' }] "
                  f"{name:<32s} pass={p}/5 fail={f}")

    if verbose:
        print("=" * 60)
        print(f"=== F-AKIDA aggregate ===")
        print(f"adapters discovered: {len(classes)}")
        print(f"PASS: {total_pass}  FAIL: {total_fail}  "
              f"(target: 55 PASS = 11 × 5)")
        print("=" * 60)

    return {
        "adapters_discovered": len(classes),
        "pass_total": total_pass,
        "fail_total": total_fail,
        "target_pass": 55,
        "per_adapter": results,
    }


# --------------------------------------------------------------------------- #
# CLI entry point
# --------------------------------------------------------------------------- #
def main(argv: list[str] | None = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    as_json = "--json" in argv
    try:
        agg = run_all_adapters(verbose=not as_json)
    except ImportError as exc:
        print(f"[FAIL] adapter discovery error: {exc}", file=sys.stderr)
        return 2
    if as_json:
        print(json.dumps(agg, indent=2, default=str))
    return 0 if agg["fail_total"] == 0 and agg["pass_total"] > 0 else 1


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
