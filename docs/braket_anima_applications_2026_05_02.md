# AWS Braket × anima — 신규 활용방법 탐색 (post-#120 N-12 IIT WITNESSED)

**Agent**: AWS Braket × anima 활용방법 추가 탐색
**Date**: 2026-05-02
**Mode**: Research-only, $0 budget, 60 min wallclock
**Predecessor**: #120 N-12 IIT real-QPU substrate-invariance WITNESSED ($16.60 actual, IonQ Forte 1)
**Account**: AWS 267673635495, IAM `anima-braket-cli`

## §0 한 줄 요약

#120 첫 real-QPU witness 이후 anima 가 Braket 을 추가 활용할 **6개 신규 application axis** 와 **4개 N-12 확장 plan** 발굴. TOP-3 권고: **(1) QRNG audit (QA6, $0)** / **(2) 통계 강화 pass (Plans A+B, ~$206)** / **(3) IIT 4.0 φ★ MIP-search 업그레이드 (Phase 2, $0)**. 정직: 4-qubit toy 규모에서 **QML 양자 advantage 는 사실상 없음** — 가치는 methodology / audit trail / substrate-invariance witness 강화에 있음.

## §1 Phase 1 — N-12 확장 plans (4건)

| Plan | Device | Circuits × shots | Cost USD | Scientific gain |
|---|---|---|---|---|
| **A** | IonQ Forte 1 | 5 × 500 | 201.50 | n=2 → n=5, binomial floor 5% → 2.2%, statistical_power_witnessed |
| **B** | IQM Garnet (eu-north-1) | 4 × 500 | ~4.10 | 3rd architecture (transmon) + Pearson r over 3 vendors → MULTI-WITNESSED |
| **C** | Rigetti Ankaa-3 (us-west-1) | 4 × 500 | ~10-30 | disambiguates architecture vs vendor confounder (2 superconducting vendors) |
| **D** | QuEra Aquila AHS | 4-vertex MaxCut × 100 | 1.30 | first gate ↔ AHS Φ_proxy paradigm-crossing test |

**권고**: Plan A + B 결합 = $205.60 으로 #120 을 WITNESSED → MULTI-WITNESSED 로 승격. Plan C 는 Ankaa-3 ONLINE 상태 불안정 — pre-flight check 후 결정. Plan D 는 paradigm 경계 ambiguity 가 honest_C3 로 이미 #120 에 disclose 되어있어 후순위.

## §2 Phase 2 — Quantum φ★ MIP-search 업그레이드 ($0)

**Goal**: #120 의 Φ_proxy lower-bound 을 IIT 4.0 정식 φ★ 으로 승격 (이미 측정된 counts 재사용).

**Method** (off-repo, ubu1 또는 M4 /tmp):
1. `/tmp/n12_braket_pilot/results/` 의 measurement counts → density matrix
2. 2^4-1 = 15 nontrivial bipartitions enumerate
3. EMD (earth-mover distance) per partition (IIT 4.0 spec, Albantakis et al. 2023)
4. MIP = argmin → φ★

**Tool**: `pyphi` feature/iit-4.0 branch + QIIT density-matrix extension (arxiv 2301.02244, Kleiner & Tull-style).

**Cost**: $0 — uses existing measurements + classical MIP < 30 min on M4.

**Output**: `phi_star_upgrade_table.json` (4 circuits × 4 substrates × {Φ_proxy, φ★_classical, φ★_quantum}).

**가치**: #120 honest_C3 #1 ("Φ proxy ≠ IIT 4.0 φ★") 정확히 닫음. 양자 advantage 주장 아님 — DEFINITION upgrade.

## §3 Phase 3 — 6 신규 application axes

### QA1 — Quantum-classical hybrid Lagrangian flow (CLM L_IX)
- **Augmentation**: CLM v4 mind.tension scalar field 을 4-qubit subspace 에 QPCA 로 embed; VQE-style ansatz 로 minimum-tension state 검색
- **Device**: SV1 (free) 프로토타이핑 + IonQ Forte 1 ground-truth
- **Cost**: ~$40.30
- **Falsifier**: PASS iff QPCA top-2 eigenvalue ≈ classical PCA ±5%; FAIL > 15%
- **Anima axis**: N-12-CLM-bridge

