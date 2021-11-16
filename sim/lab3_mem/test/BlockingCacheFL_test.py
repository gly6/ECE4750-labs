#=========================================================================
# BlockingCacheFL_test.py
#=========================================================================

from __future__ import print_function

import pytest
import random
import struct
import math
import os 
from datetime import datetime

random.seed(0xa4e28cc2)

from pymtl      import *
from pclib.test import mk_test_case_table, run_sim
from pclib.test import TestSource
from pclib.test import TestMemory

from pclib.ifcs import MemMsg,    MemReqMsg,    MemRespMsg
from pclib.ifcs import MemMsg4B,  MemReqMsg4B,  MemRespMsg4B
from pclib.ifcs import MemMsg16B, MemReqMsg16B, MemRespMsg16B

from TestCacheSink   import TestCacheSink
from lab3_mem.BlockingCacheFL import BlockingCacheFL

# We define all test cases here. They will be used to test _both_ FL and
# RTL models.
#
# Notice the difference between the TestHarness instances in FL and RTL.
#
# class TestHarness( Model ):
#   def __init__( s, src_msgs, sink_msgs, stall_prob, latency,
#                 src_delay, sink_delay, CacheModel, check_test, dump_vcd )
#
# The last parameter of TestHarness, check_test is whether or not we
# check the test field in the cacheresp. In FL model we don't care about
# test field and we set cehck_test to be False because FL model is just
# passing through cachereq to mem, so all cachereq sent to the FL model
# will be misses, whereas in RTL model we must set check_test to be True
# so that the test sink will know if we hit the cache properly.

#-------------------------------------------------------------------------
# TestHarness
#-------------------------------------------------------------------------

class TestHarness( Model ):

  def __init__( s, src_msgs, sink_msgs, stall_prob, latency,
                src_delay, sink_delay, 
                CacheModel, num_banks, check_test, dump_vcd ):

    # Messge type

    cache_msgs = MemMsg4B()
    mem_msgs   = MemMsg16B()

    # Instantiate models

    s.src   = TestSource   ( cache_msgs.req,  src_msgs,  src_delay  )
    s.cache = CacheModel   ( num_banks = num_banks )
    s.mem   = TestMemory   ( mem_msgs, 1, stall_prob, latency )
    s.sink  = TestCacheSink( cache_msgs.resp, sink_msgs, sink_delay, check_test )

    # Dump VCD

    if dump_vcd:
      s.cache.vcd_file = dump_vcd

    # Connect

    s.connect( s.src.out,       s.cache.cachereq  )
    s.connect( s.sink.in_,      s.cache.cacheresp )

    s.connect( s.cache.memreq,  s.mem.reqs[0]     )
    s.connect( s.cache.memresp, s.mem.resps[0]    )

  def load( s, addrs, data_ints ):
    for addr, data_int in zip( addrs, data_ints ):
      data_bytes_a = bytearray()
      data_bytes_a.extend( struct.pack("<I",data_int) )
      s.mem.write_mem( addr, data_bytes_a )

  def done( s ):
    return s.src.done and s.sink.done

  def line_trace( s ):
    return s.src.line_trace() + " " + s.cache.line_trace() + " " \
         + s.mem.line_trace() + " " + s.sink.line_trace()

#-------------------------------------------------------------------------
# make messages
#-------------------------------------------------------------------------

def req( type_, opaque, addr, len, data ):
  msg = MemReqMsg4B()

  if   type_ == 'rd': msg.type_ = MemReqMsg.TYPE_READ
  elif type_ == 'wr': msg.type_ = MemReqMsg.TYPE_WRITE
  elif type_ == 'in': msg.type_ = MemReqMsg.TYPE_WRITE_INIT

  msg.addr   = addr
  msg.opaque = opaque
  msg.len    = len
  msg.data   = data
  return msg

def resp( type_, opaque, test, len, data ):
  msg = MemRespMsg4B()

  if   type_ == 'rd': msg.type_ = MemRespMsg.TYPE_READ
  elif type_ == 'wr': msg.type_ = MemRespMsg.TYPE_WRITE
  elif type_ == 'in': msg.type_ = MemRespMsg.TYPE_WRITE_INIT

  msg.opaque = opaque
  msg.len    = len
  msg.test   = test
  msg.data   = data
  return msg
#----------------------------------------------------------------------
# Given Test Cases 
#----------------------------------------------------------------------
#----------------------------------------------------------------------
# Test Case: read hit path
#----------------------------------------------------------------------
# The test field in the response message: 0 == MISS, 1 == HIT

def read_hit_1word_clean( base_addr ):
  return [
    #    type  opq  addr      len data                type  opq  test len data
    req( 'in', 0x0, base_addr, 0, 0xdeadbeef ), resp( 'in', 0x0, 0,   0,  0          ),
    req( 'rd', 0x1, base_addr, 0, 0          ), resp( 'rd', 0x1, 1,   0,  0xdeadbeef ),
  ]

#----------------------------------------------------------------------
# Test Case: read hit path -- for set-associative cache
#----------------------------------------------------------------------
# This set of tests designed only for alternative design
# The test field in the response message: 0 == MISS, 1 == HIT

def read_hit_asso( base_addr ):
  return [
    #    type  opq  addr       len data                type  opq  test len data
    req( 'wr', 0x0, 0x00000000, 0, 0xdeadbeef ), resp( 'wr', 0x0, 0,   0,  0          ),
    req( 'wr', 0x1, 0x00001000, 0, 0x00c0ffee ), resp( 'wr', 0x1, 0,   0,  0          ),
    req( 'rd', 0x2, 0x00000000, 0, 0          ), resp( 'rd', 0x2, 1,   0,  0xdeadbeef ),
    req( 'rd', 0x3, 0x00001000, 0, 0          ), resp( 'rd', 0x3, 1,   0,  0x00c0ffee ),
  ]

#----------------------------------------------------------------------
# Test Case: read hit path -- for direct-mapped cache
#----------------------------------------------------------------------
# This set of tests designed only for baseline design

def read_hit_dmap( base_addr ):
  return [
    #    type  opq  addr       len data                type  opq  test len data
    req( 'wr', 0x0, 0x00000000, 0, 0xdeadbeef ), resp( 'wr', 0x0, 0,   0,  0          ),
    req( 'wr', 0x1, 0x00000080, 0, 0x00c0ffee ), resp( 'wr', 0x1, 0,   0,  0          ),
    req( 'rd', 0x2, 0x00000000, 0, 0          ), resp( 'rd', 0x2, 1,   0,  0xdeadbeef ),
    req( 'rd', 0x3, 0x00000080, 0, 0          ), resp( 'rd', 0x3, 1,   0,  0x00c0ffee ),
  ]

#-------------------------------------------------------------------------
# Test Case: write hit path
#-------------------------------------------------------------------------

def write_hit_1word_clean( base_addr ):
  return [
    #    type  opq   addr      len data               type  opq   test len data
    req( 'in', 0x00, base_addr, 0, 0x0a0b0c0d ), resp('in', 0x00, 0,   0,  0          ), # write word  0x00000000
    req( 'wr', 0x01, base_addr, 0, 0xbeefbeeb ), resp('wr', 0x01, 1,   0,  0          ), # write word  0x00000000
    req( 'rd', 0x02, base_addr, 0, 0          ), resp('rd', 0x02, 1,   0,  0xbeefbeeb ), # read  word  0x00000000
  ]

#-------------------------------------------------------------------------
# Test Case: read miss path
#-------------------------------------------------------------------------

def read_miss_1word_msg( base_addr ):
  return [
    #    type  opq   addr      len  data               type  opq test len  data
    req( 'rd', 0x00, 0x00000000, 0, 0          ), resp('rd', 0x00, 0, 0, 0xdeadbeef ), # read word  0x00000000
    req( 'rd', 0x01, 0x00000004, 0, 0          ), resp('rd', 0x01, 1, 0, 0x00c0ffee ), # read word  0x00000004
  ]

# Data to be loaded into memory before running the test

def read_miss_1word_mem( base_addr ):
  return [
    # addr      data (in int)
    0x00000000, 0xdeadbeef,
    0x00000004, 0x00c0ffee,
  ]

#'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# Created Generic Test Cases 
#'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# Read hit path for clean lines
#'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
def read_hit_clean (base_addr): 
  return [
    #    type  opq   addr      len  data               type  opq test len  data
    req( 'in', 0x00, 0x00000000, 0, 0xdeadbeef ), resp('in', 0x00, 0, 0,  0       ),
    req( 'rd', 0x01, 0x00000000, 0, 0          ), resp('rd', 0x01, 1, 0, 0xdeadbeef ), # read word  0x00000000
    req( 'rd', 0x02, 0x00000004, 0, 0          ), resp('rd', 0x02, 1, 0, 0          ), # read word  0x00000004
    req( 'rd', 0x03, 0x00000008, 0, 0          ), resp('rd', 0x03, 1, 0, 0          ), # read word  0x00000008
    req( 'rd', 0x04, 0x0000000c, 0, 0          ), resp('rd', 0x04, 1, 0, 0          ), # read word  0x0000000c
  ]
#'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# Write hit path for clean lines
#'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
def write_hit_clean (base_addr): 
  return [
    #    type  opq   addr      len  data               type  opq test len  data
    req( 'in', 0x00, 0x00000000, 0, 0xdeadbeef ), resp('in', 0x00, 0, 0, 0        ),
    req( 'wr', 0x01, 0x00000004, 0, 0x00c0ffee ), resp('wr', 0x01, 1, 0, 0        ),
    req( 'rd', 0x02, 0x00000000, 0, 0          ), resp('rd', 0x02, 1, 0, 0xdeadbeef ), # read word  0x00000000
    req( 'rd', 0x03, 0x00000004, 0, 0          ), resp('rd', 0x03, 1, 0, 0x00c0ffee ), # read word  0x00000004
  ]

