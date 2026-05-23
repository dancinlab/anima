#!/usr/bin/env python3
"""FIRST-PACK Phase 3 — chat broker (FastAPI + WebSocket).

Multi-user group chat broker for anima 0.11.0 deployment at
chat.dancinlab.org. anima 는 a special participant who joins
via the anima_participant.py side-process, NOT triggered by user msgs.

Endpoints:
  GET  /            → serve static/index.html
  GET  /static/*    → static assets
  WS   /ws          → main chat WebSocket
  WS   /ws/anima    → anima participant WebSocket (separate stream for
                      8-factor motivation telemetry + emission)
  WS   /ws/akida    → AKIDA spike telemetry stream (from Pi forwarder)
  GET  /participants → JSON snapshot of active participants
  GET  /history     → JSON snapshot of last 50 turns
  GET  /health      → {"ok": true, "anima_alive": bool}

Substrate-native invariant (project.tape @D a_substrate_native_speak):
  - broker NEVER triggers anima generation on user message arrival
  - broker FORWARDS user messages to anima_participant as environment input
  - anima_participant decides emission based on its OWN self-tick + motivation
  - anima emission arrives via /ws/anima as a normal broadcast
"""
from __future__ import annotations
import asyncio, json, time, uuid, logging, os, pathlib
from collections import deque
from typing import Any
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles

try:
    from langdetect import detect, DetectorFactory
    DetectorFactory.seed = 42
    _HAS_LANGDETECT = True
except Exception:
    _HAS_LANGDETECT = False

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger("broker")

HERE = pathlib.Path(__file__).parent
STATIC_DIR = (HERE / "static").resolve()
if not STATIC_DIR.exists():
    alt = (HERE.parent / "static").resolve()
    if alt.exists():
        STATIC_DIR = alt
    else:
        STATIC_DIR.mkdir(parents=True, exist_ok=True)

HISTORY_MAX = 50
MSG_MAX_CHARS = 500

app = FastAPI(title="anima-chat-broker", version="0.11.0")
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


# ── state ────────────────────────────────────────────────────────────────────
class BrokerState:
    def __init__(self) -> None:
        self.users: dict[str, dict[str, Any]] = {}  # client_id → {ws, nickname}
        self.anima_ws: WebSocket | None = None
        self.anima_alive: bool = False
        self.akida_subscribers: set[WebSocket] = set()
        self.history: deque[dict[str, Any]] = deque(maxlen=HISTORY_MAX)
        self.motivation_subscribers: set[WebSocket] = set()
        self.akida_history: deque[dict[str, Any]] = deque(maxlen=200)
        self.motivation_history: deque[dict[str, Any]] = deque(maxlen=200)

    def participants(self) -> list[dict[str, Any]]:
        out = [{"id": cid, "nickname": u["nickname"], "kind": "user"}
               for cid, u in self.users.items()]
        if self.anima_alive:
            out.append({"id": "anima", "nickname": "anima", "kind": "anima"})
        return out


STATE = BrokerState()


# ── lang detect ──────────────────────────────────────────────────────────────
def detect_lang(text: str) -> str:
    """Return ISO 639-1 lang code OR unicode-block heuristic."""
    if not text or not text.strip():
        return "und"
    if _HAS_LANGDETECT:
        try:
            return detect(text)
        except Exception:
            pass
    # heuristic fallback
    counts = {"ko": 0, "ja": 0, "zh": 0, "ru": 0, "en": 0}
    for ch in text:
        cp = ord(ch)
        if 0xAC00 <= cp <= 0xD7AF:
            counts["ko"] += 1
        elif 0x3040 <= cp <= 0x309F or 0x30A0 <= cp <= 0x30FF:
            counts["ja"] += 1
        elif 0x4E00 <= cp <= 0x9FFF:
            counts["zh"] += 1
        elif 0x0400 <= cp <= 0x04FF:
            counts["ru"] += 1
        elif 0x0041 <= cp <= 0x007A:
            counts["en"] += 1
    if max(counts.values()) == 0:
        return "und"
    return max(counts, key=counts.get)


