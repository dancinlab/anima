#!/usr/bin/env python3
"""Transport, emission, and soak probes for the pre-registered 7B staging gate."""
from __future__ import annotations

import argparse
import asyncio
from collections import Counter
import json
import pathlib
import re
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
    request = urllib.request.Request(
        url, headers={"User-Agent": "anima-staging-probe/1"})
    with urllib.request.urlopen(request, timeout=5) as response:
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


def _reply_contract(prompt: str, reply: str) -> dict:
    text = reply.strip()
    chars = [char for char in text if not char.isspace()]
    dominant = Counter(chars).most_common(1)[0][1] / len(chars) if chars else 1.0
    words = [word.casefold() for word in text.split() if word]
    most_repeated = Counter(words).most_common(1)[0][1] if words else 0
    repeated_word_ratio = most_repeated / len(words) if words else 1.0
    lexical_diversity = len(set(words)) / len(words) if words else 0.0
    controls = sum(
        1 for char in text
        if (ord(char) < 32 and char not in "\n\t ") or ord(char) == 127)
    control_ratio = controls / len(text) if text else 1.0
    prompt_has_hangul = any("가" <= char <= "힣" for char in prompt)
    reply_has_hangul = any("가" <= char <= "힣" for char in text)
    language_aligned = not prompt_has_hangul or reply_has_hangul
    folded_prompt = prompt.casefold().strip()
    folded_reply = text.casefold()
    if "한글" in prompt and ("가능" in prompt or "할 수" in prompt):
        semantic_alignment = reply_has_hangul and any(
            term in text for term in ("가능", "네", "예", "물론"))
    elif "consciousness" in folded_prompt:
        semantic_alignment = bool(re.search(
            r"\b(consciousness|awareness|experience|mind|sentien\w*)\b",
            folded_reply,
        ))
    else:
        semantic_alignment = True
    passed = (
        len(text) >= 4
        and dominant < 0.6
        and (most_repeated == 1 or repeated_word_ratio < 0.5)
        and lexical_diversity >= 0.55
        and control_ratio < 0.05
        and language_aligned
        and semantic_alignment
    )
    return {
        "passed": passed,
        "non_empty": len(text) >= 4,
        "dominant_character_ratio": dominant,
        "repeated_word_ratio": repeated_word_ratio,
        "lexical_diversity": lexical_diversity,
        "control_ratio": control_ratio,
        "language_aligned": language_aligned,
        "semantic_alignment": semantic_alignment,
    }


async def _conversation(args) -> dict:
    """Verify user-turn -> visible, non-degenerate, language-aligned reply."""
    import websockets

    prompts = args.prompt or ["한글 가능해?", "What is consciousness?"]
    turns = []
    async with websockets.connect(args.ws_base + "/ws") as user:
        await _recv_until(user, lambda m: m.get("type") == "hello")
        await user.send(json.dumps({"type": "nickname", "nickname": "conversation-qa"}))
        for prompt in prompts:
            started = time.time()
            await user.send(json.dumps({"type": "msg", "text": prompt}, ensure_ascii=False))
            echoed = await _recv_until(
                user,
                lambda m, prompt=prompt: (
                    m.get("type") == "msg"
                    and m.get("kind") == "user"
                    and m.get("text") == prompt),
                timeout=args.timeout,
            )
            message = await _recv_until(
                user,
                lambda m, started=started, reply_to=echoed.get("id"): (
                    m.get("type") == "msg"
                    and m.get("kind") == "anima"
                    and float(m.get("ts", 0)) >= started
                    and m.get("reply_to") == reply_to),
                timeout=args.timeout,
            )
            reply = str(message.get("text", ""))
            contract = _reply_contract(prompt, reply)
            turns.append({
                "prompt": prompt,
                "reply": reply,
                "latency_seconds": time.time() - started,
                "contract": contract,
            })
    if len({turn["reply"] for turn in turns}) != len(turns):
        for turn in turns:
            turn["contract"]["passed"] = False
            turn["contract"]["distinct_from_other_turns"] = False
    else:
        for turn in turns:
            turn["contract"]["distinct_from_other_turns"] = True
    passed = all(turn["contract"]["passed"] for turn in turns)
    if not passed:
        raise RuntimeError(json.dumps({"conversation": turns}, ensure_ascii=False))
    return {"passed": True, "turns": turns}


