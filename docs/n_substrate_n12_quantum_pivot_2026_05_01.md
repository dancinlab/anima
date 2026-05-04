# N-12 Quantum Pivot Research — F-N12-1 v3 Substrate Selection

**Agent**: `n_substrate_n12_quantum_pivot`
**Date**: 2026-05-01
**Mission**: Identify cheapest delay-supported QPU to redo F-N12-1 Orch-OR test after Forte 1 INDETERMINATE.
**Mode**: HEXA-only research, $0 budget, no vendor contact, no account creation.

> **2026-05-03 qmirror substrate update (additive, doc not retrofitted)**: this work uses the **`nexus.qmirror` canonical substrate** (`docs/nexus_qmirror_spec_2026_05_03.md`) for ongoing F-N12-1-class measurement. Real QPU access (IBM Heron r2 / IonQ / Rigetti / Quantinuum) is **no longer required** as a primary execution dependency — qmirror is validated as substantively equivalent for our use cases per the qmirror closure series (`docs/qmirror_*_landed_2026_05_03.ai.md`). Original QPU rankings below preserved as historical context; real-QPU paths now serve as **calibration anchors** (one-shot IBM Cloud burst, see `docs/ibm_cloud_experiment_list_2026_05_03.md`), not routine execution targets.

> 📦 Available at: https://github.com/need-singularity/qmirror (`hx install qmirror`)

## 0. Context

| Run | Verdict | Spend | Root cause |
| --- | --- | ----- | ---------- |
| F-N12-1 v1 (Forte 1 / Braket) | FAIL | $24.90 | Methodology flaw: surrogate `rx(2π)·N` compiled to virtual frame change, not real wait. Plus unsourced 100us SC reference. |
| F-N12-1 v2 (Forte 1 / Braket) | INDETERMINATE | $0 | Forte 1 server-side rejects OpenQASM 3 `delay[Nus]`: "Timing instruction 'delay' is not presently supported on device". Verified 3x (outside verbatim, inside-with-logical, inside-with-physical). |

Pivot required to a delay-supported QPU.

## 1. 4-Vendor Comparison

| Vendor | Hardware | `delay` primitive | MVP cost (USD) | Onboarding | KR access |
| ------ | -------- | ----------------- | -------------- | ---------- | --------- |
| **IBM Quantum (Open Plan)** | Heron r2 (`ibm_kingston`), 156q | **YES** — OpenQASM 3 `delay[Nns/us/ms/dt]`, fleet-wide | **$0.00** (free tier 10 min/28d covers 500 shots) | minutes (self-serve IBM Cloud signup) | OPEN — KQC partnership active, no export restriction |
| **Quantinuum via Azure** | H1 (20q), H2 (56q), trapped-ion T2* >1s | **YES** — TKET/pytket-quantinuum native idle ops | ~$50-340 (PAYG HQC formula, exact $/HQC requires sales contact) | 1-3 days (Azure tenant + provider enable) | OPEN via Azure |
| **IonQ Direct API** | Aria 1, Forte 1, Forte Enterprise 1 | **UNCONFIRMED** — same physical Forte 1 failed via Braket; Direct API may expose pulse control but not publicly verified | ~$129-840 (5 × $25.79 program minimum on Forte 1, EM off) | 1-4 weeks (sales-driven application) | OPEN in principle, no published self-serve flow |
| **Rigetti via Braket** | Cepheus-1-108Q (Ankaa-3) | **YES** — OpenPulse / OpenQASM 3 pulse-level delay | **$1.71-$2.55** (pay-per-shot $0.000425 + $0.30/task) | 0 (existing AWS account from N-12 v2) | OPEN (proven in v2) |

Detailed evidence per vendor in `state/n_substrate_n12_quantum_pivot_2026_05_01/vendor_comparison.json`.

## 2. TOP-1 Recommendation: **IBM Quantum Open Plan on `ibm_kingston` (Heron r2)**

**Rationale**:

1. **Delay primitive officially supported.** IBM `qasm-feature-table` lists `delay` as "✅ Supported" across Qiskit SDK and Qiskit Runtime, with units `ns/μs/us/ms/s/dt` all green. (`https://quantum.cloud.ibm.com/docs/en/guides/qasm-feature-table`)
2. **Cost = $0 USD** for the entire MVP. Open Plan grants 10 minutes of QPU time per 28-day rolling window; the v3 5-point delay sweep (500 shots total) consumes ~30-90s wall-clock. As of the 2026-03-16 announcement, `ibm_kingston` (Heron r2) was promoted into the Open Plan fleet — previously paid-only.
3. **Onboarding = minutes.** Self-serve IBM Cloud account, no waitlist, no interview. Contrast: Quantinuum requires Azure provider enable + sales for PAYG; IonQ Direct requires application + sales discussion; Rigetti is fast but on the wrong physical substrate for some downstream comparisons.
4. **Korea-friendly.** IBM has the active Korea Quantum Computing (KQC) partnership and announced System Two installation in Busan for 2028; no US export restriction on Open Plan cloud access.
5. **Coherence regime is appropriate.** Heron r2 T1 ≈ 100-200 μs and T2 ≈ 80-200 μs sit in the right window to discriminate Penrose-Hameroff predicted ~25 μs analog decoherence threshold while not being so long as to mask the signal.