# ── broadcast ────────────────────────────────────────────────────────────────
async def broadcast(payload: dict[str, Any]) -> None:
    raw = json.dumps(payload, ensure_ascii=False)
    dead = []
    for cid, u in STATE.users.items():
        try:
            await u["ws"].send_text(raw)
        except Exception:
            dead.append(cid)
    if STATE.anima_ws is not None:
        try:
            await STATE.anima_ws.send_text(raw)
        except Exception:
            STATE.anima_ws = None
            STATE.anima_alive = False
    for cid in dead:
        STATE.users.pop(cid, None)


async def push_participants() -> None:
    await broadcast({"type": "participants", "list": STATE.participants()})


# ── HTTP ─────────────────────────────────────────────────────────────────────
@app.get("/")
async def root():
    idx = STATIC_DIR / "index.html"
    if idx.exists():
        return FileResponse(str(idx))
    return HTMLResponse("<h1>anima chat broker — Phase 3</h1>"
                        "<p>WebSocket: <code>/ws</code></p>")


@app.get("/health")
async def health():
    return {"ok": True, "anima_alive": STATE.anima_alive,
            "users": len(STATE.users),
            "history_len": len(STATE.history),
            "langdetect": _HAS_LANGDETECT}


@app.get("/participants")
async def participants():
    return {"participants": STATE.participants()}


@app.get("/history")
async def history():
    return {"history": list(STATE.history)}


@app.get("/akida/recent")
async def akida_recent():
    return {"akida": list(STATE.akida_history)}


@app.get("/motivation/recent")
async def motivation_recent():
    return {"motivation": list(STATE.motivation_history)}


# ── /ws  (user chat) ─────────────────────────────────────────────────────────
@app.websocket("/ws")
async def ws_user(ws: WebSocket):
    await ws.accept()
    client_id = uuid.uuid4().hex[:8]
    nickname = f"user_{client_id[:4]}"
    STATE.users[client_id] = {"ws": ws, "nickname": nickname}
    log.info("user join %s nickname=%s", client_id, nickname)
    try:
        # send history + participants on join
        await ws.send_text(json.dumps({"type": "hello", "client_id": client_id,
                                       "nickname": nickname,
                                       "history": list(STATE.history),
                                       "participants": STATE.participants(),
                                       "anima_alive": STATE.anima_alive},
                                      ensure_ascii=False))
        await push_participants()

        while True:
            raw = await ws.receive_text()
            try:
                msg = json.loads(raw)
            except Exception:
                continue
            kind = msg.get("type", "msg")
            if kind == "nickname":
                new = (msg.get("nickname") or "").strip()[:40]
                if new:
                    STATE.users[client_id]["nickname"] = new
                    nickname = new
                    await push_participants()
                continue
            if kind == "msg":
                text = (msg.get("text") or "").strip()
                if not text:
                    continue
                if len(text) > MSG_MAX_CHARS:
                    text = text[:MSG_MAX_CHARS]
                payload = {
                    "type": "msg",
                    "id": uuid.uuid4().hex[:12],
                    "sender": nickname,
                    "sender_id": client_id,
                    "kind": "user",
                    "lang": detect_lang(text),
                    "text": text,
                    "ts": time.time(),
                }
                STATE.history.append(payload)
                await broadcast(payload)
    except WebSocketDisconnect:
        pass
    except Exception as e:
        log.warning("user ws error %s: %s", client_id, e)
    finally:
        STATE.users.pop(client_id, None)
        log.info("user leave %s", client_id)
        await push_participants()


