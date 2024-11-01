import __main__
import subprocess
import sys

from DARTS_Environment import load_environment
from DARTS_Utilities import Path_Truncate

def DARTS_Common() -> None:
    __main__.Program_Name = sys.argv[0]
    __main__.Program_Name = Path_Truncate(__main__.Program_Name)

    __main__.Program_Type = "STARTUP_ALL"
    __main__.Arg_Environment = {}
    long_environment = False

    for i in range(1, len(sys.argv)):
        if long_environment:
            name, value = sys.argv[i].split("=")
            __main__.Arg_Environment[name] = value
            long_environment = False
        elif sys.argv[i] in ["-h", "--help"]:
            DARTS_Help()
            exit()
        elif sys.argv[i] in ["-d", "--database"]:
            if __main__.Program_Type != "STARTUP_ALL":
                raise ValueError("Cannot run DARTS Database Daemon with DARTS GUI")
            __main__.Program_Type = "DATABASE"
        elif sys.argv[i] in ["-g", "--gui"]:
            if __main__.Program_Type != "STARTUP_ALL":
                raise ValueError("Cannot run DARTS GUI with DARTS Database Daemon")
            __main__.Program_Type = "GUI"
        elif sys.argv[i][0:2] == "-e":
            name, value = sys.argv[i][2:].split("=")
            __main__.Arg_Environment[name] = value
        elif sys.argv[i] == "--env":
            long_environment = True
        else:
            raise ValueError(f"Invalid argument: {sys.argv[i]}")
        
    if __main__.Program_Type == "STARTUP_ALL":
        print("Starting all DARTS processes")
        for flag in ["-d", "-g"]:
            command = []
            if ".py" in __main__.Program_Name:
                command += ["python"]

            command += [sys.argv[0], flag]
            command += [f"-e{key}={__main__.Arg_Environment[key]}" for key in __main__.Arg_Environment]
        
            subprocess.Popen(command)

    if __main__.Program_Type[0:3] == "GUI":
        print("Starting GUI")
        DARTS_GUI()

    elif __main__.Program_Type == "DATABASE":
        print("Starting Database Daemon")
        DARTS_Database()

def DARTS_Help() -> None:
    print(f"Usage: {__main__.Program_Name}")
    print("Options:")
    print("  -h            --help           : print this help message and exit")
    print("  -d            --database       : run DARTS Database Daemon (cannot be run with -g)")
    print("  -ename=value  --env name=value : set an environment variable (overrides defaults in .env)")
    print("  -g            --gui            : run DARTS GUI (cannot be run with -d; starts other instance with -d)")

def Blinky(*args, **kwargs) -> None:
    print("Blinky")

def DARTS_Database() -> None:
    load_environment(__main__.Arg_Environment)

    from DARTS_Database import DatabaseManager

    manager = DatabaseManager()
    server = manager.get_server()
    server.serve_forever()

