# DARTS_API.py
# The API functions for the DARTS Application.

import __main__
import time

import numpy as np

########################################################################
#
# DARTS Application Settings
#
########################################################################

def Settings_Get_Halt() -> bool:
    return __main__.DARTS_Settings["Settings_Halt"]

def Settings_Set_Halt(value:bool) -> None:
    __main__.DARTS_Settings["Halt"] = value

def Settings_Get_AngleType() -> str:
    return __main__.DARTS_Settings["Settings_AngleType"]

def Settings_Set_AngleType(value:str) -> None:
    __main__.DARTS_Settings["Settings_AngleType"] = value

def Settings_Get_QuaternionType() -> str:
    return __main__.DARTS_Settings["Settings_QuaternionType"]

def Settings_Set_QuaternionType(value:str) -> None:
    __main__.DARTS_Settings["Settings_QuaternionType"] = value


########################################################################
#
# DARTS Attitude Settings
#
########################################################################

def Attitude_Get_Current() -> list[float]:
    return __main__.DARTS_Settings["Attitude_Current"]

def Attitude_Set_Current(value:list[float]) -> None:
    __main__.DARTS_Settings["Attitude_Current"] = value

def Attitude_Plot_Get_StartTime() -> float:
    return __main__.DARTS_Settings["Attitude_Plot_StartTime"]

def Attitude_Plot_Set_StartTime(value:float) -> None:
    __main__.DARTS_Settings["Attitude_Plot_StartTime"] = value

def Attitude_Plot_Get_TimeLength() -> float:
    return __main__.DARTS_Settings["Attitude_Plot_TimeLength"]

def Attitude_Plot_Set_TimeLength(value:float) -> None:  
    __main__.DARTS_Settings["Attitude_Plot_TimeLength"] = value

def Attitude_Plot_Get_TimeData() -> list[float]:
    return __main__.DARTS_Settings["Attitude_Plot_TimeData"]

def Attitude_Plot_Set_TimeData(value:list[float]) -> None:
    __main__.DARTS_Settings["Attitude_Plot_TimeData"] = value

def Attitude_Plot_Get_QuaternionData() -> list[np.array]:
    return __main__.DARTS_Settings["Attitude_Plot_QuaternionData"]

def Attitude_Plot_Set_QuaternionData(value:list[np.array]) -> None:
    __main__.DARTS_Settings["Attitude_Plot_QuaternionData"] = value

def Attitude_Plot_Get_DisplayType() -> str:
    return __main__.DARTS_Settings["Attitude_Plot_DisplayType"]

def Attitude_Plot_Set_DisplayType(value:str) -> None:
    __main__.DARTS_Settings["Attitude_Plot_DisplayType"] = value