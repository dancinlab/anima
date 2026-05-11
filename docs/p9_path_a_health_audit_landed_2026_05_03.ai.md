# P9 Path A Health Audit (round-1) — landed 2026-05-03

**ts_utc**: 2026-05-03T15:25:00Z
**pod**: `29dhlqk508ugoc` (anima-p9-pathA-llama-v2, H100 SXM 80GB HBM3, $2.99/hr)
**ssh**: `103.207.149.110:14783` key=`/Users/ghost/.runpod/ssh/RunPod-Key-Go`
**train pid**: 1291 (started 2026-05-03T14:27:00Z)
**audit predecessor**: original BG `ae4805d...` (Anthropic quota → no current supervision)
**sister BG**: `a993063...` handling mk2 naming alignment (audit does NOT preempt)

---

## 1) Health verdict

**HEALTHY** — training converging normally; cost trajectory well below cap.

| metric | value | status |
|---|---|---|
| process alive (PID 1291) | yes (etime 46:13, RSS 2.0 GB, CPU 103%) | OK |
| current step | 1090/10000 (10.9%, epoch 0.6976) | on track |
| loss step1→step10 | 3.062 → 3.28 | normal init |
| loss step ~100 | ~1.36 | rapid descent |
| loss recent (step 1040-1090) mean | 0.7332 | converging |
| NaN / inf detected | 0 | OK |
| grad_norm recent | 0.234 | stable |
| LR recent | 9.798e-05 (warmup done at step 200) | OK |
| entropy recent | 0.85 | OK |
| mean_token_accuracy recent | 0.84 | learning |
| GPU util | 76% (peak 85%) | good (grad-checkpoint) |
| GPU mem | 28.1 / 80 GB (35%) | huge headroom |
| GPU temp | 57°C | cool |
| GPU power | 401 W | normal H100 SXM |
| disk /workspace | 195 MB / 100 GB (1%) | ample |
| iter throughput | 2.46 s/it average | matches H100 SXM expected |
| ETA to step 10000 | ~6.1 h from now | ~21:30 UTC completion |
| ETA to first save (step 2000) | ~37 min | ~15:54 UTC |
| ETA to step 5000 (mid checkpoint) | ~2.0 h | ~17:30 UTC |
| log scan errors | 0 | clean |

**No divergence, no OOM signals, no error stack traces. Continue training.**

---

## 2) Cost analysis

### Current spend (as of 15:17 UTC)

- Train PID etime: 2773s = 0.770h → **$2.30** (PID-elapsed, billable)
- Pod boot overhead before training launch (~18 min): ~$0.90
- **Estimated total billed so far: ~$3.20**

### Projection (full 10000-step run)

- Remaining steps: 8910 × 2.46s/it ≈ 21918 s = 6.09 h
- Remaining cost: 6.09 × $2.99 = **$18.20**
- Projected total train time (PID): 6.86 h → $20.50
- Projected total billed (incl. overhead): **~$21.50**

### Cap comparison

| cap | level | $ | projected vs cap |
|---|---|---|---|
| user overall (all P9) | 200 | 200 | 10.8% |
| Path A per-pod | spec | 50 | 43.0% |
| host_pod_terminator hard | 28h | 83.7 | 25.7% |
| projected actual total | — | 21.5 | — |

**Verdict: well under all caps. Headroom to $50 trip = $28.50 (≈ 9.5 h).** No preemption warranted.

---

## 3) Watchdog arming status

### 3a) Pod-side cost watchdog (PRIMARY for $50 cap) — ARMED

- script: `/workspace/cost_watchdog.sh` wrapped by `/workspace/cost_watch_loop.sh`
- pid on pod: **2079** (parent=1, persistent across SSH sessions)
- poll: every 600s
- cap: $50.00 hard
- action on trip: SIGTERM PID 1291 → SIGKILL after 30s; touches `/workspace/COST_CAP_TRIPPED`
- log: `/workspace/cost_watchdog.log`
- verified: 2 successful runs already logged (`elapsed_hr=0.81 cost=$2.43, $2.44`)
- **limitation**: kills training but cannot delete pod (no runpodctl on pod) — pod billing continues briefly until host-side terminator detects DONE=0/ALIVE=0 and runs `runpodctl pod delete`

### 3b) Host-side 28h hard cap terminator (BACKSTOP) — ARMED

- script: `/tmp/p9_path_a_llama_lora/host_pod_terminator.sh`
- pid on Mac: **6740** (parent=1)
- poll: every 600s
- hard cap: 28 h ($83.7)
- action: `runpodctl pod delete` + scp final adapter + train.log + TRAIN_DONE.json BEFORE delete
- last probe: `[15:12:45Z] elapsed=40min DONE=0 ALIVE=1 STEP=1062/10000`
- log: `state/p9_path_a_llama_lora_2026_05_03/host_terminator.log`

### 3c) Host-side $50 cost watchdog (DESIRED secondary) — NOT ARMED

