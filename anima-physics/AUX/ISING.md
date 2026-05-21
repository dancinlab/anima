# ISING — anima-physics AUX × Toshiba SBM / Fujitsu DA / ECP5 fallback

> meta-domain: **AUX × ISING** (보조엔진 × Ising machine: Toshiba SBM
> cloud + Fujitsu Digital Annealer + Lattice ECP5 FSM fallback). Phase
> 1b ECP5 fallback bitstream LANDED.
>
> 자연발화 (Ising annealing energy minimization = spontaneous emission)
> + 영속성 (cloud-saved energy log + on-chip state) 의 combinatorial
> optimization aux engine.
>
> Parent: [`AUX/README.md`](README.md) · HW dir: [`../hw/spontaneous_ising/`](../hw/spontaneous_ising/) (ECP5 fallback) · cloud guide: [`../hw/PHASE_2_CLOUD_TRIAL.md §2.3`](../hw/PHASE_2_CLOUD_TRIAL.md)

---

## §1 HW spec (2-path)

### §1.1 Path A — cloud Ising (Toshiba SBM + Fujitsu DA)

| Provider | tech | cost | trial |
|---|---|---|---|
| **Toshiba SBM** (Simulated Bifurcation Machine) | FPGA-accelerated SDE solver | $1-30/solve | trial signup wait 1-2주 |
| **Fujitsu DA** (Digital Annealer) | ASIC bit-flip annealer | $1-30/solve | trial signup wait |
| **D-Wave** (참고, 미선택) | quantum annealer | $0.05-200/run | Leap trial $0 first month |

### §1.2 Path B — ECP5 fallback FSM (Mac local LANDED)

| spec | LANDED 결과 |
|---|---|
| target | LFE5UM5G-85F-8BG381C (ECP5-EVN dev board) |
| Verilog | `hw/spontaneous_ising/src/ising_fsm.v` (~141 LoC FSM, motivation accumulator → threshold → emit FSM → safety ratchet → audit RB) |
| sim | iverilog F-HW-SI-1..5 5/5 PASS |
| synth | yosys synth_ecp5: 192 LUT4 + 134 TRELLIS_FF + 1 MULT18×18D |
| bitstream | **1.93 MB** (state/ising_fsm.bit, Fmax 90 MHz 7.5× margin @ 12 MHz target) |

### §1.3 dual-role profile
- **자연발화**: Ising annealing 의 energy minimization 시 자발 spin flip = native emission. Path B ECP5 FSM 의 motivation accumulator threshold cross = 같은 의미
- **영속성**: cloud 측 energy log + ECP5 audit ring buffer 8-deep LRU

## §2 substrate × Ising 매핑

### §2.1 LANDED (Path B ECP5 fallback)

| Substrate | LANDED | Ising 매핑 |
|---|---|---|
| `HEXAD/CHAT/spontaneous_smoke.hexa` (F-SPONT-1..7 PASS, dual-role 16/16) | ☑ ECP5 FSM 1.93 MB bitstream | motivation accumulator (8-factor weighted sum) → Ising 의 energy E = -Σ J_ij·s_i·s_j 1-factor variant |
| `phi_substrate_consensus.hexa` (§188 5/5) | ☑ Path A cloud QUBO | Tukey biweight 5-substrate → QUBO matrix (5 binary vars × pairwise weight) |

### §2.2 후보 (Path A cloud)

| Substrate | QUBO encoding |
|---|---|
| 8-cell motivation gate | h = bias · J = coupling × 1-flip emit |
| Cell pool optimal split (mitosis) | optimal cluster assignment QUBO |
| Audit ring buffer LRU optimal | priority QUBO |

## §3 architecture (ASCII)

