import json
import logging
import time
from wiremq.gateway.endpoints import endpointfactory

logger = logging.getLogger("bus1_logger")

with open("config.json", "r") as f:
    config = json.load(f)["bus1_config"]

dummy_msg = {
    "type": "event",
    "dest_ip": "127.0.0.1",
    "dest_port": 9002,
    "payload": {
        "from": "bus1",
        "hello": "world"
    }
}

bus1 = endpointfactory.EndpointFactory().build(config)
while True:
    msgs = bus1.receive()
    for msg in msgs:
        logger.test(f"SENDING: {msg}")
    logger.test("SENDING")
    bus1.send(dummy_msg)
    time.sleep(0.5)
