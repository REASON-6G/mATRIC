import json
import logging
import time
from wiremq.gateway.endpoints import messagebus

logger = logging.getLogger("bus3_logger")

with open("config.json", "r") as f:
    config = json.load(f)["bus3_config"]

bus = messagebus.MessageBus(config)

dummy_msg = {
    "type": "event",
    "dest_ip": "127.0.0.1",
    "dest_port": 9001,
    "payload": {
        "from": "bus3",
        "hello": "world"
    }
}

bus3 = bus.build()
while True:
    bus3.process()
    msgs = bus3.receive()
    for msg in msgs:
        logger.test(f"RECEIVED: {msg}")
    logger.test("SENDING")
    bus3.send(dummy_msg)
    time.sleep(0.5)
