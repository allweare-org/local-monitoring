from pysolarmanv5 import PySolarmanV5
from sources.base import DataSource

class SolarmanSource(DataSource):
    def __init__(self, ip, serial):
        self.client = PySolarmanV5(ip, serial)

    def read(self):
        return self.client.read_holding_registers_dict()
