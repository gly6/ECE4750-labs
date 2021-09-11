#=========================================================================
# IntMulFL_test
#=========================================================================

import pytest
import random

random.seed(0xdeadbeef)

from pymtl      import *
from pclib.test import mk_test_case_table, run_sim
from pclib.test import TestSource, TestSink

from lab1_imul.IntMulFL   import IntMulFL

#-------------------------------------------------------------------------
# TestHarness
#-------------------------------------------------------------------------

class TestHarness (Model):

  def __init__( s, imul, src_msgs, sink_msgs,
                src_delay, sink_delay,
                dump_vcd=False, test_verilog=False ):

    # Instantiate models

    s.src  = TestSource ( Bits(64), src_msgs,  src_delay  )
    s.imul = imul
    s.sink = TestSink   ( Bits(32), sink_msgs, sink_delay )

    # Dump VCD

    if dump_vcd:
      s.imul.vcd_file = dump_vcd

    # Translation

    if test_verilog:
      s.imul = TranslationTool( s.imul )

    # Connect

    s.connect( s.src.out,  s.imul.req  )
    s.connect( s.imul.resp, s.sink.in_ )

  def done( s ):
    return s.src.done and s.sink.done

  def line_trace( s ):
    return s.src.line_trace()  + " > " + \
           s.imul.line_trace()  + " > " + \
           s.sink.line_trace()

#-------------------------------------------------------------------------
# mk_req_msg
#-------------------------------------------------------------------------

def req( a, b ):
  msg = Bits( 64 )
  msg[32:64] = Bits( 32, a, trunc=True )
  msg[ 0:32] = Bits( 32, b, trunc=True )
  return msg

def resp( a ):
  return Bits( 32, a, trunc=True )

#----------------------------------------------------------------------
# Test Case: small positive * positive
#----------------------------------------------------------------------

small_pos_pos_msgs = [
  req(  2,  3 ), resp(   6 ),
  req(  4,  5 ), resp(  20 ),
  req(  3,  4 ), resp(  12 ),
  req( 10, 13 ), resp( 130 ),
  req(  8,  7 ), resp(  56 ),
]

#-------------------------------------------------------------------------
# Test Case: small positive * negative 
#-------------------------------------------------------------------------
small_pos_neg_msgs = [
  req(  2,  -2), resp( -4),
  req(  4,  -3), resp(-12),
  req( -1, 1),resp(-1),
  req( 10, -13), resp(-130),
  req( -8, 2), resp(-16)
]

#-------------------------------------------------------------------------
# Test Case: small negative * negative 
#-------------------------------------------------------------------------
small_neg_neg_msgs = [
  req(  -2,  -2), resp( 4),
  req(  -4,  -3), resp(12),
  req( -1, -1),resp(1),
  req( -10, -13), resp(130),
  req( -8, -2), resp(16)
]


#-------------------------------------------------------------------------
# Test Case: large positive * positive
#-------------------------------------------------------------------------
large_pos_pos_msgs = [
  req(  5000,  32), resp( 160000),
  req(  20000,  30), resp(600000),
  req( 500000, 20),resp(10000000),
  req( 12344, 42), resp(518448),
  req( 42068, 44), resp(1850992)
]

#-------------------------------------------------------------------------
# Test Case: large negative * positive 
#-------------------------------------------------------------------------
large_neg_pos_msgs = [
  req(  -5000,  32), resp( -160000),
  req(  -20000,  30), resp(-600000),
  req( -500000, 20),resp(-10000000),
  req( -12344, 42), resp(-518448),
  req( -42068, 44), resp(-1850992)
]

#-------------------------------------------------------------------------
# Test Case: large negative * negative 
#-------------------------------------------------------------------------
large_neg_neg_msgs = [
  req(  -5000,  -32), resp(160000),
  req(  -20000,  -30), resp(600000),
  req( -500000, -20),resp(10000000),
  req( -12344, -42), resp(518448),
  req( -42068, -44), resp(1850992)
]

#-------------------------------------------------------------------------
# Test Case: sparse numbers 
#-------------------------------------------------------------------------
sparse_msgs = [
  req(  37749765,  4), resp(150999060),
  req(2147483716, 2), resp(4294967432),
  req(2,4), resp(2*4),
  req(4652881168,4),resp(4652881168*4),
  req(37749765,37749765),resp(37749765*37749765)
]


#-------------------------------------------------------------------------
# Test Case Table
#-------------------------------------------------------------------------

test_case_table = mk_test_case_table([
  (                      "msgs                 src_delay sink_delay"),
  [ "small_pos_pos",     small_pos_pos_msgs,   0,        0          ],
  [ "small_pos_neg",     small_pos_neg_msgs,   0,	       0	        ], 
  [ "small_neg_neg",     small_neg_neg_msgs,   0,        0          ],
  [ "large_pos_pos",     large_pos_pos_msgs,   0,	       0	        ],
  [ "large_neg_neg",     large_neg_neg_msgs,   0,	       0	        ], 
  [ "large_neg_pos",     large_neg_pos_msgs,   0,	       0	        ], 
  [ "sparse",     sparse_msgs,   1,	       2	        ], 

  # ''' LAB TASK '''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  # Add more rows to the test case table to leverage the additional lists
  # of request/response messages defined above, but also to test
  # different source/sink random delays.
  # ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

])

#-------------------------------------------------------------------------
# Test cases
#-------------------------------------------------------------------------

@pytest.mark.parametrize( **test_case_table )
def test( test_params, dump_vcd ):
  run_sim( TestHarness( IntMulFL(),
                        test_params.msgs[::2], test_params.msgs[1::2],
                        test_params.src_delay, test_params.sink_delay ),
           dump_vcd )

