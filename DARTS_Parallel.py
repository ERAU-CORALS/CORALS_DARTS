# Darts_Parallel.py
# The multiprocessing class for the DARTS Application.

from multiprocessing import Process
import time

from DARTS_Environment import load_environment

def time_ms() -> int:
    return int(time.time() * 1000)

class DARTS_Process(Process):
    def __init__(self, function, period_ms:int, name:str=None, args=(), kwargs={}):
        super().__init__(target=self._loop, name=name, args=args, kwargs=kwargs)

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

    def _loop(self, *args, **kwargs):
        load_environment()
        __main__.DARTS_Database = args[0]
        for key in kwargs:
            setattr(__main__, key, kwargs[key])

        while self._runnable:
            
            loop_time = time_ms()

            if self._enabled:
                self._function()
            
            time.sleep(self._period_ms / 1000 + time_ms() - loop_time)