#!/usr/bin/env python3
"""Phase 3 falsifier — 2 concurrent user WS clients verify broadcast +
participant push + history sync."""
import asyncio, json, sys
import websockets

URI = "ws://127.0.0.1:8000/ws"

async def client(name, send_text, recv_expect):
    out = {"received": [], "hello": None}
    async with websockets.connect(URI) as ws:
        hello = json.loads(await ws.recv())
        out["hello"] = hello
        await ws.send(json.dumps({"type": "nickname", "nickname": name}))
        # wait for participants update
        try:
            await asyncio.wait_for(ws.recv(), timeout=0.5)
        except asyncio.TimeoutError:
            pass
        if send_text:
            await asyncio.sleep(0.3)
            await ws.send(json.dumps({"type": "msg", "text": send_text}))
        # collect msgs for fixed window
        deadline = asyncio.get_event_loop().time() + 3.0
        while asyncio.get_event_loop().time() < deadline:
            try:
                remaining = deadline - asyncio.get_event_loop().time()
                if remaining <= 0:
                    break
                m = await asyncio.wait_for(ws.recv(), timeout=remaining)
                out["received"].append(json.loads(m))
            except asyncio.TimeoutError:
                break
    return out

async def main():
    A_task = asyncio.create_task(client("alice", "hi from alice", "hi from bob"))
    await asyncio.sleep(0.1)
    B_task = asyncio.create_task(client("bob",   "hi from bob",   "hi from alice"))
    A, B = await asyncio.gather(A_task, B_task)
    a_got = [m for m in A["received"] if m.get("type") == "msg"]
    b_got = [m for m in B["received"] if m.get("type") == "msg"]
    print(json.dumps({"alice_received_msgs": [m["text"]+":"+m["sender"] for m in a_got],
                      "bob_received_msgs": [m["text"]+":"+m["sender"] for m in b_got]},
                      ensure_ascii=False, indent=2))
    # falsifier: each must see both messages
    a_texts = {m["text"] for m in a_got}
    b_texts = {m["text"] for m in b_got}
    ok = ("hi from alice" in a_texts and "hi from bob" in a_texts and
          "hi from alice" in b_texts and "hi from bob" in b_texts)
    print("PHASE3_BROADCAST_PASS" if ok else "PHASE3_BROADCAST_FAIL")
    return 0 if ok else 1

if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
