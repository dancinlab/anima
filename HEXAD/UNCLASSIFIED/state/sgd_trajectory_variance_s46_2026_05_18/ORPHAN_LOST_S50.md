# §50 — §46 orphan-fire recovery: ORPHAN-LOST (honest carry)

**Date**: 2026-05-18 · **Cycle**: §50 (retry of rate-limited §49/§50/§51 wave) · **$0** (pull-only, NO GPU fire, NO dispatch)

## 1. §46 pod status — GONE

§46 (`350c152ac merge(#46)`, landed as **infrastructure-only + fire ORPHAN-CARRY**)
dispatched a 2-seed sequential §16 re-fire (seeds 2026, 7777) to runpod pod
**`sjkx0md1wp6tbw`** (H100 80GB, per the AGENTS.tape orphan-carry entry). The §46
agent died (30-min worktree budget exceeded) ~70-min into the runpod 2-seed
sequential run, before any pull.

**§50 recovery attempt result**: pod `sjkx0md1wp6tbw` is **GONE**.

- `secret get runpod.api_key` → OK (key present).
- `runpod.get_pods()` (canonical SDK method per `g_fire_dispatch_robust`) →
  **`[]` — TOTAL_PODS: 0**. Re-queried twice, both empty.
- No `dispatch_s46.log` was ever committed (the §46 dir contains only
  `dispatch_s46.sh` + `eval_s46.py` + `blue_falsifier_s46.py`) — so there is no
  recorded SSH endpoint to attempt a manual scp-pull against, and the pod ID is
  known only from the AGENTS.tape carry entry, not a committed dispatch log.
- No `eval_result_seed_2026.json` / `eval_result_seed_7777.json` anywhere under
  `state/` (`find state -name 'eval_result_seed_*.json'` = empty). No partial
  pull exists.

The §46 pod self-terminated (its `dispatch_s46.sh` trap terminates the pod on
exit unless `SAVE_POD=1`; `SAVE_POD` was not set by the dying agent), OR runpod
reclaimed it. Either way the trained ckpts + per-seed eval JSON are
**unrecoverable** — they lived only on the destroyed pod's disk.

## 2. §46 verdict — ORPHAN-LOST (no SEED-STABLE / MIXED / SEED-VARIABLE measurement)

`eval_s46.py` + `blue_falsifier_s46.py` are ready and committed (4/4 🔵 sidecar
synthetic-input PASS, per §46 land), but they require the per-seed eval result
JSON as input. With zero recovered datapoints (seeds 2026 + 7777 both lost; only
§16 seed-1337 `eval_result_s16.json` exists on main as a single datapoint), the
SEED-STABLE vs SEED-VARIABLE test **cannot be run**. A 1-of-3 datapoint cannot
distinguish seed-stable data-order structure from SGD-trajectory lottery — that
discrimination needs ≥2 distinct-seed §16 fires compared against seed-1337.

**No measured §46 verdict.** This path is closed-lost, not closed-negative.

## 3. §42 answer — STAYS OPEN via §46, but ALREADY CONFIRMED via §47

§42 (`§verdict_routing_21v43_analysis_s42`) found *no clean lever within the
tier≥77 band* and hypothesised the 17-vs-29 routing split = **SGD-trajectory
lottery within an already-necessary band** (not an anchor property).

- **Via §46 (this cycle's path)**: §42 stays **OPEN** — the direct seed-variance
  test (§46) is orphan-lost and unmeasured.
- **Via §47 (independent, already landed)**: §47 CORRECTION
  (`a54ae44d8`, g6 latest-wins) reports the §40-style anchor-distinct content
  re-fire **routed 0/29** → "§42 SGD-lottery CONFIRMED, content-axis routing
  lever closed-negative." So the §42 hypothesis is **already independently
  confirmed** by the content-axis arm (§40~§47 4-attempt arc), even though the
  seed-variance arm (§46/§50) never produced a datapoint.

Net honest answer to §42: **the 17-vs-29 split is NOT an anchor-property lever
(confirmed via §47 content-axis 0/29); whether it is specifically seed-variable
vs data-order-stable remains UNMEASURED (§46 lost).** §42's broader conclusion
("lever may not exist as anchor property — likely §1.1 data-regime threshold's
other face") is supported; its narrow seed-variance sub-claim is untested.

## 4. Orphan pod audit — ZERO orphan pods

`runpod.get_pods()` = `[]`. There are **no orphan pods** on the runpod account:
not `sjkx0md1wp6tbw` (§46), not any `s46-seed-variance-*` / `carving-*` /
`l6-*` / §40/§41/§47-named pod. **Nothing to terminate; $0 ongoing cost.**
The §46 pod's own trap (or runpod reclamation) already cleaned it up — the cost
containment objective is already satisfied. See `orphan_pod_audit_s50.json`.

## 5. Cost

§50 itself = **$0** (pull-only: `secret get` + `runpod.get_pods()` + local file
ops; NO GPU fire, NO dispatch). §46's already-spent fire cost (~70-min H100,
≈ $1.5–2.5, never pulled) is sunk and was already accounted as §46 ORPHAN-CARRY
— §50 adds nothing.

## 6. Honest C3 (≥10)

1. **No measured §46 verdict produced** — this is an orphan-lost outcome, not a
   SEED-STABLE/MIXED/SEED-VARIABLE finding. Reported as lost, not fabricated.
2. **Pod ID known only secondhand** — `sjkx0md1wp6tbw` comes from the AGENTS.tape
   carry entry, not a committed `dispatch_s46.log`. The dispatch log was never
   written/committed, so even SSH-manual recovery had no endpoint to target.
3. **§46 pod GONE confirmed via canonical SDK** (`runpod.get_pods()`), the same
   method `g_fire_dispatch_robust` uses repo-wide for orphan checks. Re-queried.
4. **§42 not closed by §50** — the seed-variance discrimination is untested. Any
   future claim that "§42 is closed" must cite §47's content-axis 0/29, not §46.
5. **§47 confirmation is content-axis, not seed-axis** — it shows anchor-distinct
   *content* doesn't move routing (0/29), which supports "not an anchor-property
   lever" but does NOT directly prove "seed-variable." The two are different
   falsifiers; conflating them would be over-claim (g3).
6. **Single §16 datapoint (seed-1337) insufficient** — cannot run `eval_s46.py`'s
   3-way comparison with 1 datapoint; no degraded/partial verdict attempted.
7. **Zero orphan pods is a clean result but also means zero recovery** — the same
   trap that prevented cost overrun also destroyed the unpulled ckpts. No way to
   have both here given the dying agent never set SAVE_POD=1.
8. **Cost of §46 fire is sunk and unverified** — ~$1.5–2.5 estimate is from
   H100 hourly × ~70min; no pod billing record pulled. Estimate only.
9. **No GraphQL cross-check** — raw GraphQL endpoint format failed; relied solely
   on SDK `get_pods()`. SDK is the repo-canonical authority, but a single source.
10. **§50 is a retry after a 3-way rate-limit wave** (§49/§50/§51) — kept tight
    per instruction; no scope expansion, no speculative recovery attempts.
11. **north-star unchanged** — §50 is orphan cleanup + honest carry, zero GOAL
    movement. §15 milestone (GOAL unsolved, irreducible bottleneck = §1.1
    data-regime threshold) carries unchanged.
12. **`blue_falsifier_s46.py` NOT re-run as a "real 4/4"** — it needs recovered
    result.json input; with no recovery, only its committed synthetic-input
    4/4 🔵 (from §46 land) stands. No fabricated post-recovery battery.
