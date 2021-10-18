#=========================================================================
# slti
#=========================================================================

import random

from pymtl import *
from inst_utils import *

#-------------------------------------------------------------------------
# gen_basic_test
#-------------------------------------------------------------------------

def gen_basic_test():
  return """
    csrr x1, mngr2proc < 5
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    slti x3, x1, 6
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    csrw proc2mngr, x3 > 1
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
  """

# ''' LAB TASK ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# Define additional directed and random test cases.
# '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

#-------------------------------------------------------------------------
# gen_dest_dep_test
#-------------------------------------------------------------------------

def gen_dest_dep_test():
  return [
    gen_rimm_dest_dep_test( 5, "slti", 0x0000000f, 0x0000000f, 0x00000000 ),
    gen_rimm_dest_dep_test( 4, "slti", 0x000000f0, 0x0000000f, 0x00000000 ),
    gen_rimm_dest_dep_test( 3, "slti", 0x00000f00, 0x0000000f, 0x00000000 ),
    gen_rimm_dest_dep_test( 2, "slti", 0x0000f000, 0x0000000f, 0x00000000 ),
    gen_rimm_dest_dep_test( 1, "slti", 0xf0000000, 0x0000000f, 0x00000001 ),
    gen_rimm_dest_dep_test( 0, "slti", 0x00f00000, 0x0000000f, 0x00000000 ),
    gen_rimm_dest_dep_test( 0, "slti", 0, 0, 0 ),
    gen_rimm_dest_dep_test( 0, "slti", -20, 0, 1 ),
    gen_rimm_dest_dep_test( 0, "slti", 0, -20, 0 ),
    gen_rimm_dest_dep_test( 0, "slti", -20, -19, 1 ),
    gen_rimm_dest_dep_test( 0, "slti", -19, -20, 0 ),
    gen_rimm_dest_dep_test( 0, "slti", -20, 19, 1 ),
    gen_rimm_dest_dep_test( 0, "slti", 39, -40, 0 ),
  ]

  #-------------------------------------------------------------------------
# gen_src0_dep_test
#-------------------------------------------------------------------------

def gen_src_dep_test():
  return [
    gen_rimm_src_dep_test( 5, "slti", 0x0000000f, 0x0000000f, 0x00000000 ),
    gen_rimm_src_dep_test( 4, "slti", 0x000000f0, 0x0000000f, 0x00000000 ),
    gen_rimm_src_dep_test( 3, "slti", 0x00000f00, 0x0000000f, 0x00000000 ),
    gen_rimm_src_dep_test( 2, "slti", 0x0000f000, 0x0000000f, 0x00000000 ),
    gen_rimm_src_dep_test( 1, "slti", 0xf0000000, 0x0000000f, 0x00000001 ),
    gen_rimm_src_dep_test( 0, "slti", 0x00f00000, 0x0000000f, 0x00000000 ),
    gen_rimm_src_dep_test( 0, "slti", 0, 0, 0 ),
    gen_rimm_src_dep_test( 0, "slti", -20, 0, 1 ),
    gen_rimm_src_dep_test( 0, "slti", 0, -20, 0 ),
    gen_rimm_src_dep_test( 0, "slti", -20, -19, 1 ),
    gen_rimm_src_dep_test( 0, "slti", -19, -20, 0 ),
    gen_rimm_src_dep_test( 0, "slti", -20, 19, 1 ),
    gen_rimm_src_dep_test( 0, "slti", 39, -40, 0 ),
  ]

#-------------------------------------------------------------------------
# gen_srcs_dest_test
#-------------------------------------------------------------------------

def gen_srcs_dest_test():
  return [
    gen_rimm_src_eq_dest_test( "slti", 0x00000f0f, 0x0ff, 0x00000000 ),
    gen_rimm_src_eq_dest_test( "slti", 0x0000f0f0, 0x7f0, 0x00000000 ),
    gen_rimm_src_eq_dest_test( "slti", 0xf0000f0f, 0x0ff, 0x00000001 ),
    gen_rimm_src_eq_dest_test( "slti", 0xf000f0f0, 0x7f0, 0x00000001 ),
  ]

#-------------------------------------------------------------------------
# gen_value_test
#-------------------------------------------------------------------------

def gen_value_test():
  return [
    gen_rimm_value_test( "slti", 0x0000000f, 0x0000000f, 0x00000000 ),
    gen_rimm_value_test( "slti", 0x000000f0, 0x0000000f, 0x00000000 ),
    gen_rimm_value_test( "slti", 0x00000f00, 0x0000000f, 0x00000000 ),
    gen_rimm_value_test( "slti", 0x0000f000, 0x0000000f, 0x00000000 ),
    gen_rimm_value_test( "slti", 0xf0000000, 0x0000000f, 0x00000001 ),
    gen_rimm_value_test( "slti", 0x00f00000, 0x0000000f, 0x00000000 ),
  ]

#-------------------------------------------------------------------------
# gen_random_test
#-------------------------------------------------------------------------

def gen_random_test():
  asm_code = []
  for i in xrange(100):
    src0 = Bits( 32, random.randint(0,0xffffffff) )
    src1 = Bits( 11, random.randint(0,0x7ff) )
    dest = Bits(32, 0x00000001) if src0.int() < src1.int() else Bits(32, 0x00000000) 
    asm_code.append( gen_rimm_value_test( "slti", src0.uint(), src1.uint(), dest.uint() ) )
  return asm_code