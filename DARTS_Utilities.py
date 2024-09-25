# DARTS_API.py
# The utility functions for the DARTS Application.

import time

import DARTS_API as api

import numpy as np

########################################################################
#
# DARTS Application Utilities
#
########################################################################

def StartTestbed() -> None:
    api.Settings_Set_Halt(False)

    # Start Attitude Logging
    api.Attitude_Plot_Set_StartTime(time.time())
    api.Attitude_Plot_Set_TimeData([])

def StopTestbed() -> None:
    api.Settings_Set_Halt(True)

########################################################################
#
# DARTS Database State Utilities
#
########################################################################

def AngleType_IsDegrees() -> bool:
    return api.Settings_Get_AngleType() == "Degrees"

def AngleType_IsRadians() -> bool:
    return api.Settings_Get_AngleType() == "Radians"

def AttitudePlot_IsRPYAngles() -> bool:
    return api.Attitude_Plot_Get_DisplayType() == "RPY Angles"

def AttitudePlot_IsEulerParameters() -> bool:
    return api.Attitude_Plot_Get_DisplayType() == "Euler Parameters"

def AttitudePlot_IsGibbsRodriguez() -> bool:
    return api.Attitude_Plot_Get_DisplayType() == "Gibbs-Rodriguez"

def AttitudePlot_IsQuaternion() -> bool:
    return api.Attitude_Plot_Get_DisplayType() == "Quaternion"

########################################################################
#
# DARTS Conversion Utilities
#
########################################################################

def Convert_Quaternion_to_RPY(quaternion_data:list[np.array]) -> list[np.array]:
    # Convert Quaternion to RPY Angles
    [q0_data, q1_data, q2_data, q3_data] = quaternion_data
    roll_data = np.arctan2(2*(q0_data*q1_data + q2_data*q3_data), 1 - 2*(q1_data**2 + q2_data**2))
    pitch_data = np.arcsin(2*(q0_data*q2_data - q3_data*q1_data))
    yaw_data = np.arctan2(2*(q0_data*q3_data + q1_data*q2_data), 1 - 2*(q2_data**2 + q3_data**2))
    return [roll_data, pitch_data, yaw_data]

def Convert_Quaternion_to_Euler(quaternion_data:list[np.array]) -> dict:
    # Convert Quaternion to Euler Parameters
    [q0_data, q1_data, q2_data, q3_data] = quaternion_data
    qmag_data = np.sqrt(q1_data**2 + q2_data**2 + q3_data**2)
    return {"parameter": quaternion_data[1:4] / qmag_data, "angle": 2 * np.arccos(q0_data)}

def Convert_Quaternion_to_Gibbs(quaternion_data:list[np.array]) -> list[np.array]:
    # Convert Quaternion to Gibbs-Rodriguez Parameters
    euler_data = Convert_Quaternion_to_Euler(quaternion_data)
    return np.tan(euler_data["angle"]/2) * euler_data["parameter"]

########################################################################
#
# DARTS Target List Utilities
#
########################################################################

def Get_TargetList_Quaternion_String(index:int) -> str:
    target = api.Targets_Get_List()[index]
    if api.Settings_Get_QuaternionType() == 'Q4':
        return "[{:.3f}, {:.3f}, {:.3f}, {:.3f}]".format(target[1], target[2], target[3], target[0])
    return "[{:.3f}, {:.3f}, {:.3f}, {:.3f}]".format(target[0], target[1], target[2], target[3])