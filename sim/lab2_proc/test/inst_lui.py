#=========================================================================
# lui
#=========================================================================

import random

from pymtl import *
from inst_utils import *

#-------------------------------------------------------------------------
# gen_basic_test
#-------------------------------------------------------------------------

def gen_basic_test():
  return """
    lui x1, 0x0001
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    csrw proc2mngr, x1 > 0x00001000
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

def lui_imm_dest_dep_test():
  return [
    gen_imm_dest_dep_test( 5, "lui", 0x00000001, 0x00001000 ),
    gen_imm_dest_dep_test( 4, "lui", 0x0000000f, 0x0000f000 ),
    gen_imm_dest_dep_test( 3, "lui", 0x0000ffff, 0x0ffff000 ),
    gen_imm_dest_dep_test( 2, "lui", 0x000fffff, 0xfffff000 ),  
    gen_imm_dest_dep_test( 1, "lui", 0x000bcdef, 0xbcdef000 ),
    gen_imm_dest_dep_test( 0, "lui", 0x00000002, 0x00002000 ),           
  ]

#-------------------------------------------------------------------------
# lui_imm_value_test
#-------------------------------------------------------------------------

def lui_imm_value_test():
  return [
    gen_imm_value_test( "lui", 0x00000001, 0x00001000 ),
    gen_imm_value_test( "lui", 0x0000000f, 0x0000f000 ),
    gen_imm_value_test( "lui", 0x0000ffff, 0x0ffff000 ),
    gen_imm_value_test( "lui", 0x0000fffff, 0xfffff000 ),  
    gen_imm_value_test( "lui", 0x000bcdef, 0xbcdef000 ),
    gen_imm_value_test( "lui", 0x00000002, 0x00002000 ),    

    gen_imm_value_test( "lui", 0x0000000, 0x00000000 ),
    gen_imm_value_test( "lui", 0x000f000f, 0xf000f000 ),
    gen_imm_value_test( "lui", 0x00045678, 0x45678000 ),
    gen_imm_value_test( "lui", 0x000babab, 0xbabab000 ),  
  ]

#-------------------------------------------------------------------------
# gen_random_test
#-------------------------------------------------------------------------

def gen_random_test():
  asm_code = []
  for i in xrange(100):
    src0 = Bits( 32, random.randint(0,0x000fffff) )
    dest = src0 << 0xc
    asm_code.append( gen_imm_value_test( "lui", src0.uint(), dest.uint() ) )
  return asm_code