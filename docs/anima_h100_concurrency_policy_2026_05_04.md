---
title: H100 concurrency policy — no artificial cap (2026-05-04)
cycle: 2026-05-04
ts: 2026-05-04T00:00:00Z
status: POLICY_LANDED
bg_lane: H100-NOLIMIT
type: policy_spec
author: anima
related:
  - docs/anima_h100_concurrency_policy_landed_2026_05_04.ai.md
  - feedback_h100_no_concurrency_limit.md (auto-memory)
raw_invariants:
  - raw#9 (md only this cycle, no code)
  - raw#10 (≥5 honest C3 caveats)
  - raw#15 (no destructive paths)
---

# H100 concurrency policy — no artificial cap (2026-05-04)

## 1. Policy

### 1.1 Verbatim user directive (2026-05-04)

> "h100 동시 갯수제한 없음"

(English: "no concurrency-count limit on H100s.")

### 1.2 Authoritative interpretation

There is **NO artificial concurrency cap** on simultaneous H100 pods in this codebase or session.

This means:

- Parallel H100 BG launches are explicitly OK. N concurrent pods at a time is fine.
- Older notes/conventions that may have implied "1 H100 at a time" or "≤2 pods cap" per session are **superseded** by this directive.
- The only constraints that remain are (a) RunPod account quota, (b) per-BG dollar budget cap, and (c) the hard infra limits enumerated in §6.

What this is NOT:

- Not infinite money. Per-BG `BUDGET_HARD_CAP` is mandatory (§3).
- Not infinite infrastructure. RunPod can still rate-limit or run out of capacity (§2, §6).
- Not a green-light to skip cost-projection in BG launch prompts (§4).

## 2. Practical limits (RunPod)

RunPod imposes per-account practical limits that this policy does **not** override. These should be **probed empirically**, not assumed:

| Constraint                     | Typical band        | How to confirm                                |
| ------------------------------ | ------------------- | --------------------------------------------- |
| Simultaneous pods per account  | 5–10 (no published) | `runpodctl get pods` count vs. attempts       |
| Boot rate                      | ~10/min             | Stagger pod creation if launching N>5 at once |
| Spot capacity per region       | varies hour to hour | Try alternate region on `OUT_OF_CAPACITY`     |
| Account-level GPU-hour quota   | unpublished         | Watch for 429 / quota errors during boot      |

**Rule:** before launching >5 concurrent H100s, do a small probe (1 → 3 → N) so we discover the actual ceiling without burning budget on bulk failures.

## 3. Per-BG `BUDGET_HARD_CAP` mandate

Every H100 BG (no matter how short) **MUST** declare an explicit dollar hard-cap as part of its launch prompt. This bounds total session burn even at high concurrency.

Required fields per BG launch:

```
BUDGET_HARD_CAP_USD: <integer dollar limit, e.g. 15 or 35>
EXPECTED_WALL_HOURS: <projected runtime>
PROJECTED_BURN_USD: <cap × concurrency factor>
AUTO_KILL_TRIGGER: <criterion that fires before HARD_CAP, e.g. "wall_time > 1.5h"
                    OR "loss plateau"
                    OR "step >= 10000">
```

If concurrency = 5 and each BG sets `BUDGET_HARD_CAP=$15`, total worst-case is $75/session — bounded and auditable.

If a BG launch prompt omits `BUDGET_HARD_CAP`, treat as **REJECT** and respond with the missing field requirement.

## 4. Cost discipline at high concurrency

Concurrent pods compound burn rate linearly. At RunPod H100 spot $2.99/hr:

| Concurrency | Hourly burn | 24h burn |
| ----------- | ----------- | -------- |
| 1           | $2.99       | $71.76   |
| 3           | $8.97       | $215.28  |
| 5           | $14.95      | $358.80  |
| 9           | $26.91      | $645.84  |

Mandate per BG launch prompt:

- **Explicit dollar projection**: state expected concurrency × hourly × wall.
- **Concurrency-aware reasoning**: "running 5 in parallel = 5× hourly burn — confirm budget."
- **Default session sane cap**: $200 unless user explicitly overrides (see §6).

## 5. Auto-kill discipline

### 5.1 Trap pre-stop scp (L13)

