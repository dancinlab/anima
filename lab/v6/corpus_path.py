"""Portable resolution of the natural research corpus used by the v6 ladders.

The CI gate `no-foreign-path` rejects an author-machine path baked into source, and it is
right to: a hardcoded home directory makes every script here unrunnable by anyone else and
silently unrunnable on a pod. Resolution order is env var, then the conventional weights
directory under $HOME, then fail fast with the path it looked for -- never a silent fallback
to some other file, which would make a measurement quietly answer about the wrong corpus.
"""
import os
import pathlib

REL = "anima-weights/study303_long_transcript/cpt_mix.txt"


def natural_corpus() -> str:
    """Absolute path to the natural (ON-STANDARD, p9) research corpus."""
    env = os.environ.get("ANIMA_NATURAL_CORPUS")
    if env:
        if not pathlib.Path(env).is_file():
            raise SystemExit(f"ANIMA_NATURAL_CORPUS is set but not a file: {env}")
        return env
    p = pathlib.Path.home() / REL
    if p.is_file():
        return str(p)
    raise SystemExit(
        f"natural corpus not found at {p}\n"
        f"set ANIMA_NATURAL_CORPUS=<path to cpt_mix.txt> (or an equivalent natural corpus)"
    )
