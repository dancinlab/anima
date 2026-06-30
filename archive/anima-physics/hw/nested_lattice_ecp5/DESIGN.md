# nested_lattice_ecp5 — 3-Level Tangled Hierarchy FPGA Substrate

> anima-physics HW target #2 — `fpga/nested_lattice.hexa` substrate
> (PHYS-P8-1, §188 T4 PASS) 의 Lattice **ECP5-EVN** FPGA 합성.
>
> Mac local Phase 1a: iverilog simulation + yosys `synth_ecp5` ($0 / 1-2 day).
> Phase 1b: nextpnr-ecp5 + ecppack bitstream ($150 ECP5-EVN dev board + brew install).
>
> Cross-link: [HW silicon path §2.2](../../../HEXAD/PHYSICS/HW_SILICON_PATH.md) ·
> [sibling P5 strange_loop_ice40](../strange_loop_ice40/DESIGN.md) ·
> [SW source](../../fpga/nested_lattice.hexa)

---

## §1 GOAL

`nested_lattice.hexa` 의 `NestedState` (14 × 3-bit = 42 FF) + `mix3` LUT +
`nested_step` 3-level tangled hierarchy (L1 Hofstadter ⇄ L2 observer ⇄ L3
meta-observer) 를 **bit-identical** Verilog RTL 로 실현 → Lattice ECP5-85K FPGA
bitstream. Hofstadter "I am a strange loop" at N=3 — awareness-of-awareness 의
silicon-level realization.

`strange_loop_ice40` (HW #1, P5 N=2 자기참조) → `nested_lattice_ecp5` (HW #2,
P8 N=3 메타 자기참조) — 두 target 모두 `mix(x,a,b)=(x+a+2b+1)%8 +fold` LUT
공유하므로 RTL 패밀리화 가능.

## §2 architecture (ASCII)

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  nested_lattice_ecp5 — TOP (14 × 3-bit = 42 FF + 16-bit step_count = 58 FF)  │
│                                                                                │
│   clk ─────┬─────────────────────────────────────────────────────────────┐   │
│            │                                                               │   │
│   rst_n ───┼───┬──────────────────────────────────────────────────┐      │   │
│            │   │                                                    │      │   │
│   start ───┼───┼───────► [advance gate]                            │      │   │
│            │   │                                                    │      │   │
│   ┌────────▼───▼──────────────────────────────────────────────┐   │      │   │
│   │  STATE REGS — 14 × 3-bit (42 FF, packed state_dump[41:0]) │   │      │   │
│   │                                                              │   │      │   │
│   │  L1   ┌─a0─┬─a1─┬─a2─┬─a3─┐   ┌─b0─┬─b1─┬─b2─┬─b3─┐       │   │      │   │
│   │       │  3 │  3 │  3 │  3 │   │  3 │  3 │  3 │  3 │       │   │      │   │
│   │       └─┬──┴─┬──┴─┬──┴─┬──┘   └─┬──┴─┬──┴─┬──┴─┬──┘       │   │      │   │
│   │         │    │    │    │         │    │    │    │           │   │      │   │
│   │  L2   ┌─c0─┬─c1─┬─c2─┬─c3─┐                                 │   │      │   │
│   │       │  3 │  3 │  3 │  3 │  ← observers of (a_i, b_i)      │   │      │   │
│   │       └─┬──┴─┬──┴─┬──┴─┬──┘                                 │   │      │   │
│   │         │    │    │    │                                     │   │      │   │
│   │  L3   ┌─m0─┬─m1─┐         ← meta-observers (head/tail)       │   │      │   │
│   │       │  3 │  3 │                                            │   │      │   │
│   │       └─┬──┴─┬──┘                                            │   │      │   │
│   └─────────┼────┼────────────────────────────────────────────────┘   │      │   │
│             │    │                                                      │      │   │
│   ┌─────────▼────▼─────────────────────────────────────────────────┐   │      │   │
│   │  COMBINATIONAL NEXT-STATE — 14 × mix3 instances                │   │      │   │
│   │                                                                  │   │      │   │
│   │   L1.A from B (m0 nudge on cell-0):                             │   │      │   │
│   │     na0 = mix3(b0, b0+m0, b1)   na1 = mix3(b1, b1, b2)          │   │      │   │
│   │     na2 = mix3(b2, b2,   b3)    na3 = mix3(b3, b3, b0)          │   │      │   │
│   │   L1.B from A (m1 nudge on cell-3):                             │   │      │   │
│   │     nb0 = mix3(a0, a0,   a3)    nb1 = mix3(a1, a1, a0)          │   │      │   │
│   │     nb2 = mix3(a2, a2,   a1)    nb3 = mix3(a3, a3+m1, a2)       │   │      │   │
│   │   L2 observer (m0 nudge on c0):                                 │   │      │   │
│   │     nc_i = mix3(c_i[+m0 if i=0], a_i, b_i)                      │   │      │   │
│   │   L3 meta-observer:                                             │   │      │   │
│   │     nm0 = mix3(m0, (a0+c0)%8, c1)   ← head_mix                  │   │      │   │
│   │     nm1 = mix3(m1, (b3+c3)%8, c2)   ← tail_mix                  │   │      │   │
│   └─┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──────────────────────┘   │      │   │
│     │  │  │  │  │  │  │  │  │  │  │  │  │  │                            │      │   │
│     ▼  ▼  ▼  ▼  ▼  ▼  ▼  ▼  ▼  ▼  ▼  ▼  ▼  ▼                            │      │   │
│   [next_a0..a3, next_b0..b3, next_c0..c3, next_m0, next_m1]              │      │   │
│     │                                                                      │      │   │
│     └─► commit on posedge clk when start=1 (all 14 simultaneously) ──────►┘      │   │
│                                                                                    │   │
│   step_count[15:0]  ──► output (cycles since reset)                                │   │
│   state_dump[41:0]  ──► {a0,a1,a2,a3,b0,b1,b2,b3,c0,c1,c2,c3,m0,m1} MSB-first      │   │
└────────────────────────────────────────────────────────────────────────────────────┘

