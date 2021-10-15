#=========================================================================
# sra
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
    sra x3, x1, x2
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
    gen_rr_dest_dep_test( 5, "sra", 0x00000fff, 0x0000000f, 0x00000000 ),
    gen_rr_dest_dep_test( 4, "sra", 0x00000001, 0x00000001, 0x00000000 ),
    gen_rr_dest_dep_test( 3, "sra", 0xf0000000, 0x00000001, 0xf8000000 ),
    gen_rr_dest_dep_test( 2, "sra", 0x0000ffff, 0x00000008, 0x000000ff ),
    gen_rr_dest_dep_test( 1, "sra", 0x0000ffff, 0x00000010, 0x00000000 ),
    gen_rr_dest_dep_test( 0, "sra", 0xffffffff, 0x00000010, 0xffffffff ),
    gen_rr_dest_dep_test( 0, "sra", 0xffffffff, 0xffffffff, 0xffffffff ),
    gen_rr_dest_dep_test( 0, "sra", 0xffffffff, 0x0000001f, 0xffffffff ),
    gen_rr_dest_dep_test( 0, "sra", 0x0000000f, 0x00000020, 0x0000000f ),
    gen_rr_dest_dep_test( 0, "sra", 0x80000000, 0x0000001f, 0xffffffff ),
    gen_rr_dest_dep_test( 0, "sra", 0x8000f000, 0x00000010, 0xffff8000 ),
    gen_rr_dest_dep_test( 0, "sra", 0x0000f000, 0x0000000f, 0x00000001 ),
    gen_rr_dest_dep_test( 0, "sra", 0xf000f000, 0x0000000c, 0xffff000f ),
    gen_rr_dest_dep_test( 0, "sra", 0xf00ff000, 0x0000000c, 0xffff00ff ),
  ]

#-------------------------------------------------------------------------
# gen_src0_dep_test
#-------------------------------------------------------------------------

def gen_src0_dep_test():
  return [
    gen_rr_src0_dep_test( 5, "sra", 0x00000fff, 0x0000000f, 0x00000000 ),
    gen_rr_src0_dep_test( 4, "sra", 0x00000001, 0x00000001, 0x00000000 ),
    gen_rr_src0_dep_test( 3, "sra", 0xf0000000, 0x00000001, 0xf8000000 ),
    gen_rr_src0_dep_test( 2, "sra", 0x0000ffff, 0x00000008, 0x000000ff ),
    gen_rr_src0_dep_test( 1, "sra", 0x0000ffff, 0x00000010, 0x00000000 ),
    gen_rr_src0_dep_test( 0, "sra", 0xffffffff, 0x00000010, 0xffffffff ),
    gen_rr_src0_dep_test( 0, "sra", 0xffffffff, 0xffffffff, 0xffffffff ),
    gen_rr_src0_dep_test( 0, "sra", 0xffffffff, 0x0000001f, 0xffffffff ),
    gen_rr_src0_dep_test( 0, "sra", 0x0000000f, 0x00000020, 0x0000000f ),
    gen_rr_src0_dep_test( 0, "sra", 0x80000000, 0x0000001f, 0xffffffff ),
    gen_rr_src0_dep_test( 0, "sra", 0x8000f000, 0x00000010, 0xffff8000 ),
    gen_rr_src0_dep_test( 0, "sra", 0x0000f000, 0x0000000f, 0x00000001 ),
    gen_rr_src0_dep_test( 0, "sra", 0xf000f000, 0x0000000c, 0xffff000f ),
    gen_rr_src0_dep_test( 0, "sra", 0xf00ff000, 0x0000000c, 0xffff00ff ),
  ]

#-------------------------------------------------------------------------
# gen_src1_dep_test
#-------------------------------------------------------------------------

def gen_src1_dep_test():
  return [
    gen_rr_src1_dep_test( 5, "sra", 0x00000fff, 0x0000000f, 0x00000000 ),
    gen_rr_src1_dep_test( 4, "sra", 0x00000001, 0x00000001, 0x00000000 ),
    gen_rr_src1_dep_test( 3, "sra", 0xf0000000, 0x00000001, 0xf8000000 ),
    gen_rr_src1_dep_test( 2, "sra", 0x0000ffff, 0x00000008, 0x000000ff ),
    gen_rr_src1_dep_test( 1, "sra", 0x0000ffff, 0x00000010, 0x00000000 ),
    gen_rr_src1_dep_test( 0, "sra", 0xffffffff, 0x00000010, 0xffffffff ),
    gen_rr_src1_dep_test( 0, "sra", 0xffffffff, 0xffffffff, 0xffffffff ),
    gen_rr_src1_dep_test( 0, "sra", 0xffffffff, 0x0000001f, 0xffffffff ),
    gen_rr_src1_dep_test( 0, "sra", 0x0000000f, 0x00000020, 0x0000000f ),
    gen_rr_src1_dep_test( 0, "sra", 0x80000000, 0x0000001f, 0xffffffff ),
    gen_rr_src1_dep_test( 0, "sra", 0x8000f000, 0x00000010, 0xffff8000 ),
    gen_rr_src1_dep_test( 0, "sra", 0x0000f000, 0x0000000f, 0x00000001 ),
    gen_rr_src1_dep_test( 0, "sra", 0xf000f000, 0x0000000c, 0xffff000f ),
    gen_rr_src1_dep_test( 0, "sra", 0xf00ff000, 0x0000000c, 0xffff00ff ),
  ]

