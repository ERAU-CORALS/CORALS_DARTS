# Darts_Process.py
# The main process for the DARTS Application.

import __main__
import time

from customtkinter import CTk

import numpy as np

import DARTS_API as api
import DARTS_Utilities as util

DARTS_Database = None
DARTS_Environment = None

def _Process_Print(value:str) -> None:
    util.Debug_Print(__file__, value, DARTS_Environment["DEBUG_PROCESS"])

def DummyAttitude():
    _Process_Print("Dummy Attitude Generation")

    _Process_Print("Getting Generation Start Time")
    generation_time = time.time() - api.Attitude_Plot_Get_StartTime()
    api.Attitude_Plot_Push_TimeData(generation_time)

    _Process_Print("Generating Dummy Quaternion Data")
    q1_data = 2*np.cos(0.5 * np.pi * generation_time / 30)
    q2_data = 0.5*np.sin(np.pi * generation_time / 30 + 2 * np.pi / 3)
    q3_data = np.cos(0.75 * np.pi * generation_time / 30)
    q4_data = np.sin(2 * np.pi * generation_time / 30)

    q_mag = np.sqrt(q1_data**2 + q2_data**2 + q3_data**2 + q4_data**2)
    quat_data = [q1_data, q2_data, q3_data, q4_data]
    quat_data /= q_mag

    _Process_Print("Pushing Quaternion Data")
    api.Attitude_Plot_Push_AttitudeData(quat_data, type="Quaternion")

    while generation_time - api.Attitude_Plot_Get_TimeData()[0] > api.Attitude_Plot_Get_TimeLength():
        _Process_Print("Popping Time and Attitude Data")
        api.Attitude_Plot_Pop_TimeData()
        api.Attitude_Plot_Pop_AttitudeData()

def DummyAttitudeProcess(**kwargs):
    global DARTS_Environment
    DARTS_Environment = kwargs["Environment"]

    _Process_Print ("Dummy Attitude Process")

    print(f"Halt State: {api.Settings_Get_Halt()}")

    if not api.Settings_Get_Halt():
        DummyAttitude()
