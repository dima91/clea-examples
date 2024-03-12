import os
import json
import csv
import sys
import logging
import bleak
from os import listdir
from os.path import isfile, join
from pathlib import Path
from datetime import datetime, timezone
from .statistics import Statistics

from astarte.device import DeviceMqtt
from bleak import BleakScanner

_ROOT_DIR = Path(__file__).parent.parent.absolute()
_INTERFACES_DIR = os.path.join(Path(__file__).parent.parent.absolute(), "interfaces")


def _load_interfaces() -> [dict]:
    files = [
        join(_INTERFACES_DIR, f)
        for f in listdir(_INTERFACES_DIR)
        if isfile(join(_INTERFACES_DIR, f))
    ]
    interfaces = []
    for file in files:
        with open(file, "r") as interface_file:
            interfaces.append(json.load(interface_file))
    return interfaces


class Engine:
    def __init__(
        self,
        device_id,
        realm,
        credentials_secret,
        pairing_base_url,
        interaction_min_time,
        interaction_min_rssi,
    ):

        # Setting up 'Logger' object
        logging.basicConfig()
        self.my_logger = logging.getLogger(__name__)
        self.my_logger.setLevel(logging.DEBUG)

        self.device = DeviceMqtt(
            device_id=device_id,
            realm=realm,
            credentials_secret=credentials_secret,
            pairing_base_url=pairing_base_url,
            persistency_dir=str(_ROOT_DIR),
        )
        self.device.add_interfaces_from_dir(_INTERFACES_DIR)
        self.device.connect()
        self.ASTARTE_MAX_STRING_LENGTH = 65536

        # Creating ble_companies dictionary
        self.ble_companies = {}
        companies_file = open("data/company_identifiers.csv", encoding="utf-8")
        csv_reader = csv.reader(companies_file)
        # skipping first row
        next(csv_reader)
        for row in csv_reader:
            id = int(row[0])
            self.ble_companies[id] = {"dec_id": id, "hex_id": row[1], "name": row[2]}

        self.last_detection_time = datetime.now(timezone.utc)
        # Zeroing seconds
        self.last_sent_minute = self.last_detection_time.replace(
            second=0, microsecond=0
        )
        # Zeroing minutes
        self.last_sent_hourly = self.last_sent_minute.replace(minute=0)
        # Zeroing hours
        self.last_sent_daily = self.last_sent_hourly.replace(hour=0)

        self.my_logger.info(
            "Initial times:\n\tminute : {}\n\thours: {}\n\tday: {}".format(
                self.last_sent_minute, self.last_sent_hourly, self.last_sent_daily
            )
        )

        # Creating "Statistics" object
        self.statistics_cache = Statistics(interaction_min_time, interaction_min_rssi)

    def parse_device(self, dev):
        p_dev = {"address": dev.address, "rssi": dev.rssi, "name": dev.name}

        if "ManufacturerData" in dev.details["props"]:
            p_dev["manufacturerData"] = {}
            for key in dev.details["props"]["ManufacturerData"]:
                p_dev["manufacturerData"][key] = dev.details["props"][
                    "ManufacturerData"
                ][key].hex()
        else:
            p_dev["manufacturerData"] = None
        if p_dev["manufacturerData"] and len(p_dev["manufacturerData"].keys()) == 1:
            company_id = None
            try:
                # Searching for company identifier
                company_id = int(*p_dev["manufacturerData"])
                p_dev["vendor"] = self.ble_companies[company_id]["name"]
            except Exception:
                self.my_logger.warning(
                    "Cannot retrieve, for device {}, manufacturer company with key {}".format(
                        dev.address, company_id
                    )
                )
                p_dev["vendor"] = ""
        else:
            error_msg = ""
            if p_dev["manufacturerData"] is None:
                error_msg = "Cannot determine manufacturer data for device {}: manufacturer is None".format(
                    dev.address
                )
            else:
                error_msg = "Cannot determine manufacturer data for device {}: manufacturer array has length {}".format(
                    dev.address, len(p_dev["manufacturerData"].keys())
                )

            self.my_logger.error(error_msg)
            p_dev["vendor"] = ""

        if "AddressType" in dev.details["props"]:
            p_dev["address_type"] = dev.details["props"]["AddressType"]
        else:
            p_dev["address_type"] = None

        if "UUIDs" in dev.details["props"]:
            p_dev["UUIDs"] = []
            for item in dev.details["props"]["UUIDs"]:
                p_dev["UUIDs"].append(item)
        else:
            p_dev["UUIDs"] = None

        return p_dev

    # Periodic function executed by an async loop
    async def main_loop(self, discovery_time):
        sys.stdout.flush()
        curr_detection_time = datetime.now(timezone.utc)
        try:
            nearby_devices = await BleakScanner.discover(timeout=discovery_time)

            now = datetime.now(timezone.utc)

            # Checking if minute statistics has to be sent
            if (now - self.last_sent_minute).seconds >= 60:
                timestamp = self.last_sent_minute.replace(second=59)
                # Getting cached minute data and sending it
                payload = self.statistics_cache.get_and_clear_minute_payload()
                string_payload = json.dumps(payload)
                if len(string_payload) > self.ASTARTE_MAX_STRING_LENGTH:
                    self.my_logger.error(
                        "Cannot send payload: Its length {} is greater than {}!\n{}".format(
                            len(string_payload), self.ASTARTE_MAX_STRING_LENGTH, payload
                        )
                    )
                else:
                    self.device.send_aggregate(
                        "ai.clea.examples.blelogger.MinuteStats", "/statistics", payload, timestamp
                    )

                self.last_sent_minute = now.replace(second=0, microsecond=0)

            # Checking if hourly statistics has to be sent
            if ((now - self.last_sent_hourly).seconds // 60) >= 60:
                self.my_logger.debug(
                    "Hourly diff: (now - self.last_sent_hourly).seconds//60 = ({} - {}).seconds//60 = {}".format(
                        now,
                        self.last_sent_hourly,
                        (now - self.last_sent_hourly).seconds // 60,
                    )
                )
                timestamp = self.last_sent_hourly.replace(second=59, minute=59)
                # Getting cached hourly data and sending it
                payload = self.statistics_cache.get_and_clear_hourly_payload()
                string_payload = json.dumps(payload)
                if len(string_payload) > self.ASTARTE_MAX_STRING_LENGTH:
                    self.my_logger.error(
                        "Cannot send payload: Its length {} is greater than {}!\n{}".format(
                            len(string_payload), self.ASTARTE_MAX_STRING_LENGTH, payload
                        )
                    )
                else:
                    self.device.send_aggregate(
                        "ai.clea.examples.blelogger.HourlyStats", "/statistics", payload, timestamp
                    )

                self.last_sent_hourly = now.replace(minute=0, second=0, microsecond=0)
                self.my_logger.debug(
                    "New last_sent_hourly {}.\tTimestamp was {} ({})".format(
                        self.last_sent_hourly, timestamp.timestamp(), timestamp
                    )
                )

            # Checking if daily statistics has to be sent
            if (now - self.last_sent_daily).days > 0:
                self.my_logger.debug(
                    "Daily diff: (now - self.last_sent_daily).days = ({} - {}).days = {}".format(
                        now, self.last_sent_daily, (now - self.last_sent_daily).days
                    )
                )
                timestamp = self.last_sent_daily.replace(hour=23, minute=59, second=59)
                # Getting cached daily data and sending it
                payload = self.statistics_cache.get_and_clear_daily_payload()
                string_payload = json.dumps(payload)
                if len(string_payload) > self.ASTARTE_MAX_STRING_LENGTH:
                    self.my_logger.error(
                        "Cannot send payload: Its length {} is greater than {}!\n{}".format(
                            len(string_payload), self.ASTARTE_MAX_STRING_LENGTH, payload
                        )
                    )
                else:
                    self.device.send_aggregate(
                        "ai.clea.examples.blelogger.DailyStats", "/statistics", payload, timestamp
                    )

                self.last_sent_daily = now.replace(
                    hour=0, minute=0, second=0, microsecond=0
                )
                self.my_logger.debug(
                    "New last_sent_daily {}.\tTimestamp was {} ({})".format(
                        self.last_sent_daily, timestamp.timestamp(), timestamp
                    )
                )

            # Updating local cache
            for dev in nearby_devices:
                self.statistics_cache.update(
                    self.parse_device(dev),
                    curr_detection_time,
                    self.last_detection_time,
                )

        except bleak.exc.BleakDBusError as be:
            self.my_logger.warning("Caught this bleak exception: {}".format(be))
        except Exception as e:
            self.my_logger.warning("Caught this exception: {}".format(e))

        self.last_detection_time = curr_detection_time
