#!/usr/bin/env python3
# hexa-brain/eeg/substrates/_brainflow_helper.py
#
# BoardShim lifecycle wrapper for the brainflow substrate.
#
# This file SUPERSEDES the parts.push("...") Python heredoc that
# eeg/substrates/brainflow_substrate.hexa carried pre-2026-05-12. The
# heredoc anti-pattern (RFC-016 §1.4 — ".hexa file that is actually a
# Python body in a string heredoc, stringified + subprocess-executed") is
# retired: this is hand-maintained Python, importable directly.
#
# TWO CALL SURFACES
#   1. embedded-CPython (RFC-016 P4 `import py`):
#        hexa calls py_call("_brainflow_helper", "<fn>", "<json>") via
#        stdlib/python_ffi. json-in / json-out. Session objects live in
#        this module's _SESSIONS registry; the hexa side holds only the
#        opaque session_id string. This is the path brainflow_substrate.hexa
#        uses post-Phase-2c (see design/substrate_abstraction.md §11).
#   2. standalone CLI (legacy / selftest):
#        `python3 _brainflow_helper.py selftest|inspect` — same body,
#        argparse front. Kept so `hexa run
#        eeg/substrates/brainflow_substrate.hexa --selftest` keeps working
#        during the migration window (the .hexa shells out to this file
#        instead of emitting a /tmp/ copy of its own heredoc).
#
#   - BoardShim numpy arrays are returned as nested Python lists inside the
#     json envelope (V1 string-only contract per RFC §3.2). A V2 zero-copy
#     path via stdlib/python_ffi.py_buffer_to_hexa is deferred — see §11.
#   - _session_manager delegation still loads
#     /tmp/anima_eeg_session_manager_helper.py via importlib (BACK-COMPAT
#     with the emit-pattern in eeg/_session_manager.hexa). Splitting
#     _session_manager.hexa into its own hand-maintained .py is a separate
#     byte-identical-preserving PR (§11 Phase 2b-2).
#   - data row count for the BrainFlow real path is 32 (timestamp + 16 EEG
#     + aux rows). read_chunk returns the FULL data matrix; callers slice
#     by get_eeg_indices() for EEG-only access. The EXPECTED_DATA_ROWS=32
#     invariant in collect.hexa / eeg_recorder.hexa is preserved for the
#     brainflow path (synth / replay return 16 rows).

import argparse
import importlib.util
import json
import os
import sys
import time
import uuid

SCHEMA = "hexa-brain/eeg/brainflow_substrate/1"
DEFAULT_BOARD_ID = 2       # CYTON_DAISY_BOARD
SYNTHETIC_BOARD_ID = -1    # BrainFlow synthetic board id

STATE_PREINIT = "PREINIT"
STATE_INIT = "INIT"
STATE_RUNNING = "RUNNING"
STATE_HALTED = "HALTED"

# Legacy emit-copy path (eeg/_session_manager.hexa still writes this during
# the migration window). Phase 2b-2 added the hand-maintained
# eeg/_session_manager_helper.py — preferred when present.
_SESSION_MANAGER_LEGACY_TMP_PATH = "/tmp/anima_eeg_session_manager_helper.py"


def _session_manager_helper_candidates():
    """Resolution order for the _session_manager helper module:
      1. eeg/_session_manager_helper.py — hand-maintained (Phase 2b-2),
         resolved via __file__ so it works regardless of cwd (the
         resource/tcp sandbox runs with cwd=/tmp/resource-tcp-* — never
         rely on cwd; see design/substrate_abstraction.md §11.1).
      2. /tmp/anima_eeg_session_manager_helper.py — legacy emit-copy."""
    here = os.path.dirname(os.path.abspath(__file__))   # .../eeg/substrates
    eeg_dir = os.path.dirname(here)                      # .../eeg
    return [
        os.path.join(eeg_dir, "_session_manager_helper.py"),
        _SESSION_MANAGER_LEGACY_TMP_PATH,
    ]


# ── Session shim (DEGRADED tier — used when the _session_manager helper is
#    unavailable OR the synthetic path is requested without a real board).
#    Wire-shape mirrors _session_manager.Session for parity.
class BfShimSession:
    def __init__(self, spec):
        self.spec = dict(spec)
        self.board_id = int(spec.get("board_id", DEFAULT_BOARD_ID))
        self.port = spec.get("port")
        self.synthetic = (
            self.board_id == SYNTHETIC_BOARD_ID
            or bool(spec.get("synthetic", False))
        )
        self.state = STATE_PREINIT
        self.has_halted = False
        self.shutdown_bound = False
        self.shutdown_fired_count = 0
        self.board = None
        self.recording = None
        self.last_err = {"code": "", "advisory_url": "", "retry_action": ""}
        cs = spec.get("channel_set") or {}
        self._sample_rate_hint = int(cs.get("sample_rate") or 125)
        self._eeg_indices_hint = list(cs.get("ids") or list(range(1, 17)))


