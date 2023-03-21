
import requests, json, time
from dateutil import parser
from datetime import datetime

base_url="https://api.demo.clea.cloud/appengine/v1/showcase/devices/rK9K_J3ATZeRJRxYo7GWWg/interfaces/ai.clea.examples.vendingMachine.PromoDetails"
appengine_token="Bearer "

def publish_promo(p, data):
    print (p)
    for idx in data:

        print("\n\n")
        d=data[idx]
        print (f"{idx} -> {d}")
        resp = requests.post(f'{base_url}/{p}/{idx}', json={'data':d}, headers={"Content-Type":"application/json;charset=UTF-8",
                                                                                "Authorization":appengine_token})
        print (resp)


js  = json.load(open("/root/host_ws/edge-app/tests/promos.json"))


for p in js["data"]:
    publish_promo(p, js["data"][p])