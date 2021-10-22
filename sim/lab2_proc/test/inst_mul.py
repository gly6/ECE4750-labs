#=========================================================================
# mul
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
    csrr x2, mngr2proc < 4
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    mul x3, x1, x2
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    csrw proc2mngr, x3 > 20
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
  """

#-------------------------------------------------------------------------
# gen_dest_dep_test
#-------------------------------------------------------------------------

def gen_dest_dep_test():
  return [
    gen_rr_dest_dep_test( 5, "mul", 1, 1, 1 ),
    gen_rr_dest_dep_test( 4, "mul", 2, 1, 2 ),
    gen_rr_dest_dep_test( 3, "mul", 3, 1, 3 ),
    gen_rr_dest_dep_test( 2, "mul", 4, 1, 4 ),
    gen_rr_dest_dep_test( 1, "mul", 5, 2, 10 ),
    gen_rr_dest_dep_test( 0, "mul", 6, -1, -6 ),
    gen_rr_dest_dep_test( 0, "mul", 6, 5, 30 ),
    gen_rr_dest_dep_test( 0, "mul", 0x03, 0x05, 0x0f),
    gen_rr_dest_dep_test( 0, "mul", -2, 5, -10),
    gen_rr_dest_dep_test( 0, "mul", -10, -30, 300),
    gen_rr_dest_dep_test( 0, "mul", 1, 0, 0),
    gen_rr_dest_dep_test( 0, "mul", 0, 1, 0),
    gen_rr_dest_dep_test( 0, "mul", 0, 0, 0),
    gen_rr_dest_dep_test( 0, "mul", 0x000000a4, 0x0000000f, 0x0000099c),
    gen_rr_dest_dep_test( 0, "mul", 0x000000B1, 0x000000D5, 0x00009345),
    gen_rr_dest_dep_test( 0, "mul", 0x000000FF, 0x000000FF, 0x0000fe01),
    gen_rr_dest_dep_test( 0, "mul", 0xFFFFFFFF, 0xFFFFFFFF, 0x00000001),
    gen_rr_dest_dep_test( 0, "mul", 0x0000FFFF, 0x0000FFFF, 0xFFFE0001),
    gen_rr_dest_dep_test( 0, "mul", 0xEDEDEDED, 0xBABABABA, 0xcdef1032),
    gen_rr_dest_dep_test( 0, "mul", 0x80000000, 0x00000002, 0x00000000),
  ]

#-------------------------------------------------------------------------
# gen_src0_dep_test
#-------------------------------------------------------------------------

def gen_src0_dep_test():
  return [
    gen_rr_src0_dep_test( 5, "mul", 1, 1, 1 ),
    gen_rr_src0_dep_test( 4, "mul", 2, 1, 2 ),
    gen_rr_src0_dep_test( 3, "mul", 3, 1, 3 ),
    gen_rr_src0_dep_test( 2, "mul", 4, 1, 4 ),
    gen_rr_src0_dep_test( 1, "mul", 5, 2, 10 ),
    gen_rr_src0_dep_test( 0, "mul", 6, -1, -6 ),
    gen_rr_src0_dep_test( 0, "mul", 6, 5, 30 ),
    gen_rr_src0_dep_test( 0, "mul", 0x03, 0x05, 0x0f),
    gen_rr_src0_dep_test( 0, "mul", -2, 5, -10),
    gen_rr_src0_dep_test( 0, "mul", -10, -30, 300),
    gen_rr_src0_dep_test( 0, "mul", 1, 0, 0),
    gen_rr_src0_dep_test( 0, "mul", 0, 1, 0),
    gen_rr_src0_dep_test( 0, "mul", 0, 0, 0),
    gen_rr_src0_dep_test( 0, "mul", 0x000000a4, 0x0000000f, 0x0000099c),
    gen_rr_src0_dep_test( 0, "mul", 0x000000B1, 0x000000D5, 0x00009345),
    gen_rr_src0_dep_test( 0, "mul", 0x000000FF, 0x000000FF, 0x0000fe01),
    gen_rr_src0_dep_test( 0, "mul", 0xFFFFFFFF, 0xFFFFFFFF, 0x00000001),
    gen_rr_src0_dep_test( 0, "mul", 0x0000FFFF, 0x0000FFFF, 0xFFFE0001),
    gen_rr_src0_dep_test( 0, "mul", 0xEDEDEDED, 0xBABABABA, 0xcdef1032),
    gen_rr_src0_dep_test( 0, "mul", 0x80000000, 0x00000002, 0x00000000),
  ]
  #-------------------------------------------------------------------------
# gen_src1_dep_test
#-------------------------------------------------------------------------

def gen_src1_dep_test():
  return [
    gen_rr_src1_dep_test( 5, "mul", 1, 1, 1 ),
    gen_rr_src1_dep_test( 4, "mul", 2, 1, 2 ),
    gen_rr_src1_dep_test( 3, "mul", 3, 1, 3 ),
    gen_rr_src1_dep_test( 2, "mul", 4, 1, 4 ),
    gen_rr_src1_dep_test( 1, "mul", 5, 2, 10 ),
    gen_rr_src1_dep_test( 0, "mul", 6, -1, -6 ),
    gen_rr_src1_dep_test( 0, "mul", 6, 5, 30 ),
    gen_rr_src1_dep_test( 0, "mul", 0x03, 0x05, 0x0f),
    gen_rr_src1_dep_test( 0, "mul", -2, 5, -10),
    gen_rr_src1_dep_test( 0, "mul", -10, -30, 300),
    gen_rr_src1_dep_test( 0, "mul", 1, 0, 0),
    gen_rr_src1_dep_test( 0, "mul", 0, 1, 0),
    gen_rr_src1_dep_test( 0, "mul", 0, 0, 0),
    gen_rr_src1_dep_test( 0, "mul", 0x000000a4, 0x0000000f, 0x0000099c),
    gen_rr_src1_dep_test( 0, "mul", 0x000000B1, 0x000000D5, 0x00009345),
    gen_rr_src1_dep_test( 0, "mul", 0x000000FF, 0x000000FF, 0x0000fe01),
    gen_rr_src1_dep_test( 0, "mul", 0xFFFFFFFF, 0xFFFFFFFF, 0x00000001),
    gen_rr_src1_dep_test( 0, "mul", 0x0000FFFF, 0x0000FFFF, 0xFFFE0001),
    gen_rr_src1_dep_test( 0, "mul", 0xEDEDEDED, 0xBABABABA, 0xcdef1032),
    gen_rr_src1_dep_test( 0, "mul", 0x80000000, 0x00000002, 0x00000000),
  ]
  #-------------------------------------------------------------------------
# gen_srcs_dep_test
#-------------------------------------------------------------------------

def gen_srcs_dep_test():
  return [
    gen_rr_srcs_dep_test( 5, "mul", 1, 1, 1 ),
    gen_rr_srcs_dep_test( 4, "mul", 2, 1, 2 ),
    gen_rr_srcs_dep_test( 3, "mul", 3, 1, 3 ),
    gen_rr_srcs_dep_test( 2, "mul", 4, 1, 4 ),
    gen_rr_srcs_dep_test( 1, "mul", 5, 2, 10 ),
    gen_rr_srcs_dep_test( 0, "mul", 6, -1, -6 ),
    gen_rr_srcs_dep_test( 0, "mul", 6, 5, 30 ),
    gen_rr_srcs_dep_test( 0, "mul", 0x03, 0x05, 0x0f),
    gen_rr_srcs_dep_test( 0, "mul", -2, 5, -10),
    gen_rr_srcs_dep_test( 0, "mul", -10, -30, 300),
    gen_rr_srcs_dep_test( 0, "mul", 1, 0, 0),
    gen_rr_srcs_dep_test( 0, "mul", 0, 1, 0),
    gen_rr_srcs_dep_test( 0, "mul", 0, 0, 0),
    gen_rr_srcs_dep_test( 0, "mul", 0x000000a4, 0x0000000f, 0x0000099c),
    gen_rr_srcs_dep_test( 0, "mul", 0x000000B1, 0x000000D5, 0x00009345),
    gen_rr_srcs_dep_test( 0, "mul", 0x000000FF, 0x000000FF, 0x0000fe01),
    gen_rr_srcs_dep_test( 0, "mul", 0xFFFFFFFF, 0xFFFFFFFF, 0x00000001),
    gen_rr_srcs_dep_test( 0, "mul", 0x0000FFFF, 0x0000FFFF, 0xFFFE0001),
    gen_rr_srcs_dep_test( 0, "mul", 0xEDEDEDED, 0xBABABABA, 0xcdef1032),
    gen_rr_srcs_dep_test( 0, "mul", 0x80000000, 0x00000002, 0x00000000),
  ]
  
#-------------------------------------------------------------------------
# gen_srcs_dest_test
#-------------------------------------------------------------------------

def gen_srcs_dest_test():
  return [
    gen_rr_src0_eq_dest_test( "mul", 0x00000f0f, 0x000000ff, 0x000efff1 ),
    gen_rr_src1_eq_dest_test( "mul", 0x0000f0f0, 0x00000ff0, 0x0efff100 ),
    gen_rr_src0_eq_src1_test( "mul", 0x000f0f00, 0xc2e10000 ),
    gen_rr_srcs_eq_dest_test( "mul", 0x000f0f00, 0xc2e10000 ),
  ]

#-------------------------------------------------------------------------
# gen_value_test
#-------------------------------------------------------------------------

def gen_value_test():
  return [
    gen_rr_value_test( "mul", 0x000000a4, 0x0000000f, 0x0000099c),
    gen_rr_value_test( "mul", 0x000000B1, 0x000000D5, 0x00009345),
    gen_rr_value_test( "mul", 0x000000FF, 0x000000FF, 0x0000fe01),
    gen_rr_value_test( "mul", 0xFFFFFFFF, 0xFFFFFFFF, 0x00000001),
    gen_rr_value_test( "mul", 0x0000FFFF, 0x0000FFFF, 0xFFFE0001),
    gen_rr_value_test( "mul", 0xEDEDEDED, 0xBABABABA, 0xcdef1032),
    gen_rr_value_test( "mul", 0x80000000, 0x00000002, 0x00000000),
  ]

#-------------------------------------------------------------------------
# gen_random_test
#-------------------------------------------------------------------------

def gen_random_test():
  asm_code = []
  for i in xrange(100):
    src0 = Bits( 32, random.randint(0,0xffffffff) )
    src1 = Bits( 32, random.randint(0,0xffffffff) )
    dest = (src0 * src1) & 0xffffffff
    asm_code.append( gen_rr_value_test( "mul", src0.uint(), src1.uint(), dest.uint() ) )
  return asm_code
