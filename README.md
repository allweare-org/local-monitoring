# local-monitoring

Production-grade edge IoT system for Solarman V5 inverter monitoring on Raspberry Pi.

## System Architecture

```text
                ┌────────────────────────┐
                │   Solarman V5 Logger   │
                └──────────┬─────────────┘
                           │ Ethernet
                           ▼
                ┌────────────────────────┐
                │  Raspberry Pi 3B+      │
                │  (Edge Agent Node)     │
                └──────────┬─────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        ▼                  ▼                  ▼
 config.yaml        Data Source        systemd service
 (deployment)       (mock/real)        (auto-start)
                           │
                           ▼
                ┌────────────────────────┐
                │   SQLite Database      │
                │   inverter.db          │
                └──────────┬─────────────┘
                           │
            ┌──────────────┴──────────────┐
            ▼                             ▼
     USB Export Tool             Future Cloud Sync
```

## Quick Start

### 1. Clone & Install

```bash
git clone https://github.com/allweare-org/local-monitoring.git
cd local-monitoring/scripts
bash install.sh
```

### 2. Enable Auto-Start

```bash
sudo cp systemd/inverter.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable inverter
sudo systemctl start inverter
```

### 3. Verify

```bash
sudo systemctl status inverter
```

## Configuration

Edit `client/config.yaml` to switch between mock and real mode:

```yaml
mode: mock   # mock | real

logger:
  poll_interval: 60

solarman:
  ip: 192.168.1.20
  serial: 1234567890

storage:
  db_path: inverter.db

export:
  usb_path: /media/usb
```

## Project Structure

```text
local-monitoring/
  client/
    main.py              # Entry point
    config.yaml          # Deployment config
    config.py            # Config loader
    sources/
      base.py            # DataSource ABC
      mock.py            # Mock data source
      solarman.py        # Real Solarman V5 source
    storage/
      sqlite_db.py       # SQLite storage layer
    services/
      logger.py          # Core logging loop
      exporter.py        # USB export module
    logs/
  scripts/
    install.sh           # One-command Pi installer
    start.sh             # Start service
    stop.sh              # Stop service
  systemd/
    inverter.service     # systemd unit file
  requirements.txt
```

## USB Data Export

Plug in a USB drive and run:

```python
from services.exporter import export_db
export_db("inverter.db", "/media/usb")
```

## Runtime Behavior

When the Pi powers on:

1. systemd starts the inverter service
2. `main.py` loads `config.yaml`
3. Selects data source (mock or solarman)
4. Starts infinite logger loop
5. Writes to SQLite every interval
6. Keeps running indefinitely

## Fault Tolerance

| Failure | System Response |
| --- | --- |
| Inverter disconnects | Retry loop with 5s backoff |
| Pi reboots | Auto restart via systemd |
| Power loss | SQLite survives (durable storage) |
| SSH closed | Service continues in background |

## Design Principles

- **Offline-first** — no internet required
- **Failure-tolerant** — retries + auto restart
- **Config-driven** — no code edits in field
- **Swappable sources** — mock ↔ real via config
- **Durable storage** — SQLite, not CSV
- **Auto-start on boot** — systemd managed