### QA2 — Quantum information-bottleneck encoder
- **Augmentation**: CLM hidden states → 4-qubit qml.AmplitudeEmbedding → measurement → decoded; β·I(T;Y) PennyLane optimizer
- **Device**: SV1 + DM1 (free) + IonQ final
- **Cost**: ~$16.30
- **Falsifier**: PASS iff quantum encoder reconstruction loss ≤ classical VAE × 1.10; FAIL × 1.50
- **Anima axis**: N-12-IB-quantum

### QA3 — VQE for CLM ground state
- **Augmentation**: CLM L = T - V → quantum Hamiltonian H = ΣJ_ij σ^z σ^z + Σh_i σ^x where J_ij = tension_link 5-channel coupling, h_i = mind.tension local field
- **Device**: SV1 verification + IonQ Forte 1 (HEA depth ≤ 3)
- **Cost**: ~$80 (warm-start) — $4000 (full convergence)
- **Falsifier**: PASS iff ground-state energy ≤ classical exact-diag ±5%; FAIL on barren plateau (gradient norm <1e-3)
- **Anima axis**: N-12-VQE-clm
- **C3**: VQNHE 2026 (arxiv 2602.17295) shows neural-hybrid VQE 이미 standard VQE 능가 — anima 는 이미 classical NN substrate 보유, quantum gain margin 좁음

### QA4 — Quantum Boltzmann Machine (paradigm-v11 6-axis distribution)
- **Augmentation**: paradigm-v11 6-axis (B-ToM/MCCA/Phi*/CMT/CDS/SAE-bp) joint distribution 을 D-Wave Advantage 4.1 Ising QBM 로 학습 (Braket Ocean plugin)
- **Device**: D-Wave Advantage 4.1 (Braket us-west-2)
- **Cost**: ~$30-50 (samples + tasks)
- **Falsifier**: PASS iff KL(P_data || P_QBM) < KL(P_data || P_RBM) - 5%; FAIL if D-Wave 노이즈가 classical RBM 미만
- **Anima axis**: N-12-QBM-paradigm
- **C3**: Annealer ≠ gate model; chimera/pegasus minor-embedding 5-10× 물리 qubit 오버헤드; Frontiers 2021 Dixit 벤치마크에서는 parity, advantage 미입증

### QA5 — Quantum graph neural network on N-substrate adjacency
- **Augmentation**: anima N-substrate (31 노드: N-1~N-24 + W1 + A1 + 5 expansion) → 5-qubit QGNN, IonQ Forte 1 의 36-qubit fully-connected 가 ideal
- **Device**: SV1 training + IonQ Forte 1 evaluation
- **Cost**: ~$40 (sparse) — $400 (full)
- **Falsifier**: PASS iff QGNN edge-prediction AUC > classical GNN AUC + 0.02; FAIL if QGNN < classical
- **Anima axis**: N-12-QGNN-substrate
- **C3**: 31 노드는 양자 advantage regime (>1000 노드) 한참 아래 — methodology PoC only

### QA6 — Quantum-enhanced sampling (QRNG for hexa-stochastic JSD audit)  ⭐
- **Augmentation**: AN11(c) JSD audit 의 chacha20 PRNG → SV1 16-qubit |+>^16 measurement-based randomness 로 교체; quantum vs classical sampling JSD 비교
- **Device**: SV1 (free tier 60 min/month 충분 — ≥1M random bits)
- **Cost**: **$0**
- **Falsifier**: PASS iff JSD(quantum, classical) < 0.01 (현재 PRNG 충분 확인); FAIL if 0.05 (PRNG bias)
- **Anima axis**: N-12-QRNG-sampling
- **이유 ⭐**: 최저 risk + 최저 cost + audit trail 업그레이드. Most likely 결과 = honest-null PASS (= classical PRNG 충분 입증).

