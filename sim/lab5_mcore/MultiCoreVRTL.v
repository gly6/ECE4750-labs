//========================================================================
// 1-Core Processor-Cache-Network
//========================================================================

`ifndef LAB5_MCORE_MULTI_CORE_V
`define LAB5_MCORE_MULTI_CORE_V

`include "vc/mem-msgs.v"
`include "vc/trace.v"
`include "lab5_mcore/MultiFourCoreVRTL.v"
`include "lab5_mcore/MemNetVRTL.v"
`include "lab5_mcore/McoreDataCacheVRTL.v"


//''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
// LAB TASK: Include components
//''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

module lab5_mcore_MultiCoreVRTL
(
  input  logic                       clk,
  input  logic                       reset,

  input  logic [c_num_cores-1:0][31:0] mngr2proc_msg,
  input  logic [c_num_cores-1:0]       mngr2proc_val,
  output logic [c_num_cores-1:0]       mngr2proc_rdy,

  output logic [c_num_cores-1:0][31:0] proc2mngr_msg,
  output logic [c_num_cores-1:0]       proc2mngr_val,
  input  logic [c_num_cores-1:0]       proc2mngr_rdy,

  output mem_req_16B_t                 imemreq_msg,
  output logic                         imemreq_val,
  input  logic                         imemreq_rdy,

  input  mem_resp_16B_t                imemresp_msg,
  input  logic                         imemresp_val,
  output logic                         imemresp_rdy,

  output mem_req_16B_t                 dmemreq_msg,
  output logic                         dmemreq_val,
  input  logic                         dmemreq_rdy,

  input  mem_resp_16B_t                dmemresp_msg,
  input  logic                         dmemresp_val,
  output logic                         dmemresp_rdy,

  //  Only takes Core 0's stats_en to the interface
  output logic                         stats_en,
  output logic [c_num_cores-1:0]       commit_inst,
  output logic [c_num_cores-1:0]       icache_miss,
  output logic [c_num_cores-1:0]       icache_access,
  output logic [c_num_cores-1:0]       dcache_miss,
  output logic [c_num_cores-1:0]       dcache_access
);

  localparam c_num_cores = 4;

  mem_req_4B_t    [c_num_cores-1:0]      dcache_req_msg;
  logic           [c_num_cores-1:0]      dcache_req_val;
  logic           [c_num_cores-1:0]      dcache_req_rdy;

  mem_resp_4B_t   [c_num_cores-1:0]      dcache_resp_msg;
  logic           [c_num_cores-1:0]      dcache_resp_val;
  logic           [c_num_cores-1:0]      dcache_resp_rdy;

  mem_req_16B_t   [c_num_cores-1:0]      imemnetreq_msg; 
  logic           [c_num_cores-1:0]      imemnetreq_val;
  logic           [c_num_cores-1:0]      imemnetreq_rdy;

  mem_resp_16B_t  [c_num_cores-1:0]      imemnetresp_msg;
  logic           [c_num_cores-1:0]      imemnetresp_val;
  logic           [c_num_cores-1:0]      imemnetresp_rdy;

  mem_req_16B_t   [c_num_cores-1:0]      all_imemreq_msg; 
  logic           [c_num_cores-1:0]      all_imemreq_val;
  logic           [c_num_cores-1:0]      all_imemreq_rdy;

  mem_resp_16B_t  [c_num_cores-1:0]      all_imemresp_msg;
  logic           [c_num_cores-1:0]      all_imemresp_val;
  logic           [c_num_cores-1:0]      all_imemresp_rdy;

  logic           [c_num_cores-1:0]      all_stats_en; 

  assign stats_en         = all_stats_en[0]; 
  assign imemreq_msg      = all_imemreq_msg[0];
  assign imemreq_val      = all_imemreq_val[0];

  assign imemresp_rdy     = all_imemresp_rdy[0];
 
  assign all_imemreq_rdy  = {{3{1'b0}}, imemreq_rdy};

  assign all_imemresp_msg = {{435{1'b0}}, imemresp_msg};
  assign all_imemresp_val = {{3{1'b0}}, imemresp_val};

  lab5_mcore_MultiFourCoreVRTL proc ( 
      .clk              (clk),
      .reset            (reset),

      .mngr2proc_msg    (mngr2proc_msg),
      .mngr2proc_val    (mngr2proc_val),
      .mngr2proc_rdy    (mngr2proc_rdy),

      .proc2mngr_msg    (proc2mngr_msg),
      .proc2mngr_val    (proc2mngr_val),
      .proc2mngr_rdy    (proc2mngr_rdy),

      .imemnetreq_msg   (imemnetreq_msg),
      .imemnetreq_val   (imemnetreq_val),
      .imemnetreq_rdy   (imemnetreq_rdy),

      .imemnetresp_msg  (imemnetresp_msg),
      .imemnetresp_val  (imemnetresp_val),
      .imemnetresp_rdy  (imemnetresp_rdy),

      .dcache_req_msg   (dcache_req_msg),
      .dcache_req_val   (dcache_req_val),
      .dcache_req_rdy   (dcache_req_rdy),

      .dcache_resp_msg  (dcache_resp_msg),
      .dcache_resp_val  (dcache_resp_val),
      .dcache_resp_rdy  (dcache_resp_rdy),

      .stats_en         (all_stats_en),
      .commit_inst      (commit_inst),
      .icache_miss      (icache_miss),
      .icache_access    (icache_access)
  );

  lab5_mcore_McoreDataCacheVRTL dcache (
      .clk              (clk),
      .reset            (reset),

      .procreq_msg      (dcache_req_msg),
      .procreq_val      (dcache_req_val),
      .procreq_rdy      (dcache_req_rdy),

      .procresp_msg     (dcache_resp_msg),
      .procresp_val     (dcache_resp_val),
      .procresp_rdy     (dcache_resp_rdy),

      .mainmemreq_msg   (dmemreq_msg),
      .mainmemreq_val   (dmemreq_val),
      .mainmemreq_rdy   (dmemreq_rdy),

      .mainmemresp_msg  (dmemresp_msg),
      .mainmemresp_val  (dmemresp_val),
      .mainmemresp_rdy  (dmemresp_rdy),

      .dcache_miss      (dcache_miss),
      .dcache_access    (dcache_access)
  );

  lab5_mcore_MemNetVRTL icache (
      .clk              (clk),
      .reset            (reset),

      .memreq_msg       (imemnetreq_msg),
      .memreq_val       (imemnetreq_val),
      .memreq_rdy       (imemnetreq_rdy),

      .memresp_msg      (imemnetresp_msg),
      .memresp_val      (imemnetresp_val),
      .memresp_rdy      (imemnetresp_rdy),

      .mainmemreq_msg   (all_imemreq_msg),
      .mainmemreq_val   (all_imemreq_val),
      .mainmemreq_rdy   (all_imemreq_rdy),

      .mainmemresp_msg  (all_imemresp_msg),
      .mainmemresp_val  (all_imemresp_val),
      .mainmemresp_rdy  (all_imemresp_rdy)
  );
  // Only takes proc0's stats_en
  //''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  // LAB TASK: hook up stats and add icache stats
  //''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

  `VC_TRACE_BEGIN
  begin

    // This is staffs' line trace, which assume the processors and icaches
    // are instantiated in using generate statement, and the data cache
    // system is instantiated with the name dcache. You can add net to the
    // line trace.
    // Feel free to revamp it or redo it based on your need.

    // CORES_CACHES[0].icache.line_trace( trace_str );
    // CORES_CACHES[0].proc.line_trace( trace_str );
    // CORES_CACHES[1].icache.line_trace( trace_str );
    // CORES_CACHES[1].proc.line_trace( trace_str );
    // CORES_CACHES[2].icache.line_trace( trace_str );
    // CORES_CACHES[2].proc.line_trace( trace_str );
    // CORES_CACHES[3].icache.line_trace( trace_str );
    // CORES_CACHES[3].proc.line_trace( trace_str );

    // dcache.line_trace( trace_str );
  end
  `VC_TRACE_END

endmodule

`endif /* LAB5_MCORE_MULTI_CORE_V */
