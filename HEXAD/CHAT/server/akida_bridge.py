#!/usr/bin/env python3
"""akida_bridge.py — Pi spike_streamer TCP → broker WS forward.

mini 에서 영구 실행:
- TCP client → Pi 192.168.50.155:9512 (newline JSON spike events)
- WS client → ws://localhost:8000/ws/akida_ingest (broker fan-out)
- Pi 끊김 시 5s 재연결, broker WS 끊김 시도 동일

Used by FIRST-PACK Phase 7 AKIDA viz tab.
"""
import asyncio, json, logging, os, socket, sys, time

PI_HOST = os.environ.get("AKIDA_PI_HOST", "192.168.50.155")
PI_PORT = int(os.environ.get("AKIDA_PI_PORT", "9512"))
BROKER_WS = os.environ.get("AKIDA_BROKER_WS", "ws://localhost:8000/ws/akida_ingest")

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("akida_bridge")

try:
    import websockets  # pip install websockets
except ImportError:
    log.error("install websockets: pip install websockets")
    sys.exit(1)


async def tcp_lines(host: str, port: int):
    """Async iterator over newline-delimited JSON lines from Pi TCP server."""
    reader, writer = await asyncio.open_connection(host, port)
    log.info(f"TCP connected {host}:{port}")
    try:
        while True:
            line = await reader.readline()
            if not line:
                log.warning("TCP EOF from Pi")
                return
            line = line.decode("utf-8", errors="replace").strip()
            if not line:
                continue
            try:
                yield json.loads(line)
            except Exception as e:
                log.debug(f"parse fail {e}: {line[:80]!r}")
    finally:
        writer.close()
        try: await writer.wait_closed()
        except Exception: pass


async def forward_loop():
    """One iteration of: Pi TCP open → broker WS open → forward → close on error."""
    try:
        async with websockets.connect(BROKER_WS, max_size=2**20) as ws:
            log.info(f"WS connected {BROKER_WS}")
            async for spike in tcp_lines(PI_HOST, PI_PORT):
                # spike = {step, n_spikes, spike_ids, t_rel, regime, ...}
                # add bridge timestamp
                spike["_bridge_ts"] = time.time()
                await ws.send(json.dumps(spike, ensure_ascii=False))
    except (ConnectionRefusedError, OSError) as e:
        log.warning(f"Pi unreachable: {e}")
    except Exception as e:
        log.error(f"forward_loop err: {e}", exc_info=True)


async def main():
    while True:
        try:
            await forward_loop()
        except Exception as e:
            log.error(f"main err: {e}")
        log.info("reconnect in 5s")
        await asyncio.sleep(5)


if __name__ == "__main__":
    asyncio.run(main())
