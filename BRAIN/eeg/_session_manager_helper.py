#!/usr/bin/env python3
# anima-eeg session_manager helper.
#
# This file SUPERSEDES the parts.push("...") Python heredoc that
# eeg/_session_manager.hexa emitted at /tmp/anima_eeg_session_manager_helper.py
# retired (E-1 Phase 2b-2; see design/substrate_abstraction.md §11).
#
# BYTE-IDENTICAL-PRESERVING: the cmd_selftest() output below is character-for-
# character identical to the heredoc version, so the F_SM_01/02/03 + T_REC_01 +
# T_ERR_01 PASS conditions in eeg/_session_manager.hexa's in-hexa assertions
# stand unchanged. The schema string ("anima-eeg/_session_manager/1"), the
# advisory-URL base ("anima-eeg/docs/"), and the __EEG_SESSION_MGR__ sentinel
# anima-eeg paths here; that is a separate identity-rename PR.
#
# DEFAULTS that the .hexa interpolated as `let` constants are inlined below:
#   SCHEMA              = "anima-eeg/_session_manager/1"
#   DEFAULT_VENV_PYTHON = ".venv-eeg/bin/python"  -> VENV_PYTHON env override
#   ADVISORY_URL_BASE   = "anima-eeg/docs/"
#   DEFAULT_RECORDINGS_REL = "anima_eeg/Recordings"
#   DEFAULT_SETTINGS_REL   = "anima_eeg/Settings"

import argparse, atexit, glob, json, os, signal, sys, time, traceback
import datetime as _dt

SCHEMA          = 'anima-eeg/_session_manager/1'
VENV_PYTHON     = os.environ.get('ANIMA_EEG_VENV_PYTHON', '.venv-eeg/bin/python')
USB_SERIAL_GLOB = '/dev/cu.usbserial-*'
USB_MODEM_GLOB  = '/dev/cu.usbmodem*'

HOME = os.path.expanduser('~')
RECORDINGS_ROOT = os.path.join(HOME, 'anima_eeg/Recordings')
SETTINGS_ROOT   = os.path.join(HOME, 'anima_eeg/Settings')

def output(msg):
    sys.stderr.write(f'[output] {msg}\n'); sys.stderr.flush()

def output_error(msg):
    # bottom-bar tier: error. Visible but NOT action-blocking.
    sys.stderr.write(f'[error] {msg}\n'); sys.stderr.flush()

def modal(msg, advisory_url='', retry_action='retry|stop|help'):
    # honest C3: no PApplet -> no real popup. Operator must read stderr.
    sys.stderr.write(f'[modal] action_required: {msg} [{retry_action}] url={advisory_url}\n')
    sys.stderr.flush()

def emit_trailer(slug, detail, fix):
    sys.stderr.write(f'reason: {slug}: {detail}\n')
    sys.stderr.write(f'fix: {fix}\n'); sys.stderr.flush()

def is_leak(_m):
    _s = str(_m)
    for _n in ('PORT_ALREADY_OPEN','BOARD_NOT_READY',
               'STREAM_ALREADY_RUN','BOARD_NOT_CREATED',
               'ANOTHER_BOARD_IS_CREATED'):
        if _n in _s: return True
    for _c in (':1 ',':7 ',':8 ',':15 ',':16 ',
               ' code 1 ',' code 7 ',' code 8 ',
               ' code 15 ',' code 16 '):
        if _c in _s: return True
    return False

def cyton_soft_reset(port, baud=115200, timeout_s=3.0):
    try: import serial as _ser
    except Exception: return False
    try:
        with _ser.Serial(port, baud, timeout=0.5) as _s:
            _s.reset_input_buffer(); _s.write(b'v')
            _dl = time.time() + timeout_s; _buf = b''
            while time.time() < _dl:
                _ck = _s.read(64)
                if _ck:
                    _buf += _ck
                    if b'$$$' in _buf: time.sleep(0.2); return True
            return False
    except Exception: return False