# ── _session_manager bridge (delegation path) ──────────────────────────
def _try_load_session_manager():
    """Load the _session_manager helper module. Tries the hand-maintained
    eeg/_session_manager_helper.py first (Phase 2b-2), then the legacy
    /tmp/ emit-copy. Returns the module or None."""
    for path in _session_manager_helper_candidates():
        if not os.path.exists(path):
            continue
        try:
            spec = importlib.util.spec_from_file_location("_sm", path)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            return mod
        except Exception:
            continue
    return None


# ── Substrate contract — the 11 api_* methods ──────────────────────────
def api_open_session(spec):
    sm = _try_load_session_manager()
    board_id = int(spec.get("board_id", DEFAULT_BOARD_ID))
    port = spec.get("port")
    synth = (
        board_id == SYNTHETIC_BOARD_ID or bool(spec.get("synthetic", False))
    )
    if sm is not None and hasattr(sm, "api_open_session"):
        sess = sm.api_open_session(
            board_id, port, retry_policy=None, synthetic=synth
        )
        # Attach substrate metadata WITHOUT mutating sm.Session behavior —
        # these attrs are additive.
        cs = spec.get("channel_set") or {}
        sess._sample_rate_hint = int(cs.get("sample_rate") or 125)
        sess._eeg_indices_hint = list(cs.get("ids") or list(range(1, 17)))
        sess.spec = dict(spec)
        return sess
    # Fallback shim — used when the _session_manager helper has not been
    # emitted yet (e.g. brainflow_substrate selftest in isolation, no
    sess = BfShimSession(spec)
    sess.state = STATE_INIT
    sys.stderr.write(
        f"[output] brainflow_substrate.open (shim) "
        f"board_id={board_id} synth={synth}\n"
    )
    return sess


def api_close_session(sess):
    if sess is None:
        return
    if getattr(sess, "has_halted", False):
        return
    sm = _try_load_session_manager()
    if sm is not None and hasattr(sm, "api_close_session"):
        try:
            sm.api_close_session(sess)
            return
        except Exception:
            pass
    sess.state = STATE_HALTED
    sess.has_halted = True


def api_reinit(sess):
    if sess is None:
        return None
    spec = getattr(sess, "spec", None) or {}
    api_close_session(sess)
    sess.has_halted = False
    return api_open_session(spec)


def api_start_recording(sess, name="default", fmt="ODF", max_min=15):
    sm = _try_load_session_manager()
    if sm is not None and hasattr(sm, "api_start_recording"):
        return sm.api_start_recording(sess, name=name, fmt=fmt, max_min=max_min)

    # Shim — no real recording in DEGRADED mode.
    class _Rec:
        def __init__(self, s, n, f, m):
            self.session = s
            self.name = n
            self.fmt = f
            self.max_min = m
            self.is_open = True
            self.opened_at = time.time()

    rec = _Rec(sess, name, fmt, max_min)
    sess.state = STATE_RUNNING
    return rec


def api_stop_recording(rec):
    sm = _try_load_session_manager()
    if sm is not None and hasattr(sm, "api_stop_recording"):
        sm.api_stop_recording(rec)
        return
    if rec is None or not getattr(rec, "is_open", False):
        return
    rec.is_open = False


def api_read_chunk(sess, n_samples_max):
    """Real path: get_current_board_data(N) returns (rows, N) of float64.
    Callers slice by api_get_eeg_indices for EEG-only access. Synth path:
    returns empty list (DEGRADED tier honest disclosure — no synthetic data
    on the brainflow path when board absent; use synth_substrate for that)."""
    if sess is None or getattr(sess, "has_halted", False):
        return [], time.time()
    board = getattr(sess, "board", None)
    if board is None:
        return [], time.time()
    try:
        data = board.get_current_board_data(int(n_samples_max))
    except Exception as e:
        sess.last_err = {
            "code": "read-chunk-failed",
            "advisory_url": "",
            "retry_action": "reinit-then-retry",
        }
        sys.stderr.write(f"[error] brainflow_substrate.read_chunk {e!r}\n")
        return [], time.time()
    try:
        out = [list(row) for row in data]
    except Exception:
        out = []
    return out, time.time()


