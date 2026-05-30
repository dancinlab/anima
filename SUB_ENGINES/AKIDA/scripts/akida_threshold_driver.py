#!/usr/bin/env python3
"""akida_threshold_driver.py — the "말하기"(write) half of the COFFESHOP-on-AKIDA
bidirectional loop.

Subscribes to the broker's live motivation stream (/ws/motivation) and, on each
motivation packet, rewrites the on-chip LIF threshold on the Pi (ctrl port 9513)
so that high motivation lowers the threshold (chip fires → emit) and low
motivation raises it (chip silent). This closes the autonomous loop:

  anima motivation → broker /ws/motivation → THIS driver → set_threshold(9513)
    → on-chip threshold-and-fire(9512) → broker /ws/akida_ingest → frontend

Pairs with akida_ws_publisher.py (the "듣기"/read half, 9512 → broker).

Calibration (M-regime knee, measured live 2026-05-31): potential mean ~12-15, so
thr<=8 → fire (EMIT), thr>=16 → silent. emit-gate = motivation 0.60 (ANIMA.md
LAUNCHPAD trajectory `thr 0.60`): score>=0.60 → THR_EMIT, else THR_SILENCE.
"""
import asyncio, json, logging, os, socket, sys, time

BROKER_WS = os.environ.get("MOTIV_BROKER_WS", "ws://localhost:8000/ws/motivation")
PI5_HOST  = os.environ.get("AKIDA_PI5_HOST", "192.168.50.155")
PI5_CTRL  = int(os.environ.get("AKIDA_PI5_CTRL_PORT", "9513"))
EMIT_GATE = float(os.environ.get("EMIT_GATE", "0.60"))   # motivation threshold for emit
THR_EMIT  = int(os.environ.get("THR_EMIT", "8"))         # low thr → chip fires
THR_SIL   = int(os.environ.get("THR_SILENCE", "24"))     # high thr → chip silent

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("akida_threshold_driver")

try:
    import websockets
except ImportError:
    log.error("install websockets"); sys.exit(1)


def score_to_thr(score: float) -> int:
    """motivation score → on-chip threshold (thr ∝ −score, gated at EMIT_GATE)."""
    return THR_EMIT if score >= EMIT_GATE else THR_SIL


def send_threshold(thr: int, tries: int = 3) -> None:
    """Push a set_threshold_scalar command to the Pi ctrl port (9513).

    Retries on transient LAN errors (EHOSTUNREACH/ECONNREFUSED can flap on a
    shared L2 segment) with a short backoff before giving up.
    """
    last = None
    for attempt in range(tries):
        try:
            c = socket.create_connection((PI5_HOST, PI5_CTRL), timeout=5)
            try:
                c.sendall((json.dumps({"cmd": "set_threshold_scalar", "thr": thr}) + "\n").encode())
                time.sleep(0.05)
                return
            finally:
                c.close()
        except OSError as e:
            last = e
            time.sleep(0.3 * (attempt + 1))
    raise last


async def run() -> None:
    log.info("driver: subscribe %s → set_threshold %s:%d (gate=%.2f emit_thr=%d sil_thr=%d)",
             BROKER_WS, PI5_HOST, PI5_CTRL, EMIT_GATE, THR_EMIT, THR_SIL)
    last_thr = None
    async with websockets.connect(BROKER_WS) as ws:
        async for raw in ws:
            try:
                msg = json.loads(raw)
            except Exception:
                continue
            # the broker pushes a motivation_history snapshot first, then live packets
            packets = msg.get("list", [msg]) if msg.get("type") == "motivation_history" else [msg]
            for p in packets:
                score = p.get("score")
                if score is None:
                    continue
                thr = score_to_thr(float(score))
                if thr != last_thr:
                    try:
                        send_threshold(thr)
                        last_thr = thr
                        log.info("motivation score=%.3f → set_threshold(%d) [%s]",
                                 float(score), thr, "EMIT" if thr == THR_EMIT else "SILENCE")
                    except Exception as e:
                        log.error("ctrl send failed: %s", e)


if __name__ == "__main__":
    asyncio.run(run())