STATE_PREINIT = 'PREINIT'
STATE_INIT    = 'INIT'
STATE_RUNNING = 'RUNNING'
STATE_HALTED  = 'HALTED'

class Session:
    def __init__(self, board_id, port, synthetic=False):
        self.board_id = int(board_id)
        self.port = port
        self.synthetic = bool(synthetic)
        self.state = STATE_PREINIT
        # close_session() short-circuits when has_halted=True so
        # double-close is a no-op (F_SM_01).
        self.has_halted = False
        # GUI.requestReinit() flag equivalent.
        self.request_reinit = False
        self.board = None
        self.params = None
        self.recording = None
        self.last_err = {'code': '', 'advisory_url': '', 'retry_action': ''}
        self.shutdown_bound = False
        self.shutdown_fired_count = 0

    def to_dict(self):
        return {'board_id': self.board_id, 'port': self.port,
                'synthetic': self.synthetic, 'state': self.state,
                'has_halted': self.has_halted,
                'request_reinit': self.request_reinit,
                'shutdown_fired_count': self.shutdown_fired_count,
                'last_error': self.last_err}

def api_open_session(board_id, port, retry_policy=None, synthetic=False):
    rp = retry_policy or {'max_retries': 2, 'soft_reset': True, 'sleep_s': 0.5}
    sess = Session(board_id, port, synthetic=synthetic)
    if synthetic:
        # No hardware path: state advance only.
        sess.state = STATE_INIT
        output(f'session opened (synthetic) board_id={board_id}')
        return sess
    try:
        from brainflow.board_shim import BoardShim, BrainFlowInputParams
    except Exception as exc:
        sess.last_err = {'code': 'brainflow-import-failed',
                         'advisory_url': 'anima-eeg/docs/ibm_cloud_env_setup_runbook_2026_05_03.md',
                         'retry_action': 'install-then-retry'}
        modal(f'brainflow not importable: {exc!r}',
              advisory_url=sess.last_err['advisory_url'])
        sess.state = STATE_HALTED; sess.has_halted = True
        return sess
    params = BrainFlowInputParams(); params.serial_port = port
    BoardShim.disable_board_logger()
    try: BoardShim.release_all_sessions()
    except Exception: pass
    board = BoardShim(int(board_id), params)
    attempt = 0
    while True:
        try:
            board.prepare_session(); break
        except Exception as e1:
            if not is_leak(e1) or attempt >= rp['max_retries']:
                sess.last_err = {'code': 'prepare-session-failed',
                                 'advisory_url': 'anima-eeg/docs/cyton_soft_reset_v_command_spec_2026_05_03.md',
                                 'retry_action': 'power-cycle-then-retry'}
                modal(f'prepare_session failed: {e1!r}',
                      advisory_url=sess.last_err['advisory_url'])
                sess.state = STATE_HALTED; sess.has_halted = True
                return sess
            try: BoardShim.release_all_sessions()
            except Exception: pass
            time.sleep(rp.get('sleep_s', 0.5))
            if rp.get('soft_reset', True) and port:
                cyton_soft_reset(port)
            time.sleep(rp.get('sleep_s', 0.5))
            board = BoardShim(int(board_id), params)
            attempt += 1
    sess.board = board; sess.params = params
    sess.state = STATE_INIT
    output(f'session opened (real) board_id={board_id} port={port}')
    return sess

def api_close_session(sess):
    if sess is None: return
    if sess.has_halted:
        output('close_session: already halted (idempotent skip)')
        return
    try:
        if sess.state == STATE_RUNNING and sess.board is not None:
            try: sess.board.stop_stream()
            except Exception: pass
        if sess.board is not None:
            try: sess.board.release_session()
            except Exception: pass
        # belt-and-suspenders: release any leaked partner session.
        try:
            from brainflow.board_shim import BoardShim
            BoardShim.release_all_sessions()
        except Exception: pass
    finally:
        sess.state = STATE_HALTED
        sess.has_halted = True
        output('close_session: state=HALTED')