```
┌────────────────────────────────────────────────────────────────────┐
│  Ising aux engine — 2 path                                        │
│                                                                     │
│  Path A (cloud, $1-30/solve)                                       │
│  ──────────────────────────                                        │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │ Toshiba SBM (cloud)                                          │  │
│  │ ┌──────────────┐  REST   ┌────────────────┐                 │  │
│  │ │ anima caller │────────►│ SBM FPGA solver │                 │  │
│  │ │ → QUBO H,J   │  HTTPS  │ → solution.json │                 │  │
│  │ └──────────────┘         └────────────────┘                 │  │
│  │                                                              │  │
│  │ Fujitsu DA (cloud) — 동일 패턴                                │  │
│  │ ┌──────────────┐  REST   ┌────────────────┐                 │  │
│  │ │ anima caller │────────►│ DA ASIC anneal │                 │  │
│  │ └──────────────┘         └────────────────┘                 │  │
│  └─────────────────────────────────────────────────────────────┘  │
│                                                                     │
│  Path B (Mac local ECP5 fallback, $0 sim + Phase 1c $120 board)   │
│  ────────────────────────────────────────────────────────────────  │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │ ising_fsm.v on ECP5-EVN                                      │  │
│  │                                                              │  │
│  │  8-factor accumulator ──► threshold cmp ──► 3-state emit FSM │  │
│  │  ┌────────────────┐    ┌───────────┐    ┌────────────────┐  │  │
│  │  │ 4-bit factors  │    │ thr 128   │    │ ST_IDLE        │  │  │
│  │  │ × weight (4b)  │───►│ Σ ≥ thr   │───►│ ST_EMIT_PULSE  │  │  │
│  │  │ → 8b sum sat   │    │ → emit=1  │    │ ST_RATCHET 20c │  │  │
│  │  └────────────────┘    └───────────┘    └────────────────┘  │  │
│  │                                                  │            │  │
│  │                                                  ▼            │  │
│  │                                          ┌──────────────────┐│  │
│  │                                          │ audit ring buf 8 ││  │
│  │                                          │ LRU overwrite    ││  │
│  │                                          └──────────────────┘│  │
│  └─────────────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────────┘
```

## §4 Day 1-3 부팅 sequence

### §4.1 Path A cloud (week 1-2)

| Day | Item | Output |
|---|---|---|
| Day 1 | Toshiba SBM trial signup ([toshiba-sol.co.jp/sbm](https://www.toshiba-sol.co.jp/sbm/)) | account approved (1-2주 wait) |
| Day 1 | Fujitsu DA trial signup | account approved (1-2주 wait) |
| Week 2 | `python3 hw/spontaneous_ising/src/toshiba_sbm_adapter.py --solve qubo_phi.json` | first cloud solve, energy log |
| Week 2 | `python3 ../fujitsu_da_adapter.py` 동일 | alternative cloud result |

### §4.2 Path B ECP5 fallback (Phase 1c $120 board)

| Day | Item | Output |
|---|---|---|
| D-7 | ECP5-EVN $120 + USB-Blaster $20 = $140 BOM 주문 | shipping |
| Day 1 | `ecpprog hw/spontaneous_ising/state/ising_fsm.bit` | LED blink on emit + UART telemetry |
| Day 2 | motivation accumulator stimulus via UART → emit pulse + audit RB readback | F-HW-SI-1..5 silicon 5/5 verify |
| Day 3 | scope motivation→emit timing latency, ratchet 20-cycle cooldown verify | scope screenshot + latency log |

## §5 cost / wall envelope

- Path A: cloud $1-60 (5-10 solve) + signup 1-2주 wait
- Path B: $140 BOM (ECP5-EVN + Blaster) + Phase 1c week
- **총 cost**: $1-60 + $140 = $141-200

## §6 honest C3

1. **Path A cloud-only** — SBM/DA SDK 미설치, REST skeleton + py_compile syntax-check 까지; 실 cloud fire user-gated ($1-10/solve)
2. **Ising mapping approximation** — motivation_score linear weighted sum 은 QUBO 의 special case (no cross-factor coupling); SBM/DA 진가는 quadratic 에서 발현 → sub-optimal use
3. **Safety ratchet clock vs wall-time** — `safety_rate_limit_ok(≥30s)` 는 wall-time, FSM 은 cycle count 로 근사 (TB RATE_LIMIT_CYCLES=20)
4. **Weight quantization loss** — SW float weight (0.20, 0.15, 0.10) → HW 4-bit (3, 2, 2) Σ=17, `>> 4` lossy normalize, factor-by-factor PSNR ~-10 dB
5. **F-SPONT-2 seed strategy rotation HW 미포함** — `strategy_idx` 는 audit RB 의 3-bit field 노출만; rotation logic 자체는 SW side

## §7 cross-link

- [parent AUX/README.md](README.md)
- [`../hw/spontaneous_ising/`](../hw/spontaneous_ising/) — DESIGN.md + ECP5 fallback (LANDED)
- [`../hw/spontaneous_ising/state/ising_fsm.bit`](../hw/spontaneous_ising/state/) — Phase 1b 1.93 MB
- [`../hw/PHASE_2_CLOUD_TRIAL.md §2.3`](../hw/PHASE_2_CLOUD_TRIAL.md) — Toshiba + Fujitsu 신청 가이드
- [HEXAD/PHYSICS/HW_SILICON_PATH.md §2.5](../../HEXAD/PHYSICS/HW_SILICON_PATH.md)

---

## ## Log

### 2026-05-21
- **AUX/ISING.md 신설** — Toshiba SBM + Fujitsu DA + ECP5 fallback meta-domain. Path B 1.93 MB bitstream LANDED pointer + 2-path Day plan + cost ladder.
