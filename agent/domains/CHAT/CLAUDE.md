# agent/domains/CHAT — 폴더 가이드 (py↔hexa 포팅 SSOT)

CHAT 도메인 = anima 가 substrate-native chat participant 로 broker 에 붙는 serving lane
(FIRST-PACK Phase 3·5). 모든 `.py` 파일은 1:1 `.hexa` sidecar 를 가지며, sidecar 헤더가
각 파일의 **포팅 verdict**(full port | WRAPPER-kept)를 박제한다.

## 포팅 정책 (audit-first · 무리 포팅 금지)

`agent/` hexa-단일화는 **환원가능한 순수 로직만** hexa 로 포팅하고, 외부 py-전용
SDK(torch/transformers/peft/akida MetaTF/fastapi/uvicorn/websockets) 바인딩은
**그대로 보존**한다 — `serialize` torch-interop 선례와 동일(환원불가 interop = kept).

### (a) full hexa-native port (py 삭제됨, git 보존)

| 원 py (삭제) | hexa 포팅 | 근거 |
|---|---|---|
| `anima_emission_analyze.py` | `anima_emission_analyze.hexa` | 순수 stdlib(re·statistics·urllib·로그파싱) → has_register 마커·analyze_log·analyze_history 전부 hexa-native. behavior parity 확인(analyze_log byte-identical: n_emit=3·self_mono=0.667·score_mean=0.527). curl/awk 는 leaf op exec. |

### (b) 환원불가 py (KEPT — 외부 SDK interop, hexa 등가물 없음)

torch/akida SDK 바인딩은 hexa 불가 — 정직 보존. 각 sidecar `.hexa` 가 WRAPPER 마커
(exec dispatch 또는 doc-stub)로 kept verdict 를 기록한다.

| kept py | 외부 의존 | sidecar .hexa 역할 |
|---|---|---|
| `anima_participant.py` | torch·transformers·peft·websockets | WRAPPER exec dispatch (8-factor motivation 은 HEXAD spontaneous_lib.hexa 가 SSOT) |
| `broker.py` | fastapi·uvicorn·starlette·websockets·langdetect | WRAPPER exec dispatch (ASGI 서버) |
| `substrate_base.py` | torch (typed ABC) | doc-stub (import-only ABC, standalone 실행 없음) |
| `substrate_lora.py` | torch·transformers·peft·safetensors | doc-stub (production-default LoRA substrate) |
| `substrate_v3.py` | torch·transformers | doc-stub (ConsciousDecoderV3 research substrate) |
| `substrate_akida.py` | akida MetaTF SDK·numpy·torch | doc-stub (AKD1000 HW + numpy-LIF SW fallback) |
| `akida_sw_lif.py` | numpy | doc-stub (numpy LIF 시뮬레이터, substrate_akida SW path) |
| `anima_temp_sweep.py` | torch·transformers·peft | WRAPPER exec dispatch (Qwen2.5-1.5B+LoRA generate sweep) |

### (c) test/probe py (KEPT — 외부 SDK 의존)

| kept py | 외부 의존 | sidecar .hexa |
|---|---|---|
| `test_broker_multiuser.py` | websockets (live broker 필요) | WRAPPER exec dispatch |
| `test_broker_akida_ingest.py` | fastapi.testclient + broker.py | sidecar 없음 (in-process 회귀 가드, broker app import) |

## 불변식

- 새 `.py` 추가 = 반드시 외부 py-SDK interop 일 때만, sidecar `.hexa` WRAPPER 마커 동반.
- 순수 로직(외부 SDK 무의존)은 `.py` 가 아니라 처음부터 `.hexa` 로 저작.
- akida MetaTF / torch SDK 는 hexa 등가물이 없으므로 무리 포팅 금지(정직 보존).
