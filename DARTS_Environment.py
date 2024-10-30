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

All_Debug_Variables = Debug_Variables + Debug_Window_Variables + Debug_Program_Variables

Database_Variables = {
    "DATABASE_PORT":            6000,
    "DATABASE_KEY":             b'DARTS_Database_Key',
    "DATABASE_LOCK_TIMEOUT":    0.1,
}

All_Settings_Variables = Database_Variables.copy()

def load_environment():
    __main__.Environment = dotenv_values(find_dotenv())

    for var in All_Debug_Variables:
        if os.getenv(var) == None:
            __main__.Environment[var] = False
        else: 
            try:
                __main__.Environment[var] = bool(os.getenv(var))
            except:
                __main__.Environment[var] = False
        print(f"Strapping {var} to {__main__.Environment[var]}")

    for var in All_Settings_Variables:
        if os.getenv(var) == None:
            __main__.Environment[var] = All_Settings_Variables[var]
        else:
            try:
                __main__.Environment[var] = {"True": True, "False": False}[os.getenv(var)]
            except:
                try:
                    __main__.Environment[var] = int(os.getenv(var))
                except:
                    try:
                        __main__.Environment[var] = float(os.getenv(var))
                    except:
                        __main__.Environment[var] = os.getenv(var)
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

