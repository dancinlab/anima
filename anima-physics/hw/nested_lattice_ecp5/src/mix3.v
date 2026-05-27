// mix3.v — nested_lattice mixing function (P8 3-level hierarchy)
//
// SW source: anima-physics/fpga/nested_lattice.hexa:138 fn mix3(x,a,b)
//   y = (x + a + 2*b + 1) mod 8
//   if (y >= 4) return (y - 3) mod 8
//   else        return y
//
// Bit-identical to SW. Pure combinational, no state.
// Same shape as strange_loop_ice40/src/mix4.v (P5 sibling).
//
// Note: hexa source uses the name `mix3` to distinguish from P5's `mix4`
// (despite identical arity/semantics) — kept here for SW↔RTL mapping clarity.

`default_nettype none

module mix3 (
    input  wire [2:0] x,
    input  wire [2:0] a,
    input  wire [2:0] b,
    output wire [2:0] y
);

    // 5-bit intermediate sum (max 7+7+14+1 = 29 fits 5b)
    wire [4:0] sum   = {2'b0, x} + {2'b0, a} + ({1'b0, b, 1'b0}) + 5'd1;
    wire [2:0] mod8  = sum[2:0];

    // fold: if (y >= 4) return (y - 3) mod 8 else y
    wire [2:0] folded = (mod8 - 3'd3) & 3'b111;
    assign y = mod8[2] ? folded : mod8;

endmodule
