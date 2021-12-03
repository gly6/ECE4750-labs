`ifndef LAB5_MCORE_MULTI_FOUR_CORE_V
`define LAB5_MCORE_MULTI_FOUR_CORE_V

`include "vc/mem-msgs.v"
`include "vc/trace.v"
`include "lab5_mcore/MultiSingleCoreVRTL.v"

module lab5_mcore_MultiFourCoreVRTL (
  input  logic                                    clk,
  input  logic                                    reset,

  input  logic          [c_num_cores-1:0][31:0]   mngr2proc_msg,
  input  logic          [c_num_cores-1:0]         mngr2proc_val,
  output logic          [c_num_cores-1:0]         mngr2proc_rdy,

  output logic          [c_num_cores-1:0][31:0]   proc2mngr_msg,
  output logic          [c_num_cores-1:0]         proc2mngr_val,
  input  logic          [c_num_cores-1:0]         proc2mngr_rdy,
  
  output mem_req_16B_t  [c_num_cores-1:0]         imemnetreq_msg,
  output logic          [c_num_cores-1:0]         imemnetreq_val,
  input  logic          [c_num_cores-1:0]         imemnetreq_rdy,

  input  mem_resp_16B_t [c_num_cores-1:0]         imemnetresp_msg,
  input  logic          [c_num_cores-1:0]         imemnetresp_val,
  output logic          [c_num_cores-1:0]         imemnetresp_rdy,

  output mem_req_4B_t   [c_num_cores-1:0]         dcache_req_msg,
  output logic          [c_num_cores-1:0]         dcache_req_val,
  input  logic          [c_num_cores-1:0]         dcache_req_rdy,

  input  mem_resp_4B_t  [c_num_cores-1:0]         dcache_resp_msg,
  input  logic          [c_num_cores-1:0]         dcache_resp_val,
  output logic          [c_num_cores-1:0]         dcache_resp_rdy,

  output logic          [c_num_cores-1:0]         stats_en,
  output logic          [c_num_cores-1:0]         commit_inst,
  output logic          [c_num_cores-1:0]         icache_miss,
  output logic          [c_num_cores-1:0]         icache_access
); 
localparam c_num_cores = 4;

genvar i; 

generate 
    for ( i = 0; i < c_num_cores; i = i + 1 ) begin: PROC
    
    lab5_mcore_MultiSingleCoreVRTL proc(
        .clk                (clk),
        .reset              (reset),
        .core_id            (i),

        .mngr2proc_msg      (mngr2proc_msg[i]),
        .mngr2proc_val      (mngr2proc_val[i]),
        .mngr2proc_rdy      (mngr2proc_rdy[i]),

        .proc2mngr_msg      (proc2mngr_msg[i]),
        .proc2mngr_val      (proc2mngr_val[i]),
        .proc2mngr_rdy      (proc2mngr_rdy[i]),

        .imemnetreq_msg     (imemnetreq_msg[i]),
        .imemnetreq_val     (imemnetreq_val[i]),
        .imemnetreq_rdy     (imemnetreq_rdy[i]),

        .imemnetresp_msg    (imemnetresp_msg[i]),
        .imemnetresp_val    (imemnetresp_val[i]),
        .imemnetresp_rdy    (imemnetresp_rdy[i]),

        .dcache_req_msg     (dcache_req_msg[i]),
        .dcache_req_val     (dcache_req_val[i]),
        .dcache_req_rdy     (dcache_req_rdy[i]),

        .dcache_resp_msg    (dcache_resp_msg[i]),
        .dcache_resp_val    (dcache_resp_val[i]),
        .dcache_resp_rdy    (dcache_resp_rdy[i]),

        .stats_en           (stats_en[i]),
        .commit_inst        (commit_inst[i]),
        .icache_miss        (icache_miss[i]),
        .icache_access      (icache_access[i])
    ); 
    end
endgenerate
endmodule

`endif /* LAB5_MCORE_MULTI_CORE_V */