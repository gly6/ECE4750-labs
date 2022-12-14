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
# Test Case: dense numbers 
#-------------------------------------------------------------------------
dense_msgs = [
  req(0x2F3DFE3F,  0x2F7DFE3F), resp(0x2F3DFE3F * 0x2F7DFE3F),
  req(0x2F7DFFBF, 0x2F7FFFBF), resp(0x2F7DFFBF*0x2F7FFFBF),
  req(0x3FFFFFFF,0x2FFFFFFF), resp(0x3FFFFFFF*0x2FFFFFFF),
  req(0x3FFFE4FF,0xBFFFE4FF),resp(0x3FFFE4FF*0xBFFFE4FF),
]

#-------------------------------------------------------------------------
# Test Case: ones,zero,negative one 
#-------------------------------------------------------------------------
ones_zeros_negs_msgs = [
  req(1,  1), resp(1),
  req(1, 0), resp(0),
  req(1,-1), resp(-1),
  req(-1,0),resp(0),
]

#-------------------------------------------------------------------------
# Test Case: middle bits masked off
#-------------------------------------------------------------------------
middle_masked_off = [
  req(0xFFFF00FF,  0xFFFE00FF), resp(0xFFFF00FF*0xFFFE00FF),
  req(0xFFFC00FF, 0xFFFC00FF), resp(0xFFFC00FF*0xFFFC00FF),
  req(0xFFFB00FF,0xFFFA00FF), resp(0xFFFB00FF*0xFFFA00FF),
]

#-------------------------------------------------------------------------
# Test Case: lower order bits masked off
#-------------------------------------------------------------------------
low_order_off = [
  req(0xFFFFFFFE,  0xFFFFFFFE), resp(0xFFFFFFFE*0xFFFFFFFE),
  req(0xFFFFFFFC, 0xFFFFFFFC), resp(0xFFFFFFFC*0xFFFFFFFC),
  req(0xFFFFFFF8,0xFFFFFFF0), resp(0xFFFFFFF8*0xFFFFFFF0),
  req(0xFFFFFFE0,0xFFFFFFF0), resp(0xFFFFFFE0*0xFFFFFFF0),
]

#-------------------------------------------------------------------------
# Test Case: lower order bits masked off
#-------------------------------------------------------------------------
noconsec_zero = [
  req(0x1,0x55555555), resp(0x55555555)
]

#-------------------------------------------------------------------------
# Test Case: random test
#-------------------------------------------------------------------------
random_msgs = []
for i in xrange(50):
  a = random.randint(0,0xffff)
  b = random.randint(0,0xffff)
  c = resp( a*b )
  random_msgs.extend([req(a,b), c])
  
  
#-------------------------------------------------------------------------
# Test Case: random test 2 : Low bits masked
#-------------------------------------------------------------------------
random_low_mask_msgs = []
for i in xrange(50):
  a = (random.randint(0,0xffff)) & Bits(32,0xFFFFFF00)
  b = (random.randint(0,0xffff)) & Bits(32,0xFFFFFFDC)
  c = resp( a*b )
  random_low_mask_msgs.extend([req(a,b), c])
  
#-------------------------------------------------------------------------
# Test Case: random test 3 : middle bits masked
#-------------------------------------------------------------------------
random_mid_mask_msgs = []
for i in xrange(50):
  a = (random.randint(0,0xffff)) & Bits(32,0xFFF003FF)
  b = (random.randint(0,0xffff)) & Bits(32,0xFFE001FF)
  c = resp( a*b )
  random_mid_mask_msgs.extend([req(a,b), c])
  
  
#-------------------------------------------------------------------------
# Test Case: random test 4 : high bits masked
#-------------------------------------------------------------------------
random_high_mask_msgs = []
for i in xrange(50):
  a = (random.randint(0,0xffff)) & Bits(32,0x7FFFFFFF)
  b = (random.randint(0,0xffff)) & Bits(32,0x1FFFFFFF)
  c = resp( a*b )
  random_high_mask_msgs.extend([req(a,b), c])
  
 
#-------------------------------------------------------------------------
# Test Case: random test 5 : mix bits masked
#-------------------------------------------------------------------------
  
random_mix_mask_msgs = []
for i in xrange(50):
  a = (random.randint(0,0xffff)) & Bits(32,0xCCCE707D)
  b = (random.randint(0,0xffff)) & Bits(32,0xCCCE727D)
  c = resp( a*b )
  random_mix_mask_msgs.extend([req(a,b), c])
  
  
#-------------------------------------------------------------------------
# Test Case: random test 6 : pos_neg
#-------------------------------------------------------------------------
  
random_pos_neg_msgs = []
for i in xrange(50):
  a = (random.randint(-0xffff,0))
  b = (random.randint(0,0xffff))
  c = resp( a*b )
  random_pos_neg_msgs.extend([req(a,b), c])
  
#-------------------------------------------------------------------------
# Test Case: random test 7 : all bits anded with 1
#-------------------------------------------------------------------------
  
random_and_one_msgs = []
for i in xrange(50):
  a = (random.randint(0,0xffffffff))
  b = (random.randint(0,0xffffffff))
  
  c = resp( a*b )
  random_and_one_msgs.extend([req((a & 0xffffffff),(b & 0xffffffff) ), c])
  
#-------------------------------------------------------------------------
# Test Case Table
#-------------------------------------------------------------------------
for i in xrange(4):
  src_delay = random.randint(0,20)
  sink_delay = random.randint(0,20)

test_case_table = mk_test_case_table([
  (                      "msgs                 src_delay     sink_delay"),
  [ "small_pos_pos",     small_pos_pos_msgs,   src_delay,    sink_delay],
  [ "small_pos_neg",     small_pos_neg_msgs,   src_delay,	   sink_delay], 
  [ "small_neg_neg",     small_neg_neg_msgs,   src_delay,    sink_delay],
  [ "large_pos_pos",     large_pos_pos_msgs,   src_delay,	   sink_delay],
  [ "large_neg_neg",     large_neg_neg_msgs,   src_delay,	   sink_delay	        ], 
  [ "large_neg_pos",     large_neg_pos_msgs,   src_delay,	   sink_delay	        ], 
  [ "sparse_num",         sparse_msgs,         src_delay,	   sink_delay	        ],
  [ "dense_num",          dense_msgs,          src_delay,    sink_delay         ],
  [ "ones_zeros_neg_test", ones_zeros_negs_msgs,src_delay,   sink_delay         ],
  [ "middle_masked_off_test", middle_masked_off,  0,         0          ],
  [ "low_masked_off_test", low_order_off,      0,         0          ],
  [ "random_pos_pos", random_msgs,                 src_delay,  sink_delay          ],
  [ "random_pos_neg", random_pos_neg_msgs,                 src_delay,   sink_delay          ],
  [ "random_lomask", random_low_mask_msgs,                 src_delay,   sink_delay          ], 
  [ "random_midmask", random_mid_mask_msgs,                 src_delay,   sink_delay          ], 
  [ "random_himask", random_high_mask_msgs,                 src_delay,   sink_delay          ], 
  [ "random_mixmask", random_mix_mask_msgs,                 src_delay,   sink_delay          ],
  [ "random_AND_ones", random_and_one_msgs,                 src_delay,   sink_delay          ],
  [ "noconsec_zero", noconsec_zero,                 src_delay,   sink_delay          ]

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

