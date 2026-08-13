# R4 runtime-compatible document alignment — 2026-08-13

Status: **COMPLETED — SUPPORTED-DOCUMENT-ALIGNED-CONDITIONAL-LEARNING**.

The prior alignment arm learned all four gold conditionals, but its exact gate was unreachable
because three answers exceeded the canonical 192-byte generation budget. This protocol keeps the
immutable HF source revision and derives a new view without reading model outcomes: scan source
documents in order, retain complete single user-assistant exchanges whose UTF-8 response length is
at most `core.generator.CHAT_MAX_NEW_BYTES`, and take the first four. The frozen response lengths
are 163, 48, 44 and 66 bytes and the view SHA-256 is in `protocol.json`.

The existing document-aligned sampler, deterministic two-thread CPU path, model, seed, objective,
optimizer, 600-step endpoint, canonical decoder and gates remain fixed. The exact gate now has a
preflight proof of reachability and still requires teacher top-1 `>=0.95`, exact/target/structural
`4/4`, and prompt causal control `4/4`.

This is a local memorization/conditioning gate, not heldout meaningful conversation. It cannot
authorize 303M, IIT-mouth coupling, participant mounting or production. Vast.ai is forbidden and
the user files remain untouched.

## Result

The single treatment passed every registered bar. All four target responses were reachable within
the canonical 192-byte budget; teacher top-1 was `1.0000`, teacher CE `0.00000132`, exact response,
target-prefix and structural generation were each `4/4`, prompt CE/output controls were each `4/4`,
and all four generations stopped on the supervised canonical role boundary.

The verdict is `SUPPORTED-DOCUMENT-ALIGNED-CONDITIONAL-LEARNING`. Together with the failed stream,
horizon and capacity controls, this supports the shared train-to-runtime position map as the first
four-document root cause and rejects uniform tiny capacity as its explanation. It remains an
in-view memorization result. A 100-document and independent-panel experiment must be separately
preregistered before any 303M, IIT-mouth, participant or production action.
