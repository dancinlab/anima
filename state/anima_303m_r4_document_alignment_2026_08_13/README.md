# R4 document-aligned chat sampling — 2026-08-13

Status: **COMPLETED — INVALID-GATE-UNREACHABLE**.

The deterministic horizon and capacity arms learned the first three documents but failed the
fourth from its first response byte. Legacy stream framing guarantees document visibility but not
runtime position identity: the EOF document can occur only near position 222 in a 512-byte stream
window, while canonical isolated chat begins its user role at position zero.

This single-axis treatment uses the shared ByteCell sampler's document-aligned mode. It selects the
same complete document, places its canonical `user:` prefix at position zero, then fills the fixed
block with following corpus bytes, wrapping only after EOF. Model, four documents, seed, objective,
optimizer, 600-step horizon, decoder and gates remain fixed. The existing stream behavior remains
available as the frozen parent control.

The treatment must reach teacher top-1 `>=0.95`, exact/target/structural `4/4` and prompt causal
control `4/4`. It is only a memorization/conditioning diagnosis and cannot authorize 303M,
IIT-mouth coupling, participant mounting or production. No Vast.ai instance is allowed and the two
user files remain untouched.

## Result

Document alignment removed the observed conditional-learning failure: teacher top-1 was `1.0000`
on all four documents, target-prefix recovery was `4/4`, and both prompt CE/output interventions
were controlled `4/4`. The original exact/structural gate still read `1/4` and emitted
`FALSIFIED-DOCUMENT-ALIGNMENT-TREATMENT`.

That verdict is not interpretable. Three registered targets are 230, 304 and 256 bytes, while the
canonical generator is limited to 192 new bytes, so exact completion and a stop boundary were
unreachable before any model ran. `result.json` preserves the emitted verdict as
`original_verdict` and classifies the experiment `INVALID-GATE-UNREACHABLE`; thresholds were not
relaxed and the result was not promoted to pass.

The shared harness now exposes gate reachability, and the next separately preregistered view uses
the deterministic rule “first four complete single-turn documents whose response fits the
canonical byte budget.” The immutable source revision remains unchanged. All scale-up, IIT and
production gates remain blocked.