async def _multi_user_conversation(args) -> dict:
    """Queue two users before either answer and verify exact turn ownership."""
    import websockets

    prompts = args.prompt or ["한글 가능해?", "What is consciousness?"]
    if len(prompts) != 2:
        raise ValueError("conversation-multi-user requires exactly two prompts")
    async with (
        websockets.connect(args.ws_base + "/ws") as first,
        websockets.connect(args.ws_base + "/ws") as second,
    ):
        await _recv_until(first, lambda message: message.get("type") == "hello")
        await _recv_until(second, lambda message: message.get("type") == "hello")
        await first.send(json.dumps({"type": "nickname", "nickname": "conversation-qa-a"}))
        await second.send(json.dumps({"type": "nickname", "nickname": "conversation-qa-b"}))
        started = time.time()
        await first.send(json.dumps({"type": "msg", "text": prompts[0]}, ensure_ascii=False))
        await second.send(json.dumps({"type": "msg", "text": prompts[1]}, ensure_ascii=False))
        echoed = []
        for ws, prompt in ((first, prompts[0]), (second, prompts[1])):
            echoed.append(await _recv_until(
                ws,
                lambda message, prompt=prompt: (
                    message.get("type") == "msg"
                    and message.get("kind") == "user"
                    and message.get("text") == prompt),
                timeout=args.timeout,
            ))
        pending = {message["id"]: prompt for message, prompt in zip(echoed, prompts)}
        turns = []
        while pending:
            message = await _recv_until(
                first,
                lambda item, pending=pending: (
                    item.get("type") == "msg"
                    and item.get("kind") == "anima"
                    and item.get("reply_to") in pending),
                timeout=args.timeout,
            )
            reply_to = message["reply_to"]
            prompt = pending.pop(reply_to)
            reply = str(message.get("text", ""))
            turns.append({
                "prompt": prompt,
                "reply": reply,
                "reply_to": reply_to,
                "latency_seconds": time.time() - started,
                "contract": _reply_contract(prompt, reply),
            })
    turns.sort(key=lambda turn: prompts.index(turn["prompt"]))
    distinct = len({turn["reply"] for turn in turns}) == len(turns)
    for turn in turns:
        turn["contract"]["distinct_from_other_turns"] = distinct
        turn["contract"]["passed"] = turn["contract"]["passed"] and distinct
    if not all(turn["contract"]["passed"] for turn in turns):
        raise RuntimeError(json.dumps({"conversation_multi_user": turns}, ensure_ascii=False))
    return {"passed": True, "turns": turns}


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
            sent = time.perf_counter()
            pong_a = await user_a.ping()
            pong_b = await user_b.ping()
            await asyncio.gather(pong_a, pong_b)
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
    parser.add_argument(
        "mode",
        choices=("transport", "generation", "conversation", "conversation-multi-user",
                 "direct-generation", "soak"),
    )
    parser.add_argument("--health-url", default="http://127.0.0.1:8000/health")
    parser.add_argument("--ws-base", default="ws://127.0.0.1:8000")
    parser.add_argument("--frames", type=int, default=100)
    parser.add_argument("--emissions", type=int, default=20)
    parser.add_argument("--engine-bytes", type=int, default=32)
    parser.add_argument("--timeout", type=float, default=60.0)
    parser.add_argument("--prompt", action="append")
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
        "conversation": _conversation,
        "conversation-multi-user": _multi_user_conversation,
        "direct-generation": _direct_generation,
        "soak": _soak,
    }
    result = asyncio.run(handlers[args.mode](args))
    print(json.dumps(result, ensure_ascii=True, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
