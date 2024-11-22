# DARTS_API.py
# The API functions for the DARTS Application.

import __main__

import DARTS_Utilities as util

def _API_Print(value: str): 
    util.Debug_Print(__file__, value, __main__.Environment["DEBUG_API"])

DARTS_Database = None

def API_Initialize(DatabaseProxy) -> None:
    global DARTS_Database
    _API_Print("Initializing API")
    DARTS_Database = DatabaseProxy

########################################################################
#
# DARTS Attitude Settings
#
########################################################################

def Attitude_Get_Current_Type(type:str="RPY Angles") -> list[float]|dict[str, float]:
    _API_Print(f"Getting Attitude Current {type}")
    return DARTS_Database["Attitude"]["Current"][type]

def Attitude_Set_Current_Type(value:list[float]|dict[str, float], type:str="RPY Angles") -> None:
    _API_Print(f"Setting Attitude Current {type} to {value}")

    new_data = dict(DARTS_Database["Attitude"]["Current"])

    if type == "RPY Angles":

        new_data["RPY Angles"] = value
        new_data["Euler Parameters"] = util.Convert_RPY_to_Euler(value)
        new_data["Gibbs-Rodriguez"] = util.Convert_RPY_to_Gibbs(value)
        new_data["Quaternion"] = util.Convert_RPY_to_Quaternion(value)

    elif type == "Euler Parameters":

        new_data["RPY Angles"] = util.Convert_Euler_to_RPY(value)
        new_data["Euler Parameters"] = value
        new_data["Gibbs-Rodriguez"] = util.Convert_Euler_to_Gibbs(value)
        new_data["Quaternion"] = util.Convert_Euler_to_Quaternion(value)

    elif type == "Gibbs-Rodriguez":

        new_data["RPY Angles"] = util.Convert_Gibbs_to_RPY(value)
        new_data["Euler Parameters"] = util.Convert_Gibbs_to_Euler(value)
        new_data["Gibbs-Rodriguez"] = value
        new_data["Quaternion"] = util.Convert_Gibbs_to_Quaternion(value)

    elif type == "Quaternion":

        new_data["RPY Angles"] = util.Convert_Quaternion_to_RPY(value)
        new_data["Euler Parameters"] = util.Convert_Quaternion_to_Euler(value)
        new_data["Gibbs-Rodriguez"] = util.Convert_Quaternion_to_Gibbs(value)
        new_data["Quaternion"] = value

    DARTS_Database["Attitude"]["Current"] = new_data

def Attitude_Plot_Get_StartTime() -> float:
    _API_Print("Getting Attitude Plot Start Time")
    return DARTS_Database["Attitude"]["Plot_StartTime"]

def Attitude_Plot_Set_StartTime(value:float) -> None:
    _API_Print(f"Setting Attitude Plot StartTime to {value}")
    DARTS_Database["Attitude"]["Plot_StartTime"] = value

def Attitude_Plot_Get_TimeLength() -> float:
    _API_Print("Getting Attitude Plot Time Length")
    return DARTS_Database["Attitude"]["Plot_TimeLength"]

def Attitude_Plot_Set_TimeLength(value:float) -> None:
    _API_Print(f"Setting Attitude Plot Time Length to {value}")
    DARTS_Database["Attitude"]["Plot_TimeLength"] = value

def Attitude_Plot_Get_TimeData() -> list[float]:
    _API_Print("Getting Attitude Plot Time Data")
    return DARTS_Database["Attitude"]["Plot_TimeData"]

def Attitude_Plot_Push_TimeData(value:list[float]) -> None:
    _API_Print(f"Pusing {value} to Attitude Plot Time Data")
    new_data = list(DARTS_Database["Attitude"]["Plot_TimeData"])
    new_data.append(value)
    DARTS_Database["Attitude"]["Plot_TimeData"] = new_data

def Attitude_Plot_Pop_TimeData(index:int=0) -> float:
    _API_Print("Popping Attitude Plot Time Data")
    new_data = list(DARTS_Database["Attitude"]["Plot_TimeData"])
    value = new_data.pop(index)
    DARTS_Database["Attitude"]["Plot_TimeData"] = new_data
    return value

