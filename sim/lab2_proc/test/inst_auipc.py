#=========================================================================
# auipc
#=========================================================================

import random

from pymtl import *
from inst_utils import *

#-------------------------------------------------------------------------
# gen_basic_test
#-------------------------------------------------------------------------

def gen_basic_test():
  return """
    auipc x1, 0x00010                       # PC=0x200
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    csrw  proc2mngr, x1 > 0x00010200
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
# lui_imm_dest_dep_test
#-------------------------------------------------------------------------

def auipc_imm_dest_dep_test():
  return [
    gen_imm_dest_dep_test( 5, "auipc", 0x00000001, 0x00001000 + 0x200  ),
    gen_imm_dest_dep_test( 4, "auipc", 0x0000000f, 0x0000f000 + 0x21c ),
    gen_imm_dest_dep_test( 3, "auipc", 0x0000ffff, 0x0ffff000 + 0x234 ),
    gen_imm_dest_dep_test( 2, "auipc", 0x000fffff, 0xfffff000 + 0x248 ),  
    gen_imm_dest_dep_test( 1, "auipc", 0x000bcdef, 0xbcdef000 + 0x258 ),
    gen_imm_dest_dep_test( 0, "auipc", 0x00000002, 0x00002000 + 0x264 ),           
  ]

#-------------------------------------------------------------------------
# lui_imm_value_test
#-------------------------------------------------------------------------

def auipc_imm_value_test():
  return [
    gen_imm_value_test( "auipc", 0x00000001, 0x00001000 + 0x200 ),
    gen_imm_value_test( "auipc", 0x0000000f, 0x0000f000 + 0x208 ),
    gen_imm_value_test( "auipc", 0x0000ffff, 0x0ffff000 + 0x210 ),
    gen_imm_value_test( "auipc", 0x000fffff, 0xfffff000 + 0x218 ),  
    gen_imm_value_test( "auipc", 0x000bcdef, 0xbcdef000 + 0x220 ),
    gen_imm_value_test( "auipc", 0x00000002, 0x00002000 + 0x228 ),    

    gen_imm_value_test( "auipc", 0x00000000, 0x00000000 + 0x230 ),
    gen_imm_value_test( "auipc", 0x000f000f, 0xf000f000 + 0x238 ),
    gen_imm_value_test( "auipc", 0x00045678, 0x45678000 + 0x240 ),
    gen_imm_value_test( "auipc", 0x000babab, 0xbabab000 + 0x248 ),  
  ]

#-------------------------------------------------------------------------
# gen_random_test
#-------------------------------------------------------------------------

def gen_random_test():
  asm_code = []
  for i in xrange(100):
    src0 = Bits( 32, random.randint(0,0x000fffff) )
    dest = src0 << 0xc
    asm_code.append( gen_imm_value_test( "auipc", src0.uint(), dest.uint() + 0x200 + (8 * i)) )
  return asm_code