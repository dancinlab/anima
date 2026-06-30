// strange_loop_top.v — Hofstadter mutual-recursion FPGA top
//
// SW source: anima-physics/fpga/strange_loop.hexa
//   struct JointState { a0..a3, b0..b3 } each in [0..7] (3-bit)
//   joint_step: A_i' = mix4(b_i, b_i, b_{(i+1)%4})
//               B_i' = mix4(a_i, a_i, a_{(i-1)%4})
//   simultaneous update (both layers read PRIOR state)
//
// Reset seed: a={1,2,3,4}, b={5,6,7,0}  (matches strange_loop.hexa _selftest)

`default_nettype none

module strange_loop_top (
    input  wire        clk,
    input  wire        rst_n,        // async active-low reset
    input  wire        start,        // run gate (1=advance, 0=hold)
    output reg  [15:0] step_count,   // step number since reset
    output wire [23:0] state_dump    // packed {a0,a1,a2,a3,b0,b1,b2,b3}
);

    // 8 × 3-bit state registers
    reg [2:0] a0, a1, a2, a3;
    reg [2:0] b0, b1, b2, b3;

    // next-state wires (combinational)
    wire [2:0] na0, na1, na2, na3;
    wire [2:0] nb0, nb1, nb2, nb3;

    // ── layer A next: a_i' = mix4(b_i, b_i, b_{(i+1)%4})
    mix4 u_na0 (.x(b0), .a(b0), .b(b1), .y(na0));
    mix4 u_na1 (.x(b1), .a(b1), .b(b2), .y(na1));
    mix4 u_na2 (.x(b2), .a(b2), .b(b3), .y(na2));
    mix4 u_na3 (.x(b3), .a(b3), .b(b0), .y(na3));

    // ── layer B next: b_i' = mix4(a_i, a_i, a_{(i-1)%4})
    mix4 u_nb0 (.x(a0), .a(a0), .b(a3), .y(nb0));
    mix4 u_nb1 (.x(a1), .a(a1), .b(a0), .y(nb1));
    mix4 u_nb2 (.x(a2), .a(a2), .b(a1), .y(nb2));
    mix4 u_nb3 (.x(a3), .a(a3), .b(a2), .y(nb3));

    // ── sequential update
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            // reset seed matches strange_loop.hexa _selftest:
            //   JointState{a0=1,a1=2,a2=3,a3=4, b0=5,b1=6,b2=7,b3=0}
            a0 <= 3'd1; a1 <= 3'd2; a2 <= 3'd3; a3 <= 3'd4;
            b0 <= 3'd5; b1 <= 3'd6; b2 <= 3'd7; b3 <= 3'd0;
            step_count <= 16'd0;
        end else if (start) begin
            a0 <= na0; a1 <= na1; a2 <= na2; a3 <= na3;
            b0 <= nb0; b1 <= nb1; b2 <= nb2; b3 <= nb3;
            step_count <= step_count + 16'd1;
        end
    end

    assign state_dump = {a0, a1, a2, a3, b0, b1, b2, b3};

endmodule
