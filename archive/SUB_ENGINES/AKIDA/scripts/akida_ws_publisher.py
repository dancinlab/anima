#!/usr/bin/env python3
"""akida_ws_publisher.py — reads spike JSON from stdin, publishes to broker WS.

Pipeline: `nc 192.168.50.155 9512 | akida_ws_publisher.py`

Avoids asyncio.subprocess complexity that silently fails in LaunchAgent context.
"""
import asyncio, json, logging, os, sys, time

BROKER_WS = os.environ.get("AKIDA_BROKER_WS", "ws://localhost:8000/ws/akida_ingest")

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("akida_ws_publisher")

try:
    import websockets
except ImportError:
    log.error("install websockets")
    sys.exit(1)


async def stream_stdin_to_ws():
    log.info(f"reading stdin, publishing → {BROKER_WS}")
    ws = None
    n = 0
    loop = asyncio.get_event_loop()
    while True:
        if ws is None:
            try:
                ws = await websockets.connect(BROKER_WS, max_size=2**20)
                log.info(f"WS connected {BROKER_WS}")
            except Exception as e:
                log.warning(f"WS connect fail: {e}")
                await asyncio.sleep(2)
                continue
        # read line from stdin (blocking sync via run_in_executor)
        try:
            line = await loop.run_in_executor(None, sys.stdin.readline)
        except Exception as e:
            log.warning(f"stdin read fail: {e}")
            break
        if not line:
            log.warning("stdin EOF — exit")
            break
        line = line.strip()
        if not line:
            continue
        try:
            spike = json.loads(line)
        except Exception:
            continue
        spike["_bridge_ts"] = time.time()
        try:
            await ws.send(json.dumps(spike, ensure_ascii=False))
        except Exception as e:
            log.warning(f"ws send fail: {e}, reconnect")
            try: await ws.close()
            except Exception: pass
            ws = None
            continue
        n += 1
        if n == 1 or n % 100 == 0:
            log.info(f"forwarded {n} spikes")
    if ws:
        try: await ws.close()
        except Exception: pass


if __name__ == "__main__":
    asyncio.run(stream_stdin_to_ws())
