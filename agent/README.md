# anima agent runtime

`agent/` contains the Python chat-facing runtime for anima. It is not a separate package or
repository: the root `pyproject.toml`, shared `core/` engine, and root CI are the canonical
ownership and release surfaces.

## Active paths

- `domains/CHAT/broker.py` — FastAPI HTTP/WebSocket broker.
- `domains/CHAT/anima_participant.py` — autonomous participant and motivation flow.
- `domains/CHAT/substrate_*.py` — model/substrate adapters implementing `Substrate`.
- `domains/CHAT/akida_emit_bridge.py` — validated AKIDA spike co-gate.
- `domains/CHAT/anima_dream_stage.py` — direct Python sleep-stage context.
- `domains/CHAT/anima_imagination_loop.py` — emit-free replay through the shared Python engine.
- `dashboard/` — chat observability UI.

Install from the repository root:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -e ".[train,runtime,test]"
```

Run the local broker:

```bash
.venv/bin/python agent/domains/CHAT/broker.py
```

Run the participant only with an explicit model/checkpoint configuration appropriate to the
selected substrate. Model assets remain in private Hugging Face repositories under `dancinlab`;
credentials must come from the deployment secret environment and must not be committed.

## QA

```bash
.venv/bin/python -m pytest -q agent/domains/CHAT/test_*.py
.venv/bin/python -m compileall -q agent/domains/CHAT
```

Production GPU execution is deployed to Vast.ai. Local macOS broker management is documented in
`domains/CHAT/CHAT.md` and implemented by `scripts/deploy_local_chat.py`.