#'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# Read hit path for dirty lines 
#''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''' 
def read_hit_dirty (base_addr): 
  return [
    #    type  opq   addr      len  data               type  opq test len  data
    req( 'in', 0x00, 0x00000000, 0, 0xdeadbeef ), resp('in', 0x00, 0, 0, 0        ),
    req( 'wr', 0x01, 0x00000004, 0, 0x00c0ffee ), resp('wr', 0x01, 1, 0, 0        ),
    req( 'rd', 0x02, 0x00000000, 0, 0          ), resp('rd', 0x02, 1, 0, 0xdeadbeef ), # read word  0x00000000
    req( 'rd', 0x03, 0x00000004, 0, 0          ), resp('rd', 0x03, 1, 0, 0x00c0ffee ), # read word  0x00000004
    #req( 'rd', 0x04, 0x00000008, 0, 0          ), resp('rd', 0x04, 1, 0, 0          ), # read word  0x00000008
    #req( 'rd', 0x05, 0x0000000c, 0, 0          ), resp('rd', 0x05, 1, 0, 0          ), # read word  0x0000000c
  ]
def read_hit_dirty_mem (base_addr):
  return [
    # addr      data (in int)
    0x00000000, 0x00000000,
    0x00000004, 0x00000001,
    0x00000008, 0xabcdefab,
    0x0000000c, 0x01234567, 
    0x00000010, 0xdededede,   
  ]

#'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# Write hit path for dirty lines 
#''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''' 
def write_hit_dirty (base_addr): 
  return [
    #    type  opq   addr      len  data               type  opq test len  data
    req( 'in', 0x00, 0x00000000, 0, 0xdeadbeef ), resp('in', 0x00, 0, 0, 0        ),
    req( 'wr', 0x00, 0x00000004, 0, 0x00c0ffee ), resp('wr', 0x00, 1, 0, 0        ),
    req( 'wr', 0x00, 0x00000008, 0, 0xabcdefab ), resp('wr', 0x00, 1, 0, 0        ),
    req( 'rd', 0x01, 0x00000000, 0, 0          ), resp('rd', 0x01, 1, 0, 0xdeadbeef ), # read word  0x00000000
    req( 'rd', 0x02, 0x00000004, 0, 0          ), resp('rd', 0x02, 1, 0, 0x00c0ffee ), # read word  0x00000004
    req( 'rd', 0x03, 0x00000008, 0, 0          ), resp('rd', 0x03, 1, 0, 0xabcdefab ), # read word  0x00000008
    #req( 'rd', 0x04, 0x0000000c, 0, 0          ), resp('rd', 0x04, 1, 0, 0          ), # read word  0x0000000c
  ]
def write_hit_dirty_mem (base_addr):
  return [
    # addr      data (in int)
    0x00000000, 0x00000000,
    0x00000004, 0x00000001,
    0x00000008, 0x00000002,
    0x0000000c, 0x01234567, 
    0x00000010, 0xdededede,   
  ]
#'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# Read miss with refill and no eviction
#''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''' 
def read_miss_wr_woe( base_addr ):
  return [
    #    type  opq   addr      len  data               type  opq test len  data
    req( 'rd', 0x00, 0x00000000, 0, 0          ), resp('rd', 0x00, 0, 0, 0xdeadbeef ), # read word  0x00000000
    req( 'rd', 0x01, 0x00000004, 0, 0          ), resp('rd', 0x01, 1, 0, 0x00c0ffee ), # read word  0x00000004
    req( 'rd', 0x02, 0x00000008, 0, 0          ), resp('rd', 0x02, 1, 0, 0xabcdefab ), # read word  0x00000008
    req( 'rd', 0x03, 0x0000000c, 0, 0          ), resp('rd', 0x03, 1, 0, 0x01234567 ), # read word  0x0000000c
    req( 'rd', 0x04, 0x00000010, 0, 0          ), resp('rd', 0x04, 0, 0, 0xdededede ), # read word  0x00000010
  ]

# Data to be loaded into memory before running the test

def read_miss_wr_woe_mem( base_addr ):
  return [
    # addr      data (in int)
    0x00000000, 0xdeadbeef,
    0x00000004, 0x00c0ffee,
    0x00000008, 0xabcdefab,
    0x0000000c, 0x01234567, 
    0x00000010, 0xdededede,   
  ]
#'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# Write miss with refill and no eviction
#''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''' 
def write_miss_wr_woe (base_addr) : 
  return [
    #    type  opq   addr      len  data               type  opq test len  data
    req( 'wr', 0x00, 0x00000000, 0, 0xdeadbeef ), resp('wr', 0x00, 0, 0, 0x0), # write word  0x00000000
    req( 'rd', 0x01, 0x00000000, 0, 0          ), resp('rd', 0x01, 1, 0, 0xdeadbeef ), # read word  0x00000000
    req( 'rd', 0x02, 0x00000004, 0, 0          ), resp('rd', 0x02, 1, 0, 0x00c0ffee ), # read word  0x00000004
    req( 'rd', 0x03, 0x00000008, 0, 0          ), resp('rd', 0x03, 1, 0, 0xabcdefab ), # read word  0x00000008
    req( 'rd', 0x04, 0x0000000c, 0, 0          ), resp('rd', 0x04, 1, 0, 0x01234567 ), # read word  0x0000000c
  ]

# Data to be loaded into memory before running the test
def write_miss_wr_woe_mem (base_addr):
  return [
    # addr      data (in int)
    0x00000000, 0x00000000,
    0x00000004, 0x00c0ffee,
    0x00000008, 0xabcdefab,
    0x0000000c, 0x01234567, 
    0x00000010, 0x00000001,   
  ]
#'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# Created Direct Test Cases 
#'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# Read miss with refill and eviction
#''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''' 
def read_miss_wr_we_dt( base_addr ):
  return [
    #    type  opq   addr      len  data               type  opq test len  data
    req( 'rd', 0x00, 0x00000000, 0, 0          ), resp('rd', 0x00, 0, 0, 0xdeadbeef ), # read word  0x00000000
    req( 'rd', 0x01, 0x00000004, 0, 0          ), resp('rd', 0x01, 1, 0, 0x00c0ffee ), # read word  0x00000004
    req( 'rd', 0x02, 0x00000008, 0, 0          ), resp('rd', 0x02, 1, 0, 0xabcdefab ), # read word  0x00000008
    req( 'rd', 0x03, 0x0000000c, 0, 0          ), resp('rd', 0x03, 1, 0, 0x01234567 ), # read word  0x0000000c
    req( 'rd', 0x04, 0x00000010, 0, 0          ), resp('rd', 0x04, 0, 0, 0xdededede ), # read word  0x00000010
    req( 'rd', 0x05, 0x00001000, 0, 0          ), resp('rd', 0x05, 0, 0, 0x00000001 ), # read word  0x00001000
    req( 'rd', 0x06, 0x00001004, 0, 0          ), resp('rd', 0x06, 1, 0, 0x00000002 ), # read word  0x00001000
    req( 'rd', 0x07, 0x00001008, 0, 0          ), resp('rd', 0x07, 1, 0, 0x00000003 ), # read word  0x00001000
    req( 'rd', 0x08, 0x0000100c, 0, 0          ), resp('rd', 0x08, 1, 0, 0x00000004 ), # read word  0x00001000 
  ]

# Data to be loaded into memory before running the test

def read_miss_wr_we_dt_mem( base_addr ):
  return [
    # addr      data (in int)
    0x00000000, 0xdeadbeef,
    0x00000004, 0x00c0ffee,
    0x00000008, 0xabcdefab,
    0x0000000c, 0x01234567, 
    0x00000010, 0xdededede,   
    0x00001000, 0x00000001, 
    0x00001004, 0x00000002,
    0x00001008, 0x00000003,
    0x0000100c, 0x00000004,
  ]
#'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# Write miss with refill and eviction
#''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''' 
def write_miss_wr_we_dt( base_addr ):
  return [
    #    type  opq   addr      len  data               type  opq test len  data
    req( 'rd', 0x00, 0x00000000, 0, 0          ), resp('rd', 0x00, 0, 0, 0xdeadbeef ), # read word  0x00000000
    req( 'rd', 0x01, 0x00000004, 0, 0          ), resp('rd', 0x01, 1, 0, 0x00c0ffee ), # read word  0x00000004
    req( 'rd', 0x02, 0x00000008, 0, 0          ), resp('rd', 0x02, 1, 0, 0xabcdefab ), # read word  0x00000008
    req( 'rd', 0x03, 0x0000000c, 0, 0          ), resp('rd', 0x03, 1, 0, 0x01234567 ), # read word  0x0000000c
    req( 'rd', 0x04, 0x00000010, 0, 0          ), resp('rd', 0x04, 0, 0, 0xdededede ), # read word  0x00000010
    req( 'wr', 0x05, 0x00001000, 0, 0x00000010 ), resp('wr', 0x05, 0, 0, 0          ), # write word 0x00001000
    req( 'rd', 0x06, 0x00001000, 0, 0          ), resp('rd', 0x06, 1, 0, 0x00000010 ), # read word  0x00001000
    req( 'rd', 0x07, 0x00001004, 0, 0          ), resp('rd', 0x07, 1, 0, 0x00000002 ), # read word  0x00001000
    req( 'rd', 0x08, 0x00001008, 0, 0          ), resp('rd', 0x08, 1, 0, 0x00000003 ), # read word  0x00001000
    req( 'rd', 0x09, 0x0000100c, 0, 0          ), resp('rd', 0x09, 1, 0, 0x00000004 ), # read word  0x00001000

  ]

# Data to be loaded into memory before running the test

def write_miss_wr_we_dt_mem( base_addr ):
  return [
    # addr      data (in int)
    0x00000000, 0xdeadbeef,
    0x00000004, 0x00c0ffee,
    0x00000008, 0xabcdefab,
    0x0000000c, 0x01234567, 
    0x00000010, 0xdededede,   
    0x00001000, 0x00000001, 
    0x00001004, 0x00000002,
    0x00001008, 0x00000003,
    0x0000100c, 0x00000004,
  ]
