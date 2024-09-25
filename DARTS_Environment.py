# DARTS_Environment.py
# The environment strapping for the DARTS Application.

import __main__
import os

from dotenv import load_dotenv

Debug_Window_Variables = [
    "DEBUG_ATTITUDE_PAGE",
    "DEBUG_DEBUG_PAGE",
    "DEBUG_GAINS_PAGE",
    "DEBUG_SETTINGS_PAGE",
    "DEBUG_TARGETS_PAGE",
    "DEBUG_TELEMETRY_PAGE",
]

Debug_Program_Variables = [
    "DEBUG_API",
    "DEBUG_DATABASE",
    "DEBUG_ENVIRONMENT",
    "DEBUG_RENDERING",
    "DEBUG_PROCESS",
    "DEBUG_UTILITIES",
]

Debug_Variables = [
    "DEBUG",
    "DEBUG_PROGRAM",
    "DEBUG_WINDOW",
]

All_Variables = Debug_Variables + Debug_Window_Variables + Debug_Program_Variables

def load_environment():
    load_dotenv()

    for var in All_Variables:
        if os.getenv(var) == None:
            print(f"Strapping {var} to False")
            __main__.__dict__[var] = False
        else: 
            try:
                __main__.__dict__[var] = bool(os.getenv(var))
            except:
                __main__.__dict__[var] = False
            finally:
                print(f"Strapping {var} to {__main__.__dict__[var]}")

    if __main__.DEBUG:
        for var in Debug_Variables:
            print (f"Cascading {var} to True")
            __main__.__dict__[var] = True

    if __main__.DEBUG_WINDOW:
        for var in Debug_Window_Variables:
            print (f"Cascading {var} to True")
            __main__.__dict__[var] = True

    if __main__.DEBUG_PROGRAM:
        for var in Debug_Program_Variables:
            print (f"Cascading {var} to True")
            __main__.__dict__[var] = True