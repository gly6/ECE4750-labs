#=========================================================================
# sltiu
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
    sltiu x3, x1, 6
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
    gen_rimm_dest_dep_test( 5, "sltiu", 0x0000000f, 0x0000000f, 0x00000000 ),
    gen_rimm_dest_dep_test( 4, "sltiu", 0x000000f0, 0x0000000f, 0x00000000 ),
    gen_rimm_dest_dep_test( 3, "sltiu", 0x00000f00, 0x0000000f, 0x00000000 ),
    gen_rimm_dest_dep_test( 2, "sltiu", 0x0000f000, 0x0000000f, 0x00000000 ),
    gen_rimm_dest_dep_test( 1, "sltiu", 0xf0000000, 0x0000000f, 0x00000000 ),
    gen_rimm_dest_dep_test( 0, "sltiu", 0x00f00000, 0x0000000f, 0x00000000 ),
    gen_rimm_dest_dep_test( 0, "sltiu", 0x000006ff, 0x00000700, 0x00000001 ),
    gen_rimm_dest_dep_test( 0, "sltiu", 0x0000000e, 0x0000000f, 0x00000001 ),
    gen_rimm_dest_dep_test( 0, "sltiu", 0x00000004, 0x00000703, 0x00000001 ),
    gen_rimm_dest_dep_test( 0, "sltiu", 0x7fffffff, 0x000007ff, 0x00000000 ),
    gen_rimm_dest_dep_test( 0, "sltiu", 0x80000000, 0x0000000f, 0x00000000 ),
  ]

  #-------------------------------------------------------------------------
# gen_src0_dep_test
#-------------------------------------------------------------------------

def gen_src_dep_test():
  return [
    gen_rimm_src_dep_test( 5, "sltiu", 0x0000000f, 0x0000000f, 0x00000000 ),
    gen_rimm_src_dep_test( 4, "sltiu", 0x000000f0, 0x0000000f, 0x00000000 ),
    gen_rimm_src_dep_test( 3, "sltiu", 0x00000f00, 0x0000000f, 0x00000000 ),
    gen_rimm_src_dep_test( 2, "sltiu", 0x0000f000, 0x0000000f, 0x00000000 ),
    gen_rimm_src_dep_test( 1, "sltiu", 0xf0000000, 0x0000000f, 0x00000000 ),
    gen_rimm_src_dep_test( 0, "sltiu", 0x00f00000, 0x0000000f, 0x00000000 ),
    gen_rimm_src_dep_test( 0, "sltiu", 0x000006ff, 0x00000700, 0x00000001 ),
    gen_rimm_src_dep_test( 0, "sltiu", 0x0000000e, 0x0000000f, 0x00000001 ),
    gen_rimm_src_dep_test( 0, "sltiu", 0x00000004, 0x00000703, 0x00000001 ),
    gen_rimm_src_dep_test( 0, "sltiu", 0x7fffffff, 0x000007ff, 0x00000000 ),
    gen_rimm_src_dep_test( 0, "sltiu", 0x80000000, 0x0000000f, 0x00000000 ),
  ]

#-------------------------------------------------------------------------
# gen_srcs_dest_test
#-------------------------------------------------------------------------

def gen_srcs_dest_test():
  return [
    gen_rimm_src_eq_dest_test( "sltiu", 0x00000f0f, 0x0ff, 0x00000000 ),
    gen_rimm_src_eq_dest_test( "sltiu", 0x000000f0, 0x7f0, 0x00000001 ),
    gen_rimm_src_eq_dest_test( "sltiu", 0xf0000f0f, 0x0ff, 0x00000000 ),
    gen_rimm_src_eq_dest_test( "sltiu", 0xf000f0f0, 0x7f0, 0x00000000 ),
  ]

#-------------------------------------------------------------------------
# gen_value_test
#-------------------------------------------------------------------------

def gen_value_test():
  return [
    gen_rimm_value_test( "sltiu", 0x0000000f, 0x0000000f, 0x00000000 ),
    gen_rimm_value_test( "sltiu", 0x000000f0, 0x0000000f, 0x00000000 ),
    gen_rimm_value_test( "sltiu", 0x00000f00, 0x0000000f, 0x00000000 ),
    gen_rimm_value_test( "sltiu", 0x0000f000, 0x0000000f, 0x00000000 ),
    gen_rimm_value_test( "sltiu", 0xf0000000, 0x0000000f, 0x00000000 ),
    gen_rimm_value_test( "sltiu", 0x0000000e, 0x0000000f, 0x00000001 ),
    gen_rimm_value_test( "sltiu", 0x000006ff, 0x000007ff, 0x00000001 ),
    gen_rimm_value_test( "sltiu", 0x000007ff, 0x000007ff, 0x00000000 ),
    gen_rimm_value_test( "sltiu", 0x00000800, 0x000007ff, 0x00000000 ),
  ]

#-------------------------------------------------------------------------
# gen_random_test
#-------------------------------------------------------------------------

def gen_random_test():
  asm_code = []
  for i in xrange(100):
    src0 = Bits( 32, random.randint(0,0xffffffff) )
    src1 = Bits( 11, random.randint(0,0x7ff) )
    dest = Bits(32, 0x00000001) if src0.uint() < src1.uint() else Bits(32, 0x00000000) 
    asm_code.append( gen_rimm_value_test( "sltiu", src0.uint(), src1.uint(), dest.uint() ) )
  return asm_code