def api_get_eeg_indices(sess):
    if sess is None:
        return []
    try:
        from brainflow.board_shim import BoardShim

        bid = int(getattr(sess, "board_id", DEFAULT_BOARD_ID))
        return list(BoardShim.get_eeg_channels(bid))
    except Exception:
        return list(getattr(sess, "_eeg_indices_hint", list(range(1, 17))))


def api_get_sample_rate(sess):
    if sess is None:
        return 0
    try:
        from brainflow.board_shim import BoardShim

        bid = int(getattr(sess, "board_id", DEFAULT_BOARD_ID))
        return int(BoardShim.get_sampling_rate(bid))
    except Exception:
        return int(getattr(sess, "_sample_rate_hint", 125))


def api_stim(sess, stim_spec):
    # Signature widened 2026-05-12 (see eeg/substrates/substrate.hexa
    # APPENDIX A). Scalp EEG is read-only.
    raise NotImplementedError("brainflow_substrate: scalp EEG is read-only")


def api_on_shutdown_hook(sess, fn=None):
    sm = _try_load_session_manager()
    if sm is not None and hasattr(sm, "api_on_shutdown_hook"):
        sm.api_on_shutdown_hook(sess)
        return
    import atexit
    import signal

    if sess is None:
        return
    if getattr(sess, "shutdown_bound", False):
        return

    def _hook(*a, **kw):
        sess.shutdown_fired_count = getattr(sess, "shutdown_fired_count", 0) + 1
        try:
            api_close_session(sess)
        except Exception:
            pass

    atexit.register(_hook)
    try:
        signal.signal(signal.SIGTERM, _hook)
    except Exception:
        pass
    try:
        signal.signal(signal.SIGINT, _hook)
    except Exception:
        pass
    sess.shutdown_bound = True


def api_last_error(sess):
    if sess is None:
        return {"code": "no-session", "advisory_url": "", "retry_action": ""}
    return dict(
        getattr(sess, "last_err", {"code": "", "advisory_url": "", "retry_action": ""})
    )


# ── embedded-CPython (import py) surface: json-in / json-out ────────────
#
# Session objects cannot cross the py_call(module, fn, str) -> str boundary,
# so they live here in _SESSIONS keyed by an opaque "bf-<hex12>" string.
# The hexa side passes that string around; every json wrapper resolves it.

_SESSIONS = {}


def _arg(arg_json):
    """Decode a json arg (or accept an already-decoded dict for testing)."""
    if isinstance(arg_json, str):
        return json.loads(arg_json) if arg_json.strip() else {}
    return dict(arg_json or {})


def _sess(arg):
    sid = arg.get("session_id")
    return _SESSIONS.get(sid)


def open_session(spec_json):
    spec = _arg(spec_json)
    sess = api_open_session(spec)
    sid = "bf-" + uuid.uuid4().hex[:12]
    _SESSIONS[sid] = sess
    return json.dumps(
        {
            "session_id": sid,
            "state": getattr(sess, "state", STATE_INIT),
            "board_id": getattr(sess, "board_id", DEFAULT_BOARD_ID),
            "synthetic": bool(getattr(sess, "synthetic", False)),
        }
    )


def close_session(arg_json):
    arg = _arg(arg_json)
    sid = arg.get("session_id")
    sess = _SESSIONS.get(sid)
    api_close_session(sess)
    return json.dumps(
        {"session_id": sid, "has_halted": bool(getattr(sess, "has_halted", True))}
    )


def reinit(arg_json):
    arg = _arg(arg_json)
    old_sid = arg.get("session_id")
    old = _SESSIONS.get(old_sid)
    new_sess = api_reinit(old)
    new_sid = "bf-" + uuid.uuid4().hex[:12]
    _SESSIONS[new_sid] = new_sess
    return json.dumps(
        {
            "old_session_id": old_sid,
            "session_id": new_sid,
            "state": getattr(new_sess, "state", STATE_INIT),
        }
    )


def start_recording(arg_json):
    arg = _arg(arg_json)
    sess = _sess(arg)
    rec = api_start_recording(
        sess,
        name=arg.get("name", "default"),
        fmt=arg.get("fmt", "ODF"),
        max_min=int(arg.get("max_min", 15)),
    )
    rid = "rec-" + uuid.uuid4().hex[:12]
    _SESSIONS[rid] = rec
    return json.dumps({"recording_id": rid, "state": getattr(sess, "state", STATE_RUNNING)})


def stop_recording(arg_json):
    arg = _arg(arg_json)
    rec = _SESSIONS.get(arg.get("recording_id"))
    api_stop_recording(rec)
    return json.dumps({"recording_id": arg.get("recording_id"), "is_open": False})


