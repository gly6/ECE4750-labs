#=========================================================================
# ProcDpathComponentsRTL_test.py
#=========================================================================

import pytest
import random

from pymtl      import *
from harness    import *
from pclib.test import mk_test_case_table, run_sim
from pclib.test import run_test_vector_sim

from lab2_proc.ProcDpathComponentsRTL import ImmGenRTL
from lab2_proc.ProcDpathComponentsRTL import AluRTL

#-------------------------------------------------------------------------
# ImmGenRTL
#-------------------------------------------------------------------------

def test_immgen( test_verilog, dump_vcd ):

  header_str = \
  ( "imm_type", "inst",
    "imm*" )
  
  run_test_vector_sim( ImmGenRTL(), [ header_str,
    # imm_type inst                                imm
    [ 0,       0b11111111111100000000000000000000, 0b11111111111111111111111111111111], # I-imm
    [ 0,       0b00000000000011111111111111111111, 0b00000000000000000000000000000000], # I-imm
    [ 0,       0b01111111111100000000000000000000, 0b00000000000000000000011111111111], # I-imm
    [ 0,       0b11111111111000000000000000000000, 0b11111111111111111111111111111110], # I-imm
    [ 1,       0b11111110000000000000111110000000, 0b11111111111111111111111111111111], # S-imm
    [ 1,       0b00000001111111111111000001111111, 0b00000000000000000000000000000000], # S-imm
    [ 1,       0b01111110000000000000111110000000, 0b00000000000000000000011111111111], # S-imm
    [ 1,       0b11111110000000000000111100000000, 0b11111111111111111111111111111110], # S-imm
    [ 2,       0b11111110000000000000111110000000, 0b11111111111111111111111111111110], # B-imm
    [ 2,       0b00000001111111111111000001111111, 0b00000000000000000000000000000000], # B-imm
    [ 2,       0b11000000000000000000111100000000, 0b11111111111111111111010000011110], # B-imm
    [ 3,       0b11111111111111111111000000000000, 0b11111111111111111111000000000000], # U-imm
    [ 3,       0b00000000000000000000111111111111, 0b00000000000000000000000000000000], # U-imm
    [ 4,       0b11111111111111111111000000000000, 0b11111111111111111111111111111110], # J-imm
    [ 4,       0b00000000000000000001111111111111, 0b00000000000000000001000000000000], # J-imm
    [ 4,       0b01000000000010011001000000000000, 0b00000000000010011001010000000000], # J-imm
  ], dump_vcd, test_verilog )

#-------------------------------------------------------------------------
# AluRTL
#-------------------------------------------------------------------------

def test_alu_add( dump_vcd, test_verilog ):
  run_test_vector_sim( AluRTL(), [
    ('in0           in1           fn  out*          ops_eq*   ops_lt*  ops_ltu*'),
    [ 0x00000000,   0x00000000,   0,  0x00000000,   '?',      '?',       '?'      ],
    [ 0x0ffaa660,   0x00012304,   0,  0x0ffbc964,   '?',      '?',       '?'      ],
    #pos-neg
    [ 0x00132050,   0xd6620040,   0,  0xd6752090,   '?',      '?',       '?'      ],
    [ 0xfff0a440,   0x00004450,   0,  0xfff0e890,   '?',      '?',       '?'      ],
    # neg-neg
    [ 0xfeeeeaa3,   0xf4650000,   0,  0xf353eaa3,   '?',      '?',       '?'      ],
  ], dump_vcd, test_verilog )

def test_alu_sub( dump_vcd, test_verilog ):
  run_test_vector_sim( AluRTL(), [
    ('in0           in1           fn  out*          ops_eq*   ops_lt*  ops_ltu*'),
    [ 0x00000000,   0x00000000,   1,  0x00000000,   '?',      '?',       '?'      ],
    [ 0x0ffaa660,   0x00012304,   1,  0x0FF9835C,   '?',      '?',       '?'      ],
    #pos-neg
    [ 0x00132050,   0xd6620040,   1,  0x29B12010,   '?',      '?',       '?'      ],
    [ 0xfff0a440,   0x00004450,   1,  0xFFF05FF0,   '?',      '?',       '?'      ],
    # neg-neg
    [ 0xfeeeeaa3,   0xf4650000,   1,  0x0A89EAA3,   '?',      '?',       '?'      ],
  ], dump_vcd, test_verilog )