def Attitude_Plot_Clear_TimeData() -> None:
    _API_Print("Clearing Attitude Plot Time Data")
    DARTS_Database["Attitude"]["Plot_TimeData"] = []

def Attitude_Plot_Get_AttitudeData(type:str="RPY Angles") -> list[float]:
    _API_Print(f"Getting Attitude Plot {type} Data")
    return DARTS_Database["Attitude"]["Plot_AttitudeData"][type]

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

    new_data = dict(DARTS_Database["Attitude"]["Plot_AttitudeData"])

    for i in range(3):

        new_data["RPY Angles"][i].append(angles[i])
        new_data["Euler Parameters"]["axis"][i].append(euler["axis"][i])
        new_data["Gibbs-Rodriguez"][i].append(gibbs[i])
        new_data["Quaternion"][i].append(quat[i])

    new_data["Euler Parameters"]["angle"].append(euler["angle"])
    new_data["Quaternion"][3].append(quat[3])

    DARTS_Database["Attitude"]["Plot_AttitudeData"] = new_data

def Attitude_Plot_Pop_AttitudeData(index:int=0) -> None:
    _API_Print("Popping Attitude Plot Attitude Data")

    new_data = dict(DARTS_Database["Attitude"]["Plot_AttitudeData"])

    for i in range(3):

        new_data["RPY Angles"][i].pop(index)
        new_data["Euler Parameters"]["axis"][i].pop(index)
        new_data["Gibbs-Rodriguez"][i].pop(index)
        new_data["Quaternion"][i].pop(index)

    new_data["Euler Parameters"]["angle"].pop(index)
    new_data["Quaternion"][3].pop(index)

    DARTS_Database["Attitude"]["Plot_AttitudeData"] = new_data

def Attitude_Plot_Clear_AttitudeData() -> None:
    _API_Print("Clearing Attitude Plot Data")

    DARTS_Database["Attitude"]["Plot_AttitudeData"] = {"RPY Angles": [[],[],[]],
                                                       "Euler Parameters": {"axis": [[],[],[]], "angle": []},
                                                       "Gibbs-Rodriguez": [[],[],[]],
                                                       "Quaternion": [[],[],[],[]]}
    
def Attitude_Plot_Get_DisplayType() -> str:
    _API_Print("Getting Attitude Plot Display Type")
    return DARTS_Database["Attitude"]["Plot_DisplayType"]

def Attitude_Plot_Set_DisplayType(value:str) -> None:
    _API_Print(f"Setting Attitude Plot Display Type to {value}")
    DARTS_Database["Attitude"]["Plot_DisplayType"] = value

########################################################################
#
# DARTS Targets Settings
#
########################################################################

def Targets_Get_CurrentIndices() -> list[int]:
    _API_Print("Getting Targets Current Display Indices")
    return DARTS_Database["Target"]["Indices"]

def Targets_Set_CurrentIndices(value:list[int]) -> None:
    _API_Print(f"Setting Targets Current Display Indices to {value}")
    DARTS_Database["Target"]["Indices"] = value

def Targets_Get_List() -> list[list[float]]:
    _API_Print("Getting Targets List")
    return DARTS_Database["Target"]["List"]

def Targets_Set_List(value:list[list[float]]) -> None:
    _API_Print(f"Setting Targets List to {value}")
    DARTS_Database["Target"]["List"] = value

########################################################################
#
# DARTS Gains Settings
#
########################################################################

def Gains_Get_Matrix() -> list[list[float]]:
    _API_Print("Getting Gains Matrix")
    return DARTS_Database["Gains"]["Matrix"]

def Gains_Set_Matrix(value:list[list[float]]) -> None:
    _API_Print(f"Setting Gains Matrix to {value}")
    DARTS_Database["Gains"]["Matrix"] = value

def Gains_Get_Exponent() -> int:
    _API_Print("Getting Gains Exponent")
    return DARTS_Database["Gains"]["Exponent"]

def Gains_Set_Exponent(value:int) -> None:
    _API_Print(f"Setting Gains Exponent to {value}")
    DARTS_Database["Gains"]["Exponent"] = value

########################################################################
#
# DARTS Bluetooth Settings
#
########################################################################

def Send_1R_Requested() -> bool:
    _API_Print("Checking if 1R Data is Requested")
    return DARTS_Database["Bluetooth"]["Send_1R"]

