# DARTS_Messages.py
# The bluetooth message classes for the DARTS Application.

import ctypes

field = ctypes.c_uint16

########################################################################
#
# CORALS 1R
#
########################################################################

class CORALS_1R_W1_Data(ctypes.LittleEndianStructure):
    _fields_ = [
        ("command_active", field, 1),
        ("reserved1", field, 1),
        ("commanded_q0_negative", field, 1),
        ("commanded_q1_negative", field, 1),
        ("commanded_q2_negative", field, 1),
        ("commanded_q3_negative", field, 1),
        ("target", field, 2),
        ("action", field, 2),
        ("reserved2", field, 1),
        ("index", field, 5),
    ]

class CORALS_1R_W1(ctypes.LittleEndianUnion):
    _fields_ = [
        ("data", CORALS_1R_W1_Data),
        ("raw", field),
    ]

class CORALS_1R_W2_Data(ctypes.LittleEndianStructure):
    _fields_ = [
        ("commanded_q0_10ths", field, 4),
        ("commanded_q0_100ths", field, 4),
        ("commanded_q0_1000ths", field, 4),
        ("commanded_q0_10000ths", field, 4),
    ]

class CORALS_1R_W2(ctypes.LittleEndianUnion):
    _fields_ = [
        ("data", CORALS_1R_W2_Data),
        ("raw", field),
    ]

class CORALS_1R_W3_Data(ctypes.LittleEndianStructure):
    _fields_ = [
        ("commanded_q1_10ths", field, 4),
        ("commanded_q1_100ths", field, 4),
        ("commanded_q1_1000ths", field, 4),
        ("commanded_q1_10000ths", field, 4),
    ]

class CORALS_1R_W3(ctypes.LittleEndianUnion):
    _fields_ = [
        ("data", CORALS_1R_W3_Data),
        ("raw", field),
    ]

class CORALS_1R_W4_Data(ctypes.LittleEndianStructure):
    _fields_ = [
        ("commanded_q2_10ths", field, 4),
        ("commanded_q2_100ths", field, 4),
        ("commanded_q2_1000ths", field, 4),
        ("commanded_q2_10000ths", field, 4),
    ]

class CORALS_1R_W4(ctypes.LittleEndianUnion):
    _fields_ = [
        ("data", CORALS_1R_W4_Data),
        ("raw", field),
    ]

class CORALS_1R_W5_Data(ctypes.LittleEndianStructure):
    _fields_ = [
        ("commanded_q3_10ths", field, 4),
        ("commanded_q3_100ths", field, 4),
        ("commanded_q3_1000ths", field, 4),
        ("commanded_q3_10000ths", field, 4),
    ]

class CORALS_1R_W5(ctypes.LittleEndianUnion):
    _fields_ = [
        ("data", CORALS_1R_W5_Data),
        ("raw", field),
    ]

class CORALS_1R_Data(ctypes.LittleEndianStructure):
    _fields_ = [
        ("W1", CORALS_1R_W1),
        ("W2", CORALS_1R_W2),
        ("W3", CORALS_1R_W3),
        ("W4", CORALS_1R_W4),
        ("W5", CORALS_1R_W5)
    ]

class CORALS_1R(ctypes.LittleEndianUnion):
    _fields_ = [
        ("data", CORALS_1R_Data),
        ("raw", field * 5)
    ]

########################################################################
#
# CORALS 1T
#
########################################################################

class CORALS_1T_W1_Data(ctypes.LittleEndianStructure):
    _fields_ = [
        ("command_complete", field, 1),
        ("reserved1", field, 1),
        ("reported_q0_negative", field, 1),
        ("reported_q1_negative", field, 1),
        ("reported_q2_negative", field, 1),
        ("reported_q3_negative", field, 1),
        ("reserved2", field, 10),
    ]

class CORALS_1T_W1(ctypes.LittleEndianUnion):
    _fields_ = [
        ("data", CORALS_1T_W1_Data),
        ("raw", field),
    ]

class CORALS_1T_W2_Data(ctypes.LittleEndianStructure):
    _fields_ = [
        ("reported_q0_10ths", field, 4),
        ("reported_q0_100ths", field, 4),
        ("reported_q0_1000ths", field, 4),
        ("reported_q0_10000ths", field, 4),
    ]

class CORALS_1T_W2(ctypes.LittleEndianUnion):
    _fields_ = [
        ("data", CORALS_1T_W2_Data),
        ("raw", field),
    ]

