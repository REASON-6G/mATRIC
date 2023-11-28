import json
import logging
import time
from wiremq.gateway.endpoints import endpointfactory

logger = logging.getLogger("bus3_logger")

with open("config.json", "r") as f:
    config = json.load(f)["bus3_config"]

dummy_msg = {
    "type": "event",
    "dest_ip": "127.0.0.1",
    "dest_port": 9001,
    "payload": {
        "from": "bus3",
        "hello": "world"
    }
}

bus3 = endpointfactory.EndpointFactory().build(config)
while True:
    msgs = bus3.receive()
    for msg in msgs:
        logger.test(f"RECEIVED: {msg}")
    logger.test("SENDING")
    bus3.send(dummy_msg)
    time.sleep(0.5)