#'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# Stress test 
#''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''' 
def stress_dt (base_addr): 
  stress_dt_msgs = []
  for i in range(16):
    for j in range(4): 
      if (j == 0):
        hit = 0
      else: 
        hit = 1 
      offset = j << 2  
      index = i << 4 
      addr = index | offset 
      data = i*4+j 
      opq = i*4+j 
      stress_dt_msgs.extend([req('rd', i*4+j, addr, 0, 0), resp('rd', i*4+j, hit, 0, data)])
  return stress_dt_msgs

def stress_dt_mem(base_addr):
  stress_dt_mem_msgs = []
  for i in range(16):
    for j in range(4): 
      offset = j << 2  
      index = i << 4 
      addr = index | offset 
      data = i*4 + j 
      stress_dt_mem_msgs.extend([addr, data])
  return stress_dt_mem_msgs 
      
    

#'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# Conflict misses
#''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''' 
def conflict_miss_dt( base_addr ):
  return [
    #    type  opq   addr      len  data               type  opq test len  data
    req( 'rd', 0x00, 0x00000000, 0, 0          ), resp('rd', 0x00, 0, 0, 0xdeadbeef ), # read word  0x00000000
    req( 'rd', 0x01, 0x00000004, 0, 0          ), resp('rd', 0x01, 1, 0, 0x00c0ffee ), # read word  0x00000004
    req( 'rd', 0x02, 0x00000008, 0, 0          ), resp('rd', 0x02, 1, 0, 0xabcdefab ), # read word  0x00000008
    req( 'rd', 0x03, 0x0000000c, 0, 0          ), resp('rd', 0x03, 1, 0, 0x01234567 ), # read word  0x0000000c
    req( 'rd', 0x04, 0x00000010, 0, 0          ), resp('rd', 0x04, 0, 0, 0xdededede ), # read word  0x00000010
    req( 'rd', 0x05, 0x00001000, 0, 0          ), resp('rd', 0x05, 0, 0, 0x00000001 ), # read word  0x00001000
    req( 'rd', 0x06, 0x00001004, 0, 0          ), resp('rd', 0x06, 1, 0, 0x00000002 ), # read word  0x00001000
    req( 'rd', 0x07, 0x00001008, 0, 0          ), resp('rd', 0x07, 1, 0, 0x00000003 ), # read word  0x00001000
    req( 'rd', 0x08, 0x0000100c, 0, 0          ), resp('rd', 0x08, 1, 0, 0x00000004 ), # read word  0x00001000
    req( 'rd', 0x09, 0x00000000, 0, 0          ), resp('rd', 0x09, 0, 0, 0xdeadbeef ), # read word  0x00000000
  ]

def conflict_miss_dt_mem( base_addr ):
  return [
    # addr      data (in int)
    0x00000000, 0xdeadbeef,
    0x00000004, 0x00c0ffee,
    0x00000008, 0xabcdefab,
    0x0000000c, 0x01234567, 
    0x00000010, 0xdededede,   
    0x00001000, 0x00000001, 
    0x00001004, 0x00000002,
    0x00001008, 0x00000003,
    0x0000100c, 0x00000004,
  ]
  
def conflict_miss_dt_1( base_addr ):
  return [
    #    type  opq   addr      len  data               type  opq test len  data
    req( 'rd', 0x00, 0x00000000, 0, 0          ), resp('rd', 0x00, 0, 0, 0xdeadbeef ), # read word  0x00000000
    req( 'rd', 0x01, 0x00000004, 0, 0          ), resp('rd', 0x01, 1, 0, 0x00c0ffee ), # read word  0x00000004
    req( 'rd', 0x02, 0x00000008, 0, 0          ), resp('rd', 0x02, 1, 0, 0xabcdefab ), # read word  0x00000008
    req( 'rd', 0x03, 0x0000000c, 0, 0          ), resp('rd', 0x03, 1, 0, 0x01234567 ), # read word  0x0000000c
    req( 'rd', 0x04, 0x00000010, 0, 0          ), resp('rd', 0x04, 0, 0, 0xdededede ), # read word  0x00000010
    req( 'wr', 0x05, 0x00001000, 0, 0x00000010 ), resp('wr', 0x05, 0, 0, 0          ), # write word 0x00001000
    req( 'rd', 0x06, 0x00001000, 0, 0          ), resp('rd', 0x06, 1, 0, 0x00000010 ), # read word  0x00001000
    req( 'rd', 0x07, 0x00001004, 0, 0          ), resp('rd', 0x07, 1, 0, 0x00000002 ), # read word  0x00001000
    req( 'rd', 0x08, 0x00001008, 0, 0          ), resp('rd', 0x08, 1, 0, 0x00000003 ), # read word  0x00001000
    req( 'rd', 0x09, 0x0000100c, 0, 0          ), resp('rd', 0x09, 1, 0, 0x00000004 ), # read word  0x00001000
    req( 'rd', 0x10, 0x00000000, 0, 0          ), resp('rd', 0x10, 0, 0, 0xdeadbeef ), # read word  0x00000000
    req( 'rd', 0x11, 0x00001000, 0, 0          ), resp('rd', 0x11, 0, 0, 0x00000010 ), # read word  0x00001000
  ]

# Data to be loaded into memory before running the test

def conflict_miss_dt_mem_1( base_addr ):
  return [
    # addr      data (in int)
    0x00000000, 0xdeadbeef,
    0x00000004, 0x00c0ffee,
    0x00000008, 0xabcdefab,
    0x0000000c, 0x01234567, 
    0x00000010, 0xdededede,   
    0x00001000, 0x00000001, 
    0x00001004, 0x00000002,
    0x00001008, 0x00000003,
    0x0000100c, 0x00000004,
  ]

def check_random_test_dt (base_addr):
  return [
    #    type  opq   addr      len  data               type  opq test len  data
    req( 'wr', 0x00, 0x00000000, 0, 0xdeadbeef ), resp('wr', 0x00, 0, 0,   0), 
    req( 'wr', 0x01, 0x0000000c, 0, 0x00c0ffee ), resp('wr', 0x01, 1, 0,   0),
    req( 'wr', 0x02, 0x0000100c, 0, 0x00000001 ), resp('wr', 0x02, 0, 0,   0),
    req( 'rd', 0x03, 0x0000000c, 0, 0          ), resp('rd', 0x03, 0, 0,   0x00c0ffee), 
    req( 'wr', 0x04, 0x0000200c, 0, 0x00000002 ), resp('wr', 0x04, 0, 0,   0), 
    req( 'rd', 0x05, 0x0000000c, 0, 0          ), resp('rd', 0x05, 0, 0,   0x00c0ffee), 
  ]

#'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# Capacity test 
#'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
def capacity_dt (base_addr): 
  capacity_dt_msgs = []
  for i in range(16):
    for j in range(4): 
      if (j == 0):
        hit = 0
      else: 
        hit = 1 
      offset = j << 2  
      index = i << 4 
      addr = index | offset 
      data = i*4+j 
      opq = i*4+j 
      capacity_dt_msgs.extend([req('rd', i*4+j, addr, 0, 0), resp('rd', i*4+j, hit, 0, data)])
  capacity_dt_msgs.extend([req('rd', 64, 0x00001000, 0, 0), resp('rd', 64, 0, 0, 100)])
  return capacity_dt_msgs

def capacity_dt_mem(base_addr):
  capacity_dt_mem_msgs = []
  for i in range(16):
    for j in range(4): 
      offset = j << 2  
      index = i << 4 
      addr = index | offset 
      data = i*4 + j 
      capacity_dt_mem_msgs.extend([addr, data])
  capacity_dt_mem_msgs.extend([0x00001000, 100])
  return capacity_dt_mem_msgs 

#'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# Random test 
#'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
def cacheline_int_dt (tag, index, cache, tag_mem, msgs, num, name): 
  tag_mem.add(tag)
  offset = ['0', '4', '8', 'c']
  for i in range (4): 
    if (i == 0): 
      hit = 0 
    else:
      hit = 1
    addr_hex = tag + offset[i]
    addr = int(addr_hex, 16)
    data = random.randint(0, 0xFFFFFFFF)
    cache[index][i+1] = data
    with open(name, "a") as f:
      f.write("wr " + "addr " + addr_hex + " data " + str(data) + " hit " + str(hit) + "\n")    
    msgs.extend([req('wr', num, addr, 0, data), resp('wr', num, hit, 0, 0)])
    num += 1
    if (num > 255): num = 0
  return num     

def cacheline_refill_dt (tag, index, cache, mem):
  offset = ['0', '4', '8', 'c']
  for i in range(4):
    addr_hex = tag + offset[i]
    if (addr_hex not in mem):
      data = 0
    else: 
      data = mem[addr_hex]
    cache[index][i+1] = data 

def cacheline_evict_dt (index, cache, mem):
  offset = ['0', '4', '8', 'c']
  tag_hex = '{:07x}'.format(cache[index][0])
  for i in range(4):
    addr_hex = tag_hex + offset[i] 
    mem[addr_hex] = cache[index][i+1]

def read_request_dt (addr, refcache, refmem, reftag, num_inst, msgs, name): 
    offset_dic = {'0':1, '4':2, '8':3, 'c':4} 
    addr_hex = '{:08x}'.format(addr)
    tag_hex = addr_hex[:len(addr_hex)-1]
    index_hex= addr_hex[-2]
    offset_hex = addr_hex[-1]
    tag = int(tag_hex,16)
    index = int(index_hex, 16)
    offset = int(offset_hex, 16)
    hit = 1
    if (refcache[index][0] != tag):
        if (refcache[index][0] != -1):
            cacheline_evict_dt(index, refcache, refmem)
        if (tag_hex not in reftag):
            num_inst = cacheline_int_dt (tag_hex, index, refcache, reftag, msgs, num_inst, name)
        else: 
            cacheline_refill_dt(tag_hex, index, refcache, refmem)
            hit = 0
        refcache[index][0] = tag
    data = refcache[index][offset_dic[offset_hex]]
    with open(name, "a") as f:
      f.write("rd " + "addr " + addr_hex + " data " + str(data) + " hit " + str(hit) + "\n")
    msgs.extend([req('rd', num_inst, addr, 0, 0),resp('rd', num_inst, hit, 0, data)])
    num_inst += 1
    if (num_inst > 255): num_inst = 0
    return num_inst
  
