# DARTS_Database.py
# The database for the DARTS Application.

import __main__
from multiprocessing import current_process, Lock, get_context
from multiprocessing.managers import SyncManager, DictProxy, MakeProxyType

from DARTS_Environment import load_environment

DARTS_Environment = __main__.Environment if "Environment" in __main__.__dict__ else load_environment({})

def _Database_Print(value:str) -> None:
    from DARTS_Utilities import Debug_Print
    Debug_Print(__file__, value, (DARTS_Environment if DARTS_Environment else __main__.Environment)["DEBUG_DATABASE"])

def Database_Initialize(Environment:dict) -> None:
    global DARTS_Environment
    DARTS_Environment = Environment

default_address = ('localhost', DARTS_Environment["DATABASE_PORT"])
default_key = DARTS_Environment["DATABASE_KEY"]

class DatabaseCategory(dict):

    def __init__(self, **kwargs):
        _Database_Print(f"Creating new Database Category")
        super().__init__(**kwargs)

        _Database_Print(f"Creating Database Category Locks Dictionary")
        self._locks = {}

        _Database_Print(f"Creating Database Category Keys List")
        self._valid_keys = []

        _Database_Print(f"Creating Database Category Key Data Dictionary")
        self._key_data = {}

        self.DEBUG = bool("DEBUG" in kwargs and kwargs["DEBUG"])
    
    class DatabaseKeyData:

        def __init__(self, values:list[any]=None, range:list[any]=None, types:list[type]=None):
            _Database_Print(f"Creating Database Key Data\n\tValues: {values}\n\tRange: {range}\n\tTypes: {types}")

            if values and range:
                raise ValueError(f"Key cannot have both values and range constraints")
            
            _Database_Print(f"Setting Database Key Data Constraints")
            self.values = values if values else None
            self.range = range if range else None
            self.types = types if types else None

        def value_constrained(self) -> bool:
            return self.values is not None
        
        def range_constrained(self) -> bool:
            return self.range is not None
        
        def type_constrained(self) -> bool:
            return self.types is not None and self.types is not any
        
        def validate(self, value:any) -> bool:
            retval = True
            if self.value_constrained():
                _Database_Print(f"Validating value: {value} in set {self.values}")
                retval = value in self.values
            elif self.range_constrained():
                _Database_Print(f"Validating value: {value} in range {self.range}")
                retval = self.range[0] <= value <= self.range[1]
            
            if retval and self.type_constrained():
                _Database_Print(f"Validating type: {type(value)} in {self.types}")
                retval = type(value) in self.types
            
            _Database_Print(f"Validation result: {retval}")
            return retval

    def __setitem__(self, key:str, value:any, timeout:float=DARTS_Environment["DATABASE_LOCK_TIMEOUT"]) -> None:
        _Database_Print(f"Setting {key} to {value}")

        if key not in self._valid_keys:
            raise KeyError(f"Invalid key: {key}")

        if not self._key_data[key].validate(value):
            raise ValueError(f"Invalid value: {value} for key: {key}")
        
        if not self._locks[key].acquire(timeout=timeout):
            raise TimeoutError(f"Failed to acquire lock for {key}")
        
        super().__setitem__(key, value)

        self._locks[key].release()
    
    def __getitem__(self, key, timeout:float=DARTS_Environment["DATABASE_LOCK_TIMEOUT"]) -> any:
        _Database_Print(f"Getting value of {key}")

        if key not in self._valid_keys:
            raise KeyError(f"Invalid key: {key}")

        if not self._locks[key].acquire(timeout=timeout):
            raise TimeoutError(f"Failed to acquire lock for {key}")
        
        retval = super().__getitem__(key)

        self._locks[key].release() 
        
        return retval
    
    def register(self, key:str, default:any=None, values:list[any]=None, range:list[any]=None, types:list[type]=None) -> None:
        _Database_Print(f"Registering {key}\n\tType: {types}\n\tDefault: {default}\n\tValues: {values}\n\tRange: {range}")
        
        if key in self._valid_keys:
            raise KeyError(f"Key already registered: {key}")

        _Database_Print(f"Creating lock for {key}")
        self._locks[key] = Lock()
        
        _Database_Print(f"Acquiring lock for {key}")
        if not self._locks[key].acquire():
            raise PermissionError(f"Failed to acquire lock for {key}")

        _Database_Print(f"Creating key data for {key}")
        self._valid_keys.append(key)
        self._key_data[key] = self.DatabaseKeyData(values, range, types)

        _Database_Print(f"Validating default data for {key}")
        if not self._key_data[key].validate(default):
            raise ValueError(f"Invalid default value: {default} for key: {key}")
        
        _Database_Print(f"Setting default value for {key}")
        super().__setitem__(key, default)
        
        _Database_Print(f"Releasing lock for {key}")
        self._locks[key].release()

class DatabaseCategoryProxy(DictProxy):
    _exposed_ = ('__contains__', '__delitem__', 
                 '__getitem__', '__iter__', '__len__',
                 '__setitem__', 'clear', 'copy', 'get', 
                 'items', 'keys', 'pop', 'popitem', 
                 'setdefault', 'update', 'values', 'register')
    
    def register(self, key:str, default:any=None, values:list[any]=None, range:list[any]=None, types:list[type]=None) -> None:
        return self._callmethod('register', (key, default, values, range, types,))
    

class Database(dict):
    
    def __init__(self, categories: dict=None) -> None:

        _Database_Print(f"Creating new database with categories: {categories.keys() if categories else None}")

        _Database_Print("Attaching database categories")
        super().__init__(categories if categories else {})
        _Database_Print("Database categories attached")
    
    def attach(self, name: str, CategoryProxy:DatabaseCategoryProxy) -> None:
        _Database_Print(f"Attaching category {CategoryProxy}")

        if name in self:
            raise KeyError(f"Category already attached: {name}")
        
        super().__setitem__(name, CategoryProxy)

    def _immutable(self, *args, **kwargs) -> None:
        raise TypeError("Database keys are immutable")
    
    __setitem__ = _immutable
    __delitem__ = _immutable
    clear       = _immutable
    update      = _immutable
    setdefault  = _immutable
    pop         = _immutable
    popitem     = _immutable

class DatabaseProxy(DictProxy): 
    _exposed_ = ('__contains__', '__getitem__', '__iter__',  
                 '__len__', 'copy', 'get', 'items', 
                 'keys', 'values', 'attach')
    
    def attach(self, name: str, CategoryProxy:DatabaseCategoryProxy) -> None:
        return self._callmethod('attach', (name, CategoryProxy,))

    def _immutable(self, *args, **kwargs) -> None:
        raise TypeError("Database keys are immutable")
    
    __setitem__ = _immutable
    __delitem__ = _immutable
    clear       = _immutable
    update      = _immutable
    setdefault  = _immutable
    pop         = _immutable
    popitem     = _immutable

class DatabaseManager(SyncManager):

    def __init__(self, **kwargs):
        if 'address' not in kwargs:
            kwargs['address'] = default_address
        
        if 'authkey' not in kwargs:
            kwargs['authkey'] = default_key

        current_process().authkey = kwargs['authkey']
        
        super().__init__(**kwargs)

DatabaseManager.register("DatabaseCategory", DatabaseCategory, DatabaseCategoryProxy)
DatabaseManager.register("Database", Database, DatabaseProxy)