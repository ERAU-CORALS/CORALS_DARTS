# DARTS_Database.py
# The database for the DARTS Application.

import __main__
from threading import Lock

def _Database_Print(value:str) -> None:
    if __main__.DEBUG_DATABASE:
        print(f"Database: {value}")

class Database(dict):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._valid_keys = []
        self._valid_values = {}
        self._valid_ranges = {}
        self._valid_value_types = {}
        self._locks = {}
        self.DEBUG = bool("DEBUG" in kwargs and kwargs["DEBUG"])

    def __setitem__(self, key:str, value:any, timeout:float=0.1) -> bool:
        if not self._validate(key, value):
            raise ValueError(f"Invalid value: {value} for key: {key}")
        
        self._locks[key].acquire(timeout=timeout)

        if self._locks[key].locked():
            _Database_Print(f"Setting {key} to {value}")
        
            super().__setitem__(key, value)

            self._locks[key].release()

            return True 
        
        else:
            _Database_Print(f"Failed to acquire lock for {key}")
        
        return False
    
    def __getitem__(self, key, timeout:float=0.1) -> any:
        _Database_Print(f"Getting {key}")
        retval = None

        _Database_Print(f"Acquiring Lock for {key}")
        self._locks[key].acquire(timeout=timeout)
        _Database_Print(f"Acquiring Lock for {key}")

        if self._locks[key].locked():
            _Database_Print(f"Getting {key}")
            
            if key not in self._valid_keys:
                raise KeyError(f"Invalid key: {key}")
            
            retval = super().__getitem__(key)

            self._locks[key].release()
        else:
            _Database_Print(f"Failed to acquire lock for {key}")

        return retval
    
    def register(self, key:str, types:type, default:any=None, values:list[any]=None, range:list[any]=None) -> None:
        if key in self._valid_keys:
            raise KeyError(f"Key already registered: {key}")
        
        if values and range:
            raise ValueError(f"Key {key} cannot have both values and range constraints")
        
        _Database_Print(f"Registering {key}\n\tType: {types}\n\tDefault: {default}\n\tValues: {values}\n\tRange: {range}")

        self._valid_keys.append(key)
        self._valid_value_types[key] = types
        super().__setitem__(key, default)
        self._locks[key] = Lock()
        self._locks[key].acquire()
        
        if values is not None:
            self._valid_values[key] = values
        elif range is not None:
            self._valid_ranges[key] = range
        
        self._locks[key].release()

    def _validate(self, key:str, value:any) -> bool:
        _Database_Print(f"Validating {key} with value {value}")

        if key not in super().keys():
            _Database_Print(f"Key {key} not registered")
            return False
        if key in self._valid_values.keys():
            _Database_Print(f"Validating {key} with values {self._valid_values[key]}: {value in self._valid_values[key]}")
            return value in self._valid_values[key]
        elif key in self._valid_ranges.keys():
            _Database_Print(f"Validating {key} with range {self._valid_ranges[key]}")
            return self._valid_ranges[key][0] <= value <= self._valid_ranges[key][1]
        
        return True