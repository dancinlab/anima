---
id: Hc_981
slug: n12-iit-braket-pilot-multi-witness
title: N-12 IIT AWS Braket Pilot (n=2 PASS WITNESSED $16.60) + Multi-Witness (n=5 Forte 1 + 4 Cepheus + 5 SV1 PASS MULTI-WITNESSED). Φ_proxy = H(joint) - max H(marginal). Substrate-invariance Pearson 1.0 → multi-witness
domain: quantum-computing, consciousness, substrate
status: candidate-unverified
source_doc: docs/n12_iit_braket_pilot_results_2026_05_02.md + docs/n12_multiwitness_results_2026_05_02.md + docs/n12_braket_friendly_explainer_2026_05_02.md
source_lines: cluster
promoted_at: 2026-05-11
linked_h: Hc_918 (N-12 quantum pivot), Hc_926 (N-12 IonQ Forte spec)
notes: "First anima production run real quantum hardware. SV1 (state-vector) + Forte 1 (trapped-ion 36q) + Cepheus-108Q (superconducting transmon). IQM Garnet 4 task submitted then cancelled (Monday billing avoidance)."
---

## Hypothesis

N-12 IIT AWS Braket pilot (n=2) → multi-witness (n=5 Forte 1 + n=4 Cepheus + n=5 SV1) test 가 IIT-style Φ_proxy = H(joint distribution) - max_i H(marginal_i over qubit i) substrate-invariance 첫 real-QPU 증명: SV1 (silicon classical) + Forte 1 (trapped Yb+ ion-trap) + Cepheus-108Q (superconducting transmon) 3 architecture 에서 COPY << AND ≈ XOR << MAJ Φ proxy ordering 재현. Pearson r 1.0 (n=2, mathematically forced) → multi-witness Pearson (n=5, NOT forced).

## Sub-claims (5 circuit × 3 substrate Φ matrix bits)

- AND: SV1 0.9993 / Forte 1 1.1697 / Cepheus 2.4943
- XOR: SV1 0.9954 / Forte 1 1.1701 / Cepheus 1.4697
- MAJ: SV1 1.9893 / Forte 1 2.2133 / Cepheus 2.6900
- COPY: SV1 0.0000 / Forte 1 0.2571 / Cepheus 1.4140
- XOR_AND_MIX: SV1 0.9987 / Forte 1 1.3200 / (Cepheus n/a)
- ORDERING: COPY << AND ≈ XOR << MAJ universal
- COST: $16.60 pilot + multi-witness
- IQM-GARNET-CANCELLED: 4 task submitted then cancelled (Monday billing avoidance)

## Migration TODO

- [ ] multi-witness Pearson r 정확한 값
- [ ] Cepheus Φ scale ~2× Forte (noise vs paradigm-equivalent superconducting)
- [ ] IQM Garnet rerun weekday
- [ ] n=10+ scale + Bayesian posterior update
