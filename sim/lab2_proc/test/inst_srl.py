#=========================================================================
# srl
#=========================================================================

import random

from pymtl import *
from inst_utils import *

#-------------------------------------------------------------------------
# gen_basic_test
#-------------------------------------------------------------------------

def gen_basic_test():
  return """
    csrr x1, mngr2proc < 0x00008000
    csrr x2, mngr2proc < 0x00000003
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    srl x3, x1, x2
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    csrw proc2mngr, x3 > 0x00001000
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
    gen_rr_dest_dep_test( 5, "srl", 0x00000fff, 0x0000000f, 0x00000000 ),
    gen_rr_dest_dep_test( 4, "srl", 0x00000001, 0x00000001, 0x00000000 ),
    gen_rr_dest_dep_test( 3, "srl", 0xf0000000, 0x00000001, 0x78000000 ),
    gen_rr_dest_dep_test( 2, "srl", 0x0000ffff, 0x00000008, 0x000000ff ),
    gen_rr_dest_dep_test( 1, "srl", 0x0000ffff, 0x00000010, 0x00000000 ),
    gen_rr_dest_dep_test( 0, "srl", 0xffffffff, 0x00000010, 0x0000ffff ),
    gen_rr_dest_dep_test( 0, "srl", 0xffffffff, 0xffffffff, 0x00000001 ),
    gen_rr_dest_dep_test( 0, "srl", 0xffffffff, 0x0000001f, 0x00000001 ),
    gen_rr_dest_dep_test( 0, "srl", 0x0000000f, 0x00000020, 0x0000000f ),
    gen_rr_dest_dep_test( 0, "srl", 0x80000000, 0x0000001f, 0x00000001 ),
    gen_rr_dest_dep_test( 0, "srl", 0x8000f000, 0x00000010, 0x00008000 ),
    gen_rr_dest_dep_test( 0, "srl", 0x0000f000, 0x0000000f, 0x00000001 ),
    gen_rr_dest_dep_test( 0, "srl", 0xf000f000, 0x0000000c, 0x000f000f ),
    gen_rr_dest_dep_test( 0, "srl", 0xf00ff000, 0x0000000c, 0x000f00ff ),
  ]

#-------------------------------------------------------------------------
# gen_src0_dep_test
#-------------------------------------------------------------------------

def gen_src0_dep_test():
  return [
    gen_rr_src0_dep_test( 5, "srl", 0x00000fff, 0x0000000f, 0x00000000 ),
    gen_rr_src0_dep_test( 4, "srl", 0x00000001, 0x00000001, 0x00000000 ),
    gen_rr_src0_dep_test( 3, "srl", 0xf0000000, 0x00000001, 0x78000000 ),
    gen_rr_src0_dep_test( 2, "srl", 0x0000ffff, 0x00000008, 0x000000ff ),
    gen_rr_src0_dep_test( 1, "srl", 0x0000ffff, 0x00000010, 0x00000000 ),
    gen_rr_src0_dep_test( 0, "srl", 0xffffffff, 0x00000010, 0x0000ffff ),
    gen_rr_src0_dep_test( 0, "srl", 0xffffffff, 0xffffffff, 0x00000001 ),
    gen_rr_src0_dep_test( 0, "srl", 0xffffffff, 0x0000001f, 0x00000001 ),
    gen_rr_src0_dep_test( 0, "srl", 0x0000000f, 0x00000020, 0x0000000f ),
    gen_rr_src0_dep_test( 0, "srl", 0x80000000, 0x0000001f, 0x00000001 ),
    gen_rr_src0_dep_test( 0, "srl", 0x8000f000, 0x00000010, 0x00008000 ),
    gen_rr_src0_dep_test( 0, "srl", 0x0000f000, 0x0000000f, 0x00000001 ),
    gen_rr_src0_dep_test( 0, "srl", 0xf000f000, 0x0000000c, 0x000f000f ),
    gen_rr_src0_dep_test( 0, "srl", 0xf00ff000, 0x0000000c, 0x000f00ff ),
  ]

#-------------------------------------------------------------------------
# gen_src1_dep_test
#-------------------------------------------------------------------------

def gen_src1_dep_test():
  return [
    gen_rr_src1_dep_test( 5, "srl", 0x00000fff, 0x0000000f, 0x00000000 ),
    gen_rr_src1_dep_test( 4, "srl", 0x00000001, 0x00000001, 0x00000000 ),
    gen_rr_src1_dep_test( 3, "srl", 0xf0000000, 0x00000001, 0x78000000 ),
    gen_rr_src1_dep_test( 2, "srl", 0x0000ffff, 0x00000008, 0x000000ff ),
    gen_rr_src1_dep_test( 1, "srl", 0x0000ffff, 0x00000010, 0x00000000 ),
    gen_rr_src1_dep_test( 0, "srl", 0xffffffff, 0x00000010, 0x0000ffff ),
    gen_rr_src1_dep_test( 0, "srl", 0xffffffff, 0xffffffff, 0x00000001 ),
    gen_rr_src1_dep_test( 0, "srl", 0xffffffff, 0x0000001f, 0x00000001 ),
    gen_rr_src1_dep_test( 0, "srl", 0x0000000f, 0x00000020, 0x0000000f ),
    gen_rr_src1_dep_test( 0, "srl", 0x80000000, 0x0000001f, 0x00000001 ),
    gen_rr_src1_dep_test( 0, "srl", 0x8000f000, 0x00000010, 0x00008000 ),
    gen_rr_src1_dep_test( 0, "srl", 0x0000f000, 0x0000000f, 0x00000001 ),
    gen_rr_src1_dep_test( 0, "srl", 0xf000f000, 0x0000000c, 0x000f000f ),
    gen_rr_src1_dep_test( 0, "srl", 0xf00ff000, 0x0000000c, 0x000f00ff ),
  ]

#-------------------------------------------------------------------------
# gen_srcs_dep_test
#-------------------------------------------------------------------------

def gen_srcs_dep_test():
  return [
    gen_rr_srcs_dep_test( 5, "srl", 0x00000fff, 0x0000000f, 0x00000000 ),
    gen_rr_srcs_dep_test( 4, "srl", 0x00000001, 0x00000001, 0x00000000 ),
    gen_rr_srcs_dep_test( 3, "srl", 0xf0000000, 0x00000001, 0x78000000 ),
    gen_rr_srcs_dep_test( 2, "srl", 0x0000ffff, 0x00000008, 0x000000ff ),
    gen_rr_srcs_dep_test( 1, "srl", 0x0000ffff, 0x00000010, 0x00000000 ),
    gen_rr_srcs_dep_test( 0, "srl", 0xffffffff, 0x00000010, 0x0000ffff ),
    gen_rr_srcs_dep_test( 0, "srl", 0xffffffff, 0xffffffff, 0x00000001 ),
    gen_rr_srcs_dep_test( 0, "srl", 0xffffffff, 0x0000001f, 0x00000001 ),
    gen_rr_srcs_dep_test( 0, "srl", 0x0000000f, 0x00000020, 0x0000000f ),
    gen_rr_srcs_dep_test( 0, "srl", 0x80000000, 0x0000001f, 0x00000001 ),
    gen_rr_srcs_dep_test( 0, "srl", 0x8000f000, 0x00000010, 0x00008000 ),
    gen_rr_srcs_dep_test( 0, "srl", 0x0000f000, 0x0000000f, 0x00000001 ),
    gen_rr_srcs_dep_test( 0, "srl", 0xf000f000, 0x0000000c, 0x000f000f ),
    gen_rr_srcs_dep_test( 0, "srl", 0xf00ff000, 0x0000000c, 0x000f00ff ),
  ]

#-------------------------------------------------------------------------
# gen_srcs_dest_test
#-------------------------------------------------------------------------

def gen_srcs_dest_test():
  return [
    gen_rr_src0_eq_dest_test( "srl", 0x00000f0f, 0x00000005, 0x00000078 ),
    gen_rr_src1_eq_dest_test( "srl", 0x00000f0f, 0x00000005, 0x00000078 ),
    gen_rr_src0_eq_src1_test( "srl", 0x000fffff, 0x00000000 ),
    gen_rr_src0_eq_src1_test( "srl", 0x0000000c, 0x00000000 ),
    gen_rr_src0_eq_src1_test( "srl", 0xffffffff, 0x00000001 ),
    gen_rr_src0_eq_src1_test( "srl", 0x80ff0000, 0x80ff0000 ),
    gen_rr_src0_eq_src1_test( "srl", 0x8000000f, 0x00010000 ),
    gen_rr_srcs_eq_dest_test( "srl", 0x000fffff, 0x00000000 ),
    gen_rr_srcs_eq_dest_test( "srl", 0x0000000c, 0x00000000 ),
    gen_rr_srcs_eq_dest_test( "srl", 0xffffffff, 0x00000001 ),
    gen_rr_srcs_eq_dest_test( "srl", 0x80ff0000, 0x80ff0000 ),
    gen_rr_srcs_eq_dest_test( "srl", 0x8000000f, 0x00010000 ),
  ]

#-------------------------------------------------------------------------
# gen_value_test
#-------------------------------------------------------------------------

def gen_value_test():
  return [
    gen_rr_value_test( "srl", 0xff00ff00, 0x0000000f, 0x0001fe01 ),
    gen_rr_value_test( "srl", 0x0ff00ff0, 0x0000000f, 0x00001fe0 ),
    gen_rr_value_test( "srl", 0x00ff00ff, 0x0000000a, 0x00003fc0 ),
    gen_rr_value_test( "srl", 0xffffffff, 0x0000001f, 0x00000001 ),
  ]


#-------------------------------------------------------------------------
# gen_random_test
#-------------------------------------------------------------------------

def gen_random_test():
  asm_code = []
  for i in xrange(100):
    src0 = Bits( 32, random.randint(0,0xffffffff) )
    src1 = Bits( 32, random.randint(0,0x0000001f) )
    dest = src0 >> src1
    asm_code.append( gen_rr_value_test( "srl", src0.uint(), src1.uint(), dest.uint() ) )
  return asm_code