def write_request_dt (addr, refcache, refmem, reftag, num_inst, msgs, name):
  offset_dic = {'0':1, '4':2, '8':3, 'c':4} 
  addr_hex = '{:08x}'.format(addr)
  tag_hex = addr_hex[:len(addr_hex)-1]
  index_hex= addr_hex[-2]
  offset_hex = addr_hex[-1]
  tag = int(tag_hex,16)
  index = int(index_hex, 16)
  offset = int(offset_hex, 16)
  hit = 1
  data = random.randint(0, 0xFFFFFFFF)
  if (refcache[index][0] != tag):
    if (refcache[index][0] != -1):
      cacheline_evict_dt(index, refcache, refmem)
    if (tag_hex not in reftag):
      num_inst = cacheline_int_dt (tag_hex, index, refcache, reftag, msgs, num_inst, name)
    else: 
      cacheline_refill_dt(tag_hex, index, refcache, refmem)
      hit = 0
    refcache[index][0] = tag
  refcache[index][offset_dic[offset_hex]] = data 
  with open(name, "a") as f:
    f.write("wr " + "addr " + addr_hex + " data " + str(data) + " hit " + str(hit) + "\n")
  msgs.extend([req('wr', num_inst, addr, 0, data),resp('wr', num_inst, hit, 0, 0)])
  num_inst += 1
  if (num_inst > 255): num_inst = 0
  return num_inst
  
def random_randata_dt (base_addr):
  random_randata_dt_msgs = []
  refmem = {} 
  reftag = set()  
  refcache = [[-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1]]
  num_inst = 0 
  now = datetime.now()
  current_time = now.strftime("%H:%M:%S")
  name = "random_randata_dt.txt"
  if os.path.exists(name):
    os.remove(name)
  with open(name, "w") as f:
    f.write("Data for simple address patterns, single request type, random data " + current_time + "\n")  
  for k in range (2):           
    for i in range(100): 
      addr = i << 2 
      num_inst = read_request_dt(addr, refcache, refmem, reftag, num_inst, random_randata_dt_msgs, name)
  return random_randata_dt_msgs 

def random_rantypedata_dt (base_addr):
  random_rantypedata_dt_msgs = []
  refmem = {} 
  reftag = set()  
  refcache = [[-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1]]
  num_inst = 0 
  now = datetime.now()
  current_time = now.strftime("%H:%M:%S")
  name = "random_rantypedata_dt.txt"
  if os.path.exists(name):
    os.remove(name)
  with open(name, "w") as f:
    f.write("Data for simple address patterns, random request type, random data " + current_time + "\n")  
  for i in range(100):
    req_type = random.randint(0, 1)
    addr = i << 2 
    if (req_type == 0):
      num_inst = write_request_dt (addr, refcache, refmem, reftag, num_inst, random_rantypedata_dt_msgs, name)
    else: 
      num_inst = read_request_dt (addr, refcache, refmem, reftag, num_inst, random_rantypedata_dt_msgs, name)
  for i in range(100):
    addr = i << 2 
    num_inst = read_request_dt (addr, refcache, refmem, reftag, num_inst, random_rantypedata_dt_msgs, name)
  return random_rantypedata_dt_msgs 

def random_ranaddrtypedata_dt (base_addr):
  random_ranaddrtypedata_dt_msgs = []
  refmem = {} 
  reftag = set()  
  refcache = [[-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1]]
  num_inst = 0 
  now = datetime.now()
  current_time = now.strftime("%H:%M:%S")
  name = "random_ranaddrtypedata_dt.txt"
  addr_array = [] 
  if os.path.exists(name):
    os.remove(name)
  with open(name, "w") as f:
    f.write("Data for random address patterns, random request type, random data " + current_time + "\n")  
  for i in range(100):
    req_type = random.randint(0, 1)
    addr = random.randint(0, 0x0000FFFF) << 2
    addr_array.append(addr)
    if (req_type == 0):
      num_inst = write_request_dt (addr, refcache, refmem, reftag, num_inst, random_ranaddrtypedata_dt_msgs, name)
    else: 
      num_inst = read_request_dt (addr, refcache, refmem, reftag, num_inst, random_ranaddrtypedata_dt_msgs, name)
  for i in range(100):
    addr = addr_array[i]
    num_inst = read_request_dt (addr, refcache, refmem, reftag, num_inst, random_ranaddrtypedata_dt_msgs, name)
  return random_ranaddrtypedata_dt_msgs

def random_ranaddrtypedata_dt_1 (base_addr):
  random_ranaddrtypedata_dt_1_msgs = []
  refmem = {} 
  reftag = set()  
  refcache = [[-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1]]
  num_inst = 0 
  now = datetime.now()
  current_time = now.strftime("%H:%M:%S")
  name = "random_ranaddrtypedata_dt_1.txt"
  addr_array = [] 
  if os.path.exists(name):
    os.remove(name)
  with open(name, "w") as f:
    f.write("Data for random address patterns, random request type, random data " + current_time + "\n")  
  for i in range(100):
    req_type = random.randint(0, 1)
    addr = random.randint(0, 0x000007F) << 2
    addr_array.append(addr)
    if (req_type == 0):
      num_inst = write_request_dt (addr, refcache, refmem, reftag, num_inst, random_ranaddrtypedata_dt_1_msgs, name)
    else: 
      num_inst = read_request_dt (addr, refcache, refmem, reftag, num_inst, random_ranaddrtypedata_dt_1_msgs, name)
  for i in range(100):
    addr = addr_array[i]
    num_inst = read_request_dt (addr, refcache, refmem, reftag, num_inst, random_ranaddrtypedata_dt_1_msgs, name)
  return random_ranaddrtypedata_dt_1_msgs
 
#'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# Created Assoc Test Cases 
#'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# Read miss with refill and eviction
#''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''' 
def read_miss_wr_we_assoc( base_addr ):
  return [
    #    type  opq   addr      len  data               type  opq test len  data
    req( 'rd', 0x00, 0x00000000, 0, 0          ), resp('rd', 0x00, 0, 0, 0xdeadbeef ), # read word  0x00000000
    req( 'rd', 0x01, 0x00000004, 0, 0          ), resp('rd', 0x01, 1, 0, 0x00c0ffee ), # read word  0x00000004
    req( 'rd', 0x02, 0x00000008, 0, 0          ), resp('rd', 0x02, 1, 0, 0xabcdefab ), # read word  0x00000008
    req( 'rd', 0x03, 0x0000000c, 0, 0          ), resp('rd', 0x03, 1, 0, 0x01234567 ), # read word  0x0000000c
    req( 'rd', 0x04, 0x00000010, 0, 0          ), resp('rd', 0x04, 0, 0, 0xdededede ), # read word  0x00000010
    req( 'rd', 0x05, 0x00001000, 0, 0          ), resp('rd', 0x05, 0, 0, 0x00000001 ), # read word  0x00001000
    req( 'rd', 0x06, 0x00001004, 0, 0          ), resp('rd', 0x06, 1, 0, 0x00000002 ), # read word  0x00001000
    req( 'rd', 0x07, 0x00001008, 0, 0          ), resp('rd', 0x07, 1, 0, 0x00000003 ), # read word  0x00001000
    req( 'rd', 0x08, 0x0000100c, 0, 0          ), resp('rd', 0x08, 1, 0, 0x00000004 ), # read word  0x00001000
    req( 'rd', 0x10, 0x00002000, 0, 0          ), resp('rd', 0x10, 0, 0, 0x00000021 ), # read word  0x00001000
    req( 'rd', 0x11, 0x00002004, 0, 0          ), resp('rd', 0x11, 1, 0, 0x00000022 ), # read word  0x00001000
    req( 'rd', 0x12, 0x00002008, 0, 0          ), resp('rd', 0x12, 1, 0, 0x00000023 ), # read word  0x00001000
    req( 'rd', 0x13, 0x0000200c, 0, 0          ), resp('rd', 0x13, 1, 0, 0x00000024 ), # read word  0x00001000
 
  ]

# Data to be loaded into memory before running the test

def read_miss_wr_we_assoc_mem( base_addr ):
  return [
    # addr      data (in int)
    0x00000000, 0xdeadbeef,
    0x00000004, 0x00c0ffee,
    0x00000008, 0xabcdefab,
    0x0000000c, 0x01234567, 
    0x00000010, 0xdededede,   
    0x00001000, 0x00000001, 
    0x00001004, 0x00000002,
    0x00001008, 0x00000003,
    0x0000100c, 0x00000004,
    0x00002000, 0x00000021, 
    0x00002004, 0x00000022,
    0x00002008, 0x00000023,
    0x0000200c, 0x00000024,
  ]
