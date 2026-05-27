# spontaneous_ising — Autonomous Emission HW Substrate (Ising cloud + ECP5 FPGA)

> anima-physics HW target #5 — `HEXAD/CHAT/spontaneous_smoke.hexa` (127 LoC,
> F-SPONT-1..7 PASS) 의 silicon-level realization.
>
> **2-path strategy** (cloud + on-prem):
> - **Path A — Ising annealing cloud** (Toshiba SBM / Fujitsu DA): motivation
>   weighted-sum gate + safety conjunction → QUBO/Ising mapping → cloud REST.
>   Mac local: Python adapter skeleton (cloud SDK 미설치, syntax-check only).
> - **Path B — ECP5 FPGA fallback** (Lattice ECP5-EVN): motivation accumulator
>   (8-bit reg) + threshold cmp + safety ratchet + audit ring buffer → Verilog
>   FSM. Mac local: iverilog sim + yosys `synth_ecp5`.
>
> Cross-link: [HW silicon path §2.5](../../../HEXAD/PHYSICS/HW_SILICON_PATH.md) ·
> [SW source spontaneous_smoke.hexa](../../../HEXAD/CHAT/spontaneous_smoke.hexa) ·
> [spontaneous_lib.hexa](../../../HEXAD/CHAT/spontaneous_lib.hexa) ·
> [anima-physics PLAN G6](../../PLAN.md) HW Phase 1 target #5

---

## §1 GOAL

`spontaneous_smoke.hexa` 의 핵심 dynamics 를 silicon 으로 실현:

1. **motivation_score**: 8 intrinsic factor (relevance / info_gap / curiosity /
   pain / coherence / originality / balance / dynamics) weighted sum
   (Σw=1.0) ∈ [0, 1]
2. **threshold gate**: `should_emit = score > 0.3 (IM)` ·
   `should_interrupt = score > 0.6`
3. **safety ratchet** (4 AND): `kill_switch ∧ rate_limit (≥30s) ∧ phi_ratchet
   (Φ > ratchet/2) ∧ content_clean`
4. **audit ring buffer**: 마지막 N (=8) emit event 의 (score, strategy_idx,
   accepted) tuple 보존

→ 2 path (cloud annealer + on-prem FPGA FSM) 으로 발화권 의사결정 hardware-
offloaded.

## §2 architecture (ASCII, 2-path 모두)

### Path A — Toshiba SBM / Fujitsu DA Ising cloud

```
┌──────────────────────────────────────────────────────────────────────────┐
│  spontaneous_ising — Path A (Ising annealing cloud)                       │
│                                                                            │
│  [8 factor sensors]  rel | gap | cur | pain | coh | orig | bal | dyn       │
│        │  │   │   │   │   │   │   │                                        │
│        ▼  ▼   ▼   ▼   ▼   ▼   ▼   ▼                                        │
│  ┌─────────────────────────────────────────────┐                          │
│  │ encode_qubo(factors, weights, threshold)    │  ← Python adapter        │
│  │                                              │     (toshiba_sbm_adapter │
│  │  Objective (minimize):                       │      fujitsu_da_adapter) │
│  │    H = - Σ_i w_i · s_i · x_i                 │                          │
│  │        + λ · (Σ_i w_i · x_i − θ)²            │                          │
│  │      x_i ∈ {0, 1}  (binary "include factor") │                          │
│  │    s_i = sgn(factor_value − 0.5)             │                          │
│  │    θ = spont_im_threshold = 0.3              │                          │
│  │    λ = safety penalty                        │                          │
│  └────────────────┬────────────────────────────┘                          │
│                   │ POST /api/v1/solve (REST)                               │
│                   ▼                                                          │
│  ┌─────────────────────────────────────────────┐                          │
│  │ Cloud annealer (Toshiba SBM, Fujitsu DA)    │                          │
│  │   SBM: Simulated Bifurcation Machine        │                          │
│  │   DA:  Digital Annealer (2-bit FM coupling) │                          │
│  │   → returns optimum spin config + energy     │                          │
│  └────────────────┬────────────────────────────┘                          │
│                   │ JSON response                                            │
│                   ▼                                                          │
│  ┌─────────────────────────────────────────────┐                          │
│  │ decode_emit_decision(spins)                  │                          │
│  │   emit  = (E_min < threshold_energy)         │                          │
│  │   audit_push(score, strategy, emit)          │                          │
│  └─────────────────────────────────────────────┘                          │
│                                                                            │
│  cost: $0 dev / ~$1-10 per solve on commercial cloud                       │
│  Mac local: syntax-check only (SDK 미설치)                                  │
└──────────────────────────────────────────────────────────────────────────┘
```

