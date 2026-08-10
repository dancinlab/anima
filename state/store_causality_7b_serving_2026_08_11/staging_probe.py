#!/usr/bin/env python3
"""Transport, emission, and soak probes for the pre-registered 7B staging gate."""
from __future__ import annotations

import argparse
import asyncio
import json
import pathlib
import statistics
import sys
import time
import urllib.request

def _percentile(values: list[float], q: float) -> float:
    ordered = sorted(values)
    index = max(0, min(len(ordered) - 1, int(q * len(ordered) + 0.999999) - 1))
    return ordered[index]


def _http_health(url: str) -> tuple[float, dict]:
    started = time.perf_counter()
    with urllib.request.urlopen(url, timeout=5) as response:
        body = json.loads(response.read())
        if response.status != 200:
            raise RuntimeError(f"health status {response.status}")
    return (time.perf_counter() - started) * 1000.0, body


async def _recv_until(ws, predicate, timeout: float = 5.0) -> dict:
    deadline = time.monotonic() + timeout
    while True:
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise TimeoutError("expected WebSocket frame was not received")
        message = json.loads(await asyncio.wait_for(ws.recv(), timeout=remaining))
        if predicate(message):
            return message


async def _transport(args) -> dict:
    import websockets

    http_ms = []
    health = None
    for _ in range(args.frames):
        elapsed, health = await asyncio.to_thread(_http_health, args.health_url)
        http_ms.append(elapsed)

    async with (
        websockets.connect(args.ws_base + "/ws/anima") as participant,
        websockets.connect(args.ws_base + "/ws") as user_a,
        websockets.connect(args.ws_base + "/ws") as user_b,
    ):
        await _recv_until(participant, lambda m: m.get("type") == "hello")
        hello_a = await _recv_until(user_a, lambda m: m.get("type") == "hello")
        hello_b = await _recv_until(user_b, lambda m: m.get("type") == "hello")
        await user_a.send(json.dumps({"type": "nickname", "nickname": "probe-a"}))
        await user_b.send(json.dumps({"type": "nickname", "nickname": "probe-b"}))

        ws_ms = []
        for index in range(args.frames):
            text = f"staging-frame-{index:04d}"
            started = time.perf_counter()
            await user_a.send(json.dumps({"type": "msg", "text": text}))
            predicate = lambda m, text=text: m.get("type") == "msg" and m.get("text") == text
            await asyncio.gather(
                _recv_until(user_a, predicate),
                _recv_until(user_b, predicate),
                _recv_until(participant, predicate),
            )
            ws_ms.append((time.perf_counter() - started) * 1000.0)

    return {
        "http": {
            "n": len(http_ms),
            "failures": 0,
            "p50_ms": statistics.median(http_ms),
            "p95_ms": _percentile(http_ms, 0.95),
            "max_ms": max(http_ms),
            "last_health": health,
        },
        "websocket": {
            "n": len(ws_ms),
            "failures": 0,
            "recipients_per_frame": 3,
            "p50_ms": statistics.median(ws_ms),
            "p95_ms": _percentile(ws_ms, 0.95),
            "max_ms": max(ws_ms),
            "hello_anima_alive": [hello_a.get("anima_alive"), hello_b.get("anima_alive")],
        },
    }


async def _generation(args) -> dict:
    import websockets

    walls = []
    visible_bytes = []
    async with (
        websockets.connect(args.ws_base + "/ws/motivation") as motivation,
        websockets.connect(args.ws_base + "/ws") as user,
    ):
        await _recv_until(motivation, lambda m: m.get("type") == "motivation_history")
        await _recv_until(user, lambda m: m.get("type") == "hello")
        for _ in range(args.emissions):
            await _recv_until(motivation, lambda m: m.get("decided_emit") is True,
                              timeout=args.timeout)
            started = time.perf_counter()
            message = await _recv_until(
                user,
                lambda m: m.get("type") == "msg" and m.get("kind") == "anima",
                timeout=args.timeout,
            )
            walls.append(time.perf_counter() - started)
            visible_bytes.append(len(message.get("text", "").encode("utf-8")))

    throughput = [args.engine_bytes / wall for wall in walls]
    return {
        "n": len(walls),
        "engine_bytes_per_emission": args.engine_bytes,
        "wall_seconds": walls,
        "visible_utf8_bytes": visible_bytes,
        "p50_wall_seconds": statistics.median(walls),
        "p95_wall_seconds": _percentile(walls, 0.95),
        "min_engine_bytes_per_second": min(throughput),
        "mean_engine_bytes_per_second": statistics.mean(throughput),
    }


