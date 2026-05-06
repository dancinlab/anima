# H100 Idle Check 2026-05-05/06 — Companion Handoff

**Lane**: BG-EW (H100-IDLE-CHECK pre-β-fire)
**Audit ts**: 2026-05-06T00:00:00Z (local 2026-05-06)
**Verdict file**: `state/anima_h100_idle_check_2026_05_05/verdict.json`
**Cost**: $0 (mac audit-only, no GPU provision)
**Destructive ops**: none
**Companion doc**: `docs/anima_h100_idle_audit_2026_05_05.ai.md` (2026-05-05 snapshot — see anomaly note in §1)

---

## §1 RunPod active pods + balance

| Field | Value |
|---|---|
| `clientBalance` | **$339.25** USD |
| `currentSpendPerHr` | **$0.089/hr** (storage only — no compute) |
| Active pods | **0 RUNNING** |
| Total pods in account | 4 (all `EXITED`) |

All 4 pods are `anima-clm-v4-sanity-rerun-v2-fixture-fix-2026-05-04` H100 SXM @ $2.99/hr, exited 2026-05-04 22:56–23:28 UTC by user. They are stopped (not deleted) — contributing only the $0.089/hr storage rate.

**Anomaly vs companion doc**: `anima_h100_idle_audit_2026_05_05.ai.md` cited 1 RUNNING pod `szv2vyf06h35uy` (Pβ-SCALE 50K). Today's GraphQL `myself.pods` returns no such pod ID. Inference: pod was terminated between the 2026-05-05 audit and this 2026-05-06 check — cross-check with cost-watchdog ledger before β fire to avoid double-allocation in spend accounting.

**H100 availability + lowest pricing (RunPod marketplace, single-GPU)**:

| GPU | Memory | Uninterruptable $/hr | Bid $/hr |
|---|---|---|---|
| H100 SXM | 80 GB | **$2.69** | $1.50 |
| H100 NVL | 94 GB | $2.59 | $1.40 |
| H100 PCIe | 80 GB | $1.99 | $1.35 |

Both `secureCloud` and `communityCloud` flag true → capacity available at audit ts.

## §2 ubu1 / ubu2 GPU 상태

| Host | LAN | Tailscale | GPU status |
|---|---|---|---|
| ubu1 (RTX 5070, sm_120, torch 2.11+cu128 venv) | 192.168.50.119 — **timeout 5s** | 100.96.193.56 — **timeout 5s** | **UNKNOWN** |
| ubu2 | 192.168.50.60 — **timeout 5s** | 100.72.76.118 — **timeout 5s** | **UNKNOWN** |

Both LAN and Tailscale paths timed out → mac is off-LAN AND remote hosts not advertising on Tailscale (likely powered off, network down, or Tailscale service stopped). Cannot confirm idle/busy. **Scenario D (ubu1 idle, $0 fire) cannot be selected without reachability**.

## §3 다른 GPU source

| Provider | CLI installed | Credential | Balance/Credit |
|---|---|---|---|
| RunPod | `/opt/homebrew/bin/runpodctl` | `runpod.api_key` (50 chars) | **$339.25** |
| Vast.ai | `/Users/ghost/.local/bin/vastai` | `vast.api_key` (64 chars) | **$320.62 credit, $0 balance**, 0 instances |
| Modal | not installed | none | — |
| Lambda Labs | not installed | none | — |
| Paperspace | not installed | none | — |
| AWS Braket | — | `aws_braket.access_key_id` | quantum (not classical GPU) — N/A |
| IBM/GCP/Azure/Kaggle/Colab/Salad/TensorDock | — | none in `secret list` | — |

Two viable cloud-GPU sources: **RunPod** (primary, $339) and **Vast.ai** (secondary, $320 credit). Vast.ai SSH key absent from `~/.ssh/` (only `known_hosts_runpod` present) — first Vast launch needs key bootstrap.

