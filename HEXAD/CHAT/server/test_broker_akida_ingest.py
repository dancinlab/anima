#!/usr/bin/env python3
"""Akida ingest falsifier (inbox PR #203) — feed a sample pi5 spike_streamer
JSON frame through the live /ws/akida_ingest handler and assert it surfaces in
GET /akida/recent.

This pins the deque wiring the PR #203 patch interrogated: the ingest handler
MUST append parsed frames to the SAME STATE.akida_history deque that
/akida/recent serves. Source review already FALSIFIED hypotheses (a)/(b)/(c)/(d)
at broker.py; this test makes that wiring a regression guard.

Run:  python3 HEXAD/CHAT/server/test_broker_akida_ingest.py
Needs: fastapi[testclient] (TestClient drives the WS + GET in-process, no live
       server / no network).
"""
import json, sys
from fastapi.testclient import TestClient

# import the broker app in-process
sys.path.insert(0, __file__.rsplit("/", 1)[0])
import broker  # noqa: E402

# sample pi5 spike_streamer frame (exact format from the inbox patch)
PI5_FRAME = {
    "t_rel": 20511.83,
    "step": 204741,
    "n_spikes": 8,
    "spike_ids": [3, 17, 42, 88, 101, 150, 199, 233],
    "regime": "R3_tonic_zero_input",
    "thr": [0.1, 0.2, 0.3],
}


def main() -> int:
    # fresh deque so the assertion is not polluted by prior state
    broker.STATE.akida_history.clear()
    client = TestClient(broker.app)

    # 1) push a frame through the ingest WS handler
    with client.websocket_connect("/ws/akida_ingest") as ws:
        ws.send_text(json.dumps(PI5_FRAME))
        # second frame to confirm append accumulates (not clobber)
        ws.send_text(json.dumps({**PI5_FRAME, "step": 204742}))
        ws.close()

    # 2) read it back via the GET endpoint (must be the SAME deque)
    resp = client.get("/akida/recent")
    body = resp.json()
    recent = body.get("akida", [])

    print(json.dumps({"recent_len": len(recent),
                      "first": recent[0] if recent else None}, ensure_ascii=False, indent=2))

    checks = {
        "ingest_reaches_deque": len(recent) == 2,                       # (a) not no-op
        "same_deque_read": len(recent) > 0,                             # (b) same object
        "frame_fields_preserved": bool(recent) and recent[0].get("spike_ids") == PI5_FRAME["spike_ids"]
                                  and recent[0].get("regime") == PI5_FRAME["regime"],  # (c) JSON parsed
        "ts_normalized": bool(recent) and "ts" in recent[0],           # ts surfaced for consumers
        "maxlen_nonzero": broker.STATE.akida_history.maxlen and broker.STATE.akida_history.maxlen > 0,  # (d)
    }
    for k, v in checks.items():
        print(f"  {'PASS' if v else 'FAIL'}  {k}")

    ok = all(checks.values())
    print("AKIDA_INGEST_DEQUE_PASS" if ok else "AKIDA_INGEST_DEQUE_FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