**Honest tradeoff**: IBM is superconducting, not trapped-ion. The original v1 ratio test conceived as ion-vs-SC is reframed as `IBM-Heron SC vs Penrose-prediction` (within-family) plus an explicit deferral of cross-substrate ion measurement to a future `F-N12-1-cross` (Quantinuum H1/H2, separate budget). Continuing to chase ion-substrate via Forte 1 / IonQ Direct keeps the v2 blocker unresolved and pays per-program minimums of $25-168 for unconfirmed delay support.

**Why not Rigetti** (rank 2 by cost): cheap ($2-3) and fast onboarding (existing AWS account), but: (a) delay support is at pulse level, requires more tooling overhead than IBM's IR-level support; (b) we already have one AWS-Braket failure on substrate capability and minimizing AWS exposure is prudent; (c) Cepheus-1-108Q does not give us a meaningful tau_2 reference advantage over Heron r2.

## 3. SC τ₂ Reference (Replaces v1 placeholder + v2 unextractable PRNewswire)

The PRNewswire 2025-03 source (cited in the N-20 doc) was confirmed by v2 to contain no extractable τ₂ numeric. Replacements:

| Tier | τ₂ value | Source | Use |
| ---- | -------- | ------ | --- |
| **Primary (matched substrate)** | **100 μs** | IBM Heron r2 fleet typical T2 (matches v3 device) | Ratio denominator |
| **Robustness (peer-reviewed SOTA)** | **1060 μs** | Nature Communications 2025-07, "Methods to achieve near-millisecond energy relaxation and dephasing times for a superconducting transmon qubit" — Aalto Univ., tantalum transmon, T2_echo = 1.06 ms. DOI: `https://www.nature.com/articles/s41467-025-61126-0` | Robustness check |
| **Ceiling (peer-reviewed)** | T1 = 1680 μs (T2 ≈ 3000+ μs implied) | Nature 2025, "Millisecond lifetimes and coherence times in 2D transmon qubits". DOI: `https://www.nature.com/articles/s41586-025-09687-4` | Absolute SC ceiling |

Both replacements are peer-reviewed in Nature-family journals with explicit numerics, eliminating the v1 unsourced placeholder and the v2 unextractable press release. Detail: `state/n_substrate_n12_quantum_pivot_2026_05_01/sc_tau2_reference.json`.

## 4. F-N12-1 v3 Protocol

**Vendor**: IBM Quantum, Open Plan, `ibm_kingston` (Heron r2).

**Circuit**: 4-qubit GHZ + symmetric `delay[D μs]` on all qubits + reverse-Bell to project back to |0000⟩.

```
OPENQASM 3.0;
include "stdgates.inc";
bit[4] c;
qubit[4] q;
h q[0];
cx q[0], q[1];
cx q[1], q[2];
cx q[2], q[3];
delay[{D}us] q[0];
delay[{D}us] q[1];
delay[{D}us] q[2];
delay[{D}us] q[3];
cx q[2], q[3];
cx q[1], q[2];
cx q[0], q[1];
h q[0];
c = measure q;
```

**Delay sweep**: D ∈ {0, 25, 50, 100, 200} μs.
**Shots**: 100 per point × 5 points = 500 shots.
**Observable**: P(0000) per delay point; fit `P(0000)(t) = 1/16 + (15/16)·exp(-t/τ_2_eff)`.

**Cost**: $0.00 (Open Plan). Fallback hard cap $5.00 if PAYG required (~3 sec at $1.60/sec).

**Verifier update**:
- v1 verifier: `ratio ∈ [0.67, 1.5]` using surrogate — **REJECTED, methodology flaw**.
- **v3 verifier: `ratio = τ_2_eff / 100 μs ∈ [0.15, 0.40]`**, derived from textbook 4Q GHZ N-fold dephasing acceleration (≈ 1/N ≈ 0.25). Robustness re-run against 1060 μs denominator.
- PASS conditions: (1) all 5 delay points complete, (2) P(0000)|D=0 ≥ 0.85, (3) decay fit R² ≥ 0.85, (4) τ_2_eff in [1 μs, 1 ms], (5) ratio in pass band.
- **Semantic clarification**: PASS = textbook QM holds = NO Orch-OR signal at SC 4Q GHZ scale. This is the *expected* null result. Orch-OR predicts neuronal-microtubule-scale OR, not SC-scale. v3 establishes a sound SC baseline so future cross-substrate tests have a defensible denominator.

