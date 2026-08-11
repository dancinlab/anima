# 7B production conversation recovery — 2026-08-11

Status: COMPLETE — PRODUCTION CHAT RECOVERED.

The previous production gate proved synthetic compose-2 causality and byte-generation throughput,
but deployed that store-causality `.clm` as if it were a chat model. Live evidence falsified that
decision: Korean turns produced repetitive Spanish fragments or unrelated Korean sentences, an
English consciousness question received no attributable answer, and a later user's message could
replace the earlier question in the participant's single latest-message buffer.

## Root causes and correction

The traced production path was browser → broker → `AnimaState.m_buffer` → `emit()` → substrate →
broker. Four shared-path defects were corrected:

1. the broker and participant had no user-turn reply identity, so concurrent users overwrote one
   another; broker-issued user IDs now flow through a bounded FIFO ledger and every answer carries
   a broker-validated `reply_to`;
2. `ingest_user_msg()` inserted the current prompt embedding before `tick()` compared it, forcing
   self-similarity to 1 and `info_gap` to 0; the pending prompt is now compared with prior emissions;
3. `emit()` randomly selected an output language even for a pending user turn; the broker-detected
   language of that exact turn now reaches the existing substrate;
4. the 15-second refractory and adaptive peak intended to suppress autonomous self-monologues also
   suppressed queued conversation. Pending turns still pass the unchanged eight-factor motivation
   score and configured threshold, but do not inherit cooldown from unrelated autonomous speech.

The existing HF/LoRA substrate was extended rather than replaced. With no adapter present it uses
the model's canonical chat template with an empty system turn, preventing the model template's
default identity text while preserving the repository's `NO SYSTEM PROMPT` rule; existing LoRA
adapter routing retains its prior continuation path. Production
now uses the private HF `dancinlab/qwen2.5-7b-edge-uncensored` artifact at commit
`393b15fd8ce70c68ec3fb88e6a36b1d839265b68`, with `model.safetensors` SHA-256
`08e41efb77ae4af41c1b59c2c03d380d7bcc0f961654ef13b9ca9a0baa4b2827`.

## Verification

- Vast.ai H100 focused regression: 18/18 passed; local non-Torch regression: 6 passed, one Torch
  module skipped; syntax and diff checks passed.
- Public sequential WebSocket QA after the final no-system-prompt deployment: `한글 가능해?` →
  `네, 저는 한국어로 대화할 수 있습니다. 무엇을 도와드릴까요?` in 1.188 s;
  `What is consciousness?` → an English explanation grounded in awareness and subjective
  experience in 2.777 s.
- Two users queued before either answer: both answers carried their own broker-issued `reply_to`,
  passed language and semantic contracts, and completed in 1.102–3.290 s.
- Non-injecting public soak: 182.900 s, 34 HTTP/WebSocket probes, zero failures; HTTP p95
  285.577 ms and WebSocket ping p95 126.728 ms.
- The participant process was terminated deliberately twice while deploying the final runtime.
  The supervisor loaded new PIDs, public health returned `anima_alive=true`, and post-recovery
  semantic QA passed.
- Production model VRAM was 15,338 MiB. The local LaunchAgent broker was restarted because broker
  reply metadata changed; public HTTPS and WebSocket paths are live.

The prior throughput result remains valid only for CLM engine causality and throughput. Its
`PRODUCTION-DEPLOYED` chat verdict is retracted in that run's README/result JSON and superseded by
this record. `ING.jsonl` and `stream_mi.json` were not modified.

## Remaining issues

Public HTTP p95 during the short soak was 285.577 ms, above the earlier internal 250 ms serving
bar, although no request or WebSocket failed. The H100 rental remains active at approximately
`$2.3565/hour`; supervisor process recovery exists, but automatic host replacement and autoscaling
do not.
