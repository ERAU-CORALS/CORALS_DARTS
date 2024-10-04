import __main__
import time

import numpy as np

from DARTS_Window import Window
from DARTS_Process import DummyAttitude as AttitudeProcess
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
    __main__.DARTS_Database["Attitude"].register("Plot_TimeLength", float, default=60)
    __main__.DARTS_Database["Attitude"].register("Plot_TimeData", list, default=[])
    __main__.DARTS_Database["Attitude"].register("Plot_AttitudeData", dict, default={"RPY Angles": [[],[],[]],
                                                                                     "Euler Parameters": {"axis": [[],[],[]], "angle": []},
                                                                                     "Gibbs-Rodriguez": [[],[],[]],
                                                                                     "Quaternion": [[],[],[],[]]})
    __main__.DARTS_Database["Attitude"].register("Plot_DisplayType", str, default="RPY Angles",
                                                                          values=["RPY Angles", "Euler Parameters", "Gibbs-Rodriguez", "Quaternion"])

    __main__.DARTS_Database["Target"].register("List", list, default=[])
    __main__.DARTS_Database["Target"].register("Indices", list, default=[])

    __main__.DARTS_Database["Settings"].register("Halt", bool, default=True, values=[True, False])
    __main__.DARTS_Database["Settings"].register("AngleType", str, default="Degrees", 
                                                                   values=["Degrees", "Radians"])
    __main__.DARTS_Database["Settings"].register("QuaternionType", str, default="Q4",
                                                                        values=["Q0", "Q4"])
    
    threads = {
        "Attitude": Thread(AttitudeProcess, 200, name="Attitude"),
    }
    for key in threads:
        print(f"Starting {key} thread...")
        threads[key].start()
        print(f"{key} thread started...")

    print("Creating Window...")
    __main__.App = Window()
    print("Window Created...")
    print("Running Mainloop...")
    __main__.App.mainloop()
    print("Mainloop Exited...")

    for key in threads:
        print(f"Stopping {key} thread...")
        threads[key].stop()
        print(f"{key} thread stopped...")

if __name__ == '__main__':
    DARTS_Initialize()