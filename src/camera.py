import numpy as np
from pymem import Pymem
from pymem.exception import *
from pymem.memory import read_double,write_double,read_float,write_float
from utils.logger import log
from typing import List,Dict
import base64

class Var:
    def __init__(self, handle:int, address:int):
        self.handle = handle
        self.address = address

    def read(self):
        raise Exception("read not implemented!")

    def write(self, value):
        raise Exception("write not implemented!")

class DoubleVar(Var):
    def __init__(self, handle:int, address:int):
        Var.__init__(self, handle, address)
    
    def read(self):
        return read_double(self.handle, self.address)
    
    def write(self, value):
        write_double(self.handle, self.address, value)

class FloatVar(Var):
    def __init__(self, handle:int, address:int):
        Var.__init__(self, handle, address)
    
    def read(self):
        return read_float(self.handle, self.address)
    
    def write(self, value):
        write_float(self.handle, self.address, value)

class Injector:
    def __init__(self, process_name='FlightSimulator.exe'):
        self.pm = Pymem(process_name)
        log.debug("pid %d",self.pm.process_id)
        self.base_addr = []
        self.var_dict = {}
    
    def new(self, profile:Dict):
        self.base_addr = []
        self.var_dict = {}

        if 'patterns' in profile.keys():
            for pattern in profile['patterns']:
                addr = self.pm.pattern_scan_all(base64.b64decode(pattern))
                if type(addr) != int:
                    log.critical("addr not unique, check your pattern")
                    raise Exception()
                self.base_addr.append(addr)
        
        for variable in profile['variables']:
            addr = 0
            if 'pattern' in variable.keys():
                addr = self.base_addr[variable['pattern']]
            
            for i in range(len(variable['offsets'])-1):
                addr += variable['offsets'][i]
                addr = self.pm.read_longlong(addr)
            
            addr +=variable['offsets'][-1]

            match variable['type']:
                case 'double':
                    self.var_dict[variable['name']] = DoubleVar(self.pm.process_handle, addr)
                case 'float':
                    self.var_dict[variable['name']] = FloatVar(self.pm.process_handle, addr)


class Camera:
    def __init__(self) -> None:
        self.injector = Injector()

class ShowcaseCamera(Camera):
    def __init__(self) -> None:
        Camera.__init__(self)
        self.pos=np.array([])
        self.pos_target=np.array([])
        self.quat=np.array([])

    def __init__(self, profile:dict):
        Camera.__init__(self)
        self.injector.new(profile['showcase'])

    def init(self):
        pass

    def print_all(self):
        vars = dict()
        for (key, value) in self.injector.var_dict.items():
            print(key, value.read())
    
    def plus_one(self):
        for (key, value) in self.injector.var_dict.items():
            value.write(value.read()+1)