def api_reinit(sess):
    # F_SM_03: atomic close + open. Must succeed-or-fail atomically;
    # if open phase fails, sess remains HALTED (closed) — caller
    # must not assume RUNNING/INIT after reinit unless state asserts.
    if sess is None: return None
    sess.request_reinit = True
    api_close_session(sess)
    sess.has_halted = False  # allow new open
    new_sess = api_open_session(sess.board_id, sess.port,
                                synthetic=sess.synthetic)
    sess.request_reinit = False
    output('reinit complete')
    return new_sess

class Recording:
    def __init__(self, session, fmt, max_min, dirpath, filepath):
        self.session = session
        self.fmt = fmt              # 'ODF' | 'BDF' | 'BF' | 'NPY'
        self.max_min = int(max_min) # 5/15/30/60/120/-1
        self.dirpath = dirpath
        self.filepath = filepath
        self.opened_at = time.time()
        self.rotated_count = 0
        self.is_open = True
    def to_dict(self):
        return {'fmt': self.fmt, 'max_min': self.max_min,
                'dirpath': self.dirpath, 'filepath': self.filepath,
                'rotated_count': self.rotated_count,
                'is_open': self.is_open}

def _now_iso():
    return _dt.datetime.now(_dt.timezone.utc).strftime('%Y%m%dT%H%M%SZ')

def api_start_recording(sess, name='default', fmt='ODF', max_min=15):
    if sess is None or sess.has_halted:
        output_error('start_recording: session halted/null'); return None
    if fmt not in ('ODF','BDF','BF','NPY'):
        output_error(f'start_recording: unknown fmt {fmt}'); return None
    if max_min not in (5,15,30,60,120,-1):
        output_error(f'start_recording: max_min must be 5/15/30/60/120/-1, got {max_min}')
        return None
    dirpath = os.path.join(RECORDINGS_ROOT, f'AnimaEEGSession_{name}')
    os.makedirs(dirpath, exist_ok=True)
    ext = {'ODF':'csv','BDF':'bdf','BF':'bf','NPY':'npy'}[fmt]
    filepath = os.path.join(dirpath, f'{_now_iso()}.{ext}')
    if not sess.synthetic and sess.board is not None:
        try:
            sess.board.start_stream()
        except Exception as e2:
            sess.last_err = {'code': 'start-stream-failed',
                             'advisory_url': 'anima-eeg/docs/cyton_soft_reset_v_command_spec_2026_05_03.md',
                             'retry_action': 'reinit-then-retry'}
            modal(f'start_stream failed: {e2!r}',
                  advisory_url=sess.last_err['advisory_url'])
            return None
    sess.state = STATE_RUNNING
    rec = Recording(sess, fmt, max_min, dirpath, filepath)
    sess.recording = rec
    output(f'start_recording fmt={fmt} max_min={max_min} path={filepath}')
    return rec

def api_rotate_if_needed(rec):
    if rec is None or not rec.is_open: return False
    if rec.fmt != 'ODF': return False  # only ODF supports rotation
    if rec.max_min == -1: return False # never rotate
    elapsed_min = (time.time() - rec.opened_at) / 60.0
    if elapsed_min < rec.max_min: return False
    new_path = os.path.join(rec.dirpath, f'{_now_iso()}.csv')
    rec.filepath = new_path
    rec.opened_at = time.time()
    rec.rotated_count += 1
    output(f'rotate_if_needed: rotated to {new_path} count={rec.rotated_count}')
    return True

def api_stop_recording(rec):
    if rec is None or not rec.is_open: return
    sess = rec.session
    if sess is not None and not sess.synthetic and sess.board is not None:
        try: sess.board.stop_stream()
        except Exception: pass
    rec.is_open = False
    if sess is not None and sess.state == STATE_RUNNING:
        sess.state = STATE_INIT
    output(f'stop_recording fmt={rec.fmt}')