class CORALS_1T_W3_Data(ctypes.LittleEndianStructure):
    _fields_ = [
        ("reported_q1_10ths", field, 4),
        ("reported_q1_100ths", field, 4),
        ("reported_q1_1000ths", field, 4),
        ("reported_q1_10000ths", field, 4),
    ]

class CORALS_1T_W3(ctypes.LittleEndianUnion):
    _fields_ = [
        ("data", CORALS_1T_W3_Data),
        ("raw", field),
    ]

class CORALS_1T_W4_Data(ctypes.LittleEndianStructure):
    _fields_ = [
        ("reported_q2_10ths", field, 4),
        ("reported_q2_100ths", field, 4),
        ("reported_q2_1000ths", field, 4),
        ("reported_q2_10000ths", field, 4),
    ]

class CORALS_1T_W4(ctypes.LittleEndianUnion):
    _fields_ = [
        ("data", CORALS_1T_W4_Data),
        ("raw", field),
    ]

class CORALS_1T_W5_Data(ctypes.LittleEndianStructure):
    _fields_ = [
        ("reported_q3_10ths", field, 4),
        ("reported_q3_100ths", field, 4),
        ("reported_q3_1000ths", field, 4),
        ("reported_q3_10000ths", field, 4),
    ]

class CORALS_1T_W5(ctypes.LittleEndianUnion):
    _fields_ = [
        ("data", CORALS_1T_W5_Data),
        ("raw", field),
    ]

class CORALS_1T_Data(ctypes.LittleEndianStructure):
    _fields_ = [
        ("W1", CORALS_1T_W1),
        ("W2", CORALS_1T_W2),
        ("W3", CORALS_1T_W3),
        ("W4", CORALS_1T_W4),
        ("W5", CORALS_1T_W5)
    ]

class CORALS_1T(ctypes.LittleEndianUnion):
    _fields_ = [
        ("data", CORALS_1T_Data),
        ("raw", field * 5)
    ]

########################################################################
#
# CORALS 2R
#
########################################################################

class CORALS_2R(ctypes.LittleEndianUnion):
    _fields_ = []

########################################################################
#
# CORALS 2T
#
########################################################################

class CORALS_2T_W1_Data(ctypes.LittleEndianStructure):
    _fields_ = [
        ("reserved1", field, 4),
        ("attitude_q0_negative", field, 1),
        ("attitude_q1_negative", field, 1),
        ("attitude_q2_negative", field, 1),
        ("attitude_q3_negative", field, 1),
        ("reserved2", field, 8),
    ]

class CORALS_2T_W1(ctypes.LittleEndianUnion):
    _fields_ = [
        ("data", CORALS_2T_W1_Data),
        ("raw", field),
    ]

class CORALS_2T_W2_Data(ctypes.LittleEndianStructure):
    _fields_ = [
        ("attitude_q0_10ths", field, 4),
        ("attitude_q0_100ths", field, 4),
        ("attitude_q0_1000ths", field, 4),
        ("attitude_q0_10000ths", field, 4),
    ]

class CORALS_2T_W2(ctypes.LittleEndianUnion):
    _fields_ = [
        ("data", CORALS_2T_W2_Data),
        ("raw", field),
    ]

class CORALS_2T_W3_Data(ctypes.LittleEndianStructure):
    _fields_ = [
        ("attitude_q1_10ths", field, 4),
        ("attitude_q1_100ths", field, 4),
        ("attitude_q1_1000ths", field, 4),
        ("attitude_q1_10000ths", field, 4),
    ]

class CORALS_2T_W3(ctypes.LittleEndianUnion):
    _fields_ = [
        ("data", CORALS_2T_W3_Data),
        ("raw", field),
    ]

class CORALS_2T_W4_Data(ctypes.LittleEndianStructure):
    _fields_ = [
        ("attitude_q2_10ths", field, 4),
        ("attitude_q2_100ths", field, 4),
        ("attitude_q2_1000ths", field, 4),
        ("attitude_q2_10000ths", field, 4),
    ]

class CORALS_2T_W4(ctypes.LittleEndianUnion):
    _fields_ = [
        ("data", CORALS_2T_W4_Data),
        ("raw", field),
    ]

class CORALS_2T_W5_Data(ctypes.LittleEndianStructure):
    _fields_ = [
        ("attitude_q3_10ths", field, 4),
        ("attitude_q3_100ths", field, 4),
        ("attitude_q3_1000ths", field, 4),
        ("attitude_q3_10000ths", field, 4),
    ]

