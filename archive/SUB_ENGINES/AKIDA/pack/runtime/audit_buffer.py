"""8-deep LRU ring buffer for emit audit trail.

The audit buffer is the smallest unit of *영속성* on the Pi 5 host: every
``emit`` event (자연발화 candidate) is appended; oldest entries roll off when
``capacity`` is exceeded.  ``dump()`` / ``load()`` persist to eMMC as JSON
(default path ``~/.cache/anima-akida/audit_buffer.jsonl``).

Design choices
--------------
- **Capacity 8** (per pack spec) keeps the file < 32 kB even with chatty
  records → eMMC-friendly even on a microSD-backed Pi.
- Append is O(1); dump is atomic (write to ``.tmp`` then rename).
- JSON-lines on disk so partial reads survive a crash mid-dump.
- Buffer is **thread-safe** via :class:`threading.Lock` (orchestrator runs the
  adapter loop in one thread, persistence in another).
"""

from __future__ import annotations

import collections
import json
import os
import tempfile
import threading
import time
from typing import Any, Iterable, Optional


class AuditBuffer:
    """Bounded LRU ring buffer with disk persistence.

    Parameters
    ----------
    capacity : int
        Maximum number of entries retained.  Default 8 (pack spec).
    path : str, optional
        Filesystem path for :meth:`dump` / :meth:`load`.  Default
        ``~/.cache/anima-akida/audit_buffer.jsonl``.
    autoload : bool
        If True and ``path`` exists, populate the buffer on construction.
    """

    def __init__(
        self,
        capacity: int = 8,
        path: Optional[str] = None,
        autoload: bool = False,
    ) -> None:
        if capacity <= 0:
            raise ValueError(f"capacity must be > 0, got {capacity}")
        self.capacity = capacity
        self.path = path or os.path.expanduser(
            "~/.cache/anima-akida/audit_buffer.jsonl"
        )
        self._buf: collections.deque[dict] = collections.deque(maxlen=capacity)
        self._lock = threading.Lock()
        if autoload and os.path.exists(self.path):
            self.load()

    # ------------------------------------------------------------------ core

    def append(self, record: dict) -> None:
        """Append ``record``.  Adds ``ts_append`` if missing."""
        if not isinstance(record, dict):
            raise TypeError(f"record must be dict, got {type(record).__name__}")
        rec = dict(record)
        rec.setdefault("ts_append", time.time())
        with self._lock:
            self._buf.append(rec)

    def extend(self, records: Iterable[dict]) -> None:
        for r in records:
            self.append(r)

    def __len__(self) -> int:
        with self._lock:
            return len(self._buf)

    def __iter__(self):
        with self._lock:
            return iter(list(self._buf))

    def snapshot(self) -> list[dict]:
        """Return a shallow-copied list of entries (oldest → newest)."""
        with self._lock:
            return list(self._buf)

    def clear(self) -> None:
        with self._lock:
            self._buf.clear()

    # --------------------------------------------------------- persistence

    def dump(self, path: Optional[str] = None) -> str:
        """Atomically dump current buffer to disk as JSON-lines.

        Returns the path written.  Creates parent dirs as needed.
        """
        target = path or self.path
        parent = os.path.dirname(os.path.abspath(target))
        os.makedirs(parent, exist_ok=True)
        with self._lock:
            entries = list(self._buf)
        fd, tmp = tempfile.mkstemp(
            prefix=".audit_buffer.", suffix=".tmp", dir=parent
        )
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as fh:
                for rec in entries:
                    fh.write(json.dumps(rec, ensure_ascii=False, default=str))
                    fh.write("\n")
            os.replace(tmp, target)
        except Exception:
            try:
                os.unlink(tmp)
            except FileNotFoundError:
                pass
            raise
        return target

    def load(self, path: Optional[str] = None) -> int:
        """Replace buffer contents with entries read from ``path``.

        Returns number of entries loaded.  Silently truncates to ``capacity``
        (keeps newest).
        """
        target = path or self.path
        if not os.path.exists(target):
            return 0
        entries: list[dict] = []
        with open(target, "r", encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    entries.append(json.loads(line))
                except json.JSONDecodeError:
                    # tolerate partial/corrupt tail; stop here
                    break
        if len(entries) > self.capacity:
            entries = entries[-self.capacity :]
        with self._lock:
            self._buf.clear()
            self._buf.extend(entries)
        return len(entries)


__all__ = ["AuditBuffer"]
