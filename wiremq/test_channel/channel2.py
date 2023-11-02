import logging
import time
import json
from wiremq.gateway.endpoints import channel

logger = logging.getLogger("channel2_logger")

with open("config.json", "r") as f:
    config = json.load(f)["channel2_config"]

ch = channel.Channel(config)
ch2 = ch.build()
while True:
    ch2.process()
    msgs = ch2.receive()
    for msg in msgs:
        logger.test(msg)
    ch2.send({
        "type": "event",
        "payload": {
            "hello": "world"
        }

    })
    logger.test("SENDING MSG")
    time.sleep(0.5)
