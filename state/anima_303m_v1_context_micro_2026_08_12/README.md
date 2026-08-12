# 303M V1 context-length micro experiment — 2026-08-12

Status: **PREREGISTERED — NOT YET RUN**.

R3 proves that the IIT daemon's final state can select one of two exact bounded utterances. It is
not a learned mouth. R4 therefore remains blocked on an independently trained model that can hold
meaningful English conversation before any IIT state is allowed to affect free generation.

The immediately preceding V0/V2 micro run found that the existing trainer, serializer and
canonical generator can exactly learn one complete exchange, but both matched tiny arms collapse
on 100 exchanges. It also measured that 15,114 of 24,239 valid OpenAssistant targets cannot fit
their final complete prompt/response pair in 513 bytes. A further 303M run at the same block length
is prohibited.

V1 changes only causal context length. The fixed source, eligibility, official split, canonical
chat format, greedy decode, optimizer family, seed and total target-byte budget are unchanged.
The source census is performed at 513, 1025 and 2049 serialized bytes. Exact documents are
deduplicated, SHA-ordered, panel-decontaminated and checked for split overlap before training.

The matched short-view comparison trains the same existing ByteGPT configuration on the same 100
documents at block 512 and block 2048. Batch sizes 8 and 2 keep 4,096 target bytes per step. A third
2048 arm uses 100 preregistered long documents that cannot enter the 512 arm. No new trainer,
decoder or evaluator is introduced; training runs through `cli/train.py`, generation through
`core.generator`, and structural scoring through the existing conversation evaluator.

Promotion is fail-closed. The 2048 census must preserve at least 90% of valid targets. The short
2048 arm must outperform the 512 control and recover at least six of eight registered response
prefixes; the long arm must meet the same 6/8 recovery bar. Every arm must descend on held-out CE,
and both 2048 arms must emit at least six distinct, non-empty, structurally valid replies. Failure
forbids a 303M run, IIT-mouth coupling and production deployment. Exact hashes, bars and stop rules
are frozen in `protocol.json`; results will be appended without changing them.
