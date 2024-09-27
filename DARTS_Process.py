# Darts_Process.py
# The main process for the DARTS Application.

import __main__
import time

from customtkinter import CTk

import numpy as np

import DARTS_API as api

def _Process_Print(value:str) -> None:
    if __main__.DEBUG_PROCESS:
        print(f"Process: {value}")

def DummyAttitude():
    _Process_Print("Dummy Attitude")
    
    __main__.DARTS_Settings["Attitude_Plot_TimeData"].append(time.time() - __main__.DARTS_Settings["Attitude_Plot_StartTime"])
    while __main__.DARTS_Settings["Attitude_Plot_TimeData"][-1] - __main__.DARTS_Settings["Attitude_Plot_TimeData"][0] > api.Attitude_Plot_Get_TimeLength():
        __main__.DARTS_Settings["Attitude_Plot_TimeData"].pop(0)

    time_data = np.array(api.Attitude_Plot_Get_TimeData())

    q0_data = np.sin(2 * np.pi * time_data / 30)
    q1_data = 2*np.cos(0.5 * np.pi * time_data / 30)
    q2_data = 0.5*np.sin(np.pi * time_data / 30 + 2 * np.pi / 3)
    q3_data = np.cos(0.75 * np.pi * time_data / 30)

    q_mag = np.sqrt(q0_data**2 + q1_data**2 + q2_data**2 + q3_data**2)

    api.Attitude_Plot_Set_QuaternionData([q0_data / q_mag, 
                                          q1_data / q_mag, 
                                          q2_data / q_mag, 
                                          q3_data / q_mag])
    
    api.Attitude_Set_Current([q0_data[-1], q1_data[-1], q2_data[-1], q3_data[-1]] / q_mag[-1])

def DummyProcess():
    _Process_Print ("Dummy Process")
    loop_time = time.time()

    if not __main__.DARTS_Settings["Halt"]:
        DummyAttitude()
