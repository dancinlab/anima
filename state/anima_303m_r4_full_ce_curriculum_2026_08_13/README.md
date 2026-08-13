# R4 full-CE → aligned turn-SFT curriculum — 2026-08-13

Status: **COMPLETE — FAIL-CURRICULUM-MEANINGFUL-CONVERSATION**.

The aligned 100-document response-only model now memorizes its registered training probe exactly
but scores semantic `0/7` on the unchanged independent panel. This one-arm local Python experiment
changes only the missing language-formation phase: the existing tiny ByteGPT first receives full
next-byte CE on a fixed 1 MiB view of the immutable private English-general HF corpus, then the
unchanged 100-dialogue document-aligned turn-only phase warm-starts from that fixed engine.

Both source revisions, byte ranges, derived SHA-256 values, optimizer schedules, endpoints, seed,
model, decoder, heldout dialogue view, panel and decision table are frozen in `protocol.json`.
The response-only 1,875-step result is the preserved control; there is no fresh control arm and no
post-hoc checkpoint choice. Failure at any gate remains a recorded failure. An automatic panel
pass still requires manual review and cannot directly authorize 303M, IIT coupling, participant
mounting, or production.

The full-CE language phase passed its registered descent gate with fixed broad validation CE
`2.25960`, top-1 `0.34421`, versus uniform CE `5.54518`. The unchanged aligned turn phase again
memorized the first eight dialogue probes exactly: teacher top-1 `1.0000`, exact/target/structural
`8/8`, and prompt controls `8/8`.

Independent behavior still failed. Heldout dialogue assistant CE was `7.12117`, semantic items were
`0/7`, structural items `6/7`, and memory/correction failed. More importantly, the same broad
validation CE degraded from `2.25960` before SFT to `7.11936` after SFT. Thus this bounded run
supports catastrophic forgetting in the high-LR turn phase rather than failure of the preceding
language phase. Outputs remain meaningless fragments, so no manual review or upper gate is opened.
The next separately preregistered arm changes only turn-phase peak LR from `1e-3` to `1e-4`, reuses
the exact language checkpoint, and retains the endpoint, data, objective, sampler, seed and gates.
