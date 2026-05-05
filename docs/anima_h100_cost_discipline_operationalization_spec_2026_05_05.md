---
title: H100 cost discipline operationalization — L23/L24/L25 enforcement spec
cycle: 2026-05-05
ts: 2026-05-05T_cost_discipline_operationalization_spec
bg_lane: BG-COST-DISCIPLINE-OPERATIONALIZE
substrate: mac (spec only, $0, no exec, no commit, no roadmap mutation)
status: SPEC_LANDED
type: enforcement_spec + tooling_proposal
predecessor:
  - docs/anima_h100_concurrency_policy_2026_05_04.md (no-limit policy + $200 default cap)
  - docs/anima_h100_idle_audit_2026_05_05.ai.md (audit pattern reference)
  - docs/p9_pbeta_paradigm_d_50k_rescue_kill_landed_2026_05_05.ai.md (L23-L25 source)
  - docs/anima_session_2026_05_04_to_05_closure_audit.ai.md §8 C2/C6 (gap callout)
  - state/p9_pbeta_paradigm_d_50k_rescue_kill_2026_05_05/verdict.json (raw incident SSOT)
related:
  - tool/clm_v4_lora_train_orchestrator.hexa (recent orchestrator with L11-L13 fixes)
  - tool/anima_runpod_orchestrator.hexa (canonical pod lifecycle wrapper)
  - tool/h100_idle_guard.bash (existing launchd reclaim wrapper — L23/L24/L25 precursor)
  - tool/h100_auto_kill.hexa (existing idle reclaim — propose-only mode)
  - tool/h100_cost_tracker.hexa (existing per-round cost aggregator)
  - .own own 14 (HF Hub only) + own 15 (HF lifecycle PRIVATE→PUBLIC)
raw_invariants:
  - raw#9 (md only this cycle, no code emission)
  - raw#10 (≥5 honest C3 in §6)
  - raw#15 (additive only — no roadmap mutation, no .own mutation, no exec)
---

# H100 cost discipline operationalization — L23/L24/L25 enforcement spec (2026-05-05)

## §1 Problem statement

### 1.1 Concrete incident

On 2026-05-04 → 2026-05-05 the **Pβ Paradigm D 50K** training cycle completed successfully on RunPod H100 pod `szv2vyf06h35uy` at **2026-05-04T23:47:25Z** (50000/50000 steps, verdict `PRODUCTION_25K_FULL_PASS`, FINAL adapter saved, COMPLETE.sentinel persisted).

The pod was **not torn down for 18.30 hours** following completion. Manual rescue-kill executed at **2026-05-05T18:05:00Z** (best-estimate from rsync local mtime 17:51Z + ~14min observed kill-execution lag).

**Idle burn cost: $54.72** (18.30h × $2.99/hr H100 community spot).