def api_on_shutdown_hook(sess):
    if sess is None: return
    if sess.shutdown_bound:
        output('on_shutdown_hook: already bound (idempotent skip)')
        return
    def _hook(*_a, **_kw):
        sess.shutdown_fired_count += 1
        output(f'shutdown_hook fired n={sess.shutdown_fired_count}')
        try: api_close_session(sess)
        except Exception: traceback.print_exc()
    atexit.register(_hook)
    try: signal.signal(signal.SIGTERM, _hook)
    except Exception: pass
    try: signal.signal(signal.SIGINT,  _hook)
    except Exception: pass
    sess.shutdown_bound = True
    output('on_shutdown_hook: bound atexit + SIGTERM + SIGINT')

def api_last_error(sess):
    if sess is None:
        return {'code':'no-session','advisory_url':'','retry_action':''}
    return dict(sess.last_err)

# Spec: design/substrate_abstraction.md. These four api_*
# functions extend the BrainFlow session contract to match
# the substrate protocol declared in eeg/substrates/substrate.hexa.
def api_read_chunk(sess, n_samples_max):
    # Returns (data, ts). data is list-of-lists with shape
    # (rows, n_samples_max) — BrainFlow returns timestamp + EEG
    # + aux rows (rows == 32 for cyton_daisy). Caller MUST slice
    # by api_get_eeg_indices() for EEG-only access. Synthetic
    # session path returns [] (no synth data emitted here —
    # callers should switch to synth_substrate.hexa instead).
    if sess is None or getattr(sess,'has_halted',False):
        return [], time.time()
    if getattr(sess,'synthetic',False) or sess.board is None:
        return [], time.time()
    try:
        data = sess.board.get_current_board_data(int(n_samples_max))
        return [list(row) for row in data], time.time()
    except Exception as e:
        sess.last_err = {'code':'read-chunk-failed',
                         'advisory_url':'',
                         'retry_action':'reinit-then-retry'}
        output_error(f'read_chunk failed: {e!r}')
        return [], time.time()

def api_get_eeg_indices(sess):
    # Returns 1-indexed BrainFlow EEG channel indices. Falls
    # back to canonical 1..16 if BoardShim unavailable.
    if sess is None: return []
    try:
        from brainflow.board_shim import BoardShim
        return list(BoardShim.get_eeg_channels(int(sess.board_id)))
    except Exception:
        return list(range(1, 17))

def api_get_sample_rate(sess):
    if sess is None: return 0
    try:
        from brainflow.board_shim import BoardShim
        return int(BoardShim.get_sampling_rate(int(sess.board_id)))
    except Exception:
        return 125  # cyton_daisy default

def api_stim(sess, stim_spec):
    # BrainFlow path is scalp EEG — strictly read-only.
    # Future cl1 substrate implements api_stim; this raises.
    # Signature widened 2026-05-12 (see substrate.hexa APPENDIX A).
    raise NotImplementedError(
        '_session_manager: scalp EEG is read-only (no stim path)')