### Path B — ECP5 FPGA FSM fallback (Lattice ECP5-EVN)

```
┌──────────────────────────────────────────────────────────────────────────┐
│  spontaneous_ising — Path B (ECP5 FSM, on-prem)                            │
│                                                                            │
│   clk ─┬─────────────────────────────────────────────────────────────┐   │
│        │                                                                │   │
│   rst_n┼────────────────────────────────────────────────────────┐    │   │
│        │                                                          │    │   │
│   ┌────▼──────────────────────────────────────────────────────┐ │    │   │
│   │ INPUT REGS — 8 × 4-bit factor (Q4.0 fixed-point ∈ [0,15]) │ │    │   │
│   │   rel  gap  cur  pain  coh  orig  bal  dyn                 │ │    │   │
│   │   (8 inputs from sensor bus or AXI4-Lite)                  │ │    │   │
│   └────┬──────────────────────────────────────────────────────┘ │    │   │
│        │                                                          │    │   │
│   ┌────▼──────────────────────────────────────────────────────┐ │    │   │
│   │ MOTIVATION ACCUMULATOR — 8-bit reg (Q4.4 fixed-point)     │ │    │   │
│   │   score = Σ_i (w_i · factor_i) >> norm_shift              │ │    │   │
│   │   weights LUT (8 × 4-bit): 3,2,2,2,2,2,2,2 sum=17 ≈ Σw=1  │ │    │   │
│   └────┬──────────────────────────────────────────────────────┘ │    │   │
│        │                                                          │    │   │
│   ┌────▼──────────────────────────────────────────────────────┐ │    │   │
│   │ THRESHOLD CMP (combinational)                              │ │    │   │
│   │   gate_im     = score > IM_THRESHOLD (=0x4D ≈ 0.3)        │ │    │   │
│   │   gate_intrpt = score > INTERRUPT_THRESHOLD (=0x99 ≈ 0.6) │ │    │   │
│   └────┬──────────────────────────────────────────────────────┘ │    │   │
│        │                                                          │    │   │
│   ┌────▼──────────────────────────────────────────────────────┐ │    │   │
│   │ SAFETY RATCHET (4-input AND, combinational)                │ │    │   │
│   │   kill_sw ∧ rate_ok (cycle_since_last >= 30s_cycles)      │ │    │   │
│   │           ∧ phi_ratchet_ok ∧ content_ok                    │ │    │   │
│   └────┬──────────────────────────────────────────────────────┘ │    │   │
│        │                                                          │    │   │
│   ┌────▼──────────────────────────────────────────────────────┐ │    │   │
│   │ EMIT FSM — 3 states                                        │ │    │   │
│   │   IDLE ──(gate_im & safety)──► EMIT_PULSE (1 cycle pulse) │ │    │   │
│   │   EMIT_PULSE ──(any)──► COOLDOWN (rate-limit counter)     │ │    │   │
│   │   COOLDOWN ──(timer expire)──► IDLE                        │ │    │   │
│   └────┬──────────────────────────────────────────────────────┘ │    │   │
│        │                                                          │    │   │
│   ┌────▼──────────────────────────────────────────────────────┐ │    │   │
│   │ AUDIT RING BUFFER — 8 × 16-bit (128 FF)                    │ │    │   │
│   │   {accepted[1], strategy_idx[3], score[8], _pad[4]}        │ │    │   │
│   │   write ptr ∈ [0..7] auto-increment on each emit-eval      │ │    │   │
│   │   readout via state_dump[127:0] or AXI4-Lite               │ │    │   │
│   └────────────────────────────────────────────────────────────┘ │    │   │
│                                                                    │   │
│   emit_pulse ─────► output (1 cycle high on emit)                 │   │
│   cell_count[15:0] ──► step counter since reset                   │   │
└────────────────────────────────────────────────────────────────────┘   │
                                                                          │
   IM_THRESHOLD       = 0x4D  (8'd77,  ~0.3 in Q0.8)                      │
   INTERRUPT_THRESHOLD = 0x99 (8'd153, ~0.6 in Q0.8)                      │
   RATE_LIMIT_CYCLES   = 30 (toy, scale-to-clock for real-time)           │
   AUDIT_DEPTH         = 8                                                 │
   clock domain: single clk (~50-150 MHz target on ECP5-25F LFE5UM5G)     │
   reset: async rst_n active-low; init motivation=0, audit cleared        │
```

