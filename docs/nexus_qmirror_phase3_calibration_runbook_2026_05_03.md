# nexus.qmirror Phase 3 — IBM Cloud $200 One-Shot Calibration Runbook

> qmirror canonical SSOT: see `nexus/.roadmap.qmirror` header fields `upstream_url` + `latest_release` (current: v2.0.0, 2026-05-04). Hardcoded URLs deprecated 2026-05-04 — see `### See also (qmirror xref history)` footnote for prior callouts.

- ts_utc: 2026-05-03 (R2: option β cross-modality extension landed)
- module: **nexus.qmirror** (Phase 3 — N1+N2+N3+N4+N5 hardware anchor)
- credit envelope (R2 option β): **$210 USD total** = $150 IBM Cloud + $60 AWS Braket; $290 reserve in $500 outer envelope
- duration: day 0 (env) + day 1-6 (exec) + day 7 (lock-in) = **8 calendar days max**
- gate: per-day EXEC requires explicit user OK (raw#9 — no .py on Mac)
- runbook role: **modular** (operational) layered on `docs/ibm_cloud_experiment_list_2026_05_03.md` (planner), `docs/nexus_qmirror_spec_2026_05_03.md` §14 (spec), and `docs/qmirror_n2_cross_vendor_revision_2026_05_03.md` (option β scope)
- contributes to: `nexus/.roadmap.qmirror` cond.3 + cond.8 + entry `qmirror.phase3_calibration`
- option_selected: **β** (IBM Heron $150 + Braket IonQ Forte 1 + Rigetti Cepheus-1-108Q $60)

> **READ-ONLY repository surface for this runbook**: this doc only. All Qiskit-bearing code targets lives on cloud / pod / ubu1, never `core/anima` or `core/nexus` Mac trees (raw#9 strict).

---

## 0. Pre-flight gates (must-pass before day 0)

| gate | check | block-if-fail |
|---|---|---|
| G0.1 | qmirror Phase 1 cond.2 LANDED (`qmirror.cond.2` evidence != []) | abort runbook; re-queue after Phase 1 land |
| G0.2 | nexus host (ubu1 or pod) confirmed for SDK install | abort runbook; pick host |
| G0.3 | `core/anima/state/runpod_credit_status.json` shows non-zero usable budget OR pod budget held separately | warn-and-continue |
| G0.4 | user explicit "burst go" signal received | abort runbook |
| G0.5 | option β substrate verified (AWS Braket account active + IonQ Forte 1 ONLINE + Rigetti substitute selected) | abort runbook; option fall-back to α |

Verify gates:

```bash
# G0.1
jq -r '.required_conditions[] | select(.id=="qmirror.cond.2") | .status' \
  $NEXUS/.roadmap.qmirror
# expected: "met"  (currently "unmet" — Phase 1 not started)

# G0.2 — pick host (one of):
ssh nexus@ubu1 'uname -a && python3 --version'
ssh pod        'uname -a && python3 --version'

# G0.3
jq '.budget_remaining_usd // .remaining' \
  $ANIMA/state/runpod_credit_status.json
```

---

## 1. Day 0 — IBM Cloud env checklist (8 prereqs, ~3hr)

**Goal**: every line below produces a green check before any qubit is consumed.

| # | item | verification command | pass criterion |
|---|---|---|---|
| P1 | IBM Cloud account active | `ibmcloud account show` | `Account ID` printed, `State: ACTIVE` |
| P2 | Region = us-east (Quantum + watsonx supported) | `ibmcloud target -r us-east && ibmcloud target` | `Region: us-east` |
| P3 | Quantum service instance provisioned | `ibmcloud resource service-instances --service-name quantum-computing` | ≥1 instance, `State: active` |
| P4 | IBM Quantum API token generated + cached | `ls ~/.qiskit/qiskit-ibm.json` | file exists, mode 600, contains `token` field |
| P5 | Heron / Eagle / Falcon backends visible | `python -c "from qiskit_ibm_runtime import QiskitRuntimeService as S; [print(b.name, b.status().operational) for b in S().backends()]"` | all 3 vendor families present, ≥1 operational each |
| P6 | $200 credit attached, billing alarm @ $50/$100/$150/$190 | `ibmcloud billing account-usage --output json \| jq .` then `ibmcloud billing account-usage-alerts` | `usage: 0`, alarms set on each threshold |
| P7 | Calibration cache target dir exists on nexus host | `ssh <host> 'mkdir -p ~/nexus/modules/qmirror/calibration && ls -ld ~/nexus/modules/qmirror/calibration'` | dir exists, writable |
| P8 | qiskit-ibm-runtime ≥ 0.30 installed on host | `ssh <host> 'pip show qiskit-ibm-runtime \| grep Version'` | `Version: 0.30.x` or newer |

**SDK install path (one-time, on nexus host only — NOT Mac)**:

```bash
ssh <nexus-host>
python3 -m venv ~/.venv/qmirror_phase3
source ~/.venv/qmirror_phase3/bin/activate
pip install --upgrade pip
pip install 'qiskit==1.2.*' 'qiskit-ibm-runtime>=0.30' \
            'qiskit-aer>=0.15' 'qiskit-experiments>=0.7' \
            'numpy<2' 'matplotlib' 'scipy'
python -c "import qiskit, qiskit_ibm_runtime, qiskit_aer; print(qiskit.__version__, qiskit_ibm_runtime.__version__, qiskit_aer.__version__)"
```

**Token bootstrap (run once after P4)**:

```python
# bootstrap_token.py — runs on nexus host, NOT Mac
from qiskit_ibm_runtime import QiskitRuntimeService
QiskitRuntimeService.save_account(
    channel="ibm_cloud",
    token="<API_TOKEN>",
    instance="<CRN>",  # from `ibmcloud resource service-instance <name> --output json | jq .crn`
    overwrite=True,
)
```

---

## 1.B. Day 0 — AWS Braket env checklist (option β only, 5 prereqs, ~2hr)

**Goal**: every line below produces a green check before any Braket task is submitted. Mirrors §1 P1-P8 for the cross-modality N2b axis.

| # | item | verification command | pass criterion |
|---|---|---|---|
| B1 | AWS account active + IAM user with Braket scope verified | `AWS_DEFAULT_REGION=us-east-1 aws sts get-caller-identity` | returns `Account` + `Arn` (expected `user/anima-braket-cli`, account `267673635495`) |
| B2 | IonQ Forte 1 ONLINE in us-east-1 | `aws braket get-device --device-arn arn:aws:braket:us-east-1::device/qpu/ionq/Forte-1 --region us-east-1 --query deviceStatus` | `"ONLINE"` |
| B3 | Rigetti substitute device ONLINE in us-west-1 (Ankaa-3 RETIRED → Cepheus-1-108Q substitute, $0.30/task + $0.000425/shot, 107 qubit) | `aws braket get-device --device-arn arn:aws:braket:us-west-1::device/qpu/rigetti/Cepheus-1-108Q --region us-west-1 --query deviceStatus` | `"ONLINE"` |
| B4 | S3 bucket for Braket result staging exists + writable | `aws s3 ls s3://amazon-braket-<account-id>-<region>/ 2>/dev/null \|\| aws s3 mb s3://amazon-braket-267673635495-us-east-1` | bucket exists or created |
| B5 | Cost-tracking surrogate (cost-explorer denied for `anima-braket-cli` IAM scope) — task-level cost log file created at `nexus/modules/qmirror/calibration/braket_cost_log.jsonl` (each entry: `{ts, device_arn, task_arn, shots, planned_cost_usd, observed_cost_usd}`) | `ssh <host> 'touch ~/nexus/modules/qmirror/calibration/braket_cost_log.jsonl && ls -l ~/nexus/modules/qmirror/calibration/braket_cost_log.jsonl'` | file exists, writable |

**SDK install path (one-time, on nexus host only — NOT Mac)**:

```bash
ssh <nexus-host>
source ~/.venv/qmirror_phase3/bin/activate  # reuse venv from §1 P8
pip install 'amazon-braket-sdk>=1.85' 'amazon-braket-default-simulator>=1.23' 'boto3>=1.34'
python -c "from braket.aws import AwsDevice; d=AwsDevice('arn:aws:braket:us-east-1::device/qpu/ionq/Forte-1'); print(d.status, d.name)"
```

**AWS credential bootstrap (run once on nexus host after B1)**:

```bash
# never paste keys in commit / never store on Mac repo
mkdir -p ~/.aws && chmod 700 ~/.aws
cat > ~/.aws/credentials <<'EOF'
[default]
aws_access_key_id     = <AKIA...>
aws_secret_access_key = <SECRET>
EOF
cat > ~/.aws/config <<'EOF'
[default]
region = us-east-1
output = json
EOF
chmod 600 ~/.aws/credentials ~/.aws/config
aws sts get-caller-identity   # confirm
```

**Cost guard separation**: cost-explorer (`ce:GetCostAndUsage`) is **denied** for the `anima-braket-cli` IAM scope (read-only Braket only). Cost surveillance for option β must be done *task-side* via `braket_cost_log.jsonl` populated immediately after each `AwsQuantumTask.create()` returns. Daily aggregation:

```bash
# braket_spend_today.sh — on host, runs after each Braket EXEC window
jq -s '[.[] | select(.ts | startswith("'"$(date -u +%F)"'")) | .observed_cost_usd] | add // 0' \
   ~/nexus/modules/qmirror/calibration/braket_cost_log.jsonl
```

**Tripwires (Braket-side)**:
- soft warn at $30 cumulative → log only
- hard freeze at $55 cumulative → block further task submission, escalate to user
- hard cap at $60 cumulative → matches B-budget allocation

---

## 2. Day 1-7 daily schedule

Per-day envelope: **single contiguous EXEC window** with explicit user OK before submission. Cost runs as cumulative band — abort daily if observed > planned + $5.

**Option β schedule** — IBM and Braket axes run in parallel where possible. IBM runs are foreground (~hours of queue + minutes of run); Braket IonQ Forte 1 queue is historically 12-48 hr, so Braket tasks must be submitted on **day 1** as background and harvested on day 2-3 when results land.

| day | IBM axis | IBM $ | IBM cum | Braket axis | Braket $ | Braket cum | combined cum | primary command (on host) |
|---|---|---|---|---|---|---|---|---|
| 0 | env (P1-P8) | $0 | $0 | env (B1-B5) | $0 | $0 | $0 | (§1 + §1.B checklists) |
| 1 | N1 noise model (RB, Heron) | $60 | $60 | **N2b submit** (CHSH × 3 trial × 2 device × 250 shot, IonQ Forte 1 + Rigetti Cepheus-1-108Q, queued bg) | $60 (planned) | $60 (planned) | $60 cash + $60 reserved | IBM: `python phase3/n1_rb_heron.py --shots 10000 --qubits 0-6 --out v2_noise_heron.json` ; Braket: `python phase3/n2b_chsh_braket.py --devices forte1,cepheus --trials 3 --shots 250 --submit-only` |
| 2 | N2a intra-Heron CHSH (3 trial × 3 Heron backend × 4096 shot) | $20 | $80 | N2b harvest if ready (poll every 30 min) | (settled cost lands here when tasks complete; planned $60) | $60 | $140 | IBM: `python phase3/n2a_chsh_heron.py --backends fez,marrakesh,kingston --trials 3 --shots 4096` ; Braket: `python phase3/n2b_harvest.py --since day1` |
| 3 | N3 process tomography (Heron) | $40 | $120 | N2b late-harvest + analyze (cross-vendor S-band overlap) | (residual harvests if queue slipped) | $60 | $180 | IBM: `python phase3/n3_process_tomo.py --circuits cnot,swap,iswap,sqrtx_cnot,random --shots 1024` ; Braket: `python phase3/n2b_analyze.py --emit v2_crossvendor_chsh.json` |
| 4 | N4 random circuit fidelity (50→**30 trials**, R2 reallocation) | $12 | $132 | — (no Braket activity) | $0 | $60 | $192 | IBM: `python phase3/n4_random_fidelity.py --depths 5,10,20 --trials 30` |
| 5 | N5 scale-up GHZ (20→**16 qubit ceiling**, R2 reallocation) | $10 | $142 | — | $0 | $60 | $202 | IBM: `python phase3/n5_ghz_scaleup.py --qubits 12,14,16 --backend heron` |
| 6 | buffer + lock | $8 | $150 | — | $0 | $60 | $210 | `python phase3/lock_v3.py --aggregate --tag v3_locked` |
| 7 | release | $0 | $150 | — | $0 | $60 | $210 | `python phase3/aggregate.py && jq .calibration_status v2_*.json` |

**Parallel-execution notes**:
- Day 1 Braket submit is **submit-only** (no blocking wait). Tasks land asynchronously into the Braket S3 result bucket; observed cost is recorded into `braket_cost_log.jsonl` on harvest, not on submit.
- Day 2-3 IBM EXEC windows continue independently of Braket task state. If Braket queue slips past day 3, N2b lands on day 4 and aggregation defers to day 6 — IBM-only axes still hit their original cum line.
- Cross-vendor analysis (N2b) compares **bound saturation ratio** S/2.828 (shot-count-robust) rather than raw S — see revision doc §6 C3.2.

**Daily ritual** (every day 1-6):

1. Verify yesterday's cache hash committed (`git -C ~/nexus log -1 modules/qmirror/calibration/`).
2. Check backend health: `python -c "from qiskit_ibm_runtime import QiskitRuntimeService; b=QiskitRuntimeService().backend('<today_backend>'); print(b.status())"` — abort day if `pending_jobs > 50` or `operational=False`.
3. Snapshot current spend: `ibmcloud billing account-usage --output json | jq '.Resources[] | select(.service_name=="quantum-computing")'` — record `pre_usd`.
4. Get user EXEC OK (text confirmation).
5. Run primary command (foreground tmux session named `qmirror_phase3_dN`).
6. On completion: snapshot `post_usd`, write `nexus/modules/qmirror/calibration/v2_<axis>_2026_05_03.json`, `git add` + commit.
7. End-of-day report: actual $ spent vs planned, anomalies, next-day go/no-go.

---

## 3. Result aggregation script spec (host-side, NOT Mac)

`phase3/aggregate.py` (lives on nexus host or pod, never Mac repo):

**Inputs** (read-only):
- `nexus/modules/qmirror/calibration/v2_noise_heron_2026_05_03.json` (N1)
- `nexus/modules/qmirror/calibration/v2_crossvendor_chsh_2026_05_03.json` (N2)
- `nexus/modules/qmirror/calibration/v2_tomography_2026_05_03.json` (N3)
- `nexus/modules/qmirror/calibration/v2_random_fidelity_2026_05_03.json` (N4)
- `nexus/modules/qmirror/calibration/v2_scaleup_ghz_2026_05_03.json` (N5)

**Output**: `nexus/modules/qmirror/calibration/v3_locked_2026_05_03.json` containing:
- merged noise model (Aer-importable dict)
- vendor-independence S-statistic table
- tomography fidelity matrix
- depth × fidelity curve coefficients
- qubit × match curve (GHZ)
- `calibration_status: "LANDED"` (literal, satisfies cond.3 verifier `jq .calibration_status ... | grep -q LANDED`)

**Optional hexa front-end** (if Phase 1 lands aggregate.hexa):
`hexa run nexus/modules/qmirror/aggregate.hexa --inputs v2_*.json --out v3_locked_2026_05_03.json` — wraps `_python_bridge/aggregate.py` per python_bridge concession (qmirror.blk.1).

---

## 4. Failure recovery decision tree (3 most likely modes)

```
        ┌─────────────────────────────────────────────────────┐
        │ FAILURE detected during day N execution             │
        └────────────────┬────────────────────────────────────┘
                         │
        ┌────────────────┼────────────────┐
        ▼                ▼                ▼
   F1: queue        F2: backend       F3: partial
   timeout          maintenance       completion
   (>6hr wait)      (operational      (job submitted
                    =False mid-run)    but result corrupt)
        │                │                │
        ▼                ▼                ▼
  cancel pending    swap to alt       parse partial JSON
  jobs              backend in same   → if ≥80% shots OK
  ┌─────┴─────┐     family            → accept, mark
  │ <$5 spent │     ┌─────┴─────┐     "degraded" in cache
  │ → retry   │     │ Heron     │     ┌─────┴─────┐
  │   off-peak│     │  → Eagle  │     │ <80%      │
  │   (KST    │     │ Eagle     │     │ → discard │
  │   23-07)  │     │  → Falcon │     │   re-queue│
  └─────┬─────┘     │ all down  │     │   from $10│
        │           │  → pause  │     │   buffer  │
  ┌─────┴─────┐     │   24hr    │     └───────────┘
  │ ≥$5 spent │     │   max     │
  │ → bank    │     └───────────┘
  │   partial │
  │   write   │
  │   degraded│  3-strike rule: if same axis fails 3x → escalate
  │   marker  │  to user, propose axis-skip (lock partial v3 or
  └───────────┘  fall back to v2_partial naming).
```

**Per-mode cost cap**:
- F1 retries: capped at $5 from $10 buffer
- F2 vendor swap: no extra cost (same allocation)
- F3 re-queue: capped at $5 from buffer

**Hard abort**: if buffer ($10) exhausted by day 4, freeze remaining axes, write `v3_partial_2026_05_03.json` with `calibration_status: "PARTIAL"`, and escalate to user before any further submission.

---

## 5. Cost monitoring per-day budget guard

**Watcher script** (run as background tmux pane every day 1-6):

```bash
# spend_guard.sh — on host, runs every 5min during exec window
WINDOW_START_USD=$(jq -r '.pre_usd' /tmp/qmirror_today.json)
DAILY_CAP=$(jq -r '.daily_cap_usd' /tmp/qmirror_today.json)  # e.g., 60 for day 1
while true; do
  CUR=$(ibmcloud billing account-usage --output json \
        | jq '[.Resources[] | select(.service_name=="quantum-computing") | .billable_cost] | add // 0')
  DELTA=$(awk "BEGIN{print $CUR - $WINDOW_START_USD}")
  echo "$(date -u +%FT%TZ) delta=$DELTA cap=$DAILY_CAP"
  if awk "BEGIN{exit !($DELTA > $DAILY_CAP + 5)}"; then
     # over by $5 → page
     echo "BUDGET BREACH" >&2
     # signal main job (tmux send-keys C-c)
     tmux send-keys -t qmirror_phase3_d$DAY C-c
     break
  fi
  sleep 300
done
```

**Tripwires**:
- **soft warn** at +$2 over daily plan → log only
- **hard kill** at +$5 → SIGINT to the job + escalate to user
- **circuit breaker** at total cumulative > $195 → freeze all submission, allow only aggregate/lock

---

## 6. Cache write spec

**Path pattern**: `nexus/modules/qmirror/calibration/v2_<axis>_2026_05_03.json`

**Per-axis files**:
- `v2_noise_heron_2026_05_03.json` (N1)
- `v2_crossvendor_chsh_2026_05_03.json` (N2 — under option β contains both `payload.n2a_intra_heron` and `payload.n2b_braket_cross_modality` blocks plus `option_selected: "beta"` field for cond.8 verifier)
- `v2_tomography_2026_05_03.json` (N3)
- `v2_random_fidelity_2026_05_03.json` (N4)
- `v2_scaleup_ghz_2026_05_03.json` (N5)
- `braket_cost_log.jsonl` (option β only — append-only task-level cost log, surrogate for denied cost-explorer)
- `v3_locked_2026_05_03.json` (aggregate, day 6 — satisfies cond.3 + cond.8 verifiers)

**Common envelope (every file)**:

```json
{
  "schema_version": "qmirror.calibration.v2",
  "axis": "N1|N2|N3|N4|N5|aggregate",
  "ts_utc_start": "2026-05-04T00:00:00Z",
  "ts_utc_end":   "2026-05-04T03:14:22Z",
  "ibm_backend": {
    "name": "ibm_heron_r2",
    "vendor_family": "heron",
    "version": "<from backend.version>",
    "calibration_ts_utc": "<backend.properties().last_update_date>"
  },
  "shots_total": 70000,
  "circuits_total": 7,
  "spend_usd": 60.00,
  "spend_pre_usd": 0.00,
  "spend_post_usd": 60.00,
  "calibration_status": "LANDED|PARTIAL|DEGRADED",
  "payload": { /* axis-specific data, see per-axis schema below */ },
  "provenance": {
    "submitter_host": "ubu1|pod",
    "qiskit_version": "1.2.x",
    "qiskit_ibm_runtime_version": "0.30.x",
    "operator_signal": "user_ok_2026_05_04T00_00Z",
    "git_commit_at_submit": "<sha>"
  },
  "raw_job_ids": ["c7v...a", "c7v...b"],
  "anomalies": []
}
```

**Per-axis `payload` shapes**:

- **N1**: `{ "T1_us": [...7], "T2_us": [...7], "gate_err_1q": {...}, "gate_err_2q": {...}, "readout_err": [...7], "aer_noise_model_b64": "<base64-pickle of NoiseModel>" }`
- **N2**: `{ "S_per_trial": {"heron":[5], "eagle":[5], "falcon":[5]}, "S_mean": {...}, "S_std": {...}, "ks_test_vs_qmirror_p": 0.xx }`
- **N3**: `{ "circuits": ["cnot","swap","iswap","sqrtx_cnot","random"], "fidelity": [...5], "frobenius_distance": [...5], "density_matrices_b64": [...] }`
- **N4**: `{ "depth": [5,10,20], "fidelity_per_trial": [[50],[50],[50]], "decay_fit_alpha": x.xx }`
- **N5**: `{ "qubits": [12,16,20], "ghz_match_vs_qmirror": [...3], "qmirror_ceiling_qubits": 20 }`
- **aggregate (v3)**: `{ "merged_noise_model_b64": "...", "axes": ["N1","N2","N3","N4","N5"], "regression_summary": {...}, "qmirror_version_locked": "v3.0" }`

**Commit hygiene**: each `v2_*.json` is `git add` + commit individually with message `qmirror calib N<n> land ts=<utc>`. `v3_locked` commit blocks until all 5 N-files are present and `calibration_status` ∈ {LANDED, DEGRADED} (PARTIAL blocks).

---

## 7. Cross-links

- planner: `docs/ibm_cloud_experiment_list_2026_05_03.md`
- spec §14: `docs/nexus_qmirror_spec_2026_05_03.md`
- N2 cross-vendor revision (option β source): `docs/qmirror_n2_cross_vendor_revision_2026_05_03.md`
- roadmap cond.3 + cond.8: `nexus/.roadmap.qmirror`
- Braket prior-run reference (S=2.808 ground truth on IonQ Forte 1): `state/nexus_chsh_bell_2026_05_02/`
- post-impl landing target: `docs/qmirror_phase3_calibration_landed_2026_05_*.ai.md` (planned, post-day-7)

---

## 8. Honest C3

1. **Phase 1 not landed yet** — runbook is doc-only until cond.2 met. No EXEC possible today.
2. **SDK version drift** — qiskit-ibm-runtime API surfaced changes quarterly; pin at install time, retest before day 1.
3. **Backend rename risk** — IBM rotates backend names (e.g., `ibm_heron_r2` → `ibm_marrakesh`); P5 must re-confirm names on day 0.
4. **N5 queue at 16-qubit ceiling** — option β reduced ceiling 20→16 qubit; queue still possible at day 5 boundary; buffer absorbs.
5. **Token leakage risk** — IBM API token in `~/.qiskit/qiskit-ibm.json` mode 600 only; never commit to git, never paste to Mac.
6. **No .py on Mac** — all Qiskit code lives on host. Mac repo only stores result JSONs (committed) + this runbook.
7. **One-shot lock**: drift after day 7 is accepted (~99% → ~95% over 6mo); refresh requires fresh credit cycle.
8. **(option β) IonQ queue variance** — Forte 1 historical 12-48 hr queue. Day 1 submit guarantees at-most day 3 harvest; if Forte 1 enters a 72hr+ maintenance window day 4 fallback aborts N2b cleanly (degrades S-band claim to IBM N2a only, no budget loss since Braket charges only on completion).
9. **(option β) Cost dual-tracking** — IBM uses `ibmcloud billing account-usage`, Braket uses task-side `braket_cost_log.jsonl` (cost-explorer denied for `anima-braket-cli` IAM scope). Two ledgers, two trip-wires; daily roll-up sum is computed off-cloud during evening report. Risk: silent over-spend on whichever ledger is not consulted that day; mitigation = both ledgers must be re-read every day-end.
10. **(option β) Multi-vendor coordination** — IBM and Braket are independent control planes (separate auth, separate region, separate failure modes). A Braket-side outage cannot be papered over with IBM credit and vice versa; cross-modality N2b lands or it does not. The runbook accepts this all-or-nothing N2b semantic and declines to back-fill with simulator data.
11. **(option β) Rigetti device substitution** — Ankaa-3 (specified in revision doc) is RETIRED. Substitute is `Cepheus-1-108Q` (Rigetti, us-west-1, 107 superconducting qubits, $0.30/task + $0.000425/shot). Same provider/modality, even cheaper per shot — substitution is honest within option β intent. Recorded in B3 prereq.

---

### See also (qmirror xref history)

Prior callouts preserved verbatim per qmirror_xref_centralization cycle (2026-05-04):

> 📦 Available at: https://github.com/dancinlab/qmirror (`hx install qmirror`)
> 🚀 v2.0.0 RELEASED 2026-05-04 — closure 13/13 conds met (8 v1 + 5 v2): https://github.com/dancinlab/qmirror/releases/tag/v2.0.0

Future qmirror release URLs are canonically tracked in `nexus/.roadmap.qmirror` header field `latest_release_url`. Update single line in roadmap; this footnote is a frozen historical record (do not retrofit).
