# IBM Cloud Environment Setup Runbook — nexus.qmirror Phase 3 Calibration Burst

- ts_utc: 2026-05-03
- purpose: pre-flight environment setup for the one-shot $200 IBM Cloud burst (qmirror v2.0/v3.0 anchor)
- credit: $200 USD (IBM Cloud signup grant)
- gate: doc-only; all account-level actions executed by user
- raw#9: NO .py on Mac repo (Qiskit code lives on cloud / pod / ubu1)
- raw#15: NO personal paths in body (use `<repo>/...` placeholders)
- prereq doc: `docs/ibm_cloud_experiment_list_2026_05_03.md` (calibration burst plan, $60+$40+$40+$20+$30+$10)

---

## 0. Scope

This runbook covers IBM Cloud account / region / billing / SDK / auth / budget / verification setup. It does **not** execute any quantum job. Burst execution is gated on:
1. qmirror v1.0 implementation complete (Phase 1)
2. user explicit "burst go" signal
3. all 8 pre-flight checks in §10 green

---

## 1. Region selection

### Selection criteria

| criterion | requirement | notes |
|---|---|---|
| IBM Quantum service availability | mandatory | not all regions host Quantum control plane |
| watsonx.ai availability | mandatory (fallback only) | needed if qmirror noise modeling needs LLM-assisted parameter fit |
| latency to backend (Heron / Eagle / Falcon) | < 500 ms RTT preferred | affects iterative tomography speed only, not job cost |
| billing currency | USD preferred | EUR / JPY billing adds FX noise to $200 cap tracking |
| free-tier overlap | yes | use free Quantum Open Plan for §6 verification before paid burst |

### Candidate regions

| region code | Quantum | watsonx | currency | recommendation |
|---|---|---|---|---|
| **us-east (Washington DC)** | yes (primary control plane) | yes | USD | **PRIMARY — recommended** |
| eu-de (Frankfurt) | yes | yes | EUR | backup; FX adds ~1% noise to budget |
| jp-tok (Tokyo) | partial (some backends only) | yes | JPY | not recommended; backend coverage gap |
| us-south (Dallas) | yes | yes | USD | acceptable backup if us-east capacity issue |
| br-sao (São Paulo) | no | yes | BRL | not viable for Quantum |
| au-syd (Sydney) | no | yes | AUD | not viable for Quantum |

### Decision

- **Primary: us-east (Washington DC)** — full Heron + Eagle + Falcon backend coverage, USD billing, lowest FX noise on $200 cap.
- **Backup: eu-de (Frankfurt)** — full backend coverage, EUR billing (track FX rate at burst start).
- **Avoid: jp-tok** — partial backend coverage breaks N2 cross-vendor axis.

---

## 2. Account verification

### Step-by-step

1. **Login to IBM Cloud console** (`https://cloud.ibm.com`).
2. **Verify email + 2FA enabled** — Account Settings → Login Settings → enable TOTP (authenticator app).
3. **Confirm billing profile** — Manage → Billing and Usage → Payment Methods → confirm credit grant of $200 USD listed under "Promotional credits".
4. **Verify resource group exists** — Manage → Account → Resource Groups → ensure `default` group present (or create `qmirror-burst` group for isolation).
5. **Set primary region** to `us-east` — top-right region selector.
6. **Enable IBM Quantum service**:
   - Catalog → search "Quantum" → "IBM Quantum" → select region `us-east` → plan: start with **Open** (free tier) for verification, then upgrade to **Pay-As-You-Go** before burst day 1.
7. **Enable watsonx.ai** (optional fallback):
   - Catalog → search "watsonx.ai" → select region `us-east` → plan: **Essentials** (or Lite for verification only).
8. **Generate IAM API key** — Manage → Access (IAM) → API keys → Create → name `qmirror-burst-key` → save the key value to a secure password manager (only shown once).
9. **Assign IAM roles**:
   - account-level: `Viewer`
   - resource group `default` (or `qmirror-burst`): `Editor`
   - Quantum service instance: `Manager` (needed to submit jobs and read results)
   - watsonx.ai instance: `Editor` (if used)
10. **Confirm tax / address** — required for Pay-As-You-Go upgrade; missing tax fields will block backend submission.

### Acceptance signal

- Account dashboard shows: $200 promotional credit available, IBM Quantum service provisioned in us-east, IAM API key created and stored securely.

