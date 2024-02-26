import requests, json, sys

BASE_URL = "https://api.spaceshipinvest.com.au/v0/external/query"

def post(payload, headers=None):
    if headers is None:
        response = requests.post(url=BASE_URL, json=payload)
    else:
        response = requests.post(url=BASE_URL, json=payload, headers=headers)
    handle_response(payload, response)
    return response.json()

def handle_response(payload, response):
    if response.status_code != 200:
        print(json.dumps(payload)[:1000])
        print("Request failed with status code:", response.status_code)
        print("Response:", response.text)
        sys.exit(1)