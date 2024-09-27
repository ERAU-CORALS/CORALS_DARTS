import __main__
import time

import numpy as np

from DARTS_Window import Window as App
from DARTS_Process import DummyAttitudeProcess as AttitudeProcess
from DARTS_Threading import DARTS_Thread as Thread
from DARTS_Database import Database
from DARTS_Environment import load_environment

def DARTS_Initialize():
    load_environment()

    __main__.DARTS_Database = {
        "Attitude": Database(),
        "Target": Database(),
        "Settings": Database(),
    }

    __main__.DARTS_Database["Attitude"].register("Current", dict, default={"RPY Angles": [0, 0, 0],
                                                                           "Euler Parameters": {"axis": [0, 0, 0], "angle": 0},
                                                                           "Gibbs-Rodriguez": [0, 0, 0],
                                                                           "Quaternion": [0, 0, 0, 1]})
    
    __main__.DARTS_Database["Attitude"].register("Plot_StartTime", float, default=time.time())
    __main__.DARTS_Database["Attitude"].register("Plot_TimeLength", float, default=0)
    __main__.DARTS_Database["Attitude"].register("Plot_TimeData", list, default=[])
    __main__.DARTS_Database["Attitude"].register("Plot_AttitudeData", dict, default={"Roll": [], "Pitch": [], "Yaw": [],
                                                                                     "E1": [], "E2": [], "E3": [], "Phi": [],
                                                                                     "P1": [], "P2": [], "P3": [],
                                                                                     "Q1": [], "Q2": [], "Q3": [], "Q4": []})

    __main__.DARTS_Database["Target"].register("List", list, default=[])

    __main__.DARTS_Database["Settings"].register("Halt", bool, default=True, values=[True, False])
    __main__.DARTS_Database["Settings"].register("AngleType", str, default="Degrees", 
                                                                   values=["Degrees", "Radians"])
    __main__.DARTS_Database["Settings"].register("QuaternionType", str, default="Q4",
                                                                        values=["Q0", "Q4"])
    
    threads = {
        "Attitude": Thread(AttitudeProcess, 200)
    }
    for key in threads:
        threads[key].start()

    App = App()
    App.mainloop()

    for key in threads:
        threads[key].stop()

if __name__ == '__main__':
    DARTS_Initialize()