Every H100 BG MUST install a SIGTERM/SIGINT trap that scp's critical artifacts (savepoint, train.log, verdict.json) to ubu1 BEFORE the pod terminates. One pod hang during artifact rescue should not gate other BGs.

Reference: `state/runpod_pod_purge_2026_05_03/` (6 EXITED pods purged 2026-05-03 — confirmed scp pre-stop saved their last savepoints).

### 5.2 Heartbeat-aware dispatch

Each BG should heartbeat (e.g., touch `state/<bg>/heartbeat.ts` every 60s). Watcher process sees heartbeat staleness > 5min → auto-stop pod via `runpodctl stop`. One orchestrator hang must not bleed budget on N concurrent zombies.

### 5.3 No shared dispatcher gating

Concurrent BGs MUST NOT share a single foreground orchestrator that serializes them. If orchestrator hangs, all N BGs hang. Use independent BG launches (Agent run_in_background=true × N), each with its own auto-kill chain.

## 6. Hard limits we still respect

These are infra-level limits this policy does **not** override:

1. **HF Hub rate limits** — don't 100-pods-DoS huggingface.co. Stagger savepoint pushes if N>5; consider a single shared push proxy when concurrency is high.
2. **L11 setsid SSH detach mandatory** — every remote launch must `setsid nohup … &` so the SSH client closing doesn't kill the pod-side process. One nohup-over-ssh hang × N concurrent = N hangs (compounding).
3. **Pod boot 60-second slot churn** — RunPod throttles boot rate (~10/min). Stagger creations: if launching 10 H100s, expect ~1 minute of boot ramp.
4. **User-set total session budget** — default sane cap **$200 per session** unless user explicitly overrides (e.g. "OK $500 for this cycle"). Exceeding requires explicit re-confirmation.
5. **Per-BG `BUDGET_HARD_CAP`** — see §3, required per BG.
6. **RunPod account GPU-hour quota** — unpublished but real; rare at <10 pods, can hit at >10.

## 7. Roadmap annotation proposals (additive_only — DO NOT mutate)

The following roadmap entries currently encode compute-concurrency assumptions that this policy contextualizes. **Do NOT edit `.roadmap.*` files directly this cycle.** Instead, propose `cross_link.compute_concurrency_policy` annotations for next-cycle land:

### 7.1 `.roadmap.p9_sft`

Currently encodes:

- header `cost_band`: `"$650-850 (9 H100 parallel, 24hr) ~ $1500-3000 (9 H100 serial 9일 + actual sweep, success p 0.70-0.90)"`
- `cond.2` desc: `"9 H100 parallel option ($650-850, 24hr) 또는 1 H100 serial 9일 ($650)"`
- `blk.1`: `"9 H100 parallel $650-850 또는 serial $1500-3000"`

Proposed annotation (next cycle):

```json
"cross_link": {
  ...,
  "compute_concurrency_policy": "no-limit_2026_05_04",
  "concurrency_policy_doc": "docs/anima_h100_concurrency_policy_2026_05_04.md",
  "concurrency_note": "9 H100 parallel option preferred; serial path is fallback only — no infra concurrency cap per 2026-05-04 user directive"
}
```

### 7.2 `.roadmap.clm`

No explicit concurrency text found, but cross_link to p9_sft inherits the policy. Proposed annotation:

```json
"cross_link": {
  ...,
  "compute_concurrency_policy": "no-limit_2026_05_04 (inherited via p9_sft)"
}
```

### 7.3 `.roadmap.eeg`

`cond.7` references daemon/24-7 concurrency at the EEG-software layer (no GPU concurrency). H100 concurrency irrelevant here. **No annotation needed.**

### 7.4 `.roadmap.blm_brain_lm`

Phase 4 cost_band `"$500-2000 H100 LoRA path"` is single-path text, no concurrency assumption. Proposed annotation:

```json
"cross_link": {
  ...,
  "compute_concurrency_policy": "no-limit_2026_05_04",
  "concurrency_note": "Phase 4 LoRA path is per-pod; running multiple LoRA variants in parallel is policy-OK"
}
```

### 7.5 `.roadmap.anima_clm_eeg`

No direct H100 reference, but `realswap_pending_2026_05_03` and downstream training cycles inherit. Proposed annotation:

```json
"cross_link": {
  ...,
  "compute_concurrency_policy": "no-limit_2026_05_04 (inherited)"
}
```

### 7.6 `.roadmap.training`

`mk_xii_retrain_plan` ($2200-6700) and Pilot-T1 launcher hardening reference H100. Proposed annotation:

```json
"cross_link": {
  ...,
  "compute_concurrency_policy": "no-limit_2026_05_04",
  "concurrency_note": "Mk.XII retrain Phase 3a 13B critical gate is single-pod design but Phase 1/2 LoRA fan-out can run N-parallel under per-BG BUDGET_HARD_CAP"
}
```

### 7.7 Summary

| Roadmap                       | Has H100 ref | Annotation proposed |
| ----------------------------- | ------------ | ------------------- |
| `.roadmap.p9_sft`             | yes (3x)     | yes                 |
| `.roadmap.clm`                | inherited    | yes                 |
| `.roadmap.blm_brain_lm`       | yes (1x)     | yes                 |
| `.roadmap.anima_clm_eeg`      | inherited    | yes                 |
| `.roadmap.training`           | yes          | yes                 |
| `.roadmap.eeg`                | no (CPU/EEG) | no                  |

**5 roadmap files** have annotation proposals. None are landed this cycle (additive_only proposals only).

## 8. Honest C3 caveats (raw#10)

1. **"No limit" is policy not infra.** RunPod can and does rate-limit. Per-account simultaneous-pod ceiling is unpublished — typically 5-10. Boot rate throttle ~10/min. This policy does not override the cloud provider; it only removes our self-imposed cap.

2. **Concurrent burn compounds fast.** 5×$2.99/h = $15/h. 9 × 24h = $645+. Without per-BG `BUDGET_HARD_CAP` and a session-level cap, an unattended high-concurrency cycle could burn $1000+ overnight on stuck/zombie pods.

3. **One bad BG can OOM the account quota.** Rare at <10 pods, common at >10. A misconfigured launcher fan-out (e.g., infinite restart loop) could trigger account-level quota lockout, blocking *all* future launches in the session — affecting unrelated work.

4. **HF Hub is a shared resource.** N concurrent savepoint pushes can hit HF rate limits (especially LFS). Stagger pushes or use a shared proxy when N>5; otherwise expect 429s and partial uploads.

5. **L11 setsid + L13 trap pre-stop scp are MANDATORY** at high concurrency. One nohup-over-ssh hang at N=1 is annoying. At N=9 it's nine simultaneous hangs that all need manual rescue. Without setsid+trap discipline, this policy invites disasters that the old "1 H100 at a time" cap implicitly prevented.

6. **Probing is cheap; bulk-launching blind is not.** Before going N=9 directly, probe N=1 → N=3 → N=9 to discover any hidden RunPod ceilings. Cost of probe: ~$1. Cost of 9 simultaneous OUT_OF_CAPACITY failures: 9 botched savepoints + ~$10 wasted boot churn.

7. **Auto-kill heartbeat must not share state.** If all N BGs write heartbeats to the same file, concurrent fsync races can corrupt the heartbeat. Use `state/<bg_id>/heartbeat.ts` per-BG (separate paths, no shared lock).

## 9. Audit log

- 2026-05-04: policy doc landed (this file).
- 2026-05-04: auto-memory entry landed (`feedback_h100_no_concurrency_limit.md`).
- 2026-05-04: 5 roadmap files identified for annotation; annotations are proposals only — DO NOT mutate `.roadmap.*` this cycle. Land in next-cycle additive_only commit per user policy.

## 10. References

- User directive 2026-05-04: "h100 동시 갯수제한 없음"
- `state/markers/anima_h100_concurrency_policy_landed.marker` (next cycle)
- `feedback_h100_no_concurrency_limit.md` (auto-memory, this cycle)
- `docs/anima_h100_concurrency_policy_landed_2026_05_04.ai.md` (1-page summary, this cycle)
- Sister memory: `feedback_session_multi_bg.md` (≥2 BG parallel mandate)
- Sister memory: `feedback_parallel_bg_git_race.md` (git index race at N≥2)
- Predecessor: `project_runpod_pod_purge_2026_05_03.md` (6 EXITED H100 pods purged)