def test_alu_and( dump_vcd, test_verilog ):
  run_test_vector_sim( AluRTL(), [
    ('in0           in1           fn  out*          ops_eq*   ops_lt*  ops_ltu*'),
    [ 0x00000000,   0x00000000,   2,  0x00000000,   '?',      '?',       '?'      ],
    [ 0x0ffaa660,   0x00012304,   2,  0x00002200,   '?',      '?',       '?'      ],
    #pos-neg
    [ 0x00132050,   0xd6620040,   2,  0x00020040,   '?',      '?',       '?'      ],
    [ 0xfff0a440,   0x00004450,   2,  0x00000440,   '?',      '?',       '?'      ],
    # neg-neg
    [ 0xfeeeeaa3,   0xf4650000,   2,  0xf4640000,   '?',      '?',       '?'      ],
    [ 0xffffffff,   0xffffffff,   2,  0xffffffff,   '?',      '?',       '?'      ],
    [ 0x00000000,   0xffffffff,   2,  0x00000000,   '?',      '?',       '?'      ],
    [ 0xffffffff,   0x00000000,   2,  0x00000000,   '?',      '?',       '?'      ],
  ], dump_vcd, test_verilog )

def test_alu_or( dump_vcd, test_verilog ):
  run_test_vector_sim( AluRTL(), [
    ('in0           in1           fn  out*          ops_eq*   ops_lt*  ops_ltu*'),
    [ 0x00000000,   0x00000000,   3,  0x00000000,   '?',      '?',       '?'      ],
    [ 0x0ffaa660,   0x00012304,   3,  0x0FFBA764,   '?',      '?',       '?'      ],
    #pos-neg
    [ 0x00132050,   0xd6620040,   3,  0xD6732050,   '?',      '?',       '?'      ],
    [ 0xfff0a440,   0x00004450,   3,  0xFFF0E450,   '?',      '?',       '?'      ],
    # neg-neg
    [ 0xfeeeeaa3,   0xf4650000,   3,  0xFEEFEAA3,   '?',      '?',       '?'      ],
    [ 0xffffffff,   0xffffffff,   3,  0xffffffff,   '?',      '?',       '?'      ],
    [ 0x00000000,   0xffffffff,   3,  0xffffffff,   '?',      '?',       '?'      ],
    [ 0xffffffff,   0x00000000,   3,  0xffffffff,   '?',      '?',       '?'      ],
  ], dump_vcd, test_verilog )

def test_alu_xor( dump_vcd, test_verilog ):
  run_test_vector_sim( AluRTL(), [
    ('in0           in1           fn  out*          ops_eq*   ops_lt*  ops_ltu*'),
    [ 0xff00ff00,   0x0f0f0f0f,   4,  0xf00ff00f,   '?',      '?',       '?'      ],
    [ 0x0ff00ff0,   0xf0f0f0f0,   4,  0xff00ff00,   '?',      '?',       '?'      ],
    [ 0x00ff00ff,   0x0f0f0f0f,   4,  0x0ff00ff0,   '?',      '?',       '?'      ],
    [ 0xf00ff00f,   0xf0f0f0f0,   4,  0x00ff00ff,   '?',      '?',       '?'      ],
    [ 0xfeeeeaa3,   0xf4650000,   4,  0x0A8BEAA3,   '?',      '?',       '?'      ],
    [ 0xffffffff,   0xffffffff,   4,  0x00000000,   '?',      '?',       '?'      ],
    [ 0x00000000,   0xffffffff,   4,  0xffffffff,   '?',      '?',       '?'      ],
    [ 0xffffffff,   0x00000000,   4,  0xffffffff,   '?',      '?',       '?'      ],
  ], dump_vcd, test_verilog )
  
