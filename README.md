# local-monitoring

Local monitoring system for Deye solar inverters that cannot upload data to the Deye cloud due to Wi-Fi/internet access issues. A Raspberry Pi on the local network polls the Solarman logger attached to the inverter and records data to CSV.

## How It Works

1. The Solarman Wi-Fi logger is connected to the Deye inverter and exposes Modbus TCP on port **8899**
2. A Raspberry Pi on the same local network polls the logger every 60 seconds using [`pysolarmanv5`](https://github.com/jmccrohan/pysolarmanv5)
3. Inverter register data (battery SOC, power output, grid voltage, etc.) is timestamped and appended to a local CSV file

## Project Structure

```text
client/
├── find_logger.py    # Network scanner to discover the Solarman logger IP on your LAN
├── logger.py         # Main data logger — connects to a real inverter and logs to CSV
└── logger_test.py    # Simulation — generates fake inverter data for testing without hardware
```

## Setup

### 1. Find Your Logger

Run the network scanner to discover the Solarman logger on your local network:

```bash
python client/find_logger.py
```

This scans the subnet (default `192.168.1.0/24`) for devices with port 8899 open.

### 2. Configure

Edit `client/logger.py` and set:

- `LOGGER_IP` — the IP address found in step 1
- `SERIAL_NUMBER` — the serial number of your Solarman logger / inverter
- `POLL_INTERVAL` — polling frequency in seconds (default: 60)

### 3. Run

**With a real inverter:**

```bash
pip install pysolarmanv5
python client/logger.py
```

**Without hardware (simulation mode):**

```bash
python client/logger_test.py
```

This generates random values for battery SOC, inverter power, and grid voltage — useful for testing the CSV pipeline.

## Output

Data is logged to `inverter_log.csv` in the `client/` directory with timestamped rows:

```csv
timestamp,battery_soc,grid_voltage,inverter_power
2026-04-21 10:30:00,85,230,1500
```

## Dependencies

- Python 3
- [`pysolarmanv5`](https://github.com/jmccrohan/pysolarmanv5) (only needed for real logger connection)