#'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# Write miss with refill and eviction
#''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''' 
def write_miss_wr_we_assoc( base_addr ):
  return [
    #    type  opq   addr      len  data               type  opq test len  data
    req( 'rd', 0x00, 0x00000000, 0, 0          ), resp('rd', 0x00, 0, 0, 0xdeadbeef ), # read word  0x00000000
    req( 'rd', 0x01, 0x00000004, 0, 0          ), resp('rd', 0x01, 1, 0, 0x00c0ffee ), # read word  0x00000004
    req( 'rd', 0x02, 0x00000008, 0, 0          ), resp('rd', 0x02, 1, 0, 0xabcdefab ), # read word  0x00000008
    req( 'rd', 0x03, 0x0000000c, 0, 0          ), resp('rd', 0x03, 1, 0, 0x01234567 ), # read word  0x0000000c
    req( 'rd', 0x04, 0x00000010, 0, 0          ), resp('rd', 0x04, 0, 0, 0xdededede ), # read word  0x00000010
    req( 'wr', 0x05, 0x00001000, 0, 0x00000010 ), resp('wr', 0x05, 0, 0, 0          ), # read word  0x00001000
    req( 'rd', 0x05, 0x00001000, 0, 0          ), resp('rd', 0x05, 1, 0, 0x00000010 ), # read word  0x00001000
    req( 'rd', 0x06, 0x00001004, 0, 0          ), resp('rd', 0x06, 1, 0, 0x00000002 ), # read word  0x00001000
    req( 'rd', 0x07, 0x00001008, 0, 0          ), resp('rd', 0x07, 1, 0, 0x00000003 ), # read word  0x00001000
    req( 'rd', 0x08, 0x0000100c, 0, 0          ), resp('rd', 0x08, 1, 0, 0x00000004 ), # read word  0x00001000
    req( 'wr', 0x09, 0x00002000, 0, 0x00000020 ), resp('rd', 0x09, 0, 0, 0          ), # read word  0x00001000
    req( 'rd', 0x10, 0x00002000, 0, 0          ), resp('rd', 0x10, 1, 0, 0x00000020 ), # read word  0x00001000
    req( 'rd', 0x11, 0x00002004, 0, 0          ), resp('rd', 0x11, 1, 0, 0x00000022 ), # read word  0x00001000
    req( 'rd', 0x12, 0x00002008, 0, 0          ), resp('rd', 0x12, 1, 0, 0x00000023 ), # read word  0x00001000
    req( 'rd', 0x13, 0x0000200c, 0, 0          ), resp('rd', 0x13, 1, 0, 0x00000024 ), # read word  0x00001000
 
  ]

# Data to be loaded into memory before running the test

def write_miss_wr_we_assoc_mem( base_addr ):
  return [
    # addr      data (in int)
    0x00000000, 0xdeadbeef,
    0x00000004, 0x00c0ffee,
    0x00000008, 0xabcdefab,
    0x0000000c, 0x01234567, 
    0x00000010, 0xdededede,   
    0x00001000, 0x00000001, 
    0x00001004, 0x00000002,
    0x00001008, 0x00000003,
    0x0000100c, 0x00000004,
    0x00002000, 0x00000021, 
    0x00002004, 0x00000022,
    0x00002008, 0x00000023,
    0x0000200c, 0x00000024,
  ]

def write_miss_wr_we_assoc_1( base_addr ):
  return [
    #    type  opq   addr      len  data               type  opq test len  data
    req( 'wr', 0x00, 0x00000000, 0, 0x00000030 ), resp('rd', 0x00, 0, 0, 0          ), # read word  0x00000000
    req( 'rd', 0x00, 0x00000000, 0, 0          ), resp('rd', 0x00, 1, 0, 0x00000030 ),
    req( 'rd', 0x01, 0x00000004, 0, 0          ), resp('rd', 0x01, 1, 0, 0x00c0ffee ), # read word  0x00000004
    req( 'rd', 0x02, 0x00000008, 0, 0          ), resp('rd', 0x02, 1, 0, 0xabcdefab ), # read word  0x00000008
    req( 'rd', 0x03, 0x0000000c, 0, 0          ), resp('rd', 0x03, 1, 0, 0x01234567 ), # read word  0x0000000c
    req( 'rd', 0x04, 0x00000010, 0, 0          ), resp('rd', 0x04, 0, 0, 0xdededede ), # read word  0x00000010
    req( 'wr', 0x05, 0x00001000, 0, 0x00000010 ), resp('wr', 0x05, 0, 0, 0          ), # read word  0x00001000
    req( 'rd', 0x05, 0x00001000, 0, 0          ), resp('rd', 0x05, 1, 0, 0x00000010 ), # read word  0x00001000
    req( 'rd', 0x06, 0x00001004, 0, 0          ), resp('rd', 0x06, 1, 0, 0x00000002 ), # read word  0x00001000
    req( 'rd', 0x07, 0x00001008, 0, 0          ), resp('rd', 0x07, 1, 0, 0x00000003 ), # read word  0x00001000
    req( 'rd', 0x08, 0x0000100c, 0, 0          ), resp('rd', 0x08, 1, 0, 0x00000004 ), # read word  0x00001000
    req( 'wr', 0x09, 0x00002000, 0, 0x00000020 ), resp('rd', 0x09, 0, 0, 0          ), # read word  0x00001000
    req( 'rd', 0x10, 0x00002000, 0, 0          ), resp('rd', 0x10, 1, 0, 0x00000020 ), # read word  0x00001000
    req( 'rd', 0x11, 0x00002004, 0, 0          ), resp('rd', 0x11, 1, 0, 0x00000022 ), # read word  0x00001000
    req( 'rd', 0x12, 0x00002008, 0, 0          ), resp('rd', 0x12, 1, 0, 0x00000023 ), # read word  0x00001000
    req( 'rd', 0x13, 0x0000200c, 0, 0          ), resp('rd', 0x13, 1, 0, 0x00000024 ), # read word  0x00001000
 
  ]

# Data to be loaded into memory before running the test

def write_miss_wr_we_assoc_1_mem( base_addr ):
  return [
    # addr      data (in int)
    0x00000000, 0xdeadbeef,
    0x00000004, 0x00c0ffee,
    0x00000008, 0xabcdefab,
    0x0000000c, 0x01234567, 
    0x00000010, 0xdededede,   
    0x00001000, 0x00000001, 
    0x00001004, 0x00000002,
    0x00001008, 0x00000003,
    0x0000100c, 0x00000004,
    0x00002000, 0x00000021, 
    0x00002004, 0x00000022,
    0x00002008, 0x00000023,
    0x0000200c, 0x00000024,
  ]
#'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# Stress test 
#''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''' 
def stress_assoc (base_addr): 
  stress_assoc_msgs = []
  for k in range(2): 
    for i in range(8):
      for j in range(4): 
        if (j == 0):
          hit = 0
        else: 
          hit = 1 
        tag = k << 7 
        offset = j << 2  
        index = i << 4 
        addr = tag | index | offset 
        data = 32*k + i*4 + j 
        opq = 32*k + i*4 + j 
        stress_assoc_msgs.extend([req('rd', i*4+j, addr, 0, 0), resp('rd', i*4+j, hit, 0, data)])
  return stress_assoc_msgs

def stress_assoc_mem(base_addr):
  stress_assoc_mem_msgs = []
  for k in range(2):
    for i in range(8):
      for j in range(4): 
        tag = k << 7
        offset = j << 2  
        index = i << 4 
        addr = tag| index | offset 
        data = 32*k + i*4 + j 
        stress_assoc_mem_msgs.extend([addr, data])
  return stress_assoc_mem_msgs 
      
#'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# Conflict misses
#''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''' 
def conflict_miss_assoc( base_addr ):
  return [
    #    type  opq   addr      len  data               type  opq test len  data
    req( 'rd', 0x00, 0x00000000, 0, 0          ), resp('rd', 0x00, 0, 0, 0xdeadbeef ), # read word  0x00000000
    req( 'rd', 0x01, 0x00000004, 0, 0          ), resp('rd', 0x01, 1, 0, 0x00c0ffee ), # read word  0x00000004
    req( 'rd', 0x02, 0x00000008, 0, 0          ), resp('rd', 0x02, 1, 0, 0xabcdefab ), # read word  0x00000008
    req( 'rd', 0x03, 0x0000000c, 0, 0          ), resp('rd', 0x03, 1, 0, 0x01234567 ), # read word  0x0000000c
    req( 'rd', 0x04, 0x00000010, 0, 0          ), resp('rd', 0x04, 0, 0, 0xdededede ), # read word  0x00000010
    req( 'rd', 0x05, 0x00001000, 0, 0          ), resp('rd', 0x05, 0, 0, 0x00000001 ), # read word  0x00001000
    req( 'rd', 0x06, 0x00001004, 0, 0          ), resp('rd', 0x06, 1, 0, 0x00000002 ), # read word  0x00001000
    req( 'rd', 0x07, 0x00001008, 0, 0          ), resp('rd', 0x07, 1, 0, 0x00000003 ), # read word  0x00001000
    req( 'rd', 0x08, 0x0000100c, 0, 0          ), resp('rd', 0x08, 1, 0, 0x00000004 ), # read word  0x00001000
    req( 'rd', 0x09, 0x00000000, 0, 0          ), resp('rd', 0x09, 1, 0, 0xdeadbeef ), # read word  0x00000000
    req( 'rd', 0x10, 0x00002000, 0, 0          ), resp('rd', 0x10, 0, 0, 0x00000021 ), # read word  0x00001000
    req( 'rd', 0x11, 0x00002004, 0, 0          ), resp('rd', 0x11, 1, 0, 0x00000022 ), # read word  0x00001000
    req( 'rd', 0x12, 0x00002008, 0, 0          ), resp('rd', 0x12, 1, 0, 0x00000023 ), # read word  0x00001000
    req( 'rd', 0x13, 0x0000200c, 0, 0          ), resp('rd', 0x13, 1, 0, 0x00000024 ), # read word  0x00001000
    req( 'rd', 0x14, 0x00000000, 0, 0          ), resp('rd', 0x14, 1, 0, 0xdeadbeef ), # read word  0x00000000
    req( 'rd', 0x15, 0x00001000, 0, 0          ), resp('rd', 0x15, 0, 0, 0x00000001 ), # read word  0x00001000
 
  ]

# Data to be loaded into memory before running the test

