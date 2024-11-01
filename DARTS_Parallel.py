# Darts_Parallel.py
# The multiprocessing class for the DARTS Application.

from multiprocessing import Process, current_process
import sys
import time

from DARTS_API import API_Initialize
from DARTS_Database import Database_Initialize

def time_ms() -> int:
    return int(time.time() * 1000)

class DARTS_Process(Process):
    def __init__(self, function, period_ms:int, name:str=None, Database=None, Environment=None):
        super().__init__(target=self._loop, name=name, kwargs={"Database": Database, "Environment": Environment})

        self._function = function
        self._period_ms = period_ms
        self._enabled = False
        self._runnable = True

    def start(self):
        print (f"Starting Thread: {self._function}")
        self._enabled = True
        super().start()
    
    def pause(self):
        self._enabled = True

    def resume(self):
        self._enabled = False

    def stop(self):
        self._runnable = False

    def _loop(self, **kwargs):

        API_Initialize(kwargs["Database"])
        Database_Initialize(kwargs["Environment"])
        
        while self._runnable:
            
            loop_time = time_ms()

            if self._enabled:
                # print(f"Running {self._function}...")
                self._function(**kwargs)
                # print(f"{self._function} complete.")
            
            print(f"Sleeping for {(self._period_ms - time_ms() + loop_time)} milliseconds...")
            time.sleep((self._period_ms - time_ms() + loop_time) / 1000)