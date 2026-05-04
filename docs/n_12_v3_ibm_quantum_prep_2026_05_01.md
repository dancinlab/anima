# N-12 v3 IBM Quantum Open Plan — Launch-Ready Prep

Agent: `n_12_v3_ibm_quantum_prep`
Date UTC: 2026-05-01
Off-repo dir: `/Users/ghost/n12_v3_ibm/`
On-repo dir: `state/n_12_v3_ibm_quantum_prep_2026_05_01/`
Parents: #46 (vendor pivot research), #54 (v2 INDETERMINATE), #39 (v1 FAIL)

> **2026-05-03 qmirror substrate update (additive)**: this prep package targets IBM Quantum Open Plan. Per the qmirror closure series 2026-05-03, the **`nexus.qmirror` canonical substrate** (`docs/nexus_qmirror_spec_2026_05_03.md`) is now the primary execution path for F-N12-1 / Orch-OR-class measurement; real IBM Heron r2 access is **not required** for routine science. The IBM path documented here is preserved as a **calibration anchor** (one-shot $200 IBM Cloud burst, see `docs/ibm_cloud_experiment_list_2026_05_03.md` and `docs/nexus_qmirror_phase3_calibration_runbook_2026_05_03.md`) — not as primary execution.

> qmirror canonical SSOT: see `nexus/.roadmap.qmirror` header fields `upstream_url` + `latest_release` (current: v2.0.0, 2026-05-04). Hardcoded URLs deprecated 2026-05-04 — see `### See also (qmirror xref history)` footnote for prior callouts.

## Headline

F-N12-1 v3 launch package is **ready**. User can take it from $0 to live IBM Quantum Open Plan submission in **~7 minutes** of user-time after this prep. Agent did not create accounts, did not submit jobs (per $0 budget constraint and mission spec).

## 1. Deliverables

### 1.1 Off-repo scripts (HEXA-only repo compliance)

| Path | Role | LOC |
| ---- | ---- | --- |
| `/Users/ghost/n12_v3_ibm/submit_ibm.py` | Build 4q GHZ + delay sweep, submit to ibm_kingston via SamplerV2, save `results_<ts>.json` | ~140 |
| `/Users/ghost/n12_v3_ibm/verify_F_N12_1_v3.py` | Exponential fit `tau_2_eff` + 5-check verifier (incl. ratio band [0.15, 0.40] vs SC ref 100us primary, 1.06ms robustness, 1.68ms ceiling) | ~150 |
| `/Users/ghost/n12_v3_ibm/launch.sh` | One-liner: env check -> submit -> verify | ~40 |

All three are `chmod +x`. Zero `.py` files were written inside the anima repo (verified).

### 1.2 On-repo state JSONs

- `state/n_12_v3_ibm_quantum_prep_2026_05_01/user_onboarding_checklist.json` — the 5-step user flow
- `state/n_12_v3_ibm_quantum_prep_2026_05_01/launch_artifact_manifest.json` — script paths + parameters + cost cap
- `state/n_12_v3_ibm_quantum_prep_2026_05_01/ibm_kingston_specs_verified.json` — Heron r2 device specs + sources
- `state/n_12_v3_ibm_quantum_prep_2026_05_01/honest_c3.json` — top-3 caveats

## 2. User onboarding (5 steps, ~7 min)

| # | Step | Time |
| - | ---- | ---- |
| 1 | Sign up at https://quantum.ibm.com/ (email + verify, no CC) | 5 min |
| 2 | Account Settings -> API Keys -> copy token | 1 min |
| 3 | `mkdir -p ~/.qiskit && echo "<token>" > ~/.qiskit/ibm-quantum-token.txt` | <1 min |
| 4 | `pip install 'qiskit>=1.2' 'qiskit-ibm-runtime>=0.30' numpy scipy` | <1 min |
| 5 | `bash ~/n12_v3_ibm/launch.sh` | <1 min user-time + 1-60 min queue |

Total user-active time: ~7 minutes. Wall clock to PASS/FAIL verdict: 1 min to ~24 h depending on queue.

## 3. Launch one-liner preview

```
bash ~/n12_v3_ibm/launch.sh
```

What it does (verbatim from `launch.sh`):

1. Verify token at `~/.qiskit/ibm-quantum-token.txt` OR `$IBM_QUANTUM_TOKEN`.
2. Verify python deps (`qiskit`, `qiskit_ibm_runtime`, `numpy`, `scipy`).
3. Run `submit_ibm.py` -> queues 5 PUBs (one per delay point) on ibm_kingston via SamplerV2; saves `~/n12_v3_ibm/results_<UTC-timestamp>.json`.
4. Run `verify_F_N12_1_v3.py` against newest results file -> saves `_verdict.json` next to it; prints PASS/FAIL.

## 4. Discrepancy with `f_n12_1_v3_protocol.json` (delay sweep)