# ── /ws/anima  (anima participant link) ──────────────────────────────────────
@app.websocket("/ws/anima")
async def ws_anima(ws: WebSocket):
    await ws.accept()
    if STATE.anima_ws is not None:
        await ws.send_text(json.dumps({"type": "error",
                                       "reason": "anima_already_connected"}))
        await ws.close()
        return
    STATE.anima_ws = ws
    STATE.anima_alive = True
    log.info("anima connected")
    try:
        await ws.send_text(json.dumps({"type": "hello",
                                       "history": list(STATE.history),
                                       "participants": STATE.participants()},
                                      ensure_ascii=False))
        await push_participants()
        while True:
            raw = await ws.receive_text()
            try:
                msg = json.loads(raw)
            except Exception:
                continue
            kind = msg.get("type", "")
            if kind == "msg":
                text = (msg.get("text") or "").strip()
                if not text:
                    continue
                payload = {
                    "type": "msg",
                    "id": uuid.uuid4().hex[:12],
                    "sender": "anima",
                    "sender_id": "anima",
                    "kind": "anima",
                    "lang": msg.get("lang") or detect_lang(text),
                    "text": text[:MSG_MAX_CHARS],
                    "ts": time.time(),
                    "motivation": msg.get("motivation"),
                    "factors": msg.get("factors"),
                }
                STATE.history.append(payload)
                await broadcast(payload)
            elif kind == "motivation":
                # 8-factor telemetry stream (does NOT broadcast to all users
                # by default — pushes only to motivation_subscribers)
                ts = msg.get("ts", time.time())
                packet = {"type": "motivation",
                          "ts": ts,
                          "score": msg.get("score"),
                          "threshold": msg.get("threshold"),
                          "factors": msg.get("factors"),
                          "decided_emit": msg.get("decided_emit", False)}
                STATE.motivation_history.append(packet)
                raw_p = json.dumps(packet, ensure_ascii=False)
                dead = []
                for sub in STATE.motivation_subscribers:
                    try:
                        await sub.send_text(raw_p)
                    except Exception:
                        dead.append(sub)
                for d in dead:
                    STATE.motivation_subscribers.discard(d)
    except WebSocketDisconnect:
        pass
    except Exception as e:
        log.warning("anima ws error: %s", e)
    finally:
        STATE.anima_ws = None
        STATE.anima_alive = False
        log.info("anima disconnected")
        await push_participants()


# ── /ws/motivation  (frontend motivation subscriber) ─────────────────────────
@app.websocket("/ws/motivation")
async def ws_motivation(ws: WebSocket):
    await ws.accept()
    STATE.motivation_subscribers.add(ws)
    try:
        # send recent history on subscribe
        await ws.send_text(json.dumps({"type": "motivation_history",
                                       "list": list(STATE.motivation_history)},
                                      ensure_ascii=False))
        while True:
            await ws.receive_text()  # ignore inbound, subscriber only
    except WebSocketDisconnect:
        pass
    except Exception:
        pass
    finally:
        STATE.motivation_subscribers.discard(ws)


# ── /ws/akida_ingest  (Pi spike streamer push) ───────────────────────────────
@app.websocket("/ws/akida_ingest")
async def ws_akida_ingest(ws: WebSocket):
    await ws.accept()
    log.info("akida ingest connected")
    try:
        while True:
            raw = await ws.receive_text()
            try:
                msg = json.loads(raw)
            except Exception as e:
                log.warning("akida ingest json drop: %s raw=%r", e, raw[:200])
                continue
            STATE.akida_history.append(msg)
            # fan-out to akida subscribers
            dead = []
            for sub in STATE.akida_subscribers:
                try:
                    await sub.send_text(raw)
                except Exception:
                    dead.append(sub)
            for d in dead:
                STATE.akida_subscribers.discard(d)
    except WebSocketDisconnect:
        pass
    except Exception as e:
        log.warning("akida ingest error: %s", e)
    finally:
        log.info("akida ingest disconnected")


# ── /ws/akida  (frontend akida subscriber) ───────────────────────────────────
@app.websocket("/ws/akida")
async def ws_akida(ws: WebSocket):
    await ws.accept()
    STATE.akida_subscribers.add(ws)
    try:
        await ws.send_text(json.dumps({"type": "akida_history",
                                       "list": list(STATE.akida_history)},
                                      ensure_ascii=False))
        while True:
            await ws.receive_text()
    except WebSocketDisconnect:
        pass
    except Exception:
        pass
    finally:
        STATE.akida_subscribers.discard(ws)


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", "8000"))
    host = os.environ.get("HOST", "0.0.0.0")
    log.info("broker starting on %s:%d  static=%s", host, port, STATIC_DIR)
    uvicorn.run(app, host=host, port=port, log_level="info")
