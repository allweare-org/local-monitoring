from pysolarmanv5 import PySolarmanV5
from data_source import DataSource

class RealSolarmanSource(DataSource):
    def __init__(self, ip, serial):
        self.client = PySolarmanV5(ip, serial)

    def read(self):
        return self.client.read_holding_registers_dict()