def read_chunk(arg_json):
    arg = _arg(arg_json)
    data, ts = api_read_chunk(_sess(arg), int(arg.get("n_max", 32)))
    return json.dumps({"data": data, "ts": ts})


def get_eeg_indices(arg_json):
    return json.dumps(api_get_eeg_indices(_sess(_arg(arg_json))))


def get_sample_rate(arg_json):
    return json.dumps(api_get_sample_rate(_sess(_arg(arg_json))))


def stim(arg_json):
    # Mirrors api_stim — always raises for the brainflow (scalp EEG) path.
    # Returned only so the embedded-CPython caller gets a structured error
    # instead of a raw traceback string.
    return json.dumps(
        {
            "ok": False,
            "stim_id": "",
            "wall_time_ns": time.time_ns(),
            "frames_injected": 0,
            "last_err": {
                "code": "stim-not-implemented",
                "advisory_url": "",
                "retry_action": "use-cl1-substrate",
            },
        }
    )


def last_error(arg_json):
    return json.dumps(api_last_error(_sess(_arg(arg_json))))


# ── standalone CLI (legacy / selftest) ─────────────────────────────────
def cmd_selftest(args):
    print("== brainflow_substrate selftest ==")
    print(f"schema={SCHEMA}")
    print("mode=selftest_synthetic")
    fails = 0
    sm = _try_load_session_manager()
    print(f"  session_manager_helper_present={sm is not None}")

    spec = {
        "backend": "brainflow",
        "board_id": SYNTHETIC_BOARD_ID,
        "port": None,
        "synthetic": True,
        "channel_set": {
            "name": "cyton_daisy_16",
            "ids": list(range(1, 17)),
            "sample_rate": 125,
            "coords_3d": None,
        },
    }
    # F_SUB_02a: open + read + close on synth path returns expected sample_rate
    s1 = api_open_session(spec)
    sr = api_get_sample_rate(s1)
    idx = api_get_eeg_indices(s1)
    data, ts = api_read_chunk(s1, 32)
    print(f"  sample_rate={sr} eeg_idx[:4]={idx[:4]} data_rows={len(data)}")
    f02a = sr == 125 and len(idx) >= 1
    print(f'F_SUB_02_shape={"PASS" if f02a else "FAIL"}')
    if not f02a:
        fails += 1

    # F_SUB_02b: api_stim raises
    raised = False
    try:
        api_stim(s1, None)
    except NotImplementedError:
        raised = True
    print(f'F_SUB_02_stim_raises={"PASS" if raised else "FAIL"}')
    if not raised:
        fails += 1

    # F_SUB_02c: idempotent close
    api_close_session(s1)
    had_halt = getattr(s1, "has_halted", False)
    api_close_session(s1)  # double-close no-op
    f02c = had_halt is True and getattr(s1, "has_halted", False) is True
    print(f'F_SUB_02_idempotent={"PASS" if f02c else "FAIL"}')
    if not f02c:
        fails += 1

    # F_SUB_02d: embedded-CPython json surface round-trips (open → read → close)
    o = json.loads(open_session(json.dumps(spec)))
    rc = json.loads(read_chunk(json.dumps({"session_id": o["session_id"], "n_max": 32})))
    cl = json.loads(close_session(json.dumps({"session_id": o["session_id"]})))
    f02d = (
        isinstance(o.get("session_id"), str)
        and o["session_id"].startswith("bf-")
        and "data" in rc
        and cl.get("has_halted") is True
    )
    print(f'F_SUB_02_json_surface={"PASS" if f02d else "FAIL"}')
    if not f02d:
        fails += 1

    if fails == 0:
        print("verdict=PASS")
    else:
        print(f"verdict=FAIL fails={fails}")
    print("selftest=ok")
    print("DONE")
    sys.exit(0 if fails == 0 else 1)


def cmd_inspect(args):
    print(f"schema={SCHEMA}")
    print("mode=inspect")
    print(f"default_board_id={DEFAULT_BOARD_ID}")
    print(f"synthetic_board_id={SYNTHETIC_BOARD_ID}")
    print("delegates_to=_session_manager.hexa-helper")
    print("read_chunk_path=BoardShim.get_current_board_data")
    print("embedded_cpython_surface=open_session,close_session,reinit,"
          "start_recording,stop_recording,read_chunk,get_eeg_indices,"
          "get_sample_rate,stim,last_error")
    print("inspect=ok")
    print("DONE")


def main():
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("selftest")
    sub.add_parser("inspect")
    args = p.parse_args()
    if args.cmd == "selftest":
        cmd_selftest(args)
    elif args.cmd == "inspect":
        cmd_inspect(args)
    else:
        sys.exit(2)


if __name__ == "__main__":
    main()
