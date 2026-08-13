# R4 dialogue-support scale ladder — 2026-08-13

Status: **COMPLETE — FAIL-DIALOGUE-SUPPORT-SCALE**.

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

All three registered arms completed locally on deterministic CPU with two threads. Increasing
support improved held-out assistant CE monotonically from the 100-document control `5.00458` to
`2.36451`, `1.82383` and `1.75553` at 500, 1,500 and 3,500 documents. Broad validation CE stayed
below uniform at `1.99803`, `1.86849` and `1.82543`.

That teacher-forced improvement did not become meaningful free generation. The three arms scored
semantic `0/7`; structural scores were `1/7`, `0/7`, `0/7`; memory and correction both failed.
The primary 3,500-document endpoint produced repeated `store/start` phrases, while its fixed
training probe reached only teacher top-1 `0.55216` and target-prefix `0/8`. The bounded conclusion
is therefore that more unique dialogue at the same 15,000-row compute improves held-out prediction
but is insufficient for this mouth's free conversation. It does not yet distinguish insufficient
optimization exposure from insufficient capacity.

Raw responses, logs, summaries, `.bin` engines and exact-resume `.pt` files are preserved only in
private HF revision
`dancinlab/anima-303m-r4-dialogue-scale-2026-08-13@1146240912244c7127b442196e2047a6f7641eac`.
An independent download verified all 27 registered artifacts (`45,959,357` bytes) with zero SHA-256
mismatches. The first upload's custody manifest failed closed because it used absolute paths and
hashed itself before writing; revision `114624...` contains the corrected relative, self-excluding
manifest. The models themselves were unchanged.

The next allowed result-bearing axis is a separately preregistered 3,500-document
optimization-exposure test. Another 303M run, IIT-mouth coupling, participant mounting and
production remain blocked.
