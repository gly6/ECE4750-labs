#=========================================================================
# addi
#=========================================================================

import random

from pymtl                import *
from inst_utils import *

#-------------------------------------------------------------------------
# gen_basic_test
#-------------------------------------------------------------------------

def gen_basic_test():
  return """

    csrr x1, mngr2proc, < 5
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    addi x3, x1, 0x0004
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    csrw proc2mngr, x3 > 9
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
    gen_rimm_dest_dep_test( 5, "addi", 1, 1, 2 ),
    gen_rimm_dest_dep_test( 4, "addi", 2, 1, 3 ),
    gen_rimm_dest_dep_test( 3, "addi", 3, 1, 4 ),
    gen_rimm_dest_dep_test( 2, "addi", 4, 1, 5 ),
    gen_rimm_dest_dep_test( 1, "addi", 5, 1, 6 ),
    gen_rimm_dest_dep_test( 0, "addi", 6, 1, 7 ),
    gen_rimm_dest_dep_test( 0, "addi", 6, 5, 11 ),
    gen_rimm_dest_dep_test( 0, "addi", 0x03, 0x01, 0x04),
    gen_rimm_dest_dep_test( 0, "addi", -2, 5, 3),
    gen_rimm_dest_dep_test( 0, "addi", -10, 30, 20),
    gen_rimm_dest_dep_test( 5, "addi", 1, 1, 2 ),
    gen_rimm_dest_dep_test( 4, "addi", 2, 1, 3 ),
    gen_rimm_dest_dep_test( 3, "addi", 3, 1, 4 ),
    gen_rimm_dest_dep_test( 2, "addi", 4, 1, 5 ),
    gen_rimm_dest_dep_test( 1, "addi", 5, 1, 6 ),
    gen_rimm_dest_dep_test( 0, "addi", 6, 1, 7 ),
    gen_rimm_dest_dep_test( 0, "addi", 6, 5, 11 ),
    gen_rimm_dest_dep_test( 0, "addi", 1, 0, 1),
    gen_rimm_dest_dep_test( 0, "addi", 0, 1, 1),
    gen_rimm_dest_dep_test( 0, "addi", 0x000000A4, 0xF, 0x000000B3),
    gen_rimm_dest_dep_test( 0, "addi", 0x000000B1, 0xD5, 0x00000186),
    gen_rimm_dest_dep_test( 0, "addi", 0x000000FF, 0xFF, 0x000001FE),
    gen_rimm_dest_dep_test( 0, "addi", 0xFFFFFFFF, 0xFF, 0x000000FE),
    gen_rimm_dest_dep_test( 0, "addi", 0xFFFFFF00, 0xFF, 0xFFFFFFFF),
    gen_rimm_dest_dep_test( 0, "addi", 0xFFFFFF01, 0xFF, 0x00000000),
    gen_rimm_dest_dep_test( 0, "addi", 0xFFFFFFFF, 0x7FF, 0x000007FE),
  ]

#-------------------------------------------------------------------------
# gen_src_dep_test
#-------------------------------------------------------------------------

def gen_src_dep_test():
  return [
    gen_rimm_src_dep_test( 5, "addi", 1, 1, 2 ),
    gen_rimm_src_dep_test( 4, "addi", 2, 1, 3 ),
    gen_rimm_src_dep_test( 3, "addi", 3, 1, 4 ),
    gen_rimm_src_dep_test( 2, "addi", 4, 1, 5 ),
    gen_rimm_src_dep_test( 1, "addi", 5, 1, 6 ),
    gen_rimm_src_dep_test( 0, "addi", 6, 1, 7 ),
    gen_rimm_src_dep_test( 0, "addi", 6, 5, 11 ),
    gen_rimm_src_dep_test( 0, "addi", 0x03, 0x01, 0x04),
    gen_rimm_src_dep_test( 0, "addi", -2, 5, 3),
    gen_rimm_src_dep_test( 0, "addi", -10, 30, 20),
    gen_rimm_src_dep_test( 5, "addi", 1, 1, 2 ),
    gen_rimm_src_dep_test( 4, "addi", 2, 1, 3 ),
    gen_rimm_src_dep_test( 3, "addi", 3, 1, 4 ),
    gen_rimm_src_dep_test( 2, "addi", 4, 1, 5 ),
    gen_rimm_src_dep_test( 1, "addi", 5, 1, 6 ),
    gen_rimm_src_dep_test( 0, "addi", 6, 1, 7 ),
    gen_rimm_src_dep_test( 0, "addi", 6, 5, 11 ),
    gen_rimm_src_dep_test( 0, "addi", 1, 0, 1),
    gen_rimm_src_dep_test( 0, "addi", 0, 1, 1),
    gen_rimm_src_dep_test( 0, "addi", 0x000000A4, 0xF, 0x000000B3),
    gen_rimm_src_dep_test( 0, "addi", 0x000000B1, 0xD5, 0x00000186),
    gen_rimm_src_dep_test( 0, "addi", 0x000000FF, 0xFF, 0x000001FE),
    gen_rimm_src_dep_test( 0, "addi", 0xFFFFFFFF, 0xFF, 0x000000FE),
    gen_rimm_src_dep_test( 0, "addi", 0xFFFFFF00, 0xFF, 0xFFFFFFFF),
    gen_rimm_src_dep_test( 0, "addi", 0xFFFFFF01, 0xFF, 0x00000000),
    gen_rimm_src_dep_test( 0, "addi", 0xFFFFFFFF, 0x7FF, 0x000007FE),
  ]


#-------------------------------------------------------------------------
# gen_srcs_dest_test
#-------------------------------------------------------------------------

def gen_srcs_dest_test():
  return [
    gen_rimm_src_eq_dest_test( "addi", 25, 1, 26 ),
    gen_rimm_src_eq_dest_test( "addi", -25, 25, 0 ),
    gen_rimm_src_eq_dest_test( "addi", 26, 10, 36 ),
    gen_rimm_src_eq_dest_test( "addi", 0xffffffff, 0x7ff, 0x7fe ),
  ]

#-------------------------------------------------------------------------
# gen_value_test
#-------------------------------------------------------------------------

def gen_value_test():
  return [

    gen_rimm_value_test( "addi", 0x00000000, 0x00000000, 0x00000000 ),
    gen_rimm_value_test( "addi", 0x00000001, 0x00000001, 0x00000002 ),
    gen_rimm_value_test( "addi", 0x00000003, 0x00000007, 0x0000000a ),

    gen_rimm_value_test( "addi", 0xffff8000, 0x00000000, 0xffff8000 ),
    gen_rimm_value_test( "addi", 0x80000000, 0x00000000, 0x80000000 ),
    gen_rimm_value_test( "addi", 0x80000000, 0x000007ff, 0x800007ff ),

    gen_rimm_value_test( "addi", 0x00000000, 0x000007ff, 0x000007ff ),
    gen_rimm_value_test( "addi", 0x7fffffff, 0x00000000, 0x7fffffff ),
    gen_rimm_value_test( "addi", 0x7fffffff, 0x000007ff, 0x800007fe ),

    gen_rimm_value_test( "addi", 0x80000000, 0x000007ff, 0x800007ff ),
    gen_rimm_value_test( "addi", 0x7fffffff, 0x00000010, 0x8000000f ),

    gen_rimm_value_test( "addi", 0x00000000, 0x000001cc, 0x000001cc ),
    gen_rimm_value_test( "addi", 0xffffffff, 0x00000001, 0x00000000 ),
    gen_rimm_value_test( "addi", 0xffffffff, 0x000000ff, 0x000000fe ),

  ]

#-------------------------------------------------------------------------
# gen_random_test
#-------------------------------------------------------------------------

def gen_random_test():
  asm_code = []
  for i in xrange(100):
    src0 = Bits( 32, random.randint(0,0xffffffff) )
    src1 = Bits( 32, random.randint(0,0x000007ff) )
    dest = src0 + src1
    asm_code.append( gen_rimm_value_test( "addi", src0.uint(), src1.uint(), dest.uint() ) )
  return asm_code