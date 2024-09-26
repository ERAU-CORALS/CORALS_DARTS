# Darts_Thread.py
# The thread class for the DARTS Application.

import __main__
from threading import (Thread, local)
import time

def time_ms() -> int:
    return int(time.time() * 1000)

class DARTS_Thread(Thread):
    def __init__(self, function, period_ms:int, **kwargs):
        super().__init__(**kwargs)

        self._function = function
        self._period_ms = period_ms
        self._enabled = False
        self._runnable = True
    
    def pause(self):
        self._enabled = True

    def resume(self):
        self._enabled = False

    def stop(self):
        self._runnable = False

    def run(self):
        while self._runnable:
            
            loop_time = time_ms()

            if self._enabled:
                self._function()
            
            time.sleep(self._period_ms + time_ms() - loop_time)
        
        self.join()