## §3 file structure

```
hw/spontaneous_ising/
├── DESIGN.md                       ← 본 문서
├── README.md                       ← quick-start
├── src/
│   ├── ising_fsm.v                 ← Path B ECP5 FSM TOP (~100 LoC)
│   ├── ising_fsm_tb.v              ← iverilog testbench (F-HW-SI-1..5)
│   ├── toshiba_sbm_adapter.py      ← Path A Toshiba SBM REST adapter
│   └── fujitsu_da_adapter.py       ← Path A Fujitsu DA REST adapter
├── constraints/
│   └── ecp5_evn.lpf                ← ECP5-EVN (LFE5UM5G-85F) pin map
├── build.sh                        ← iverilog sim + yosys synth_ecp5 + py syntax
└── state/                          ← compile artifacts
    ├── sim.log
    ├── synth.log
    ├── ising_fsm.json
    └── adapter_syntax.log
```

## §4 SW ↔ HW mapping

| `spontaneous_smoke.hexa` / `spontaneous_lib.hexa` | Path A (Ising) | Path B (FSM) | note |
|---|---|---|---|
| `motivation_score(rel,gap,cur,pain,coh,orig,bal,dyn)` (8 factor weighted sum) | QUBO objective coefficient `−w_i · s_i` | `score <= Σ (w_i · factor_i)` combinational adder | Σw=1.0 closed (B-SPONT-7) |
| `should_emit(score) = score > 0.3` | penalty term `λ (Σ w_i x_i − 0.3)²` | `gate_im = (score > 8'd77)` | IM threshold |
| `should_interrupt(score) = score > 0.6` | secondary threshold τ₂ | `gate_intrpt = (score > 8'd153)` | rare path |
| `safety_combined(kill, rate, phi_r, content)` 4-AND | post-decode AND on cloud response | `safety = kill_sw & rate_ok & phi_r & content_ok` | F-SPONT-5 |
| `safety_rate_limit_ok(seconds) = seconds >= 30s` | adapter-side deferred (clock not in cloud) | `rate_ok = (cooldown_cnt == 0)` | F-SPONT-7 (sim cycles → real seconds via clk freq) |
| `audit_entry_accepted(score, strategy, accepted)` | append to local log file | 16-bit packed → ring buffer [8] | F-SPONT-4 |
| `spont_seed_strategy_count = 4` | strategy_idx[1:0] = 2-bit | strategy_idx[2:0] | 3-bit reserve for future |
| Reset state (no prior emit) | accumulator=0, cooldown=0 | motivation=0, audit cleared, FSM=IDLE | matches SW |

Cost / weight mapping (Path B 8-bit accumulator):

| factor | SW weight (`spont_weight_*`) | HW weight (4-bit, Q0.4 approx, ×16) | rounded | Σ |
|---|---|---|---|---|
| relevance   | 0.20 | 3.20 | 3 | 3 |
| info_gap    | 0.10 | 1.60 | 2 | 5 |
| curiosity   | 0.15 | 2.40 | 2 | 7 |
| pain        | 0.10 | 1.60 | 2 | 9 |
| coherence   | 0.10 | 1.60 | 2 | 11 |
| originality | 0.10 | 1.60 | 2 | 13 |
| balance     | 0.15 | 2.40 | 2 | 15 |
| dynamics    | 0.10 | 1.60 | 2 | 17 |