---

## 3. IBM Quantum SDK install

### SDK identity

- **Primary package: `qiskit-ibm-runtime`** (current SDK; replaces deprecated `qiskit-ibmq-provider`)
- companion: `qiskit` (core circuit + transpiler)
- simulator: `qiskit-aer` (for qmirror local NoiseModel injection)

### Install (cloud / pod / ubu1 — NOT Mac repo)

```
pip install qiskit qiskit-ibm-runtime qiskit-aer
```

Optional pinned versions for reproducibility (record actual versions in `<repo>/state/qmirror_calibration_<ts>/env_lock.json`):

```
pip install "qiskit>=1.2,<2.0" "qiskit-ibm-runtime>=0.30,<1.0" "qiskit-aer>=0.15,<1.0"
```

### Verification

```
python -c "from qiskit_ibm_runtime import QiskitRuntimeService; print(QiskitRuntimeService.global_service)"
python -c "import qiskit; print(qiskit.__version__)"
python -c "import qiskit_aer; print(qiskit_aer.__version__)"
```

### File location convention

- code: `<remote-host>:~/qmirror/calibration/` (pod or ubu1)
- output: `<repo>/state/qmirror_calibration_<ts>/` (Mac repo, results only — no .py)

---

## 4. Auth token generation

### Two distinct tokens

| token | scope | where generated | where stored |
|---|---|---|---|
| **IBM Cloud IAM API key** | classical IBM Cloud (billing, watsonx, resource groups) | cloud.ibm.com → Manage → Access (IAM) → API keys | env var `IBMCLOUD_API_KEY` |
| **IBM Quantum (Runtime) token** | quantum service only; CRN-scoped | auto-derived from IAM API key + Quantum service CRN, OR generated via `https://quantum.ibm.com` legacy console | env var `QISKIT_IBM_TOKEN` |

### Modern auth flow (recommended)

The new `qiskit-ibm-runtime` uses **IBM Cloud IAM** (single token):

```
from qiskit_ibm_runtime import QiskitRuntimeService

QiskitRuntimeService.save_account(
    channel="ibm_cloud",
    token="<IBMCLOUD_API_KEY>",
    instance="<QUANTUM_SERVICE_CRN>",
    set_as_default=True,
)
```

The `instance` CRN is found at: cloud.ibm.com → Resource list → Services → IBM Quantum → "CRN" field.

### Legacy auth (fallback only)

If using the deprecated `quantum.ibm.com` token:

```
QiskitRuntimeService.save_account(channel="ibm_quantum", token="<LEGACY_TOKEN>")
```

The legacy `ibm_quantum` channel is being sunset; prefer `ibm_cloud` for any work past 2025.

### Storage convention

- never commit tokens to git
- store in: shell secrets manager (e.g. macOS Keychain, 1Password) → exported to remote shell `~/.bashrc` on pod/ubu1 only when running burst
- rotate: after burst complete, revoke the `qmirror-burst-key` to prevent residual exposure

---

## 5. Budget guard ($200 hard cap)

### Mechanism layering (defense in depth)

| layer | tool | trigger | action |
|---|---|---|---|
| L1 — soft alert | IBM Cloud Billing → Spending Notifications | $50 cumulative | email to user |
| L2 — soft alert | IBM Cloud Billing → Spending Notifications | $100 cumulative | email + SMS (if configured) |
| L3 — soft alert | IBM Cloud Billing → Spending Notifications | $150 cumulative | email + SMS, manual review checkpoint |
| L4 — hard alert | IBM Cloud Billing → Spending Notifications | $190 cumulative | email + SMS + **stop submitting new jobs** (manual gate) |
| L5 — hard cap | promotional credit exhaustion | $200 | IBM auto-stops paid services (promotional credits do not auto-bill credit card) |
| L6 — independent log | local burst tracker `<repo>/state/qmirror_calibration_<ts>/budget_log.jsonl` | every job submission | per-job estimated cost appended; pre-submit check refuses if `sum + next > $200` |

### Setup steps

1. Manage → Billing and Usage → **Spending notifications** → Add notification.
2. Create 4 notifications at $50 / $100 / $150 / $190 USD thresholds.
3. **Disable auto-bill credit card** until burst complete (Manage → Payment Methods → remove or disable card; promotional credit alone funds the burst).
4. Enable **resource group spending limit** if available: Manage → Account → Resource Groups → `qmirror-burst` → set monthly limit $200.
5. Local L6 tracker: every job submitted via `qiskit-ibm-runtime` is wrapped in a pre-submit budget check that reads `budget_log.jsonl` and refuses if running total + estimated cost > $200.