class CORALS_2T_W5(ctypes.LittleEndianUnion):
    _fields_ = [
        ("data", CORALS_2T_W5_Data),
        ("raw", field),
    ]

class CORALS_2T_Data(ctypes.LittleEndianStructure):
    _fields_ = [
        ("W1", CORALS_2T_W1),
        ("W2", CORALS_2T_W2),
        ("W3", CORALS_2T_W3),
        ("W4", CORALS_2T_W4),
        ("W5", CORALS_2T_W5)
    ]

class CORALS_2T(ctypes.LittleEndianUnion):
    _fields_ = [
        ("data", CORALS_2T_Data),
        ("raw", field * 5)
    ]

########################################################################
#
# CORALS 3R
#
########################################################################

class CORALS_3R(ctypes.LittleEndianUnion):
    _fields_ = []

########################################################################
#
# CORALS 3T
#
########################################################################

class CORALS_3T(ctypes.LittleEndianUnion):
    _fields_ = []

########################################################################
#
# CORALS 4R
#
########################################################################

class CORALS_4R_W1_Data(ctypes.LittleEndianStructure):
    _fields_ = [
        ("command_active", field, 1),
        ("reserved1", field, 6),
        ("commanded_gain11_negative", field, 1),
        ("commanded_gain12_negative", field, 1),
        ("commanded_gain13_negative", field, 1),
        ("commanded_gain21_negative", field, 1),
        ("commanded_gain22_negative", field, 1),
        ("commanded_gain23_negative", field, 1),
        ("commanded_gain31_negative", field, 1),
        ("commanded_gain32_negative", field, 1),
        ("commanded_gain33_negative", field, 1),
    ]

class CORALS_4R_W1(ctypes.LittleEndianUnion):
    _fields_ = [
        ("data", CORALS_4R_W1_Data),
        ("raw", field),
    ]

class CORALS_4R_W2_Data(ctypes.LittleEndianStructure):
    _fields_ = [
        ("commanded_gain11_10ths", field, 4),
        ("commanded_gain11_100ths", field, 4),
        ("commanded_gain11_exp_negative", field, 1),
        ("commanded_gain11_exp", field, 7),
    ]

class CORALS_4R_W2(ctypes.LittleEndianUnion):
    _fields_ = [
        ("data", CORALS_4R_W2_Data),
        ("raw", field),
    ]

class CORALS_4R_W3_Data(ctypes.LittleEndianStructure):
    _fields_ = [
        ("commanded_gain12_10ths", field, 4),
        ("commanded_gain12_100ths", field, 4),
        ("commanded_gain12_exp_negative", field, 1),
        ("commanded_gain12_exp", field, 7),
    ]

class CORALS_4R_W3(ctypes.LittleEndianUnion):
    _fields_ = [
        ("data", CORALS_4R_W3_Data),
        ("raw", field),
    ]

class CORALS_4R_W4_Data(ctypes.LittleEndianStructure):
    _fields_ = [
        ("commanded_gain13_10ths", field, 4),
        ("commanded_gain13_100ths", field, 4),
        ("commanded_gain13_exp_negative", field, 1),
        ("commanded_gain13_exp", field, 7),
    ]

class CORALS_4R_W4(ctypes.LittleEndianUnion):
    _fields_ = [
        ("data", CORALS_4R_W4_Data),
        ("raw", field),
    ]

class CORALS_4R_W5_Data(ctypes.LittleEndianStructure):
    _fields_ = [
        ("commanded_gain21_10ths", field, 4),
        ("commanded_gain21_100ths", field, 4),
        ("commanded_gain21_exp_negative", field, 1),
        ("commanded_gain21_exp", field, 7),
    ]

class CORALS_4R_W5(ctypes.LittleEndianUnion):
    _fields_ = [
        ("data", CORALS_4R_W5_Data),
        ("raw", field),
    ]

class CORALS_4R_W6_Data(ctypes.LittleEndianStructure):
    _fields_ = [
        ("commanded_gain22_10ths", field, 4),
        ("commanded_gain22_100ths", field, 4),
        ("commanded_gain22_exp_negative", field, 1),
        ("commanded_gain22_exp", field, 7),
    ]

class CORALS_4R_W6(ctypes.LittleEndianUnion):
    _fields_ = [
        ("data", CORALS_4R_W6_Data),
        ("raw", field),
    ]

