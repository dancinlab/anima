---
id: Hc_944
slug: nexus-qmirror-module-spec
title: nexus.qmirror — Qiskit Aer + ANU QRNG vacuum-fluctuation = noiseless QPU statistically indistinguishable (~30q state-vec, ~50q MPS) at $0 ongoing. drop-in replacement for HMAC-DRBG + chsh + iit_mip + tomography
domain: quantum-computing, infrastructure
status: candidate-unverified
source_doc: docs/nexus_qmirror_spec_2026_05_03.md
source_lines: 1-40
promoted_at: 2026-05-11
linked_h: Hc_914 (qmirror arxiv draft), H_135 (cycle-3 NEXUS cluster cross-link 2026-05-11)
notes: "Module surface: qrng, chsh, iit_mip, tomography, circuit, phi. Drop-in replacement of HMAC-DRBG. v2.0.0 (2026-05-04). NOT real QPU — no physical entanglement, no quantum advantage."
---

## Hypothesis

QPU 계약 없는 nexus host 가 classical Qiskit Aer state-vector unitary evolution + ANU QRNG vacuum-fluctuation REST API (free) 조합으로 noiseless QPU 와 statistically indistinguishable (~30q state-vec, ~50q MPS) 한 "self quantum computer" 가능. $0 ongoing cost. HMAC-DRBG path + chsh + iit_mip + tomography drop-in replacement.

## Sub-claims

- MATH: Qiskit Aer / Cirq state-vector exact unitary evolution
- MEASUREMENT: ANU QRNG vacuum-fluctuation REST API (free)
- EQUIVALENCE: noiseless QPU statistically indistinguishable in simulator-tractable regime
- TRACTABLE: ~30 qubits state-vector, ~50 qubits MPS
- SURFACE: qrng / chsh / iit_mip / tomography / circuit / phi
- NOT: real QPU, no physical entanglement, no hardware noise model, no quantum advantage

## Migration TODO

- [ ] Hc_914 arxiv draft 와 cross-link 일관성
- [ ] 30→50 qubit MPS scaling 한계
- [ ] ANU QRNG vs HMAC-DRBG 의 statistical test reproducibility
- [ ] noise model injection API