Σ = 17 (norm divisor; >> 4 then +small correction). Σ ≈ 16 → 4-bit shift right
gives normalized score (small bias accepted as Q4.4 → Q0.8 hand-off; documented
as honest C3 #2).

## §5 falsifier (HW Phase 1a — iverilog + yosys synth_ecp5)

| ID | Test | Expected |
|---|---|---|
| F-HW-SI-1 | Motivation reset = 0 | At cycle 0 after `rst_n`, `motivation_acc == 8'h00`, `emit_pulse == 0`, audit RB cleared. |
| F-HW-SI-2 | Motivation increment per cycle (factors driven) | With all 8 factor inputs = `4'hF` (max), `motivation_acc` reaches `8'hFF` (saturated max) within `ceil(17/1)` cycles via the combinational adder snapshot (single-cycle compute, multi-cycle assert via TB). |
| F-HW-SI-3 | Threshold cross → emit pulse | Drive factor combo s.t. `motivation_acc > 8'h4D` while safety inputs all 1 → `emit_pulse == 1` for exactly 1 cycle, then FSM transitions to COOLDOWN. |
| F-HW-SI-4 | Safety ratchet limits emit rate | After an emit, cooldown counter blocks subsequent emit attempts for `RATE_LIMIT_CYCLES` (=30 in TB) even if score stays above threshold. Verify `emit_pulse` count over 100 cycle window ≤ 4. |
| F-HW-SI-5 | Audit ring buffer holds last N=8 emits | After 10 emit events, audit RB contains exactly events 3..10 (oldest 2 overwritten); read `audit_dump` and check `accepted` bit + `strategy_idx` + `score` for last entry. |

## §6 build pipeline (Phase 1a — Mac local $0)

```bash
cd hw/spontaneous_ising/
./build.sh sim       # iverilog → vvp → trace.vcd + sim.log
./build.sh synth     # yosys synth_ecp5 → ising_fsm.json + synth.log
./build.sh adapters  # python3 -m py_compile *_adapter.py → adapter_syntax.log
./build.sh all       # all of the above
```

Phase 1b (out of scope for this cycle):

- Path A: register for Toshiba SBM trial OR AWS Marketplace listing; provide
  API key via env var; run end-to-end QUBO encode → solve → decode.
- Path B: `brew install --HEAD prjtrellis nextpnr-ecp5`; `nextpnr-ecp5 --25k
  --package CABGA381 --lpf constraints/ecp5_evn.lpf --json state/ising_fsm.json
  --textcfg state/ising_fsm.cfg`; `ecppack` → bitstream; `openFPGALoader -b
  ecp5_evn state/ising_fsm.bit`. Board: Lattice ECP5-EVN (LFE5UM5G-85F) ~$200.

## §7 honest C3

1. **Path A cloud-only on Mac** — Toshiba SBM / Fujitsu DA SDK 는 사용자 등록
   + commercial license 필요 (월 $1k+). 본 cycle 은 REST API skeleton +
   `py_compile` syntax check 까지만; 실제 cloud fire 는 별도 user-gated
   ($1-10/solve, 등록 진행 필요).
2. **Ising mapping approximation** — `motivation_score` 의 linear weighted sum
   은 사실 QUBO objective 의 special case (no x_i x_j coupling). DA/SBM 의
   진가는 quadratic coupling 에서 나오므로, 본 mapping 은 sub-optimal use of
   the annealer. 향후 cross-factor synergy (예: balance × phi_ratchet quadratic
   penalty) 를 도입하면 진정한 Ising 문제로 격상 가능 — 본 cycle 은
   linear-coefficient-only skeleton 으로 design 1차 PoC.
3. **Safety ratchet 검증 (clock vs wall-time)** — `safety_rate_limit_ok(>=30s)`
   는 wall-time second 인데, FSM 에서는 cycle count 로 근사. TB 에서 30
   cycles 로 축소 (100 MHz clock 시 0.3 µs ≠ 30 s); 실제 board 에서는
   `RATE_LIMIT_CYCLES = 30 * clk_freq_hz` 로 parameterize 필요. F-HW-SI-4 는
   "monotone counter blocks emit" 만 검증, 절대 wall-time 은 deferral.
4. **Weight quantization loss** — SW 의 float weight (0.20, 0.15, 0.10) 가
   HW 의 4-bit weight (3, 2, 2) 로 매핑되며 Σ=17 (NOT 16 = 2^4), 17 ≠ unity
   power-of-2 → normalize 가 `>> 4` 로 lossy. 실측 motivation score 의
   factor-by-factor PSNR ~−10 dB 추정 (단조성은 보존). 정밀이 필요하면 16-bit
   accumulator + 8-bit weight 으로 격상 (LUT/FF cost ~2-3×).
5. **F-SPONT-2 seed strategy rotation HW 미포함** — `strategy_idx` 는 audit RB
   에 저장만 되고, "rotation 자체" 는 SW (`spont_seed_strategy_*`) side; HW 는
   외부에서 들어오는 idx 를 단순 저장 + AC. F-SPONT-6 meta-emission flag 도
   마찬가지로 audit RB 의 1-bit reserved field 로만 노출 (rendering 은 SW).

## §8 falsifier 사전등록 (re-stated for SSOT)

F-HW-SI-1 motivation_reset_zero · F-HW-SI-2 motivation_increment_per_cycle ·
F-HW-SI-3 threshold_cross_emit_pulse · F-HW-SI-4 safety_ratchet_rate_limit ·
F-HW-SI-5 audit_ring_buffer_depth_N.

verdict 채점: `state/sim.log` 의 `PASS F-HW-SI-N` line 수 카운트 = 5/5.
