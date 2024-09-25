# DARTS_API.py
# The API functions for the DARTS Application.

import __main__
import time

import numpy as np

def _API_Print(value:str) -> None:
    if __main__.DEBUG_API:
        print(f"API: {value}")

########################################################################
#
# DARTS Application Settings
#
########################################################################

def Settings_Get_Halt() -> bool:
    _API_Print("Getting Halt Setting")
    return __main__.DARTS_Settings["Settings_Halt"]

def Settings_Set_Halt(value:bool) -> None:
    _API_Print(f"Setting Halt Setting to {value}")
    __main__.DARTS_Settings["Halt"] = value

def Settings_Get_AngleType() -> str:
    _API_Print("Getting Angle Type Setting")
    return __main__.DARTS_Settings["Settings_AngleType"]

def Settings_Set_AngleType(value:str) -> None:
    _API_Print(f"Setting Angle Type Setting to {value}")
    __main__.DARTS_Settings["Settings_AngleType"] = value

def Settings_Get_QuaternionType() -> str:
    _API_Print("Getting Quaternion Type Setting")
    return __main__.DARTS_Settings["Settings_QuaternionType"]

def Settings_Set_QuaternionType(value:str) -> None:
    _API_Print(f"Setting Quaternion Type Setting to {value}")
    __main__.DARTS_Settings["Settings_QuaternionType"] = value


########################################################################
#
# DARTS Attitude Settings
#
########################################################################

def Attitude_Get_Current() -> list[float]:
    _API_Print("Getting Attitude Current")
    return __main__.DARTS_Settings["Attitude_Current"]

def Attitude_Set_Current(value:list[float]) -> None:
    _API_Print(f"Setting Attitude Current to {value}")
    __main__.DARTS_Settings["Attitude_Current"] = value

def Attitude_Plot_Get_StartTime() -> float:
    _API_Print("Getting Attitude Plot Start Time")
    return __main__.DARTS_Settings["Attitude_Plot_StartTime"]

def Attitude_Plot_Set_StartTime(value:float) -> None:
    _API_Print(f"Setting Attitude Plot StartTime to {value}")
    __main__.DARTS_Settings["Attitude_Plot_StartTime"] = value

def Attitude_Plot_Get_TimeLength() -> float:
    _API_Print("Getting Attitude Plot Time Length")
    return __main__.DARTS_Settings["Attitude_Plot_TimeLength"]

def Attitude_Plot_Set_TimeLength(value:float) -> None:  
    _API_Print(f"Setting Attitude Plot Time Length to {value}")
    __main__.DARTS_Settings["Attitude_Plot_TimeLength"] = value

def Attitude_Plot_Get_TimeData() -> list[float]:
    _API_Print("Getting Attitude Plot Time Data")
    return __main__.DARTS_Settings["Attitude_Plot_TimeData"]

def Attitude_Plot_Set_TimeData(value:list[float]) -> None:
    _API_Print(f"Setting Attitude Plot Time Data to {value}")
    __main__.DARTS_Settings["Attitude_Plot_TimeData"] = value

def Attitude_Plot_Get_QuaternionData() -> list[np.array]:
    _API_Print("Getting Attitude Plot Quaternion Data")
    return __main__.DARTS_Settings["Attitude_Plot_QuaternionData"]

def Attitude_Plot_Set_QuaternionData(value:list[np.array]) -> None:
    _API_Print(f"Setting Attitude Plot Quaternion Data to {value}")
    __main__.DARTS_Settings["Attitude_Plot_QuaternionData"] = value

def Attitude_Plot_Get_DisplayType() -> str:
    _API_Print("Getting Attitude Plot Display Type")
    return __main__.DARTS_Settings["Attitude_Plot_DisplayType"]

def Attitude_Plot_Set_DisplayType(value:str) -> None:
    _API_Print(f"Setting Attitude Plot Display Type to {value}")
    __main__.DARTS_Settings["Attitude_Plot_DisplayType"] = value

########################################################################
#
# DARTS Targets Settings
#
########################################################################

def Targets_Get_CurrentDisplayIndex() -> int|list[int]:
    _API_Print("Getting Targets Current Display Index")
    return __main__.DARTS_Settings["Targets_CurrentDisplayIndex"]

def Targets_Set_CurrentDisplayIndex(value:int|list[int]) -> None:
    _API_Print(f"Setting Targets Current Display Index to {value}")
    __main__.DARTS_Settings["Targets_CurrentDisplayIndex"] = value

def Targets_Get_List() -> list[list[float]]:
    _API_Print("Getting Targets List")
    return __main__.DARTS_Settings["Targets_List"]

def Targets_Set_List(value:list[list[float]]) -> None:
    _API_Print(f"Setting Targets List to {value}")
    __main__.DARTS_Settings["Targets_List"] = value