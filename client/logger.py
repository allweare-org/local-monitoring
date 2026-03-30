import csv
import time
from datetime import datetime
from pysolarmanv5 import SolarmanV5

# -----------------------------
# CONFIG
# -----------------------------
LOGGER_IP = "192.168.1.20"      # Change this on-site
SERIAL_NUMBER = 1234567890      # Change this (from inverter/logger)
CSV_FILE = "inverter_log.csv"
POLL_INTERVAL = 60              # seconds

def log_to_csv(data):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    keys = sorted(data.keys())
    row = [timestamp] + [data.get(k, "") for k in keys]

    # Create file with header if it doesn't exist
    try:
        with open(CSV_FILE, "r"):
            pass
    except FileNotFoundError:
        with open(CSV_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["timestamp"] + keys)

    # Append row
    with open(CSV_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(row)

    print(f"{timestamp} | Logged data")

# -----------------------------
# MAIN LOOP
# -----------------------------
def main():
    print("Starting Deye CSV logger...")

    modbus = SolarmanV5(LOGGER_IP, SERIAL_NUMBER)

    while True:
        try:
            data = modbus.read_holding_registers_dict()
            log_to_csv(data)
        except Exception as e:
            print(f"Error: {e}")

        time.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    main()