#!/usr/bin/env python3
"""akida_threshold_driver.py — "말하기"(write) half of COFFESHOP-on-AKIDA loop.

Pure-stdlib (urllib + socket): polls the broker's /motivation/recent for the
latest anima motivation_score and rewrites the on-chip LIF threshold on the Pi
(ctrl 9513) so high motivation → low threshold (fire/emit), low → high (silent).

Runs on the system python3 (no venv, no websockets) so it keeps macOS Local
Network access to the Pi LAN — the venv interpreter is denied that and gets
EHOSTUNREACH on 192.168.50.x while localhost still works.

  anima motivation → broker /motivation/recent → THIS driver → set_threshold(9513)
    → on-chip threshold-and-fire(9512) → broker /ws/akida_ingest → frontend
"""
import json, os, socket, time, urllib.request

BROKER   = os.environ.get("MOTIV_BROKER", "http://localhost:8000")
PI5_HOST = os.environ.get("AKIDA_PI5_HOST", "192.168.50.155")
PI5_CTRL = int(os.environ.get("AKIDA_PI5_CTRL_PORT", "9513"))
EMIT_GATE = float(os.environ.get("EMIT_GATE", "0.60"))
THR_EMIT  = int(os.environ.get("THR_EMIT", "8"))
THR_SIL   = int(os.environ.get("THR_SILENCE", "24"))
POLL_S    = float(os.environ.get("POLL_S", "0.8"))


def score_to_thr(score):
    return THR_EMIT if score >= EMIT_GATE else THR_SIL


def send_threshold(thr, tries=3):
    last = None
    for attempt in range(tries):
        try:
            c = socket.create_connection((PI5_HOST, PI5_CTRL), timeout=5)
            try:
                c.sendall((json.dumps({"cmd": "set_threshold_scalar", "thr": thr}) + "\n").encode())
                time.sleep(0.05); return
            finally:
                c.close()
        except OSError as e:
            last = e; time.sleep(0.3 * (attempt + 1))
    raise last


def latest_score():
    raw = urllib.request.urlopen(BROKER + "/motivation/recent", timeout=4).read()
    hist = json.loads(raw).get("motivation", [])
    for p in reversed(hist):
        if p.get("score") is not None:
            return float(p["score"]), p.get("ts")
    return None, None


def main():
    print("driver(stdlib): poll %s/motivation/recent → set_threshold %s:%d "
          "(gate=%.2f emit=%d sil=%d)" % (BROKER, PI5_HOST, PI5_CTRL, EMIT_GATE, THR_EMIT, THR_SIL), flush=True)
    last_thr = None; last_ts = None
    while True:
        try:
            score, ts = latest_score()
            if score is not None and ts != last_ts:
                last_ts = ts
                thr = score_to_thr(score)
                if thr != last_thr:
                    send_threshold(thr); last_thr = thr
                    print("motivation score=%.3f → set_threshold(%d) [%s]"
                          % (score, thr, "EMIT" if thr == THR_EMIT else "SILENCE"), flush=True)
        except Exception as e:
            print("WARN", repr(e)[:100], flush=True)
        time.sleep(POLL_S)


if __name__ == "__main__":
    main()
