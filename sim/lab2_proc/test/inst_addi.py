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
    gen_rimm_dest_dep_test( 0, "addi", -10, 30, 20),
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
    gen_rimm_dest_dep_test( 0, "addi", 1, 0, 1),
    gen_rimm_dest_dep_test( 0, "addi", 0, 1, 1),
    gen_rimm_dest_dep_test( 0, "addi", 0x000000A4, 0x0000000F, 0x000000B3),
    gen_rimm_dest_dep_test( 0, "addi", 0x000000B1, 0x000000D5, 0x00000186),
    gen_rimm_dest_dep_test( 0, "addi", 0x000000FF, 0x000000FF, 0x000001FE),
    gen_rimm_dest_dep_test( 0, "addi", 0xFFFFFFFF, 0xFFFFFFFF, 0xFFFFFFFE),
    gen_rimm_dest_dep_test( 0, "addi", 0xFFFFFFFF, 0xFFFFFFFF, 0xFFFFFFFE),
    gen_rimm_dest_dep_test( 0, "addi", 0xEDEDEDED, 0xBABABABA, 0xA8A8A8A7),
  ]