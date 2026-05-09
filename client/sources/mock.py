import random
from sources.base import DataSource

class MockSource(DataSource):
    def read(self):
        return {
            "voltage": round(220 + random.random() * 10, 2),
            "current": round(4 + random.random() * 2, 2),
            "power": round(1000 + random.random() * 200, 2)
        }
