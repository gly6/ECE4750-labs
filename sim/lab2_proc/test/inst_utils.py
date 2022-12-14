#=========================================================================
# inst_utils
#=========================================================================
# Includes helper functions to simplify creating assembly tests.

from pymtl import *

#-------------------------------------------------------------------------
# print_asm
#-------------------------------------------------------------------------
# Pretty print a generated assembly syntax

def print_asm( asm_code ):

  # If asm_code is a single string, then put it in a list to simplify the
  # rest of the logic.

  asm_code_list = asm_code
  if isinstance( asm_code, str ):
    asm_code_list = [ asm_code ]

  # Create a single list of lines

  asm_list = []
  for asm_seq in asm_code_list:
    asm_list.extend( asm_seq.splitlines() )

  # Print the assembly. Remove duplicate blank lines.

  prev_blank_line = False
  for asm in asm_list:
    if asm.strip() == "":
      if not prev_blank_line:
        print asm
        prev_blank_line = True
    else:
      prev_blank_line = False
      print asm

#-------------------------------------------------------------------------
# gen_nops
#-------------------------------------------------------------------------

def gen_nops( num_nops ):
  if num_nops > 0:
    return "nop\n" + ("    nop\n"*(num_nops-1))
  else:
    return ""

#-------------------------------------------------------------------------
# gen_word_data
#-------------------------------------------------------------------------

def gen_word_data( data_list ):

  data_str = ".data\n"
  for data in data_list:
    data_str += ".word {}\n".format(data)

  return data_str

#-------------------------------------------------------------------------
# gen_hword_data
#-------------------------------------------------------------------------

def gen_hword_data( data_list ):

  data_str = ".data\n"
  for data in data_list:
    data_str += ".hword {}\n".format(data)

  return data_str

#-------------------------------------------------------------------------
# gen_byte_data
#-------------------------------------------------------------------------

def gen_byte_data( data_list ):

  data_str = ".data\n"
  for data in data_list:
    data_str += ".byte {}\n".format(data)

  return data_str

#-------------------------------------------------------------------------
# gen_rr_src01_template
#-------------------------------------------------------------------------
# Template for register-register instructions. We first write src0
# register and then write the src1 register before executing the
# instruction under test. We parameterize the number of nops after
# writing both src registers and the instruction under test to enable
# using this template for testing various bypass paths. We also
# parameterize the register specifiers to enable using this template to
# test situations where the srce registers are equal and/or equal the
# destination register.

def gen_rr_src01_template(
  num_nops_src0, num_nops_src1, num_nops_dest,
  reg_src0, reg_src1,
  inst, src0, src1, result
):
  return """

    # Move src0 value into register
    csrr {reg_src0}, mngr2proc < {src0}
    {nops_src0}

    # Move src1 value into register
    csrr {reg_src1}, mngr2proc < {src1}
    {nops_src1}

    # Instruction under test
    {inst} x3, {reg_src0}, {reg_src1}
    {nops_dest}

    # Check the result
    csrw proc2mngr, x3 > {result}

  """.format(
    nops_src0 = gen_nops(num_nops_src0),
    nops_src1 = gen_nops(num_nops_src1),
    nops_dest = gen_nops(num_nops_dest),
    **locals()
  )

#-------------------------------------------------------------------------
# gen_rr_src10_template
#-------------------------------------------------------------------------
# Similar to the above template, except that we reverse the order in
# which we write the two src registers.

def gen_rr_src10_template(
  num_nops_src0, num_nops_src1, num_nops_dest,
  reg_src0, reg_src1,
  inst, src0, src1, result
):
  return """

    # Move src1 value into register
    csrr {reg_src1}, mngr2proc < {src1}
    {nops_src1}

    # Move src0 value into register
    csrr {reg_src0}, mngr2proc < {src0}
    {nops_src0}

    # Instruction under test
    {inst} x3, {reg_src0}, {reg_src1}
    {nops_dest}

    # Check the result
    csrw proc2mngr, x3 > {result}

  """.format(
    nops_src0 = gen_nops(num_nops_src0),
    nops_src1 = gen_nops(num_nops_src1),
    nops_dest = gen_nops(num_nops_dest),
    **locals()
  )

