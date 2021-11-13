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

module wben_module (
  input logic   [1:0]   in,
  output logic  [15:0]  out  
);
  always_comb begin
    case (in)
    2'd0 : out = 16'h000F;
    2'd1 : out = 16'h00F0;
    2'd2 : out = 16'h0F00; 
    2'd3 : out = 16'hF000;
    default: out = 0;
    endcase
  end
endmodule 

module read_mux_sel (
  input   logic [1:0] in,
  input   logic       en, 
  input   logic [2:0] cashereq_type,
  output  logic [2:0] out 
);
  always_comb begin
    if (en && cashereq_type == 0) 
      out = in + 1; 
    else 
      out = 0;
  end
endmodule 

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

  input  logic  [2:0]                 cachereq_type, // init = 010, read = 000 
  output logic                        cachereq_en,
  output logic                        memresp_en,
  output logic                        write_data_mux_sel,
  input  logic  [31:0]                cachereq_addr,
  output logic                        tag_array_ren,
  output logic                        tag_array_wen,
  output logic                        data_array_ren,
  output logic                        data_array_wen,
  output logic  [15:0]                data_array_wben,
  output logic                        read_data_reg_en,
  input  logic                        tag_match,
  output logic                        evict_addr_reg_en,
  output logic  [2:0]                 read_word_mux_sel,
  output logic                        memreq_addr_mux_sel,
  output logic  [2:0]                 cacheresp_type,
  output logic  [1:0]                 hit,
  output logic  [2:0]                 memreq_type
  

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
      state_reg <= state_next;
    end
  end

  //----------------------------------------------------------------------
  // DIRTY & VALID BITS
  //----------------------------------------------------------------------

  logic valid_in;
  logic dirty_in;

  logic read_data_dirty;
  logic wen_dirty = 0;

  logic read_data_val;
  logic wen_val = 0;

  vc_Regfile_1r1w#(1,16) dirty
  (
    .clk(clk),
    .reset(reset),
    .read_addr(cachereq_addr[(idw + ofw - 1 + p_idx_shamt):(ofw + p_idx_shamt)]),
    .read_data(read_data_dirty),
    .write_en(wen_dirty),
    .write_addr(cachereq_addr[(idw + ofw - 1 + p_idx_shamt):(ofw + p_idx_shamt)]),
    .write_data(dirty_in)

  );

  vc_Regfile_1r1w#(1,16) valid
  (
    .clk(clk),
    .reset(reset),
    .read_addr(cachereq_addr[(idw + ofw - 1 + p_idx_shamt):(ofw + p_idx_shamt)]),
    .read_data(read_data_val),
    .write_en(wen_val),
    .write_addr(cachereq_addr[(idw + ofw - 1 + p_idx_shamt):(ofw + p_idx_shamt)]),
    .write_data(valid_in)
  );
  logic [1:0] hit_in = {1'b0,tag_match && read_data_val};
  vc_EnReg#(2) hit_reg 
  (
    .clk    (clk),
    .reset  (reset), 
    .q      (hit), 
    .d      (hit_in),
    .en     (hit_en)
  );

  vc_EnReg#(3) cache_type_reg 
  (
    .clk    (clk),
    .reset  (reset),
    .q      (cacheresp_type),
    .d      (cachereq_type),
    .en     (cache_type_en)
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
<<<<<<< HEAD
         if (cachereq_type == 2) state_next = IN;
         else if ((tag_match == 1) && ( cachereq_type == 0) && (read_data_val))  state_next = RD;
         else if ((tag_match == 1) && ( cachereq_type == 1) && (read_data_val))  state_next = WD;
         else if ((tag_match == 0) && ( read_data_dirty == 0) || !(read_data_val)) state_next = RR;
         else if ((tag_match == 0) && ( read_data_dirty == 1)) state_next = EP; 
=======
         if (cachereq_type == 3'b010) state_next = IN;
         else if ((tag_match) && ( cachereq_type == 0) && (read_data_val))  state_next = RD;
         else if ((tag_match) && ( cachereq_type == 1) && (read_data_val))  state_next = WD;
         //else if ((tag_match == 0) && ( read_data_dirty == 0) || !(read_data_val)) state_next = RR;
         //else if ((tag_match == 0) && ( read_data_dirty == 1)) state_next = EP;
         else if ((!(read_data_val) || !(tag_match))  && (read_data_dirty == 0)) state_next = RR; 
         else if ((!(read_data_val) || !(tag_match)) && (read_data_dirty == 1)) state_next = EP; 
>>>>>>> 088755c8e67a90bd2bbe49e943c5058299017264
       end

       IN: begin
         wen_val = 1;
         state_next = W;
       end  

       W: begin
        if (cacheresp_rdy) state_next = I;
        else if (!cacheresp_rdy) begin
          state_next = W;
          end
        end
       
       RD: state_next = W;

       WD: begin 
         if (tag_match == 1) begin
           wen_dirty = 1;
           wen_val = 1;
         end
         state_next = W;
       end         

       RR: begin
         if (!memreq_rdy) state_next = RR;
         else if (memreq_rdy) state_next = RW;
       end

      RW: begin
        if (!memresp_val) state_next = RW;
        else if (memresp_val) state_next = RU;
      end

      RU: begin
        if (cachereq_type == 0) state_next = RD;
        else if (cachereq_type == 1) state_next = WD;
      end
 
      EP: state_next = ER;

      ER: begin
        if (!memreq_rdy) state_next = ER;
        else if (memreq_rdy) state_next = EW;
      end

      EW: begin
        if (!memresp_val) state_next = EW;
        else if (memresp_val) state_next = RR;
      end

     default: state_next = I;

     endcase
    end
  //----------------------------------------------------------------------
  // OUTPUT ( CONTROL SIGNAL TABLE ) 
  //----------------------------------------------------------------------
  //Wben Signal 
  localparam write_all = 16'hFFFF;
  logic hit_en;
  logic cache_type_en;
  logic read_word_mux_sel_en; 
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
   input [15:0] cs_data_array_wben,
   input cs_read_data_reg_en,
   input cs_evict_addr_reg_en,
   input cs_read_word_mux_sel_en,
   input cs_memreq_addr_mux_sel,
   input cs_cache_type_en,
   input cs_hit_en,
   input [2:0] cs_memreq_type,
   input cs_dirty_in,
   input cs_valid_in,
   input cs_wen_val,
   input cs_wen_dirty,
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
   read_word_mux_sel_en = cs_read_word_mux_sel_en;
   memreq_addr_mux_sel = cs_memreq_addr_mux_sel;
   cache_type_en = cs_cache_type_en;
   hit_en = cs_hit_en;
   memreq_type = cs_memreq_type;
   dirty_in = cs_dirty_in;
   valid_in = cs_valid_in;
   wen_val = cs_wen_val;
   wen_dirty = cs_wen_dirty;  
   
  end
  endtask
  
  logic [15:0] wben; 
  wben_module wben_module 
  (
    .in(cachereq_addr[ofw-1:2]),
    .out(wben)
  );

  read_mux_sel read_mux_sel 
  (
    .in(cachereq_addr[ofw-1:2]),
    .cashereq_type(cacheresp_type), 
    .en(read_word_mux_sel_en),
    .out(read_word_mux_sel)
  );



always_comb begin
 case(state_reg)
<<<<<<< HEAD
     //cachereq  cacheresp  memreq memresp  cachereq memresp write_data  tag_arr  tag_arr data_array data_arr data_arr  read_data  evict_addr  read_word  memreq  cacheresp  hit memreq   dirty  valid   wen_   wen_
    //rdy       val        val    rdy      en       en      mux_sel     ren      wen     ren        wen      wben      reg_en     reg_en      mux_sel  addr_mux  type           type      in      in      val  dirty
  I: cs(1,    0,         0,      0,       1,       0,      1'bx,        0,        0,       0,      0,          0,       0,       0,         3'dx,     1'dx,         3'bx,   hit, 3'bx,    1'bx,  1'bx,    0,  0  );
  TC:cs(0,    0,         0,      0,       0,       0,      1'bx,        1,        0,       0,      0,          0,    	0,       0,         3'dx,      1'dx,         3'bx,   hit, 3'bx,     1'bx,  1'bx,    0,  0  );
  IN:cs(0,    1,         0,      0,       0,       0,      1'b0,        0,        1,       0,      0,          1,    	1,       0,         3'd1,      1'dx,         3'd2,   hit, 3'bx,     1'bx,  1'bx,    0,  0  );
  WD:cs(0,    0,         0,      0,       1,       0,      1'b0,        0,        0,       0,      1,         0,      0,       0,         3'dx,      1'd1,         3'bx,   hit, 3'd1,     1,     1,       1,  1  );  
  RD:cs(0,    1,         0,      0,       1,       1,      1'b0,        0,        0,       1,      0,          0,    	1,       0,         3'd1,    1'd0,             3'bx, hit, 3'd0,     1'bx,  1'bx,    0,  0  );
  RR:cs(0,    0,         1,      0,       0,       1,      1'b0,        0,        0,       0,      0,          0,    	0,       0,         3'dx,      1,           3'd0,    hit, 3'd0,     1'bx,  1'bx,    0,  0  );
  RW:cs(0,    0,         0,      1,       1,       0,      1'bx,        0,        0,       0,      0,          0,    	0,       0,         3'dx,      0,           3'd0,    hit, 3'd0,     1'bx,  1'bx,    0,  0  );
  RU:cs(0,    1,         0,      1,       1,       1,      1'b1,        0,        1,       0,      0,          1,    	0,       0,         3'dx,     1'd0,            3'bx, hit, 3'd1,     0,     1,       1,  0  );
  EP:cs(0,    0,         0,      0,       1,       0,      1'bx,        1,        0,       1,      0,          0,    	0,       1,         3'dx,    0,          3'dx,       hit, 3'bx,     1'bx,  1'bx,    0,  0  );
  ER:cs(0,    0,         1,      0,       0,       0,      1'bx,        0,        0,       0,      0,          0,    	0,       1,         3'd0,   0,           3'dx,       hit, 3'bx,     1'bx,  1'bx,    0,  0  );    
  EW:cs(0,    0,         0,      1,       1,       0,      1'bx,        0,        0,       0,      0,        0,    	0,       0,         3'bx,     1'bx,         3'dx,      hit, 3'bx,     1'bx,  1'bx,    0,  0  );
  W: cs(0,    0,         0,      0,       0,       0,      1'bx,        0,        0,       0,      0,          0,    	0,       0,       3'bx,     1'dx,         3'dx,      hit, 3'bx,     1'bx,  1'bx,    0,  0  ); 
  default: cs( 0, 0,       0,      0,       0,      0,       1'bx,        0,        0,       0,      0,         0,      0,       0,       3'bx,     1'dx,         3'dx,    hit, 3'bx,     1'bx,  1'bx,    0,  0 );
  endcase
=======
     //cachereq  cacheresp  memreq memresp  cachereq memresp write_data  tag_arr  tag_arr data_array data_arr data_arr    read_data  evict_addr  read_word    memreq    cacheresp hit_en  memreq  dirty   valid   wen_  wen_
     //rdy       val        val    rdy      en       en      mux_sel     ren      wen     ren        wen      wben        reg_en     reg_en      mux_sel_en   addr_mux  type_en           type    in      in      val   dirty
  I: cs(1,       0,         0,     0,       1,       0,      1'bx,       0,       0,      0,         0,       0,          0,         0,          0,           1'dx,     0,        0,      3'bx,   1'bx,   1'bx,   0,    0  );
  TC:cs(0,       0,         0,     0,       0,       0,      1'bx,       1,       0,      0,         0,       0,    	    0,         0,          0,           1'dx,     1,        1,      3'bx,   1'bx,   1'bx,   0,    0  );
  IN:cs(0,       0,         0,     0,       0,       0,      1'b0,       0,       1,      0,         1,       wben,    	  1,         0,          0,           1'dx,     0,        0,      3'bx,   1'bx,   1,      1,    0  );
  WD:cs(0,       0,         0,     0,       0,       0,      1'b0,       0,       0,      0,         1,       wben,       0,         0,          0,           1'd1,     0,        0,      3'd1,   1,      1,      1,    1  );  
  RD:cs(0,       0,         0,     0,       0,       0,      1'b0,       0,       0,      1,         0,       0,    	    1,         0,          0,           1'd0,     0,        0,      3'd0,   1'bx,   1'bx,   0,    0  );
  RR:cs(0,       0,         1,     0,       0,       0,      1'b0,       0,       0,      0,         0,       0,    	    0,         0,          0,           1,        0,        0,      3'd0,   1'bx,   1'bx,   0,    0  );
  RW:cs(0,       0,         0,     1,       0,       1,      1'bx,       0,       0,      0,         0,       0,    	    0,         0,          0,           0,        0,        0,      3'd0,   1'bx,   1'bx,   0,    0  );
  RU:cs(0,       0,         0,     0,       0,       0,      1'b1,       0,       1,      0,         1,       write_all,  0,         0,          0,           1'd0,     0,        0,      3'd1,   0,      1,      1,    0  );
  EP:cs(0,       0,         0,     0,       0,       0,      1'bx,       1,       0,      1,         0,       0,    	    0,         1,          0,           0,        0,        0,      3'bx,   1'bx,   1'bx,   0,    0  );
  ER:cs(0,       0,         1,     0,       0,       0,      1'bx,       0,       0,      0,         0,       0,    	    0,         1,          0,           0,        0,        0,      3'bx,   1'bx,   1'bx,   0,    0  );    
  EW:cs(0,       0,         0,     0,       0,       0,      1'bx,       0,       0,      0,         0,       0,    	    0,         0,          0,           1'bx,     0,        0,      3'bx,   1'bx,   1'bx,   0,    0  );
  W: cs(0,       1,         0,     0,       0,       0,      1'bx,       0,       0,      0,         0,       0,    	    0,         0,          1,           1'dx,     0,        0,      3'bx,   1'bx,   1'bx,   0,    0  ); 
  default: cs( 0,0,         0,     0,       0,       0,      1'bx,       0,       0,      0,         0,       0,          0,         0,          0,           1'dx,     0,        0,      3'bx,   1'bx,   1'bx,   0,    0  );
  endcase   
>>>>>>> 088755c8e67a90bd2bbe49e943c5058299017264
end















endmodule

`endif