def conflict_miss_assoc_mem( base_addr ):
  return [
    # addr      data (in int)
    0x00000000, 0xdeadbeef,
    0x00000004, 0x00c0ffee,
    0x00000008, 0xabcdefab,
    0x0000000c, 0x01234567, 
    0x00000010, 0xdededede,   
    0x00001000, 0x00000001, 
    0x00001004, 0x00000002,
    0x00001008, 0x00000003,
    0x0000100c, 0x00000004,
    0x00002000, 0x00000021, 
    0x00002004, 0x00000022,
    0x00002008, 0x00000023,
    0x0000200c, 0x00000024,
  ]
def conflict_miss_assoc_1( base_addr ):
  return [
    #    type  opq   addr      len  data               type  opq test len  data
    req( 'rd', 0x00, 0x00000000, 0, 0          ), resp('rd', 0x00, 0, 0, 0xdeadbeef ), #replace index 0
    req( 'rd', 0x01, 0x00000004, 0, 0          ), resp('rd', 0x01, 1, 0, 0x00c0ffee ), 
    req( 'rd', 0x02, 0x00000008, 0, 0          ), resp('rd', 0x02, 1, 0, 0xabcdefab ), 
    req( 'rd', 0x03, 0x0000000c, 0, 0          ), resp('rd', 0x03, 1, 0, 0x01234567 ),
    req( 'rd', 0x04, 0x00000010, 0, 0          ), resp('rd', 0x04, 0, 0, 0xdededede ), #replace index 1
    req( 'wr', 0x05, 0x00001000, 0, 0x00000010 ), resp('wr', 0x05, 0, 0, 0          ), #replace index 0
    req( 'rd', 0x05, 0x00001000, 0, 0          ), resp('rd', 0x05, 1, 0, 0x00000010 ), 
    req( 'rd', 0x06, 0x00001004, 0, 0          ), resp('rd', 0x06, 1, 0, 0x00000002 ), 
    req( 'rd', 0x07, 0x00001008, 0, 0          ), resp('rd', 0x07, 1, 0, 0x00000003 ), 
    req( 'rd', 0x08, 0x0000100c, 0, 0          ), resp('rd', 0x08, 1, 0, 0x00000004 ), 
    req( 'rd', 0x09, 0x00000000, 0, 0          ), resp('rd', 0x09, 1, 0, 0xdeadbeef ), 
    req( 'wr', 0x09, 0x00002000, 0, 0x00000020 ), resp('rd', 0x09, 0, 0, 0          ), #replace index 0
    req( 'rd', 0x10, 0x00002000, 0, 0          ), resp('rd', 0x10, 1, 0, 0x00000020 ), 
    req( 'rd', 0x11, 0x00002004, 0, 0          ), resp('rd', 0x11, 1, 0, 0x00000022 ), 
    req( 'rd', 0x12, 0x00002008, 0, 0          ), resp('rd', 0x12, 1, 0, 0x00000023 ), 
    req( 'rd', 0x13, 0x0000200c, 0, 0          ), resp('rd', 0x13, 1, 0, 0x00000024 ), 
    req( 'rd', 0x14, 0x00000000, 0, 0          ), resp('rd', 0x14, 1, 0, 0xdeadbeef ), 
    req( 'rd', 0x15, 0x00001000, 0, 0          ), resp('rd', 0x15, 0, 0, 0x00000010 ), #evict and replace index 0
 
  ]

# Data to be loaded into memory before running the test

def conflict_miss_assoc_mem_1( base_addr ):
  return [
    # addr      data (in int)
    0x00000000, 0xdeadbeef,
    0x00000004, 0x00c0ffee,
    0x00000008, 0xabcdefab,
    0x0000000c, 0x01234567, 
    0x00000010, 0xdededede,   
    0x00001000, 0x00000001, 
    0x00001004, 0x00000002,
    0x00001008, 0x00000003,
    0x0000100c, 0x00000004,
    0x00002000, 0x00000021, 
    0x00002004, 0x00000022,
    0x00002008, 0x00000023,
    0x0000200c, 0x00000024,
  ]
def shorter_conflict_miss_assoc_1 (base_addr): 
   return [
    #    type  opq   addr      len  data               type  opq test len  data
    req( 'rd', 0x00, 0x00000000, 0, 0          ), resp('rd', 0x00, 0, 0, 0xdeadbeef ), #replace index 0 lru 1
    req( 'rd', 0x01, 0x00000010, 0, 0          ), resp('rd', 0x01, 0, 0, 0xdededede ), #replace index 1 lru 1 
    req( 'wr', 0x02, 0x00001000, 0, 0x00000010 ), resp('wr', 0x02, 0, 0, 0          ), #replace index 0 lru 0
    req( 'rd', 0x03, 0x00001000, 0, 0          ), resp('rd', 0x03, 1, 0, 0x00000010 ), 
    req( 'rd', 0x04, 0x00000000, 0, 0          ), resp('rd', 0x04, 1, 0, 0xdeadbeef ), #lru 1
    req( 'wr', 0x05, 0x00002000, 0, 0x00000020 ), resp('rd', 0x05, 0, 0, 0          ), #evict and replace index 0 lru 0
    req( 'rd', 0x06, 0x00002000, 0, 0          ), resp('rd', 0x06, 1, 0, 0x00000020 ), 
    req( 'rd', 0x07, 0x00000000, 0, 0          ), resp('rd', 0x07, 1, 0, 0xdeadbeef ), #lru 1
    req( 'rd', 0x08, 0x00001000, 0, 0          ), resp('rd', 0x08, 0, 0, 0x00000010 ), #evict and replace index 0 lru 0
 
  ]
def shorter_conflict_miss_assoc_mem_1( base_addr ):
  return [
    # addr      data (in int)
    0x00000000, 0xdeadbeef,
    0x00000004, 0x00c0ffee,
    0x00000008, 0xabcdefab,
    0x0000000c, 0x01234567, 
    0x00000010, 0xdededede,   
    0x00001000, 0x00000001, 
    0x00001004, 0x00000002,
    0x00001008, 0x00000003,
    0x0000100c, 0x00000004,
    0x00002000, 0x00000021, 
    0x00002004, 0x00000022,
    0x00002008, 0x00000023,
    0x0000200c, 0x00000024,
  ]

def flipbit (lru):
  if (lru == 0):
      return 1
  else: 
      return 0

def lru_replacement(base_addr): 
  now = datetime.now()
  current_time = now.strftime("%H:%M:%S")
  if os.path.exists("lru_replacement.txt"):
    os.remove("lru_replacement.txt")
  with open("lru_replacement.txt", "w") as f:
    f.write("Data for LRU at " + current_time + "\n")
  lru_replacement_msgs = []
  cache = [-1,-1]
  lru = 0
  for i in range(50): 
    tag = random.randint(0,3) 
    hit = 0
    if (cache[flipbit(lru)] == tag): 
        hit = 1 
    if (cache[lru] == tag):
        hit = 1 
        lru = flipbit(lru)
    if (hit == 0): 
        cache[lru] = tag 
        lru = flipbit(lru) 
    data = tag + 1
    addr = tag << 7
    with open("lru_replacement.txt", "a") as f:
      f.write("addr " + '{:04x}'.format(addr) + " data " + str(data) + " hit " + str(hit) + "\n")
    lru_replacement_msgs.extend([req('rd', i, addr, 0, 0), resp('rd', i, hit, 0, data)]) 
  return lru_replacement_msgs   

def lru_replacement_mem(base_addr):
  return [
    # addr      data (in int)
    0x00000000, 0x00000001,
    0x00000080, 0x00000002,
    0x00000100, 0x00000003,
    0x00000180, 0x00000004,
  ]

def lru_replacement_1 (base_addr): 
   return [
    #    type  opq   addr      len  data               type  opq test len  data
    req( 'rd', 0x00, 0x00000180, 0, 0          ), resp('rd', 0x00, 0, 0, 0x00000004 ), 
    req( 'rd', 0x01, 0x00000000, 0, 0          ), resp('rd', 0x01, 0, 0, 0x00000001 ), 
    req( 'rd', 0x02, 0x00000000, 0, 0          ), resp('rd', 0x02, 1, 0, 0x00000001 ), 
    req( 'rd', 0x03, 0x00000180, 0, 0          ), resp('rd', 0x03, 1, 0, 0x00000004 ), 
   ] 

def cacheline_int_assoc (tag, index, cache, tag_mem, msgs, num, lru, name): 
  tag_mem.add(tag)
  offset = ['0', '4', '8', 'c']
  for i in range (4): 
    if (i == 0): 
      hit = 0 
    else:
      hit = 1
    addr_hex = tag + offset[i]
    data = random.randint(0, 0xFFFFFFFF)
    cache[lru][index][i+1] = data 
    addr = int(addr_hex, 16) 
    with open(name, "a") as f:
      f.write("wr " + "addr " + addr_hex + " data " + str(data) + " hit " + str(hit) + " index " + str(index) + " lru " + str(lru) + "\n")  
    msgs.extend([req('wr', num, addr, 0, data), resp('wr', num, hit, 0, 0)])
    num += 1
    if (num > 255): num = 0
  return num     

def cacheline_refill_assoc (tag, index, cache, mem, lru):
  offset = ['0', '4', '8', 'c']
  for i in range(4):
    addr_hex = tag + offset[i]
    if (addr_hex not in mem):
      data = 0
    else: 
      data = mem[addr_hex]
    cache[lru][index][i+1] = data 
    
def cacheline_evict_assoc (index, cache, mem, lru):
  offset = ['0', '4', '8', 'c']
  tag_hex = '{:07x}'.format(cache[lru][index][0])
  for i in range(4):
    addr_hex = tag_hex + offset[i] 
    mem[addr_hex] = cache[lru][index][i+1]

