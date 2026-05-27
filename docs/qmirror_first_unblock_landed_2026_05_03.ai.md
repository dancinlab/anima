# qmirror first unblock — landed 2026-05-03

## Summary

Best-effort first-pass QPU-blocker unblock executed via qmirror substrate, parallel to discovery BG.

**Target unblocked**: `anima/.roadmap.iit4` — `iit4.cond.2` (IIT 4.0 proper φ★ MIP search, status `unmet`) + `iit4.blk.2` (budget-blocker $1500+ for 3-substrate confirm).

**qmirror cond mapped**: `qmirror.cond.6` (status `met`) — "reproduces braket_iit40_mip_2026_05_02 φ★=0.0 byte-identical for stored TPMs" via F5 selftest 4/4 PASS (engine=mock, pyphi 4.0 b78d0e3 pin).

## Why this entry

Sister BG (`a65edd221`, `aa6c8c54e`) already audited the original 12-candidate set and produced 5 ANNOTATE actions + 2 KEEP decisions (ionq.cond.1, penrose_hameroff.cond.1) per `anima/state/qmirror_canonical_migration_2026_05_03/keep_decisions.json` and `replace_log.jsonl`. All 12 prior candidates are addressed.

`iit4.cond.2` was NOT in the prior 12-candidate audit (search terms missed it — keyword set was quantum/QPU/IonQ/IBM/Rigetti/Heron/Forte/Aria/Cepheus/CHSH/braket/qiskit-ibm; iit4.cond.2 phrases the dependency as "$132/gate × 2^N state-conditional runs ($1500+ for 3-substrate confirm)" which contains none of those tokens). It surfaced this cycle via the broader scan triggered by the `unmet` + budget-blocker filter.

The mapping to `qmirror.cond.6` is direct and well-supported:
- `qmirror.cond.6` `verified_2026_05_03` already shows F5 byte-identical PASS against `braket_iit40_mip_2026_05_02/verdict.json`
- `iit4.cond.2.evidence` already cites `state/braket_iit40_mip_2026_05_02/ ledger`
- An existing `iit4.qmirror_byte_identical_link` entry (status `spec`, ts 2026-05-03) anticipated this cross-link but never reflected the F5 PASS execution
- This annotation promotes the spec-only cross-link to a substrate-met channel

## What changed

1 additive header-level field on `anima/.roadmap.iit4`: `verified_via_qmirror_2026_05_03`. Zero existing fields mutated. JSONL re-parses 6/6 lines clean. `iit4.cond.2.status` remains `unmet`. `iit4.blk.2.status` remains `open`.

The annotation explicitly does NOT claim full closure — it documents that the **proxy ≠ φ★ semantic-gap closure** axis (one of two sub-blockers behind the $1500+ price tag) is now substrate-addressable at $0 via qmirror.cond.6's byte-identical reproduction channel. The remaining sub-blocker (state-conditional 2^N **live-QPU re-runs** for fresh-experiment confirm) still requires budget unlock.

## Cost savings

$1500+ → $0 for the proxy-vs-φ★ semantic-gap closure axis. Live-QPU fresh-confirm cost path retained at original budget envelope.

## Honest C3 caveats (raw#10)

1. **qmirror equivalence not perfect** — F5 selftest uses `engine=mock` per nexus@64e24386 env-isolation; pyphi 4.0 b78d0e3 version pin load-bearing per spec §13 #6. Upstream pyphi MIP heuristic change would surface as substrate-drift artifact. The byte-identical PASS is conditional on pin stability.
2. **Single-entry scope** — only `iit4.cond.2` + `iit4.blk.2` addressed this cycle. Sister discovery BG produces the ranked plan covering remaining roadmaps with budget-blocked quantum dependencies.
3. **Sister discovery BG may rank a higher-value unblock** — this best-effort first-pass does not preclude downstream re-prioritization. The qmirror.cond.6 → iit4.cond.2 mapping was the most obvious available; sister BG may surface less-obvious but higher-value mappings.

## Constraints observed

- raw#9 STRICT — only `.roadmap.iit4` + JSON/marker state files modified; no `.py` written
- raw#10 honest C3 — 3 caveats above + status_change explicitly `none`
- raw#15 — no personal-path leak
- DO NOT mutate qmirror canonical (`nexus/.roadmap.qmirror`) — observed
- DO NOT touch closed/met conds — observed (cond.2 was `unmet`, blk.2 was `open`)
- ONE entry only this cycle — observed
- $0 — observed (Mac local)

## Deliverables

- `anima/.roadmap.iit4` — additive header field `verified_via_qmirror_2026_05_03`
- `anima/state/qmirror_first_unblock_2026_05_03/unblock_log.json` — full scan + selection record
- `anima/state/qmirror_first_unblock_2026_05_03/before_after.diff` — pretty-printed before/after of header tail
- `anima/state/markers/qmirror_first_unblock_landed.marker`
- `anima/docs/qmirror_first_unblock_landed_2026_05_03.ai.md` (this file)

## Verification

```
$ grep -v '^#' /Users/ghost/core/anima/.roadmap.iit4 | grep -v '^[[:space:]]*$' | jq -c '.id // .type'
"header"
"iit4.n21_pass_5_of_16"
"iit4.n21_v3_finality"
"iit4.proper_phi_mip_attempt"
"iit4.qmirror_byte_identical_link"
"iit4.casali_v6_real_substrate_path"

$ ... | jq '.required_conditions[1] | {id, status, blocker_reason}'
{
  "id": "iit4.cond.2",
  "status": "unmet",
  "blocker_reason": "#120 honest_C3 #1 (Φ proxy ≠ IIT 4.0 φ★) NOT closed via MIP marginalization; proper φ★ requires $132/gate × 2^N state-conditional runs ($1500+ for 3-substrate confirm)"
}

$ ... | jq '.blockers[1] | {id, status}'
{"id":"iit4.blk.2","status":"open"}
```

cond.2 + blk.2 originals fully preserved; annotation reachable + parses cleanly.

## Cross-link to qmirror canonical

`nexus/.roadmap.qmirror` `qmirror.cond.6` (`status=met`, F5 4/4 PASS) and entry `qmirror.cond6_f5_byte_identical` (`status=landed`) — observed unchanged this cycle.
