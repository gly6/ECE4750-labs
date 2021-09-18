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
  output logic result_reset,
  output logic[4:0] shamt,
  output logic result_en

  // Data Signals
  
  input logic[31:0] b_out

);
  localparam c_nbits = 32;
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

  //----------------------------------------------------------------------
  // State Transitions
  //----------------------------------------------------------------------

  logic req_go;
  logic resp_go;
  logic is_calc_done;

  assign req_go       = req_val  && req_rdy;
  assign resp_go      = resp_val && resp_rdy;
  assign is_calc_done = !(b_out && 32'xFFFFFFFF);

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

  localparam b_x  = 1'dx;
  localparam b_rs = 1'd0;
  localparam b_ld = 1'd1;
  
  localparam a_x  = 1'dx;
  localparam a_ls = 1'd0;
  localparam a_ld = 1'd1;

  task cs
  (
    input logic       cs_req_rdy,
    input logic       cs_resp_val,
    input logic       cs_a_mux_sel,
    input logic       cs_b_mux_sel,
    input logic       cs_result_en,
    input logic       cs_result_reset,
    input logic[4:0]  cs_shamt
  );
  begin
    req_rdy   = cs_req_rdy;
    resp_val  = cs_resp_val;
    a_mux_sel = cs_a_mux_sel;
    b_mux_sel = cs_b_mux_sel;
    result_reset = cs_result_reset;
    shamt = cs_shamt;
    result_en = cs_result_en;
  end
  endtask


  // Set outputs using a control signal "table"

  always_comb begin
    
    //req rdy, resp val, a_mux_sel, b_mux_sel, result_en, result_reset, shamt
    case ( state_reg )
      //                             req resp a mux  a  b mux b  
      //                             rdy val  sel    en sel   en
      //STATE_IDLE:                                 cs( 1,  0,   a_ld,  1, b_ld, 1 );
      STATE_IDLE:                                      cs( 1, 0, a_ld, b_ld, 0, 1, 0);
      STATE_CALC: if ( !([31:0]b_out && 32'xFFFFFFFF) ) cs( 0, 0, a_ls, b_rs, 1, 0, 32);
             else if ( !([30:0]b_out && 31'xFFFFFFFF) ) cs( 0, 0, a_ls, b_rs, 1, 0, 31);
             else if ( !([29:0]b_out && 31'xFFFFFFFF) ) cs( 0, 0, a_ls, b_rs, 1, 0, 30);
             else if ( !([28:0]b_out && 31'xFFFFFFFF) ) cs( 0, 0, a_ls, b_rs, 1, 0, 29);
             else if ( !([27:0]b_out && 31'xFFFFFFFF) ) cs( 0, 0, a_ls, b_rs, 1, 0, 28);
             else if ( !([26:0]b_out && 31'xFFFFFFFF) ) cs( 0, 0, a_ls, b_rs, 1, 0, 27);
             else if ( !([25:0]b_out && 31'xFFFFFFFF) ) cs( 0, 0, a_ls, b_rs, 1, 0, 26);
             else if ( !([24:0]b_out && 31'xFFFFFFFF) ) cs( 0, 0, a_ls, b_rs, 1, 0, 25);
             else if ( !([23:0]b_out && 31'xFFFFFFFF) ) cs( 0, 0, a_ls, b_rs, 1, 0, 24);
             else if ( !([22:0]b_out && 31'xFFFFFFFF) ) cs( 0, 0, a_ls, b_rs, 1, 0, 23);
             else if ( !([21:0]b_out && 31'xFFFFFFFF) ) cs( 0, 0, a_ls, b_rs, 1, 0, 22);
             else if ( !([20:0]b_out && 31'xFFFFFFFF) ) cs( 0, 0, a_ls, b_rs, 1, 0, 21);
             else if ( !([19:0]b_out && 31'xFFFFFFFF) ) cs( 0, 0, a_ls, b_rs, 1, 0, 20);
             else if ( !([18:0]b_out && 31'xFFFFFFFF) ) cs( 0, 0, a_ls, b_rs, 1, 0, 19);
             else if ( !([17:0]b_out && 31'xFFFFFFFF) ) cs( 0, 0, a_ls, b_rs, 1, 0, 18);
             else if ( !([16:0]b_out && 31'xFFFFFFFF) ) cs( 0, 0, a_ls, b_rs, 1, 0, 17);
             else if ( !([15:0]b_out && 31'xFFFFFFFF) ) cs( 0, 0, a_ls, b_rs, 1, 0, 16);
             else if ( !([14:0]b_out && 31'xFFFFFFFF) ) cs( 0, 0, a_ls, b_rs, 1, 0, 15);
             else if ( !([13:0]b_out && 31'xFFFFFFFF) ) cs( 0, 0, a_ls, b_rs, 1, 0, 14);
             else if ( !([12:0]b_out && 31'xFFFFFFFF) ) cs( 0, 0, a_ls, b_rs, 1, 0, 13);
             else if ( !([11:0]b_out && 31'xFFFFFFFF) ) cs( 0, 0, a_ls, b_rs, 1, 0, 12);
             else if ( !([10:0]b_out && 31'xFFFFFFFF) ) cs( 0, 0, a_ls, b_rs, 1, 0, 11);
             else if ( !([9:0]b_out && 31'xFFFFFFFF) ) cs( 0, 0, a_ls, b_rs, 1, 0, 10);
             else if ( !([8:0]b_out && 31'xFFFFFFFF) ) cs( 0, 0, a_ls, b_rs, 1, 0, 9);
             else if ( !([7:0]b_out && 31'xFFFFFFFF) ) cs( 0, 0, a_ls, b_rs, 1, 0, 8);
             else if ( !([6:0]b_out && 31'xFFFFFFFF) ) cs( 0, 0, a_ls, b_rs, 1, 0, 7);
             else if ( !([5:0]b_out && 31'xFFFFFFFF) ) cs( 0, 0, a_ls, b_rs, 1, 0, 6);
             else if ( !([4:0]b_out && 31'xFFFFFFFF) ) cs( 0, 0, a_ls, b_rs, 1, 0, 5);
             else if ( !([3:0]b_out && 31'xFFFFFFFF) ) cs( 0, 0, a_ls, b_rs, 1, 0, 4);
             else if ( !([2:0]b_out && 31'xFFFFFFFF) ) cs( 0, 0, a_ls, b_rs, 1, 0, 3);
             else if ( !([1:0]b_out && 31'xFFFFFFFF) ) cs( 0, 0, a_ls, b_rs, 1, 0, 2);
             else if ( !([0:0]b_out && 31'xFFFFFFFF) ) cs( 0, 0, a_ls, b_rs, 1, 0, 1);
             else cs( 0, 0, a_ls, b_rs, 0, 0, 0);

      STATE_DONE:                                    cs( 0, 1, a_x, b_x, 0, 0, 0);
      default                         cs( 'x, 'x, a_x, b_x, add_x, result_x, 'x);

    endcase

  end

endmodule


  //CONTROL DESIGN END