def test_alu_sll( dump_vcd, test_verilog ):
  run_test_vector_sim( AluRTL(), [
    ('in0           in1           fn  out*          ops_eq*   ops_lt*  ops_ltu*'),
    [ 0xff00ff00,   0x0000000f,   5,  0x7f800000,   '?',      '?',       '?'      ],
    [ 0x0ff00ff0,   0x0000000f,   5,  0x07f80000,   '?',      '?',       '?'      ],
    [ 0x00ff00ff,   0x0000000a,   5,  0xfc03fc00,   '?',      '?',       '?'      ],
    [ 0xffffffff,   0x0000001f,   5,  0x80000000,   '?',      '?',       '?'      ],
    [ 0x0000ffff,   0x00000008,   5,  0x00ffff00,   '?',      '?',       '?'      ],
    [ 0xffffffff,   0xffffffff,   5,  0x80000000,   '?',      '?',       '?'      ],
    [ 0xffffffff,   0x00000020,   5,  0xffffffff,   '?',      '?',       '?'      ],
    [ 0x0000f000,   0x00000008,   5,  0x00f00000,   '?',      '?',       '?'      ],
  ], dump_vcd, test_verilog )

def test_alu_srl( dump_vcd, test_verilog ):
  run_test_vector_sim( AluRTL(), [
    ('in0           in1           fn  out*          ops_eq*   ops_lt*  ops_ltu*'),
    [ 0xff00ff00,   0x0000000f,   6,  0x0001fe01,   '?',      '?',       '?'      ],
    [ 0x0ff00ff0,   0x0000000f,   6,  0x00001fe0,   '?',      '?',       '?'      ],
    [ 0x00ff00ff,   0x0000000a,   6,  0x00003fc0,   '?',      '?',       '?'      ],
    [ 0xffffffff,   0x0000001f,   6,  0x00000001,   '?',      '?',       '?'      ],
    [ 0x0000ffff,   0x00000008,   6,  0x000000ff,   '?',      '?',       '?'      ],
    [ 0xffffffff,   0xffffffff,   6,  0x00000001,   '?',      '?',       '?'      ],
    [ 0xffffffff,   0x00000020,   6,  0xffffffff,   '?',      '?',       '?'      ],
    [ 0x0000f000,   0x00000008,   6,  0x000000f0,   '?',      '?',       '?'      ],
  ], dump_vcd, test_verilog )

def test_alu_sra( dump_vcd, test_verilog ):
  run_test_vector_sim( AluRTL(), [
    ('in0           in1           fn  out*          ops_eq*   ops_lt*  ops_ltu*'),
    [ 0xff00ff00,   0x0000000f,   7,  0xfffffe01,   '?',      '?',       '?'      ],
    [ 0x0ff00ff0,   0x0000000f,   7,  0x00001fe0,   '?',      '?',       '?'      ],
    [ 0x00ff00ff,   0x0000000a,   7,  0x00003fc0,   '?',      '?',       '?'      ],
    [ 0xffffffff,   0x0000001f,   7,  0xffffffff,   '?',      '?',       '?'      ],
    [ 0x0000ffff,   0x00000008,   7,  0x000000ff,   '?',      '?',       '?'      ],
    [ 0xffffffff,   0xffffffff,   7,  0xffffffff,   '?',      '?',       '?'      ],
    [ 0xffffffff,   0x00000020,   7,  0xffffffff,   '?',      '?',       '?'      ],
    [ 0x0000f000,   0x00000008,   7,  0x000000f0,   '?',      '?',       '?'      ],
  ], dump_vcd, test_verilog )

def test_alu_slt( dump_vcd, test_verilog ):
  run_test_vector_sim( AluRTL(), [
    ('in0           in1           fn  out*          ops_eq*   ops_lt*  ops_ltu*'),
    [ 0x0000000f,   0x0000000f,   8,  0x00000000,   '?',      '?',       '?'      ],
    [ 0x000000f0,   0x0000000f,   8,  0x00000000,   '?',      '?',       '?'      ],
    [ 0x00000f00,   0x0000000f,   8,  0x00000000,   '?',      '?',       '?'      ],
    [ 0x0000f000,   0x0000000f,   8,  0x00000000,   '?',      '?',       '?'      ],
    [ 0xf0000000,   0x0000000f,   8,  0x00000001,   '?',      '?',       '?'      ],
    [ 0x00f00000,   0x0000000f,   8,  0x00000000,   '?',      '?',       '?'      ],
    [ 0xFFFFFFEC,   0x00000013,   8,  0x00000001,   '?',      '?',       '?'      ],
    [ 0x00000014,   0xFFFFFFED,   8,  0x00000000,   '?',      '?',       '?'      ],
    [ 0x00000014,   0x00000013,   8,  0x00000000,   '?',      '?',       '?'      ],
    [ 0x00000013,   0x00000014,   8,  0x00000001,   '?',      '?',       '?'      ],
  ], dump_vcd, test_verilog )

