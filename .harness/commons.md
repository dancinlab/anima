# anima — commons repo override

Anima-specific exceptions layered on the cross-project commons SSOT. Only the slugs listed here
override commons; every other commons rule still applies.

## preserve-state
- do: Keep the CONTENT not the file — findings/numbers/parity into the card body + `HYPOTHESES.jsonl`, verdicts into ARCHITECTURE gate nodes, volatile scratch to `/tmp` (`a_no_scatter_hypotheses_first`)
- dont: New writes under `state/` or `archive/state/` (read-only fossils · blocked by `H-NO-STATE-DIR` + G7) · a per-experiment scratch dir · only `state/verdicts/` excepted (`a_claim_verify`)
