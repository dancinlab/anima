# Compose-2 CLMConvMoE 7B chat-staging serving gate — 2026-08-11

Status: PRE-REGISTERED — execution pending.

This gate follows `state/store_causality_7b_longrun_2026_08_10`. It reuses the live chat
participant boundary (`agent/domains/CHAT/anima_participant.py`), its existing `Substrate`
interface, the broker's HTTP/WebSocket routes, and the canonical CLM decode implementation in
`core/decode.py`. It does not add an engine, evaluator, model format, chat trigger, prompt, corpus,
or scoring path. User messages remain environment input; model generation remains self-tick driven.

## Frozen inputs and deployment boundary

- source baseline: Git commit `5f8142c6c`
- model: private HF repository
  `dancinlab/anima-store-causality-7b-longrun-2026-08-10`, artifact commit
  `0e26f4623c514bc6192a93f14e7a466a6f8bd59a`, final `.clm` SHA-256
  `0e4ff48cbba04ac49f1f005350a9c51a74de87393c35c20551b9374a1a2c9b04`
- model and training data remain HF-only under `dancinlab`; the model may exist only in ephemeral
  Vast.ai scratch/cache during this run and is deleted at teardown
- all model loading, inference, load, and soak work runs on Vast.ai, never on mini
- staging uses a private/local broker on the rented instance; it must not replace the current
  participant at `chat.dancinlab.org` or change production DNS
- the existing broker contract remains `GET /health`, user `WS /ws`, and participant
  `WS /ws/anima`; no request-response generation endpoint is introduced
- `ING.jsonl` and `stream_mi.json` remain untouched

The implementation may add only a CLM-backed implementation of the existing `Substrate` interface
and select it through the existing `--substrate` option. It must use `core/decode.py` weight loading,
forward taps, and sampled decode. Invalid byte sequences are converted to standard Unicode
replacement characters only at the WebSocket text boundary so JSON/WebSocket encoding cannot fail;
the engine output itself is not rewritten or prompted.

## Fixed serving bars

No result-dependent retry, checkpoint substitution, decode-bar change, or threshold adjustment is
allowed. Infrastructure failure may be rerun only with the same inputs and bars.

1. cold model load and participant readiness: at most 300 seconds;
2. HTTP `/health`: status 200 and p95 at most 250 ms over at least 100 requests;
3. WebSocket broker broadcast: correct two-user + participant fan-out and p95 at most 500 ms over
   at least 100 frames;
4. 7B generation: at least 2.0 emitted bytes/s and p95 generation wall at most 45 seconds over at
   least 20 fixed 32-byte emissions after warm-up;
5. serving peak VRAM: at most 70 GiB on an 80 GiB GPU;
6. soak: at least 30 minutes, no participant/broker crash or reconnect loss, no failed HTTP/WS
   probe, and warm-to-end host-RSS and GPU-memory growth each at most 5%;
7. rollback: stop the CLM participant, observe `anima_alive=false`, start the pre-existing AKIDA
   software-fallback substrate without changing broker code, recover `anima_alive=true`, and pass
   HTTP/WS probes within 120 seconds.

Chat output is not approved from transport health alone. The unchanged canonical `ρ·form` reach
measurement in `anima-py evaluate` must also pass its existing frozen coherence bar (at least four
of five continuations at KWR 0.50 or above). This is recorded as a production gate, not replaced by
a new serving scorer. A `ρ·form` failure blocks production but does not suppress the transport and
performance measurements needed to diagnose the staging runtime.

The 7B causal instrument is checked once before serving measurements using the existing
`anima-py evaluate --store-causality` path. Pair-oracle below 0.90 stops the run before serving
interpretation. A passing pair-oracle does not rerun or reinterpret the already closed causal
battery.

## Production decision

Every functional, performance, soak, rollback, and existing `ρ·form` bar must pass before production
can be approved.
Failure is recorded unchanged in this README and `result.json`; production remains blocked. The
production LaunchAgent and `https://chat.dancinlab.org` are restarted or changed only after a
separate explicit production approval. This staging gate itself ends by deleting the Vast.ai
instance and its ephemeral HF cache.
