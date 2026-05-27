// ising_fsm_tb.v — iverilog testbench for spontaneous_ising Path B FSM
//
// F-HW-SI-1: motivation_acc resets to 0 after rst_n; emit_pulse=0; audit cleared.
// F-HW-SI-2: With all factor inputs = 4'hF, motivation_acc saturates at expected
//             weighted-sum value within 1 cycle (combinational adder).
// F-HW-SI-3: Score crossing IM_THRESHOLD with safety inputs all 1 → emit_pulse
//             goes high for exactly 1 cycle.
// F-HW-SI-4: After an emit, cooldown blocks further emits for RATE_LIMIT_CYCLES;
//             count emits over a 100-cycle window ≤ 4.
// F-HW-SI-5: After multiple emits, audit ring buffer holds the most recent
//             AUDIT_DEPTH entries; last entry's accepted/strategy/score readable.

`default_nettype none
`timescale 1ns / 1ps

module ising_fsm_tb;

    reg clk = 0;
    reg rst_n = 0;

    reg  [3:0] f_rel, f_gap, f_cur, f_pain, f_coh, f_orig, f_bal, f_dyn;
    reg        kill_sw, phi_ratchet_ok, content_ok;
    reg  [2:0] strategy_idx;

    wire        emit_pulse;
    wire [7:0]  motivation_acc;
    wire        gate_im, gate_intrpt, safety_combined_w;
    wire [15:0] cell_count;
    wire [127:0] audit_dump;

    // Shrink rate limit for sim brevity (still tests the ratchet property)
    ising_fsm #(
        .IM_THRESHOLD       (8'd77),
        .INTERRUPT_THRESHOLD(8'd153),
        .RATE_LIMIT_CYCLES  (16'd20)
    ) dut (
        .clk(clk),
        .rst_n(rst_n),
        .f_rel(f_rel),   .f_gap(f_gap),   .f_cur(f_cur),  .f_pain(f_pain),
        .f_coh(f_coh),   .f_orig(f_orig), .f_bal(f_bal),  .f_dyn(f_dyn),
        .kill_sw(kill_sw),
        .phi_ratchet_ok(phi_ratchet_ok),
        .content_ok(content_ok),
        .strategy_idx(strategy_idx),
        .emit_pulse(emit_pulse),
        .motivation_acc(motivation_acc),
        .gate_im(gate_im),
        .gate_intrpt(gate_intrpt),
        .safety_combined_w(safety_combined_w),
        .cell_count(cell_count),
        .audit_dump(audit_dump)
    );

    // 100 MHz clock
    always #5 clk = ~clk;

    integer i;
    integer emit_count;
    reg     pass_f1, pass_f2, pass_f3, pass_f4, pass_f5;

    initial begin
        $dumpfile("state/ising_fsm.vcd");
        $dumpvars(0, ising_fsm_tb);

        // ── init inputs ────────────────────────────────────────────────
        f_rel = 0; f_gap = 0; f_cur = 0; f_pain = 0;
        f_coh = 0; f_orig = 0; f_bal = 0; f_dyn = 0;
        kill_sw = 0; phi_ratchet_ok = 0; content_ok = 0;
        strategy_idx = 3'd0;

        // ── F-HW-SI-1: reset state ─────────────────────────────────────
        #12 rst_n = 1;
        @(posedge clk);
        #1;
        $display("[F-HW-SI-1] cycle=%0d motivation=%0d emit=%b audit_dump=%h",
                 cell_count, motivation_acc, emit_pulse, audit_dump);
        pass_f1 = (motivation_acc == 8'd0) && (emit_pulse == 1'b0)
               && (audit_dump == 128'd0);
        if (pass_f1) $display("PASS F-HW-SI-1");
        else         $display("FAIL F-HW-SI-1");

        // ── F-HW-SI-2: drive all factors max → weighted sum saturates ──
        f_rel = 4'hF; f_gap = 4'hF; f_cur = 4'hF; f_pain = 4'hF;
        f_coh = 4'hF; f_orig = 4'hF; f_bal = 4'hF; f_dyn = 4'hF;
        // weighted_sum = 15 × (3+2+2+2+2+2+2+2) = 15 × 17 = 255 = 0xFF
        // motivation_acc is purely combinational on inputs
        #1;
        $display("[F-HW-SI-2] motivation=%0d (expect 255)", motivation_acc);
        pass_f2 = (motivation_acc == 8'hFF);
        if (pass_f2) $display("PASS F-HW-SI-2");
        else         $display("FAIL F-HW-SI-2");

        // ── F-HW-SI-3: threshold cross → emit_pulse for 1 cycle ────────
        // safety inputs ON; score is already saturated above threshold
        kill_sw = 1; phi_ratchet_ok = 1; content_ok = 1;
        strategy_idx = 3'd1;
        // Wait one clock for FSM IDLE → EMIT_PULSE
        @(posedge clk); #1;
        // Now state should be EMIT_PULSE → emit_pulse high
        $display("[F-HW-SI-3] cycle=%0d emit=%b (expect 1)", cell_count, emit_pulse);
        pass_f3 = (emit_pulse == 1'b1);
        // Next cycle: must drop back to 0 (single-pulse)
        @(posedge clk); #1;
        $display("[F-HW-SI-3] next cycle emit=%b (expect 0)", emit_pulse);
        pass_f3 = pass_f3 && (emit_pulse == 1'b0);
        if (pass_f3) $display("PASS F-HW-SI-3");
        else         $display("FAIL F-HW-SI-3");

        // ── F-HW-SI-4: safety ratchet limits emit rate ─────────────────
        // Run 100 cycles with inputs still maxed + safety on; count emits.
        emit_count = 0;
        for (i = 0; i < 100; i = i + 1) begin
            @(posedge clk); #1;
            if (emit_pulse) emit_count = emit_count + 1;
        end
        $display("[F-HW-SI-4] emit_count over 100 cycles = %0d (expect <= 4)", emit_count);
        // With RATE_LIMIT_CYCLES = 20, minimum gap between emits is ~22 cycles
        // (1 EMIT_PULSE + 1 entering COOLDOWN + 20 cooldown). 100 / 22 ≈ 4
        pass_f4 = (emit_count <= 4) && (emit_count >= 1);
        if (pass_f4) $display("PASS F-HW-SI-4");
        else         $display("FAIL F-HW-SI-4");

        // ── F-HW-SI-5: audit ring buffer depth = 8, last-N preserved ───
        // We have now produced (1 from F-HW-SI-3) + emit_count emits.
        // Generate 5 more with varying strategy_idx so we can verify writeback.
        strategy_idx = 3'd5;
        for (i = 0; i < 200; i = i + 1) begin
            @(posedge clk); #1;
            if (emit_pulse) begin
                $display("[F-HW-SI-5] emit @cycle=%0d audit_dump=%h",
                         cell_count, audit_dump);
            end
        end
        // Each audit entry is 16 bits: {accepted[1], strategy[3], score[8], pad[4]}
        // Most recent entry should have accepted=1, strategy=5, score=0xFF.
        // We probe by checking that at least one slot in audit_dump matches the
        // expected pattern (accepted=1 strategy=5 score=FF) and that all 8
        // entries have the "accepted" MSB set (ring buffer fully populated).
        pass_f5 = 1'b1;
        begin: chk_audit
            reg [15:0] ent;
            reg        any_match;
            any_match = 1'b0;
            for (i = 0; i < 8; i = i + 1) begin
                ent = audit_dump[i*16 +: 16];
                if (ent[15] !== 1'b1) pass_f5 = 1'b0;  // all entries populated
                if ((ent[15] == 1'b1) && (ent[14:12] == 3'd5)
                    && (ent[11:4] == 8'hFF)) any_match = 1'b1;
            end
            if (!any_match) pass_f5 = 1'b0;
        end
        $display("[F-HW-SI-5] audit_dump=%h", audit_dump);
        if (pass_f5) $display("PASS F-HW-SI-5");
        else         $display("FAIL F-HW-SI-5");

        $display("---");
        $display("[SUMMARY] F-HW-SI-1=%b F-HW-SI-2=%b F-HW-SI-3=%b F-HW-SI-4=%b F-HW-SI-5=%b",
                 pass_f1, pass_f2, pass_f3, pass_f4, pass_f5);
        $finish;
    end

endmodule

`default_nettype wire
