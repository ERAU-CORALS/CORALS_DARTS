# Darts_Process.py
# The main process for the DARTS Application.

import __main__
import time

from customtkinter import CTk

import numpy as np

import DARTS_API as api
import DARTS_Utilities as util

def _Process_Print(value:str) -> None:
    if __main__.DEBUG_PROCESS:
        print(f"Process: {value}")

def DummyAttitude():
    _Process_Print("Dummy Attitude Generation")

    generation_time = time.time() - __main__.DARTS_Database["Attitude"]["Plot_StartTime"]
    __main__.DARTS_Database["Attitude"]["Plot_TimeData"].append(generation_time)

    q1_data = 2*np.cos(0.5 * np.pi * generation_time / 30)
    q2_data = 0.5*np.sin(np.pi * generation_time / 30 + 2 * np.pi / 3)
    q3_data = np.cos(0.75 * np.pi * generation_time / 30)
    q4_data = np.sin(2 * np.pi * generation_time / 30)

    q_mag = np.sqrt(q0_data**2 + q1_data**2 + q2_data**2 + q3_data**2)
    quat_data = [q1_data, q2_data, q3_data, q4_data]
    quat_data /= q_mag

    rpy_angles = util.Convert_Quaternion_to_RPY([q1_data, q2_data, q3_data, q4_data])
    roll_data, pitch_data, yaw_data = rpy_angles
    
    euler_parameters = util.Convert_Quaternion_to_EulerParameters([q1_data, q2_data, q3_data, q4_data])
    e1_data, e2_data, e3_data = euler_parameters["axis"]
    phi_data = euler_parameters["angle"]

    gibbs_parameters = util.Convert_Euler_to_Gibbs(euler_parameters)
    p1_data, p2_data, p3_data = gibbs_parameters

    __main__.DARTS_Database["Attitude"]["Current"]["RPY Angles"] = rpy_angles
    __main__.DARTS_Database["Attitude"]["Current"]["Euler Parameters"] = euler_parameters
    __main__.DARTS_Database["Attitude"]["Current"]["Gibbs-Rodriguez"] = gibbs_parameters
    __main__.DARTS_Database["Attitude"]["Current"]["Quaternion"] = quat_data

    __main__.DARTS_Database["Attitude"]["Plot_AttitudeData"]["Roll"].append(roll_data)
    __main__.DARTS_Database["Attitude"]["Plot_AttitudeData"]["Pitch"].append(pitch_data)
    __main__.DARTS_Database["Attitude"]["Plot_AttitudeData"]["Yaw"].append(yaw_data)

    __main__.DARTS_Database["Attitude"]["Plot_AttitudeData"]["E1"].append(e1_data)
    __main__.DARTS_Database["Attitude"]["Plot_AttitudeData"]["E2"].append(e2_data)
    __main__.DARTS_Database["Attitude"]["Plot_AttitudeData"]["E3"].append(e3_data)
    __main__.DARTS_Database["Attitude"]["Plot_AttitudeData"]["Phi"].append(phi_data)

    __main__.DARTS_Database["Attitude"]["Plot_AttitudeData"]["P1"].append(p1_data)
    __main__.DARTS_Database["Attitude"]["Plot_AttitudeData"]["P2"].append(p2_data)
    __main__.DARTS_Database["Attitude"]["Plot_AttitudeData"]["P3"].append(p3_data)

    __main__.DARTS_Database["Attitude"]["Plot_AttitudeData"]["Q1"].append(q1_data)
    __main__.DARTS_Database["Attitude"]["Plot_AttitudeData"]["Q2"].append(q2_data)
    __main__.DARTS_Database["Attitude"]["Plot_AttitudeData"]["Q3"].append(q3_data)
    __main__.DARTS_Database["Attitude"]["Plot_AttitudeData"]["Q4"].append(q4_data)

    while generation_time - __main__.DARTS_Database["Attitude"]["Plot_TimeData"][0] > __main__.DARTS_Database["Attitude"]["Plot_TimeLength"]:
        __main__.DARTS_Database["Attitude"]["Plot_TimeData"].pop(0)
        for key in __main__.DARTS_Database["Attitude"]["Plot_AttitudeData"]:
            __main__.DARTS_Database["Attitude"]["Plot_AttitudeData"][key].pop(0)

def DummyAttitudeProcess():
    _Process_Print ("Dummy Process")
    loop_time = time.time()

    if not __main__.DARTS_Settings["Halt"]:
        DummyAttitude()
