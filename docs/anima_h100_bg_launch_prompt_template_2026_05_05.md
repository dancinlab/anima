---
title: anima H100 BG launch prompt template — L23/L24/L25 6-checklist boilerplate
cycle: 2026-05-05
ts: 2026-05-05T_h100_bg_launch_prompt_template
status: TEMPLATE
type: launch_prompt_template
predecessor:
  - docs/anima_h100_cost_discipline_operationalization_spec_2026_05_05.md (§3.4 — completion checklist source)
  - docs/anima_own_16_h100_cost_discipline_landed_2026_05_05.ai.md (admission)
  - docs/anima_h100_cost_watchdog_phase1_landed_2026_05_05.ai.md (Phase 1 tooling — h100_cost_watchdog.hexa + h100_idle_auto_killer.hexa)
related:
  - tool/h100_register.bash (boot wrapper — rule 1)
  - tool/h100_cost_watchdog.hexa (--deregister entrypoint — rule 3)
  - tool/h100_alert_emit.bash (alert sink — rule 6)
  - tool/h100_idle_auto_killer.hexa (escalation ladder — rule 6)
  - tool/anima_bg_prompt_validator.hexa (PROPOSED future cycle — convention→tool migration)
  - feedback_h100_cost_discipline_l23_l25_watchdog_own_16.md (memory SSOT)
raw_invariants:
  - raw#9 (md only this cycle, no code emission)
  - raw#10 (≥5 honest C3 in §7)
  - raw#15 (additive only — template, not retire of prior conventions)
---

# anima H100 BG launch prompt template — L23/L24/L25 enforcement (2026-05-05)

## §1 Scope

This template applies to **every H100 (or other GPU substrate with billable
runpodctl-managed pods) BG launch prompt with `target_usd ≥ $1`**. Examples:

- CLM-v4 LoRA training BGs (`tool/clm_v4_lora_train_orchestrator.hexa`)
- P9 / Pβ / Mk.XII training BGs (`tool/anima_runpod_orchestrator.hexa`)
- Smoke / dogfood / Phase 4 validation BGs (even $1-3 budgets)
- Any cycle where pod allocation cost is non-trivial

**Non-applicable**: pure mac BGs (`cost = $0` substrate), HF Hub upload BGs
(no GPU pod), inference-only API calls.

**Authority**: (`.own` SSOT) — H100 cost discipline L23/L24/L25
watchdog enforcement, anchored to Pβ Paradigm D 50K rescue $54.72 idle-burn
incident (2026-05-04 → 2026-05-05).

---

## §2 6 mandatory checklist items

Every qualifying BG launch prompt MUST include the following six items
verbatim (lane-specific substitutions in `<...>`):

### Item 1 — Boot phase (rule a)

Immediately after pod allocation succeeds, register with the watchdog:

```bash
bash $REPO_ROOT/tool/h100_register.bash <POD_ID> <BG_LANE> <TARGET_USD>
```

This writes `state/h100_watchdog/pods/<POD_ID>.json` with the canonical
schema:

```json
{
  "pod_id": "<POD_ID>",
  "bg_lane": "<BG_LANE>",
  "target_usd": <TARGET_USD>,
  "start_ts": "<ISO8601>",
  "expected_completion_ts": "<ISO8601 + headroom>",
  "owner_orchestrator": "<orchestrator-hexa-name>",
  "last_heartbeat_ts": "<ISO8601>"
}
```

### Item 2 — Heartbeat phase (rule b)

In the BG main poll-loop, every iteration MUST touch the heartbeat
sentinel:

```bash
touch state/h100_watchdog/heartbeats/<BG_LANE>.txt
```

Stale-heartbeat threshold is **300s** (hard-coded in
`tool/h100_cost_watchdog.hexa` Phase 1). Watchdog daemon flags age > 300s
as `staleness_alert` to ledger.

### Item 3 — Trap pre-stop (L24 verification)

Before `runpodctl pod stop` or `runpodctl pod delete`, deregister:

```bash
hexa run tool/h100_cost_watchdog.hexa --deregister <POD_ID>
```

