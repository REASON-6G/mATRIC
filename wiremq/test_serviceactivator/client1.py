"""Makes a single request to the cpu api."""

import requests

resp = requests.get(
    "http://127.0.0.1:8000/testapi/v1/cpu/get_percent",
    headers={
        'Content-Type': "application/json",
        'User-Agent': "wiremq-demo-application",
        'Accept': "application/json"
    },
    params={
        "data": "hello",
        "aux": "world"
    },
    timeout=15
)

print(resp)
print(resp.json())