def Request_Send_1R() -> None:
    _API_Print("Requesting 1R Data")
    DARTS_Database["Bluetooth"]["Send_1R"] = True

def Send_2R_Requested() -> bool:
    _API_Print("Checking if 2R Data is Requested")
    return DARTS_Database["Bluetooth"]["Send_2R"]

def Request_Send_2R() -> None:
    _API_Print("Requesting 2R Data")
    DARTS_Database["Bluetooth"]["Send_2R"] = True

def Send_3R_Requested() -> bool:
    _API_Print("Checking if 3R Data is Requested")
    return DARTS_Database["Bluetooth"]["Send_3R"]

def Request_Send_3R() -> None:
    _API_Print("Requesting 3R Data")
    DARTS_Database["Bluetooth"]["Send_3R"] = True

def Send_4R_Requested() -> bool:
    _API_Print("Checking if 4R Data is Requested")
    return DARTS_Database["Bluetooth"]["Send_4R"]

def Request_Send_4R() -> None:
    _API_Print("Requesting 4R Data")
    DARTS_Database["Bluetooth"]["Send_4R"] = True

def Send_5R_Requested() -> bool:
    _API_Print("Checking if 5R Data is Requested")
    return DARTS_Database["Bluetooth"]["Send_5R"]

def Request_Send_5R() -> None:
    _API_Print("Requesting 5R Data")
    DARTS_Database["Bluetooth"]["Send_5R"] = True

def Get_BLE_Commanded_Q0() -> float:
    _API_Print("Getting BLE Commanded Q0")
    return DARTS_Database["Bluetooth"]["Commanded_Q0"]

def Set_BLE_Commanded_Q0(value:float) -> None:
    _API_Print(f"Setting BLE Commanded Q0 to {value}")
    DARTS_Database["Bluetooth"]["Commanded_Q0"] = value

def Get_BLE_Commanded_Q1() -> float:
    _API_Print("Getting BLE Commanded Q1")
    return DARTS_Database["Bluetooth"]["Commanded_Q1"]

def Set_BLE_Commanded_Q1(value:float) -> None:
    _API_Print(f"Setting BLE Commanded Q1 to {value}")
    DARTS_Database["Bluetooth"]["Commanded_Q1"] = value

def Get_BLE_Commanded_Q2() -> float:
    _API_Print("Getting BLE Commanded Q2")
    return DARTS_Database["Bluetooth"]["Commanded_Q2"]

def Set_BLE_Commanded_Q2(value:float) -> None:
    _API_Print(f"Setting BLE Commanded Q2 to {value}")
    DARTS_Database["Bluetooth"]["Commanded_Q2"] = value

def Get_BLE_Commanded_Q3() -> float:
    _API_Print("Getting BLE Commanded Q3")
    return DARTS_Database["Bluetooth"]["Commanded_Q3"]

def Set_BLE_Commanded_Q3(value:float) -> None:
    _API_Print(f"Setting BLE Commanded Q3 to {value}")
    DARTS_Database["Bluetooth"]["Commanded_Q3"] = value

def Get_BLE_Target_Type() -> str:
    _API_Print("Getting BLE Target Type")
    return DARTS_Database["Bluetooth"]["Target_Type"]

def Set_BLE_Target_Type(value:str) -> None:
    _API_Print(f"Setting BLE Target Type to {value}")
    DARTS_Database["Bluetooth"]["Target_Type"] = value

def Get_BLE_Target_Action() -> str:
    _API_Print("Getting BLE Target Action")
    return DARTS_Database["Bluetooth"]["Target_Action"]

def Set_BLE_Target_Action(value:str) -> None:
    _API_Print(f"Setting BLE Target Action to {value}")
    DARTS_Database["Bluetooth"]["Target_Action"] = value

def Get_BLE_Target_Index() -> int:
    _API_Print("Getting BLE Target Index")
    return DARTS_Database["Bluetooth"]["Target_Index"]

def Set_BLE_Target_Index(value:int) -> None:
    _API_Print(f"Setting BLE Target Index to {value}")
    DARTS_Database["Bluetooth"]["Target_Index"] = value