This separates BG-completion from pod-state (L24 lesson: BG-process-gone
is AMBIGUOUS — `runpodctl pod get` is the authoritative pod-alive check).
Archives `state/h100_watchdog/pods/<POD_ID>.json` →
`state/h100_watchdog/closed/<POD_ID>.json`.

### Item 4 — Verdict.json schema (5 required fields)

Final `verdict.json` MUST include:

```json
{
  "pod_kill_verified_404": <bool>,
  "watchdog_deregistered": <bool>,
  "cost_target_usd": <float>,
  "cost_actual_usd": <float>,
  "cost_overrun_2x_alerted": <bool>
}
```

- `pod_kill_verified_404`: result of
  `runpodctl pod get <POD_ID> 2>&1 | grep -q 'not found'`
- `watchdog_deregistered`: result of `--deregister` call (Item 3)
- `cost_target_usd`: per-BG budget (matches Item 1 `<TARGET_USD>`)
- `cost_actual_usd`: pod_runtime_hours × pod_hourly_rate
- `cost_overrun_2x_alerted`: true if `actual / target > 2.0`

`success: true` requires `pod_kill_verified_404 && watchdog_deregistered`
both true. `cost_overrun_ratio > 1.5` requires explicit honest-c3 entry
citing root cause + lesson learned (rule c + spec §3.4 d).

### Item 5 — L23 fail-fast (rate-limit takeover)

If BG agent detects:
- Anthropic 429 rate-limit response, OR
- mac orchestrator heartbeat absent > 5min

BG MUST emit a foreground takeover trigger to STDOUT (operator console)
with the literal copy-pasteable rescue command:

```bash
RUNPOD_API_KEY=$(/Users/ghost/core/secret/bin/secret get runpod.api_key --raw) \
  /opt/homebrew/bin/runpodctl pod delete <POD_ID>
```

Trigger MUST fire within **5 minutes** of detection. This closes the L23
gap exposed by Pβ rescue: BG was rate-limited at the kill-pod step;
foreground rescue command was not pre-stamped, so operator had to
re-derive pod ID from session log.

### Item 6 — L25 escalation awareness

BG prompt MUST acknowledge the cost-overrun escalation ladder enforced
by `tool/h100_cost_watchdog.hexa` + `tool/h100_idle_auto_killer.hexa`:

| Ratio | Action | Wall-time gate |
|-------|--------|----------------|
| `actual/target > 2×` | push notify + terminal bell + STDOUT log | immediate (next poll) |
| `actual/target > 3×` | auto-PAUSE (NOT delete) via auto-killer | + 30min no operator ack |
| post-pause | auto-DELETE + full state archive to `state/h100_archive/` | + 24h grace, still no ack |

The BG itself does NOT execute escalation — the watchdog does. The BG
prompt's job is to acknowledge awareness so honest-c3 disclosure of
cost-overrun is anticipated, not surprising.

---

## §3 Example boot snippet (hexa orchestrator integration)

Excerpt from a hypothetical
`tool/clm_v4_lora_train_orchestrator.hexa` lifecycle (verbatim shape, see
Phase 2 PATCH_NOTES for exact line numbers in real orchestrator):

```hexa
# --- Item 1: Boot phase ---
let pod_id = runpod_pod_create_h100(...)
sh "bash $REPO_ROOT/tool/h100_register.bash {pod_id} {bg_lane} {target_usd}"

# --- Item 2: Heartbeat phase (in main poll loop) ---
loop {
  ...poll training progress...
  sh "touch state/h100_watchdog/heartbeats/{bg_lane}.txt"
  sleep 60
}

# --- Item 3: Trap pre-stop (atexit / SIGTERM trap) ---
on_exit {
  sh "hexa run tool/h100_cost_watchdog.hexa --deregister {pod_id}"
  sh "RUNPOD_API_KEY=$(secret get runpod.api_key --raw) runpodctl pod delete {pod_id}"
  let kill_404 = sh_capture "runpodctl pod get {pod_id} 2>&1 | grep -q 'not found' && echo true || echo false"
  ...
}

# --- Item 4: Verdict.json schema ---
write_json("verdict.json", {
  ...,
  "pod_kill_verified_404": kill_404,
  "watchdog_deregistered": true,
  "cost_target_usd": target_usd,
  "cost_actual_usd": runtime_hr * hourly_rate,
  "cost_overrun_2x_alerted": (actual / target_usd > 2.0)
})

# --- Item 5: L23 rescue (embedded as comment for operator) ---
# IF RATE-LIMITED OR ORCHESTRATOR DEAD:
#   RUNPOD_API_KEY=$(/Users/ghost/core/secret/bin/secret get runpod.api_key --raw) \
#     /opt/homebrew/bin/runpodctl pod delete {pod_id}

# --- Item 6: L25 acknowledgment (prompt-level, no code) ---
```

