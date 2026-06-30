# agent/domains/CHAT — folder guide (py↔hexa porting SSOT)

The CHAT domain = the serving lane where anima attaches to the broker as a substrate-native chat participant
(FIRST-PACK Phase 3·5). Every `.py` file has a 1:1 `.hexa` sidecar, and the sidecar header
records each file's **porting verdict** (full port | WRAPPER-kept).

## Porting policy (audit-first · no forced porting)

`agent/` hexa-unification ports to hexa **only reducible pure logic**, while bindings to external py-only
SDKs (torch/transformers/peft/akida MetaTF/fastapi/uvicorn/websockets) are
**preserved as-is** — same as the `serialize` torch-interop precedent (irreducible interop = kept).

### (a) full hexa-native port (py deleted, git-preserved)

| original py (deleted) | hexa port | rationale |
|---|---|---|
| `anima_emission_analyze.py` | `anima_emission_analyze.hexa` | pure stdlib (re·statistics·urllib·log parsing) → has_register marker·analyze_log·analyze_history all hexa-native. behavior parity confirmed (analyze_log byte-identical: n_emit=3·self_mono=0.667·score_mean=0.527). curl/awk are leaf op exec. |

### (b) irreducible py (KEPT — external SDK interop, no hexa equivalent)

torch/akida SDK bindings can't be hexa — honestly preserved. Each sidecar `.hexa` records the kept verdict
via a WRAPPER marker (exec dispatch or doc-stub).

| kept py | external dependency | sidecar .hexa role |
|---|---|---|
| `anima_participant.py` | torch·transformers·peft·websockets | WRAPPER exec dispatch (the 8-factor motivation SSOT is HEXAD spontaneous_lib.hexa) |
| `broker.py` | fastapi·uvicorn·starlette·websockets·langdetect | WRAPPER exec dispatch (ASGI server) |
| `substrate_base.py` | torch (typed ABC) | doc-stub (import-only ABC, no standalone execution) |
| `substrate_lora.py` | torch·transformers·peft·safetensors | doc-stub (production-default LoRA substrate) |
| `substrate_v3.py` | torch·transformers | doc-stub (ConsciousDecoderV3 research substrate) |
| `substrate_akida.py` | akida MetaTF SDK·numpy·torch | doc-stub (AKD1000 HW + numpy-LIF SW fallback) |
| `akida_sw_lif.py` | numpy | doc-stub (numpy LIF simulator, substrate_akida SW path) |
| `anima_temp_sweep.py` | torch·transformers·peft | WRAPPER exec dispatch (Qwen2.5-1.5B+LoRA generate sweep) |

### (c) test/probe py (KEPT — external SDK dependency)

| kept py | external dependency | sidecar .hexa |
|---|---|---|
| `test_broker_multiuser.py` | websockets (needs live broker) | WRAPPER exec dispatch |
| `test_broker_akida_ingest.py` | fastapi.testclient + broker.py | no sidecar (in-process regression guard, broker app import) |

## Invariants

- A new `.py` is added only when it's external py-SDK interop, accompanied by a sidecar `.hexa` WRAPPER marker.
- Pure logic (no external SDK dependency) is authored as `.hexa` from the start, not `.py`.
- akida MetaTF / torch SDK have no hexa equivalent, so no forced porting (honest preservation).
