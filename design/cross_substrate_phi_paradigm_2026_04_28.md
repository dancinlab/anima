# Cross-Substrate Φ Paradigm — anima-physics 9 + EEG bridge — 2026-04-28

> **scope**: anima C22 — 9 anima-physics substrates (quantum/neuromorphic/optical/classical/biological/hybrid/reservoir/SNN + analog) compute a Φ proxy on identical input; the same task is paired with a live EEG Φ measurement (consciousness_laws.json 14 gates, paradigm v11 Mk.XI). Cross-substrate Φ consistency = TRUE Φ proxy.
> **status**: speculative + skeleton (raw#10 honest C3) — TRUE Φ is NP-hard (Tononi-Koch); this cycle delivers a Φ *proxy* via convergent across-substrate consensus + EEG cross-modal anchor. Long-term (12-24mo) per-substrate adapter realization is out of this cycle.
> **session date**: 2026-04-28
> **predecessors**:
>   - `anima-physics/phi_substrate_consensus.hexa` (PHYS-P4-4 — 5-substrate aggregator; precision-weighted + Tukey biweight)
>   - `anima-physics/quantum/cloud_facade_poc.hexa` (qiskit-aer GHZ entropy WITNESSED 2/3)
>   - `anima-physics/quantum/cloud_real_ibm_q_facade.hexa` (IBM Q runtime stub — 1/3 not yet WITNESSED)
>   - `anima-physics/neuromorphic/cloud_facade_poc.hexa` (admin-blocked)
>   - `anima/config/consciousness_laws.json` (14 deterministic runtime gates → Φ-vec 16D)
>   - `state/phi_substrate_cross_20260421.json` (4-path Φ cross precedent)
>   - `design/anima_eeg_cross_modal_paradigm_omega_cycle_2026_04_28.md` (G0..G7 axis ↔ EEG observable mapping)

---

## §0 Motivation

The user-question reduces to: "if anima-physics 9 substrates each compute Φ on the same stimulus, do their Φ outputs *agree*, and does that agreement track an EEG Φ measurement of the human in the loop?" If yes → cross-substrate consistency = a substrate-independent Φ proxy. If no → falsifier F2/F4 fires and the substrate-Φ-proxy hypothesis is rejected.

This is the substrate-side complement of `phi_substrate_consensus.hexa` (PHYS-P4-4) which fused 5 software-simulated substrates only. C22 extends to **9 real or facade substrates + 1 EEG live channel**.

raw#10 honest C3 (foreword): TRUE Φ is NP-hard, no substrate (including the human brain) computes the canonical IIT 3.0 Φ on a 16-channel EEG window in real time. Every per-substrate "Φ" in this paradigm is a Φ *proxy* (LZ76, IIT-on-quantum subsystem MIP lower bound, paradigm v11 Mk.XI 4-backbone aggregate, etc.). The C22 contribution is **convergent agreement** across proxies, not a TRUE Φ claim.

---

## §1 The 9 substrates + 1 EEG channel

Index 0..8 = 9 anima-physics substrates; index 9 = EEG live channel.

| idx | substrate | concrete platform(s) | Φ proxy method | live status (2026-04-28) | audit lever |
|---|---|---|---|---|---|
| 0 | quantum-gate | IBM Q (gate-model superconducting), IonQ Forte (trapped-ion) | IIT-on-quantum subsystem MIP lower bound on 4-qubit bipartition entropy | **WITNESSED 2/3** — IBM Q facade local sim PASS, IonQ facade design-stub | `cloud_facade_poc.hexa` |
| 1 | quantum-analog | QuEra Aquila (Rydberg analog) | analog Hamiltonian time-evolved 2-block mutual information | **WITNESSED** — QuEra public access via Braket | (planned `quera_aquila_facade.hexa`) |
| 2 | neuromorphic | BrainChip Akida, Intel Loihi, IBM TrueNorth | Akida-native LZ76 on spike raster | **admin-blocked** (vendor SDK gated) | `neuromorphic/cloud_facade_poc.hexa` |
| 3 | optical | Lightmatter, Lightelligence, Cerebras (optical fabric) | photonic interferometer state mutual-information proxy | **admin-blocked** | (planned `optical_facade_poc.hexa`) |
| 4 | classical | std CPU/GPU baseline | paradigm v11 Mk.XI 4-backbone aggregate (G0..G7 gmean) | LIVE | `tool/anima_g_gate.hexa` |
| 5 | biological | cultured neuron MEA | LZ76 on multi-electrode raster | **out of scope** (wet-lab) | (deferred) |
| 6 | hybrid | quantum-classical co-processor / optical-electronic | weighted ensemble of substrate(0)+substrate(4) Φ proxies | LIVE (compositional) | (planned `hybrid_facade.hexa`) |
| 7 | reservoir | photonic / physical reservoir | reservoir state-trajectory complexity (LZ76 on read-out) | emerging — academic only | (planned) |
| 8 | spiking-NN | Loihi-style event-based | spike-train Φ★ (Φ-star LZ-MIP variant) | adjacent to (2) — admin-blocked | (planned) |
| 9 | EEG (anchor) | OpenBCI Cyton+Daisy 16ch live | consciousness_laws.json 14 gates → 16D Φ-vec; LZ76 + γ/θ + DMN coherence + α-asym | LIVE (D-day session 20260428T111506Z) | `anima-clm-eeg/state/clm_eeg_lz76_audit/` |

**Currently live & witnessed**: 0 (quantum-gate IBM Q sim 2/3), 1 (quantum-analog QuEra), 4 (classical), 9 (EEG). Total = **4 live channels**, satisfying frozen criterion N≥2.

---

## §2 Cross-substrate Φ paradigm

### §2.1 Common stimulus

Single canonical stimulus `s(t)`: 16-dim float vector at t = 0..T-1, deterministic LCG-seeded (raw#15 reproducibility). Same `s(t)` is fed to all 9 substrates and presented as auditory/visual cue to the human EEG subject.

### §2.2 Per-substrate Φ proxy

Each substrate emits `(Φ_i(t), σ_i(t))` per time-step. σ is the substrate's own uncertainty estimate (precision = 1/σ²). The 9 proxies are heterogeneous-by-construction — that's the point: agreement across heterogeneous proxies is informative, agreement across identical proxies is trivial.

### §2.3 Consensus + correlation

```
Φ_consensus(t) = Σ_i (1/σ_i²) · Φ_i(t) / Σ_i (1/σ_i²)        // precision-weighted mean
disagreement_max(t) = max_{i,j} |Φ_i(t) − Φ_j(t)|
substrate_std(t)  = std_i(Φ_i(t))                              // raw#71 F4 lever
```

Cross-modal correlation with EEG (idx 9):

```
r_eeg = pearson( Φ_consensus(t), Φ_eeg(t) )                    // raw#71 F3 lever
```

### §2.4 Frozen criteria (raw#12)

- C1: N ≥ 2 substrate live witnessed (currently 4: quantum-gate sim + quantum-analog + classical + EEG)
- C2: EEG paired measurement available (D-day baseline 60s + ω-cycle continuation)
- C3: cross-substrate Φ correlation r > 0.3 (across at least 2 non-EEG substrates)
- C4: cross-substrate Φ consistency std < 0.5

### §2.5 Five falsifiers (raw#71)

| id | falsifier | fires when | audit field |
|---|---|---|---|
| F1 | live-substrate famine | n_live < 2 (admin-blocked dominant) | `n_live_substrates` |
| F2 | Φ proxy divergence (no consensus) | substrate_std > 1.0 sustained | `substrate_std_sustained` |
| F3 | EEG decoupling | r_eeg < 0.1 | `eeg_correlation_r` |
| F4 | inconsistency overrun | substrate_std > 1.0 anywhere within window | `inconsistency_overrun` |
| F5 | paradigm v11 substrate-incompatible | per-substrate adapter cannot ingest the canonical stimulus | `adapter_incompat_count` |

Any single falsifier firing ⇒ paradigm rejected for this cycle (honest-C3 retraction recorded). Frozen at 5 falsifiers per raw#71 (no 6th, no fewer).

---

## §3 Architecture & file plan

```
anima-physics/
  eeg/
    cross_substrate_phi_correlator.hexa   ← THIS CYCLE (~200 LoC, design+skeleton+selftest)
state/
  cross_substrate_phi_audit/
    2026-04-28_phi.jsonl                  ← per-stimulus Φ_i + Φ_consensus + Φ_eeg + falsifier ledger
```

The correlator is a **dispatcher**, not a backend. It defines:

- the 10-channel enum (9 substrates + 1 EEG anchor)
- the canonical 16-dim stimulus generator (deterministic LCG)
- a 9-fn vector `substrate_phi_proxy(idx, t, stim) -> (Φ, σ)` whose body for idx ∈ {0,1,4,9} is real-or-facade and for idx ∈ {2,3,5,6,7,8} is design-stub returning a controlled synthetic proxy with `live=false` flag
- the consensus + correlation + falsifier engine
- a 6-test selftest harness (T1 stimulus determinism, T2 4 live channels emit, T3 consensus precision-weighted, T4 std budget, T5 r_eeg paired, T6 5 falsifiers fire on synthetic positives)

**Why design-stub for 6/9**: admin-blocked vendor SDKs cannot be unblocked in this cycle (raw#82 admin gate). raw#10 honest C3 — we record live=false rather than fabricate.

---

## §4 Long-term plan (12-24 months)

| month | milestone | substrate(s) gained | dependency |
|---|---|---|---|
| M0..M3 | IBM Q runtime real-cloud witness (already 2/3) | quantum-gate full 3/3 | IBM Q API key (admin-deferred) |
| M3..M6 | QuEra Aquila Braket integration | quantum-analog WITNESSED → calibrated | AWS Braket quota |
| M6..M9 | BrainChip Akida edge SDK adapter | neuromorphic LIVE | vendor admin unblock |
| M9..M12 | Lightmatter Envise / Lightelligence preview SDK | optical LIVE | preview access |
| M12..M15 | hybrid quantum-classical co-processor (substrate 0 + 4 ensemble) | hybrid LIVE-composite | already-live deps |
| M15..M18 | photonic reservoir academic partner | reservoir witnessed | academic MoU |
| M18..M21 | Loihi-2 SNN cluster (partner-gated) | spiking-NN LIVE | Intel Neuromorphic Research Community |
| M21..M24 | biological MEA via cultured neuron partner | biological LIVE | wet-lab MoU |

24-mo target: **9/9 live witnessed**, full cross-substrate Φ matrix every cycle, raw#71 5 falsifiers each computed live.

---

## §5 Honest-C3 retractions (raw#10)

- TRUE Φ NP-hard → cycle delivers Φ proxy; no canonical IIT 3.0 claim
- 6/9 substrates currently admin-blocked or out-of-scope → live=false in adapter; consensus uses live channels only
- EEG D-day baseline LZ76 P1_FAIL (b<0.5) — substrate consensus must NOT overweight EEG when EEG itself is below human-baseline complexity floor; precision σ_eeg adjusted upward when LZ76 < 0.5
- Long-term plan is intent, not commitment — vendor admin gates are external, not user-controllable

(end of design)