#-------------------------------------------------------------------------
# gen_rr_dest_dep_test
#-------------------------------------------------------------------------
# Test the destination bypass path by varying how many nops are
# inserted between the instruction under test and reading the destination
# register with a csrr instruction.

def gen_rr_dest_dep_test( num_nops, inst, src0, src1, result ):
  return gen_rr_src01_template( 0, 8, num_nops, "x1", "x2",
                                inst, src0, src1, result )

#-------------------------------------------------------------------------
# gen_rr_src1_dep_test
#-------------------------------------------------------------------------
# Test the source 1 bypass paths by varying how many nops are inserted
# between writing the src1 register and reading this register in the
# instruction under test.

def gen_rr_src1_dep_test( num_nops, inst, src0, src1, result ):
  return gen_rr_src01_template( 8-num_nops, num_nops, 0, "x1", "x2",
                                inst, src0, src1, result )

#-------------------------------------------------------------------------
# gen_rr_src0_dep_test
#-------------------------------------------------------------------------
# Test the source 0 bypass paths by varying how many nops are inserted
# between writing the src0 register and reading this register in the
# instruction under test.

def gen_rr_src0_dep_test( num_nops, inst, src0, src1, result ):
  return gen_rr_src10_template( num_nops, 8-num_nops, 0, "x1", "x2",
                                inst, src0, src1, result )

#-------------------------------------------------------------------------
# gen_rr_srcs_dep_test
#-------------------------------------------------------------------------
# Test both source bypass paths at the same time by varying how many nops
# are inserted between writing both src registers and reading both
# registers in the instruction under test.

def gen_rr_srcs_dep_test( num_nops, inst, src0, src1, result ):
  return gen_rr_src01_template( 0, num_nops, 0, "x1", "x2",
                                inst, src0, src1, result )

#-------------------------------------------------------------------------
# gen_rr_src0_eq_dest_test
#-------------------------------------------------------------------------
# Test situation where the src0 register specifier is the same as the
# destination register specifier.

def gen_rr_src0_eq_dest_test( inst, src0, src1, result ):
  return gen_rr_src01_template( 0, 0, 0, "x3", "x2",
                                inst, src0, src1, result )

#-------------------------------------------------------------------------
# gen_rr_src1_eq_dest_test
#-------------------------------------------------------------------------
# Test situation where the src1 register specifier is the same as the
# destination register specifier.

def gen_rr_src1_eq_dest_test( inst, src0, src1, result ):
  return gen_rr_src01_template( 0, 0, 0, "x1", "x3",
                                inst, src0, src1, result )

#-------------------------------------------------------------------------
# gen_rr_src0_eq_src1_test
#-------------------------------------------------------------------------
# Test situation where the src register specifiers are the same.

def gen_rr_src0_eq_src1_test( inst, src, result ):
  return gen_rr_src01_template( 0, 0, 0, "x1", "x1",
                                inst, src, src, result )

#-------------------------------------------------------------------------
# gen_rr_srcs_eq_dest_test
#-------------------------------------------------------------------------
# Test situation where all three register specifiers are the same.

def gen_rr_srcs_eq_dest_test( inst, src, result ):
  return gen_rr_src01_template( 0, 0, 0, "x3", "x3",
                                inst, src, src, result )

#-------------------------------------------------------------------------
# gen_rr_value_test
#-------------------------------------------------------------------------
# Test the actual operation of a register-register instruction under
# test. We assume that bypassing has already been tested.

def gen_rr_value_test( inst, src0, src1, result ):
  return gen_rr_src01_template( 0, 0, 0, "x1", "x2",
                                inst, src0, src1, result )

#-------------------------------------------------------------------------
# gen_rimm_template
#-------------------------------------------------------------------------
# Template for register-immediate instructions. We first write the src
# register before executing the instruction under test. We parameterize
# the number of nops after writing the src register and the instruction
# under test to enable using this template for testing various bypass
# paths. We also parameterize the register specifiers to enable using
# this template to test situations where the srce registers are equal
# and/or equal the destination register.