def read_request_assoc (addr, refcache, refmem, reftag, num_inst, msgs, lru_array, name): 
  offset_dic = {'0':1, '4':2, '8':3, 'c':4} 
  addr_hex = '{:08x}'.format(addr)
  offset_hex = addr_hex[-1]
  tag_hex = addr_hex[:len(addr_hex)-1]
  addr_bin = '{:032b}'.format(addr)
  index_bin = addr_bin[25:28]
  tag = int(tag_hex,16)
  index = int(index_bin, 2)
  offset = int(offset_hex, 16)
  hit = 1
  lru = lru_array[index]
  if ((refcache[0][index][0] != tag) and (refcache[1][index][0] != tag)):
    if (refcache[lru][index][0] != -1):
      cacheline_evict_assoc(index, refcache, refmem, lru)
    if (tag_hex not in reftag):
      num_inst = cacheline_int_assoc (tag_hex, index, refcache, reftag, msgs, num_inst, lru, name)
    else: 
      cacheline_refill_assoc(tag_hex, index, refcache, refmem, lru)
      hit = 0
    refcache[lru][index][0] = tag
    lru_array[index] = flipbit(lru)
  else: 
    if (refcache[lru][index][0] == tag):
      lru_array[index] = flipbit(lru)
  if (refcache[0][index][0] == tag):
    data = refcache[0][index][offset_dic[offset_hex]]
  else:
    data = refcache[1][index][offset_dic[offset_hex]]
  with open(name, "a") as f:
    f.write("rd " + "addr " + addr_hex + " data " + str(data) + " hit " + str(hit) + " index " + str(index) + " lru " + str(lru) + "\n")
  msgs.extend([req('rd', num_inst, addr, 0, 0),resp('rd', num_inst, hit, 0, data)])
  num_inst += 1
  if (num_inst > 255): num_inst = 0
  return num_inst

def write_request_assoc (addr, refcache, refmem, reftag, num_inst, msgs, lru_array, name):
  offset_dic = {'0':1, '4':2, '8':3, 'c':4} 
  addr_hex = '{:08x}'.format(addr)
  offset_hex = addr_hex[-1]
  tag_hex = addr_hex[:len(addr_hex)-1]
  addr_bin = '{:032b}'.format(addr)
  index_bin = addr_bin[25:28]
  tag = int(tag_hex,16)
  index = int(index_bin, 2)
  offset = int(offset_hex, 16)
  hit = 1
  lru = lru_array[index]
  data = random.randint(0, 0xFFFFFFFF)
  if ((refcache[0][index][0] != tag) and (refcache[1][index][0] != tag)):
    if (refcache[lru][index][0] != -1):
      cacheline_evict_assoc(index, refcache, refmem, lru)
    if (tag_hex not in reftag):
      num_inst = cacheline_int_assoc (tag_hex, index, refcache, reftag, msgs, num_inst, lru, name)
    else: 
      cacheline_refill_assoc(tag_hex, index, refcache, refmem, lru)
      hit = 0
    refcache[lru][index][0] = tag
    lru_array[index] = flipbit(lru)
  else: 
    if (refcache[lru][index][0] == tag):
      lru_array[index] = flipbit(lru)
  if (refcache[0][index][0] == tag):
      refcache[0][index][offset_dic[offset_hex]] = data
  else:
      refcache[1][index][offset_dic[offset_hex]] = data
  with open(name, "a") as f:
    f.write("wr " + "addr " + addr_hex + " data " + str(data) + " hit " + str(hit) + " index " + str(index) + " lru " + str(lru) + "\n")
  msgs.extend([req('wr', num_inst, addr, 0, data),resp('wr', num_inst, hit, 0, 0)])
  num_inst += 1
  if (num_inst > 255): num_inst = 0
  return num_inst

def random_randata_assoc (base_addr):
  random_randata_assoc_msgs = []
  refmem = {} 
  reftag = set()  
  refcache_0 = [[-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1]]
  refcache_1 =[[-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1]]
  lru_array = [0, 0, 0, 0, 0, 0, 0, 0]
  refcache = [refcache_0, refcache_1]
  num_inst = 0 
  now = datetime.now()
  current_time = now.strftime("%H:%M:%S")
  name = "random_randata_assoc.txt"
  addr_array = [] 
  if os.path.exists(name):
    os.remove(name)
  with open(name, "w") as f:
    f.write("Data for simple address patterns, simple request type, random data " + current_time + "\n") 
  for i in range(75):
    addr = i << 2
    num_inst = read_request_assoc (addr, refcache, refmem, reftag, num_inst, random_randata_assoc_msgs, lru_array, name)
  for i in range(75):
    addr = i << 2 
    num_inst = read_request_assoc (addr, refcache, refmem, reftag, num_inst, random_randata_assoc_msgs, lru_array, name)
  return random_randata_assoc_msgs

def random_rantypedata_assoc (base_addr):
  random_rantypedata_assoc_msgs = []
  refmem = {} 
  reftag = set()  
  refcache_0 = [[-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1]]
  refcache_1 =[[-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1]]
  lru_array = [0, 0, 0, 0, 0, 0, 0, 0]
  refcache = [refcache_0, refcache_1]
  num_inst = 0 
  now = datetime.now()
  current_time = now.strftime("%H:%M:%S")
  name = "random_rantypedata_assoc.txt"
  addr_array = [] 
  if os.path.exists(name):
    os.remove(name)
  with open(name, "w") as f:
    f.write("Data for simple address patterns, random request type, random data " + current_time + "\n") 
  for i in range(75):
    addr = i << 2
    req_type = random.randint(0, 1)
    if (req_type == 0):
        num_inst = read_request_assoc (addr, refcache, refmem, reftag, num_inst, random_rantypedata_assoc_msgs, lru_array, name)
    else:
        num_inst = write_request_assoc (addr, refcache, refmem, reftag, num_inst, random_rantypedata_assoc_msgs, lru_array, name)
  for i in range(75):
    addr = i << 2 
    num_inst = read_request_assoc (addr, refcache, refmem, reftag, num_inst, random_rantypedata_assoc_msgs, lru_array, name)
  return random_rantypedata_assoc_msgs

def random_ranaddrtypedata_assoc (base_addr):
  random_ranaddrtypedata_assoc_msgs = []
  refmem = {} 
  reftag = set()  
  refcache_0 = [[-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1]]
  refcache_1 =[[-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1]]
  lru_array = [0, 0, 0, 0, 0, 0, 0, 0]
  refcache = [refcache_0, refcache_1]
  num_inst = 0 
  now = datetime.now()
  current_time = now.strftime("%H:%M:%S")
  name = "random_ranaddrtypedata_assoc.txt"
  addr_array = [] 
  if os.path.exists(name):
    os.remove(name)
  with open(name, "w") as f:
    f.write("Data for random address patterns, random request type, random data " + current_time + "\n") 
  for i in range(100):
    addr = random.randint(0, 0x0000FFFF) << 2
    addr_array.append(addr) 
    req_type = random.randint(0, 1)
    if (req_type == 0):
        num_inst = read_request_assoc (addr, refcache, refmem, reftag, num_inst, random_ranaddrtypedata_assoc_msgs, lru_array, name)
    else:
        num_inst = write_request_assoc (addr, refcache, refmem, reftag, num_inst, random_ranaddrtypedata_assoc_msgs, lru_array, name)
  for i in range(100):
    addr = addr_array[i]
    num_inst = read_request_assoc (addr, refcache, refmem, reftag, num_inst, random_ranaddrtypedata_assoc_msgs, lru_array, name)
  return random_ranaddrtypedata_assoc_msgs

def random_ranaddrtypedata_assoc_1 (base_addr):
  random_ranaddrtypedata_assoc_1_msgs = []
  refmem = {} 
  reftag = set()  
  refcache_0 = [[-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1]]
  refcache_1 =[[-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1]]
  lru_array = [0, 0, 0, 0, 0, 0, 0, 0]
  refcache = [refcache_0, refcache_1]
  num_inst = 0 
  now = datetime.now()
  current_time = now.strftime("%H:%M:%S")
  name = "random_ranaddrtypedata_assoc_1.txt"
  addr_array = [] 
  if os.path.exists(name):
    os.remove(name)
  with open(name, "w") as f:
    f.write("Data for random address patterns, random request type, random data " + current_time + "\n") 
  for i in range(100):
    addr = random.randint(0, 0x0000007F) << 2
    addr_array.append(addr) 
    req_type = random.randint(0, 1)
    if (req_type == 0):
        num_inst = read_request_assoc (addr, refcache, refmem, reftag, num_inst, random_ranaddrtypedata_assoc_1_msgs, lru_array, name)
    else:
        num_inst = write_request_assoc (addr, refcache, refmem, reftag, num_inst, random_ranaddrtypedata_assoc_1_msgs, lru_array, name)
  for i in range(100):
    addr = addr_array[i]
    num_inst = read_request_assoc (addr, refcache, refmem, reftag, num_inst, random_ranaddrtypedata_assoc_1_msgs, lru_array, name)
  return random_ranaddrtypedata_assoc_1_msgs


#----------------------------------------------------------------------
# Banked cache test
#----------------------------------------------------------------------
# The test field in the response message: 0 == MISS, 1 == HIT

# This test case is to test if the bank offset is implemented correctly.
#
# The idea behind this test case is to differentiate between a cache
# with no bank bits and a design has one/two bank bits by looking at cache
# request hit/miss status.

#'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# LAB TASK:
#'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
def banking_zero( base_addr ):
  return [
    #    type  opq  addr      len data                type  opq  test len data
    req( 'in', 0x0, 0x00000000, 0, 0xdeadbeef ), resp( 'in', 0x0, 0,   0,  0          ),
    req( 'rd', 0x1, 0x00000000, 0, 0          ), resp( 'rd', 0x1, 1,   0,  0xdeadbeef ),
    req( 'wr', 0x2, 0x00000010, 0, 0x00000001 ), resp( 'wr', 0x2, 0,   0,  0          ), 
  ]

