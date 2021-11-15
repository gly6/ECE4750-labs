//=========================================================================
// Alternative Blocking Cache Datapath
//=========================================================================

`ifndef LAB3_MEM_BLOCKING_CACHE_ALT_DPATH_V
`define LAB3_MEM_BLOCKING_CACHE_ALT_DPATH_V

`include "vc/mem-msgs.v"

//''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
// LAB TASK: Include necessary files
//''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

module lab3_mem_BlockingCacheAltDpathVRTL
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
  // LAB TASK: Add dpath signals
  //''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  // Control Signals

  input logic cachereq_en,
  input logic memresp_en,
  input logic write_data_mux_sel,
  input logic tag_array_ren_0,
  input logic tag_array_wen_0,
  input logic tag_array_ren_1,
  input logic tag_array_wen_1,
  input logic data_array_ren,
  input logic data_array_wen,
  input logic [15:0] data_array_wben,
  input logic read_data_reg_en,
  input logic evict_addr_reg_en_0,
  input logic evict_addr_reg_en_1,
  input logic [1:0] memreq_addr_mux_sel,
  input logic [1:0] hit,
  input logic [2:0] read_word_mux_sel,
  input logic [2:0] cacheresp_type,
  input logic [2:0] memreq_type,
  
  // Status Signals
  
  output logic [2:0] cachereq_type,
  output logic [31:0] cachereq_addr,
  output logic tag_match_0,
  output logic tag_match_1
  

);

  // local parameters not meant to be set from outside
  localparam size = 256;             // Cache size in bytes
  localparam dbw  = 32;              // Short name for data bitwidth
  localparam abw  = 32;              // Short name for addr bitwidth
  localparam o    = 8;               // Short name for opaque bitwidth
  localparam clw  = 128;             // Short name for cacheline bitwidth
  localparam nbl  = size*8/clw;      // Number of blocks in the cache
  localparam nby  = nbl/2;           // Number of blocks per way
  localparam idw  = $clog2(nby);     // Short name for index bitwidth
  localparam ofw  = $clog2(clw/8);   // Short name for the offset bitwidth
  // In this lab, to simplify things, we always use all bits except for the
  // offset in the tag, rather than storing the "normal" 24 bits. This way,
  // when implementing a multi-banked cache, we don't need to worry about
  // re-inserting the bank id into the address of a cacheline.
  localparam tgw  = abw - ofw;       // Short name for the tag bitwidth

  //''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  // LAB TASK: Implement Dpath
  //'''''''

//First column of datapath

//memresp and cachereq registers

logic [clw-1:0] memresp_data_reg_out; 
vc_EnReg#(clw) memresp_data_reg
(
  .clk    (clk),
  .reset  (reset),
  .q      (memresp_data_reg_out),
  .d      (memresp_msg.data),
  .en     (memresp_en)
);


logic [dbw-1:0] cachereq_data_reg_out; 
vc_EnReg#(dbw) cachereq_data_reg
(
  .clk    (clk),
  .reset  (reset),
  .q      (cachereq_data_reg_out),
  .d      (cachereq_msg.data),
  .en     (cachereq_en)
);

logic [abw-1:0] cachereq_addr_reg_out; 
assign cachereq_addr = cachereq_addr_reg_out;
vc_EnReg#(abw) cachereq_addr_reg
(
  .clk    (clk),
  .reset  (reset),
  .q      (cachereq_addr_reg_out),
  .d      (cachereq_msg.addr),
  .en     (cachereq_en)
);

vc_EnReg#(3) cachereq_type_reg
(
  .clk    (clk),
  .reset  (reset),
  .q      (cachereq_type),
  .d      (cachereq_msg.type_),
  .en     (cachereq_en)
);

logic [o-1:0] cachereq_opaque_reg_out; 
vc_EnReg#(o) cachereq_opaque_reg
(
  .clk    (clk),
  .reset  (reset),
  .q      (cachereq_opaque_reg_out),
  .d      (cachereq_msg.opaque),
  .en     (cachereq_en)
);

//end memresp and cachereq registers

//Second column of datapath

//repl
logic [(dbw*4)-1:0] repl_out;
assign repl_out = {cachereq_data_reg_out, cachereq_data_reg_out, cachereq_data_reg_out, cachereq_data_reg_out};
//end repl

logic [clw-1:0] write_data_mux_out;
vc_Mux2#(clw) write_data_mux 
(
  .in0  (repl_out),
  .in1  (memresp_data_reg_out), 
  .sel  (write_data_mux_sel),
  .out  (write_data_mux_out)
);

//Third column of datapath

//Tag and data arrays
logic [(tgw-1):0] tag_array_read_data_0;
vc_CombinationalBitSRAM_1rw#(tgw, nbl) tag_array_0
(
  .clk          (clk),
  .reset        (reset),
  .read_en      (tag_array_ren_0),
  .read_addr    (cachereq_addr_reg_out[(idw + ofw - 1 + p_idx_shamt):(ofw + p_idx_shamt)]),
  .write_en     (tag_array_wen_0),
  .write_addr   (cachereq_addr_reg_out[(idw + ofw - 1 + p_idx_shamt):(ofw + p_idx_shamt)]),
  .write_data   (cachereq_addr_reg_out[31:4]),
  .read_data    (tag_array_read_data_0)
);

logic [(tgw-1):0] tag_array_read_data_1;
vc_CombinationalBitSRAM_1rw#(tgw, nbl) tag_array_1
(
  .clk          (clk),
  .reset        (reset),
  .read_en      (tag_array_ren_1),
  .read_addr    (cachereq_addr_reg_out[(idw + ofw - 1 + p_idx_shamt):(ofw + p_idx_shamt)]),
  .write_en     (tag_array_wen_1),
  .write_addr   (cachereq_addr_reg_out[(idw + ofw - 1 + p_idx_shamt):(ofw + p_idx_shamt)]),
  .write_data   (cachereq_addr_reg_out[31:4]),
  .read_data    (tag_array_read_data_1)
);

logic [clw - 1:0] data_array_read_data;
vc_CombinationalSRAM_1rw#(clw , nbl) data_array
(
  .clk            (clk),
  .reset          (reset),
  .read_en        (data_array_ren),
  .read_addr      (cachereq_addr_reg_out[(idw + ofw - 1 + p_idx_shamt):(ofw + p_idx_shamt)]),
  .write_en       (data_array_wen),
  .write_addr     (cachereq_addr_reg_out[(idw + ofw - 1 + p_idx_shamt):(ofw + p_idx_shamt)]),
  .write_data     (write_data_mux_out),
  .write_byte_en  (data_array_wben),
  .read_data      (data_array_read_data)
);

//Fourth column of datapath

logic [clw - 1:0] read_data_reg_out;
vc_EnReg#(clw) read_data_reg
(
  .clk    (clk),
  .reset  (reset),
  .q      (read_data_reg_out),
  .d      (data_array_read_data),
  .en     (read_data_reg_en)
);

logic cmp_0_out;
vc_EqComparator#(tgw) cmp_0
(
  .in0 (cachereq_addr_reg_out[31:4]),
  .in1 (tag_array_read_data_0),
  .out (cmp_0_out)
);

logic cmp_1_out;
vc_EqComparator#(tgw) cmp_1
(
  .in0 (cachereq_addr_reg_out[31:4]),
  .in1 (tag_array_read_data_1),
  .out (cmp_1_out)
);

assign tag_match_0 = cmp_0_out;
assign tag_match_1 = cmp_1_out;

//mk_addr_tag_array_0
logic [(abw - 1):0]mk_addr_tag_array_read_data_0;
assign mk_addr_tag_array_read_data_0 = {tag_array_read_data_0, 4'b0000};

//mk_addr_tag_array_1 
logic [(abw - 1):0]mk_addr_tag_array_read_data_1;
assign mk_addr_tag_array_read_data_1 = {tag_array_read_data_1, 4'b0000};
 
//mk_addr cachereq_addr_reg
logic [31:0] mk_addr_cachereq_addr_reg_out;
assign mk_addr_cachereq_addr_reg_out = {mk_addr_cachereq_addr_reg_out[31:4], 4'b0000};

//Fifth column of datapath

logic [(abw - 1):0] evict_addr_reg_out_0;
vc_EnReg#(abw) evict_addr_reg_0
(
  .clk    (clk),
  .reset  (reset),
  .q      (evict_addr_reg_out_0),
  .d      (mk_addr_tag_array_read_data_0),
  .en     (evict_addr_reg_en_0)
);

logic [(abw - 1):0] evict_addr_reg_out_1;
vc_EnReg#(abw) evict_addr_reg_1
(
  .clk    (clk),
  .reset  (reset),
  .q      (evict_addr_reg_out_1),
  .d      (mk_addr_tag_array_read_data_1),
  .en     (evict_addr_reg_en_1)
);

logic [abw-1:0] memreq_addr_mux_out;
vc_Mux3#(abw) memreq_addr_mux 
(
  .in0  (evict_addr_reg_out_0),
  .in1  (evict_addr_reg_out_1),
  .in2  (cachereq_addr_reg_out), 
  .sel  (memreq_addr_mux_sel),
  .out  (memreq_addr_mux_out)
);

logic [(clw/4 -1):0] read_word_mux_out;
vc_Mux5#(clw/4) read_word_mux
(
  //.in0    (read_data_reg_out[clw - 1:clw/4 * 3]),
  //.in1    (read_data_reg_out[(clw/4 * 3 - 1):clw/4 * 2]),
  //.in2    (read_data_reg_out[(clw/4 * 2 - 1):clw/4]),
  //.in3    (read_data_reg_out[(clw/4 - 1):0]),
  //.in4    ('h0),
  .in0    (0), 
  .in1    (read_data_reg_out[(clw/4 - 1):0]),
  .in2    (read_data_reg_out[(clw/4 * 2 - 1):clw/4]),
  .in3    (read_data_reg_out[(clw/4 * 3 - 1):clw/4 * 2]),
  .in4    (read_data_reg_out[clw - 1:clw/4 * 3]),
  .sel    (read_word_mux_sel),
  .out    (read_word_mux_out)
);

//Cacheresp_msg and memreq_msg

//cacheresp_msg
assign cacheresp_msg.opaque = cachereq_opaque_reg_out;
assign cacheresp_msg.type_ = cacheresp_type;
assign cacheresp_msg.len = 2'b00;
assign cacheresp_msg.test = hit;
assign cacheresp_msg.data = read_word_mux_out;
//end cacheresp_msg

//memreq_msg
assign memreq_msg.type_ = memreq_type;
assign memreq_msg.len = 4'b0000;
assign memreq_msg.addr = memreq_addr_mux_out;
assign memreq_msg.data = read_data_reg_out;
assign memreq_msg.opaque = 8'b00000000;
//end memreq_msg'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

endmodule

`endif
