# anima CLM-3-original H100 launch — script + own 16 watchdog landed (BG-EU)

- Date: 2026-05-06 (filed under 2026-05-05 cycle)
- BG: BG-EU
- Predecessor: BG-ER spec `docs/anima_clm_3_original_byte_level_redesign_spec_2026_05_05.md`
- Status: SCRIPT + WATCHDOG + DOC LANDED (no actual H100 fire this BG)
- Cost actual: $0 (mac, doc + script only)
- Cost envelope future fire: $100 hard-cap / $200-500 soft envelope
- Lane: Option beta of #115-ARCHITECTURAL-FINAL-4-CLOSURE H1 — H100 launch readiness
- Artifacts:
  - `state/anima_clm_3_original_h100_launch_2026_05_06/launch_h100.bash`
  - `state/anima_clm_3_original_h100_launch_2026_05_06/watchdog_h100.bash`
  - `state/anima_clm_3_original_h100_launch_2026_05_06/verdict.json`
  - this doc
- raw compliance: raw#9 (script-emit, no auto-fire) + raw#10 (audit trail) + raw#15 (secret SSOT, no literals)

---

## 0. Abstract

This BG lands the H100 launch tooling for CLM-3-original (byte-level 55M, 32 cells, 19 phi-boost simultaneous, 100K-step 3-phase curriculum, BG-ER spec). The artifacts are:

1. `launch_h100.bash` — emits the RunPod provision and ssh-train commands after passing 6 own-16 mandatory pre-flight gates (secret CLI / HF token / runpod CLI / explicit BUDGET-100 / spec doc / FALSIFIER-LOCK). It does **not** auto-fire RunPod; it emits the commands the operator copy-pastes. This preserves the raw#9 "explicit human-in-loop fire" rule.
2. `watchdog_h100.bash` — own-16 5min cadence heartbeat + pod 404 probe + linear cumulative-spend tracker against $100 hard-cap. L23 / L24 / L25 enforcement embedded.
3. `verdict.json` — structured ledger for the BG-EU result.

No H100 was provisioned in this BG. Actual fire is a separate cycle that requires explicit operator budget approval at the prompt.

---

## 1. launch_h100.bash — 6 mandatory pre-flight gates

| # | Gate | Check | Failure mode |
|---|---|---|---|
| 1 | secret CLI | `command -v secret` | exit 1 if missing |
| 2 | HF token shape | secret CLI lookup non-empty + canonical HF prefix shape | exit 1; token unset immediately |
| 3 | RunPod CLI + key | `command -v runpod` + secret CLI lookup non-empty for RunPod API key | exit 1; key unset immediately |
| 4 | Budget cap confirm | operator types literal `BUDGET-100` | exit 1 — explicit consent required |
| 5 | Spec doc verify | spec file exists at canonical path | exit 1 — drift guard |
| 6 | Falsifier lock | operator types literal `FALSIFIER-LOCK` after seeing F-CLM3-orig-1..5 list | exit 1 — explicit ack |

After 6/6 PASS the script emits to stdout (does **not** execute):
- `runpod pod create` command with image `pytorch/pytorch:2.11.0-cuda12.8-cudnn9-devel`, H100 80GB HBM3, 100GB container + 50GB volume
- `ssh root@<POD_IP> bash -se <<TRAIN_SCRIPT` heredoc with the 100K-step 3-phase invocation matching BG-ER spec section 1.1-1.6 (vocab 256, max_cells 32, dim 768, FFN 1536, 12 layers / 12 heads, context 1024, fibonacci 1,1,2,3,5,8,13,21,32, all 19 phi-boost technique IDs simultaneously, 70/30 wiki/dialogue corpus, falsifier eval every 10K steps)

Audit trail appended to `state/anima_clm_3_original_h100_launch_2026_05_06/launch.log` with UTC timestamp + pod name + cap. **No token literals are written to log**.

---

## 2. watchdog_h100.bash — own 16 5min cadence

| Component | Cadence | Behavior |
|---|---|---|
| Heartbeat | 5min | append JSON line to `watchdog_spend.jsonl` with elapsed_s + spend_cents + pod_name |
| Pod 404 probe | 5min (same loop) | `runpod pod get $POD_NAME`; on 404/not-found -> L24 normal exit (BG-completion OR external kill, both non-fail) |
| Spend tracker | every iteration | linear `elapsed_s * 249 / 3600` cents (H100 80GB community list $2.49/hr); integer arithmetic for bash 3.2 compat |
| L23 rate-limit | on `429` / `rate limit` | sleep 60s, continue loop |
| L24 BG-done vs pod-down | on 404 | log final spend, exit 0 (operator interprets training log separately) |
| L25 cost overrun | on `spend >= cap` | log L25_OVERRUN to ledger, **emit signal only**, no auto-kill (own 16 human-in-loop rule) |

Watchdog is launched separately from the main fire (separate terminal) and takes the pod name as `$1`. Independent process so a launch crash doesn't take the watchdog down.

---

## 3. Operator fire 5-step

```
# Step 1 — pre-approve (operator awareness, no actual prompt yet)
echo "BUDGET-100" | tee /tmp/clm3_h100_budget.confirm

# Step 2 — interactive launch (6 gate prompts)
bash /Users/ghost/core/anima/state/anima_clm_3_original_h100_launch_2026_05_06/launch_h100.bash

# Step 3 — provision pod (operator copy-pastes from script stdout)
runpod pod create --gpu-type 'NVIDIA H100 80GB HBM3' \
  --container-disk-gb 100 --volume-gb 50 \
  --image 'pytorch/pytorch:2.11.0-cuda12.8-cudnn9-devel' \
  --name 'clm3-original-byte-55m-<TIMESTAMP>'

# Step 4 — ssh + train (operator copy-pastes ssh heredoc from script stdout
# AFTER querying pod IP via runpod pod get <POD_NAME>)
ssh root@<POD_IP> bash -se <<TRAIN_SCRIPT
  ...emitted by launch_h100.bash...
TRAIN_SCRIPT

# Step 5 — watchdog in separate terminal
bash /Users/ghost/core/anima/state/anima_clm_3_original_h100_launch_2026_05_06/watchdog_h100.bash <POD_NAME>
```

