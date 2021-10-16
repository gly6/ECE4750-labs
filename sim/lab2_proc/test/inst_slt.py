#=========================================================================
# slt
#=========================================================================

import random

from pymtl import *
from inst_utils import *

#-------------------------------------------------------------------------
# gen_basic_test
#-------------------------------------------------------------------------

def gen_basic_test():
  return """
    csrr x1, mngr2proc < 4
    csrr x2, mngr2proc < 5
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    slt x3, x1, x2
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
    gen_rr_dest_dep_test( 5, "slt", 0x0000000f, 0x0000000f, 0x00000000 ),
    gen_rr_dest_dep_test( 4, "slt", 0x000000f0, 0x0000000f, 0x00000000 ),
    gen_rr_dest_dep_test( 3, "slt", 0x00000f00, 0x0000000f, 0x00000000 ),
    gen_rr_dest_dep_test( 2, "slt", 0x0000f000, 0x0000000f, 0x00000000 ),
    gen_rr_dest_dep_test( 1, "slt", 0xf0000000, 0x0000000f, 0x00000001 ),
    gen_rr_dest_dep_test( 0, "slt", 0x00f00000, 0x0000000f, 0x00000000 ),
    gen_rr_dest_dep_test( 0, "slt", 0, 0, 0 ),
    gen_rr_dest_dep_test( 0, "slt", -20, 0, 1 ),
    gen_rr_dest_dep_test( 0, "slt", 0, -20, 0 ),
    gen_rr_dest_dep_test( 0, "slt", -20, -19, 1 ),
    gen_rr_dest_dep_test( 0, "slt", -19, -20, 0 ),
    gen_rr_dest_dep_test( 0, "slt", -20, 19, 1 ),
    gen_rr_dest_dep_test( 0, "slt", 39, -40, 0 ),
  ]

  #-------------------------------------------------------------------------
# gen_src0_dep_test
#-------------------------------------------------------------------------

def gen_src0_dep_test():
  return [
    gen_rr_src0_dep_test( 5, "slt", 0x0000000f, 0x0000000f, 0x00000000 ),
    gen_rr_src0_dep_test( 4, "slt", 0x000000f0, 0x0000000f, 0x00000000 ),
    gen_rr_src0_dep_test( 3, "slt", 0x00000f00, 0x0000000f, 0x00000000 ),
    gen_rr_src0_dep_test( 2, "slt", 0x0000f000, 0x0000000f, 0x00000000 ),
    gen_rr_src0_dep_test( 1, "slt", 0xf0000000, 0x0000000f, 0x00000001 ),
    gen_rr_src0_dep_test( 0, "slt", 0x00f00000, 0x0000000f, 0x00000000 ),
    gen_rr_src0_dep_test( 0, "slt", 0, 0, 0 ),
    gen_rr_src0_dep_test( 0, "slt", -20, 0, 1 ),
    gen_rr_src0_dep_test( 0, "slt", 0, -20, 0 ),
    gen_rr_src0_dep_test( 0, "slt", -20, -19, 1 ),
    gen_rr_src0_dep_test( 0, "slt", -19, -20, 0 ),
    gen_rr_src0_dep_test( 0, "slt", -20, 19, 1 ),
    gen_rr_src0_dep_test( 0, "slt", 39, -40, 0 ),
  ]

  #-------------------------------------------------------------------------
# gen_src1_dep_test
#-------------------------------------------------------------------------

def gen_src1_dep_test():
  return [
    gen_rr_src1_dep_test( 5, "slt", 0x0000000f, 0x0000000f, 0x00000000 ),
    gen_rr_src1_dep_test( 4, "slt", 0x000000f0, 0x0000000f, 0x00000000 ),
    gen_rr_src1_dep_test( 3, "slt", 0x00000f00, 0x0000000f, 0x00000000 ),
    gen_rr_src1_dep_test( 2, "slt", 0x0000f000, 0x0000000f, 0x00000000 ),
    gen_rr_src1_dep_test( 1, "slt", 0xf0000000, 0x0000000f, 0x00000001 ),
    gen_rr_src1_dep_test( 0, "slt", 0x00f00000, 0x0000000f, 0x00000000 ),
    gen_rr_src1_dep_test( 0, "slt", 0, 0, 0 ),
    gen_rr_src1_dep_test( 0, "slt", -20, 0, 1 ),
    gen_rr_src1_dep_test( 0, "slt", 0, -20, 0 ),
    gen_rr_src1_dep_test( 0, "slt", -20, -19, 1 ),
    gen_rr_src1_dep_test( 0, "slt", -19, -20, 0 ),
    gen_rr_src1_dep_test( 0, "slt", -20, 19, 1 ),
    gen_rr_src1_dep_test( 0, "slt", 39, -40, 0 ),
  ]

  #-------------------------------------------------------------------------
# gen_srcs_dep_test
#-------------------------------------------------------------------------

def gen_srcs_dep_test():
  return [
    gen_rr_srcs_dep_test( 5, "slt", 0x0000000f, 0x0000000f, 0x00000000 ),
    gen_rr_srcs_dep_test( 4, "slt", 0x000000f0, 0x0000000f, 0x00000000 ),
    gen_rr_srcs_dep_test( 3, "slt", 0x00000f00, 0x0000000f, 0x00000000 ),
    gen_rr_srcs_dep_test( 2, "slt", 0x0000f000, 0x0000000f, 0x00000000 ),
    gen_rr_srcs_dep_test( 1, "slt", 0xf0000000, 0x0000000f, 0x00000001 ),
    gen_rr_srcs_dep_test( 0, "slt", 0x00f00000, 0x0000000f, 0x00000000 ),
    gen_rr_srcs_dep_test( 0, "slt", 0, 0, 0 ),
    gen_rr_srcs_dep_test( 0, "slt", -20, 0, 1 ),
    gen_rr_srcs_dep_test( 0, "slt", 0, -20, 0 ),
    gen_rr_srcs_dep_test( 0, "slt", -20, -19, 1 ),
    gen_rr_srcs_dep_test( 0, "slt", -19, -20, 0 ),
    gen_rr_srcs_dep_test( 0, "slt", -20, 19, 1 ),
    gen_rr_srcs_dep_test( 0, "slt", 39, -40, 0 ),
  ]

#-------------------------------------------------------------------------
# gen_srcs_dest_test
#-------------------------------------------------------------------------

def gen_srcs_dest_test():
  return [
    gen_rr_src0_eq_dest_test( "slt", 0x00000f0f, 0x000000ff, 0x00000000 ),
    gen_rr_src1_eq_dest_test( "slt", 0x0000f0f0, 0x00000ff0, 0x00000000 ),
    gen_rr_src0_eq_dest_test( "slt", 0xf0000f0f, 0x000000ff, 0x00000001 ),
    gen_rr_src1_eq_dest_test( "slt", 0xf000f0f0, 0x00000ff0, 0x00000001 ),
    gen_rr_src0_eq_src1_test( "slt", 0x000f0f00, 0x00000000 ),
    gen_rr_srcs_eq_dest_test( "slt", 0x000f0f00, 0x00000000 ),
  ]

#-------------------------------------------------------------------------
# gen_value_test
#-------------------------------------------------------------------------

def gen_value_test():
  return [
    gen_rr_value_test( "slt", 0x0000000f, 0x0000000f, 0x00000000 ),
    gen_rr_value_test( "slt", 0x000000f0, 0x0000000f, 0x00000000 ),
    gen_rr_value_test( "slt", 0x00000f00, 0x0000000f, 0x00000000 ),
    gen_rr_value_test( "slt", 0x0000f000, 0x0000000f, 0x00000000 ),
    gen_rr_value_test( "slt", 0xf0000000, 0x0000000f, 0x00000001 ),
    gen_rr_value_test( "slt", 0x00f00000, 0x0000000f, 0x00000000 ),
  ]

#-------------------------------------------------------------------------
# gen_random_test
#-------------------------------------------------------------------------

def gen_random_test():
  asm_code = []
  for i in xrange(100):
    src0 = Bits( 32, random.randint(0,0xffffffff) )
    src1 = Bits( 32, random.randint(0,0xffffffff) )
    dest = Bits(32, 0x00000001) if src0.int() < src1.int() else Bits(32, 0x00000000) 
    asm_code.append( gen_rr_value_test( "slt", src0.uint(), src1.uint(), dest.uint() ) )
  return asm_code