class CORALS_4R_W7_Data(ctypes.LittleEndianStructure):
    _fields_ = [
        ("commanded_gain23_10ths", field, 4),
        ("commanded_gain23_100ths", field, 4),
        ("commanded_gain23_exp_negative", field, 1),
        ("commanded_gain23_exp", field, 7),
    ]

class CORALS_4R_W7(ctypes.LittleEndianUnion):
    _fields_ = [
        ("data", CORALS_4R_W7_Data),
        ("raw", field),
    ]

class CORALS_4R_W8_Data(ctypes.LittleEndianStructure):
    _fields_ = [
        ("commanded_gain31_10ths", field, 4),
        ("commanded_gain31_100ths", field, 4),
        ("commanded_gain31_exp_negative", field, 1),
        ("commanded_gain31_exp", field, 7),
    ]

class CORALS_4R_W8(ctypes.LittleEndianUnion):
    _fields_ = [
        ("data", CORALS_4R_W8_Data),
        ("raw", field),
    ]

class CORALS_4R_W9_Data(ctypes.LittleEndianStructure):
    _fields_ = [
        ("commanded_gain32_10ths", field, 4),
        ("commanded_gain32_100ths", field, 4),
        ("commanded_gain32_exp_negative", field, 1),
        ("commanded_gain32_exp", field, 7),
    ]

class CORALS_4R_W9(ctypes.LittleEndianUnion):
    _fields_ = [
        ("data", CORALS_4R_W9_Data),
        ("raw", field),
    ]

class CORALS_4R_W10_Data(ctypes.LittleEndianStructure):
    _fields_ = [
        ("commanded_gain33_10ths", field, 4),
        ("commanded_gain33_100ths", field, 4),
        ("commanded_gain33_exp_negative", field, 1),
        ("commanded_gain33_exp", field, 7),
    ]

class CORALS_4R_W10(ctypes.LittleEndianUnion):
    _fields_ = [
        ("data", CORALS_4R_W10_Data),
        ("raw", field),
    ]

class CORALS_4R_Data(ctypes.LittleEndianUnion):
    _fields_ = [
        ("W1", CORALS_4R_W1),
        ("W2", CORALS_4R_W2),
        ("W3", CORALS_4R_W3),
        ("W4", CORALS_4R_W4),
        ("W5", CORALS_4R_W5),
        ("W6", CORALS_4R_W6),
        ("W7", CORALS_4R_W7),
        ("W8", CORALS_4R_W8),
        ("W9", CORALS_4R_W9),
        ("W10", CORALS_4R_W10)
    ]

class CORALS_4R(ctypes.LittleEndianUnion):
    _fields_ = [
        ("data", CORALS_4R_Data),
        ("raw", field * 10)
    ]

########################################################################
#
# CORALS 4T
#
########################################################################

class CORALS_4T_W1_Data(ctypes.LittleEndianStructure):
    _fields_ = [
        ("command_complete", field, 1),
        ("reserved1", field, 6),
        ("reported_gain11_negative", field, 1),
        ("reported_gain12_negative", field, 1),
        ("reported_gain13_negative", field, 1),
        ("reported_gain21_negative", field, 1),
        ("reported_gain22_negative", field, 1),
        ("reported_gain23_negative", field, 1),
        ("reported_gain31_negative", field, 1),
        ("reported_gain32_negative", field, 1),
        ("reported_gain33_negative", field, 1),
    ]

class CORALS_4T_W1(ctypes.LittleEndianUnion):
    _fields_ = [
        ("data", CORALS_4T_W1_Data),
        ("raw", field),
    ]

class CORALS_4T_W2_Data(ctypes.LittleEndianStructure):
    _fields_ = [
        ("reported_gain11_10ths", field, 4),
        ("reported_gain11_100ths", field, 4),
        ("reported_gain11_exp_negative", field, 1),
        ("reported_gain11_exp", field, 7),
    ]

class CORALS_4T_W2(ctypes.LittleEndianUnion):
    _fields_ = [
        ("data", CORALS_4T_W2_Data),
        ("raw", field),
    ]

class CORALS_4T_W3_Data(ctypes.LittleEndianStructure):
    _fields_ = [
        ("reported_gain12_10ths", field, 4),
        ("reported_gain12_100ths", field, 4),
        ("reported_gain12_exp_negative", field, 1),
        ("reported_gain12_exp", field, 7),
    ]

class CORALS_4T_W3(ctypes.LittleEndianUnion):
    _fields_ = [
        ("data", CORALS_4T_W3_Data),
        ("raw", field),
    ]