def DARTS_GUI() -> None:
    load_environment(__main__.Arg_Environment)

    import time
    from DARTS_Database import DatabaseManager

    manager = DatabaseManager()
    manager.connect()

    DARTS_Environment = manager.dict(load_environment(__main__.Arg_Environment))

    DARTS_Database = manager.Database({cat: manager.DatabaseCategory() for cat in 
                                                ("Attitude", "Target", "Settings")})
    DARTS_Database["Attitude"].register \
        ("Current", default={"RPY Angles": [0, 0, 0],
                             "Euler Parameters": {"axis": [0, 0, 0], "angle": 0},
                             "Gibbs-Rodriguez": [0, 0, 0],
                             "Quaternion": [0, 0, 0, 1]},
                    types=[dict])
    DARTS_Database["Attitude"].register \
        ("Plot_StartTime", default=time.time(), types=[int, float])
    DARTS_Database["Attitude"].register \
        ("Plot_TimeLength", default=60, types=[int, float])
    DARTS_Database["Attitude"].register \
        ("Plot_TimeData", default=[], types=[list])
    DARTS_Database["Attitude"].register \
        ("Plot_AttitudeData", default={"RPY Angles": [[],[],[]],
                                        "Euler Parameters": {"axis": [[],[],[]], "angle": []},
                                        "Gibbs-Rodriguez": [[],[],[]],
                                        "Quaternion": [[],[],[],[]]},
                      types=[dict])
    DARTS_Database["Attitude"].register \
        ("Plot_DisplayType", default="RPY Angles",
                             values=["RPY Angles", "Euler Parameters", "Gibbs-Rodriguez", "Quaternion"],
                             types=[str])
    
    DARTS_Database["Target"].register \
        ("List", default=[], types=[list])
    DARTS_Database["Target"].register \
        ("Indices", default=[], types=[list])
    
    DARTS_Database["Settings"].register \
        ("Halt", default=True, values=[True, False], types=[bool])
    DARTS_Database["Settings"].register \
        ("AngleType", default="Degrees", values=["Degrees", "Radians"], types=[str])
    DARTS_Database["Settings"].register \
        ("QuaternionType", default="Q4", values=["Q0", "Q4"], types=[str])
    
    from DARTS_API import API_Initialize
    API_Initialize(DARTS_Database)
    
    from DARTS_Parallel import DARTS_Process as Process
    from DARTS_Process import DummyAttitudeProcess as AttitudeProcess

    processes = {
        "Attitude": Process(AttitudeProcess, 1000, name="Attitude", Database=DARTS_Database, Environment=DARTS_Environment),
        "Blinky" : Process(Blinky, 1000, name="Blinky"),
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

    Start_Processes(processes)

    from DARTS_Window import Window

    __main__.App = Window()
    __main__.App.mainloop()

    Stop_Processes(processes)

# def DARTS_Initialize():
#     load_environment()

#     __main__.DARTS_Database = Database(daemon=True)

#     __main__.DARTS_Database.new("Attitude")

#     __main__.DARTS_Database["Attitude"].register("Current", dict, default={"RPY Angles": [0, 0, 0],
#                                                                            "Euler Parameters": {"axis": [0, 0, 0], "angle": 0},
#                                                                            "Gibbs-Rodriguez": [0, 0, 0],
#                                                                            "Quaternion": [0, 0, 0, 1]})
    
#     __main__.DARTS_Database["Attitude"].register("Plot_StartTime", float, default=time.time())
#     __main__.DARTS_Database["Attitude"].register("Plot_TimeLength", float, default=60)
#     __main__.DARTS_Database["Attitude"].register("Plot_TimeData", list, default=[])
#     __main__.DARTS_Database["Attitude"].register("Plot_AttitudeData", dict, default={"RPY Angles": [[],[],[]],
#                                                                                      "Euler Parameters": {"axis": [[],[],[]], "angle": []},
#                                                                                      "Gibbs-Rodriguez": [[],[],[]],
#                                                                                      "Quaternion": [[],[],[],[]]})
#     __main__.DARTS_Database["Attitude"].register("Plot_DisplayType", str, default="RPY Angles",
#                                                                           values=["RPY Angles", "Euler Parameters", "Gibbs-Rodriguez", "Quaternion"])

#     __main__.DARTS_Database.new("Target")

#     __main__.DARTS_Database["Target"].register("List", list, default=[])
#     __main__.DARTS_Database["Target"].register("Indices", list, default=[])

#     __main__.DARTS_Database.new("Settings")
    
#     __main__.DARTS_Database["Settings"].register("Halt", bool, default=True, values=[True, False])
#     __main__.DARTS_Database["Settings"].register("AngleType", str, default="Degrees", 
#                                                                    values=["Degrees", "Radians"])
#     __main__.DARTS_Database["Settings"].register("QuaternionType", str, default="Q4",
#                                                                         values=["Q0", "Q4"])
    

#     processes = {
#         "Attitude": Process(AttitudeProcess, 200, name="Attitude"),
#         "Blinky" : Process(lambda: print("Blinky"), 1000, name="Blinky")
#     }

#     def Start_Processes(processes: dict[str, Process]) -> None:
#         for key in processes:
#             print(f"Starting {key} thread...")
#             processes[key].start()
#             print(f"{key} thread started...")

#     def Stop_Processes(processes: dict[str, Process]) -> None:
#         for key in processes:
#             print(f"Stopping {key} thread...")
#             processes[key].stop()
#             print(f"{key} thread stopped...")

#     def DARTS_Exit() -> None:
#         Stop_Processes(processes)
#         exit()

#     print("Creating Window...")
#     __main__.App = Window()
#     print("Window Created...")
#     __main__.App.after(1000, lambda: Start_Processes(processes))
#     __main__.App.protocol("WM_DELETE_WINDOW", DARTS_Exit)
#     print("Running Mainloop...")
#     __main__.App.mainloop()

if __name__ == '__main__':
    print(sys.argv)
    DARTS_Common()