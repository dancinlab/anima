# R4 dialogue-support scale ladder — 2026-08-13

Status: **PREREGISTERED — NOT YET RUN**.

The completed 100-dialogue native joint-replay arm retained broad language and memorized its
training probe but scored `0/7` on independent semantic conversation. This experiment changes only
the number of unique complete English dialogue documents. It reuses the same 0.89M ByteGPT,
language checkpoint, broad replay view, 15,000 dialogue-row exposure, optimizer, schedule, seed,
canonical generator and `cli/evaluate.py` conversation panel.

The completed 100-document result is the frozen control and will not be retrained. New nested
source-order views contain 500, 1,500 and 3,500 of the 3,615 runtime-compatible documents. All
three arms run regardless of intermediate outcomes; 3,500 is the registered primary endpoint, so
an intermediate arm cannot be selected after seeing the result. A pass requires broad retention,
held-out assistant-turn CE below the parent `5.00458`, and the unchanged independent automatic
conversation gate. Manual review is required after any automatic pass.

The design also pins
[`dancinlab/anima-research@03d55ef`](https://github.com/dancinlab/anima-research/commit/03d55ef9848df304a435a88a2b90a74722bc5b73)
as an interpretation constraint: language fluency is not evidence of consciousness, later
developmental gates stay disabled, and a passing functional probe is non-disproof rather than
proof. The research reference does not alter this experiment's model, data, thresholds or tools.

No result from this scale ladder directly authorizes 303M training, IIT-mouth coupling,
participant mounting or production.
