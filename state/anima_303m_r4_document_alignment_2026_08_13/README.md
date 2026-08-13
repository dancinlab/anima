# R4 document-aligned chat sampling — 2026-08-13

Status: **PREREGISTERED — NOT YET RUN**.

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
