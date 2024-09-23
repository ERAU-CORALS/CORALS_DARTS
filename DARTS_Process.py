# Darts_Process.py
# The main process for the DARTS Application.

import __main__
import time

from customtkinter import CTk

import numpy as np

def DummyAttitude(App: CTk):
    loop_time = time.time()

    __main__.DARTS_Settings["AttitudeDisplayTime"].append(loop_time - __main__.DARTS_Settings["StartTime"])
    if __main__.DARTS_Settings["AttitudeDisplayTime"][-1] - __main__.DARTS_Settings["AttitudeDisplayTime"][0] > 10:
        __main__.DARTS_Settings["AttitudeDisplayTime"].pop(0)

    time_data = np.array(__main__.DARTS_Settings["AttitudeDisplayTime"])

    q0_data = np.sin(2 * np.pi * time_data / 10)
    q1_data = 2*np.cos(0.5 * np.pi * time_data / 10)
    q2_data = 0.5*np.sin(np.pi * time_data / 10 + 2 * np.pi / 3)
    q3_data = np.cos(0.75 * np.pi * time_data / 10)

    q_mag = np.sqrt(q0_data**2 + q1_data**2 + q2_data**2 + q3_data**2)

    __main__.DARTS_Settings["AttitudeDisplayData"][0] = q0_data / q_mag
    __main__.DARTS_Settings["AttitudeDisplayData"][1] = q1_data / q_mag
    __main__.DARTS_Settings["AttitudeDisplayData"][2] = q2_data / q_mag
    __main__.DARTS_Settings["AttitudeDisplayData"][3] = q3_data / q_mag

def DummyProcess(App: CTk):
    print ("Dummy Process")
    loop_time = time.time()

    if not __main__.DARTS_Settings["Halt"]:
        DummyAttitude(App)

    App.after(int(time.time() - loop_time + 200), DummyProcess, App)
