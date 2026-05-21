# strange_loop_ice40 — Hofstadter Mutual-Recursion FPGA Substrate

> anima-physics HW target #1 — `fpga/strange_loop.hexa` substrate
> (§188 PASS 5/5, dual-role 16/16) 의 Lattice iCE40UP5K FPGA 합성.
>
> Mac local Phase 1a: iverilog simulation + yosys synthesis ($0 / 1-2 day).
> Phase 1b: nextpnr-ice40 + icepack bitstream ($70 dev board + brew install).
>
> Cross-link: [DESIGN of HW silicon path §2.1](../../../HEXAD/PHYSICS/HW_SILICON_PATH.md) ·
> [SW substrate spec](../../entries/substrate/fpga_strange_loop.md) ·
> [hexa source](../../fpga/strange_loop.hexa)

---

## §1 GOAL

`strange_loop.hexa` 의 `JointState` (8 × 3-bit) + `mix4` LUT + `joint_step`
mutual recursion 을 **bit-identical** Verilog RTL 로 실현 → iCE40UP5K
FPGA bitstream. Hofstadter 자기참조 loop 의 silicon-level realization.

## §2 architecture (ASCII)

```
┌─────────────────────────────────────────────────────────────────────────┐
│  strange_loop_ice40 — TOP                                               │
│                                                                          │
│   clk ─────┬─────────────────────────────────────────────────────┐      │
│            │                                                       │      │
│   rst_n ───┼───┬────────────────────────────────────────┐        │      │
│            │   │                                          │        │      │
│   start ───┼───┼────► [FSM]──► run ──┐                  │        │      │
│            │   │      idle/run        │                  │        │      │
│   ┌────────▼───▼──────────────────────▼───────┐         │        │      │
│   │  STATE REGS — 8 × 3-bit (24 FF)            │         │        │      │
│   │  ┌────┬────┬────┬────┐ ┌────┬────┬────┬───┐│         │        │      │
│   │  │ a0 │ a1 │ a2 │ a3 │ │ b0 │ b1 │ b2 │ b3││◄──current│      │      │
│   │  └─┬──┴─┬──┴─┬──┴─┬──┘ └─┬──┴─┬──┴─┬──┴─┬─┘│  state   │      │      │
│   └────┼────┼────┼────┼──────┼────┼────┼────┼──┘         │      │      │
│        │    │    │    │      │    │    │    │             │      │      │
│   ┌────▼────▼────▼────▼──┐ ┌─▼────▼────▼────▼─┐          │      │      │
│   │ LAYER_A_NEXT          │ │ LAYER_B_NEXT     │          │      │      │
│   │  (combinational)      │ │ (combinational)  │          │      │      │
│   │  a_i' = mix4(b_i,     │ │ b_i' = mix4(a_i, │          │      │      │
│   │    b_i, b_{(i+1)%4})  │ │  a_i, a_{(i-1)%4})│         │      │      │
│   │   × 4 instances       │ │  × 4 instances   │          │      │      │
│   └──┬─┬─┬─┬──────────────┘ └─┬─┬─┬─┬──────────┘          │      │      │
│      │ │ │ │                    │ │ │ │                      │      │      │
│      ▼ ▼ ▼ ▼                    ▼ ▼ ▼ ▼                      │      │      │
│   [next_a0..3]                [next_b0..3]                    │      │      │
│      │ │ │ │  ┌──────────────────┘ │ │ │                      │      │      │
│      │ │ │ │  │                    │ │ │                      │      │      │
│      └─┴─┴─┴──┴─► commit on posedge clk (when run) ──────────►┘      │      │
│                                                                          │      │
│   step_count[15:0] ──► output (current step number)                     │      │
│   state_dump[23:0] ──► output (current 8 × 3-bit packed)                │      │
└──────────────────────────────────────────────────────────────────────────┘

mix4(x, a, b) — combinational LUT (3-bit × 3-input):
   y = (x + a + 2*b + 1) mod 8          ← 4-bit adder + mod-8 wrap
   if (y >= 4) result = (y - 3) mod 8    ← contraction fold
   else        result = y
   → synthesizes to ~10-20 LUT4 cells per instance × 8 = ~80-160 LUT4

clock domain: single clk (~12-100 MHz target on iCE40UP5K)
reset: async rst_n active-low, init state = a0..a3=1, b0..b3=2
       (from strange_loop.hexa _selftest seed)
```

