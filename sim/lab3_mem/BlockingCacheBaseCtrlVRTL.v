//=========================================================================
// Baseline Blocking Cache Control
//=========================================================================

`ifndef LAB3_MEM_BLOCKING_CACHE_BASE_CTRL_V
`define LAB3_MEM_BLOCKING_CACHE_BASE_CTRL_V

`include "vc/mem-msgs.v"
`include "vc/assert.v"
`include "vc/regfiles.v"
//''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
// LAB TASK: Include necessary files
//''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

module lab3_mem_BlockingCacheBaseCtrlVRTL
#(
  parameter p_idx_shamt    = 0
)
(
  input  logic                        clk,
  input  logic                        reset,

  // Cache Request

  input  logic                        cachereq_val,
  output logic                        cachereq_rdy,

  // Cache Response

  output logic                        cacheresp_val,
  input  logic                        cacheresp_rdy,

  // Memory Request

  output logic                        memreq_val,
  input  logic                        memreq_rdy,

  // Memory Response

  input  logic                        memresp_val,
  output logic                        memresp_rdy,

  input  logic                        cachereq_type,
  output logic                       cachereq_en,
  output logic                       memresp_en,
  output logic                       write_data_mux_sel,
  input  logic                        cachereq_addr,
  output logic                       tag_array_ren,
  output logic                       tag_array_wen,
  output logic                       data_array_ren,
  output logic                       data_array_wen,
  output logic                       data_array_wben,
  output logic                       read_data_reg_en,
  input  logic                        tag_match,
  output logic                       evict_addr_reg_en,
  output logic                       read_word_mux_sel,
  output logic                       memreq_addr_mux_sel,
  output logic                       cacheresp_type,
  output logic                       hit,
  output logic                       memreq_type
  

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


  // muxsel signals
  localparam mux_x = 2'bx;
  localparam mux_zero = 2'b0;
  localparam mux_one = 2'b1;
  localparam mux_two = 2'b10;
  localparam mux_three = 2'b11;



  //----------------------------------------------------------------------
  // STATE DEFINITIONS
  //----------------------------------------------------------------------

  localparam I = 4'd0;  // STATE_IDLE
  localparam TC = 4'd1; // STATE_TAG_CHECK
  localparam IN = 4'd2; // STATE_INIT_DATA_ACCESS
  localparam RD = 4'd3; // STATE_READ_DATA_ACCESS
  localparam WD = 4'd4; // STATE_WRITE_DATA_ACCESS
  localparam EP = 4'd5; // STATE_EVICT_PREPARE
  localparam ER = 4'd6; // STATE_EVICT_REQUEST
  localparam EW = 4'd7; // STATE_EVICT_wAIT
  localparam RR = 4'd8; // STATE_REFILL_REQUEST
  localparam RW = 4'd9; // STATE_REFILL_WAIT
  localparam RU = 4'd10;// STATE_REFILL_UPDATE
  localparam W  = 4'd11;// STATE_WAIT

  //----------------------------------------------------------------------
  // STATE
  //----------------------------------------------------------------------

  logic [3:0] state_reg;
  logic [3:0] state_next;

  always_ff@(posedge clk) begin
    if (reset == 1) begin
      state_reg <= I;
    end
    else begin
      state_next <= state_reg;
    end
  end

  //----------------------------------------------------------------------
  // DIRTY & VALID BITS
  //----------------------------------------------------------------------

  logic read_data_dirty;
  logic wen_dirty = 0;

  logic read_data_val;
  logic wen_val = 0;

  vc_Regfile_1r1w#(1,16) dirty
  (
    .clk(clk),
    .reset(reset),
    .read_addr(cachereq_addr[7:4]),
    .read_data(read_data_dirty),
    .write_en(wen_dirty),
    .write_addr(cachereq_addr[7:4]),
    .write_data(cachereq_addr[31:4])

  );

  vc_Regfile_1r1w#(1,16) valid
  (
    .clk(clk),
    .reset(reset),
    .read_addr(cachereq_addr[7:4]),
    .read_data(read_data_val),
    .write_en(wen_val),
    .write_addr(cachereq_addr[7:4]),
    .write_data(cachereq_addr[31:4])
  );

  //----------------------------------------------------------------------
  // STATE TRANSITIONS
  //----------------------------------------------------------------------

  // Variables for "goto state" signals

  localparam init_trans = 1'd1;
  logic idle = !(cachereq_val); // go to idle state
  //logic go_tc; // go to tag check


  always_comb begin

    state_next = state_reg;
 
    case (state_reg)

       I: begin 
         if (!idle) state_next = TC;
       end

       TC: begin 
         if (init_trans) state_next = IN;
         else if ((tag_match == 1) && ( cachereq_type == 0) && (read_data_val))  state_next = RD;
         else if ((tag_match == 1) && ( cachereq_type == 1) && (read_data_val))  state_next = WD;
         else if ((tag_match == 0) && ( read_data_dirty == 0) || !(read_data_val)) state_next = RR;
         else if ((tag_match == 0) && ( read_data_dirty == 1)) state_next = EP; 
       end

       IN: begin
         wen_valid = 1;
         state_next = W;
       end  

       W: begin
        if (cacheresp_rdy) state_next = I;
        else begin
          state_next = W;
          end
        end
       
       RD: state_next = W;

       WD: begin 
         if (tag_match == 1) begin
           wen_dirty = 1;
           wen_valid = 1;
         end
         state_next = W;
       end         

       RR: begin
         if (!memreq_rdy) state_next = RR;
         else state_next = RW;
       end

      RW: begin
        if (!memresp_val) state_next = RW;
        else state_next = RU;
      end

      RU: begin
        if (cachereq_type == 0) state_next = RD;
        else state_next = WD;
      end
 
      EP: state_next = ER;

      ER: begin
        if (!memreq_rdy) state_next = ER;
        else state_next = EW;
      end

      EW: begin
        if (!memresp_val) state_next = EW;
        else state_next = RR;
      end

     endcase
    end
  //----------------------------------------------------------------------
  // OUTPUT ( CONTROL SIGNAL TABLE ) 
  //----------------------------------------------------------------------

  task cs
  (
   input cs_cachereq_rdy,
   input cs_cacheresp_val,
   input cs_memreq_val,
   input cs_memresp_rdy,
   input cs_cachereq_en,
   input cs_memresp_en,
   input cs_write_data_mux_sel,
   input cs_tag_array_ren,
   input cs_tag_array_wen,
   input cs_data_array_ren,
   input cs_data_array_wen,
   input cs_data_array_wben,
   input cs_read_data_reg_en,
   input cs_evict_addr_reg_en,
   input cs_read_word_mux_sel,
   input cs_memreq_addr_mux_sel,
   input cs_cacheresp_type,
   input cs_hit,
   input cs_memreq_type
  );
  begin
   cachereq_rdy = cs_cachereq_rdy;
   cacheresp_val = cs_cacheresp_val;
   memreq_val = cs_memreq_val;
   memresp_rdy = cs_memresp_rdy;
   cachereq_en = cs_cachereq_en;
   memresp_en = cs_memresp_en;
   write_data_mux_sel = cs_write_data_mux_sel;
   tag_array_ren = cs_tag_array_ren;
   tag_array_wen = cs_tag_array_wen;
   data_array_ren = cs_data_array_ren;
   data_array_wen = cs_data_array_wen;
   data_array_wben = cs_data_array_wben;
   read_data_reg_en = cs_read_data_reg_en;
   evict_addr_reg_en = cs_evict_addr_reg_en;
   read_word_mux_sel = cs_read_word_mux_sel;
   memreq_addr_mux_sel = cs_memreq_addr_mux_sel;
   cacheresp_type = cs_cacheresp_type;
   hit = cs_hit;
   memreq_type = cs_memreq_type;
  end
  endtask

  assign hit = tag_match && read_data_val;

  always_comb begin
   case(state_reg)
      //cachereq  cacheresp  memreq memresp  cachereq memresp write_data  tag_arr  tag_arr data_array  data_arr  read_data  evict_addr  read_word  cacheresp hit memreq
      //rdy       val        val    rdy      en       en      mux_sel     ren      wen     ren         wben      reg_en     reg_en      mux_sel    type          type
    I: cs(  1,    0,         0,      0,       0,       0,       1'bx,       0,        0,       0,          0,          0,       0,         mux_x,      1'bx,     1'bx,  1'bx);
    TC:cs(  0,    0,         0,      0,       1,       0,      1'bx,        1,        0,       0,          0,          0,       0,         mux_x,      1'bx,      hit,   1'bx);
    IN:cs(  0,    1,         0,      0,       1,       0,      mux_zero,    0,        1,       0,          1,          1,       0,        mux_one,   c_write_init, hit, 1'bx);     
    RD:cs(  0,    1,         0,      0,       1,       1,      mux_zero,    0,        0,       1,          0,          1,       0,        mux_one,     0,         hit,  0);
    RR:cs(  0,    0,         1,      0,       0,       1,      mux_one,     0,        0,       0,          0,          0,       0,        mux_x,        0,        hit,   0);
    RW:cs(  0,    0,         0,      1,       1,       0,      1'bx,        0,        0,       0,          0,          0,       0,        mux_x,         0,        hit,   0);
    RU:cs(  0,    1,         0,      1,       1,       1,      mux_one,     0,        1,       0,          1,          0,       0,         mux_x,        1,        hit,   1);
    EP:cs(  0,    0,         0,      0,       1,       0,      1'bx,        1,        0,       1,          0,          0,       1,          mux_zero,    1'bx,      hit,   1'bx);
    ER:cs(  0,    0,         1,      0,       0,       0,      1'bx,        0,        0,       0,          0,          0,       1,         mux_zero,     1'bx,      hit, 1'bx);     
    EW:cs(  0,    0,         0,      1,       1,       0,      1'bx,        0,        0,       0,          0,          0,       0,         mux_x,         1'bx,      hit,  1'bx);
    W: cs(  0,    0,         0,      0,       0,       0,      mux_x,        0,        0,       0,          0,          0,       0,         mux_x,    1'bx,    hit,    1'bx); 
    endcase
  end















endmodule

`endif