def Get_BLE_Reported_Q0() -> float:
    _API_Print("Getting BLE Reported Q0")
    return DARTS_Database["Bluetooth"]["Reported_Q0"]

def Set_BLE_Reported_Q0(value:float) -> None:
    _API_Print(f"Setting BLE Reported Q0 to {value}")
    DARTS_Database["Bluetooth"]["Reported_Q0"] = value

def Get_BLE_Reported_Q1() -> float:
    _API_Print("Getting BLE Reported Q1")
    return DARTS_Database["Bluetooth"]["Reported_Q1"]

def Set_BLE_Reported_Q1(value:float) -> None:
    _API_Print(f"Setting BLE Reported Q1 to {value}")
    DARTS_Database["Bluetooth"]["Reported_Q1"] = value

def Get_BLE_Reported_Q2() -> float:
    _API_Print("Getting BLE Reported Q2")
    return DARTS_Database["Bluetooth"]["Reported_Q2"]

def Set_BLE_Reported_Q2(value:float) -> None:
    _API_Print(f"Setting BLE Reported Q2 to {value}")
    DARTS_Database["Bluetooth"]["Reported_Q2"] = value

def Get_BLE_Reported_Q3() -> float:
    _API_Print("Getting BLE Reported Q3")
    return DARTS_Database["Bluetooth"]["Reported_Q3"]

def Set_BLE_Reported_Q3(value:float) -> None:
    _API_Print(f"Setting BLE Reported Q3 to {value}")
    DARTS_Database["Bluetooth"]["Reported_Q3"] = value

def Get_BLE_Attitude_Q0() -> float:
    _API_Print("Getting BLE Attitude Q0")
    return DARTS_Database["Bluetooth"]["Attitude_Q0"]

def Set_BLE_Attitude_Q0(value:float) -> None:
    _API_Print(f"Setting BLE Attitude Q0 to {value}")
    DARTS_Database["Bluetooth"]["Attitude_Q0"] = value

def Get_BLE_Attitude_Q1() -> float:
    _API_Print("Getting BLE Attitude Q1")
    return DARTS_Database["Bluetooth"]["Attitude_Q1"]

def Set_BLE_Attitude_Q1(value:float) -> None:
    _API_Print(f"Setting BLE Attitude Q1 to {value}")
    DARTS_Database["Bluetooth"]["Attitude_Q1"] = value

def Get_BLE_Attitude_Q2() -> float:
    _API_Print("Getting BLE Attitude Q2")
    return DARTS_Database["Bluetooth"]["Attitude_Q2"]

def Set_BLE_Attitude_Q2(value:float) -> None:
    _API_Print(f"Setting BLE Attitude Q2 to {value}")
    DARTS_Database["Bluetooth"]["Attitude_Q2"] = value

def Get_BLE_Attitude_Q3() -> float:
    _API_Print("Getting BLE Attitude Q3")
    return DARTS_Database["Bluetooth"]["Attitude_Q3"]

def Set_BLE_Attitude_Q3(value:float) -> None:
    _API_Print(f"Setting BLE Attitude Q3 to {value}")
    DARTS_Database["Bluetooth"]["Attitude_Q3"] = value

########################################################################
#
# DARTS Application Settings
#
########################################################################

def Settings_Get_Halt() -> bool:
    _API_Print("Getting Halt Setting")
    return DARTS_Database["Settings"]["Halt"]

def Settings_Set_Halt(value:bool) -> None:
    _API_Print(f"Setting Halt Setting to {value}")
    DARTS_Database["Settings"]["Halt"] = value

def Settings_Get_AngleType() -> str:
    _API_Print("Getting Angle Type Setting")
    return DARTS_Database["Settings"]["AngleType"]

def Settings_Set_AngleType(value:str) -> None:
    _API_Print(f"Setting Angle Type Setting to {value}")
    DARTS_Database["Settings"]["AngleType"] = value

def Settings_Get_QuaternionType() -> str:
    _API_Print("Getting Quaternion Type Setting")
    return DARTS_Database["Settings"]["QuaternionType"]

def Settings_Set_QuaternionType(value:str) -> None:
    _API_Print(f"Setting Quaternion Type Setting to {value}")
    DARTS_Database["Settings"]["QuaternionType"] = value