#!/usr/bin/env python3
"""akida_bridge.py — simplified: nc subprocess → broker WS (no async generator).

mini Python asyncio.open_connection() fails Errno 65 for LAN IP (macOS specific,
nc binary fine). Wrap nc as subprocess to bypass.
"""
import asyncio, json, logging, os, sys, time

PI_HOST = os.environ.get("AKIDA_PI_HOST", "192.168.50.155")
PI_PORT = int(os.environ.get("AKIDA_PI_PORT", "9512"))
BROKER_WS = os.environ.get("AKIDA_BROKER_WS", "ws://localhost:8000/ws/akida_ingest")
NC_BIN = os.environ.get("AKIDA_NC", "/usr/bin/nc")

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("akida_bridge")

try:
    import websockets
except ImportError:
    log.error("install websockets: pip install websockets")
    sys.exit(1)


async def run_once():
    """One full iteration: spawn nc + connect WS + forward all lines until either side fails."""
    proc = await asyncio.create_subprocess_exec(
        NC_BIN, "-w", "300", PI_HOST, str(PI_PORT),
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        stdin=asyncio.subprocess.DEVNULL,
    )
    log.info(f"nc subprocess pid={proc.pid} → {PI_HOST}:{PI_PORT}")
    try:
        ws = await websockets.connect(BROKER_WS, max_size=2**20)
        log.info(f"WS connected {BROKER_WS}")
    except Exception as e:
        log.warning(f"WS connect fail: {e}")
        proc.terminate()
        return
    try:
        n = 0
        while True:
            line = await proc.stdout.readline()
            if not line:
                err = (await proc.stderr.read()).decode("utf-8", errors="replace")[:200]
                log.warning(f"nc EOF (pid={proc.pid}, stderr={err!r})")
                break
            txt = line.decode("utf-8", errors="replace").strip()
            if not txt:
                continue
            try:
                spike = json.loads(txt)
            except Exception:
                continue
            spike["_bridge_ts"] = time.time()
            try:
                await ws.send(json.dumps(spike, ensure_ascii=False))
            except Exception as se:
                log.warning(f"ws send fail: {se}")
                break
            n += 1
            if n == 1 or n % 100 == 0:
                log.info(f"forwarded {n} spikes")
    finally:
        try: await ws.close()
        except Exception: pass
        try:
            proc.terminate()
            await proc.wait()
        except Exception: pass


async def main():
    while True:
        try:
            await run_once()
        except Exception as e:
            log.exception(f"run_once exception: {e}")
        log.info("reconnect in 5s")
        await asyncio.sleep(5)


if __name__ == "__main__":
    asyncio.run(main())
