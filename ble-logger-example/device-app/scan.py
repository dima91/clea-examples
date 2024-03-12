import signal
import argparse
import logging
from src.configs import get as get_configs, setup_astarte
from src.Loop import Loop
from src.engine import Engine


class ProgramKilled(Exception):
    pass


def signal_handler(signum, frame):
    logging.getLogger(__name__).info("Shutting Down...")
    raise ProgramKilled


def main():
    cfg = get_configs()
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)

    device_id = cfg.get("device_id", "")
    realm = cfg.get("realm", "")
    credentials_secret = cfg.get("credentials_secret", "")
    pairing_base_url = cfg.get("pairing_base_url", "")
    interaction_min_time = int(cfg["interaction_min_time_sec"])
    interaction_min_rssi = int(cfg["interaction_min_rssi"])

    engine = Engine(
        device_id=device_id,
        realm=realm,
        credentials_secret=credentials_secret,
        pairing_base_url=pairing_base_url,
        interaction_min_time=interaction_min_time,
        interaction_min_rssi=interaction_min_rssi,
    )
    job = Loop(
        cfg.get("wait_time_seconds", 0),
        engine.main_loop,
        cfg.get("discovery_time_sec", 2),
    )
    try:
        job.start()
    except ProgramKilled:
        job.stop()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="BLE Scanner")
    parser.add_argument("-v", "--version", action="version", version="%(prog)s 0.1b")
    parser.add_argument("-c", "--config", action="store_true", help="Configure Astarte")
    args = parser.parse_args()
    if args.config:
        setup_astarte()
    else:
        main()
