"""Makes a single request to the cpu api."""

import requests

resp = requests.post(
    "http://127.0.0.1:8000/testapi/v1/ram/get_available",
    headers={
        'Content-Type': "application/json",
        'User-Agent': "wiremq-demo-application",
        'Accept': "application/json"
    },
    data={
        "hello": "world",
        "one": 1,
        "two": "two"
    },
    timeout=15
)

print(resp)
print(resp.json())