def gen_rimm_template(
  num_nops_src, num_nops_dest,
  reg_src,
  inst, src, imm, result
):
  return """

    # Move src value into register
    csrr {reg_src}, mngr2proc < {src}
    {nops_src}

    # Instruction under test
    {inst} x3, {reg_src}, {imm}
    {nops_dest}

    # Check the result
    csrw proc2mngr, x3 > {result}

  """.format(
    nops_src  = gen_nops(num_nops_src),
    nops_dest = gen_nops(num_nops_dest),
    **locals()
  )

#-------------------------------------------------------------------------
# gen_rimm_dest_dep_test
#-------------------------------------------------------------------------
# Test the destination bypass path by varying how many nops are
# inserted between the instruction under test and reading the destination
# register with a csrr instruction.

def gen_rimm_dest_dep_test( num_nops, inst, src, imm, result ):
  return gen_rimm_template( 8, num_nops, "x1",
                            inst, src, imm, result )

#-------------------------------------------------------------------------
# gen_rimm_src_dep_test
#-------------------------------------------------------------------------
# Test the source bypass paths by varying how many nops are inserted
# between writing the src register and reading this register in the
# instruction under test.

def gen_rimm_src_dep_test( num_nops, inst, src, imm, result ):
  return gen_rimm_template( num_nops, 0, "x1",
                            inst, src, imm, result )

#-------------------------------------------------------------------------
# gen_rimm_src_eq_dest_test
#-------------------------------------------------------------------------
# Test situation where the src register specifier is the same as the
# destination register specifier.

def gen_rimm_src_eq_dest_test( inst, src, imm, result ):
  return gen_rimm_template( 0, 0, "x3",
                            inst, src, imm, result )

#-------------------------------------------------------------------------
# gen_rimm_value_test
#-------------------------------------------------------------------------
# Test the actual operation of a register-immediate instruction under
# test. We assume that bypassing has already been tested.

def gen_rimm_value_test( inst, src, imm, result ):
  return gen_rimm_template( 0, 0, "x1",
                            inst, src, imm, result )

#-------------------------------------------------------------------------
# gen_imm_template
#-------------------------------------------------------------------------
# Template for immediate instructions. We parameterize the number of nops
# after the instruction under test to enable using this template for
# testing various bypass paths.

def gen_imm_template( num_nops_dest, inst, imm, result ):
  return """

    # Instruction under test
    {inst} x3, {imm}
    {nops_dest}

    # Check the result
    csrw proc2mngr, x3 > {result}

  """.format(
    nops_dest = gen_nops(num_nops_dest),
    **locals()
  )

#-------------------------------------------------------------------------
# gen_imm_dest_dep_test
#-------------------------------------------------------------------------
# Test the destination bypass path by varying how many nops are
# inserted between the instruction under test and reading the destination
# register with a csrr instruction.

def gen_imm_dest_dep_test( num_nops, inst, imm, result ):
  return gen_imm_template( num_nops, inst, imm, result )

#-------------------------------------------------------------------------
# gen_imm_value_test
#-------------------------------------------------------------------------
# Test the actual operation of an immediate instruction under test. We
# assume that bypassing has already been tested.

def gen_imm_value_test( inst, imm, result ):
  return gen_imm_template( 0, inst, imm, result )

#-------------------------------------------------------------------------
# gen_jal_template
#-------------------------------------------------------------------------
gen_jal_template_id = 0

def gen_jal_dest_dep_test(num_nop_a, link_addr):

    # Create unique labels

    global gen_jal_template_id
    id_a = "label_{}".format( gen_jal_template_id + 1 )
    #id_b = "label_{}".format( gen_jal_template_id + 2 )
    #id_c = "label_{}".format( gen_jal_template_id + 3 )
    gen_jal_template_id += 3

    return """

    # Use r3 to track the control flow pattern
    addi  x3, x0, 0x000     # 0x0200
    jal   x1, {id_a}   # 0x0200 + nops_a * 4
    addi  x3, x3, 0b01  # 0x0228
    {nops_a}

  {id_a}:
    addi  x3, x3, 0b010

    # Check the link address
    csrw  proc2mngr, x1 > {link}

    # Only the second bit should be set if jump was taken
    csrw  proc2mngr, x3 > 0b010

  """.format(  
    nops_a = gen_nops(num_nop_a),    
    link = str(hex(link_addr)),
    #nops_b  = gen_nops(num_nop_b),
    #link = str(hex(0x0208 + (num_nop_a * 4))),
    #link = str(hex(0x0200 + (test_number * 0x38))),
    **locals()
  )