### Acceptance signal

- 4 spending notifications visible in console
- credit card disabled or removed
- L6 local tracker file exists with header row

---

## 6. Test queries (verification, near-zero cost)

Run these on the **Open Plan (free tier)** before upgrading to Pay-As-You-Go. They confirm SDK + auth + backend access without touching the $200 budget.

### Test 1 — list backends (no shots, no cost)

```
from qiskit_ibm_runtime import QiskitRuntimeService
service = QiskitRuntimeService()
for backend in service.backends():
    print(backend.name, backend.num_qubits, backend.status().operational)
```

Expected: list of backends including at least one Heron / Eagle / Falcon device showing `operational=True`.

### Test 2 — simulator round-trip (no real backend, free)

```
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
qc = QuantumCircuit(2, 2)
qc.h(0); qc.cx(0, 1); qc.measure([0, 1], [0, 1])
result = AerSimulator().run(qc, shots=1024).result()
print(result.get_counts())
```

Expected: counts dict with `00` and `11` near 50/50, no `01`/`10`.

### Test 3 — minimum-cost real backend job (Open Plan free shots)

```
from qiskit import QuantumCircuit, transpile
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2
service = QiskitRuntimeService()
backend = service.least_busy(operational=True, simulator=False, min_num_qubits=2)
qc = QuantumCircuit(2, 2)
qc.h(0); qc.cx(0, 1); qc.measure([0, 1], [0, 1])
qc_t = transpile(qc, backend)
sampler = SamplerV2(mode=backend)
job = sampler.run([qc_t], shots=100)
print("job_id:", job.job_id())
print(job.result()[0].data.c.get_counts())
```

Expected: job_id returned, result counts show Bell-state distribution. **Run on Open Plan only** to avoid burning paid credit on verification.

### Test 4 — auth + CRN sanity

```
from qiskit_ibm_runtime import QiskitRuntimeService
service = QiskitRuntimeService(channel="ibm_cloud")
print("instance:", service.active_account()["instance"])
print("channel:", service.active_account()["channel"])
```

Expected: prints CRN matching the us-east Quantum service instance.

---

## 7. Region-specific gotchas

| gotcha | impact | mitigation |
|---|---|---|
| **Heron r2 backends concentrated in us-east** | jp-tok / eu-de may lack newest Heron generation; N1 noise model anchored to wrong revision | confirm us-east primary; N1 must run on us-east `ibm_torino` or successor |
| **Falcon backends being retired** | N2 cross-vendor needs Falcon device; some Falcon r5 already decommissioned | check `service.backends(filters=lambda b: 'falcon' in b.name.lower())` on day 0; if zero, substitute with closest-generation alternative and document |
| **eu-de billing in EUR** | $200 cap drifts ±1-3% with FX | snapshot FX rate at burst start; convert spending log to USD for §5 L6 tracker |
| **jp-tok limited to specific Quantum plans** | some Pay-As-You-Go SKUs not offered in jp-tok | another reason to avoid jp-tok |
| **maintenance windows differ by region** | Heron downtime in us-east may not coincide with eu-de | check `backend.status().status_msg` on day 0; have eu-de fallback warm |
| **queue priority varies by plan + region** | Open Plan jobs may queue 6-24h | upgrade to Pay-As-You-Go before N5 (largest job, longest queue) |
| **session-mode required for low-latency iterative jobs** | N3 tomography needs back-to-back submissions | use `Session` context manager, but be aware sessions consume reserved time = $$ |

---

## 8. Failure recovery

### Scenario: account suspension

| signal | response |
|---|---|
| billing dispute hold | check email for IBM compliance request; respond within 7 days; do not submit new jobs |
| TOS flag (rare) | open ticket via cloud.ibm.com → Support → Manage Cases |
| credential leak detected | revoke API key immediately, regenerate, update env var on remote hosts |

### Scenario: billing dispute

1. Export usage CSV: Manage → Billing and Usage → Usage → Export.
2. Cross-reference with local `budget_log.jsonl` (§5 L6).
3. Open dispute case with itemized job_id list.
4. Pause burst until resolved.