class CORALS_4T_W4_Data(ctypes.LittleEndianStructure):
    _fields_ = [
        ("reported_gain13_10ths", field, 4),
        ("reported_gain13_100ths", field, 4),
        ("reported_gain13_exp_negative", field, 1),
        ("reported_gain13_exp", field, 7),
    ]

class CORALS_4T_W4(ctypes.LittleEndianUnion):
    _fields_ = [
        ("data", CORALS_4T_W4_Data),
        ("raw", field),
    ]

class CORALS_4T_W5_Data(ctypes.LittleEndianStructure):
    _fields_ = [
        ("reported_gain21_10ths", field, 4),
        ("reported_gain21_100ths", field, 4),
        ("reported_gain21_exp_negative", field, 1),
        ("reported_gain21_exp", field, 7),
    ]

class CORALS_4T_W5(ctypes.LittleEndianUnion):
    _fields_ = [
        ("data", CORALS_4T_W5_Data),
        ("raw", field),
    ]

class CORALS_4T_W6_Data(ctypes.LittleEndianStructure):
    _fields_ = [
        ("reported_gain22_10ths", field, 4),
        ("reported_gain22_100ths", field, 4),
        ("reported_gain22_exp_negative", field, 1),
        ("reported_gain22_exp", field, 7),
    ]

class CORALS_4T_W6(ctypes.LittleEndianUnion):
    _fields_ = [
        ("data", CORALS_4T_W6_Data),
        ("raw", field),
    ]

class CORALS_4T_W7_Data(ctypes.LittleEndianStructure):
    _fields_ = [
        ("reported_gain23_10ths", field, 4),
        ("reported_gain23_100ths", field, 4),
        ("reported_gain23_exp_negative", field, 1),
        ("reported_gain23_exp", field, 7),
    ]

class CORALS_4T_W7(ctypes.LittleEndianUnion):
    _fields_ = [
        ("data", CORALS_4T_W7_Data),
        ("raw", field),
    ]

class CORALS_4T_W8_Data(ctypes.LittleEndianStructure):
    _fields_ = [
        ("reported_gain31_10ths", field, 4),
        ("reported_gain31_100ths", field, 4),
        ("reported_gain31_exp_negative", field, 1),
        ("reported_gain31_exp", field, 7),
    ]

class CORALS_4T_W8(ctypes.LittleEndianUnion):
    _fields_ = [
        ("data", CORALS_4T_W8_Data),
        ("raw", field),
    ]

class CORALS_4T_W9_Data(ctypes.LittleEndianStructure):
    _fields_ = [
        ("reported_gain32_10ths", field, 4),
        ("reported_gain32_100ths", field, 4),
        ("reported_gain32_exp_negative", field, 1),
        ("reported_gain32_exp", field, 7),
    ]

class CORALS_4T_W9(ctypes.LittleEndianUnion):
    _fields_ = [
        ("data", CORALS_4T_W9_Data),
        ("raw", field),
    ]

class CORALS_4T_W10_Data(ctypes.LittleEndianStructure):
    _fields_ = [
        ("reported_gain33_10ths", field, 4),
        ("reported_gain33_100ths", field, 4),
        ("reported_gain33_exp_negative", field, 1),
        ("reported_gain33_exp", field, 7),
    ]

class CORALS_4T_W10(ctypes.LittleEndianUnion):
    _fields_ = [
        ("data", CORALS_4T_W10_Data),
        ("raw", field),
    ]

class CORALS_4T_Data(ctypes.LittleEndianStructure):
    _fields_ = [
        ("W1", CORALS_4T_W1),
        ("W2", CORALS_4T_W2),
        ("W3", CORALS_4T_W3),
        ("W4", CORALS_4T_W4),
        ("W5", CORALS_4T_W5),
        ("W6", CORALS_4T_W6),
        ("W7", CORALS_4T_W7),
        ("W8", CORALS_4T_W8),
        ("W9", CORALS_4T_W9),
        ("W10", CORALS_4T_W10)
    ]

class CORALS_4T(ctypes.LittleEndianUnion):
    _fields_ = [
        ("data", CORALS_4T_Data),
        ("raw", field * 10)
    ]

########################################################################
#
# CORALS 5R
#
########################################################################

class CORALS_5R(ctypes.LittleEndianUnion):
    _fields_ = []

########################################################################
#
# CORALS 5T
#
########################################################################

class CORALS_5R(ctypes.LittleEndianUnion):
    _fields_ = []