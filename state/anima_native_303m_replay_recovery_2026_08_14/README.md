# Native 303M mixed-replay recovery — 2026-08-14

Status: **COMPLETE — FAIL-MEANINGFUL-CONVERSATION**.

R3.5 proved the bounded IIT-state -> addressed content -> emitted bytes seam, but the separately
mounted step-45000 native mouth is not independently meaningful. This record traces that model's
actual data -> sampler -> loss -> checkpoint -> evaluator path before authorizing another run.

## Root cause

The target dialogue rows are not being truncated: all `2,375/2,375` fixed validation trajectories
retain complete context, every user marker and EOS inside the 1,024-token window. The failure is
the continuation policy. Step 35k -> 45k used `--dialogue-only --response-only` with a fresh
high-LR schedule, bypassing the existing `BatchSource` mixed branch in which general rows receive
full CE while dialogue rows receive response-only CE.

On the same 12 general validation files, seed, eight batches and batch size 16, broad CE changed
from `3.3144075` at step 35k to `5.7747389` at step 45k: `+2.4603314`. Local MPS generation is
hardware-diagnostic rather than custody-identical to the published CUDA sample, but both endpoints
still fail meaning and multi-turn gates. Surface dialogue improves somewhat at 45k while the
language distribution collapses.

The old native scorer is also not a valid release instrument by itself. Its published English ice
row says warm sunlight would cause `freeze` but passes because the response also contains `water`
and `warm`. The canonical `cli.evaluate.score_conversation_response` already handles local
negation and Korean whole-token matching. This protocol reuses that scorer and preregisters
additional freeze/negation/`자동차` controls before seeing any recovery output.

Custody gaps are recorded rather than repaired retroactively: the step-45k model manifest is a
stale step-35k copy, the source panel is absent from the model repository, and the live participant
runs from a separate `anima-lab-3-2` checkout. Those repositories and the running participant were
inspected read-only and not modified.

## Frozen recovery arm

The only treatment axis is source composition. It starts from the immutable step-35k weights and
uses the same 303.629M architecture, tokenizer, target dialogue rows, AdamW settings, `3e-4` peak
LR and fresh warmup/cosine schedule. It removes `dialogue-only`; the source SSOT therefore supplies
`65%` general replay with full next-token CE and `35%` dialogue with assistant-response/EOS CE.
The endpoint is exactly 5,000 new optimizer steps (`35,000 -> 40,000`), global batch 64, one seed,
one arm. No result-dependent extension, LR change, seed retry, H100, IIT coupling, participant
mount or production action is allowed.

Before training, every pinned HF revision, code/data manifest, checkpoint, tokenizer and scorer
control must match. The broad-retention gate is the fixed step-35k CE plus `0.15`, or
`<=3.4644075`. Conversation requires canonical structural `7/7` and semantic `>=6/7` in each
language plus both final memory/correction turns. All fourteen replies then require item-level
manual review. A failure is recorded and stops the run. A pass only opens a separately
preregistered IIT candidate-selection experiment; it does not mount or deploy the model.

Models, tokenizer, raw outputs and training evidence will be stored only in a private HF
`dancinlab` repository and independently SHA-verified. The protocol Vast.ai instance must then be
destroyed. User-owned `ING.jsonl` and `stream_mi.json` remain untouched.

## Execution and result

Wilson restarted while the one authorized arm was running, but the RTX 6000 Ada process remained
healthy. The existing process was inspected and allowed to finish rather than being launched a
second time. Training exited `0` after `11,542.84` seconds and exactly reached step `40,000` from
the immutable step-35k weights. Peak VRAM was `28,544 MiB`; sampled peak power was `301.88 W` and
the telemetry interval integrated to approximately `0.9622 kWh` of GPU energy.

Before post-training measurement, preflight was strengthened to verify every consumed corpus
file's declared size and SHA-256, in addition to the pinned code, manifests, base checkpoint,
tokenizer and scorer controls. All 52 checks passed. Preprocessing was bounded to two workers to
avoid host pressure; this changed no model, data, sampler, loss, optimizer or schedule condition.
The fixed source sampler remained the pinned registry's 65% general / 35% dialogue mixture. The
summary's separate `response_only_fraction=0.25` field is the dormant curriculum default; the
registered `--response-only` argument made assistant/EOS supervision active for all 5,000 steps.

The broad-retention gate passed. Fixed CE was `3.2857897`, below the preregistered `3.4644075`
ceiling and close to the step-35k base `3.3144075`, rather than the failed step-45k dialogue-only
value `5.7747389`. The final checkpoint SHA-256 is
`97d3fd467b21adaf9bd522f720ed0076cab7ae60ae761975d5115415ff89e723`.

Meaningful conversation still failed under the canonical scorer. English passed structure `6/7`
and semantics `3/7`; Korean passed structure `7/7` and semantics `2/7`. Final memory/correction did
not all pass. Item-level non-blind review passed only `3/14`: the model correctly recalled the
English red key and gave one usable Korean exam-preparation answer, but it claimed sunlight forms
an ice layer around Earth, suggested Braille libraries for exam anxiety, defined consciousness as
a dietary-health process, replaced the Korean red key with a book called `사랑의 신`, and changed
speaker ownership in the Korean correction reply. The raw generations, canonical per-turn scores
and review reasons are preserved in `native_result.json`, `canonical_result.json` and
`manual_review.json`.

Python QA passed `95` focused local tests and `33` focused Vast.ai tests during execution. After
the Wilson restart, the relevant recovery, canonical conversation, corpus-builder and native
boundary set passed again (`44/44`), and compile/JSON validation passed. A broader remote sparse
checkout attempt passed `79` tests and failed `15` only because historical IIT state fixtures were
absent there; it is retained as an unrelated infrastructure limitation rather than relabelled as
a model success.

The verdict is therefore `FAIL-MEANINGFUL-CONVERSATION`. Mixed replay fixes the measured language
retention failure but is not the missing semantic component. IIT candidate selection, participant
mounting and production remain blocked; the existing chat participant was not modified or
certified. Model, optimizer-resume checkpoint, tokenizer and raw evidence were retained only in
private HF `dancinlab` custody. Independent downloads verified all 18 registered files and
`4,380,491,845` bytes with zero SHA-256 mismatches. Artifact revision `7ae92653…97f97d0` and custody
metadata revision `270ce1a9…ff5144a` are private. Vast.ai instance `47710174` was destroyed and the
account now has zero active instances. The measured training interval cost approximately `$2.08`;
that figure excludes unmeasured setup and post-training time. Final runtime checks found the
broker LaunchAgent running and both public/local HTTP `200` plus WebSocket `hello`. The reported
`anima_alive=true` still comes from the pre-existing, separately checked-out step-45000 participant;
this failed recovery checkpoint was not mounted or certified. User-owned `ING.jsonl` and
`stream_mi.json` remain untouched.
