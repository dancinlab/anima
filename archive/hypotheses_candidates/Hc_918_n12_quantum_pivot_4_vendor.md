---
id: Hc_918
slug: n12-quantum-pivot-4-vendor
title: N-12 Quantum Pivot — IBM Heron r2 (Open Plan $0) > Quantinuum H1/H2 ($50-340) > IonQ Direct ($129-840) > Rigetti Cepheus ($1.71-2.55). delay primitive 지원 + Penrose-Hameroff 25μs analog decoherence 검출 가능
domain: quantum-computing, consciousness
status: candidate-unverified
source_doc: docs/n_substrate_n12_quantum_pivot_2026_05_01.md
source_lines: 1-50
promoted_at: 2026-05-11
linked_h: Hc_902 (N-substrate), Hc_914 (qmirror)
notes: "F-N12-1 v1 FAIL (Forte 1 surrogate methodology) → v2 INDETERMINATE (OpenQASM3 delay rejected) → v3 pivot to IBM Heron r2. Heron r2 T1≈100-200μs, T2≈80-200μs."
---

## Hypothesis

Penrose-Hameroff Orch-OR 25μs analog decoherence threshold 검출 가능한 QPU 4-vendor 비교: IBM Heron r2 Open Plan ($0 free tier, delay primitive 공식 지원, Korea-friendly KQC partnership) > Quantinuum H1/H2 (trapped-ion T2*>1s, $50-340 PAYG) > IonQ Direct (unconfirmed delay, $129-840) > Rigetti Cepheus ($1.71-2.55, pulse-level delay). IBM Heron r2 T1≈100-200μs, T2≈80-200μs 가 25μs threshold 검출에 적합.

## Sub-claims

- IBM-OPEN: Heron r2 ibm_kingston 156q + delay primitive (ns/μs/us/ms/s/dt) + $0 + 10min/28d + KQC partnership
- QUANTINUUM: H1 (20q), H2 (56q), trapped-ion T2*>1s, TKET/pytket idle ops, $50-340 PAYG
- IONQ: Aria 1 / Forte 1 / Forte Enterprise 1, delay UNCONFIRMED, $129-840
- RIGETTI: Cepheus-1-108Q (Ankaa-3), OpenPulse/OpenQASM3 pulse-delay, $1.71-2.55
- PENROSE-25us: ~25μs analog decoherence threshold prediction
- HERON-WINDOW: T1≈100-200μs, T2≈80-200μs 가 25μs discrimination 적합
- v1 root cause: surrogate rx(2π)·N compiled to virtual frame change, not real wait
- v2 root cause: Forte 1 OpenQASM3 'delay' server-rejected ×3

## Migration TODO

- [ ] IBM Heron r2 v3 실행 (5-point delay sweep, 500 shots, 30-90s wall-clock)
- [ ] qmirror 2026-05-03 substrate update — 실QPU access optional
- [ ] cross-substrate ion measurement (Quantinuum H1/H2) future F-N12-1-cross
- [ ] Penrose-Hameroff 25μs threshold prediction source
