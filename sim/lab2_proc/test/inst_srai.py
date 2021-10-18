#=========================================================================
# srai
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
    srai x3, x1, 0x03
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
    gen_rimm_dest_dep_test( 5, "srai", 0x00000fff, 0x0000000f, 0x00000000 ),
    gen_rimm_dest_dep_test( 4, "srai", 0x00000001, 0x00000001, 0x00000000 ),
    gen_rimm_dest_dep_test( 3, "srai", 0xf0000000, 0x00000001, 0xf8000000 ),
    gen_rimm_dest_dep_test( 2, "srai", 0x0000ffff, 0x00000008, 0x000000ff ),
    gen_rimm_dest_dep_test( 1, "srai", 0x0000ffff, 0x00000010, 0x00000000 ),
    gen_rimm_dest_dep_test( 0, "srai", 0xffffffff, 0x00000010, 0xffffffff ),
    gen_rimm_dest_dep_test( 0, "srai", 0xffffffff, 0x0000001f, 0xffffffff ),
    gen_rimm_dest_dep_test( 0, "srai", 0xffffffff, 0x0000001f, 0xffffffff ),
    gen_rimm_dest_dep_test( 0, "srai", 0x0000000f, 0x00000000, 0x0000000f ),
    gen_rimm_dest_dep_test( 0, "srai", 0x80000000, 0x0000001f, 0xffffffff ),
    gen_rimm_dest_dep_test( 0, "srai", 0x8000f000, 0x00000010, 0xffff8000 ),
    gen_rimm_dest_dep_test( 0, "srai", 0x0000f000, 0x0000000f, 0x00000001 ),
    gen_rimm_dest_dep_test( 0, "srai", 0xf000f000, 0x0000000c, 0xffff000f ),
    gen_rimm_dest_dep_test( 0, "srai", 0xf00ff000, 0x0000000c, 0xffff00ff ),
  ]

#-------------------------------------------------------------------------
# gen_src_dep_test
#-------------------------------------------------------------------------

def gen_src_dep_test():
  return [
    gen_rimm_src_dep_test( 5, "srai", 0x00000fff, 0x0000000f, 0x00000000 ),
    gen_rimm_src_dep_test( 4, "srai", 0x00000001, 0x00000001, 0x00000000 ),
    gen_rimm_src_dep_test( 3, "srai", 0xf0000000, 0x00000001, 0xf8000000 ),
    gen_rimm_src_dep_test( 2, "srai", 0x0000ffff, 0x00000008, 0x000000ff ),
    gen_rimm_src_dep_test( 1, "srai", 0x0000ffff, 0x00000010, 0x00000000 ),
    gen_rimm_src_dep_test( 0, "srai", 0xffffffff, 0x00000010, 0xffffffff ),
    gen_rimm_src_dep_test( 0, "srai", 0xffffffff, 0x0000001f, 0xffffffff ),
    gen_rimm_src_dep_test( 0, "srai", 0xffffffff, 0x0000001f, 0xffffffff ),
    gen_rimm_src_dep_test( 0, "srai", 0x0000000f, 0x00000000, 0x0000000f ),
    gen_rimm_src_dep_test( 0, "srai", 0x80000000, 0x0000001f, 0xffffffff ),
    gen_rimm_src_dep_test( 0, "srai", 0x8000f000, 0x00000010, 0xffff8000 ),
    gen_rimm_src_dep_test( 0, "srai", 0x0000f000, 0x0000000f, 0x00000001 ),
    gen_rimm_src_dep_test( 0, "srai", 0xf000f000, 0x0000000c, 0xffff000f ),
    gen_rimm_src_dep_test( 0, "srai", 0xf00ff000, 0x0000000c, 0xffff00ff ),
  ]


#-------------------------------------------------------------------------
# gen_srcs_dest_test
#-------------------------------------------------------------------------

def gen_srcs_dest_test():
  return [
    gen_rimm_src_eq_dest_test( "srai", 0x00000f0f, 0x00000005, 0x00000078 ),
    gen_rimm_src_eq_dest_test( "srai", 0xff00ff00, 0x0000000f, 0xfffffe01 ),
    gen_rimm_src_eq_dest_test( "srai", 0xffffffff, 0x0000001f, 0xffffffff ),
    gen_rimm_src_eq_dest_test( "srai", 0xffffffff, 0x0000001f, 0xffffffff ),
    gen_rimm_src_eq_dest_test( "srai", 0x0000000f, 0x00000000, 0x0000000f ),
    gen_rimm_src_eq_dest_test( "srai", 0x80000000, 0x0000001f, 0xffffffff ),
    gen_rimm_src_eq_dest_test( "srai", 0x8000f000, 0x00000010, 0xffff8000 ),
  ]

#-------------------------------------------------------------------------
# gen_value_test
#-------------------------------------------------------------------------

def gen_value_test():
  return [
    gen_rimm_value_test( "srai", 0xff00ff00, 0x0000000f, 0xfffffe01 ),
    gen_rimm_value_test( "srai", 0x0ff00ff0, 0x0000000f, 0x00001fe0 ),
    gen_rimm_value_test( "srai", 0x00ff00ff, 0x0000000a, 0x00003fc0 ),
    gen_rimm_value_test( "srai", 0xffffffff, 0x0000001f, 0xffffffff ),
  ]


#-------------------------------------------------------------------------
# gen_random_test
#-------------------------------------------------------------------------

# Right arithmetic bit shift python code inspired by stack overflow post
# https://stackoverflow.com/questions/64963170/how-to-do-arithmetic-right-shift-in-python-for-signed-and-unsigned-values

def sra(x,m):
    if x & 2**(31) != 0:  # MSB is 1, i.e. x is negative
        fillerString = str('1'*m + '0'*(32-m))
        filler = int(fillerString, 2)
        x = (x >> m) | filler  # fill in 0's with 1's
        return x
    else:
        return x >> m

def gen_random_test():
  asm_code = []
  for i in xrange(100):
    src0 = Bits( 32, random.randint(0,0xffffffff) )
    src1 = Bits( 5, random.randint(0,0x0000001f) )
    dest = Bits( 32, sra(src0.uint(), src1.uint()))
    asm_code.append( gen_rimm_value_test( "srai", src0.uint(), src1.uint(), dest.uint() ) )
  return asm_code