### Scenario: region migration mid-burst

If us-east becomes degraded during the burst:

1. Stop new submissions; note current $ spent.
2. Provision Quantum service in eu-de (backup region).
3. Update `QiskitRuntimeService.save_account()` with new CRN.
4. Re-run §6 Test 1 + Test 4 to confirm new region access.
5. Snapshot FX rate (if EUR) and update §5 L6 tracker conversion.
6. Re-submit only the **incomplete axes** (do not re-run completed N1-N5 axes already paid for in us-east).
7. Document migration in `<repo>/state/qmirror_calibration_<ts>/region_migration_<ts>.json`.

### Scenario: $200 exhausted before burst complete

- promotional credit auto-stops paid jobs (no surprise card charge if §5 step 3 was followed)
- accept partial result; document which axes were funded
- do NOT add credit card to "finish" — would defeat the one-shot lock-in discipline (raw#91 honest C3)
- update `docs/ibm_cloud_experiment_list_2026_05_03.md` revision table with R3 entry noting partial completion

### Scenario: SDK auth failure mid-burst

1. Check token expiry: IAM API keys do not expire by default but can be revoked.
2. Regenerate IAM API key from console.
3. Update env var on remote host.
4. Re-run `QiskitRuntimeService.save_account()`.
5. Verify with §6 Test 4.

---

## 9. References

- IBM Cloud console: `https://cloud.ibm.com`
- IBM Quantum Platform: `https://quantum.ibm.com` (legacy console; new work via cloud.ibm.com preferred)
- Qiskit Runtime docs: `https://docs.quantum.ibm.com/`
- Qiskit Runtime Python API: `https://docs.quantum.ibm.com/api/qiskit-ibm-runtime`
- watsonx.ai docs: `https://www.ibm.com/products/watsonx-ai`
- calibration plan (this runbook's parent): `docs/ibm_cloud_experiment_list_2026_05_03.md`
- nexus.qmirror spec: `docs/nexus_qmirror_spec_2026_05_03.md`

---

## 10. Pre-Calibration-burst checklist (8 gates)

Before user issues "burst go" on day 0, all 8 must be green:

| # | gate | acceptance |
|---|---|---|
| 1 | region selected = us-east | console region selector shows us-east |
| 2 | $200 promotional credit visible | billing dashboard confirms |
| 3 | IBM Quantum service provisioned in us-east | resource list shows service instance |
| 4 | IAM API key generated + stored securely | password manager entry present |
| 5 | `QiskitRuntimeService.save_account()` succeeds with `ibm_cloud` channel | §6 Test 4 passes |
| 6 | 4 spending notifications configured ($50/$100/$150/$190) | billing → spending notifications shows 4 entries |
| 7 | credit card disabled / removed | payment methods empty or disabled |
| 8 | §6 Test 1-4 all pass on Open Plan | output captured to `<repo>/state/qmirror_calibration_preflight_<ts>/verify_log.txt` |

When all 8 green: user issues "burst go" → proceed with day 1 (N1 noise model RB).

---

## 11. Honest C3 (raw#91)

1. **No live IBM docs access during this writeup** — region/SDK/auth details are based on stable public IBM Cloud product structure as of late 2025 / early 2026; verify against current docs at burst day 0.
2. **Promotional credit terms vary** — IBM may attach time limits (typically 30/60/90 days) to the $200 grant; check expiry on signup confirmation email and plan burst within window.
3. **Open Plan free tier limits** — typically 10 minutes/month of QPU time; §6 verification tests should fit, but a few extra retries could exhaust free quota and force paid mode early.
4. **`ibm_quantum` channel sunset timing** — legacy channel may be removed mid-2026; use `ibm_cloud` channel from day 0 to avoid mid-burst migration.
5. **Falcon device retirement risk** — may not be available at burst time; N2 cross-vendor axis allocation may need substitution (document in calibration plan revision).
6. **No automation here** — every step in this runbook is user-executed via console or remote shell; this doc does not script anything (raw#9 + doc-only gate).
7. **CRN format assumption** — assumes IBM has not changed CRN structure; if changed, follow current `QiskitRuntimeService` error message guidance.
8. **Budget guard is advisory not enforced** — IBM does not provide hard mid-job cancellation at $190 threshold; L4 alert is a manual stop signal, not automatic.
