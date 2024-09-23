import time

from dotenv import load_dotenv
import numpy as np

from DARTS_Window import Window as App
from DARTS_Process import DummyProcess as Main

class DARTS_Database(dict):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        print(f"Setting {key} to {value}")

DARTS_Settings = DARTS_Database()
DARTS_Settings["Halt"] = True
DARTS_Settings["AngleType"] = "Degrees"
DARTS_Settings["Attitude"] = [0, 0, 0, 0]
DARTS_Settings["Target"] = [0, 0, 0, 0]
DARTS_Settings["StartTime"] = time.time()
DARTS_Settings["AttitudeDisplayTime"] = []
DARTS_Settings["AttitudeDisplayData"] = [np.array([]),
                                         np.array([]),
                                         np.array([]),
                                         np.array([])]
DARTS_Settings["AttitudeDisplayType"] = "Quaternion"

if __name__ == '__main__':
    load_dotenv()

    App = App()
    Main(App)
    App.mainloop()