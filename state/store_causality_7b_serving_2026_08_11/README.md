# Compose-2 CLMConvMoE 7B chat-staging serving gate — 2026-08-11

Status: COMPLETE — serving mechanics passed; production blocked by canonical `ρ·form` failure.

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

## Implementation and actual call flow

The existing participant now selects `CLMSubstrate` through `build_substrate("clm")`. Each emission
continues through `CLMSubstrate.generate` → `core/decode.py::clm_decode_argmax` → the canonical
CLMConvMoE forward; broker routing remains the existing `/ws/anima` broadcast path. No request-
response endpoint, prompt, engine, evaluator, or model format was added.

The first real 7B load exposed the common loader's scale failure: every int4 block was expanded
through full-size int64 and float64 intermediates, transposed with another copy, and only then moved
to CUDA. `core/decode.py` now decodes blocks in their production transposed orientation and
dequantizes directly into CUDA-owned arrays. Small-fixture block equality tests and the real H100
checkpoint verified that the canonical values and forward path are unchanged. The final runtime
source under test was `0688b29a4`.

## Execution result

The unchanged store-causality preflight returned pair-oracle `1.0000` and `SUPPORTED-CAUSAL`
(normal/recovery `0.8359375`; A removal `0.421875`; B removal `0.46875`; shuffle `0.4921875`).
The serving measurements then completed on one Vast.ai H100 SXM 80 GB:

- cold process-to-CLM-ready log interval: `8.07 s` (bar `≤300 s`);
- HTTP health: 100/100, p95 `1.111 ms` (bar `≤250 ms`);
- two-user + participant WebSocket fan-out: 100/100 to all three recipients, p95 `13.978 ms`
  (bar `≤500 ms`);
- canonical `CLMSubstrate.generate`: 20 fixed 32-byte emissions, p95 `11.677 s`, minimum
  `2.152 bytes/s`, mean `2.763 bytes/s` (bars `≤45 s`, `≥2.0 bytes/s`);
- peak serving VRAM: `54,801 MiB` (`53.52 GiB`, bar `≤70 GiB`);
- soak: `1,804.121 s`, 359 HTTP/WS probes, zero failures, HTTP/WS p95
  `3.606/21.024 ms`; warm-to-end RSS `862,044→862,716 KiB` (`+0.078%`) and GPU memory
  `54,801→54,801 MiB` (`0%`), both below the `5%` growth cap;
- rollback: CLM stop exposed `anima_alive=false`; the existing AKIDA numpy software fallback
  restored `anima_alive=true` in `1.350 s`, then passed the existing two-user broadcast probe
  (bar `≤120 s`).

The required canonical `ρ·form` measurement failed unchanged: form-rate `0.20` (one of five
continuations), self-shuffle `0.00`, frozen gate `0.70`. Therefore transport, performance, memory,
soak, and rollback pass, but the overall staging gate fails and production remains blocked. The
failure is generation coherence, not serving infrastructure; no retry, alternate checkpoint, or
threshold change was attempted.

H100 regression QA passed 16/16 across the int4 block loader, CLM substrate, store-causality
evaluator, and dual-address CLMS training/parity tests. The instance was deleted after measurement;
active Vast.ai rentals are zero, the delete-time estimated cost was `$3.4527`, and no model copy was
downloaded to mini. `ING.jsonl` and `stream_mi.json` remained untouched. Production DNS,
LaunchAgent, and `chat.dancinlab.org` were not changed because production was not approved.
The existing broker LaunchAgent remained running, and read-only live verification returned HTTP
200 plus a WebSocket `hello` frame through Cloudflare. Its pre-existing production participant was
not connected (`anima_alive=false`); this run did not replace or restart it because the production
gate failed.
