# Native 303M mixed-replay recovery — 2026-08-14

Status: **PREREGISTERED — GPU arm not started**.

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