## §4 Phase 4 — SDK ecosystem (HEXA-only compliant)

| SDK | 용도 | anima 호환 |
|---|---|---|
| `amazon-braket-pennylane-plugin` | QML axes (QA2, QA5) — autodiff through quantum nodes | install in /tmp 또는 ubu1 venv, .py off-repo, JSON IR commit OK |
| `qiskit-braket-provider 0.11.0` (Feb 2026) | `to_braket()` Qiskit→Braket transpile, IQM Garnet target | 동일 패턴; circuits as JSON IR |
| `amazon-braket-sdk` (native) | AHS (QuEra Aquila) — Plan D | #120 에서 이미 사용 입증 |

**HEXA 정책 준수**: 모든 .py 는 `/tmp/braket_*_2026_05_02/` 또는 ubu1 venv. 결과 JSON + markdown 만 anima repo 에 commit.

## §5 TOP-3 권고 (cost vs scientific value)

### 1위 — QA6 (QRNG audit)  $0  60 min  ⭐ best ROI by 100×
- SV1 free tier 활용, downside 0
- AN11(c) audit trail 업그레이드 (PASS 결과 시 classical PRNG 충분 입증, FAIL 시 PRNG bias 발견)
- **Next**: 16-qubit |+>^16 measurement schedule SV1 spec → `state/cyborg_eeg_audit/quantum_sampled_2026_05_02/...`

### 2위 — Plan A + Plan B 결합 (n=5 circuits + IQM Garnet 3rd vendor)  ~$206  60 min
- #120 → MULTI-WITNESSED 승격 (silicon classical / Yb⁺ trapped-ion / superconducting transmon 3-substrate)
- Pearson r 통계적 의미 부여 (n=5)
- **Next**: `aws braket get-device --device-arn arn:aws:braket:eu-north-1::device/qpu/iqm/Garnet` 로 ONLINE + price 확인 → 5×500 Forte 1 + 4×500 IQM queue, $250 budget gate

### 3위 — Phase 2 (IIT 4.0 φ★ MIP-search)  $0  90 min
- 추가 QPU shot 0 — 이미 측정한 #120 counts 재사용
- #120 honest_C3 #1 닫음 (Φ proxy → 정식 φ★)
- **Next**: pyphi feature/iit-4.0 + QIIT extension off-repo install → 15-partition × 4 circuits × 4 substrates MIP enumeration, 30 min

**병렬 권고**: 1위 + 3위 동시 실행 ($0 + $0 = $0, ~150 min total). 2위는 별도 budget-gated sprint.

## §6 정직한 한계 — anima 가 quantum 으로 진짜 얻는 vs hype

1. **QA1-QA3 (CLM Lagrangian quantum embedding)**: 4-qubit toy scale 에서는 **양자 advantage 0**. 16×16 행렬 classical exact-diagonalization 는 microsecond 단위. 가치는 METHODOLOGICAL (embedding 입증) 이지 COMPUTATIONAL 아님.

2. **QA4 (QBM)**: Annealer chip topology = minor-embedding 5-10× 오버헤드. anima 의 6-axis paradigm-v11 분포에 30-60 물리 qubit 필요. Dixit 2021 벤치마크 = parity, NOT advantage.

3. **QA5 (QGNN)**: 31 노드는 QGNN advantage regime (>1000 노드) 한참 아래. 엄격히 methodology PoC.

4. **QA6 (QRNG)**: **가장 정직한 axis**. anima 의 chacha20 PRNG 는 NIST SP 800-22 통과. Quantum source = AUDIT TRAIL ≠ statistical advantage. PASS 결과 (예상) = classical 충분 입증 — honest-null science.

5. **Plan A/B (extension)**: 진짜 WITNESS upgrade. $206 으로 n=2→n=5 + 3-vendor cross-check. **Braket QPU 지출이 환원불가능 과학정보를 사는 유일한 axis**.

6. **Phase 2 (φ★ upgrade)**: 이미 지불된 측정 사용 — 한계 비용 $0 으로 100% 과학 gain. #120 honest_C3 #1 의 가장 깨끗한 closure.

