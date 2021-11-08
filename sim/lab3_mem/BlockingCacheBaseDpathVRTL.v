//=========================================================================
// Baseline Blocking Cache Datapath
//=========================================================================

`ifndef LAB3_MEM_BLOCKING_CACHE_BASE_DPATH_V
`define LAB3_MEM_BLOCKING_CACHE_BASE_DPATH_V

`include "vc/mem-msgs.v"
`include "vc/arithmetic.v"
`include "vc/muxes.v"
`include "vc/regs.v"
`include "vc/srams.v"

//''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
// LAB TASK: Include necessary files
//''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

module lab3_mem_BlockingCacheBaseDpathVRTL
#(
  parameter p_idx_shamt    = 0
)
(
  input  logic                        clk,
  input  logic                        reset,

  // Cache Request

  input  mem_req_4B_t                 cachereq_msg,

  // Cache Response

  output mem_resp_4B_t                cacheresp_msg,

  // Memory Request

  output mem_req_16B_t                memreq_msg,

  // Memory Response

  input  mem_resp_16B_t               memresp_msg,

  //''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  // LAB TASK: Define additional ports
  //''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

  // Control Signals

  input logic cachereq_en,
  input logic memresp_en,
  input logic write_data_mux_sel,
  input logic tag_array_ren,
  input logic tag_array_wen,
  input logic data_array_ren,
  input logic data_array_wen,
  input logic data_array_wben,
  input logic read_data_reg_en,
  input logic evict_addr_reg_en,
  input logic memreq_addr_mux_sel,
  input logic hit,
  input logic [1:0] read_word_mux_sel,
  input logic [2:0] cacheresp_type,
  input logic [2:0] memreq_type,
  
  // Status Signals
  
  output logic [2:0] cachereq_type,
  output logic [31:0] cachereq_addr,
  output logic tag_match,
  
);

  // local parameters not meant to be set from outside
  localparam size = 256;             // Cache size in bytes
  localparam dbw  = 32;              // Short name for data bitwidth
  localparam abw  = 32;              // Short name for addr bitwidth
  localparam o    = 8;               // Short name for opaque bitwidth
  localparam clw  = 128;             // Short name for cacheline bitwidth
  localparam nbl  = size*8/clw;      // Number of blocks in the cache
  localparam nby  = nbl;             // Number of blocks per way
  localparam idw  = $clog2(nby);     // Short name for index bitwidth
  localparam ofw  = $clog2(clw/8);   // Short name for the offset bitwidth
  // In this lab, to simplify things, we always use all bits except for the
  // offset in the tag, rather than storing the "normal" 24 bits. This way,
  // when implementing a multi-banked cache, we don't need to worry about
  // re-inserting the bank id into the address of a cacheline.
  localparam tgw  = abw - ofw;       // Short name for the tag bitwidth

//''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
// LAB TASK: Implement data-path
//''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''



logic [127:0] memresp_data_reg_out; 
vc_EnReg#(dbw, 0) cachereq_data_reg
(
  .clk    (clk),
  .reset  (reset),
  .q      (memresp_data_reg_out),
  .d      (memresp_msg [127:0]),
  .en     (memresp_en)
);


logic [dbw-1:0] cachereq_data_reg_out; 
vc_EnReg#(dbw, 0) cachereq_data_reg
(
  .clk    (clk),
  .reset  (reset),
  .q      (cachereq_data_reg_out),
  .d      (cachereq_msg [dbw-1:0]),
  .en     (cachereq_en)
);

logic [abw-1:0] cachereq_addr_reg_out; 
vc_EnReg#(abw, 0) cachereq_addr_reg
(
  .clk    (clk),
  .reset  (reset),
  .q      (cachereq_addr_reg_out),
  .d      (cachereq_msg [65:34]),
  .en     (cachereq_en)
);

logic [2:0] cachereq_type_reg_out; 
vc_EnReg#(3, 0) cachereq_type_reg
(
  .clk    (clk),
  .reset  (reset),
  .q      (cachereq_type_reg_out),
  .d      (cachereq_msg [76:74]),
  .en     (cachereq_en)
);

logic [o-1:0] cachereq_opaque_reg_out; 
vc_EnReg#(dbw, 0) cachereq_opaque_reg
(
  .clk    (clk),
  .reset  (reset),
  .q      (cachereq_opaque_reg_out),
  .d      (cachereq_msg [73:66]),
  .en     (cachereq_en)
);

//repl
logic [127:0] repl_out;
assign repl_out = {cachereq_data_reg_out, cachereq_data_reg_out, cachereq_data_reg_out, cachereq_data_reg_out};
//end repl

logic [127:0] write_data_mux_out;
vc_Mux2#(128) write_data_mux 
(
  .in0  (repl_out),
  .in1  (memresp_data_reg_out), 
  .sel  (write_data_mux_sel),
  .out  (write_data_mux_out)
);

logic [27:0] tag_array_read_data;
vc_CombinationalBitSRAM_1rw#(28, 16) tag_array
(
  .clk          (clk),
  .reset        (reset),
  .read_en      (tag_array_ren),
  .read_addr    (cachereq_addr_reg_out[7:4]),
  .write_en     (tag_array_wen),
  .write_addr   (cachereq_addr_reg_out[7:4]),
  .write_data   (cachereq_addr_reg_out[31:4]),
  .read_data    (tag_array_read_data)
);

logic [127:0] data_array_read_data;
vc_CombinationalSRAM_1rw#(128,16) data_array
(
  .clk            (clk),
  .reset          (reset),
  .read_en        (data_array_ren),
  .read_addr      (cachereq_addr_reg_out[7:4]),
  .write_en       (data_array_wen),
  .write_addr     (cachereq_addr_reg_out[7:4]),
  .write_data     (write_data_mux_out),
  .write_byte_en  (data_array_wben),
  .read_data      (data_array_read_data)
);

logic [127:0] read_data_reg_out;
vc_EnReg#(clw, 0) cachereq_opaque_reg
(
  .clk    (clk),
  .reset  (reset),
  .q      (read_data_reg_out),
  .d      (data_array_read_data),
  .en     (read_data_reg_en)
);

endmodule

`endif
