from config import load_config
from sources.mock import MockSource
from sources.solarman import SolarmanSource
from storage.sqlite_db import Database
from services.logger import LoggerService

def main():
    config = load_config()

    if config["mode"] == "mock":
        source = MockSource()
    else:
        source = SolarmanSource(
            config["solarman"]["ip"],
            config["solarman"]["serial"]
        )

    db = Database(config["storage"]["db_path"])

    logger = LoggerService(
        source,
        db,
        config["logger"]["poll_interval"]
    )

    logger.run()

if __name__ == "__main__":
    main()
