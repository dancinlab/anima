// nested_lattice_top.v — 3-level tangled hierarchy FPGA top
//
// SW source: anima-physics/fpga/nested_lattice.hexa
//   struct NestedState { a0..a3, b0..b3, c0..c3, m0, m1 } each 3-bit (0..7)
//   nested_step performs simultaneous update across L1, L2, L3 (all use OLD s):
//
//   L1 — Hofstadter strange loop with L3 meta modulation
//     na0 = mix3(b0, b0 + m0, b1)        ← m0 feedback nudge on cell 0
//     na1 = mix3(b1, b1,      b2)
//     na2 = mix3(b2, b2,      b3)
//     na3 = mix3(b3, b3,      b0)
//     nb0 = mix3(a0, a0,      a3)
//     nb1 = mix3(a1, a1,      a0)
//     nb2 = mix3(a2, a2,      a1)
//     nb3 = mix3(a3, a3 + m1, a2)        ← m1 feedback nudge on cell 3
//
//   L2 — observer of L1, with L3 feedback on c0
//     nc0 = mix3(c0 + m0, a0, b0)        ← m0 feedback on c0
//     nc1 = mix3(c1,      a1, b1)
//     nc2 = mix3(c2,      a2, b2)
//     nc3 = mix3(c3,      a3, b3)
//
//   L3 — meta-observer, watches L1+L2 jointly
//     nm0 = mix3(m0, (a0 + c0) mod 8, c1)  ← head meta
//     nm1 = mix3(m1, (b3 + c3) mod 8, c2)  ← tail meta
//
// Reset seed (SEED parameter, default 1) uses nested_new(seed) formula:
//   ai  = (seed*3+1, *5+7, *7+11, *11+13) mod 8
//   bi  = (seed*13+2, *17+3, *19+5, *23+6) mod 8
//   ci  = (seed*29+1, *31+2, *37+3, *41+4) mod 8
//   m0  = (seed*43+1) mod 8
//   m1  = (seed*47+1) mod 8
//
// Layout: 14 × 3-bit state = 42 FF + 16-bit step_count = 58 FF total
// state_dump packing (MSB→LSB):
//   [41:39] a0 [38:36] a1 [35:33] a2 [32:30] a3
//   [29:27] b0 [26:24] b1 [23:21] b2 [20:18] b3
//   [17:15] c0 [14:12] c1 [11:09] c2 [08:06] c3
//   [05:03] m0 [02:00] m1

