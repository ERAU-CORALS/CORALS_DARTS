# DARTS_API.py
# The API functions for the DARTS Application.

import __main__
import time

import numpy as np
from scipy.spatial.transform import Rotation as rot

import DARTS_Utilities as util

def _API_Print(value:str) -> None:
    if __main__.DEBUG_API:
        print(f"API: {value}")

########################################################################
#
# DARTS Attitude Settings
#
########################################################################

def Attitude_Get_Current_Type(type:str="RPY Angles") -> list[float]|dict[str, float]:
    _API_Print(f"Getting Attitude Current {type}")
    return __main__.DARTS_Database["Attitude"]["Current"][type]

def Attitude_Set_Current_Type(value:list[float]|dict[str, float], type:str="RPY Angles") -> None:
    _API_Print(f"Setting Attitude Current {type} to {value}")

    if type == "RPY Angles":

        __main__.DARTS_Database["Attitude"]["Current"]["RPY Angles"] = value
        __main__.DARTS_Database["Attitude"]["Current"]["Euler Parameters"] = util.Convert_RPY_to_Euler(value)
        __main__.DARTS_Database["Attitude"]["Current"]["Gibbs-Rodriguez"] = util.Convert_RPY_to_Gibbs(value)
        __main__.DARTS_Database["Attitude"]["Current"]["Quaternion"] = util.Convert_RPY_to_Quaternion(value)

    elif type == "Euler Parameters":

        __main__.DARTS_Database["Attitude"]["Current"]["RPY Angles"] = util.Convert_Euler_to_RPY(value)
        __main__.DARTS_Database["Attitude"]["Current"]["Euler Parameters"] = value
        __main__.DARTS_Database["Attitude"]["Current"]["Gibbs-Rodriguez"] = util.Convert_Euler_to_Gibbs(value)
        __main__.DARTS_Database["Attitude"]["Current"]["Quaternion"] = util.Convert_Euler_to_Quaternion(value)

    elif type == "Gibbs-Rodriguez":

        __main__.DARTS_Database["Attitude"]["Current"]["RPY Angles"] = util.Convert_Gibbs_to_RPY(value)
        __main__.DARTS_Database["Attitude"]["Current"]["Euler Parameters"] = util.Convert_Gibbs_to_Euler(value)
        __main__.DARTS_Database["Attitude"]["Current"]["Gibbs-Rodriguez"] = value
        __main__.DARTS_Database["Attitude"]["Current"]["Quaternion"] = util.Convert_Gibbs_to_Quaternion(value)

    elif type == "Quaternion":

        __main__.DARTS_Database["Attitude"]["Current"]["RPY Angles"] = util.Convert_Quaternion_to_RPY(value)
        __main__.DARTS_Database["Attitude"]["Current"]["Euler Parameters"] = util.Convert_Quaternion_to_Euler(value)
        __main__.DARTS_Database["Attitude"]["Current"]["Gibbs-Rodriguez"] = util.Convert_Quaternion_to_Gibbs(value)
        __main__.DARTS_Database["Attitude"]["Current"]["Quaternion"] = value

def Attitude_Plot_Get_StartTime() -> float:
    _API_Print("Getting Attitude Plot Start Time")
    return __main__.DARTS_Database["Attitude"]["Plot_StartTime"]

def Attitude_Plot_Set_StartTime(value:float) -> None:
    _API_Print(f"Setting Attitude Plot StartTime to {value}")
    __main__.DARTS_Database["Attitude"]["Plot_StartTime"] = value

def Attitude_Plot_Get_TimeLength() -> float:
    _API_Print("Getting Attitude Plot Time Length")
    return __main__.DARTS_Database["Attitude"]["Plot_TimeLength"]

def Attitude_Plot_Set_TimeLength(value:float) -> None:
    _API_Print(f"Setting Attitude Plot Time Length to {value}")
    __main__.DARTS_Database["Attitude"]["Plot_TimeLength"] = value

def Attitude_Plot_Get_TimeData() -> list[float]:
    _API_Print("Getting Attitude Plot Time Data")
    return __main__.DARTS_Database["Attitude"]["Plot_TimeData"]

def Attitude_Plot_Push_TimeData(value:list[float]) -> None:
    _API_Print(f"Setting Attitude Plot Time Data to {value}")
    __main__.DARTS_Database["Attitude"]["Plot_TimeData"].append(value)

def Attitude_Plot_Pop_TimeData(index:int=0) -> float:
    _API_Print("Popping Attitude Plot Time Data")
    return __main__.DARTS_Database["Attitude"]["Plot_TimeData"].pop(index)

def Attitude_Plot_Clear_TimeData() -> None:
    _API_Print("Clearing Attitude Plot Time Data")
    __main__.DARTS_Database["Attitude"]["Plot_TimeData"].clear()

def Attitude_Plot_Get_AttitudeData(type:str="RPY Angles") -> list[float]:
    _API_Print(f"Getting Attitude Plot {type} Data")
    return __main__.DARTS_Database["Attitude"]["Plot_AttitudeData"][type]

