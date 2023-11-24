import logging
import time
import json
from wiremq.gateway.endpoints import endpointfactory

logger = logging.getLogger("channel1_logger")

with open("config.json", "r") as f:
    config = json.load(f)["channel1_config"]

ch1 = endpointfactory.EndpointFactory().build(config)

while True:
    msgs = ch1.receive()
    for msg in msgs:
        logger.test(msg)
    time.sleep(0.5)