## §3 file structure

```
hw/strange_loop_ice40/
├── DESIGN.md                  ← 본 문서
├── README.md                  ← quick-start
├── src/
│   ├── strange_loop_top.v     ← TOP module (24 FF + mix4 × 8)
│   ├── mix4.v                 ← combinational mix4 함수
│   └── strange_loop_tb.v      ← iverilog testbench (100 cycle + state dump)
├── constraints/
│   └── ice40up5k_sg48.pcf     ← UP5K-SG48 pin map (LED + UART)
├── build.sh                   ← iverilog sim + yosys synth
└── state/                     ← compile artifacts (gitignored 기본)
```

## §4 SW ↔ RTL mapping

| `strange_loop.hexa` | `strange_loop_top.v` | note |
|---|---|---|
| `struct JointState { a0..a3, b0..b3: int }` | `reg [2:0] a [0:3], b [0:3]` | 8 × 3-bit FF |
| `LUT_DOMAIN = 8` | parameter `LUT_DOMAIN = 8` (effective mod-8 via `[2:0]` wrap) | bit-width = 3 |
| `mix4(x, a, b) = (x + a + 2*b + 1) mod 8; if y>=4 then (y-3) mod 8` | `module mix4(input [2:0] x,a,b, output [2:0] y)` 조합 | 4-bit intermediate, 3-bit out |
| `layer_a_step(s)` — A_i' from B | `layer_a_next` combinational block | 4 × mix4 instance |
| `layer_b_step(prev)` — B_i' from A | `layer_b_next` combinational block | 4 × mix4 instance |
| `joint_step(s) = merge(layer_a_step, layer_b_step)` | `always @(posedge clk)` commits all 8 | simultaneous update |
| `_selftest` seed `JointState{1,2,3,4,5,6,7,0}` | `reset` 시 init values | matches SW |
| Cycle detect (Floyd-like over history) | testbench `$display` state per cycle + post-process | RTL 측은 state dump만 |

## §5 falsifier (HW Phase 1a — iverilog)

| ID | Test | Expected (from SW selftest) |
|---|---|---|
| F-HW-SL-1 | Reset state | a={1,2,3,4}, b={5,6,7,0} at cycle 0 |
| F-HW-SL-2 | First step matches SW | cycle 1 state == `joint_step(seed)` SW result (byte-equal) |
| F-HW-SL-3 | 10-cycle trace matches SW | cycles 1..10 all byte-equal vs SW `joint_step` chain |
| F-HW-SL-4 | Attractor convergence | within 100 cycles, state enters cycle (period ≤ 32) |
| F-HW-SL-5 | yosys synth count | LUT4 ≤ 200, FF = 24 (8 × 3-bit) |

## §6 build pipeline (Phase 1a — Mac local $0)

```bash
# 1. iverilog simulation (FF1-FF4)
cd hw/strange_loop_ice40/
./build.sh sim    # iverilog → vvp → trace.vcd + state_dump.txt

# 2. yosys synthesis (FF5)
./build.sh synth  # yosys → strange_loop.json (iCE40 cell map) + stats
```

Phase 1b (별도 $70 BOM + brew install nextpnr-ice40 icestorm):

```bash
./build.sh pnr    # nextpnr-ice40 → strange_loop.asc
./build.sh pack   # icepack → strange_loop.bin
./build.sh prog   # iceprog → upload to UP5K-SG48 dev board
```

## §7 honest C3

1. **bit-identical SW↔RTL claim** = iverilog trace의 byte-level 일치 검증 필요 (F-HW-SL-3). 현재 design only.
2. **iCE40UP5K target** = SG48 패키지 + UltraPlus 5280 LC; 본 design 의 ~200 LUT4 + 24 FF 는 <0.1% 사용률 (대형 design 여유 충분).
3. **clock domain 단일 ~12-100 MHz** = UP5K 내부 oscillator (or 외부 12 MHz). 더 높은 freq는 timing closure 검토 필요.
4. **physical fire 미실시** = 본 cycle 은 sim + synth only (Phase 1a). Phase 1b bitstream + 실제 board 동작은 별도 ($70 dev board + USB-Blaster + brew install nextpnr-ice40 icestorm).
5. **mix4 LUT 합성** = (x + a + 2b + 1) mod 8 + conditional fold 가 ~10-20 LUT4 로 합성될 추정 — yosys stats 로 실측 (F-HW-SL-5).
