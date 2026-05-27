---
id: Hc_945
slug: nexus-qrng-ionq-drbg-seed
title: nexus QRNG — IonQ Forte 1 trapped-ion (H^16 |0⟩ + Z-basis, 4096 bits/256 shots, $20.78, 219s queue) → NIST SP 800-90A HMAC-DRBG seed. Bit balance 2037/2059, p_max 0.502686
domain: quantum-computing, cryptography
status: candidate-unverified
source_doc: docs/nexus_qrng_quantum_seed_2026_05_02.md
source_lines: 1-40
promoted_at: 2026-05-11
linked_h: Hc_944, Hc_914, H_135 (cycle-3 NEXUS cluster cross-link 2026-05-11)
notes: "B1 EXEC mission 2026-05-02. IonQ Forte 1 Maryland trapped-ion. Hadamard16 |0⟩ → Z measurement. NIST SP 800-90B simplified MCV."
---

## Hypothesis

nexus runtime PRNG 의 algorithmic urandom seed source 를 IonQ Forte 1 trapped-ion QPU 의 H^16 |0⟩ Z-basis measurement (4096 bits/256 shots, queue 219s, $20.78) 으로 대체 → NIST SP 800-90A HMAC-DRBG. Entropy assessment: bit balance 2037/2059 (ideal 2048/2048), p_max 0.502686 (~ideal 0.5).

## Sub-claims

- DEVICE: IonQ Forte 1 (arn:aws:braket:us-east-1::device/qpu/ionq/Forte-1) trapped-ion
- CIRCUIT: OpenQASM 3.0 — H^16 |0⟩ + Z-basis measurement
- BITS: 4096 (16q × 256 shots), 219s queue, 2026-05-02T14:04:38Z
- COST: $20.78 (Task $0.30 + Shot 256×$0.08=$20.48)
- ENTROPY: bit balance 2037/2059, p_max 0.502686 (NIST SP 800-90B simplified MCV)
- DRBG: NIST SP 800-90A HMAC-DRBG output = nexus seed

## Migration TODO

- [ ] p_max 0.502686 의 deviation 분석
- [ ] bit balance Chi-square test 통계
- [ ] qmirror ANU QRNG (free) vs IonQ Forte ($20.78) 의 trade-off
- [ ] sister-repo PR pending → land
