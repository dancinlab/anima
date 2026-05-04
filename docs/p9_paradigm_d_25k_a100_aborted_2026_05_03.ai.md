# P9 Paradigm D 25K A100 Distill — ABORTED (Pre-Training Spot Preempt + Cycle Cost Cap Risk)

**Date**: 2026-05-03
**Phase**: `p9_paradigm_d_25k_a100_2026_05_03`
**Verdict**: `ABORTED_PRE_TRAINING_SPOT_PREEMPT_DURING_TRANSFER`
**Substrate intended**: NVIDIA A100-SXM4-80GB community spot @ $0.79/hr
**Cycle cost actual**: $1.72 (well under $14.50 cap)
**Marker**: `state/markers/p9_paradigm_d_25k_a100_aborted.marker`

---

## TL;DR

Spot stock VERIFIED available at $0.79/hr (well below $0.85 cap). Pod created cleanly on first attempt. SSH worked, deps installed, ubu1→pod rsync streaming proven. **However**, the pod was preempted ~30 min after boot, while `best.pt` (5.0GB) was at 56% transfer. Pod fully terminated (volume gone). On reflection of (slow ubu1 home upload @ 7 MB/s × unpredictable spot preempt within 30 min) the structural unreliability cannot guarantee $14.50 cap compliance for an 18h training run. **Aborted on completion-quality grounds** (not stock grounds — A100 spot IS available).

## Pod Lifecycle (this cycle)

| Pod ID | Status | Notes |
|---|---|---|
| `99ziv0qfjnjbbf` | terminated | First attempt — missing `PUBLIC_KEY` env, sshd authorized_keys empty, SSH refused |
| `7ubgzj4s8spb4p` | preempted | Second attempt — PUBLIC_KEY set, ssh ok, deps installed, transfer at 56% then preempted at ~30 min uptime |
| `2au2y1ur428k7m` | terminated by us | Third attempt — re-rented after preempt, then terminated as part of abort decision |
| `29dhlqk508ugoc` | terminated independently | Pre-existing Path A pod (NOT touched by this BG), found gone at cycle close |
| `fuewrx9moxe6gz` ⚠ | RUNNING at cycle close | H100 SXM secure $2.99/hr, **NOT created by this BG** — likely sister BG a686f9030 fall-back; flagged for user reconciliation |

## Deliverables Completed

- A100 SXM4 80GB community spot stock VERIFIED ($0.79/hr, 3 successful pod_rent calls)
- Pod provisioning workflow validated (PUBLIC_KEY env required for sshd auto-bootstrap; ~2 min from rent to ssh ready)
- Pod dep install proven: peft 0.13.0 + transformers 4.45.2 + sentencepiece + rsync (~90s on first boot)
- ubu1→pod direct SSH trust established (ed25519 pubkey + hostkey scan)
- Bundle staged on ubu1 `/tmp/anima_bundle_a100/` (5.13 GB total — preserved for next-cycle re-attempt)
- Launch wrapper authored: `/tmp/launch_a100_distill.sh` (sets ANIMA_RATE_USD_PER_HR=0.79, COST_CAP_USD=14.50, WALL_MAX_SEC=64800; setsid+nohup+disown for full detach)

## Deliverables Blocked by Abort

- No successful boot-to-train cycle (transfer never completed before preempt)
- No initial 1K-step loss measurement (training never started)
- No F1 holdout / KL eval (no production weights produced)

## Preempt Event Detail

- ts_utc: 2026-05-03T15:54:30Z
- pod_id: 7ubgzj4s8spb4p
- uptime at preempt: ~30 min
- transfer progress: 2,996,568,064 / 5,365,727,261 bytes (55.9%)
- rsync exit: code 255, "Connection to 216.249.100.66 closed by remote host; Broken pipe"
- pod state immediately after: `pod=null` (full termination, /workspace volume gone)
- preempt signal received by training script: false (training never started)

## Next Actions (Ranked by Completion Quality)

1. **HF Hub pre-stage** (rank 1, recommended): One-time upload of `best.pt` from ubu1 to HF Hub private repo (slow but one-time); subsequent A100 spot pod boots download from HF Hub at 100+ MB/s pod-side. Cuts re-transfer cost from 15 min to 5 min on every preempt. Spec-compliant. ETA total: ~20h, cost ~$14.
2. **Network volume** (rank 2): Pre-create RunPod 100GB network volume, upload best.pt once, mount on every spot pod (volume survives pod termination). Best preempt resilience. Caveat: locks pods to a specific datacenter. Cost: ~$10/month/100GB + spot hourly.
3. **Run on ubu1 RTX 5070** (rank 3): No preempt, $0 cost; 50-100h wall clock vs 18h on A100. Already validated on v1 mini-run.
4. **Wait-and-retry A100 spot** (rank 4): Current loop; high variance time-to-success; risks blowing cap with multiple preempts.
5. **Fall back to H100/A100 on-demand** (rank 5, **VIOLATES SPEC**): ~$2-3/hr, no preempt; only mention as user-decision option.

**Recommendation**: RANK 1 (HF Hub pre-stage). It preserves spec compliance ($0.79/hr A100 spot), eliminates the slow-uplink × preempt-risk multiplier, and the one-time HF upload investment becomes permanent infrastructure for future runs.

## Honest C3

1. A100 SXM4 80GB community spot IS structurally available at $0.79/hr — NOT supply-constrained (vs HBM3 yesterday).
2. Pre-train preempt is rare but does happen — bad luck or weak machine; either way, plan for it.
3. ubu1 home upload @ 7 MB/s avg is a binding constraint; even without preempts, 12 min full transfer.
4. RunPod spot pod `/workspace` volume is NOT preserved across full pod termination — must use network volume for pre-staged data.
5. Cycle cost: $1.72 (3 pods × short uptimes). Balance went $345.13 → $343.41. Well under $14.50 cap.

## Cross-BG Concern

At cycle close, pod `fuewrx9moxe6gz` (H100 SXM secure, $2.99/hr, AP-IN-1) was RUNNING in the account. **This BG did NOT create it.** Likely sister BG a686f9030 fell back to H100 secure despite the spec saying "ABORT if HBM3 community unavailable; do NOT fall back to secure or NVL". User/orchestrator should reconcile whether to terminate it or keep it.

## Files

- Verdict: `state/p9_paradigm_d_25k_a100_2026_05_03/verdict.json`
- Pod metadata: `state/p9_paradigm_d_25k_a100_2026_05_03/pod_metadata.json`
- Launch attempt log: `state/p9_paradigm_d_25k_a100_2026_05_03/launch_attempt_log.jsonl` (13 events)
- Marker: `state/markers/p9_paradigm_d_25k_a100_aborted.marker`
- Handoff (this file): `docs/p9_paradigm_d_25k_a100_aborted_2026_05_03.ai.md`
- ubu1 staged bundle: `/tmp/anima_bundle_a100/` (preserved, 5.13 GB)
- Launch wrapper: `/tmp/launch_a100_distill.sh` (Mac-local; ready to scp to next pod)
- Reused script: `/tmp/p9_paradigm_d_distill_v2.py` on ubu1 (1071 LoC, RESUME SCAFFOLDING — unchanged from sister BG)
- Reused watchdog: `/tmp/distill_watchdog.sh` on ubu1 (env-var driven, supports A100 rate override)