#-------------------------------------------------------------------------
# gen_jal_base_dep_test
#-------------------------------------------------------------------------
# Test the base register bypass paths by varying how many nops are
# inserted between writing the base register and reading this register in
# the instruction under test.

def gen_jal_base_dep_test( num_nops, link_addr ):
  return gen_jal_dest_dep_test( num_nops, link_addr)

#-------------------------------------------------------------------------
# gen_jalr_template
#-------------------------------------------------------------------------
gen_jalr_template_id = 0

def gen_jalr_template(num_nop_a, num_nop_b, link_addr):

    # Create unique labels

    global gen_jalr_template_id
    id_a = "label_{}".format( gen_jalr_template_id + 1 )
    #id_b = "label_{}".format( gen_jal_template_id + 2 )
    #id_c = "label_{}".format( gen_jal_template_id + 3 )
    gen_jalr_template_id += 3
    return """

    # Use r3 to track the control flow pattern
    addi  x3, x0, 0           # 0x0200
                              #
    lui x1,      %hi[{id_a}] # 0x0204
    addi x1, x1, %lo[{id_a}] # 0x0208
                              #
    {nops_a}
                              #
    jalr  x31, x1, 0          # 0x022c
    addi  x3, x3, 0b01        # 0x0230

    {nops_b}

  {id_a}:
    addi  x3, x3, 0b10

    # Check the link address
    csrw  proc2mngr, x31 > {link}

    # Only the second bit should be set if jump was taken
    csrw  proc2mngr, x3  > 0b10

  """.format(  
    nops_a = gen_nops(num_nop_a),    
    nops_b = gen_nops(num_nop_b), 
    link = str(hex(link_addr)),
    #nops_b  = gen_nops(num_nop_b),
    #link = str(hex(0x0208 + (num_nop_a * 4))),
    #link = str(hex(0x0200 + (test_number * 0x38))),
    **locals()
  )

#-------------------------------------------------------------------------
# gen_jalr_base_dep_test
#-------------------------------------------------------------------------
# Test the base register bypass paths by varying how many nops are
# inserted between writing the base register and reading this register in
# the instruction under test.

def gen_jalr_base_dep_test( num_nops_a, num_nops_b, link_addr ):
  return gen_jalr_template( num_nops_a, num_nops_b, link_addr)

#-------------------------------------------------------------------------
# gen_br2_template
#-------------------------------------------------------------------------
# Template for branch instructions with two sources. We test two forward
# branches and one backwards branch. The way we actually do the test is
# we update a register to reflect the control flow; certain bits in this
# register are set at different points in the program. Then we can check
# the control flow bits at the end to see if only the bits we expect are
# set (i.e., the program only executed those points that we expect). Note
# that test also makes sure that the instruction in the branch delay slot
# is _not_ executed.

# We currently need the id to create labels unique to this test. We might
# eventually allow local labels (e.g., 1f, 1b) as in gas.

gen_br2_template_id = 0

