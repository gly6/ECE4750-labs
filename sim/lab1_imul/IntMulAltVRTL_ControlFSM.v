 //CONTROL DESIGN START

module lab1_imul_IntMulAltVRTL_IntMulAltCtrl(
  
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
  output logic result_reset,
  output logic result_en,
  output logic[4:0] shamt,
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
 always_ff @( posedge clk ) begin
    if ( reset ) begin
      state_reg <= STATE_IDLE;
    end
    else begin
      state_reg <= state_next;
    end
  end
  //----------------------------------------------------------------------
  // State Transitions
  //----------------------------------------------------------------------

  logic req_go;
  logic resp_go;
  logic is_calc_done;

  assign req_go       = req_val  && req_rdy;
  assign resp_go      = resp_val && resp_rdy;
  assign is_calc_done = ((b_out & 32'hFFFFFFFF) == 0);

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

  localparam add_x = 1'dx;
  localparam add_add = 1'd0;
  localparam add_resp = 1'd1;

  task cs
  (
    input logic       cs_req_rdy,
    input logic       cs_resp_val,
    input logic       cs_a_mux_sel,
    input logic       cs_b_mux_sel,
    input logic       cs_add_mux_sel,
    input logic       cs_result_en,
    input logic       cs_result_reset,
    input logic[4:0]  cs_shamt
  );
  begin
    req_rdy   = cs_req_rdy;
    resp_val  = cs_resp_val;
    a_mux_sel = cs_a_mux_sel;
    b_mux_sel = cs_b_mux_sel;
    add_mux_sel = cs_add_mux_sel;
    result_en = cs_result_en;
    result_reset = cs_result_reset;
    shamt = cs_shamt;
  end
  endtask
 

  // Set outputs using a control signal "table"

  always_comb begin
    
    //req rdy, resp val, a_mux_sel, b_mux_sel, add_mux_sel, result_en, result_reset, shamt
    case ( state_reg )
      //                             req resp a mux  a  b mux b  
      //                             rdy val  sel    en sel   en
      //STATE_IDLE:                                 cs( 1,  0,   a_ld,  1, b_ld, 1 );

      STATE_IDLE:                                      cs( 1, 0, a_ld, b_ld, add_resp, 0, 1, 0);
      STATE_CALC: if ( (b_out[30:0] & 31'h7FFFFFFF) == 0 ) cs( 0, 0, a_ls, b_rs, add_resp, 1, 0, 31);
             else if ( (b_out[29:0] & 30'h3FFFFFFF) == 0 ) cs( 0, 0, a_ls, b_rs, add_resp, 1, 0, 30);
             else if ( (b_out[28:0] & 29'h1FFFFFFF) == 0 ) cs( 0, 0, a_ls, b_rs, add_resp, 1, 0, 29);
             else if ( (b_out[27:0] & 28'hFFFFFFF) == 0 ) cs( 0, 0, a_ls, b_rs, add_resp, 1, 0, 28);
             else if ( (b_out[26:0] & 27'h7FFFFFF) == 0 ) cs( 0, 0, a_ls, b_rs, add_resp, 1, 0, 27);
             else if ( (b_out[25:0] & 26'h3FFFFFF) == 0 ) cs( 0, 0, a_ls, b_rs, add_resp, 1, 0, 26);
             else if ( (b_out[24:0] & 25'h1FFFFFF) == 0 ) cs( 0, 0, a_ls, b_rs, add_resp, 1, 0, 25);
             else if ( (b_out[23:0] & 24'hFFFFFF) == 0 ) cs( 0, 0, a_ls, b_rs, add_resp, 1, 0, 24);
             else if ( (b_out[22:0] & 23'h7FFFFF) == 0 ) cs( 0, 0, a_ls, b_rs, add_resp, 1, 0, 23);
             else if ( (b_out[21:0] & 22'h3FFFFF) == 0 ) cs( 0, 0, a_ls, b_rs, add_resp, 1, 0, 22);
             else if ( (b_out[20:0] & 21'h1FFFFF) == 0 ) cs( 0, 0, a_ls, b_rs, add_resp, 1, 0, 21);
             else if ( (b_out[19:0] & 20'hFFFFF) == 0 ) cs( 0, 0, a_ls, b_rs, add_resp, 1, 0, 20);
             else if ( (b_out[18:0] & 19'h7FFFF) == 0 ) cs( 0, 0, a_ls, b_rs, add_resp, 1, 0, 19);
             else if ( (b_out[17:0] & 18'h3FFFF) == 0 ) cs( 0, 0, a_ls, b_rs, add_resp, 1, 0, 18);
             else if ( (b_out[16:0] & 17'h1FFFF) == 0 ) cs( 0, 0, a_ls, b_rs, add_resp, 1, 0, 17);
             else if ( (b_out[15:0] & 16'hFFFF) == 0 ) cs( 0, 0, a_ls, b_rs, add_resp, 1, 0, 16);
             else if ( (b_out[14:0] & 15'h7FFF) == 0 ) cs( 0, 0, a_ls, b_rs, add_resp, 1, 0, 15);
             else if ( (b_out[13:0] & 14'h3FFF) == 0 ) cs( 0, 0, a_ls, b_rs, add_resp, 1, 0, 14);
             else if ( (b_out[12:0] & 13'h1FFF) == 0 ) cs( 0, 0, a_ls, b_rs, add_resp, 1, 0, 13);
             else if ( (b_out[11:0] & 12'hFFF) == 0 ) cs( 0, 0, a_ls, b_rs, add_resp, 1, 0, 12);
             else if ( (b_out[10:0] & 11'h7FF) == 0 ) cs( 0, 0, a_ls, b_rs, add_resp, 1, 0, 11);
             else if ( (b_out[9:0] & 10'h3FF) == 0 ) cs( 0, 0, a_ls, b_rs, add_resp, 1, 0, 10);
             else if ( (b_out[8:0] & 9'h1FF) == 0 ) cs( 0, 0, a_ls, b_rs, add_resp, 1, 0, 9);
             else if ( (b_out[7:0] & 8'hFF) == 0 ) cs( 0, 0, a_ls, b_rs, add_resp, 1, 0, 8);
             else if ( (b_out[6:0] & 7'h7F) == 0 ) cs( 0, 0, a_ls, b_rs, add_resp, 1, 0, 7);
             else if ( (b_out[5:0] & 6'h3F) == 0 ) cs( 0, 0, a_ls, b_rs, add_resp, 1, 0, 6);
             else if ( (b_out[4:0] & 5'h1F) == 0 ) cs( 0, 0, a_ls, b_rs, add_resp, 1, 0, 5);
             else if ( (b_out[3:0] & 4'hF) == 0 ) cs( 0, 0, a_ls, b_rs, add_resp, 1, 0, 4);
             else if ( (b_out[2:0] & 3'h7) == 0 ) cs( 0, 0, a_ls, b_rs, add_resp, 1, 0, 3);
             else if ( (b_out[1:0] & 2'h3) == 0 ) cs( 0, 0, a_ls, b_rs, add_resp, 1, 0, 2);
             else if ( (b_out[0:0] & 1'h1) == 0 ) cs( 0, 0, a_ls, b_rs, add_resp, 1, 0, 1);
             else cs( 0, 0, a_ls, b_rs, add_add, 1, 0, 1);

      STATE_DONE:                     cs( 0, 1, a_x, b_x, add_x, 0, 0, 0);
      default                         cs( 'x, 'x, a_x, b_x, add_x, 'x, 'x, 'x);


    endcase

  end

endmodule


  //CONTROL DESIGN END