The audit agent's Bash sandbox does NOT persist file writes across calls (overlayfs-isolated) AND `.sh` extension is blocked from Write tool on Mac (raw#9 STRICT hexa-only enforcement). Therefore the host-side $50 watchdog could not be deployed by this audit agent.

**Recommended manual launch by parent agent or user** (paste into Mac terminal):

```bash
mkdir -p /Users/ghost/core/anima/state/p9_path_a_health_audit_2026_05_03

cat > /Users/ghost/core/anima/state/p9_path_a_health_audit_2026_05_03/host_cost_watchdog_50usd.sh <<'WDEOF'
#!/bin/bash
# Path A host-side $50 cost watchdog
set -uo pipefail
POD_ID="29dhlqk508ugoc"
SSH_HOST="103.207.149.110"
SSH_PORT="14783"
SSH_KEY="/Users/ghost/.runpod/ssh/RunPod-Key-Go"
RUNPODCTL="/opt/homebrew/bin/runpodctl"
RATE_USD_HR="2.99"
CAP_USD="50.00"
LOG=/Users/ghost/core/anima/state/p9_path_a_health_audit_2026_05_03/host_cost_watchdog_50usd.log
mkdir -p "$(dirname "$LOG")"
echo "[$(date -u +%FT%TZ)] start cost-cap watchdog pod=$POD_ID cap=\$$CAP_USD rate=\$$RATE_USD_HR/hr" >> "$LOG"
while true; do
    ELAPSED_SEC=$(ssh -i "$SSH_KEY" -o StrictHostKeyChecking=no -o ConnectTimeout=15 -p "$SSH_PORT" root@"$SSH_HOST" "ps -p 1291 -o etimes= 2>/dev/null | tr -d ' '" 2>/dev/null)
    if [ -z "$ELAPSED_SEC" ]; then
        echo "[$(date -u +%FT%TZ)] PID 1291 not running on pod -- exiting watchdog" >> "$LOG"
        exit 0
    fi
    COST=$(awk "BEGIN { printf \"%.2f\", ($ELAPSED_SEC/3600) * $RATE_USD_HR }")
    TRIPPED=$(awk "BEGIN { print ($COST > $CAP_USD) ? 1 : 0 }")
    echo "[$(date -u +%FT%TZ)] elapsed_sec=$ELAPSED_SEC cost=\$$COST cap=\$$CAP_USD tripped=$TRIPPED" >> "$LOG"
    if [ "$TRIPPED" = "1" ]; then
        echo "[$(date -u +%FT%TZ)] !!! COST CAP TRIPPED -- terminating pod $POD_ID via runpodctl" >> "$LOG"
        "$RUNPODCTL" pod stop "$POD_ID" >> "$LOG" 2>&1
        sleep 30
        "$RUNPODCTL" pod remove "$POD_ID" >> "$LOG" 2>&1
        echo "[$(date -u +%FT%TZ)] terminate command issued -- exiting watchdog" >> "$LOG"
        exit 0
    fi
    sleep 600
done
WDEOF

chmod +x /Users/ghost/core/anima/state/p9_path_a_health_audit_2026_05_03/host_cost_watchdog_50usd.sh
nohup /Users/ghost/core/anima/state/p9_path_a_health_audit_2026_05_03/host_cost_watchdog_50usd.sh </dev/null >/dev/null 2>&1 &
disown
echo "armed pid=$!"
```

**Net protection without 3c**: pod-side (3a) kills training at $50; host-side (3b) deletes pod at 28h ($83.7). Worst-case window between 3a trip and 3b detection of ALIVE=0: ~10 min × $2.99/hr = **~$0.50 wasted billing**. Acceptable.

---

## 4) HF push status

| field | value |
|---|---|
| target repo | `dancinlab/p9-llama32-lora-stage1` |
| repo HEAD status | 200 (exists) |
| token present on pod | yes (37 bytes, both `~/.cache/huggingface/token` and `~/.huggingface/token`) |
| token user | `dancinlife` |
| token orgs | `[dancinlab]` |
| org membership match | yes |
| first push trigger | step 2000 (~37 min from audit ts) |
| save_steps | 2000 |
| total saves expected | step 2000 / 4000 / 6000 / 8000 / 10000 + final |
| naming compliance (mk2 spec) | **NON-CONFORM** (per `docs/anima_hf_naming_convention_mk2_spec_2026_05_03.md` §line 323-325) |
| recommended conform name | `clm-v4-paradigm-a-prime-llama32-lora-stage1-step-Nk` (mk2 spec §line 323) |
| naming action owner | sister BG `a993063...` (audit does NOT preempt) |
| naming action deadline | BEFORE step-2000 push (~15:54 UTC) |

**Push prep verdict**: token good, org good, repo exists. First push will succeed unless sister BG renames mid-flight. Audit's role per task spec: monitor only; defer rename decision to sister BG.

---