def test_alu_sltu( dump_vcd, test_verilog ):
  run_test_vector_sim( AluRTL(), [
    ('in0           in1           fn  out*          ops_eq*   ops_lt*  ops_ltu*'),
    [ 0x0000000f,   0x0000000f,   9,  0x00000000,   '?',      '?',       '?'      ],
    [ 0x000000f0,   0x0000000f,   9,  0x00000000,   '?',      '?',       '?'      ],
    [ 0x00000f00,   0x0000000f,   9,  0x00000000,   '?',      '?',       '?'      ],
    [ 0x0000f000,   0x0000000f,   9,  0x00000000,   '?',      '?',       '?'      ],
    [ 0xf0000000,   0x0000000f,   9,  0x00000000,   '?',      '?',       '?'      ],
    [ 0x00f00000,   0x0000000f,   9,  0x00000000,   '?',      '?',       '?'      ],
    [ 0xFFFFFFEC,   0x00000013,   9,  0x00000000,   '?',      '?',       '?'      ],
    [ 0x00000014,   0xFFFFFFED,   9,  0x00000001,   '?',      '?',       '?'      ],
    [ 0x00000014,   0x00000013,   9,  0x00000000,   '?',      '?',       '?'      ],
    [ 0x00000013,   0x00000014,   9,  0x00000001,   '?',      '?',       '?'      ],
  ], dump_vcd, test_verilog )

#''' LAB TASK ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# Add more ALU function tests
#'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def test_alu_cp_op0( dump_vcd, test_verilog ):
  run_test_vector_sim( AluRTL(), [
    ('in0           in1           fn  out*          ops_eq*   ops_lt*  ops_ltu*'),
    [ 0x00000000,   0x00000000,  11,  0x00000000,   '?',      '?',       '?'      ],
    [ 0x0ffaa660,   0x00012304,  11,  0x0ffaa660,   '?',      '?',       '?'      ],
    [ 0x00132050,   0xd6620040,  11,  0x00132050,   '?',      '?',       '?'      ],
    [ 0xfff0a440,   0x00004450,  11,  0xfff0a440,   '?',      '?',       '?'      ],
    [ 0xfeeeeaa3,   0xf4650000,  11,  0xfeeeeaa3,   '?',      '?',       '?'      ],
  ], dump_vcd, test_verilog )

def test_alu_cp_op1( dump_vcd, test_verilog ):
  run_test_vector_sim( AluRTL(), [
    ('in0           in1           fn  out*          ops_eq*   ops_lt*  ops_ltu*'),
    [ 0x00000000,   0x00000000,  12,  0x00000000,   '?',      '?',       '?'      ],
    [ 0x0ffaa660,   0x00012304,  12,  0x00012304,   '?',      '?',       '?'      ],
    [ 0x00132050,   0xd6620040,  12,  0xd6620040,   '?',      '?',       '?'      ],
    [ 0xfff0a440,   0x00004450,  12,  0x00004450,   '?',      '?',       '?'      ],
    [ 0xfeeeeaa3,   0xf4650000,  12,  0xf4650000,   '?',      '?',       '?'      ],
  ], dump_vcd, test_verilog )

def test_alu_fn_equality( dump_vcd, test_verilog ):
  run_test_vector_sim( AluRTL(), [
    ('in0           in1           fn  out*          ops_eq*   ops_lt*  ops_ltu*'),
    [ 0x00000000,   0x00000000,  14,  0x00000000,   1,        '?',       '?'      ],
    [ 0x0ffaa660,   0x00012304,  14,  0x00000000,   0,        '?',       '?'      ],
    [ 0x00132050,   0xd6620040,  14,  0x00000000,   0,        '?',       '?'      ],
    [ 0xfff0a440,   0x00004450,  14,  0x00000000,   0,        '?',       '?'      ],
    [ 0xfeeeeaa3,   0xf4650000,  14,  0x00000000,   0,        '?',       '?'      ],
  ], dump_vcd, test_verilog )



