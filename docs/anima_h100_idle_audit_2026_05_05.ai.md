# H100 Idle Audit 2026-05-05 — Companion Handoff

**Lane**: BG-H100-IDLE-AUDIT
**Audit ts**: 2026-05-05T01:45:00Z
**Verdict**: `state/h100_idle_audit_2026_05_05/verdict.json`

## Findings

- **1 pod total** running on RunPod (down from earlier multi-pod sessions): `szv2vyf06h35uy` (anima-pbeta-paradigm-d-50k-scaleup-2026-05-04, H100 80GB HBM3 @ $2.99/hr). Classification: **IDLE_OWNED**. No EXTERNAL_PROTECTED r=16 pods present in account inventory; α'''-EVAL-FIX pod has already terminated.

- **Active expected pods** for this session: only Pβ-SCALE 50K (szv2vyf06h35uy). EVAL-FIX + r=16 retrain pods are absent from pod list — already cleaned up upstream.

- **Idle/stale found**: YES — 1 IDLE_OWNED pod. Training completed successfully at 2026-05-04T23:47:27Z (50000/50000 steps, verdict `PRODUCTION_25K_FULL_PASS`, COMPLETE.sentinel persisted, final adapter at `/workspace/p9_pbeta_distill/savepoints/step_50000`). Last heartbeat 23:47:20Z. Now ~2h post-completion: 0% GPU util, 0 MiB GPU mem, no python/train processes, no mac orchestrator owning the pod. **Burning $2.99/hr for nothing**; ~$5.86 already wasted since completion.

- **Recommended kill commands (NOT executed)**:
  1. **PRE-KILL PULL** (mandatory unless HF upload confirmed): `rsync -avz -e 'ssh -i /Users/ghost/.runpod/ssh/RunPod-Key-Go -p 17478' root@103.207.149.79:/workspace/p9_pbeta_distill/results/ /Users/ghost/core/anima/state/p9_pbeta_paradigm_d_50k_2026_05_04/results/ && rsync -avz -e 'ssh -i /Users/ghost/.runpod/ssh/RunPod-Key-Go -p 17478' root@103.207.149.79:/workspace/p9_pbeta_distill/savepoints/step_50000/ /Users/ghost/core/anima/state/p9_pbeta_paradigm_d_50k_2026_05_04/savepoints/step_50000/`
  2. **KILL**: `RUNPOD_API_KEY=$(/Users/ghost/core/secret/bin/secret get runpod.api_key --raw) /opt/homebrew/bin/runpodctl pod delete szv2vyf06h35uy`
  3. **Estimated savings if executed within next 60min**: ~$2.99/hr ongoing avoided (i.e., ~$71.76 over the next 24h if left alive vs killed now).

- **Honest C3 (≥5)**:
  - C3-1: Pod state can flip mid-audit; verdict snapshot is 01:44 UTC.
  - C3-2: SSH liveness used 10s timeout; a slow-hanging python could have been missed. Cross-checked with `ps auxf` (only sshd+bash visible) — strong signal no work is running.
  - C3-3: External r=16 retrain pods (s43, s44) NOT in pod list — likely already terminated. No EXTERNAL_PROTECTED action needed.
  - C3-4: runpodctl pod list cache may lag by seconds; corroborated via `pod get` which agreed.
  - C3-5: Cost calc excludes pre-emption refund credits, egress, storage charges; true ongoing savings if killed = ~$2.99/hr.
  - C3-6: Audit did NOT pull results back to mac — KILL_NOW_DISCARD without pull will lose verdict.json + trajectory.json + final adapter (50K steps, 7.3GB workspace).
  - C3-7: No HF Hub upload was verified — cannot confirm adapter was already pushed. User should check HF repo before discarding.

## Decision options for user

1. **PULL_RESULTS_THEN_KILL** (recommended default): rsync results+adapter → mac, then `runpodctl pod delete szv2vyf06h35uy`. Saves $2.99/hr ongoing, preserves Pβ 50K verdict for downstream eval/HF upload. ETA ~5–10 min for rsync (7.3GB workspace; final adapter only is much smaller).
2. **KEEP_ALIVE_FOR_HF_UPLOAD**: leave pod running and run HF upload from H100 (faster bandwidth than mac). Recommend only if HF push will be initiated within ~1h; otherwise pure waste.
3. **KILL_NOW_DISCARD**: kill immediately without pull. **Only safe if HF Hub already received the adapter+verdict** for `anima-pbeta-paradigm-d-50k-scaleup`. Otherwise loses 50K-step training output.

**No auto-kill executed in this BG (per raw#15 destructive-op rule).**
