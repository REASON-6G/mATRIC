import json
import logging
import time
from wiremq.gateway.endpoints import endpointfactory

logger = logging.getLogger("bus2_logger")

with open("config.json", "r") as f:
    config = json.load(f)["bus2_config"]

dummy_msg = {
    "type": "event",
    "dest_ip": "127.0.0.1",
    "dest_port": 9003,
    "payload": {
        "from": "bus2",
        "hello": "world"
    }
}

bus2 = endpointfactory.EndpointFactory().build(config)
while True:
    msgs = bus2.receive()
    for msg in msgs:
        logger.test(f"RECEIVED: {msg}")
    logger.test("SENDING")
    bus2.send(dummy_msg)
    time.sleep(0.5)