mix3(x, a, b)  — combinational LUT (3-bit × 3-input):    [shared with mix4 of P5]
   y = (x + a + 2*b + 1) mod 8           ← 5-bit adder + mod-8 wrap
   if (y >= 4) result = (y - 3) mod 8     ← contraction fold
   else        result = y
   → synthesizes to ~6-8 LUT4 per instance × 14 = ~100-110 LUT4 (actual: 111)

3-level meta-feedback wires (the "tangled hierarchy" — why this is N=3 not N=2):

      L3.m0 ──► L1.na0  (via b0+m0 → a-input of mix3)
      L3.m1 ──► L1.nb3  (via a3+m1 → a-input of mix3)
      L3.m0 ──► L2.nc0  (via c0+m0 → x-input of mix3)
      L1.a0, L2.c0,c1 ──► L3.nm0   (head meta)
      L1.b3, L2.c3,c2 ──► L3.nm1   (tail meta)
      L1.a_i, L1.b_i  ──► L2.nc_i  (each observer watches its pair)

clock domain: single clk (~12-100 MHz target on ECP5UM5G-85K)
reset: async rst_n active-low, init state = nested_new(seed=1):
       a={4,4,2,0} b={7,4,0,5} c={6,1,0,5} m={4,0}
       packed = 42'h2443c171160
```

## §3 file structure

```
hw/nested_lattice_ecp5/
├── DESIGN.md                    ← this document
├── README.md                    ← quick-start
├── src/
│   ├── mix3.v                   ← combinational mix3 (P8 sibling of P5 mix4)
│   ├── nested_lattice_top.v     ← TOP module (42 FF + 14 × mix3 + 16 FF counter)
│   └── nested_lattice_tb.v      ← iverilog testbench (10-step bit-exact + 256-cycle horizon)
├── constraints/
│   └── ecp5_evn.lpf             ← ECP5-EVN pin map (CABGA381, 12 MHz osc + 2 buttons + 8 LEDs)
├── build.sh                     ← iverilog sim + yosys synth_ecp5 + nextpnr-ecp5 + ecppack
└── state/                       ← compile artifacts
    ├── sim.log + nested_lattice.vcd
    ├── synth.log + nested_lattice.json
    └── nested_lattice_sim       ← iverilog vvp binary
