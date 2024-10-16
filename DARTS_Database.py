# DARTS_Database.py
# The database for the DARTS Application.

import __main__
from multiprocessing import current_process
from multiprocessing.managers import SyncManager, DictProxy, MakeProxyType

def _Database_Print(value:str) -> None:
    if __main__.DEBUG_DATABASE:
        print(f"Database: {value}")

default_address = ('localhost', 6000)
default_key = b'DARTS_Database_Key'

class Database(dict):
    
    def __init__(self, categories:list[str]) -> None:
        super().__init__({cat: __main__.Manager.DatabaseCategory() for cat in categories})

    def _immutable(self, *args, **kwargs) -> None:
        raise TypeError("Database keys are immutable")
    
    __setitem__ = _immutable
    __delitem__ = _immutable
    clear       = _immutable
    update      = _immutable
    setdefault  = _immutable
    pop         = _immutable
    popitem     = _immutable

DatabaseProxy = MakeProxyType("DatabaseProxy", 
                              ('__contains__', '__getitem__', '__iter__',  
                               '__len__', 'copy', 'get', 'items', 
                               'keys', 'values'))

class DatabaseCategory(dict):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        manager = DatabaseManager()
        manager.connect()

        self._locks = manager.dict()
        self._valid_keys = manager.list()
        self._key_data = manager.dict()

        self.DEBUG = bool("DEBUG" in kwargs and kwargs["DEBUG"])
    
    class DatabaseKeyData:

        def __init__(self, values:list[any]=None, range:list[any]=None, types:list[type]=None):
            if values and range:
                raise ValueError(f"Key cannot have both values and range constraints")
            
            with DatabaseManager() as manager:
                self.values = [values] if values else None
                self.range = [values] if range else None

                self.types = [values] if types else None

        def value_constrained(self) -> bool:
            return self.values is not None
        
        def range_constrained(self) -> bool:
            return self.range is not None
        
        def type_constrained(self) -> bool:
            return self.types is not None
        
        def validate(self, value:any) -> bool:
            retval = True
            if self.value_constrained():
                retval = value in self.values
            elif self.range_constrained():
                retval = self.range[0] <= value <= self.range[1]
            
            if retval and self.type_constrained():
                retval = type(value) in self.types
            
            return retval

    def __setitem__(self, key:str, value:any, timeout:float=0.1):
        _Database_Print(f"Setting {key} to {value}")

        if key not in self._valid_keys:
            raise KeyError(f"Invalid key: {key}")

        if not self._key_data[key].validate(value):
            raise ValueError(f"Invalid value: {value} for key: {key}")
        
        self._locks[key].acquire(timeout=timeout)

        if not self._locks[key].locked():
            raise TimeoutError(f"Failed to acquire lock for {key}")
        
        super().__setitem__(key, value)

        self._locks[key].release()
    
    def __getitem__(self, key, timeout:float=0.1) -> any:
        _Database_Print(f"Getting {key}")

        if key not in self._valid_keys:
            raise KeyError(f"Invalid key: {key}")
        
        self._locks[key].acquire(timeout=timeout)

        if not self._locks[key].locked():
            raise TimeoutError(f"Failed to acquire lock for {key}")
        
        retval = super().__getitem__(key)

        self._locks[key].release()        
        
        return retval
    
    def register(self, key:str, default:any=None, values:list[any]=None, range:list[any]=None, types:list[type]=any) -> None:
        if key in self._valid_keys:
            raise KeyError(f"Key already registered: {key}")
        
        _Database_Print(f"Registering {key}\n\tType: {types}\n\tDefault: {default}\n\tValues: {values}\n\tRange: {range}")

        self._locks[key] = __main__.Manager.Lock()
        
        self._locks[key].acquire()

        self._valid_keys.append(key)
        self._key_data[key] = self.DatabaseKeyData(values, range, types)

        if not self._key_data[key].validate(default):
            raise ValueError(f"Invalid default value: {default} for key: {key}")
        
        super().__setitem__(key, default)
        
        self._locks[key].release()

DatabaseCategoryProxy = MakeProxyType("DatabaseCategoryProxy", 
                                      ('__contains__', '__delitem__', 
                                       '__getitem__', '__iter__', '__len__',
                                       '__setitem__', 'clear', 'copy', 'get', 
                                       'items', 'keys', 'pop', 'popitem', 
                                       'setdefault', 'update', 'values', 'register'))
class DatabaseManager(SyncManager):

    def __init__(self, **kwargs):
        if 'address' not in kwargs:
            kwargs['address'] = default_address
        
        if 'authkey' not in kwargs:
            kwargs['authkey'] = default_key

        current_process().authkey = kwargs['authkey']
        
        super().__init__(**kwargs)

        self.register("Database", Database, DatabaseProxy)
        self.register("DatabaseCategory", DatabaseCategory, DatabaseCategoryProxy)