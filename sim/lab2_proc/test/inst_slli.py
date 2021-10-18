#=========================================================================
# slli
#=========================================================================

import random

from pymtl import *
from inst_utils import *

#-------------------------------------------------------------------------
# gen_basic_test
#-------------------------------------------------------------------------

def gen_basic_test():
  return """
    csrr x1, mngr2proc < 0x80008000
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    slli x3, x1, 0x03
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    csrw proc2mngr, x3 > 0x00040000
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
    gen_rimm_dest_dep_test( 5, "sll", 0x00000fff, 0x0000000f, 0x07ff8000 ),
    gen_rimm_dest_dep_test( 4, "sll", 0x00000001, 0x00000001, 0x00000002 ),
    gen_rimm_dest_dep_test( 3, "sll", 0xf0000000, 0x00000001, 0xe0000000 ),
    gen_rimm_dest_dep_test( 2, "sll", 0x0000ffff, 0x00000008, 0x00ffff00 ),
    gen_rimm_dest_dep_test( 1, "sll", 0x0000ffff, 0x00000010, 0xffff0000 ),
    gen_rimm_dest_dep_test( 0, "sll", 0xffffffff, 0x00000010, 0xffff0000 ),
    gen_rimm_dest_dep_test( 0, "sll", 0xffffffff, 0x0000001f, 0x80000000 ),
    gen_rimm_dest_dep_test( 0, "sll", 0xffffffff, 0x0000001f, 0x80000000 ),
    gen_rimm_dest_dep_test( 0, "sll", 0xffffffff, 0x00000000, 0xffffffff ),
    gen_rimm_dest_dep_test( 0, "sll", 0x00000001, 0x0000001f, 0x80000000 ),
    gen_rimm_dest_dep_test( 0, "sll", 0x00000002, 0x0000001f, 0x00000000 ),
    gen_rimm_dest_dep_test( 0, "sll", 0x0000f000, 0x00000008, 0x00f00000 ),
  ]

#-------------------------------------------------------------------------
# gen_src0_dep_test
#-------------------------------------------------------------------------

def gen_src0_dep_test():
  return [
    gen_rimm_src_dep_test( 5, "sll", 0x00000fff, 0x0000000f, 0x07ff8000 ),
    gen_rimm_src_dep_test( 4, "sll", 0x00000001, 0x00000001, 0x00000002 ),
    gen_rimm_src_dep_test( 3, "sll", 0xf0000000, 0x00000001, 0xe0000000 ),
    gen_rimm_src_dep_test( 2, "sll", 0x0000ffff, 0x00000008, 0x00ffff00 ),
    gen_rimm_src_dep_test( 1, "sll", 0x0000ffff, 0x00000010, 0xffff0000 ),
    gen_rimm_src_dep_test( 0, "sll", 0xffffffff, 0x00000010, 0xffff0000 ),
    gen_rimm_src_dep_test( 0, "sll", 0xffffffff, 0x0000001f, 0x80000000 ),
    gen_rimm_src_dep_test( 0, "sll", 0xffffffff, 0x0000001f, 0x80000000 ),
    gen_rimm_src_dep_test( 0, "sll", 0xffffffff, 0x00000000, 0xffffffff ),
    gen_rimm_src_dep_test( 0, "sll", 0x00000001, 0x0000001f, 0x80000000 ),
    gen_rimm_src_dep_test( 0, "sll", 0x00000002, 0x0000001f, 0x00000000 ),
    gen_rimm_src_dep_test( 0, "sll", 0x0000f000, 0x00000008, 0x00f00000 ),
  ]

#-------------------------------------------------------------------------
# gen_srcs_dest_test
#-------------------------------------------------------------------------

def gen_srcs_dest_test():
  return [
    gen_rimm_src_eq_dest_test( "sll", 0x00000f0f, 0x00000005, 0x0001e1e0 ),
    gen_rimm_src_eq_dest_test( "sll", 0x00000f0f, 0x0000001f, 0x00000000 ),
    gen_rimm_src_eq_dest_test( "sll", 0xf0000f0f, 0x0000001f, 0x00000001 ),
  ]

#-------------------------------------------------------------------------
# gen_value_test
#-------------------------------------------------------------------------

def gen_value_test():
  return [
    gen_rimm_value_test( "sll", 0xff00ff00, 0x0000000f, 0x7f800000 ),
    gen_rimm_value_test( "sll", 0x0ff00ff0, 0x0000000f, 0x07f80000 ),
    gen_rimm_value_test( "sll", 0x00ff00ff, 0x0000000a, 0xfc03fc00 ),
    gen_rimm_value_test( "sll", 0xffffffff, 0x0000001f, 0x80000000 ),
  ]


#-------------------------------------------------------------------------
# gen_random_test
#-------------------------------------------------------------------------

def gen_random_test():
  asm_code = []
  for i in xrange(100):
    src0 = Bits( 32, random.randint(0,0xffffffff) )
    src1 = Bits( 5, random.randint(0,0x0000001f) )
    dest = src0 << src1
    asm_code.append( gen_rimm_value_test( "slli", src0.uint(), src1.uint(), dest.uint() ) )
  return asm_code