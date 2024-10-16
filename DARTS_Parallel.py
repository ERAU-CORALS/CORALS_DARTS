# Darts_Parallel.py
# The multiprocessing class for the DARTS Application.

import __main__
from multiprocessing import Process
from multiprocessing.managers import BaseManager
import time

from DARTS_Environment import load_environment

def time_ms() -> int:
    return int(time.time() * 1000)

class DARTS_Process(Process):
    def __init__(self, function, period_ms:int, **kwargs):
        super().__init__(target=self._loop, **kwargs)

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

    def _loop(self):
        load_environment()

        while self._runnable:
            
            loop_time = time_ms()

            if self._enabled:
                self._function()
            
            time.sleep(self._period_ms / 1000 + time_ms() - loop_time)