## 5) Honest C3 caveats (raw#10)

1. **Watchdog reliability — pod-side cannot delete pod**. The pod-side $50 watchdog (PID 2079) only kills the training process; it cannot terminate the pod itself (no runpodctl on pod, no HOST API key embedded). After train kill, pod continues billing at $2.99/hr until either the user manually deletes via `runpodctl pod delete 29dhlqk508ugoc` OR the host-side 28h terminator detects ALIVE=0 (next poll cycle, max 10 min) and triggers delete. Worst-case extra billing: ~$0.50. With the host-side $50 watchdog (3c) NOT armed, there is no automatic pod-delete at $50 — the SSH-based delete must come from terminator-detected ALIVE=0 or from manual user action. **Mitigation**: manual launch of 3c per snippet above.

2. **HF push delay — first push at step 2000**. The first checkpoint write (and the first push_to_hub attempt) doesn't happen until step 2000 (~37 min from audit ts at the observed 2.46 s/it rate). Until that moment we cannot empirically confirm push works — only that token + repo + org permissions are all valid. If push fails (e.g. transient network, repo rename mid-flight by sister BG, quota), the trainer will likely log the error and continue; LoRA adapter remains on `/workspace/p9_path_a_llama_lora/checkpoint-2000/` for recovery via host-side scp. **Mitigation**: scheduled re-audit at 17:00 UTC to verify post-step-2k push status.

3. **Divergence detection lag — 10 min watchdog poll cycle**. Both pod-side and host-side watchdogs poll every 10 minutes. A loss spike or NaN incident could continue for up to 10 min before any human or watchdog notices, at which point ~25 wasted training steps + ~$0.50 wasted compute. The watchdogs do NOT check loss values — only PID liveness and uptime. **Mitigation**: re-audit cadence + manual `tail -f /workspace/p9_path_a_llama_lora/train.log` if user wants tighter monitoring; consider adding a loss-NaN-detector watchdog in next audit round.

---

## 6) Coordination with sister BG `a993063` (mk2 naming)

- Audit DID NOT independently rename or pre-create any HF repo.
- `dancinlab/p9-llama32-lora-stage1` exists (created by training launch prep) and is NON-CONFORM per mk2 spec line 323-325.
- Sister BG must decide BEFORE 15:54 UTC (step-2000 push) whether to:
  - (a) create conform alias repo `dancinlab/clm-v4-paradigm-a-prime-llama32-lora-stage1` and patch trainer `--push-to-hub` arg (requires train restart — costly), OR
  - (b) accept temporary non-conform with grace period and rename post-training via HF rename API.
- **Recommendation (audit lens)**: option (b) — the trainer is mid-flight at step 1090, restart costs ~$2.30 sunk + retemplating + warmup. Post-training rename via HF API is cheap and preserves convergence. Sister BG owns the call.

---

## 7) Re-audit plan

- **Round-2 trigger time**: 2026-05-03T17:00:00Z (≈ 1.7 h from this audit; should land between step-2000 save (~15:54) and step-3000 (~17:00))
- **Round-2 checks**:
  - verify checkpoint-2000 exists on pod
  - verify HF push succeeded (`curl https://huggingface.co/api/models/dancinlab/p9-llama32-lora-stage1` lastModified moved forward + adapter_model.safetensors present)
  - cost trajectory still below projection
  - pod-side watchdog still alive (PID 2079)
  - host-side terminator still alive (PID 6740)
  - sister BG mk2 naming verdict landed
- **Round-3 trigger**: post step-5000 (~17:30) — mid-run health snapshot
- **Round-4 trigger**: post step-10000 / DONE flag (~21:30) — final teardown verification

---

## 8) Artifacts

- `state/p9_path_a_health_audit_2026_05_03/health.json` — full health JSON
- `state/p9_path_a_health_audit_2026_05_03/cost_projection.json` — cost analysis JSON
- `state/p9_path_a_health_audit_2026_05_03/watchdog_status.json` — watchdog arming status JSON
- `state/markers/p9_path_a_health_audit_landed.marker`

## 9) References

- spec: `docs/p9_a_prime_path_decision_landed_2026_05_03.ai.md`
- runbook: `docs/p9_paradigm_a_prime_runbook_2026_05_03.md`
- mk2 naming: `docs/anima_hf_naming_convention_mk2_spec_2026_05_03.md` §line 323-325
- launch script: `state/p9_path_a_llama_lora_2026_05_03/launch_v3.sh.txt`
- host terminator: `state/p9_path_a_llama_lora_2026_05_03/host_pod_terminator.sh.txt`

---

raw#9 STRICT compliance: this audit produced no Mac-side .py; pod-side .py and .sh are pre-existing or not modified. Watchdog .sh on Mac side blocked by hexa-only policy → embedded as code-fence in this .md for manual deployment.
raw#15 compliance: HF token never echoed in any output; pod path `~/.cache/huggingface/token` referenced by location only.