def banking_four( base_addr ):
  return [
    #    type  opq  addr      len data                type  opq  test len data
    req( 'in', 0x0, 0x00000000, 0, 0xdeadbeef ), resp( 'in', 0x0, 0,   0,  0          ),
    req( 'rd', 0x1, 0x00000000, 0, 0          ), resp( 'rd', 0x1, 1,   0,  0xdeadbeef ),
  ]

#-------------------------------------------------------------------------
# Test table for generic test
#-------------------------------------------------------------------------

test_case_table_generic = mk_test_case_table([
  (                         "msg_func               mem_data_func           nbank stall lat src sink"),
  [ "read_hit_1word_clean",  read_hit_1word_clean,  None,                   0,    0.0,  0,  0,  0    ],
  [ "read_miss_1word",       read_miss_1word_msg,   read_miss_1word_mem,    0,    0.0,  0,  0,  0    ],
  [ "read_hit_1word_4bank",  read_hit_1word_clean,  None,                   4,    0.0,  0,  0,  0    ],
  [ "read_hit_clean",        read_hit_clean,        None,                   0,    0.0,  0,  0,  0    ],
  [ "write_hit_clean",       write_hit_clean,       None,                   0,    0.0,  0,  0,  0    ],
  [ "read_hit_dirty",        read_hit_dirty,        read_hit_dirty_mem,     0,    0.0,  0,  0,  0    ],
  [ "write_hit_dirty",       write_hit_dirty,       write_hit_dirty_mem,    0,    0.0,  0,  0,  0    ],
  [ "read_miss_wr_woe",      read_miss_wr_woe,      read_miss_wr_woe_mem,   0,    0.0,  0,  0,  0    ],
  [ "write_miss_wr_woe",     write_miss_wr_woe,     write_miss_wr_woe_mem,  0,    0.0,  0,  0,  0    ],

  #'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  # LAB TASK: Add test cases to this table
  #'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

])

@pytest.mark.parametrize( **test_case_table_generic )
def test_generic( test_params, dump_vcd ):
  msgs = test_params.msg_func( 0 )
  if test_params.mem_data_func != None:
    mem = test_params.mem_data_func( 0 )
  # Instantiate testharness
  harness = TestHarness( msgs[::2], msgs[1::2],
                         test_params.stall, test_params.lat,
                         test_params.src, test_params.sink,
                         BlockingCacheFL, test_params.nbank,
                         False, dump_vcd )
  # Load memory before the test
  if test_params.mem_data_func != None:
    harness.load( mem[::2], mem[1::2] )
  # Run the test
  run_sim( harness, dump_vcd )

#-------------------------------------------------------------------------
# Test table for set-associative cache (alternative design)
#-------------------------------------------------------------------------

test_case_table_set_assoc = mk_test_case_table([
  (                                   "msg_func                       mem_data_func                 nbank stall lat src sink"),
  [ "read_hit_asso",                  read_hit_asso,                  None,                               0,    0.0,  0,  0,  0    ],
  [ "read_hit_clean",                 read_hit_clean,                 None,                               0,    0.0,  0,  0,  0    ],
  [ "write_hit_clean",                write_hit_clean,                None,                               0,    0.0,  0,  0,  0    ],
  [ "read_hit_dirty",                 read_hit_dirty,                 read_hit_dirty_mem,                 0,    0.0,  0,  0,  0    ],
  [ "write_hit_dirty",                write_hit_dirty,                write_hit_dirty_mem,                0,    0.0,  0,  0,  0    ],
  [ "read_miss_wr_woe",               read_miss_wr_woe,               read_miss_wr_woe_mem,               0,    0.0,  0,  0,  0    ],
  [ "write_miss_wr_woe",              write_miss_wr_woe,              write_miss_wr_woe_mem,              0,    0.0,  0,  0,  0    ],
  [ "read_miss_wr_we_assoc",          read_miss_wr_we_assoc,          read_miss_wr_we_assoc_mem,          0,    0.0,  0,  0,  0    ],
  [ "write_miss_wr_we_assoc",         write_miss_wr_we_assoc,         write_miss_wr_we_assoc_mem,         0,    0.0,  0,  0,  0    ],
  [ "write_miss_wr_we_assoc_1",       write_miss_wr_we_assoc_1,       write_miss_wr_we_assoc_1_mem,       0,    0.0,  0,  0,  0    ],
  [ "conflict_miss_assoc",            conflict_miss_assoc,            conflict_miss_assoc_mem,            0,    0.0,  0,  0,  0    ], 
  [ "shorter_conflict_miss_assoc_1",  shorter_conflict_miss_assoc_1,  shorter_conflict_miss_assoc_mem_1,  0,    0.0,  0,  0,  0    ],
  [ "conflict_miss_assoc_1",          conflict_miss_assoc_1,          conflict_miss_assoc_mem_1,          0,    0.0,  0,  0,  0    ], 
  [ "stress_assoc",                   stress_assoc,                   stress_assoc_mem,                   0,    0.0,  0,  0,  0    ],
  [ "lru_replacement_1",              lru_replacement_1,              lru_replacement_mem,                0,    0.0,  0,  0,  0    ],
  [ "lru_replacement",                lru_replacement,                lru_replacement_mem,                0,    0.0,  0,  0,  0    ],
  [ "random_randata_assoc",           random_randata_assoc,           None,                               0,    0.0,  0,  0,  0    ],
  [ "random_rantypedata_assoc",       random_rantypedata_assoc,       None,                               0,    0.0,  0,  0,  0    ],
  [ "random_ranaddrtypedata_assoc",   random_ranaddrtypedata_assoc,   None,                               0,    0.0,  0,  0,  0    ],
  [ "random_ranaddrtypedata_assoc_1", random_ranaddrtypedata_assoc_1, None,                               0,    0.0,  0,  0,  0,   ],

  #'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  # LAB TASK: Add test cases to this table
  #'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

])

@pytest.mark.parametrize( **test_case_table_set_assoc )
def test_set_assoc( test_params, dump_vcd ):
  msgs = test_params.msg_func( 0 )
  if test_params.mem_data_func != None:
    mem  = test_params.mem_data_func( 0 )
  # Instantiate testharness
  harness = TestHarness( msgs[::2], msgs[1::2],
                         test_params.stall, test_params.lat,
                         test_params.src, test_params.sink,
                         BlockingCacheFL, test_params.nbank,
                         False, dump_vcd )
  # Load memory before the test
  if test_params.mem_data_func != None:
    harness.load( mem[::2], mem[1::2] )
  # Run the test
  run_sim( harness, dump_vcd )


#-------------------------------------------------------------------------
# Test table for direct-mapped cache (baseline design)
#-------------------------------------------------------------------------

test_case_table_dir_mapped = mk_test_case_table([
  (                                 "msg_func                     mem_data_func                   nbank stall lat src sink"),
  [ "read_hit_dmap",                read_hit_dmap,                None,                           0,    0.0,  0,  0,  0    ],
  [ "read_hit_clean",               read_hit_clean,               None,                           0,    0.0,  0,  0,  0    ],
  [ "write_hit_clean",              write_hit_clean,              None,                           0,    0.0,  0,  0,  0    ],
  [ "read_hit_dirty",               read_hit_dirty,               read_hit_dirty_mem,             0,    0.0,  0,  0,  0    ],
  [ "write_hit_dirty",              write_hit_dirty,              write_hit_dirty_mem,            0,    0.0,  0,  0,  0    ],
  [ "read_miss_wr_woe",             read_miss_wr_woe,             read_miss_wr_woe_mem,           0,    0.0,  0,  0,  0    ],
  [ "write_miss_wr_woe",            write_miss_wr_woe,            write_miss_wr_woe_mem,          0,    0.0,  0,  0,  0    ],
  [ "read_miss_wr_we_dt",           read_miss_wr_we_dt,           read_miss_wr_we_dt_mem,         0,    0.0,  0,  0,  0    ],
  [ "write_miss_wr_we_dt",          write_miss_wr_we_dt,          write_miss_wr_we_dt_mem,        0,    0.0,  0,  0,  0    ],
  [ "conflict_miss_dt",             conflict_miss_dt,             conflict_miss_dt_mem,           0,    0.0,  0,  0,  0    ], 
  [ "conflict_miss_dt_1",           conflict_miss_dt_1,           conflict_miss_dt_mem_1,         0,    0.0,  0,  0,  0    ], 
  [ "stress_dt",                    stress_dt,                    stress_dt_mem,                  0,    0.0,  0,  0,  0    ],
  [ "capacity_dt",                  capacity_dt,                  capacity_dt_mem,                0,    0.0,  0,  0,  0    ],
  [ "random_randata_dt",            random_randata_dt,            None,                           0,    0.0,  0,  0,  0    ],
  [ "random_rantypedata_dt",        random_rantypedata_dt,        None,                           0,    0.0,  0,  0,  0    ],
  [ "random_ranaddrtypedata_dt",    random_ranaddrtypedata_dt,    None,                           0,    0.0,  0,  0,  0    ],
  [ "check_random_test_dt",         check_random_test_dt,         None,                           0,    0.0,  0,  0,  0    ],
  [ "random_ranaddrtypedata_dt_1",  random_ranaddrtypedata_dt_1,  None,                           0,    0.0,  0,  0,  0    ],
  #'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  # LAB TASK: Add test cases to this table
  #'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

])

@pytest.mark.parametrize( **test_case_table_dir_mapped )
def test_dir_mapped( test_params, dump_vcd ):
  msgs = test_params.msg_func( 0 )
  if test_params.mem_data_func != None:
    mem  = test_params.mem_data_func( 0 )
  # Instantiate testharness
  harness = TestHarness( msgs[::2], msgs[1::2],
                         test_params.stall, test_params.lat,
                         test_params.src, test_params.sink,
                         BlockingCacheFL, test_params.nbank,
                         False, dump_vcd )
  # Load memory before the test
  if test_params.mem_data_func != None:
    harness.load( mem[::2], mem[1::2] )
  # Run the test
  run_sim( harness, dump_vcd )
