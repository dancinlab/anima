---
id: Hc_914
slug: qmirror-classical-qpu-mirror
title: qmirror — classical CPU mirror of QPU (Qiskit Aer + ANU QRNG + HMAC-DRBG) 8 closure 통과, IBM Heron r2 CHSH S=2.357±0.050, cross-vendor 4-vendor concordance, $0/sec vs $1.60-2.30/sec
domain: quantum-computing, hardware, statistics
status: candidate-unverified
source_doc: docs/qmirror_arxiv_draft_2026_05_03.md
source_lines: 1-50
promoted_at: 2026-05-11
linked_h: H_002, Hc_902
notes: "arxiv draft v0.1. 8 closure conditions: spec coverage / falsifier-self-test / CHSH existence / NIST SP 800-22 / Bell reproduction / pyphi byte-identical / Rigetti-IBM concordance / 4-vendor matrix."
---

## Hypothesis

Qiskit Aer state-vector simulation + ANU QRNG vacuum-fluctuation REST + HMAC-DRBG SHA-256 의 조합이 simulator-tractable regime (~30 qubits state-vector / 50 qubits MPS) 에서 noiseless QPU 와 statistically equivalent. 8 closure 조건 (spec coverage / falsifier-self-test / CHSH existence S=2.357±0.050 on IBM Heron r2 / NIST SP 800-22 statistical battery / Bell ref S=2.808 vs qmirror 2.838 |Δ|=0.030 / pyphi byte-identical Φ* / Rigetti Cepheus 108Q vs IBM Heron r2 |ΔS|=0.084 / IonQ Aria-1+Forte-1+Rigetti+IBM 4-vendor concordance matrix) 모두 통과. $0/sec vs IBM Heron $1.60-2.30/sec, one-time calibration $41.34.

## Sub-claims

- COND-1: specification coverage (8 closure)
- COND-2: falsifier-driven self-test
- COND-3: CHSH existence proof on IBM Heron r2 ibm_fez, S=2.357±0.050
- COND-4: NIST SP 800-22 statistical battery on QRNG drop-in regression
- COND-5: Bell inequality reproduction (ref 2.808 vs qmirror 2.838, |Δ|=0.030)
- COND-6: IIT 4.0 Φ* pyphi byte-identical validation
- COND-7: cross-family intra-superconducting concordance (Rigetti vs IBM, |ΔS|=0.084)
- COND-8: 4-vendor matrix (IonQ Aria-1, Forte-1, Rigetti Cepheus, IBM Heron r2)
- COST: $0/sec vs $1.60-2.30/sec IBM Heron + one-time $41.34
- CAVEAT-1: simulator-tractable regime 한계 (30 qubits state-vector, 50 qubits MPS)
- CAVEAT-2: 5 honest caveats including post-hoc band revision selection-bias risk

## Migration TODO

- [ ] CHSH 2.357 vs Tsirelson 2√2≈2.828 차이의 noise 모델 정량화
- [ ] Bell |Δ|=0.030 의 statistical significance
- [ ] 30→50 qubit MPS regime 의 simulator complexity scaling
- [ ] 5 honest caveats 의 selection-bias 정량화
