---
date: 2026-05-05
agent: BG-PBETA-RESCUE-KILL
cycle: p9_pbeta_paradigm_d_50k_rescue_kill_2026_05_05
status: LANDED — POD_KILLED_404_VERIFIED + SAVEPOINTS_LOCAL
ssot_artifact: state/p9_pbeta_paradigm_d_50k_rescue_kill_2026_05_05/verdict.json
predecessor: state/p9_pbeta_paradigm_d_50k_2026_05_04/results/verdict.json (PRODUCTION_25K_FULL_PASS @ step 50000)
pod_id: szv2vyf06h35uy
training_completed_utc: 2026-05-04T23:47:25Z
manual_kill_utc_estimate: 2026-05-05T18:05:00Z
---

# PBETA paradigm-D 50k rescue-kill LANDED (2026-05-05)

## §1 Headline

- **rsync DONE**: `savepoints/final/` + `savepoints/step_50000/` pulled local (193MB each, all 7 state files per dir present, adapter_model.safetensors 76.06MB)
- **manual kill 404 VERIFIED**: pod `szv2vyf06h35uy` terminated foreground after BG-PBETA-RESCUE-KILL was rate-limited mid-flight (rsync completed, pod-stop did not)
- **post-completion idle burn ~$54.72** estimate (18.30h × $2.99/hr H100 community spot) — significantly above $5-7 spec anticipation; rsync local mtime 17:51Z bounds lower kill time, training finished 2026-05-04T23:47:25Z
- **T-2 PBETA-HOLDOUT500-EVAL launch eligible**: savepoints local + integrity-verified, ready for downstream F-D-1 per-token KL ≤0.5 nats vs Mistral-7B reference cycle (the production gate, NOT this rescue-kill)
- training-side verdict `PRODUCTION_25K_FULL_PASS` carried forward; phi_star_h100_probe_final min=35.54 mean=36.74; F1_bleu1=0.0039 (CLM-self holdout proxy)

## §2 Honest C3 (raw#10)

- C1 BG rate-limit happened mid-flight AFTER rsync but BEFORE `runpodctl pod stop` — L19+L23 lesson: BG-completion-but-pod-still-up is an unguarded transition state; future trap design must foreground-fallback the kill step
- C2 idle burn $54.72 estimate vs spec's $5-7 anticipation = ~10x overrun; root cause is BG monitor not detecting completion-then-stall state, not rsync slowness (rsync completed normally per local mtime)
- C3 manual kill UTC 2026-05-05T18:05Z is best-estimate from rsync local mtime 17:51Z + observed ~14min kill-execution lag; exact `runpodctl pod delete` timestamp not captured in local logs — authoritative timestamp would require operator terminal records
- C4 savepoint integrity verified by file-presence + size only; SHA256 cross-check against pod-side originals impossible (pod terminated, originals gone) — true integrity pending downstream re-load smoke test in T-2 cycle
- C5 training graceful_shutdown=False but aborted=False — train loop exited normally at step 50000, FINAL adapter saved before trap, rsync narrowly completed before BG rate-limit; trap pre-kill scp (L13) never invoked because BG monitor died before trap would have fired
- C6 phi_star_h100_probe_final values are H100-side measurements; cross-substrate drift expected per eeg.cond.4 sample-partition phi proxy lesson — true verdict pending Mac/CPU re-measurement in T-2

## §3 Lessons banked (forward)

- **L23 rate-limit-resilience-via-foreground-fallback**: any BG that ends in `runpodctl pod stop+delete` MUST have a foreground-fallback path that operator can invoke at any rate-limit boundary; document the fallback command literally in the BG spec so operator can copy-paste without re-deriving pod ID
- **L24 BG-completion-detection vs pod-state-detection separation**: BG monitor tracks BG process exit; pod-state monitor tracks runpodctl pod existence; conflating these creates the 18h idle-burn gap observed here. Future BG specs should require BOTH signals before declaring "rescue done"
- **L25 cost-overrun honest-C3 inflation**: when actual idle burn exceeds spec estimate by >2x, escalate to user with concrete numbers (h, $, gap-cause) rather than burying in C3 notes — done here in §1 headline but should be standard

## §4 Cross-link

- Training cycle SSOT: `state/p9_pbeta_paradigm_d_50k_2026_05_04/results/verdict.json`
- Savepoints local: `state/p9_pbeta_paradigm_d_50k_2026_05_04/savepoints/{final,step_50000}/`
- This rescue verdict: `state/p9_pbeta_paradigm_d_50k_rescue_kill_2026_05_05/verdict.json`
- Next: T-2 PBETA-HOLDOUT500-EVAL (F-D-1 per-token KL ≤0.5 nats vs Mistral-7B; CPU/Mac substrate; the production gate)