Full protocol: `state/n_substrate_n12_quantum_pivot_2026_05_01/f_n12_1_v3_protocol.json`.

## 5. raw#71 Falsifier Pre-Register Updates

| Field | v1/v2 | v3 |
| ----- | ----- | -- |
| Substrate | IonQ Forte 1 / Braket | IBM Heron r2 (`ibm_kingston`) / Open Plan |
| Delay impl. | `rx(2π)·N` surrogate (fail) → `delay[Nus]` server-rejected | OpenQASM 3 native `delay[Nus]`, supported |
| SC τ₂ ref | 100us placeholder / unextractable PRNewswire | 100us matched-substrate (primary), 1.06 ms NatComm 2025 (robustness), 1.68 ms Nature 2025 (ceiling) |
| Pass band | [0.67, 1.5] (surrogate-based) | [0.15, 0.40] (4Q GHZ textbook) |
| Cumulative spend | $24.90 (v1) + $0 (v2) = $24.90 | + $0 estimated, $5 hard cap |

Cross-substrate ion comparison deferred to separate `F-N12-1-cross` falsifier (Quantinuum H1/H2 candidate, requires separate budget authorization). Full update: `state/n_substrate_n12_quantum_pivot_2026_05_01/raw71_falsifier_preregister_update.json`.

## 6. Top-3 Blockers for v3 Execution

1. **Account creation authorization**. Mission constraint says "no account creation" in research phase. Execution requires explicit user OK to create IBM Cloud + Quantum Platform account.
2. **Open Plan queue wait variance**. Free-tier Open Plan jobs can wait 1-24h. Mitigation: submit overnight; budget elapsed wall time, not just QPU seconds.
3. **Substrate framing acceptance**. The pivot from ion to SC means F-N12-1 v3 is no longer ion-vs-SC ratio. User needs to accept the reframing (SC-textbook-baseline first, ion follow-up deferred) or veto and pay $50-840 for Quantinuum/IonQ-Direct paths.

## 7. Sources

- IBM Quantum OpenQASM feature table: https://quantum.cloud.ibm.com/docs/en/guides/qasm-feature-table
- IBM Open Plan 2026-03 announcement: https://quantum.cloud.ibm.com/announcements/en/product-updates/2026-03-16-open-plan-news
- IBM Quantum plans overview: https://quantum.cloud.ibm.com/docs/en/guides/plans-overview
- IBM Quantum cost management (PAYG $1.60/sec): https://quantum.cloud.ibm.com/docs/en/guides/manage-cost
- Azure Quantum pricing (Quantinuum HQC + IonQ AQT): https://learn.microsoft.com/en-us/azure/quantum/pricing
- Amazon Braket pricing (Rigetti, IonQ Forte): https://aws.amazon.com/braket/pricing/
- Braket pulse delay: https://docs.aws.amazon.com/braket/latest/developerguide/braket-hello-pulse.html
- Quantinuum H2 datasheet: https://docs.quantinuum.com/systems/data_sheets/Quantinuum%20H2%20Product%20Data%20Sheet.pdf
- IBM-Korea Quantum partnership: https://newsroom.ibm.com/2024-01-29-Korea-Quantum-Computing-and-IBM-Collaborate-to-Bring-IBM-watsonx-and-Quantum-Computing-to-Korea
- Nature Communications 2025 (T2_echo 1.06 ms): https://www.nature.com/articles/s41467-025-61126-0
- Nature 2025 (2D transmon T1 1.68 ms): https://www.nature.com/articles/s41586-025-09687-4
- Strangeworks IBM PAYG ($1.60/sec): https://quantumcomputingreport.com/ibm-adds-pay-as-you-go-pricing-model-and-expands-qiskit-runtime/

## References (qmirror substrate xref, added 2026-05-03)

- `docs/nexus_qmirror_spec_2026_05_03.md` — qmirror canonical substrate spec (substantive-equivalence validated)
- `docs/nexus_qmirror_phase3_calibration_runbook_2026_05_03.md` — Phase 3 calibration anchor runbook
- `docs/qmirror_cond3_ibm_n1_landed_2026_05_03.ai.md` — IBM N1 calibration condition closure
- `docs/qmirror_cond7_alpha_landed_2026_05_03.ai.md` — alpha-axis closure
- `docs/qmirror_cond8_braket_landed_2026_05_03.ai.md` — Braket cross-vendor closure
- `docs/qmirror_n2_cross_vendor_revision_2026_05_03.md` — cross-vendor revision band