def gen_br2_template(
  num_nops_src0, num_nops_src1,
  reg_src0, reg_src1,
  inst, src0, src1, taken
):

  # Determine the expected control flow pattern

  if taken:
    control_flow_pattern = 0b101010
  else:
    control_flow_pattern = 0b111111

  # Create unique labels

  global gen_br2_template_id
  id_a = "label_{}".format( gen_br2_template_id + 1 )
  id_b = "label_{}".format( gen_br2_template_id + 2 )
  id_c = "label_{}".format( gen_br2_template_id + 3 )
  gen_br2_template_id += 3

  return """

    # x3 will track the control flow pattern
    addi   x3, x0, 0

    # Move src0 value into register
    csrr   {reg_src0}, mngr2proc < {src0}
    {nops_src0}

    # Move src1 value into register
    csrr   {reg_src1}, mngr2proc < {src1}
    {nops_src1}

    {inst} {reg_src0}, {reg_src1}, {id_a}  # br -.
    addi   x3, x3, 0b000001                #     |
                                           #     |
{id_b}:                                    # <---+-.
    addi   x3, x3, 0b000010                #     | |
                                           #     | |
    {inst} {reg_src0}, {reg_src1}, {id_c}  # br -+-+-.
    addi   x3, x3, 0b000100                #     | | |
                                           #     | | |
{id_a}:                                    # <---' | |
    addi   x3, x3, 0b001000                #       | |
                                           #       | |
    {inst} {reg_src0}, {reg_src1}, {id_b}  # br ---' |
    addi   x3, x3, 0b010000                #         |
                                           #         |
{id_c}:                                    # <-------'
    addi   x3, x3, 0b100000                #

    # Check the control flow pattern
    csrw   proc2mngr, x3 > {control_flow_pattern}

  """.format(
    nops_src0 = gen_nops(num_nops_src0),
    nops_src1 = gen_nops(num_nops_src1),
    **locals()
  )

#-------------------------------------------------------------------------
# gen_br2_src1_dep_test
#-------------------------------------------------------------------------
# Test the source 1 bypass paths by varying how many nops are inserted
# between writing the src1 register and reading this register in the
# instruction under test.

def gen_br2_src1_dep_test( num_nops, inst, src0, src1, taken ):
  return gen_br2_template( 8-num_nops, num_nops, "x1", "x2",
                           inst, src0, src1, taken )

#-------------------------------------------------------------------------
# gen_br2_src0_dep_test
#-------------------------------------------------------------------------
# Test the source 0 bypass paths by varying how many nops are inserted
# between writing the src0 register and reading this register in the
# instruction under test.

def gen_br2_src0_dep_test( num_nops, inst, src0, src1, result ):
  return gen_br2_template( num_nops, 0, "x1", "x2",
                           inst, src0, src1, result )

#-------------------------------------------------------------------------
# gen_br2_srcs_dep_test
#-------------------------------------------------------------------------
# Test both source bypass paths at the same time by varying how many nops
# are inserted between writing both src registers and reading both
# registers in the instruction under test.

def gen_br2_srcs_dep_test( num_nops, inst, src0, src1, result ):
  return gen_br2_template( 0, num_nops, "x1", "x2",
                           inst, src0, src1, result )

#-------------------------------------------------------------------------
# gen_br2_src0_eq_src1_test
#-------------------------------------------------------------------------
# Test situation where the src register specifiers are the same.

def gen_br2_src0_eq_src1_test( inst, src, result ):
  return gen_br2_template( 0, 0, "x1", "x1",
                                 inst, src, src, result )

#-------------------------------------------------------------------------
# gen_br2_value_test
#-------------------------------------------------------------------------
# Test the correct branch resolution based on various source values.

def gen_br2_value_test( inst, src0, src1, taken ):
  return gen_br2_template( 0, 0, "x1", "x2", inst, src0, src1, taken )

# ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

#-------------------------------------------------------------------------
# gen_sd_template
#-------------------------------------------------------------------------

def gen_sd_template(
  num_nops_sword, num_nops_dest,
  reg_base, reg_sword,
  inst, offset, base, sword, result
):
  return """
    # Move base value into register
    csrr {reg_base}, mngr2proc < {base}    
   
    # Move sword value into register
    csrr {reg_sword}, mngr2proc < {sword}
    {nops_sword}    
         
    # Instruction under test
    {inst} {reg_sword}, {offset}({reg_base})
    {nops_dest}
    
    # Instruction to extract loaded word
    lw x3, {offset}({reg_base})
    
    # Check the result
    csrw proc2mngr, x3 > {result}

  """.format(  
    nops_sword = gen_nops(num_nops_sword),    
    nops_dest  = gen_nops(num_nops_dest),
    **locals()
  )

#-------------------------------------------------------------------------
# gen_sd_dest_dep_test
#-------------------------------------------------------------------------
# Test the destination bypass path by varying how many nops are
# inserted between the instruction under test and reading the destination
# register with a csrr instruction.

