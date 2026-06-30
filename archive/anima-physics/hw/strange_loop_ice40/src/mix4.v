// mix4.v — Hofstadter strange_loop mixing function
//
// SW source: anima-physics/fpga/strange_loop.hexa:141 fn mix4(x,a,b)
//   y = (x + a + 2*b + 1) mod 8
//   if (y >= 4) return (y - 3) mod 8
//   else        return y
//
// Bit-identical to SW. Pure combinational, no state.

`default_nettype none

module mix4 (
    input  wire [2:0] x,
    input  wire [2:0] a,
    input  wire [2:0] b,
    output wire [2:0] y
);

    // intermediate: 5-bit to avoid overflow on x+a+2b+1 (max 7+7+14+1=29 fits 5b)
    wire [4:0] sum   = {2'b0, x} + {2'b0, a} + ({1'b0, b, 1'b0}) + 5'd1;
    wire [2:0] mod8  = sum[2:0];  // mod 8 = lower 3 bits

    // fold: if (y >= 4) return (y - 3) mod 8 else y
    wire [2:0] folded = (mod8 - 3'd3) & 3'b111;
    assign y = mod8[2] ? folded : mod8;

endmodule
