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

    def __setitem__(self, key:str, value:any) -> bool:
        if not self._validate(key, value):
            raise ValueError(f"Invalid value: {value} for key: {key}")
        
        self._locks[key].acquire()

        with self._locks[key]:
            _Database_Print(f"Setting {key} to {value}")
        
            super().__setitem__(key, value)

            self._locks[key].release()

            return True
        
        return False
    
    def __getitem__(self, key) -> any:
        retval = None

        self._locks[key].acquire()

        with self._locks[key]:
            _Database_Print(f"Getting {key}")
            
            if key not in self._valid_keys:
                raise KeyError(f"Invalid key: {key}")
            
            retval = super().__getitem__(key)

            self._locks[key].release()

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
            return False
        if key in self._valid_values.keys():
            return value in self._valid_values[key]
        elif key in self._valid_ranges.keys():
            return self._valid_ranges[key][0] <= value <= self._valid_ranges[key][1]
        
        return True