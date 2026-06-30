// ising_fsm.v — anima spontaneous emission FSM (Path B, ECP5 fallback)
//
// SW source: HEXAD/CHAT/spontaneous_smoke.hexa + spontaneous_lib.hexa
//   motivation_score(rel,gap,cur,pain,coh,orig,bal,dyn) = Σ w_i · factor_i
//   should_emit(score) = score > 0.3   (IM threshold)
//   safety_combined(kill, rate, phi_r, content) = AND
//   audit_entry_accepted(score, strategy, accepted) → ring buffer depth=8
//
// HW realization (Path B): 8 × 4-bit factor inputs → weighted sum
// (single-cycle combinational adder) → 8-bit motivation accumulator →
// threshold cmp → 3-state emit FSM → safety AND → audit ring buffer (8 × 16).
//
// Reset state: motivation=0, FSM=IDLE, cooldown=0, audit cleared.
// Clock domain: single clk (~50-150 MHz target on ECP5-25F/85F).

`default_nettype none

module ising_fsm #(
    parameter IM_THRESHOLD        = 8'd77,    // ~0.3 in Q0.8 (0.30 × 256 = 76.8)
    parameter INTERRUPT_THRESHOLD = 8'd153,   // ~0.6 in Q0.8 (0.60 × 256 = 153.6)
    parameter RATE_LIMIT_CYCLES   = 16'd30,   // toy; scale to clk freq for real-time
    parameter AUDIT_DEPTH         = 4'd8      // last-N ring buffer depth
) (
    input  wire        clk,
    input  wire        rst_n,            // async active-low

    // 8 factor inputs (Q0.4 fixed-point ∈ [0, 15])
    input  wire [3:0]  f_rel, f_gap, f_cur, f_pain,
    input  wire [3:0]  f_coh, f_orig, f_bal, f_dyn,

    // safety / control inputs
    input  wire        kill_sw,          // 1 = enabled (env ANIMA_SPONT_OFF=0)
    input  wire        phi_ratchet_ok,   // 1 = phi > ratchet/2
    input  wire        content_ok,       // 1 = content_clean
    input  wire [2:0]  strategy_idx,     // {0..7}, audit-only (caller controls rotation)

    // outputs
    output wire        emit_pulse,       // 1-cycle high on emit fire
    output wire [7:0]  motivation_acc,   // current weighted-sum score (Q0.8)
    output wire        gate_im,          // score > IM_THRESHOLD
    output wire        gate_intrpt,      // score > INTERRUPT_THRESHOLD
    output wire        safety_combined_w,// kill & rate_ok & phi_r & content
    output wire [15:0] cell_count,       // cycle count since reset
    output wire [127:0] audit_dump       // {8 entries × 16 bit each}
);

    // ── §1 weighted sum (combinational adder, Q4.4-ish → Q0.8 via >>4) ───
    // Weights chosen to mirror spont_weight_* (sum ≈ 17, see DESIGN.md §4)
    //   relevance=3, info_gap=2, curiosity=2, pain=2,
    //   coherence=2, originality=2, balance=2, dynamics=2
    wire [11:0] weighted_sum;
    assign weighted_sum =
          {4'b0, f_rel}  * 4'd3
        + {4'b0, f_gap}  * 4'd2
        + {4'b0, f_cur}  * 4'd2
        + {4'b0, f_pain} * 4'd2
        + {4'b0, f_coh}  * 4'd2
        + {4'b0, f_orig} * 4'd2
        + {4'b0, f_bal}  * 4'd2
        + {4'b0, f_dyn}  * 4'd2;
    // weighted_sum ∈ [0, 15 × 17] = [0, 255] → fits 8-bit
    assign motivation_acc = weighted_sum[7:0];

    // ── §2 threshold cmps (combinational) ──────────────────────────────
    assign gate_im     = (motivation_acc > IM_THRESHOLD);
    assign gate_intrpt = (motivation_acc > INTERRUPT_THRESHOLD);

    // ── §3 cooldown counter (rate-limit ratchet) ───────────────────────
    reg [15:0] cooldown_cnt;
    wire rate_ok;
    assign rate_ok = (cooldown_cnt == 16'd0);

    assign safety_combined_w = kill_sw & rate_ok & phi_ratchet_ok & content_ok;

    // ── §4 emit FSM (3 states: IDLE, EMIT_PULSE, COOLDOWN) ─────────────
    localparam ST_IDLE       = 2'd0;
    localparam ST_EMIT_PULSE = 2'd1;
    localparam ST_COOLDOWN   = 2'd2;
    reg [1:0] state, state_n;

    always @(*) begin
        state_n = state;
        case (state)
            ST_IDLE: begin
                if (gate_im & safety_combined_w) state_n = ST_EMIT_PULSE;
            end
            ST_EMIT_PULSE: begin
                state_n = ST_COOLDOWN;
            end
            ST_COOLDOWN: begin
                if (cooldown_cnt == 16'd0) state_n = ST_IDLE;
            end
            default: state_n = ST_IDLE;
        endcase
    end

    // ── §5 audit ring buffer (8 × 16-bit) ──────────────────────────────
    //   layout per entry: {accepted[1], strategy_idx[3], score[8], pad[4]}
    reg [15:0] audit [0:7];
    reg [2:0]  audit_wptr;
    reg [15:0] cell_count_r;

    integer k;

    // emit_pulse is combinational on current state: high for exactly the one
    // cycle when state == ST_EMIT_PULSE (entered from IDLE, exits to COOLDOWN).
    assign emit_pulse = (state == ST_EMIT_PULSE);

    // ── §6 sequential update ───────────────────────────────────────────
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            state        <= ST_IDLE;
            cooldown_cnt <= 16'd0;
            audit_wptr   <= 3'd0;
            cell_count_r <= 16'd0;
            for (k = 0; k < 8; k = k + 1) audit[k] <= 16'd0;
        end else begin
            state        <= state_n;
            cell_count_r <= cell_count_r + 16'd1;

            // cooldown counter decrement (saturate at 0)
            if (cooldown_cnt != 16'd0) cooldown_cnt <= cooldown_cnt - 16'd1;

            // On entering EMIT_PULSE (from IDLE): reload cooldown + push audit
            if (state == ST_IDLE && state_n == ST_EMIT_PULSE) begin
                cooldown_cnt      <= RATE_LIMIT_CYCLES;
                audit[audit_wptr] <= {1'b1, strategy_idx, motivation_acc, 4'b0000};
                audit_wptr        <= audit_wptr + 3'd1;
            end
        end
    end

    assign cell_count = cell_count_r;

    // pack 8 × 16-bit audit entries (entry 0 = LSB)
    assign audit_dump = {audit[7], audit[6], audit[5], audit[4],
                         audit[3], audit[2], audit[1], audit[0]};

endmodule

`default_nettype wire