def cmd_selftest(args):
    print('== _session_manager selftest ==')
    print(f'schema={SCHEMA}')
    print('mode=selftest_synthetic')
    print(f'venv_python_exists={os.path.exists(VENV_PYTHON)}')
    fails = 0
    print('')
    print('[F_SM_01] open + close idempotent (close 2x no-op)')
    s1 = api_open_session(-1, '<synthetic>', synthetic=True)
    print(f'  state_after_open={s1.state}')
    api_close_session(s1)
    print(f'  state_after_close1={s1.state} has_halted={s1.has_halted}')
    api_close_session(s1)  # double-close: must be no-op
    print(f'  state_after_close2={s1.state} has_halted={s1.has_halted}')
    f01_ok = (s1.state == STATE_HALTED and s1.has_halted == True)
    print(f'F_SM_01={"PASS" if f01_ok else "FAIL"}')
    if not f01_ok: fails += 1
    print('')
    print('[F_SM_02] SIGTERM/atexit hook fires close_session')
    s2 = api_open_session(-1, '<synthetic>', synthetic=True)
    api_on_shutdown_hook(s2)
    print(f'  shutdown_bound={s2.shutdown_bound}')
    # Synthetic SIGTERM injection: invoke hook closure directly
    # (sending real SIGTERM to self risks aborting selftest before
    #  print). Same code path the signal handler would take.
    # Find the registered hook in atexit registry (private API): use
    # the SIGTERM handler we set, retrievable via signal.getsignal.
    h = signal.getsignal(signal.SIGTERM)
    if callable(h):
        try: h(signal.SIGTERM, None)
        except SystemExit: pass
    print(f'  shutdown_fired_count={s2.shutdown_fired_count}')
    print(f'  state_after_hook={s2.state} has_halted={s2.has_halted}')
    f02_ok = (s2.shutdown_fired_count >= 1 and s2.has_halted == True)
    print(f'F_SM_02={"PASS" if f02_ok else "FAIL"}')
    if not f02_ok: fails += 1
    print('')
    print('[F_SM_03] reinit (close + open) atomic, state PREINIT->INIT')
    s3 = api_open_session(-1, '<synthetic>', synthetic=True)
    state_pre = s3.state
    s3b = api_reinit(s3)
    print(f'  state_pre={state_pre} state_post={s3b.state}')
    f03_ok = (state_pre == STATE_INIT and s3b is not None
              and s3b.state == STATE_INIT)
    print(f'F_SM_03={"PASS" if f03_ok else "FAIL"}')
    if not f03_ok: fails += 1
    print('')
    print('[T_REC_01] start_recording / rotate_if_needed / stop_recording')
    s4 = api_open_session(-1, '<synthetic>', synthetic=True)
    rec = api_start_recording(s4, name='selftest', fmt='ODF', max_min=15)
    rec_ok = rec is not None and s4.state == STATE_RUNNING
    rotated_immediate = api_rotate_if_needed(rec)  # 0s elapsed → False
    api_stop_recording(rec)
    api_close_session(s4)
    rec_pass = (rec_ok and rotated_immediate == False
                and rec.is_open == False and s4.state == STATE_HALTED)
    print(f'T_REC_01={"PASS" if rec_pass else "FAIL"}')
    if not rec_pass: fails += 1
    print('')
    print('[T_ERR_01] last_error round-trip')
    s5 = api_open_session(-1, '<synthetic>', synthetic=True)
    err = api_last_error(s5)
    err_pass = ('code' in err and 'advisory_url' in err
                and 'retry_action' in err)
    print(f'  err_keys={sorted(err.keys())}')
    api_close_session(s5)
    print(f'T_ERR_01={"PASS" if err_pass else "FAIL"}')
    if not err_pass: fails += 1
    print('')
    if fails == 0:
        print('verdict=PASS')
        print('__EEG_SESSION_MGR__ PASS HALTED')
    else:
        print(f'verdict=FAIL fails={fails}')
        print(f'__EEG_SESSION_MGR__ FAIL fails={fails}')
    print('selftest=ok')
    print('DONE')
    sys.exit(0 if fails == 0 else 1)

def cmd_inspect(args):
    print(f'schema={SCHEMA}')
    print('mode=inspect')
    print('exported_api=open_session,close_session,reinit,start_recording,rotate_if_needed,stop_recording,on_shutdown_hook,last_error')
    print('states=PREINIT,INIT,RUNNING,HALTED')
    print('formats=ODF,BDF,BF,NPY')
    print('rotation_min=5,15,30,60,120,-1')
    print('feedback_tiers=output,error,modal')
    print('shutdown_signals=SIGTERM,SIGINT,atexit')
    print('shutdown_NOT_reached=SIGKILL')
    print('falsifiers=F_SM_01,F_SM_02,F_SM_03')
    print('inspect=ok')
    print('DONE')

def main():
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest='cmd', required=True)
    sub.add_parser('selftest')
    sub.add_parser('inspect')
    args = p.parse_args()
    if args.cmd == 'selftest': cmd_selftest(args)
    elif args.cmd == 'inspect':  cmd_inspect(args)
    else: sys.exit(2)

if __name__ == '__main__': main()
