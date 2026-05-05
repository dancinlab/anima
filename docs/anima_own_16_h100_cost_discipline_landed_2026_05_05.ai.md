---
title: anima own 16 — H100 cost discipline L23/L24/L25 watchdog admission LANDED
cycle: 2026-05-05
ts: 2026-05-05T_own_16_admission_landed
bg_lane: BG-OWN-16-ADMISSION
substrate: mac (admission only — $0, no exec, no commit, no roadmap mutation)
status: LANDED
type: own_admission_handoff
predecessor:
  - docs/anima_h100_cost_discipline_operationalization_spec_2026_05_05.md (BG-COST-DISCIPLINE-OPERATIONALIZE — own 16 candidate proposal source)
  - docs/p9_pbeta_paradigm_d_50k_rescue_kill_landed_2026_05_05.ai.md (L23-L25 lessons banked)
  - state/p9_pbeta_paradigm_d_50k_rescue_kill_2026_05_05/verdict.json (Pβ rescue idle burn $54.72 incident SSOT)
  - .own own 14 (HF Hub WHERE) + own 15 (HF lifecycle HOW) — sister external-resource-consumption mandates
related:
  - tool/h100_cost_watchdog.hexa (Phase 1 PROPOSED — separate process, 5min poll, pure bash daemon hot path)
  - tool/h100_idle_auto_killer.hexa (Phase 1 PROPOSED — escalation ladder executor)
  - tool/clm_v4_lora_train_orchestrator.hexa (Phase 2 integration target)
  - tool/anima_runpod_orchestrator.hexa (Phase 2 integration target)
  - tool/h100_idle_guard.bash + tool/h100_auto_kill.hexa + tool/h100_cost_tracker.hexa (existing tooling overlap — Phase 1 must explicit retire/absorb per spec C8)
raw_invariants:
  - raw#9 (md only this cycle, no code emission)
  - raw#10 (≥5 honest C3 in §honest_c3)
  - raw#15 (additive only — own 1-15 verbatim preserved, no roadmap mutation, no exec)
---

# anima own 16 admission — H100 cost discipline L23/L24/L25 watchdog (2026-05-05)

## Summary