---

## §4 Validation hexa hook (PROPOSED — future cycle)

`tool/anima_bg_prompt_validator.hexa` (NOT yet emitted) is the proposed
tool-level enforcement for Phase 3. Surface:

```bash
hexa run tool/anima_bg_prompt_validator.hexa --prompt-file <path>
# Exit 0: all 6 items present
# Exit 1: missing items (lists which) + cost gate (≥$1 trigger)
```

Validator scans for required tokens:

| Item | Required token regex |
|------|----------------------|
| 1 (boot) | `h100_register\.bash\s+\S+\s+\S+\s+\S+` |
| 2 (heartbeat) | `state/h100_watchdog/heartbeats` |
| 3 (deregister) | `h100_cost_watchdog\.hexa.*--deregister` |
| 4 (verdict) | all 5 field names appear in prompt |
| 5 (L23 rescue) | `secret get runpod.api_key.*runpodctl pod delete` |
| 6 (L25 ladder) | `auto-PAUSE\|auto-DELETE\|escalation` mentioned |

Until this validator lands, Phase 3 is **convention-level** (
honest-c3#7).

---

## §5 Deviation policy

Adoption is gated by `target_usd`:

| Cost band | Adoption requirement |
|-----------|---------------------|
| `target_usd ≥ $5` | **MANDATORY** — all 6 items required, no exceptions |
| `$1 ≤ target_usd < $5` | **strongly recommended** — skip allowed only with explicit honest-c3 justification in BG launch prompt |
| `target_usd = $0` (mac, no GPU pod) | **optional** — template not applicable |

Phase 4 smoke ($1-3 budget) is a deliberate dogfood test of the
mandatory-band template — the smoke pod registers with the same watchdog
it is validating.

---

## §6 Precedent

**Pβ rescue 2026-05-05 incident** — root incident driving L23/L24/L25
synthesis and admission:

- Pod `szv2vyf06h35uy`, Pβ Paradigm D 50K training cycle.
- Training completed successfully at 2026-05-04T23:47:25Z (50000/50000
  steps, FINAL adapter saved, COMPLETE.sentinel persisted).
- Pod stayed alive 18.30h post-completion until manual rescue-kill at
  2026-05-05T18:05:00Z.
- Idle burn = $54.72 = ~65% of session H100 spend (~$83-85 total).
- Root cause: BG agent rate-limited (Anthropic 429) at the kill-pod step
  AFTER rsync completed; mac orchestrator dead (also 429); pod alive
  burning $2.99/hr until operator manual rescue.
- L23-L25 lessons banked in `state/p9_pbeta_paradigm_d_50k_rescue_kill_2026_05_05/verdict.json`
  honest_c3, but were not enforcement-enforced — (this template's
  authority) closes that gap.

This template is the convention-level Phase 3 enforcement of the
operationalization spec; Phase 4 smoke + future
`anima_bg_prompt_validator.hexa` migrate convention → tool.

---

## §7 Honest C3 (raw#10 — ≥5 disclosure)

1. **Template adoption is convention, not tool-enforced** — no validator
   hexa exists yet (see §4); a BG launch prompt that omits Items 1-6 will
   still execute. Enforcement relies on operator + orchestrator-author
   discipline. Mitigation = future cycle ships
   `tool/anima_bg_prompt_validator.hexa` + leak_guard-style PreToolUse hook
   that lints BG agent prompts before launch. Until then, Phase 3 is
   advisory-mandatory not blocking-mandatory.

2. **Cost ≥ $1 threshold is heuristic** — chosen because Phase 4 smoke
   itself is $1-3 (dogfood requires self-application); below $1 the
   bookkeeping overhead arguably exceeds risk. But $1 floor is not
   principled — a $0.50 BG that goes 100× over still burns $50, same
   ballpark as Pβ. Real principle = **any pod that can leak runtime
   billing if BG dies**, regardless of target. Consider lowering threshold
   after first 30d production data if sub-$1 incidents emerge.

3. **L23 foreground takeover within 5min unrealistic if operator offline**
   — Item 5's "trigger fires within 5min of detection" assumes operator
   is at the terminal. Overnight runs, weekend autonomy, multi-day
   training cycles → operator may be unreachable for hours, not minutes.
   Mitigation = L25 auto-pause ladder fires at 30min + auto-delete at
   24h, but those are budget-protective, not work-protective. A truly
   L23-resilient design needs an out-of-band operator-paging channel
   (push notify, SMS, on-call rotation) — out of scope for this template.

4. **Auto-pause vs auto-kill trade-off chosen pause-first (Item 6)** —
   pause preserves in-flight work but extends cost up to 24h × hourly
   rate before delete. For a stuck $2.99/hr H100, 24h grace = $71.76
   additional burn per stuck pod. This is acceptable because the Pβ
   incident actually completed training BEFORE idle burn began — kill-
   first on partial-state pods would lose the FINAL adapter pre-rsync.
   Trade-off accepted at admission, restated here for prompt-
   author awareness.

5. **Verdict.json schema evolution may break checklist** — Item 4 lists
   5 fields; if Phase 4 smoke or future cycles surface missing fields
   (e.g., `cost_overrun_3x_pause_triggered`, `state_archive_path`,
   `auto_killer_invoked_ts`), schema bumps to v2 and old prompts fail
   field-presence linting. Mitigation = treat field list as v1 floor
   (additive only); validator should accept superset. But this discipline
   is not codified anywhere yet — risk that v2 schema rolls out without
   backward-compat declaration.

6. **Template is mac-substrate-specific in Item 5 rescue command** —
   `/opt/homebrew/bin/runpodctl` path is Apple Silicon homebrew. ubu1 / ubu2
   substrate operators copying this template literally will hit "command
   not found". Mitigation = document substrate-specific rescue path
   variants in §3.4 of the source spec; future template iteration should
   use `which runpodctl` resolution, not hardcoded path. Honest framing:
   this template is mac-orchestrator-centric because that's where every
   anima H100 BG currently launches from.

7. **Phase 3 Items 5+6 are prompt-text disclosure, not executable** —
   Items 1-4 emit code/state; Items 5+6 are operator-awareness statements
   in the BG prompt body. A BG that includes Items 1-4 verbatim but skips
   5-6 will pass any token-level lint while losing the L23/L25 epistemic
   payload. This is unavoidable for prose-level lessons — only solution
   is prompt-template adherence checked against this doc by future
   validator (see §4).

---

## §8 References

- spec: `docs/anima_h100_cost_discipline_operationalization_spec_2026_05_05.md`
- admission: `docs/anima_own_16_h100_cost_discipline_landed_2026_05_05.ai.md`
- Phase 1 landed: `docs/anima_h100_cost_watchdog_phase1_landed_2026_05_05.ai.md`
- memory SSOT: `feedback_h100_cost_discipline_l23_l25_watchdog_own_16.md`
- Pβ rescue precedent: `state/p9_pbeta_paradigm_d_50k_rescue_kill_2026_05_05/verdict.json`
- sister memory:
  - `feedback_always_subagent_bg.md` (BG dispatch mandate)
  - `feedback_session_multi_bg.md` (multi-BG mandate)
  - `feedback_h100_no_concurrency_limit.md` (— pre-dispatch)
