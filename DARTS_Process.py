# Darts_Process.py
# The main process for the DARTS Application.

import __main__
import time

from customtkinter import CTk

import numpy as np

import DARTS_API as api
import DARTS_Utilities as util

def _Process_Print(value:str) -> None:
    if __main__.DEBUG:
        print(f"Process: {value}", flush=True)

def DummyAttitude():
    _Process_Print("Dummy Attitude Generation")

    generation_time = time.time() - api.Attitude_Plot_Get_StartTime()
    api.Attitude_Plot_Push_TimeData(generation_time)

    q1_data = 2*np.cos(0.5 * np.pi * generation_time / 30)
    q2_data = 0.5*np.sin(np.pi * generation_time / 30 + 2 * np.pi / 3)
    q3_data = np.cos(0.75 * np.pi * generation_time / 30)
    q4_data = np.sin(2 * np.pi * generation_time / 30)

    q_mag = np.sqrt(q1_data**2 + q2_data**2 + q3_data**2 + q4_data**2)
    quat_data = [q1_data, q2_data, q3_data, q4_data]
    quat_data /= q_mag

    api.Attitude_Plot_Push_AttitudeData(quat_data, type="Quaternion")

    while generation_time - api.Attitude_Plot_Get_StartTime() > api.Attitude_Plot_Get_TimeLength():
        api.Attitude_Plot_Pop_TimeData()
        api.Attitude_Plot_Pop_AttitudeData()

def DummyAttitudeProcess():
    _Process_Print ("Dummy Process")

    print(f"Halt State: {api.Settings_Get_Halt()}")

    if not api.Settings_Get_Halt():
        DummyAttitude()
