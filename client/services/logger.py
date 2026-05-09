import time

class LoggerService:
    def __init__(self, source, db, interval):
        self.source = source
        self.db = db
        self.interval = interval

    def run(self):
        while True:
            try:
                data = self.source.read()

                if data:
                    self.db.insert(data)
                    print("Logged:", data)

            except Exception as e:
                print("Error:", e)
                time.sleep(5)
                continue

            time.sleep(self.interval)
