# kuramoto_neuromorphic — Kuramoto Coupling on Spiking Neuromorphic Substrate

> anima-physics HW target #3 — `social/kuramoto_coupling.hexa` substrate
> (§188 PASS 6/6) 의 Intel **Loihi 2** + BrainChip **Akida** neuromorphic
> mapping.
>
> Mac local Phase 1a: numpy oscillator-network sim (N=8, T=1000)
> + Python adapter syntactic compile ($0 / immediate).
> Phase 1b: Intel NRC (Loihi 2 cloud) + BrainChip MetaTF cloud submit
> (cloud-only — Mac에 실 HW 없음).
>
> Cross-link: [DESIGN of HW silicon path §2.3](../../../HEXAD/PHYSICS/HW_SILICON_PATH.md) ·
> [SW substrate spec](../../social/kuramoto_coupling.hexa) ·
> reference: [strange_loop_ice40](../strange_loop_ice40/DESIGN.md)
> (FPGA target #1 patterned-after).

---

## §1 GOAL

`kuramoto_coupling.hexa` 의 `simulate_network(N, K, steps, dt, seed)` 의
N-oscillator continuous-phase Kuramoto dynamics 를 **spiking neuromorphic
substrate** 위에 mapping. Loihi 2 의 graded-spike + asynchronous fabric
은 phase oscillator 의 sub-threshold dynamics 에, Akida 의 event-driven
binary-spike + weighted coupling 은 phase-locked attractor 형성에 자연
적합. order parameter `r = |1/N · Σ e^{iθ_j}|` 를 spike-rate 또는
phase-resolved spike-time readout 에서 복원.

## §2 architecture (ASCII)

```
┌─────────────────────────────────────────────────────────────────────────┐
│ kuramoto_neuromorphic — Spike Substrate (clock-LESS asynchronous fabric)│
│                                                                          │
│   Oscillator-i   ω_i (intrinsic freq)        Oscillator-j   ω_j         │
│   ┌──────────────┐                            ┌──────────────┐          │
│   │ PHASE_ACC_i  │   spike when θ ≥ 2π        │ PHASE_ACC_j  │          │
│   │ θ_i(t) ∈[0,2π)│  →  emit spike  ─────┐    │ θ_j(t) ∈[0,2π)│         │
│   │ + bias ω_i   │     θ_i ← θ_i − 2π   │    │ + bias ω_j   │          │
│   └──────┬───────┘                       │    └──────┬───────┘          │
│          │                               │           │                  │
│          │   coupling current            │           │                  │
│          │   I_i = (K/N)·Σ sin(θ_j−θ_i) │           │                  │
│          │   ◄─────────────── async ─────┼───────────┘                  │
│          ▼                               ▼                              │
│   ┌──────────────────────────────────────────────────────┐              │
│   │  COUPLING MATRIX (all-to-all, weight K/N)            │              │
│   │  ┌────┬────┬────┬────┬────┬────┬────┬────┐          │              │
│   │  │ 0  │K/N │K/N │K/N │K/N │K/N │K/N │K/N │ row 0   │              │
│   │  ├────┼────┼────┼────┼────┼────┼────┼────┤          │              │
│   │  │K/N │ 0  │K/N │ …                       row 1   │              │
│   │  │ …                                                │              │
│   │  └──────────────────────────────────────────────────┘              │
│   │  (Loihi 2 dendrite tree / Akida CNP fully-connected weights)       │
│   └──────────────────────────────────────────────────────┘              │
│                                                                          │
│   ┌──────────────────────────────────────────────────────┐              │
│   │  READOUT — order parameter r                         │              │
│   │   spike-time histogram per oscillator                │              │
│   │   → estimate θ_i(t) from inter-spike interval        │              │
│   │   → r = | (1/N) · Σ exp(i·θ_i) |                     │              │
│   │   Loihi 2: graded-spike payload carries phase        │              │
│   │   Akida:   spike-rate-coded phase (1 spike / cycle)  │              │
│   └──────────────────────────────────────────────────────┘              │
│                                                                          │
│   time substrate: **CLOCK-LESS** asynchronous event-driven              │
│      (vs FPGA target #1 strange_loop_ice40 which has explicit posedge   │
│       clk + 8 × 3-bit registers updating in lockstep)                   │
│      → spikes are timestamped events; no global clock domain;           │
│        coupling propagates ASAP through dendrite tree                   │
└──────────────────────────────────────────────────────────────────────────┘

NEUROMORPHIC ≠ FPGA — key differences:
   FPGA (strange_loop_ice40)       neuromorphic (this target)
   ───────────────────────────     ────────────────────────────────────
   synchronous posedge clk         asynchronous spike events
   bit-identical RTL simulation    spike-train statistical equivalence
   yosys → bitstream → board       Python SDK → cloud submit (Loihi 2 NRC,
                                     Akida MetaTF) — Mac에 실 HW 없음
   $70 dev board (UPduino v3)      cloud quota (Intel NRC), $0 educational
   iverilog Mac local exact sim    numpy continuous-phase sim (this design)
                                     — neuromorphic exact sim 은 NxSDK/MetaTF
                                     cloud 가 필요
```

## §3 file structure

```
hw/kuramoto_neuromorphic/
├── DESIGN.md                       ← 본 문서
├── README.md                       ← quick-start
├── src/
│   ├── kuramoto_local_sim.py       ← numpy N=8 oscillator sim
│   │                                  + F-HW-KU-1..5 falsifier
│   ├── kuramoto_loihi2_adapter.py  ← Intel NxSDK skeleton (cloud submit)
│   └── kuramoto_akida_adapter.py   ← BrainChip MetaTF skeleton (cloud submit)
├── build.sh                        ← local sim + adapter syntax check
└── state/                          ← compile / sim artifacts
    ├── sim.log                       (kuramoto_local_sim output)
    └── adapter_syntax.log            (py_compile output for adapters)
```

## §4 SW ↔ neuromorphic mapping

| `kuramoto_coupling.hexa` | Loihi 2 (NxSDK) | Akida (MetaTF) |
|---|---|---|
| `make_omegas(n, seed)` Gaussian ω_i | `nx.Compartment(bias=ω_i)` per neuron | `akida.InputLayer` with bias offsets |
| `make_initial_phases(n, seed)` θ_i(0) | `compartment.phase = θ_i(0)` (graded init) | `InputLayer.activation = θ_i/(2π)` |
| `kuramoto_step(phases, ω, K, dt)` | dendritic accumulator: `I_i = Σ_j w_ij·sin(θ_j−θ_i)`, weights `w_ij = K/N` | `FullyConnected(weights=K/N · all-ones)` layer feedback |
| `next = θ_i + dt·(ω_i + I_i)` | LIF compartment voltage update + threshold-cross-spike | spike emit when activation ≥ 1.0, wrap to 0 |
| `cos(θ_i), sin(θ_i)` for `r` | graded-spike payload (Loihi 2: 8-bit graded value) | inter-spike interval decode (Akida: rate-coded) |
| `order_params(phases) → [r, ψ]` | host-side post-process from spike train | host-side post-process from spike-rate histogram |
| `simulate_network(...)` exposed API | `nx.Network.run(num_steps=steps)` cloud submit | `model.fit(...)` + cloud inference |
| 6/6 PASS self-test (T1..T6) | F-HW-KU-1..5 (this DESIGN.md) | F-HW-KU-1..5 (this DESIGN.md) |

## §5 falsifier (HW Phase 1a — Mac local numpy sim)

| ID | Test | Expected |
|---|---|---|
| F-HW-KU-1 | Phase initialization uniform random in [0, 2π) | mean(θ_i(0)) ≈ π, std(θ_i(0)) ≈ π/√3 (≈ 1.81) within ±20% over N=8, 1 seed |
| F-HW-KU-2 | K below critical (K=0.1) → r low | r_tail(K=0.1) < 0.3 (matches SW T2) |
| F-HW-KU-3 | K above critical → r high | r_tail(K=5.0) > 0.7 (with OMEGA_STD=1.5 → K_c≈2.4; K=2.0 sits just below K_c and stochastic finite-N drift keeps r ≲ 0.65, so the falsifier uses K=5.0 which is genuinely above critical. r(K=2.0) ≈ 0.6 is still emitted in the summary line for traceability.) |
| F-HW-KU-4 | Order parameter monotone in K sweep | mean over 3 seeds: r̄(K=0.1) ≤ r̄(K=1.0) ≤ r̄(K=5.0) |
| F-HW-KU-5 | Long-time stability (last 100 steps) | std(r[last 100]) < 0.1 at K=2.0 (locked regime stable) |

## §6 build pipeline (Phase 1a — Mac local $0)

```bash
# 1. local numpy oscillator-network simulation
cd hw/kuramoto_neuromorphic/
./build.sh sim       # python3 src/kuramoto_local_sim.py → state/sim.log
                     # runs N=8, T=1000, dt=0.01 sweep over K, F-HW-KU-1..5

# 2. adapter syntax check (no SDK installed — pure py_compile)
./build.sh adapters  # python3 -m py_compile src/kuramoto_loihi2_adapter.py
                     # python3 -m py_compile src/kuramoto_akida_adapter.py
                     #   → state/adapter_syntax.log

# 3. both
./build.sh all       # sim + adapters
```

Phase 1b (cloud-side, NOT included in this design — separate dispatch):

```bash
# Loihi 2 (Intel NRC cloud — requires nx-sdk install on cloud VM):
pip install nxsdk          # Intel-only, gated access
python3 src/kuramoto_loihi2_adapter.py --submit --n 8 --k 2.0 --steps 1000

# Akida (BrainChip MetaTF cloud — pip install akida + cnp2akida):
pip install akida
python3 src/kuramoto_akida_adapter.py --submit --n 8 --k 2.0 --steps 1000
```

## §7 honest C3

1. **Loihi 2 / Akida = cloud-only on Mac** — Intel NRC 및 BrainChip MetaTF
   는 Mac 에 SDK 가 native 동작하지 않음 (Intel: Linux-only NxSDK,
   gated educational access; Akida: pip install 가능하나 실 chip 은 별도
   USB stick or cloud). 본 cycle 의 adapter 들은 **skeleton only** — import
   시도 자체를 try/except 로 감싸 syntactic compile 만 보장.
2. **Mac sim approximation** — `kuramoto_local_sim.py` 는 numpy continuous
   Euler integration. 실제 Loihi 2 LIF compartment dynamics 와 Akida
   event-driven spike timing 은 본 sim 과 **수치적으로 다름** (LIF τ,
   threshold, refractory period 모두 무시). 본 sim 은 dynamics 의
   *수학적* 동등성만 검증 — neuromorphic exact replication 은 cloud cycle
   필요.
3. **실 spike-train 미검증** — F-HW-KU-1..5 는 numpy phase array 위에서
   만 검증. Loihi 2 graded-spike payload decode + Akida spike-rate
   readout 의 round-trip parity 는 cloud cycle 에서만 가능.
4. **N=8 default scale** — 본 cycle 은 SW source `simulate_network(8, ...)`
   와 동일 stub. Loihi 2 (1 M neuron / chip) 및 Akida (1 M neuron / NSoC)
   은 N >> 1000 까지 자연 스케일 — 본 design 은 spec 의 minimum N=8
   case 만 검증.
5. **build.sh adapter syntax check ≠ functional verify** — py_compile 은
   parse + bytecode 생성만 검증. import-time side effect 또는 cloud
   SDK API contract 위반은 catch 못함. cloud submit 이 실 검증.
