#!/usr/bin/env python3
"""audit_logger.py — Python sidecar JSONL audit logger for Phase B bounded-run
(RESEARCH.md §24, 2026-05-18 first user-gated bounded-run cycle).

Resolves the 6/6 audit-log STUB from §24 design (HEXAD/CHAT/thinker_talker_lib.hexa
audit_entry_accepted returns canonical string only; JSONL serialize was deferred
to hexa-lang fs RFC). Python sidecar = honest carve-out: hexa-native impl is later
RFC, but the Phase B *measurement* protocol's 6th safety control (persistent
audit log) becomes empirically enforceable NOW.

Append-only JSONL contract (B-PHASE-B-RUN-1 closed):
  - file opened in mode='a' (POSIX O_APPEND atomic-per-write)
  - line-buffered (`buffering=1`) — each `write()` flushes
  - one JSON object per line, '\n' terminated
  - no truncate path, no seek backwards
  - byte-count strictly non-decreasing across writes (verified post-run)

Per-step record schema (B-PHASE-B-RUN-2 / -3 / -4 closed predicates feed off this):
  {
    "timestamp_iso8601": str,
    "step": int,
    "thinker_score": float,
    "motivation_components": {  # 8-factor breakdown
      "relevance": float, "info_gap": float, "curiosity": float, "pain": float,
      "coherence": float, "originality": float, "balance": float, "dynamics": float,
    },
    "psi_dir": float,             # Engine A ⇄ G coordinate (Law-71 mirror)
    "psi_entropy": float,
    "tension": float,
    "safety_flags": {             # 6/6 enforceable controls
      "kill_switch_on": bool,     # #1 — env ANIMA_SPONT_OFF
      "rate_limit_ok": bool,      # #2 — seconds_since_last >= MIN_EMIT_INTERVAL
      "content_filter_ok": bool,  # #3 — content_clean (dry-run True per Phase B scope)
      "phi_ratchet_ok": bool,     # #4 — phi > ratchet/2 (B-E-1)
      "meta_tag_present": bool,   # #5 — spont_meta_prefix on emit-side
      "audit_log_active": bool,   # #6 — THIS LOGGER ACTIVE (was STUB, now True)
    },
    "talker_decision": bool,      # talker_should_emit(score, safety_combined)
    "action": str,                # one of {"THINK_ONLY", "EMIT", "SAFETY_BLOCK"}
  }

g_doc_consolidation: state/* only. No docs/* file created.
g3 / B-IDENTITY-5 / f1/f2/f3 safe (no corpus, no helper-token, no σ/τ/φ/J₂).
"""

from __future__ import annotations
import datetime as _dt
import io
import json
import os
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Optional, IO


# ────────────────────────────────────────────────────────────────────────────
# action enum (closed 3-set)
# ────────────────────────────────────────────────────────────────────────────
ACTION_THINK_ONLY   = "THINK_ONLY"
ACTION_EMIT         = "EMIT"
ACTION_SAFETY_BLOCK = "SAFETY_BLOCK"
ACTION_SET = frozenset({ACTION_THINK_ONLY, ACTION_EMIT, ACTION_SAFETY_BLOCK})


# ────────────────────────────────────────────────────────────────────────────
# logger
# ────────────────────────────────────────────────────────────────────────────
@dataclass
class AuditLogger:
    """Append-only JSONL audit logger. Append-mode + line-buffered = each
    `write_step` produces exactly one '\\n'-terminated line, no partial writes
    on normal exit. Byte-count monotone non-decreasing across writes — verified
    post-run by B-PHASE-B-RUN-1.
    """
    log_path: Path
    _fh: Optional[IO[str]] = field(default=None, repr=False)
    _records_written: int = 0
    _byte_counts: list = field(default_factory=list, repr=False)  # for B-1 verification

    def __enter__(self) -> "AuditLogger":
        # mode 'a' = append. `buffering=1` only valid on text streams ⇒ line-buffered.
        # POSIX O_APPEND: each write is atomic at file-system level.
        self._fh = open(self.log_path, mode="a", encoding="utf-8", buffering=1)
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        if self._fh is not None:
            self._fh.flush()
            self._fh.close()
            self._fh = None

    def write_step(self, record: dict) -> None:
        """Append one JSONL line. Records byte-count before/after for B-1 invariant.
        """
        if self._fh is None:
            raise RuntimeError("AuditLogger: use as context manager (`with` block)")
        # validate action enum (closed 3-set, structural invariant)
        action = record.get("action")
        if action not in ACTION_SET:
            raise ValueError(f"AuditLogger: action {action!r} not in {ACTION_SET}")
        # validate safety_flags is dict with 6 booleans (B-PHASE-B-RUN-2 / -4 source)
        flags = record.get("safety_flags", {})
        if not isinstance(flags, dict) or len(flags) != 6:
            raise ValueError(
                f"AuditLogger: safety_flags must have exactly 6 controls, got {len(flags)}"
            )
        # byte count BEFORE write
        try:
            before = self.log_path.stat().st_size
        except FileNotFoundError:
            before = 0
        line = json.dumps(record, ensure_ascii=False, separators=(",", ":")) + "\n"
        self._fh.write(line)
        self._fh.flush()
        # byte count AFTER write
        after = self.log_path.stat().st_size
        # invariant: after >= before AND after - before == len(line.encode('utf-8'))
        assert after >= before, (
            f"AuditLogger byte-count monotone violation: before={before} after={after}"
        )
        assert after - before == len(line.encode("utf-8")), (
            f"AuditLogger byte-count delta mismatch: "
            f"actual={after-before} expected={len(line.encode('utf-8'))}"
        )
        self._byte_counts.append((before, after))
        self._records_written += 1

    @property
    def records_written(self) -> int:
        return self._records_written

    @property
    def byte_counts(self) -> list:
        return list(self._byte_counts)


def iso8601_now() -> str:
    """UTC iso8601 with millisecond precision, deterministic format."""
    now = _dt.datetime.now(_dt.timezone.utc)
    return now.strftime("%Y-%m-%dT%H:%M:%S.") + f"{now.microsecond // 1000:03d}Z"


# ────────────────────────────────────────────────────────────────────────────
# self-check (importable; only fires on direct invocation)
# ────────────────────────────────────────────────────────────────────────────
def _selftest_logger() -> None:
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        p = Path(td) / "test_audit.jsonl"
        with AuditLogger(p) as al:
            al.write_step({
                "timestamp_iso8601": iso8601_now(),
                "step": 0,
                "thinker_score": 0.1,
                "motivation_components": {"relevance": 0.0, "info_gap": 0.0,
                    "curiosity": 0.0, "pain": 0.0, "coherence": 0.0,
                    "originality": 0.0, "balance": 0.0, "dynamics": 0.0},
                "psi_dir": 0.5, "psi_entropy": 0.5, "tension": 0.0,
                "safety_flags": {"kill_switch_on": True, "rate_limit_ok": True,
                    "content_filter_ok": True, "phi_ratchet_ok": True,
                    "meta_tag_present": True, "audit_log_active": True},
                "talker_decision": False,
                "action": ACTION_THINK_ONLY,
            })
        assert al.records_written == 1
        content = p.read_text(encoding="utf-8")
        assert content.count("\n") == 1, f"line count: {content.count(chr(10))}"
        # parse round-trip
        rec = json.loads(content.strip())
        assert rec["step"] == 0
        assert rec["action"] == ACTION_THINK_ONLY
        assert len(rec["safety_flags"]) == 6
    print("audit_logger selftest: PASS")


if __name__ == "__main__":
    _selftest_logger()
