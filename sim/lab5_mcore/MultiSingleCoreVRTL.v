`ifndef LAB5_MCORE_MULTI_SINGLE_CORE_V
`define LAB5_MCORE_MULTI_SINGLE_CORE_V

`include "vc/mem-msgs.v"
`include "vc/trace.v"
`include "lab2_proc/ProcAltVRTL.v"
`include "lab3_mem/BlockingCacheAltVRTL.v"

module lab5_mcore_MultiSingleCoreVRTL(
  input  logic                         clk,
  input  logic                         reset,
  input  logic [31:0]                  core_id, 

  input  logic [31:0]                  mngr2proc_msg,
  input  logic                         mngr2proc_val,
  output logic                         mngr2proc_rdy,

  output logic [31:0]                  proc2mngr_msg,
  output logic                         proc2mngr_val,
  input  logic                         proc2mngr_rdy,

  output mem_req_16B_t                 imemnetreq_msg,
  output logic                         imemnetreq_val,
  input  logic                         imemnetreq_rdy,

  input  mem_resp_16B_t                imemnetresp_msg,
  input  logic                         imemnetresp_val,
  output logic                         imemnetresp_rdy,
  
  output mem_req_4B_t                  dcache_req_msg,
  output logic                         dcache_req_val,
  input  logic                         dcache_req_rdy,

  input  mem_resp_4B_t                 dcache_resp_msg,
  input  logic                         dcache_resp_val,
  output logic                         dcache_resp_rdy,

  //  Only takes Core 0's stats_en to the interface
  output logic                         stats_en,
  output logic                         commit_inst,
  output logic                         icache_miss,
  output logic                         icache_access

);

  mem_req_4B_t                          icache_req_msg;
  logic                                 icache_req_val;
  logic                                 icache_req_rdy;

  mem_resp_4B_t                         icache_resp_msg;
  logic                                 icache_resp_val;
  logic                                 icache_resp_rdy;

  logic                                 proc_commit_inst;

lab2_proc_ProcAltVRTL  
  #(
    .p_num_cores  (4)
  ) proc 
  (
    .clk           (clk),
    .reset         (reset),

    .core_id       (core_id),

    .imemreq_msg   (icache_req_msg),
    .imemreq_val   (icache_req_val),
    .imemreq_rdy   (icache_req_rdy),

    .imemresp_msg  (icache_resp_msg),
    .imemresp_val  (icache_resp_val),
    .imemresp_rdy  (icache_resp_rdy),

    .dmemreq_msg   (dcache_req_msg),
    .dmemreq_val   (dcache_req_val),
    .dmemreq_rdy   (dcache_req_rdy),

    .dmemresp_msg  (dcache_resp_msg),
    .dmemresp_val  (dcache_resp_val),
    .dmemresp_rdy  (dcache_resp_rdy),

    .mngr2proc_msg (mngr2proc_msg),
    .mngr2proc_val (mngr2proc_val),
    .mngr2proc_rdy (mngr2proc_rdy),

    .proc2mngr_msg (proc2mngr_msg),
    .proc2mngr_val (proc2mngr_val),
    .proc2mngr_rdy (proc2mngr_rdy),

    .stats_en      (stats_en),
    .commit_inst   (proc_commit_inst)
  );

  lab3_mem_BlockingCacheAltVRTL 
  #(
    .p_num_banks   (1)
  )
  icache
  (
    .clk           (clk),
    .reset         (reset),

    .cachereq_msg  (icache_req_msg),
    .cachereq_val  (icache_req_val),
    .cachereq_rdy  (icache_req_rdy),

    .cacheresp_msg (icache_resp_msg),
    .cacheresp_val (icache_resp_val),
    .cacheresp_rdy (icache_resp_rdy),

    .memreq_msg    (imemnetreq_msg),
    .memreq_val    (imemnetreq_val),
    .memreq_rdy    (imemnetreq_rdy),

    .memresp_msg   (imemnetresp_msg),
    .memresp_val   (imemnetresp_val),
    .memresp_rdy   (imemnetresp_rdy)

  );

  assign commit_inst   = proc_commit_inst;
  assign icache_miss   = icache_resp_val & icache_resp_rdy & ~icache_resp_msg.test[0];
  assign icache_access = icache_req_val  & icache_req_rdy;

endmodule 
`endif /* LAB5_MCORE_MULTI_CORE_V */