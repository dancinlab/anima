# R4 runtime-compatible document alignment — 2026-08-13

Status: **PREREGISTERED — NOT YET RUN**.

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
