`include "vc/arithmetic.v"
`include "vc/muxes.v"
`include "vc/regs.v"


module lab1_imul_IntMulAltVRTL_Dpath(
  input  logic        clk,
  input  logic        reset,
  
  //Data Signal 
  input  logic        req_val,
  output logic        req_rdy,
  input  logic [63:0] req_msg,

  output logic        resp_val,
  input  logic        resp_rdy,
  output logic [31:0] resp_msg,

  //Control Signal
  input  logic        a_mux_sel,
  input  logic        b_mux_sel, 
  input  logic        result_reset, 
  input  logic        add_mux_sel, 
  input  logic [4:0]  shamt, 

  //Status Signal 
  output logic [31:0] b_out    
);

  // ''' LAB TASK ''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  // Instantiate datapath and control models here and then connect them
  // together.
  // '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
// a - first 32 bits, b - last 32 bits
//top of mux is 0 
localparam c_nbits = 32; 
//extra stuff, can comment out if necessary 
logic [c_nbits-1:0] req_msg_a;
vc_Mux2#(c_nbits) a_in_mux 
(
  .in0  (req_msg[31:0]),
  .in1  (req_msg[63:32]),
  .sel  (gt_com),
  .out  (req_msg_a)
);

logic [c_nbits-1:0] req_msg_b;
vc_Mux2#(c_nbits) b_in_mux 
(
  .in0  (req_msg[63:32]),
  .in1  (req_msg[31:0]),
  .sel  (gt_com),
  .out  (req_msg_b)
);

logic gt_com; 
vc_GtComparator#(c_nbits) comparator 
(
  .in0  (req_msg[63:32]),
  .in1  (req_msg[31:0]), 
  .out  (gt_com)
);

//MAIN PART OF THE CODE 
//uncomment for functionality if above is commented 
//logic [c_nbits-1:0] req_msg_a = req_msg[63:32];
//logic [c_nbits-1:0] req_msg_b = req_msg[31:0];
logic [c_nbits-1:0] a_mux_out; 
vc_Mux2#(c_nbits) a_mux 
(
  .in0  (a_shift_out),
  .in1  (req_msg_a),
  .sel  (a_mux_sel), 
  .out  (a_mux_out)   
);


logic [c_nbits-1:0] b_mux_out; 
vc_Mux2#(c_nbits) b_mux 
(
  .in0  (b_shift_out),
  .in1  (req_msg_b),  
  .sel  (b_mux_sel),
  .out  (b_mux_out)
); 

logic [c_nbits-1:0] a_reg_out; 
vc_ResetReg#(32, 0) a_reg 
(
  .clk    (clk),
  .reset  (reset),
  .q      (a_reg_out),
  .d      (a_mux_out)
);

logic [c_nbits-1:0] b_reg_out;
vc_ResetReg#(32, 0) b_reg
(
  .clk    (clk),
  .reset  (reset),
  .q      (b_reg_out),
  .d      (b_mux_out)
);

logic [c_nbits-1:0] b_shift_out;
vc_RightLogicalShifter#(c_nbits, 5) b_shift_right 
(
  .in     (b_reg_out), 
  .shamt  (shamt), 
  .out    (b_shift_out)
);

logic [c_nbits-1:0] a_shift_out; 
vc_LeftLogicalShifter#(c_nbits, 5) a_shift_left 
(
  .in     (a_reg_out),
  .shamt  (shamt), 
  .out    (a_shift_out)
);

logic [c_nbits-1:0] result_reg_out; 
vc_ResetReg#(c_nbits) result_reg 
(
    .clk    (clk),
    .reset  (reset || result_reset),
    .q      (result_reg_out),
    .d      (add_mux_out)
);

logic [c_nbits-1:0] result_adder_out;
vc_SimpleAdder#(c_nbits)  result_adder 
(
  .in0    (a_reg_out),
  .in1    (result_reg_out),
  .out    (result_adder_out)
);

logic [c_nbits-1:0] add_mux_out
vc_Mux2#(c_nbits) add_mux 
(
  .in0    (result_reg_out),
  .in1    (result_adder_out),
  .sel    (add_mux_sel),
  .out    (add_mux_out)
);

assign resp_msg = result_reg_out; 
assign b_out = b_reg_out; 

endmodule