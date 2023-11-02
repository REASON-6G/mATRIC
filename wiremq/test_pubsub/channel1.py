import logging
import time
import json
from wiremq.gateway.endpoints import channel

"""
Channel 1 subscribes to the pubsub channel by sending a subscription message.

It then logs any received notifications.
"""

logger = logging.getLogger("channel1_logger")

with open("config.json", "r") as f:
    config = json.load(f)["channel1_config"]

subscription_message = {
    "type": "command",
    "payload": {
        "command": 21,
        "params": {
            "alias": "channel1",
            "host": "127.0.0.1",
            "port": 8803,
            "topics": ["cpu"],
            "criteria": {
                "cpu": {
                    "cpu_percent": ("gt", 5.0)
                }
            }
        }
    }
}

ch = channel.Channel(config)

ch1 = ch.build()
ch1.send(subscription_message)
while True:
    ch1.process()
    msgs = ch1.receive()
    for msg in msgs:
        logger.test(msg)
    time.sleep(0.5)