def Attitude_Plot_Push_AttitudeData(value:list[float], type:str="RPY Angles") -> None:
    _API_Print(f"Setting Attitude Plot {type} Data to {value}")
    
    if type == "RPY Angles":

        angles = value
        euler = util.Convert_RPY_to_Euler(value)
        gibbs = util.Convert_RPY_to_Gibbs(value)
        quat = util.Convert_RPY_to_Quaternion(value)

    elif type == "Euler Parameters":

        angles = util.Convert_Euler_to_RPY(value)
        euler = value
        gibbs = util.Convert_Euler_to_Gibbs(value)
        quat = util.Convert_Euler_to_Quaternion(value)

    elif type == "Gibbs-Rodriguez":

        angles = util.Convert_Gibbs_to_RPY(value)
        euler = util.Convert_Gibbs_to_Euler(value)
        gibbs = value
        quat = util.Convert_Gibbs_to_Quaternion(value)

    elif type == "Quaternion":

        angles = util.Convert_Quaternion_to_RPY(value)
        euler = util.Convert_Quaternion_to_Euler(value)
        gibbs = util.Convert_Quaternion_to_Gibbs(value)
        quat = value

    for i in range(3):

        __main__.DARTS_Database["Attitude"]["Plot_AttitudeData"]["RPY Angles"][i].append(angles[i])
        __main__.DARTS_Database["Attitude"]["Plot_AttitudeData"]["Euler Parameters"]["axis"][i].append(euler["axis"][i])
        __main__.DARTS_Database["Attitude"]["Plot_AttitudeData"]["Gibbs-Rodriguez"][i].append(gibbs[i])
        __main__.DARTS_Database["Attitude"]["Plot_AttitudeData"]["Quaternion"][i].append(quat[i])

    __main__.DARTS_Database["Attitude"]["Plot_AttitudeData"]["Euler Parameters"]["angle"].append(euler["angle"])
    __main__.DARTS_Database["Attitude"]["Plot_AttitudeData"]["Quaternion"][3].append(quat[3])

def Attitude_Plot_Pop_AttitudeData(index:int=0) -> None:
    _API_Print("Popping Attitude Plot Attitude Data")

    for i in range(3):

        __main__.DARTS_Database["Attitude"]["Plot_AttitudeData"]["RPY Angles"][i].pop(index)
        __main__.DARTS_Database["Attitude"]["Plot_AttitudeData"]["Euler Parameters"]["axis"][i].pop(index)
        __main__.DARTS_Database["Attitude"]["Plot_AttitudeData"]["Gibbs-Rodriguez"][i].pop(index)
        __main__.DARTS_Database["Attitude"]["Plot_AttitudeData"]["Quaternion"][i].pop(index)

    __main__.DARTS_Database["Attitude"]["Plot_AttitudeData"]["Euler Parameters"]["angle"].pop(index)
    __main__.DARTS_Database["Attitude"]["Plot_AttitudeData"]["Quaternion"][3].pop(index)

def Attitude_Plot_Clear_AttitudeData() -> None:
    _API_Print("Clearing Attitude Plot Data")

    for i in range(3):
            
        __main__.DARTS_Database["Attitude"]["Plot_AttitudeData"]["RPY Angles"][i].clear()
        __main__.DARTS_Database["Attitude"]["Plot_AttitudeData"]["Euler Parameters"]["axis"][i].clear()
        __main__.DARTS_Database["Attitude"]["Plot_AttitudeData"]["Gibbs-Rodriguez"][i].clear()
        __main__.DARTS_Database["Attitude"]["Plot_AttitudeData"]["Quaternion"][i].clear()

    __main__.DARTS_Database["Attitude"]["Plot_AttitudeData"]["Euler Parameters"]["angle"].clear()
    __main__.DARTS_Database["Attitude"]["Plot_AttitudeData"]["Quaternion"][3].clear()
    
def Attitude_Plot_Get_DisplayType() -> str:
    _API_Print("Getting Attitude Plot Display Type")
    return __main__.DARTS_Database["Attitude"]["Plot_DisplayType"]

def Attitude_Plot_Set_DisplayType(value:str) -> None:
    _API_Print(f"Setting Attitude Plot Display Type to {value}")
    __main__.DARTS_Database["Attitude"]["Plot_DisplayType"] = value

########################################################################
#
# DARTS Targets Settings
#
########################################################################

def Targets_Get_CurrentIndices() -> list[int]:
    _API_Print("Getting Targets Current Display Indices")
    return __main__.DARTS_Database["Target"]["Indices"]

def Targets_Set_CurrentIndices(value:list[int]) -> None:
    _API_Print(f"Setting Targets Current Display Indices to {value}")
    __main__.DARTS_Database["Target"]["Indices"] = value

def Targets_Get_List() -> list[list[float]]:
    _API_Print("Getting Targets List")
    return __main__.DARTS_Database["Target"]["List"]

def Targets_Set_List(value:list[list[float]]) -> None:
    _API_Print(f"Setting Targets List to {value}")
    __main__.DARTS_Database["Target"]["List"] = value

########################################################################
#
# DARTS Application Settings
#
########################################################################

def Settings_Get_Halt() -> bool:
    _API_Print("Getting Halt Setting")
    return __main__.DARTS_Database["Settings"]["Halt"]

def Settings_Set_Halt(value:bool) -> None:
    _API_Print(f"Setting Halt Setting to {value}")
    __main__.DARTS_Database["Settings"]["Halt"] = value

def Settings_Get_AngleType() -> str:
    _API_Print("Getting Angle Type Setting")
    return __main__.DARTS_Database["Settings"]["AngleType"]

def Settings_Set_AngleType(value:str) -> None:
    _API_Print(f"Setting Angle Type Setting to {value}")
    __main__.DARTS_Database["Settings"]["AngleType"] = value

def Settings_Get_QuaternionType() -> str:
    _API_Print("Getting Quaternion Type Setting")
    return __main__.DARTS_Database["Settings"]["QuaternionType"]

def Settings_Set_QuaternionType(value:str) -> None:
    _API_Print(f"Setting Quaternion Type Setting to {value}")
    __main__.DARTS_Database["Settings"]["QuaternionType"] = value