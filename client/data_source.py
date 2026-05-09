from abc import ABC, abstractmethod

class DataSource(ABC):
    @abstractmethod
    def read(self):
        """Return inverter data as a dictionary"""
        pass