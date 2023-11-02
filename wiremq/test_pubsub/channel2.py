import logging
import time
import json
from wiremq.gateway.endpoints import channel


"""
Channel 2 is pre-subscribed to the pubsub channel on both topics with no
criteria; it receives all notifications.

When the pubsub channel starts publishing. channel 2 logs any notifications
received.
"""

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
    time.sleep(0.5)
