import __main__
import time

from DARTS_Window import Window
from DARTS_Process import DummyAttitudeProcess as AttitudeProcess
from DARTS_Parallel import DARTS_Process as Process
from DARTS_Database import DatabaseManager as Database
from DARTS_Environment import load_environment

def DARTS_Initialize():
    load_environment()

    __main__.DARTS_Database = Database(daemon=True)

    __main__.DARTS_Database.new("Attitude")

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

    __main__.DARTS_Database.new("Target")

    __main__.DARTS_Database["Target"].register("List", list, default=[])
    __main__.DARTS_Database["Target"].register("Indices", list, default=[])

    __main__.DARTS_Database.new("Settings")
    
    __main__.DARTS_Database["Settings"].register("Halt", bool, default=True, values=[True, False])
    __main__.DARTS_Database["Settings"].register("AngleType", str, default="Degrees", 
                                                                   values=["Degrees", "Radians"])
    __main__.DARTS_Database["Settings"].register("QuaternionType", str, default="Q4",
                                                                        values=["Q0", "Q4"])
    

    processes = {
        "Attitude": Process(AttitudeProcess, 200, name="Attitude"),
        "Blinky" : Process(lambda: print("Blinky"), 1000, name="Blinky")
    }

    def Start_Processes(processes: dict[str, Process]) -> None:
        for key in processes:
            print(f"Starting {key} thread...")
            processes[key].start()
            print(f"{key} thread started...")

    def Stop_Processes(processes: dict[str, Process]) -> None:
        for key in processes:
            print(f"Stopping {key} thread...")
            processes[key].stop()
            print(f"{key} thread stopped...")

    def DARTS_Exit() -> None:
        Stop_Processes(processes)
        exit()

    print("Creating Window...")
    __main__.App = Window()
    print("Window Created...")
    __main__.App.after(1000, lambda: Start_Processes(processes))
    __main__.App.protocol("WM_DELETE_WINDOW", DARTS_Exit)
    print("Running Mainloop...")
    __main__.App.mainloop()

if __name__ == '__main__':
    DARTS_Initialize()