def gen_sd_dest_dep_test( num_nops, inst, base, sword, result ):
  return gen_sd_template( 8, num_nops, "x1", "x2", inst, 0, base, sword, result )

#-------------------------------------------------------------------------
# gen_sd_base_dep_test
#-------------------------------------------------------------------------
# Test the base register bypass paths by varying how many nops are
# inserted between writing the base register and reading this register in
# the instruction under test.

def gen_sd_base_dep_test( num_nops, inst, base, sword, result ):
  return gen_sd_template( num_nops, 0, "x1", "x2", inst, 0, base, sword, result )

#-------------------------------------------------------------------------
# gen_sd_base_eq_dest_test
#-------------------------------------------------------------------------
# Test situation where the base register specifier is the same as the
# destination register specifier.

def gen_sd_base_eq_dest_test( inst, base, sword, result ):
  return gen_sd_template(  0, 0, "x3", "x2", inst, 0, base, sword, result )

#-------------------------------------------------------------------------
# gen_sd_value_test
#-------------------------------------------------------------------------
# Test the actual operation of a register-register instruction under
# test. We assume that bypassing has already been tested.

def gen_sd_value_test( inst, offset, base, sword, result ):
  return gen_sd_template(  0, 0, "x1", "x2", inst, offset, base, sword, result )

#-------------------------------------------------------------------------
# gen_ld_template
#-------------------------------------------------------------------------
# Template for load instructions. We first write the base register before
# executing the instruction under test. We parameterize the number of
# nops after writing the base register and the instruction under test to
# enable using this template for testing various bypass paths. We also
# parameterize the register specifiers to enable using this template to
# test situations where the base register is equal to the destination
# register.

def gen_ld_template(
  num_nops_base, num_nops_dest,
  reg_base,
  inst, offset, base, result
):
  return """

    # Move base value into register
    csrr {reg_base}, mngr2proc < {base}
    {nops_base}

    # Instruction under test
    {inst} x3, {offset}({reg_base})
    {nops_dest}

    # Check the result
    csrw proc2mngr, x3 > {result}

  """.format(
    nops_base = gen_nops(num_nops_base),
    nops_dest = gen_nops(num_nops_dest),
    **locals()
  )

#-------------------------------------------------------------------------
# gen_ld_dest_dep_test
#-------------------------------------------------------------------------
# Test the destination bypass path by varying how many nops are
# inserted between the instruction under test and reading the destination
# register with a csrr instruction.

def gen_ld_dest_dep_test( num_nops, inst, base, result ):
  return gen_ld_template( 8, num_nops, "x1", inst, 0, base, result )

#-------------------------------------------------------------------------
# gen_ld_base_dep_test
#-------------------------------------------------------------------------
# Test the base register bypass paths by varying how many nops are
# inserted between writing the base register and reading this register in
# the instruction under test.

def gen_ld_base_dep_test( num_nops, inst, base, result ):
  return gen_ld_template( num_nops, 0, "x1", inst, 0, base, result )

#-------------------------------------------------------------------------
# gen_ld_base_eq_dest_test
#-------------------------------------------------------------------------
# Test situation where the base register specifier is the same as the
# destination register specifier.

def gen_ld_base_eq_dest_test( inst, base, result ):
  return gen_ld_template( 0, 0, "x3", inst, 0, base, result )

#-------------------------------------------------------------------------
# gen_ld_value_test
#-------------------------------------------------------------------------
# Test the actual operation of a register-register instruction under
# test. We assume that bypassing has already been tested.

def gen_ld_value_test( inst, offset, base, result ):
  return gen_ld_template( 0, 0, "x1", inst, offset, base, result )

# ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''



def gen_jalr_dest_dep_test( num_nop_a, num_nop_b):
    return """

    # Use r3 to track the control flow pattern
    addi  x3, x0, 0           # 0x0200
                              #
    lui x1,      %hi[label_a] # 0x0204
    addi x1, x1, %lo[label_a] # 0x0208  
    {nops_a}
    jalr  x31, x1, 0          # 0x022c
    addi  x3, x3, 0b01        # 0x0230
    {nops_b}

  label_a:
    addi  x3, x3, 0b10

    # Check the link address
    csrw  proc2mngr, x31 > {link}

    # Only the second bit should be set if jump was taken
    csrw  proc2mngr, x3  > 0b10

  """.format(  
    nops_a = gen_nops(num_nop_a),    
    nops_b  = gen_nops(num_nop_b),
    link = str(hex(0x0208 + (num_nop_a * 4))),
    **locals()
  )

