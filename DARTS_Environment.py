# DARTS_Environment.py
# The environment strapping for the DARTS Application.

import __main__
import os

from dotenv import find_dotenv
from dotenv.main import dotenv_values

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
    __main__.Environment = dotenv_values(find_dotenv())

    for var in All_Variables:
        if os.getenv(var) == None:
            print(f"Strapping {var} to False")
            __main__.Environment[var] = False
        else: 
            try:
                __main__.Environment[var] = bool(os.getenv(var))
            except:
                __main__.Environment[var] = False
            finally:
                print(f"Strapping {var} to {__main__.Environment[var]}")

    for key in __main__.Arg_Environment:
        print (f"Overriding {key} with {__main__.Arg_Environment[key]}")
        try:
            __main__.Environment[key] = {"True": True, "False": False}[__main__.Arg_Environment[key]]
        except:
            try:
                __main__.Environment[key] = int(__main__.Arg_Environment[key])
            except:
                try:
                    __main__.Environment[key] = float(__main__.Arg_Environment[key])
                except:
                    __main__.Environment[key] = __main__.Arg_Environment[key]

    if __main__.Environment["DEBUG"]:
        for var in Debug_Variables:
            print (f"Cascading {var} to True")
            __main__.Environment[var] = True

    if __main__.Environment["DEBUG_WINDOW"]:
        for var in Debug_Window_Variables:
            print (f"Cascading {var} to True")
            __main__.Environment[var] = True

    if __main__.Environment["DEBUG_PROGRAM"]:
        for var in Debug_Program_Variables:
            print (f"Cascading {var} to True")
            __main__.Environment[var] = True