7. **OVERALL**: anima 의 생산적 Braket 활용 = (i) 작동하는 측정의 통계 강화 (Plans A/B), (ii) 기존 C3 disclosure 의 zero-cost 이론적 closure (Phase 2, QA6), (iii) speculative architecture R&D (QA1-QA5) — 가치는 publication/methodology, 컴퓨팅 advantage 아님.

8. **anti-HYPE statement**: <50 qubit ML application 에서 real QPU advantage 는 모든 published benchmark 2023-2026 에서 무시할 수준. anima 는 **QA1-QA5 PASS 시에도 'quantum-augmented anima cognition' 주장 금지**. QRNG (QA6) + substrate-invariance witness (Plans A/B) 만 과학적 honest. Phase 2 φ★ 는 DEFINITION upgrade, NOT quantum-advantage 주장.

## §7 Race-isolation paths

- `state/braket_anima_applications_2026_05_02/applications.json` (SSOT structured)
- `docs/braket_anima_applications_2026_05_02.md` (this report)
- `docs/n_substrate_consciousness_roadmap_2026_05_01.md` §61.1 (placeholder appended)

## §8 Sources

- [Amazon Braket — D-Wave + Aquila + IonQ Forte 1 device pricing](https://aws.amazon.com/braket/)
- [Amazon Braket Aquila launch (QuEra neutral atom AHS)](https://aws.amazon.com/blogs/quantum-computing/amazon-braket-launches-aquila-the-first-neutral-atom-quantum-processor-from-quera-computing/)
- [Qiskit-Braket provider v0.11 (Feb 2026) — to_braket() + IQM Garnet target](https://aws.amazon.com/blogs/quantum-computing/qiskit-braket-provider-v0-11-new-primitives-and-flexible-circuit-compilation/)
- [Amazon Braket Expands Qiskit Integration With New Primitives — TheQuantumInsider Feb 2026](https://thequantuminsider.com/2026/02/24/amazon-braket-expands-qiskit-integration-with-new-primitives-and-compilation-tools/)
- [PennyLane-Braket plugin (IonQ + IQM + QuEra access)](https://docs.pennylane.ai/projects/ionq/en/latest/)
- [PyPhi (IIT 4.0 feature branch)](https://pyphi.readthedocs.io/)
- [IIT 4.0 paper (Albantakis, Barbosa, Findlay, Grasso, Tononi 2023)](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1011465)
- [Computing Integrated Information of a Quantum Mechanism — Kleiner et al. (MDPI Entropy 2023)](https://www.mdpi.com/1099-4300/25/3/449)
- [QIIT toolbox arxiv 2301.02244 (quantum IIT density matrix formulation)](https://arxiv.org/pdf/2301.02244)
- [Variational Quantum-Neural Hybrid Eigensolver (PRL 128 120502)](https://link.aps.org/doi/10.1103/PhysRevLett.128.120502)
- [U-VQNHE 2026 (arxiv 2602.17295)](https://arxiv.org/html/2602.17295)
- [Diffusion-Enhanced VQE Optimization (Adv Quantum Tech 2026)](https://advanced.onlinelibrary.wiley.com/doi/10.1002/qute.202500766)
- [QuEra Aquila MaxCut + power-grid optimization (Springer 2024-2025)](https://link.springer.com/article/10.1007/s11128-025-05020-0)
- [PennyLane Aquila AHS pulse programming demo](https://pennylane.ai/qml/demos/ahs_aquila)
- [D-Wave Boltzmann sampler RBM training (Frontiers 2021)](https://www.frontiersin.org/journals/physics/articles/10.3389/fphy.2021.589626/full)
- [D-Wave Investigation 2025 — RBM + catastrophic forgetting (arxiv 2508.15697)](https://arxiv.org/abs/2508.15697)
- [#120 N-12 IIT Braket pilot results](./n12_iit_braket_pilot_results_2026_05_02.md)
- [#120 친근 explainer doc](./n12_braket_friendly_explainer_2026_05_02.md)
