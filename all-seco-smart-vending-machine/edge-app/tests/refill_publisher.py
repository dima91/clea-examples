
import requests, json

base_url="https://api.eu1.astarte.cloud/appengine/v1/tester/devices/5y1wzoO0Tiic7f7wP2Mzig/interfaces/ai.clea.examples.vendingMachine.RefillEvent"
appengine_token="Bearer "

def publish_product(p, data) :
    print (p)
    for idx in data:
        d=data[idx]
        print (f"{idx} -> {d}")
        resp = requests.post(f'{base_url}/{p}/{idx}', json={'data':d}, headers={"Content-Type":"application/json;charset=UTF-8",
                                                                                "Authorization":appengine_token})
        print (resp)


d={
    "refillerID":"abcdef",
    "note":"Nothing to note"
}
res = requests.post(f'{base_url}/refill', json={'data':d}, headers={"Content-Type":"application/json;charset=UTF-8", "Authorization":appengine_token})
print(res)