| Source | delay_points_us |
| ------ | --------------- |
| Mission prompt (this agent) | `[10, 50, 100, 200, 500]` |
| `f_n12_1_v3_protocol.json` (#46 research output) | `[0, 25, 50, 100, 200]` |

**Resolution adopted**: mission prompt sweep `[10, 50, 100, 200, 500]` us.

Rationale:
- Wider dynamic range (max delay = 5x ibm_kingston T2 typical) yields better tau_2 fit leverage on the right tail.
- Lose: the D=0 entanglement-quality reference. Mitigated in verifier by check #2 = `P(0000)|D_min=10us >= 0.80` (relaxed from `>=0.85` at D=0).
- The protocol's lower bound (25us as Penrose-Hameroff ~25us threshold marker) is preserved by the 10us point being adjacent to the threshold region; user can post-process to interpolate at 25us.

If user prefers strict protocol compliance, edit `DELAY_POINTS_US` on line 30 of `submit_ibm.py` to `[0, 25, 50, 100, 200]` before launch.

## 5. Cost cap (Phase 4)

- **Primary path**: $0.00. Open Plan = 10 min/28d free; expected QPU compute for 5 PUBs x 100 shots = 10-30 sec (verified via WebSearch 2026-05-01 IBM doc).
- **PAYG fallback**: hard cap $5.00. At $1.60/sec (Strangeworks 2024 cite) or equivalently $96/min (IBM 2026 doc), $5 buys ~3 sec compute — insufficient for full sweep. Recommendation if Open Plan exhausted = wait for next 28d rolling window, do NOT pay.
- 2026-03-16 promotional bonus: 180 extra minutes/12mo for users who log >=20 min in any 12mo window (irrelevant for first run, useful for follow-ups).

## 6. ibm_kingston specs verified (Phase 5 honest C3)

| Field | Value | Substrate match? |
| ----- | ----- | ---------------- |
| Family | Heron r2 | Y (matches v3 SC primary ref) |
| Qubits | 156, heavy-hex | OK |
| T1 typical | 100-300 us | OK |
| T2 typical | 80-200 us | Y (matches 100us primary ref denominator) |
| OpenQASM 3 `delay` | YES (us/ns/dt verified in IBM feature table) | Y |
| Open Plan eligible | YES since 2026-03-16 | Y |
| KR access | YES (KQC partnership, no export restriction) | Y |
| Queue wait | 1 min - 24 h variance | risk acknowledged |

Sources cross-checked:
- IBM announcement 2025-04-09 (kingston launch)
- IBM announcement 2026-03-16 (Open Plan kingston rotation)
- IBM feature table (delay primitive)
- Qiskit issue #1613 (CLOSED 2024-04-19, was user-error, not actual delay+SamplerV2 bug)

## 7. Top blockers for user side

1. **Account creation**. Agent cannot sign up on user's behalf (mission spec + reasonable trust constraint). User must do step 1-2.
2. **Queue latency**. 1-24h variance; submit_ibm.py uses blocking `job.result()`. Recommend tmux/screen if user closes terminal.
3. **Substrate framing**. v3 PASS = textbook QM holds = expected NULL Orch-OR signal at SC scale. This is *not* a falsification of Orch-OR (which predicts neuronal-MT-scale OR). User needs to accept this reframing or veto in favor of $50-840 Quantinuum/IonQ-Direct ion-substrate path.

## 8. Race isolation

Writes confined to:
- `state/n_12_v3_ibm_quantum_prep_2026_05_01/` (new, 4 JSONs)
- `docs/n_12_v3_ibm_quantum_prep_2026_05_01.md` (this file)
- `/Users/ghost/n12_v3_ibm/` (off-repo, 3 scripts)

Untouched:
- `state/n_substrate_n12_aws_exec_2026_05_01/` (#39 v1 FAIL frozen)
- `state/n_substrate_n12_aws_exec_v2_2026_05_01/` (#54 v2 INDETERMINATE frozen)
- `state/n_substrate_n12_quantum_pivot_2026_05_01/` (#46 research baseline frozen)
- alpha pod, nexus, all GPU pods (HEXA-only prep mode)

## 9. Sources

- IBM Heron R2 Heron / kingston announcement: https://quantum.cloud.ibm.com/announcements/en/product-updates/2025-04-09-aachen-kingston
- Open Plan kingston rotation 2026-03-16: https://quantum.cloud.ibm.com/announcements/en/product-updates/2026-03-16-open-plan-news
- OpenQASM `delay` feature table: https://quantum.cloud.ibm.com/docs/en/guides/qasm-feature-table
- Qiskit Runtime SamplerV2 docs: https://docs.quantum.ibm.com/api/qiskit-ibm-runtime/sampler-v2
- IBM Quantum plans: https://quantum.cloud.ibm.com/docs/en/guides/plans-overview
- qiskit-ibm-runtime issue #1613 (CLOSED): https://github.com/Qiskit/qiskit-ibm-runtime/issues/1613
- Heron r2 specs (postquantum): https://postquantum.com/industry-news/ibm-heron-r2-quantum/
- IBM Heron Wikipedia: https://en.wikipedia.org/wiki/IBM_Heron
- Korea Quantum Computing partnership: https://newsroom.ibm.com/2024-01-29-Korea-Quantum-Computing-and-IBM-Collaborate-to-Bring-IBM-watsonx-and-Quantum-Computing-to-Korea

## References (qmirror substrate xref, added 2026-05-03)

- `docs/nexus_qmirror_spec_2026_05_03.md` — qmirror canonical substrate spec
- `docs/nexus_qmirror_phase3_calibration_runbook_2026_05_03.md` — IBM calibration anchor runbook
- `docs/ibm_cloud_experiment_list_2026_05_03.md` — $500 IBM Cloud burst plan (qmirror-anchored)
- `docs/qmirror_cond3_ibm_n1_landed_2026_05_03.ai.md` — IBM N1 calibration condition closure
- `docs/qmirror_cond3_band_revise_landed_2026_05_03.ai.md`

---

### See also (qmirror xref history)

Prior callouts preserved verbatim per qmirror_xref_centralization cycle (2026-05-04):

> 📦 Available at: https://github.com/need-singularity/qmirror (`hx install qmirror`)
> 🚀 v2.0.0 RELEASED 2026-05-04 — closure 13/13 conds met (8 v1 + 5 v2): https://github.com/need-singularity/qmirror/releases/tag/v2.0.0

Future qmirror release URLs are canonically tracked in `nexus/.roadmap.qmirror` header field `latest_release_url`. Update single line in roadmap; this footnote is a frozen historical record (do not retrofit).
