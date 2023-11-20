import logging
import time
import json
from wiremq.gateway.endpoints import channel

logger = logging.getLogger("in_channel_logger")

with open("config.json", "r") as f:
    config = json.load(f)["in_channel_config"]

ch = channel.Channel(config)
ch1 = ch.build()
logger.test(f"Listening on {config['host']}:{config['port']}")

while True:
    ch1.process()
    msgs = ch1.receive()
    for msg in msgs:
        logger.test(msg)
    time.sleep(0.05)