async def _direct_generation(args) -> dict:
    if not args.checkpoint:
        raise ValueError("--checkpoint is required for direct-generation")
    chat_dir = pathlib.Path(__file__).resolve().parents[2] / "agent" / "domains" / "CHAT"
    sys.path.insert(0, str(chat_dir))
    from substrate_clm import CLMSubstrate

    substrate = CLMSubstrate(args.checkpoint)
    substrate.generate("staging warmup", max_new=args.engine_bytes)
    walls = []
    visible_bytes = []
    for index in range(args.emissions):
        started = time.perf_counter()
        text = substrate.generate(f"staging emission {index:02d}", max_new=args.engine_bytes)
        walls.append(time.perf_counter() - started)
        visible_bytes.append(len(text.encode("utf-8")))
    throughput = [args.engine_bytes / wall for wall in walls]
    return {
        "scope": "CLMSubstrate.generate via canonical core/decode",
        "n": len(walls),
        "engine_bytes_per_emission": args.engine_bytes,
        "wall_seconds": walls,
        "visible_utf8_bytes": visible_bytes,
        "p50_wall_seconds": statistics.median(walls),
        "p95_wall_seconds": _percentile(walls, 0.95),
        "min_engine_bytes_per_second": min(throughput),
        "mean_engine_bytes_per_second": statistics.mean(throughput),
    }


async def _soak(args) -> dict:
    import websockets

    started = time.monotonic()
    http_ms = []
    ws_ms = []
    probes = 0
    async with (
        websockets.connect(args.ws_base + "/ws") as user_a,
        websockets.connect(args.ws_base + "/ws") as user_b,
    ):
        await _recv_until(user_a, lambda m: m.get("type") == "hello")
        await _recv_until(user_b, lambda m: m.get("type") == "hello")
        while time.monotonic() - started < args.duration:
            elapsed, health = await asyncio.to_thread(_http_health, args.health_url)
            if not health.get("ok") or not health.get("anima_alive"):
                raise RuntimeError(f"unhealthy during soak: {health}")
            http_ms.append(elapsed)
            text = f"soak-probe-{probes:05d}"
            sent = time.perf_counter()
            await user_a.send(json.dumps({"type": "msg", "text": text}))
            predicate = lambda m, text=text: m.get("type") == "msg" and m.get("text") == text
            await asyncio.gather(_recv_until(user_a, predicate), _recv_until(user_b, predicate))
            ws_ms.append((time.perf_counter() - sent) * 1000.0)
            probes += 1
            await asyncio.sleep(args.interval)

    return {
        "requested_seconds": args.duration,
        "elapsed_seconds": time.monotonic() - started,
        "probes": probes,
        "failures": 0,
        "http_p95_ms": _percentile(http_ms, 0.95),
        "websocket_p95_ms": _percentile(ws_ms, 0.95),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("transport", "generation", "direct-generation", "soak"))
    parser.add_argument("--health-url", default="http://127.0.0.1:8000/health")
    parser.add_argument("--ws-base", default="ws://127.0.0.1:8000")
    parser.add_argument("--frames", type=int, default=100)
    parser.add_argument("--emissions", type=int, default=20)
    parser.add_argument("--engine-bytes", type=int, default=32)
    parser.add_argument("--timeout", type=float, default=60.0)
    parser.add_argument("--checkpoint")
    parser.add_argument("--duration", type=float, default=1800.0)
    parser.add_argument("--interval", type=float, default=5.0)
    args = parser.parse_args()
    if min(args.frames, args.emissions, args.engine_bytes) <= 0:
        parser.error("frames, emissions, and engine-bytes must be positive")
    if args.duration <= 0 or args.interval <= 0 or args.timeout <= 0:
        parser.error("duration, interval, and timeout must be positive")
    handlers = {
        "transport": _transport,
        "generation": _generation,
        "direct-generation": _direct_generation,
        "soak": _soak,
    }
    result = asyncio.run(handlers[args.mode](args))
    print(json.dumps(result, ensure_ascii=True, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
