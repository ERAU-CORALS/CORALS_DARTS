# DARTS_API.py
# The utility functions for the DARTS Application.

import time

import DARTS_API as api

import numpy as np
from scipy.spatial.transform import Rotation as rot

########################################################################
#
# DARTS Application Utilities
#
########################################################################

def Debug_Print(file: str, value:str, condition:bool=True) -> None:
    if condition:
        import inspect
        parent_frame = inspect.currentframe().f_back
        print(f"[{file}({inspect.getframeinfo(parent_frame).lineno}): {parent_frame.f_code.co_name}]\t{value}")

def StartTestbed() -> None:
    # Start Attitude Logging
    api.Attitude_Plot_Set_StartTime(time.time())
    api.Attitude_Plot_Clear_TimeData()
    api.Attitude_Plot_Clear_AttitudeData()

    api.Settings_Set_Halt(False)

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

# RPY Angles

def Convert_RPY_to_Euler(rpy_data:list[float]) -> dict:
    # Convert RPY Angles to Euler Parameters
    return Convert_Quaternion_to_Euler(Convert_RPY_to_Quaternion(rpy_data))

def Convert_RPY_to_Gibbs(rpy_data:list[float]) -> list[float]:
    # Convert RPY Angles to Gibbs-Rodriguez Parameters
    return Convert_Quaternion_to_Gibbs(Convert_RPY_to_Quaternion(rpy_data))

def Convert_RPY_to_Quaternion(rpy_data:list[float]) -> list[float]:
    # Convert RPY Angles to Quaternion
    rmatrix = rot.from_euler("xyz", rpy_data)
    return rmatrix.as_quat(scalar_first=False)

# Euler Parameters

def Convert_Euler_to_RPY(euler_data:dict) -> list[float]:
    # Convert Euler Parameters to RPY Angles
    return Convert_Quaternion_to_RPY(Convert_Euler_to_Quaternion(euler_data))

def Convert_Euler_to_Gibbs(euler_data:dict) -> list[float]:
    # Convert Euler Parameters to Gibbs-Rodriguez Parameters
    return np.tan(euler_data["angle"]/2) * euler_data["axis"]

def Convert_Euler_to_Quaternion(euler_data:dict) -> list[float]:
    # Convert Euler Parameters to Quaternion
    return euler_data["axis"] * np.sin(euler_data["angle"]/2) + [np.cos(euler_data["angle"]/2)]

# Gibbs-Rodriguez Parameters

def Convert_Gibbs_to_RPY(gibbs_data:list[float]) -> list[float]:
    # Convert Gibbs-Rodriguez Parameters to RPY Angles
    return Convert_Quaternion_to_RPY(Convert_Gibbs_to_Quaternion(gibbs_data))

def Convert_Gibbs_to_Euler(gibbs_data:list[float]) -> dict:
    # Convert Gibbs-Rodriguez Parameters to Euler Parameters
    return {"axis": gibbs_data / np.linalg.norm(gibbs_data), 
            "angle": 2 * np.arctan(np.linalg.norm(gibbs_data))}

def Convert_Gibbs_to_Quaternion(gibbs_data:list[float]) -> list[float]:
    # Convert Gibbs-Rodriguez Parameters to Quaternion
    return Convert_Euler_to_Quaternion(Convert_Gibbs_to_Euler(gibbs_data))

# Quaternion

def Convert_Quaternion_to_RPY(quaternion_data:list[float]) -> list[float]:
    # Convert Quaternion to RPY Angles
    [q1_data, q2_data, q3_data, q4_data] = quaternion_data
    roll_data = np.arctan2(2*(q4_data*q1_data + q2_data*q3_data), 1 - 2*(q1_data**2 + q2_data**2))
    pitch_data = np.arcsin(2*(q4_data*q2_data - q3_data*q1_data))
    yaw_data = np.arctan2(2*(q4_data*q3_data + q1_data*q2_data), 1 - 2*(q2_data**2 + q3_data**2))
    return [roll_data, pitch_data, yaw_data]

def Convert_Quaternion_to_Euler(quaternion_data:list[float]) -> dict:
    # Convert Quaternion to Euler Parameters
    [q1_data, q2_data, q3_data, q4_data] = quaternion_data
    qhat_mag = np.linalg.norm(quaternion_data[0:3])
    return {"axis": quaternion_data[0:3] / qhat_mag, "angle": 2 * np.arccos(q4_data)}

def Convert_Quaternion_to_Gibbs(quaternion_data:list[float]) -> list[float]:
    # Convert Quaternion to Gibbs-Rodriguez Parameters
    return Convert_Euler_to_Gibbs(Convert_Quaternion_to_Euler(quaternion_data))

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