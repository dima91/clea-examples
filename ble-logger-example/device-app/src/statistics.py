import json
import logging
from multiprocessing.spawn import prepare
import time


def prepare_payload_for_device_type(
    devices_cache, detected_devices_cache, vendors_dict, interactions_array
):
    for i in devices_cache:
        item = devices_cache[i]
        item_addres = item["device"]["address"]

        # Detections
        detected_devices_cache.append(item_addres)
        # Vendors
        vendor = item["device"]["vendor"]
        if vendor == "":
            vendors_dict["Unknown"].append(item_addres)
        else:
            if vendors_dict.get(vendor) is None:
                vendors_dict[vendor] = []
            vendors_dict[vendor].append(item_addres)
        # Interactions
        if interactions_array is not None and item["has_interacted"]:
            interactions_array.append(item["presence_time"])


def prepare_astarte_payload(source_cache):
    payload = {
        "detectedSmartphones": [],
        "detectedAccessories": [],
        "interactions": [],
        "smartphonesVendors": "",
        "accessoriesVendors": "",
    }
    smartphones_vendors = {"Unknown": []}
    accessories_vendors = {"Unknown": []}

    # Analyzing smartphones cache
    prepare_payload_for_device_type(
        source_cache["smartphones"],
        payload["detectedSmartphones"],
        smartphones_vendors,
        payload["interactions"],
    )

    # Analyzing accessories cache
    prepare_payload_for_device_type(
        source_cache["accessories"],
        payload["detectedAccessories"],
        accessories_vendors,
        None,
    )

    source_cache["smartphones"].clear()
    source_cache["accessories"].clear()

    payload["smartphonesVendors"] = json.dumps(smartphones_vendors)
    payload["accessoriesVendors"] = json.dumps(accessories_vendors)

    return payload


class Statistics:
    def __init__(self, interaction_min_time, interaction_min_rssi) -> None:
        """Each item in following contains following fields:
        device
        presence_time
        has_interacted
        #rssi_summation
        #rssi_count
        """
        self.minute_data = {"smartphones": {}, "accessories": {}}
        self.hourly_data = {"smartphones": {}, "accessories": {}}
        self.daily_data = {"smartphones": {}, "accessories": {}}

        self.interaction_min_time = interaction_min_time
        self.interaction_min_rssi = interaction_min_rssi
        self.last_detection_time = int(time.time())

    def update_local_cache(
        self, dev, cache_dict, curr_detection_time, last_detection_time
    ):
        dev_id = dev["address"]

        # Creating current device if not present in local caches
        if cache_dict.get(dev_id) is None:
            # print ('Adding {} having address type {}'.format(dev_id, dev['address_type']))
            cache_dict[dev_id] = {
                "device": dev,
                "presence_time": 0,
                "has_interacted": False,
            }

        item = cache_dict[dev_id]

        # Augmenting presence_time IFF the rssi value is greater than or equal to interaction_min_rssi,
        #   zeroing it if rssi is lower than such value and it didn't have an interaction
        if dev["rssi"] >= self.interaction_min_rssi:
            item["presence_time"] += int(
                (curr_detection_time - last_detection_time).seconds
            )
        elif not item["has_interacted"]:
            item["presence_time"] = 0

        # Checking if current device has interacted
        if item["presence_time"] >= self.interaction_min_time:
            item["has_interacted"] = True

    # Updating local caches with incoming device
    def update(self, device, curr_time, last_detection_time):

        if device["address_type"] == "random":
            # Updating smartphones lists
            self.update_local_cache(
                device, self.minute_data["smartphones"], curr_time, last_detection_time
            )
            self.update_local_cache(
                device, self.hourly_data["smartphones"], curr_time, last_detection_time
            )
            self.update_local_cache(
                device, self.daily_data["smartphones"], curr_time, last_detection_time
            )
            pass

        elif device["address_type"] == "public":
            # Updating accessories lists
            self.update_local_cache(
                device, self.minute_data["accessories"], curr_time, last_detection_time
            )
            self.update_local_cache(
                device, self.hourly_data["accessories"], curr_time, last_detection_time
            )
            self.update_local_cache(
                device, self.daily_data["accessories"], curr_time, last_detection_time
            )
            pass

        else:
            logging.getLogger(__name__).error(
                "Unknown device type with MAC address {}".format(device["address"])
            )

    def get_and_clear_minute_payload(self):
        return prepare_astarte_payload(self.minute_data)

    def get_and_clear_hourly_payload(self):
        return prepare_astarte_payload(self.hourly_data)

    def get_and_clear_daily_payload(self):
        return prepare_astarte_payload(self.daily_data)
