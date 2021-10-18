#=========================================================================
# srli
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
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    srli x3, x1, 0x03
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
    gen_rimm_dest_dep_test( 5, "srli", 0x00000fff, 0x0000000f, 0x00000000 ),
    gen_rimm_dest_dep_test( 4, "srli", 0x00000001, 0x00000001, 0x00000000 ),
    gen_rimm_dest_dep_test( 3, "srli", 0xf0000000, 0x00000001, 0x78000000 ),
    gen_rimm_dest_dep_test( 2, "srli", 0x0000ffff, 0x00000008, 0x000000ff ),
    gen_rimm_dest_dep_test( 1, "srli", 0x0000ffff, 0x00000010, 0x00000000 ),
    gen_rimm_dest_dep_test( 0, "srli", 0xffffffff, 0x00000010, 0x0000ffff ),
    gen_rimm_dest_dep_test( 0, "srli", 0xffffffff, 0x0000001f, 0x00000001 ),
    gen_rimm_dest_dep_test( 0, "srli", 0x0000000f, 0x00000000, 0x0000000f ),
    gen_rimm_dest_dep_test( 0, "srli", 0x80000000, 0x0000001f, 0x00000001 ),
    gen_rimm_dest_dep_test( 0, "srli", 0x8000f000, 0x00000010, 0x00008000 ),
    gen_rimm_dest_dep_test( 0, "srli", 0x0000f000, 0x0000000f, 0x00000001 ),
    gen_rimm_dest_dep_test( 0, "srli", 0xf000f000, 0x0000000c, 0x000f000f ),
    gen_rimm_dest_dep_test( 0, "srli", 0xf00ff000, 0x0000000c, 0x000f00ff ),
  ]

#-------------------------------------------------------------------------
# gen_src_dep_test
#-------------------------------------------------------------------------

def gen_src_dep_test():
  return [
    gen_rimm_src_dep_test( 5, "srli", 0x00000fff, 0x0000000f, 0x00000000 ),
    gen_rimm_src_dep_test( 4, "srli", 0x00000001, 0x00000001, 0x00000000 ),
    gen_rimm_src_dep_test( 3, "srli", 0xf0000000, 0x00000001, 0x78000000 ),
    gen_rimm_src_dep_test( 2, "srli", 0x0000ffff, 0x00000008, 0x000000ff ),
    gen_rimm_src_dep_test( 1, "srli", 0x0000ffff, 0x00000010, 0x00000000 ),
    gen_rimm_src_dep_test( 0, "srli", 0xffffffff, 0x00000010, 0x0000ffff ),
    gen_rimm_src_dep_test( 0, "srli", 0xffffffff, 0x0000001f, 0x00000001 ),
    gen_rimm_src_dep_test( 0, "srli", 0x0000000f, 0x00000000, 0x0000000f ),
    gen_rimm_src_dep_test( 0, "srli", 0x80000000, 0x0000001f, 0x00000001 ),
    gen_rimm_src_dep_test( 0, "srli", 0x8000f000, 0x00000010, 0x00008000 ),
    gen_rimm_src_dep_test( 0, "srli", 0x0000f000, 0x0000000f, 0x00000001 ),
    gen_rimm_src_dep_test( 0, "srli", 0xf000f000, 0x0000000c, 0x000f000f ),
    gen_rimm_src_dep_test( 0, "srli", 0xf00ff000, 0x0000000c, 0x000f00ff ),
  ]


#-------------------------------------------------------------------------
# gen_srcs_dest_test
#-------------------------------------------------------------------------

def gen_srcs_dest_test():
  return [
    gen_rimm_src_eq_dest_test( "srli", 0x00000f0f, 0x00000005, 0x00000078 ),
    gen_rimm_src_eq_dest_test( "srli", 0xff00ff00, 0x0000000f, 0x0001fe01 ),
    gen_rimm_src_eq_dest_test( "srli", 0xffffffff, 0x0000001f, 0x00000001 ),
    gen_rimm_src_eq_dest_test( "srli", 0x0000000f, 0x00000000, 0x0000000f ),
    gen_rimm_src_eq_dest_test( "srli", 0x80000000, 0x0000001f, 0x00000001 ),
    gen_rimm_src_eq_dest_test( "srli", 0x8000f000, 0x00000010, 0x00008000 ),
  ]

#-------------------------------------------------------------------------
# gen_value_test
#-------------------------------------------------------------------------

def gen_value_test():
  return [
    gen_rimm_value_test( "srli", 0xff00ff00, 0x0000000f, 0x0001fe01 ),
    gen_rimm_value_test( "srli", 0x0ff00ff0, 0x0000000f, 0x00001fe0 ),
    gen_rimm_value_test( "srli", 0x00ff00ff, 0x0000000a, 0x00003fc0 ),
    gen_rimm_value_test( "srli", 0xffffffff, 0x0000001f, 0x00000001 ),
  ]


#-------------------------------------------------------------------------
# gen_random_test
#-------------------------------------------------------------------------

def gen_random_test():
  asm_code = []
  for i in xrange(100):
    src0 = Bits( 32, random.randint(0,0xffffffff) )
    src1 = Bits( 5, random.randint(0,0x0000001f) )
    dest = src0 >> src1
    asm_code.append( gen_rimm_value_test( "srli", src0.uint(), src1.uint(), dest.uint() ) )
  return asm_code