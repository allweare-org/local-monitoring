import time
import random
from datetime import datetime
import csv

CSV_FILE = "inverter_log.csv"

def log_fake_data():
    data = {
        "battery_soc": random.randint(50, 100),
        "inverter_power": random.randint(500, 3000),
        "grid_voltage": random.randint(220, 240)
    }

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    keys = sorted(data.keys())
    row = [timestamp] + [data[k] for k in keys]

    try:
        with open(CSV_FILE, "r"):
            pass
    except FileNotFoundError:
        with open(CSV_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["timestamp"] + keys)

    with open(CSV_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(row)

    print(f"{timestamp} | Fake data logged")

while True:
    log_fake_data()
    time.sleep(60)