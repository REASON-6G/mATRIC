import logging
import time
import json
from wiremq.gateway.endpoints import channel

logger = logging.getLogger("channel1_logger")

with open("config.json", "r") as f:
    config = json.load(f)["channel1_config"]

ch = channel.Channel(config)

ch1 = ch.build()

print(ch1._config)
while True:
    ch1.process()
    msgs = ch1.receive()
    for msg in msgs:
        logger.test(msg)
    time.sleep(0.5)