## §4 유휴도 verdict — 시나리오 B

| Scenario | Met? | Note |
|---|---|---|
| A: Idle H100 instance already RUNNING → free fire | NO | 0 RUNNING pods |
| **B: Balance sufficient + H100 available → fresh provision** | **YES** | RunPod $339 + H100 SXM $2.69/hr available |
| C: Balance insufficient → defer | NO | $339 ≫ $100 cap |
| D: ubu1 RTX 5070 idle → $0 5–10 day fire | UNKNOWN | unreachable |
| E: All sources busy → defer | NO | RunPod + Vast both clean |

## §5 β fire decision recommend

**PROCEED — RunPod fresh H100 provision**.

**Rationale (ranked by 완성도)**:
1. Clean slate (no $ burning) — no risk of double-billing or zombie pod confusion
2. Balance/cap ratio: $339 / $100 cap = 3.4× headroom; H100 SXM uninterruptable $2.69/hr × 10h = $26.90 (27% of $100 cap)
3. Vast.ai = secondary fallback (no SSH key bootstrapped → +15min cold start; defer unless RunPod region outage)
4. ubu1 path UNKNOWN — defer until reachability restored; do NOT block β fire on it
5. Per memory `project_runpod_pod_purge_2026_05_03`: Phase 2 must boot fresh from HF base mirror — fits this scenario

**Pre-flight checklist (own 16 / L23-L24-L25)**:
- [ ] Watchdog registered pre-launch
- [ ] Heartbeat cadence 5min
- [ ] Pod 404 verify path wired
- [ ] Per-BG budget cap $100 (BG-ER recommendation)
- [ ] PEFT + lm-eval pre-flight smoke (V2_FAIL retro)
- [ ] `transformers>=4.51` pinned with `lm-eval 0.4.11`
- [ ] HF base mirror confirmed accessible (project_runpod_pod_purge memory)

## §6 Honest C3 (≥5)

1. **C3-1 ubu1/ubu2 reachability UNKNOWN** — both LAN and Tailscale timed out. If user is on-LAN at home, ubu1 idle ($0, 5-10 days) may dominate β fire economics over RunPod ($26.90 / 10h). Recommend retrying ubu reachability before locking in RunPod path.
2. **C3-2 Balance snapshot is point-in-time** — concurrent BG launches in same session can race-deplete; β fire should re-query balance immediately before pod create.
3. **C3-3 Lowest-price H100 SXM $2.69/hr is likely community cloud** — secure cloud uninterruptable rate may be higher (typically $2.99–$3.49 for SXM); the safer β-fire pick should pin secureCloud=true and budget for $3.49/hr × 10h = $34.90 (still under cap).
4. **C3-4 No token leak in verdict/doc** — `runpod.api_key` and `vast.api_key` accessed via secret CLI, redacted at rest; raw#9/10/15 + audit-doc-redact rule observed.
5. **C3-5 Companion doc anomaly** — `anima_h100_idle_audit_2026_05_05.ai.md` referenced pod `szv2vyf06h35uy` RUNNING; absent here. Implies KILL happened upstream between 2026-05-05 and 2026-05-06; cross-check `state/h100_alert_ledger_2026_05.jsonl` and cost watchdog before β fire to confirm spend accounting.
6. **C3-6 Vast.ai instances=0 confirmed but SSH key not bootstrapped** — `/Users/ghost/.ssh/` contains only `known_hosts_runpod`. First Vast launch needs `vast.ssh_private` + `vast.ssh_pub` extraction from secret CLI (~15min).
7. **C3-7 Single-cloud risk** — Modal/Lambda/Paperspace/IBM/GCP/Azure all absent from credential store. RunPod region outage during β fire = no immediate failover (Vast bootstrap = 15min). Consider Modal credential add as part of broader resilience plan.

---

**End of audit. No commits, no destructive ops, no GPU provision performed.**
