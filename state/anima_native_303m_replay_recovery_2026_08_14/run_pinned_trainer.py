#!/usr/bin/env python3
"""Launch pinned native trainer with bounded corpus preprocessing workers."""

from __future__ import annotations

import argparse
from pathlib import Path
import runpy
import sys


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workers", type=int, required=True)
    parser.add_argument("trainer", type=Path)
    parser.add_argument("trainer_args", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    if args.workers <= 0:
        parser.error("workers must be positive")
    if not args.trainer.is_file():
        parser.error("pinned trainer does not exist")

    sys.path.insert(0, str(args.trainer.resolve().parent))
    from measurement.native_dialogue_registry import NATIVE_DIALOGUE_SPEC

    NATIVE_DIALOGUE_SPEC["native_dialogue5"]["preprocessing_workers"] = args.workers
    sys.argv = [str(args.trainer), *args.trainer_args]
    runpy.run_path(str(args.trainer), run_name="__main__")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