- **own 16 added to .own** — additive append at line 570+ (own 1-15 verbatim preserved per raw#15). Slug `h100-cost-discipline-l23-l25-watchdog`. Format consistent with own 14 + own 15 (slug / base / since / scope / rule / enforcement / exceptions / bans / proof / follow-up / category / applies-to / phase / severity / honest-c3 / note / why / enforce-layer). Three-phase enforcement ladder declared: Phase 1 (new tooling — h100_cost_watchdog.hexa + h100_idle_auto_killer.hexa) → Phase 2 (existing orchestrator integration boot/heartbeat/trap/verdict) → Phase 3 (BG launch prompt template L23/L24/L25 checklist mandatory).
- **memory entry written** at `/Users/ghost/.hive/claude-config/hive-hook-bus/projects/-Users-ghost-core-anima/memory/feedback_h100_cost_discipline_l23_l25_watchdog_own_16.md` + **MEMORY.md updated** with new line linking to the entry. Memory frontmatter (name / description / type=feedback) consistent with sister entries feedback_anima_models_datasets_hf_only.md (own 14) + feedback_hf_release_private_to_public_after_verification.md (own 15).
- **Sister own 14 + own 15 + own 16 = external-resource-consumption axes triad formed** — own 14 = storage WHERE (HF Hub) + own 15 = publication HOW (PRIVATE→PUBLIC lifecycle) + own 16 = compute lifecycle (boot→heartbeat→exit→404-verify). All three are post-dispatch lifecycle enforcement complementing own 6 (pre-dispatch autonomous GPU policy). own 16 + own 6 form pre/post-dispatch GPU lifecycle pair.
- **Pβ $54.72 incident precedent cited** — state/p9_pbeta_paradigm_d_50k_rescue_kill_2026_05_05/verdict.json captures the raw incident: Pβ Paradigm D 50K completed successfully at 2026-05-04T23:47:25Z, pod alive 18.30h until manual rescue-kill at 2026-05-05T18:05:00Z, $54.72 idle burn = 65% of total session H100 spend (~$83-85). Root cause = BG agent rate-limited (Anthropic 429) at the kill-pod step after rsync completed. own 16 is the operationalization gap closure for L23/L24/L25 lessons that were prose-banked in verdict.json honest_c3 but not enforcement-enforced.
- **handoff doc landed** — this doc (status: LANDED, additive-only per raw#15, no commit, no exec).

## Honest C3 (raw#10 ≥5 disclosure)

1. **Watchdog polling overhead is trivial but scales linearly** — at 1 pod = 12 polls/hour, at 10 concurrent pods = 120 polls/hour. Still negligible vs runpodctl rate-limit headroom, but worth tracking once we routinely run >20 concurrent BGs.

2. **Auto-pause vs auto-kill trade-off chosen pause-first** — pause preserves in-flight work (operator option to resume + rsync) but extends cost a bit longer until 24h grace expires; kill terminates cost immediately but loses unsaved progress. own 16 chose pause-first because the Pβ incident actually completed training successfully BEFORE idle burn began — a kill-first policy on partial-state pods could lose the FINAL adapter pre-rsync. The honest cost is that 24h grace × $2.99/hr = up to $71.76 additional burn per stuck pod if user is unresponsive (still better than $54.72×N stuck pods over multi-day audit cycle).

3. **Watchdog process itself can recursively rate-limit-fail** — if implemented as Anthropic-API-calling BG, the watchdog hitting 429 would create a meta-failure (the watchdog watching the watcher problem). Mitigation: pure bash daemon hot path (no API calls in the polling loop), hexa surface only for selftest/admin one-shots. spec C4 acknowledges and mitigates. NOT a complete fix — bash daemon itself can crash; cron + launchd respawn convention partially mitigates but creates its own failure modes.

4. **Cost-overrun threshold 2× / 3× heuristic NOT principled** — chosen empirically against Pβ's 10× incident (target ~$5-7, actual $54.72). May need recalibration after first 30d production data; threshold likely should differ per training-cycle class (smoke <$5 budget should trip earlier in absolute terms; full-train <$200 should allow more headroom proportionally). Phase 1 implementation should expose threshold as per-pod config, not global constant.

5. **Retroactive operationalization (reactive not proactive)** — L23-L25 lessons were banked in Pβ rescue verdict.json honest_c3 FIRST, then own 16 operationalizes them AFTER the $54.72 loss. Future incident classes likely follow the same pattern (bank L26+ lessons → operationalize as own 17+ after sufficient cost signal). The honest framing: anima self-improvement loop is reactive at the autonomy-mandate level, not predictive.

6. **Existing tooling overlap creates SSOT race risk** — tool/h100_idle_guard.bash + tool/h100_auto_kill.hexa + tool/h100_cost_tracker.hexa already exist with partial overlap to the proposed h100_cost_watchdog.hexa + h100_idle_auto_killer.hexa. Phase 1 ships without explicit retire/absorb decision = three watchdogs racing each other. Spec C8 calls this out as deferred-to-Phase-1 design choice, but the gap is real and could cause double-kill or split-brain registry state.

7. **Phase 3 prompt template enforcement relies on human discipline** — no tool can enforce a checklist on a free-form Agent run_in_background prompt. Mitigation = stamp template into BG subagent system prompt convention (raw#-future), but until that convention is concrete the L23/L24/L25 checklist is as enforceable as the operator remembering to include it. The honest framing: own 16 enforcement Phase 3 is convention-level, not tool-level.

## Triad summary

```
external-resource-consumption axes triad (anima 2026-05):

own 14 — storage WHERE         own 15 — publication HOW       own 16 — compute lifecycle
HF Hub mandate                 PRIVATE→PUBLIC after gates     boot→heartbeat→exit→404-verify
(weights + datasets >5MB)      (verification suite ALL PASS)  (L23/L24/L25 enforcement)

      \                              |                              /
       \                             |                             /
        \____________________________|____________________________/
                                     |
                          post-dispatch lifecycle
                                     |
                              own 6 (pre-dispatch
                              autonomous GPU policy)
```

own 14 + own 15 + own 16 are all post-dispatch lifecycle mandates. own 6 is the pre-dispatch autonomy mandate. Together they form the complete anima external-resource-consumption discipline stack (pre-dispatch authorization + post-dispatch storage + publication + compute lifecycle).

## Status

LANDED. own 16 admission complete. Phase 1 / Phase 2 / Phase 3 implementation deferred to subsequent BG cycles per spec docs/anima_h100_cost_discipline_operationalization_spec_2026_05_05.md.
