
import requests, json, time
from dateutil import parser
from datetime import datetime

base_url="https://api.eu1.astarte.cloud/appengine/v1/tester/devices/5y1wzoO0Tiic7f7wP2Mzig/interfaces/ai.clea.examples.vendingMachine.AdvertisementDetails"
appengine_token="Bearer "

def publish_adv(p, data):
    print (p)
    for idx in data:

        print("\n\n")
        d=data[idx]
        print (f"{idx} -> {d}")
        resp = requests.post(f'{base_url}/{p}/{idx}', json={'data':d}, headers={"Content-Type":"application/json;charset=UTF-8",
                                                                                "Authorization":appengine_token})
        print (resp)


js  = json.load(open("/root/host_ws/edge-app/tests/advertisements.json"))


for p in js["data"]:
    publish_adv(p, js["data"][p])