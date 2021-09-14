 //CONTROL DESIGN START

module lab1_imul_IntMulBaseVRTL_IntMulBaseCtrl(
  
  input  logic        clk,
  input  logic        reset,

  // Dataflow signals

  input  logic        req_val,
  output logic        req_rdy,
  output logic        resp_val,
  input  logic        resp_rdy,

  // Control Signals

  output logic a_mux_sel,
  output logic b_mux_sel,
  output logic add_mux_sel,
  output logic result_mux_sel,
  output logic result_en,

  // Data Signals
  
  input logic b_lsb,

);

  //----------------------------------------------------------------------
  // State Definitions
  //----------------------------------------------------------------------

  localparam STATE_IDLE = 2'd0;
  localparam STATE_CALC = 2'd1;
  localparam STATE_DONE = 2'd2;

  //----------------------------------------------------------------------
  // State
  //----------------------------------------------------------------------

  logic [1:0] state_reg;
  logic [1:0] state_next;

  always_ff @( posedge clk ) begin
    if ( reset ) begin
      state_reg <= STATE_IDLE;
    end
    else begin
      state_reg <= state_next;
    end
  end

  //----------------------------------------------------------------------
  // Counter Logic
  //----------------------------------------------------------------------
  logic [7:0] counter;
  logic [7:0] counter_next;
  logic is_cnt_lt_32;

  vc_ResetReg#(8, 0) count_reg
  (
    .clk    (clk),
    .reset  (reset),
    .q      (count_next),
    .d      (counter)  
  );

  // Less-than comparator

  vc_LtComparator#(c_nbits) count_lt_32
  (
    .in0   (counter),
    .in1   (0'd32),
    .out   (is_cnt_lt_32)
  );

  always_ff @(posedge clk) begin
    case (state_reg)
      STATE_CALC: count_next = count_next + 1;
      default: count_next = 0;
    endcase
  end

  //----------------------------------------------------------------------
  // State Transitions
  //----------------------------------------------------------------------

  logic req_go;
  logic resp_go;
  logic is_calc_done;

  assign req_go       = req_val  && req_rdy;
  assign resp_go      = resp_val && resp_rdy;
  assign is_calc_done = !is_cnt_lt_32;

  always_comb begin

    state_next = state_reg;

    case ( state_reg )

      STATE_IDLE: if ( req_go    )    state_next = STATE_CALC;
      STATE_CALC: if ( is_calc_done ) state_next = STATE_DONE;
      STATE_DONE: if ( resp_go   )    state_next = STATE_IDLE;
      default:    state_next = 'x;

    endcase

  end

//----------------------------------------------------------------------
  // State Outputs
  //----------------------------------------------------------------------

  // Mux Parameters

  localparam b_x   = 1'dx;
  localparam b_rs = 1'd0;
  localparam b_ld = 1'd1;
  
  localparam a_x   = 2'dx;
  localparam a_ls = 1'd0;
  localparam a_ld = 1'd1;

  localparam add_x = 1'dx;
  localparam add_add = 1'd0;
  localparam add_resp = 1'd1;

  localparam result_x = 1'dx;
  localparam result_add = 1'd0;
  localparam result_0 = 1'd1;

  // //GCD Mux Values


  // localparam a_ld  = 2'd0;
  // localparam a_b   = 2'd1;
  // localparam a_sub = 2'd2;

  // localparam b_ld  = 1'd0;
  // localparam b_a   = 1'd1;

  // //End GCD Mux Values

  task cs
  (
    input logic       cs_req_rdy,
    input logic       cs_resp_val,
    input logic [1:0] cs_a_mux_sel,
    input logic       cs_b_mux_sel,
    input logic       cs_add_mux_sel,
    input logic       cs_result_mux_sel,
    input logic       cs_result_en
  );
  begin
    req_rdy   = cs_req_rdy;
    resp_val  = cs_resp_val;
    a_mux_sel = cs_a_mux_sel;
    b_mux_sel = cs_b_mux_sel;
    add_mux_sel = cs_add_mux_sel;
    result_mux_sel = cs_result_mux_sel;
    result_en = cs_result_en;
  end
  endtask

  // Labels for Mealy transistions

  logic do_swap;
  logic do_sub;

  assign do_add_shift = b_lsb;
  assign do_shift  = !b_lsb;

  // Set outputs using a control signal "table"

  always_comb begin
    
    //req rdy, resp val, a_mux_sel, b_mux_sel, add_mux_sel, result_mux_sel, result_en
    cs( 0, 0, a_x, 0, b_x, 0 );
    case ( state_reg )
      //                             req resp a mux  a  b mux b  
      //                             rdy val  sel    en sel   en
      //STATE_IDLE:                cs( 1,  0,   a_ld,  1, b_ld, 1 );
      STATE_IDLE:                     cs( 1, 0, a_ld, b_ld, add_resp, result_0, 1);
      STATE_CALC: if ( do_add_shift ) cs( 0, 0, a_ls, b_rs, add_add, result_add, 1);
             else if ( do_shift  )    cs( 0, 0, a_ls, b_rs, add_resp, result_add, 0);
      STATE_DONE:                     cs( 0, 1, a_x, b_x, add_resp, result_add, 0);
      default                         cs( 'x, 'x, a_x, b_x, add_x, result_x, 'x);

    endcase

  end

endmodule


  //CONTROL DESIGN END
