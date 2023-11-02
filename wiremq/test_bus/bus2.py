import json
import logging
import time
from wiremq.gateway.endpoints import messagebus

logger = logging.getLogger("bus2_logger")

with open("config.json", "r") as f:
    config = json.load(f)["bus2_config"]

bus = messagebus.MessageBus(config)

dummy_msg = {
    "type": "event",
    "dest_ip": "127.0.0.1",
    "dest_port": 9003,
    "payload": {
        "from": "bus2",
        "hello": "world"
    }
}

bus2 = bus.build()
while True:
    bus2.process()
    msgs = bus2.receive()
    for msg in msgs:
        logger.test(f"RECEIVED: {msg}")
    logger.test("SENDING")
    bus2.send(dummy_msg)
    time.sleep(0.5)
