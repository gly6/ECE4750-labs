#=========================================================================
# blt
#=========================================================================

import random

from pymtl import *
from inst_utils import *

#-------------------------------------------------------------------------
# gen_basic_test
#-------------------------------------------------------------------------

def gen_basic_test():
  return """

    # Use x3 to track the control flow pattern
    addi  x3, x0, 0

    csrr  x1, mngr2proc < 2
    csrr  x2, mngr2proc < 1

    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop

    # This branch should be taken
    blt   x2, x1, label_a
    addi  x3, x3, 0b01

    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop

  label_a:
    addi  x3, x3, 0b10

    # Only the second bit should be set if branch was taken
    csrw proc2mngr, x3 > 0b10

  """

# ''' LAB TASK ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# Define additional directed and random test cases.
# '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

#-------------------------------------------------------------------------
# gen_src0_dep_taken_test
#-------------------------------------------------------------------------

def gen_src0_dep_taken_test():
  return [
    gen_br2_src0_dep_test( 5, "blt", 1, 7, True ),
    gen_br2_src0_dep_test( 4, "blt", 2, 7, True ),
    gen_br2_src0_dep_test( 3, "blt", 3, 7, True ),
    gen_br2_src0_dep_test( 2, "blt", 4, 7, True ),
    gen_br2_src0_dep_test( 1, "blt", 5, 7, True ),
    gen_br2_src0_dep_test( 0, "blt", 6, 7, True ),
  ]

#-------------------------------------------------------------------------
# gen_src0_dep_nottaken_test
#-------------------------------------------------------------------------

def gen_src0_dep_nottaken_test():
  return [    
    gen_br2_src0_dep_test( 5, "blt", 1, 1, False ),
    gen_br2_src0_dep_test( 4, "blt", 2, 2, False ),
    gen_br2_src0_dep_test( 3, "blt", 3, 3, False ),
    gen_br2_src0_dep_test( 2, "blt", 4, 4, False ),
    gen_br2_src0_dep_test( 1, "blt", 5, 5, False ),
    gen_br2_src0_dep_test( 0, "blt", 6, 6, False ),
    gen_br2_src0_dep_test( 5, "blt", 2, 1, False ),
    gen_br2_src0_dep_test( 4, "blt", 4, 2, False ),
    gen_br2_src0_dep_test( 3, "blt", 6, 3, False ),
    gen_br2_src0_dep_test( 2, "blt", 8, 4, False ),
    gen_br2_src0_dep_test( 1, "blt", 10, 5, False ),
    gen_br2_src0_dep_test( 0, "blt", 12, 6, False ),
  ]

#-------------------------------------------------------------------------
# gen_src1_dep_taken_test
#-------------------------------------------------------------------------

def gen_src1_dep_taken_test():
  return [
    gen_br2_src1_dep_test( 5, "blt", 1, 7, True ),
    gen_br2_src1_dep_test( 4, "blt", 2, 7, True ),
    gen_br2_src1_dep_test( 3, "blt", 3, 7, True ),
    gen_br2_src1_dep_test( 2, "blt", 4, 7, True ),
    gen_br2_src1_dep_test( 1, "blt", 5, 7, True ),
    gen_br2_src1_dep_test( 0, "blt", 6, 7, True ),
  ]

#-------------------------------------------------------------------------
# gen_src1_dep_nottaken_test
#-------------------------------------------------------------------------

def gen_src1_dep_nottaken_test():
  return [
    gen_br2_src1_dep_test( 5, "blt", 1, 1, False ),
    gen_br2_src1_dep_test( 4, "blt", 2, 2, False ),
    gen_br2_src1_dep_test( 3, "blt", 3, 3, False ),
    gen_br2_src1_dep_test( 2, "blt", 4, 4, False ),
    gen_br2_src1_dep_test( 1, "blt", 5, 5, False ),
    gen_br2_src1_dep_test( 0, "blt", 6, 6, False ),
    gen_br2_src1_dep_test( 5, "blt", 2, 1, False ),
    gen_br2_src1_dep_test( 4, "blt", 4, 2, False ),
    gen_br2_src1_dep_test( 3, "blt", 6, 3, False ),
    gen_br2_src1_dep_test( 2, "blt", 8, 4, False ),
    gen_br2_src1_dep_test( 1, "blt", 10, 5, False ),
    gen_br2_src1_dep_test( 0, "blt", 12, 6, False ),
  ]