#-------------------------------------------------------------------------
# gen_srcs_dep_test
#-------------------------------------------------------------------------

def gen_srcs_dep_test():
  return [
    gen_rr_srcs_dep_test( 5, "sra", 0x00000fff, 0x0000000f, 0x00000000 ),
    gen_rr_srcs_dep_test( 4, "sra", 0x00000001, 0x00000001, 0x00000000 ),
    gen_rr_srcs_dep_test( 3, "sra", 0xf0000000, 0x00000001, 0xf8000000 ),
    gen_rr_srcs_dep_test( 2, "sra", 0x0000ffff, 0x00000008, 0x000000ff ),
    gen_rr_srcs_dep_test( 1, "sra", 0x0000ffff, 0x00000010, 0x00000000 ),
    gen_rr_srcs_dep_test( 0, "sra", 0xffffffff, 0x00000010, 0xffffffff ),
    gen_rr_srcs_dep_test( 0, "sra", 0xffffffff, 0xffffffff, 0xffffffff ),
    gen_rr_srcs_dep_test( 0, "sra", 0xffffffff, 0x0000001f, 0xffffffff ),
    gen_rr_srcs_dep_test( 0, "sra", 0x0000000f, 0x00000020, 0x0000000f ),
    gen_rr_srcs_dep_test( 0, "sra", 0x80000000, 0x0000001f, 0xffffffff ),
    gen_rr_srcs_dep_test( 0, "sra", 0x8000f000, 0x00000010, 0xffff8000 ),
    gen_rr_srcs_dep_test( 0, "sra", 0x0000f000, 0x0000000f, 0x00000001 ),
    gen_rr_srcs_dep_test( 0, "sra", 0xf000f000, 0x0000000c, 0xffff000f ),
    gen_rr_srcs_dep_test( 0, "sra", 0xf00ff000, 0x0000000c, 0xffff00ff ),
  ]

#-------------------------------------------------------------------------
# gen_srcs_dest_test
#-------------------------------------------------------------------------

def gen_srcs_dest_test():
  return [
    gen_rr_src0_eq_dest_test( "sra", 0x00000f0f, 0x00000005, 0x00000078 ),
    gen_rr_src1_eq_dest_test( "sra", 0x00000f0f, 0x00000005, 0x00000078 ),
    gen_rr_src0_eq_src1_test( "sra", 0x000fffff, 0x00000000 ),
    gen_rr_src0_eq_src1_test( "sra", 0x0000000c, 0x00000000 ),
    gen_rr_src0_eq_src1_test( "sra", 0xffffffff, 0xffffffff ),
    gen_rr_src0_eq_src1_test( "sra", 0x80ff0000, 0x80ff0000 ),
    gen_rr_src0_eq_src1_test( "sra", 0x8000000f, 0xffff0000 ),
    gen_rr_srcs_eq_dest_test( "sra", 0x000fffff, 0x00000000 ),
    gen_rr_srcs_eq_dest_test( "sra", 0x0000000c, 0x00000000 ),
    gen_rr_srcs_eq_dest_test( "sra", 0xffffffff, 0xffffffff ),
    gen_rr_srcs_eq_dest_test( "sra", 0x80ff0000, 0x80ff0000 ),
    gen_rr_srcs_eq_dest_test( "sra", 0x8000000f, 0xffff0000 ),
  ]

#-------------------------------------------------------------------------
# gen_value_test
#-------------------------------------------------------------------------

def gen_value_test():
  return [
    gen_rr_value_test( "sra", 0xff00ff00, 0x0000000f, 0xfffffe01 ),
    gen_rr_value_test( "sra", 0x0ff00ff0, 0x0000000f, 0x00001fe0 ),
    gen_rr_value_test( "sra", 0x00ff00ff, 0x0000000a, 0x00003fc0 ),
    gen_rr_value_test( "sra", 0xffffffff, 0x0000001f, 0xffffffff ),
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
    src1 = Bits( 32, random.randint(0,0x0000001f) )
    dest = Bits( 32, sra(src0.uint(), src1.uint()))
    asm_code.append( gen_rr_value_test( "sra", src0.uint(), src1.uint(), dest.uint() ) )
  return asm_code