**Session-level impact: $54.72 ≈ 65% of total session H100 spend (~$83-85 USD)**. The remaining 35% (~$28-30) covered four scientific cycles end-to-end (Path A retrain v2 retry-3, Pβ Paradigm D 50K production training itself, CLM-2 LoRA SFT, α'''-EVAL-FIX).

### 1.2 Generalizable root cause

The proximate failure was that BG-PBETA-RESCUE-KILL **was rate-limited mid-flight** (Anthropic API throttle / errno 429-class) **after** rsync of savepoints completed, but **before** `runpodctl pod stop` could execute. The mac orchestrator (the BG agent) died; the pod kept running.

Decomposed into three orthogonal failure modes:

1. **L23 rate-limit-fallback failure** — BG agent process died mid-script; no foreground operator-takeover trigger fired automatically. The script's pod-kill step was reached only on a successor manual cycle hours later.
2. **L24 BG-completion vs pod-state-down conflation** — BG monitor signal "BG agent process exit" was ambiguous: it can mean (a) successful completion, (b) crashed completion, (c) rate-limited completion-pending. Without a separate pod-state polling channel, no alarm fired when the BG was gone but the pod was alive.
3. **L25 cost-overrun escalation absent** — there was no $/hr ticker watching the pod-side spend independent of the orchestrator. By the time idle burn hit $54.72 (~10× the spec-anticipated $5-7), the user had no signal until the next session began and the audit BG ran.

### 1.3 Why this generalizes

The same three-mode failure can recur on **any** future BG that drives a long-lived pod:
- The agent (mac orchestrator) is a different process from the pod; either can die independently.
- BG agents can be rate-limited at any point in their script — not just at boot or at completion. Mid-script termination at the "kill the pod" step is the worst boundary because it leaves the pod alive with no scheduled tear-down.
- Without an independent watchdog, the cost-loss compounds at $2.99/hr until the next human audit cycle.

Lessons L23, L24, L25 were **banked** in `state/p9_pbeta_paradigm_d_50k_rescue_kill_2026_05_05/verdict.json:honest_c3` and in `docs/p9_pbeta_paradigm_d_50k_rescue_kill_landed_2026_05_05.ai.md §3` — but they were **not operationalized**. They live as prose, not as enforcement. The next BG that hits the same rate-limit boundary will reproduce the same loss.

This spec defines the operationalization gap closure: **how next-cycle BG dispatch logic should enforce L23/L24/L25 to prevent repeat**.

---

## §2 L23/L24/L25 enforcement requirements

### 2.1 L23 — rate-limit-fallback enforcement

#### Detect signals
- **Anthropic API errno 429** observed by the BG agent (rate-limit throttle).
- **BG agent process exit (any reason)** observed by an external watchdog while a registered pod is still alive.
- **Heartbeat staleness** — the BG agent fails to ping the watchdog for `> 5 min`.

#### Required action
**Foreground takeover trigger** must fire **within 5 minutes** of any of the three detect signals. "Foreground takeover" means: the user (operator) is notified with the **literal copy-pasteable runpodctl command** to stop+delete the pod, and the watchdog continues to poll until the pod is 404-verified.

#### Tooling shape
- A **separate process** (NOT inside the BG agent) — `tool/h100_cost_watchdog.hexa` — runs persistently and polls all registered pods every 5 minutes.
- The watchdog reads `state/h100_watchdog/pods/<pod_id>.json` (per-pod registry: `pod_id`, `bg_lane`, `target_usd`, `start_ts`, `expected_completion_ts`, `last_heartbeat_ts`, `owner_orchestrator`).
- On stale heartbeat OR observed BG agent exit + pod still alive, watchdog emits to `state/h100_watchdog/alerts/<ts>_<pod_id>.json` and to a user-facing notification channel (push notification + terminal bell + STDOUT to a tail-able log).
- **Foreground rescue command literal** must already be embedded in the BG launch prompt (§3.4) so the operator can copy-paste without re-deriving pod ID.

### 2.2 L24 — BG-completion vs pod-state-down separation

#### Detect signals
- **BG agent process exit observed by watchdog** — but pod-state has NOT been verified `404 not found`.
- **Sentinel COMPLETE** written by training script — but pod has NOT been stopped (covers the Pβ scenario exactly: COMPLETE.sentinel persisted, pod alive 18h).

#### Required action
**Pre-emptive pod kill** via runpodctl (separate auth / not via the dead BG agent) **before** the BG can mark itself done. The BG completion hook MUST call:

```
runpodctl pod get <id> 2>&1 | grep -q 'not found'
```

If this returns non-zero (pod is still alive), the BG completion step must NOT exit; instead it must:
1. Re-attempt `runpodctl pod stop <id>` + `runpodctl pod delete <id>`.
2. Re-poll `pod get` until 404.
3. Only then write `state/<bg>/verdict.json` with `pod_kill_verified_404: true`.
4. Only then deregister from the watchdog.

#### Tooling shape
- The orchestrator hexa templates already partially implement this (`clm_v4_lora_train_orchestrator.hexa` line 493-497: `POD_KILL_404='false'; if echo "$POST" | grep -qiE 'not found|404|...'; then POD_KILL_404='true'`). The gap is that this 404 check runs **inside the BG**, so a rate-limited BG never reaches it.
- The watchdog (§2.1 tooling) closes the gap: even if the BG dies, the watchdog polls `pod get` independently and triggers L23 escalation when BG-exit + pod-alive coincide.
- Verdict.json schema must add **two** required fields:
  - `pod_kill_verified_404: bool` (already present in `clm_v4_lora_train_orchestrator.hexa`)
  - `watchdog_deregistered: bool` (NEW — proves the watchdog acknowledged the pod is gone)

### 2.3 L25 — cost-overrun escalation

#### Detect signals
- **Actual cost > 2× spec target_usd** (heuristic threshold, see §6 C6).
- **Idle burn detection** — pod alive AND `$ABS_DIFF (now − last_step_ts) > 30 min` (no training step in 30 min) AND no orchestrator heartbeat in 5 min → idle.

#### Required action
**Notify user** via push notification + auto-pause pod (do NOT auto-kill). The auto-pause step is reversible (`runpodctl pod stop` keeps pod artifacts, `runpodctl pod start` resumes), allowing user to either resume (if false alarm) or full-delete (if confirmed idle).

**Wait for user action**. Auto-kill is intentionally NOT permitted in this spec — false-positive auto-kills lose in-flight work, which is reputationally worse than $5-10 of extra burn while waiting for human review.

#### Tooling shape
- A **$/hr ticker process** running outside the BG agent — `tool/h100_idle_auto_killer.hexa` (despite the filename, the action ladder is alert → auto-pause → user-confirm → kill, NOT immediate kill).
- Subscribes to watchdog alerts; aggregates `actual_usd = (now − start_ts) × bid_usd_per_hr_per_pod` per pod.
- When `actual_usd > 2 × target_usd`, emits a push notification with: pod_id, bg_lane, target_usd, actual_usd, idle_minutes_estimate, copy-paste rescue commands.
- When `actual_usd > 3 × target_usd` AND no user response in 30min, executes `runpodctl pod stop` (pause, not delete) and updates state.

---

## §3 Concrete tooling proposals

### 3.1 NEW `tool/h100_cost_watchdog.hexa`

Separate persistent process. Polls pods every 5 minutes. Emits cost ledger + alerts.

**Inputs**:
- `state/h100_watchdog/pods/<pod_id>.json` — per-pod registry (registered by orchestrators at boot)
- `state/h100_watchdog/heartbeats/<bg_id>.txt` — BG agent heartbeat timestamps (touched every 5 min by orchestrators)

**Outputs**:
- `state/h100_watchdog/ledger.jsonl` — append-only cost ledger (pod_id, ts, bid_usd_per_hr, elapsed_h, cumulative_usd)
- `state/h100_watchdog/alerts/<ts>_<pod_id>_<reason>.json` — alert records (reason ∈ {stale_heartbeat, bg_dead_pod_alive, idle_no_steps, cost_2x_target, cost_3x_target_autopause})

**Polling logic** (per cycle, every 5 min):
1. List `state/h100_watchdog/pods/*.json`.
2. For each, run `runpodctl pod get <pod_id>` — record current pod state.
3. Check heartbeat freshness: `now − last_heartbeat_ts < 5 min` → OK; else stale → emit alert.
4. Compute `cumulative_usd = (now − start_ts) × bid_usd_per_hr`. Append to ledger.
5. If `cumulative_usd > 2 × target_usd` → emit `cost_2x_target` alert.
6. If `cumulative_usd > 3 × target_usd` AND age of `cost_2x_target` alert > 30 min AND no user-ack → emit `cost_3x_target_autopause` AND issue `runpodctl pod stop <pod_id>`.
7. If pod_get returns `not found` → mark deregistered, archive to `state/h100_watchdog/closed/<pod_id>.json`.

**Reuse existing precedent**:
- `tool/h100_idle_guard.bash` (launchd wrapper) — already exists; refactor to delegate detection logic to this new hexa watchdog.
- `tool/h100_auto_kill.hexa` (propose-only mode) — already exists; this watchdog supersedes for the alert+auto-pause action ladder.
- `tool/h100_cost_tracker.hexa` (per-round aggregator) — keep as offline analysis tool; watchdog focuses on **live** cost stream.

### 3.2 NEW `tool/h100_idle_auto_killer.hexa`

Subscribes to watchdog alerts. **Despite the filename, action ladder is alert → auto-pause → user-confirm → delete; never immediate auto-delete**.

**Trigger**: file-watch on `state/h100_watchdog/alerts/*.json`.

**Action ladder**:
1. Alert reason `stale_heartbeat` (5 min) → push notify.
2. Alert reason `bg_dead_pod_alive` (15 min) → push notify + emit copy-paste rescue command.
3. Alert reason `idle_no_steps` (30 min) → push notify + tag pod as suspected-idle.
4. Alert reason `cost_2x_target` → push notify + concrete numbers (target $X, actual $Y, gap-cause).
5. Alert reason `cost_3x_target_autopause` (only after 30 min of no user response on 2x alert) → `runpodctl pod stop <pod_id>` (pause, NOT delete; reversible).
6. **No auto-delete in any tier**. User must confirm the delete via explicit acknowledgement file (e.g., touch `state/h100_watchdog/acks/<pod_id>_DELETE_OK`).

### 3.3 PATCH existing orchestrator hexa templates

Required orchestrator-side hooks (apply to `tool/clm_v4_lora_train_orchestrator.hexa`, `tool/anima_runpod_orchestrator.hexa`, and any future orchestrator):

#### Boot-time hook (§2.1 / §2.2)
1. Register pod with watchdog: write `state/h100_watchdog/pods/<pod_id>.json` with fields `{pod_id, bg_lane, target_usd, expected_completion_ts, owner_orchestrator, bid_usd_per_hr_per_pod, start_ts}`.
2. Spawn (or rely on launchd-supervised) watchdog process if not already running.

#### Per-cycle hook (§2.1)
3. Heartbeat ping every 5 min: touch `state/h100_watchdog/heartbeats/<bg_id>.txt` with current ts. (Reuse `HEARTBEAT_PATH` pattern from `clm_v4_lora_train_orchestrator.hexa:41`.)

#### Trap pre-stop hook (§2.2 — already present, augment)
4. On EXIT/INT/TERM trap, BEFORE pod stop:
   - L13 trap pre-stop scp/rsync rescue (existing).
   - **NEW**: write `state/h100_watchdog/heartbeats/<bg_id>.txt` with marker "EXITING".
5. After `runpodctl pod stop+delete`:
   - **NEW**: poll `runpodctl pod get <pod_id>` until 404 (max 3 retries × 30s).
   - **NEW**: if 404 confirmed, deregister: delete `state/h100_watchdog/pods/<pod_id>.json` (archive to `state/h100_watchdog/closed/`).
   - **NEW**: if 404 NOT confirmed after retries, write `state/h100_watchdog/alerts/<ts>_<pod_id>_kill_failed.json` and exit non-zero.

#### Verdict-write hook (§2.2)
6. Verdict.json schema additions (mandatory for all H100 BGs):
   - `pod_kill_verified_404: bool` (already present in clm_v4 orchestrator)
   - `watchdog_deregistered: bool` (NEW)
   - `actual_usd: float` (NEW — cumulative spend from watchdog ledger)
   - `target_usd: float` (NEW — spec target for delta-tracking)
   - `cost_overrun_ratio: float` (NEW — actual / target)

### 3.4 NEW BG launch prompt template — completion checklist

All H100 BG launch prompts (memory entry `feedback_always_subagent_bg.md` template) must include the following checklist block:

```
## BG completion checklist (L23/L24/L25 enforcement — mandatory)

(a) verdict.json written with required fields:
    pod_kill_verified_404: true
    watchdog_deregistered: true
    actual_usd: <float>
    target_usd: <float>
    cost_overrun_ratio: <float>

(b) pod 404 verified via:
    runpodctl pod get <pod_id> 2>&1 | grep -q 'not found'

(c) watchdog deregistered (state/h100_watchdog/pods/<pod_id>.json removed
    OR archived to state/h100_watchdog/closed/<pod_id>.json)

(d) cost computed (actual vs target); if cost_overrun_ratio > 1.5
    add explicit honest-C3 entry citing root cause + lesson learned

(e) rate-limit fallback ready: copy-pasteable rescue command embedded
    in this prompt, e.g.:
    RUNPOD_API_KEY=$(/Users/ghost/core/secret/bin/secret get runpod.api_key --raw) \
      /opt/homebrew/bin/runpodctl pod delete <POD_ID>
```

---

## §4 Implementation plan

| Phase | Cost | Substrate | Wall time | Deliverable |
|-------|------|-----------|-----------|-------------|
| **Phase 1** | $0 | mac | ~2h | Write `tool/h100_cost_watchdog.hexa` + `tool/h100_idle_auto_killer.hexa` (hexa-only per raw#9 / py-to-hexa rule); selftest mode validates polling + alert emission against synthetic pod fixture |
| **Phase 2** | $0 | mac | ~1h | Patch `tool/clm_v4_lora_train_orchestrator.hexa` + `tool/anima_runpod_orchestrator.hexa` with §3.3 boot/heartbeat/trap/verdict hooks (additive PATCH_NOTES.md per raw#15) |
| **Phase 3** | $0 | mac | ~30min | Update memory `feedback_always_subagent_bg.md` (or new `feedback_h100_bg_launch_l23_l25_checklist.md`) with §3.4 mandatory checklist; cross-link from `feedback_pbeta_chat_capability_fail_substrate_research_pass_decoupled.md` |
| **Phase 4** | $1-3 | H100 (smoke) | ~30min | Boot 1 minimal H100 pod, register with watchdog, simulate 3 scenarios: (a) graceful complete + 404 verify, (b) BG-killed mid-flight + watchdog auto-pause, (c) heartbeat-stale → alert. Tear down pod cleanly. |
| **TOTAL** | **$1-3** | mixed | ~4h | Full L23/L24/L25 enforcement landed |

**Phase ordering rationale**: Phase 1 (tool emission) before Phase 2 (orchestrator patches) so the patch references real tool paths. Phase 3 (memory + prompt template) before Phase 4 (smoke) so smoke uses the new launch checklist as the test harness.

**Cost discipline note**: Phase 4 smoke pod must itself be registered with the watchdog being tested (dogfood pattern). Use $1-3 budget hard-cap with auto-pause configured at 1.5× target.

---

## §5 Memory + roadmap propagation

### 5.1 Memory updates (proposal — not landed in this BG)

#### Update `feedback_pbeta_chat_capability_fail_substrate_research_pass_decoupled.md`
Add cross-link section: "Cost discipline operationalization: see `docs/anima_h100_cost_discipline_operationalization_spec_2026_05_05.md` for L23/L24/L25 enforcement closure preventing $54.72-class repeat."

#### NEW `feedback_h100_bg_launch_l23_l25_checklist.md` (proposed)
Captures §3.4 launch prompt checklist as auto-memory; cross-links to `feedback_h100_no_concurrency_limit.md` (sister) + `feedback_session_multi_bg.md` (multi-BG mandate) + `feedback_always_subagent_bg.md` (BG dispatch).

### 5.2 Roadmap annotation proposal — `.roadmap.training`

`.roadmap.training` currently encodes Mk.XII retrain ($2200-6700 H100) + Pilot-T1 launcher hardening. Proposed additive annotation (next-cycle land, NOT this cycle):

```json
"cross_link": {
  ...,
  "h100_cost_discipline_operationalization": "anima_h100_cost_discipline_operationalization_spec_2026_05_05",
  "h100_cost_discipline_doc": "docs/anima_h100_cost_discipline_operationalization_spec_2026_05_05.md",
  "l23_l25_enforcement_status": "spec_landed_2026_05_05 / phase_1_pending"
}
```

### 5.3 Roadmap annotation proposal — `.roadmap.p9_sft`

Similar additive `cross_link.h100_cost_discipline_operationalization` annotation; predecessor incident is the Pβ Paradigm D 50K cycle which sits under p9_sft.

### 5.4 own 16 candidate — H100 cost discipline operationalization

`.own` taxonomy currently lands at own 14 (HF Hub only) + own 15 (HF lifecycle PRIVATE→PUBLIC). own 14 + 15 form an HF triad pattern (WHERE + HOW). A parallel triad on the **compute lifecycle** axis is proposed:

- **own 16 (proposed)**: "anima-local: H100 cost discipline operationalization — L23/L24/L25 watchdog + completion checklist + foreground fallback mandatory"
  - **slug**: `h100-cost-discipline-l23-l25-watchdog`
  - **base**: anima/.own SSOT + own 5 (no preset cost cap) + own 6 (GPU dispatch + watchdog) + raw#10 honest-disclosure
  - **scope**: every H100 BG launch lifecycle (boot → heartbeat → exit → kill → verdict) MUST integrate watchdog registration, heartbeat pings, trap-based 404 verification, deregistration, and verdict cost-overrun fields.
  - **rule (a)**: every H100 BG MUST register with watchdog at boot (write `state/h100_watchdog/pods/<pod_id>.json`).
  - **rule (b)**: every H100 BG MUST heartbeat every 5 min (`state/h100_watchdog/heartbeats/<bg_id>.txt`).
  - **rule (c)**: every H100 BG verdict.json MUST include `pod_kill_verified_404 + watchdog_deregistered + actual_usd + target_usd + cost_overrun_ratio` fields.
  - **rule (d)**: every H100 BG launch prompt MUST include §3.4 completion checklist + rate-limit fallback rescue command.
  - **rule (e)**: watchdog auto-pause (NOT auto-delete) at 3× target_usd; user-confirm required for delete.
  - **enforcement (advisory)**: linter `tool/h100_bg_launch_lint.hexa` (PROPOSED) checks launch prompts for required fields.
  - **enforcement (audit)**: `state/h100_watchdog/ledger.jsonl` + `state/h100_watchdog/alerts/*.json` form audit trail.
  - **bans**: H100 BG launch without watchdog registration; verdict.json without 404 + watchdog_deregistered + cost fields; auto-delete (only auto-pause permitted).
  - **proof**: this spec doc; precedent Pβ idle burn $54.72 incident (preventable per L24/L25).
  - **category**: meta-triad + proof-truth.
  - **applies-to**: h100-bg-launch-lifecycle + cost-discipline.
  - **severity**: warn (escalate to block per follow-up linter).
  - **note**: own 16 = compute-lifecycle triad partner to own 14 (HF WHERE) + own 15 (HF HOW lifecycle); together own 14 + 15 + 16 cover anima's external-resource-consumption axes (storage / publication / compute).

**DO NOT mutate `.own` in this BG. Proposal only — land in next-cycle additive_only commit.**

---

## §6 Honest C3 (raw#10, ≥5)

- **C1 watchdog adds polling overhead — but trivial at anima scale.** 1 SSH per pod per 5 min × 12 polls/hour at typical 1-3 pods concurrently = 12-36 polls/hour. RunPod API limits are far above this. SSH-keepalive cost is sub-cent. The watchdog process itself is a single hexa loop; its CPU/memory footprint is negligible. **Verdict: trivial.** This is a non-issue at observed concurrency bands.

- **C2 auto-pause vs auto-kill trade-off — auto-pause chosen, but with reversibility cost.** Auto-pause (`runpodctl pod stop`) preserves pod artifacts (workspace, savepoints) while billing stops. `runpodctl pod start` resumes, but resumed pods may land on a different host (state-loss risk for in-progress training). Auto-kill (delete) is simpler but loses any unsaved in-flight work. **The 3× threshold + 30-min user-response window before auto-pause** is the explicit trade-off lever — if user response window is too short, false-positive pauses lose cycles; if too long, idle burn dominates. Default 30 min is heuristic, calibration TBD per Q2.

- **C3 user push notification frequency = signal-to-noise tuning, currently uncalibrated.** "Notify on every $5 burn" is too noisy at $200 session cap (40 notifications). "Notify on 2× overrun" at low-target BGs ($1 target → notify at $2) creates spam from naturally-variable cycles. "Notify on 1h idle" misses the L24 pattern entirely (Pβ idle burn was 18h, but we want to catch at hour 1, not 18). **Proposed initial calibration**: alert-tier-1 at 30min stale heartbeat, alert-tier-2 at 2× cost overrun (pause threshold at 3×), alert-tier-3 at 1h idle-no-steps. Refine after 5-10 alert events of real-session data.

- **C4 watchdog process itself can rate-limit-fail — recursive concern.** If the watchdog is a hexa orchestrator subject to the same Anthropic rate-limit boundary as the BG agent, it has the same failure mode. **Mitigation**: implement watchdog as a **pure bash daemon** (or launchd-supervised hexa entry that does not invoke Anthropic API), so Anthropic rate-limits cannot kill it. Alternative: run watchdog under `cron` / `launchd` with restart-on-exit policy. The watchdog's job is mechanical (poll `runpodctl pod get`, write JSON, emit notification) — it does not require LLM tokens. **This is the correct fix for the recursion**; however, "restart-on-exit" policies still have rare-failure modes (e.g., if launchd itself loses the plist, watchdog gone silently). Defense-in-depth: add a daily cron audit that confirms watchdog is alive.

- **C5 retroactive — L24 was banked but not enforced; this spec is reactive not proactive.** L24 emerged from a $54.72 incident that already happened. This spec closes the gap **after** the loss. A truly proactive process would have anticipated L24 from L11 (SSH detach) + L13 (trap pre-stop scp) by reasoning: "if the BG agent dies between L13's scp and the pod stop, the pod is orphaned." The chain was visible in principle; the team reasoned about agent + pod liveness as a single signal. **Lesson-of-lesson**: future spec reviews should explicitly enumerate "process A and process B can each die independently — what happens at each combination?" cartesian-product as a design checklist.

- **C6 cost-overrun threshold (2×) is heuristic, not principled.** Why 2× and not 1.5× or 3×? Pure heuristic. 2× balances "early warning" vs "noise from naturally-variable cycle costs". Some legitimate cycles do run 1.5-2× target (e.g., training that hits a hard problem and needs more steps). A more principled threshold would derive from per-cycle target_usd distribution + variance — i.e., per-lane calibrated z-score thresholds. **For initial roll-out**, 2× alert + 3× pause is the proposed default; refinement per Q1/Q2 after observing real alert frequency.

- **C7 spec doc is .md only per raw#9; no actual hexa code emitted in this BG.** This is a **spec/proposal** cycle. Phase 1-4 implementation requires a separate exec cycle. The risk is that specs land but implementation lags — see C5 about L24 itself. **Mitigation**: spec doc names exact tool paths (`tool/h100_cost_watchdog.hexa`, `tool/h100_idle_auto_killer.hexa`) so implementation can be unambiguously kicked off; Phase 4 smoke at $1-3 keeps the bar low.

- **C8 overlapping prior tools — not all paths are NEW.** `tool/h100_idle_guard.bash`, `tool/h100_auto_kill.hexa`, and `tool/h100_cost_tracker.hexa` already exist with overlapping responsibilities. This spec proposes NEW tools but should be read as **net-new-functionality + refactor of existing-tools-into-watchdog-architecture** rather than greenfield. Phase 1 must include explicit superset/refactor decision: which existing tool paths persist, which deprecate, which absorb. Default proposal: keep `h100_cost_tracker.hexa` (offline analysis), wrap `h100_auto_kill.hexa` from `h100_idle_guard.bash` into the new watchdog's reactive layer, retire `h100_idle_guard.bash` as a thin launchd wrapper that just invokes the new watchdog.

- **C9 watchdog ownership question is unresolved (Q4).** macOS launchd vs cron vs anima-side hexa daemon — each has trade-offs. launchd is canonical for macOS persistent processes (already used by `h100_idle_guard.bash`); cron is portable but less reliable on sleep/wake. A hexa entry has best dogfood-coherence with the rest of anima but introduces the C4 recursion concern. Recommended default: launchd-supervised + bash inner loop + hexa for selftest/admin commands.

- **C10 phase 4 smoke is itself a $1-3 cost — possibly violates own 5 "completeness-first" with sub-budget cap.** own 5 says "no preset cost cap" for research, but smoke tests are infra/tooling, not research. own 6 explicitly authorizes "canary-probe" — this is exactly that. $1-3 bound for a tooling smoke is justified per own 6; not in tension with own 5.

---

## §7 Decision queue

### Q1: 5-min vs 10-min watchdog poll interval?

**Trade-offs**:
- **5-min**: faster detection of stale heartbeat / idle pod. ~12 RunPod API calls/hr/pod.
- **10-min**: half the API calls; ~5-10min worst-case detection lag. Likely indistinguishable for cost-overrun (which is already tier-1 alert at 30min stale).

**Recommendation**: **5-min default** — doubled-check if RunPod API rate-limit becomes observed-issue, drop to 10-min. Detection-latency advantage of 5-min outweighs API call cost (sub-cent).

**User decision needed**: ack default 5-min OR override.

### Q2: auto-pause vs notify-only on cost-overrun?

**Trade-offs**:
- **Auto-pause** (this spec's proposal): self-healing if user is asleep / unavailable; reversible (`pod start`); but state-loss risk on host re-allocation.
- **Notify-only**: zero state-loss risk; but if user is unavailable for hours, idle burn continues.

**Recommendation**: **auto-pause at 3× target_usd ONLY after 30-min no user response on 2× alert** (this spec's tier ladder). Conservative — gives user clear escalation path before any pod-side action.

**User decision needed**: ack the 3× + 30-min ladder OR adjust thresholds.

### Q3: own 16 admission?

**Trade-offs**:
- **Yes admit own 16**: completes compute-lifecycle triad with own 14 + own 15; binding mandate for future BGs; warn-tier severity escalates to block via follow-up linter.
- **Defer**: own taxonomy may already over-quantify; could fold cost discipline into existing own 6 (GPU dispatch + watchdog) as additive sub-rules.

**Recommendation**: **admit own 16** — own 6 is too broad (covers entire GPU dispatch policy); own 16 specifically scopes **lifecycle enforcement + verdict.json schema additions + linter follow-up** which is a sharper, more actionable rule. Forms clean compute-lifecycle triad partner to HF triad (own 14 + own 15).

**User decision needed**: ack own 16 admission with proposed slug + rules in §5.4 OR fold into own 6.

### Q4: who owns watchdog process — anima daemon, cron, or launchd?

**Trade-offs**:
- **launchd** (macOS canonical): already-precedent via `tool/h100_idle_guard.bash`; persistent across reboots; user-session-attached.
- **cron**: portable; less reliable on sleep/wake; macOS deprecated for new use cases.
- **anima hexa daemon**: best dogfood; introduces C4 recursion concern (see §6).

**Recommendation**: **launchd-supervised + bash inner loop + hexa entry for selftest/admin** — combines macOS canonical reliability with hexa dogfood for admin/observability paths. Inner loop is bash to avoid C4 recursion (no Anthropic API calls in hot path).

**User decision needed**: ack launchd + bash + hexa-admin combo OR pick alternative.

### Q5: deferred — naming convention for `tool/h100_idle_auto_killer.hexa`?

The filename suggests "auto-killer" but the action is auto-pause + user-confirm-before-delete. Misleading filename creates risk of misuse (operator assumes auto-delete is enabled). Rename candidates: `tool/h100_idle_auto_pauser.hexa`, `tool/h100_cost_overrun_responder.hexa`. **Defer to Phase 1 implementation** for naming finalization; not a spec-time blocker.

---

## §8 Compliance markers

- **raw#9 (md only)**: this doc is .md only; no .py / .sh / .hexa / .json artifacts emitted in this BG. ✓
- **raw#10 (≥5 honest C3)**: §6 has 10 honest C3 bullets. ✓
- **raw#15 (additive only — no destructive paths)**: no roadmap mutation, no .own mutation, no exec, no commit. ✓
- **py-to-hexa rule**: all proposed tooling targets `.hexa` (raw#9 strict) or bash daemon (acceptable per `tool/h100_idle_guard.bash` precedent for launchd-supervised wrappers). ✓
- **session multi-BG**: this is a $0 spec BG; can run alongside other BGs in same session. ✓

## §9 Cross-link summary

| Reference | Role |
|-----------|------|
| `state/p9_pbeta_paradigm_d_50k_rescue_kill_2026_05_05/verdict.json` | L23-L25 source incident verdict (SSOT) |
| `docs/p9_pbeta_paradigm_d_50k_rescue_kill_landed_2026_05_05.ai.md` §3 | L23-L25 lessons banked (prose) |
| `docs/anima_session_2026_05_04_to_05_closure_audit.ai.md` §8 C2/C6 | gap callout: "banked but not yet operationalized" |
| `docs/anima_h100_concurrency_policy_2026_05_04.md` §3, §5 | per-BG BUDGET_HARD_CAP + auto-kill discipline (predecessor mandate) |
| `docs/anima_h100_idle_audit_2026_05_05.ai.md` | audit pattern reference (manual run, no auto-trigger) |
| `tool/clm_v4_lora_train_orchestrator.hexa` | recent orchestrator with heartbeat (line 41) + L13 trap (line 240+) + 404 verify (line 493+) |
| `tool/anima_runpod_orchestrator.hexa` | canonical pod-lifecycle wrapper (boot/run/terminate); patch target |
| `tool/h100_idle_guard.bash` | existing launchd reclaim wrapper — predecessor; refactor target |
| `tool/h100_auto_kill.hexa` | existing propose-only auto-kill; absorbed into watchdog reactive layer |
| `tool/h100_cost_tracker.hexa` | existing per-round aggregator; complementary to live watchdog ledger |
| `feedback_pbeta_chat_capability_fail_substrate_research_pass_decoupled.md` | sister memory; cross-link target |
| `feedback_always_subagent_bg.md` | BG dispatch mandate; §3.4 checklist update target |
| `.own own 5 + own 6 + own 14 + own 15` | predecessor own entries; own 16 candidate joins compute-lifecycle triad |
| `.roadmap.p9_sft` + `.roadmap.training` | additive cross_link annotation targets (Phase 5.2 / 5.3) |

---

**End of spec.** Implementation kicks off via Phase 1 ($0 mac, ~2h hexa watchdog + auto-pauser emission); Phase 4 smoke at $1-3 H100 confirms full L23/L24/L25 enforcement closure.