#=========================================================================
# TestHarness
#=========================================================================

class TestHarness (Model):

  #-----------------------------------------------------------------------
  # constructor
  #-----------------------------------------------------------------------

  def __init__( s, ProcModel, src_delay, sink_delay,
                              mem_stall_prob, mem_latency ):

    s.src    = TestSource    ( 32, [], src_delay  )
    s.sink   = TestSink      ( 32, [], sink_delay )
    s.proc   = ProcModel     ()
    s.mem    = TestMemory    ( MemMsg4B(), 2, mem_stall_prob, mem_latency )

    # Processor <-> Proc/Mngr

    s.connect( s.proc.mngr2proc, s.src.out         )
    s.connect( s.proc.proc2mngr, s.sink.in_        )

    # Processor <-> Memory

    s.connect( s.proc.imemreq,   s.mem.reqs[0]     )
    s.connect( s.proc.imemresp,  s.mem.resps[0]    )
    s.connect( s.proc.dmemreq,   s.mem.reqs[1]     )
    s.connect( s.proc.dmemresp,  s.mem.resps[1]    )

  #-----------------------------------------------------------------------
  # load
  #-----------------------------------------------------------------------

  def load( self, mem_image ):

    # Iterate over the sections

    sections = mem_image.get_sections()
    for section in sections:

      # For .mngr2proc sections, copy section into mngr2proc src

      if section.name == ".mngr2proc":
        for i in xrange(0,len(section.data),4):
          bits = struct.unpack_from("<I",buffer(section.data,i,4))[0]
          self.src.src.msgs.append( Bits(32,bits) )

      # For .proc2mngr sections, copy section into proc2mngr_ref src

      elif section.name == ".proc2mngr":
        for i in xrange(0,len(section.data),4):
          bits = struct.unpack_from("<I",buffer(section.data,i,4))[0]
          self.sink.sink.msgs.append( Bits(32,bits) )

      # For all other sections, simply copy them into the memory

      else:
        start_addr = section.addr
        stop_addr  = section.addr + len(section.data)
        self.mem.mem[start_addr:stop_addr] = section.data

  #-----------------------------------------------------------------------
  # cleanup
  #-----------------------------------------------------------------------

  def cleanup( s ):
    del s.mem.mem[:]

  #-----------------------------------------------------------------------
  # done
  #-----------------------------------------------------------------------

  def done( s ):
    return s.src.done and s.sink.done

  #-----------------------------------------------------------------------
  # line_trace
  #-----------------------------------------------------------------------

  def line_trace( s ):
    return s.src.line_trace()  + " > " + \
           s.proc.line_trace() + "|" + \
           s.mem.line_trace()  + " > " + \
           s.sink.line_trace()

#=========================================================================
# run_test
#=========================================================================

def run_test( ProcModel, gen_test, src_delay=0, sink_delay=0,
                                   mem_stall_prob=0, mem_latency=0,
                                   max_cycles=5000 ):

  # Instantiate and elaborate the model

  model = TestHarness( ProcModel, src_delay, sink_delay,
                                  mem_stall_prob, mem_latency  )
  model.elaborate()

  # Assemble the test program

  mem_image = assemble( gen_test() )

  # Load the program into the model

  model.load( mem_image )

  # Create a simulator using the simulation tool

  sim = SimulationTool( model )

  # Run the simulation

  print()

  sim.reset()
  while not model.done() and sim.ncycles < max_cycles:
    sim.print_line_trace()
    sim.cycle()

  # Force a test failure if we timed out

  assert sim.ncycles < max_cycles

  # Add a couple extra ticks so that the VCD dump is nicer

  sim.cycle()
  sim.cycle()
  sim.cycle()

  model.cleanup()

