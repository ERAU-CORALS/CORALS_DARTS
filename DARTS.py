import time

import numpy as np

from DARTS_Window import Window as App
from DARTS_Process import DummyProcess as Main
from DARTS_Database import DARTS_Database as Database
from DARTS_Environment import load_environment

if __name__ == '__main__':
    load_environment()

    DARTS_Settings = Database()
    DARTS_Settings.register("Halt", True, [True, False])
    DARTS_Settings.register("AngleType", "Degrees", ["Degrees", "Radians"])
    DARTS_Settings.register("Attitude", [0, 0, 0, 0])
    DARTS_Settings.register("Target", [0, 0, 0, 0])
    DARTS_Settings.register("StartTime", time.time())
    DARTS_Settings.register("AttitudeDisplayTime", [])
    DARTS_Settings.register("AttitudeDisplayData", [np.array([]),
                                                    np.array([]),
                                                    np.array([]),
                                                    np.array([])])
    DARTS_Settings.register("AttitudeDisplayType", "Quaternion", ["RPY Angles", 
                                                                "Euler Parameters", 
                                                                "Gibbs-Rodriguez", 
                                                                "Quaternion"])

    App = App()
    
    Main(App)
    App.mainloop()