#-------------------------------------------------------------------------
# gen_srcs_dep_taken_test
#-------------------------------------------------------------------------

def gen_srcs_dep_taken_test():
  return [
    gen_br2_srcs_dep_test( 5, "blt", 1, 2, True ),
    gen_br2_srcs_dep_test( 4, "blt", 2, 3, True ),
    gen_br2_srcs_dep_test( 3, "blt", 3, 4, True ),
    gen_br2_srcs_dep_test( 2, "blt", 4, 5, True ),
    gen_br2_srcs_dep_test( 1, "blt", 5, 6, True ),
    gen_br2_srcs_dep_test( 0, "blt", 6, 7, True ),
  ]

#-------------------------------------------------------------------------
# gen_srcs_dep_nottaken_test
#-------------------------------------------------------------------------

def gen_srcs_dep_nottaken_test():
  return [


    gen_br2_srcs_dep_test( 5, "blt", 1, 1, False ),
    gen_br2_srcs_dep_test( 4, "blt", 2, 2, False ),
    gen_br2_srcs_dep_test( 3, "blt", 3, 3, False ),
    gen_br2_srcs_dep_test( 2, "blt", 4, 4, False ),
    gen_br2_srcs_dep_test( 1, "blt", 5, 5, False ),
    gen_br2_srcs_dep_test( 0, "blt", 6, 6, False ),
    gen_br2_srcs_dep_test( 5, "blt", 2, 1, False ),
    gen_br2_srcs_dep_test( 4, "blt", 4, 2, False ),
    gen_br2_srcs_dep_test( 3, "blt", 6, 3, False ),
    gen_br2_srcs_dep_test( 2, "blt", 8, 4, False ),
    gen_br2_srcs_dep_test( 1, "blt", 10, 5, False ),
    gen_br2_srcs_dep_test( 0, "blt", 12, 6, False ),
  ]

#-------------------------------------------------------------------------
# gen_src0_eq_src1_nottaken_test
#-------------------------------------------------------------------------

def gen_src0_eq_src1_test():
  return [
    gen_br2_src0_eq_src1_test( "blt", 1, False ),
  ]

#-------------------------------------------------------------------------
# gen_value_test
#-------------------------------------------------------------------------

def gen_value_test():
  return [

    gen_br2_value_test( "blt", -1, -1, False ),
    gen_br2_value_test( "blt", -1,  0, True  ),
    gen_br2_value_test( "blt", -1,  1, True  ),

    gen_br2_value_test( "blt",  0, -1, False  ),
    gen_br2_value_test( "blt",  0,  0, False ),
    gen_br2_value_test( "blt",  0,  1, True  ),

    gen_br2_value_test( "blt",  1, -1, False  ),
    gen_br2_value_test( "blt",  1,  0, False  ),
    gen_br2_value_test( "blt",  1,  1, False ),

    gen_br2_value_test( "blt", 0xfffffff7, 0xfffffff7, False ),
    gen_br2_value_test( "blt", 0x7fffffff, 0x7fffffff, False ),
    gen_br2_value_test( "blt", 0xfffffff7, 0x7fffffff, True ),
    gen_br2_value_test( "blt", 0x7fffffff, 0xfffffff7, False ),

  ]

#-------------------------------------------------------------------------
# gen_random_test
#-------------------------------------------------------------------------

def gen_random_test():
  asm_code = []
  for i in xrange(25):
    taken = random.choice([True, False])
    src0  = Bits( 32, random.randint(0, 0xffffffff) )
    if taken:
      # Branch taken, src0 < src1
      src1 = Bits( 32, random.randint((src0.int() + 1), 2147483647) )
    else:
      # Branch not taken, src0 >= src1
      src1 = Bits( 32, random.randint(-2147483648, src0.int()) )
    asm_code.append( gen_br2_value_test( "blt", src0.int(), src1.int(), taken ) )
  return asm_code