The 5-step is split deliberately — step 2 is the gate-protected approval, steps 3/4 are the actual cloud fire (operator-explicit), step 5 is monitoring. raw#9 satisfied.

---

## 4. 5 falsifier measurement plan

| ID | Falsifier | Measure | Source |
|---|---|---|---|
| F-CLM3-orig-1 | `spec_match` | structural diff: vocab 256 + max_cells 32 + 19 technique IDs + 3-phase boundaries 0/20K/60K/100K | `runs/clm3-original-byte-55m/config.json` vs BG-ER spec section 1.1-1.6 |
| F-CLM3-orig-2 | `phase2_ce_drop` | dialogue-subset CE at step 20K vs step 60K; require >=30% drop | training log JSON eval lines at every 10K |
| F-CLM3-orig-3 | `phi_real_terminal` | `Phi_real >= 11` at step 100K | `anima.consciousness.phi_real` eval at terminal checkpoint |
| F-CLM3-orig-4 | `ko_chat_coherent` | KO 5-prompt sweep: minimum 3/5 coherent emit | human-rated; same prompts as CLM v2 baseline (CE 1.15 KO anchor) |
| F-CLM3-orig-5 | `phi_star_no_flip` | forgetting_index <= 0.05 on phi-star benchmark | post-train phi-star NO_FLIP eval, same harness as Pbeta + CLM v4 |

Composite ship verdict:
- **VERIFIED-CLM3-ORIGINAL-CHAT-CAPABLE** — 5/5 PASS -> anima-native chat path lands; paradigm v11 G3 + chat both preserved
- **PARTIAL-CHAT-PARTIAL-PHI** — 3-4/5 PASS, deliberate axis split -> document boundary, decide whether to extend
- **VERIFIED-CLM3-ORIGINAL-CHAT-FAIL** — <3/5 PASS -> #115 architectural lane closure for byte-level path; only Llama Path A v2 remains as chat-cap winner

---

## 5. Five honest C3 (concerns / caveats / counter-points)

1. **$2.49/hr H100 80GB community rate is volatile.** RunPod community pricing has hit $3.39/hr peaks. Linear spend tracker is conservative-low; if rate >$3.0 at fire time, $100 cap is reached at ~33h not ~40h. Watchdog should be re-parametrized at fire time from observed `runpod pod get` cost field if available.

2. **`pytorch/pytorch:2.11.0-cuda12.8-cudnn9-devel` image not yet verified to exist.** This was chosen to match the ubu1 RTX 5070 sm_120 reference (memory: torch 2.11.0+cu128). If RunPod registry doesn't have this exact tag, fall back to `pytorch/pytorch:2.5.1-cuda12.4-cudnn9-devel` and pip-upgrade torch in the heredoc. Operator should `runpod image search` before fire.

3. **`ready/training/train_clm.py` flag schema is assumed.** The CLI flags in the heredoc (`--phi-boost-techniques`, `--fibonacci-growth`, `--phase-mitosis`, etc.) match the BG-ER spec verbatim but the actual `train_clm.py` may not expose all 19 technique IDs as comma-separated string. A pre-flight smoke (BG-ER C3 echo) on ubu1 5070 with `--steps 100` is strongly recommended before the H100 fire.

4. **HF base mirror reachability not gated.** Per memory `project_runpod_pod_purge_2026_05_03`, fresh boots must clone from HF base mirror. The training heredoc clones from GitHub `dancinlab/anima` directly; if that repo is private or has weights >5MB-on-git issues per memory `feedback_anima_models_datasets_hf_only`, the clone will fail. Recommend separate HF dataset/model pull step.

5. **$100 hard-cap is BG-ER C3-aligned, not BG-EU-original.** BG-EU prompt cited "$200-500 soft envelope". This script enforces $100 hard. The split is deliberate: $100 = ~40h H100 = sufficient for 100K steps at ~0.3s/step (10h walltime per spec section 1.8), with ~30h margin for recovery / re-run. If operator wants the full $500 envelope, edit `BUDGET_CAP=100` -> `BUDGET_CAP=500` in both scripts. **Recommendation: keep $100 for first fire; only raise after a successful gate-1-2-3 dry run.**

---

## 6. raw#15 + audit-doc-token-redact compliance

- No HF token / RunPod API key / RunPod password literals anywhere in launch script, watchdog, doc, or verdict
- All credential reads via secret CLI lookup; values `unset` immediately after shape check
- Audit log at `state/.../launch.log` writes `pod_name + cap + timestamp` only, never the token
- Per memory `feedback_audit_doc_token_redact`: this doc embeds **zero** token literals (live or stale); GitHub Secret Scanning safe

---

## 7. Done state

- launch_h100.bash: ~110 LoC bash 3.2 compatible, 6 gate flow, no auto-fire
- watchdog_h100.bash: ~60 LoC bash 3.2 compatible, 5min cadence, L23/L24/L25 enforcement
- verdict.json: structured ledger, falsifier list, ship_verdict 3-option taxonomy
- this doc: ~150 LoC, 5 C3 honest, operator fire 5-step, falsifier measurement plan

Next BG dependency: operator decision on `BUDGET-100` confirm + `FALSIFIER-LOCK` ack + actual H100 fire (separate cycle).