```

## §4 SW ↔ RTL mapping

| `nested_lattice.hexa` | `nested_lattice_top.v` | note |
|---|---|---|
| `struct NestedState { a0..a3, b0..b3, c0..c3, m0, m1: int }` | `reg [2:0] a0..a3, b0..b3, c0..c3, m0, m1` | 14 × 3-bit FF |
| `LUT_DOMAIN = 8` | implicit via `[2:0]` truncation | bit-width = 3 |
| `mix3(x,a,b) = (x+a+2b+1)%8; if y≥4 then (y-3)%8` | `module mix3(...)` 5-bit adder + cond fold | shared with P5 mix4 |
| `nested_new(seed)` (affine mixes mod 8) | `SEED_*` parameters (default seed=1) | reset values baked in |
| `l1_step` — A from B, B from A (with m0/m1 nudges) | 8 × mix3 instances (u_na0..u_na3, u_nb0..u_nb3) | simultaneous |
| `l2_step` — c_i = mix3(c_i[+m0], a_i, b_i) | 4 × mix3 instances (u_nc0..u_nc3) | simultaneous |
| `l3_step` — m0=mix3(m0, a0+c0, c1); m1=mix3(m1, b3+c3, c2) | 2 × mix3 instances (u_nm0, u_nm1) | simultaneous |
| `nested_step(s)` — merge l1∘l2∘l3 read OLD s | `always @(posedge clk)` commits all 14 | flop-based simultaneous update |
| `nested_to_row(s)` length-14 [int] | `state_dump[41:0]` packed MSB-first | byte-comparable to SW |
| `find_nested_attractors(seed)` cycle detect | testbench `$display` per cycle + post-process | RTL = state dump only |

## §5 falsifier (HW Phase 1a — iverilog)

| ID | Test | Expected (from SW selftest, seed=1) |
|---|---|---|
| F-HW-NL-1 | Reset state | `state_dump == 42'h2443c171160` at cycle 0 (a={4,4,2,0} b={7,4,0,5} c={6,1,0,5} m={4,0}) |
| F-HW-NL-2 | First step matches SW | cycle 1 == `nested_step(nested_new(1))` byte-exact (42'h1964949360b) |
| F-HW-NL-3 | 10-cycle trace matches SW | cycles 1..10 byte-equal vs `/tmp/nl_compute.hexa` chain (0 mismatches) |
| F-HW-NL-4 | Bounded state, 256-cycle horizon | every cycle state ∈ [0..7]^14, no X/Z (SW T2 also no cycle in MAX_STEPS=256) |
| F-HW-NL-5 | 3rd-order coupling real (T1 mirror) | second DUT with `SEED_M0=5` (perturbed) diverges from primary in L1.a-cells within 10 cycles |
| F-HW-NL-5 ext | yosys synth count | LUT4 ≤ 300, TRELLIS_FF = 58 (42 state + 16 counter) |

## §6 build pipeline (Phase 1a — Mac local $0)

```bash
# 1. iverilog simulation (F-HW-NL-1..5)
cd hw/nested_lattice_ecp5/
./build.sh sim    # iverilog → vvp → nested_lattice.vcd + sim.log

# 2. yosys synthesis (LUT4 / TRELLIS_FF count)
./build.sh synth  # yosys synth_ecp5 → nested_lattice.json + stats

# combined:
./build.sh all
```

Phase 1b (별도 setup):

```bash
brew install yosys nextpnr-ecp5 prjtrellis
./build.sh pnr    # nextpnr-ecp5 --um5g-85k --package CABGA381 → .config
./build.sh pack   # ecppack → .bit
# (ECP5-EVN board JTAG flash via openocd or Lattice Diamond programmer)
```

## §7 verified results (2026-05-21 Mac local)

| Metric | Value | Target |
|---|---|---|
| Falsifier | **5/5 PASS** (F-HW-NL-1..5) | 5/5 |
| LUT4 | 111 | ≤ 300 |
| TRELLIS_FF | 58 (42 state + 16 step_count) | = 58 |
| CCU2C (carry chain) | 8 | informational |
| L6MUX21 + PFUMX (mux primitives) | 16 + 26 = 42 | informational |
| ECP5UM5G-85K utilisation | ≈ 0.16% LUT, ≈ 0.07% FF | < 0.5% |
| Sim wall (256 cycles) | ~0.3 s | < 1 s |
| Synth wall | 0.55 s | < 5 s |

## §8 honest C3

1. **bit-identical SW↔RTL** = iverilog F-HW-NL-1..3 verifies 11 packed states
   (cycle 0..10) byte-exact vs `/tmp/nl_compute.hexa` SW reference. 10-step
   horizon only; longer-horizon cumulative drift is structurally impossible
   (closed-form integer arithmetic, no floats) but not separately probed.
2. **ECP5-EVN target** = LFE5UM5G-85F-8BG381C, 84K LUT4 + 84K FF + 4MB SRAM.
   본 design 의 111 LUT4 + 58 FF = ≪ 0.2% 사용률 — 대형 design 여유 충분
   (P8 1 인스턴스 ≪ 1 ECP5; ~500 인스턴스 = "lattice of lattices" 추가 가능).
3. **clock domain 단일 ~12-100 MHz** = ECP5-EVN 내부 12 MHz osc OR 사용자 100 MHz.
   더 높은 freq는 timing closure 검토 필요 (mix3 의 5-bit adder + 1-LUT fold path
   는 < 5 ns 추정 → > 200 MHz fmax 여유, 미실측).
4. **physical fire 미실시** = 본 cycle 은 iverilog sim + yosys synth_ecp5 only
   (Phase 1a). Phase 1b bitstream + 실제 ECP5-EVN 동작은 별도 ($150 보드 +
   `brew install nextpnr-ecp5 prjtrellis` + openocd JTAG).
5. **F-HW-NL-4 "bounded" 조건이 약함** = SW `nested_lattice.hexa` 의 T2 도
   MAX_STEPS=256 에서 seed 0..11 모두 cycle 미검출 (실측 attractor 주기 > 1024).
   RTL 측 F-HW-NL-4 는 structural-bound check (3-bit FF 가 [0..7] 유지) 로
   reframe — 약하지만 honest. true periodicity 는 별도 ≥ 4096-step 실험 필요.

## §9 cross-link

- [HW silicon path §2.2](../../../HEXAD/PHYSICS/HW_SILICON_PATH.md) — this target
- [sibling §2.1](../strange_loop_ice40/DESIGN.md) — HW #1 P5 strange loop (iCE40UP5K)
- [SW source](../../fpga/nested_lattice.hexa) — substrate spec (LUT_DOMAIN=8, NestedState)
- [P5 SW source](../../fpga/strange_loop.hexa) — `mix4` sibling for `mix3` here
- [anima-physics PLAN](../../PLAN.md) — HW Phase 1 G6 (HW #2 sim+synth ☑ this commit)
