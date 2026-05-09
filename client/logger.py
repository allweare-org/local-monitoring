import csv
import os
import time
from datetime import datetime

from mock_source import MockSource
from solarman_source import RealSolarmanSource

CSV_FILE = "inverter_log.csv"
POLL_INTERVAL = 60

# 🔥 SWITCH HERE
USE_MOCK = True


def log_to_csv(data):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    keys = sorted(data.keys())
    row = [timestamp] + [data.get(k, "") for k in keys]

    with open(CSV_FILE, "a", newline="") as f:
        writer = csv.writer(f)

        # write header only if file is empty
        if f.tell() == 0:
            writer.writerow(["timestamp"] + keys)

        writer.writerow(row)


def main():
    if USE_MOCK:
        source = MockSource()
        print("Using MOCK source")
    else:
        source = RealSolarmanSource("192.168.1.20", 1234567890)
        print("Using REAL Solarman source")

    while True:
        try:
            # 1. Read data safely
            data = source.read()

            # 2. Validate data exists
            if not data:
                print("Warning: empty data received")
                continue

            # 3. Log to CSV safely
            try:
                log_to_csv(data)
                with open("heartbeat.txt", "w") as f:
                    f.write(str(time.time()))
                print("OK:", data)

            except Exception as e:
                print("CSV write failed:", e)

            # 4. Print heartbeat
            print("OK:", data)

        except Exception as e:
            print("Sensor read error:", e)

            # IMPORTANT: prevents infinite crash loop
            time.sleep(5)
            continue

        # normal polling delay
        time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    main()