# DARTS_Database.py
# The database for the DARTS Application.

class DARTS_Database(dict):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.valid_keys = []
        self.valid_values = {}
        self.DEBUG = "DEBUG" in kwargs and kwargs["DEBUG"]

    def __setitem__(self, key:str, value:any) -> None:
        if key not in self.valid_keys:
            raise KeyError(f"Invalid key: {key}")
        if not self._validate(key, value):
            raise ValueError(f"Invalid value: {value} for key: {key}")
        print(f"Setting {key} to {value}")
        super().__setitem__(key, value)
    
    def __getitem__(self, key) -> any:
        if key not in self.valid_keys:
            raise KeyError(f"Invalid key: {key}")
        return super().__getitem__(key)
    
    def register(self, key:str, default:any=None, values:any=None) -> None:
        if key in self.valid_keys:
            raise KeyError(f"Key already registered: {key}")
        self.valid_keys.append(key)
        if values:
            self.valid_values[key] = values
        self[key] = default

    def _validate(self, key:str, value:any) -> bool:
        if key in self.valid_values:
            return value in self.valid_values[key]
        return True