`default_nettype none

module nested_lattice_top #(
    parameter [2:0] SEED_A0 = 3'd4,    // seed=1 defaults (see nested_new(1))
    parameter [2:0] SEED_A1 = 3'd4,
    parameter [2:0] SEED_A2 = 3'd2,
    parameter [2:0] SEED_A3 = 3'd0,
    parameter [2:0] SEED_B0 = 3'd7,
    parameter [2:0] SEED_B1 = 3'd4,
    parameter [2:0] SEED_B2 = 3'd0,
    parameter [2:0] SEED_B3 = 3'd5,
    parameter [2:0] SEED_C0 = 3'd6,
    parameter [2:0] SEED_C1 = 3'd1,
    parameter [2:0] SEED_C2 = 3'd0,
    parameter [2:0] SEED_C3 = 3'd5,
    parameter [2:0] SEED_M0 = 3'd4,
    parameter [2:0] SEED_M1 = 3'd0
) (
    input  wire        clk,
    input  wire        rst_n,        // async active-low
    input  wire        start,        // run gate (1=advance, 0=hold)
    output reg  [15:0] step_count,   // step number since reset
    output wire [41:0] state_dump    // packed 14 × 3-bit
);

    // ── 14 × 3-bit state registers
    reg [2:0] a0, a1, a2, a3;
    reg [2:0] b0, b1, b2, b3;
    reg [2:0] c0, c1, c2, c3;
    reg [2:0] m0, m1;

    // ── next-state wires (combinational)
    wire [2:0] na0, na1, na2, na3;
    wire [2:0] nb0, nb1, nb2, nb3;
    wire [2:0] nc0, nc1, nc2, nc3;
    wire [2:0] nm0, nm1;

    // Pre-adders for L3-modulated inputs (truncated to 3 bits — mix3 wraps mod 8 internally).
    // hexa: mix3(x, a, b) computes (x + a + 2b + 1) mod 8; truncating a-input to 3 bits
    // before the call is bit-identical because addition then mod-8 is the same as
    // mod-8-then-addition-then-mod-8.
    wire [2:0] b0_plus_m0 = b0 + m0;    // for na0
    wire [2:0] a3_plus_m1 = a3 + m1;    // for nb3
    wire [2:0] c0_plus_m0 = c0 + m0;    // for nc0
    wire [2:0] a0_plus_c0 = a0 + c0;    // L3 head_mix (passed as b-input to mix3)
    wire [2:0] b3_plus_c3 = b3 + c3;    // L3 tail_mix

    // ── L1 — A from B (with m0 nudge on cell 0)
    mix3 u_na0 (.x(b0), .a(b0_plus_m0), .b(b1), .y(na0));
    mix3 u_na1 (.x(b1), .a(b1),         .b(b2), .y(na1));
    mix3 u_na2 (.x(b2), .a(b2),         .b(b3), .y(na2));
    mix3 u_na3 (.x(b3), .a(b3),         .b(b0), .y(na3));

    // ── L1 — B from A (with m1 nudge on cell 3)
    mix3 u_nb0 (.x(a0), .a(a0),         .b(a3), .y(nb0));
    mix3 u_nb1 (.x(a1), .a(a1),         .b(a0), .y(nb1));
    mix3 u_nb2 (.x(a2), .a(a2),         .b(a1), .y(nb2));
    mix3 u_nb3 (.x(a3), .a(a3_plus_m1), .b(a2), .y(nb3));

    // ── L2 — observer, c_i = mix3(c_i [+ m0 on cell 0], a_i, b_i)
    mix3 u_nc0 (.x(c0_plus_m0), .a(a0), .b(b0), .y(nc0));
    mix3 u_nc1 (.x(c1),         .a(a1), .b(b1), .y(nc1));
    mix3 u_nc2 (.x(c2),         .a(a2), .b(b2), .y(nc2));
    mix3 u_nc3 (.x(c3),         .a(a3), .b(b3), .y(nc3));

    // ── L3 — meta observer
    mix3 u_nm0 (.x(m0), .a(a0_plus_c0), .b(c1), .y(nm0));
    mix3 u_nm1 (.x(m1), .a(b3_plus_c3), .b(c2), .y(nm1));

    // ── sequential commit: simultaneous update (all next-state wires sampled from OLD regs)
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            a0 <= SEED_A0; a1 <= SEED_A1; a2 <= SEED_A2; a3 <= SEED_A3;
            b0 <= SEED_B0; b1 <= SEED_B1; b2 <= SEED_B2; b3 <= SEED_B3;
            c0 <= SEED_C0; c1 <= SEED_C1; c2 <= SEED_C2; c3 <= SEED_C3;
            m0 <= SEED_M0; m1 <= SEED_M1;
            step_count <= 16'd0;
        end else if (start) begin
            a0 <= na0; a1 <= na1; a2 <= na2; a3 <= na3;
            b0 <= nb0; b1 <= nb1; b2 <= nb2; b3 <= nb3;
            c0 <= nc0; c1 <= nc1; c2 <= nc2; c3 <= nc3;
            m0 <= nm0; m1 <= nm1;
            step_count <= step_count + 16'd1;
        end
    end

    // Packed observable state — 14 × 3-bit = 42 bits, MSB-first
    assign state_dump = {a0, a1, a2, a3,
                         b0, b1, b2, b3,
                         c0, c1, c2, c3,
                         m0, m1};

endmodule
